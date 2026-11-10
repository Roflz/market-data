"""Rebuild the overnight_break model's trades WITH entry/exit timestamps (for overlap diagnostics only),
the same way chosen_models.overnight_break does, and check count/total $ against chosen_models_trades.csv."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402

os.chdir(c.PROJ)
import calendar_days as cdays  # noqa: E402
import exits_compare as ec  # noqa: E402
import exits_engine as ee  # noqa: E402

b = pd.read_pickle("data/x5_NQ.pkl")
D = ee.Day(b[b.index.year >= ec.FIRST_YEAR])
D.pos = pd.Index(D.idx)
ec.G["NQ"] = D
sets = ec.entry_sets("NQ")
t = ee.run(D, sets["Overnight break + daily trend"], "hold", k0=2.0)
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
cash = ds.index[ds.cash_day]
expiry = cdays.expiry_fridays(cash)
sp = ee.SPEC["NQ"]
bars = t.bar.to_numpy()
date = pd.to_datetime(D.sess[bars])
ent_bar = bars + 1
ex_bar = ent_bar + t.hold_bars.to_numpy() - 1
idx = pd.DatetimeIndex(D.idx)
out = pd.DataFrame({"date": date, "side": np.where(t.dir > 0, "long", "short"), "dir": t.dir,
                    "entry_ts": idx[ent_bar], "exit_bar_ts": idx[ex_bar], "exit": t.exit,
                    "usd": (t.pts - sp["comm"] / sp["usd"]) * sp["usd"]})
out = out[out.date.isin(cash) & ~out.date.isin(expiry)]
ctx = pd.read_pickle("data/market_context.pkl")
after_drop = set(ctx.index[ctx.spx_ret_1d_prev <= -2.0])
out = out[~out.date.isin(after_drop)].reset_index(drop=True)
ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
ref = ref[ref.model == "overnight_break"]
print("rebuilt", len(out), round(out.usd.sum(), 2), "ref", len(ref), round(ref.usd.sum(), 2))
print(out.head())
out.to_csv(os.path.join(c.OUT, "onbreak_trades_with_times.csv"), index=False)
