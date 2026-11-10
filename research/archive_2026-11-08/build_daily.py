"""Daily session table for calendar tests (research only). Run from the project folder.
One row per Globex session (labelled by the date it ends): RTH open (9:30 bar open), RTH close (15:59 bar close, or the
last RTH bar on early closes), Globex close (last bar of the session), in both back-adjusted points (point changes inside
a contract are exact; roll gaps removed) and raw prices of the contract trading at 9:30 (for bp sizing), plus the
contract id and whether the contract changed since the previous session (a roll)."""
import sys
import numpy as np
import pandas as pd

OUT = sys.argv[1]
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
    T = T[(T.rth_first_tmin == 570) & (T.n_rth_bars >= 200)]          # real cash sessions only
    T["cash_holiday"] = T.rth_last_tmin <= 785                         # Globex-only holiday session ending 13:00 ET
    T["early_close"] = (T.rth_last_tmin > 785) & (T.rth_last_tmin < 959)  # cash closes 13:00, futures 13:15
    T["cash_day"] = ~T.cash_holiday
    T["roll_since_prev"] = T.inst.ne(T.inst.shift()) & T.inst.shift().notna()
    T.to_pickle(f"{OUT}/daily_{sym}.pkl")
    print(f"{sym}: {len(T)} sessions {T.index.min():%Y-%m-%d} -> {T.index.max():%Y-%m-%d}; "
          f"early closes {int(T.early_close.sum())}; cash holidays {int(T.cash_holiday.sum())}; rolls {int(T.roll_since_prev.sum())}")
