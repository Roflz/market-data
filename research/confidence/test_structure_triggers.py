"""Hand-made bar checks for structure_triggers.detect (k=2 swings, tick 0.25) + no-look-ahead perturbation test +
a label_entries integration check."""
import numpy as np
import pandas as pd

import labels as lb
import structure_triggers as st

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)

TICK = 0.25
def frame(hlc, start="2024-03-05 09:30", freq="5min"):
    a = np.asarray(hlc, float)
    idx = pd.date_range(start, periods=len(a), freq=freq)
    return pd.DataFrame(dict(O=a[:, 2], H=a[:, 0], L=a[:, 1], C=a[:, 2], seg=1, run=1, inst=1,
                             sess=idx.normalize()), index=idx)
def mirror(hlc):
    return [(-l, -h, -c) for h, l, c in hlc]
def ev_list(ev):
    return [(int(r.i), int(r.d), r.trigger, round(float(r.stop), 9)) for r in ev.itertuples()]
def det(hlc, k=2):
    return st.detect(frame(hlc), tick=TICK, tf=5, k=k)

# uptrend: swing lows 8 (bar 2), 9 (bar 6), 10.5 (bar 10); swing highs 12 (bar 4), 13 (bar 8)
UP = [(11, 9.5, 10), (10.5, 9, 9.5), (10, 8, 9), (11, 9, 10.5), (12, 10, 11), (11, 9.5, 10), (10.5, 9, 10),
      (12, 10, 11.5), (13, 11, 12), (12.5, 11, 11.5), (12, 10.5, 11)]

# ---- (a) BOS
A = UP + [(12.8, 11, 12.5), (13.5, 12, 13.2), (14, 13, 13.8), (14.2, 13.5, 14)]
ev = det(A)
check("BOS: one long at bar 12 (first close above the 13 swing high), stop = swing low 10.5 - 1 tick",
      ev_list(ev) == [(12, 1, "bos", 10.25)])
check("BOS: second close above the same high (bar 13) does not re-trigger", (ev.i == 13).sum() == 0)
check("events frame for label_entries: patterns [] and n_patterns 0",
      ev.patterns.iloc[0] == [] and ev.n_patterns.iloc[0] == 0 and ev.t.iloc[0] == frame(A).index[12])
evm = det(mirror(A))
check("BOS short mirror: short at bar 12, stop = swing high -10.5 + 1 tick", ev_list(evm) == [(12, -1, "bos", -10.25)])
# confirmation delay: the break comes at bar 11, the bar-10 swing low (10.5) is NOT known until bar 12's close,
# so the stop must use the swing low known at bar 11 (9 at bar 6)
A2 = UP + [(13.5, 11, 13.2), (14, 12.5, 13.8), (14.2, 13.5, 14)]
check("BOS no look-ahead: break before the next swing low is confirmed uses the older low (9 - tick)",
      ev_list(det(A2)) == [(11, 1, "bos", 8.75)])
check("BOS no look-ahead (short mirror)", ev_list(det(mirror(A2))) == [(11, -1, "bos", -8.75)])

# ---- (b) CHoCH: mirrored uptrend = downtrend (swing highs -8 @2, -9 @6; swing lows -12 @4, -13 @8), then bar 11
# closes above the latest confirmed swing high (-9) -> long; stop = lowest low since bar 6 (-13 @ bar 8) - tick
B = mirror(UP) + [(-8.5, -11, -8.8), (-8, -9, -8.2)]
ev = det(B)
check("CHoCH: one long at bar 11, stop = lowest low since the swing high - 1 tick",
      ev_list(ev) == [(11, 1, "choch", -13.25)])
check("CHoCH short mirror", ev_list(det(mirror(B))) == [(11, -1, "choch", 13.25)])
# no trend (swing highs rising, lows falling): a close above the swing high is neither BOS nor CHoCH
# raise the bar-6 swing high above the bar-2 one (higher high) while the lows keep falling
By = [list(x) for x in B]; By[6] = [-7.5, -10.5, -10]; By[5] = [-9.6, -12, -10]; By[7] = [-9.5, -13, -11.5]
evy = det([tuple(x) for x in By])
check("mixed structure (higher high, lower low): no BOS/CHoCH", (evy.trigger.isin(["bos", "choch"])).sum() == 0)

# ---- (c) reclaim: uptrend, the bar-6 swing low (9, confirmed at bar 8) is closed below at bar 10 and reclaimed at 12
C_ = UP[:10] + [(11, 8.5, 8.8), (9.5, 8.2, 8.6), (10, 8.4, 9.5), (10.2, 9.4, 10)]
ev = det(C_)
check("reclaim: long at bar 12, stop = excursion low 8.2 - tick; the bar-10 close below the swing low in an "
      "uptrend is a CHoCH short (stop = highest high since the swing low 13 + tick)",
      ev_list(ev) == [(10, -1, "choch", 13.25), (12, 1, "reclaim", 7.95)])
check("reclaim short mirror", ev_list(det(mirror(C_))) == [(10, 1, "choch", -13.25), (12, -1, "reclaim", -7.95)])
def reclaim_after(n_below):
    """close below the 9 level at bar 10, stay below for n_below bars in total, then close above."""
    path = UP[:10] + [(11, 8.5, 8.8)] + [(9, 8.4 - 0.01 * j, 8.7) for j in range(n_below - 1)] + [(10, 8.6, 9.5),
                                                                                                 (10.2, 9.4, 10)]
    e = det(path)
    return e[e.trigger == "reclaim"]
r5, r6 = reclaim_after(5), reclaim_after(6)
check("reclaim 5 bars after the breakdown counts (t - j0 = 5)", r5.i.tolist() == [15])
check("reclaim 6 bars after the breakdown does not (the breakdown held)", len(r6) == 0)
r5m = det(mirror(UP[:10] + [(11, 8.5, 8.8)] + [(9, 8.4 - 0.01 * j, 8.7) for j in range(4)] + [(10, 8.6, 9.5),
                                                                                                (10.2, 9.4, 10)]))
check("reclaim window mirror", r5m[r5m.trigger == "reclaim"].i.tolist() == [15])

# ---- no look-ahead: perturb every bar after t, events with i <= t must be identical (k=5, random walk)
rng = np.random.default_rng(1)
n = 1500
c = 100 + np.cumsum(rng.normal(0, 1, n))
h = c + rng.uniform(0, 1.5, n); l = c - rng.uniform(0, 1.5, n)
cc = l + (h - l) * rng.uniform(0, 1, n)
base = frame(np.c_[np.round(h * 4) / 4, np.round(l * 4) / 4, np.round(cc * 4) / 4], start="2024-03-04 18:00",
             freq="1min")                                     # 1-min spacing: one segment, nothing in the 16:45 tail
base["run"] = np.r_[np.ones(800, int), 2 * np.ones(n - 800, int)]     # a contract roll at bar 800
base["seg"] = base["run"]
E = st.detect(base, tick=TICK, tf=1, k=5)
check("random walk produces all three triggers in both directions",
      set(zip(E.trigger, E.d)) == {(x, d) for x in st.TRIGGERS for d in (1, -1)})
same = True
for t in (300, 650, 799, 805, 1200):
    p = base.copy()
    m = len(p) - t - 1
    shift = rng.normal(0, 3, m).cumsum()
    for col in "OHLC":
        p.iloc[t + 1:, p.columns.get_loc(col)] += shift
    p.iloc[t + 1:, p.columns.get_loc("H")] += rng.uniform(0, 2, m)
    Ep = st.detect(p, tick=TICK, tf=1, k=5)
    a = E[E.i <= t].drop(columns="patterns").reset_index(drop=True)
    bq = Ep[Ep.i <= t].drop(columns="patterns").reset_index(drop=True)
    same &= a.equals(bq) and len(a) > 0
check("perturbing bars after t never changes events at bars <= t", same)
# truncation: the events at bar t computed from bars 0..t only (the future does not exist) equal the full-run ones
H_, L_, C_r = (base[x].to_numpy(np.float64) for x in "HLC"); run_ = base.run.to_numpy()
full = {}
for i_, trg, stp, lvl, age in st._scan_long(H_, L_, C_r, run_, 5, TICK):
    full.setdefault(i_, []).append((trg, stp))
trunc_ok = True
for t in range(20, n, 7):
    ev_t = [(trg, stp) for i_, trg, stp, lvl, age in st._scan_long(H_[:t + 1], L_[:t + 1], C_r[:t + 1], run_[:t + 1],
                                                                  5, TICK) if i_ == t]
    trunc_ok &= ev_t == full.get(t, [])
check("truncation: events at bar t from data up to t only == full-history events (swing confirmation delay)",
      trunc_ok and sum(len(v) for v in full.values()) > 0)
check("no event in a new contract before its own swings exist (first bars after the roll)",
      ((E.i >= 800) & (E.i < 800 + 2 * 5 + 1)).sum() == 0)

# ---- label_entries integration: BOS at bar 12 enters at bar 13's open; 1-minute path hits the 1R target
b = frame(A)
idx1 = pd.date_range(b.index[0], periods=len(b) * 5, freq="1min")
m1 = pd.DataFrame(dict(O=13.5, H=13.6, L=13.4, C=13.5, inst=1, sess=idx1.normalize()), index=idx1)
ev = det(A)
b.loc[b.index[13], "O"] = 13.5
m1.loc[idx1[67], "H"] = 17.0                                         # bar 13's 3rd minute: +3.5 points
lab = lb.label_entries("NQ", 5, b, ev, target_R=(1.0,), max_bars=1, m1=m1)
r = lab.iloc[0]
check("label_entries: entry = next bar's open, risk = entry - stop, 1R target hit",
      r.entry == 13.5 and abs(r.risk_pts - 3.25) < 1e-9 and r["exit_kind_1"] == "target")
print("ALL PASS" if ok else "SOME FAILED")
