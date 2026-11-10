"""Small helpers shared by the overnight-break strategy (model 7) and the ML filter (model 10)."""
import numpy as np
import pandas as pd


def since_sign_change(x, cap=120):
    """Bars since the sign of x last changed, signed by the current sign, capped at `cap`."""
    s = np.sign(np.nan_to_num(x))
    out = np.zeros(len(s))
    run = 0
    for i in range(len(s)):
        run = run + 1 if i and s[i] == s[i - 1] else 1
        out[i] = min(run, cap) * s[i]
    return out


def stats(u, dates):
    """Trade statistics for net $ per trade `u` with trade dates (day-level t-statistic)."""
    if len(u) == 0:
        return dict(trades=0, net=0.0, per_trade=np.nan, win=np.nan, t=np.nan, avg_win=np.nan, avg_loss=np.nan,
                    pf=np.nan, max_dd=0.0, lose_streak=0)
    u = np.asarray(u, float)
    daily = pd.Series(u).groupby(pd.Series(dates)).sum()
    t = daily.mean() / (daily.std() / np.sqrt(len(daily))) if len(daily) > 2 and daily.std() > 0 else np.nan
    w, l = u[u > 0], u[u <= 0]
    eq = np.cumsum(u)
    streak = best = 0
    for x in u:
        streak = streak + 1 if x <= 0 else 0
        best = max(best, streak)
    return dict(trades=len(u), net=float(u.sum()), per_trade=float(u.mean()), win=float((u > 0).mean()), t=float(t),
                avg_win=float(w.mean()) if len(w) else 0.0, avg_loss=float(l.mean()) if len(l) else 0.0,
                pf=float(w.sum() / -l.sum()) if l.sum() < 0 else np.inf,
                max_dd=float((np.maximum.accumulate(eq) - eq).max()), lose_streak=int(best))
