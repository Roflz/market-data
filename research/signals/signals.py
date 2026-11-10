"""
Signal detection: candlestick patterns and context signals on any bar timeframe, plus the price move that followed.

  bars(sym, tf)        1-minute CME bars (research_lib.bars_1m) aggregated to tf-minute bars aligned to the New York
                       clock (5, 15, 60 ... minutes; 120 = even hours). A bar never spans a contract roll or the daily
                       17:00-18:00 ET break (bars are built per Globex session and contract).
  context(b)           indicators known at each bar's CLOSE (no look-ahead):
                         ema8/ema20/ema50, trend (+1 if EMA8>EMA20>EMA50, -1 if EMA8<EMA20<EMA50, else 0),
                         atr14 (Wilder), mom14 = 100*C/C[14 bars ago], mom_slope (+1 rising / -1 falling / 0),
                         swing_lo / swing_hi = the latest CONFIRMED fractal swing low/high (k=3 bars each side; a pivot
                         counts only once the 3 bars after it have closed), dist_sup / dist_res = distance from the close
                         to them in ATRs, vwap (session VWAP from 1-minute bars) and dist_vwap in ATRs, clv = close
                         location in the bar's range, rel_range = range / average range of the previous 20 bars,
                         vol_regime = ATR / its 100-bar average, tod = time-of-day bucket, dow = weekday.
  patterns(b)          one column per pattern: +1 bullish, -1 bearish, 0 none; neutral patterns use +1 for "present".
                         Exact rules are in PATTERN_RULES. Multi-bar patterns need all their bars in one session and
                         contract. Averages (avgB10, avgR10, ...) use the bars BEFORE the pattern's first bar (same
                         contract; they may reach back across the daily 17:00-18:00 break). No pattern fires on a
                         zero-range bar or when the 10-bar average range is 0 (dead market).
  forward(b, h)        what followed: entry at the NEXT bar's open (a signal is only known at the bar close); for each
                         horizon h bars: move to the close of bar t+h (points, ATRs, bp of price); MFE/MAE over the next
                         10 bars in ATRs. Never across a session end or roll (NaN instead).
Usage: see run_signal_stats.py. All prices raw (not back-adjusted); everything per contract run.
"""
import numpy as np
import pandas as pd

import research_lib as rl

SPEC = {"ES": dict(usd=5.0, tick=0.25, micro="MES"), "NQ": dict(usd=2.0, tick=0.25, micro="MNQ"),
        "YM": dict(usd=0.5, tick=1.0, micro="MYM")}
for _s in SPEC.values():
    _s["cost"] = 2 * _s["tick"] * _s["usd"] + 1.0              # 1 tick each way + $1.00 commission per round trip
HORIZONS = (1, 3, 5, 10, 20)
K_SWING = 3


# --------------------------------------------------------------------------------------------- bars
def bars(sym, tf):
    m = rl.bars_1m(sym)
    df = pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64),
                       "L": m.Low.to_numpy(np.float64), "C": m.Close.to_numpy(np.float64),
                       "V": m.Volume.to_numpy(np.float64), "inst": m.instrument_id.to_numpy(),
                       "sess": m.sess.to_numpy()}, index=m.index.tz_localize(None))
    del m
    tp = (df.H + df.L + df.C) / 3
    g = df.groupby([df.sess, df.inst], sort=False)
    df["vwap"] = (tp * df.V).groupby([df.sess, df.inst], sort=False).cumsum() / g.V.cumsum().replace(0, np.nan)
    if tf == 1:
        out = df
    else:
        bucket = df.index.floor(f"{tf}min")
        key = [df.sess, df.inst, bucket]
        out = df.groupby(key, sort=False).agg(O=("O", "first"), H=("H", "max"), L=("L", "min"), C=("C", "last"),
                                              V=("V", "sum"), vwap=("vwap", "last"))
        out = out.reset_index().rename(columns={"level_2": "ts"})
        out = out.rename(columns={out.columns[2]: "ts"}).set_index("ts").sort_index()
    out["seg"] = (out.sess.ne(out.sess.shift()) | out.inst.ne(out.inst.shift())).cumsum()
    out["run"] = out.inst.ne(out.inst.shift()).cumsum()                 # one contract = one run (indicators reset)
    return out


# --------------------------------------------------------------------------------------------- swings
def pivots(b, k):
    """Fractal swing points: a swing low at bar p has a lower low than each of the k bars before AND after it (strict),
    all in the same contract run. It is only KNOWN at the close of bar p+k. Returns (lo_piv, hi_piv) boolean arrays
    indexed by the pivot bar p."""
    run = b.run.to_numpy()
    hl, hh = b.L.to_numpy(), b.H.to_numpy()
    n = len(b)
    lo = np.ones(n, bool); hi = np.ones(n, bool)
    for j in range(1, k + 1):
        lo &= (hl < np.roll(hl, j)) & (hl < np.roll(hl, -j))
        hi &= (hh > np.roll(hh, j)) & (hh > np.roll(hh, -j))
    same = np.zeros(n, bool)
    same[k:n - k] = (run[:n - 2 * k] == run[2 * k:])
    lo &= same; hi &= same
    lo[:k] = lo[n - k:] = False; hi[:k] = hi[n - k:] = False
    return lo, hi


# --------------------------------------------------------------------------------------------- context
def _by_run(s, run, f):
    return s.groupby(run, sort=False).transform(f)


def _valid(run, n):
    """True where the previous n bars (and this one) are in the same run."""
    return run.eq(run.shift(n))


def context(b, tick=0.25, k_swing=K_SWING):
    run = b.run
    c = pd.DataFrame(index=b.index)
    for n in (8, 10, 20, 50):
        e = _by_run(b.C, run, lambda s, n=n: s.ewm(span=n, adjust=False).mean())
        c[f"ema{n}"] = e.where(_valid(run, n))
    c["trend"] = np.select([(c.ema8 > c.ema20) & (c.ema20 > c.ema50), (c.ema8 < c.ema20) & (c.ema20 < c.ema50)], [1, -1], 0)
    c.loc[c.ema50.isna(), "trend"] = 0
    pc = b.C.shift().where(_valid(run, 1))
    tr = pd.concat([b.H - b.L, (b.H - pc).abs(), (b.L - pc).abs()], axis=1).max(axis=1)
    atr = _by_run(tr, run, lambda s: s.ewm(alpha=1 / 14, adjust=False).mean()).where(_valid(run, 14))
    c["atr14"] = atr.clip(lower=2 * tick)          # floor: 2 ticks, so near-zero ranges in dead markets don't explode ratios
    c["mom14"] = (100 * b.C / b.C.shift(14)).where(_valid(run, 14))
    c["mom_slope"] = np.sign(c.mom14 - c.mom14.shift()).fillna(0).astype(int)
    k = k_swing
    lo_piv, hi_piv = pivots(b, k)
    hl, hh = b.L.to_numpy(), b.H.to_numpy()
    # level becomes known at bar p+k (its close)
    sl = pd.Series(np.nan, index=b.index); sh = pd.Series(np.nan, index=b.index)
    p = np.flatnonzero(lo_piv); sl.iloc[p + k] = hl[p]
    p = np.flatnonzero(hi_piv); sh.iloc[p + k] = hh[p]
    c["swing_lo"] = sl.groupby(run, sort=False).ffill()
    c["swing_hi"] = sh.groupby(run, sort=False).ffill()
    c["dist_sup"] = (b.C - c.swing_lo) / c.atr14
    c["dist_res"] = (c.swing_hi - b.C) / c.atr14
    c["dist_vwap"] = (b.C - b.vwap) / c.atr14
    rng = (b.H - b.L)
    c["clv"] = ((b.C - b.L) / rng).where(rng > 0)
    c["rel_range"] = (rng / rng.shift().rolling(20).mean()).where(_valid(run, 20))
    c["vol_regime"] = (c.atr14 / c.atr14.rolling(100).mean()).where(_valid(run, 100))
    m = b.index.hour * 60 + b.index.minute
    c["tod"] = pd.cut(m, [-1, 119, 479, 569, 629, 899, 959, 1019, 1079, 1440], right=True,
                      labels=["Asia (0-2)", "Europe (2-8)", "US pre (8-9:30)", "Open (9:30-10:30)", "Midday (10:30-15)",
                              "Close (15-16)", "Post (16-17)", "closed", "Asia (18-24)"]).astype(str)
    c.loc[c.tod == "Asia (18-24)", "tod"] = "Asia (18-2)"
    c.loc[c.tod == "Asia (0-2)", "tod"] = "Asia (18-2)"
    c["dow"] = (b.index + pd.Timedelta(hours=6)).dayofweek               # session weekday (Sunday night -> Monday)
    return c


# --------------------------------------------------------------------------------------------- patterns
PATTERN_RULES = {
    # name: (kind, rule text)   kind: 'dir' = directional (textbook direction), 'neutral' = no direction
    "doji": ("neutral", "body <= 0.1 x avgR10 (TA-Lib BodyDoji)"),
    "dragonfly_doji": ("dir", "doji AND upper shadow <= 0.1 x range AND lower shadow >= 0.6 x range -> bullish"),
    "gravestone_doji": ("dir", "doji AND lower shadow <= 0.1 x range AND upper shadow >= 0.6 x range -> bearish"),
    "hammer": ("dir", "range >= avgR10, lower shadow >= 2 x body, upper <= 0.1 x range, prior close < EMA10 -> bullish"),
    "hanging_man": ("dir", "hammer shape after prior close > EMA10 -> bearish (textbook)"),
    "inverted_hammer": ("dir", "range >= avgR10, upper >= 2 x body, lower <= 0.1 x range, prior close < EMA10 -> bullish (textbook)"),
    "shooting_star": ("dir", "inverted-hammer shape after prior close > EMA10 -> bearish"),
    "marubozu": ("dir", "body >= 0.9 x range AND body > avgB10; direction of the body"),
    "spinning_top": ("neutral", "body <= 0.3 x range AND both shadows >= body AND range >= 0.5 x avgR10"),
    "engulfing": ("dir", "bar2 body engulfs bar1 body (opposite colours, at least one side strictly), body2 > avgB10, "
                         "bar1 against the EMA10 trend; bullish after a down bar below EMA10, bearish mirror"),
    "harami": ("dir", "body1 > avgB10, body2 <= avgB10, body2 strictly inside body1; bullish if bar1 down and close1 < EMA10, bearish mirror"),
    "piercing": ("dir", "bar1 down with body > avgB10, bar2 opens <= close1 and closes above the middle of body1 but below open1 -> bullish"),
    "dark_cloud": ("dir", "mirror of piercing -> bearish"),
    "morning_evening_star": ("dir", "TA-Lib style 3 bars: long body 1, small body 2 gapping beyond body 1, long body 3 closing "
                                    "beyond 30% into body 1; morning (bullish) after close1 < EMA10, evening mirror"),
    "three_soldiers_crows": ("dir", "3 bars same colour, each closing beyond the previous close, each opening inside the "
                                    "previous body, bodies > 0.5 x avgB10, shadow on the close side <= 0.3 x body"),
    "three_inside": ("dir", "harami (body2 inside body1) then bar3 closes beyond open1 in the reversal direction"),
    "inside_bar": ("neutral", "high < previous high AND low > previous low"),
    "outside_bar": ("dir", "high > previous high AND low < previous low; direction of the close vs open"),
    "pin_bar": ("dir", "range >= avgR10 and one shadow >= 2/3 of range: long lower shadow bullish, long upper bearish"),
    "nr7": ("neutral", "range smaller than each of the previous 6 ranges"),
    "tweezer": ("dir", "lows within 0.05 x avgR10, bar1 down, bar2 up, close1 < EMA10 -> bullish bottom; highs mirror -> bearish top"),
    "inside_bar_breakout": ("dir", "first close beyond the mother bar's high/low within 3 bars after an inside bar"),
    "nr7_breakout": ("dir", "first close beyond an NR7 bar's high/low within 3 bars"),
    "clv_extreme": ("dir", "range >= 4 ticks; close in the bottom 20% of the range -> bullish, top 20% -> bearish (reversal)"),
    "bar_80_20": ("dir", "range >= 4 ticks; opens in the top 20% and closes in the bottom 20% -> bullish (fade), mirror bearish"),
    "tall_trend_bar": ("dir", "range > 1.46 x avgR22 and body >= 0.5 x range; direction of the body (continuation)"),
    "five_lower_lows_higher_highs": ("dir", "5 consecutive lower lows -> bullish (reversal); 5 higher highs -> bearish"),
    "clv5_extreme": ("dir", "close within the bottom 10% of the last 5 bars' range -> bullish; top 10% -> bearish"),
}


def patterns(b, ctx, tick=0.25):
    O, H, L, C = (b[x].to_numpy() for x in "OHLC")
    seg = b.seg.to_numpy(); runa = b.run.to_numpy()
    n = len(b)
    body = np.abs(C - O); rng = H - L
    up = H - np.maximum(O, C); lo = np.minimum(O, C) - L
    bull, bear = C > O, C < O

    def prev(a, k=1):
        out = np.full(n, np.nan) if a.dtype.kind == "f" else np.zeros(n, a.dtype)
        out[k:] = a[:-k]
        return out

    def avg_before(a, w, lag=1):
        """mean of a over the w bars before bar t-lag+1 (i.e. ending at t-lag), same segment required."""
        s = pd.Series(a).shift(lag).rolling(w).mean().to_numpy()
        # the lookback may span the 17:00-18:00 break (same contract run), so overnight bars get averages too
        m = w + lag - 1
        same = np.zeros(n, bool)
        if m == 0:
            same[:] = True
        elif n > m:
            same[m:] = runa[m:] == runa[:-m]
        return np.where(same, s, np.nan)

    def same_seg(k):
        out = np.zeros(n, bool)
        out[k:] = seg[k:] == seg[:-k]
        return out

    avgB10, avgR10, avgR22 = avg_before(body, 10), avg_before(rng, 10), avg_before(rng, 22)
    avgB10_1, avgB10_2 = avg_before(body, 10, 2), avg_before(body, 10, 3)
    ema10 = ctx.ema10.to_numpy()
    below = prev(C) < prev(ema10); above = prev(C) > prev(ema10)
    s1, s2, s3, s6 = same_seg(1), same_seg(2), same_seg(3), same_seg(6)
    P = {}
    doji = body <= 0.1 * avgR10
    P["doji"] = doji.astype(int)
    P["dragonfly_doji"] = (doji & (up <= 0.1 * rng) & (lo >= 0.6 * rng) & (rng > 0)).astype(int)
    P["gravestone_doji"] = -(doji & (lo <= 0.1 * rng) & (up >= 0.6 * rng) & (rng > 0)).astype(int)
    ham_shape = (rng >= avgR10) & (lo >= 2 * body) & (up <= 0.1 * rng)
    inv_shape = (rng >= avgR10) & (up >= 2 * body) & (lo <= 0.1 * rng)
    P["hammer"] = (ham_shape & below & s1).astype(int)
    P["hanging_man"] = -(ham_shape & above & s1).astype(int)
    P["inverted_hammer"] = (inv_shape & below & s1).astype(int)
    P["shooting_star"] = -(inv_shape & above & s1).astype(int)
    maru = (body >= 0.9 * rng) & (body > avgB10)
    P["marubozu"] = np.where(maru & bull, 1, np.where(maru & bear, -1, 0))
    P["spinning_top"] = ((body <= 0.3 * rng) & (up >= body) & (lo >= body) & (rng >= 0.5 * avgR10) & (body > 0)).astype(int)
    O1, H1, L1, C1 = prev(O), prev(H), prev(L), prev(C)
    body1 = np.abs(C1 - O1); bull1, bear1 = C1 > O1, C1 < O1
    eng_b = bear1 & bull & (O <= C1) & (C >= O1) & ((O < C1) | (C > O1)) & (body > avgB10) & below
    eng_s = bull1 & bear & (O >= C1) & (C <= O1) & ((O > C1) | (C < O1)) & (body > avgB10) & above
    P["engulfing"] = np.where(eng_b & s1, 1, np.where(eng_s & s1, -1, 0))
    inside_body = (np.maximum(O, C) < np.maximum(O1, C1)) & (np.minimum(O, C) > np.minimum(O1, C1))
    har = (body1 > avgB10_1) & (body <= avgB10) & inside_body & s1
    P["harami"] = np.where(har & bear1 & below, 1, np.where(har & bull1 & above, -1, 0))
    mid1 = (O1 + C1) / 2
    P["piercing"] = (bear1 & (body1 > avgB10_1) & bull & (O <= C1) & (C > mid1) & (C < O1) & s1).astype(int)
    P["dark_cloud"] = -(bull1 & (body1 > avgB10_1) & bear & (O >= C1) & (C < mid1) & (C > O1) & s1).astype(int)
    O2, C2 = prev(O, 2), prev(C, 2)
    body2 = np.abs(C2 - O2)
    ema10_2 = prev(ema10, 2)
    star_m = ((C2 < O2) & (body2 > avgB10_2) & (body1 <= avgB10_1) & (np.maximum(O1, C1) < np.minimum(O2, C2))
              & bull & (body > avgB10) & (C > C2 + 0.3 * body2) & (C2 < ema10_2) & s2)
    star_e = ((C2 > O2) & (body2 > avgB10_2) & (body1 <= avgB10_1) & (np.minimum(O1, C1) > np.maximum(O2, C2))
              & bear & (body > avgB10) & (C < C2 - 0.3 * body2) & (C2 > ema10_2) & s2)
    P["morning_evening_star"] = np.where(star_m, 1, np.where(star_e, -1, 0))
    C3 = prev(C, 3)
    def soldiers(sign):
        ok = s2.copy()
        for k in (0, 1, 2):
            Ok, Ck = prev(O, k) if k else O, prev(C, k) if k else C
            Ck1, Ok1 = prev(C, k + 1), prev(O, k + 1)
            bk = np.abs(Ck - Ok)
            sh = (prev(up, k) if k else up) if sign > 0 else (prev(lo, k) if k else lo)
            ok &= (np.sign(Ck - Ok) == sign) & (bk > 0.5 * (prev(avgB10, k) if k else avgB10)) & (sh <= 0.3 * bk)
            if k < 2:
                ok &= (sign * (Ck - Ck1) > 0) & (Ok >= np.minimum(Ok1, Ck1)) & (Ok <= np.maximum(Ok1, Ck1))
        return ok
    P["three_soldiers_crows"] = np.where(soldiers(1), 1, np.where(soldiers(-1), -1, 0))
    har1 = np.r_[False, har[:-1]]
    P["three_inside"] = np.where(har1 & (C2 < O2) & bull & (C > O2) & (C2 < ema10_2) & s2, 1,
                                 np.where(har1 & (C2 > O2) & bear & (C < O2) & (C2 > ema10_2) & s2, -1, 0))
    inside = (H < H1) & (L > L1) & s1
    P["inside_bar"] = inside.astype(int)
    outside = (H > H1) & (L < L1) & s1
    P["outside_bar"] = np.where(outside & bull, 1, np.where(outside & bear, -1, 0))
    pin_b = (rng >= avgR10) & (lo >= 2 / 3 * rng); pin_s = (rng >= avgR10) & (up >= 2 / 3 * rng)
    P["pin_bar"] = np.where(pin_b & ~pin_s, 1, np.where(pin_s & ~pin_b, -1, 0))
    r_prev = np.column_stack([prev(rng, k) for k in range(1, 7)])
    nr7 = (rng < np.nanmin(r_prev, axis=1)) & s6 & np.isfinite(r_prev).all(axis=1)
    P["nr7"] = nr7.astype(int)
    tw_b = (np.abs(L - L1) <= 0.05 * avgR10) & bear1 & bull & below & s1
    tw_s = (np.abs(H - H1) <= 0.05 * avgR10) & bull1 & bear & above & s1
    P["tweezer"] = np.where(tw_b, 1, np.where(tw_s, -1, 0))

    def breakout(mark, hi_lvl, lo_lvl):
        """first close beyond the stored levels within 3 bars after a marked bar (same segment)."""
        out = np.zeros(n, int)
        idx = np.flatnonzero(mark)
        for i in idx:
            for j in range(i + 1, min(i + 4, n)):
                if seg[j] != seg[i]:
                    break
                if C[j] > hi_lvl[i]:
                    out[j] = 1; break
                if C[j] < lo_lvl[i]:
                    out[j] = -1; break
        return out
    P["inside_bar_breakout"] = breakout(inside, H1, L1)            # mother bar = bar before the inside bar
    P["nr7_breakout"] = breakout(nr7, H, L)
    big = rng >= 4 * tick
    clv = np.where(rng > 0, (C - L) / np.where(rng > 0, rng, 1), np.nan)
    olv = np.where(rng > 0, (O - L) / np.where(rng > 0, rng, 1), np.nan)
    P["clv_extreme"] = np.where(big & (clv <= 0.2), 1, np.where(big & (clv >= 0.8), -1, 0))
    P["bar_80_20"] = np.where(big & (olv >= 0.8) & (clv <= 0.2), 1, np.where(big & (olv <= 0.2) & (clv >= 0.8), -1, 0))
    tall = (rng > 1.46 * avgR22) & (body >= 0.5 * rng) & big
    P["tall_trend_bar"] = np.where(tall & bull, 1, np.where(tall & bear, -1, 0))
    s5 = same_seg(5)
    ll = s5.copy(); hhh = s5.copy()
    for k in range(5):
        ll &= prev(L, k) < prev(L, k + 1) if k else L < L1
        hhh &= prev(H, k) > prev(H, k + 1) if k else H > H1
    P["five_lower_lows_higher_highs"] = np.where(ll, 1, np.where(hhh, -1, 0))
    s4 = same_seg(4)
    hh5 = pd.Series(H).rolling(5).max().to_numpy(); ll5 = pd.Series(L).rolling(5).min().to_numpy()
    clv5 = np.where(hh5 > ll5, (C - ll5) / np.where(hh5 > ll5, hh5 - ll5, 1), np.nan)
    P["clv5_extreme"] = np.where(s4 & (clv5 <= 0.1), 1, np.where(s4 & (clv5 >= 0.9), -1, 0))
    # No pattern on flat (zero-range) bars or in dead stretches: a bar with one price (O=H=L=C, common in thin 1-minute
    # data and limit-locked markets) is not a candle, and when the 10-bar average range is 0 every "x times the average"
    # test passes trivially. Every bar of a multi-bar pattern must have a range.
    live = rng > 0
    dead = ~(avgR10 > 0)
    span = {"engulfing": 2, "harami": 2, "piercing": 2, "dark_cloud": 2, "tweezer": 2, "inside_bar": 2, "outside_bar": 2,
            "morning_evening_star": 3, "three_soldiers_crows": 3, "three_inside": 3}
    for k in P:
        ok = live & ~dead
        for j in range(1, span.get(k, 1)):
            ok &= prev(live, j).astype(bool)
        P[k] = np.where(ok, P[k], 0)
    out = pd.DataFrame({k: np.nan_to_num(v).astype(np.int8) for k, v in P.items()}, index=b.index)
    return out


# --------------------------------------------------------------------------------------------- forward moves
def forward(b, ctx):
    O, H, L, C = (b[x].to_numpy() for x in "OHLC")
    seg = b.seg.to_numpy(); n = len(b)
    atr = ctx.atr14.to_numpy()
    entry = np.full(n, np.nan); entry[:-1] = np.where(seg[1:] == seg[:-1], O[1:], np.nan)
    f = {}
    for h in HORIZONS:
        x = np.full(n, np.nan)
        ok = np.zeros(n, bool); ok[:-h] = seg[h:] == seg[:-h]
        x[:-h] = C[h:]
        x = np.where(ok, x, np.nan)
        f[f"fwd{h}_pts"] = x - entry
        f[f"fwd{h}_atr"] = (x - entry) / atr
        f[f"fwd{h}_bp"] = 1e4 * (x - entry) / entry
    hmax = pd.Series(H[::-1]).rolling(10, min_periods=1).max().to_numpy()[::-1]     # max of H[t..t+9]
    lmin = pd.Series(L[::-1]).rolling(10, min_periods=1).min().to_numpy()[::-1]
    mfe = np.full(n, np.nan); mae = np.full(n, np.nan)
    ok10 = np.zeros(n, bool); ok10[:-10] = seg[10:] == seg[:-10]
    mfe[:-1] = hmax[1:]; mae[:-1] = lmin[1:]
    f["up10_atr"] = np.where(ok10, (mfe - entry) / atr, np.nan)                  # best rise over next 10 bars
    f["down10_atr"] = np.where(ok10, (entry - mae) / atr, np.nan)                # worst fall over next 10 bars
    f["entry"] = entry
    return pd.DataFrame(f, index=b.index)
