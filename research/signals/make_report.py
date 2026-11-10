"""
Combine out/stats_*, context_*, cond_* into readable tables: REPORT.md and all_*.csv.
Usage: cd research/signals && PYTHONPATH=../../pylib:../..:. python3 make_report.py
Reading guide (written into the report):
  edge5 = average move over the next 5 bars in the pattern's direction, in ATRs, MINUS what an average bar did
          (so drift is removed); 0.05 ATR on 15-minute ES is roughly 0.15 points. $5 = after costs at 1 micro.
  consistent = same sign in 2010-17, 2018-21 and 2022-26 (YM: 2018-21 and 2022-26).
"""
import glob

import numpy as np
import pandas as pd


def md(df):
    """DataFrame -> markdown table (no extra packages)."""
    df = df.reset_index()
    head = "| " + " | ".join(str(c) for c in df.columns) + " |\n|" + "---|" * len(df.columns)
    body = ["| " + " | ".join("" if pd.isna(v) else (f"{v:+.3f}" if isinstance(v, float) else str(v)) for v in r) + " |"
            for r in df.itertuples(index=False)]
    return head + "\n" + "\n".join(body)

S = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("out/stats_*.csv"))], ignore_index=True)
C = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("out/context_*.csv"))], ignore_index=True)
K = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("out/cond_*.csv"))], ignore_index=True)
S.to_csv("all_stats.csv", index=False); C.to_csv("all_context.csv", index=False); K.to_csv("all_cond.csv", index=False)

eras = [c for c in S.columns if c.startswith("edge5_20")]
def consistent(r):
    v = [r[e] for e in eras if pd.notna(r[e])]
    return len(v) >= 2 and (all(x > 0 for x in v) or all(x < 0 for x in v))
S["consistent"] = S.apply(consistent, axis=1)
D = S[S.n >= 30].copy()
L = []
L.append("# Signal detection: what followed each pattern\n")
L.append("Markets ES (MES), NQ (MNQ) 2010-2026 and YM (MYM) 2018-2026; timeframes 1, 5, 15, 60, 120 minutes; all Globex "
         "hours. Entry at the next bar's open after the signal bar closes. **edge5** = average move over the next 5 bars in "
         "the pattern's direction, in ATRs (ATR = the timeframe's average true range), minus what an average bar did. "
         "**$5** = the same move in dollars at 1 micro after costs (MES $3.50, MNQ/MYM $2.00 per round trip). "
         "**consistent** = same sign in every era (2010-17, 2018-21, 2022-26). t is naive (signals cluster).\n")
for tf in sorted(D.tf.unique()):
    x = D[D.tf == tf]
    L.append(f"\n## {tf}-minute bars\n")
    piv = x.pivot_table(index=["pattern", "direction"], columns="market", values="edge5_atr")
    usd = x.pivot_table(index=["pattern", "direction"], columns="market", values="usd5_per_micro")
    n = x.pivot_table(index=["pattern", "direction"], columns="market", values="per_year")
    cons = x.pivot_table(index=["pattern", "direction"], columns="market", values="consistent", aggfunc="first")
    rows = []
    for idx in piv.index:
        cells = []
        for mk in ("ES", "NQ", "YM"):
            if mk in piv.columns and pd.notna(piv.loc[idx, mk]):
                cells.append(f"{piv.loc[idx, mk]:+.3f} / ${usd.loc[idx, mk]:+.1f} / {n.loc[idx, mk]:,.0f}" + (" ✓" if cons.loc[idx, mk] else ""))
            else:
                cells.append("-")
        same = [np.sign(piv.loc[idx, mk]) for mk in ("ES", "NQ", "YM") if mk in piv.columns and pd.notna(piv.loc[idx, mk])]
        tag = "all markets +" if same and all(s > 0 for s in same) else ("all markets -" if same and all(s < 0 for s in same) else "")
        rows.append((idx[0], idx[1], *cells, tag, np.nanmean([piv.loc[idx, mk] for mk in piv.columns])))
    rows.sort(key=lambda r: -r[-1])
    L.append("| Pattern | Direction | ES: edge5 / $5 / per yr | NQ | YM | Agreement |\n|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |")
# confirmation score summary (all directional patterns pooled, per market and timeframe)
L.append("\n## Does more confirmation help? (directional patterns pooled)\n")
L.append("Confirmations counted at the signal: trend with the pattern, momentum turning with it, at support (long) / "
         "resistance (short) within 0.5 ATR, on the cheap side of VWAP (below for longs, above for shorts).\n")
k = K[K.split == "confirmations (0-4)"].copy()
k["w"] = k.n * k.edge5_atr
g = k.groupby(["market", "tf", "group"]).agg(n=("n", "sum"), w=("w", "sum"))
g["edge5_atr"] = g.w / g.n
t = g.edge5_atr.unstack("group").round(3)
L.append(md(t))
for split in ("trend", "momentum", "level", "vwap"):
    kk = K[K.split == split].copy(); kk["w"] = kk.n * kk.edge5_atr
    gg = kk.groupby(["market", "tf", "group"]).agg(n=("n", "sum"), w=("w", "sum")); gg["edge5"] = gg.w / gg.n
    L.append(f"\n**{split} agreement**, average edge5 (ATR) of all directional patterns:\n")
    L.append(md(gg.edge5.unstack("group").round(3)))
open("REPORT.md", "w").write("\n".join(L) + "\n")
print(f"REPORT.md written: {len(D)} pattern rows, {D.consistent.sum()} consistent across eras")
