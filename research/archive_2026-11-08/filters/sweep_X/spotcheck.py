"""Hand spot-check of 5 trades' stop widths straight from the raw 1-minute CSV (independent of x5/exits_engine):
build the 5-min bars ending at the signal bar, ATR(14) of true range, R = 2 x ATR, raw signal close, width = R/close."""
import os

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
T = pd.read_pickle(f"{OUT}/base_trades.pkl")
pick = T.iloc[[100, 500, 900, 1300, 1700]]
days = set(pick.date.dt.strftime("%Y-%m-%d"))
rows = []
for ch in pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "Volume", "instrument_id"],
                      chunksize=1_000_000):
    rows.append(ch[ch.ts_event.str[:10].isin(days)])
m = pd.concat(rows)
m.index = pd.to_datetime(m.ts_event, utc=True).dt.tz_convert("America/New_York")
res = []
for r in pick.itertuples():
    s = r.signal_bar_time
    w = m[(m.index >= s - pd.Timedelta(minutes=70)) & (m.index < s + pd.Timedelta(minutes=5))]
    assert w.instrument_id.nunique() == 1, "roll inside window"
    b = w.resample("5min", label="left", closed="left").agg({"High": "max", "Low": "min", "Close": "last"}).dropna()
    b = b[b.index <= s]
    pc = b.Close.shift()
    tr = np.maximum.reduce([b.High - b.Low, (b.High - pc).abs(), (b.Low - pc).abs()])
    atr = tr[-14:].mean()
    res.append(dict(date=r.date.date(), signal=s.strftime("%H:%M"), n5=len(b), atr_hand=atr, atr_engine=r.atr5_signal,
                    R_hand=2 * atr, R_engine=r.R_pts, close_hand=b.Close.iloc[-1], close_engine=r.raw_signal_close,
                    width_hand=2 * atr / b.Close.iloc[-1], width_engine=r.M1, M3_hand=2 * atr * 2 + 2, M3=r.M3))
R = pd.DataFrame(res)
pd.set_option("display.width", 250)
print(R.to_string())
R.to_csv(f"{OUT}/spotcheck_widths.csv", index=False)
