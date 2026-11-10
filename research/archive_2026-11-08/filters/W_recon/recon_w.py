"""Reconcile Filter W (builders X and Y). Independent re-implementation of the decision from the base inputs,
sensitivity of the decision to the readings of SPEC.md, raw-bar check of the raw price for every trade,
pass rule, report-only items and per-year CSV.
Run: cd <project> && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 recon_w.py"""
import json, os
import numpy as np, pandas as pd

S = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/"
OUT = S + "W_recon/"
X = pd.read_csv(S + "W_X/W_decisions.csv", parse_dates=["date"])
Y = pd.read_csv(S + "W_Y/W_trades.csv", parse_dates=["date"])
base = pd.read_pickle(S + "W_Y/base_overnight_break.pkl")
cal = pd.read_pickle(S + "W_Y/calendar.pkl")
ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
ob_ref = ref[ref.model == "overnight_break"].reset_index(drop=True)
res = {}

# ---- 0. base set equals the project CSV
assert len(base) == len(ob_ref) == 1731
res["base_equal_csv"] = bool((base.date.values == ob_ref.date.values).all() and (base.side.values == ob_ref.side.values).all()
                             and np.allclose(base.usd, ob_ref.usd) and np.allclose(base.bp, ob_ref.bp))

# ---- 1. raw-bar check of raw price (signal 5-min bar close) for every trade, from the raw 1-min file
d = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Close", "instrument_id"])
d.index = pd.to_datetime(d.pop("ts_event"), utc=True).dt.tz_convert("America/New_York")
d = d[~d.index.duplicated()].sort_index()
sig = pd.DatetimeIndex(base.signal_bar_time)
if sig.tz is None:
    sig = sig.tz_localize("America/New_York")
last1m = sig + pd.Timedelta(minutes=4)                    # last 1-min bar inside the signal 5-min bar
pos = d.index.searchsorted(last1m, side="right") - 1      # last 1-min bar stamped <= :04
rc = d.Close.to_numpy()[pos]; rt = d.index[pos]
inside = (rt >= sig) & (rt <= last1m)
diff = np.abs(rc - base.raw_ref_price.to_numpy())
res["raw_price_check"] = {"n": int(len(base)), "bar_found_inside": int(inside.sum()),
                          "max_abs_diff_pts": float(diff[inside].max()), "n_diff_gt_0.01": int((diff[inside] > 0.01).sum())}
del d

# ---- 2. independent decision (explicit loop) with a reading switch
def decide(width, dates, days, first, lookback=250, q=67, strict=True):
    days = pd.DatetimeIndex(days).sort_values()
    days = days[days >= first]
    dpos = {dd: i for i, dd in enumerate(days)}
    out = np.zeros(len(width), bool); thr = np.full(len(width), np.nan); nw = np.zeros(len(width), int)
    dates = pd.DatetimeIndex(dates)
    for i, dt in enumerate(dates):
        p = days.searchsorted(dt)                         # days strictly before dt
        if p < lookback:
            continue
        lo, hi = days[p - lookback], dt
        m = (dates >= lo) & (dates < hi)
        w = width[m]
        if len(w) == 0:
            continue
        thr[i] = np.percentile(w, q); nw[i] = len(w)
        out[i] = width[i] > thr[i] if strict else width[i] >= thr[i]
    return out, thr, nw

cash = pd.DatetimeIndex(cal["cash_days"]); first = pd.Timestamp(cal["model_first_sess"])
width = (base.R_pts / base.raw_ref_price).to_numpy()
rem, thr, nw = decide(width, base.date, cash, first)
res["recon_vs_X"] = int((rem == (X.decision == "remove").to_numpy()).sum())
res["recon_vs_Y"] = int((rem == (Y.decision == "remove").to_numpy()).sum())
res["X_vs_Y"] = int(((X.decision == "remove") == (Y.decision == "remove")).sum())
res["recon_thr_max_diff_vs_Y"] = float(np.nanmax(np.abs(thr - Y.p67_width.to_numpy())))
elig = ~np.isnan(thr)
res["min_margin_width_minus_thr"] = float(np.nanmin(np.abs(width - thr)))

# sensitivity to other readings (report only; the decision rule used is the spec's literal one above)
sens = {}
w_fill = (base.R_pts / base.entry_fill_raw).to_numpy()
r2, _, _ = decide(w_fill, base.date, cash, first); sens["raw_price=entry_fill"] = r2
glbx = pd.DatetimeIndex(ds.index)                         # every Globex session as a trading day
r3, _, _ = decide(width, base.date, glbx, first); sens["trading_days=all_globex_sessions"] = r3
r4, _, _ = decide(width, base.date, cash, first, strict=False); sens["above_inclusive"] = r4
r5, _, _ = decide(width, base.date, cash, pd.Timestamp(ds.index[ds.cash_day][0])); sens["history_from_2010_data_start"] = r5
res["sensitivity"] = {}
for k, r in sens.items():
    R_ = base.usd[r]
    res["sensitivity"][k] = {"n_flips_vs_main": int((r != rem).sum()), "removed": int(r.sum()),
                             "removed_usd": float(R_.sum()),
                             "removed_2010_17": float(base.usd[r & (base.date.dt.year <= 2017)].sum()),
                             "removed_2018_26": float(base.usd[r & (base.date.dt.year >= 2018)].sum())}

# ---- 3. pass rule
def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))
def dstats(df):
    dd_ = df.groupby("date").usd.sum().sort_index(); c = dd_.cumsum()
    c0 = np.r_[0.0, c.to_numpy()]
    return {"net": float(dd_.sum()), "max_dd": float((c.cummax() - c).max()),
            "max_dd_from0": float((np.maximum.accumulate(c0) - c0).max()), "worst_day": float(dd_.min())}

def evaluate(extra=0.0):
    T = base[["date", "usd", "raw_ref_price"]].copy(); T["usd"] -= extra; T["rem"] = rem
    K, Rm = T[~T.rem], T[T.rem]
    yr = T.date.dt.year
    a = {"full": float(Rm.usd.sum()), "2010_17": float(Rm.usd[Rm.date.dt.year <= 2017].sum()),
         "2018_26": float(Rm.usd[Rm.date.dt.year >= 2018].sum())}
    a["pass"] = bool(a["full"] < 0 and a["2010_17"] < 0 and a["2018_26"] < 0)
    tt = welch(K.usd, Rm.usd)
    b = {"t": tt, "kept_mean": float(K.usd.mean()), "removed_mean": float(Rm.usd.mean()), "pass": bool(tt >= 2.0),
         "t_eligible_only": welch(K.usd[elig[~T.rem.to_numpy()]], Rm.usd)}
    s0, s1 = dstats(T), dstats(K)
    c = {"before": s0, "after": s1, "pass": bool(s1["max_dd"] <= s0["max_dd"] and s1["worst_day"] >= s0["worst_day"]
                                                 and s1["max_dd_from0"] <= s0["max_dd_from0"])}
    out = {"kept_n": int(len(K)), "removed_n": int(len(Rm)), "kept_usd": float(K.usd.sum()), "a": a, "b": b, "c": c,
           "share_removed": float(T.rem.mean()), "share_removed_of_eligible": float(T.rem[elig].mean()),
           "PASS": bool(a["pass"] and b["pass"] and c["pass"])}
    per = {}
    for name, y0, y1 in [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020),
                         ("2021-23", 2021, 2023), ("2024-26", 2024, 2026), ("2023-26", 2023, 2026)]:
        m = (yr >= y0) & (yr <= y1)
        per[name] = {"n": int(m.sum()), "removed_n": int((m & T.rem).sum()), "kept_usd": float(T.usd[m & ~T.rem].sum()),
                     "removed_usd": float(T.usd[m & T.rem].sum()),
                     "share_removed": float(T.rem[m].mean()) if m.any() else None}
    out["eras"] = per
    # combined 3-model book
    allt = ref[["model", "date", "usd"]].copy(); allt["usd"] -= extra
    others = allt[allt.model != "overnight_break"][["date", "usd"]]
    out["book"] = {"before": dstats(pd.concat([others, T[["date", "usd"]]])),
                   "after": dstats(pd.concat([others, K[["date", "usd"]]]))}
    return out, T

r1, T1 = evaluate(0.0)
r2_, T2 = evaluate(1.0)
res["one_tick"], res["two_tick"] = r1, r2_

# ---- per-year CSV
rows = []
for y in sorted(T1.date.dt.year.unique()):
    g1 = T1[T1.date.dt.year == y]; g2 = T2[T2.date.dt.year == y]
    rows.append({"year": y, "trades": len(g1), "removed_n": int(g1.rem.sum()), "share_removed": round(g1.rem.mean(), 3),
                 "base_usd": g1.usd.sum(), "kept_usd": g1.usd[~g1.rem].sum(), "removed_usd": g1.usd[g1.rem].sum(),
                 "removed_usd_per_trade": round(g1.usd[g1.rem].mean(), 2) if g1.rem.any() else np.nan,
                 "kept_usd_per_trade": round(g1.usd[~g1.rem].mean(), 2),
                 "kept_usd_2tick": g2.usd[~g2.rem].sum(), "removed_usd_2tick": g2.usd[g2.rem].sum()})
py = pd.DataFrame(rows); py.to_csv(OUT + "W_per_year.csv", index=False)
dec = base[["date", "side", "usd", "R_pts", "raw_ref_price", "entry_fill_raw"]].copy()
dec["width"] = width; dec["p67_width"] = thr; dec["window_trades"] = nw; dec["eligible"] = elig
dec["decision"] = np.where(rem, "remove", "keep")
dec["X_decision"] = X.decision.values; dec["Y_decision"] = Y.decision.values
dec.to_csv(OUT + "W_decisions_final.csv", index=False)
json.dump(res, open(OUT + "W_recon_summary.json", "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ("one_tick", "two_tick")}, indent=1, default=str))
for k in ("one_tick", "two_tick"):
    r = res[k]; print(k, json.dumps({kk: r[kk] for kk in ("kept_n", "removed_n", "kept_usd", "a", "b", "c", "PASS",
                                                         "share_removed", "share_removed_of_eligible", "book")}, default=str))
    for e, v in r["eras"].items(): print("  ", e, v)
print(py.to_string())
