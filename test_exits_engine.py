"""Unit tests for exits_engine.simulate on hand-made price paths with known answers.
Usage:  PYTHONPATH=./pylib python3 test_exits_engine.py"""
import numpy as np
import exits_engine as ee


class Fake:
    def __init__(self, bars, atr=1.0, day=None):
        a = np.array(bars, float)
        self.Open, self.High, self.Low, self.Close = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
        n = len(a)
        self.atr5 = np.full(n, atr); self.ema20_5 = np.full(n, np.nan)
        self.h60_close = np.full(n, np.nan); self.h60_ema20 = np.full(n, np.nan); self.delta5 = np.zeros(n)
        self.day = np.zeros(n, int) if day is None else np.array(day)
        self.tmin = np.full(n, 600)
        last = np.r_[self.day[1:] != self.day[:-1], True]; ends = np.flatnonzero(last)
        self.day_end = ends[np.searchsorted(ends, np.arange(n))]; self.n = n


def check(name, got, want_pnl, want_reason=None, tol=1e-9):
    ok = got is not None and abs(got[1] - want_pnl) < tol and (want_reason is None or got[2] == want_reason)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: got {None if got is None else (round(got[1], 4), got[2], got[0])}, want ({want_pnl}, {want_reason})")
    return ok


ok = True
# signal bar 0; entry bar 1 opens 100 -> long entry 100.25; k0=2, atr=1 -> R=2, stop 98.25
base = [(100, 100, 100, 100)]
# 1 target_2 = 104.25 needs a high >= 104.50
ok &= check("long target", ee.simulate(Fake(base + [(100, 101, 99.5, 100.5), (100.5, 104.6, 100, 104)]), 0, 1, "target_2", 2), 4.0, "target")
# 2 target touched but not traded through (104.4 < 104.5) -> forced close at last bar: 104 - 0.25 - 100.25
ok &= check("target needs trade-through", ee.simulate(Fake(base + [(100, 101, 99.5, 100.5), (100.5, 104.4, 100, 104)]), 0, 1, "target_2", 2), 3.5, "close")
# 3 gap through stop: opens 97 -> fill 97 - 0.25
ok &= check("gap through stop", ee.simulate(Fake(base + [(100, 100.5, 99.5, 100), (97, 97.5, 96, 97)]), 0, 1, "target_2", 2), -3.5, "stop")
# 4 stop and target in the same bar -> stop wins: 98.25 - 0.25 - 100.25
ok &= check("stop wins same bar", ee.simulate(Fake(base + [(100, 105, 98, 101)]), 0, 1, "target_2", 2), -2.25, "stop")
# 5 trail_2: highs 101,103,105 -> stop ratchets to 105-2=103; next bar low 102.9, open 104 -> fill 103 - 0.25
ok &= check("trail_2 ratchet", ee.simulate(Fake(base + [(100, 101, 99.9, 100.9), (100.9, 103, 100.8, 102.9), (102.9, 105, 102.8, 104.8), (104, 104.2, 102.9, 103.5), (103.5, 110, 103.5, 110)]), 0, 1, "trail_2", 2), 2.5, "stop")
# 6 trail never loosens: after best 105 (stop 103) a lower high must not lower the stop
ok &= check("trail never loosens", ee.simulate(Fake(base + [(100, 105, 99.9, 104.5), (104.5, 104.6, 103.1, 103.2), (103.2, 103.3, 102.95, 103)]), 0, 1, "trail_2", 2), 2.5, "stop")
# 7 forced close at session end (hold): last bar of day closes 101 -> 101 - 0.25 - 100.25; next day's bar ignored
ok &= check("hold to session close", ee.simulate(Fake(base + [(100, 100.5, 99.9, 100.2), (100.2, 101.2, 100, 101), (90, 90, 80, 80)], day=[0, 0, 0, 1]), 0, 1, "hold", 2), 0.5, "close")
# 8 short mirror of test 1: entry 99.75, R=2, stop 101.75, target 95.75 needs low <= 95.50
ok &= check("short target", ee.simulate(Fake(base + [(100, 100.5, 99, 99.5), (99.5, 100, 95.4, 96)]), 0, -1, "target_2", 2), 4.0, "target")
# 9 short gap through stop: opens 103 -> fill 103 + 0.25
ok &= check("short gap stop", ee.simulate(Fake(base + [(100, 100.5, 99.5, 100), (103, 104, 102.5, 103)]), 0, -1, "target_2", 2), -3.5, "stop")
# 10 scale: +1.5R target = 103.25 (needs high >= 103.5): half books +3.0; stop -> breakeven 100.25, then trails 3 ATR
#    behind the best high 103.6 -> 100.6, rounded down to the tick 100.50; next bar's low 100.2 stops the second half
#    at 100.50 - 0.25 = 100.25 (breakeven, 0.0)
ok &= check("scale-out", ee.simulate(Fake(base + [(100, 103.6, 99.9, 103), (103, 103.1, 100.2, 100.4), (100.4, 101, 100, 100.5)]), 0, 1, "scale", 2), 0.5 * 3.0 + 0.5 * 0.0, "stop")
# 12 off-grid stop: R = 2 x 1.3 = 2.6 -> stop 100.25-2.6 = 97.65 must sit at 97.50; a low of 97.50 fills 97.25 (-3.00)
ok &= check("stop snapped to tick", ee.simulate(Fake(base + [(100, 100.5, 97.5, 98)], atr=1.3), 0, 1, "hold", 2), -3.0, "stop")
# 13 bar OPENS through the target then trades to the stop -> target filled first at the limit
ok &= check("open through target", ee.simulate(Fake(base + [(100, 104.4, 99.5, 104), (104.75, 105, 98, 99)]), 0, 1, "target_2", 2), 4.0, "target")
# 14 a signal on a session's last bar enters at the next session's open (6 PM reopen) and is flattened at that session's close
ok &= check("enter at reopen", ee.simulate(Fake(base + [(100, 101, 99.9, 101)], day=[0, 1]), 0, 1, "hold", 2), 0.5, "close")
# 15 clock exit: tmin of bars (minute of day); exit at the close of the first bar closing at/after 10:30 (630)
f = Fake(base + [(100, 101, 99.9, 100.5), (100.5, 102, 100.4, 101.75), (101.75, 103, 101, 102.5)])
f.tmin = np.array([600, 615, 625, 630])          # bar 2 starts 10:25 -> closes 10:30
ok &= check("clock_630", ee.simulate(f, 0, 1, "clock_630", 2), 101.75 - 0.25 - 100.25, "clock")
# 16 time stop: at 10 minutes (2nd bar close) open profit 0.25/2 = 0.125R < 0.5R -> exit at that close
ok &= check("tstop_10_0.5", ee.simulate(Fake(base + [(100, 100.6, 99.9, 100.5), (100.5, 100.8, 100.3, 100.5), (100.5, 110, 100.5, 110)]), 0, 1, "tstop_10_0.5", 2), 100.5 - 0.25 - 100.25, "tstop")
# 17 profit lock: once +1R (102.25) reached, stop -> breakeven; later drop to 100 fills at 100.25 - 0.25
ok &= check("lock_1_0", ee.simulate(Fake(base + [(100, 102.5, 99.9, 102.3), (102.3, 102.4, 99.8, 100)]), 0, 1, "lock_1_0", 2), -0.25, "stop")
# 18 stop at a given price: 99.10 snaps down to 99.00 (R = 100.25 - 99.00 = 1.25); a low of 98.9 fills 98.75
r = ee.simulate(Fake(base + [(100, 100.5, 98.9, 99.2)]), 0, 1, "hold", 2, stop_px=99.1)
ok &= check("stop at a given price", r, 98.75 - 100.25, "stop") and abs(r[5] - 1.25) < 1e-9
# 19 entry already through the given stop (100.40 snaps to 100.25 = the entry fill) -> no trade
none = ee.simulate(Fake(base + [(100, 100.5, 99.9, 100.2)]), 0, 1, "hold", 2, stop_px=100.4) is None
print(f"{'PASS' if none else 'FAIL'}  entry already through the stop: no trade"); ok &= none
# 20 min_R: risk 1.25 is below the 1.5 minimum -> no trade
none = ee.simulate(Fake(base + [(100, 100.5, 98.9, 99.2)]), 0, 1, "hold", 2, stop_px=99.1, min_R=1.5) is None
print(f"{'PASS' if none else 'FAIL'}  min_R: no trade"); ok &= none
# 21 R_pts overrides k0 x ATR: R = 1.5 -> stop 98.75; a low of 98.75 fills 98.50
ok &= check("R_pts override", ee.simulate(Fake(base + [(100, 100.5, 98.75, 99)]), 0, 1, "hold", 2, R_pts=1.5), 98.5 - 100.25, "stop")
# 22 failed breakout: level 100.5; bar 1 closes 100.6 (still above), bar 2 closes 100.4 (back below) -> exit 100.4 - 0.25
ok &= check("level exit", ee.simulate(Fake(base + [(100, 100.8, 99.9, 100.6), (100.6, 100.7, 100.3, 100.4), (100.4, 105, 100.4, 105)]), 0, 1, "hold", 2, level=100.5), 100.4 - 0.25 - 100.25, "level")
# 23 failed breakdown (short entry 99.75): level 99.5; bar 2 closes 99.6 (back above) -> exit 99.6 + 0.25
ok &= check("level exit short", ee.simulate(Fake(base + [(100, 100.1, 99.2, 99.4), (99.4, 99.7, 99.3, 99.6), (99.6, 99.6, 95, 95)]), 0, -1, "hold", 2, level=99.5), 99.75 - (99.6 + 0.25), "level")
# 23b stop at a given price, taken at the signal close (R 100.25-99.5 = 0.75), but the next bar OPENS at 99.2, below
#     the stop: fill 99.45, out at once at the open 99.2 - 0.25 = 98.95 -> -0.50
ok &= check("open gaps through the given stop", ee.simulate(Fake(base + [(99.2, 99.3, 99.0, 99.1)]), 0, 1, "hold", 2, stop_px=99.6), -0.5, "stop")
# 24 run() passes per-signal settings and reports R
tr = ee.run(Fake(base + [(100, 100.5, 98.9, 99.2)]), [(0, 1)], "hold", k0=2, extra={0: {"stop_px": 99.1}})
good = len(tr) == 1 and tr.exit[0] == "stop" and abs(tr.R_pts[0] - 1.25) < 1e-9 and abs(tr.pts[0] + 1.5) < 1e-9
print(f"{'PASS' if good else 'FAIL'}  run() with per-signal stop"); ok &= good
print("\nALL PASS" if ok else "\nSOME TESTS FAILED")
