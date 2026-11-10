"""Download 2010-now hourly bars for one CME continuous front contract into data/{SYM}_fut_1h.csv.
Usage (from the project folder): PYTHONPATH=./pylib python3 get_hourly.py CL"""
import sys
import time
import fetch_databento as f

s = sys.argv[1]
t0 = time.time()
kw = dict(dataset="GLBX.MDP3", symbols=[f"{s}.v.0"], stype_in="continuous", schema="ohlcv-1h", start="2010-06-06", end=f.END)
df = f.client().timeseries.get_range(**kw).to_df()
df.index = df.index.tz_convert("America/New_York")
df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
df = df[["Open", "High", "Low", "Close", "Volume", "instrument_id"]]
out = f"data/{s}_fut_1h.csv"
df.to_csv(out)
print(f"{out}: {len(df):,} bars {df.index.min():%Y-%m-%d} -> {df.index.max():%Y-%m-%d}, "
      f"{df.instrument_id.nunique()} contracts, {time.time() - t0:.0f}s", flush=True)
