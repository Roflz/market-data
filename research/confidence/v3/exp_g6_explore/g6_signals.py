"""
v3/exp_g6_explore/g6_signals.py - G6 EXPLORATORY signals X1-X5, exactly as frozen in v3/PREREG.md section 3
(sha256 c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460).

Every signal is fn(S, B) -> entries (session, entry, exit, d[, stop_pts, target_pts]) and reads only S (the
market's sessions table) and B ({tf: bars}); X1 on MNQ / MYM also reads the ES sessions table (prev_ret_cc, a
column known at the 18:00 open) through a closure, and is re-checked with BOTH tables truncated (g6_run.cross_check).

Implementation choices where the frozen text is silent (fixed before any result was seen, stated here):
- X1: ES prev_ret_cc NaN (the previous ES session was a roll session) -> no trade. X1b: px_1000 == px_0930 -> no trade.
- X2: gap uses prev_close_1600 exactly as written (no fallback); NaN (roll sessions) -> no trade. stop_pts = target_pts
  = |px_0930 - prev_close_1600| (the target IS the previous 16:00 close; the stop is the same distance beyond entry).
- X3: range bars = 15-min bars of the session starting 18:00 .. 01:45 (offsets 0 .. 465 min); at least 16 of the 32
  range bars must exist (data-quality guard). Signal bars start 02:00 .. 04:45; the first close strictly beyond the
  range -> enter at the mark where that bar closes (bar start + 15 min), side = break direction;
  stop_pts = side * (entry mark price - range midpoint); entries whose fill is already through the midpoint
  (stop_pts <= 0) are skipped. Exit at the 09:30 mark.
- X4: slot returns r_j = px_end / px_start - 1 for the 13 RTH slots 09:30-10:00 ... 15:30-16:00; signal and sd over
  the previous 20 sessions (rows of the sessions table; at least 15 valid values), score = |mean| / sd; the slot
  with the largest score, side = sign(mean).
- X5: calm = prev_rv_rth <= the 1/3 quantile of prev_rv_rth over the previous 250 sessions (full 250 required);
  stretch = |px_1200/px_0930 - 1| > 0.5 x mean |px_1200/px_0930 - 1| of the previous 20 sessions (>= 15 valid).
"""
import numpy as np
import pandas as pd

LAST = pd.Timestamp("2025-06-27")          # calendar end (2025-06-30 session dropped, PREREG 0.1)


def _ent(S, sel, entry, exit_, d, stop=None, tgt=None):
    sel = (pd.Series(sel, index=S.index).fillna(False).astype(bool) & (S.index <= LAST)).to_numpy()
    e = pd.DataFrame({"session": S.index[sel], "entry": entry if np.isscalar(entry) else np.asarray(entry)[sel],
                      "exit": exit_ if np.isscalar(exit_) else np.asarray(exit_)[sel],
                      "d": np.asarray(d)[sel].astype(int)})
    if stop is not None:
        e["stop_pts"] = np.asarray(stop, float)[sel]
    if tgt is not None:
        e["target_pts"] = np.asarray(tgt, float)[sel]
    return e.reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ X1
def x1a_fn(es_S=None):
    def fn(S, B):
        cond = (S["prev_ret_cc"] if es_S is None else es_S["prev_ret_cc"].reindex(S.index)) <= -0.02
        return _ent(S, cond, "0930", "1600", np.ones(len(S)))
    return fn


def x1b_fn(es_S=None):
    def fn(S, B):
        cond = (S["prev_ret_cc"] if es_S is None else es_S["prev_ret_cc"].reindex(S.index)) <= -0.02
        m = S["px_1000"] - S["px_0930"]
        d = -np.sign(m.fillna(0.0).to_numpy())
        return _ent(S, cond & (d != 0), "1000", "1600", d)
    return fn


# ------------------------------------------------------------------------------------------------ X2
def x2_fn(S, B):
    pc = S["prev_close_1600"]
    g = S["px_0930"] / pc - 1
    a = g.abs()
    sel = (a > 0.0015) & (a < 0.005)
    pts = (S["px_0930"] - pc).abs().to_numpy()
    d = -np.sign(g.fillna(0.0).to_numpy())
    return _ent(S, sel & (d != 0), "0930", "1100", d, stop=pts, tgt=pts)


# ------------------------------------------------------------------------------------------------ X3
def x3_fn(S, B):
    b = B[15]
    sess = pd.DatetimeIndex(b["session"])
    off = ((b.index - (sess - pd.Timedelta(hours=6))) // pd.Timedelta(minutes=1)).to_numpy()
    rmask = (off >= 0) & (off <= 465)
    r = b.loc[rmask]
    rg = r.groupby(pd.DatetimeIndex(r["session"]))
    rng_ = pd.DataFrame({"rh": rg["H"].max(), "rl": rg["L"].min(), "n": rg.size()})
    rng_ = rng_[rng_["n"] >= 16]
    smask = (off >= 480) & (off <= 645)
    s = b.loc[smask, ["session", "C"]].copy()
    s["off"] = off[smask]
    s = s.join(rng_, on="session", how="inner")
    up = s["C"] > s["rh"]
    dn = s["C"] < s["rl"]
    s = s.loc[up | dn].copy()
    s["d"] = np.where(s["C"] > s["rh"], 1, -1)
    s = s.sort_index().groupby("session", sort=True).head(1)
    s = s[s["session"].isin(S.index)]
    k = ((s["off"].to_numpy() + 15) // 15).astype(int)
    from harness import MARKS
    sidx = S.index.get_indexer(pd.DatetimeIndex(s["session"]))
    PX = S[[f"px_{m}" for m in MARKS]].to_numpy(np.float64)
    epx = PX[sidx, k]
    mid = (s["rh"].to_numpy() + s["rl"].to_numpy()) / 2
    stop = s["d"].to_numpy() * (epx - mid)
    ok = np.isfinite(epx) & (stop > 0) & (pd.DatetimeIndex(s["session"]) <= LAST)
    e = pd.DataFrame({"session": pd.DatetimeIndex(s["session"])[ok], "entry": k[ok], "exit": "0930",
                      "d": s["d"].to_numpy()[ok], "stop_pts": stop[ok]})
    e.attrs["skipped_through_mid"] = int((np.isfinite(epx) & (stop <= 0)).sum())
    return e.reset_index(drop=True)


# ------------------------------------------------------------------------------------------------ X4
SLOT_START = ["0930", "1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500", "1530"]
SLOT_END = SLOT_START[1:] + ["1600"]


def x4_fn(S, B):
    R = pd.DataFrame({j: S[f"px_{b}"] / S[f"px_{a}"] - 1 for j, (a, b) in enumerate(zip(SLOT_START, SLOT_END))},
                     index=S.index)
    mu = R.rolling(20, min_periods=15).mean().shift(1)
    sd = R.rolling(20, min_periods=15).std().shift(1)
    sc = (mu.abs() / sd.where(sd > 0)).to_numpy()
    valid = np.isfinite(sc).any(axis=1)
    sc2 = np.where(np.isfinite(sc), sc, -np.inf)
    j = sc2.argmax(axis=1)
    sgn = np.sign(mu.to_numpy()[np.arange(len(S)), j])
    sel = pd.Series(valid & (sgn != 0), index=S.index)
    e = _ent(S, sel, np.array(SLOT_START)[j], np.array(SLOT_END)[j], np.nan_to_num(sgn))
    return e


# ------------------------------------------------------------------------------------------------ X5
def x5_fn(S, B):
    rv = S["prev_rv_rth"]
    thr = rv.shift(1).rolling(250, min_periods=250).quantile(1 / 3)
    calm = rv <= thr
    mv = S["px_1200"] / S["px_0930"] - 1
    avg = mv.abs().rolling(20, min_periods=15).mean().shift(1)
    sel = calm & (mv.abs() > 0.5 * avg)
    d = -np.sign(mv.fillna(0.0).to_numpy())
    return _ent(S, sel & (d != 0), "1200", "1530", d)


def signal_fns(sym, es_S):
    """hid -> (fn, family, uses 15-min bars). es_S = the ES sessions table (X1 condition for MNQ/MYM)."""
    ext = None if sym == "ES" else es_S
    return {"X1a": (x1a_fn(ext), "F2", False), "X1b": (x1b_fn(ext), "F2", False), "X2": (x2_fn, "F3", False),
            "X3": (x3_fn, "F3", True), "X4": (x4_fn, "F1", False), "X5": (x5_fn, "F3", False)}
