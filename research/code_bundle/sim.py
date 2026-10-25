"""Adaptive wind-power forecasting with concept-drift detection - simulation engine."""
import time
import numpy as np
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor

RATED = 2000.0            # kW
HPW = 168                 # hours per week
TOTAL_WEEKS = 106
INIT_WEEKS = 26
DRIFT_WEEK = 28
WIN = 4 * HPW             # retraining window (672 h)
FEATS = ["v", "sin_d", "cos_d", "temp", "p_l1", "p_l2", "p_l24", "p_m6", "v_l1", "v_m3"]


def power_curve(v, temp, vin=3.0, vr=12.0, vout=25.0):
    rho = 101325.0 / (287.05 * (temp + 273.15))
    corr = rho / 1.225
    p = RATED * (v ** 3 - vin ** 3) / (vr ** 3 - vin ** 3) * corr
    p = np.where(v < vin, 0.0, p)
    p = np.minimum(p, RATED)
    p = np.where(v >= vout, 0.0, p)
    return np.maximum(p, 0.0)


def ar1(rng, n, phi):
    x = np.zeros(n)
    e = rng.standard_normal(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + np.sqrt(1 - phi ** 2) * e[i]
    return x


def generate(seed, drift=True, magnitude=1.0, n_weeks=TOTAL_WEEKS, drift_week=DRIFT_WEEK):
    """Hourly synthetic farm-level data. Returns dict of arrays."""
    rng = np.random.default_rng(seed)
    n = n_weeks * HPW
    t = np.arange(n)
    doy = (t / 24.0) % 365
    season = 1.0 * np.cos(2 * np.pi * (doy - 20) / 365)            # winter windier
    diurnal = 0.7 * np.sin(2 * np.pi * ((t % 24) - 14) / 24)
    v_true = 7.6 + 1.3 * season + diurnal + 2.7 * ar1(rng, n, 0.96)
    v_true = np.clip(v_true, 0.0, 30.0)
    temp = 17 + 9 * np.cos(2 * np.pi * (doy - 200) / 365) + 3 * np.sin(2 * np.pi * ((t % 24) - 15) / 24) \
        + 1.5 * ar1(rng, n, 0.97)
    d = 225 + 55 * ar1(rng, n, 0.97)
    d = d % 360
    p_true = power_curve(v_true, temp)
    v_meas = v_true + 0.15 * rng.standard_normal(n)
    d_meas = d + 4 * rng.standard_normal(n)
    onset = None
    if drift:
        onset = drift_week * HPW
        m = magnitude
        after = t >= onset
        # (1) real concept drift: rotor/ageing + wake of a new obstacle in SW sector
        deg = 1.0 - 0.075 * m
        sector = ((d > 200) & (d < 265)).astype(float)
        wake = 1.0 - 0.085 * m * sector
        p_true = np.where(after, p_true * deg * wake, p_true)
        # (2) anemometer recalibration (input / virtual drift)
        v_meas = np.where(after, v_meas * (1 + 0.04 * m), v_meas)
    p_obs = p_true * (1 + 0.008 * rng.standard_normal(n)) + 7.0 * rng.standard_normal(n)
    p_obs = np.clip(p_obs, 0.0, RATED)
    return dict(v=v_meas, v_true=v_true, d=d_meas, temp=temp, p=p_obs, p_clean=p_true, onset=onset, n=n)


def features(D):
    p, v = D["p"], D["v"]
    n = D["n"]
    rad = np.deg2rad(D["d"])
    X = np.zeros((n, len(FEATS)))
    X[:, 0] = v
    X[:, 1] = np.sin(rad)
    X[:, 2] = np.cos(rad)
    X[:, 3] = D["temp"]
    lag = lambda a, k: np.concatenate([np.full(k, a[0]), a[:-k]])
    X[:, 4] = lag(p, 1)
    X[:, 5] = lag(p, 2)
    X[:, 6] = lag(p, 24)
    cs = np.cumsum(np.insert(p, 0, 0))
    m6 = np.array([(cs[i] - cs[max(i - 6, 0)]) / max(min(i, 6), 1) for i in range(n)])
    X[:, 7] = m6
    X[:, 8] = lag(v, 1)
    csv = np.cumsum(np.insert(v, 0, 0))
    X[:, 9] = np.array([(csv[i] - csv[max(i - 3, 0)]) / max(min(i, 3), 1) for i in range(n)])
    return X


def new_model(seed):
    return HistGradientBoostingRegressor(max_iter=120, learning_rate=0.1, max_depth=6,
                                         min_samples_leaf=20, random_state=seed)


HALF_LIFE = 336.0
PRE_W = 0.08


def fit_recent(seed, X, y, lo, hi, half_life=None, tau=None):
    """Fit on rows lo..hi-1 with exponentially decaying recency weights."""
    hl = HALF_LIFE if half_life is None else half_life
    age = (hi - 1 - np.arange(lo, hi)).astype(float)
    w = 0.5 ** (age / hl)
    if tau is not None:   # drift-aware weighting: down-weight data before the estimated change point
        w = np.where(np.arange(lo, hi) < tau, w * PRE_W, w)
    m = new_model(seed)
    m.fit(X[lo:hi], y[lo:hi], sample_weight=w)
    return m


def psi(ref, cur, bins=10):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    r = np.histogram(ref, edges)[0] / len(ref)
    c = np.histogram(cur, edges)[0] / len(cur)
    r, c = np.clip(r, 1e-4, None), np.clip(c, 1e-4, None)
    return float(np.sum((c - r) * np.log(c / r)))


class PageHinkley:
    """Page-Hinkley test for an increase in mean, against a fixed reference level mu0."""
    def __init__(self, mu0, delta, lam):
        self.mu0, self.delta, self.lam = mu0, delta, lam
        self.reset()

    def reset(self):
        self.m = 0.0
        self.M = 0.0
        self.t_min = None
        self.k = 0

    def update(self, x, t):
        self.m += x - self.mu0 - self.delta
        if self.m < self.M:
            self.M = self.m
            self.t_min = t
        return (self.m - self.M) > self.lam


class Cusum:
    def __init__(self, mu0, sigma0, k=0.5, h=8.0):
        self.mu0, self.s0, self.k, self.h = mu0, sigma0, k, h
        self.g = 0.0

    def reset(self):
        self.g = 0.0

    def update(self, x, t):
        z = (x - self.mu0) / self.s0
        self.g = max(0.0, self.g + z - self.k)
        return self.g > self.h


class AdwinDet:
    def __init__(self, delta=0.002):
        from river.drift import ADWIN
        self.delta = delta
        self.a = ADWIN(delta=delta)
        self.prev = None

    def reset(self):
        from river.drift import ADWIN
        self.a = ADWIN(delta=self.delta)

    def update(self, x, t):
        before = self.a.estimation
        self.a.update(x)
        return bool(self.a.drift_detected and self.a.estimation > before)


def run_static(model, X, y, i0):
    pred = model.predict(X[i0:])
    return pred


def run_weekly(seed, X, y, i0, base_model):
    """Blind weekly retraining on the last WIN hours."""
    n = len(y)
    pred = np.zeros(n - i0)
    model = base_model
    t_retrain = 0.0
    k = 0
    i = i0
    while i < n:
        j = min(i + HPW, n)
        pred[i - i0:j - i0] = model.predict(X[i:j])
        t0 = time.perf_counter()
        m = fit_recent(seed, X, y, max(0, j - WIN), j)
        t_retrain += time.perf_counter() - t0
        model = m
        k += 1
        i = j
    return pred, k, t_retrain


def run_adaptive(seed, X, y, D, i0, base_model, cal, detector="ph", use_input=True,
                 delta_f=0.6, lam_f=15.0, cooldown=48, block=24, ks_alpha=1e-6, psi_thr=0.25,
                 win=WIN, record=False):
    """Drift-triggered retraining (test-then-train) on a sliding recent window."""
    n = len(y)
    pred = np.zeros(n - i0)
    model = base_model
    mu0, sigma0 = cal['mu0'], cal['s0']
    zbuf = np.zeros(n - i0)
    if detector == "ph":
        det = PageHinkley(mu0, delta_f * sigma0, lam_f * sigma0)
    elif detector == "cusum":
        det = Cusum(mu0, sigma0)
    elif detector == "adwin":
        det = AdwinDet()
    elif detector in ("none", "kspsi"):
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
        P = model.predict(X[i:j])
        fired = None
        for k in range(i, j):
            e = abs(P[k - i] - y[k]) / cal['means'][np.digitize(P[k - i], cal['edges'])]
            pred[k - i0] = P[k - i]
            zbuf[k - i0] = e
            td = time.perf_counter()
            hit = False
            src = None
            if det is not None and detector != "kspsi":
                if det.update(e, k):
                    hit, src = True, detector
            if record:
                trace["err"].append(e)
                trace["ph"].append(getattr(det, "m", 0.0) - getattr(det, "M", 0.0) if detector == "ph" else 0.0)
            # input monitoring once a day
            if (use_input or detector == "kspsi") and k % 24 == 23 and k - i0 > 2 * HPW:
                cur = D["v"][k - HPW + 1:k + 1]
                ref = D["v"][k - HPW - 4 * HPW + 1:k - HPW + 1]
                ks = stats.ks_2samp(ref, cur)
                pv = psi(ref, cur)
                # direction consistency as extra input
                if record:
                    trace["ks"].append((k, ks.pvalue, ks.statistic))
                    trace["psi"].append((k, pv))
                if (ks.pvalue < ks_alpha and pv > psi_thr):
                    # input shift is only an alarm when accompanied by degraded accuracy
                    recent = np.mean(zbuf[max(0, k - i0 - 23):k - i0 + 1])
                    if detector == "kspsi" or recent > mu0 + 2 * sigma0:
                        if not hit:
                            hit, src = True, "input"
            t_detect += time.perf_counter() - td
            if hit and (k - last_retrain) >= cooldown:
                fired = (k, src)
                break
            elif hit:
                if det is not None and hasattr(det, "reset") and detector != "kspsi":
                    det.reset()
        if fired is None:
            i = j
            continue
        k, src = fired
        tau = getattr(det, "t_min", None)
        if tau is None or src == "input":
            tau = k - 24
        tau = max(tau - 12, 0)
        alarms.append(k)
        sources.append(src)
        t0 = time.perf_counter()
        lo = max(0, k + 1 - win)
        m = fit_recent(seed, X, y, lo, k + 1, tau=tau)
        t_retrain += time.perf_counter() - t0
        model = m
        retrain_t.append(k)
        last_retrain = k
        if det is not None and hasattr(det, "reset"):
            det.reset()
        # prediction for hours after k within this block are re-done with new model
        i = k + 1
    res = dict(pred=pred, alarms=alarms, sources=sources, n_retrain=len(retrain_t),
               t_retrain=t_retrain, t_detect=t_detect, retrain_t=retrain_t)
    if record:
        res["trace"] = trace
    return res


def metrics(y, p):
    e = p - y
    mae = float(np.mean(np.abs(e)))
    rmse = float(np.sqrt(np.mean(e ** 2)))
    return mae, rmse, rmse / RATED * 100


def calibrate(model_seed, X, y, i0):
    """Rolling-origin validation inside the initial window (origins at weeks 10, 14, 18, 22): models trained
    like a drift-triggered retrain forecast the next 4 weeks. The pooled residuals give a heteroscedasticity
    map (mean absolute error per forecast-level bin) so that monitored errors are standardised:
    z = |e| / m(pred). Returns the initial model and the calibration dict."""
    P, E = [], []
    for wk in (10, 14, 18, 22):
        cut = wk * HPW
        m = fit_recent(model_seed, X, y, max(0, cut - WIN), cut)
        p = m.predict(X[cut:cut + 4 * HPW])
        P.append(p)
        E.append(np.abs(p - y[cut:cut + 4 * HPW]))
    P, E = np.concatenate(P), np.concatenate(E)
    edges = np.quantile(P, np.linspace(0, 1, 7))[1:-1]
    b = np.digitize(P, edges)
    means = np.array([max(E[b == k].mean(), 1.0) for k in range(6)])
    z = E / means[b]
    final = new_model(model_seed)
    final.fit(X[:i0], y[:i0])
    return final, dict(edges=edges, means=means, mu0=float(z.mean()), s0=float(z.std()))


def experiment(seed, drift=True, magnitude=1.0, record=False, detector="ph", do_weekly=True, **kw):
    D = generate(seed, drift=drift, magnitude=magnitude)
    X = features(D)
    y = D["p"]
    i0 = INIT_WEEKS * HPW
    base, cal = calibrate(seed, X, y, i0)
    yt = y[i0:]
    out = {"D": D, "mu0": cal['mu0'], "s0": cal['s0'], "cal": cal, "i0": i0}
    out["static"] = dict(pred=run_static(base, X, y, i0))
    if do_weekly:
        wp, wk, wt = run_weekly(seed, X, y, i0, base)
    else:
        wp, wk, wt = out["static"]["pred"], 0, 0.0
    out["weekly"] = dict(pred=wp, n_retrain=wk, t_retrain=wt)
    ad = run_adaptive(seed, X, y, D, i0, base, cal, detector=detector, record=record, **kw)
    out["adaptive"] = ad
    out["y"] = yt
    out["X"] = X
    out["base"] = base
    for k in ("static", "weekly", "adaptive"):
        out[k]["metrics"] = metrics(yt, out[k]["pred"])
    if drift:
        onset = D["onset"]
        first = [a for a in ad["alarms"] if a >= onset]
        out["delay"] = (first[0] - onset) if first else None
        out["false_alarms"] = len([a for a in ad["alarms"] if a < onset])
    else:
        out["delay"] = None
        out["false_alarms"] = len(ad["alarms"])
    return out
