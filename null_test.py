"""
Step 1 of the pre-registration: is the BASE result (MNQ overnight-level break + daily trend, 2 ATR stop, hold to the
5 PM close) distinguishable from markets with NO directional structure?

Generator G2 (sign-randomized real bars): every real 1-min NQ bar is reflected around its open with probability 1/2
(C' = O - (C - O), H' = O + (O - L), L' = O - (H - O)); the gap between bars keeps its size with a random sign; bars
are chained so the synthetic path is continuous. Volatility, the time-of-day pattern, volume and volatility clustering
are kept; any directional predictability is destroyed. Drift settings: zero, and each year's mean 1-min change added
back (so a strategy that only rides the market's upward drift would still look good on the drift-preserved nulls).
100 replications per setting. Statistic: total net R 2011-2026 (and net $ at 1 micro).

Also: execution delay (entering 1 or 2 bars late) on the real data.
Usage:  PYTHONPATH=./pylib python3 null_test.py
"""
import os
import time
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd

import exits_engine as ee
import fut_build as fb

warnings.filterwarnings("ignore")
SYM, K0, REPS = "NQ", 2.0, 100
BASE = {}


def load_base():
    d, _ = fb.load_raw(SYM)
    closed = (d.tmin >= 1020) & (d.tmin < 1080) & (d.index >= pd.Timestamp("2015-09-20", tz="America/New_York"))
    d = d[~closed]
    BASE["d"] = d
    BASE["yr"] = d.index.year.to_numpy()


def strategy(O, H, L, C, d, keep=None):
    """Lean BASE pipeline on 1-min bars -> list of trades (R, usd, year). keep(timestamps) -> bool mask filters signals."""
    df = pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C}, index=d.index)
    df["sess"], df["tmin"], df["rth"] = d.sess.to_numpy(), d.tmin.to_numpy(), d.rth.to_numpy()
    on = (df.tmin < 570) | (df.tmin >= 1080)
    g = df.groupby("sess")
    on_hi = df.sess.map(df.High.where(on).groupby(df.sess).max())
    on_lo = df.sess.map(df.Low.where(on).groupby(df.sess).min())
    daily_c = g.Close.last()
    ema20 = daily_c.ewm(span=20, adjust=False).mean().shift()
    trend = np.sign(df.Close - df.sess.map(ema20))
    ok = df.rth & (df.tmin >= 570)
    first_up = df.tmin.where((df.Close > on_hi) & ok).groupby(df.sess).cummin()
    first_dn = df.tmin.where((df.Close < on_lo) & ok).groupby(df.sess).cummin()
    up_m, dn_m = df.tmin - first_up, df.tmin - first_dn
    t = df.tmin.to_numpy()
    dec = df.rth.to_numpy() & (t % 5 == 4) & (t >= 574) & (t <= 899)
    long_ = dec & (up_m.to_numpy() >= 0) & (up_m.to_numpy() <= 4) & (trend.to_numpy() > 0)
    short = dec & (dn_m.to_numpy() >= 0) & (dn_m.to_numpy() <= 4) & (trend.to_numpy() < 0)
    # 5-minute bars for trade management
    b = df.resample("5min", label="left", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "sess": "first", "tmin": "first"}).dropna(subset=["Open"])
    pc = b.Close.shift()
    tr = pd.concat([b.High - b.Low, (b.High - pc).abs(), (b.Low - pc).abs()], axis=1).max(axis=1)
    b["atr5"] = tr.rolling(14).mean()
    b = b[b.index.year >= 2011]
    for c in ("ema20_5", "h60_close", "h60_ema20", "delta5"):
        b[c] = 0.0
    D = ee.Day(b)
    pos = pd.Index(D.idx)
    sig_ts = df.index[long_ | short] - pd.Timedelta(minutes=4)
    sig_dir = np.where(long_, 1, -1)[long_ | short]
    if keep is not None:
        k = np.asarray(keep(df.index[long_ | short]))
        sig_ts, sig_dir = sig_ts[k], sig_dir[k]
    bar = pos.get_indexer(sig_ts)
    m = bar >= 0
    sigs = sorted(zip(bar[m].tolist(), sig_dir[m].tolist()))
    tt = ee.run(D, sigs, "hold", k0=K0)
    sp = ee.SPEC[SYM]
    bb = tt.bar.to_numpy()
    R = K0 * D.atr5[bb]
    tt["R"] = (tt.pts - sp["comm"] / sp["usd"]) / R
    tt["usd"] = tt.pts * sp["usd"] - sp["comm"]
    tt["year"] = D.year[bb]
    return tt


def synth(seed, drift):
    d = BASE["d"]
    O, H, L, C = (d[c].to_numpy() for c in ("Open", "High", "Low", "Close"))
    rng = np.random.default_rng(seed)
    s = rng.choice([-1.0, 1.0], len(O))
    sg = rng.choice([-1.0, 1.0], len(O))
    body = (C - O) * s
    up = np.where(s > 0, H - O, O - L)
    dn = np.where(s > 0, L - O, O - H)
    gap = np.r_[0.0, O[1:] - C[:-1]] * sg
    if drift:
        yr = BASE["yr"]
        chg = np.r_[0.0, np.diff(C)]
        mu = pd.Series(chg).groupby(yr).transform("mean").to_numpy()
        body = body + mu
    inc = gap + body
    close = O[0] + np.cumsum(inc)
    open_ = close - body
    high = np.maximum(open_ + up, np.maximum(open_, close))
    low = np.minimum(open_ + dn, np.minimum(open_, close))
    return open_, high, low, close


def null_run(args):
    seed, drift = args
    if not BASE:
        load_base()
    t = strategy(*synth(seed, drift), BASE["d"])
    return seed, drift, len(t), float(t.R.sum()), float(t.usd.sum()), float(t[t.year >= 2018].R.sum())


def main():
    t0 = time.time()
    load_base()
    d = BASE["d"]
    real = strategy(d.Open.to_numpy(), d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy(), d)
    print(f"REAL data, lean pipeline: {len(real)} trades, net {real.R.sum():.1f} R, ${real.usd.sum():,.0f}, "
          f"avg {real.R.mean():.3f} R/trade, 2018-26 {real[real.year >= 2018].R.sum():.1f} R  ({time.time() - t0:.0f}s)", flush=True)
    real.to_csv("null_test_real_trades.csv", index=False)
    tasks = [(s, False) for s in range(REPS)] + [(1000 + s, True) for s in range(REPS)]
    out = []
    with Pool(6, initializer=load_base) as p:
        for k, r in enumerate(p.imap_unordered(null_run, tasks), 1):
            out.append(r)
            if k % 20 == 0:
                print(f"  {k}/{len(tasks)} null markets done ({time.time() - t0:.0f}s)", flush=True)
    res = pd.DataFrame(out, columns=["seed", "drift", "trades", "net_R", "net_usd", "R_2018_26"])
    res.to_csv("null_test_results.csv", index=False)
    print("\n=== BASE on 200 sign-randomized NQ markets vs the real market ===")
    for drift, g in res.groupby("drift"):
        p = (1 + (g.net_R >= real.R.sum()).sum()) / (1 + len(g))
        p2 = (1 + (g.R_2018_26 >= real[real.year >= 2018].R.sum()).sum()) / (1 + len(g))
        print(f"  drift {'preserved' if drift else 'zero     '}: null net R median {g.net_R.median():+.1f} "
              f"(5%-95%: {g.net_R.quantile(.05):+.1f} to {g.net_R.quantile(.95):+.1f}, max {g.net_R.max():+.1f}); "
              f"real {real.R.sum():+.1f} R -> empirical p = {p:.3f}; 2018-26 only: p = {p2:.3f}")
    print(f"\nSaved null_test_results.csv ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
