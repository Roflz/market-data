"""
Hand check of 5 trades' stop widths straight from the raw 1-minute CSV (independent of x5 / exits_engine):
5-min bars (open-time label), true range of the 14 bars ending at the signal bar, ATR = their mean, stop = 2 x ATR,
raw price = close of the last 1-min bar inside the signal 5-min bar. Also an independent recomputation of M4.
"""
import numpy as np
import pandas as pd

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/sweep_Y"
T = pd.read_pickle(f"{OUT}/base_trades.pkl")
picks = [3, 400, 900, 1300, 1700]
wins = [(T.sig_time[k] - pd.Timedelta(hours=3), T.sig_time[k] + pd.Timedelta(minutes=5)) for k in picks]

parts = []
for ch in pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"],
                      chunksize=2_000_000):
    ts = pd.to_datetime(ch.ts_event, utc=True).dt.tz_convert("America/New_York")
    keep = np.zeros(len(ch), bool)
    for a, z in wins:
        keep |= ((ts >= a) & (ts < z)).to_numpy()
    if keep.any():
        c = ch[keep].copy()
        c.index = ts[keep]
        parts.append(c)
M = pd.concat(parts)

lines = []
for k, (a, z) in zip(picks, wins):
    m = M[(M.index >= a) & (M.index < z)]
    insts = m.instrument_id.unique()
    b = m.resample("5min", label="left", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    sig = T.sig_time[k]
    pos = b.index.get_loc(sig)
    trs = []
    for j in range(pos - 13, pos + 1):                       # the 14 bars ending at the signal bar
        h, l, pc = b.High.iloc[j], b.Low.iloc[j], b.Close.iloc[j - 1]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    atr = sum(trs) / 14
    stop = 2 * atr
    raw = b.Close.iloc[pos]
    width = stop / raw
    lines.append(f"trade {k} {T.date[k]:%Y-%m-%d} {T.side[k]} signal {sig:%H:%M} inst {list(insts)}: "
                 f"hand ATR {atr:.4f} stop {stop:.4f} raw close {raw} width {width:.6f} $risk {stop*2+2:.2f} | "
                 f"pipeline ATR {T.atr5[k]:.4f} stop {T.stop_pts[k]:.4f} raw {T.raw_px[k]} width {T.M1[k]:.6f} "
                 f"$risk {T.M3[k]:.2f} | match {np.isclose(width, T.M1[k]) and np.isclose(stop, T.stop_pts[k])}")

# independent M4 recomputation (pandas groupby instead of positional slicing)
x5 = pd.read_pickle("data/x5_NQ.pkl")
sess_order = pd.unique(x5.sess)
by_sess = {s: g.to_numpy(float) for s, g in x5.atr5.groupby(x5.sess, sort=False)}
for k in picks:
    s = x5.sess.loc[T.sig_time[k]]
    p = list(sess_order).index(s)
    prev = np.concatenate([by_sess[q] for q in sess_order[p - 60:p]])
    m4 = x5.atr5.loc[T.sig_time[k]] / np.median(prev)
    lines.append(f"trade {k} M4 independent {m4:.6f} pipeline {T.M4[k]:.6f} match {np.isclose(m4, T.M4[k])}; "
                 f"history sessions {sess_order[p-60]:%Y-%m-%d}..{sess_order[p-1]:%Y-%m-%d} (trade session {s:%Y-%m-%d})")
txt = "\n".join(lines)
print(txt)
open(f"{OUT}/spot_check.txt", "w").write(txt + "\n")
