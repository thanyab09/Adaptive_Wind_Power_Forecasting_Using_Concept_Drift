import pickle, json, numpy as np
from scipy import stats
main = pickle.load(open("main.pkl","rb"))
HPW=168; ON=28*HPW
out={}
def mae(m,s,d=True): return main[(d,s)][m]["metrics"][0]
def rm(m,s,d=True): return main[(d,s)][m]["metrics"][1]
for a,b in (("static","adaptive"),("weekly","adaptive"),("static","weekly")):
    x=[mae(a,s) for s in range(10)]; y=[mae(b,s) for s in range(10)]
    t=stats.ttest_rel(x,y); w=stats.wilcoxon(x,y)
    out[f"{a}_vs_{b}"]=dict(t=float(t.statistic),p=float(t.pvalue),w=float(w.statistic),wp=float(w.pvalue),
        diff=float(np.mean(np.array(x)-np.array(y))), sd=float(np.std(np.array(x)-np.array(y),ddof=1)))
    x=[rm(a,s) for s in range(10)]; y=[rm(b,s) for s in range(10)]
    t=stats.ttest_rel(x,y); out[f"{a}_vs_{b}_rmse"]=dict(t=float(t.statistic),p=float(t.pvalue))
# late alarms
early,late=[],[]
for s in range(10):
    rt=np.array(main[(True,s)]["adaptive"]["retrain_t"])
    early.append(int(((rt>=ON)&(rt<ON+3*HPW)).sum())); late.append(int((rt>=ON+3*HPW).sum()))
out["early"]=early; out["late"]=late
# retrain time per retrain
out["sec_per_retrain_adaptive"]=float(np.mean([main[(True,s)]["adaptive"]["t_retrain"]/max(main[(True,s)]["adaptive"]["n_retrain"],1) for s in range(10)]))
out["sec_per_retrain_weekly"]=float(np.mean([main[(True,s)]["weekly"]["t_retrain"]/80 for s in range(10)]))
out["t_detect_per_step_ms"]=float(np.mean([main[(True,s)]["adaptive"]["t_detect"] for s in range(10)])/13440*1000)
out["corr_delay_wind"]=None
json.dump(out,open("extra2.json","w"),indent=1)
print(json.dumps(out,indent=1))
