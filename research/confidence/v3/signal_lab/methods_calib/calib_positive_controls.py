"""Quick calibration of candidate POSITIVE CONTROLS on v3 15-min bars + sessions (pre-holdout data only)."""
import numpy as np, pandas as pd, sys
from scipy.stats import spearmanr
sys.path.insert(0, 'v3')
import stats_protocol as sp

def ic(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    return spearmanr(x[m], y[m])[0], int(m.sum())

def sess_ic_t(df, xcol, ycol):
    # per-session Spearman IC, then t of the mean over sessions with Newey-West (Fama-MacBeth analogue)
    g = df.dropna(subset=[xcol, ycol]).groupby('session')
    v = g.apply(lambda d: spearmanr(d[xcol], d[ycol])[0] if len(d) > 8 else np.nan).dropna().values
    t, se, _ = sp.hac_t(v)
    return v.mean(), t, len(v)

for sym in ['ES', 'NQ']:
    b = pd.read_parquet(f'v3/data/bars_{sym}_15.parquet')
    b['rng'] = b.H - b.L
    b['slot'] = b.index.hour * 4 + b.index.minute // 15
    b['r20'] = b.rng.rolling(20, min_periods=20).mean()
    prof = b.groupby('slot').rng.median()
    b['prof'] = b.slot.map(prof)
    g = b.groupby('session')
    b['rng_next'] = g.rng.shift(-1)
    b['prof_next'] = g.prof.shift(-1)
    b['ret'] = (b.C - b.O)
    b['ret_next'] = g.ret.shift(-1)
    # forward 4 bars, starting next bar open
    b['O_next'] = g.O.shift(-1); b['C_4'] = g.C.shift(-4)
    b['fwd4'] = b.C_4 - b.O_next
    b['back4'] = b.C - g.O.shift(3)
    hh = pd.concat([g.H.shift(-k) for k in range(1, 5)], axis=1).max(axis=1)
    ll = pd.concat([g.L.shift(-k) for k in range(1, 5)], axis=1).min(axis=1)
    b['frng4'] = hh - ll
    b['prof4'] = sum(g.prof.shift(-k) for k in range(1, 5))
    print(f'===== {sym} 15-min, {b.session.nunique()} sessions {b.index[0].date()}..{b.index[-1].date()}')
    # 1. time-of-day profile
    p = prof
    def sl(h, m): return h * 4 + m // 15
    print('TOD median range (pts): 03:00 %.2f | 08:15 %.2f | 08:30 %.2f | 09:30 %.2f | 12:00 %.2f | 15:45 %.2f | 16:30 %.2f | 20:00 %.2f' % tuple(
        p[sl(h, m)] for h, m in [(3, 0), (8, 15), (8, 30), (9, 30), (12, 0), (15, 45), (16, 30), (20, 0)]))
    # ratio by era
    for era, m in [('2010-17', b.index < '2018-01-01'), ('2018-25H1', b.index >= '2018-01-01')]:
        pe = b[m].groupby('slot').rng.median()
        print(f'  {era}: 08:30/08:15 = {pe[sl(8,30)]/pe[sl(8,15)]:.2f}  09:30/12:00 = {pe[sl(9,30)]/pe[sl(12,0)]:.2f}  09:30/03:00 = {pe[sl(9,30)]/pe[sl(3,0)]:.2f}')
    # 2. vol clustering
    x = (b.r20 / b.prof).values; y = (b.rng_next / b.prof_next).values
    print('VOL CLUSTERING  IC(R20/slot-profile, next-bar range/slot-profile) pooled = %.3f (n=%d)' % ic(x, y))
    b['x_vc'] = x; b['y_vc'] = y
    print('   per-session mean IC %.3f  NW t %.1f  sessions %d' % sess_ic_t(b, 'x_vc', 'y_vc'))
    print('   raw IC(R20, next range) (incl. time-of-day) = %.3f' % ic(b.r20.values, b.rng_next.values)[0])
    print('   IC(this bar range/prof, next range/prof) = %.3f' % ic((b.rng / b.prof).values, y)[0])
    # 3. leverage effect: signed past 4-bar return (R20 units) vs next 4-bar range (deseasonalised)
    xl = (b.back4 / b.r20).values; yl = (b.frng4 / b.prof4).values
    print('LEVERAGE  IC(past-4-bar return in R20, next-4-bar range / profile) = %.3f (expect < 0)' % ic(xl, yl)[0])
    # 4. direction: next-bar return vs this bar return, and back4 vs fwd4 (R20 units)
    print('DIRECTION  IC(bar ret, next bar ret) = %.4f ; IC(back4, fwd4) = %.4f' % (ic(b.ret.values, b.ret_next.values)[0], ic(b.back4.values, (b.fwd4 / b.r20).values)[0]))
    # 5. sessions-based: overnight drift, Euro-open hour, intraday momentum
    S = pd.read_parquet(f'v3/data/sessions_{sym}.parquet')
    S = S[S.index < '2025-06-30'] if isinstance(S.index, pd.DatetimeIndex) else S
    def r(a, c): return (S[f'px_{c}'] - S[f'px_{a}'])
    rng_day = (S['px_1645'] - S['px_1800']).abs()
    for nm, a, c in [('overnight 18:00-09:30', '1800', '0930'), ('Euro open 02:00-03:00', '0200', '0300'), ('RTH 09:30-16:00', '0930', '1600'), ('16:00-16:45', '1600', '1645')]:
        v = r(a, c).dropna()
        for era, m in [('2010-17', v.index < '2018-01-01'), ('2018-20', (v.index >= '2018-01-01') & (v.index < '2021-01-01')), ('2021-25H1', v.index >= '2021-01-01')]:
            vv = v[m].values
            t = vv.mean() / (vv.std(ddof=1) / np.sqrt(len(vv)))
            print(f'  {nm:24s} {era}: mean {vv.mean():+.2f} pts/session  t {t:+.1f}  n {len(vv)}')
    # Gao et al.: 16:00(prev)->10:00 return predicts 15:30-16:00 return.  In sessions table: px_1800 ~ prev evening; use 1800->1000
    f = r('1800', '1000'); l = r('1530', '1600')
    m = f.notna() & l.notna()
    for era, mm in [('2010-17', m & (f.index < '2018-01-01')), ('2018-25H1', m & (f.index >= '2018-01-01'))]:
        c = np.corrcoef(f[mm], l[mm])[0, 1]
        print(f'  INTRADAY MOMENTUM corr(18:00->10:00, 15:30->16:00) {era}: {c:+.3f} n {mm.sum()}  (t ~ {c*np.sqrt(mm.sum()):+.1f})')
    # day-level vol clustering: yesterday's 9:30-16:00 abs range proxy vs today
    rr = (S[[f'px_{k}' for k in ['0930', '1000', '1030', '1100', '1200', '1300', '1400', '1500', '1600']]].max(axis=1) - S[[f'px_{k}' for k in ['0930', '1000', '1030', '1100', '1200', '1300', '1400', '1500', '1600']]].min(axis=1))
    print('  DAY VOL CLUSTERING corr(log RTH mark-range yesterday, today) = %.2f' % np.corrcoef(np.log(rr.shift(1)[1:] + 0.25), np.log(rr[1:] + 0.25))[0, 1])
