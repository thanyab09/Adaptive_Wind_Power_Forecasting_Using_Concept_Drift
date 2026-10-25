"""Prequential (test-then-train) baseline evaluation for Static, Adaptive, and Weekly models."""
import time
from typing import Dict, Any, Optional
import numpy as np
from scipy import stats
from ..config import (
    HOURS_PER_WEEK,
    RETRAINING_WINDOW_HOURS,
    COOLDOWN_HOURS,
    PREDICTION_BLOCK_HOURS,
    RATED_POWER_KW,
    PAGE_HINKLEY_DELTA_FACTOR,
    PAGE_HINKLEY_LAMBDA_FACTOR,
    KS_ALPHA,
    PSI_THRESHOLD,
)
from .forecaster import compute_metrics, predict_power
from .adaptation_controller import fit_recent_model
from .drift_detectors import PageHinkley, Cusum, AdwinDet, compute_psi


def run_static(model, X: np.ndarray, y: np.ndarray, i0: int) -> np.ndarray:
    """Static Baseline: Evaluated prequentially without any model updates."""
    preds = model.predict(X[i0:])
    return np.clip(preds, 0.0, RATED_POWER_KW)


def run_weekly(
    seed: int,
    X: np.ndarray,
    y: np.ndarray,
    i0: int,
    base_model,
    win: int = RETRAINING_WINDOW_HOURS,
) -> Tuple[np.ndarray, int, float]:
    """
    Weekly Baseline: Retrains blindly every 168 hours on the last 672 hours.
    No concept drift awareness or change-point downweighting.
    """
    n = len(y)
    pred = np.zeros(n - i0)
    model = base_model
    t_retrain = 0.0
    k = 0
    i = i0

    while i < n:
        j = min(i + HOURS_PER_WEEK, n)
        # Forecast for the upcoming week
        week_preds = model.predict(X[i:j])
        pred[i - i0 : j - i0] = np.clip(week_preds, 0.0, RATED_POWER_KW)

        # Retrain at week boundary
        t0 = time.perf_counter()
        m = fit_recent_model(seed, X, y, max(0, j - win), j)
        t_retrain += time.perf_counter() - t0
        model = m
        k += 1
        i = j

    return pred, k, t_retrain


def run_adaptive(
    seed: int,
    X: np.ndarray,
    y: np.ndarray,
    D: dict,
    i0: int,
    base_model,
    cal: dict,
    detector: str = "ph",
    use_input: bool = True,
    delta_f: float = PAGE_HINKLEY_DELTA_FACTOR,
    lam_f: float = PAGE_HINKLEY_LAMBDA_FACTOR,
    cooldown: int = COOLDOWN_HOURS,
    block: int = PREDICTION_BLOCK_HOURS,
    ks_alpha: float = KS_ALPHA,
    psi_thr: float = PSI_THRESHOLD,
    win: int = RETRAINING_WINDOW_HOURS,
    record: bool = False,
) -> dict:
    """
    Proposed Adaptive Framework:
      - Forecasts next power before receiving label (prequential).
      - Converts error into scale-free standardized error z_t using 6-quantile heteroscedasticity map.
      - Monitors z_t with Page-Hinkley test (or CUSUM / ADWIN).
      - Monitors wind speed distribution daily with KS test and PSI.
      - Retrains only upon confirmed drift and elapsed 48h cooldown.
      - Down-weights observations preceding estimated change point tau_hat.
    """
    n = len(y)
    pred = np.zeros(n - i0)
    model = base_model
    mu0, sigma0 = cal["mu0"], cal["s0"]
    zbuf = np.zeros(n - i0)

    # Initialize error detector
    if detector == "ph":
        det = PageHinkley(mu0, delta_f * sigma0, lam_f * sigma0)
    elif detector == "cusum":
        det = Cusum(mu0, sigma0)
    elif detector == "adwin":
        det = AdwinDet()
    else:
        det = None

    alarms, retrain_t = [], []
    sources = []
    t_retrain = 0.0
    t_detect = 0.0
    last_retrain = -10 ** 9
    trace = {"ph": [], "ks": [], "psi": [], "err": []} if record else None

    i = i0
    while i < n:
        j = min(i + block, n)
        # Block prediction
        P_raw = model.predict(X[i:j])
        P = np.clip(P_raw, 0.0, RATED_POWER_KW)

        fired = None
        for k in range(i, j):
            # Heteroscedastic standardization: z = |e| / m(y_hat)
            bin_idx = np.digitize(P[k - i], cal["edges"])
            bin_idx = min(bin_idx, len(cal["means"]) - 1)
            exp_err = max(cal["means"][bin_idx], 1.0)
            e = abs(P[k - i] - y[k]) / exp_err

            pred[k - i0] = P[k - i]
            zbuf[k - i0] = e

            td = time.perf_counter()
            hit = False
            src = None

            # 1. Error-based detector update
            if det is not None and detector != "kspsi":
                if det.update(e, k):
                    hit, src = True, detector

            if record:
                trace["err"].append(float(e))
                ph_val = float(det.statistic) if (det and detector == "ph") else 0.0
                trace["ph"].append(ph_val)

            # 2. Daily input-distribution monitor
            if (use_input or detector == "kspsi") and k % 24 == 23 and (k - i0) > 2 * HOURS_PER_WEEK:
                cur_v = D["v"][k - HOURS_PER_WEEK + 1 : k + 1]
                ref_v = D["v"][k - 5 * HOURS_PER_WEEK + 1 : k - HOURS_PER_WEEK + 1]
                ks_stat, ks_pval = stats.ks_2samp(ref_v, cur_v)
                pv = compute_psi(ref_v, cur_v)

                if record:
                    trace["ks"].append((k, float(ks_pval), float(ks_stat)))
                    trace["psi"].append((k, float(pv)))

                if ks_pval < ks_alpha and pv > psi_thr:
                    # Input drift requires error corroboration (24h mean z > mu0 + 2*sigma0)
                    recent_err = np.mean(zbuf[max(0, k - i0 - 23) : k - i0 + 1])
                    if detector == "kspsi" or recent_err > (mu0 + 2.0 * sigma0):
                        if not hit:
                            hit, src = True, "input"

            t_detect += time.perf_counter() - td

            # Check cooldown guard
            if hit and (k - last_retrain) >= cooldown:
                fired = (k, src)
                break
            elif hit:
                # Suppressed by cooldown; reset detector so it re-arms
                if det is not None and hasattr(det, "reset") and detector != "kspsi":
                    det.reset()

        if fired is None:
            i = j
            continue

        # Drift confirmed & authorized
        k, src = fired
        tau = getattr(det, "t_min", None)
        if tau is None or src == "input":
            tau = k - 24
        tau = max(tau - 12, 0)

        alarms.append(k)
        sources.append(src)

        # Retrain on recent 672h window
        t0 = time.perf_counter()
        lo = max(0, k + 1 - win)
        m = fit_recent_model(seed, X, y, lo, k + 1, tau=tau)
        t_retrain += time.perf_counter() - t0
        model = m
        retrain_t.append(k)
        last_retrain = k

        if det is not None and hasattr(det, "reset"):
            det.reset()

        # Re-compute predictions after hour k using updated model
        i = k + 1

    res = {
        "pred": pred,
        "alarms": alarms,
        "sources": sources,
        "n_retrain": len(retrain_t),
        "t_retrain": t_retrain,
        "t_detect": t_detect,
        "retrain_t": retrain_t,
    }
    if record:
        res["trace"] = trace
    return res
