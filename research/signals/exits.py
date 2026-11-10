"""
Trade simulation for signal entries with signal-based exits (no fixed holding time).

Timing (same as the pattern stats):
  * a pattern is known at the CLOSE of its last bar i; entry = OPEN of bar e = i+1 (same session and contract).
  * an exit signal is known at the close of bar j (j >= e); the exit fills at the OPEN of bar j+1.
  * everything is flat by 16:45 ET: the last bar whose close is at or before 16:45 (or the session's last bar on early
    closes / contract rolls) is the FORCED-EXIT bar F; a trade still open there exits at C[F]. Bars after 16:45 take
    no entries.
  * optional stop: long stop below the pattern's low (1 tick beyond), short stop above its high. Checked on every bar the
    trade is held (e .. last bar before the exit fill); fills at the stop or at the bar's open if it gapped through.
    A stop and an exit signal on the same bar: the stop comes first (the signal is only known at the close).
Results are in $ per micro contract after costs (sg.SPEC cost: 1 tick slippage each way + $1 commission).
Every signal is simulated on its own (no position netting between signals); the prop-account replay is separate.
"""
import numpy as np

import signals as sg

CUTOFF_MIN = 16 * 60 + 45            # flat by 16:45 ET
SESSION_END_MIN = 17 * 60            # Globex daily break 17:00-18:00 ET
# bars a pattern spans (for the stop beyond the pattern's extreme); breakouts: mother/NR7 bar up to 3 bars back
SPAN = {"engulfing": 2, "harami": 2, "piercing": 2, "dark_cloud": 2, "outside_bar": 2, "tweezer": 2,
        "morning_evening_star": 3, "three_soldiers_crows": 3, "three_inside": 3, "five_lower_lows_higher_highs": 6,
        "clv5_extreme": 5, "inside_bar_breakout": 3, "nr7_breakout": 3}
DIRECTIONAL = [k for k, (kind, _) in sg.PATTERN_RULES.items() if kind == "dir"]
FREQUENT = ["clv_extreme", "clv5_extreme", "bar_80_20", "tall_trend_bar", "nr7_breakout", "outside_bar",
            "inside_bar_breakout"]                 # each fires on 7-43% of bars
CLASSIC = [k for k in DIRECTIONAL if k not in FREQUENT]
EXIT_SETS = {
    "opp_same": "the SAME pattern fires in the opposite direction",
    "opp_classic": "any classic candle pattern fires in the opposite direction (" + ", ".join(CLASSIC) + ")",
    "opp_any": "ANY directional pattern fires in the opposite direction (includes the very frequent close-location ones)",
    "opp_any2": "at least 2 different directional patterns fire in the opposite direction on the same bar",
}


def session_frame(b, tf):
    """allowed[t]: bar t closes at or before 16:45 (or is not in the 16:45-17:00 tail); forced[t]: index of the forced
    exit bar of t's session/contract segment (last allowed bar of the segment)."""
    m = (b.index.hour * 60 + b.index.minute).to_numpy()
    tail = (m > CUTOFF_MIN - tf) & (m < SESSION_END_MIN)
    allowed = ~tail
    seg = b.seg.to_numpy()
    n = len(b)
    idx = np.where(allowed, np.arange(n), -1)
    # last allowed index per segment, then broadcast to every bar of the segment
    last = np.full(n, -1)
    starts = np.r_[0, np.flatnonzero(seg[1:] != seg[:-1]) + 1]
    ends = np.r_[starts[1:], n]
    run_max = np.maximum.reduceat(idx, starts)
    for s, e, v in zip(starts, ends, run_max):
        last[s:e] = v
    return allowed, last


def next_true(mask):
    """nxt[t] = smallest j >= t with mask[j], else len(mask)."""
    n = len(mask)
    pos = np.where(mask, np.arange(n), n)
    return np.minimum.accumulate(pos[::-1])[::-1]


def pattern_extreme(L, H, i, span, d):
    """stop reference: lowest low (long) / highest high (short) of bars i-span+1 .. i (same segment assumed)."""
    lo = L[i].copy(); hi = H[i].copy()
    for s in range(1, span):
        j = np.maximum(i - s, 0)
        lo = np.minimum(lo, L[j]); hi = np.maximum(hi, H[j])
    return np.where(d > 0, lo, hi)


def simulate(O, H, L, C, e, d, x_end, x_price, stop=None, trail_lo=None, trail_hi=None, tick=0.25, target=None):
    """Walk each trade bar by bar from its entry bar e to its planned exit.
    x_end[k]: last bar the trade is HELD (inclusive) before its planned exit fill; x_price[k]: planned exit price.
    stop[k]: initial stop level (NaN = none). On each held bar the stop is checked first (fill at the stop, or at the
    bar's open if it gapped through), then the target (limit: needs a trade 1 tick THROUGH it, fills at the target).
    trail_lo / trail_hi: per-bar arrays with the level of a swing low / high CONFIRMED at that bar's close (NaN
    otherwise). After each held bar, a long's stop ratchets up to (newly confirmed swing low - 1 tick), a short's down
    to (swing high + 1 tick); it never loosens. The new stop applies from the NEXT bar.
    Returns exit price, exit bar, how (0 = planned exit, 1 = stop, 2 = target), MFE in points over held bars."""
    n_tr = len(e)
    px = x_price.astype(float).copy()
    xb = x_end.copy()
    how = np.zeros(n_tr, np.int8)
    mfe = np.zeros(n_tr)
    entry = O[e]
    st = np.full(n_tr, np.nan) if stop is None else np.asarray(stop, float).copy()
    tg = None if target is None else np.asarray(target, float)
    trail = trail_lo is not None
    act = np.arange(n_tr)
    k = 0
    while len(act):
        t = e[act] + k
        live = t <= x_end[act]
        act, t = act[live], t[live]
        if not len(act):
            break
        dd = d[act]
        s = st[act]
        hit = np.where(dd > 0, L[t] <= s, H[t] >= s) & np.isfinite(s)
        if hit.any():
            h_idx = act[hit]; th = t[hit]
            px[h_idx] = np.where(d[h_idx] > 0, np.minimum(O[th], st[h_idx]), np.maximum(O[th], st[h_idx]))
            xb[h_idx] = th; how[h_idx] = 1
            act, t, dd = act[~hit], t[~hit], dd[~hit]
        if tg is not None and len(act):
            g = tg[act]
            hit = np.where(dd > 0, H[t] >= g + tick, L[t] <= g - tick) & np.isfinite(g)
            if hit.any():
                h_idx = act[hit]
                px[h_idx] = tg[h_idx]; xb[h_idx] = t[hit]; how[h_idx] = 2
                act, t, dd = act[~hit], t[~hit], dd[~hit]
        if not len(act):
            break
        fav = np.where(dd > 0, H[t] - entry[act], entry[act] - L[t])
        mfe[act] = np.maximum(mfe[act], fav)
        if trail:
            lo_new, hi_new = trail_lo[t], trail_hi[t]
            cur = st[act]
            up = np.where(dd > 0, np.fmax(cur, lo_new - tick), np.fmin(cur, hi_new + tick))
            # fmax/fmin ignore NaN: NaN current stop + new level -> the new level; no new level -> unchanged
            st[act] = up
        k += 1
    return px, xb, how, mfe


def fresh(mask):
    """True on bars where mask becomes True (was False on the previous bar)."""
    prev = np.r_[False, mask[:-1]]
    return mask & ~prev


def plan_exits(e, d, forced, exit_bear_next, exit_bull_next, O, C):
    """Opposite-signal exit plan (before stops): first opposite signal at bar j >= e; exit at O[j+1] if j < F, else the
    forced exit at C[F]. Returns held-through bar, exit price, reason (1 = signal, 0 = forced 16:45/session end)."""
    F = forced[e]
    j = np.where(d > 0, exit_bear_next[e], exit_bull_next[e])
    sig = j < F
    x_end = np.where(sig, j, F)
    x_price = np.where(sig, O[np.minimum(j + 1, len(O) - 1)], C[F])
    return x_end, x_price, sig.astype(np.int8)
