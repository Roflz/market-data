"""Independent raw load of NQ 1-min bars -> cached pickle (NY time, raw + back-adjusted prices, 5-min ATR)."""
import os, numpy as np, pandas as pd
W = os.path.dirname(os.path.abspath(__file__))
P1 = f"{W}/nq1m.pkl"; P5 = f"{W}/nq5m.pkl"
def load1():
    if os.path.exists(P1):
        return pd.read_pickle(P1)
    d = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"])
    ts = pd.to_datetime(d.pop("ts_event"), utc=True, format="ISO8601").dt.tz_convert("America/New_York").dt.tz_localize(None)
    d.index = pd.DatetimeIndex(ts)
    d = d[~d.index.duplicated()].sort_index()
    pd.to_pickle(d, P1)
    return d
def load5():
    if os.path.exists(P5):
        return pd.read_pickle(P5)
    d = load1().copy()
    tm = d.index.hour * 60 + d.index.minute
    d = d[~((tm >= 1020) & (tm < 1080) & (d.index >= pd.Timestamp("2015-09-20")))]
    inst = d.instrument_id.to_numpy()
    roll = np.r_[False, inst[1:] != inst[:-1]]
    jump = np.where(roll, d.Open.to_numpy() - np.r_[np.nan, d.Close.to_numpy()[:-1]], 0.0)
    adj = np.r_[np.cumsum(jump[::-1])[::-1][1:], 0.0]          # sum of later jumps
    A = d[["Open", "High", "Low", "Close"]].add(adj, axis=0)
    A["sess"] = (d.index + pd.Timedelta(hours=6)).normalize()
    A["inst"] = inst
    b = A.resample("5min", label="left", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "sess": "first", "inst": "last"}).dropna(subset=["Open"])
    pc = b.Close.shift()
    tr = np.maximum(b.High - b.Low, np.maximum((b.High - pc).abs(), (b.Low - pc).abs()))
    b["atr"] = tr.rolling(14).mean()
    pd.to_pickle(b, P5)
    return b
if __name__ == "__main__":
    os.chdir("/run/media/roflz/Disk 2/_/market_data")
    d = load1(); print(len(d), d.index.min(), d.index.max())
    b = load5(); print(len(b))
