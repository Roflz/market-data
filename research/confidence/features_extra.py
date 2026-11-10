"""Extra entry features: FEATURE_RESEARCH.md section 4, Block A (multi-horizon returns) and Block B (range position and
timing of extremes).

Usage:
  build_blocks(sym, tf)          -> DataFrame on signals.bars(sym, tf).index (float32), RAW long-perspective values
  compute_blocks(b, tick)        -> the same from a bars-like frame (H L C run columns), pure function of b
  orient_blocks(X, d)            -> X seen from trade direction d (+1 long / -1 short), see "Orientation"
  BLOCK_A, BLOCK_B               column lists

Every value at bar t uses bars <= t only (known at t's close) and only bars of the SAME contract run (signals.bars
'run' column); a window that would reach into an earlier run gives NaN.
R20 = mean (H - L) of the 20 bars BEFORE t (t-20 .. t-1, same run), floored at 2 ticks (= features.r20, = the R20 column
of the entry datasets). R20-unit values are winsorized to +-50 like features.CLIP.

Block A (signed: + = price went up):
  retN            = (C_t - C_{t-N}) / R20_t, N = 1, 2, 3, 5, 10, 20 (NaN if bar t-N is not in t's run)
  ret60_volscaled = (C_t - C_{t-60}) / (R20_t * sqrt(60))
Block B (window of N bars = t-N+1 .. t, bar t included; NaN if bar t-N+1 is not in t's run):
  rsvN            = (C_t - LL_N) / (HH_N - LL_N), N = 5, 20, 60; NaN when HH_N == LL_N. 0 = close at the low, 1 = high
  prev_close_rsv20 = rsv20 of bar t-1 (window t-20 .. t-1, bar t-1's close); NaN if t-1 is in another run
  bars_since_high20 = (t - most recent bar in the 20-bar window whose H equals HH_20) / 20   (0 .. 0.95)
  bars_since_low20  = same with L and LL_20;  bars_since_high60 / bars_since_low60 = same over 60 bars, / 60
  range20_width   = (HH_20 - LL_20) / R20_t  (unsigned)
  Ties: the MOST RECENT bar that made the high/low counts (an equal high made later resets the count).

Orientation (orient_blocks; done here, NOT by walkforward.orient - these columns are not in features.SIGNED):
  for a short (d = -1): retN and ret60_volscaled times -1; rsv5/20/60 and prev_close_rsv20 -> 1 - value;
  bars_since_high* <-> bars_since_low* swap; range20_width unchanged. So + / high values always mean "price moved in
  the trade's direction" / "close near the extreme in the trade's direction" and bars_since_high means "bars since
  the favourable extreme" for both sides. Exact identity: orient_blocks(compute_blocks(b), -1) ==
  compute_blocks(price-mirrored b) (H' = -L, L' = -H, C' = -C), tested in test_features_extra.py.
"""
import math

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

RET_N = (1, 2, 3, 5, 10, 20)
RSV_N = (5, 20, 60)
CLIP_R20 = 50.0
BLOCK_A = [f"ret{n}" for n in RET_N] + ["ret60_volscaled"]
BLOCK_B = [f"rsv{n}" for n in RSV_N] + ["prev_close_rsv20", "bars_since_high20", "bars_since_low20",
                                        "bars_since_high60", "bars_since_low60", "range20_width"]
COLUMNS = BLOCK_A + BLOCK_B
RET_COLS = BLOCK_A
RSV_COLS = [f"rsv{n}" for n in RSV_N] + ["prev_close_rsv20"]
SWAP = {"bars_since_high20": "bars_since_low20", "bars_since_high60": "bars_since_low60"}


def _same_run(run, k):
    """ok[t] = bar t-k exists and is in t's run (runs are contiguous, so every bar in between is too)."""
    out = np.zeros(len(run), bool)
    if k == 0:
        out[:] = True
    elif k < len(run):
        out[k:] = run[k:] == run[:-k]
    return out


def _lag(a, k):
    out = np.full(len(a), np.nan)
    if 0 < k < len(a):
        out[k:] = a[:-k]
    return out


def _div(a, b):
    with np.errstate(divide="ignore", invalid="ignore"):
        out = a / b
    return np.where(np.isfinite(out), out, np.nan)


def r20(b, tick):
    """Mean (H - L) of the 20 bars before t in t's run, floored at 2 ticks; NaN in a run's first 20 bars."""
    rng = (b["H"] - b["L"]).to_numpy(np.float64)
    m = pd.Series(rng).rolling(20).mean().to_numpy()       # m[j] = mean rng[j-19 .. j]
    out = np.full(len(rng), np.nan)
    out[1:] = m[:-1]                                        # mean rng[t-20 .. t-1]
    out = np.where(_same_run(b["run"].to_numpy(), 20), out, np.nan)
    return np.maximum(out, 2 * tick)


def _window_stats(H, L, run, n):
    """HH, LL over bars t-n+1..t and bars since the most recent HH / LL bar (NaN where the window leaves t's run)."""
    N = len(H)
    hh = np.full(N, np.nan); ll = np.full(N, np.nan); bsh = np.full(N, np.nan); bsl = np.full(N, np.nan)
    if N >= n:
        wh = sliding_window_view(H, n)                      # row j = bars j .. j+n-1, i.e. t = j+n-1
        wl = sliding_window_view(L, n)
        hh[n - 1:] = wh.max(axis=1)
        ll[n - 1:] = wl.min(axis=1)
        bsh[n - 1:] = np.argmax(wh[:, ::-1], axis=1)        # reversed: first max = most recent one, offset = bars ago
        bsl[n - 1:] = np.argmin(wl[:, ::-1], axis=1)
    ok = _same_run(run, n - 1)
    return [np.where(ok, a, np.nan) for a in (hh, ll, bsh, bsl)]


def compute_blocks(b, tick):
    """Block A + B columns (raw, long perspective) from a bars-like frame with H, L, C, run. float32, on b.index."""
    H = b["H"].to_numpy(np.float64); L = b["L"].to_numpy(np.float64); C = b["C"].to_numpy(np.float64)
    run = b["run"].to_numpy()
    R = r20(b, tick)
    out = {}
    for n in RET_N:
        out[f"ret{n}"] = np.where(_same_run(run, n), _div(C - _lag(C, n), R), np.nan)
    out["ret60_volscaled"] = np.where(_same_run(run, 60), _div(C - _lag(C, 60), R * math.sqrt(60)), np.nan)
    st = {n: _window_stats(H, L, run, n) for n in RSV_N}
    for n in RSV_N:
        hh, ll, _, _ = st[n]
        out[f"rsv{n}"] = _div(C - ll, hh - ll)
    out["prev_close_rsv20"] = np.where(_same_run(run, 1), _lag(out["rsv20"], 1), np.nan)
    for n in (20, 60):
        _, _, bsh, bsl = st[n]
        out[f"bars_since_high{n}"] = bsh / n
        out[f"bars_since_low{n}"] = bsl / n
    hh, ll, _, _ = st[20]
    out["range20_width"] = _div(hh - ll, R)
    X = pd.DataFrame(out, index=b.index)[COLUMNS]
    clip = RET_COLS + ["range20_width"]
    X[clip] = X[clip].clip(-CLIP_R20, CLIP_R20)
    X.loc[~np.isfinite(R), :] = np.nan                    # nothing without the scale unit (run's first 20 bars)
    return X.astype(np.float32)


def build_blocks(sym, tf):
    """Block A + B on signals.bars(sym, tf).index (loads 1-minute data: heavy)."""
    import signals as sg                                    # noqa: PLC0415
    b = sg.bars(sym, tf)
    return compute_blocks(b, sg.SPEC[sym]["tick"])


def orient_blocks(X, d):
    """X (any subset of COLUMNS) seen from direction d (+1 / -1, scalar or per row), float32 copy."""
    d = np.broadcast_to(np.asarray(d, np.float32), (len(X),)).astype(np.float32)
    short = d < 0
    out = X.astype(np.float32, copy=True)
    for c in RET_COLS:
        if c in X.columns:
            out[c] = X[c].to_numpy(np.float32) * d
    for c in RSV_COLS:
        if c in X.columns:
            v = X[c].to_numpy(np.float32)
            out[c] = np.where(short, np.float32(1.0) - v, v)
    for a, c in SWAP.items():
        if a in X.columns and c in X.columns:
            va, vc = X[a].to_numpy(np.float32), X[c].to_numpy(np.float32)
            out[a] = np.where(short, vc, va)
            out[c] = np.where(short, va, vc)
        elif a in X.columns or c in X.columns:
            raise KeyError(f"orient_blocks needs both {a} and {c}")
    return out
