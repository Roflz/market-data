"""
LucidFlex 25K evaluation: ways to cut drawdown, replayed trade by trade (trade times from a paper_log.py backfill).
Rules as research/prop_lucid_flex.py, plus Lucid's daily loss limit (DLL on, $600 for 25K per third-party sources;
soft breach: no more trading that day). Within a day, trades are processed in time order. Approximation: daily stops
react to REALIZED P&L when a trade closes; an open trade is not closed early by a daily stop (slightly optimistic).
Money: each trade rescaled to today's NQ price (27,100), 1 micro unless stated.
Usage: PYTHONPATH=./pylib python3 research/prop_lucid_flex_dd.py <paper_log backfill csv>
"""
import sys, itertools
import numpy as np, pandas as pd

START, TARGET, MLL, LOCK_TRIGGER, LOCK_AT, LUCID_DLL = 25_000.0, 1_250.0, 1_000.0, 26_100.0, 25_100.0, 600.0
P_NOW = 27_100.0
L = pd.read_csv(sys.argv[1])
L = L[(L.kind == 'live') & L.signal.isin(['long', 'short'])].copy()
L['usd_today'] = ((L.net_pts + 1.0) / L.entry_px) * P_NOW * 2 - 2.0
L['date'] = pd.to_datetime(L.date)
L['ent'] = L.entry_time.str.replace(':', '').astype(int); L['ext'] = L.exit_time.str.replace(':', '').astype(int)
cal = pd.DatetimeIndex(sorted(pd.to_datetime(pd.read_csv(sys.argv[1]).date).unique()))

def daily_pnl(models, day_stop, day_goal, onb_max, micros=1):
    """Day P&L series after intraday rules."""
    x = L[L.model_or_lead.isin(models)].sort_values(['date', 'ent', 'ext'])
    out = {}
    for d, g in x.groupby('date'):
        realized, closed, n_onb = 0.0, [], 0
        for r in g.itertuples(index=False):
            done = sum(p for t, p in closed if t <= r.ent)          # realized before this entry
            if done <= -min(day_stop, LUCID_DLL) or (day_goal and done >= day_goal):
                continue
            if r.model_or_lead == 'overnight_break':
                if n_onb >= onb_max: continue
                n_onb += 1
            closed.append((r.ext, r.usd_today * micros))
        out[d] = sum(p for _, p in closed)
    return pd.Series(out).reindex(cal, fill_value=0.0)

def evaluate(daily, cons=0.40):
    v = daily.to_numpy(); n = len(v); res = []
    for s in range(n):
        bal, hi, best, locked, out, d = START, START, 0.0, False, 'open', 0
        for i in range(s, n):
            d += 1; bal += v[i]; best = max(best, v[i]); hi = max(hi, bal)
            locked = locked or hi > LOCK_TRIGGER
            if bal <= (LOCK_AT if locked else hi - MLL): out = 'fail'; break
            p = bal - START
            if p >= TARGET and best <= cons * p: out = 'pass'; break
        res.append((out, d))
    return pd.DataFrame(res, columns=['out', 'days'], index=daily.index)

SETS = {'all 3': ['overnight_break', 'opening_range', 'expiry_fade'],
        'ONB + expiry': ['overnight_break', 'expiry_fade'],
        'ONB + ORB': ['overnight_break', 'opening_range'], 'ONB only': ['overnight_break']}
rows = []
for (sname, models), stop, goal, onb_max in itertools.product(SETS.items(), [600, 400, 300, 200, 150], [0, 500, 400, 300], [3, 1]):
    dly = daily_pnl(models, stop, goal, onb_max)
    r = evaluate(dly); done = r[r.out != 'open']
    def rate(a, b):
        z = done.loc[a:b]; return (z.out == 'pass').mean()
    rows.append(dict(models=sname, day_stop=stop, day_goal=goal or None, onb_per_day=onb_max,
                     pass_all=(done.out == 'pass').mean(), pass_2018_21=rate('2018', '2021'), pass_2022_26=rate('2022', '2026'),
                     pass_2024_26=rate('2024', '2026'), days_to_pass=done[done.out == 'pass'].days.median(),
                     worst_day=dly.min(), net_per_year=dly.sum() / ((cal[-1] - cal[0]).days / 365.25)))
R = pd.DataFrame(rows)
R.to_csv('research/prop_lucid_flex_dd_results.csv', index=False)
base = R[(R.day_stop == 600) & R.day_goal.isna() & (R.onb_per_day == 3)]
f = {c: '{:.0%}'.format for c in ('pass_all', 'pass_2018_21', 'pass_2022_26', 'pass_2024_26')}
f.update(worst_day='{:,.0f}'.format, net_per_year='{:,.0f}'.format)
pd.set_option('display.width', 220)
print("BASELINE per model set (Lucid DLL $600 only, no extra rules)"); print(base.to_string(index=False, formatters=f))
R['min_era'] = R[['pass_2018_21', 'pass_2022_26']].min(axis=1)
print("\nTOP 15 by the WORSE of the two eras (must hold in both 2018-21 and 2022-26)")
print(R.sort_values('min_era', ascending=False).head(15).drop(columns='min_era').to_string(index=False, formatters=f))
for s in SETS:
    x = R[R.models == s]; b = x[(x.day_stop == 600) & x.day_goal.isna() & (x.onb_per_day == 3)].iloc[0]
    print(f"\n{s}: effect of each lever alone vs baseline {b.pass_all:.0%} (2018-21 {b.pass_2018_21:.0%}, 2022-26 {b.pass_2022_26:.0%})")
    for lab, m in (('day stop', (x.day_goal.isna()) & (x.onb_per_day == 3)), ('day goal', (x.day_stop == 600) & (x.onb_per_day == 3)),
                   ('1 ONB/day', (x.day_stop == 600) & x.day_goal.isna())):
        print('  ' + lab + ': ' + ', '.join(f"{(r.day_stop if lab=='day stop' else r.day_goal if lab=='day goal' else r.onb_per_day)}->{r.pass_all:.0%}/{r.pass_2018_21:.0%}/{r.pass_2022_26:.0%}" for r in x[m].itertuples()))
