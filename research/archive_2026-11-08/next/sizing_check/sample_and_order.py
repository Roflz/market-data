import os, sys, math, numpy as np, pandas as pd
W = os.path.dirname(os.path.abspath(__file__))
SZ = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/next/sizing"
os.chdir("/run/media/roflz/Disk 2/_/market_data"); sys.path.insert(0, ".")
import position_sizing as ps                      # read-only import of the builder's code
T, p26 = pd.read_pickle(f"{SZ}/sizing_trades_cache.pkl")
K = ps.expiry_k(T)[0]
X = pd.read_pickle(f"{W}/rebuild.pkl")
assert (T.model.values == X.model.values).all() and (T.date.values == X.date.values).all()
bp = {B: ps.simulate(T, B, False, p26, K) for B in (100, 200)}
bs200 = ps.simulate(T, 200, True, p26, K)
rng = np.random.default_rng(12345)
pick = []
for m, n in (("overnight_break", 10), ("opening_range", 10), ("expiry_fade", 4)):
    idx = X.index[(X.model == m) & X.date.dt.year.isin([2012, 2015, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026])]
    pick += sorted(rng.choice(idx, n, replace=False).tolist())
pick += X.index[(X.model != "expiry_fade") & (X.date >= "2026-06-01")][:4].tolist()     # a few recent ones
rows = []
for i in pick:
    r = X.loc[i]
    if r.model == "expiry_fade":
        stop = K * r.adr20_2; how = f"ADR20={r.adr20_2:.2f} x K={K:.3f}"
        ent, sp = r.price2, np.nan
    elif r.model == "opening_range":
        stop = r.stop_ind; how = f"9:30 open {r.oc:.2f}, 9:34 close {r.cc934:.2f}, candle {'low' if r.side=='long' else 'high'} {r.stop_px:.2f}"
        ent, sp = r.entry_px, r.stop_px
    else:
        stop = r.stop_ind; how = f"signal bar {r.sig_bar:%H:%M}, 2xATR14(5m)={r.stop_ind:.2f}"
        ent, sp = r.entry_px, r.stop_px
    rpc = 2 * stop + 2
    hand = {B: min(10, math.floor(B / rpc)) for B in (100, 200)}
    hs = min(10, math.floor(200 * r.price2 / p26 / rpc))
    rows.append(dict(model=r.model, date=f"{r.date:%Y-%m-%d}", side=r.side, entry=f"{r.entry_time:%H:%M}", fill=ent, stop_px=sp,
                     stop_pts=round(stop, 2), risk_1micro=round(rpc, 2), how=how,
                     c100_hand=hand[100], c100_builder=int(bp[100].contracts[i]), c200_hand=hand[200], c200_builder=int(bp[200].contracts[i]),
                     c200scaled_hand=hs, c200scaled_builder=int(bs200.contracts[i])))
R = pd.DataFrame(rows)
R["all_match"] = (R.c100_hand == R.c100_builder) & (R.c200_hand == R.c200_builder) & (R.c200scaled_hand == R.c200scaled_builder)
R.to_csv(f"{W}/hand_sample.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(R.drop(columns=["how"]).to_string(index=False)); print(R[["model", "date", "how"]].to_string(index=False))
print("sample size", len(R), "all match:", bool(R.all_match.all()))

# --- time-order test on builder's combined logic: drop the LAST trade of each multi-trade day, earlier sizes must not change
for B, sc in ((100, False), (200, False), (200, True)):
    full = ps.simulate(T, B, sc, p26, K, open_cap=ps.OPEN_CAP, day_limit=ps.DAY_LIMIT)
    last = T.groupby("date").cumcount(ascending=False) == 0
    multi = T.groupby("date").date.transform("size") > 1
    keep = ~(last & multi)
    T2 = T[keep].reset_index(drop=True)
    s2 = ps.simulate(T2, B, sc, p26, K, open_cap=ps.OPEN_CAP, day_limit=ps.DAY_LIMIT)
    diff = int((full.contracts[keep].to_numpy() != s2.contracts.to_numpy()).sum())
    # also: reversing a day's later trades' order must not change the first trade
    print(f"time order ${B} {'scaled' if sc else 'fixed'}: removing each day's last trade changed {diff} earlier sizes (expect 0)")
    # combined never sizes UP and never touches the first trade of a day
    plain = ps.simulate(T, B, sc, p26, K)
    first = T.groupby("date").cumcount() == 0
    print(f"   combined > plain on {(full.contracts > plain.contracts).sum()} trades; first-of-day changed {(full.contracts[first] != plain.contracts[first]).sum()}")
    # entries ordered by time within each day
    print("   entries sorted within day:", bool(T.groupby("date").entry_time.apply(lambda s: s.is_monotonic_increasing).all()))

# --- how often does the realised loss exceed the budget (gaps/slippage), 2019-2026, plain fixed $200 and scaled $200
for lab, S in (("fixed $200", bp[200]), ("scaled $200", bs200)):
    s = S[(S.date >= "2019-01-01") & (S.contracts > 0) & (S.model != "expiry_fade")]
    ratio = -s.net_usd / s.budget
    print(f"{lab}: taken {len(s)}, losses > budget {int((ratio > 1.0001).sum())} ({100*(ratio>1.0001).mean():.1f}%), worst loss = {ratio.max():.2f} x budget on {s.date[ratio.idxmax()]:%Y-%m-%d} {s.model[ratio.idxmax()]}")
    # risk actually taken vs budget
    print(f"   risk taken / budget: median {((s.contracts*s.risk_per_micro)/s.budget).median():.2f}")

# --- 2026 $100: which combined-rule bind turned +$699 into -$267?
c = pd.read_csv(f"{SZ}/sized_trades_fixed_combined_100.csv", parse_dates=["date"]); p = pd.read_csv(f"{SZ}/sized_trades_fixed_plain_100.csv", parse_dates=["date"])
dd = c[(c.contracts != p.contracts) & (c.date >= "2026-01-01")]
print(pd.concat([dd[["model","date","entry_time","exit_time","risk_per_micro","usd_1micro","contracts"]], p.loc[dd.index, "contracts"].rename("plain_contracts")], axis=1).to_string())
same_day = c[c.date.isin(dd.date)][["model","date","entry_time","exit_time","risk_per_micro","usd_1micro","contracts"]]
print(same_day.to_string())
