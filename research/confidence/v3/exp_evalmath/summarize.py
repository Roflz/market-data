"""Builds v3/out/evalmath_summary.txt from the evalmath tables (light)."""
import os
import pandas as pd
H = os.path.dirname(os.path.abspath(__file__))
O = os.path.join(os.path.dirname(H), "out")
pd.set_option("display.width", 200)
L = []
p = L.append
a = pd.read_csv(os.path.join(H, "table_A.csv"))
p("EVAL MATH (synthetic) - LucidFlex 25K: +$1,250 target, $1,000 EOD trailing DD (locks +100), $600 daily limit, "
  "consistency 40%/50%. 20,000 independent accounts per cell. pass10 = % of accounts passed within 10 trading days.")
p("Zero-edge Gaussian at daily sd $350-500 passes within 10 days 10-11% (c=40%) = the v2 luck bar (8-11%): calibrated.")
for c in (0.4, 0.5):
    x = a[(a.cons == c) & (a.intra == 0)]
    for v, lab in (("pass10", "pass within 10 days %"), ("pass20", "pass within 20 days %"),
                   ("bust20", "bust within 20 days %"), ("pass_rate", "eventual pass rate % (pass/(pass+fail), 120 d)")):
        p(f"\nA. Gaussian days, hard -600 daily stop, consistency {c:.0%}: {lab}; rows = daily Sharpe (mean/sd), cols = daily sd $")
        p(x.pivot(index="S", columns="sd", values=v).round(1).to_string())
x = a[(a.cons == 0.4)]
p("\nA2. intraday enforcement of the drawdown (c=40%), pass10 minus EOD-only pass10, and bust20 change:")
e0 = x[x.intra == 0].set_index(["S", "sd"])
e1 = x[x.intra == 1].set_index(["S", "sd"])
p((e1.pass10 - e0.pass10).unstack().round(1).to_string())
p((e1.bust20 - e0.bust20).unstack().round(1).to_string())
g = pd.read_csv(os.path.join(H, "table_G.csv"))
p("\nG. Two-point trades (stop -1R = $B, target +bR), up to nmax trades/day, never risk past the $600 daily room, "
  "daily profit stop. ER = net expectancy in R per trade. Best config per row (c=40%):")
for ER in (0.0, 0.05, 0.1, 0.2):
    y = g[(g.cons == 0.4) & (g.ER == ER)].sort_values("pass10", ascending=False).head(3)
    p(y[["ER", "b", "win_rate", "B", "nmax", "pstop", "lstop", "S_day", "pass5", "pass10", "pass20", "bust20",
         "pass_rate", "med_days_pass"]].round(2).to_string(index=False))
gg = g[g.cons == 0.4]
for k, lab in (("b", "payoff b (target in R)"), ("pstop", "daily profit stop"), ("lstop", "stop after a red day"),
               ("nmax", "max trades/day"), ("B", "$ risk per trade")):
    p(f"\nG: best pass10 by {lab} (rows = ER):")
    p(gg.groupby(["ER", k]).pass10.max().unstack().round(1).to_string())
p("\nG: best eventual pass rate by payoff b:")
p(gg.groupby(["ER", "b"]).pass_rate.max().unstack().round(1).to_string())
f = pd.read_csv(os.path.join(H, "table_F2.csv"))
p("\nF2. REAL random trades (v2 luck pools, 15-min bars, 1.5R target / 16-bar exit, costs in, 2018-2025H1), random side, "
  "demeaned to zero edge, + edge $/micro/trade; sequential with the daily-room rule. Best pass10 per market x edge (c=40%):")
ff = f[f.cons == 0.4]
p(ff.groupby(["market", "edge_usd"]).pass10.max().unstack().round(1).to_string())
p("same, eventual pass rate:")
p(ff.groupby(["market", "edge_usd"]).pass_rate.max().unstack().round(1).to_string())
p("ES fixed micros, 2 trades/day, no profit stop (pass10 / pass_rate):")
y = ff[(ff.market == "ES") & (ff.n == 2) & (ff.pstop == "none") & ff["size"].str.startswith("k")]
p(y.pivot(index="edge_usd", columns="size", values="pass10").round(1).to_string())
p(y.pivot(index="edge_usd", columns="size", values="pass_rate").round(1).to_string())
p("ES with/without first-win profit stop (best pass10 over size, n):")
p(ff[ff.market == "ES"].groupby(["edge_usd", "pstop"]).pass10.max().unstack().round(1).to_string())
for nm, t in (("E05", "ER 0.05"), ("E", "ER 0.10"), ("E20", "ER 0.20")):
    e = pd.read_csv(os.path.join(H, f"table_{nm}.csv"))
    e = e[(e.cons == 0.4) & (~e.intraday)]
    p(f"\nE. sizing rules, {t}, 2 trades/day (1.5R target), vol clustering, daily-room rule (c=40%). best per rule:")
    r = e.sort_values("pass10", ascending=False).groupby("policy").head(1)
    p(r[["policy", "param", "pstop", "micros_avg", "pass5", "pass10", "pass20", "bust20", "pass60", "pass_rate",
         "med_days_pass"]].round(1).to_string(index=False))
c = pd.read_csv(os.path.join(H, "table_C.csv"))
p("\nC. autocorrelation / regimes / sparse event-day edges (daily sd $300, c=40%):")
p(c[c.cons == 0.4][["kind", "S", "param", "pass5", "pass10", "pass20", "bust20", "pass_rate"]].round(1).to_string(index=False))
d = pd.read_csv(os.path.join(H, "table_D.csv"))
p("\nD. K streams of daily Sharpe s each; 'rescaled' = total daily sd kept at $300, 'fixed_each' = each at $150 sd (c=40%):")
p(d[d.cons == 0.4][["s_each", "rho", "K", "S_comb", "mode", "sd", "pass10", "pass20", "bust20", "pass_rate"]].round(2).to_string(index=False))
b = pd.read_csv(os.path.join(H, "table_B.csv"))
p("\nB. skew at matched trade mean & sd (daily sd ~$300), EOD check, no profit stop, c=40% (caveat: two-point lattice effects):")
y = b[(b.cons == 0.4) & (~b.intraday) & (b.pstop == 0)]
for v in ("pass10", "pass20", "bust20", "pass_rate"):
    p(f"{v} (rows S, n; cols win rate)")
    p(y.pivot_table(index=["S", "n"], columns="win_rate", values=v).round(1).to_string())
open(os.path.join(O, "evalmath_summary.txt"), "w").write("\n".join(L) + "\n")
print("\n".join(L)[:3000])
