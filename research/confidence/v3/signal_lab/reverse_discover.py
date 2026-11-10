"""
v3/signal_lab/reverse_discover.py - DISCOVERY HALF ONLY (sessions 2010-2017): what did the metrics look like at the
bar BEFORE big moves, compared with ordinary bars matched on market, time-of-day slot and volatility decile?

Big moves (per market, 15-min bars, decision = a bar's close, entry = next bar's open, as in lab.Panel):
  H1   : forward 1-hour move (dir_h4) whose size |move| / R20 is in the top 5% of its 15-min time-of-day slot
  EOD  : move to the 16:45 close (dir_eod) in the top 5% of its slot
  TDAY : strong trend day: decision bar 09:15-09:30 ET, |move to 16:45| / R20 in the top 15% of sessions AND
         |move| >= 0.6 x the 09:30-16:45 range (the day closes near its extreme)
Matched comparison: each metric is standardised WITHIN its stratum (market x slot x volatility decile) over all bars
of the stratum, so a big-move bar is only compared with bars of the same market, time of day and volatility.
  size_smd   = mean z on big-move bars - mean z on the other bars          (metric different before ANY big move?)
  abs_smd    = the same on |z| (metric unusually EXTREME, either sign, before big moves?)
  dir_smd    = mean z before big UP moves - mean z before big DOWN moves  (does it tell the DIRECTION?)
  all_ic     = rank correlation of the metric with the forward move over ALL bars (what a trader could use)
Stability: every number is also computed per calendar year (2010-2017); yrs_same = years with the full-period sign,
t_yr = mean / sd * sqrt(n years). ES and NQ separately (YM has no 2010-17 data: it is a fully fresh market later).
"""
import os
import sys
import time

import numpy as np
import pandas as pd
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness as H  # noqa: E402
import lab as L  # noqa: E402
import reverse_feats as RF  # noqa: E402

OUT = os.path.join(HERE, "out", "reverse")
DISC_END = pd.Timestamp("2018-01-01")


def disc_bars(sym, tf=15):
    b = H.bars(sym, tf)
    return b[pd.DatetimeIndex(b.session) < DISC_END]


def ystat(vals):
    v = np.asarray(vals, float)
    v = v[np.isfinite(v)]
    if len(v) < 3:
        return np.nan, 0, len(v)
    m = v.mean()
    t = m / (v.std(ddof=1) / np.sqrt(len(v))) if v.std(ddof=1) > 0 else np.nan
    return t, int((np.sign(v) == np.sign(m)).sum()), len(v)


def zscore_within(x, strat):
    s = pd.Series(x)
    g = s.groupby(strat)
    mu, sd = g.transform("mean"), g.transform("std")
    return ((s - mu) / sd.where(sd > 0)).to_numpy()


def analyse(sym):
    t0 = time.time()
    b = disc_bars(sym)
    P = L.Panel(b, sym, 15, n_boot=10)
    F = RF.features(b).reindex(P.bars.index)
    ok = P.ok.copy()
    ts = P.bars.index
    mins = ((ts.hour * 60 + ts.minute).to_numpy() - 18 * 60) % 1440
    slot = mins // 15
    med = pd.Series(P.r20).rolling(100, min_periods=50).median().to_numpy()
    vr = P.r20 / med
    qs = np.nanquantile(vr[ok], np.linspace(0.1, 0.9, 9))
    vol = np.where(np.isfinite(vr), np.searchsorted(qs, vr), -1)
    ok &= vol >= 0
    year = pd.DatetimeIndex(P.bars.session).year.to_numpy()
    strat = np.where(ok, slot * 100 + vol, -1)
    Y = {k: P.Y[:, L.COL[k]] for k in ("dir_h4", "dir_eod", "rng_eod")}
    moves = {}
    for k, nm in (("dir_h4", "H1"), ("dir_eod", "EOD")):
        a = np.abs(Y[k])
        thr = pd.Series(np.where(ok, a, np.nan)).groupby(slot).transform(lambda s: s.quantile(0.95)).to_numpy()
        big = ok & np.isfinite(a) & (a >= thr)
        moves[nm] = (big, np.sign(Y[k]), ok & np.isfinite(a), Y[k])
    # trend days: decision bar = the bar starting 09:15 ET (pos 61 on 15-min bars)
    t915 = ok & (mins == (9 * 60 + 15 - 18 * 60) % 1440)
    a = np.abs(Y["dir_eod"])
    qual = a / Y["rng_eod"]
    thr = np.nanquantile(a[t915], 0.85)
    td = t915 & (a >= thr) & (qual >= 0.6)
    moves["TDAY"] = (td, np.sign(Y["dir_eod"]), t915 & np.isfinite(a), Y["dir_eod"])
    rows = []
    for mv, (big, sgn, base, fwd) in moves.items():
        for feat in RF.FEATS:
            x = F[feat].to_numpy(np.float64)
            use = base & np.isfinite(x)
            st = np.where(use, strat, -1)
            z = zscore_within(np.where(use, x, np.nan), st)
            use &= np.isfinite(z)
            bg, od = use & big, use & ~big
            up, dn = bg & (sgn > 0), bg & (sgn < 0)
            az = np.abs(z)
            r = dict(sym=sym, move=mv, feat=feat, n_big=int(bg.sum()), n_up=int(up.sum()), n_dn=int(dn.sum()),
                     n_ord=int(od.sum()), size_smd=np.nanmean(z[bg]) - np.nanmean(z[od]),
                     abs_smd=np.nanmean(az[bg]) - np.nanmean(az[od]),
                     dir_smd=np.nanmean(z[up]) - np.nanmean(z[dn]))
            # rank IC with the forward move over all usable bars (by year too)
            xr = np.full(len(x), np.nan)
            xr[use] = z[use]
            ics, ys, ds, ss, as_ = [], [], [], [], []
            for yv in np.unique(year[use]):
                m = use & (year == yv) & np.isfinite(fwd)
                if m.sum() < 200 or (m & up).sum() < 5 or (m & dn).sum() < 5:
                    continue
                ics.append(np.corrcoef(rankdata(z[m]), rankdata(fwd[m]))[0, 1])
                ds.append(np.nanmean(z[m & up]) - np.nanmean(z[m & dn]))
                ss.append(np.nanmean(z[m & big]) - np.nanmean(z[m & ~big]))
                as_.append(np.nanmean(az[m & big]) - np.nanmean(az[m & ~big]))
                ys.append(yv)
            m = use & np.isfinite(fwd)
            r["all_ic"] = np.corrcoef(rankdata(z[m]), rankdata(fwd[m]))[0, 1]
            # does the metric's top fifth (within stratum) move in its direction on ALL bars? (forward move in R20)
            qhi, qlo = np.nanquantile(z[m], 0.8), np.nanquantile(z[m], 0.2)
            r["all_top_minus_bot"] = np.nanmean(fwd[m & (z > qhi)]) - np.nanmean(fwd[m & (z <= qlo)])
            for nm, v in (("dir", ds), ("size", ss), ("abs", as_), ("ic", ics)):
                t, same, ny = ystat(v)
                r[f"{nm}_t_yr"], r[f"{nm}_yrs_same"] = t, same
            r["years"] = len(ys)
            rows.append(r)
    D = pd.DataFrame(rows)
    print(f"[disc] {sym}: {len(b)} bars, moves H1={moves['H1'][0].sum()} EOD={moves['EOD'][0].sum()} "
          f"TDAY={moves['TDAY'][0].sum()} ({time.time() - t0:.0f}s)", flush=True)
    return D


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    D = pd.concat([analyse(s) for s in ("ES", "NQ")], ignore_index=True)
    D.to_csv(os.path.join(OUT, "discovery_2010_17.csv"), index=False)
    pd.set_option("display.width", 250, "display.max_rows", 400, "display.max_columns", 30)
    cols = ["feat", "n_big", "size_smd", "size_t_yr", "abs_smd", "abs_t_yr", "dir_smd", "dir_t_yr", "dir_yrs_same",
            "all_ic", "ic_t_yr", "ic_yrs_same", "all_top_minus_bot"]
    for (s, mv), g in D.groupby(["sym", "move"]):
        print(f"\n=== {s} {mv} ===")
        print(g[cols].sort_values("dir_t_yr", key=np.abs, ascending=False).round(3).to_string(index=False))
