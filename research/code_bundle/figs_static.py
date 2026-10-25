import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Ellipse, Polygon

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25})
NAVY, TEAL, AMBER, RED, GREY, GREEN, PURPLE = "#1f3a5f", "#1b8a8f", "#e8a317", "#c0392b", "#6b7280", "#2e8b57", "#6c4ab6"
OUT = "figs/"


def save(fig, name, dpi=200):
    fig.savefig(OUT + name, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc="#e8f0fa", ec=NAVY, fs=9, bold=False, tc="black", lw=1.4, style="round,pad=0.02,rounding_size=0.08"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", wrap=True)
    return p


def arrow(ax, p1, p2, color=NAVY, lw=1.6, style="-|>", ls="-", rad=0.0, ms=12):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, ls=ls,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0)
    ax.add_patch(a)


def blank(w, h, xl=(0, 10), yl=(0, 10)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.axis("off"); ax.grid(False)
    return fig, ax


# 1 ---------------------------------------------------------------- power curve
def fig_power_curve():
    v = np.linspace(0, 28, 600)
    vin, vr, vout, R = 3, 12, 25, 2000
    p = np.where(v < vin, 0, np.minimum(R * (v ** 3 - vin ** 3) / (vr ** 3 - vin ** 3), R))
    p = np.where(v >= vout, 0, p)
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    ax.plot(v, p, color=NAVY, lw=2.4)
    ax.axvspan(0, vin, color="#d7dde5", alpha=.5); ax.axvspan(vin, vr, color="#cfe8e9", alpha=.5)
    ax.axvspan(vr, vout, color="#fbe9c2", alpha=.6); ax.axvspan(vout, 28, color="#f4cfcb", alpha=.5)
    for x, t in [(1.5, "Region 1\nbelow cut-in"), (7.5, "Region 2\nP ∝ v³"), (18.5, "Region 3\nrated power"), (26.6, "Cut-out")]:
        ax.text(x, 2150, t, ha="center", va="bottom", fontsize=8.5)
    ax.annotate("cut-in 3 m/s", (vin, 0), (4.6, 330), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=8.5)
    ax.annotate("rated speed 12 m/s", (vr, R), (14.5, 1450), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=8.5)
    ax.annotate("cut-out 25 m/s", (vout, R), (21.0, 1050), arrowprops=dict(arrowstyle="->", color=GREY), fontsize=8.5)
    ax.set_ylim(0, 2600); ax.set_xlim(0, 28)
    ax.set_xlabel("Wind speed (m/s)"); ax.set_ylabel("Power output (kW)")
    ax.set_title("Idealised 2 MW turbine power curve", fontweight="bold")
    save(fig, "f_power_curve.png")


# 2 ---------------------------------------------------------------- drift types
def fig_drift_types():
    rng = np.random.default_rng(3)
    n = 200
    t = np.arange(n)
    fig, axs = plt.subplots(2, 2, figsize=(8.4, 5.2), sharex=True)
    base = rng.normal(0, 0.25, n)
    ser = {
        "(a) Sudden (abrupt) drift": base + np.where(t > 100, 2.0, 0),
        "(b) Gradual drift": base + np.where(t > 70, np.clip((t - 70) / 60, 0, 1) * 2.0 * (rng.random(n) < np.clip((t - 70) / 60, 0, 1)), 0),
        "(c) Incremental drift": base + np.clip((t - 60) / 90, 0, 1) * 2.0,
        "(d) Recurring drift": base + 2.0 * (((t > 50) & (t < 90)) | (t > 150)),
    }
    for ax, (k, s) in zip(axs.ravel(), ser.items()):
        ax.plot(t, s, color=NAVY, lw=1.1)
        ax.set_title(k, fontsize=10, fontweight="bold"); ax.set_ylim(-1, 3.4)
    for ax in axs[1]:
        ax.set_xlabel("Time step")
    for ax in axs[:, 0]:
        ax.set_ylabel("Mean of data stream")
    fig.tight_layout()
    save(fig, "f_drift_types.png")


# 3 ---------------------------------------------------------------- real vs virtual drift
def fig_real_virtual():
    rng = np.random.default_rng(5)
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.4), sharey=True, sharex=True)
    x = rng.uniform(0, 1, 160)
    f = lambda x: 1 / (1 + np.exp(-10 * (x - .5)))
    y0 = f(x) + rng.normal(0, .04, 160)
    axs[0].scatter(x, y0, s=10, color=NAVY); axs[0].set_title("(a) Original concept", fontsize=10, fontweight="bold")
    x2 = rng.uniform(0.35, 1, 160); y2 = f(x2) + rng.normal(0, .04, 160)
    axs[1].scatter(x2, y2, s=10, color=TEAL); axs[1].set_title("(b) Virtual drift: P(x) changes", fontsize=10, fontweight="bold")
    x3 = rng.uniform(0, 1, 160); y3 = 0.8 * f(x3 - .08) + rng.normal(0, .04, 160)
    axs[2].scatter(x3, y3, s=10, color=RED); axs[2].set_title("(c) Real drift: P(y|x) changes", fontsize=10, fontweight="bold")
    xs = np.linspace(0, 1, 100)
    for ax in axs:
        ax.plot(xs, f(xs), color=GREY, ls="--", lw=1); ax.set_xlabel("Input x (e.g. wind speed)")
    axs[0].set_ylabel("Target y (power)")
    axs[2].plot(xs, 0.8 * f(xs - .08), color=RED, lw=1.5)
    fig.tight_layout()
    save(fig, "f_real_virtual.png")


# 4 ---------------------------------------------------------------- architecture
def mbox(ax, x, y, w, h, title, desc, fc, ec):
    box(ax, x, y, w, h, "", fc=fc, ec=ec)
    ax.text(x + w / 2, y + h - 0.55, title, ha="center", va="center", fontsize=9.5, fontweight="bold")
    ax.text(x + w / 2, y + 0.75, desc, ha="center", va="center", fontsize=7.8, color="#333")


def fig_architecture():
    fig, ax = blank(11, 7.4, (0, 22), (0, 15))
    ax.text(11, 14.5, "Proposed Drift-Adaptive Wind-Power Forecasting Architecture", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    W, H = 4.8, 3.0
    mods = [(0.4, "M1  Data Acquisition", "Power history, wind speed,\ndirection, temperature"),
            (5.9, "M2  Preprocessing", "Cleaning, scaling, lag, rolling\n& sin/cos direction features"),
            (11.4, "M3  Forecast Model", "Gradient-boosted regressor\ntrained on initial window"),
            (16.9, "M4  Prediction &\nError Monitor", "Forecast vs actual power\n-> residual stream")]
    for x, t, d in mods:
        mbox(ax, x, 10.2, W, H, t, d, "#dbe9f7", NAVY)
    for i in range(3):
        arrow(ax, (mods[i][0] + W, 11.7), (mods[i + 1][0], 11.7))
    mbox(ax, 16.9, 5.0, W, H, "M5  Drift Detector", "Input drift: KS test / PSI\nError drift: Page-Hinkley", "#fbe3df", RED)
    mbox(ax, 11.4, 5.0, W, H, "M6  Adaptation\nController", "Retrain on recent window,\ncool-down guard", "#fdf0cf", AMBER)
    mbox(ax, 5.9, 5.0, W, H, "M7  Evaluation &\nComparison", "MAE, RMSE, nRMSE, delay,\nretrains, runtime", "#dff3e6", GREEN)
    arrow(ax, (19.3, 10.2), (19.3, 8.0), color=RED)
    ax.text(19.55, 9.1, "errors &\ninputs", fontsize=8, color=RED, va="center")
    arrow(ax, (16.9, 6.5), (16.2, 6.5), color=AMBER)
    ax.text(16.55, 7.0, "alarm", fontsize=8, ha="center", color="#a87400")
    arrow(ax, (13.8, 8.0), (13.8, 10.2), color=AMBER, lw=2.4)
    ax.text(14.05, 9.1, "updated model", fontsize=8, color="#a87400", va="center")
    arrow(ax, (11.4, 10.4), (10.7, 8.0), color=GREEN, ls="--", lw=1.2)
    ax.text(10.2, 9.1, "forecasts", fontsize=8, color=GREEN, ha="right")
    ax.add_patch(Rectangle((0.4, 0.5), 10.6, 3.6, fc="none", ec=GREY, ls="--", lw=1.4))
    box(ax, 0.8, 0.9, 4.6, 1.8, "B  Static Baseline\n(frozen initial model)", fc="#eceff3", ec=GREY, bold=True, fs=9)
    box(ax, 6.0, 0.9, 4.6, 1.8, "Weekly-retrain baseline\n(blind schedule)", fc="#eceff3", ec=GREY, bold=True, fs=9)
    ax.text(5.7, 3.5, "Control models (never drift-triggered)", ha="center", fontsize=8.5, color=GREY, style="italic")
    arrow(ax, (3.1, 4.1), (6.7, 5.0), color=GREY, ls="--", lw=1.2)
    arrow(ax, (8.3, 4.1), (8.3, 5.0), color=GREY, ls="--", lw=1.2)
    ax.text(15.0, 2.2, "Solid arrows: data flow\nAmber loop (M6 -> M3): model update on alarm\nDashed: evaluation / control path", fontsize=8.5, va="center",
            bbox=dict(boxstyle="round", fc="#fafafa", ec="#cccccc"))
    save(fig, "f_architecture.png")


# 5 ---------------------------------------------------------------- methodology flowchart
def fig_flow():
    fig, ax = blank(7.4, 10.5, (0, 10), (0, 21))
    steps = [("Start: historical power + weather data", "#e8f0fa", "oval"),
             ("Chronological split:\ninitial window | online stream", "#dbe9f7", "box"),
             ("Preprocess: clean, scale,\nlag / rolling / sin-cos features", "#dbe9f7", "box"),
             ("Train base model on initial window;\nfreeze copy as static baseline", "#dbe9f7", "box"),
             ("Calibrate error reference (μ₀, σ₀)\nby rolling-origin validation", "#dbe9f7", "box"),
             ("Next stream hour t: forecast power", "#dff3e6", "box"),
             ("Actual power revealed:\nresidual e(t), standardised z(t)", "#dff3e6", "box"),
             ("Update monitors:\nPage-Hinkley on z(t); KS / PSI on inputs", "#fbe3df", "box")]
    ys = np.linspace(20, 5.2, len(steps))
    for (t, c, k), y in zip(steps, ys):
        if k == "oval":
            ax.add_patch(Ellipse((4, y), 6.6, 1.15, fc=c, ec=NAVY, lw=1.4))
            ax.text(4, y, t, ha="center", va="center", fontsize=9)
        else:
            box(ax, 0.7, y - 0.6, 6.6, 1.2, t, fc=c, fs=9)
    for i in range(len(steps) - 1):
        arrow(ax, (4, ys[i] - 0.6), (4, ys[i + 1] + 0.6))
    # decision
    yd = 3.0
    ax.add_patch(Polygon([[4, yd + 1.25], [6.8, yd], [4, yd - 1.25], [1.2, yd]], fc="#fdf0cf", ec=AMBER, lw=1.5))
    ax.text(4, yd, "Drift alarm and\ncool-down elapsed?", ha="center", va="center", fontsize=8.5)
    arrow(ax, (4, ys[-1] - 0.6), (4, yd + 1.25))
    # yes branch
    box(ax, 7.2, 0.9, 2.6, 1.5, "Retrain on recent\nwindow, drift-aware\nweights; swap model", fc="#fdf0cf", ec=AMBER, fs=8)
    arrow(ax, (6.8, yd), (8.5, 2.4), color=AMBER)
    ax.text(7.7, 3.3, "Yes", fontsize=9, color=AMBER, fontweight="bold")
    ax.text(4.2, 1.35, "No", fontsize=9, fontweight="bold", color=NAVY)
    # loop back
    ax.plot([8.5, 8.5, 9.8, 9.8], [0.9, 0.35, 0.35, ys[5]], color=NAVY, lw=1.5)
    ax.plot([4, 4], [1.75, 0.35], color=NAVY, lw=1.5)
    ax.plot([4, 8.5], [0.35, 0.35], color=NAVY, lw=1.5)
    arrow(ax, (9.8, ys[5]), (7.3, ys[5]))
    ax.text(9.95, 5.0, "next hour", rotation=90, va="center", fontsize=8.5, color=NAVY)
    save(fig, "f_flowchart.png")


# 6 ---------------------------------------------------------------- DFD
def fig_dfd():
    fig, ax = blank(10.6, 6.2, (0, 22), (0, 13))
    ax.text(11, 12.4, "Level-1 Data Flow Diagram", ha="center", fontsize=13, fontweight="bold", color=NAVY)
    box(ax, 0.3, 5.4, 3.2, 2.2, "Data Source\n(SCADA / NWP /\nSynthetic generator)", fc="#eceff3", ec=GREY, fs=8.5, style="square,pad=0.02")
    procs = [(5.0, 8.2, "1.0\nPreprocess &\nFeature Build"), (9.6, 8.2, "2.0\nTrain / Update\nModel"), (14.2, 8.2, "3.0\nForecast"),
             (14.2, 3.0, "4.0\nMonitor Errors\n& Inputs"), (9.6, 3.0, "5.0\nDetect Drift"), (5.0, 3.0, "6.0\nEvaluate")]
    for x, y, t in procs:
        ax.add_patch(Ellipse((x + 1.7, y + 1.1), 3.4, 2.4, fc="#dbe9f7", ec=NAVY, lw=1.4))
        ax.text(x + 1.7, y + 1.1, t, ha="center", va="center", fontsize=8.5)
    # stores
    for x, y, t in [(9.3, 11.0, "D1  Feature store"), (9.3, 0.4, "D2  Alarm & metric log")]:
        ax.plot([x, x + 3.8], [y, y], color=NAVY); ax.plot([x, x + 3.8], [y + 0.9, y + 0.9], color=NAVY)
        ax.text(x + 1.9, y + 0.45, t, ha="center", va="center", fontsize=8.5)
    box(ax, 18.6, 5.4, 3.2, 2.2, "Grid operator /\nAnalyst", fc="#eceff3", ec=GREY, fs=9, style="square,pad=0.02")
    A = lambda a, b, **k: arrow(ax, a, b, **k)
    A((3.5, 6.9), (5.0, 8.9)); ax.text(3.6, 8.2, "raw data", fontsize=8)
    A((8.4, 9.3), (9.6, 9.3)); A((13.0, 9.3), (14.2, 9.3))
    A((15.9, 8.2), (15.9, 5.4)); ax.text(16.1, 6.8, "forecast", fontsize=8)
    A((14.2, 4.1), (13.0, 4.1)); A((9.6, 4.1), (8.4, 4.1))
    A((11.3, 5.4), (11.3, 8.2), color=AMBER, lw=2); ax.text(11.5, 6.8, "alarm →\nretrain", fontsize=8, color="#a87400")
    A((6.7, 8.2), (6.7, 5.4), ls="--", color=GREY)
    A((9.3, 11.45), (7.0, 10.5)); A((12.3, 11.0), (12.3, 10.4), color=GREY)
    A((11.3, 3.0), (11.3, 1.3), color=GREY)
    A((17.6, 9.3), (19.8, 7.6)); ax.text(18.9, 8.9, "forecasts", fontsize=8)
    A((6.7, 3.0), (9.2, 0.9), color=GREY)
    A((6.7, 3.0), (19.6, 5.4), color=GREEN, rad=0.35, ls="--"); ax.text(14.0, 0.4, "reports", fontsize=8, color=GREEN)
    save(fig, "f_dfd.png")


# 7 ---------------------------------------------------------------- use case diagram
def fig_usecase():
    fig, ax = blank(8.2, 5.6, (0, 16), (0, 11))
    ax.add_patch(Rectangle((4.2, 0.3), 10.6, 10.4, fc="#fafafa", ec=NAVY, lw=1.4))
    ax.text(9.5, 10.2, "Drift-Adaptive Forecasting System", ha="center", fontweight="bold", color=NAVY)
    uc = [(9.5, 8.8, "Load / simulate data"), (9.5, 7.2, "Train base model"), (9.5, 5.6, "Forecast power"),
          (9.5, 4.0, "Monitor drift"), (9.5, 2.4, "Retrain on alarm"), (12.8, 6.4, "Compare models"), (12.8, 3.2, "View reports")]
    for x, y, t in uc:
        ax.add_patch(Ellipse((x, y), 4.2 if x < 12 else 3.0, 1.15, fc="#e8f0fa", ec=NAVY))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.2 if x < 12 else 7.6)
    for (px, py, nm) in [(1.5, 6.5, "Data\nScientist"), (1.5, 2.4, "Grid\nOperator")]:
        ax.add_patch(Circle((px, py + 1.0), 0.35, fc="white", ec=NAVY, lw=1.5))
        ax.plot([px, px], [py + 0.65, py - 0.3], color=NAVY, lw=1.5)
        ax.plot([px - .6, px + .6], [py + 0.35, py + 0.35], color=NAVY, lw=1.5)
        ax.plot([px, px - .5], [py - 0.3, py - 1.0], color=NAVY, lw=1.5); ax.plot([px, px + .5], [py - 0.3, py - 1.0], color=NAVY, lw=1.5)
        ax.text(px, py - 1.6, nm, ha="center", fontsize=8.5)
    for y in (8.8, 7.2, 5.6, 4.0, 2.4):
        ax.plot([2.1, 7.4], [6.8, y], color=GREY, lw=0.8)
    for y in (5.6, 4.0, 3.2):
        ax.plot([2.1, 7.4 if y != 3.2 else 11.3], [2.2, y], color=GREY, lw=0.8)
    ax.plot([2.1, 11.3], [6.8, 6.4], color=GREY, lw=0.8)
    save(fig, "f_usecase.png")


# 8 ---------------------------------------------------------------- sequence diagram
def fig_sequence():
    fig, ax = blank(9.6, 6.4, (0, 24), (0, 16))
    names = ["Data stream", "Forecaster\n(M3/M4)", "Drift detector\n(M5)", "Controller\n(M6)", "Evaluator\n(M7)"]
    xs = [2, 6.6, 11.2, 15.8, 20.4]
    for x, n in zip(xs, names):
        box(ax, x - 1.7, 14.2, 3.4, 1.4, n, fc="#dbe9f7", fs=8.5, bold=True)
        ax.plot([x, x], [14.2, 0.4], color=GREY, ls="--", lw=1)
    msgs = [(0, 1, 13.2, "features x(t)"), (1, 0, 12.2, "forecast ŷ(t)"), (0, 2, 11.2, "actual y(t)"),
            (2, 2, 10.2, "update PH / KS / PSI"), (2, 3, 8.3, "ALARM (threshold crossed)"),
            (3, 3, 7.3, "cool-down check, select window"), (3, 1, 5.7, "retrain(window, weights)"),
            (1, 3, 4.7, "updated model"), (1, 4, 3.7, "forecasts: static / adaptive"),
            (0, 4, 2.7, "actual y(t)"), (4, 4, 1.7, "MAE, RMSE, delay, retrains")]
    for a, b, y, t in msgs:
        if a == b:
            ax.add_patch(FancyArrowPatch((xs[a], y), (xs[a], y - .6), connectionstyle="arc3,rad=-1.8", arrowstyle="-|>", mutation_scale=10, color=NAVY, lw=1.3))
            ax.text(xs[a] + 0.9, y - 0.3, t, fontsize=8, va="center")
        else:
            arrow(ax, (xs[a], y), (xs[b], y), ms=10, lw=1.3)
            ax.text((xs[a] + xs[b]) / 2, y + 0.25, t, ha="center", fontsize=8)
    save(fig, "f_sequence.png")


# 9 ---------------------------------------------------------------- chronological split
def fig_split():
    fig, ax = blank(10, 3.0, (0, 106), (0, 6))
    ax.add_patch(Rectangle((0, 2), 22, 1.6, fc="#bcd6ef", ec=NAVY)); ax.text(11, 2.8, "Calibration folds", ha="center", fontsize=8.5)
    ax.add_patch(Rectangle((22, 2), 4, 1.6, fc="#8fb9e3", ec=NAVY)); ax.text(24, 2.8, "val", ha="center", fontsize=8)
    ax.add_patch(Rectangle((26, 2), 80, 1.6, fc="#fdf0cf", ec=AMBER)); ax.text(66, 2.8, "Online stream (80 weeks): test-then-train", ha="center", fontsize=9)
    ax.plot([0, 26], [4.4, 4.4], color=NAVY, lw=2); ax.text(13, 4.65, "Initial window: 26 weeks (4,368 h)", ha="center", fontsize=9, fontweight="bold")
    ax.plot([26, 106], [4.4, 4.4], color=AMBER, lw=2); ax.text(66, 4.65, "Stream: 80 weeks (13,440 h)", ha="center", fontsize=9, fontweight="bold")
    ax.axvline(28, ymin=0.1, ymax=0.9, color=RED, lw=2, ls="--"); ax.text(28.6, 0.9, "drift onset: week 28", color=RED, fontsize=8.5)
    for w in (0, 26, 52, 78, 104):
        ax.text(w, 1.65, f"wk {w}", ha="center", fontsize=8, color=GREY)
    save(fig, "f_split.png")


# 10 --------------------------------------------------------------- direction encoding
def fig_direction():
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.6))
    th = np.arange(0, 361)
    ax = axs[0]
    ax.plot(th, th, color=RED, lw=2, label="raw angle θ")
    ax.axvline(359, color=GREY, ls=":"); ax.annotate("359° and 1° are\n358° apart numerically", (330, 330), (140, 330), fontsize=8, arrowprops=dict(arrowstyle="->", color=GREY))
    ax.set_xlabel("Wind direction θ (degrees)"); ax.set_ylabel("Raw feature value"); ax.set_title("(a) Raw angle: discontinuity at 0°/360°", fontsize=9.5, fontweight="bold")
    ax = axs[1]
    ax.plot(th, np.sin(np.deg2rad(th)), color=NAVY, lw=2, label="sin θ"); ax.plot(th, np.cos(np.deg2rad(th)), color=TEAL, lw=2, label="cos θ")
    ax.set_xlabel("Wind direction θ (degrees)"); ax.set_title("(b) Cyclic encoding: continuous", fontsize=9.5, fontweight="bold"); ax.legend(fontsize=8)
    fig.tight_layout(); save(fig, "f_direction.png")


# 11 --------------------------------------------------------------- weighting
def fig_weights():
    age = np.arange(0, 673)
    w = 0.5 ** (age / 336)
    t = 672 - age
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    ax.plot(t, w, color=NAVY, lw=2, label="Recency weight (half-life 336 h)")
    tau = 520
    w2 = np.where(t < tau, w * 0.08, w)
    ax.plot(t, w2, color=AMBER, lw=2, label="With drift-aware down-weighting (pre-change × 0.08)")
    ax.axvline(tau, color=RED, ls="--"); ax.text(tau + 6, 0.62, "estimated change\npoint τ̂", color=RED, fontsize=8.5)
    ax.set_xlabel("Hours within the 672 h retraining window (oldest → newest)"); ax.set_ylabel("Sample weight"); ax.legend(fontsize=8, loc="center left")
    ax.set_title("Sample weights used when retraining", fontweight="bold"); save(fig, "f_weights.png")


# 12 --------------------------------------------------------------- Page-Hinkley concept
def fig_ph_concept():
    rng = np.random.default_rng(8)
    n = 300
    x = np.abs(rng.normal(1.0, 0.8, n)); x[150:] = np.abs(rng.normal(3.0, 1.2, n - 150))
    mu0, d, lam = 1.0, 0.5, 12.0
    m = np.cumsum(x - mu0 - d); M = np.minimum.accumulate(m); stat = m - M
    alarm = int(np.argmax(stat > lam))
    fig, axs = plt.subplots(2, 1, figsize=(7.8, 5.0), sharex=True)
    axs[0].plot(x, color=NAVY, lw=0.8); axs[0].axvline(150, color=RED, ls="--"); axs[0].set_ylabel("Standardised error z(t)")
    axs[0].text(152, 6.3, "true change", color=RED, fontsize=8.5)
    axs[1].plot(stat, color=TEAL, lw=1.6, label="PH statistic  mₜ − Mₜ"); axs[1].axhline(lam, color=AMBER, ls="--", label="threshold λ")
    axs[1].axvline(alarm, color=GREEN, ls=":", lw=2); axs[1].text(alarm + 3, lam * 2.2, f"alarm at t = {alarm}\n(delay {alarm - 150} steps)", color=GREEN, fontsize=8.5)
    axs[1].set_xlabel("Time step"); axs[1].set_ylabel("Statistic"); axs[1].legend(fontsize=8, loc="upper left")
    fig.tight_layout(); save(fig, "f_ph_concept.png")


# 13 --------------------------------------------------------------- KS & PSI concept
def fig_ks_concept():
    rng = np.random.default_rng(2)
    ref = rng.normal(8, 2.6, 800); cur = rng.normal(8.8, 2.8, 400)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.6))
    axs[0].hist(ref, bins=25, alpha=.6, color=NAVY, density=True, label="Reference window")
    axs[0].hist(cur, bins=25, alpha=.6, color=AMBER, density=True, label="Current window")
    axs[0].set_xlabel("Wind speed (m/s)"); axs[0].set_ylabel("Density"); axs[0].legend(fontsize=8); axs[0].set_title("(a) Distribution comparison", fontsize=9.5, fontweight="bold")
    a, b = np.sort(ref), np.sort(cur)
    grid = np.linspace(0, 18, 400)
    Fa = np.searchsorted(a, grid) / len(a); Fb = np.searchsorted(b, grid) / len(b)
    k = np.argmax(np.abs(Fa - Fb))
    axs[1].plot(grid, Fa, color=NAVY, label="ECDF reference"); axs[1].plot(grid, Fb, color=AMBER, label="ECDF current")
    axs[1].vlines(grid[k], min(Fa[k], Fb[k]), max(Fa[k], Fb[k]), color=RED, lw=2)
    axs[1].text(grid[k] + .4, (Fa[k] + Fb[k]) / 2, f"D = {abs(Fa[k]-Fb[k]):.3f}", color=RED, fontsize=9)
    axs[1].set_xlabel("Wind speed (m/s)"); axs[1].legend(fontsize=8); axs[1].set_title("(b) KS statistic = max ECDF gap", fontsize=9.5, fontweight="bold")
    fig.tight_layout(); save(fig, "f_ks_concept.png")


# 14 --------------------------------------------------------------- Gantt
def fig_gantt():
    tasks = [("Problem study & literature survey", 0, 3), ("Synthetic data generator design", 2, 5), ("Feature engineering & base model", 4, 7),
             ("Drift detectors (PH, KS/PSI, ADWIN, CUSUM)", 6, 10), ("Adaptation controller", 8, 11), ("Experiments & sensitivity analysis", 10, 14),
             ("Result analysis & visualisation", 13, 16), ("Report writing & review", 14, 18)]
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    for i, (t, s, e) in enumerate(tasks[::-1]):
        ax.barh(i, e - s, left=s, color=[NAVY, TEAL, AMBER, PURPLE, GREEN, RED, GREY, "#3b7dd8"][i % 8], height=0.55)
        ax.text(e + 0.15, i, "", fontsize=8)
    ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t for t, _, _ in tasks[::-1]], fontsize=8.5)
    ax.set_xlabel("Project week"); ax.set_xlim(0, 19); ax.set_xticks(range(0, 19, 2)); ax.grid(axis="x", alpha=.3); ax.grid(axis="y", visible=False)
    ax.set_title("Project schedule", fontweight="bold"); save(fig, "f_gantt.png")


# 15 --------------------------------------------------------------- class diagram
def fig_class():
    fig, ax = blank(10.4, 5.4, (0, 24), (0, 12.5))
    def cls(x, y, w, name, attrs, meths, h=None):
        h = h or (1.0 + 0.62 * (len(attrs) + len(meths)))
        ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=NAVY, lw=1.4))
        ax.add_patch(Rectangle((x, y + h - 1.0), w, 1.0, fc="#dbe9f7", ec=NAVY, lw=1.4))
        ax.text(x + w / 2, y + h - 0.5, name, ha="center", va="center", fontweight="bold", fontsize=9)
        yy = y + h - 1.55
        for a in attrs:
            ax.text(x + 0.2, yy, a, fontsize=7.6, va="center"); yy -= 0.62
        ax.plot([x, x + w], [yy + 0.31, yy + 0.31], color=NAVY, lw=0.8); yy -= 0.1
        for m in meths:
            ax.text(x + 0.2, yy, m, fontsize=7.6, va="center"); yy -= 0.62
        return (x, y, w, h)
    a = cls(0.3, 6.0, 5.8, "WindDataGenerator", ["+seed: int", "+drift: bool", "+magnitude: float"], ["+generate(): dict", "+features(): ndarray"])
    b = cls(7.3, 6.0, 5.2, "Forecaster", ["+model: HistGBR", "+window: int"], ["+fit(X, y, w)", "+predict(X)"])
    c = cls(13.8, 6.0, 5.2, "DriftDetector«abstract»", ["+mu0, sigma0", "+threshold"], ["+update(z, t): bool", "+reset()"])
    d = cls(7.3, 0.4, 5.2, "AdaptationController", ["+cooldown: int", "+tau: int"], ["+on_alarm(t)", "+retrain()"])
    e = cls(19.2, 7.8, 4.5, "PageHinkley", ["+delta, lambda"], ["+update()"], h=3.4)
    f = cls(19.2, 3.9, 4.5, "KSPSIMonitor", ["+alpha, psi_thr"], ["+update()"], h=3.4)
    g = cls(0.3, 0.4, 5.8, "Evaluator", ["+mae, rmse, nrmse", "+delay, retrains"], ["+compare(): table"])
    arrow(ax, (6.1, 8.0), (7.3, 8.0), style="-|>"); arrow(ax, (12.5, 8.0), (13.8, 8.0), style="-|>")
    arrow(ax, (15.5, 6.0), (12.5, 2.6), style="-|>"); arrow(ax, (9.9, 3.9), (9.9, 6.0), style="-|>")
    arrow(ax, (19.2, 9.5), (19.0, 9.5), style="-|>"); arrow(ax, (19.2, 5.6), (19.0, 7.0), style="-|>")
    arrow(ax, (7.3, 1.5), (6.1, 1.5), style="-|>")
    save(fig, "f_class.png")


# 16 --------------------------------------------------------------- literature themes
def fig_lit():
    themes = ["Drift-aware\nwind forecasting", "Online ensembles /\nload (drift)", "Spatio-temporal\nGNN", "Transfer / domain\nadaptation", "Reviews", "Input-bias\ncorrection"]
    cnt = [3, 1, 2, 3, 2, 1]
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    bars = ax.bar(themes, cnt, color=[NAVY, TEAL, AMBER, PURPLE, GREEN, GREY])
    for b, c in zip(bars, cnt):
        ax.text(b.get_x() + b.get_width() / 2, c + .05, str(c), ha="center", fontsize=9)
    ax.set_ylabel("Number of surveyed works"); ax.set_ylim(0, 4); ax.tick_params(axis="x", labelsize=8)
    ax.set_title("Distribution of surveyed literature by theme", fontweight="bold"); save(fig, "f_lit.png")


if __name__ == "__main__":
    for f in [fig_power_curve, fig_drift_types, fig_real_virtual, fig_architecture, fig_flow, fig_dfd, fig_usecase, fig_sequence,
              fig_split, fig_direction, fig_weights, fig_ph_concept, fig_ks_concept, fig_gantt, fig_class, fig_lit]:
        f(); print("ok", f.__name__)
