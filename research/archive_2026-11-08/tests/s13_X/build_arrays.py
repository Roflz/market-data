"""Builder X, Section 13: build per-day x minute arrays of 1-min bars for 08:00-10:14 ET (cached pickle).
Slot s = minute offset from 08:00 ET; bar stamped (open time) 08:00+s. Missing bar -> NaN, inst -> -1."""
import sys, numpy as np, pandas as pd

OUT = sys.argv[1]
T0, NSLOT = 8 * 60, 135          # 08:00 .. 10:14 ET


def build(sym):
    df = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"],
                     dtype={"Open": "float64", "High": "float64", "Low": "float64", "Close": "float64",
                            "Volume": "int64", "instrument_id": "int64"})
    ts = pd.to_datetime(df.ts_event, utc=True, format="ISO8601").dt.tz_convert("America/New_York")
    tmin = (ts.dt.hour * 60 + ts.dt.minute).to_numpy()
    keep = (tmin >= T0) & (tmin < T0 + NSLOT)
    df = df[keep].copy()
    ts = ts[keep]
    df["date"] = ts.dt.tz_localize(None).dt.normalize().to_numpy()
    df["slot"] = tmin[keep] - T0
    dup = df.duplicated(["date", "slot"]).sum()
    days = pd.DatetimeIndex(sorted(df.date.unique()))
    di = days.get_indexer(df.date)
    A = {}
    for c in ("Open", "High", "Low", "Close"):
        a = np.full((len(days), NSLOT), np.nan)
        a[di, df.slot.to_numpy()] = df[c].to_numpy()
        A[c] = a
    inst = np.full((len(days), NSLOT), -1, dtype=np.int64)
    inst[di, df.slot.to_numpy()] = df.instrument_id.to_numpy()
    A["inst"] = inst
    A["days"] = days
    A["dup"] = int(dup)
    print(sym, len(days), "days; duplicates", dup)
    return A


pd.to_pickle({s: build(s) for s in ("NQ", "ES")}, OUT)
