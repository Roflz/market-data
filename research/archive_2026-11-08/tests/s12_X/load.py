"""Build per-day RTH arrays (days x 390 minutes, 9:30..15:59) for NQ and ES; cache to pickle in this dir."""
import os, pickle
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "rth_arrays.pkl")


def load_sym(sym):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"])
    ts = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York")
    d = d.drop(columns="ts_event")
    d["date"] = ts.dt.tz_localize(None).dt.normalize()
    d["tmin"] = (ts.dt.hour * 60 + ts.dt.minute).astype(np.int16)
    d["ts"] = ts.dt.tz_localize(None)
    d = d[(d.tmin >= 570) & (d.tmin < 960)]
    d = d.drop_duplicates(subset=["ts"]).sort_values("ts")
    return d


def build():
    out = {}
    for sym in ("NQ", "ES"):
        d = load_sym(sym)
        days = pd.DatetimeIndex(sorted(d.date.unique()))
        di = days.get_indexer(d.date)
        mi = d.tmin.to_numpy() - 570
        n = len(days)
        A = {}
        for col in ("Open", "High", "Low", "Close"):
            a = np.full((n, 390), np.nan)
            a[di, mi] = d[col].to_numpy()
            A[col] = a
        inst = np.full((n, 390), -1, dtype=np.int64)
        inst[di, mi] = d.instrument_id.to_numpy()
        A["inst"] = inst
        A["days"] = days
        out[sym] = A
    with open(CACHE, "wb") as f:
        pickle.dump(out, f, protocol=4)
    return out


def get():
    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    return build()


if __name__ == "__main__":
    o = build()
    for s in o:
        A = o[s]
        ex = ~np.isnan(A["Close"])
        print(s, len(A["days"]), A["days"][0], A["days"][-1], "bars present frac", ex.mean())
