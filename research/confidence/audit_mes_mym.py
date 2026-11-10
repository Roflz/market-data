"""Quick audit of the MES / MYM data and labels.
1) 25 random entry labels per market recomputed by hand from the 1-minute bars (independent simple loop).
2) Data checks: bars per session by year, price jumps within a contract, flat/zero-volume bars, events per year.
  python3 audit_mes_mym.py ES   (or YM / NQ)"""
import sys
import warnings

import numpy as np
import pandas as pd

import exits as ex
import labels as lb
import signals as sg

warnings.filterwarnings("ignore")
SYM = sys.argv[1]
spec = sg.SPEC[SYM]; tick, usd, cost = spec["tick"], spec["usd"], spec["cost"]
b = sg.bars(SYM, 15)
_, forced = ex.session_frame(b, 15)
m1 = lb.load_1m(SYM)
E = pd.read_parquet(f"out/entries_{SYM}_15.parquet", columns=["t", "i", "d", "stop", "entry", "pnl_usd_1.5",
                                                              "exit_kind_1.5"])
rng = np.random.default_rng(7)
S = E.iloc[np.sort(rng.choice(len(E), 25, replace=False))]
bad = 0
for _, r in S.iterrows():
    i, d, stop = int(r.i), int(r.d), float(r.stop)
    e = i + 1; T = min(i + 16, forced[i])
    t_from, t_to = b.index[e], b.index[T] + pd.Timedelta(minutes=15)
    inst = b.inst.iloc[e]
    M = m1[(m1.index >= t_from) & (m1.index < t_to) & (m1.inst == inst)]
    entry = M.O.iloc[0]; risk = d * (entry - stop)
    if risk < 0:
        pnl, kind = -cost, "stop"
    else:
        tgt = entry + d * 1.5 * risk; xp = None; kind = "time"
        for _, m in M.iterrows():
            if (d > 0 and m.L <= stop) or (d < 0 and m.H >= stop):
                xp = (min(m.O, stop) - tick) if d > 0 else (max(m.O, stop) + tick); kind = "stop"; break
            if (d > 0 and m.H >= tgt + tick) or (d < 0 and m.L <= tgt - tick):
                xp = tgt; kind = "target"; break
        if xp is None:
            xp = M.C.iloc[-1]
        pnl = d * (xp - entry) * usd - cost
    ok = abs(pnl - r["pnl_usd_1.5"]) < 1e-6 and abs(entry - r.entry) < 1e-9 and kind == r["exit_kind_1.5"]
    bad += not ok
    if not ok:
        print(f"MISMATCH {r.t} d={d}: hand entry {entry} pnl {pnl:+.2f} {kind} | stored entry {r.entry} "
              f"pnl {r['pnl_usd_1.5']:+.2f} {r['exit_kind_1.5']}")
print(f"{SYM}: labels recomputed by hand: {25 - bad}/25 match")

# data checks
y = b.index.year
per_sess = b.groupby([y, b.sess]).size().groupby(level=0).median()
same = (b.inst.to_numpy()[1:] == b.inst.to_numpy()[:-1])
jump = np.abs(b.O.to_numpy()[1:] - b.C.to_numpy()[:-1])
R = (b.H - b.L).rolling(20).mean().to_numpy()[:-1]
big = same & (jump > 10 * np.nan_to_num(R, nan=np.inf))
flat = (b.H == b.L)
ev = pd.DatetimeIndex(E.t).year.value_counts().sort_index()
print(f"{SYM}: median 15-min bars per session by year: {per_sess.astype(int).to_dict()}")
print(f"{SYM}: bar-to-bar jumps > 10 average bars within a contract: {int(big.sum())} "
      f"(largest {jump[same].max():.2f} pts on {b.index[1:][same][np.argmax(jump[same])]})")
print(f"{SYM}: flat bars: {flat.mean():.2%}; zero-volume bars: {(b.V == 0).mean():.2%}")
print(f"{SYM}: entry events per year: {ev.to_dict()}")
