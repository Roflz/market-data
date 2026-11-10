"""Builder Y, section 12: cache RTH 1-min bars of NQ and ES as per-day 390-minute grids.
Grid minute i (0..389) = bar stamped 9:30 + i minutes (ET). NaN where the bar is missing.
Saves cache_{SYM}.pkl in this dir: dict(days, O, H, L, C, inst) with arrays shaped (ndays, 390)."""
import os, pickle
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
for sym in ("NQ", "ES"):
    out = f"{HERE}/cache_{sym}.pkl"
    if os.path.exists(out):
        print(sym, "cached"); continue
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"])
    ts = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York")
    tmin = (ts.dt.hour * 60 + ts.dt.minute).to_numpy()
    keep = (tmin >= 570) & (tmin < 960)
    d = d[keep].copy(); ts = ts[keep]
    d["date"] = ts.dt.tz_localize(None).dt.normalize().to_numpy()
    d["i"] = tmin[keep] - 570
    d = d.drop_duplicates(["date", "i"])
    days = np.array(sorted(d.date.unique()))
    di = np.searchsorted(days, d.date.to_numpy())
    res = {"days": pd.DatetimeIndex(days)}
    for col, nm in (("Open", "O"), ("High", "H"), ("Low", "L"), ("Close", "C")):
        a = np.full((len(days), 390), np.nan)
        a[di, d.i.to_numpy()] = d[col].to_numpy()
        res[nm] = a
    a = np.full((len(days), 390), -1, dtype=np.int64)
    a[di, d.i.to_numpy()] = d.instrument_id.to_numpy()
    res["inst"] = a
    with open(out, "wb") as f:
        pickle.dump(res, f)
    # intraday instrument changes inside RTH
    nchg = 0
    for r in range(len(days)):
        u = np.unique(a[r][a[r] >= 0])
        if len(u) > 1:
            nchg += 1
    print(sym, len(days), "days; RTH sessions with >1 instrument:", nchg)
