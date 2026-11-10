import numpy as np, pandas as pd, time, sys
D = "/run/media/roflz/Disk 2/_/market_data/data"
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events"
for sym in ("NQ", "ES"):
    t0 = time.time()
    d = pd.read_csv(f"{D}/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "Volume", "instrument_id"])
    ts = pd.to_datetime(d.ts_event, utc=True)
    d["m"] = ((ts - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(minutes=1)).astype(np.int64)
    d = d.drop(columns="ts_event").drop_duplicates("m").sort_values("m")
    d.to_parquet(f"{OUT}/{sym}_1m.parquet")
    print(sym, len(d), time.time() - t0, d.m.min(), d.m.max())
