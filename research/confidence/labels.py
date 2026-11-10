"""
Module 2 of the confidence study (SPEC.md): entry events, triple-barrier entry labels walked on 1-MINUTE bars, and
exit-decision rows for open trades.

  entry_events(b, P)            one row per (signal bar t, direction d) where at least one DIRECTIONAL pattern of
                                direction d fires (textbook direction). Stop reference = most extreme L (long) / H
                                (short) over the largest span of the patterns that fired, minus / plus 1 tick. Spans:
                                exits.SPAN (default 1 bar); the two breakouts use max(exits.SPAN, their ACTUAL extent)
                                (see breakout_spans: from the mother / NR7 bar to the breakout bar, up to 5 / 4 bars;
                                exits.SPAN's fixed 3 missed the mother bar on ~40% of ES inside_bar_breakout fires).
  random_events(b, frac, seed)  a random `frac` of the eligible bars, random direction, stop = the signal bar's own
                                low - 1 tick (long) / high + 1 tick (short). Baseline / "random entry" events.
  (both take sym= or tick=; without them the tick is inferred from b's price grid, with a warning on short frames)
  label_entries(sym, tf, b, events, target_R, max_bars)
                                entry at the OPEN of bar t+1, stop at the event's stop, target = entry + d*R*risk,
                                time limit = close of bar t+max_bars or the 16:45 forced-exit bar (whichever first).
                                The path is walked minute by minute; net $ per micro after costs per target R.
  exit_rows(sym, tf, b, F, events, max_bars, frac, seed)
                                one row per (trade, tf-bar k the trade is still open at the close of): feature row
                                F[k], trade state, and the label "exiting at the open of k+1 beats holding the
                                baseline trade (stop only, no target, time limit) to its end".

Event frame columns (both generators): t (signal bar start time), i (position of the signal bar in b), d (+1 long /
-1 short), patterns (list of pattern names; [] for random events), n_patterns, stop (price).

Timing / no look-ahead (SPEC "Timing rules"):
  * tf-bar index = START time (New York, tz-naive); its OHLC is known at start + tf.
  * an event on bar t is known at t's close; the entry fills at the OPEN of bar e = t+1, which must be in the same
    session segment `seg` (same session AND contract) and must not be later than the segment's 16:45 forced-exit bar
    (exits.session_frame). Events that cannot be entered that way are not generated (and are dropped by the labelers).
  * the stop reference uses bars t-span+1 .. t only (all closed at t's close), clamped to t's segment.
  * exits: a stop/target is checked on every 1-minute bar from the entry minute to the last minute of the time-limit
    bar. Exit-row features and trade state use bars <= k only; the label uses the future (it is the label).

Costs (SPEC "Costs"): every trade pays signals.SPEC[sym]["cost"] (= $1.00 commission + 1 tick slippage each way);
a STOP fill slips one EXTRA tick (fill = min(open, stop) - 1 tick for a long; mirror for a short). Targets are limit
orders: they need a print 1 tick THROUGH the target and fill exactly at the target (also on a gap through it).
If one minute touches both the stop and the target, the stop is assumed first.
Entry exactly AT the stop (risk 0) is not "past" it: it is walked like any trade, and its first minute (open = stop)
touches the stop, so it is a stop fill at stop -/+ 1 tick (pnl = -cost - 1 tick). Only an entry strictly beyond the
stop is "past the stop" (SPEC: exit at the entry open, loss = the costs). risk_pts / risk_usd can therefore be 0:
guard every division by risk downstream (exit_rows skips such trades - they never stay open past their first minute).

Exit rows are pooled across markets downstream (walkforward groups them by `trade`), so every exit row carries
`market` and a trade id that is unique across markets and calls: "<sym>:<src>:<signal bar start>:<L|S>" (a "#n"
suffix numbers repeats of an identical event within one call). The trade-state columns in R units are clipped to
R_CLIP (a 1-tick risk would otherwise give |open_R| in the hundreds and dominate a linear model).

1-minute mapping: every tf bar of signals.bars(sym, tf) is the group (sess, contract, floor(ts, tf)) of 1-minute bars.
We rebuild that mapping from research_lib.bars_1m and walk the 1-minute rows from the first minute of the entry bar to
the last minute of the time-limit bar in true chronological order. (On the yearly DST fall-back night the tz-naive
01:00-01:59 hour occurs twice and signals.bars merges both into the same tf bars; the walk then simply covers the
real minutes between those bars' first and last minute - a negligible once-a-year approximation.)
"""
import warnings

import numpy as np
import pandas as pd

import exits as ex
import research_lib as rl
import signals as sg

DIRECTIONAL = list(ex.DIRECTIONAL)                      # the 25 textbook-direction patterns
KIND = np.array(["time", "stop", "target"])             # exit_kind codes 0 / 1 / 2
_MIN = pd.Timedelta(minutes=1)
R_CLIP = (-5.0, 10.0)                                   # bounds of the R-unit trade-state columns of exit_rows
MIN_INFER_PRICES = 1000                                 # infer_tick warns below this many prices
# breakout pattern -> (its setup column in P, bars from the setup bar back to the pattern's first bar). In
# signals.patterns a breakout is the first close beyond the setup's levels within BREAKOUT_LOOK bars after the setup
# bar; the levels of inside_bar_breakout are the MOTHER bar's (the bar before the inside bar), of nr7_breakout the
# NR7 bar's own.
BREAKOUT_SETUP = {"inside_bar_breakout": ("inside_bar", 1), "nr7_breakout": ("nr7", 0)}
BREAKOUT_LOOK = 3


# --------------------------------------------------------------------------------------------- helpers
def _rkey(R):
    """column suffix for a target multiple: 1.0 -> '1', 1.5 -> '1.5', 2.0 -> '2'."""
    return f"{float(R):g}"


def infer_tf(b):
    """Bar length in minutes = the smallest positive start-time step between consecutive bars of one segment."""
    m = b.index.as_unit("s").asi8 // 60
    seg = b.seg.to_numpy()
    dm = np.diff(m)[(seg[1:] == seg[:-1])]
    dm = dm[dm > 0]
    if not len(dm):
        raise ValueError("cannot infer tf from b; pass tf=")
    return int(dm.min())


def infer_tick(b):
    """Largest common price grid of b's highs and lows (YM 1.0, ES/NQ 0.25 on a full history).
    Unreliable on a short frame (a few ES bars may all sit on a 0.5 or 1.0 grid): warns when fewer than
    MIN_INFER_PRICES prices are available. Prefer the market's tick (sg.SPEC[sym]['tick'], see resolve_tick)."""
    px = np.r_[b.H.to_numpy(np.float64), b.L.to_numpy(np.float64)]
    px = px[np.isfinite(px)]
    tick = 0.01
    for tk in (1.0, 0.5, 0.25, 0.1, 0.05, 0.01):
        q = px / tk
        if np.all(np.abs(q - np.round(q)) < 1e-6):
            tick = tk
            break
    if len(px) < MIN_INFER_PRICES:
        warnings.warn(f"tick inferred as {tick} from only {len(px)} prices (may be too coarse); "
                      "pass sym= or tick=", stacklevel=3)
    return tick


def resolve_tick(b, tick=None, sym=None):
    """tick if given, else the market's tick sg.SPEC[sym]['tick'] if sym is given, else infer_tick(b)."""
    if tick is not None:
        return float(tick)
    if sym is not None:
        return float(sg.SPEC[sym]["tick"])
    return infer_tick(b)


def eligible(b, tf):
    """ok[t]: an event on bar t can be entered at the open of bar t+1 (same segment, entry bar not after the 16:45
    forced-exit bar F); forced[t]: index of F for t's segment (exits.session_frame)."""
    allowed, forced = ex.session_frame(b, tf)
    seg = b.seg.to_numpy()
    n = len(b)
    ok = np.zeros(n, bool)
    if n > 1:
        ok[:-1] = (seg[1:] == seg[:-1]) & (np.arange(1, n) <= forced[:-1])
    ok &= allowed
    return ok, forced


def _seg_start(b):
    seg = b.seg.to_numpy()
    n = len(seg)
    start = np.r_[True, seg[1:] != seg[:-1]] if n else np.zeros(0, bool)
    return np.maximum.accumulate(np.where(start, np.arange(n), 0))


def _extreme(L, H, i, span, d, s0):
    """lowest L (long) / highest H (short) of bars max(i-span+1, segment start) .. i, vectorized over events."""
    lo = L[i].copy(); hi = H[i].copy()
    for s in range(1, int(span.max()) + 1 if len(span) else 1):
        use = span > s
        j = np.maximum(i - s, s0)
        lo = np.where(use, np.minimum(lo, L[j]), lo)
        hi = np.where(use, np.maximum(hi, H[j]), hi)
    return np.where(d > 0, lo, hi)


def breakout_spans(b, P):
    """Actual bar extent of every breakout fire: {pattern: int array on b} for the BREAKOUT_SETUP patterns in P.

    exits.SPAN gives the breakouts a fixed 3 bars, but the breakout bar j can come up to BREAKOUT_LOOK bars after the
    setup bar i, so the textbook stop level (beyond the mother bar i-1 / the NR7 bar i) can lie outside that window.
    Here the setup bar of each fire is recovered exactly as signals.patterns' breakout() assigns it: the LARGEST
    setup bar i in j-1 .. j-BREAKOUT_LOOK (same segment) for which j is the first bar after i that closes beyond i's
    levels (above the high is checked first, as there). span[j] = j - (first bar of the pattern) + 1, i.e. 3..5 for
    inside_bar_breakout (mother bar .. j) and 2..4 for nr7_breakout (NR7 bar .. j); 1 where the pattern does not
    fire. If P lacks the setup column or no setup matches the fired direction (P not made by signals.patterns from
    this b), the largest possible extent is used (BREAKOUT_LOOK + back + 1 = 5 / 4). These are the exact extents;
    entry_events uses max(extent, exits.SPAN).
    Only bars <= j are used (the stop is known at j's close): no look-ahead."""
    n = len(b)
    H, L, C = (b[c].to_numpy(np.float64) for c in "HLC")
    seg = b.seg.to_numpy()
    j = np.arange(n)
    out = {}
    for name, (setup, back) in BREAKOUT_SETUP.items():
        if name not in P.columns:
            continue
        fire = P[name].to_numpy().astype(np.int64)
        span = np.where(fire != 0, BREAKOUT_LOOK + back + 1, 1).astype(np.int64)
        if setup in P.columns and n:
            mark = P[setup].to_numpy() != 0
            hi = np.r_[np.full(back, np.nan), H[:n - back]]                 # levels stored on the setup bar
            lo = np.r_[np.full(back, np.nan), L[:n - back]]
            found = np.zeros(n, bool)
            for s in range(1, BREAKOUT_LOOK + 1):                            # s = 1 is the largest (winning) setup
                i = np.maximum(j - s, 0)
                cand = (j - s >= 0) & mark[i] & (seg[i] == seg) & ~found
                for m in range(1, s):                                        # no earlier close beyond i's levels
                    cm = C[np.minimum(i + m, n - 1)]
                    cand &= ~((cm > hi[i]) | (cm < lo[i]))
                dirn = np.where(C > hi[i], 1, np.where(C < lo[i], -1, 0))
                hit = cand & (dirn != 0)
                span = np.where(hit & (dirn == fire) & (fire != 0), s + back + 1, span)
                found |= hit
        out[name] = span
    return out


# --------------------------------------------------------------------------------------------- events
def entry_events(b, P, tf=None, tick=None, sym=None):
    """Textbook-direction pattern events.

    b: signals.bars(sym, tf) frame; P: signals.patterns(b, ctx) on b.index (the directional columns, plus the
    inside_bar / nr7 setup columns for the breakout spans).
    One row per (bar t, direction d) where >= 1 directional pattern has value d on t and the trade can be entered at
    the open of t+1 (see `eligible`). If both directions fire on the same bar, both rows are created.
    stop = min L (long) / max H (short) over the largest span of the patterns that fired, minus / plus 1 tick
    (clamped to t's segment). Spans: exits.SPAN (patterns not listed span 1 bar); for inside_bar_breakout and
    nr7_breakout max(exits.SPAN, actual extent from the mother / NR7 bar to t) (breakout_spans), so the stop always
    lies beyond the setup bar and is never tighter than the SPEC's exits.SPAN rule.
    tick: tick= if given, else sg.SPEC[sym]['tick'] if sym= is given, else inferred from b (warns on short frames;
    pass sym= or tick= in production). tf is inferred from b when not given.
    Returns DataFrame [t, i, d, patterns, n_patterns, stop] sorted by (i, d)."""
    tf = infer_tf(b) if tf is None else tf
    tick = resolve_tick(b, tick, sym)
    names = [c for c in DIRECTIONAL if c in P.columns]
    A = P[names].to_numpy(np.int8)
    span = np.array([ex.SPAN.get(c, 1) for c in names], np.int64)
    bspan = {names.index(k): v for k, v in breakout_spans(b, P).items() if k in names}
    ok, _ = eligible(b, tf)
    L, H = b.L.to_numpy(np.float64), b.H.to_numpy(np.float64)
    s0 = _seg_start(b)
    names_arr = np.array(names, dtype=object)
    bits = (np.int64(1) << np.arange(len(names), dtype=np.int64))
    parts = []
    for d in (1, -1):
        M = (A == d) & ok[:, None]
        i = np.flatnonzero(M.any(axis=1))
        Mi = M[i]
        code = Mi.astype(np.int64) @ bits
        uniq, inv = np.unique(code, return_inverse=True)
        lists = [names_arr[(u & bits) != 0].tolist() for u in uniq]       # one list per distinct combination
        pats = [list(lists[k]) for k in inv]                                 # fresh list per row
        S = np.repeat(span[None, :], len(i), axis=0)                         # span per (event, pattern)
        for c, v in bspan.items():
            S[:, c] = np.maximum(v[i], span[c])                              # never tighter than exits.SPAN
        mspan = (Mi * S).max(axis=1)
        dd = np.full(len(i), d, np.int8)
        stop = _extreme(L, H, i, mspan, dd, s0[i]) - d * tick
        parts.append(pd.DataFrame({"t": b.index[i], "i": i, "d": dd, "patterns": pats,
                                   "n_patterns": Mi.sum(axis=1).astype(np.int16), "stop": stop}))
    ev = pd.concat(parts, ignore_index=True).sort_values(["i", "d"], kind="stable").reset_index(drop=True)
    return ev


def random_events(b, frac, seed, tf=None, tick=None, sym=None):
    """Random-entry baseline events: a random `frac` of the eligible bars (sampled without replacement), each with a
    random direction; stop = the signal bar's own L - 1 tick (long) / H + 1 tick (short).
    tick / sym / tf as in entry_events. Same columns as entry_events (patterns = [], n_patterns = 0)."""
    tf = infer_tf(b) if tf is None else tf
    tick = resolve_tick(b, tick, sym)
    ok, _ = eligible(b, tf)
    cand = np.flatnonzero(ok)
    rng = np.random.default_rng(seed)
    n = int(round(frac * len(cand)))
    i = np.sort(rng.choice(cand, size=n, replace=False))
    d = rng.choice(np.array([-1, 1], np.int8), size=n)
    stop = np.where(d > 0, b.L.to_numpy(np.float64)[i] - tick, b.H.to_numpy(np.float64)[i] + tick)
    return pd.DataFrame({"t": b.index[i], "i": i, "d": d, "patterns": [[] for _ in range(n)],
                         "n_patterns": np.zeros(n, np.int16), "stop": stop})


# --------------------------------------------------------------------------------------------- 1-minute path
def load_1m(sym):
    """research_lib.bars_1m(sym) as a tz-naive (New York wall time) frame with O, H, L, C, inst, sess, in true
    chronological order (the same rows signals.bars aggregates)."""
    m = rl.bars_1m(sym)
    return pd.DataFrame({"O": m.Open.to_numpy(np.float64), "H": m.High.to_numpy(np.float64),
                         "L": m.Low.to_numpy(np.float64), "C": m.Close.to_numpy(np.float64),
                         "inst": m.instrument_id.to_numpy(), "sess": m.sess.to_numpy()},
                        index=m.index.tz_localize(None))


def map_1m(m1, b, tf):
    """first[j], last[j]: first / last row of m1 (chronological positions) that belong to tf bar j of b, where a tf
    bar is the group (contract, floor(start, tf)) exactly as in signals.bars; -1 if bar j has no 1-minute rows."""
    mins1 = m1.index.as_unit("s").asi8 // 60
    bmin = b.index.as_unit("s").asi8 // 60
    codes, uniq = pd.factorize(np.r_[m1.inst.to_numpy(), b.inst.to_numpy()])
    if len(uniq) >= 4096:
        raise ValueError("too many contracts for the key encoding")
    c1, cb = codes[:len(m1)], codes[len(m1):]
    k1 = (mins1 - mins1 % tf) * 4096 + c1
    kb = bmin * 4096 + cb
    order = np.argsort(kb, kind="stable")
    ks = kb[order]
    pos = np.searchsorted(ks, k1)
    pos = np.minimum(pos, len(ks) - 1)
    hit = ks[pos] == k1
    bar = np.where(hit, order[pos], -1)
    rows = np.arange(len(m1))
    first = np.full(len(b), np.iinfo(np.int64).max, np.int64)
    last = np.full(len(b), -1, np.int64)
    np.minimum.at(first, bar[hit], rows[hit])
    np.maximum.at(last, bar[hit], rows[hit])
    first[last < 0] = -1
    return first, last


def walk_1m(O1, H1, L1, C1, r0, r1, d, stop, target, tick):
    """Walk trades minute by minute (vectorized over active trades, loop over the minute OFFSET).

    r0 / r1: first / last 1-minute row of each trade's path (inclusive); d: +1 / -1; stop: price (NaN = none);
    target: (n, nR) target prices (NaN = none). Each minute: stop first (long: L1 <= stop -> fill min(O1, stop) - 1
    tick; short mirror), then each still-open target (long: H1 >= target + 1 tick -> fill at target; short mirror).
    A stop ends every still-open target column of that trade. Not exited by r1 -> time exit at C1[r1].
    Returns kind (n, nR) int8 (0 time / 1 stop / 2 target), exit price (n, nR), exit row (n, nR)."""
    n, nR = target.shape
    kind = np.zeros((n, nR), np.int8)
    xrow = np.repeat(r1[:, None], nR, axis=1).astype(np.int64)
    xpx = np.repeat(C1[r1][:, None], nR, axis=1) if n else np.zeros((0, nR))
    open_ = np.ones((n, nR), bool)
    act = np.arange(n)
    L_ = int((r1 - r0).max()) + 1 if n else 0
    for k in range(L_):
        r = r0[act] + k
        live = r <= r1[act]
        act, r = act[live], r[live]
        if not len(act):
            break
        dd = d[act]; s = stop[act]
        o, h, l = O1[r], H1[r], L1[r]
        sh = np.where(dd > 0, l <= s, h >= s)                               # NaN stop -> False
        spx = np.where(dd > 0, np.minimum(o, s) - tick, np.maximum(o, s) + tick)
        g = target[act]
        th = np.where((dd > 0)[:, None], h[:, None] >= g + tick, l[:, None] <= g - tick)
        op = open_[act]
        hs = op & sh[:, None]
        ht = op & ~hs & th
        if hs.any():
            a, c = np.nonzero(hs)
            kind[act[a], c] = 1; xpx[act[a], c] = spx[a]; xrow[act[a], c] = r[a]
        if ht.any():
            a, c = np.nonzero(ht)
            kind[act[a], c] = 2; xpx[act[a], c] = g[a, c]; xrow[act[a], c] = r[a]
        op = op & ~hs & ~ht
        open_[act] = op
        act = act[op.any(axis=1)]
    return kind, xpx, xrow


def _prepare(sym, tf, b, events, max_bars, m1):
    """Common trade set-up: drops events that cannot be entered; returns dict of arrays and the 1-minute arrays."""
    spec = sg.SPEC[sym]
    ok, forced = eligible(b, tf)
    i = events.i.to_numpy(np.int64) if "i" in events else b.index.get_indexer(events.t)
    keep = (i >= 0) & ok[np.maximum(i, 0)]
    m1 = load_1m(sym) if m1 is None else m1
    first, last = map_1m(m1, b, tf)
    i_k = i[keep]
    e = i_k + 1
    T = np.minimum(i_k + max_bars, forced[i_k])                          # time-limit bar (held through its close)
    keep2 = (first[e] >= 0) & (last[T] >= 0)
    sel = np.flatnonzero(keep)[keep2]
    i_k, e, T = i_k[keep2], e[keep2], T[keep2]
    d = events.d.to_numpy(np.int64)[sel]
    stop = events.stop.to_numpy(np.float64)[sel]
    entry = b.O.to_numpy(np.float64)[e]
    risk = d * (entry - stop)                                             # > 0 normally; 0 at, < 0 past the stop
    return dict(spec=spec, sel=sel, i=i_k, e=e, T=T, d=d, stop=stop, entry=entry, risk=risk, forced=forced,
                r0=first[e], r1=last[T], m1=m1, first=first,
                O1=m1.O.to_numpy(np.float64), H1=m1.H.to_numpy(np.float64), L1=m1.L.to_numpy(np.float64),
                C1=m1.C.to_numpy(np.float64), ts1=m1.index)


def _t_end(z, kind, xrow, T, b, tf, past):
    """exit timestamp: end of the exit minute (stop/target), close of the time-limit bar (time), entry open (past
    stop)."""
    t_min = z["ts1"][xrow] + _MIN
    t_bar = b.index[T] + pd.Timedelta(minutes=tf)
    out = np.where(kind == 0, t_bar.to_numpy(), t_min.to_numpy())
    out = np.where(past, b.index[z["e"]].to_numpy(), out)
    return pd.DatetimeIndex(out)


# --------------------------------------------------------------------------------------------- entry labels
def label_entries(sym, tf, b, events, target_R=(1.0, 1.5, 2.0), max_bars=16, m1=None):
    """Triple-barrier labels for entry events, walked on 1-minute bars.

    entry = O[t+1]; risk = |entry - stop|; target_R = entry + d * R * risk; time limit = close of bar t+max_bars or
    the 16:45 forced-exit bar F of the segment, whichever is first (time exit at that bar's close).
    If the entry is already PAST the stop (d*(entry-stop) < 0) the trade exits at the entry open: pnl = -cost,
    exit_kind 'stop', past_stop True, t_end = entry time (SPEC). An entry exactly AT the stop (risk 0) is walked
    like any other trade: its first minute (open = stop) touches the stop, so it is stopped there at stop -/+ 1 tick,
    pnl = -cost - 1 tick $, exit_kind 'stop', past_stop False, t_end = end of the entry minute. So risk_pts /
    risk_usd can be 0 (and are |entry - stop| > 0 for past-stop rows): guard any division by risk downstream.
    m1: optional preloaded load_1m(sym) frame (reuse it across calls).
    Returns the (enterable) events with added columns: market (= sym), t_entry, entry, risk_pts, risk_usd,
    past_stop, and for every R (suffix '1', '1.5', '2'): target_<R>, exit_px_<R>, pnl_usd_<R> (net $ per micro),
    y_<R> (pnl > 0), exit_kind_<R> ('stop' / 'target' / 'time'), t_end_<R> (exit time, for purging).
    Primary label: y_1.5."""
    z = _prepare(sym, tf, b, events, max_bars, m1)
    spec, d, entry, risk, stop = z["spec"], z["d"], z["entry"], z["risk"], z["stop"]
    tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
    R = np.asarray(target_R, np.float64)
    past = risk < 0                                                       # risk == 0 is walked (stopped at once)
    target = entry[:, None] + d[:, None] * R[None, :] * risk[:, None]
    target[past] = np.nan
    stop_w = np.where(past, np.nan, stop)
    r1 = np.where(past, z["r0"], z["r1"])                                # past-stop trades are not walked
    kind, xpx, xrow = walk_1m(z["O1"], z["H1"], z["L1"], z["C1"], z["r0"], r1, d, stop_w, target, tick)
    pnl = d[:, None] * (xpx - entry[:, None]) * usd - cost
    pnl[past] = -cost
    kind[past] = 1
    xpx[past] = entry[past, None]
    out = events.iloc[z["sel"]].copy()
    out["market"] = sym
    out["t_entry"] = b.index[z["e"]]
    out["entry"] = entry
    out["risk_pts"] = np.abs(entry - stop)
    out["risk_usd"] = np.abs(entry - stop) * usd
    out["past_stop"] = past
    for c, r in enumerate(R):
        s = _rkey(r)
        out[f"target_{s}"] = target[:, c]
        out[f"exit_px_{s}"] = xpx[:, c]
        out[f"pnl_usd_{s}"] = pnl[:, c]
        out[f"y_{s}"] = pnl[:, c] > 0
        out[f"exit_kind_{s}"] = KIND[kind[:, c]]
        out[f"t_end_{s}"] = _t_end(z, kind[:, c], xrow[:, c], z["T"], b, tf, past)
    return out


# --------------------------------------------------------------------------------------------- exit rows
def trade_keys(sym, src, t, d):
    """Trade ids "<sym>:<src>:<t as YYYY-mm-ddTHH:MM>:<L|S>" (one per trade, vectorized). An id is a function of the
    event alone, so it is unique across markets and across calls; repeats of an identical (src, t, d) within one call
    get "#1", "#2", ... appended. Returns an object array of str."""
    key = pd.Series(pd.DatetimeIndex(t).strftime("%Y-%m-%dT%H:%M"), dtype=object)
    key = (f"{sym}:" + pd.Series(np.asarray(src, dtype=object), dtype=object) + ":" + key + ":"
           + pd.Series(np.where(np.asarray(d) > 0, "L", "S"), dtype=object))
    rep = key.groupby(key, sort=False).cumcount()
    key = key.where(rep == 0, key + "#" + rep.astype(str))
    return key.to_numpy(dtype=object)


def exit_rows(sym, tf, b, F, events, max_bars=32, frac=0.25, seed=0, m1=None, rand=None):
    """Exit-decision rows for open trades.

    Trades: a random `frac` of `events` (src 'signal') PLUS random_events(b, frac, seed+1) (src 'random'; or pass your
    own `rand` events frame). Each is managed with the BASELINE: stop at its stop reference (1-minute walk, extra
    stop tick), no target, time exit at the close of bar t+max_bars or of the 16:45 forced bar F, whichever first.
    Trades entered at / past their stop (risk <= 0) are skipped: they never stay open past their first minute, and
    their R units would divide by 0.
    One row for every tf bar k (k >= entry bar) at whose close the baseline trade is still open and k < time-limit
    bar (so exiting at O[k+1] is a real alternative): trade, market (= sym), src, t (signal time), k (position in
    b), ts (bar k start), d, all F columns at row k (F must be aligned to b), trade state known at k's close:
      open_R = (C_k - entry) * d / risk; mfe_R / mae_R = best favourable / worst adverse excursion of bars e..k in R
      (both >= 0); bars_held = k - e + 1; dist_stop_R = (C_k - stop) * d / risk; mins_to_1645 = minutes from k's
      close to the close of the forced-exit bar; risk_pts, risk_usd (unclipped: the model can see a tiny risk);
      open_R, mfe_R, mae_R and dist_stop_R are clipped to R_CLIP (a 1-tick risk gives values in the hundreds);
    and the label: exit_gain_usd = net $ of exiting at O[k+1] minus net $ of holding to the baseline end (same
    round-trip cost both ways, so only the price difference and the stop's extra tick remain), y_exit = gain > 0,
    t_end = baseline exit time. hold_pnl_usd and end_kind ('stop' / 'time') describe the baseline.
    trade = "<sym>:<src>:<signal bar start YYYY-mm-ddTHH:MM>:<L|S>", unique across markets and calls (the same
    event always gets the same id; repeats of an identical event within one call get a "#n" suffix), so the rows
    of several markets can be pooled and grouped by `trade` (walkforward.exit_weights / exit policies)."""
    if len(F) != len(b) or not F.index.equals(b.index):
        raise ValueError("F must be on b.index (one row per tf bar, same order)")
    spec = sg.SPEC[sym]
    tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
    rng = np.random.default_rng(seed)
    n_s = int(round(frac * len(events)))
    sig = events.iloc[np.sort(rng.choice(len(events), size=n_s, replace=False))]
    if rand is None:
        rand = random_events(b, frac, seed + 1, tf=tf, tick=tick)
    ev = pd.concat([sig[["t", "i", "d", "stop"]].assign(src="signal"),
                    rand[["t", "i", "d", "stop"]].assign(src="random")], ignore_index=True)
    z = _prepare(sym, tf, b, ev, max_bars, m1)
    live = z["risk"] > 0
    for key in ("sel", "i", "e", "T", "d", "stop", "entry", "risk", "r0", "r1"):
        z[key] = z[key][live]
    d, entry, risk, stop, e, T = z["d"], z["entry"], z["risk"], z["stop"], z["e"], z["T"]
    n = len(d)
    kind, xpx, xrow = walk_1m(z["O1"], z["H1"], z["L1"], z["C1"], z["r0"], z["r1"], d, stop,
                              np.full((n, 1), np.nan), tick)
    kind, xpx, xrow = kind[:, 0], xpx[:, 0], xrow[:, 0]
    # tf bar of the stop minute = the largest bar j in e..T whose first 1-minute row <= the stop row
    # (loop over the bar OFFSET; at most max_bars steps)
    stopped = kind == 1
    fr = z["first"]
    sbar = T.copy()
    for s in range(int((T - e).max()) + 1 if n else 0):
        j = np.minimum(e + s, T)
        inside = stopped & (j <= T) & (fr[j] <= xrow) & (fr[j] >= 0)
        sbar = np.where(inside, j, sbar)
    k_last = np.where(stopped, sbar - 1, T - 1)                         # last bar at whose close we are still open
    nk = np.maximum(k_last - e + 1, 0)
    tid = np.repeat(np.arange(n), nk)
    off = np.arange(nk.sum()) - np.repeat(np.cumsum(nk) - nk, nk)
    k = e[tid] + off
    O, H, L, C = (b[c].to_numpy(np.float64) for c in "OHLC")
    dr, en, rk = d[tid], entry[tid], risk[tid]
    fav = np.where(dr > 0, H[k], -L[k])
    adv = np.where(dr > 0, -L[k], H[k])
    g = pd.Series(tid)
    mfe = pd.Series(fav).groupby(g).cummax().to_numpy() - dr * en
    mae = pd.Series(adv).groupby(g).cummax().to_numpy() + dr * en
    hold = d * (xpx - entry) * usd - cost
    now = dr * (O[k + 1] - en) * usd - cost
    t_end = _t_end(z, kind, xrow, T, b, tf, np.zeros(n, bool))
    src = ev.src.to_numpy()[z["sel"]]
    tkey = trade_keys(sym, src, b.index[z["i"]], d)
    Fn = F.to_numpy(np.float32)[k]
    out = pd.DataFrame({"trade": tkey[tid], "market": sym, "src": src[tid], "t": b.index[z["i"]][tid],
                        "k": k, "ts": b.index[k], "d": dr.astype(np.int8)})
    out = pd.concat([out, pd.DataFrame(Fn, columns=F.columns)], axis=1)
    fz = z["forced"][z["i"]][tid]
    lo_R, hi_R = R_CLIP
    out["open_R"] = np.clip((C[k] - en) * dr / rk, lo_R, hi_R)
    out["mfe_R"] = np.clip(mfe / rk, lo_R, hi_R)
    out["mae_R"] = np.clip(mae / rk, lo_R, hi_R)
    out["bars_held"] = (k - e[tid] + 1).astype(np.int16)
    out["dist_stop_R"] = np.clip((C[k] - stop[tid]) * dr / rk, lo_R, hi_R)
    out["mins_to_1645"] = ((b.index[fz] - b.index[k]).to_numpy() / _MIN).astype(np.float32)
    out["risk_pts"] = rk
    out["risk_usd"] = rk * usd
    out["exit_gain_usd"] = now - hold[tid]
    out["y_exit"] = out.exit_gain_usd.to_numpy() > 0
    out["hold_pnl_usd"] = hold[tid]
    out["end_kind"] = KIND[kind[tid]]
    out["t_end"] = t_end[tid]
    return out
