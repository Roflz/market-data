"""
H1/H2 pullback entries (Al Brooks bar counting) with STOP-ORDER entries, labelled on the 1-minute path.

Long (shorts are the mirror: lows/highs swapped, L1/L2):
  trend     at the signal bar's close: EMA8 > EMA20 > EMA50 and the last two CONFIRMED 5-bar swing highs are rising and
            the last two confirmed 5-bar swing lows are rising (higher highs and higher lows).
  pullback  after a trend high (a bar making the highest high since the last reset), the first bar with a LOWER high
            starts the pullback. Reset when a bar makes a new high above the trend high. Cancelled (until the next new
            trend high) if a bar's low breaks the last confirmed swing low (the higher low gave way).
  attempts  inside the pullback, a bar whose high goes above the prior bar's high, right after a lower-high bar, is
            an attempt to resume the trend: the 1st is H1, the 2nd H2, ...
  order     at the close of every lower-high bar s inside a valid pullback: buy stop at H[s] + 1 tick for bar s+1
            (the attempt number it would be = attempts so far + 1). Cancelled if bar s+1 does not trade there.
  stop      1 tick below the pullback low (lowest low since the trend high, through bar s) = `stop`;
            alternative 1 tick below the signal bar's low = `stop_sig`.
Everything about the setup is known at bar s's close (swings are confirmed k bars after the pivot).

Labelling (label_stop_entries): the order fills on the FIRST 1-minute bar of bar s+1 whose high reaches the trigger,
at max(that minute's open, trigger) + 1 tick of stop slippage (a gap through the trigger fills at the open + 1 tick;
mirror for shorts), the same extra tick stop-loss exits pay. The trade is then walked with
labels.walk_1m from that minute (stop first in every minute, including the fill minute = conservative), targets at
1 / 1.5 / 2 x risk, time limit = close of bar s+max_bars or the 16:45 forced bar, costs as in labels.py.
"""
import numpy as np
import pandas as pd

import exits as ex
import labels as lb
import signals as sg


def confirmed_swings(b, k=5):
    """last and previous confirmed swing high / low values at each bar (NaN until known), per contract run."""
    lo, hi = sg.pivots(b, k)
    L, H = b.L.to_numpy(), b.H.to_numpy(); n = len(b); run = b.run.to_numpy()
    out = {}
    for name, piv, P in (("lo", lo, L), ("hi", hi, H)):
        last = np.full(n, np.nan); prev = np.full(n, np.nan)
        cur = np.nan; before = np.nan; r_prev = None
        conf = np.full(n, np.nan); q = np.flatnonzero(piv); conf[q + k] = P[q]
        for t in range(n):
            if run[t] != r_prev:
                cur = before = np.nan; r_prev = run[t]
            if not np.isnan(conf[t]):
                before, cur = cur, conf[t]
            last[t], prev[t] = cur, before
        out[name], out[name + "_prev"] = last, prev
    return out


def detect(b, ctx, tick, tf, k=5, max_attempt=4):
    """All pending H/L orders (one row per signal bar s and direction). Columns: i (= s), t, d, attempt, trigger,
    stop, stop_sig, trend_ext, pb_extreme, depth (pullback size / leg from the last confirmed swing), bars_pb.
    Works in a MIRRORED space for shorts (X = -low, Y = -high), so one loop handles both directions."""
    H, L = b.H.to_numpy(), b.L.to_numpy()
    seg = b.seg.to_numpy(); run = b.run.to_numpy(); n = len(b)
    allowed, forced = ex.session_frame(b, tf)
    e8, e20, e50 = (ctx[f"ema{x}"].to_numpy() for x in (8, 20, 50))
    sw = confirmed_swings(b, k)
    rows = []
    for d in (1, -1):
        X, Y = (H, L) if d > 0 else (-L, -H)               # X: trend side extreme, Y: pullback side extreme
        if d > 0:
            trend = (e8 > e20) & (e20 > e50) & (sw["hi"] > sw["hi_prev"]) & (sw["lo"] > sw["lo_prev"])
            guard = sw["lo"]                                # last confirmed higher low (price)
        else:
            trend = (e8 < e20) & (e20 < e50) & (sw["lo"] < sw["lo_prev"]) & (sw["hi"] < sw["hi_prev"])
            guard = -sw["hi"]                               # mirrored last lower high
        ref = -np.inf; in_pb = broken = False; count = 0; pbx = np.inf; bars = 0
        for t in range(n):
            if t == 0 or run[t] != run[t - 1]:              # new contract: start over
                ref = X[t]; in_pb = broken = False; count = 0; pbx = np.inf; bars = 0
                continue
            if X[t] > ref:                                  # new trend extreme: pullback over
                ref = X[t]; in_pb = broken = False; count = 0; pbx = np.inf; bars = 0
                continue
            if broken:
                continue
            if not in_pb:
                if X[t] < X[t - 1]:                         # first lower high after the trend extreme
                    in_pb = True; count = 0; pbx = Y[t]; bars = 0
                else:
                    continue
            pbx = min(pbx, Y[t]); bars += 1
            g = guard[t]
            if not np.isnan(g) and Y[t] < g:                # the higher low gave way: no entries until a new extreme
                in_pb = False; broken = True
                continue
            if t >= 2 and X[t] > X[t - 1] and X[t - 1] <= X[t - 2]:
                count += 1                                  # an attempt (H1, H2, ...) happened on this bar
            ok = (X[t] <= X[t - 1] and trend[t] and count < max_attempt and t + 1 < n and seg[t + 1] == seg[t]
                  and allowed[t + 1] and forced[t + 1] >= t + 1)
            if ok:
                leg = ref - g if not np.isnan(g) else np.nan
                rows.append((t, d, count + 1, d * (X[t] + tick), d * (pbx - tick), d * (Y[t] - tick), d * ref,
                             d * pbx, (ref - pbx) / leg if leg > 0 else np.nan, bars))
    ev = pd.DataFrame(rows, columns=["i", "d", "attempt", "trigger", "stop", "stop_sig", "trend_ext", "pb_extreme",
                                     "depth", "bars_pb"])
    ev["i"] = ev["i"].astype(np.int64)
    ev.insert(1, "t", b.index[ev.i.to_numpy()])
    return ev.sort_values(["i", "d"]).reset_index(drop=True)


def label_stop_entries(sym, tf, b, ev, target_R=(1.0, 1.5, 2.0), max_bars=16, m1=None, stop_col="stop"):
    """Fill the stop orders on bar i+1's 1-minute path and walk the triggered trades (see module docstring)."""
    spec = sg.SPEC[sym]; tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
    m1 = lb.load_1m(sym) if m1 is None else m1
    first, last = lb.map_1m(m1, b, tf)
    _, forced = ex.session_frame(b, tf)
    O1, H1, L1, C1 = (m1[x].to_numpy(np.float64) for x in "OHLC")
    i = ev.i.to_numpy(); e = i + 1; d = ev.d.to_numpy(); trig = ev.trigger.to_numpy(np.float64)
    ok = (first[e] >= 0)
    # first minute of bar e reaching the trigger (loop over minute offsets within the bar, max tf minutes)
    fill_row = np.full(len(ev), -1, np.int64)
    for off in range(tf):
        r = first[e] + off
        live = ok & (fill_row < 0) & (r <= last[e])
        rr = np.where(live, r, 0)
        hit = live & np.where(d > 0, H1[rr] >= trig, L1[rr] <= trig)
        fill_row[hit] = r[hit]
    trig_ok = fill_row >= 0
    sel = np.flatnonzero(trig_ok)
    fr = fill_row[sel]; dd = d[sel]
    # a stop-order entry is a stop fill: it slips 1 tick like stop-loss exits do (labels.walk_1m), gap or not
    entry = np.where(dd > 0, np.maximum(O1[fr], trig[sel]) + tick, np.minimum(O1[fr], trig[sel]) - tick)
    stop = ev[stop_col].to_numpy(np.float64)[sel]
    T = np.minimum(i[sel] + max_bars, forced[i[sel]])
    r1 = last[T]
    good = r1 >= fr
    sel, fr, dd, entry, stop, T, r1 = sel[good], fr[good], dd[good], entry[good], stop[good], T[good], r1[good]
    risk = dd * (entry - stop)
    R = np.asarray(target_R, float)
    target = entry[:, None] + dd[:, None] * R[None, :] * np.maximum(risk, 0)[:, None]
    past = risk <= 0
    target[past] = np.nan
    kind, xpx, xrow = lb.walk_1m(O1, H1, L1, C1, fr, np.where(past, fr, r1), dd, np.where(past, np.nan, stop),
                                 target, tick)
    pnl = dd[:, None] * (xpx - entry[:, None]) * usd - cost
    pnl[past] = -cost; kind[past] = 1
    out = ev.iloc[sel].copy()
    out["market"] = sym
    out["t_entry"] = m1.index[fr]
    out["entry"] = entry; out["stop_used"] = stop
    out["risk_pts"] = np.abs(entry - stop); out["risk_usd"] = np.abs(entry - stop) * usd
    out["past_stop"] = past
    ts1 = m1.index
    for c, r in enumerate(R):
        s = lb._rkey(r)
        out[f"pnl_usd_{s}"] = pnl[:, c]
        out[f"y_{s}"] = pnl[:, c] > 0
        out[f"exit_kind_{s}"] = lb.KIND[kind[:, c]]
        t_min = ts1[xrow[:, c]] + pd.Timedelta(minutes=1)
        t_bar = b.index[T] + pd.Timedelta(minutes=tf)
        out[f"t_end_{s}"] = pd.DatetimeIndex(np.where(kind[:, c] == 0, t_bar.to_numpy(), t_min.to_numpy()))
    out.attrs["n_orders"] = len(ev); out.attrs["n_triggered"] = int(trig_ok.sum())
    return out
