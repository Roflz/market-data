"""
Exit engine: every trade has an initial stop, is managed bar by bar on 5-minute bars across the whole Globex
session (6:00 PM -> 5:00 PM ET, overnight included), and is flattened at the 5:00 PM ET close because the market
shuts 5-6 PM (and Friday 5 PM -> Sunday 6 PM). Exits decide from data when to get out instead of a fixed target.

Fills (1 micro contract, MES $5/pt or MNQ $2/pt, $1.00 commission per round trip):
  entry   : next bar's open + 1 tick
  stops   : the stop price - 1 tick, or the bar's open if it gapped through the stop (worse)
  targets : limit at the target, filled only if price trades 1 tick through it
  market exits (trend break, order-flow, close) : bar close - 1 tick
  If a bar hits both stop and target, the stop counts (conservative).
Trailing levels only use bars that have already closed (no look-ahead).

Exit rules (all keep the initial stop):
  target_m      fixed target at m x initial risk (R)
  hold          ride to the 5 PM ET close unless stopped
  trail_k       chandelier: stop = best high since entry - k x ATR(5-min); only ratchets toward profit
  be_trail_k    stop to breakeven once +1R, then trail_k
  scale         half off at +1.5R; stop to breakeven; other half trails at 3 x ATR to stop or close
  ema5 / ema60  once price has closed on the right side, exit on a close back through 5-min EMA20 / 60-min EMA20
  chan12        stop trails at the lowest low (longs) of the last 12 closed 5-min bars (1 hour)
  flow          exit when estimated delta over the last 3 bars is against the trade AND price made no new best for 3 bars
  clock_T       exit at the close of the first bar that closes at/after clock minute T (e.g. clock_630 = 10:30 ET)
  after_N       exit at the close once the trade is N minutes old
  tstop_N_x     time stop: when the trade is N minutes old, exit if open profit < x R, otherwise keep holding
  lock_m_j      profit lock: once the best open profit reaches m R, stop -> breakeven and (if j > 0) trail j x ATR

Optional per-trade stop settings (simulate keywords, or run(..., extra={signal bar: {...}})); all off by default:
  R_pts     initial risk in points instead of k0 x ATR(5-min) at the signal bar
  stop_px   initial stop at this price (e.g. just inside a broken level); R = distance from the entry fill to it
  min_R     no trade if R is smaller than this; with stop_px, judged at the signal close (close + 1 tick - stop),
            and if the next open then gaps through the stop the trade is stopped out at that open
  level     also exit at the close of the first bar that closes back through this price (failed breakout)
simulate() returns R (points) as its last element; run() reports it in the R_pts column.
"""
import numpy as np
import pandas as pd

TICK = SLIP = 0.25
SPEC = {"ES": dict(usd=5.0, comm=1.0, micro="MES"), "NQ": dict(usd=2.0, comm=1.0, micro="MNQ")}
EXITS = (["target_1.5", "target_2", "target_3", "hold"] + [f"trail_{k}" for k in (2, 3, 4, 6)]
         + ["be_trail_3", "scale", "ema5", "ema60", "chan12", "flow"])


def snap_stop(x, d):
    """A real stop order sits on a tick: longs round down, shorts round up (never better than the formula)."""
    return np.floor(x / TICK + 1e-9) * TICK if d > 0 else np.ceil(x / TICK - 1e-9) * TICK


def snap_tgt(x, d):
    """A real limit target sits on a tick: longs round up, shorts round down."""
    return np.ceil(x / TICK - 1e-9) * TICK if d > 0 else np.floor(x / TICK + 1e-9) * TICK


class Day:
    """Full-session 5-minute bars (6 PM -> 5 PM ET) as plain numpy arrays; 'day' = Globex session."""
    def __init__(self, b):
        r = b.copy()
        self.idx = r.index
        for c in ("Open", "High", "Low", "Close", "atr5", "ema20_5", "h60_close", "h60_ema20", "delta5"):
            setattr(self, c, r[c].to_numpy(float))
        self.day = pd.factorize(r.sess)[0]
        self.sess = r.sess.to_numpy()
        self.tmin = r.tmin.to_numpy()
        self.year = r.index.year.to_numpy()
        self.n = len(r)
        last = np.r_[self.day[1:] != self.day[:-1], True]
        self.day_end = np.zeros(self.n, int)                  # index of each day's last bar
        ends = np.flatnonzero(last)
        self.day_end = ends[np.searchsorted(ends, np.arange(self.n))]


def simulate(D, i, d, rule, k0=3.0, R_pts=None, stop_px=None, min_R=None, level=None):
    """Signal on bar i's close, direction d (+1/-1).
    Returns (exit_bar, pnl_points, reason, hold_bars, mfe_R, R_points); optional keywords: see the module notes."""
    e = i + 1                       # a signal on a session's last bar enters at the 6 PM reopen
    if e >= D.n:
        return None
    O, H, L, C, A = D.Open, D.High, D.Low, D.Close, D.atr5
    entry = O[e] + d * SLIP
    if stop_px is not None:
        # stop at a given price. Take/skip is decided from the signal bar's close (known when the order is sent);
        # R for the position's risk units comes from the actual fill.
        stop = snap_stop(stop_px, d) if np.isfinite(stop_px) else np.nan
        R_sig = (C[i] + d * SLIP - stop) * d
        if not np.isfinite(R_sig) or R_sig <= 0 or (min_R is not None and R_sig < min_R):
            return None
        R = (entry - stop) * d
        if R <= 0:                                                # the open gapped through the stop: out at once
            return e, (O[e] - d * SLIP - entry) * d, "stop", 1, 0.0, R_sig
    else:
        R = k0 * A[i] if R_pts is None else R_pts
        if not np.isfinite(R) or R <= 0 or (min_R is not None and R < min_R):
            return None
        stop = snap_stop(entry - d * R, d)
    end = D.day_end[e]
    kind = rule.split("_")[0]
    target = snap_tgt(entry + d * float(rule.split("_")[1]) * R, d) if kind == "target" else None
    tgt_half = snap_tgt(entry + d * 1.5 * R, d)
    k = float(rule.split("_")[-1]) if kind in ("trail", "be") else 3.0
    parts = rule.split("_")
    tdone = False
    best = entry
    armed = False
    half_done, half_pnl = False, 0.0
    no_new_best = 0
    for t in range(e, end + 1):
        # 0) the bar OPENED through a resting limit: the opening print filled it before any later stop touch
        if target is not None and ((O[t] >= target + TICK) if d > 0 else (O[t] <= target - TICK)):
            return t, (target - entry) * d, "target", t - e + 1, (best - entry) * d / R, R
        if kind == "scale" and not half_done and ((O[t] >= tgt_half + TICK) if d > 0 else (O[t] <= tgt_half - TICK)):
            half_done, half_pnl = True, (tgt_half - entry) * d
            stop = max(stop, entry) if d > 0 else min(stop, entry)
        # 1) stop (gap-aware)
        hit = L[t] <= stop if d > 0 else H[t] >= stop
        if hit:
            fill = (min(stop, O[t]) if d > 0 else max(stop, O[t])) - d * SLIP
            pnl = (fill - entry) * d
            if kind == "scale":
                pnl = 0.5 * pnl + 0.5 * (half_pnl if half_done else pnl)
            return t, pnl, "stop", t - e + 1, (best - entry) * d / R, R
        # 2) fixed or partial targets
        if target is not None and ((H[t] >= target + TICK) if d > 0 else (L[t] <= target - TICK)):
            bx = max(best, H[t]) if d > 0 else min(best, L[t])
            return t, (target - entry) * d, "target", t - e + 1, (bx - entry) * d / R, R
        if kind == "scale" and not half_done:
            if (H[t] >= tgt_half + TICK) if d > 0 else (L[t] <= tgt_half - TICK):
                half_done, half_pnl = True, (tgt_half - entry) * d
                stop = max(stop, entry) if d > 0 else min(stop, entry)
        # 3) close-based exits, evaluated on this bar's close
        new_best = (H[t] > best) if d > 0 else (L[t] < best)
        best = max(best, H[t]) if d > 0 else min(best, L[t])
        no_new_best = 0 if new_best else no_new_best + 1
        c = C[t]
        exit_close = False
        if kind in ("ema5", "ema60"):
            ref = D.ema20_5[t] if kind == "ema5" else D.h60_ema20[t]
            px = c if kind == "ema5" else D.h60_close[t]
            right = (px > ref) if d > 0 else (px < ref)
            exit_close = armed and not right
            armed = armed or right
        elif kind == "flow" and t - e >= 2:
            fl = D.delta5[t - 2:t + 1].sum() * d
            exit_close = fl < 0 and no_new_best >= 3
        elif kind == "clock":
            exit_close = D.tmin[t] + 5 >= float(parts[1])
        elif kind == "after":
            exit_close = (t - e + 1) * 5 >= float(parts[1])
        elif kind == "tstop" and not tdone and (t - e + 1) * 5 >= float(parts[1]):
            tdone = True
            exit_close = (c - entry) * d / R < float(parts[2])
        failed = level is not None and ((c < level) if d > 0 else (c > level))
        if exit_close or failed or t == end:
            pnl = (c - d * SLIP - entry) * d
            if kind == "scale" and half_done:
                pnl = 0.5 * half_pnl + 0.5 * pnl
            why = "close" if t == end else (kind if exit_close else "level")
            return t, pnl, why, t - e + 1, (best - entry) * d / R, R
        # 4) update trailing stops for the NEXT bar (only uses closed bars)
        if kind == "trail" or (kind == "be" and (best - entry) * d >= R) or (kind == "scale" and half_done):
            if kind == "be" or kind == "scale":
                stop = max(stop, entry) if d > 0 else min(stop, entry)
            trail = snap_stop(best - d * k * A[t], d)
            stop = max(stop, trail) if d > 0 else min(stop, trail)
        elif kind == "lock" and (best - entry) * d >= float(parts[1]) * R:
            stop = max(stop, entry) if d > 0 else min(stop, entry)
            if float(parts[2]) > 0:
                trail = snap_stop(best - d * float(parts[2]) * A[t], d)
                stop = max(stop, trail) if d > 0 else min(stop, trail)
        elif kind == "chan12" and t - e >= 0:
            lo = L[max(e, t - 11):t + 1].min() if d > 0 else H[max(e, t - 11):t + 1].max()
            if t - e >= 11:
                stop = max(stop, lo) if d > 0 else min(stop, lo)
    return None


def run(D, signals, rule, k0=3.0, max_per_day=3, extra=None):
    """signals: array of (bar_index, direction) sorted by bar. One position at a time, max trades per day.
    extra: optional {signal bar: dict of simulate keywords (R_pts, stop_px, min_R, level)} for per-trade stops."""
    out, free, per_day = [], -1, {}
    for i, d in signals:
        if i < free or per_day.get(D.day[i], 0) >= max_per_day:
            continue
        r = simulate(D, i, d, rule, k0, **((extra or {}).get(i, {})))
        if r is None:
            continue
        t, pnl, why, hold, mfe, R = r
        out.append((i, d, pnl, why, hold, mfe, R))
        per_day[D.day[i]] = per_day.get(D.day[i], 0) + 1
        free = t                                              # next signal may come from the exit bar's close
    return pd.DataFrame(out, columns=["bar", "dir", "pts", "exit", "hold_bars", "mfe_R", "R_pts"])
