"""
v3/exp_synth/synth_dll.py - EXPLORATORY eval-realism check of the P1 portfolio (descriptive; not a new rule; logged).

The v2 eval judge books each day at its CLOSING P&L floored at -$600. A real Lucid account is flattened as soon as the
day's running P&L (realised + open) touches -$600. Here every P1 trade's open P&L is walked on 5-minute bars (worst price
of each bar, costs included, micros applied); after its exit the trade contributes its realised P&L for the rest of the
session. All trades of the session are summed per 5-minute bar; a day whose running total touches -$600 is booked at
-$600. The trailing drawdown is end-of-day in Lucid, so it is unchanged. Same eval_daily as the v2 judge.
Light (v3 5-minute bars + saved trade tables).
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path.insert(0, V3)
import harness as H  # noqa: E402
import eval_sim as es  # noqa: E402

OUT = os.path.join(V3, "out")
SYN = os.path.join(OUT, "synthesis")
END = pd.Timestamp("2025-06-27")
tA = pd.read_csv(os.path.join(SYN, "tierA.csv"))
COMP = [h for h in tA.loc[tA.label == "SIGNIFICANT", "hid"] if h != "P0"]
CAL = pd.read_csv(os.path.join(OUT, "daily", "A1.csv"), parse_dates=["session"])["session"]
CAL = pd.DatetimeIndex(CAL[CAL <= END])


def load(h):
    t = pd.read_parquet(os.path.join(OUT, "trades", f"{h}.parquet"))
    t = t[pd.DatetimeIndex(t.session) <= END].copy()
    t["comp"] = h
    t = t.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    t["risk_usd"] = t["pnl_usd"].shift(1).rolling(100, min_periods=100).std()
    return t


T = pd.concat([load(h) for h in COMP], ignore_index=True)
T["session"] = pd.DatetimeIndex(T.session).normalize()
T["uid"] = np.arange(len(T))

# session grid = NQ 5-minute bar starts of each traded session
gb = H.bars("NQ", 5)[["session"]].reset_index()
gb["session"] = pd.DatetimeIndex(gb.session).normalize()
grid = gb[gb.session.isin(T.session.unique())].rename(columns={"ts": "ts"})

paths = []
for m in T.market.unique():
    t = T[T.market == m]
    b = H.bars(m, 5)[["H", "L"]].reset_index()
    x = grid.merge(t[["uid", "session", "t_entry", "t_exit", "d", "entry_px", "cost_usd", "pnl_usd"]], on="session")
    x = x.merge(b, on="ts", how="left")
    usd = H.SPEC[m]["usd"]
    open_w = np.where(x.d > 0, x.L - x.entry_px, x.entry_px - x.H) * usd - x.cost_usd
    open_w = np.where(np.isfinite(open_w), open_w, -x.cost_usd)       # missing bar: no new extreme known
    val = np.where(x.ts < x.t_entry, 0.0, np.where(x.ts < x.t_exit, open_w, x.pnl_usd))
    paths.append(pd.DataFrame({"uid": x.uid.to_numpy(), "session": x.session.to_numpy(), "ts": x.ts.to_numpy(),
                               "v": val}))
P = pd.concat(paths, ignore_index=True)

# sizing policies -> micros per trade
POL = {"1 micro": np.ones(len(T)), "3 micros": np.full(len(T), 3.0)}
for B in (150, 250):
    POL[f"${B} risk"] = np.where(T.risk_usd > 0, np.minimum(np.floor(B / T.risk_usd + 1e-9), 20), 0.0)
rows = []
for name, mic in POL.items():
    if name.endswith("risk"):
        use = mic > 0
    else:
        use = np.ones(len(T), bool)
    mu = pd.Series(mic, index=T.uid)
    Pm = P[P.uid.isin(T.uid[use])].copy()
    Pm["v"] = Pm["v"] * mu.reindex(Pm.uid).to_numpy()
    worst = Pm.groupby(["session", "ts"]).v.sum().groupby(level=0).min().reindex(CAL, fill_value=0.0)
    eod = (T.pnl_usd * mic)[use].groupby(T.session[use]).sum().reindex(CAL, fill_value=0.0)
    d_eod = eod.clip(lower=-600)
    hit = worst <= -600
    d_int = d_eod.where(~hit, -600.0)
    for lab, dly in (("closing P&L floored at -$600 (v2 judge style)", d_eod), ("intraday $600 stop", d_int)):
        e = es.eval_daily(dly, (0.40, 0.50))
        e.insert(0, "model", lab)
        e.insert(0, "sizing", name)
        e["dll_hit_days_pct_of_traded"] = 100 * hit[eod.index[(eod != 0)]].mean()
        e["closed_above_m600_but_hit"] = int((hit & (eod > -600)).sum())
        rows.append(e)
out = pd.concat(rows, ignore_index=True)
keep = ["sizing", "model", "consistency", "window", "pass_pct", "fail_pct", "within_5", "within_10", "within_20",
        "days_pass_median", "dll_hit_days_pct_of_traded", "closed_above_m600_but_hit"]
out = out[[c for c in keep if c in out.columns]]
out.to_csv(os.path.join(SYN, "P1_eval_intraday_dll_EXPLORATORY.csv"), index=False)
H.log("P1-evalrealism", "+".join(COMP), "P1 eval with intraday $600 stop on the 5-min running P&L (descriptive)",
      params=dict(sizings=list(POL)), note="exploratory eval-model check, not a new rule")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 30)
print(out.round(2).to_string(index=False))
