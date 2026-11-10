"""Stability checks of two candidate skip rules (R1: skip breakout models the day after S&P -2%+; R2: skip
opening_range on scheduled Fed statement days). Reads project files only; writes nothing into the project.
Run: cd <project> && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this file>
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.getcwd())
import calendar_days as cd  # noqa: E402

OUTDIR = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/skiprules/stability"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def welch_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 5 or len(b) < 5:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def win(x):
    return (np.asarray(x) > 0).mean() * 100 if len(x) else np.nan


def trimmed_mean(x, frac=0.05):
    x = np.sort(np.asarray(x, float))
    k = int(np.floor(len(x) * frac))
    return x[k:len(x) - k].mean() if len(x) > 2 * k else np.nan


def row(label, a, b):
    t = welch_t(a, b)
    return (f"{label:22s} cond n={len(a):4d} ${a.mean() if len(a) else np.nan:+8.2f} win {win(a):5.1f}% | "
            f"other n={len(b):5d} ${b.mean():+7.2f} win {win(b):5.1f}% | diff {a.mean() - b.mean() if len(a) else np.nan:+8.2f} "
            f"t {t:+6.2f}")


def max_dd(daily):
    eq = daily.sort_index().cumsum()
    peak = np.maximum.accumulate(np.r_[0.0, eq.values])[1:]
    dd = eq.values - peak
    i = dd.argmin()
    j = np.argmax(np.r_[0.0, eq.values][: i + 2]) - 1  # index of peak (-1 = start)
    return dd.min(), (eq.index[j] if j >= 0 else None), eq.index[i]


def main():
    T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ctx = pd.read_pickle("data/market_context.pkl")
    T = T.join(ctx[["spx_ret_1d_prev"]], on="date")
    fomc = cd.fomc_days()
    F = pd.read_csv("data/fomc_dates.csv", parse_dates=["date"])
    F = F[F.scheduled]
    pc = set(F[F.press_conference].date)
    T["fomc"] = T.date.isin(fomc)
    T["fomc_pc"] = T.date.isin(pc)
    T["r1"] = T.spx_ret_1d_prev <= -2
    T["year"] = T.date.dt.year
    say(f"Trades: {len(T)}; missing spx_ret_1d_prev: {int(T.spx_ret_1d_prev.isna().sum())}")

    tests = [("R1", "overnight_break", "r1"), ("R1", "opening_range", "r1"),
             ("R2", "opening_range", "fomc"), ("R2-context", "overnight_break", "fomc")]
    periods = [("2010-2015", 2010, 2015), ("2016-2020", 2016, 2020), ("2021-2026", 2021, 2026)]

    for rule, m, c in tests:
        g = T[T.model == m]
        a, b = g[g[c]], g[~g[c]]
        say(f"\n==================== {rule} / {m} (condition column: {c})")
        say(row("full sample", a.usd, b.usd))
        say("-- 1. sub-periods")
        for lab, y0, y1 in periods:
            gg = g[(g.year >= y0) & (g.year <= y1)]
            say(row(lab, gg[gg[c]].usd, gg[~gg[c]].usd))
        say("-- 1b. calendar years (only years with condition trades)")
        full_other = b.usd.mean()
        n_years = n_below_same = n_below_full = 0
        for y, gg in g.groupby("year"):
            ca, cb = gg[gg[c]].usd, gg[~gg[c]].usd
            if len(ca) == 0:
                continue
            n_years += 1
            n_below_same += ca.mean() < cb.mean()
            n_below_full += ca.mean() < full_other
            say(f"   {y}: cond n={len(ca):3d} ${ca.mean():+8.2f} (sum {ca.sum():+7.0f}) win {win(ca):5.1f}% | "
                f"other-days same year ${cb.mean():+7.2f}")
        say(f"   years with condition trades: {n_years}; cond $/trade below same-year other-day avg: {n_below_same}; "
            f"below full-sample other-day avg (${full_other:+.2f}): {n_below_full}")
        say("-- 3. concentration (condition days)")
        daily = a.groupby("date").usd.sum().sort_values()
        worst5 = daily.index[:5]
        rest = a[~a.date.isin(worst5)]
        say(f"   cond total ${a.usd.sum():+.0f} over {len(a)} trades / {len(daily)} days")
        say(f"   worst 5 days: " + ", ".join(f"{d:%Y-%m-%d} {daily[d]:+.0f}" for d in worst5) +
            f" (sum {daily.iloc[:5].sum():+.0f})")
        say(f"   without worst 5 days: n={len(rest)} total ${rest.usd.sum():+.0f} ${rest.usd.mean():+.2f}/trade "
            f"win {win(rest.usd):.1f}% t vs other {welch_t(rest.usd, b.usd):+.2f}")
        best5 = daily.index[-5:]
        rest2 = a[~a.date.isin(best5)]
        say(f"   (for symmetry, without best 5 days: ${rest2.usd.mean():+.2f}/trade)")
        say(f"   median: cond ${a.usd.median():+.2f} vs other ${b.usd.median():+.2f}")
        say(f"   trimmed mean (5% each tail): cond ${trimmed_mean(a.usd):+.2f} vs other ${trimmed_mean(b.usd):+.2f}")
        say(f"   share of cond trades that are stops: {(a.exit == 'stop').mean() * 100:.1f}% vs other "
            f"{(b.exit == 'stop').mean() * 100:.1f}%")
        say("-- 4. long vs short")
        for s in ("long", "short"):
            say(row(f"{s}", a[a.side == s].usd, b[b.side == s].usd))

    # 2. R1 threshold neighbours
    say("\n==================== 2. R1 thresholds (prior-day S&P return <= -X%) and exclusive bands")
    for m in ("overnight_break", "opening_range"):
        g = T[T.model == m]
        say(f"-- {m}")
        for x in (1.0, 1.5, 2.0, 2.5, 3.0):
            msk = g.spx_ret_1d_prev <= -x
            say(row(f"<= -{x:.1f}%", g[msk].usd, g[~msk].usd))
        bands = [(-1.5, -1.0), (-2.0, -1.5), (-2.5, -2.0), (-3.0, -2.5), (-99, -3.0)]
        for lo, hi in bands:
            msk = (g.spx_ret_1d_prev > lo) & (g.spx_ret_1d_prev <= hi)
            say(row(f"band ({lo},{hi}]", g[msk].usd, g[~msk].usd))
        # also the mirror (up days) as a control
        for x in (2.0,):
            msk = g.spx_ret_1d_prev >= x
            say(row(f"control >= +{x:.1f}%", g[msk].usd, g[~msk].usd))

    # 5. R2 splits
    say("\n==================== 5. R2 splits (opening_range on scheduled Fed days)")
    for m in ("opening_range", "overnight_break"):
        g = T[T.model == m]
        a, b = g[g.fomc], g[~g.fomc]
        say(f"-- {m}")
        say(row("press conf", a[a.fomc_pc].usd, b.usd))
        say(row("no press conf", a[~a.fomc_pc].usd, b.usd))
        say(row("Fed day < 2019", a[a.year < 2019].usd, b[b.year < 2019].usd))
        say(row("Fed day >= 2019", a[a.year >= 2019].usd, b[b.year >= 2019].usd))
        pre = a[a.year < 2019]
        say(row("<2019 press conf", pre[pre.fomc_pc].usd, b[b.year < 2019].usd))
        say(row("<2019 no press conf", pre[~pre.fomc_pc].usd, b[b.year < 2019].usd))

    # overlap of rules
    ov = T[(T.model == "opening_range") & T.r1 & T.fomc]
    say(f"\nopening_range trades hit by both R1 and R2: {len(ov)}")

    # 6. system effect
    say("\n==================== 6. System effect (all three models, 1 micro each, daily equity)")
    T["rm_r1"] = T.r1 & T.model.isin(["overnight_break", "opening_range"])
    T["rm_r2"] = T.fomc & (T.model == "opening_range")
    scen = {"baseline": pd.Series(False, index=T.index), "R1 only": T.rm_r1, "R2 only": T.rm_r2,
            "R1 + R2": T.rm_r1 | T.rm_r2}
    all_days = pd.DatetimeIndex(sorted(T.date.unique()))
    for name, rm in scen.items():
        k = T[~rm]
        daily = k.groupby("date").usd.sum().reindex(all_days, fill_value=0.0)
        dd, pk, tr = max_dd(daily)
        bym = k.groupby("model").usd.sum()
        yr = k.groupby(k.date.dt.year).usd.sum()
        say(f"{name:9s} trades {len(k):5d} removed {int(rm.sum()):4d} (removed $ {T[rm].usd.sum():+8.0f}) | total ${k.usd.sum():+9.0f} "
            f"| maxDD ${dd:,.0f} ({pk:%Y-%m-%d} -> {tr:%Y-%m-%d}) | worst year ${yr.min():+.0f} ({yr.idxmin()}) | "
            + ", ".join(f"{mm} {v:+.0f}" for mm, v in bym.items()))
    # by sub-period of the removed trades' $
    say("removed $ by sub-period:")
    for name in ("R1 only", "R2 only"):
        rm = scen[name]
        r = T[rm]
        say(f"  {name}: " + ", ".join(f"{lab} n={len(r[(r.year >= y0) & (r.year <= y1)])} "
                                      f"${r[(r.year >= y0) & (r.year <= y1)].usd.sum():+.0f}" for lab, y0, y1 in periods))
    open(f"{OUTDIR}/stability_output.txt", "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
