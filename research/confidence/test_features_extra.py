"""Tests for features_extra.py (Blocks A and B). Synthetic data only (light; no 1-minute data is loaded).
Usage: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_features_extra.py

1. Hand-made bars: exact values of every column at chosen bars, run boundaries -> NaN, ties -> most recent bar.
2. Loop-based reference implementation on a 1,500-bar random walk with 3 contract runs: all columns equal.
3. R20 equals features.r20 (the scale unit of the entry datasets).
4. PERTURBATION: for many cut bars t, every bar after t is replaced by garbage (also: given a new run id, or dropped);
   rows <= t must be bit-identical.
5. Orientation: orient_blocks(X, -1) == compute_blocks(price-mirrored bars); orient_blocks(X, +1) == X.
(The real-data check R20 == entries_NQ_15.R20 at the joined rows runs in run_feature_blocks.py.)
"""
import math
import sys

import numpy as np
import pandas as pd

import features as fe
import features_extra as fx

ok_all = True
TICK = 0.25


def check(name, cond, info=""):
    global ok_all
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info and not cond else ""))
    ok_all &= bool(cond)


def same(a, b):
    """Bit-identical incl. NaN positions."""
    a = np.asarray(a, np.float32); b = np.asarray(b, np.float32)
    return a.shape == b.shape and bool(np.all((a == b) | (np.isnan(a) & np.isnan(b))))


def close(a, b, tol=1e-5):
    a = np.asarray(a, np.float64); b = np.asarray(b, np.float64)
    return a.shape == b.shape and bool(np.all((np.abs(a - b) <= tol) | (np.isnan(a) & np.isnan(b))))


def walk(n, runs, seed=0):
    rng = np.random.default_rng(seed)
    C = 1000 + np.cumsum(rng.integers(-8, 9, n)) * TICK
    O = np.r_[C[0], C[:-1]] + rng.integers(-2, 3, n) * TICK
    H = np.maximum(O, C) + rng.integers(0, 6, n) * TICK
    L = np.minimum(O, C) - rng.integers(0, 6, n) * TICK
    run = np.repeat(np.arange(1, len(runs) + 1), runs)
    idx = pd.date_range("2020-01-01", periods=n, freq="15min")
    return pd.DataFrame({"O": O, "H": H, "L": L, "C": C, "V": 1.0, "run": run}, index=idx)


# --------------------------------------------------------------------------------------------- 1. hand-made
n = 80
H = np.full(n, 101.0); L = np.full(n, 99.0); C = np.full(n, 100.0)
C[60] = 100.5                                       # bar 60: close 100.5
H[50] = 103.0                                       # 20-bar high at bar 50 (t=60 -> 10 bars ago)
H[55] = 103.0                                       # equal high later -> most recent counts: 5 bars ago
L[45] = 96.0                                        # 20-bar window of t=60 is 41..60: low 96 at 45 -> 15 bars ago
L[5] = 90.0                                         # 60-bar window of t=60 is 1..60: low 90 at bar 5 -> 55 bars ago
C[40] = 98.0                                        # ret20 at 60: 100.5 - 98 = 2.5
C[59] = 101.0                                       # ret1 at 60: -0.5
b = pd.DataFrame({"H": H, "L": L, "C": C, "run": 1}, index=pd.date_range("2021-01-04", periods=n, freq="15min"))
X = fx.compute_blocks(b, TICK)
R = fx.r20(b, TICK)
# R20 at 60 = mean range of bars 40..59: all 2 except bar 45 (101-96=5), 50 (103-99=4), 55 (4)
r60 = (17 * 2 + 5 + 4 + 4) / 20
check("hand R20[60]", abs(R[60] - r60) < 1e-12, f"{R[60]} vs {r60}")
x = X.iloc[60]
check("hand ret1", abs(x.ret1 - (-0.5 / r60)) < 1e-6, x.ret1)
check("hand ret20", abs(x.ret20 - (2.5 / r60)) < 1e-6, x.ret20)
check("hand ret60_volscaled", abs(x.ret60_volscaled - (0.5 / (r60 * math.sqrt(60)))) < 1e-6, x.ret60_volscaled)
check("hand rsv20", abs(x.rsv20 - (100.5 - 96) / (103 - 96)) < 1e-6, x.rsv20)
check("hand rsv60", abs(x.rsv60 - (100.5 - 90) / (103 - 90)) < 1e-6, x.rsv60)
check("hand rsv5 (window 56..60: H 101, L 99)", abs(x.rsv5 - 0.75) < 1e-6, x.rsv5)
check("hand bars_since_high20 tie -> most recent (5/20)", abs(x.bars_since_high20 - 5 / 20) < 1e-7,
      x.bars_since_high20)
check("hand bars_since_low20 (15/20)", abs(x.bars_since_low20 - 15 / 20) < 1e-7, x.bars_since_low20)
check("hand bars_since_low60 (55/60)", abs(x.bars_since_low60 - 55 / 60) < 1e-7, x.bars_since_low60)
check("hand bars_since_high60 (5/60)", abs(x.bars_since_high60 - 5 / 60) < 1e-7, x.bars_since_high60)
check("hand range20_width", abs(x.range20_width - 7 / r60) < 1e-6, x.range20_width)
# prev_close_rsv20 at 61 = rsv20 at 60
check("hand prev_close_rsv20[61] == rsv20[60]", X.prev_close_rsv20.iloc[61] == X.rsv20.iloc[60])
# bars_since_high20 at t=50 (the high bar itself) = 0
check("hand bars_since_high20 = 0 on the high bar", X.bars_since_high20.iloc[55] == 0.0)
# first 20 bars (no R20) -> NaN; 60-bar items NaN before bar 59
check("hand NaN before R20 exists", X.iloc[:20].isna().all().all())
check("hand rsv60 NaN at 58, finite at 59", np.isnan(X.rsv60.iloc[58]) and np.isfinite(X.rsv60.iloc[59]))
check("hand ret60 NaN at 59, finite at 60", np.isnan(X.ret60_volscaled.iloc[59])
      and np.isfinite(X.ret60_volscaled.iloc[60]))
# flat window -> rsv NaN
bf = pd.DataFrame({"H": 100.0, "L": 100.0, "C": 100.0, "run": 1}, index=b.index)
Xf = fx.compute_blocks(bf, TICK)
check("flat bars: rsv NaN, range20_width 0, R20 at 2-tick floor", Xf.rsv20.iloc[30:].isna().all()
      and (Xf.range20_width.iloc[30:] == 0).all() and fx.r20(bf, TICK)[30] == 2 * TICK)
# run boundary: second run starts at bar 40 -> everything NaN for bars 40..59, ret5 needs 5 bars of the new run + R20
b2 = b.copy(); b2.loc[b2.index[40:], "run"] = 2
X2 = fx.compute_blocks(b2, TICK)
check("run boundary: NaN until the new run has 20 bars", X2.iloc[40:60].isna().all().all()
      and np.isfinite(X2.ret5.iloc[60]) and np.isnan(X2.rsv60.iloc[79]) and np.isfinite(X2.ret20.iloc[60])
      and np.isnan(X2.ret60_volscaled.iloc[79]) and np.isfinite(X2.rsv20.iloc[60]))
check("dtypes float32 and column order", list(X.columns) == fx.COLUMNS and (X.dtypes == np.float32).all())

# --------------------------------------------------------------------------------------------- 2. loop reference
B = walk(1500, [500, 400, 600], seed=1)
XB = fx.compute_blocks(B, TICK)
Hh, Ll, Cc, rr = B.H.to_numpy(), B.L.to_numpy(), B.C.to_numpy(), B.run.to_numpy()
ref = {c: np.full(len(B), np.nan) for c in fx.COLUMNS}
Rref = np.full(len(B), np.nan)
for t in range(len(B)):
    if t >= 20 and rr[t - 20] == rr[t]:
        Rref[t] = max(np.mean(Hh[t - 20:t] - Ll[t - 20:t]), 2 * TICK)
    Rt = Rref[t]
    if not np.isfinite(Rt):
        continue
    for nn in fx.RET_N:
        if t >= nn and rr[t - nn] == rr[t]:
            ref[f"ret{nn}"][t] = np.clip((Cc[t] - Cc[t - nn]) / Rt, -50, 50)
    if t >= 60 and rr[t - 60] == rr[t]:
        ref["ret60_volscaled"][t] = np.clip((Cc[t] - Cc[t - 60]) / (Rt * math.sqrt(60)), -50, 50)
    for nn in (5, 20, 60):
        if t >= nn - 1 and rr[t - nn + 1] == rr[t]:
            hh, ll = Hh[t - nn + 1:t + 1].max(), Ll[t - nn + 1:t + 1].min()
            ref[f"rsv{nn}"][t] = (Cc[t] - ll) / (hh - ll) if hh > ll else np.nan
            if nn in (20, 60):
                jh = max(j for j in range(t - nn + 1, t + 1) if Hh[j] == hh)
                jl = max(j for j in range(t - nn + 1, t + 1) if Ll[j] == ll)
                ref[f"bars_since_high{nn}"][t] = (t - jh) / nn
                ref[f"bars_since_low{nn}"][t] = (t - jl) / nn
            if nn == 20:
                ref["range20_width"][t] = np.clip((hh - ll) / Rt, -50, 50)
    if t >= 20 and rr[t - 20] == rr[t]:                  # bar t-1's 20-bar window t-20..t-1
        hh, ll = Hh[t - 20:t].max(), Ll[t - 20:t].min()
        ref["prev_close_rsv20"][t] = (Cc[t - 1] - ll) / (hh - ll) if hh > ll else np.nan
check("reference R20 == fx.r20", close(fx.r20(B, TICK), Rref, 1e-9))
for c in fx.COLUMNS:
    check(f"reference {c}", close(XB[c].to_numpy(), ref[c], 1e-5))
check("random walk: some finite values in every column", XB.notna().sum().min() > 500)

# --------------------------------------------------------------------------------------------- 3. R20 == features.r20
check("fx.r20 == features.r20 (bit-identical)", same(fx.r20(B, TICK), fe.r20(B, TICK)))

# --------------------------------------------------------------------------------------------- 4. perturbation
rng = np.random.default_rng(7)
n_fail = 0
cuts = list(range(15, 1500, 37)) + [499, 500, 501, 899, 900, 1499]
for t in cuts:
    for mode in ("garbage", "newrun", "drop"):
        P = B.copy()
        if mode == "drop":
            P = P.iloc[:t + 1]
        else:
            k = len(P) - t - 1
            if k == 0:
                continue
            g = rng.normal(0, 500, (k, 3)) + 1000
            P.iloc[t + 1:, P.columns.get_loc("H")] = g.max(axis=1) + 5
            P.iloc[t + 1:, P.columns.get_loc("L")] = g.min(axis=1) - 5
            P.iloc[t + 1:, P.columns.get_loc("C")] = g[:, 1]
            if mode == "newrun":
                P.iloc[t + 1:, P.columns.get_loc("run")] = 99
        XP = fx.compute_blocks(P, TICK)
        if not same(XP.iloc[:t + 1].to_numpy(), XB.iloc[:t + 1].to_numpy()):
            n_fail += 1
check(f"perturbation: rows <= t unchanged ({len(cuts)} cuts x 3 modes)", n_fail == 0, f"{n_fail} failures")

# --------------------------------------------------------------------------------------------- 5. orientation
M = B.copy()
M["H"], M["L"], M["C"] = -B.L, -B.H, -B.C
XM = fx.compute_blocks(M, TICK)
XS = fx.orient_blocks(XB, -1)
check("orient(-1) == blocks of the price-mirrored bars", close(XS.to_numpy(), XM.to_numpy(), 1e-5))
check("orient(+1) is the identity", same(fx.orient_blocks(XB, 1).to_numpy(), XB.to_numpy()))
d = np.where(np.arange(len(XB)) % 2 == 0, 1, -1)
XD = fx.orient_blocks(XB, d)
check("orient per-row d: longs keep, shorts == orient(-1)",
      same(XD.iloc[::2].to_numpy(), XB.iloc[::2].to_numpy()) and same(XD.iloc[1::2].to_numpy(), XS.iloc[1::2].to_numpy()))
check("orient: range20_width unchanged, bars_since swapped, rsv -> 1 - rsv",
      same(XS.range20_width, XB.range20_width) and same(XS.bars_since_high20, XB.bars_since_low20)
      and close(XS.rsv20, 1 - XB.rsv20.astype(np.float64), 1e-6) and same(XS.ret5, -XB.ret5))
check("block columns are not in features.SIGNED (walkforward must not re-orient them)",
      not (set(fx.COLUMNS) & (set(fe.SIGNED) | set(fe.MIRROR) | set(fe.MIRROR.values()))))

print("ALL PASS" if ok_all else "SOME FAILED")
sys.exit(0 if ok_all else 1)
