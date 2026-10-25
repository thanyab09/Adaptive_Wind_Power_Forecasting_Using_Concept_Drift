import pickle, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.inspection import permutation_importance
from figs_static import save, NAVY, TEAL, AMBER, RED, GREY, GREEN, PURPLE
import sim
from sim import HPW, RATED, INIT_WEEKS, DRIFT_WEEK, FEATS

main = pickle.load(open("main.pkl", "rb"))
R = json.load(open("results.json"))
A = main[(True, 0)]["arrays"]
N = main[(False, 0)]["arrays"]
i0 = A["i0"]
COL = {"static": RED, "adaptive": NAVY, "weekly": GREEN}
LAB = {"static": "Static", "adaptive": "Adaptive (drift-triggered)", "weekly": "Weekly retrain"}


def wk_axis(n):
    return INIT_WEEKS + np.arange(n) / HPW


# ------------------------------------------------------------------ data overview
def f_data_overview():
    D = sim.generate(0, drift=False)
    s, e = 0, 3 * HPW
    t = np.arange(s, e) / 24
    fig, axs = plt.subplots(4, 1, figsize=(8.4, 7.2), sharex=True)
    axs[0].plot(t, D["v"][s:e], color=NAVY, lw=1); axs[0].set_ylabel("Wind speed\n(m/s)")
    axs[1].plot(t, D["d"][s:e], color=TEAL, lw=1); axs[1].set_ylabel("Direction\n(deg)")
    axs[2].plot(t, D["temp"][s:e], color=AMBER, lw=1); axs[2].set_ylabel("Temperature\n(°C)")
    axs[3].plot(t, D["p"][s:e], color=RED, lw=1); axs[3].set_ylabel("Power\n(kW)")
    axs[3].set_xlabel("Day")
    axs[0].set_title("First three weeks of the synthetic hourly stream (seed 0)", fontweight="bold")
    fig.tight_layout(); save(fig, "d_overview.png")


def f_weekly_profile():
    D = sim.generate(0, drift=True)
    wk = np.arange(sim.TOTAL_WEEKS)
    v = D["v"][:len(wk) * HPW].reshape(-1, HPW).mean(1); p = D["p"].reshape(-1, HPW).mean(1)
    fig, axs = plt.subplots(2, 1, figsize=(8.4, 5.4), sharex=True)
    for ax, y, lab, c in ((axs[0], v, "Mean wind speed (m/s)", NAVY), (axs[1], p, "Mean power (kW)", RED)):
        ax.plot(wk, y, color=c, lw=1.6); ax.set_ylabel(lab)
        ax.axvspan(0, INIT_WEEKS, color="#cfe0f3", alpha=.5); ax.axvline(DRIFT_WEEK, color="k", ls="--", lw=1.4)
    axs[0].text(DRIFT_WEEK + .6, v.max() * .98, "drift onset (week 28)", fontsize=8.5)
    axs[0].text(1, v.max() * .98, "initial window", fontsize=8.5)
    axs[1].set_xlabel("Week")
    axs[0].set_title("Weekly mean profiles with seasonality and injected drift", fontweight="bold")
    fig.tight_layout(); save(fig, "d_weekly.png")


def f_power_scatter():
    D = sim.generate(0, drift=True)
    on = DRIFT_WEEK * HPW
    pre = slice(0, on); post = slice(on + 24, on + 24 + 20 * HPW)
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.0), sharey=True, sharex=True)
    for ax, sl, c, t in ((axs[0], pre, NAVY, "(a) Before drift (weeks 0-28)"), (axs[1], post, RED, "(b) After drift (weeks 28-48)")):
        ax.scatter(D["v"][sl], D["p"][sl], s=3, alpha=.35, color=c)
        vv = np.linspace(0, 25, 200); ax.plot(vv, sim.power_curve(vv, 17.0), color="k", lw=1.4, label="nominal curve (17 °C)")
        ax.set_title(t, fontsize=10, fontweight="bold"); ax.set_xlabel("Measured wind speed (m/s)"); ax.legend(fontsize=8, loc="upper left")
    axs[0].set_ylabel("Power (kW)")
    fig.tight_layout(); save(fig, "d_power_scatter.png")


def f_speed_hist():
    D = sim.generate(0, drift=True)
    ref = D["v"][:INIT_WEEKS * HPW]; cur = D["v"][(DRIFT_WEEK + 1) * HPW:(DRIFT_WEEK + 9) * HPW]
    nd = sim.generate(0, drift=False)["v"][(DRIFT_WEEK + 1) * HPW:(DRIFT_WEEK + 9) * HPW]
    ks1 = stats.ks_2samp(ref, cur); ks0 = stats.ks_2samp(ref, nd)
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.8), sharey=True)
    for ax, c, lab, ks in ((axs[0], cur, "with sensor drift", ks1), (axs[1], nd, "no drift", ks0)):
        ax.hist(ref, bins=30, density=True, alpha=.55, color=NAVY, label="Initial window")
        ax.hist(c, bins=30, density=True, alpha=.55, color=AMBER, label=f"Weeks 29-36 ({lab})")
        ax.set_xlabel("Measured wind speed (m/s)"); ax.legend(fontsize=8)
        ax.set_title(f"KS D = {ks.statistic:.3f}, p = {ks.pvalue:.1e}", fontsize=10, fontweight="bold")
    axs[0].set_ylabel("Density")
    fig.tight_layout(); save(fig, "d_speed_hist.png")
    return ks1, ks0


def f_rose():
    D = sim.generate(0, drift=True)
    d = np.deg2rad(D["d"] % 360)
    fig = plt.figure(figsize=(5.2, 5.0)); ax = fig.add_subplot(111, projection="polar")
    bins = np.linspace(0, 2 * np.pi, 37)
    h, _ = np.histogram(d, bins)
    cen = (bins[:-1] + bins[1:]) / 2
    colors = [RED if 200 <= np.rad2deg(c) <= 265 else NAVY for c in cen]
    ax.bar(cen, h / h.sum() * 100, width=2 * np.pi / 36, color=colors, alpha=.85, edgecolor="white")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    ax.set_title("Wind-direction rose (% of hours)\nred = wake-affected sector 200°-265°", fontsize=10, fontweight="bold", pad=14)
    save(fig, "d_rose.png")


def f_corr_importance():
    D = sim.generate(0, drift=False)
    X = sim.features(D); y = D["p"]
    names = ["wind speed", "sin(dir)", "cos(dir)", "temp", "P(t-1)", "P(t-2)", "P(t-24)", "mean P(6h)", "v(t-1)", "mean v(3h)"]
    M = np.column_stack([X, y]); C = np.corrcoef(M[:INIT_WEEKS * HPW].T)
    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    im = ax.imshow(C, cmap="RdBu_r", vmin=-1, vmax=1)
    labs = names + ["power(t)"]
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(len(labs))); ax.set_yticklabels(labs, fontsize=8); ax.grid(False)
    for i in range(len(labs)):
        for j in range(len(labs)):
            ax.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center", fontsize=6.5, color="white" if abs(C[i, j]) > .6 else "black")
    fig.colorbar(im, ax=ax, fraction=0.046); ax.set_title("Pearson correlation matrix (initial window)", fontweight="bold")
    fig.tight_layout(); save(fig, "d_corr.png")
    i0_ = INIT_WEEKS * HPW
    m = sim.new_model(0); m.fit(X[:i0_], y[:i0_])
    pi = permutation_importance(m, X[i0_:i0_ + 8 * HPW], y[i0_:i0_ + 8 * HPW], n_repeats=6, random_state=0,
                                scoring="neg_mean_absolute_error")
    imp = pi.importances_mean; order = np.argsort(imp)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.barh(np.array(names)[order], imp[order], xerr=pi.importances_std[order], color=TEAL)
    ax.set_xlabel("Increase in MAE when feature is permuted (kW)"); ax.set_title("Permutation feature importance of the base model", fontweight="bold")
    fig.tight_layout(); save(fig, "d_importance.png")
    return dict(zip(names, imp.tolist()))


def f_calibration():
    cal = A["cal"]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    edges = np.concatenate([[0], cal["edges"], [RATED]])
    cen = (edges[:-1] + edges[1:]) / 2
    ax.bar(range(6), cal["means"], color=TEAL)
    ax.set_xticks(range(6)); ax.set_xticklabels([f"{edges[i]:.0f}-{edges[i+1]:.0f}" for i in range(6)], fontsize=8)
    for i, v in enumerate(cal["means"]):
        ax.text(i, v + .3, f"{v:.1f}", ha="center", fontsize=8.5)
    ax.set_xlabel("Forecast-level bin (kW)"); ax.set_ylabel("Mean absolute error (kW)")
    ax.set_title("Heteroscedasticity map used to standardise residuals (seed 0)", fontweight="bold")
    fig.tight_layout(); save(fig, "d_calibration.png")


# ------------------------------------------------------------------ rolling error
def weekly_mae(arr, y):
    n = len(y) // HPW
    return np.abs(arr[:n * HPW] - y[:n * HPW]).reshape(n, HPW).mean(1)


def f_rolling(arrs, key, fname, title, onset=True, alarms=None):
    y = arrs["y"]
    wks = INIT_WEEKS + np.arange(len(y) // HPW) + .5
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    for m, p in (("static", "p_static"), ("weekly", "p_weekly"), ("adaptive", "p_adapt")):
        ax.plot(wks, weekly_mae(arrs[p], y), color=COL[m], lw=1.8, label=LAB[m])
    if onset:
        ax.axvline(DRIFT_WEEK, color="k", ls="--", lw=1.3); ax.text(DRIFT_WEEK + .7, ax.get_ylim()[1] * .9, "drift onset", fontsize=8.5)
    if alarms is not None:
        for a in alarms:
            ax.axvline(a / HPW, color=AMBER, lw=.8, alpha=.8)
        ax.plot([], [], color=AMBER, lw=1, label="Retraining events")
    ax.set_xlabel("Week"); ax.set_ylabel("Weekly MAE (kW)"); ax.legend(fontsize=8.5); ax.set_title(title, fontweight="bold")
    fig.tight_layout(); save(fig, fname)


def f_cum():
    y = A["y"]
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    t = INIT_WEEKS + np.arange(len(y)) / HPW
    for m, p in (("static", "p_static"), ("weekly", "p_weekly"), ("adaptive", "p_adapt")):
        ax.plot(t, np.cumsum(np.abs(A[p] - y)) / 1000, color=COL[m], lw=1.8, label=LAB[m])
    ax.axvline(DRIFT_WEEK, color="k", ls="--", lw=1.2)
    ax.set_xlabel("Week"); ax.set_ylabel("Cumulative absolute error (MWh)"); ax.legend(fontsize=8.5)
    ax.set_title("Cumulative absolute forecast error (drift scenario)", fontweight="bold")
    fig.tight_layout(); save(fig, "d_cum.png")


def f_ph_trace():
    tr = A["trace"]; ph = np.array(tr["ph"]); z = np.array(tr["err"])
    t = INIT_WEEKS + np.arange(len(ph)) / HPW
    lam = 15.0 * A["cal"]["s0"]
    fig, axs = plt.subplots(2, 1, figsize=(8.6, 5.4), sharex=True)
    axs[0].plot(t, z, color=GREY, lw=.4, alpha=.8); axs[0].plot(t, np.convolve(z, np.ones(24) / 24, mode="same"), color=NAVY, lw=1.2, label="24 h moving mean of z")
    axs[0].axvline(DRIFT_WEEK, color="k", ls="--", lw=1.2); axs[0].set_ylabel("Standardised error z"); axs[0].legend(fontsize=8); axs[0].set_ylim(0, 8)
    axs[1].plot(t, ph, color=TEAL, lw=1.0); axs[1].axhline(lam, color=AMBER, ls="--", label=f"threshold λ = 15σ₀ = {lam:.1f}")
    for a in A["alarms"]:
        axs[1].plot(a / HPW, lam, "v", color=RED, ms=6)
    axs[1].plot([], [], "v", color=RED, label="alarm / retrain"); axs[1].axvline(DRIFT_WEEK, color="k", ls="--", lw=1.2)
    axs[1].set_xlabel("Week"); axs[1].set_ylabel("PH statistic mₜ − Mₜ"); axs[1].legend(fontsize=8, loc="upper right")
    axs[0].set_title("Page-Hinkley monitoring of the standardised error stream", fontweight="bold")
    fig.tight_layout(); save(fig, "d_ph_trace.png")


def f_input_monitor():
    ks = np.array(A["trace"]["ks"]); ps = np.array(A["trace"]["psi"])
    fig, axs = plt.subplots(2, 1, figsize=(8.6, 5.0), sharex=True)
    t = ks[:, 0] / HPW
    axs[0].semilogy(t, np.clip(ks[:, 1], 1e-30, 1), color=NAVY, lw=1.2); axs[0].axhline(1e-6, color=AMBER, ls="--", label="α = 10⁻⁶")
    axs[0].axvline(DRIFT_WEEK, color="k", ls="--"); axs[0].set_ylabel("KS p-value (log)"); axs[0].legend(fontsize=8)
    axs[1].plot(ps[:, 0] / HPW, ps[:, 1], color=TEAL, lw=1.2); axs[1].axhline(0.25, color=AMBER, ls="--", label="PSI = 0.25 (major shift)")
    axs[1].axvline(DRIFT_WEEK, color="k", ls="--"); axs[1].set_ylabel("PSI"); axs[1].set_xlabel("Week"); axs[1].legend(fontsize=8)
    axs[0].set_title("Daily input-distribution monitors on wind speed", fontweight="bold")
    fig.tight_layout(); save(fig, "d_input_monitor.png")
    return ks, ps


def f_zoom():
    y = A["y"]; on = A["onset"] - i0
    s, e = on - 48, on + 7 * 24
    t = np.arange(s, e) / 24
    fig, ax = plt.subplots(figsize=(8.8, 4.2))
    ax.plot(t, y[s:e], color="k", lw=1.3, label="Actual")
    ax.plot(t, A["p_static"][s:e], color=RED, lw=1.1, label="Static")
    ax.plot(t, A["p_adapt"][s:e], color=NAVY, lw=1.1, label="Adaptive")
    ax.axvline(on / 24, color="k", ls="--"); ax.text(on / 24 + .05, 2050, "drift onset", fontsize=8.5)
    for a in A["alarms"]:
        if s <= a - i0 < e:
            ax.axvline((a - i0) / 24, color=AMBER, lw=1, ls=":")
    ax.set_xlabel("Day of stream"); ax.set_ylabel("Power (kW)"); ax.legend(fontsize=8.5, ncol=3, loc="lower left"); ax.set_ylim(0, 2200)
    ax.set_title("Forecasts around the drift onset (dotted amber = retraining events)", fontweight="bold")
    fig.tight_layout(); save(fig, "d_zoom.png")


def f_bars():
    fig, axs = plt.subplots(2, 2, figsize=(8.8, 6.2))
    for r, (key, nm) in enumerate((("drift", "Drift scenario"), ("nodrift", "No-drift scenario"))):
        for c, (met, lab) in enumerate((("mae", "MAE (kW)"), ("rmse", "RMSE (kW)"))):
            ax = axs[r, c]
            vals = [R[key][m][met][0] for m in ("static", "adaptive", "weekly")]
            err = [R[key][m][met][1] for m in ("static", "adaptive", "weekly")]
            b = ax.bar(["Static", "Adaptive", "Weekly"], vals, yerr=err, capsize=4, color=[RED, NAVY, GREEN])
            for bb, v in zip(b, vals):
                ax.text(bb.get_x() + bb.get_width() / 2, v + max(err) + max(vals) * .02, f"{v:.1f}", ha="center", fontsize=9)
            ax.set_ylabel(lab); ax.set_title(f"{nm}: {lab.split()[0]}", fontsize=10, fontweight="bold"); ax.set_ylim(0, max(vals) * 1.25)
    fig.tight_layout(); save(fig, "d_bars.png")


def f_retrain_cost():
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.8))
    for ax, met, lab in ((axs[0], "retrains", "Number of retrainings"), (axs[1], "t_retrain", "Cumulative retraining time (s)")):
        x = np.arange(2); w = .26
        for k, m in enumerate(("static", "adaptive", "weekly")):
            vals = [R["drift"][m][met][0], R["nodrift"][m][met][0]]
            b = ax.bar(x + (k - 1) * w, vals, w, color=COL[m], label=LAB[m])
            for bb, v in zip(b, vals):
                ax.text(bb.get_x() + bb.get_width() / 2, v + max(R["drift"]["weekly"][met][0], 1) * .02, f"{v:.1f}" if met == "t_retrain" else f"{v:.0f}", ha="center", fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels(["Drift", "No drift"]); ax.set_ylabel(lab)
    axs[0].legend(fontsize=7.5, loc="upper left")
    fig.tight_layout(); save(fig, "d_retrain_cost.png")


def f_delay():
    d = [x if x is not None else 0 for x in R["delays"]]
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    ax.bar(range(1, 11), d, color=TEAL)
    ax.axhline(R["delay_mean"], color=RED, ls="--", label=f"mean = {R['delay_mean']:.1f} h")
    for i, v in enumerate(d):
        ax.text(i + 1, v + 1, f"{v}", ha="center", fontsize=8.5)
    ax.set_xlabel("Random seed"); ax.set_ylabel("Detection delay (hours)"); ax.set_xticks(range(1, 11)); ax.set_xticklabels(range(10))
    ax.legend(fontsize=9); ax.set_title("First-alarm detection delay per seed", fontweight="bold")
    fig.tight_layout(); save(fig, "d_delay.png")


def f_scatter_pred():
    y = A["y"]; on = A["onset"] - i0
    sl = slice(on + 14 * 24, on + 14 * 24 + 20 * HPW)
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 4.2), sharex=True, sharey=True)
    for ax, p, c, t in ((axs[0], "p_static", RED, "(a) Static"), (axs[1], "p_adapt", NAVY, "(b) Adaptive")):
        ax.scatter(y[sl], A[p][sl], s=3, alpha=.3, color=c); ax.plot([0, 2000], [0, 2000], "k--", lw=1)
        r2 = 1 - np.sum((y[sl] - A[p][sl]) ** 2) / np.sum((y[sl] - y[sl].mean()) ** 2)
        ax.set_title(f"{t}   R² = {r2:.3f}", fontsize=10, fontweight="bold"); ax.set_xlabel("Actual power (kW)")
    axs[0].set_ylabel("Predicted power (kW)")
    fig.tight_layout(); save(fig, "d_scatter_pred.png")


def f_resid():
    y = A["y"]; on = A["onset"] - i0
    sl = slice(on + 14 * 24, None)
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    for m, p in (("static", "p_static"), ("weekly", "p_weekly"), ("adaptive", "p_adapt")):
        ax.hist((A[p] - y)[sl], bins=np.linspace(-500, 500, 81), alpha=.5, color=COL[m], label=f"{LAB[m]} (σ = {np.std((A[p]-y)[sl]):.0f} kW)")
    ax.set_xlabel("Residual (kW)"); ax.set_ylabel("Frequency"); ax.legend(fontsize=8.5)
    ax.set_title("Residual distribution after the drift transient", fontweight="bold")
    fig.tight_layout(); save(fig, "d_resid.png")


def f_timeline():
    fig, axs = plt.subplots(2, 1, figsize=(8.6, 5.0), sharex=True)
    for ax, drift, nm in ((axs[0], True, "Drift scenario"), (axs[1], False, "No-drift scenario")):
        for s in range(10):
            ts = np.array(main[(drift, s)]["adaptive"]["retrain_t"]) / HPW
            ax.plot(ts, np.full_like(ts, s), "o", ms=4, color=NAVY if drift else GREY)
        ax.set_ylabel("Seed"); ax.set_yticks(range(10)); ax.set_title(nm, fontsize=10, fontweight="bold")
        if drift:
            ax.axvline(DRIFT_WEEK, color=RED, ls="--"); ax.text(DRIFT_WEEK + .3, 9.2, "onset", color=RED, fontsize=8.5)
        else:
            ax.text(60, 4.5, "no retraining events in any seed", ha="center", fontsize=10, color=GREY)
        ax.set_xlim(INIT_WEEKS, sim.TOTAL_WEEKS); ax.set_ylim(-.7, 10)
    axs[1].set_xlabel("Week")
    fig.tight_layout(); save(fig, "d_timeline.png")


def f_err_by_speed():
    y = A["y"]; v = A["v"][i0:]; on = A["onset"] - i0
    bins = np.arange(0, 21, 2)
    idx = np.digitize(v, bins)
    pre = np.arange(len(y)) < on; post = np.arange(len(y)) >= on + 14 * 24
    res = {}
    for nm, p, mask in (("Static, before drift", "p_static", pre), ("Static, after drift", "p_static", post), ("Adaptive, after drift", "p_adapt", post)):
        e = np.abs(A[p] - y)
        res[nm] = [e[mask & (idx == k)].mean() if (mask & (idx == k)).sum() > 10 else np.nan for k in range(1, len(bins))]
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    w = .27; x = np.arange(len(bins) - 1)
    for k, (nm, c) in enumerate(zip(res, (GREY, RED, NAVY))):
        ax.bar(x + (k - 1) * w, res[nm], w, color=c, label=nm)
    ax.set_xticks(x); ax.set_xticklabels([f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)], fontsize=8)
    ax.set_xlabel("Measured wind-speed bin (m/s)"); ax.set_ylabel("MAE (kW)"); ax.legend(fontsize=8.5)
    ax.set_title("Where the error comes from: MAE by wind-speed bin", fontweight="bold")
    fig.tight_layout(); save(fig, "d_err_speed.png")
    return res


def f_box():
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.8))
    for ax, key, t in ((axs[0], "drift", "Drift scenario"), (axs[1], "nodrift", "No-drift scenario")):
        data = [R[key][m]["mae_seeds"] for m in ("static", "adaptive", "weekly")]
        bp = ax.boxplot(data, patch_artist=True, widths=.55, tick_labels=["Static", "Adaptive", "Weekly"])
        for patch, c in zip(bp["boxes"], (RED, NAVY, GREEN)):
            patch.set_facecolor(c); patch.set_alpha(.55)
        for k, d in enumerate(data):
            ax.scatter(np.full(len(d), k + 1) + np.random.default_rng(k).uniform(-.12, .12, len(d)), d, s=12, color="k", zorder=3)
        ax.set_ylabel("MAE (kW)"); ax.set_title(t, fontsize=10, fontweight="bold")
    fig.tight_layout(); save(fig, "d_box.png")


# ------------------------------------------------------------------ sensitivity
def f_detectors():
    S = R["sens"]["det"]
    names = {"ph": "Page-Hinkley", "cusum": "CUSUM", "adwin": "ADWIN", "kspsi": "KS + PSI only"}
    ks = [k for k in ("ph", "cusum", "adwin", "kspsi") if k in S]
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.6))
    spec = [("mae", "Adaptive MAE (kW)", lambda r: r["mae"][0]), ("delay", "Detection delay (h)", lambda r: r["delay"][0] or 0),
            ("retr", "Retrainings (drift)", lambda r: r["retr"][0]), ("fa", "False alarms (no drift)", lambda r: r["fa_nodrift"][0])]
    for ax, (k, lab, f) in zip(axs, spec):
        vals = [f(S[d]) for d in ks]
        b = ax.bar([names[d].replace(" ", "\n", 1) for d in ks], vals, color=[NAVY, TEAL, AMBER, PURPLE][:len(ks)])
        for bb, v in zip(b, vals):
            ax.text(bb.get_x() + bb.get_width() / 2, v + max(vals) * .02, f"{v:.1f}", ha="center", fontsize=8.5)
        ax.set_title(lab, fontsize=9.5, fontweight="bold"); ax.tick_params(axis="x", labelsize=7.5); ax.set_ylim(0, max(vals) * 1.2 + 1e-6)
    fig.tight_layout(); save(fig, "d_detectors.png")


def f_sweeps():
    S = R["sens"]
    # lambda
    fig, axs = plt.subplots(1, 3, figsize=(10.4, 3.5))
    L = S["lam_d"]; Ln = S["lam_nd"]
    x = [r["v"] for r in L]
    axs[0].plot(x, [r["delay"][0] for r in L], "o-", color=NAVY); axs[0].set_ylabel("Detection delay (h)"); axs[0].set_title("Delay vs λ", fontsize=10, fontweight="bold")
    axs[1].plot(x, [r["retr"][0] for r in L], "o-", color=AMBER, label="drift"); axs[1].plot(x, [r["retr"][0] for r in Ln], "s--", color=GREY, label="no drift")
    axs[1].set_ylabel("Retrainings"); axs[1].set_title("Retrainings vs λ", fontsize=10, fontweight="bold"); axs[1].legend(fontsize=8)
    axs[2].plot(x, [r["mae"][0] for r in L], "o-", color=RED); axs[2].set_ylabel("Adaptive MAE (kW)"); axs[2].set_title("MAE vs λ (drift)", fontsize=10, fontweight="bold")
    for ax in axs:
        ax.set_xlabel("PH threshold λ (multiples of σ₀)")
    fig.tight_layout(); save(fig, "d_sweep_lam.png")
    # cooldown
    C = S["cd"]
    fig, axs = plt.subplots(1, 3, figsize=(10.4, 3.5)); x = [r["v"] for r in C]
    axs[0].plot(x, [r["retr"][0] for r in C], "o-", color=AMBER); axs[0].set_ylabel("Retrainings")
    axs[1].plot(x, [r["mae"][0] for r in C], "o-", color=RED); axs[1].set_ylabel("Adaptive MAE (kW)")
    axs[2].plot(x, [r["t_retrain"][0] for r in C], "o-", color=NAVY); axs[2].set_ylabel("Retraining time (s)")
    for ax, t in zip(axs, ("Retrainings", "Accuracy", "Compute")):
        ax.set_xlabel("Cool-down (hours)"); ax.set_title(t + " vs cool-down", fontsize=10, fontweight="bold"); ax.set_xscale("log")
    fig.tight_layout(); save(fig, "d_sweep_cd.png")
    # window
    W = S["win"]; x = [r["v"] for r in W]
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.5))
    axs[0].plot(x, [r["mae"][0] for r in W], "o-", color=RED); axs[0].set_ylabel("Adaptive MAE (kW)")
    axs[1].plot(x, [r["retr"][0] for r in W], "o-", color=AMBER); axs[1].set_ylabel("Retrainings")
    for ax in axs:
        ax.set_xlabel("Retraining window (weeks)"); ax.set_xticks(x)
    fig.tight_layout(); save(fig, "d_sweep_win.png")
    # magnitude
    M = S["mag"]; x = [r["v"] for r in M]
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.8))
    axs[0].plot(x, [r["static_mae"][0] for r in M], "o-", color=RED, label="Static"); axs[0].plot(x, [r["mae"][0] for r in M], "o-", color=NAVY, label="Adaptive")
    axs[0].set_xlabel("Drift magnitude (1.0 = baseline)"); axs[0].set_ylabel("MAE (kW)"); axs[0].legend(fontsize=8.5)
    gain = [(r["static_mae"][0] - r["mae"][0]) / r["static_mae"][0] * 100 for r in M]
    axs[1].bar([str(v) for v in x], gain, color=TEAL)
    for i, g in enumerate(gain):
        axs[1].text(i, g + (2 if g >= 0 else -6), f"{g:.0f}%", ha="center", fontsize=8.5)
    axs[1].axhline(0, color="k", lw=.8)
    axs[1].set_xlabel("Drift magnitude"); axs[1].set_ylabel("MAE reduction vs static (%)")
    fig.tight_layout(); save(fig, "d_sweep_mag.png")


if __name__ == "__main__":
    extra = {}
    f_data_overview(); f_weekly_profile(); f_power_scatter()
    ks1, ks0 = f_speed_hist(); extra["ks_drift"] = [float(ks1.statistic), float(ks1.pvalue)]; extra["ks_nodrift"] = [float(ks0.statistic), float(ks0.pvalue)]
    f_rose(); extra["importance"] = f_corr_importance(); f_calibration()
    f_rolling(A, "drift", "d_roll_drift.png", "Weekly MAE: drift scenario (seed 0)", True, A["alarms"])
    f_rolling(N, "nodrift", "d_roll_nodrift.png", "Weekly MAE: no-drift scenario (seed 0)", False)
    f_cum(); f_ph_trace(); f_input_monitor(); f_zoom(); f_bars(); f_retrain_cost(); f_delay(); f_scatter_pred(); f_resid(); f_timeline()
    res = f_err_by_speed(); extra["err_speed"] = {k: [None if np.isnan(x) else float(x) for x in v] for k, v in res.items()}
    f_box()
    # extra stats for text
    y = A["y"]; on = A["onset"] - i0
    post = slice(on + 14 * 24, None)
    extra["post_mae"] = {m: float(np.mean(np.abs(A[p][post] - y[post]))) for m, p in (("static", "p_static"), ("adaptive", "p_adapt"), ("weekly", "p_weekly"))}
    extra["pre_mae"] = {m: float(np.mean(np.abs(A[p][:on] - y[:on]))) for m, p in (("static", "p_static"), ("adaptive", "p_adapt"), ("weekly", "p_weekly"))}
    extra["transient_mae"] = {m: float(np.mean(np.abs(A[p][on:on + 14 * 24] - y[on:on + 14 * 24]))) for m, p in (("static", "p_static"), ("adaptive", "p_adapt"), ("weekly", "p_weekly"))}
    extra["seed0_alarms"] = [int(a) for a in A["alarms"]]; extra["seed0_sources"] = A["sources"]; extra["onset"] = int(A["onset"]); extra["i0"] = int(i0)
    extra["cal"] = {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in A["cal"].items()}
    if "sens" in R:
        f_detectors(); f_sweeps()
    json.dump(extra, open("extra.json", "w"), indent=1)
    print("figures done")
