"""
Summarize out/exits_*.csv: for each exit rule, the average $ per trade (per micro, after costs) pooled over entry
patterns, next to the fixed 5-bar exit and to the rule's own random-timing control (shuffle).
Entry groups: 'classic' = the classic candle patterns (exits.CLASSIC), 'frequent' = the very frequent ones.
  PYTHONPATH=../../pylib:../..:. python3 make_exit_report.py
Writes out/EXITS_REPORT.md, out/exits_pooled.csv, charts/exits_heatmap_{group}.png
"""
import glob

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import exits as ex

d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("out/exits_??_*.csv"))], ignore_index=True)
d["group"] = np.where(d.pattern.isin(ex.CLASSIC), "classic", "frequent")
ORDER = ["fixed_5", "fixed_10", "fixed_20", "hold_1645", "opp_same", "opp_classic", "opp_any", "opp_any2",
         "opp_classic_at_level", "choch_3", "choch_5", "mom_turn", "mom_cross100", "ema8_cross", "ema20_cross",
         "trail_3", "trail_5", "trail_10", "tgt_swing", "tgt_fib382", "tgt_fib618", "tgt_fib1272"]


def wmean(g, col, w="n"):
    m = g[col].notna() & (g[w] > 0)
    return (g.loc[m, col] * g.loc[m, w]).sum() / g.loc[m, w].sum() if m.any() else np.nan


rows = []
for (grp, mk, tf, rule, stop), g in d.groupby(["group", "micro", "tf", "exit", "stop"]):
    rows.append(dict(group=grp, micro=mk, tf=tf, exit=rule, stop=stop, trades=g.n.sum(),
                     usd=wmean(g, "usd"), hit=wmean(g, "hit"), hold_min=wmean(g, "hold_min_median"),
                     usd_2022_26=wmean(g, "usd_2022_26", "n_2022_26"), usd_2018plus=wmean(g, "usd_2018plus", "n_2018plus"),
                     avg_win=wmean(g, "avg_win"), avg_loss=wmean(g, "avg_loss"), gave_back=wmean(g, "gave_back_usd")))
pooled = pd.DataFrame(rows)
sh = pooled[pooled.exit.str.startswith("shuffle_")].assign(exit=lambda x: x.exit.str.replace("shuffle_", ""))
pooled = pooled.merge(sh[["group", "micro", "tf", "exit", "usd"]].rename(columns={"usd": "shuffle_usd"}),
                      on=["group", "micro", "tf", "exit"], how="left")
pooled.loc[pooled.stop != "none", "shuffle_usd"] = np.nan
base = pooled[pooled.exit == "fixed_5"][["group", "micro", "tf", "stop", "usd"]].rename(columns={"usd": "fixed5_usd"})
pooled = pooled.merge(base, on=["group", "micro", "tf", "stop"], how="left")
pooled = pooled[~pooled.exit.str.startswith("shuffle_")]
pooled.to_csv("out/exits_pooled.csv", index=False)


def md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f"{v:,.2f}" if isinstance(v, float) else str(v) for v in r.values) + " |")
    return "\n".join(out)


lines = ["# Exit study: $ per trade per micro contract after costs\n",
         "Same entries for every exit rule (each directional pattern; entry at the next bar's open; flat by 16:45 ET). "
         "Pooled over patterns, weighted by number of trades. 'vs random timing' = the rule minus the same entries held "
         "for randomly re-assigned holding times drawn from that rule's own holding times (positive = the rule picks "
         "better exit moments than chance).\n"]
for grp in ("classic", "frequent"):
    for stop in ("none", "pattern"):
        x = pooled[(pooled.group == grp) & (pooled.stop == stop)]
        if x.empty:
            continue
        lines.append(f"\n## Entries: {grp} patterns, stop: {'none' if stop == 'none' else 'beyond the pattern'}\n")
        for mk in ("MES", "MNQ", "MYM"):
            t = x[x.micro == mk].copy()
            if t.empty:
                continue
            t["vs_random"] = t.usd - t.shuffle_usd
            t["vs_fixed5"] = t.usd - t.fixed5_usd
            t["exit"] = pd.Categorical(t.exit, ORDER)
            piv = t.pivot_table(index="exit", columns="tf", values="usd", observed=False)
            piv.columns = [f"{c}m $/trade" for c in piv.columns]
            hold = t.pivot_table(index="exit", columns="tf", values="hold_min", observed=False)
            hold.columns = [f"{c}m hold min" for c in hold.columns]
            vr = t.pivot_table(index="exit", columns="tf", values="vs_random", observed=False)
            vr.columns = [f"{c}m vs random" for c in vr.columns]
            r22 = t.pivot_table(index="exit", columns="tf", values="usd_2022_26", observed=False)
            r22.columns = [f"{c}m 2022-26" for c in r22.columns]
            tab = pd.concat([piv, r22, vr, hold], axis=1).dropna(how="all").reset_index()
            lines.append(f"### {mk}\n" + md(tab.round(2)) + "\n")
open("out/EXITS_REPORT.md", "w").write("\n".join(lines))

# heatmaps: $ per trade minus the fixed 5-bar exit, rows = exit rules, columns = market x timeframe
for grp in ("classic", "frequent"):
    for stop in ("none", "pattern"):
        x = pooled[(pooled.group == grp) & (pooled.stop == stop)].copy()
        if x.empty:
            continue
        x["col"] = x.micro + " " + x.tf.astype(str) + "m"
        x["diff"] = x.usd - x.fixed5_usd
        piv = x.pivot_table(index="exit", columns="col", values="usd")
        piv = piv.reindex([r for r in ORDER if r in piv.index])
        cols = sorted(piv.columns, key=lambda s: (s.split()[0], int(s.split()[1][:-1])))
        piv = piv[cols]
        fig, ax = plt.subplots(figsize=(1.0 * len(cols) + 4, 0.45 * len(piv) + 2))
        lim = np.nanpercentile(np.abs(piv.values), 95)
        im = ax.imshow(piv.values, cmap="RdYlGn", vmin=-lim, vmax=lim, aspect="auto")
        for (r, cc), v in np.ndenumerate(piv.values):
            if np.isfinite(v):
                ax.text(cc, r, f"{v:.1f}", ha="center", va="center", fontsize=8)
        ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=45, ha="right")
        ax.set_yticks(range(len(piv))); ax.set_yticklabels(piv.index)
        ax.set_title(f"$ per trade per micro after costs, {grp} entry patterns, stop: {stop}", loc="left")
        fig.colorbar(im, ax=ax, shrink=0.6)
        plt.tight_layout(); fig.savefig(f"charts/exits_heatmap_{grp}_{stop}.png", dpi=95); plt.close(fig)
print("report written")
