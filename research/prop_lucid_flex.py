"""
LucidFlex 25K evaluation, replayed on the live models' daily P&L (chosen_models_trades.csv), from every start date.
Rules (support.lucidtrading.com, read 2026-11-08): profit target $1,250; max loss limit $1,000 trailing on the highest
END-OF-DAY balance, locking at $25,100 once the closing balance exceeds $26,100; breach when the balance reaches the
limit; best day <= 40% of profit to pass (50% with the add-on); max 20 micros.
Simplifications (stated in the output): the breach is checked on closing balances only (the help page describes an
end-of-day drawdown; an intraday check would fail somewhat more often); the overnight break is held to 17:00 in the
backtest, but Lucid flattens at 16:45; no daily loss limit (optional at purchase).
Two money scales: 'actual' = the historical $ at 1 micro; 'today' = each trade's net move rescaled to today's NQ price
(27,100), which is what the same trades would be worth now (one micro risked far less in 2018-2020).
Usage: PYTHONPATH=./pylib python3 research/prop_lucid_flex.py
"""
import numpy as np, pandas as pd

START, TARGET, MLL, LOCK_TRIGGER, LOCK_AT = 25_000.0, 1_250.0, 1_000.0, 26_100.0, 25_100.0
P_NOW, COST = 27_100.0, 2.0
T = pd.read_csv('chosen_models_trades.csv', parse_dates=['date'])
px = 1e4 * (T.usd / 2) / T.bp                                   # raw entry price implied by $ and bp
gross_pts = T.usd / 2 + 1.0                                      # add back the 1-point round-trip cost
T['usd_today'] = (gross_pts / px) * P_NOW * 2 - COST              # same % move at today's price, minus $2 cost
T.loc[T.bp == 0, 'usd_today'] = -COST

SETS = {'all 3 models': ['overnight_break', 'opening_range', 'expiry_fade'],
        'overnight break + opening range': ['overnight_break', 'opening_range'],
        'overnight break + expiry fade': ['overnight_break', 'expiry_fade'],
        'opening range + expiry fade': ['opening_range', 'expiry_fade'],
        'overnight break only': ['overnight_break'], 'opening range only': ['opening_range']}

def run(daily, cons):
    """daily: Series of day P&L in trading-day order. Returns per start: outcome, days, end index."""
    v = daily.to_numpy(); n = len(v); res = []
    for s in range(n):
        bal, hi, best, locked = START, START, 0.0, False
        out, d = 'open', 0
        for i in range(s, n):
            d += 1; bal += v[i]; best = max(best, v[i])
            hi = max(hi, bal)
            if not locked and hi > LOCK_TRIGGER: locked = True
            floor = LOCK_AT if locked else hi - MLL
            if bal <= floor:
                out = 'fail'; break
            prof = bal - START
            if prof >= TARGET and best <= cons * prof:
                out = 'pass'; break
        res.append((out, d))
    return pd.DataFrame(res, columns=['out', 'days'], index=daily.index)

cal = pd.DatetimeIndex(sorted(T.date.unique()))
rows = []
for scale in ('today', 'actual'):
    col = 'usd_today' if scale == 'today' else 'usd'
    for name, models in SETS.items():
        for k in (1, 2, 3):
            daily = (T[T.model.isin(models)].groupby('date')[col].sum() * k).reindex(cal, fill_value=0.0)
            daily = daily['2018-01-01':]                            # start dates from 2018 (modern prices/costs)
            for cons in (0.40, 0.50):
                r = run(daily, cons); done = r[r.out != 'open']
                rows.append(dict(scale=scale, models=name, micros=k, consistency=f'{cons:.0%}', starts=len(done),
                                 pass_rate=(done.out == 'pass').mean(), fail_rate=(done.out == 'fail').mean(),
                                 median_days_to_pass=done[done.out == 'pass'].days.median(),
                                 median_days_to_fail=done[done.out == 'fail'].days.median(),
                                 pass_rate_2024_26=(done.loc['2024':].out == 'pass').mean()))
R = pd.DataFrame(rows)
R.to_csv('research/prop_lucid_flex_results.csv', index=False)
pd.set_option('display.width', 200)
for scale in ('today', 'actual'):
    print(f"\n=== {scale} prices; start any trading day 2018-2026; breach checked at the close; 40% consistency ===")
    x = R[(R.scale == scale) & (R.consistency == '40%')].drop(columns=['scale', 'consistency'])
    print(x.to_string(index=False, formatters={'pass_rate': '{:.0%}'.format, 'fail_rate': '{:.0%}'.format, 'pass_rate_2024_26': '{:.0%}'.format}))
print("\n=== 50% consistency add-on (today's prices) ===")
x = R[(R.scale == 'today') & (R.consistency == '50%')].drop(columns=['scale', 'consistency'])
print(x.to_string(index=False, formatters={'pass_rate': '{:.0%}'.format, 'fail_rate': '{:.0%}'.format, 'pass_rate_2024_26': '{:.0%}'.format}))
