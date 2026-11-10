"""
Tighter stops for the LucidFlex evaluation, combined with the shorter-hold variants of eval_short_trades.py.
Same method and pass-rate rules (today's prices, 1 micro, starts 2018-2026, EOD trailing $1,000, target $1,250, 40%
consistency, daily loss limit not modelled). Overnight-break stop: multiple of the live 2 x ATR (0.5 = 1 ATR) or a cap as
a share of price. Opening range: multiple of the first candle or a cap.
Usage: PYTHONPATH=./pylib:. python3 research/eval_tight_stops.py
"""
import numpy as np, pandas as pd
import research_lib as rl
src = open('research/eval_short_trades.py').read()
ns = {'np': np, 'pd': pd, 'rl': rl}
exec(src.split('rows, exp = [], onem')[0].split('import research_lib as rl')[1], ns)
today, daily, row, paths, cal = ns['today'], ns['daily'], ns['row'], ns['paths'], ns['cal']

def onb(stop, exit_time=None, entry_before=None):
    r = rl.replay('overnight_break', exit_time=exit_time or '16:45', **stop)
    ent = pd.DatetimeIndex(paths['ts'][r.path_row.to_numpy(), 0]); hm = ent.hour * 100 + ent.minute
    keep = np.ones(len(r), bool)
    if exit_time: keep &= hm < int(exit_time.replace(':', ''))
    if entry_before: keep &= hm < entry_before
    r = r[keep]; r = r[pd.to_datetime(r.date) >= '2018-01-01']
    return r.assign(usd_today=today(r))

exp = rl.replay('expiry_fade'); exp = exp[pd.to_datetime(exp.date) >= '2018-01-01']; exp = exp.assign(usd_today=today(exp))
STOPS = {'2 ATR (now)': {}, '1.5 ATR': {'stop_mult': 0.75}, '1 ATR': {'stop_mult': 0.5},
         'cap 0.20%': {'stop_cap_frac': 0.0020}, 'cap 0.15%': {'stop_cap_frac': 0.0015}, 'cap 0.10%': {'stop_cap_frac': 0.0010}}
HOLDS = {'hold to 16:45': {}, 'exit 10:30': {'exit_time': '10:30'}, '9:xx entries only': {'entry_before': 1000}}
rows = []
for hname, h in HOLDS.items():
    for sname, s in STOPS.items():
        o = onb(s, **h)
        rows.append(row(f'ONB {hname}, stop {sname}', daily(o), len(o)))
        rows.append(row(f'  + expiry', daily(o, exp), len(o) + len(exp)))
for sname, s in {'1 candle (now)': {}, '0.75 candle': {'stop_mult': 0.75}, '0.5 candle': {'stop_mult': 0.5},
                 'cap 0.10%': {'stop_cap_frac': 0.0010}}.items():
    for t in (None, '10:30'):
        r = rl.replay('opening_range', exit_time=t, **s); r = r[pd.to_datetime(r.date) >= '2018-01-01']
        r = r.assign(usd_today=today(r))
        rows.append(row(f'ORB {"hold" if t is None else "exit " + t}, stop {sname}', daily(r), len(r)))
R = pd.DataFrame(rows); R.to_csv('research/eval_tight_stops_results.csv', index=False)
f = {c: '{:.0%}'.format for c in ('pass_all', 'pass_18_21', 'pass_22_26')}
f.update({c: '{:,.0f}'.format for c in ('net_yr', 'worst_day', 'max_dd', 'trades_yr')}, day_mean='{:+.1f}'.format,
         day_sd='{:.0f}'.format, edge_per_var='{:+.2f}'.format, days='{:.0f}'.format)
pd.set_option('display.width', 220); print(R.to_string(index=False, formatters=f))
