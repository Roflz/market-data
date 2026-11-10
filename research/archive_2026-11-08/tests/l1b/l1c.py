"""L1c: jobs-day filter for the live breakouts (pre-registered in the review doc, section 13)."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, '.')
import calendar_days as cd
S = '/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/tests'
nfp = set(pd.to_datetime(pd.read_csv(f'{S}/s13_X/nfp_dates.csv').date)); cpi = cd.cpi_days()
d = pd.read_csv('data/NQ_fut_1m.csv', usecols=['ts_event', 'Open', 'Close', 'instrument_id'])
d = d[d.ts_event >= '2010-06-01']
t = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert('America/New_York')
d = d.assign(day=t.dt.tz_localize(None).dt.normalize(), hm=t.dt.hour * 100 + t.dt.minute)
d = d[d.hm.isin([830, 844]) & d.day.isin(nfp | cpi)]
fade = {}
for day, g in d.groupby('day'):
    g = g.set_index('hm')
    if 830 in g.index and 844 in g.index and g.instrument_id.nunique() == 1:
        mv = g.Close[844] - g.Open[830]
        if mv != 0: fade[day] = 'short' if mv > 0 else 'long'
T = pd.read_csv('chosen_models_trades.csv', parse_dates=['date'])
T = T[T.model.isin(['opening_range', 'overnight_break'])]
T['fade'] = T.date.map(fade)
def welch(a, b):
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
def report(sub, label):
    s = sub[sub.fade.notna()]
    keep, skip = s[s.side == s.fade], s[s.side != s.fade]
    tt = welch(keep.usd, skip.usd) if len(keep) > 2 and len(skip) > 2 else np.nan
    print(f'{label:42s} keep n={len(keep):3d} ${keep.usd.mean():+7.2f}/tr (${keep.usd.sum():+7.0f})  '
          f'skip n={len(skip):3d} ${skip.usd.mean():+7.2f}/tr (${skip.usd.sum():+7.0f})  t={tt:+.2f}  '
          f'R keep {keep.R.mean():+.2f} skip {skip.R.mean():+.2f}')
    return keep, skip, tt
late, early = T.date >= '2018-01-01', T.date < '2018-01-01'
isn, isc = T.date.isin(nfp), T.date.isin(cpi)
print('JUDGED: jobs days 2018-2026, both models')
k, s, tt = report(T[late & isn], 'both models')
print(f'  pass = skipped avg < 0 ({s.usd.mean() < 0}) and t >= 2 ({tt >= 2}) -> {"PASS" if s.usd.mean() < 0 and tt >= 2 else "FAIL"}')
print('  by year (skipped trades $):', s.groupby(s.date.dt.year).usd.sum().round(0).to_dict())
print('  by year (kept trades $):   ', k.groupby(k.date.dt.year).usd.sum().round(0).to_dict())
print('REPORT ONLY')
for m in ('opening_range', 'overnight_break'):
    report(T[late & isn & (T.model == m)], f'{m} jobs 2018-26')
report(T[early & isn], 'both, jobs days 2010-2017')
report(T[late & isc], 'both, CPI days 2018-2026')
report(T[early & isc], 'both, CPI days 2010-2017')
