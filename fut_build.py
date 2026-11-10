"""
Real ES / NQ futures (Databento, ~23h/day) -> the 88 entry-time measures used by the ML filter (model 10) and the
overnight-level break flags used by the overnight-break strategy (model 7).

What's new vs the ETF version
  - Indicators (EMA 8/20/50, Momentum 14, volume) run on the full Globex session, like your chart.
  - Contract rolls are back-adjusted (price gap at each roll removed from all earlier prices).
  - Higher timeframes: 5 / 15 / 60-minute EMA 20/50, MACD(12,26,9), slope - only from CLOSED bars.
  - Daily trend: vs 20-day EMA of daily closes, prior-day and 5-day moves.
  - Levels: overnight high/low, prior-day RTH high/low/close, opening range (9:30-9:45),
    Initial Balance (9:30-10:30), RTH VWAP - distance in ATRs and position.
  - Regime: daily ATR vs 100-day median, 60-min ADX(14), 60-bar trend efficiency.
  - Event days: 8:30 ET data releases and 2:00 PM Wednesday (FOMC-style) shocks detected from the
    bars themselves (scheduled in advance in real life; known by 8:31 / 14:01).
  - Decision points every 5 minutes during 9:35-15:00 ET.

Outputs data/fut_features_{ES,NQ}.pkl
Usage:  PYTHONPATH=./pylib python3 fut_build.py
"""
import warnings

import numpy as np
import pandas as pd

from common import since_sign_change

warnings.filterwarnings("ignore")
SPEC = {"ES": dict(usd=5.0, comm=1.0, micro="MES"), "NQ": dict(usd=2.0, comm=1.0, micro="MNQ")}


def load_raw(sym):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", index_col=0)
    d.index = pd.to_datetime(d.index, utc=True).tz_convert("America/New_York")
    d = d[~d.index.duplicated()].sort_index()
    # back-adjust rolls: at each contract change remove the jump between old close and new open
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)          # sum of all LATER jumps
    for c in ("Open", "High", "Low", "Close"):
        d[c] = d[c] + adj
    # trading session date: Globex day runs 18:00 -> 17:00 ET, labelled by the day it ends
    sess = (d.index + pd.Timedelta(hours=6)).date
    d["sess"] = sess
    d["tmin"] = d.index.hour * 60 + d.index.minute
    d["rth"] = (d.tmin >= 570) & (d.tmin < 960)
    return d, int(roll.sum())


def rsi(close, n=14):
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + gain / loss)


def htf(d, rule, prefix):
    """Higher-timeframe bars, stamped at their CLOSE time, merged onto 1-min bars by their close time."""
    o = d.resample(rule, label="right", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
    pc = o.Close.shift()
    tr = pd.concat([o.High - o.Low, (o.High - pc).abs(), (o.Low - pc).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    e20, e50 = o.Close.ewm(span=20, adjust=False).mean(), o.Close.ewm(span=50, adjust=False).mean()
    macd = o.Close.ewm(span=12, adjust=False).mean() - o.Close.ewm(span=26, adjust=False).mean()
    hist = macd - macd.ewm(span=9, adjust=False).mean()
    f = pd.DataFrame({f"{prefix}_atr": atr,
                      f"{prefix}_d20": (o.Close - e20) / atr, f"{prefix}_d50": (o.Close - e50) / atr,
                      f"{prefix}_s20_50": (e20 - e50) / atr, f"{prefix}_slope20": (e20 - e20.shift(3)) / atr,
                      f"{prefix}_macd": macd / atr, f"{prefix}_macdh": hist / atr,
                      f"{prefix}_r3": (o.Close - o.Close.shift(3)) / atr,
                      f"{prefix}_rsi": rsi(o.Close),
                      f"{prefix}_d200": (o.Close - o.Close.ewm(span=200, adjust=False).mean()) / atr})
    if prefix == "h60":                                              # ADX(14) on 60-min bars
        up, dn = o.High.diff(), -o.Low.diff()
        pdm = up.where((up > dn) & (up > 0), 0.0).rolling(14).sum()
        mdm = dn.where((dn > up) & (dn > 0), 0.0).rolling(14).sum()
        trs = tr.rolling(14).sum()
        dx = 100 * (pdm - mdm).abs() / (pdm + mdm)
        f["h60_adx"] = dx.rolling(14).mean()
        f["h60_di"] = 100 * (pdm - mdm) / trs
    f.index.name = "close_time"
    close_time = d.index + pd.Timedelta(minutes=1)
    m = pd.merge_asof(pd.DataFrame({"close_time": close_time}), f.reset_index(), on="close_time", direction="backward")
    m.index = d.index
    return m.drop(columns="close_time")


def build(sym):
    d, n_rolls = load_raw(sym)
    C, O, H, L, V = d.Close, d.Open, d.High, d.Low, d.Volume
    # decision points: closes of 5-minute bars, 9:35-15:00 ET (trades flat by 15:59)
    rth_idx = np.flatnonzero(d.rth.to_numpy())
    tt_all = d.tmin.to_numpy()
    dec_mask = (tt_all[rth_idx] % 5 == 4) & (tt_all[rth_idx] >= 574) & (tt_all[rth_idx] <= 899)
    dec0 = np.flatnonzero(dec_mask)                       # positions within the RTH subset
    pick = rth_idx[dec0]                                  # positions within the full 1-min series
    F = {}

    def put(name, series):
        F[name] = np.asarray(series)[pick].astype(np.float32)

    # your 1-minute chart, on the full session
    for n in (8, 20, 50):
        d[f"ema{n}"] = C.ewm(span=n, adjust=False).mean()
    d["mom"] = C - C.shift(14)
    pc = C.shift()
    tr = pd.concat([H - L, (H - pc).abs(), (L - pc).abs()], axis=1).max(axis=1)
    d["atr"] = tr.rolling(14).mean()
    A = d.atr
    put("d_ema8", (C - d.ema8) / A); put("d_ema20", (C - d.ema20) / A); put("d_ema50", (C - d.ema50) / A)
    put("s_8_20", (d.ema8 - d.ema20) / A); put("s_20_50", (d.ema20 - d.ema50) / A)
    put("slope8", (d.ema8 - d.ema8.shift(5)) / A); put("slope20", (d.ema20 - d.ema20.shift(5)) / A)
    put("slope50", (d.ema50 - d.ema50.shift(10)) / A)
    put("since_x8_20", since_sign_change((d.ema8 - d.ema20).to_numpy()))
    put("since_x20_50", since_sign_change((d.ema20 - d.ema50).to_numpy()))
    put("mom", d.mom / A); put("dmom3", (d.mom - d.mom.shift(3)) / A)
    lo, hi = d.mom.rolling(60).min(), d.mom.rolling(60).max()
    put("mom_pct60", (d.mom - lo) / (hi - lo))
    put("since_mom_x", since_sign_change(d.mom.to_numpy()))
    put("rsi14", rsi(C))
    ema200 = C.ewm(span=200, adjust=False).mean()
    put("d_ema200", (C - ema200) / A); put("s_50_200", (d.ema50 - ema200) / A)
    top, bot = np.maximum(O, C), np.minimum(O, C)
    for k in range(3):
        put(f"c{k}_body", ((C - O) / A).shift(k)); put(f"c{k}_uw", ((H - top) / A).shift(k))
        put(f"c{k}_lw", ((bot - L) / A).shift(k))
    put("relvol", V / V.rolling(30).mean().shift())
    put("vol_tod", V / V.groupby(d.tmin).transform(lambda s: s.rolling(20, min_periods=5).mean().shift()))
    for n in (5, 15, 30, 60):
        put(f"r{n}", (C - C.shift(n)) / A)
    put("eff60", (C - C.shift(60)) / C.diff().abs().rolling(60).sum())

    # higher timeframes (closed bars only)
    for rule, p in (("5min", "h5"), ("15min", "h15"), ("60min", "h60")):
        h = htf(d, rule, p)
        if p == "h5":
            d["atr5"] = h.h5_atr
            put("atr5_over_atr1", h.h5_atr / A)
        for c in h.columns:
            if not c.endswith("_atr"):
                put(c, h[c])
        del h

    # daily (session) trend and regime
    g = d.groupby("sess")
    daily = g.agg(c=("Close", "last"), h=("High", "max"), l=("Low", "min"))
    daily["ema20"] = daily.c.ewm(span=20, adjust=False).mean()
    daily["range"] = daily.h - daily.l
    daily["datr"] = daily.range.rolling(14).mean()
    prev = daily.shift()
    m = lambda s: d.sess.map(s)
    datr = m(prev.datr)
    put("day_vs_ema20", (C - m(prev.ema20)) / datr)
    put("prev_day_ret", m((prev.c - prev.c.shift()) / prev.datr))
    put("ret_5d", m((prev.c - prev.c.shift(5)) / prev.datr))
    put("vol_regime", m(prev.datr / prev.range.rolling(100).median()))

    # levels: prior RTH day, overnight, opening range, initial balance, RTH VWAP, today's open
    r = d[d.rth]
    rd = r.groupby("sess").agg(rh=("High", "max"), rl=("Low", "min"), rc=("Close", "last"))
    rprev = rd.shift()
    for name, s_ in (("pd_high", rprev.rh), ("pd_low", rprev.rl), ("pd_close", rprev.rc)):
        put(f"d_{name}", (C - m(s_)) / datr)
    on = d[(d.tmin < 570) | (d.tmin >= 1080)]
    ond = on.groupby("sess").agg(oh=("High", "max"), ol=("Low", "min"))
    put("d_on_high", (C - m(ond.oh)) / datr)
    put("d_on_low", (C - m(ond.ol)) / datr)
    levels = {"on": (m(ond.oh), m(ond.ol), d.tmin >= 570)}
    for name, end_ in (("or", 585), ("ib", 630)):
        win = d.rth & (d.tmin < end_)
        hi_ = d.High.where(win).groupby(d.sess).transform("max")
        lo_ = d.Low.where(win).groupby(d.sess).transform("min")
        ok = d.tmin >= end_
        put(f"{name}_pos", ((C - lo_) / (hi_ - lo_)).where(ok))
        put(f"{name}_width", ((hi_ - lo_) / datr).where(ok))
        levels[name] = (hi_, lo_, ok)
    # minutes since today's first close above each high / below each low (-1 = not broken yet)
    for name, (hi_, lo_, ok) in levels.items():
        for side, broke in (("up", (C > hi_) & ok & d.rth), ("down", (C < lo_) & ok & d.rth)):
            first = d.tmin.where(broke).groupby(d.sess).cummin()
            put(f"{name}_break_{side}_mins", (d.tmin - first).fillna(-1))
    tp = (H + L + C) / 3
    rv = V.where(d.rth, 0)
    vwap = (tp * rv).groupby(d.sess).cumsum() / rv.groupby(d.sess).cumsum()
    put("d_vwap", (C - vwap) / d.atr5)
    put("d_open", (C - d.Open.where(d.tmin == 570).groupby(d.sess).transform("max")) / datr)

    # event days, detected from the bars (in real life these are scheduled in advance)
    rng1 = (H - L) / A.shift()
    ev830 = rng1.where(d.tmin == 510).groupby(d.sess).transform("max")
    put("event_830", (ev830 > 4).astype(float))
    ev14 = rng1.where((d.tmin == 840) & (d.index.dayofweek == 2)).groupby(d.sess).transform("max")
    put("event_1400", ((ev14 > 4) & (d.tmin >= 841)).astype(float))
    put("tmin", d.tmin); put("dow", d.index.dayofweek)

    # save the entry-time measures at every 5-minute decision point (9:35-15:00 ET)
    a5 = d.atr5.to_numpy()[pick]
    ok = np.isfinite(a5) & (a5 > 0)
    ts = d.index[pick][ok]
    X = pd.DataFrame({k: v[ok] for k, v in F.items()})
    pd.to_pickle({"X": X, "ts": ts, "date": d.sess.to_numpy()[pick][ok], "year": ts.year.to_numpy(),
                  "tmin": d.tmin.to_numpy()[pick][ok]}, f"data/fut_features_{sym}.pkl")
    print(f"{sym}: {len(d):,} one-minute bars ({d.sess.nunique()} sessions, {n_rolls} rolls back-adjusted), "
          f"{len(X):,} decision points x {X.shape[1]} measures", flush=True)

if __name__ == "__main__":
    for s in ("ES", "NQ"):
        build(s)
