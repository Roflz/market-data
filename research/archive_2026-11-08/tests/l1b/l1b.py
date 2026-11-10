"""L1b: jobs-report / CPI fade with alternative exits. Signal = 8:44 close - 8:30 open; fade at the 8:45 open,
exit at the open of the exit bar. 1 tick slippage each way + $1 commission. Skip if roll or >5 missing minutes
between 8:30 and the exit bar."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, '.')
import calendar_days as cd
S = '/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests'
nfp = set(pd.to_datetime(pd.read_csv(f'{S}/s13_X/nfp_dates.csv').date))
cpi = cd.cpi_days()
SPEC = {'NQ': (2.0, 0.25, 1.0), 'ES': (5.0, 0.25, 1.0)}   # $/pt, tick, commission

def load(sym):
    d = pd.read_csv(f'data/{sym}_fut_1m.csv', usecols=['ts_event', 'Open', 'Close', 'instrument_id'])
    d = d[d.ts_event >= '2009-12-31']
    t = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert('America/New_York')
    d = d.assign(day=t.dt.tz_localize(None).dt.normalize(), hm=t.dt.hour * 100 + t.dt.minute)
    d = d[(d.hm >= 830) & (d.hm <= 945)]
    return d

def run(d, sym, days, exit_hm):
    ppt, tick, comm = SPEC[sym]
    rows = []
    for day, g in d[d.day.isin(days)].groupby('day'):
        g = g.set_index('hm')
        need = [830, 844, 845, exit_hm]
        if any(h not in g.index for h in need):
            continue
        w = g.loc[830:exit_hm]
        mins = [h // 100 * 60 + h % 100 for h in w.index]
        if w.instrument_id.nunique() > 1 or np.max(np.diff(mins)) > 6:
            continue
        sig = g.Close[844] - g.Open[830]
        if sig == 0:
            continue
        dr = -np.sign(sig)
        ent = g.Open[845] + dr * tick
        ex = g.Open[exit_hm] - dr * tick
        pts = dr * (ex - ent) - comm / ppt
        rows.append(dict(date=day, side='long' if dr > 0 else 'short', entry=ent, exit=ex, net_pts=pts,
                         usd=pts * ppt, bp=1e4 * pts / g.Open[845]))
    return pd.DataFrame(rows)

def stat(x, label):
    u = x.usd
    t = u.mean() / (u.std(ddof=1) / np.sqrt(len(u))) if len(u) > 2 else np.nan
    top5 = u.nlargest(5).sum()
    print(f'{label:44s} n={len(u):4d}  ${u.mean():+7.2f}/trade  total ${u.sum():+9.1f}  t={t:+.2f}  '
          f'median ${u.median():+.1f}  win {np.mean(u > 0):.0%}  without top5 ${u.sum() - top5:+.0f}')
    return t

NQ, ES = load('NQ'), load('ES')
cut = pd.Timestamp('2018-01-01')
nfp_late = {x for x in nfp if x >= cut}; nfp_early = {x for x in nfp if x < cut}
cpi_late = {x for x in cpi if x >= cut}
for ex in (945, 935, 930):
    print(f'---- exit at the {ex // 100}:{ex % 100:02d} open')
    a = run(NQ, 'NQ', nfp_late, ex); stat(a, 'MNQ jobs days 2018-2026')
    b = run(ES, 'ES', nfp_late, ex); stat(b, 'MES jobs days 2018-2026')
    stat(run(NQ, 'NQ', nfp_early, ex), 'MNQ jobs days 2010-2017 (report)')
    stat(run(NQ, 'NQ', cpi_late, ex), 'MNQ CPI days 2018-2026 (report)')
    a.to_csv(f'{S}/l1b/L1b_MNQ_nfp_exit{ex}.csv', index=False)
    print(a.groupby(a.date.dt.year).usd.sum().round(0).to_dict())
