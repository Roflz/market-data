"""
Step 4 of the pre-registration: FOMC handling with the official Fed calendar (data/fomc_dates.csv, scheduled meetings).
  BASE-raw  BASE with no FOMC rule at all (the earlier version blocked entries using a size-of-bar detector, which
            peeked at the 2 PM bar; this removes that)
  F1        no new entries from 30 minutes before to 15 minutes after the scheduled statement time on statement days
  F2        trade only on days in EVEN weeks of the FOMC cycle (Cieslak, Morse & Vissing-Jorgensen):
            week 0 = trading days -1..3 around a statement (day 0), week 1 = days 4..8, week 2 = 9..13, ...
Usage:  PYTHONPATH=./pylib python3 fomc_step.py
"""
import warnings
import numpy as np
import pandas as pd
import fut_build as fb
import null_test as nt
warnings.filterwarnings("ignore")

fomc = pd.read_csv("data/fomc_dates.csv")
fomc = fomc[fomc.scheduled]
fomc["date"] = pd.to_datetime(fomc.date).dt.date


def cycle_week(trading_days):
    st = sorted(fomc.date)
    days = sorted(trading_days)
    pos = {d: i for i, d in enumerate(days)}
    st_idx = [pos[d] for d in st if d in pos]
    wk = {}
    for d, i in pos.items():
        nxt = [j for j in st_idx if j >= i]
        prv = [j for j in st_idx if j <= i]
        if nxt and nxt[0] - i == 1:                      # the day before a statement belongs to week 0
            wk[d] = 0
        elif prv:
            wk[d] = (i - prv[-1] + 1) // 5
        else:
            wk[d] = np.nan
    return wk


for sym in ("NQ", "ES"):
    nt.SYM = sym
    d, _ = fb.load_raw(sym)
    closed = (d.tmin >= 1020) & (d.tmin < 1080) & (d.index >= pd.Timestamp("2015-09-20", tz="America/New_York"))
    d = d[~closed]
    O, H, L, C = (d[c].to_numpy() for c in ("Open", "High", "Low", "Close"))
    st_time = {r.date: int(r.statement_time_et[:2]) * 60 + int(r.statement_time_et[3:]) for r in fomc.itertuples()}
    rth_days = sorted(set(d.index[d.rth].date))
    wk = cycle_week(rth_days)

    def f1(ts):
        dt = ts.date
        tm = ts.hour * 60 + ts.minute
        return np.array([not (x in st_time and st_time[x] - 30 <= m <= st_time[x] + 15) for x, m in zip(dt, tm)])

    def f2(ts):
        return np.array([wk.get(x, np.nan) % 2 == 0 for x in ts.date])

    out = {}
    for name, keep in (("BASE-raw", None), ("F1 FOMC blackout", f1), ("F2 even cycle weeks", f2)):
        t = nt.strategy(O, H, L, C, d, keep)
        yr = t.groupby("year").R.sum()
        out[name] = dict(trades=len(t), total_R=t.R.sum(), R_per_trade=t.R.mean(), usd=t.usd.sum(),
                         years_up=f"{int((yr > 0).sum())}/{len(yr)}", R_2026=float(yr.get(2026, 0)))
        out[name]["by_year"] = yr.round(1).to_dict()
    res = pd.DataFrame(out).T
    print(f"\n######## {'MNQ' if sym == 'NQ' else 'MES'} ########")
    print(res.drop(columns="by_year").round(3).to_string())
    yrs = pd.DataFrame({k: v["by_year"] for k, v in out.items()}).T
    print("Net R by year:\n" + yrs.to_string())
    # descriptive: BASE-raw R per trade by cycle week (not a strategy)
    t = nt.strategy(O, H, L, C, d)
    t["wk"] = [wk.get(x) for x in pd.DatetimeIndex(t.sess.astype(str)).date] if "sess" in t else np.nan
