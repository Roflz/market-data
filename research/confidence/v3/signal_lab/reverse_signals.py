"""
v3/signal_lab/reverse_signals.py - the FROZEN candidate signals from reverse_discover.py (2010-17 discovery half).
Written and hashed into out/reverse_candidates.md BEFORE any 2018-2025H1 number was computed. Do not edit after the
confirmation run: a changed file means a new, separately counted experiment.
Each entry: fn(bars) -> Series (known at the bar's close), lab kind, pre-registered sign of the effect, primary hold
(lab target column), and whether it is a DIRECTION or SIZE claim.
"""
import numpy as np
import pandas as pd

import reverse_feats as RF

SURGE = 0.5                     # log volume vs usual for the time of day: 0.5 = 1.65x (discovery top ~20%)


def _f(col):
    def fn(b):
        return RF.features(b)[col].reindex(b.index)
    return fn


def surge_fade(b):
    f = RF.features(b).reindex(b.index)
    return f["d_ema8"].where(f["vol_rel"] > SURGE)


def vol_ratio_0930(b):
    f = RF.features(b).reindex(b.index)
    at = (b.index.hour == 9) & (b.index.minute == 15)              # bar 09:15-09:30 ET, known at 09:30
    return f["r20_r100"].where(at)


CANDIDATES = {
    # ---------------- DIRECTION claims
    "rev_stretch_ema8": dict(fn=_f("d_ema8"), kind="continuous", sign=-1, hold="dir_h4", claim="direction",
                             desc="distance of close from EMA8 in average bars; far above -> next hour down"),
    "rev_last_hour": dict(fn=_f("ret4"), kind="continuous", sign=-1, hold="dir_h4", claim="direction",
                          desc="last hour's move in average bars; up hour -> next hour down"),
    "rev_new_day_extreme": dict(fn=_f("new_hod"), kind="continuous", sign=-1, hold="dir_h4", claim="direction",
                                desc="+1 bar made a new high of day, -1 a new low; new high -> next hour down"),
    "rev_surge_fade": dict(fn=surge_fade, kind="continuous", sign=-1, hold="dir_h4", claim="direction",
                           desc="distance from EMA8, only on bars with volume >= 1.65x usual for the time of day"),
    "rev_outside_up_eod": dict(fn=_f("outside"), kind="event", sign=+1, hold="dir_eod", claim="direction",
                               desc="outside bar (higher high and lower low than the last bar) -> drift up to 16:45"),
    "rev_inside_down_eod": dict(fn=_f("inside"), kind="event", sign=-1, hold="dir_eod", claim="direction",
                                desc="inside bar -> drift down to 16:45"),
    "rev_volratio_0930": dict(fn=vol_ratio_0930, kind="continuous", sign=-1, hold="dir_eod", claim="direction",
                              desc="at 09:30 ET: average bar of last 20 / last 100 bars; high -> down into 16:45"),
    # ---------------- SIZE claims (a big move is coming, direction unknown)
    "rev_bigbar_size": dict(fn=_f("rng1"), kind="continuous", sign=+1, hold="abs_h4", claim="size",
                            desc="last bar's range / average bar; big bar -> bigger move next hour"),
    "rev_volsurge_size": dict(fn=_f("vol_rel"), kind="continuous", sign=+1, hold="abs_h4", claim="size",
                              desc="log volume vs usual for the time of day; surge -> bigger move next hour"),
    "rev_nr7_quiet": dict(fn=_f("nr7"), kind="event", sign=-1, hold="abs_h4", claim="size",
                          desc="narrowest bar of the last 7 -> SMALLER move next hour (no 'squeeze' breakout)"),
}
