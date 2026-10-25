"""Concept drift detection algorithms and error stream calibration."""
from typing import Dict, Any, Tuple, Optional
import numpy as np
from scipy import stats
from ..config import (
    PAGE_HINKLEY_DELTA_FACTOR,
    PAGE_HINKLEY_LAMBDA_FACTOR,
    KS_ALPHA,
    PSI_THRESHOLD,
    ERROR_CORROBORATION_SIGMA,
    RATED_POWER_KW,
)


class PageHinkley:
    """
    Page-Hinkley test for detecting upward shifts in mean of the standardized error stream.
    Gives a natural estimate of the change point tau_hat.
    """
    def __init__(self, mu0: float, delta: float, lam: float):
        self.mu0 = float(mu0)
        self.delta = float(delta)
        self.lam = float(lam)
        self.reset()

    def reset(self):
        self.m = 0.0
        self.M = 0.0
        self.t_min = None
        self.k = 0

    def update(self, x: float, t: int) -> bool:
        self.k += 1
        self.m += x - self.mu0 - self.delta
        if self.m < self.M:
            self.M = self.m
            self.t_min = t
        return (self.m - self.M) > self.lam

    @property
    def statistic(self) -> float:
        return float(self.m - self.M)


class Cusum:
    """One-sided Cumulative Sum (CUSUM) control chart on standardized deviations."""
    def __init__(self, mu0: float, sigma0: float, k: float = 0.5, h: float = 8.0):
        self.mu0 = float(mu0)
        self.s0 = float(sigma0)
        self.k = float(k)
        self.h = float(h)
        self.reset()

    def reset(self):
        self.g = 0.0

    def update(self, x: float, t: int) -> bool:
        z = (x - self.mu0) / max(self.s0, 1e-6)
        self.g = max(0.0, self.g + z - self.k)
        return self.g > self.h

    @property
    def statistic(self) -> float:
        return float(self.g)


class AdwinDet:
    """Adaptive Windowing (ADWIN) detector wrapper from River."""
    def __init__(self, delta: float = 0.002):
        from river.drift import ADWIN
        self.delta = delta
        self.a = ADWIN(delta=delta)
        self.prev = None

    def reset(self):
        from river.drift import ADWIN
        self.a = ADWIN(delta=self.delta)

    def update(self, x: float, t: int) -> bool:
        before = self.a.estimation
        self.a.update(x)
        return bool(self.a.drift_detected and self.a.estimation > before)

    @property
    def statistic(self) -> float:
        return float(self.a.estimation if hasattr(self.a, "estimation") else 0.0)


def compute_psi(ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
    """
    Computes Population Stability Index (PSI) between reference and current feature distributions.
    PSI < 0.1: negligible shift
    0.1 <= PSI <= 0.25: moderate shift
    PSI > 0.25: significant shift
    """
    if len(ref) == 0 or len(cur) == 0:
        return 0.0
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref)
    c = np.histogram(cur, edges)[0] / len(cur)
    r = np.clip(r, 1e-4, None)
    c = np.clip(c, 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))


def compute_ks_test(ref: np.ndarray, cur: np.ndarray) -> Tuple[float, float]:
    """Computes Kolmogorov-Smirnov 2-sample test statistic and p-value."""
    if len(ref) == 0 or len(cur) == 0:
        return 0.0, 1.0
    res = stats.ks_2samp(ref, cur)
    return float(res.statistic), float(res.pvalue)


def calibrate_error_bins(
    X: np.ndarray,
    y: np.ndarray,
    seed: int,
    initial_hours: int,
    retrain_win: int,
    fit_func,
) -> Tuple[Any, Dict[str, Any]]:
    """
    Rolling-origin cross-validation on initial window (weeks 10, 14, 18, 22).
    Generates 6-quantile error bins so that residuals are standardized by forecast power level:
      z_t = |y_t - y_hat_t| / m(y_hat_t)
    Returns:
      base_model, calibration_dict (edges, means, mu0, s0)
    """
    P_list, E_list = [], []
    hpw = 168

    for wk in (10, 14, 18, 22):
        cut = wk * hpw
        m = fit_func(seed, X, y, max(0, cut - retrain_win), cut)
        p_val = m.predict(X[cut : cut + 4 * hpw])
        p_val = np.clip(p_val, 0.0, RATED_POWER_KW)
        y_val = y[cut : cut + 4 * hpw]
        P_list.append(p_val)
        E_list.append(np.abs(p_val - y_val))

    P = np.concatenate(P_list)
    E = np.concatenate(E_list)

    # 6 quantile bins over forecast levels
    edges = np.quantile(P, np.linspace(0, 1, 7))[1:-1]
    b = np.digitize(P, edges)
    means = np.array([max(E[b == k].mean(), 1.0) for k in range(6)])
    z = E / means[b]

    # Train base model on full initial window
    from .forecaster import build_forecaster
    base_model = build_forecaster(seed)
    base_model.fit(X[:initial_hours], y[:initial_hours])

    cal_dict = {
        "edges": edges.tolist(),
        "means": means.tolist(),
        "mu0": float(z.mean()),
        "s0": float(z.std()),
    }
    return base_model, cal_dict


def standardize_residual(pred_power: float, actual_power: float, cal: Dict[str, Any]) -> float:
    """Converts raw prediction error into scale-independent score z."""
    edges = np.asarray(cal["edges"])
    means = np.asarray(cal["means"])
    bin_idx = int(np.digitize(pred_power, edges))
    expected_error = float(means[min(bin_idx, len(means) - 1)])
    return float(abs(pred_power - actual_power) / max(expected_error, 1.0))
