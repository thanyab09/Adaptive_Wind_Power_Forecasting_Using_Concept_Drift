import pickle, time
from sim import *
def slim(o):
    r = {k: o[k] for k in ('mu0','s0','delay','false_alarms')}
    for k in ('static','weekly','adaptive'):
        r[k] = {kk:vv for kk,vv in o[k].items() if kk not in ('pred','trace')}
    return r
sens = {}; t0 = time.time()
def run(key, **kw):
    sens[key] = slim(experiment(kw.pop('seed'), do_weekly=False, **kw))
for det in ('ph','cusum','adwin','kspsi'):
    for seed in range(5):
        for drift in (True, False):
            run(('det',det,drift,seed), seed=seed, drift=drift, detector=det, use_input=(det!='adwin'))
            if det == 'ph':   # default configuration doubles as lam=15
                sens[('lam',15,drift,seed)] = sens[('det','ph',drift,seed)]
                if drift:
                    sens[('cd',48,True,seed)] = sens[('det','ph',True,seed)]
                    sens[('win',4,True,seed)] = sens[('det','ph',True,seed)]
                    sens[('mag',1.0,True,seed)] = sens[('det','ph',True,seed)]
    print('det', det, round(time.time()-t0), flush=True)
    pickle.dump(sens, open('sens.pkl','wb'))
for lam in (6, 10, 25, 40):
    for seed in range(5):
        for drift in (True, False):
            run(('lam',lam,drift,seed), seed=seed, drift=drift, lam_f=float(lam))
    print('lam', lam, round(time.time()-t0), flush=True)
for cd in (12, 24, 96, 168):
    for seed in range(5):
        run(('cd',cd,True,seed), seed=seed, drift=True, cooldown=cd)
    print('cd', cd, round(time.time()-t0), flush=True)
for w in (2, 6, 8):
    for seed in range(5):
        run(('win',w,True,seed), seed=seed, drift=True, win=w*HPW)
    print('win', w, round(time.time()-t0), flush=True)
for m in (0.0, 0.1, 0.25, 0.5, 1.5):
    for seed in range(5):
        run(('mag',m,True,seed), seed=seed, drift=(m>0), magnitude=max(m,1e-9))
    print('mag', m, round(time.time()-t0), flush=True)
pickle.dump(sens, open('sens.pkl','wb'))
print('DONE')
