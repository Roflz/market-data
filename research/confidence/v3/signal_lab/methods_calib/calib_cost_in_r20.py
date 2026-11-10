# round-trip cost in R20 units and sd of forward returns in R20 units, per market / timeframe / era (one file at a time)
import numpy as np, pandas as pd, gc
SPEC = {'ES': (5.0, 0.25), 'NQ': (2.0, 0.25), 'YM': (0.5, 1.0)}
for sym in ['ES', 'NQ', 'YM']:
    usd_pt, tick = SPEC[sym]
    cost_pts = (2 * 1.0) / usd_pt + 2 * tick         # $1 each way + 1 tick each way
    for tf in [5, 15, 60]:
        b = pd.read_parquet(f'v3/data/bars_{sym}_{tf}.parquet', columns=['O', 'H', 'L', 'C', 'session'])
        r20 = (b.H - b.L).rolling(20).mean()
        g = b.groupby('session')
        on = g.O.shift(-1)
        f1 = (g.C.shift(-1) - on) / r20; f4 = (g.C.shift(-4) - on) / r20
        rth = (b.index.hour * 60 + b.index.minute >= 570) & (b.index.hour < 16)
        out = []
        for era, m in [('10-17', b.index < '2018-01-01'), ('18-25H1', b.index >= '2018-01-01')]:
            if m.sum() == 0: continue
            c_all = np.nanmedian(cost_pts / r20[m]); c_rth = np.nanmedian(cost_pts / r20[m & rth])
            out.append(f'{era}: cost/R20 median all {c_all:.2f} RTH {c_rth:.2f} | sd fwd1 {np.nanstd(f1[m]):.2f} fwd4 {np.nanstd(f4[m]):.2f} R20 | median R20 {np.nanmedian(r20[m]):.2f} pts')
        print(f'{sym} {tf:>2}m cost {cost_pts:.2f} pts:  ' + '  ||  '.join(out))
        del b; gc.collect()
