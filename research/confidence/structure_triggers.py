"""
Structure triggers as entry proposers (market-structure breaks and failed breaks), entered at the NEXT bar's open and
labelled with labels.label_entries (1-minute path, same costs / targets / time limit as the v1 pattern entries).

Swings: signals.pivots fractals with k bars each side (default k=5), per contract run. A swing at bar p is KNOWN only
at the close of bar p+k (it joins the state at that bar's close, before that bar's close is tested). All state resets
at a new contract run. Everything below is evaluated at the close of the signal bar t; shorts are the exact mirror
(highs <-> lows, prices negated).

  sh, sh_prev  latest / previous confirmed swing-high price;  sl, sl_prev  latest / previous confirmed swing-low price.
  uptrend      sh > sh_prev AND sl > sl_prev (both known);   downtrend  sh < sh_prev AND sl < sl_prev.

(a) bos     (break of structure, continuation). In an UPTREND, the FIRST close above the latest confirmed swing high
            sh (C[t] > sh; each swing high can be broken once - later closes above the same level do nothing)
            -> long. stop = sl - 1 tick (latest confirmed swing low).
(b) choch   (change of character, reversal). In a DOWNTREND, the first close above the latest confirmed swing high
            -> long. stop = lowest low from that swing high's pivot bar through t, - 1 tick (this is the most recent
            swing low after the high, or any lower unconfirmed low since).
            (a) and (b) share the "first close above sh" event: it is bos, choch or nothing (no trend) - never two.
(c) reclaim (failed breakdown). A close below the latest confirmed swing low sl starts an excursion at bar j0 (each
            swing low can start one excursion). If a close back ABOVE that level happens at bar t with t - j0 <= 5
            -> long; stop = lowest low of bars j0..t - 1 tick. If 5 bars after j0 have passed with no close above,
            the breakdown held and the excursion ends with no trade. No trend condition.

Events are only emitted on bars that can be entered at the next bar's open (labels.eligible: same session segment,
not after the 16:45 forced bar), but the state machine runs on every bar (a "first close" on a non-tradable bar
consumes the level).
"""
import numpy as np
import pandas as pd

import labels as lb
import signals as sg

TRIGGERS = ("bos", "choch", "reclaim")
RECLAIM_BARS = 5
EVENT_COLS = ["t", "i", "d", "trigger", "patterns", "n_patterns", "stop", "level", "bars_since_level"]


def _scan_long(H, L, C, run, k, tick, reclaim_bars=RECLAIM_BARS):
    """Long-side triggers on (possibly mirrored) arrays. Returns list of (i, trigger, stop, level, bars_since_level)."""
    n = len(H)
    lo, hi = sg.pivots(pd.DataFrame(dict(H=H, L=L, run=run)), k)
    conf_hi = np.full(n, -1, np.int64); conf_lo = np.full(n, -1, np.int64)   # pivot index confirmed at bar t
    q = np.flatnonzero(hi); conf_hi[q + k] = q
    q = np.flatnonzero(lo); conf_lo[q + k] = q
    out = []
    nan = np.nan
    r_prev = None
    for t in range(n):
        if run[t] != r_prev:                                  # new contract: forget everything
            r_prev = run[t]
            sh = sh_prev = sl = sl_prev = nan
            sh_p = sl_p = -1; sh_c = sl_c = -1
            sh_done = sl_used = True
            exc = False; exc_lvl = nan; j0 = -1; exc_c = -1
        if conf_hi[t] >= 0:
            sh_prev, sh, sh_p, sh_c, sh_done = sh, H[conf_hi[t]], conf_hi[t], t, False
        if conf_lo[t] >= 0:
            sl_prev, sl, sl_p, sl_c, sl_used = sl, L[conf_lo[t]], conf_lo[t], t, False
        # (a)/(b): first close above the latest confirmed swing high
        if not sh_done and C[t] > sh:
            sh_done = True
            known = not (np.isnan(sh_prev) or np.isnan(sl) or np.isnan(sl_prev))
            if known and sh > sh_prev and sl > sl_prev:
                out.append((t, "bos", sl - tick, sh, t - sh_c))
            elif known and sh < sh_prev and sl < sl_prev:
                out.append((t, "choch", L[sh_p:t + 1].min() - tick, sh, t - sh_c))
        # (c): failed breakdown of a confirmed swing low
        if exc:
            if C[t] > exc_lvl:
                if t - j0 <= reclaim_bars:
                    out.append((t, "reclaim", L[j0:t + 1].min() - tick, exc_lvl, t - exc_c))
                exc = False
            elif t - j0 >= reclaim_bars:
                exc = False
        if not exc and not sl_used and C[t] < sl:
            sl_used = True
            exc, exc_lvl, j0, exc_c = True, sl, t, sl_c
    return out


def detect(b, tick, tf, k=5, reclaim_bars=RECLAIM_BARS):
    """All structure-trigger events on bars b (signals.bars frame: O H L C seg run, index = bar start).
    Returns DataFrame [t, i, d, trigger, patterns (= []), n_patterns (= 0), stop, level, bars_since_level]
    sorted by (i, d, trigger); a labels.label_entries events frame (entry at the open of bar i+1)."""
    H, L, C = (b[x].to_numpy(np.float64) for x in "HLC")
    run = b.run.to_numpy()
    ok, _ = lb.eligible(b, tf)
    rows = []
    for d in (1, -1):
        Hd, Ld, Cd = (H, L, C) if d > 0 else (-L, -H, -C)
        for i, trg, stop, lvl, age in _scan_long(Hd, Ld, Cd, run, k, tick, reclaim_bars):
            if ok[i]:
                rows.append((i, d, trg, d * stop, d * lvl, age))
    ev = pd.DataFrame(rows, columns=["i", "d", "trigger", "stop", "level", "bars_since_level"])
    ev["i"] = ev["i"].astype(np.int64)
    ev["d"] = ev["d"].astype(np.int8)
    ev["t"] = b.index[ev.i.to_numpy()]
    ev["patterns"] = [[] for _ in range(len(ev))]
    ev["n_patterns"] = 0
    ev = ev[EVENT_COLS].sort_values(["i", "d", "trigger"]).reset_index(drop=True)
    return ev


def one_hots(ev):
    """trg_<name> float32 one-hot columns for the model."""
    return pd.DataFrame({f"trg_{x}": (ev["trigger"].to_numpy() == x).astype(np.float32) for x in TRIGGERS},
                        index=ev.index)
