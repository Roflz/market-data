"""Price-level-neutral (R and bp) versions of the sub-period, threshold and split checks, plus bootstrap of
year-block stability. Run from the project dir with PYTHONPATH=./pylib."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.getcwd())
import calendar_days as cd  # noqa: E402

def welch_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 5 or len(b) < 5: return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))

T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
ctx = pd.read_pickle("data/market_context.pkl")
T = T.join(ctx[["spx_ret_1d_prev"]], on="date")
T["fomc"] = T.date.isin(cd.fomc_days()); T["r1"] = T.spx_ret_1d_prev <= -2; T["year"] = T.date.dt.year
print(T.groupby("model")[["R", "bp"]].apply(lambda d: d.notna().mean()))
print("median $|usd| by period and model:")
T["per"] = pd.cut(T.year, [2009, 2015, 2020, 2026], labels=["2010-15", "2016-20", "2021-26"])
print(T.groupby(["model", "per"], observed=True).usd.apply(lambda x: x.abs().mean()).unstack().round(1))
periods = [("all", 2010, 2026), ("2010-2015", 2010, 2015), ("2016-2020", 2016, 2020), ("2021-2026", 2021, 2026)]
for rule, m, c in [("R1", "overnight_break", "r1"), ("R1", "opening_range", "r1"), ("R2", "opening_range", "fomc")]:
    g = T[T.model == m]
    for unit in ("R", "bp"):
        line = []
        for lab, y0, y1 in periods:
            gg = g[(g.year >= y0) & (g.year <= y1)]
            a, b = gg[gg[c]][unit].dropna(), gg[~gg[c]][unit].dropna()
            line.append(f"{lab}: {a.mean():+.3f} vs {b.mean():+.3f} (t {welch_t(a, b):+.2f}, n={len(a)})")
        print(f"{rule} {m} [{unit}] " + " | ".join(line))
# thresholds in bp
for m in ("overnight_break", "opening_range"):
    g = T[T.model == m]
    print(f"-- thresholds bp {m}")
    for x in (1.0, 1.5, 2.0, 2.5, 3.0):
        msk = g.spx_ret_1d_prev <= -x
        print(f"  <= -{x}: n={msk.sum()} bp {g[msk].bp.mean():+.2f} vs {g[~msk].bp.mean():+.2f} t {welch_t(g[msk].bp, g[~msk].bp):+.2f}; "
              f"R {g[msk].R.mean():+.3f} vs {g[~msk].R.mean():+.3f} t {welch_t(g[msk].R.dropna(), g[~msk].R.dropna()):+.2f}")
    for lo, hi in [(-1.5, -1.0), (-2.0, -1.5), (-2.5, -2.0)]:
        msk = (g.spx_ret_1d_prev > lo) & (g.spx_ret_1d_prev <= hi)
        s = g[msk]
        print(f"  band ({lo},{hi}]: n={len(s)} $ mean {s.usd.mean():+.2f} median {s.usd.median():+.2f} "
              f"top3 $ {sorted(s.usd)[-3:]} mean-ex-top3 {np.sort(s.usd)[:-3].mean():+.2f} bp {s.bp.mean():+.2f}")
# Fed splits in bp
g = T[T.model == "opening_range"]
F = pd.read_csv("data/fomc_dates.csv", parse_dates=["date"]); F = F[F.scheduled]
pc = set(F[F.press_conference].date)
a, b = g[g.fomc], g[~g.fomc]
for lab, msk_a, msk_b in [("<2019", a.year < 2019, b.year < 2019), (">=2019", a.year >= 2019, b.year >= 2019),
                          ("2018+", a.year >= 2018, b.year >= 2018), ("<2018", a.year < 2018, b.year < 2018)]:
    print(f"OR Fed {lab}: n={msk_a.sum()} bp {a[msk_a].bp.mean():+.2f} vs {b[msk_b].bp.mean():+.2f} t {welch_t(a[msk_a].bp, b[msk_b].bp):+.2f}"
          f" | $ {a[msk_a].usd.mean():+.2f} vs {b[msk_b].usd.mean():+.2f} t {welch_t(a[msk_a].usd, b[msk_b].usd):+.2f}")
# Fed day split by press conference within 2011-2018 (when only some meetings had one)
w = a[(a.year >= 2011) & (a.year <= 2018)]; wb = b[(b.year >= 2011) & (b.year <= 2018)]
for lab, s in [("2011-18 pc", w[w.date.isin(pc)]), ("2011-18 no pc", w[~w.date.isin(pc)])]:
    print(f"{lab}: n={len(s)} $ {s.usd.mean():+.2f} bp {s.bp.mean():+.2f} vs other bp {wb.bp.mean():+.2f} t {welch_t(s.bp, wb.bp):+.2f}")
# Fed-day OR by side and sub-period
for lab, y0, y1 in periods[1:]:
    s = a[(a.year >= y0) & (a.year <= y1)]
    print(f"OR Fed {lab}: long n={(s.side=='long').sum()} ${s[s.side=='long'].usd.mean():+.2f}, short n={(s.side=='short').sum()} ${s[s.side=='short'].usd.mean():+.2f}")
# R1 combined both models: R1 trades by side and period
for m in ("overnight_break", "opening_range"):
    gm = T[(T.model == m) & T.r1]
    for lab, y0, y1 in periods[1:]:
        s = gm[(gm.year >= y0) & (gm.year <= y1)]
        print(f"{m} R1 {lab}: long n={(s.side=='long').sum()} ${s[s.side=='long'].usd.mean():+.2f}, short n={(s.side=='short').sum()} ${s[s.side=='short'].usd.mean():+.2f}")
# Random-day placebo: how often does skipping the same number of random trade days (per model) improve total by as much?
rng = np.random.default_rng(0)
for lab, m, c in [("R1 ob", "overnight_break", "r1"), ("R1 or", "opening_range", "r1"), ("R2 or", "opening_range", "fomc")]:
    g = T[T.model == m]; k = int(g[c].sum()); obs = g[g[c]].usd.sum()
    sims = np.array([rng.choice(g.usd.values, k, replace=False).sum() for _ in range(20000)])
    print(f"placebo {lab}: removed-trade sum {obs:+.0f}; random {k} trades sum <= obs in {np.mean(sims <= obs)*100:.2f}% of 20000")
