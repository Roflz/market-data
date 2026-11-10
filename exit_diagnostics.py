"""
Where does the overnight-break setup make and lose money, and what would different exit timing / management do?
Same entries for every row (2 ATR initial stop, flat at the 5 PM ET close at the latest), 1 micro, after costs.
Usage:  PYTHONPATH=./pylib python3 exit_diagnostics.py
"""
import warnings

import numpy as np
import pandas as pd

import exits_compare as ec
import exits_engine as ee

warnings.filterwarnings("ignore")
pd.set_option("display.width", 230)
ec.init()
SETUP = "Overnight break + daily trend"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def evalrule(sym, rule, k0=2.0, setname=SETUP):
    D, sp = ec.G[sym], ee.SPEC[sym]
    t = ee.run(D, ec.G[("sets", sym)][setname], rule, k0=k0)
    b = t.bar.to_numpy()
    t["usd"] = t.pts * sp["usd"] - sp["comm"]
    t["R"] = (t.pts - sp["comm"] / sp["usd"]) / (k0 * D.atr5[b])
    t["year"] = D.year[b]
    yr = t.groupby("year").R.mean()
    late = t[t.year >= 2018]
    return dict(rule=rule, trades=len(t), net=t.usd.sum(), R_tr=t.R.mean(), t=t.R.mean() / (t.R.std() / np.sqrt(len(t))),
                yrs_up=f"{int((yr > 0).sum())}/{len(yr)}", R_2018_26=late.R.mean(), net_2026=t[t.year == 2026].usd.sum(),
                win=(t.usd > 0).mean(), hold_h=t.hold_bars.mean() * 5 / 60), t


for sym in ("NQ", "ES"):
    micro = ee.SPEC[sym]["micro"]
    say(f"\n########## {micro} | {SETUP} | initial stop 2 x ATR(5m) ##########")
    base, bt = evalrule(sym, "hold")
    groups = {
        "1. Exit at a fixed clock time (ET) instead of holding to 5 PM":
            [f"clock_{m}" for m in (600, 630, 660, 690, 720, 780, 840, 900, 960)] + ["hold"],
        "2. Exit after a fixed time in the trade": [f"after_{n}" for n in (15, 30, 60, 90, 120, 180, 240, 360)] + ["hold"],
        "3. Time stop: at N minutes, exit if open profit < x R, otherwise hold to 5 PM":
            [f"tstop_{n}_{x}" for n in (30, 60, 90, 120) for x in (0, 0.5, 1)] + ["hold"],
        "4. Profit lock: once best open profit >= m R, stop to breakeven and trail j ATR (j=0: breakeven only)":
            [f"lock_{m}_{j}" for m in (1, 1.5, 2, 3) for j in (0, 1, 2, 3)] + ["hold", "trail_6"],
    }
    for title, rules in groups.items():
        say(f"\n{title}")
        say(pd.DataFrame([evalrule(sym, r)[0] for r in rules]).round(3).to_string(index=False))

    # 5. anatomy of the hold policy
    D = ec.G[sym]
    held = bt[bt.exit == "close"]
    stopped = bt[bt.exit == "stop"]
    say(f"\n5. Anatomy of 'hold' ({len(bt)} trades)")
    say(f"  held to 5 PM: {len(held)} trades; final result avg {held.R.mean():.2f}R vs best open profit avg {held.mfe_R.mean():.2f}R "
        f"-> gave back {(held.mfe_R - held.R).mean():.2f}R on average; "
        f"{((held.mfe_R - held.R) > 0.5 * held.mfe_R.clip(lower=1e-9)).mean():.0%} gave back more than half of their best")
    say(f"  stopped out: {len(stopped)} trades; {(stopped.mfe_R >= 0.5).mean():.0%} had been up >= 0.5R first, "
        f"{(stopped.mfe_R >= 1).mean():.0%} >= 1R, {(stopped.mfe_R >= 2).mean():.0%} >= 2R")
    # average open profit (R) by minutes since entry, for trades still open, using bar closes
    rows = []
    for tr in bt.itertuples():
        e = tr.bar + 1
        R = 2.0 * D.atr5[tr.bar]
        entry = D.Open[e] + tr.dir * ee.SLIP
        for j in range(tr.hold_bars):
            rows.append((j * 5 + 5, (D.Close[e + j] - entry) * tr.dir / R, D.tmin[e + j]))
    p = pd.DataFrame(rows, columns=["mins", "openR", "tmin"])
    curve = p.groupby(pd.cut(p.mins, [0, 15, 30, 60, 90, 120, 180, 240, 300, 360, 480])).openR.agg(["mean", "size"])
    say("  average open profit (R) of trades still open, by minutes since entry:")
    say("   " + ", ".join(f"{str(k)}: {v['mean']:+.2f}R (n={int(v['size'])})" for k, v in curve.iterrows()))
    clock = p.groupby((p.tmin // 60)).openR.mean()
    say("  average open profit (R) of open trades by clock hour: " + ", ".join(f"{int(h)}:00 {v:+.2f}R" for h, v in clock.items()))

open("exit_diagnostics_output.txt", "w").write("\n".join(OUT))
