"""
Swing-point detection data for different swing sizes k (bars on EACH side). One market and timeframe per run.
  PYTHONPATH=../../pylib:../..:. python3 swing_study.py ES 15
For each k: swings per day, swing size (move from a swing low to the next swing high and back, in points), how long
until a swing is confirmed (k bars), and what happened when price later came back to the swing level: bounce (moved
1 ATR away in the swing's direction first) or break (closed 0.25 ATR beyond the level first), within 20 bars. The same
revisit test on RANDOM bars' lows/highs is given for comparison. Writes out/swings_{SYM}_{TF}.csv.
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import signals as sg

warnings.filterwarnings("ignore")
SYM, TF = sys.argv[1], int(sys.argv[2])
KS = (2, 3, 5, 8, 10, 15, 20)
WIN, LOOK = 20, 200            # bars to resolve bounce/break after a revisit; bars to wait for a revisit
t0 = time.time()
spec = sg.SPEC[SYM]
b = sg.bars(SYM, TF)
c = sg.context(b, tick=spec["tick"])
H, L, C = b.H.to_numpy(), b.L.to_numpy(), b.C.to_numpy()
run = b.run.to_numpy(); atr = c.atr14.to_numpy()
n = len(b)
days = b.sess.nunique()
rng = np.random.default_rng(12345)


def revisit(levels_at, side):
    """levels_at: array of (pivot index p, known-from index t0). side=+1 swing low (support), -1 swing high.
    Returns outcome counts: revisited, bounce, break, unresolved."""
    out = {"revisited": 0, "bounce": 0, "break": 0, "unresolved": 0, "n": 0}
    for p, t0 in levels_at:
        if t0 >= n - 1 or not np.isfinite(atr[t0]):
            continue
        out["n"] += 1
        lvl, a = (L[p] if side > 0 else H[p]), atr[t0]
        end = min(n, t0 + 1 + LOOK)
        seg = slice(t0 + 1, end)
        same = run[seg] == run[p]
        zone = (L[seg] <= lvl + 0.25 * a) if side > 0 else (H[seg] >= lvl - 0.25 * a)
        hit = np.flatnonzero(zone & same)
        if not len(hit):
            continue
        t1 = t0 + 1 + hit[0]
        out["revisited"] += 1
        e2 = min(n, t1 + WIN)
        s2 = slice(t1, e2)
        ok = run[s2] == run[p]
        if side > 0:
            bnc = np.flatnonzero((H[s2] >= lvl + 1.0 * a) & ok)
            brk = np.flatnonzero((C[s2] < lvl - 0.25 * a) & ok)
        else:
            bnc = np.flatnonzero((L[s2] <= lvl - 1.0 * a) & ok)
            brk = np.flatnonzero((C[s2] > lvl + 0.25 * a) & ok)
        fb = bnc[0] if len(bnc) else 10 ** 9
        fk = brk[0] if len(brk) else 10 ** 9
        if fb == fk == 10 ** 9:
            out["unresolved"] += 1
        elif fb < fk:
            out["bounce"] += 1
        else:
            out["break"] += 1
    return out


rows = []
for k in KS:
    lo, hi = sg.pivots(b, k)
    plo, phi = np.flatnonzero(lo), np.flatnonzero(hi)
    # swing size: alternate lows and highs in time order, size = |price move| between consecutive opposite swings
    ev = sorted([(p, -1, L[p]) for p in plo] + [(p, 1, H[p]) for p in phi])
    sizes, gaps = [], []
    for (p1, s1, v1), (p2, s2, v2) in zip(ev, ev[1:]):
        if s1 != s2 and run[p1] == run[p2]:
            sizes.append(abs(v2 - v1)); gaps.append(p2 - p1)
    sizes = np.array(sizes)
    out_lo = revisit([(p, p + k) for p in plo], +1)
    out_hi = revisit([(p, p + k) for p in phi], -1)
    m = len(plo) + len(phi)
    # random comparison: the same number of random bars, their low (as support) / high (as resistance), same delay k
    rp = rng.choice(np.arange(k, n - k), size=min(m, 20000), replace=False)
    half = len(rp) // 2
    r_lo = revisit([(p, p + k) for p in rp[:half] if run[p] == run[min(p + k, n - 1)]], +1)
    r_hi = revisit([(p, p + k) for p in rp[half:] if run[p] == run[min(p + k, n - 1)]], -1)
    def rates(o1, o2):
        rv = o1["revisited"] + o2["revisited"]; nn = o1["n"] + o2["n"]
        res = o1["bounce"] + o1["break"] + o2["bounce"] + o2["break"]
        return (rv / nn if nn else np.nan, (o1["bounce"] + o2["bounce"]) / res if res else np.nan,
                (o1["unresolved"] + o2["unresolved"]) / rv if rv else np.nan)
    rev, hold, unres = rates(out_lo, out_hi)
    rrev, rhold, runres = rates(r_lo, r_hi)
    rows.append(dict(market=SYM, tf=TF, k=k, confirm_delay_min=k * TF, swings_per_day=m / days,
                     swing_lows=len(plo), swing_highs=len(phi),
                     size_median_pts=np.median(sizes) if len(sizes) else np.nan,
                     size_p25_pts=np.percentile(sizes, 25) if len(sizes) else np.nan,
                     size_p75_pts=np.percentile(sizes, 75) if len(sizes) else np.nan,
                     size_median_2022_26_pts=np.nan, bars_between_median=np.median(gaps) if gaps else np.nan,
                     revisit_rate=rev, bounce_rate=hold, unresolved_share=unres,
                     random_revisit_rate=rrev, random_bounce_rate=rhold))
    late = [s for (p1, s1, v1), (p2, s2, v2), s in zip(ev, ev[1:], [None] * len(ev))] if False else None
    # recent swing size (2022-26) in points, closer to today's price level
    idx = b.index
    recent = [abs(v2 - v1) for (p1, s1, v1), (p2, s2, v2) in zip(ev, ev[1:])
              if s1 != s2 and run[p1] == run[p2] and idx[p1].year >= 2022]
    rows[-1]["size_median_2022_26_pts"] = np.median(recent) if recent else np.nan
    print(f"  k={k:2d}: {m / days:6.2f} swings/day, median size {rows[-1]['size_median_pts']:.2f} pts, "
          f"bounce {hold:.0%} vs random {rhold:.0%}", flush=True)
pd.DataFrame(rows).to_csv(f"out/swings_{SYM}_{TF}.csv", index=False)
print(f"{SYM} {TF}m swing study done in {time.time() - t0:.0f}s", flush=True)
