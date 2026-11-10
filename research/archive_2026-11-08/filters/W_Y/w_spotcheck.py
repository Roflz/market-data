"""
Builder Y, Filter W: hand spot-check of 5 trades' filter inputs from the RAW 1-minute bars (data/NQ_fut_1m.csv),
independent of x5_NQ.pkl / exits_engine:
  - rebuild the 5-minute bars around the signal from raw 1-min bars (bar open stamps, ET), check one instrument_id
  - ATR(14) on 5-min true ranges at the signal bar -> stop distance = 2 x ATR
  - raw price = the signal 5-min bar's last 1-min close (raw contract price)
  - width = stop / raw price; compare with W_trades.csv
  - threshold: recount the previous 250 cash days from daily_sessions_NQ.pkl and take pandas' quantile(0.67) of the
    widths of trades dated inside them; compare with p67_width and the keep/remove decision
  - confirm every 1-min bar used closes at or before the decision time (signal bar open + 5 min = entry time)
"""
import os

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
T = pd.read_csv(os.path.join(OUT, "W_trades.csv"), parse_dates=["date"])
T["signal_bar_time"] = pd.to_datetime(T.signal_bar_time, utc=True).dt.tz_convert("America/New_York")
T["entry_time"] = pd.to_datetime(T.entry_time, utc=True).dt.tz_convert("America/New_York")

rng = np.random.default_rng(12345)
elig = T[T.hist_days >= 250]
pick = list(rng.choice(elig[elig.decision == "remove"].index, 3, replace=False)) + \
       list(rng.choice(elig[elig.decision == "keep"].index, 2, replace=False))
pick = sorted(pick)
need = set(T.loc[pick, "date"].dt.date)

parts = []
for ch in pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"],
                      chunksize=1_000_000):
    ts = pd.to_datetime(ch.ts_event, utc=True).dt.tz_convert("America/New_York")
    keep = pd.Series(ts.dt.date).isin(need).to_numpy()
    if keep.any():
        c = ch[keep].copy()
        c.index = ts[keep]
        parts.append(c.drop(columns="ts_event"))
raw = pd.concat(parts).sort_index()
raw = raw[~raw.index.duplicated()]

ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
cash = ds.index[ds.cash_day]
cash = cash[cash >= pd.Timestamp("2011-01-03")]
rows = []
for i in pick:
    tr = T.loc[i]
    S = tr.signal_bar_time
    dec_time = S + pd.Timedelta(minutes=5)
    m = raw[(raw.index >= S - pd.Timedelta(hours=3)) & (raw.index < dec_time)]
    assert m.index.max() < dec_time and m.index.max() + pd.Timedelta(minutes=1) <= tr.entry_time
    one_contract = m.instrument_id.nunique() == 1
    b5 = m.resample("5min", label="left", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    pc = b5.Close.shift()
    trr = pd.concat([b5.High - b5.Low, (b5.High - pc).abs(), (b5.Low - pc).abs()], axis=1).max(axis=1)
    atr = trr.iloc[-14:].mean()
    assert b5.index[-1] == S
    stop = 2 * atr
    px = m.Close.iloc[-1]
    width = stop / px
    # threshold by hand
    pos = cash.get_loc(tr.date)
    win = cash[pos - 250:pos]
    wt = T[T.date.isin(win)]
    thr = wt.width.quantile(0.67)
    dec = "remove" if width > thr else "keep"
    rows.append(dict(date=tr.date.date(), side=tr.side, signal_bar=S.strftime("%H:%M"), one_contract=one_contract,
                     raw_atr14=round(atr, 4), raw_stop=round(stop, 4), csv_R_pts=round(tr.R_pts, 4),
                     raw_close=px, csv_raw_price=tr.raw_price_signal_close, raw_width=width, csv_width=tr.width,
                     hand_thr=thr, csv_thr=tr.p67_width, n_win=len(wt), csv_n_win=tr.window_trades,
                     hand_decision=dec, csv_decision=tr.decision,
                     match=bool(np.isclose(width, tr.width, rtol=1e-6) and np.isclose(thr, tr.p67_width)
                                and dec == tr.decision and len(wt) == tr.window_trades)))
R = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.max_columns", 30)
print(R.T)
R.to_csv(os.path.join(OUT, "W_spotcheck.csv"), index=False)
print("all 5 match:", R.match.all())
