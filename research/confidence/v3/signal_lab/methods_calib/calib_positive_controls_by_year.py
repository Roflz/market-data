import numpy as np, pandas as pd
from scipy.stats import spearmanr
def ic(x, y):
    m = np.isfinite(x) & np.isfinite(y); return spearmanr(x[m], y[m])[0], int(m.sum())
for sym in ['ES', 'NQ', 'YM']:
    b = pd.read_parquet(f'v3/data/bars_{sym}_15.parquet')
    b['rng'] = b.H - b.L; b['slot'] = b.index.hour * 4 + b.index.minute // 15
    b['prof'] = b.slot.map(b.groupby('slot').rng.median())
    g = b.groupby('session')
    b['ret'] = b.C - b.O; b['ret_next'] = g.ret.shift(-1); b['r20'] = b.rng.rolling(20).mean()
    b['O_next'] = g.O.shift(-1)
    b['back4'] = b.C - g.O.shift(3)
    hh = pd.concat([g.H.shift(-k) for k in range(1, 5)], axis=1).max(axis=1); ll = pd.concat([g.L.shift(-k) for k in range(1, 5)], axis=1).min(axis=1)
    b['y_lev'] = (hh - ll) / sum(g.prof.shift(-k) for k in range(1, 5)); b['x_lev'] = b.back4 / b.r20
    yr = b.index.year
    rev = [ic(b.ret.values[yr == y], b.ret_next.values[yr == y])[0] for y in range(2010, 2026)]
    lev = [ic(b.x_lev.values[yr == y], b.y_lev.values[yr == y])[0] for y in range(2010, 2026)]
    print(sym, 'next-bar reversal IC by year:', ' '.join(f'{v:+.3f}' for v in rev), '| neg years', sum(v < 0 for v in rev), '/16')
    print(sym, 'leverage IC by year:        ', ' '.join(f'{v:+.3f}' for v in lev), '| neg years', sum(v < 0 for v in lev), '/16')
    # 8:30 bar on first Friday of month (proxy for payrolls day) vs other weekdays
    d = b[(b.index.hour == 8) & (b.index.minute == 30)].copy()
    d['ff'] = (d.index.dayofweek == 4) & (d.index.day <= 7)
    pre = b[(b.index.hour == 8) & (b.index.minute == 15)].rng
    print(sym, '8:30 bar median range: first-Friday %.2f vs other days %.2f (ratio %.2f); 8:15 bar %.2f' % (d[d.ff].rng.median(), d[~d.ff].rng.median(), d[d.ff].rng.median() / d[~d.ff].rng.median(), pre.median()))
    S = pd.read_parquet(f'v3/data/sessions_{sym}.parquet')
    cols = [f'px_{k}' for k in ['0930', '1000', '1030', '1100', '1200', '1300', '1400', '1500', '1600']]
    rr = (S[cols].max(axis=1) - S[cols].min(axis=1)); lr = np.log(rr + 1e-9)
    m = np.isfinite(lr) & np.isfinite(lr.shift(1)) & (rr > 0) & (rr.shift(1) > 0)
    print(sym, 'DAY vol clustering corr(log RTH mark-range yesterday, today) = %.2f  n %d' % (np.corrcoef(lr.shift(1)[m], lr[m])[0, 1], m.sum()))
