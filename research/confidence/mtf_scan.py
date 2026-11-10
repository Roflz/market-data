"""
Multi-timeframe agreement, raw (no model). Base = the 15-min pullback triggers (trigger_scan.py rules, both sides).
At the 15-min signal bar's CLOSE, using only 5-min and 60-min bars that have CLOSED by then (same contract):
  trend60   the last closed 60-min bar is in a trend the same way (EMA8 > EMA20 > EMA50, EMA50 rising; mirror for shorts)
  trig5     a 5-min pullback trigger (same rules) fired the same way in the last 6 five-minute bars (30 minutes)
  mom5      on the last closed 5-min bar, Momentum(14) rose (fell for shorts) and EMA8 is above (below) EMA20
  score     trend60 + trig5 + mom5 (0-3): how many of the other timeframes agree with the 15-min signal.
Exits (exit_study.simulate on the 1-minute path): the old 1.5R / 16 bars, and "stop only, hold to 16:45".
Writes out/mtf_trades_{sym}.parquet and out/mtf_scan.csv.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 -u mtf_scan.py [NQ ES YM]
"""
import gc
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

import exit_study as es
import features as fe
import labels as lb
import signals as sg
import trigger_scan as ts
import walkforward as wf

RULES = ["ema8_pb", "ema20_pb", "ema50_pb", "mom_turn", "pb_break"]
EXITS = ["1.5R target, 16 bars (old)", "stop only, hold to 16:45"]


def bars(sym, tf):
    b, ctx = fe._load(sym, tf)
    k = b.index < wf.HOLDOUT_SESSION_START
    return b.loc[k], ctx.loc[k]


def latest_closed(b_base, tf_base, b_h, tf_h, vals):
    """vals (len(b_h), m) of the latest higher/lower-tf bar of the SAME contract whose close <= the base bar's close
    (NaN if none). Same rule as features.htf_features."""
    vals = np.asarray(vals, np.float64).reshape(len(b_h), -1)
    out = np.full((len(b_base), vals.shape[1]), np.nan)
    close_t = (b_base.index + pd.Timedelta(minutes=tf_base)).to_numpy()
    close_h = (b_h.index + pd.Timedelta(minutes=tf_h)).to_numpy()
    inst, inst_h = b_base.inst.to_numpy(), b_h.inst.to_numpy()
    for u in np.unique(inst):
        r = np.flatnonzero(inst == u); rh = np.flatnonzero(inst_h == u)
        if not len(rh):
            continue
        j = np.searchsorted(close_h[rh], close_t[r], side="right") - 1
        ok = j >= 0
        out[r[ok]] = vals[rh[j[ok]]]
    return out


def trend_dir(ctx):
    """+1 / -1 / 0: EMA stack with EMA50 rising (falling) vs 5 bars earlier."""
    e8, e20, e50 = (ctx[c].to_numpy(np.float64) for c in ("ema8", "ema20", "ema50"))
    e50_5 = np.r_[np.full(5, np.nan), e50[:-5]]
    up = (e8 > e20) & (e20 > e50) & (e50 > e50_5)
    dn = (e8 < e20) & (e20 < e50) & (e50 < e50_5)
    return np.where(up, 1.0, np.where(dn, -1.0, 0.0))


def context_columns(sym, b15):
    tick = sg.SPEC[sym]["tick"]
    b60, c60 = bars(sym, 60)
    t60 = latest_closed(b15, 15, b60, 60, trend_dir(c60))[:, 0]
    b5, c5 = bars(sym, 5)
    ev5 = ts.detect(b5, c5, tick, 5)
    ev5 = ev5[ev5.rule != "trend_all"]
    n5 = len(b5)
    rec = {}
    for d in (1, -1):
        fired = np.zeros(n5); fired[ev5.loc[ev5.d == d, "i"].to_numpy()] = 1
        # any trigger in the last 6 five-minute bars of the same contract run
        roll = pd.Series(fired).groupby(b5.run.to_numpy()).transform(lambda s: s.rolling(6, min_periods=1).max())
        rec[d] = roll.to_numpy()
    mom = c5["mom14"].to_numpy(np.float64); dm = np.r_[np.nan, np.diff(mom)]
    e8, e20 = c5["ema8"].to_numpy(np.float64), c5["ema20"].to_numpy(np.float64)
    m5 = np.where((dm > 0) & (e8 > e20), 1.0, np.where((dm < 0) & (e8 < e20), -1.0, 0.0))
    V = latest_closed(b15, 15, b5, 5, np.column_stack([rec[1], rec[-1], m5]))
    del b5, c5, ev5; gc.collect()
    return dict(trend60=t60, trig5_long=V[:, 0], trig5_short=V[:, 1], mom5=V[:, 2])


def main(markets):
    out = []
    for sym in markets:
        t0 = time.time()
        tick = sg.SPEC[sym]["tick"]
        b15, c15 = bars(sym, 15)
        ev = ts.detect(b15, c15, tick, 15)
        ev = ev[ev.rule.isin(RULES)].reset_index(drop=True)
        C = context_columns(sym, b15)
        i, d = ev.i.to_numpy(), ev.d.to_numpy()
        ev["trend60"] = (C["trend60"][i] == d).astype(int)
        ev["trig5"] = (np.where(d > 0, C["trig5_long"][i], C["trig5_short"][i]) == 1).astype(int)
        ev["mom5"] = (C["mom5"][i] == d).astype(int)
        ev["score"] = ev.trend60 + ev.trig5 + ev.mom5
        m1 = lb.load_1m(sym); m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
        for name in EXITS:
            res, sel = es.simulate(sym, 15, b15, c15, ev, m1, *es.EXITS[name][:5])
            col = "pnl_old" if name.startswith("1.5R") else "pnl_hold"
            ev[col] = np.nan
            ev.loc[ev.index[sel], col] = res.pnl.to_numpy()
        ev["year"] = pd.DatetimeIndex(ev.t).year
        ev["market"] = sym
        ev.to_parquet(f"out/mtf_trades_{sym}.parquet", compression="zstd")
        out.append(ev)
        x = ev.assign(period=np.where(ev.year <= 2020, "2010-20", "2021-25"))
        p = x.pivot_table(index="score", columns="period", values=["pnl_old", "pnl_hold"], aggfunc="mean").round(2)
        p["trades/yr"] = (x.groupby("score").size() / x.year.nunique()).round(0)
        print(f"\n{sym}: {len(ev):,} 15-min triggers ({time.time() - t0:.0f}s); $/trade by agreement score\n{p.to_string()}",
              flush=True)
        del m1, b15, c15; fe.clear_cache(); gc.collect()
    A = pd.concat(out)
    A["period"] = np.where(A.year <= 2020, "2010-20", "2021-25")
    S = A.groupby(["market", "rule", "d", "score", "period"]).agg(
        n=("pnl_old", "size"), usd_old=("pnl_old", "mean"), usd_hold=("pnl_hold", "mean")).reset_index()
    S.to_csv("out/mtf_scan.csv", index=False)
    print("done", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["NQ", "ES", "YM"])
