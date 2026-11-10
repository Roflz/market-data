import numpy as np, pandas as pd
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/W_X/"
T = pd.read_pickle(OUT + "W_decisions.pkl")
P = pd.read_pickle(OUT + "ob_trades.pkl"); cal = pd.DatetimeIndex(P["cash_days"]).sort_values()
rng = np.random.default_rng(12345)
pick = list(rng.choice(T.index[T.remove], 2, replace=False)) + list(rng.choice(T.index[~T.remove & T.eligible], 2, replace=False)) \
       + [int(T.index[T.eligible][0])]
d = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"])
d.index = pd.to_datetime(d.pop("ts_event"), utc=True).dt.tz_convert("America/New_York")
d = d[~d.index.duplicated()].sort_index()
for i in pick:
    r = T.loc[i]; s = r.signal_bar_open
    w = d[(d.index >= s - pd.Timedelta(days=4)) & (d.index < s + pd.Timedelta(minutes=5))].copy()
    tmin = w.index.hour * 60 + w.index.minute
    if s >= pd.Timestamp("2015-09-20", tz="America/New_York"):
        w = w[~((tmin >= 1020) & (tmin < 1080))]
    b = w.resample("5min", label="left", closed="left").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last",
                                                             "instrument_id": "last"}).dropna(subset=["Open"])
    b = b.iloc[-15:]; assert b.index[-1] == s
    pc = b.Close.shift(); tr = np.maximum.reduce([b.High - b.Low, (b.High - pc).abs(), (b.Low - pc).abs()])[1:]
    atr = tr.mean(); Rh = 2 * atr; raw_close = b.Close.iloc[-1]
    same_inst = b.instrument_id.nunique() == 1
    # hand percentile with an explicit loop
    k = cal.get_loc(r.date); win = set(cal[k - 250:k])
    ws = [x.width for x in T.itertuples() if x.date in win]
    p = np.percentile(ws, 67)
    print(f"{r.date:%Y-%m-%d} {r.side:5s} sig {s:%H:%M} inst_const={same_inst} | R hand {Rh:.4f} vs {r.R_pts:.4f} | raw close hand {raw_close} vs {r.raw_px:.2f}"
          f" | width hand {Rh/raw_close:.6f} vs {r.width:.6f} | p67 hand {p:.6f} (n={len(ws)}) vs {r.p67_width:.6f} (n={r.n_window})"
          f" | decision hand {'remove' if Rh/raw_close > p else 'keep'} vs {r.decision}")
# look-ahead checks
print("window ends strictly before date:", all(cal[c - 1] < dt for c, dt in zip(T.cal_pos, T.date)))
print("signal bar close <= entry bar open:", ((T.signal_bar_open + pd.Timedelta(minutes=5)) <= T.entry_bar_open).all())
