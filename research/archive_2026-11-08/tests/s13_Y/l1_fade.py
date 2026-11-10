"""Section 13 / L1: major 8:30 release fade, explicit bar-by-bar state machine per day.
Run: cd project && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this file>"""
import os, sys, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.append(os.getcwd())
from load_bars import build
import calendar_days as cd   # project module (read-only), cwd = project

T0830, T0845, T0945 = 8 * 60 + 30, 8 * 60 + 45, 9 * 60 + 45
COST_PTS = {"NQ": 1.00, "ES": 0.70}         # round-trip cost per micro, in points
USD_PT = {"NQ": 2.0, "ES": 5.0}             # micro $ per point
MAX_GAP_MIN = 5


def day_window(bars_day):
    """Bars stamped 8:30..9:45 inclusive. Returns (window df, skip_reason or None)."""
    w = bars_day[(bars_day.tmin >= T0830) & (bars_day.tmin <= T0945)]
    if len(w) == 0:
        return w, "no bars"
    if w.tmin.iloc[0] != T0830:
        return w, "8:30 bar missing"
    if w.tmin.iloc[-1] != T0945:
        return w, "9:45 bar missing"
    if (w.tmin == T0845).sum() != 1:
        return w, "8:45 bar missing"
    if w.instrument_id.nunique() != 1:
        return w, "contract roll inside 8:30-9:45"
    if np.diff(w.tmin.to_numpy()).max() > MAX_GAP_MIN:
        return w, "gap > 5 min inside 8:30-9:45"
    return w, None


def simulate_day(w, signal="open845", stop_mult=None, force_dir=None):
    """Explicit state machine over the bars of one day's 8:30-9:45 window.
    signal: 'open845' = move 8:30 open -> 8:45 open (spec as written);
            'close844' = move 8:30 open -> 8:44 close (strict: only closed bars before 8:45).
    stop_mult: None = time exit only; 2.0 = disaster stop 2 x |move| beyond entry.
    force_dir: use this direction instead of the fade (for the ES-with-NQ-signal report)."""
    state = "WAIT_830"
    o830 = c844 = None
    pos = 0; entry = stop = move = None; entry_t = None
    for r in w.itertuples(index=False):
        t = r.tmin
        if state == "WAIT_830":
            if t == T0830:
                o830 = r.Open
                state = "MEASURING"
            # (the 8:30 bar's own range is irrelevant)
            continue
        if state == "MEASURING":
            if t < T0845:
                c844 = r.Close if t == T0845 - 1 else c844   # last closed bar before 8:45 (its close)
                continue
            # t == 8:45 bar open: decide (uses only the 8:30 open and, for 'open845', the 8:45 open print itself)
            ref = r.Open if signal == "open845" else c844
            if ref is None:
                return None, "8:44 bar missing (strict signal)"
            move = ref - o830
            if move == 0 and force_dir is None:
                return None, "zero move"
            pos = force_dir if force_dir is not None else (-1 if move > 0 else 1)
            entry, entry_t = r.Open, r.ts
            stop = entry - pos * stop_mult * abs(move) if (stop_mult and move != 0) else None
            state = "IN_POSITION"
            # fall through: the entry bar can also hit the stop after the open
        if state == "IN_POSITION":
            if t == T0945:                                   # time exit at the 9:45 bar open
                return dict(entry_ts=entry_t, exit_ts=r.ts, side="long" if pos > 0 else "short", entry=entry,
                            exit=r.Open, reason="time", move_830_845=move, o830=o830, stop=stop), None
            if stop is not None:
                if t != T0845 and pos * (r.Open - stop) <= 0:       # opened through the stop
                    return dict(entry_ts=entry_t, exit_ts=r.ts, side="long" if pos > 0 else "short", entry=entry,
                                exit=r.Open, reason="stop_gap", move_830_845=move, o830=o830, stop=stop), None
                hit = (r.Low <= stop) if pos > 0 else (r.High >= stop)
                if hit:
                    return dict(entry_ts=entry_t, exit_ts=r.ts, side="long" if pos > 0 else "short",
                                entry=entry, exit=stop, reason="stop", move_830_845=move, o830=o830, stop=stop), None
    return None, "window ended without exit"


def to_row(d, rec, sym, tags):
    pos = 1 if rec["side"] == "long" else -1
    gross = pos * (rec["exit"] - rec["entry"])
    net = gross - COST_PTS[sym]
    return dict(date=d.date(), entry_time=rec["entry_ts"].strftime("%H:%M"), exit_time=rec["exit_ts"].strftime("%H:%M"),
                side=rec["side"], entry=rec["entry"], exit=rec["exit"], exit_reason=rec["reason"], gross_pts=gross,
                net_pts=net, gross_usd=gross * USD_PT[sym], net_usd=net * USD_PT[sym], net_bp=1e4 * net / rec["entry"],
                o830=rec["o830"], move_830_845=rec["move_830_845"], stop=rec["stop"], **tags)


def run(sym, days, tags_of, signal="open845", stop_mult=None, force_map=None):
    """force_map: {date: direction} to trade a given direction (skip days not in the map)."""
    bars = build(sym)
    by_day = dict(tuple(bars[bars.date.isin(list(days))].groupby("date")))
    rows, skips = [], []
    for d in sorted(days):
        b = by_day.get(d)
        if b is None:
            skips.append(dict(date=d.date(), reason="no bars (outside data / closed)")); continue
        w, why = day_window(b)
        if why:
            skips.append(dict(date=d.date(), reason=why)); continue
        fdir = None
        if force_map is not None:
            if d not in force_map:
                skips.append(dict(date=d.date(), reason="no direction from the signal market")); continue
            fdir = force_map[d]
        rec, why = simulate_day(w, signal=signal, stop_mult=stop_mult, force_dir=fdir)
        if rec is None:
            skips.append(dict(date=d.date(), reason=why)); continue
        rows.append(to_row(d, rec, sym, tags_of(d)))
    return pd.DataFrame(rows), pd.DataFrame(skips)
