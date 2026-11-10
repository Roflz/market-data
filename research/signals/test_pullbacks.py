"""Tests for pullbacks.py on hand-made candles.
Usage: cd research/signals && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 test_pullbacks.py"""
import warnings

import numpy as np
import pandas as pd

import pullbacks as pb
import signals as sg

warnings.filterwarnings("ignore", category=RuntimeWarning)
ok_all = True


def check(name, cond):
    global ok_all
    print(("PASS " if cond else "FAIL ") + name)
    ok_all &= bool(cond)


def frame(mids, start="2024-01-01 18:00"):
    """One bar per mid price: H = mid + 1, L = mid - 1, close 0.3 above the mid if the mid rose, else below."""
    m = np.array(mids, float)
    up = np.r_[True, np.diff(m) >= 0]
    C = np.where(up, m + 0.3, m - 0.3); O = np.where(up, m - 0.3, m + 0.3)
    idx = pd.date_range(start, periods=len(m), freq="5min")
    b = pd.DataFrame({"O": O, "H": m + 1, "L": m - 1, "C": C, "V": 100.0, "inst": 1,
                      "sess": pd.Timestamp("2024-01-02"), "vwap": m}, index=idx)
    b["seg"] = 1
    b["run"] = 1
    return b


def run(b):
    c = sg.context(b, tick=0.25)
    return pb.detect(b, c, k_leg=5, sym="NQ", tf=5), c


rise = [100.0 + i for i in range(60)]                       # 100..159, no swing points
dip = [158, 157, 156, 155, 154, 153]                        # swing low SL at mid 153 (L = 152)
leg = [155, 157, 159, 161, 163, 165, 167, 169, 171, 173]    # swing high SH at mid 173 (H = 174)
pull = [171, 169, 167, 165, 163]                            # pullback low PL at mid 163 (L = 162)
cont = [165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193]
I_SL = len(rise) + len(dip) - 1
I_SH = I_SL + len(leg)
I_PL = I_SH + len(pull)

# 1. simple up-leg, pullback, continuation
b = frame(rise + dip + leg + pull + cont)
df, c = run(b)
check("trend is +1 at SH (test setup)", c.trend.iloc[I_SH] == 1)
check("exactly one pullback found", len(df) == 1)
r = df.iloc[0]
check("bullish, SL/SH/PL at the expected bars", r.direction == 1 and (r.i_SL, r.i_SH, r.i_PL) == (I_SL, I_SH, I_PL))
check("prices SL 152, SH 174, PL 162", (r.SL, r.SH, r.PL) == (152, 174, 162))
check("depth = 12/22, nearest Fibonacci 0.5", abs(r.depth - 12 / 22) < 1e-12 and r.fib_near == 0.5)
check("leg 22 pts = $44 per MNQ", r.leg_pts == 22 and r.leg_usd == 44)
check("bars in impulse 10, in pullback 5", r.bars_impulse == 10 and r.bars_pullback == 5)
# after the event (mid 169, close 169.3) the bars go 171, 173, 175: the high 176 > 174 on the 3rd bar
check("outcome continuation after 3 bars", r.outcome == "continuation" and r.bars_to_outcome == 3)
check("max favourable move = 194 - 169.3, max adverse 0", abs(r.mfe_pts - (194 - 169.3)) < 1e-9 and r.mae_pts == 0)

# 3. look-ahead: event = PL + 3, and the row is identical (except the outcome) when the data ends at the event bar
check("event bar = PL + 3", r.i_event == r.i_PL + 3 and r.event_wait == 0)
dfe, _ = run(b.iloc[:r.i_event + 1])
dfb, _ = run(b.iloc[:r.i_event])
keep = [k for k in df.columns if k not in ("outcome", "bars_to_outcome", "i_outcome", "n_window", "mfe_pts", "mae_pts",
                                           "mfe_usd", "mae_usd", "end_pts", "end_usd")]
same = len(dfe) == 1 and all((dfe.iloc[0][k] == r[k]) or (pd.isna(dfe.iloc[0][k]) and pd.isna(r[k])) for k in keep)
check("same stats when the data stops at the event bar", same)
check("no pullback when the data stops one bar before the event", len(dfb) == 0)
check("outcome is no_time when nothing follows the event", len(dfe) == 1 and dfe.iloc[0].outcome == "no_time")

# 2. the first swing low after SH is BELOW SL: not a pullback
deep = [171, 167, 163, 159, 155, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169]
b2 = frame(rise + dip + leg + deep)
df2, _ = run(b2)
check("swing low below SL -> no pullback", len(df2) == 0)

# failure: after the event the price closes below PL (162)
fail = [165, 167, 169, 166, 163, 160, 158, 156, 158, 160, 162, 164, 166]
b3 = frame(rise + dip + leg + pull + fail)
df3, _ = run(b3)
check("failure case found", len(df3) >= 1 and df3.iloc[0].i_SH == I_SH)
r3 = df3.iloc[0]
# event close 169.3; next bars: 166 (C 165.7), 163 (C 162.7), 160 (C 159.7 < 162) -> failure on bar 3
check("outcome failure after 3 bars", r3.outcome == "failure" and r3.bars_to_outcome == 3)
check("max adverse move = 169.3 - 155", abs(r3.mae_pts - (169.3 - 155)) < 1e-9)

# mirror: the same shape upside down is a bearish pullback with the same depth and outcome
bm = b.copy()
bm["H"], bm["L"] = 400 - b.L, 400 - b.H
bm["O"], bm["C"], bm["vwap"] = 400 - b.O, 400 - b.C, 400 - b.vwap
dfm, _ = run(bm)
check("mirror: one bearish pullback", len(dfm) == 1 and dfm.iloc[0].direction == -1)
check("mirror: same bars, depth and outcome",
      len(dfm) == 1 and (dfm.iloc[0].i_SH, dfm.iloc[0].i_PL, dfm.iloc[0].outcome) == (I_SH, I_PL, "continuation")
      and abs(dfm.iloc[0].depth - r.depth) < 1e-12 and dfm.iloc[0].SH == 400 - 174)

# flat by 16:45: an event bar at 16:40 on 5-minute bars has no bar left in the window
b4 = frame(rise + dip + leg + pull + cont, start="2024-01-02 16:40")
b4.index = b4.index - (b4.index[I_PL + 3] - pd.Timestamp("2024-01-02 16:40"))
df4, _ = run(b4)
check("event at 16:40 -> no_time (flat by 16:45)", len(df4) == 1 and df4.iloc[0].outcome == "no_time")

print("ALL PASS" if ok_all else "SOME FAILED")
