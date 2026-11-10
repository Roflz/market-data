"""Tests for features.py.
Usage: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 test_features.py

1. PERTURBATION (look-ahead) test on real data: ~3,000 15-min bars of ES/NQ/YM around the March 2023 roll. For several
   cut bars t, every 1-minute bar starting at or after t's close is replaced by garbage (in ALL markets; the 1-minute
   bars are also the VWAP and 60-min source), or dropped, or given a new contract id; build_features is re-run for each
   market and every row <= t of F (and of b) must be bit-identical. Also at tf = 5 and 60.
2. Independent loop-based reference implementations on the same real slice (swings, structure, fib, breaks, R20,
   trend, momentum, session, 60-min mapping, cross-market).
3. Hand-made bars for a few columns, orient(), column list / dtypes.
4. Regression tests for the review findings: features.orient == walkforward.orient and walkforward._prepare
   (one direction convention, MIRROR swap included); a full
   price-mirror test of compute_features (60-min and other markets mirrored too) against the documented
   exceptions; fibpos NaN when one bar is both swing pivots; mom_x100 touch-and-return; winsorizing (CLIP) of the
   R20-floor blow-ups. Plus full-history checks of the same on ES/NQ/YM.
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import features as fe
import research_lib as rl
import signals as sg

warnings.simplefilter("ignore", RuntimeWarning)
ok_all = True
W0, W1 = "2023-02-01", "2023-03-20"            # ES/NQ/YM roll on 2023-03-14 20:00 inside the window
TZ = "America/New_York"


def check(name, cond, info=""):
    global ok_all
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info and not cond else ""))
    ok_all &= bool(cond)


# --------------------------------------------------------------------------------------------- data plumbing
_orig_bars_1m = rl.bars_1m
SRC = {}
for s in fe.MARKETS:
    m = _orig_bars_1m(s)
    SRC[s] = m[(m.index >= pd.Timestamp(W0, tz=TZ)) & (m.index < pd.Timestamp(W1, tz=TZ))].copy()


def build(sources, sym, tf):
    """build_features(sym, tf) with research_lib.bars_1m returning sources[sym] (no caching)."""
    rl.bars_1m = lambda s, _src=sources: _src[s].copy()
    try:
        return fe.build_features(sym, tf, cache=False)
    finally:
        rl.bars_1m = _orig_bars_1m


def garbage(m, cut, rng, new_inst=False):
    """Replace every 1-min bar starting at/after `cut` (naive NY time) with random prices/volume."""
    m = m.copy()
    after = m.index.tz_localize(None) >= cut
    k = int(after.sum())
    if not k:
        return m
    base = m.Close[~after].iloc[-1] if (~after).any() else 1000.0
    p = base * rng.uniform(0.3, 3.0) * np.exp(np.cumsum(rng.normal(0, 0.01, k)))
    o = p; c = p * (1 + rng.normal(0, 0.005, k))
    m.loc[after, "Open"] = o
    m.loc[after, "Close"] = c
    m.loc[after, "High"] = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.003, k)))
    m.loc[after, "Low"] = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.003, k)))
    m.loc[after, "Volume"] = rng.integers(0, 5000, k)
    if new_inst:
        m.loc[after, "instrument_id"] = 987654321
    return m


def frames_equal_upto(A, B, T):
    """Rows with index <= T identical (NaN == NaN). Returns (ok, list of differing columns)."""
    a, bb = A[A.index <= T], B[B.index <= T]
    if len(a) != len(bb) or not a.index.equals(bb.index):
        return False, ["<index>"]
    bad = []
    for c in a.columns:
        x, y = a[c].to_numpy(), bb[c].to_numpy()
        if x.dtype.kind in "fc":
            same = np.array_equal(x, y, equal_nan=True)
        else:
            same = np.array_equal(x.astype(str), y.astype(str))
        if not same:
            bad.append(c)
    return not bad, bad


# --------------------------------------------------------------------------------------------- 1. perturbation
print("== perturbation test (look-ahead)")
t0 = time.time()
BASE = {(s, tf): build(SRC, s, tf) for tf in (15,) for s in fe.MARKETS}
bE = BASE[("ES", 15)][0]
idx = bE.index
r = bE.run.to_numpy(); roll = int(np.flatnonzero(r[1:] != r[:-1])[0] + 1)
mins = idx.hour * 60 + idx.minute


def first_at(hhmm, after):
    h, mm = hhmm
    return int(np.flatnonzero((mins == h * 60 + mm) & (np.arange(len(idx)) > after))[0])


cuts = sorted({roll - 1, roll, roll + 25, first_at((18, 0), 1200), first_at((16, 45), 1500), first_at((10, 15), 2000),
               first_at((10, 45), 2200), first_at((9, 30), 900), len(idx) - 400})
print(f"   {len(idx)} ES 15-min bars {idx[0]} .. {idx[-1]}; cut bars: " + ", ".join(str(idx[c]) for c in cuts))
rng = np.random.default_rng(7)
n_cmp = 0
for ci in cuts:
    T = idx[ci]
    cut = T + pd.Timedelta(minutes=15)
    variants = {
        "garbage": {s: garbage(SRC[s], cut, rng) for s in fe.MARKETS},
        "garbage+new contract": {s: garbage(SRC[s], cut, rng, new_inst=True) for s in fe.MARKETS},
        "truncated": {s: SRC[s][SRC[s].index.tz_localize(None) < cut] for s in fe.MARKETS},
    }
    for vname, srcs in variants.items():
        for s in fe.MARKETS:
            b0, F0 = BASE[(s, 15)]
            b1, F1 = build(srcs, s, 15)
            okF, badF = frames_equal_upto(F0, F1, T)
            okb, badb = frames_equal_upto(b0, b1, T)
            n_cmp += 1
            if not (okF and okb):
                check(f"{s} cut {T} {vname}: rows <= t identical", False, f"F: {badF} b: {badb}")
            if vname == "garbage":                 # the perturbation must actually reach the features after t
                a, z = F0[F0.index > T], F1[F1.index > T]
                common = a.index.intersection(z.index)
                changed = not np.array_equal(a.loc[common].to_numpy(), z.loc[common].to_numpy(), equal_nan=True)
                if not changed:
                    check(f"{s} cut {T}: garbage changed rows after t", False)
check(f"rows <= t identical for {len(cuts)} cuts x 3 variants x 3 markets ({n_cmp} rebuilds, all 80 columns + b)",
      ok_all)
# the test can see a 1-bar look-ahead: next bar's close differs between base and garbage at the cut bar
b1g, _ = build({s: garbage(SRC[s], idx[cuts[3]] + pd.Timedelta(minutes=15), np.random.default_rng(1))
                for s in fe.MARKETS}, "ES", 15)
leak0 = bE.C.shift(-1).loc[idx[cuts[3]]]; leak1 = b1g.C.shift(-1).loc[idx[cuts[3]]]
check("sanity: a deliberately leaky value (next close) would be caught", leak0 != leak1)
# other timeframes, two cuts each
for tf in (5, 60):
    for s in ("ES", "NQ"):
        b0, F0 = build(SRC, s, tf)
        for frac in (0.4, 0.75):
            T = b0.index[int(len(b0) * frac)]
            cut = T + pd.Timedelta(minutes=tf)
            srcs = {x: garbage(SRC[x], cut, rng) for x in fe.MARKETS}
            b1, F1 = build(srcs, s, tf)
            okF, badF = frames_equal_upto(F0, F1, T)
            check(f"tf={tf} {s} cut {T}: rows <= t identical", okF, str(badF))
print(f"   perturbation tests took {time.time() - t0:.1f}s")

# --------------------------------------------------------------------------------------------- 2. references
print("== loop-based reference implementations on the real ES slice")
b, F = BASE[("ES", 15)]
n = len(b)
O, H, L, C, V = (b[x].to_numpy(np.float64) for x in "OHLCV")
run, seg, inst = b.run.to_numpy(), b.seg.to_numpy(), b.inst.to_numpy()
tick = sg.SPEC["ES"]["tick"]


def close(name, got, exp, rtol=2e-5, atol=2e-5):
    got = np.asarray(got, np.float64); exp = np.asarray(exp, np.float32).astype(np.float64)
    same_nan = np.array_equal(np.isnan(got), np.isnan(exp))
    m = ~np.isnan(exp)
    ok = same_nan and np.allclose(got[m], exp[m], rtol=rtol, atol=atol)
    info = "" if ok else (f"nan mismatch at {np.flatnonzero(np.isnan(got) != np.isnan(exp))[:5]}" if not same_nan
                          else f"max diff {np.max(np.abs(got[m] - exp[m])):.3g} at {np.flatnonzero(~np.isclose(got[m], exp[m], rtol=rtol, atol=atol))[:5]}")
    check(f"{name} matches the reference ({int(m.sum())} non-NaN)", ok and m.sum() > 0, info)


R = np.full(n, np.nan)
for t in range(20, n):
    if run[t - 20] == run[t]:
        R[t] = max(np.mean(H[t - 20:t] - L[t - 20:t]), 2 * tick)
close("R20 (b.R20)", b.R20.to_numpy(), R)


def ref_pivots(H, L, run, k):
    nn = len(H)
    hi = np.zeros(nn, bool); lo = np.zeros(nn, bool)
    for p in range(k, nn - k):
        if run[p - k] != run[p + k]:
            continue
        nb = [p + i for i in range(-k, k + 1) if i]
        hi[p] = all(H[p] > H[j] for j in nb)
        lo[p] = all(L[p] < L[j] for j in nb)
    return hi, lo


def ref_structure(H, L, C, run, R, k):
    nn = len(H)
    hp, lp = ref_pivots(H, L, run, k)
    hs, ls = list(np.flatnonzero(hp)), list(np.flatnonzero(lp))
    out = {c: np.full(nn, np.nan) for c in ("dhi", "dlo", "brk", "struct", "fib", "atfib")}
    for t in range(nn):
        def latest(lst, vals):
            c = [p for p in lst if p + k <= t]
            if not c or run[c[-1] + k] != run[t]:
                return None, np.nan, np.nan
            p = c[-1]
            prev = vals[c[-2]] if len(c) > 1 and run[c[-2]] == run[p] else np.nan
            return p, vals[p], prev
        ph, h, hprev = latest(hs, H)
        pl, l, lprev = latest(ls, L)
        out["dhi"][t] = (C[t] - h) / R[t]
        out["dlo"][t] = (C[t] - l) / R[t]
        up = ph is not None and C[t] > h and not any(C[s] > h for s in range(ph + k + 1, t))
        dn = pl is not None and C[t] < l and not any(C[s] < l for s in range(pl + k + 1, t))
        out["brk"][t] = float(up) - float(dn)
        if not np.isnan(hprev) and not np.isnan(lprev):
            out["struct"][t] = 1.0 if (h > hprev and l > lprev) else -1.0 if (h < hprev and l < lprev) else 0.0
        if ph is not None and pl is not None:
            a, z, sgn = (l, h, 1.0) if ph > pl else (h, l, -1.0)
            # one bar that is both the latest swing high and low: leg direction unknown -> fibpos NaN
            out["fib"][t] = (C[t] - a) / (z - a) * sgn if (z != a and ph != pl) else np.nan
            if np.isfinite(R[t]) and z != a:
                out["atfib"][t] = float(any(abs(C[t] - (a + f * (z - a))) <= 0.15 * R[t] for f in (0.382, 0.5, 0.618)))
    return out


def cl(c, ref):
    """The reference after F's winsorizing (fe.CLIP) of column c."""
    return np.clip(ref, -fe.CLIP[c], fe.CLIP[c]) if c in fe.CLIP else ref


for k in fe.SWING_K:
    ref = ref_structure(H, L, C, run, R, k)
    close(f"dist_swhi_{k}", F[f"dist_swhi_{k}"], cl(f"dist_swhi_{k}", ref["dhi"]))
    close(f"dist_swlo_{k}", F[f"dist_swlo_{k}"], cl(f"dist_swlo_{k}", ref["dlo"]))
    close(f"brk_{k}", F[f"brk_{k}"], ref["brk"])
    close(f"struct_{k}", F[f"struct_{k}"], ref["struct"])
    close(f"fibpos_{k}", F[f"fibpos_{k}"], cl(f"fibpos_{k}", ref["fib"]))
    close(f"atfib_{k}", F[f"atfib_{k}"], ref["atfib"])
check("brk_5 fires both ways and is rare", (F.brk_5 == 1).sum() > 5 and (F.brk_5 == -1).sum() > 5
      and (F.brk_5 != 0).mean() < 0.2)

ctx = sg.context(b[["O", "H", "L", "C", "V", "inst", "sess", "vwap", "seg", "run"]], tick=tick)
e8, e20, e50 = (ctx[c].to_numpy() for c in ("ema8", "ema20", "ema50"))
m14 = ctx.mom14.to_numpy()
ref = {c: np.full(n, np.nan) for c in ("stack", "slope", "share", "mslope", "mx", "volrel")}
side, cur = 0.0, None                          # side of the last mom14 != 100 before t in the run (0 = none yet)
for t in range(n):
    if run[t] != cur:
        side, cur = 0.0, run[t]
    if np.isfinite(e50[t]):
        ref["stack"][t] = 1.0 if e8[t] > e20[t] > e50[t] else -1.0 if e8[t] < e20[t] < e50[t] else 0.0
    if t >= 10 and run[t - 10] == run[t]:
        ref["slope"][t] = (e20[t] - e20[t - 10]) / R[t]
    if t >= 19 and np.all(np.isfinite(e20[t - 19:t + 1])):
        ref["share"][t] = 2 * np.mean(C[t - 19:t + 1] > e20[t - 19:t + 1]) - 1
    if t >= 3 and run[t - 3] == run[t]:
        ref["mslope"][t] = m14[t] - m14[t - 3]
    if t >= 1 and run[t - 1] == run[t] and np.isfinite(m14[t]) and np.isfinite(m14[t - 1]):
        ref["mx"][t] = 1.0 if (m14[t] > 100 and side <= 0) else -1.0 if (m14[t] < 100 and side >= 0) else 0.0
    if np.isfinite(m14[t]) and m14[t] != 100:
        side = float(np.sign(m14[t] - 100))
    if t >= 20 and run[t - 20] == run[t] and V[t - 20:t].mean() > 0:
        ref["volrel"][t] = V[t] / V[t - 20:t].mean()
close("ema_stack", F.ema_stack, ref["stack"])
close("ema20_slope", F.ema20_slope, cl("ema20_slope", ref["slope"]))
close("above_ema20_share", F.above_ema20_share, ref["share"])
close("dist_ema20", F.dist_ema20, cl("dist_ema20", (C - e20) / R))
close("mom", F.mom, m14 - 100)
close("mom_slope3", F.mom_slope3, ref["mslope"])
close("mom_x100", F.mom_x100, ref["mx"])
close("vol_rel", F.vol_rel, cl("vol_rel", ref["volrel"]))
close("dist_vwap", F.dist_vwap, cl("dist_vwap", (C - b.vwap.to_numpy()) / R))
close("rng_rel", F.rng_rel, cl("rng_rel", (H - L) / R))
close("clv", F.clv, np.where(H > L, 2 * (C - L) / np.where(H > L, H - L, 1) - 1, 0))

# session features
gap = np.full(n, np.nan); drr = np.full(n, np.nan); dret = np.full(n, np.nan)
seg_ids = list(dict.fromkeys(seg))
seg_rng = {s: H[seg == s].max() - L[seg == s].min() for s in seg_ids}
f = 0
for t in range(n):
    if t > 0 and seg[t] != seg[t - 1]:
        f = t
    if f > 0 and run[f - 1] == run[f]:
        gap[t] = (O[f] - C[f - 1]) / R[f]
    i = seg_ids.index(seg[t])
    if i >= 20:
        drr[t] = (H[f:t + 1].max() - L[f:t + 1].min()) / np.mean([seg_rng[s] for s in seg_ids[i - 20:i]])
    dret[t] = (C[t] - O[f]) / R[t]
close("gap_open", F.gap_open, cl("gap_open", gap))
close("day_range_rel", F.day_range_rel, cl("day_range_rel", drr))
close("day_ret", F.day_ret, cl("day_ret", dret))

# 60-min mapping
rl.bars_1m = lambda s: SRC[s].copy()
b60 = sg.bars("ES", 60)
rl.bars_1m = _orig_bars_1m
c60 = sg.context(b60, tick=tick)
st60 = ref_structure(*(b60[x].to_numpy(np.float64) for x in "HLC"), b60.run.to_numpy(), np.ones(len(b60)), 5)["struct"]
h_ref = np.full((n, 3), np.nan)
close60 = b60.index + pd.Timedelta(minutes=60)
for t in range(n):
    ok = np.flatnonzero((b60.inst.to_numpy() == inst[t]) & (close60 <= idx[t] + pd.Timedelta(minutes=15)))
    if len(ok):
        j = ok[-1]
        h_ref[t] = [c60.trend.iloc[j] if np.isfinite(c60.ema50.iloc[j]) else np.nan, c60.mom14.iloc[j] - 100, st60[j]]
close("h1_ema_stack", F.h1_ema_stack, h_ref[:, 0])
close("h1_mom", F.h1_mom, h_ref[:, 1])
close("h1_struct_5", F.h1_struct_5, h_ref[:, 2])
for hhmm, src in (("10:15", "09:00"), ("10:45", "10:00"), ("09:45", "09:00"), ("10:00", "09:00")):
    t = idx.get_loc(pd.Timestamp(f"2023-03-02 {hhmm}"))
    j = b60.index.get_loc(pd.Timestamp(f"2023-03-02 {src}"))
    check(f"15-min bar {hhmm} uses the 60-min bar {src} (the last one closed by {hhmm}+15)",
          np.isclose(F.h1_mom.iloc[t], c60.mom14.iloc[j] - 100, atol=1e-4))

# cross-market
bN = BASE[("NQ", 15)][0]
pos = {ts: i for i, ts in enumerate(bN.index)}
xr = np.full(n, np.nan); xs = np.full(n, np.nan)
cN = sg.context(bN[["O", "H", "L", "C", "V", "inst", "sess", "vwap", "seg", "run"]], tick=tick)
for t in range(n):
    i = pos.get(idx[t])
    if i is not None:
        xr[t] = (bN.C.iloc[i] - bN.O.iloc[i]) / bN.R20.iloc[i]
        xs[t] = cN.trend.iloc[i] if np.isfinite(cN.ema50.iloc[i]) else np.nan
close("x_NQ_ret", F.x_NQ_ret, cl("x_NQ_ret", xr))
close("x_NQ_ema_stack", F.x_NQ_ema_stack, xs)
bY, FY = BASE[("YM", 15)]
check("YM frame has x_ES_ and x_NQ_ columns, not x_YM_", {"x_ES_ret", "x_NQ_ret"} <= set(FY.columns)
      and "x_YM_ret" not in FY.columns)

# patterns and families
P = sg.patterns(b[["O", "H", "L", "C", "V", "inst", "sess", "vwap", "seg", "run"]], ctx, tick=tick)
check("pat_ columns equal signals.patterns", all(np.array_equal(F[f"pat_{p}"].to_numpy(), P[p].to_numpy())
                                                  for p in fe.DIRECTIONAL + fe.NEUTRAL))
check("fam_reversal = clip(sum of members)", np.array_equal(
    F.fam_reversal.to_numpy(), np.clip(P[fe.FAMILIES["reversal"]].sum(axis=1).to_numpy(), -1, 1).astype(np.float32)))

# --------------------------------------------------------------------------------------------- 3. hand-made
print("== hand-made checks")


def frame(rows, seg=None, run=None, start="2024-01-02 10:00"):
    a = np.array(rows, float)
    ix = pd.date_range(start, periods=len(a), freq="15min")
    bb = pd.DataFrame({"O": a[:, 0], "H": a[:, 1], "L": a[:, 2], "C": a[:, 3], "V": 100.0, "inst": 1,
                       "sess": pd.Timestamp(start).normalize(), "vwap": a[:, 3]}, index=ix)
    bb["seg"] = 1 if seg is None else seg
    bb["run"] = 1 if run is None else run
    return bb


# R20: ranges 1, 2, 3, ... -> R20 at bar 20 = mean(1..20) = 10.5; zero ranges -> 2-tick floor; run break -> NaN
rows = [(100, 100 + (i + 1) / 2, 100 - (i + 1) / 2, 100) for i in range(25)]
Rh = fe.r20(frame(rows), 0.25)
check("R20 = mean range of the 20 bars before (bar 20 -> 10.5, bar 24 -> 14.5), NaN before",
      np.isnan(Rh[:20]).all() and Rh[20] == 10.5 and Rh[24] == 14.5)
check("R20 floor 2 ticks", fe.r20(frame([(100, 100, 100, 100)] * 22), 0.25)[21] == 0.5)
check("R20 NaN for 20 bars after a contract roll",
      np.isnan(fe.r20(frame(rows + rows, run=np.r_[np.ones(25), 2 * np.ones(25)]), 0.25)[25:45]).all())

# swing high break (k = 5): flat 101/99 bars, a spike to 110 at bar 25, back to flat, then closes 108, 111, 112, 105, 111
flat = [(100, 101, 99, 100)] * 25
rows = flat + [(100, 110, 99.5, 100)] + [(100, 101, 99, 100)] * 5 + [(100, 108.5, 99.5, 108), (108, 111.5, 107, 111),
                                                                     (111, 112.5, 110, 112), (112, 112, 104, 105),
                                                                     (105, 111.5, 104.5, 111)]
bh = frame(rows)
Rb = fe.r20(bh, 0.25)
st = fe.structure(bh, 5, Rb)
p = 25
check("swing high unknown until 5 bars after the pivot", np.isnan(st["dist_swhi_5"][p + 4])
      and np.isclose(st["dist_swhi_5"][p + 5], (100 - 110) / Rb[p + 5]))
check("brk_5 = +1 on the first close above 110 only (not the 2nd, not a re-cross)",
      list(st["brk_5"][p + 6:]) == [0, 1, 0, 0, 0])

# structure / fib on a zigzag: vertices 100 -> 110 -> 104 -> 114 -> 108 -> 118 (rising highs and lows), 8 bars a leg
vert = [100, 110, 104, 114, 108, 118, 113]
path = np.concatenate([np.linspace(a, z, 9)[:-1] for a, z in zip(vert[:-1], vert[1:])] + [[vert[-1]]])
rows = [(c, c + 0.25, c - 0.25, c) for c in path]
bz = frame([(100, 100.25, 99.75, 100)] * 22 + rows)
stz = fe.structure(bz, 5, np.full(len(bz), 1.0))
t = 22 + 5 * 8 + 6                      # 6 bars after the 118 top (confirmed at +5), close on the way down to 113
cz = bz.C.iloc[t]
check("struct_5 = +1 on rising highs and lows", stz["struct_5"][t] == 1)
a0, a1 = 108 - 0.25, 118 + 0.25          # the leg runs from the swing LOW's L to the swing HIGH's H
check("fibpos_5 = (C - leg start)/(leg end - start) for the up leg L 107.75 -> H 118.25",
      np.isclose(stz["fibpos_5"][t], (cz - a0) / (a1 - a0)), f"{stz['fibpos_5'][t]} vs {(cz - a0) / (a1 - a0)}")
check("atfib_5 = 1 within 0.15 R20 of a fib level (close %.3f)" % cz,
      stz["atfib_5"][t] == float(any(abs(cz - (a0 + f * (a1 - a0))) <= 0.15 for f in fe.FIB_LEVELS)))

# session features: two sessions, the second gaps up 3 points
s1 = [(100, 101, 99, 100)] * 30
s2 = [(103, 104, 102, 103.5), (103.5, 106, 103, 105)]
bs = frame(s1 + s2, seg=np.r_[np.ones(30), 2, 2])
Rs = fe.r20(bs, 0.25)
sf = fe.session_features(bs, Rs)
check("gap_open = (first open - prior close) / R20 on every bar of the new session",
      np.allclose(sf["gap_open"][30:], 3 / 2) and np.isnan(sf["gap_open"][:30]).all())
check("day_ret = (close - session open) / R20", np.isclose(sf["day_ret"][31], (105 - 103) / 2))
bs2 = frame(s1 + s2, seg=np.r_[np.ones(30), 2, 2], run=np.r_[np.ones(30), 2, 2])
check("no gap across a contract roll", np.isnan(fe.session_features(bs2, Rs)["gap_open"][30:]).all())

# time buckets
ix = pd.DatetimeIndex(["2024-01-07 18:00", "2024-01-08 01:45", "2024-01-08 02:00", "2024-01-08 08:00",
                       "2024-01-08 09:15", "2024-01-08 09:30", "2024-01-08 10:30", "2024-01-08 14:45",
                       "2024-01-08 15:00", "2024-01-08 16:45", "2024-01-12 12:00"])
tf_ = fe.time_features(ix)
names = [next(k for k in fe.TOD if tf_[f"tod_{k}"][i] == 1) for i in range(len(ix))]
check("tod buckets", names == ["asia", "asia", "europe", "uspre", "uspre", "open", "midday", "midday", "close",
                               "close", "midday"], str(names))
check("one tod bucket per bar", np.all(sum(tf_[f"tod_{k}"] for k in fe.TOD) == 1))
check("dow: Sunday-evening session = Monday (0), Friday = 4", tf_["dow_0"][0] == 1 and tf_["dow_0"][1] == 1
      and tf_["dow_4"][-1] == 1)

# mom_x100 on a hand-made path: flat 100 for 15 bars, then 101 (cross up), 102, 99 (cross down)
rows = [(100, 100.5, 99.5, 100)] * 15 + [(100, 101, 100, 101), (101, 102, 101, 102)] + [(100, 100, 98, 99)] * 15
bm = frame(rows)
Fm = fe.compute_features(bm, sg.context(bm), sg.patterns(bm, sg.context(bm)), 15, 0.25)
x = Fm.mom_x100.to_numpy()
check("mom_x100: NaN in warm-up, +1 on the cross above 100, -1 on the cross below",
      np.isnan(x[:15]).all() and x[15] == 1 and x[16] == 0 and x[17] == -1)
check("compute_features without 60-min / other markets: h1_ NaN, no x_ columns",
      Fm.h1_mom.isna().all() and not any(c.startswith("x_") for c in Fm.columns))

# orient: SIGNED x d, and for shorts the MIRROR pair swapped. REGRESSION for review finding "walkforward.py and
# features.py orient shorts differently" (walkforward used to multiply by d only): both modules must give one frame.
G = fe.orient(F, -1)
sc = [c for c in fe.SIGNED if c in F.columns and c not in fe.MIRROR and c not in fe.MIRROR.values()]
uc = [c for c in F.columns if c not in fe.SIGNED]
check("orient(-1): plain signed columns negated", np.array_equal(G[sc].to_numpy(), -F[sc].to_numpy(), equal_nan=True))
check("orient(-1): unsigned columns unchanged", np.array_equal(G[uc].to_numpy(), F[uc].to_numpy(), equal_nan=True))
check("orient(-1): dist_swhi <- -dist_swlo and dist_swlo <- -dist_swhi (k = 5, 10)",
      all(np.array_equal(G[a].to_numpy(), -F[c].to_numpy(), equal_nan=True)
          and np.array_equal(G[c].to_numpy(), -F[a].to_numpy(), equal_nan=True) for a, c in fe.MIRROR.items())
      and set(fe.MIRROR) == {"dist_swhi_5", "dist_swhi_10"})
check("orient(+1) = F and orient twice with -1 = F", fe.orient(F, 1).equals(F) and fe.orient(G, -1).equals(F))
d = np.where(np.arange(n) % 2 == 0, 1, -1)
Gd = fe.orient(F, d)
check("orient with a per-row direction", Gd.iloc[::2].equals(F.iloc[::2]) and Gd.iloc[1::2].equals(G.iloc[1::2]))
try:
    import inspect
    import walkforward as wf
    wf_err = None
except Exception as e:                          # walkforward.py is built in parallel; a broken import is a FAIL here
    wf_err = repr(e)
check("import walkforward", wf_err is None, str(wf_err))
if wf_err is None:
    same = True
    for dd in (-np.ones(n), np.ones(n), d.astype(float), np.random.default_rng(3).choice([-1.0, 1.0], n)):
        W = wf.orient(F, dd, wf.default_signed(), wf.default_mirror())
        same &= list(W.columns) == list(F.columns) and np.array_equal(
            W.to_numpy(np.float32), fe.orient(F, dd).to_numpy(np.float32), equal_nan=True)
    check("REGRESSION one convention: walkforward.orient(F, d, default_signed(), default_mirror()) == "
          "features.orient(F, d) (all short, all long, alternating, random d)", same)
    check("walkforward's defaults are features.SIGNED / features.MIRROR, walk_forward(mirror='auto') by default",
          list(wf.default_signed()) == list(fe.SIGNED) and wf.default_mirror() == fe.MIRROR
          and inspect.signature(wf.walk_forward).parameters["mirror"].default == "auto")
    # end to end through walkforward's own preparation step (the reviewer's failure point: _prepare -> orient)
    ev = F.copy()
    ev["t"] = F.index
    ev["d"] = np.where(np.arange(n) % 3 == 0, 1, -1)
    ev["market"] = "ES"
    ev["y_1.5"] = (np.arange(n) % 2).astype(float)
    ev["pnl_usd_1.5"] = 1.0
    ev["t_end_1.5"] = F.index + pd.Timedelta(minutes=60)
    try:
        S = wf._prepare(ev, list(F.columns), "entry", "y_1.5", "pnl_usd_1.5", "t_end_1.5", None, False, "trade",
                        None, "auto")
        Xo, err = S["Xo"], ""
    except Exception as e:
        Xo, err = None, repr(e)
    if Xo is not None:
        want = fe.orient(F.loc[S["df"].index], S["df"]["d"].to_numpy())
        r0 = np.flatnonzero(S["df"]["d"].to_numpy() < 0)[200:203]
        err = (f"rows {r0}: wf dist_swhi_5 {Xo.dist_swhi_5.to_numpy()[r0]} vs features "
               f"{want.dist_swhi_5.to_numpy()[r0]}")
    check("REGRESSION walkforward._prepare orients every column exactly as features.orient (shorts' dist_swhi_k "
          "= -dist_swlo_k)", Xo is not None and Xo.index.equals(want.index)
          and np.array_equal(Xo.to_numpy(np.float32), want.to_numpy(np.float32), equal_nan=True), err)

# MIRROR TEST on the full compute_features output (60-min and cross-market inputs mirrored too): prices p -> K - p.
# The module docstring promises: orient(F of the mirrored chart, -1) equals F column by column (the MIRROR pair
# included), except the one-sided pattern PARTNER pairs (equal to F's partner column) and the ratio-based mom /
# mom_slope3 / h1_mom (no exact relation; mom keeps its sign).
# (REGRESSION, review findings "fibpos tie breaks antisymmetry" and "docstring claims more than the code delivers")
RAW = ["O", "H", "L", "C", "V", "inst", "sess", "vwap", "seg", "run"]
KM = 40000.0                                    # multiple of every tick, above every 2023 price -> exact, positive


def mirror(x):
    m = x[RAW].copy()
    m["O"], m["C"], m["vwap"] = KM - x.O, KM - x.C, KM - x.vwap
    m["H"], m["L"] = KM - x.L, KM - x.H
    return m


def compute_from(bars, b60_, others):
    """compute_features(ES bars, 60-min ES bars, {market: bars}) the way build_features does."""
    cx = sg.context(bars, tick=tick)
    xm = {m: (bo, sg.context(bo, tick=sg.SPEC[m]["tick"]), fe.r20(bo, sg.SPEC[m]["tick"])) for m, bo in others.items()}
    return fe.compute_features(bars, cx, sg.patterns(bars, cx, tick=tick), 15, tick, b60_, sg.context(b60_, tick=tick),
                               xm)


raw_b60 = b60[RAW]
others = {m: BASE[(m, 15)][0][RAW] for m in ("NQ", "YM")}
F_re = compute_from(b[RAW], raw_b60, others)
check("compute_features on build_features' inputs reproduces F", F_re.equals(F))
Fm = compute_from(mirror(b[RAW]), mirror(raw_b60), {m: mirror(x) for m, x in others.items()})
Gm = fe.orient(Fm, -1)
PARTNER = {f"pat_{a}": f"pat_{z}" for a, z in (("hammer", "shooting_star"), ("inverted_hammer", "hanging_man"),
                                                ("dragonfly_doji", "gravestone_doji"), ("piercing", "dark_cloud"))}
PARTNER.update({v: k for k, v in list(PARTNER.items())})
RATIO = {"mom", "mom_slope3", "h1_mom"}
bad = []
for c in F.columns:
    if c in RATIO:
        continue
    want, got = F[PARTNER.get(c, c)].to_numpy(np.float64), Gm[c].to_numpy(np.float64)
    if not (np.array_equal(np.isnan(want), np.isnan(got))
            and np.allclose(got[~np.isnan(want)], want[~np.isnan(want)], rtol=1e-4, atol=1e-4)):
        bad.append(f"{c}: {np.mean(~np.isclose(got, want, rtol=1e-4, atol=1e-4, equal_nan=True)):.4f}")
check(f"mirror: orient(F_mirror, -1) == F (or its PARTNER column) for all {F.shape[1] - len(RATIO)} non-ratio "
      "columns", not bad, "; ".join(bad))
check("mirror: the PARTNER pairs really differ from F's own column (the docstring's exceptions are real)",
      all(not np.array_equal(Gm[c].to_numpy(), F[c].to_numpy(), equal_nan=True) for c in PARTNER))
check("mirror: mom and h1_mom keep their sign (ratios, so only the sign is antisymmetric)",
      all(np.array_equal(np.sign(Gm[c].to_numpy()), np.sign(F[c].to_numpy()), equal_nan=True)
          and not np.allclose(Gm[c].to_numpy(), F[c].to_numpy(), equal_nan=True) for c in ("mom", "h1_mom")))
Fm_plain = Fm.copy()
Fm_plain[[c for c in fe.SIGNED if c in Fm.columns]] *= -1
check("mirror: plain multiplication by d (no MIRROR swap) would break it for dist_swhi/dist_swlo",
      all(not np.allclose(Fm_plain[c].to_numpy(), F[c].to_numpy(), equal_nan=True) for c in fe.MIRROR))
lo5, hi5 = sg.pivots(b, 5)
hb5 = fe._swing_side(hi5, H, run, 5)[2]
lb5 = fe._swing_side(lo5, L, run, 5)[2]
tie = (hb5 == lb5) & (hb5 >= 0)
check(f"fibpos_5 NaN on the {int(tie.sum())} slice rows whose latest swing high and low are the same bar, "
      "atfib_5 still defined there", tie.sum() > 0 and F.fibpos_5[tie].isna().all() and F.atfib_5[tie].notna().all())

# fibpos tie, hand-made: one outside bar is both the 5-bar swing high and swing low (both close directions)
for cc in (96.0, 104.0):
    rows = [(100, 101, 99, 100)] * 25 + [(100, 105, 95, cc)] + [(100, 101, 99, 100)] * 10
    bt = frame(rows)
    stt = fe.structure(bt, 5, fe.r20(bt, 0.25))
    check(f"fibpos_5 NaN when the same bar (close {cc}) is the latest swing high and low; atfib_5 defined",
          np.isnan(stt["fibpos_5"][30:]).all() and np.isfinite(stt["dist_swhi_5"][30:]).all()
          and np.isfinite(stt["atfib_5"][30:]).all())

# mom_x100 touch-and-return (REGRESSION, review finding "mom_x100 counts a touch of exactly 100 as a cross"):
# closes 100 x 15, then mom14 = close for bars 15..28: 101 100 101 100 99 100 99 100 101 102 100 100 99 98
path = [100.0] * 15 + [101, 100, 101, 100, 99, 100, 99, 100, 101, 102, 100, 100, 99, 98]
bt = frame([(c, c + 0.5, c - 0.5, c) for c in path])
ct = sg.context(bt)
check("hand path: mom14 equals the planned values", np.allclose(ct.mom14.to_numpy()[14:], [100.0] + path[15:]))
xt = fe.compute_features(bt, ct, sg.patterns(bt, ct), 15, 0.25).mom_x100.to_numpy()
exp = [np.nan, 1, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, -1, 0]
check("mom_x100: 101->100->101 and 99->100->99 are no cross, 101->100->99 and 99->100->101 are",
      np.array_equal(xt[14:], exp, equal_nan=True), str(list(xt[14:])))
xr_ = fe.mom_cross_100(np.array([99, 100, 101, np.nan, 100, 101.0]), np.array([1, 1, 1, 2, 2, 2]))
check("mom_cross_100: the side does not carry over a contract roll (new run: 100 -> 101 is a cross again)",
      np.array_equal(xr_, [np.nan, 0, 1, np.nan, np.nan, 1], equal_nan=True), str(xr_))

# winsorizing (REGRESSION, review finding "heavy unclipped tails from R20 hitting its 2-tick floor"): 25 locked flat
# bars (R20 = 2-tick floor 0.5) then a 40-point drop: raw day_ret -80, rng_rel 80 -> F clips them to -50 / 50
rows = [(100, 100, 100, 100)] * 25 + [(100, 100, 60, 60)]
bl = frame(rows)
cxl = sg.context(bl)
Fl = fe.compute_features(bl, cxl, sg.patterns(bl, cxl), 15, 0.25)
raw_l = fe.session_features(bl, fe.r20(bl, 0.25))
check("R20 at its floor -> raw day_ret -80; F.day_ret = -50, F.rng_rel = 50, F.dist_ema8 = -50 (clipped)",
      raw_l["day_ret"][-1] == -80 and Fl.day_ret.iloc[-1] == -50 and Fl.rng_rel.iloc[-1] == 50
      and Fl.dist_vwap.iloc[-1] == 0 and Fl.dist_ema8.iloc[-1] == -50, str(Fl.iloc[-1][["day_ret", "rng_rel"]]))
check("winsorizing keeps NaN (day_range_rel without 20 prior sessions)", Fl.day_range_rel.isna().all())
check("CLIP bounds are symmetric (mirror-safe) and cover every R20-unit / ratio column",
      set(fe.CLIP) >= {f"{c}_{k}" for k in fe.SWING_K for c in ("dist_swhi", "dist_swlo", "fibpos")}
      | {"dist_ema8", "dist_ema20", "dist_ema50", "dist_vwap", "ema20_slope", "day_ret", "gap_open", "rng_rel",
         "vol_rel", "day_range_rel"} | {f"x_{m}_ret" for m in fe.MARKETS})

# column list / dtypes
check("columns = COLUMNS(sym), 80 for ES", list(F.columns) == fe.COLUMNS("ES") and F.shape[1] == 80)
check("all float32, index = b.index", all(F.dtypes == np.float32) and F.index.equals(b.index))
check("SIGNED covers every signed column of all three markets",
      set(fe.SIGNED) >= {c for s in fe.MARKETS for c in fe.COLUMNS(s) if c not in uc})
check("24 directional pattern columns + 4 neutral", len(fe.DIRECTIONAL) == 24 and len(fe.NEUTRAL) == 4)

# --------------------------------------------------------------------------------------------- timing
print("== timing (full history)")
fe.clear_cache()
t0 = time.time()
FULL = {}
for s in fe.MARKETS:
    t1 = time.time()
    FULL[s] = fe.build_features(s, 15)
    print(f"   {s}: {len(FULL[s][1])} rows x {FULL[s][1].shape[1]} cols in {time.time() - t1:.1f}s")
check("all three markets in < 60 s", time.time() - t0 < 60, f"{time.time() - t0:.1f}s")
print(f"   total {time.time() - t0:.1f}s")

print("== full-history regression checks (review findings)")
for s, (bb, FF) in FULL.items():
    over = {c: float(np.nanmax(np.abs(FF[c]))) for c in fe.CLIP if c in FF.columns
            if np.nanmax(np.abs(FF[c])) > fe.CLIP[c]}
    at = max(float((np.abs(FF[c]) >= fe.CLIP[c]).mean()) for c in fe.CLIP if c in FF.columns and c[:6] != "fibpos")
    check(f"{s}: every CLIP column within its bound; R20-unit columns at the bound on <= 0.2% of rows ({at:.5f})",
          not over and at <= 0.002, str(over))
    m = bb.mom14
    prev = np.sign(m - 100).replace(0, np.nan).groupby(bb.run).ffill().groupby(bb.run).shift(1)   # independent
    x = FF.mom_x100
    touch = int(((x == 1) & (prev == 1)).sum() + ((x == -1) & (prev == -1)).sum())
    mp = m.groupby(bb.run).shift(1)
    missed = int((((m > 100) & (mp < 100)) & (x != 1)).sum() + (((m < 100) & (mp > 100)) & (x != -1)).sum())
    check(f"{s}: mom_x100 has no touch-and-return events and keeps every direct cross "
          f"({int((x != 0).sum() - x.isna().sum())} crosses)", touch == 0 and missed == 0, f"{touch} {missed}")
bE_, FE_ = FULL["ES"]
for k in fe.SWING_K:
    lo_, hi_ = sg.pivots(bE_, k)
    rE = bE_.run.to_numpy()
    hb_ = fe._swing_side(hi_, bE_.H.to_numpy(np.float64), rE, k)[2]
    lb_ = fe._swing_side(lo_, bE_.L.to_numpy(np.float64), rE, k)[2]
    tie = (hb_ == lb_) & (hb_ >= 0)
    check(f"ES full: fibpos_{k} NaN on all {int(tie.sum())} rows whose latest swing high and low are one bar",
          tie.sum() > 100 and FE_[f"fibpos_{k}"][tie].isna().all())
row = lambda s, ts: FULL[s][1].loc[pd.Timestamp(ts, tz=FULL[s][1].index.tz)]    # noqa: E731
check("ES 2022-01-07 09:45 (8:30 NFP bar is both swing pivots): fibpos_5 NaN (was -0.24)",
      np.isnan(row("ES", "2022-01-07 09:45").fibpos_5))
check("ES 2010-06-08 03:30 (mom14 100.047 -> 100.0 -> 100.189): mom_x100 = 0 (was +1)",
      row("ES", "2010-06-08 03:30").mom_x100 == 0 and row("ES", "2010-06-08 03:15").mom_x100 == 0)
r_nq = row("NQ", "2020-03-16 09:45")
check("NQ 2020-03-16 09:45 (limit-locked, R20 at the 2-tick floor): dist_swhi_5 / day_ret / rng_rel clipped to "
      "-50 / -50 / 50 (were -1473.5 / -1323.5 / 577), b.R20 itself unchanged (0.5)",
      r_nq.dist_swhi_5 == -50 and r_nq.day_ret == -50 and r_nq.rng_rel == 50
      and FULL["NQ"][0].R20.loc[r_nq.name] == 0.5)

print("ALL PASS" if ok_all else "SOME FAILED")
sys.exit(0 if ok_all else 1)
