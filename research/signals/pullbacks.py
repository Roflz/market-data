"""
Pullback detector (long setups; shorts are the exact mirror).

  detect(b, ctx, k_leg=5, sym=None, tf=None) -> DataFrame, one row per pullback.

Definition (long; for shorts swap highs and lows):
  1. Impulse leg: a swing low SL followed by a swing high SH, both fractal swings with k_leg bars each side
     (signals.pivots), same contract run. SL is the latest k_leg swing low before SH; SL must be the lowest low and SH
     the highest high of the bars SL..SH. Trend must be +1 (EMA8 > EMA20 > EMA50) at the SH bar.
  2. Pullback low PL: the FIRST 3-bar swing low after SH. It must be above SL (a higher low; if the first 3-bar swing
     low after SH is at or below SL, the leg has no pullback) and it must be the lowest low since SH.
     No close above SH is allowed from SH up to the event bar (otherwise the pullback was already over).
  3. Depth = (SH - PL) / (SH - SL); kept when 0.1 <= depth < 1.
  4. Event bar = the bar at whose close the whole setup is known: PL + 3 (the 3 bars after PL have closed).
     If SH (needs k_leg bars after it) is confirmed later than that, the event waits for SH's confirmation
     (column event_wait > 0; no new low below PL is allowed in that wait). All stats use information up to the
     event bar's close only; the outcome columns are the only look-ahead.
  5. Outcome ("what happened next"), from the event bar's close: within 40 bars, same session and contract, flat
     by 16:45 ET (a bar may be used only if it ENDS by 16:45, or belongs to the evening part of the session):
       continuation = a high above SH comes before a close below PL (if one bar does both, the high came first:
       a close is the last price of a bar); failure = a close below PL first; neither = none in the window;
       no_time = no bar left in the window. mfe/mae = best and worst move from the event close over the whole
       window (points and $ per micro contract), end_pts = close of the last window bar minus the event close.
     All moves are "in the trade's direction": + is good for the trade (up for longs, down for shorts).
     to_SH_pts / to_PL_pts = distance from the event close to SH (target side) and to PL (stop side), known at the event.

Pattern list: every pattern that fired on bars PL-2 .. event; "+" = pattern points in the trade's direction,
"-" = against it (neutral patterns have no sign).
Divergence (hidden divergence): price made a higher low (PL above SL) but Momentum(14) at PL is lower than at SL.
mom_flip: Momentum(14) was above 100 at SH and is at/below 100 at PL (the pullback erased the 14-bar gain).

Bar-index columns i_SL, i_SH, i_PL, i_event are positions in b (b.iloc). For shorts they are the mirrored points:
i_SL = the leg's starting swing HIGH, i_SH = the leg's swing LOW, i_PL = the pullback HIGH. Prices SL, SH, PL are
the raw prices of those points.
"""
import numpy as np
import pandas as pd

import signals as sg

FIBS = (0.236, 0.382, 0.5, 0.618, 0.786)
K_PB = 3
HORIZON = 40
FLAT_MIN = 16 * 60 + 45          # flat by 16:45 ET
DEPTH_MIN = 0.1
FREQUENT = {"clv_extreme", "clv5_extreme", "bar_80_20", "nr7", "inside_bar", "doji", "spinning_top"}


def _tf_minutes(b):
    d = np.diff(b.index.asi8[:2000]) / 6e10
    d = d[d > 0]
    return int(np.min(d)) if len(d) else 1


def detect(b, ctx, k_leg=5, sym=None, tf=None, pats=None, horizon=HORIZON):
    """b: signals.bars(), ctx: signals.context(b) (k_swing does not matter here), pats: signals.patterns() (computed
    if None). sym selects the $ per point (SPEC[sym]['usd']); tf (minutes) is inferred from the index if None."""
    tf = tf or _tf_minutes(b)
    usd = sg.SPEC[sym]["usd"] if sym in sg.SPEC else np.nan
    tick = sg.SPEC[sym]["tick"] if sym in sg.SPEC else 0.25
    if pats is None:
        pats = sg.patterns(b, ctx, tick=tick)
    H, L, C = b.H.to_numpy(float), b.L.to_numpy(float), b.C.to_numpy(float)
    V = b.V.to_numpy(float)
    run, seg = b.run.to_numpy(), b.seg.to_numpy()
    n = len(b)
    mins = (b.index.hour * 60 + b.index.minute).to_numpy()
    # a bar may be held in the outcome window if it ends by 16:45, or is in the evening (18:00+) part of the session
    usable = (mins + tf <= FLAT_MIN) | (mins >= 18 * 60)
    trend = ctx.trend.to_numpy()
    ema20, ema50 = ctx.ema20.to_numpy(), ctx.ema50.to_numpy()
    mom = ctx.mom14.to_numpy()
    vwap = b.vwap.to_numpy(float)
    tod = ctx.tod.to_numpy() if "tod" in ctx else np.full(n, "")
    lo_k, hi_k = sg.pivots(b, k_leg)
    lo3, hi3 = sg.pivots(b, K_PB)
    pnames = list(pats.columns)
    pmat = pats.to_numpy()
    rows = []
    for d in (1, -1):
        # mirror to "long" arrays: hi/lo/cl in trade-direction terms
        if d > 0:
            hi, lo, cl, legL, legH, pbL = H, L, C, lo_k, hi_k, lo3
        else:
            hi, lo, cl, legL, legH, pbL = -L, -H, -C, hi_k, lo_k, hi3
        legL_idx = np.flatnonzero(legL)
        pb_idx = np.flatnonzero(pbL)
        for sh in np.flatnonzero(legH):
            if trend[sh] != d:
                continue
            j = np.searchsorted(legL_idx, sh) - 1
            if j < 0:
                continue
            sl = legL_idx[j]
            if run[sl] != run[sh]:
                continue
            if lo[sl] > lo[sl:sh + 1].min() or hi[sh] < hi[sl:sh + 1].max():
                continue
            q = np.searchsorted(pb_idx, sh, side="right")
            if q >= len(pb_idx):
                continue
            pl = pb_idx[q]
            if run[pl] != run[sh] or lo[pl] <= lo[sl]:
                continue                                           # first swing low after SH is not a higher low
            if lo[pl] > lo[sh + 1:pl + 1].min():
                continue                                           # a lower low came before PL: PL is not the low
            ev = max(pl + K_PB, sh + k_leg)
            if ev >= n or run[ev] != run[sh]:
                continue
            if cl[sh + 1:ev + 1].max() > hi[sh]:
                continue                                           # closed above SH before the setup was known
            if lo[pl + 1:ev + 1].min() < lo[pl]:
                continue                                           # PL broken while waiting for SH's confirmation
            leg = hi[sh] - lo[sl]
            depth = (hi[sh] - lo[pl]) / leg
            if not (DEPTH_MIN <= depth < 1):
                continue
            fi = int(np.argmin([abs(depth - f) for f in FIBS]))
            fib = FIBS[fi]
            # distances from PL to the lines: + = PL stopped short of the line (stayed on the trend side), - = went through
            e20 = lo[pl] - d * ema20[pl]
            e50 = lo[pl] - d * ema50[pl]
            vw = lo[pl] - d * vwap[pl]
            m_sl, m_sh, m_pl = mom[sl], mom[sh], mom[pl]
            dm = lambda m: d * (m - 100)                           # momentum in trade-direction terms
            imp = slice(sl + 1, sh + 1); pbz = slice(sh + 1, pl + 1)
            fired = []
            for r in range(max(pl - 2, 0), ev + 1):
                for c in np.flatnonzero(pmat[r]):
                    v = int(pmat[r, c]) * d
                    fired.append((pnames[c], v))
            seen = {}
            for nm, v in fired:
                seen.setdefault((nm, v), 0)
                seen[(nm, v)] += 1
            lab = lambda nm, v: nm + ("" if sg.PATTERN_RULES[nm][0] == "neutral" else ("+" if v > 0 else "-"))
            pat_str = " ".join(lab(nm, v) for (nm, v) in seen)
            pat_major = " ".join(lab(nm, v) for (nm, v) in seen if nm not in FREQUENT)
            n_with = sum(1 for (nm, v) in seen if v > 0 and sg.PATTERN_RULES[nm][0] == "dir")
            n_against = sum(1 for (nm, v) in seen if v < 0 and sg.PATTERN_RULES[nm][0] == "dir")
            # ---------------- outcome (look-ahead)
            w = []
            for t in range(ev + 1, min(ev + horizon, n - 1) + 1):
                if seg[t] != seg[ev] or not usable[t]:
                    break
                w.append(t)
            out, t_out = "no_time", -1
            if w:
                out = "neither"
                for t in w:
                    if hi[t] > hi[sh]:
                        out, t_out = "continuation", t; break
                    if cl[t] < lo[pl]:
                        out, t_out = "failure", t; break
                wa = np.array(w)
                mfe = max(0.0, hi[wa].max() - cl[ev]); mae = max(0.0, cl[ev] - lo[wa].min())
                endp = cl[wa[-1]] - cl[ev]
            else:
                mfe = mae = endp = np.nan
            px = lambda a, i: a[i] if d > 0 else -a[i]
            rows.append(dict(
                direction=d, i_SL=sl, i_SH=sh, i_PL=pl, i_event=ev,
                t_SL=b.index[sl], t_SH=b.index[sh], t_PL=b.index[pl], t_event=b.index[ev],
                SL=px(lo, sl), SH=px(hi, sh), PL=px(lo, pl), event_close=C[ev], event_wait=ev - (pl + K_PB),
                to_SH_pts=hi[sh] - cl[ev], to_PL_pts=cl[ev] - lo[pl],
                leg_pts=leg, leg_usd=leg * usd, pb_pts=hi[sh] - lo[pl], pb_usd=(hi[sh] - lo[pl]) * usd,
                depth=depth, fib_near=fib, fib_dist=depth - fib, fib_dist_pts=(depth - fib) * leg,
                PL_to_ema20=e20, PL_to_ema50=e50, PL_to_vwap=vw,
                touch_ema20=bool(e20 <= 0), touch_ema50=bool(e50 <= 0), touch_vwap=bool(vw <= 0),
                mom_SL=m_sl, mom_SH=m_sh, mom_PL=m_pl,
                divergence=bool(np.isfinite(m_pl) and np.isfinite(m_sl) and dm(m_pl) < dm(m_sl)),
                mom_flip=bool(np.isfinite(m_pl) and np.isfinite(m_sh) and dm(m_sh) > 0 >= dm(m_pl)),
                bars_impulse=sh - sl, bars_pullback=pl - sh,
                vol_impulse=V[imp].mean(), vol_pullback=V[pbz].mean(),
                vol_ratio=V[pbz].mean() / V[imp].mean() if V[imp].mean() > 0 else np.nan,
                trend_event=int(trend[ev]) * d, trend_still=bool(trend[ev] == d),
                patterns=pat_str, patterns_major=pat_major, n_pat_with=n_with, n_pat_against=n_against,
                time=b.index[ev].strftime("%H:%M"), tod=tod[ev], year=b.index[ev].year,
                outcome=out, bars_to_outcome=(t_out - ev) if t_out > 0 else np.nan, i_outcome=t_out,
                n_window=len(w), mfe_pts=mfe, mae_pts=mae, mfe_usd=mfe * usd, mae_usd=mae * usd,
                end_pts=endp, end_usd=endp * usd,
            ))
    df = pd.DataFrame(rows)
    if len(df):
        df = df.sort_values("i_event", kind="stable").reset_index(drop=True)
    return df


DEPTH_BUCKETS = [(-np.inf, 0.236, "<0.236"), (0.236, 0.382, "0.236-0.382"), (0.382, 0.5, "0.382-0.5"),
                 (0.5, 0.618, "0.5-0.618"), (0.618, 0.786, "0.618-0.786"), (0.786, np.inf, ">=0.786")]


def depth_bucket(depth):
    out = np.empty(len(depth), object)
    for a, z, lab in DEPTH_BUCKETS:
        out[(depth >= a) & (depth < z)] = lab
    return out
