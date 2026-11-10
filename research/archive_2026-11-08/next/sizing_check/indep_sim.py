"""Independent sizing simulation from the raw rebuild (rebuild.pkl): own stops, own exit times, CSV 1-micro $."""
import os, sys, math, json, numpy as np, pandas as pd
W = os.path.dirname(os.path.abspath(__file__))
SZ = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/sizing"
os.chdir("/run/media/roflz/Disk 2/_/market_data")
X = pd.read_pickle(f"{W}/rebuild.pkl")
P26 = float(pd.read_pickle("data/daily_sessions_NQ.pkl").pipe(lambda d: d.close_raw[(d.index.year == 2026) & d.cash_day].mean()))
# expiry K: mean of the worst 10% of losses in ADR20 units (independent recompute)
e = X[(X.model == "expiry_fade") & X.adr20_2.notna()]
loss = np.sort((np.maximum(0, -e.usd_csv / 2) / e.adr20_2).to_numpy())[::-1]
K = loss[:math.ceil(0.1 * len(loss))].mean()
print(f"K_exp independent = {K:.4f} over {len(e)} trades")

ORDER = {"opening_range": 0, "overnight_break": 1, "expiry_fade": 2}
def size(budget, scaled, combined, cap=10):
    rows = []
    for day, g in X.groupby("date", sort=True):
        g = g.assign(o=g.model.map(ORDER)).sort_values(["entry_time", "o"])
        book = []                                         # (exit_time, n, rpc, usd)
        for r in g.itertuples():
            b = budget * (r.price2 / P26 if scaled else 1.0)
            stop = K * r.adr20_2 if r.model == "expiry_fade" else r.stop_ind
            if np.isnan(stop):                            # expiry with no ADR history: builder trades 1 micro
                rows.append((r.Index, 1, np.nan, b)); book.append((r.exit_time2 if False else r.exit_time, 1, 0.0, r.usd_csv)); continue
            rpc = 2 * stop + 2
            n = min(cap, math.floor(b / rpc))
            if combined and n > 0:
                openr = sum(k * q for (xt, k, q, u) in book if xt > r.entry_time)
                real = sum(k * u for (xt, k, q, u) in book if xt <= r.entry_time)
                n = min(n, max(0, math.floor((1.5 * b - openr) / rpc)))
                n = min(n, max(0, math.floor((2.0 * b - max(0.0, -real) - openr) / rpc)))
            rows.append((r.Index, n, rpc, b))
            xt = r.exit_time2 if r.model != "expiry_fade" else r.exit_time
            if n > 0: book.append((xt, n, rpc, r.usd_csv))
    S = pd.DataFrame(rows, columns=["i", "n", "rpc", "b"]).set_index("i").reindex(X.index)
    S["net"] = S.n * X.usd_csv
    S["date"] = X.date; S["model"] = X.model
    return S

def met(S, lo=None, hi=None):
    s = S if lo is None else S[S.date >= lo]
    if hi is not None: s = s[s.date <= hi]
    d = s.groupby("date").net.sum(); c = d.cumsum().to_numpy()
    dd = float((np.maximum.accumulate(np.r_[0, c])[1:] - c).max())
    yrs = (s.date.max() - s.date.min()).days / 365.25
    return dict(net=round(float(d.sum()), 2), per_yr=round(float(d.sum()) / yrs, 1), dd=round(dd, 2),
                worst_day=float(d.min()), worst_month=float(d.groupby(d.index.to_period("M")).sum().min()),
                skip_pct=round(100 * float((S.loc[s.index, "n"] == 0).mean()), 1))

summ = json.load(open(f"{SZ}/sizing_summary.json"))["scenarios"]
out = {}
for tag, (B, sc, cb) in {"fixed_plain_100": (100, False, False), "fixed_combined_100": (100, False, True),
                         "scaled_plain_100": (100, True, False), "scaled_combined_100": (100, True, True),
                         "fixed_plain_200": (200, False, False), "scaled_plain_200": (200, True, False),
                         "fixed_combined_200": (200, False, True), "scaled_combined_200": (200, True, True),
                         "fixed_plain_50": (50, False, False), "fixed_combined_50": (50, False, True)}.items():
    S = size(B, sc, cb)
    S.to_pickle(f"{W}/indep_{tag}.pkl")
    f = f"{SZ}/sized_trades_{tag}.csv"
    if os.path.exists(f):
        Bt = pd.read_csv(f)
        print(f"{tag}: per-trade contracts differ from builder's CSV on {int((Bt.contracts.values != S.n.values).sum())} of {len(S)} trades")
    for per, lo, hi in (("2026", "2026-01-01", None), ("2019_2026", "2019-01-01", None), ("full", None, None)):
        mine = met(S, pd.Timestamp(lo) if lo else None)
        theirs = summ[tag][per]
        out[f"{tag}|{per}"] = (mine, {k: round(theirs[k], 2) for k in ("net_usd", "net_per_year", "max_dd", "worst_day", "worst_month", "skipped_1micro_pct")})
        ok = abs(mine["net"] - theirs["net_usd"]) < 0.01 and abs(mine["dd"] - theirs["max_dd"]) < 0.01
        print(f"   {per:9s} mine net {mine['net']:>10,.2f} DD {mine['dd']:>9,.2f} wd {mine['worst_day']:>8,.0f} wm {mine['worst_month']:>8,.0f} | builder net {theirs['net_usd']:>10,.2f} DD {theirs['max_dd']:>9,.2f} wd {theirs['worst_day']:>8,.0f} wm {theirs['worst_month']:>8,.0f}  {'MATCH' if ok else 'DIFF'}")
# baseline 1 micro
S1 = X.assign(net=X.usd_csv)
for lo in ("2019-01-01", "2026-01-01"):
    print("1-micro baseline from", lo, met(S1.assign(n=1), pd.Timestamp(lo)))
ef = X[(X.model == "expiry_fade") & (X.date >= "2019-01-01")]
print("expiry fixed 1 micro 2019-2026: net", ef.usd_csv.sum(), "worst", ef.usd_csv.min())
json.dump({k: v for k, v in out.items()}, open(f"{W}/indep_metrics.json", "w"), indent=1, default=str)
