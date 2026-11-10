"""Threshold medians / outlier check for R1."""
import numpy as np, pandas as pd
T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
T = T.join(pd.read_pickle("data/market_context.pkl")[["spx_ret_1d_prev"]], on="date")
for m in ("overnight_break", "opening_range"):
    g = T[T.model == m]
    print(f"-- {m}: other-day median ${g[g.spx_ret_1d_prev > -1].usd.median():+.2f}")
    for x in (1.0, 1.5, 2.0, 2.5, 3.0):
        s = g[g.spx_ret_1d_prev <= -x]; o = g[g.spx_ret_1d_prev > -x]
        print(f"  <= -{x}: n={len(s)} median ${s.usd.median():+.2f} (other {o.usd.median():+.2f}) win {(s.usd>0).mean()*100:.1f}% "
              f"mean ex best trade ${np.sort(s.usd)[:-1].mean():+.2f}; best trade {s.loc[s.usd.idxmax(),'date']:%Y-%m-%d} ${s.usd.max():+.1f} (prev SPX {s.loc[s.usd.idxmax(),'spx_ret_1d_prev']:+.2f}%)")
