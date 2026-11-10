"""Build per-day 1-minute arrays (days x minute-of-session, 08:00..15:59 ET = 480 slots) for NQ and ES.
Arrays hold the bars of each date's own RTH contract (the data has exactly one instrument per RTH session).
Also stores: inst (RTH contract of the day), prior-cash-day contract, NYSE flags from daily_sessions_{sym}.pkl.
Run from the project dir (read-only); output: s11_X/cache_{sym}.pkl
"""
import os
import sys
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
S0 = 480            # 08:00 in minutes
NS = 480            # 08:00 .. 15:59


def build(sym):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume",
                                                       "instrument_id"])
    ts = pd.DatetimeIndex(pd.to_datetime(d.ts_event, utc=True, format="ISO8601")).tz_convert("America/New_York")
    tm = np.asarray(ts.hour * 60 + ts.minute)
    m = (tm >= S0) & (tm < S0 + NS)
    d = d.loc[m].reset_index(drop=True)
    dates = pd.to_datetime(pd.Index(ts[m].strftime("%Y-%m-%d")))
    slot = tm[m] - S0
    ds = pd.read_pickle(f"data/daily_sessions_{sym}.pkl")
    ds = ds[ds.cash_day].copy()                                   # NYSE trading days (Globex-only holidays removed)
    days = pd.DatetimeIndex(ds.index)
    di = days.get_indexer(dates)
    ok = di >= 0
    nd = len(days)
    g = {}
    for c in ["Open", "High", "Low", "Close", "Volume"]:
        a = np.full((nd, NS), np.nan)
        a[di[ok], slot[ok]] = d.loc[ok, c].to_numpy(float)
        g[c] = a
    ib = np.full((nd, NS), -1, np.int64)
    ib[di[ok], slot[ok]] = d.loc[ok, "instrument_id"].to_numpy()
    inst = ds.inst.to_numpy().astype(np.int64)                    # RTH contract of each day (single per RTH)
    # keep only bars of the day's RTH contract (pre-market bars of another contract, if any, become NaN)
    foreign = (ib >= 0) & (ib != inst[:, None])
    for c in g:
        g[c][foreign] = np.nan
    prev_inst = np.r_[-1, inst[:-1]]                              # largest-volume contract on the prior NYSE day
    info = pd.DataFrame({"inst": inst, "prev_inst": prev_inst, "early": ds.early_close.to_numpy(),
                         "full": ~ds.early_close.to_numpy()}, index=days)
    print(sym, "days", nd, "foreign premarket bars", int(foreign.sum()),
          "days whose RTH contract != prior-day contract", int((inst != prev_inst).sum()))
    pd.to_pickle({"days": days, "g": g, "info": info}, f"{OUT}/cache_{sym}.pkl")


if __name__ == "__main__":
    for s in sys.argv[1:] or ["NQ", "ES"]:
        build(s)
