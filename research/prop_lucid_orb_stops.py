"""
LucidFlex 25K evaluation pass rates with wider opening-range stops (1x-4x the first candle), using research_lib.
Overnight break is flattened at 16:45 ET (Lucid's auto-close). Lucid daily loss limit $600 on; trades processed in time
order within each day; money rescaled to today's NQ price; 1 micro; starts on every trading day 2018-2026.
Usage: PYTHONPATH=./pylib python3 research/prop_lucid_orb_stops.py
"""
import sys
import numpy as np, pandas as pd
import research_lib as rl
sys.argv = ['x', '/dev/null']
src = open('research/prop_lucid_flex_dd.py').read()
ns = {}
exec(src.split("L = pd.read_csv")[0], ns)                          # constants
exec("def evaluate" + src.split("def evaluate")[1].split("SETS =")[0], ns)
evaluate = ns['evaluate']; P_NOW, DLL = ns['P_NOW'], ns['LUCID_DLL']

live = rl.live_trades(include_skipped=False)
tcol = [c for c in live.columns if 'entry' in c and 'time' in c][0]
def to_today(df):
    px = 1e4 * df.net_pts / df.bp
    out = ((df.net_pts + 1.0) / px) * P_NOW * 2 - 2.0
    return out.where(df.bp != 0, -2.0)

def frame(model, **kw):
    r = rl.replay(model, **kw)
    lt = live[live.model == model][['path_row', 'date', tcol]]
    r = r.merge(lt, on=['path_row', 'date'], how='left')
    if r[tcol].isna().any():                                        # trades not in the live set (e.g. re-entries): fall back
        r[tcol] = r[tcol].fillna(pd.to_datetime(r.date) + pd.Timedelta(hours=9, minutes=35))
    hm = lambda s: pd.to_datetime(s).dt.hour * 100 + pd.to_datetime(s).dt.minute
    return pd.DataFrame({'model': model, 'date': pd.to_datetime(r.date), 'ent': hm(r[tcol]), 'ext': hm(r.exit_time),
                         'usd_today': to_today(r), 'usd': r.usd})

onb = frame('overnight_break', exit_time='16:45')
exp = frame('expiry_fade')
print(f"overnight break with the 16:45 flatten: ${onb.usd.sum():,.0f} (vs $23,214 held to 17:00)")
cal = pd.DatetimeIndex(sorted(live.date.unique()))

def daily(trades):
    out = {}
    for d, g in trades.sort_values(['date', 'ent', 'ext']).groupby('date'):
        closed = []
        for r in g.itertuples(index=False):
            if sum(p for t, p in closed if t <= r.ent) <= -DLL: continue
            closed.append((r.ext, r.usd_today))
        out[d] = sum(p for _, p in closed)
    return pd.Series(out).reindex(cal, fill_value=0.0)['2018-01-01':]

rows = []
for m in (1.0, 1.5, 2.0, 3.0, 4.0):
    orb = frame('opening_range', stop_mult=m)
    for name, parts in (('ORB alone', [orb]), ('ONB + ORB', [onb, orb]), ('all 3', [onb, orb, exp])):
        dly = daily(pd.concat(parts)); r = evaluate(dly); done = r[r.out != 'open']
        rate = lambda a, b: (done.loc[a:b].out == 'pass').mean()
        rows.append(dict(models=name, orb_stop=f'{m:g}x', orb_net_1micro=orb.usd.sum(), pass_all=(done.out == 'pass').mean(),
                         p2018_21=rate('2018', '2021'), p2022_26=rate('2022', '2026'), p2024_26=rate('2024', '2026'),
                         days_to_pass=done[done.out == 'pass'].days.median(), worst_day=dly.min()))
for name, parts in (('ONB + expiry', [onb, exp]), ('ONB only', [onb])):
    dly = daily(pd.concat(parts)); r = evaluate(dly); done = r[r.out != 'open']
    rate = lambda a, b: (done.loc[a:b].out == 'pass').mean()
    rows.append(dict(models=name, orb_stop='-', orb_net_1micro=np.nan, pass_all=(done.out == 'pass').mean(), p2018_21=rate('2018', '2021'),
                     p2022_26=rate('2022', '2026'), p2024_26=rate('2024', '2026'), days_to_pass=done[done.out == 'pass'].days.median(), worst_day=dly.min()))
R = pd.DataFrame(rows); R.to_csv('research/prop_lucid_orb_stops_results.csv', index=False)
f = {c: '{:.0%}'.format for c in ('pass_all', 'p2018_21', 'p2022_26', 'p2024_26')}
f.update(orb_net_1micro='{:,.0f}'.format, worst_day='{:,.0f}'.format)
pd.set_option('display.width', 200); print(R.to_string(index=False, formatters=f))
