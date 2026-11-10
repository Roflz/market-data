"""
v3/signal_lab/reverse_feats.py - metrics known at a bar's CLOSE, for reverse-engineering big moves (2026-11-09).

features(b) -> DataFrame aligned to b.index (bar START time). Every column uses only bars up to and including the
row's own bar (rolling windows, cumulative within-session maxima, previous sessions). No full-sample statistics, so a
truncated frame gives identical values (the lab's look-ahead truncation test re-runs these functions).
All distances are in R20 units (R20 = mean high-low of the last 20 bars of the same contract run, as in lab.Panel).
"""
import numpy as np
import pandas as pd

TICK = {"ES": 0.25, "NQ": 0.25, "YM": 1.0}


def _r20(b):
    rng = (b.H - b.L)
    r = rng.groupby(b.run, sort=False).transform(lambda s: s.rolling(20, min_periods=20).mean())
    return r


def features(b):
    b = b.sort_index()
    C, O, Hh, L, V = b.C, b.O, b.H, b.L, b.V
    run, sess = b.run, b.session
    r20 = _r20(b)
    r20 = r20.where(r20 > 0)
    f = pd.DataFrame(index=b.index)
    gC = C.groupby(run, sort=False)
    # --- recent price action
    f["body1"] = (C - O) / r20                                     # last bar's body
    f["rng1"] = (Hh - L) / r20                                     # last bar's range vs average bar
    f["clv"] = ((C - L) / (Hh - L).where(Hh > L)) - 0.5           # close location in the bar (-0.5 low .. +0.5 high)
    f["ret4"] = (C - gC.shift(4)) / r20                            # last hour (15-min bars)
    f["ret16"] = (C - gC.shift(16)) / r20                          # last 4 hours
    sopen = O.groupby(sess, sort=False).transform("first")
    f["ret_sess"] = (C - sopen) / r20                              # since 18:00 open
    rng5 = (Hh - L).groupby(run, sort=False).transform(lambda s: s.rolling(5, min_periods=5).mean())
    f["r5_r20"] = rng5 / r20                                       # short-term vol expansion
    r100 = (Hh - L).groupby(run, sort=False).transform(lambda s: s.rolling(100, min_periods=60).mean())
    f["r20_r100"] = r20 / r100                                     # medium-term vol expansion
    # --- trend indicators (the user's EMAs / momentum / VWAP)
    f["d_ema8"] = (C - b.ema8) / r20
    f["d_ema20"] = (C - b.ema20) / r20
    f["d_ema50"] = (C - b.ema50) / r20
    f["slope20"] = (b.ema20 - b.ema20.groupby(run, sort=False).shift(4)) / r20
    f["stack"] = np.where((b.ema8 > b.ema20) & (b.ema20 > b.ema50), 1.0,
                          np.where((b.ema8 < b.ema20) & (b.ema20 < b.ema50), -1.0, 0.0))
    f.loc[b.ema50.isna(), "stack"] = np.nan
    f["mom14"] = b.mom14 / r20
    f["d_vwap"] = (C - b.vwap) / r20
    # --- day structure (high / low of day so far)
    hod = Hh.groupby(sess, sort=False).cummax()
    lod = L.groupby(sess, sort=False).cummin()
    f["pos_day"] = (C - lod) / (hod - lod).where(hod > lod) - 0.5
    f["d_hod"] = (hod - C) / r20
    f["d_lod"] = (C - lod) / r20
    f["day_rng"] = (hod - lod) / r20
    k = b.groupby(sess, sort=False).cumcount()
    newh = (Hh >= hod) & (k > 0)
    newl = (L <= lod) & (k > 0)
    f["new_hod"] = newh.astype(float) - newl.astype(float)        # +1 bar made a new high of day, -1 new low
    # --- previous session levels (same contract only)
    sg = b.groupby(sess, sort=False).agg(pc=("C", "last"), ph=("H", "max"), pl=("L", "min"), inst=("inst", "last"),
                                         so=("O", "first"), si=("inst", "first"))
    prev = sg[["pc", "ph", "pl", "inst"]].shift(1)
    same = prev.inst.eq(sg.si)
    for c in ("pc", "ph", "pl"):
        prev.loc[~same, c] = np.nan
    P = prev.reindex(sess.values)
    P.index = b.index
    f["d_pclose"] = (C - P.pc) / r20
    f["d_phigh"] = (C - P.ph) / r20
    f["d_plow"] = (C - P.pl) / r20
    gap = (sg.so - prev.pc).reindex(sess.values).to_numpy()
    f["gap"] = gap / r20
    # --- bar patterns
    pH, pL = Hh.groupby(run, sort=False).shift(1), L.groupby(run, sort=False).shift(1)
    f["inside"] = ((Hh <= pH) & (L >= pL)).astype(float)
    f["outside"] = ((Hh > pH) & (L < pL)).astype(float)
    sgn = np.sign(C - O)
    blk = (sgn != sgn.groupby(run, sort=False).shift(1)).groupby(run, sort=False).cumsum()
    f["streak"] = sgn * (sgn.groupby([run, blk], sort=False).cumcount() + 1)
    rng = Hh - L
    mn7 = rng.groupby(run, sort=False).transform(lambda s: s.rolling(7, min_periods=7).min())
    f["nr7"] = (rng <= mn7).astype(float)                         # narrowest bar of the last 7
    # --- participation
    pos = ((b.index.hour * 60 + b.index.minute - 18 * 60) % 1440).to_numpy()
    vmed = V.groupby(pos, sort=False).transform(lambda s: s.rolling(20, min_periods=10).median().shift(1))
    f["vol_rel"] = np.log(V / vmed.where(vmed > 0))               # log volume vs same time of day, last 20 sessions
    f["r20"] = r20
    return f


FEATS = ["body1", "rng1", "clv", "ret4", "ret16", "ret_sess", "r5_r20", "r20_r100", "d_ema8", "d_ema20", "d_ema50",
         "slope20", "stack", "mom14", "d_vwap", "pos_day", "d_hod", "d_lod", "day_rng", "new_hod", "d_pclose",
         "d_phigh", "d_plow", "gap", "inside", "outside", "streak", "nr7", "vol_rel"]
