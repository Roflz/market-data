"""
v3/exp_synth/synth_p1.py - SYNTHESIS step 5 of PREREG.md: the eval portfolio P1 and its statistics.

P1 (fixed rule) = the Tier A rules labelled SIGNIFICANT by synth_stats.py (read from out/synthesis/tierA.csv; P0 is
the pre-specified combination test, not a tradeable rule, so it is not a component).
Each trade gets virtual risk_usd = sd of its component's per-micro net $ over the component's previous 100 trades
(time order, known before entry; the first 100 trades of each component get no risk and are not taken).
Sizing ('risk', 150/250/400) in H.eval (cap 20 micros, $600 daily limit, 40% and 50% rules); fixed 1 and 3 micros are
added as descriptive extras. Twins: 200 C1 realisations of the same components (same side, marks, year; random
session), each twin trade inheriting the micros-defining risk_usd of the real trade it copies (via tid), so the twin
differs from the real portfolio only in timing.

Statistics (same tests as the hypotheses, on daily P&L): 1 micro per trade (A3 = 1 per market) and $250-risk sized.
NOTE: P1's component list is chosen from the results (the survivors), so its p-values are descriptive, not
confirmatory; the confirmatory evidence is the Holm family (A1..A5, P0).

usage: python3 v3/exp_synth/synth_p1.py [n_twins]
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path.insert(0, V3)
sys.path.insert(0, os.path.join(V3, "exp_G4"))
import harness as H  # noqa: E402
import stats_protocol as sp  # noqa: E402

OUT = os.path.join(V3, "out")
SYN = os.path.join(OUT, "synthesis")
END = pd.Timestamp("2025-06-27")
SEED = 20261109
NT = int(sys.argv[1]) if len(sys.argv) > 1 else 200
SIZ = [("risk", 150), ("risk", 250), ("risk", 400), ("fixed", 1), ("fixed", 3)]
KEYS = ["policy", "consistency", "window"]
MET = ["pass_pct", "bust_pct", "within_5", "within_10", "within_20", "days_pass_median"]

tA = pd.read_csv(os.path.join(SYN, "tierA.csv"))
COMP = [h for h in tA.loc[tA.label == "SIGNIFICANT", "hid"] if h != "P0"]
print("P1 components:", COMP)
CAL = pd.read_csv(os.path.join(OUT, "daily", "A1.csv"), parse_dates=["session"])["session"]
CAL = pd.DatetimeIndex(CAL[CAL <= END])
assert len(CAL) == 3876


# ------------------------------------------------------------------------------------------- real trades + risk
def load_real(h):
    t = pd.read_parquet(os.path.join(OUT, "trades", f"{h}.parquet"))
    t = t[pd.DatetimeIndex(t.session) <= END].copy()
    if "tid" not in t.columns:
        t["tid"] = np.arange(len(t))
    c1col = {"A1": "c1", "A3": "c1", "A4": "c1"}.get(h, "c1")
    t["c1v"] = t[c1col].astype(float)
    t["comp"] = h
    t = t.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    t["risk_usd"] = t["pnl_usd"].shift(1).rolling(100, min_periods=100).std()
    return t


REAL = {h: load_real(h) for h in COMP}
real_all = pd.concat(REAL.values(), ignore_index=True)
cols = ["market", "session", "t_entry", "t_exit", "risk_usd", "pnl_usd", "comp", "tid", "c1v", "d"]
real_all = real_all[cols].sort_values("t_entry", kind="stable").reset_index(drop=True)


# ------------------------------------------------------------------------------------------- statistics
def daily_of(df, val):
    g = df.assign(v=val).groupby(pd.DatetimeIndex(df.session).normalize())["v"].sum()
    return g.reindex(CAL, fill_value=0.0)


def cp(x):
    return sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, float), B=5000, seed=SEED)


def summarize(net, d, u2=None, ntr=None, name=""):
    s = CAL.to_numpy().astype("datetime64[D]")
    yr = CAL.year.to_numpy()
    rn = sp.robust_report(net.to_numpy(), s)
    rd = sp.robust_report(d.to_numpy(), s)
    out = dict(name=name, n_trades=ntr, mean_net_day=float(net.mean()), mean_d_day=float(d.mean()),
               p_net=cp(net)[0], p_d=cp(d)[0], t_net=rn["all"][1], t_d=rd["all"][1],
               sharpe_ann=float(net.mean() / net.std(ddof=1) * np.sqrt(252)),
               daily_sharpe=float(net.mean() / net.std(ddof=1)), sd_day=float(net.std(ddof=1)),
               net_2010_17=rn["2010_17"], net_2018_25H1=rn["2018_25H1"], net_2022p=rn["2022+"],
               d_2010_17=rd["2010_17"], d_2018_25H1=rd["2018_25H1"], wo_best10=rn["drop_best"], winsor=rn["winsor"],
               share_years_pos=rn["share_years_pos"], by_year=rn["by_year"],
               best10_share=float(np.sort(net.to_numpy())[-10:].sum() / net.sum()),
               sessions_traded_pct=None)
    if u2 is not None:
        out["u2_2010_17"] = float(u2[yr <= 2017].mean())
        out["u2_2018_25H1"] = float(u2[yr >= 2018].mean())
        out["u2_share_years_pos"] = float((pd.Series(u2.to_numpy(), index=yr).groupby(level=0).sum() > 0).mean())
    return out


DLY = {h: pd.read_csv(os.path.join(OUT, "daily", f"{h}.csv"), parse_dates=["session"]).set_index("session")
       .reindex(CAL, fill_value=0.0) for h in COMP}
net1 = sum(DLY[h]["net_U1"] for h in COMP)
d1 = sum(DLY[h]["d"] for h in COMP)
u21 = sum(DLY[h]["net_U2"] for h in COMP)
ntr1 = int(sum(DLY[h]["n_trades"].sum() for h in COMP))
S1 = summarize(net1, d1, u21, ntr1, "P1 at 1 micro per trade (A3 = 1 MES + 1 MNQ + 1 MYM)")
S1["sessions_traded_pct"] = float((sum(DLY[h]["n_trades"] for h in COMP) > 0).mean())
S1["per_trade_net"] = float(net1.sum() / ntr1)
S1["per_component_net_per_trade"] = {h: float(DLY[h]["net_U1"].sum() / DLY[h]["n_trades"].sum()) for h in COMP}
S1["corr_net"] = pd.DataFrame({h: DLY[h]["net_U1"] for h in COMP}).corr().round(3).to_dict()
S1["corr_d"] = pd.DataFrame({h: DLY[h]["d"] for h in COMP}).corr().round(3).to_dict()
# per-market split of the 1-micro stream
S1["by_market_net_per_trade"] = {}
for m in ("ES", "NQ", "YM"):
    x = real_all[real_all.market == m]
    S1["by_market_net_per_trade"][m] = dict(n=int(len(x)), usd_per_trade=float(x.pnl_usd.mean()) if len(x) else None)

# $250-risk sized stream (micros = floor(250 / risk), cap 20; first 100 trades of each component not taken)
mic = np.where(real_all.risk_usd > 0, np.minimum(np.floor(250 / real_all.risk_usd + 1e-9), 20), 0)
real_all["mic250"] = mic
netR = daily_of(real_all, real_all.pnl_usd * mic)
dR = daily_of(real_all, (real_all.pnl_usd - real_all.c1v) * mic)
SR = summarize(netR, dR, None, int((mic > 0).sum()), "P1 sized at $250 virtual risk per trade (before Lucid rules)")
SR["micros_mean"] = float(mic[mic > 0].mean())
SR["micros_by_comp"] = real_all[mic > 0].groupby("comp")["mic250"].mean().round(2).to_dict()
SR["risk_by_comp_median"] = real_all.groupby("comp")["risk_usd"].median().round(1).to_dict()
print(json.dumps({k: v for k, v in S1.items() if k != "by_year"}, indent=0, default=float)[:3000])
print(json.dumps({k: v for k, v in SR.items() if k != "by_year"}, indent=0, default=float)[:2000])

# ------------------------------------------------------------------------------------------- twins (C1)
def twins_A1():
    t = pd.read_parquet(os.path.join(V3, "exp_g1_noiseband", "cache", "twins_A1.parquet"),
                        columns=["market", "session", "t_entry", "t_exit", "d", "entry", "exit", "tid", "pnl_usd", "rep"])
    r = REAL["A1"]
    # A1 trade table has no tid: twins' tid = row of the trade list (sorted by session/entry) -> check marks/side match
    base = pd.read_parquet(os.path.join(OUT, "trades", "A1.parquet"))
    base = base[pd.DatetimeIndex(base.session) <= END].reset_index(drop=True)
    chk = t[t.rep == 0].merge(base[["entry", "exit", "d"]].reset_index().rename(columns={"index": "tid"}), on="tid",
                              suffixes=("", "_b"))
    assert (chk.entry.astype(str) == chk.entry_b.astype(str)).all() and (chk.d == chk.d_b).all(), "A1 tid mismatch"
    key = base.reset_index().rename(columns={"index": "tid"})[["tid", "t_entry"]]
    rk = r[["t_entry", "risk_usd"]].drop_duplicates("t_entry")
    key = key.merge(rk, on="t_entry", how="left")[["tid", "risk_usd"]]
    t = t.merge(key, on="tid", how="left")
    return t


def twins_A3():
    out = []
    for s in ("ES", "NQ", "YM"):
        c = pd.read_parquet(os.path.join(V3, "exp_g3_expiry", "cache", f"c1_A3_{s}_999.parquet"))
        c = c[c.rep < NT].copy()
        c["market"] = s
        out.append(c)
    t = pd.concat(out, ignore_index=True).drop(columns=["risk_usd"], errors="ignore")
    r = REAL["A3"][["market", "tid", "risk_usd", "d"]].rename(columns={"d": "d_real"})
    t = t.merge(r, on=["market", "tid"], how="left")
    assert (t.d == t.d_real).all(), "A3 twin side mismatch"
    return t


def twins_A4():
    import g4lib as G
    S = H.sessions("NQ")
    ent = G.release_fade()(S, {})
    ent = ent[pd.DatetimeIndex(ent.session) <= G.END].reset_index(drop=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        L = G.run_leg("NQ", ent, 4, R=NT, nrep_ctrl=2)
    c = L["c1"].drop(columns=["risk_usd"], errors="ignore")
    assert len(L["trades"]) == len(REAL["A4"])
    r = REAL["A4"][["tid", "risk_usd", "d"]].rename(columns={"d": "d_real"})
    c = c.merge(r, on="tid", how="left")
    assert (c.d == c.d_real).all(), "A4 twin side mismatch"
    return c


TW = {}
if "A1" in COMP:
    TW["A1"] = twins_A1()
if "A3" in COMP:
    TW["A3"] = twins_A3()
if "A4" in COMP:
    TW["A4"] = twins_A4()
for h in COMP:
    assert h in TW, f"no twin builder for {h}"
for h, t in TW.items():
    t["session"] = pd.DatetimeIndex(t.session)
    TW[h] = t[(t.session <= END) & (t.rep < NT)]
    print(h, "twin trades", len(TW[h]), "reps", TW[h].rep.nunique(), "risk NaN share", round(TW[h].risk_usd.isna().mean(), 3))

# ------------------------------------------------------------------------------------------- eval
ec = ["market", "session", "t_entry", "t_exit", "risk_usd", "pnl_usd"]
t0 = time.time()
real_ev = H.eval(real_all[ec], sizing=SIZ, calendar_=CAL)
print("real eval", round(time.time() - t0, 1), "s")
real_ev.to_csv(os.path.join(SYN, "P1_eval_real.csv"), index=False)
rows = []
for r in range(NT):
    x = pd.concat([TW[h].loc[TW[h].rep == r, ec] for h in COMP], ignore_index=True).sort_values("t_entry")
    e = H.eval(x, sizing=SIZ, calendar_=CAL)
    e["rep"] = r
    rows.append(e[KEYS + MET + ["rep"]])
    if r % 20 == 0:
        print("twin", r, round(time.time() - t0, 1), "s", flush=True)
tw = pd.concat(rows, ignore_index=True)
tw.to_csv(os.path.join(SYN, "P1_eval_twins_raw.csv"), index=False)
lb = pd.read_csv(os.path.join(V3, "..", "v2", "out", "luck_bar.csv"))
out = []
for key, g in tw.groupby(KEYS, sort=False):
    rr = real_ev.set_index(KEYS).loc[key]
    row = dict(zip(KEYS, key))
    for m in ("pass_pct", "within_5", "within_10", "within_20"):
        row[f"{m}_real"] = float(rr[m])
        row[f"{m}_twin"] = float(g[m].mean())
        row[f"{m}_rank_p"] = float((1 + (g[m] >= rr[m]).sum()) / (1 + len(g)))
    row["bust_real"] = float(rr["bust_pct"])
    row["bust_twin"] = float(g["bust_pct"].mean())
    row["bust_rank_p_lower"] = float((1 + (g["bust_pct"] <= rr["bust_pct"]).sum()) / (1 + len(g)))
    row["days_pass_median_real"] = float(rr["days_pass_median"])
    row["days_pass_median_twin"] = float(g["days_pass_median"].median())
    row["micros_mean"] = float(rr["micros_mean"])
    row["trades_taken"] = float(rr["trades_taken"])
    for mk in ("NQ", "ES"):
        q = lb[(lb.market == mk) & (lb.window == key[2]) & (lb.consistency == key[1])]
        row[f"luck_within_10_{mk}"] = float(q.best_within_10.iloc[0]) if len(q) else np.nan
        row[f"luck_pass_{mk}"] = float(q.best_pass_pct.iloc[0]) if len(q) else np.nan
    out.append(row)
out = pd.DataFrame(out)
out.to_csv(os.path.join(SYN, "P1_eval_vs_twins.csv"), index=False)
json.dump(dict(components=COMP, n_twins=NT, stats_1micro=S1, stats_risk250=SR), open(os.path.join(SYN, "P1_stats.json"), "w"),
          indent=1, default=float)
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
print(out.round(3).to_string(index=False))
print("done", round(time.time() - t0, 1), "s")
