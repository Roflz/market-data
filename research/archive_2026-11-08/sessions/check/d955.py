"""09:55-10:00 ET long: $ per trade, by year, minute breakdown, robustness."""
import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from grid import grid, pevent, pclose, biggap_cum, ROOT
from events import event, cash, cpi, MULT, COST

for sym in ("NQ", "ES"):
    df = event(sym, 9 * 60 + 55, 5, 0)   # p0 = 9:55 open, p1 = 10:00 open
    df["pts"] = df.p1 - df.p0
    df["usd"] = df.pts * MULT[sym] - COST[sym]
    df["bp"] = 1e4 * df.imp
    print(f"\n{sym} long 09:55->10:00 (07:55->08:00 Denver): n={len(df)} mean {df.bp.mean():+.2f} bp, "
          f"mean pts {df.pts.mean():+.3f}, net ${df.usd.mean():+.2f}/trade, hit {np.mean(df.pts > 0):.3f}, "
          f"t {df.pts.mean() / (df.pts.std() / np.sqrt(len(df))):.2f}")
    y = df.groupby("yr").agg(n=("bp", "size"), bp=("bp", "mean"), pts=("pts", "mean"), usd=("usd", "mean"),
                             hit=("pts", lambda x: np.mean(x > 0)))
    print(y.round(2).to_string())
    # trimmed: drop top/bottom 1%
    q = df.bp.quantile([0.01, 0.99])
    tr = df[(df.bp > q.iloc[0]) & (df.bp < q.iloc[1])]
    print(f"  1% trimmed mean {tr.bp.mean():+.3f} bp t {tr.bp.mean() / (tr.bp.std() / np.sqrt(len(tr))):.2f}; median {df.bp.median():+.3f}")
    # minute breakdown 9:50..10:04 signed means
    G = grid(sym)
    rows = []
    for mm in range(9 * 60 + 45, 10 * 60 + 6):
        d1 = event(sym, mm, 1, 0)
        rows.append((f"{mm // 60:02d}:{mm % 60:02d}", 1e4 * d1.imp.mean(), d1.imp.mean() / (d1.imp.std() / np.sqrt(len(d1)))))
    print("  1-min signed mean bp (bar open->next open):", ", ".join(f"{a} {b:+.2f}(t{c:+.1f})" for a, b, c in rows))
    # weekday
    df["wd"] = pd.DatetimeIndex(df.sess).dayofweek
    print("  by weekday bp:", df.groupby("wd").bp.mean().round(2).to_dict())
    # 2018+ net per trade
    e2 = df[df.yr >= 2018]
    print(f"  2018-26: net ${e2.usd.mean():+.2f}, 2022-26 net ${df[df.yr >= 2022].usd.mean():+.2f}")
