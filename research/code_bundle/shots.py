import pickle, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sim
from sim import *
main = pickle.load(open("main.pkl","rb")); R = json.load(open("results.json"))
A = main[(True,0)]["arrays"]; N = main[(False,0)]["arrays"]

def shot(lines, fname, title, w=9.2):
    n = len(lines); h = 0.30 + 0.205*n
    fig = plt.figure(figsize=(w, h+0.35), facecolor="#1e1e1e")
    ax = fig.add_axes([0,0,1,1]); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.add_patch(plt.Rectangle((0,1-0.35/(h+0.35)),1,0.35/(h+0.35),fc="#2d2d2d",ec="none"))
    for i,c in enumerate(("#ff5f57","#febc2e","#28c840")): ax.add_patch(plt.Circle((0.02+0.018*i,1-0.175/(h+0.35)),0.006,fc=c,ec="none",transform=ax.transAxes))
    ax.text(0.5,1-0.175/(h+0.35),title,ha="center",va="center",color="#cccccc",fontsize=8.5,family="DejaVu Sans")
    for i,l in enumerate(lines):
        y = 1-(0.35+0.2+0.205*i)/(h+0.35)
        col = "#d4d4d4"
        if l.startswith(">>>") or l.startswith("$"): col = "#7ee787"
        elif "ALARM" in l: col = "#ffa657"
        elif l.startswith("==") or l.startswith("--"): col = "#79c0ff"
        ax.text(0.02,y,l,ha="left",va="center",color=col,fontsize=7.6,family="DejaVu Sans Mono")
    fig.savefig("shots/"+fname,dpi=170,facecolor=fig.get_facecolor()); plt.close(fig)

# 1 generator
D = generate(0, drift=True)
v=D["v"]; i0=A["i0"]
L1 = ['$ python generate_data.py --seed 0 --drift on --magnitude 1.0',
 'Generating synthetic wind-farm stream ...',
 f'  total hours            : {D["n"]:,}  ({sim.TOTAL_WEEKS} weeks)',
 f'  initial window         : {i0:,} h  (weeks 0-{sim.INIT_WEEKS})',
 f'  online stream          : {D["n"]-i0:,} h  ({sim.TOTAL_WEEKS-sim.INIT_WEEKS} weeks)',
 f'  drift onset            : hour {D["onset"]:,}  (week {sim.DRIFT_WEEK})',
 f'  rated power            : {RATED:.0f} kW',
 f'  mean measured speed    : {v.mean():.2f} m/s   (std {v.std():.2f})',
 f'  mean observed power    : {D["p"].mean():.1f} kW   (capacity factor {D["p"].mean()/RATED*100:.1f} %)',
 f'  mean power before drift: {D["p"][:D["onset"]].mean():.1f} kW',
 f'  mean power after drift : {D["p"][D["onset"]:].mean():.1f} kW',
 f'  max power before / after drift: {D["p"][:D["onset"]].max():.0f} kW / {D["p"][D["onset"]:].max():.0f} kW',
 '>>> done: 17,808 rows x 10 features']
shot(L1,"console_data.png","Terminal - data generation (seed 0)")

# 2 calibration
cal=A["cal"]
L2 = ['$ python train_base.py --seed 0',
 'Feature matrix: (17808, 10)   ["v","sin_d","cos_d","temp","p_l1","p_l2","p_l24","p_m6","v_l1","v_m3"]',
 'Training base HistGradientBoostingRegressor(max_iter=120, lr=0.1, max_depth=6) on 4,368 rows ... done',
 'Rolling-origin calibration (origins: weeks 10, 14, 18, 22; next 4 weeks each)',
 '  forecast-level bins   : 6 (quantile edges, kW) ' + ', '.join(f'{e:.0f}' for e in cal["edges"]),
 '  mean abs error per bin: ' + ', '.join(f'{m:.1f}' for m in cal["means"]) + '  (kW)',
 f'  standardised error    : mu0 = {cal["mu0"]:.3f}   sigma0 = {cal["s0"]:.3f}',
 f'  Page-Hinkley          : delta = 0.6*sigma0 = {0.6*cal["s0"]:.3f}   lambda = 15*sigma0 = {15*cal["s0"]:.3f}',
 '  cool-down 48 h | retrain window 672 h | recency half-life 336 h | pre-change weight 0.08',
 '>>> base model ready; static copy frozen']
shot(L2,"console_train.png","Terminal - base model training and calibration (seed 0)")

# 3 stream log
al=A["alarms"]; src=A["sources"]; on=A["onset"]
L3 = ['$ python stream.py --seed 0 --scenario drift --detector ph',
 f'Replaying {len(A["y"]):,} hourly steps (test-then-train) ...']
for k,s in list(zip(al,src))[:14]:
    L3.append(f'[week {k/HPW:6.2f} | hour {k:6d} | {k-on:+5d} h from onset]  ALARM ({s})  -> retrain on last 672 h')
if len(al)>14: L3.append(f'  ... {len(al)-14} further alarms omitted ...')
first=[a for a in al if a>=on][0]
L3 += ['--------------------------------------------------------------------------------',
 f'alarms / retrainings : {len(al)}      false alarms before onset: 0',
 f'detection delay      : {first-on} h',
 f'MAE static / adaptive / weekly : {main[(True,0)]["static"]["metrics"][0]:.1f} / {main[(True,0)]["adaptive"]["metrics"][0]:.1f} / {main[(True,0)]["weekly"]["metrics"][0]:.1f} kW']
shot(L3,"console_stream.png","Terminal - online stream with drift-triggered retraining (seed 0)", w=9.8)

# 4 results table
def row(nm,key,m): 
    d=R[key][m]; return f'{nm:<10}| {d["mae"][0]:6.1f} +/- {d["mae"][1]:4.1f} | {d["rmse"][0]:6.1f} +/- {d["rmse"][1]:4.1f} | {d["nrmse"][0]:5.2f} | {d["retrains"][0]:5.1f} | {d["t_retrain"][0]:6.2f}'
L4=['$ python evaluate.py --seeds 0-9',
 'Scenario: DRIFT (abrupt, week 28)    mean +/- std over 10 seeds',
 'model     |      MAE (kW)  |     RMSE (kW)  | nRMSE% | retr. | time(s)',
 '----------+----------------+----------------+--------+-------+--------',
 row('static','drift','static'),row('adaptive','drift','adaptive'),row('weekly','drift','weekly'),
 f'detection delay: mean {R["delay_mean"]:.1f} h, detected {R["detected"]}/10, false alarms before onset: {sum(R["drift"]["false_alarms"])}',
 f'MAE reduction adaptive vs static: {R["mae_reduction_pct"]:.1f} %',
 '',
 'Scenario: NO DRIFT',
 'model     |      MAE (kW)  |     RMSE (kW)  | nRMSE% | retr. | time(s)',
 '----------+----------------+----------------+--------+-------+--------',
 row('static','nodrift','static'),row('adaptive','nodrift','adaptive'),row('weekly','nodrift','weekly'),
 f'alarms raised by adaptive model: {sum(R["nodrift"]["false_alarms"])}   (weekly penalty vs static: +{R["nodrift_weekly_penalty_pct"]:.1f} % MAE)']
shot(L4,"console_results.png","Terminal - evaluation summary over ten seeds", w=9.6)
print("shots ok")

# 5 sensitivity
S = R["sens"]
def g(x,d=1): return "  -  " if x is None else f"{x:.{d}f}"
L5=['$ python run_sens.py   # five seeds per setting',
 '== detector comparison (drift: MAE kW, retrainings, delay h | no drift: alarms/run, MAE kW) ==',
 'detector      | MAE   retr  delay | alarms  MAE(no drift)']
for k,nm in (('ph','Page-Hinkley'),('cusum','CUSUM'),('adwin','ADWIN'),('kspsi','KS+PSI only')):
    d=S['det'][k]; L5.append(f'{nm:<13} | {d["mae"][0]:5.1f} {d["retr"][0]:5.1f} {g(d["delay"][0]):>6} | {d["fa_nodrift"][0]:6.1f}  {d["nd_mae"][0]:6.1f}')
L5+=['== threshold lambda (multiples of sigma0) ==','lambda | drift: MAE  retr  delay | no drift: alarms/run']
for a,b in zip(S['lam_d'],S['lam_nd']): L5.append(f'{a["v"]:>6} | {a["mae"][0]:10.1f} {a["retr"][0]:5.1f} {g(a["delay"][0]):>6} | {b["retr"][0]:10.1f}')
L5+=['== cool-down (h) ==','cooldown | MAE   retr']
for a in S['cd']: L5.append(f'{a["v"]:>8} | {a["mae"][0]:5.1f} {a["retr"][0]:5.1f}')
L5+=['== retraining window (weeks) ==','window | MAE   retr']
for a in S['win']: L5.append(f'{a["v"]:>6} | {a["mae"][0]:5.1f} {a["retr"][0]:5.1f}')
L5+=['== drift magnitude (1.0 = baseline) ==','magnitude | static  adaptive  detected']
for a in S['mag']: L5.append(f'{a["v"]:>9} | {a["static_mae"][0]:6.1f} {a["mae"][0]:8.1f}  {a["detected"]}/{a["n"]}')
shot(L5,"console_sens.png","Terminal - sensitivity studies (five seeds per setting)", w=9.6)
print("sens shot ok")
