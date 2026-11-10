"""Hand-made bars for exits.py: timing of entries/exits, 16:45 cutoff, stops, gaps, shorts.
  PYTHONPATH=../../pylib:../..:. python3 test_exits.py"""
import numpy as np
import pandas as pd

import exits as ex


def frame(times, seg=None):
    idx = pd.DatetimeIndex(times)
    b = pd.DataFrame(index=idx)
    b["seg"] = seg if seg is not None else 1
    return b


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name


# 1. 16:45 cutoff on 5-minute bars: bars starting 16:45/16:50/16:55 take no part; forced bar = 16:40 (closes 16:45)
t = pd.date_range("2024-03-05 16:20", "2024-03-05 16:55", freq="5min").append(pd.DatetimeIndex(["2024-03-05 18:00", "2024-03-05 18:05"]))
b = frame(t, seg=[1] * 8 + [2, 2])
allowed, forced = ex.session_frame(b, 5)
check("cutoff: 16:45+ bars not allowed", list(allowed) == [True] * 5 + [False] * 3 + [True, True])
check("cutoff: forced bar is 16:40 for the whole session", all(forced[:8] == 4) and all(forced[8:] == 9))
# 60-minute bars: 15:00 bar closes 16:00 (ok), 16:00 bar closes 17:00 (not ok)
b60 = frame(pd.DatetimeIndex(["2024-03-05 14:00", "2024-03-05 15:00", "2024-03-05 16:00"]))
a60, f60 = ex.session_frame(b60, 60)
check("cutoff 60m: 16:00 bar excluded, forced = 15:00 bar", list(a60) == [True, True, False] and f60[0] == 1)
# overnight bars are allowed (session runs 18:00 -> 16:45 next day)
bo = frame(pd.DatetimeIndex(["2024-03-05 23:00", "2024-03-06 02:00", "2024-03-06 09:30"]))
check("overnight bars allowed", ex.session_frame(bo, 5)[0].all())

# 2. next_true
check("next_true", list(ex.next_true(np.array([0, 1, 0, 0, 1, 0], bool))) == [1, 1, 4, 4, 4, 6])

# synthetic prices: 10 bars, one segment, forced bar = 9
O = np.array([100, 101, 102, 103, 104, 105, 106, 107, 108, 109.0])
H = O + 1.0; L = O - 1.0; C = O + 0.5
forced = np.full(10, 9)
e = np.array([2]); d = np.array([1])
# 3. bearish exit signal at bar 5 -> long exits at O[6]
bear = np.zeros(10, bool); bear[5] = True; bull = np.zeros(10, bool)
x_end, x_px, sig = ex.plan_exits(e, d, forced, ex.next_true(bear), ex.next_true(bull), O, C)
check("long exits at next open after the opposite signal", x_end[0] == 5 and x_px[0] == O[6] and sig[0] == 1)
# 4. signal on the entry bar itself (known at its close) -> exit at the next open
bear2 = np.zeros(10, bool); bear2[2] = True
x_end, x_px, sig = ex.plan_exits(e, d, forced, ex.next_true(bear2), ex.next_true(bull), O, C)
check("signal on entry bar -> exit O[e+1]", x_end[0] == 2 and x_px[0] == O[3])
# signal BEFORE the entry bar (on the pattern bar) is ignored
bear3 = np.zeros(10, bool); bear3[1] = True
x_end, x_px, sig = ex.plan_exits(e, d, forced, ex.next_true(bear3), ex.next_true(bull), O, C)
check("signal before entry ignored -> forced exit at C[F]", x_end[0] == 9 and x_px[0] == C[9] and sig[0] == 0)
# 5. signal on the forced bar -> forced exit at its close
bear4 = np.zeros(10, bool); bear4[9] = True
x_end, x_px, sig = ex.plan_exits(e, d, forced, ex.next_true(bear4), ex.next_true(bull), O, C)
check("signal on forced bar -> C[F]", x_end[0] == 9 and x_px[0] == C[9] and sig[0] == 0)

# 6. stops
x_end, x_px = np.array([5]), np.array([O[6]])
Ls = L.copy(); Ls[4] = 95.0                     # bar 4 trades down to 95; stop 99 -> filled at 99
px, xb, st, mfe = ex.simulate(O, H, Ls, C, e, d, x_end, x_px, np.array([99.0]))
check("long stop hit inside a bar fills at the stop", st[0] and px[0] == 99.0 and xb[0] == 4)
Og = O.copy(); Og[4] = 97.0; Lg = L.copy(); Lg[4] = 96.0
px, xb, st, mfe = ex.simulate(Og, H, Lg, C, e, d, x_end, x_px, np.array([99.0]))
check("long stop gapped through fills at the open", st[0] and px[0] == 97.0)
px, xb, st, mfe = ex.simulate(O, H, L, C, e, d, x_end, x_px, np.array([99.0]))
check("stop never touched -> planned exit", (not st[0]) and px[0] == O[6])
# stop on the bar after the last held bar (the exit-fill bar) is NOT checked: trade already out at its open
Lx = L.copy(); Lx[6] = 90.0
px, xb, st, mfe = ex.simulate(O, H, Lx, C, e, d, x_end, x_px, np.array([99.0]))
check("stop not checked after the exit fill", (not st[0]) and px[0] == O[6])
# stop and exit signal on the same bar -> stop first
Ly = L.copy(); Ly[5] = 90.0
px, xb, st, mfe = ex.simulate(O, H, Ly, C, e, d, x_end, x_px, np.array([99.0]))
check("stop on the signal bar comes first", st[0] and px[0] == 99.0 and xb[0] == 5)
# entry open already beyond the stop -> out at the entry open
Oz = O.copy(); Oz[2] = 98.0; Lz = L.copy(); Lz[2] = 97.0
px, xb, st, mfe = ex.simulate(Oz, H, Lz, C, e, d, x_end, x_px, np.array([99.0]))
check("entry already through stop -> exit at entry price", st[0] and px[0] == 98.0 and xb[0] == 2)
# MFE: long held bars 2..5, highs O+1 -> best = H[5]-O[2] = 4
px, xb, st, mfe = ex.simulate(O, H, L, C, e, d, x_end, x_px, None)
check("MFE over held bars", mfe[0] == H[5] - O[2])

# 7. shorts mirror: bullish signal at 6 -> exit O[7]; short stop above
ds = np.array([-1]); bull5 = np.zeros(10, bool); bull5[6] = True
x_end, x_px, sig = ex.plan_exits(e, ds, forced, ex.next_true(np.zeros(10, bool)), ex.next_true(bull5), O, C)
check("short exits at next open after a bullish signal", x_end[0] == 6 and x_px[0] == O[7])
Hs = H.copy(); Hs[3] = 120.0
px, xb, st, mfe = ex.simulate(O, Hs, L, C, e, ds, x_end, x_px, np.array([110.0]))
check("short stop fills at the stop", st[0] and px[0] == 110.0 and xb[0] == 3)
check("short MFE uses lows", ex.simulate(O, H, L, C, e, ds, x_end, x_px, None)[3][0] == O[2] - L[2])

# 8. pattern extreme over the span
Lp = np.array([5, 3, 4, 6.0]); Hp = np.array([9, 8, 10, 7.0])
check("pattern extreme long (span 2 at bar 2)", ex.pattern_extreme(Lp, Hp, np.array([2]), 2, np.array([1]))[0] == 3)
check("pattern extreme short (span 3 at bar 3)", ex.pattern_extreme(Lp, Hp, np.array([3]), 3, np.array([-1]))[0] == 10)

# 9. trailing stop: long, initial stop 99; swing low 103 confirmed at bar 4 -> stop 102.75 from bar 5; bar 5 low 102 -> out
tl = np.full(10, np.nan); th_ = np.full(10, np.nan); tl[4] = 103.0
Lt = L.copy(); Lt[5] = 102.0
x_end, x_px = np.array([8]), np.array([O[9]])
px, xb, how, mfe = ex.simulate(O, H, Lt, C, e, d, x_end, x_px, np.array([99.0]), tl, th_, 0.25)
check("trail ratchets to new swing low and stops next bar", how[0] == 1 and px[0] == 102.75 and xb[0] == 5)
Lt2 = L.copy(); Lt2[4] = 102.0                     # low on the confirming bar itself does not use the new stop
px, xb, how, mfe = ex.simulate(O, H, Lt2, C, e, d, x_end, x_px, np.array([99.0]), tl, th_, 0.25)
check("new trail level not applied on its own confirming bar", how[0] == 0)
tl2 = np.full(10, np.nan); tl2[4] = 90.0           # a lower swing low never loosens the stop
Lt3 = L.copy(); Lt3[6] = 98.5
px, xb, how, mfe = ex.simulate(O, H, Lt3, C, e, d, x_end, x_px, np.array([99.0]), tl2, th_, 0.25)
check("trail never loosens", how[0] == 1 and px[0] == 99.0)
# 10. target: long target 104.5 needs a high >= 104.75; bar 3 high 104 no, bar 4 high 105 yes -> fill 104.5
px, xb, how, mfe = ex.simulate(O, H, L, C, e, d, x_end, x_px, np.array([99.0]), target=np.array([104.5]))
check("target fills at the target 1 tick through", how[0] == 2 and px[0] == 104.5 and xb[0] == 4)
Lb = L.copy(); Lb[4] = 98.0                        # stop and target in the same bar -> stop first
px, xb, how, mfe = ex.simulate(O, H, Lb, C, e, d, x_end, x_px, np.array([99.0]), target=np.array([104.5]))
check("stop before target on the same bar", how[0] == 1 and px[0] == 99.0)
px, xb, how, mfe = ex.simulate(O, H, L, C, e, ds, x_end, x_px, None, target=np.array([101.5]))
check("short target", how[0] == 2 and px[0] == 101.5 and xb[0] == 2)
check("fresh()", list(ex.fresh(np.array([1, 1, 0, 1, 0, 1, 1], bool))) == [True, False, False, True, False, True, False])
print("ALL PASS")
