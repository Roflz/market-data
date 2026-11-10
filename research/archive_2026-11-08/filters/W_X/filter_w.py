"""Filter W: skip overnight-break trades whose stop width (R_pts / raw price) is above the 67th percentile of the widths
of all live OB trades dated in the previous 250 trading days (strictly before the trade date)."""
import json, numpy as np, pandas as pd
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/W_X/"
P = pd.read_pickle(OUT + "ob_trades.pkl")
T = P["live"].copy()
cal = pd.DatetimeIndex(P["cash_days"]).sort_values()
first = P["first_sess"]
assert first in cal
pos = cal.get_indexer(T.date); assert (pos >= 0).all()
k0 = cal.get_loc(first)
T["cal_pos"] = pos
T["hist_days"] = pos - k0                              # trading days of model history strictly before the date
# window: trades with cal_pos in [pos-250, pos-1]  (vectorized via sorted cumulative positions)
tp = T.cal_pos.to_numpy(); w = T.width.to_numpy()
lo = np.searchsorted(tp, tp - 250, side="left"); hi = np.searchsorted(tp, tp, side="left")
assert (np.diff(tp) >= 0).all()
p67 = np.array([np.percentile(w[a:b], 67) if b > a else np.nan for a, b in zip(lo, hi)])
T["n_window"] = hi - lo
T["window_start"] = cal[np.maximum(tp - 250, 0)]
T["p67_width"] = p67
T["eligible"] = T.hist_days >= 250
T["remove"] = T.eligible & (T.width > T.p67_width)
T["decision"] = np.where(T.remove, "remove", "keep")
cols = ["date", "side", "usd", "signal_bar_open", "entry_bar_open", "exit_bar_open", "exit", "R_pts", "atr5_signal",
        "close_adj_signal", "back_adj", "raw_px", "width", "hist_days", "window_start", "n_window", "p67_width",
        "eligible", "decision", "gross_pts", "net_pts", "bp", "R"]
T[cols].to_csv(OUT + "W_decisions.csv", index=False)
pd.to_pickle(T, OUT + "W_decisions.pkl")

def dd(daily):
    c = daily.cumsum(); return float((c.cummax() - c).max())
def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))
def summ(x):
    return dict(n=int(len(x)), usd=round(float(x.usd.sum()), 2), usd_per_trade=round(float(x.usd.mean()), 3) if len(x) else None)

K, R = T[~T.remove], T[T.remove]
y = T.date.dt.year
res = {"n_total": len(T), "usd_total": float(T.usd.sum()), "kept": summ(K), "removed": summ(R),
       "share_removed": float(T.remove.mean()), "share_removed_of_eligible": float(T.remove[T.eligible].mean()),
       "n_eligible": int(T.eligible.sum()), "first_eligible_date": str(T.date[T.eligible].min().date())}
r1 = R[R.date.dt.year <= 2017]; r2 = R[R.date.dt.year >= 2018]
a = {"removed_full": float(R.usd.sum()), "removed_2010_17": float(r1.usd.sum()), "removed_2018_26": float(r2.usd.sum())}
a["pass"] = bool(a["removed_full"] < 0 and a["removed_2010_17"] < 0 and a["removed_2018_26"] < 0)
t_ = welch(K.usd, R.usd)
b = {"welch_t_kept_minus_removed": t_, "kept_mean": float(K.usd.mean()), "removed_mean": float(R.usd.mean()), "pass": t_ >= 2.0}
d0 = T.groupby("date").usd.sum(); d1 = K.groupby("date").usd.sum()
c = {"dd_before": dd(d0), "dd_after": dd(d1), "worst_day_before": float(d0.min()), "worst_day_after": float(d1.min())}
c["pass"] = bool(c["dd_after"] <= c["dd_before"] and c["worst_day_after"] >= c["worst_day_before"])
# also drawdown measured from a $0 start (alternative)
def dd0(daily):
    c = np.r_[0, daily.cumsum().to_numpy()]; return float((np.maximum.accumulate(c) - c).max())
c["dd_before_from0"], c["dd_after_from0"] = dd0(d0), dd0(d1)
res.update(a=a, b=b, c=c, passed=bool(a["pass"] and b["pass"] and c["pass"]))

# report-only
eras = [(2010, 2013), (2014, 2017), (2018, 2020), (2021, 2023), (2024, 2026), (2023, 2026)]
def block(lo_, hi_, adj=0.0):
    m = (y >= lo_) & (y <= hi_); g = T[m].copy(); g["usd"] -= adj
    k, r = g[~g.remove], g[g.remove]
    return dict(n=int(len(g)), base_usd=round(float(g.usd.sum()), 1), kept_n=int(len(k)), kept_usd=round(float(k.usd.sum()), 1),
                removed_n=int(len(r)), removed_usd=round(float(r.usd.sum()), 1),
                removed_per_trade=round(float(r.usd.mean()), 2) if len(r) else None,
                kept_per_trade=round(float(k.usd.mean()), 2) if len(k) else None,
                share_removed=round(float(len(r) / len(g)), 3) if len(g) else None)
res["eras"] = {f"{a_}-{b_}": block(a_, b_) for a_, b_ in eras}
res["years"] = {int(yy): block(yy, yy) for yy in sorted(y.unique())}
# 2 ticks per fill: $1 less per trade
T2 = T.copy(); T2["usd"] -= 1.0
K2, R2 = T2[~T2.remove], T2[T2.remove]
res["two_tick"] = {"kept_usd": float(K2.usd.sum()), "removed_usd": float(R2.usd.sum()),
                   "removed_2010_17": float(R2[R2.date.dt.year <= 2017].usd.sum()),
                   "removed_2018_26": float(R2[R2.date.dt.year >= 2018].usd.sum()),
                   "welch_t": welch(K2.usd, R2.usd),
                   "dd_before": dd(T2.groupby("date").usd.sum()), "dd_after": dd(K2.groupby("date").usd.sum()),
                   "worst_before": float(T2.groupby("date").usd.sum().min()), "worst_after": float(K2.groupby("date").usd.sum().min()),
                   "eras": {f"{a_}-{b_}": block(a_, b_, 1.0) for a_, b_ in eras}}
# combined 3-model book
import os
book = pd.read_csv(os.getcwd() + "/chosen_models_trades.csv", parse_dates=["date"])
assert (book.model == "overnight_break").sum() == len(T)
ob_idx = book.index[book.model == "overnight_break"]
bk = book.loc[ob_idx].reset_index().merge(T[["date", "side", "usd", "remove"]].assign(k=T.groupby(["date", "side"]).cumcount()),
                                         left_on=["date", "side", book.loc[ob_idx].groupby(["date", "side"]).cumcount().to_numpy()],
                                         right_on=["date", "side", "k"], how="left", suffixes=("", "_w"))
assert len(bk) == len(T) and (bk.usd == bk.usd_w).all()
drop = set(bk.loc[bk.remove, "index"])
B0 = book.groupby("date").usd.sum(); B1 = book.drop(index=list(drop)).groupby("date").usd.sum()
B1 = B1.reindex(B0.index, fill_value=0.0)
res["book"] = {"usd_before": float(B0.sum()), "usd_after": float(B1.sum()), "dd_before": dd(B0), "dd_after": dd(B1),
               "worst_day_before": float(B0.min()), "worst_day_after": float(B1.min()), "n_trades_removed": len(drop)}
json.dump(res, open(OUT + "W_summary.json", "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ("years",)}, indent=1, default=str))
print(pd.DataFrame(res["years"]).T.to_string())
