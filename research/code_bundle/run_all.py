import pickle, numpy as np, time, sys
from sim import *
def slim(o, keep_arrays=False):
    r = {k: o[k] for k in ('mu0','s0','delay','false_alarms')}
    for k in ('static','weekly','adaptive'):
        r[k] = {kk:vv for kk,vv in o[k].items() if kk not in ('pred','trace')}
    return r
main = {}
t0=time.time()
for drift in (True, False):
    for seed in range(10):
        o = experiment(seed, drift=drift, record=(seed==0))
        r = slim(o)
        if seed == 0:   # keep arrays for figures
            r['arrays'] = dict(y=o['y'], p_static=o['static']['pred'], p_adapt=o['adaptive']['pred'],
                p_weekly=o['weekly']['pred'], v=o['D']['v'], v_true=o['D']['v_true'], d=o['D']['d'], temp=o['D']['temp'],
                p=o['D']['p'], p_clean=o['D']['p_clean'], onset=o['D']['onset'], trace=o['adaptive']['trace'],
                alarms=o['adaptive']['alarms'], sources=o['adaptive']['sources'], cal=o['cal'], i0=o['i0'])
            # feature importance via permutation on a stream slice
        main[(drift, seed)] = r
        print('main', drift, seed, round(time.time()-t0), flush=True)
pickle.dump(main, open('main.pkl','wb'))

sens = {}
# detector comparison (drift scenario, 5 seeds)
for det in ('ph','cusum','adwin','kspsi'):
    for seed in range(5):
        for drift in (True, False):
            o = experiment(seed, drift=drift, detector=det, do_weekly=False, use_input=(det!='adwin'))
            sens[('det',det,drift,seed)] = slim(o)
    print('det', det, round(time.time()-t0), flush=True)
# lambda sweep
for lam in (6, 10, 15, 25, 40):
    for seed in range(5):
        for drift in (True, False):
            o = experiment(seed, drift=drift, do_weekly=False, lam_f=float(lam))
            sens[('lam',lam,drift,seed)] = slim(o)
    print('lam', lam, round(time.time()-t0), flush=True)
# cooldown sweep
for cd in (12, 24, 48, 96, 168):
    for seed in range(5):
        o = experiment(seed, drift=True, do_weekly=False, cooldown=cd)
        sens[('cd',cd,True,seed)] = slim(o)
    print('cd', cd, round(time.time()-t0), flush=True)
# window sweep
for w in (2, 4, 6, 8):
    for seed in range(5):
        o = experiment(seed, drift=True, do_weekly=False, win=w*HPW)
        sens[('win',w,True,seed)] = slim(o)
    print('win', w, round(time.time()-t0), flush=True)
# magnitude sweep
for m in (0.0, 0.1, 0.25, 0.5, 1.0, 1.5):
    for seed in range(5):
        o = experiment(seed, drift=(m>0), magnitude=max(m,1e-9), do_weekly=False)
        sens[('mag',m,True,seed)] = slim(o)
    print('mag', m, round(time.time()-t0), flush=True)
pickle.dump(sens, open('sens.pkl','wb'))
print('DONE')
