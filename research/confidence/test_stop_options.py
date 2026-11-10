"""Hand-made checks of stop_options.build_stops (run: same PYTHONPATH as stop_options.py)."""
import sys
sys.argv = ["x", "NQ"]
import numpy as np
import pandas as pd
import stop_options as so

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok &= bool(cond)

# 30 bars: a swing low (5-bar) at bar 10 = 95, confirmed at bar 15; signal at bar 20 close 100
n = 30
L = np.full(n, 99.0); H = np.full(n, 101.0); C = np.full(n, 100.0); O = np.full(n, 100.0)
L[10] = 95.0; H[12] = 103.0
idx = pd.date_range("2024-01-02 09:30", periods=n, freq="15min")
b = pd.DataFrame(dict(O=O, H=H, L=L, C=C, run=1, seg=1, sess=idx.normalize()), index=idx)
ev = pd.DataFrame(dict(i=[20, 20], d=[1, -1], stop=[98.75, 101.25], R20=[2.0, 2.0]))
S = so.build_stops(ev, b)
check("pattern unchanged", S["pattern"][0] == 98.75 and S["pattern"][1] == 101.25)
check("pattern_min1: at least 1 avg bar (2 pts) away", S["pattern_min1"][0] == 98.0 and S["pattern_min1"][1] == 102.0)
risk_cost = so.COST / (0.15 * so.USD)
check("pattern_cost: cost <= 15% of risk", (100 - S["pattern_cost"][0]) * so.USD * 0.15 >= so.COST - 1e-9)
check("swing5 long = confirmed swing low 95 - 1 tick", S["swing5"][0] == 94.75)
check("swing5 short = swing high 103 + 1 tick", S["swing5"][1] == 103.25)
check("avg2 = 2 avg bars", S["avg2"][0] == 96.0 and S["avg2"][1] == 104.0)
check("usd40 for MNQ = 20 pts", S["usd40"][0] == 80.0 and S["usd40"][1] == 120.0)
check("snap rounds away from entry", so.snap(np.array([98.1, 101.9]), np.array([1, -1])).tolist() == [98.0, 102.0])
# swing not yet confirmed -> fallback to pattern_min1
ev2 = pd.DataFrame(dict(i=[12], d=[1], stop=[98.75], R20=[2.0]))
S2 = so.build_stops(ev2, b)
check("swing5 before confirmation falls back to pattern_min1", S2["swing5"][0] == S2["pattern_min1"][0])
print("ALL PASS" if ok else "SOME FAILED")
