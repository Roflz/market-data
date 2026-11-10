"""
Stress test for the overnight-level break + daily-trend setup (MNQ, with MES for comparison).

  A. Parameter neighborhood: initial stop x trailing width x break freshness x trend filter x trades/day.
     A real edge should be a broad plateau, not one lucky spike.
  B. Costs: 1-4 ticks slippage per side, $1.00 / $2.00 commission.
  C. Stability: results in risk units (R) per year, first half vs second half, by volatility regime, time of day, weekday.
  D. Monte Carlo (block bootstrap by month): distribution of yearly P&L, max drawdown, chance of a losing year.
  E. Overfitting statistics:
       Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014) for N = 70 / 980 / 5000 trials
       Probability of Backtest Overfitting via CSCV (Bailey, Borwein, Lopez de Prado & Zhu) over the 70 exit x stop
       variants of this setup.
Usage:  PYTHONPATH=./pylib python3 stress_test.py
"""
import itertools
import warnings

import numpy as np
import pandas as pd
from scipy.stats import norm

import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
ec.init()
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


def signals(sym, fresh=4, trend="ema20", both=False):
    D = ec.G[sym]
    F = pd.read_pickle(f"data/fut_features_{sym}.pkl")
    X = F["X"]
    bar = D.pos.get_indexer(pd.DatetimeIndex(F["ts"]) - pd.Timedelta(minutes=4))
    tr = {"ema20": np.sign(X.day_vs_ema20), "ret5d": np.sign(X.ret_5d), "none": np.ones(len(X))}[trend]
    up = (X.on_break_up_mins >= 0) & (X.on_break_up_mins <= fresh)
    dn = (X.on_break_down_mins >= 0) & (X.on_break_down_mins <= fresh)
    if trend == "none":
        sig = np.where(up, 1, np.where(dn, -1, 0))
    else:
        sig = np.where(up & (tr > 0), 1, np.where(dn & (tr < 0), -1, 0))
    m = (sig != 0) & (bar >= 0)
    return sorted(zip(bar[m].tolist(), sig[m].tolist()))


def trades(sym, rule="trail_6", k0=2.0, fresh=4, trend="ema20", per_day=3, slip_ticks=1, comm=None):
    D, sp = ec.G[sym], ee.SPEC[sym]
    ee.SLIP = 0.25 * slip_ticks
    t = ee.run(D, signals(sym, fresh, trend), rule, k0=k0, max_per_day=per_day)
    ee.SLIP = 0.25
    c = sp["comm"] if comm is None else comm
    b = t.bar.to_numpy()
    t["usd"] = t.pts * sp["usd"] - c
    t["R"] = (t.pts - c / sp["usd"]) / (k0 * D.atr5[b])
    t["year"], t["sess"], t["tmin"] = D.year[b], D.sess[b], D.tmin[b]
    return t


def summary(t):
    yr = t.groupby("year").R.mean()
    return dict(trades=len(t), net=t.usd.sum(), R_per_trade=t.R.mean(),
                t_stat=t.R.mean() / (t.R.std() / np.sqrt(len(t))), years_up=int((yr > 0).sum()), years=len(yr),
                y2026=t[t.year == 2026].usd.sum())


for sym in ("NQ", "ES"):
    micro = ee.SPEC[sym]["micro"]
    say(f"\n################ {micro}: overnight-level break + daily trend ################")
    # ---------------- A. parameter neighborhood
    say("\nA. Parameter neighborhood: avg R per trade (after costs) by initial stop (rows) x exit (cols); "
        "break within 5 min, daily EMA20 trend, max 3 trades/day")
    grid = {}
    for k0 in (1, 1.5, 2, 2.5, 3, 4, 6):
        for rule in ("trail_3", "trail_4", "trail_6", "hold", "ema60"):
            grid[(k0, rule)] = summary(trades(sym, rule, k0))
    g = pd.DataFrame(grid).T
    say(g.R_per_trade.unstack().round(3).to_string())
    say(f"  share of the {len(g)} stop x exit cells with positive R: {(g.R_per_trade > 0).mean():.0%}; "
        f"with t > 2: {(g.t_stat > 2).mean():.0%}")
    say("\nA2. Entry-rule variations (exit trail_6, stop 2): break freshness x trend filter x trades/day")
    rows = []
    for fresh, trend, pdmax in itertools.product((4, 9, 14), ("ema20", "ret5d", "none"), (1, 3)):
        s = summary(trades(sym, "trail_6", 2.0, fresh, trend, pdmax))
        rows.append({"break within (min)": fresh + 1, "trend filter": trend, "max/day": pdmax, **s})
    say(pd.DataFrame(rows).round(3).to_string(index=False))

    # ---------------- B. costs
    say("\nB. Cost sensitivity (trail_6, stop 2): net $ 2011-2026 and avg R")
    rows = []
    for slip in (1, 2, 3, 4):
        for comm in (1.0, 2.0):
            s = summary(trades(sym, slip_ticks=slip, comm=comm))
            rows.append({"slippage ticks/side": slip, "commission $": comm, **s})
    say(pd.DataFrame(rows).round(3).to_string(index=False))

    # ---------------- C. stability
    base = trades(sym)
    say("\nC. Stability (trail_6, stop 2)")
    halves = {"2011-2017": base[base.year <= 2017], "2018-2026": base[base.year >= 2018]}
    for k, v in halves.items():
        s = summary(v)
        say(f"  {k}: {s['trades']} trades, avg {s['R_per_trade']:.3f} R, t={s['t_stat']:.2f}, net ${s['net']:,.0f}")
    b5 = pd.read_pickle(f"data/x5_{sym}.pkl")
    vr = (b5.atr5 / (b5.d_atr / 15)).reindex(ec.G[sym].idx[base.bar]).to_numpy()
    base["vol_tercile"] = pd.qcut(vr, 3, labels=["quiet", "normal", "volatile"])
    base["hour"] = (base.tmin // 60).astype(int)
    base["weekday"] = pd.DatetimeIndex(ec.G[sym].idx[base.bar]).day_name().str[:3]
    for col in ("vol_tercile", "hour", "weekday"):
        say(f"  by {col}: " + ", ".join(f"{k}: {v.R.mean():+.3f}R (n={len(v)})" for k, v in base.groupby(col)))

    # ---------------- D. Monte Carlo
    say("\nD. Monte Carlo, 10,000 simulated years (block bootstrap of whole months from 2018-2026 and from all years)")
    for label, src in (("2018-2026", base[base.year >= 2018]), ("2011-2026", base)):
        mon = src.assign(m=pd.DatetimeIndex(ec.G[sym].idx[src.bar]).to_period("M")).groupby("m")
        months = [g.usd.to_numpy() for _, g in mon]
        rng = np.random.default_rng(0)
        yearly, dds = [], []
        for _ in range(10000):
            seq = np.concatenate([months[j] for j in rng.integers(0, len(months), 12)])
            eq = np.cumsum(seq)
            yearly.append(eq[-1] if len(eq) else 0)
            dds.append((np.maximum.accumulate(np.r_[0, eq]) - np.r_[0, eq]).max())
        yearly, dds = np.array(yearly), np.array(dds)
        say(f"  sampling {label}: yearly P&L median ${np.median(yearly):,.0f} (5%: ${np.percentile(yearly, 5):,.0f}, "
            f"95%: ${np.percentile(yearly, 95):,.0f}); P(losing year) {np.mean(yearly < 0):.0%}; "
            f"max drawdown median ${np.median(dds):,.0f}, 95th pct ${np.percentile(dds, 95):,.0f}")
    risk_usd = (2.0 * ec.G[sym].atr5[base.bar] * ee.SPEC[sym]["usd"])
    say(f"  initial risk per trade at 1 micro: median ${np.median(risk_usd):.0f} "
        f"(2024-26: ${np.median(risk_usd[base.year >= 2024]):.0f}); for 1% risk per trade that implies an account of "
        f"about ${np.median(risk_usd[base.year >= 2024]) * 100:,.0f}")

    # ---------------- E. overfitting statistics
    say("\nE. Overfitting statistics")
    sess_all = pd.Index(np.unique(ec.G[sym].sess))
    daily = {}
    for k0 in ec.STOPS:
        for rule in ee.EXITS:
            t = trades(sym, rule, float(k0))
            daily[(rule, k0)] = t.groupby("sess").R.sum().reindex(sess_all, fill_value=0.0)
    M = pd.DataFrame(daily)                                     # sessions x 70 variants, daily R
    sr = M.mean() / M.std()                                     # per-session Sharpe of each variant
    best = ("trail_6", 2)
    x = M[best].to_numpy()
    T = len(x)
    srh = x.mean() / x.std()
    sk = pd.Series(x).skew()
    ku = pd.Series(x).kurt() + 3
    var_sr = sr.var()
    for N in (70, 980, 5000):
        g_ = 0.5772156649
        sr0 = np.sqrt(var_sr) * ((1 - g_) * norm.ppf(1 - 1 / N) + g_ * norm.ppf(1 - 1 / (N * np.e)))
        dsr = norm.cdf((srh - sr0) * np.sqrt(T - 1) / np.sqrt(1 - sk * srh + (ku - 1) / 4 * srh ** 2))
        say(f"  Deflated Sharpe, N={N:5d} trials: observed per-session SR {srh:.4f} (annualized {srh * np.sqrt(252):.2f}), "
            f"expected best-of-N by luck {sr0:.4f} -> probability the true SR > 0 = {dsr:.3f}")
    # CSCV / PBO
    S = 16
    blocks = np.array_split(np.arange(T), S)
    Mv = M.to_numpy()
    logits = []
    for comb in itertools.combinations(range(S), S // 2):
        is_idx = np.concatenate([blocks[i] for i in comb])
        oos_idx = np.concatenate([blocks[i] for i in range(S) if i not in comb])
        is_sr = Mv[is_idx].mean(0) / Mv[is_idx].std(0)
        oos_sr = Mv[oos_idx].mean(0) / Mv[oos_idx].std(0)
        j = int(np.argmax(is_sr))
        rank = (oos_sr < oos_sr[j]).mean() + 0.5 / len(oos_sr)
        logits.append(np.log(rank / (1 - rank)))
    logits = np.array(logits)
    say(f"  Probability of Backtest Overfitting (CSCV, 16 blocks, {len(logits)} splits, 70 variants): "
        f"{np.mean(logits <= 0):.2f}  (median out-of-sample rank of the in-sample best: "
        f"{1 / (1 + np.exp(-np.median(logits))):.2f}; 0.5 = coin flip, 1.0 = always the best)")
    say(f"  share of the 70 variants with positive total R: {(M.sum() > 0).mean():.0%}")

open("stress_test_output.txt", "w").write("\n".join(OUT))
