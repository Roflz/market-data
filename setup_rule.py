"""
The overnight-break entry rule (model 7).
At a 5-minute decision close between 9:35 and 15:00 ET:
  buy  if price's first close above the overnight high (6 PM - 9:30 AM) happened within the last `fresh`+1 minutes
       and price is above the 20-day EMA of daily closes;
  sell if price's first close below the overnight low happened within that window and price is below the EMA.
No new entries from 30 minutes before to 15 minutes after a scheduled FOMC statement (official Fed calendar).
"""
import numpy as np
import pandas as pd

NAME = "Overnight break + daily trend"


def fomc_blackout(ts):
    f = pd.read_csv("data/fomc_dates.csv")
    f = f[f.scheduled]
    st = {pd.Timestamp(r.date).date(): int(r.statement_time_et[:2]) * 60 + int(r.statement_time_et[3:]) for r in f.itertuples()}
    ts = pd.DatetimeIndex(ts)
    mins = ts.hour * 60 + ts.minute
    return np.array([d in st and st[d] - 30 <= m <= st[d] + 15 for d, m in zip(ts.date, mins)])


def overnight_break(X, ts, fresh=4, trend="ema20", blackout=True):
    """Signal per decision row: +1 buy, -1 sell, 0 none."""
    tr = {"ema20": np.sign(X.day_vs_ema20), "ret5d": np.sign(X.ret_5d), "none": np.ones(len(X))}[trend]
    up = (X.on_break_up_mins >= 0) & (X.on_break_up_mins <= fresh)
    dn = (X.on_break_down_mins >= 0) & (X.on_break_down_mins <= fresh)
    if trend == "none":
        sig = np.where(up, 1, np.where(dn, -1, 0))
    else:
        sig = np.where(up & (tr > 0), 1, np.where(dn & (tr < 0), -1, 0))
    if blackout:
        sig = np.where(fomc_blackout(ts), 0, sig)
    return sig
