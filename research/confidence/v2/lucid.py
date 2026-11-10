"""
v2/lucid.py - Lucid's daily close done right for the v2 pipeline: flat from 16:45 to 18:00 ET.

exits.session_frame (used by labels.eligible -> label_entries, exit_study.simulate, trigger_scan) only treats bars
that close in 16:45-17:00 as the 'tail'. Until about 2015 (and on a few later days) the 1-minute data has trading
after 17:00 in the SAME session (old CME schedule: e.g. ES 16:30-17:15 / 17:30), so the forced-exit bar could be the
17:15 bar and trades could be entered and held after 16:45 - not allowed at Lucid. Example: ES 15-min random
trades in 2010-2015 exited up to 17:30 (about 5,000 of 62,000 pool trades).

session_frame(b, tf) here: a bar is NOT allowed if it closes after 16:45 and starts before 18:00 (the next session's
open), so the forced-exit bar is the last bar that closes by 16:45. install() swaps it into the exits module for
this process (attribute lookup at call time, so labels.eligible / label_entries / exit_study.simulate all use it);
the code in research/confidence and research/signals is not modified and earlier outputs are unaffected.
"""
import numpy as np

import exits as ex

CUTOFF_MIN = 16 * 60 + 45
REOPEN_MIN = 18 * 60
_ORIG = ex.session_frame


def session_frame(b, tf):
    """(allowed[t], forced[t]) as exits.session_frame, with tail = bars closing after 16:45 and starting < 18:00."""
    m = (b.index.hour * 60 + b.index.minute).to_numpy()
    allowed = ~((m > CUTOFF_MIN - tf) & (m < REOPEN_MIN))
    seg = b.seg.to_numpy()
    n = len(b)
    last = np.full(n, -1)
    if n:
        idx = np.where(allowed, np.arange(n), -1)
        starts = np.r_[0, np.flatnonzero(seg[1:] != seg[:-1]) + 1]
        ends = np.r_[starts[1:], n]
        for s, e, v in zip(starts, ends, np.maximum.reduceat(idx, starts)):
            last[s:e] = v
    return allowed, last


def install():
    ex.session_frame = session_frame


def uninstall():
    ex.session_frame = _ORIG
