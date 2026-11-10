"""Skeptic re-run of the volatility-map headline numbers from the raw 1-minute bars."""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, __import__("os").path.dirname(__file__))
from grid import grid, pclose, biggap_cum, ROOT

ds = pd.read_pickle(f"{ROOT}/data/daily_sessions_NQ.pkl")
cash = set(pd.to_datetime(ds.index[ds.cash_day]).normalize().to_numpy().astype("datetime64[D]"))
cpi = set(pd.to_datetime(pd.read_csv(f"{ROOT}/data/cpi_dates.csv").date).to_numpy().astype("datetime64[D]"))


def slot_moves(sym):
    G = grid(sym)
    n = len(G["C"])
    bgc = biggap_cum(G)
    s = np.flatnonzero(G["et_min"] % 5 == 0)
    s = s[(s >= 1) & (s + 4 < n)]
    pr, ir, lr = pclose(G, s - 1)
    pe, ie, le = pclose(G, s + 4)
    ok = ~np.isnan(pr) & ~np.isnan(pe) & (ir == ie)
    # no gap > 5 missing minutes between the reference bar and the end bar
    ok &= (bgc[np.clip(le, 0, None)] - bgc[np.clip(lr, 0, None)]) == 0
    mv = np.where(ok, 1e4 * np.log(pe / pr), np.nan)
    df = pd.DataFrame({"sess": G["sess"][s], "et_min": G["et_min"][s], "mv": mv})
    df = df[ok]
    df = df[df.sess.isin(cash)]
    # session slots: 18:00 .. 16:55 (exclude 17:00-17:55)
    df = df[(df.et_min < 17 * 60) | (df.et_min >= 18 * 60)]
    df["yr"] = pd.DatetimeIndex(df.sess).year
    return df


def hm(x):
    return f"{x // 60:02d}:{x % 60:02d}"


for sym in ("NQ", "ES"):
    df = slot_moves(sym)
    df["a"] = df.mv.abs()
    for era, sub in (("all", df), ("2010-17", df[df.yr <= 2017]), ("2018-26", df[df.yr >= 2018])):
        g = sub.groupby("et_min").a
        mean = g.mean()
        dayavg = mean.mean()
        print(f"\n{sym} {era}: slots={len(mean)} day-avg slot={dayavg:.2f} bp  sessions={sub.sess.nunique()}")
        top = mean.sort_values(ascending=False).head(8)
        print("  top:", ", ".join(f"{hm(k)} {v:.2f} ({v / dayavg:.2f}x)" for k, v in top.items()))
        for t in (7 * 60, 8 * 60, 8 * 60 + 20, 8 * 60 + 25, 8 * 60 + 30, 8 * 60 + 35, 9 * 60, 9 * 60 + 25, 9 * 60 + 30,
                  10 * 60, 15 * 60 + 50, 3 * 60, 2 * 60 + 55):
            print(f"  {hm(t)} mean {mean[t]:.2f} med {g.median()[t]:.2f} rel {mean[t] / dayavg:.2f}x  vs prev slot {mean[t] / mean[t - 5]:.2f}x")
    # 8:30 slot CPI vs not
    s830 = df[df.et_min == 8 * 60 + 30]
    for era, sub in (("all", s830), ("2010-17", s830[s830.yr <= 2017]), ("2018-26", s830[s830.yr >= 2018])):
        c = sub.sess.isin(cpi)
        print(f"  8:30 {era}: CPI n={c.sum()} mean {sub.a[c].mean():.1f} med {sub.a[c].median():.1f} | nonCPI mean {sub.a[~c].mean():.2f}")
    # 2022 CPI
    c22 = s830[(s830.yr == 2022) & s830.sess.isin(cpi)]
    print(f"  CPI 2022 8:30 mean {c22.a.mean():.1f} n={len(c22)}")
    # signed drift t-stats at 09:55 and 09:25 (all slots: how many exceed |t|)
    g = df.groupby("et_min").mv
    tt = g.mean() / (g.std() / np.sqrt(g.count()))
    print(f"  signed t: 09:55 {tt[595]:.2f} 09:25 {tt[565]:.2f}; slots with |t|>3: {(tt.abs() > 3).sum()} of {len(tt)}; max {tt.abs().idxmax()}={tt.abs().max():.2f}")
    for t in (595, 565):
        x = df[df.et_min == t]
        for era, sub in (("2010-17", x[x.yr <= 2017]), ("2018-26", x[x.yr >= 2018])):
            print(f"    {hm(t)} {era}: mean {sub.mv.mean():+.3f} bp t {sub.mv.mean() / (sub.mv.std() / np.sqrt(len(sub))):+.2f} n={len(sub)}")
    df.to_parquet(f"{__import__('os').path.dirname(__file__)}/slots_{sym}.parquet")
