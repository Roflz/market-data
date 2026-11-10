"""Cache NQ/ES 1-min (ts ET, Open, instrument_id) as compact pickles; independent re-implementation."""
import pandas as pd, numpy as np, os
W = os.path.dirname(os.path.abspath(__file__))
for sym in ("NQ", "ES"):
    out = f"{W}/m1_{sym}.pkl"
    if os.path.exists(out):
        continue
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "instrument_id"],
                    dtype={"Open": "float64", "instrument_id": "int64"})
    ts = pd.to_datetime(d.ts_event, utc=True, format="ISO8601").dt.tz_convert("America/New_York")
    d = pd.DataFrame({"ts": ts, "Open": d.Open.astype("float32"), "inst": d.instrument_id.astype("int64")})
    d = d.drop_duplicates("ts").sort_values("ts").reset_index(drop=True)
    d.to_pickle(out)
    print(sym, len(d), d.ts.min(), d.ts.max())
