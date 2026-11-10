"""
Stop-loss options for the entry events: the same events and the same labeler (labels.label_entries: entry at the next
bar's open, target 1/1.5/2 x risk, 16-bar / 16:45 time limit, 1-minute path, costs + extra stop tick), but the stop
placed by different rules. Every stop is known at the SIGNAL bar's close (long shown; shorts mirrored):

  pattern        1 tick past the pattern's extreme (v1)
  pattern_min1   the pattern stop, but at least 1 average bar (R20) below the signal close
  pattern_cost   the pattern stop, but far enough that costs are at most 15% of the risk
  swing5         1 tick below the latest confirmed 5-bar swing low that is below the close (else pattern_min1)
  swing10        same with 10-bar swings
  avg1, avg2     1 / 2 average bars below the signal close (volatility-scaled, like AFML's barriers)
  usd40, usd100  a fixed $40 / $100 risk per micro below the signal close

Writes out/stops_<SYM>_15.parquet (one row per event x option: labels + option) and prints a summary.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 stop_options.py NQ
"""
import sys
import time
import warnings

import numpy as np
import pandas as pd

import labels as lb
import signals as sg
import walkforward as wf

warnings.filterwarnings("ignore")
SYM = sys.argv[1] if len(sys.argv) > 1 else "NQ"
TF = 15
OPTIONS = ["pattern", "pattern_min1", "pattern_cost", "swing5", "swing10", "avg1", "avg2", "usd40", "usd100"]
spec = sg.SPEC[SYM]; TICK, USD, COST = spec["tick"], spec["usd"], spec["cost"]


def snap(px, d):
    """round a stop to the tick grid, AWAY from the entry (long: down, short: up)."""
    return np.where(d > 0, np.floor(px / TICK + 1e-9), np.ceil(px / TICK - 1e-9)) * TICK


def swing_levels(b, k):
    """latest confirmed swing low / high at each bar (known k bars after the pivot), per contract run."""
    lo, hi = sg.pivots(b, k)
    L, H = b.L.to_numpy(), b.H.to_numpy(); n = len(b); run = b.run.to_numpy()
    out = []
    for piv, P in ((lo, L), (hi, H)):
        a = np.full(n, np.nan); q = np.flatnonzero(piv); a[q + k] = P[q]
        out.append(pd.Series(a).groupby(run).ffill().to_numpy())
    return out


def build_stops(ev, b):
    i = ev.i.to_numpy(); d = ev.d.to_numpy(); C = b.C.to_numpy()[i]; R20 = ev.R20.to_numpy()
    pat = ev.stop.to_numpy()
    min1 = C - d * R20
    risk_cost = COST / (0.15 * USD)                                  # points of risk for cost <= 15% of it
    S = {"pattern": pat,
         "pattern_min1": np.where(d > 0, np.minimum(pat, min1), np.maximum(pat, min1)),
         "pattern_cost": np.where(d > 0, np.minimum(pat, C - risk_cost), np.maximum(pat, C + risk_cost)),
         "avg1": C - d * R20, "avg2": C - d * 2 * R20,
         "usd40": C - d * 40 / USD, "usd100": C - d * 100 / USD}
    for k in (5, 10):
        lo, hi = swing_levels(b, k)
        lvl = np.where(d > 0, lo[i], hi[i]) - d * TICK
        ok = np.isfinite(lvl) & (d * (C - lvl) > 0)                  # must be on the stop side of the close
        S[f"swing{k}"] = np.where(ok, lvl, S["pattern_min1"])
    return {k: snap(v, d) for k, v in S.items()}


if __name__ == "__main__":
    t0 = time.time()
    keep = ["t", "i", "d", "patterns", "n_patterns", "stop", "R20", "session"]
    ev = pd.read_parquet(f"out/entries_{SYM}_{TF}.parquet", columns=keep)
    b = sg.bars(SYM, TF)
    assert (b.index[ev.i.to_numpy()] == pd.DatetimeIndex(ev.t)).all(), "event bar index mismatch"
    ev["patterns"] = ev.patterns.fillna("").str.split("|")
    m1 = lb.load_1m(SYM); m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    stops = build_stops(ev, b)
    parts = []
    for opt in OPTIONS:
        e2 = ev.copy(); e2["stop"] = stops[opt]
        lab = lb.label_entries(SYM, TF, b, e2[["t", "i", "d", "patterns", "n_patterns", "stop"]],
                               target_R=(1.0, 1.5, 2.0), max_bars=16, m1=m1)
        lab = lab.drop(columns=["patterns"]).assign(stop_option=opt)
        parts.append(lab)
        p = lab["pnl_usd_1.5"]
        print(f"{opt:13s} n={len(lab):,}  risk ${lab.risk_usd.median():6.2f} (median)  "
              f"$/trade {p.mean():+.2f}  hit {lab['y_1.5'].mean():.1%}  stopped {(lab['exit_kind_1.5'] == 'stop').mean():.0%}"
              f"  ({time.time() - t0:.0f}s)", flush=True)
    out = pd.concat(parts, ignore_index=True)
    out.to_parquet(f"out/stops_{SYM}_{TF}.parquet", compression="zstd")
    print(f"saved out/stops_{SYM}_{TF}.parquet ({len(out):,} rows) in {time.time() - t0:.0f}s")
