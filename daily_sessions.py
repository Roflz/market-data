"""
Daily session table for calendar and regime tests: data/daily_sessions_{ES,NQ}.pkl, one row per cash session.
RTH open = 9:30 bar open; RTH close = 15:59 bar close (or the last RTH bar on early-close days); Globex close = the
session's last bar (5 PM ET since late 2015; 5:15-5:30 PM before that, and 4:15 PM on some early Fridays). Prices both back-adjusted (point changes inside a contract are exact, roll gaps removed;
use these for multi-day P&L) and raw (the contract trading at 9:30; use these for bp and sizing). Flags: early close,
cash holiday (Globex-only session), contract roll since the previous session.
Usage:  PYTHONPATH=./pylib python3 daily_sessions.py
"""
import numpy as np
import pandas as pd

OUT = "data"
for sym in ("ES", "NQ"):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", index_col=0)
    d.index = pd.to_datetime(d.index, utc=True).tz_convert("America/New_York")
    d = d[~d.index.duplicated()].sort_index()
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    d["aO"], d["aC"] = d.Open + adj, d.Close + adj
    d["sess"] = (d.index + pd.Timedelta(hours=6)).date
    tmin = d.index.hour * 60 + d.index.minute
    d["tmin"] = tmin
    rth = d[(tmin >= 570) & (tmin < 960)]
    g = rth.groupby("sess")
    first = g.head(1).set_index("sess")
    last = g.tail(1).set_index("sess")
    sess_last = d.groupby("sess").tail(1).set_index("sess")
    T = pd.DataFrame({
        "rth_first_tmin": first.tmin, "inst": first.instrument_id,
        "open_raw": first.Open, "open_adj": first.aO,
        "close_raw": last.Close, "close_adj": last.aC, "rth_last_tmin": last.tmin,
        "glbx_close_adj": sess_last.aC.reindex(first.index), "glbx_close_raw": sess_last.Close.reindex(first.index),
        "n_rth_bars": g.size(),
    })
    T.index = pd.to_datetime(T.index)
    hol = (T.rth_first_tmin == 570) & (T.rth_last_tmin <= 785)         # Globex-only holiday session ending 13:00 ET
    T = T[(T.rth_first_tmin == 570) & ((T.n_rth_bars >= 200) | hol)]   # real cash sessions, plus holiday sessions
    T["cash_holiday"] = T.rth_last_tmin <= 785
    T["early_close"] = (T.rth_last_tmin > 785) & (T.rth_last_tmin < 959)  # cash closes 13:00, futures 13:15
    T["cash_day"] = ~T.cash_holiday
    # roll flag measured against the previous CASH day (a roll on a holiday session is carried to the next cash day)
    T["roll_since_prev"] = False
    C = T[T.cash_day]
    T.loc[C.index, "roll_since_prev"] = (C.inst.ne(C.inst.shift()) & C.inst.shift().notna()).to_numpy()
    T.to_pickle(f"{OUT}/daily_sessions_{sym}.pkl")
    print(f"{sym}: {len(T)} sessions {T.index.min():%Y-%m-%d} -> {T.index.max():%Y-%m-%d}; "
          f"early closes {int(T.early_close.sum())}; cash holidays {int(T.cash_holiday.sum())}; rolls {int(T.roll_since_prev.sum())}")
