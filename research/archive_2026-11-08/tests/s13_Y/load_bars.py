"""Build a cache of 1-minute bars stamped 08:00-10:59 ET (bar OPEN times) for NQ and ES.
ts_event strings carry an explicit UTC offset; we parse them as UTC and convert to America/New_York."""
import os, sys
import numpy as np, pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
PROJ = "/run/media/roflz/Disk 2/_/market_data"

def build(sym):
    path = f"{OUT}/bars_{sym}_0800_1100.pkl"
    if os.path.exists(path):
        return pd.read_pickle(path)
    parts = []
    for ch in pd.read_csv(f"{PROJ}/data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"],
                          dtype={"ts_event": str}, chunksize=2_000_000):
        hh = ch.ts_event.str.slice(11, 13)
        ch = ch[hh.isin(["06", "07", "08", "09", "10", "11", "12"])]     # coarse prefilter with margin (offset handled below)
        ts = pd.to_datetime(ch.ts_event, utc=True).dt.tz_convert("America/New_York")
        tmin = ts.dt.hour * 60 + ts.dt.minute
        keep = (tmin >= 8 * 60) & (tmin < 11 * 60)
        ch = ch[keep.to_numpy()].copy()
        ts = ts[keep]
        ch["ts"] = ts.dt.tz_localize(None).to_numpy()
        ch["date"] = ts.dt.tz_localize(None).dt.normalize().to_numpy()
        ch["tmin"] = tmin[keep].astype(np.int16).to_numpy()
        parts.append(ch.drop(columns="ts_event"))
    df = pd.concat(parts, ignore_index=True).sort_values("ts").reset_index(drop=True)
    df.to_pickle(path)
    return df

if __name__ == "__main__":
    for s in ["NQ", "ES"]:
        d = build(s)
        print(s, len(d), d.ts.min(), d.ts.max(), d.date.nunique())
