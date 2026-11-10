"""
Real-data calibration of the signal lab (light: 15-min bars, ~1 GB; ~4 minutes).

  1. NULL on real prices: random persistent signals (AR(1) 0.95 within the session, continuous and +-1 clustered
     events) carry no information by construction. With real volatility clustering, time-of-day patterns, drift and
     fat tails, each p-value must still reject ~5% of the time at 0.05, and the honest t must have sd ~1 at h16.
  2. POSITIVE CONTROLS (effects known to exist, from v3/signal_lab/out/methods_calibration.txt):
       next-bar reversal: this bar's return (C - O)/R20 -> next bar's return is slightly NEGATIVE (16/16 years);
       leverage: last 4 bars' return -> the next 4 bars' range is SMALLER after up moves (16/16 years).
     The lab must find both with the right sign. The reversal is checked with and without the 'last-bar sign'
     control (that control absorbs part of it by design).
Output: v3/signal_lab/out/calibration_real.txt (+ .csv)

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/signal_lab \
      OMP_NUM_THREADS=3 nice -n 5 python3 v3/signal_lab/calibrate_real.py [ES] [n_null]
"""
import os
import sys
import time

import numpy as np
import pandas as pd

import harness as H
import lab as L
from test_lab import _ar_within

sym = sys.argv[1] if len(sys.argv) > 1 else "ES"
n_null = int(sys.argv[2]) if len(sys.argv) > 2 else 100
tf = 15
t0 = time.time()
lines = [f"### calibrate_real.py {sym} {tf}-min  (run {pd.Timestamp.now():%Y-%m-%d %H:%M})"]
P = L.Panel(H.bars(sym, tf), sym, tf)
lines.append(f"panel: {P.n} bars, {P.T} sessions, build {P.build_s:.1f}s")
rng = np.random.default_rng(7)
rows = []
for i in range(n_null):
    a = _ar_within(rng, P.sess_code, 0.95)
    x, kind = (a, "continuous") if i % 2 == 0 else (np.where(a > 1.2, 1.0, np.where(a < -1.2, -1.0, 0.0)), "sided")
    r = L.evaluate(P, x, kind, name=f"null{i}", power=False, event_study=False, ic=False)
    t = r["table"]
    for c in ("dir_h1", "dir_h4", "dir_h16", "abs_h4", "path"):
        rows.append(dict(sig=i, kind=kind, col=c, p_boot=t.at[c, "p_boot"], p_nw=t.at[c, "p_nw"],
                         p_placebo=t.at[c, "p_placebo"], p_placebo_emp=t.at[c, "p_placebo_emp"], p=t.at[c, "p"],
                         t_honest=t.at[c, "effect"] / t.at[c, "se_boot"], t_naive=t.at[c, "t_iid_bar"]))
    rows.append(dict(sig=i, kind=kind, col="p_dir(6 horizons)", p=r["p_dir"]))
    rows.append(dict(sig=i, kind=kind, col="p_size(6 horizons)", p=r["p_size"]))
D = pd.DataFrame(rows)
D.to_csv(os.path.join(L.OUT, f"calibration_real_{sym}.csv"), index=False)
fpr = D.groupby("col")[["p_boot", "p_nw", "p_placebo", "p_placebo_emp", "p"]].apply(lambda g: (g < 0.05).mean())
lines.append(f"\nNULL: {n_null} random persistent signals on real {sym} {tf}-min prices; share with p < 0.05 "
             f"(should be ~0.05; binomial sd ~{np.sqrt(0.05 * 0.95 / n_null):.3f}):")
lines.append(fpr.round(3).to_string())
h16 = D[D.col == "dir_h16"]
lines.append(f"sd of t at h16 (16 overlapping bars): honest (session bootstrap) {h16.t_honest.std():.2f}, "
             f"naive bar-level iid {h16.t_naive.std():.2f}  (honest should be ~1)")

# positive controls
b = P.bars
r20 = pd.Series(P.r20, index=b.index)
bar_ret = (b.C - b.O) / r20
back4 = (b.C - b.C.shift(4)).where(b.seg.eq(b.seg.shift(4))) / r20
lines.append("\nPOSITIVE CONTROLS")
for name, x, fe, col in (("next-bar reversal, default controls", bar_ret, L.FE_DEFAULT, "dir_h1"),
                         ("next-bar reversal, without last-bar-sign control", bar_ret,
                          tuple(f for f in L.FE_DEFAULT if f != "prev"), "dir_h1"),
                         ("leverage: back-4 return -> next-4 range", back4, L.FE_DEFAULT, "rng_h4")):
    PP = P if fe == L.FE_DEFAULT else L.Panel(b, sym, tf, fe=fe)
    r = L.evaluate(PP, x, "continuous", name=name, power=False)
    t = r["table"]
    lines.append(f"  {name}: {col} effect {t.at[col, 'effect']:+.4f} R20 (CI {t.at[col, 'ci_lo']:+.4f} .. "
                 f"{t.at[col, 'ci_hi']:+.4f}), IC {t.at[col, 'ic']:+.4f}, p {t.at[col, 'p']:.2g}, placebo rank p "
                 f"{t.at[col, 'p_placebo_emp']:.3g}, same sign {int(t.at[col, 'years_same'])}/{int(t.at[col, 'years_n'])} "
                 f"years; verdict: {L.verdict_lines(r)[0 if col.startswith('dir') else 1]}")
lines.append(f"\nruntime {time.time() - t0:.0f}s")
txt = "\n".join(lines)
print(txt)
with open(os.path.join(L.OUT, "calibration_real.txt"), "a") as f:
    f.write(txt + "\n\n")
