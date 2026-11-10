"""
Shorter holds for the LucidFlex evaluation: does exiting earlier cut variance more than it cuts edge?
For each variant: daily mean and standard deviation of P&L at 1 micro (rescaled to today's NQ price), the
'edge per unit of variance' (mean / variance: the number that sets the odds of hitting a $ target before a $ loss
limit), worst day, max drawdown, and LucidFlex 25K pass rates (EOD trailing $1,000, target $1,250, 40% consistency;
daily loss limit not modelled). Starts on every trading day 2018-2026.
Uses research_lib.replay (exact engine fills). Overnight-break variants with a clock exit drop signals that would
enter at or after the exit time (you would not take a trade that must exit at once).
Usage: PYTHONPATH=./pylib:. python3 research/eval_short_trades.py
"""
import numpy as np, pandas as pd
import research_lib as rl

P_NOW, START, TARGET, MLL, LOCK_TRIGGER, LOCK_AT = 27_100.0, 25_000.0, 1_250.0, 1_000.0, 26_100.0, 25_100.0
cal = pd.DatetimeIndex(sorted(rl.live_trades().date.unique()))
cal = cal[cal >= '2018-01-01']
paths = rl.trade_paths('overnight_break')

def today(df):
    px = 1e4 * df.net_pts / df.bp
    return (((df.net_pts + 1.0) / px) * P_NOW * 2 - 2.0).where(df.bp != 0, -2.0)

def onb(exit_time=None, entry_before=None):
    r = rl.replay('overnight_break', exit_time=exit_time or '16:45')
    ent = pd.DatetimeIndex(paths['ts'][r.path_row.to_numpy(), 0])
    hm = ent.hour * 100 + ent.minute
    keep = np.ones(len(r), bool)
    if exit_time: keep &= hm < int(exit_time.replace(':', ''))
    if entry_before: keep &= hm < entry_before
    return r[keep].assign(usd_today=lambda x: today(x))

def onem(model, exit_time=None):
    return rl.replay(model, exit_time=exit_time).assign(usd_today=lambda x: today(x))

def daily(*frames):
    x = pd.concat(frames); x['date'] = pd.to_datetime(x.date)
    return x.groupby('date').usd_today.sum().reindex(cal, fill_value=0.0)

def passrate(v):
    v = v.to_numpy(); n = len(v); res = []
    for s in range(n):
        bal, hi, best, locked, out, d = START, START, 0.0, False, 'open', 0
        for i in range(s, n):
            d += 1; bal += v[i]; best = max(best, v[i]); hi = max(hi, bal); locked = locked or hi > LOCK_TRIGGER
            if bal <= (LOCK_AT if locked else hi - MLL): out = 'fail'; break
            p = bal - START
            if p >= TARGET and best <= 0.40 * p: out = 'pass'; break
        res.append((out, d))
    r = pd.DataFrame(res, columns=['out', 'days'], index=cal); done = r[r.out != 'open']
    rate = lambda a, b: (done.loc[a:b].out == 'pass').mean()
    return (done.out == 'pass').mean(), rate('2018', '2021'), rate('2022', '2026'), done[done.out == 'pass'].days.median()

def row(name, dly, n_trades):
    traded = dly[dly != 0]
    mu, sd = dly.mean(), dly.std()
    cum = dly.cumsum(); dd = (np.maximum.accumulate(np.r_[0, cum.to_numpy()])[1:] - cum.to_numpy()).max()
    p, p1, p2, days = passrate(dly)
    yrs = (cal[-1] - cal[0]).days / 365.25
    return dict(variant=name, trades_yr=n_trades / yrs, net_yr=dly.sum() / yrs, day_mean=mu, day_sd=sd,
                edge_per_var=1e4 * mu / sd ** 2, worst_day=dly.min(), max_dd=dd, pass_all=p, pass_18_21=p1, pass_22_26=p2, days=days)

rows, exp = [], onem('expiry_fade')
exp = exp[pd.to_datetime(exp.date) >= '2018-01-01']
for t in (None, '10:30', '11:00', '12:00', '13:00', '14:00', '15:00'):
    o = onb(t); o = o[pd.to_datetime(o.date) >= '2018-01-01']
    lab = 'close (16:45)' if t is None else t
    rows.append(row(f'ONB exit {lab}', daily(o), len(o)))
    rows.append(row(f'ONB exit {lab} + expiry', daily(o, exp), len(o) + len(exp)))
o = onb(None, entry_before=1000); o = o[pd.to_datetime(o.date) >= '2018-01-01']
rows.append(row('ONB 9:xx entries only, close', daily(o), len(o)))
rows.append(row('ONB 9:xx entries only + expiry', daily(o, exp), len(o) + len(exp)))
for t in ('10:00', '10:30', '11:00', '12:00', '13:00', '14:00', '15:00', None):
    r = onem('opening_range', t); r = r[pd.to_datetime(r.date) >= '2018-01-01']
    rows.append(row(f'ORB exit {t or "close (15:59)"}', daily(r), len(r)))
rows.append(row('expiry fade alone', daily(exp), len(exp)))
R = pd.DataFrame(rows); R.to_csv('research/eval_short_trades_results.csv', index=False)
f = {c: '{:.0%}'.format for c in ('pass_all', 'pass_18_21', 'pass_22_26')}
f.update({c: '{:,.0f}'.format for c in ('net_yr', 'worst_day', 'max_dd', 'trades_yr')}, day_mean='{:+.1f}'.format,
         day_sd='{:.0f}'.format, edge_per_var='{:+.2f}'.format, days='{:.0f}'.format)
pd.set_option('display.width', 220); print(R.to_string(index=False, formatters=f))
