"""System total / max drawdown when R1 uses neighbouring thresholds (R2 off and on)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.getcwd())
import calendar_days as cd  # noqa: E402
T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
T = T.join(pd.read_pickle("data/market_context.pkl")[["spx_ret_1d_prev"]], on="date")
fed = T.date.isin(cd.fomc_days()) & (T.model == "opening_range")
days = pd.DatetimeIndex(sorted(T.date.unique()))
def stats(rm):
    k = T[~rm]; eq = k.groupby("date").usd.sum().reindex(days, fill_value=0).cumsum()
    dd = (eq - np.maximum(eq.cummax(), 0)).min()
    return f"removed {int(rm.sum()):4d} total ${k.usd.sum():+8.0f} maxDD ${dd:,.0f}"
brk = T.model.isin(["overnight_break", "opening_range"])
for x in (1.0, 1.5, 2.0, 2.5, 3.0):
    r1 = brk & (T.spx_ret_1d_prev <= -x)
    print(f"R1 at -{x}%: alone {stats(r1)} | with R2 {stats(r1 | fed)}")
