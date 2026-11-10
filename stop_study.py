"""
Stop study for the overnight-break model (review items 1.1, 1.2 and 1.7). Specified 2026-11-08, before running.

Same entries for every variant (setup_rule.overnight_break: first close beyond the overnight high/low with the daily
trend, decisions 9:35-15:00 ET, Fed blackout), held to the 5 PM ET close unless stopped, 1 tick slippage per fill,
$1.00 per round trip, one position at a time, max 3 trades per session. Four stop variants (3 new trials):
  A0  current: resting stop 2 x ATR(14) of 5-min bars at the signal bar (at 9:35 that window is mostly pre-market)
  A1  item 1.2: resting stop 2 x TODV. TODV (time-of-day volatility) = average true range of the twelve 5-min bars
      after the signal's clock time (the trade's first hour), averaged over the previous 20 sessions (no same-day data)
  B   item 1.1, level stop: resting stop at the broken overnight level - 0.5 x TODV (+ for shorts); no trade when
      the entry fill is already back inside the range (the risk would come out under 0.5 x TODV)
  C   item 1.1, failed-breakout exit: A1 plus an exit at the close of the first 5-min bar that closes back inside
      the overnight range (below the overnight high for longs, above the overnight low for shorts)
Results (item 1.7) are in R = net $ / the trade's initial $ risk, i.e. as if every trade risks the same amount.
Dollars at a fixed 1 contract are shown for reference only. Paired tests compare day-level sums of R.
Usage:  PYTHONPATH=./pylib python3 stop_study.py   ->  stop_study_output.txt, stop_study_trades.csv
"""
import warnings

import numpy as np
import pandas as pd

import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
pd.set_option("display.width", 220)
K, BUF, WIN, LOOKBACK = 2.0, 0.5, 12, 20
VARIANTS = ["A0", "A1", "B", "C"]
NAME = {"A0": "A0 current (2 x ATR14)", "A1": "A1 2 x time-of-day vol", "B": "B  stop inside the level",
        "C": "C  A1 + close-back-inside exit"}
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def true_range(H, L, C):
    pc = np.r_[np.nan, C[:-1]]
    return np.fmax(H - L, np.fmax(np.abs(H - pc), np.abs(L - pc)))


def context(sym):
    """Per-bar time-of-day volatility (from prior sessions only) and per-session overnight high/low (6 PM-9:30 AM)."""
    b = pd.read_pickle(f"data/x5_{sym}.pkl")
    tr = true_range(b.High.to_numpy(), b.Low.to_numpy(), b.Close.to_numpy())
    day = pd.factorize(b.sess)[0]
    slot = (b.tmin.to_numpy() // 5).astype(int)
    M = np.full((day.max() + 1, 288), np.nan)                 # sessions x 5-min clock slots
    M[day, slot] = tr
    fwd = np.full_like(M, np.nan)
    for j in range(100, 200):                                 # signal bars run 9:30-14:55 (slots 114-179)
        fwd[:, j] = np.nanmean(M[:, j + 1:j + 1 + WIN], axis=1)
    hist = pd.DataFrame(fwd).rolling(LOOKBACK, min_periods=10).mean().shift(1).to_numpy()
    todv = pd.Series(hist[day, slot], index=b.index)
    on = (b.tmin >= 1080) | (b.tmin < 570)
    lv = b[on].groupby("sess").agg(on_hi=("High", "max"), on_lo=("Low", "min"))
    return todv, lv


def run_variant(sym, var, D, sigs, todv, lev):
    extra = {}
    for i, d in sigs:
        if var == "A1":
            extra[i] = dict(R_pts=K * todv[i])
        elif var == "B":
            extra[i] = dict(stop_px=lev[i] - d * BUF * todv[i], min_R=BUF * todv[i])
        elif var == "C":
            extra[i] = dict(R_pts=K * todv[i], level=lev[i])
    t = ee.run(D, sigs, "hold", k0=K, extra=extra)
    sp = ee.SPEC[sym]
    b = t.bar.to_numpy()
    t["R"] = (t.pts - sp["comm"] / sp["usd"]) / t.R_pts
    t["usd"] = t.pts * sp["usd"] - sp["comm"]
    t["risk_usd"] = t.R_pts * sp["usd"]
    t["year"], t["sess"], t["tmin"] = D.year[b], D.sess[b], D.tmin[b]
    t["variant"], t["market"] = var, sp["micro"]
    return t


def summary(t):
    yr = t.groupby("year").R.sum()
    daily = t.groupby("sess").R.sum()
    early, late = t[t.year <= 2017], t[t.year >= 2018]
    return {"trades": len(t), "win %": 100 * (t.R > 0).mean(), "stopped %": 100 * (t.exit == "stop").mean(),
            "avg R": t.R.mean(), "total R": t.R.sum(), "t": daily.mean() / (daily.std() / np.sqrt(len(daily))),
            "years up": f"{int((yr > 0).sum())}/{len(yr)}", "avg R 2011-17": early.R.mean(),
            "avg R 2018-26": late.R.mean(), "$ at 1 contract": t.usd.sum(), "median risk $": t.risk_usd.median()}


def paired(t, base):
    a, b = t.groupby("sess").R.sum(), base.groupby("sess").R.sum()
    days = a.index.union(b.index)
    dlt = a.reindex(days, fill_value=0.0) - b.reindex(days, fill_value=0.0)
    ya, yb = t.groupby("year").R.sum(), base.groupby("year").R.sum()
    yrs = ya.index.union(yb.index)
    better = int((ya.reindex(yrs, fill_value=0.0) > yb.reindex(yrs, fill_value=0.0)).sum())
    return {"R difference": dlt.sum(), "t of difference": dlt.mean() / (dlt.std() / np.sqrt(len(dlt))),
            "years better": f"{better}/{len(yrs)}"}


def main():
    ec.init()
    trades = []
    for sym in ("NQ", "ES"):
        micro = ee.SPEC[sym]["micro"]
        D = ec.G[sym]
        all_sigs = ec.G[("sets", sym)]["Overnight break + daily trend"]
        todv_s, lv = context(sym)
        todv = todv_s.reindex(D.idx).to_numpy()
        sess = pd.Series(D.sess)
        hi, lo = sess.map(lv.on_hi).to_numpy(), sess.map(lv.on_lo).to_numpy()
        lev = {i: (hi[i] if d > 0 else lo[i]) for i, d in all_sigs}
        sigs = [(i, d) for i, d in all_sigs if np.isfinite(todv[i]) and np.isfinite(lev[i])]
        say(f"\n######## {micro}: overnight break + daily trend, hold to 5 PM, 2011-2026 ########")
        say(f"Signals: {len(all_sigs)}; with time-of-day volatility and the overnight level available: {len(sigs)}")
        chk = run_variant(sym, "A0", D, all_sigs, todv, lev)
        say(f"Reproduction check, A0 on all signals with the updated engine: {len(chk)} trades, {chk.R.sum():.2f} R, "
            f"${chk.usd.sum():,.1f} at 1 contract")

        res = {v: run_variant(sym, v, D, sigs, todv, lev) for v in VARIANTS}
        trades += list(res.values())

        # 1.2: how big is each stop measure next to the 5-min bars the trade actually meets in its first hour?
        trD = true_range(D.High, D.Low, D.Close)
        rows = []
        for i, d in sigs:
            j = np.arange(i + 1, min(i + 1 + WIN, D.n))
            j = j[D.day[j] == D.day[i]]
            if len(j):
                rows.append((D.tmin[i] // 60, D.atr5[i] / trD[j].mean(), todv[i] / trD[j].mean()))
        r = pd.DataFrame(rows, columns=["hour", "ATR14", "TODV"])
        tab = r.groupby("hour").agg(signals=("ATR14", "size"), ATR14=("ATR14", "median"), TODV=("TODV", "median"))
        for v in ("A0", "A1"):
            t = res[v]
            early_stop = (t.exit == "stop") & (t.hold_bars <= WIN)
            tab[f"{v} stopped in 1st hour %"] = (100 * early_stop.groupby(t.tmin // 60).mean()).reindex(tab.index)
        say("\n1.2  Stop measure / average size of the next hour's actual 5-min bars (median, by signal hour ET).")
        say("     1.0 = the measure matches what the trade meets; below 1 = the stop is tighter than it looks.")
        say(tab.round(2).to_string())

        # variants, normalized (R) and at 1 contract
        say("\nVariants (R = net $ / initial $ risk, so every trade risks the same amount; $ at 1 contract for reference)")
        s = pd.DataFrame({NAME[v]: summary(res[v]) for v in VARIANTS}).T
        say(s.to_string(float_format=lambda x: f"{x:,.3f}" if abs(x) < 10 else f"{x:,.1f}"))
        say("\nPaired differences in R (day-level sums; t of the daily difference; years with more R than the base)")
        p = pd.DataFrame({f"{NAME[v]} vs {NAME[b][:2]}": paired(res[v], res[b])
                          for v, b in (("A1", "A0"), ("B", "A0"), ("C", "A0"), ("B", "A1"), ("C", "A1"))}).T
        say(p.to_string(float_format=lambda x: f"{x:,.2f}"))

        # 1.1: trades that closed back inside the range, versus holding them with the same stop (C vs A1)
        a1, c = res["A1"].set_index("bar"), res["C"].set_index("bar")
        common = a1.index.intersection(c.index)
        cut = c.loc[common][c.loc[common].exit == "level"].index
        held = a1.loc[cut]
        say(f"\n1.1  Variant C exited {len(cut)} of {len(common)} shared trades on a close back inside the range.")
        say(f"     Those trades averaged {c.loc[cut].R.mean():+.3f} R with the exit and {held.R.mean():+.3f} R if held "
            f"(A1); {int((held.R >= 2).sum())} of them were +2R or better winners when held "
            f"({held.R[held.R >= 2].sum():.1f} R of A1's {res['A1'].R.sum():.1f} R total).")
        say(f"     Variant B took {len(res['B'])} trades vs {len(res['A1'])} for A1 (it skips entries already back "
            f"inside the range; the rest is one-position-at-a-time).")

        # robustness checks (added after the first run; not new variants): where A0 and A1 differ, and costlier fills
        say("\nRobustness (added after the first run). A0 vs A1 by signal hour (ET): trades, avg R, $ at 1 contract")
        hh = {v: res[v].assign(hour=res[v].tmin // 60).groupby("hour").agg(trades=("R", "size"), avg_R=("R", "mean"),
                                                                            usd=("usd", "sum")) for v in ("A0", "A1")}
        say(pd.concat(hh, axis=1).round(3).to_string())
        say("\nSlippage per fill (ticks), every fill: total R, avg R and $ at 1 contract")
        rows = {}
        for ticks in (1, 2, 3):
            ee.SLIP = 0.25 * ticks
            for v in ("A0", "A1"):
                t = run_variant(sym, v, D, sigs, todv, lev)
                rows[f"{NAME[v]}, {ticks} tick"] = {"total R": t.R.sum(), "avg R": t.R.mean(), "t": summary(t)["t"],
                                                    "$ at 1 contract": t.usd.sum()}
        ee.SLIP = 0.25
        say(pd.DataFrame(rows).T.to_string(float_format=lambda x: f"{x:,.3f}" if abs(x) < 10 else f"{x:,.1f}"))

    pd.concat(trades, ignore_index=True)[["market", "variant", "bar", "sess", "year", "tmin", "dir", "exit", "hold_bars",
                                          "pts", "R_pts", "R", "usd", "risk_usd"]].to_csv("stop_study_trades.csv",
                                                                                         index=False)
    open("stop_study_output.txt", "w").write("\n".join(OUT) + "\n")
    say("\nSaved stop_study_output.txt and stop_study_trades.csv")


if __name__ == "__main__":
    main()
