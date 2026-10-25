import pickle, json, numpy as np

main = pickle.load(open("main.pkl", "rb"))
try:
    sens = pickle.load(open("sens.pkl", "rb"))
except Exception:
    sens = {}
R = {}


def ms(a):
    a = np.array(a, dtype=float)
    return [float(a.mean()), float(a.std(ddof=1)) if len(a) > 1 else 0.0]


for drift in (True, False):
    key = "drift" if drift else "nodrift"
    R[key] = {}
    for m in ("static", "adaptive", "weekly"):
        mets = np.array([main[(drift, s)][m]["metrics"] for s in range(10)])
        R[key][m] = dict(mae=ms(mets[:, 0]), rmse=ms(mets[:, 1]), nrmse=ms(mets[:, 2]),
                         mae_seeds=mets[:, 0].tolist(), rmse_seeds=mets[:, 1].tolist(),
                         retrains=ms([main[(drift, s)][m].get("n_retrain", 0) for s in range(10)]),
                         t_retrain=ms([main[(drift, s)][m].get("t_retrain", 0.0) for s in range(10)]))
    R[key]["alarm_sources"] = {}
    srcs = [x for s in range(10) for x in main[(drift, s)]["adaptive"]["sources"]]
    for x in set(srcs):
        R[key]["alarm_sources"][x] = srcs.count(x)
    R[key]["t_detect"] = ms([main[(drift, s)]["adaptive"]["t_detect"] for s in range(10)])
    R[key]["false_alarms"] = [main[(drift, s)]["false_alarms"] for s in range(10)]
    R[key]["retrain_t_seeds"] = [main[(drift, s)]["adaptive"]["retrain_t"] for s in range(10)]
    R[key]["mu0"] = [main[(drift, s)]["mu0"] for s in range(10)]
    R[key]["s0"] = [main[(drift, s)]["s0"] for s in range(10)]
dl = [main[(True, s)]["delay"] for s in range(10)]
R["delays"] = dl
R["delay_mean"] = float(np.mean([d for d in dl if d is not None]))
R["detected"] = int(sum(d is not None for d in dl))
st, ad, wk = R["drift"]["static"]["mae"][0], R["drift"]["adaptive"]["mae"][0], R["drift"]["weekly"]["mae"][0]
R["mae_reduction_pct"] = (st - ad) / st * 100
R["gap_to_weekly_pct"] = (ad - wk) / wk * 100
R["retrain_ratio"] = R["drift"]["weekly"]["retrains"][0] / max(R["drift"]["adaptive"]["retrains"][0], 1e-9)
R["nodrift_weekly_penalty_pct"] = (R["nodrift"]["weekly"]["mae"][0] - R["nodrift"]["static"]["mae"][0]) / R["nodrift"]["static"]["mae"][0] * 100

# paired per-seed reductions
R["red_seeds"] = [(main[(True, s)]["static"]["metrics"][0] - main[(True, s)]["adaptive"]["metrics"][0]) / main[(True, s)]["static"]["metrics"][0] * 100 for s in range(10)]

# sensitivity
def sg(prefix, vals, drift=True, extra=None):
    out = []
    for v in vals:
        rows = [sens[(prefix, v, drift, s)] for s in range(5) if (prefix, v, drift, s) in sens]
        if not rows:
            continue
        mae = [r["adaptive"]["metrics"][0] for r in rows]
        smae = [r["static"]["metrics"][0] for r in rows]
        dly = [r["delay"] for r in rows if r["delay"] is not None]
        out.append(dict(v=v, mae=ms(mae), static_mae=ms(smae), retr=ms([r["adaptive"]["n_retrain"] for r in rows]),
                        delay=ms(dly) if dly else [None, None], fa=ms([r["false_alarms"] for r in rows]),
                        detected=len(dly), n=len(rows), t_retrain=ms([r["adaptive"]["t_retrain"] for r in rows])))
    return out


if sens:
    R["sens"] = {}
    dets = {}
    for det in ("ph", "cusum", "adwin", "kspsi"):
        d, nd = [], []
        for s in range(5):
            if ("det", det, True, s) in sens:
                d.append(sens[("det", det, True, s)])
                nd.append(sens[("det", det, False, s)])
        if d:
            dly = [r["delay"] for r in d if r["delay"] is not None]
            dets[det] = dict(mae=ms([r["adaptive"]["metrics"][0] for r in d]), retr=ms([r["adaptive"]["n_retrain"] for r in d]),
                             delay=ms(dly) if dly else [None, None], detected=len(dly), n=len(d),
                             fa_nodrift=ms([r["false_alarms"] for r in nd]), nd_mae=ms([r["adaptive"]["metrics"][0] for r in nd]),
                             nd_static=ms([r["static"]["metrics"][0] for r in nd]),
                             fa_pre=ms([r["false_alarms"] for r in d]), t_detect=ms([r["adaptive"]["t_detect"] for r in d]))
    R["sens"]["det"] = dets
    R["sens"]["lam_d"] = sg("lam", (6, 10, 15, 25, 40), True)
    R["sens"]["lam_nd"] = sg("lam", (6, 10, 15, 25, 40), False)
    R["sens"]["cd"] = sg("cd", (12, 24, 48, 96, 168), True)
    R["sens"]["win"] = sg("win", (2, 4, 6, 8), True)
    R["sens"]["mag"] = sg("mag", (0.0, 0.1, 0.25, 0.5, 1.0, 1.5), True)
json.dump(R, open("results.json", "w"), indent=1, default=lambda o: None)
print(json.dumps({k: R[k] for k in ("mae_reduction_pct", "gap_to_weekly_pct", "retrain_ratio", "nodrift_weekly_penalty_pct", "delay_mean", "detected")}, indent=1))
for k in ("drift", "nodrift"):
    for m in ("static", "adaptive", "weekly"):
        print(k, m, {a: [round(x, 2) for x in R[k][m][a]] for a in ("mae", "rmse", "nrmse", "retrains", "t_retrain")})
print("sources", R["drift"]["alarm_sources"], R["nodrift"]["alarm_sources"], "fa", R["drift"]["false_alarms"], R["nodrift"]["false_alarms"])
print("delays", R["delays"])
