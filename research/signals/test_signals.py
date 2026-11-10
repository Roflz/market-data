"""Tests for signals.py on hand-made candles. Usage: cd research/signals && PYTHONPATH=../../pylib:../..:. python3 test_signals.py"""
import numpy as np
import pandas as pd

import signals as sg

ok_all = True


def frame(rows, seg=None):
    a = np.array(rows, float)
    idx = pd.date_range("2024-01-02 10:00", periods=len(a), freq="15min")
    b = pd.DataFrame({"O": a[:, 0], "H": a[:, 1], "L": a[:, 2], "C": a[:, 3], "V": 100.0, "inst": 1,
                      "sess": pd.Timestamp("2024-01-02"), "vwap": a[:, 3]}, index=idx)
    b["seg"] = 1 if seg is None else seg
    b["run"] = 1
    return b


def check(name, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + name)
    ok_all &= bool(cond)


# 30 calm bars drifting DOWN (body 1, range 2) so EMA10 is above price, then the test bars
calm = [(100 - 0.5 * i, 100 - 0.5 * i + 0.5, 100 - 0.5 * i - 1.5, 100 - 0.5 * i - 1.0) for i in range(30)]
last = calm[-1][3]

# hammer: range 4 (>= avgR10 = 2), lower shadow 3 >= 2 x body 0.5, upper 0 <= 0.1 x range, prior close < EMA10
b = frame(calm + [(last, last + 0.5, last - 3.5, last + 0.5)])
p = sg.patterns(b, sg.context(b))
check("hammer fires on the last bar only", p.hammer.iloc[-1] == 1 and p.hammer.iloc[:-1].abs().sum() == 0)
check("hammer also counts as bullish pin bar", p.pin_bar.iloc[-1] == 1)

# bullish engulfing: down bar then a bigger up bar engulfing its body, below EMA10
b = frame(calm + [(last, last + 0.25, last - 1.25, last - 1.0), (last - 1.25, last + 1.5, last - 1.5, last + 1.25)])
p = sg.patterns(b, sg.context(b))
check("bullish engulfing fires on bar 2", p.engulfing.iloc[-1] == 1)

# inside bar then breakout above the mother bar 2 bars later
m = (last, last + 3, last - 3, last + 1)
ins = (last + 1, last + 2, last - 1, last)
nob = (last, last + 2.5, last - 0.5, last + 2.5)          # close 2.5 < mother high 3: no breakout yet
brk = (last + 2.5, last + 4, last + 2, last + 3.5)        # close 3.5 > 3: breakout
b = frame(calm + [m, ins, nob, brk])
p = sg.patterns(b, sg.context(b))
check("inside bar detected", p.inside_bar.iloc[-3] == 1)
check("inside-bar breakout on the first close above the mother high", p.inside_bar_breakout.iloc[-1] == 1 and p.inside_bar_breakout.iloc[-2] == 0)

# breakout must not cross a session/segment boundary
seg = np.r_[np.ones(len(calm) + 3), 2]
b = frame(calm + [m, ins, nob, brk], seg=seg)
p = sg.patterns(b, sg.context(b))
check("no breakout across a session boundary", p.inside_bar_breakout.iloc[-1] == 0)

# swing low confirmed only 3 bars after the pivot (no look-ahead)
rows = [(10, 11, 9, 10)] * 5 + [(10, 10.5, 5, 9)] + [(9, 10, 8, 9.5)] * 6
b = frame(rows)
c = sg.context(b)
check("swing low unknown at the pivot bar and 2 bars after", c.swing_lo.iloc[5:8].isna().all())
check("swing low = 5 from the 3rd bar after the pivot", c.swing_lo.iloc[8] == 5 and c.swing_lo.iloc[-1] == 5)

# forward move: entry at the NEXT bar's open, exit at the close h bars later, same segment only
rows = [(100 + i, 101 + i, 99 + i, 100.5 + i) for i in range(30)]
b = frame(rows)
f = sg.forward(b, sg.context(b))
check("entry is the next bar's open", f.entry.iloc[10] == 111)
check("fwd1 = close of bar t+1 - next open", f.fwd1_pts.iloc[10] == (111.5 - 111))
check("fwd5 = close of bar t+5 - next open", f.fwd5_pts.iloc[10] == (115.5 - 111))
check("no forward value past the end", np.isnan(f.fwd5_pts.iloc[-3]))

# trend state and momentum
c = sg.context(b)
check("rising series -> trend +1 once EMA50 exists", c.trend.iloc[-1] == 0 and True)   # only 30 bars: EMA50 not valid yet
rows = [(100 + i, 101 + i, 99 + i, 100.5 + i) for i in range(80)]
b = frame(rows); c = sg.context(b)
check("rising series of 80 bars -> trend +1", c.trend.iloc[-1] == 1)
check("momentum14 = 100 x C / C[14 bars ago]", abs(c.mom14.iloc[-1] - 100 * 179.5 / 165.5) < 1e-9)

# flat (zero-range) bars and dead stretches never produce a pattern
rows = [(100 + 0.5 * (i % 3), 101 + 0.5 * (i % 3), 99, 100) for i in range(30)] + [(100, 100, 100, 100)]
b = frame(rows); p = sg.patterns(b, sg.context(b))
check("flat bar is not a hammer / doji / inside bar / any pattern", (p.iloc[-1] == 0).all())
rows = [(100, 100, 100, 100)] * 20 + [(100, 100.25, 99, 100.25)]
b = frame(rows); p = sg.patterns(b, sg.context(b))
check("no pattern when the 10-bar average range is 0", (p.iloc[-1] == 0).all())

print("\nALL PASS" if ok_all else "\nSOME TESTS FAILED")
