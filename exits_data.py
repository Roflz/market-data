"""
Full-session 5-minute bars for ES / NQ futures (Databento, rolls back-adjusted) with everything the exit tests need.
Trades can now last any length: overnight and multi-day, so bars cover the whole ~23h Globex session.

Columns (all known at the bar's close, no look-ahead):
  Open High Low Close Volume, sess (trading-session date), rth (bar starts 9:30-15:55 ET), tmin (minute of day)
  atr5        : 14-bar ATR on 5-min bars
  ema20_5     : EMA 20 on 5-min closes
  h60_close, h60_ema20, h60_ema50, h60_atr, h60_lo20, h60_hi20 : last CLOSED 60-min bar's close, EMAs, ATR(14),
                lowest low / highest high of the last 20 closed 60-min bars
  d_atr       : 14-session average daily range (prior sessions)
  delta5      : approximate buy-minus-sell volume (bulk volume classification on 1-min bars, summed to 5-min)
  cvd         : cumulative delta since the session start
Output: data/x5_{ES,NQ}.pkl
Usage:  PYTHONPATH=./pylib python3 exits_data.py
"""
import warnings

import numpy as np
import pandas as pd
from math import erf, sqrt

import fut_build as fb

warnings.filterwarnings("ignore")


def norm_cdf(x):
    return 0.5 * (1 + np.vectorize(lambda v: erf(v / sqrt(2)))(x))


def build(sym):
    d, n_rolls = fb.load_raw(sym)
    # drop stray prints in the closed 5-6 PM ET hour (after CME moved the close from 5:15 to 5:00 PM in Sept 2015)
    closed = (d.tmin >= 1020) & (d.tmin < 1080) & (d.index >= pd.Timestamp("2015-09-20", tz="America/New_York"))
    d = d[~closed]
    # bulk volume classification (Easley, Lopez de Prado & O'Hara): buy share = Phi(dP / sigma) per 1-min bar
    dp = d.Close.diff()
    sig = dp.rolling(390, min_periods=60).std()
    z = (dp / sig).clip(-6, 6).fillna(0).to_numpy()
    from scipy.special import ndtr  # noqa: E402  (available via sklearn's scipy dependency)
    buy = ndtr(z)
    d["delta1"] = d.Volume * (2 * buy - 1)

    agg = {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum", "delta1": "sum",
           "sess": "first", "tmin": "first"}
    b = d.resample("5min", label="left", closed="left").agg(agg).dropna(subset=["Open"])
    b = b.rename(columns={"delta1": "delta5"})
    b["rth"] = (b.tmin >= 570) & (b.tmin < 960)
    pc = b.Close.shift()
    tr = pd.concat([b.High - b.Low, (b.High - pc).abs(), (b.Low - pc).abs()], axis=1).max(axis=1)
    b["atr5"] = tr.rolling(14).mean()
    b["ema20_5"] = b.Close.ewm(span=20, adjust=False).mean()
    b["cvd"] = b.delta5.groupby(b.sess).cumsum()

    # 60-minute bars, stamped at their close, merged by the 5-min bar's close time
    h = d.resample("60min", label="right", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    hpc = h.Close.shift()
    htr = pd.concat([h.High - h.Low, (h.High - hpc).abs(), (h.Low - hpc).abs()], axis=1).max(axis=1)
    hf = pd.DataFrame({"h60_close": h.Close, "h60_ema20": h.Close.ewm(span=20, adjust=False).mean(),
                       "h60_ema50": h.Close.ewm(span=50, adjust=False).mean(), "h60_atr": htr.rolling(14).mean(),
                       "h60_lo20": h.Low.rolling(20).min(), "h60_hi20": h.High.rolling(20).max()})
    hf.index.name = "t"
    close_t = b.index + pd.Timedelta(minutes=5)
    m = pd.merge_asof(pd.DataFrame({"t": close_t}), hf.reset_index(), on="t", direction="backward")
    for c in hf.columns:
        b[c] = m[c].to_numpy()

    # daily (session) context from PRIOR sessions only
    rng = d.groupby("sess").agg(h=("High", "max"), l=("Low", "min"))
    datr = (rng.h - rng.l).rolling(14).mean().shift()
    b["d_atr"] = b.sess.map(datr)
    b["day"] = pd.factorize(b.sess)[0]
    b = b.dropna(subset=["atr5", "h60_atr", "d_atr"])
    pd.to_pickle(b, f"data/x5_{sym}.pkl")
    print(f"{sym}: {len(b):,} five-minute bars, {b.sess.nunique()} sessions "
          f"({b.index.min():%Y-%m-%d} -> {b.index.max():%Y-%m-%d}), {n_rolls} rolls back-adjusted", flush=True)


if __name__ == "__main__":
    for s in ("ES", "NQ"):
        build(s)
