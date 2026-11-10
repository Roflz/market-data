"""Example idea file for try_idea.py. Copy it, change the function, keep the METRICS dict shape.

Idea: a pullback to EMA20 in an up-stack (EMA8 > EMA20 > EMA50) whose bar closes back above EMA8 -> long;
the mirror image -> short. Values use only the current and earlier bars (known at the bar's close).
Long and short are listed as separate metrics because pooling both sides can hide a one-sided edge.
"""
import numpy as np
import pandas as pd


def _pullback(b, side):
    up = (b.ema8 > b.ema20) & (b.ema20 > b.ema50)
    dn = (b.ema8 < b.ema20) & (b.ema20 < b.ema50)
    if side > 0:
        hit = up & (b.L <= b.ema20) & (b.C > b.ema8)
    else:
        hit = dn & (b.H >= b.ema20) & (b.C < b.ema8)
    ok = b.ema50.notna()
    return pd.Series(np.where(hit, float(side), 0.0), index=b.index).where(ok)


METRICS = {
    "ema20_pullback_long": dict(fn=lambda b: _pullback(b, +1), kind="sided",
                                desc="up-stack EMA8>20>50, bar touches EMA20 and closes above EMA8 -> long"),
    "ema20_pullback_short": dict(fn=lambda b: _pullback(b, -1), kind="sided",
                                 desc="down-stack EMA8<20<50, bar touches EMA20 and closes below EMA8 -> short"),
}
