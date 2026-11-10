"""Research only (not part of the trading system): does volatility known before a trade relate to how the main model's
trades turn out? Main model as-is (2 x ATR stop, hold to 5 PM). Volatility is measured in % of the UNADJUSTED price
(point moves / the real contract price), so the roll back-adjustment can't distort it. Run from the project folder."""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import exits_compare as ec
import exits_engine as ee

pd.set_option("display.width", 200)
ec.init()


def raw_close(sym):
    r = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Close"])
    ts = pd.to_datetime(r.ts_event, utc=True).dt.tz_convert("America/New_York")
    r["sess"] = (ts + pd.Timedelta(hours=6)).dt.date
    return r.groupby("sess").Close.last()


def measures(sym):
    b = pd.read_pickle(f"data/x5_{sym}.pkl")
    px = raw_close(sym)
    prev_px = px.shift()                                       # real price level known before the session
    dp = b.Close.diff().where(b.sess.eq(b.sess.shift()))       # point moves inside one session (no roll jumps)
    rv_pts = np.sqrt((dp ** 2).groupby(b.sess).sum())
    on = (b.tmin >= 1080) | (b.tmin < 570)
    on_rng = b[on].groupby("sess").apply(lambda g: g.High.max() - g.Low.min())
    m = pd.DataFrame({"rv": rv_pts, "on": on_rng}).join(prev_px.rename("p"))
    m["rv_pct"] = 100 * m.rv / m.p * np.sqrt(252)               # session realized vol, annualized %
    m["on_pct"] = 100 * m.on / m.p
    out = pd.DataFrame(index=m.index)
    out["vol20"] = m.rv_pct.shift().rolling(20).mean()         # trailing 20 sessions, before today
    out["vol_prev"] = m.rv_pct.shift()                         # yesterday
    out["vol_change"] = out.vol_prev / out.vol20                # yesterday vs its 20-day norm
    out["on_range"] = m.on_pct / m.on_pct.shift().rolling(20).mean()   # today's overnight range vs normal (known 9:30)
    return out


for sym in ("NQ", "ES"):
    D = ec.G[sym]; sp = ee.SPEC[sym]
    t = ee.run(D, ec.G[("sets", sym)]["Overnight break + daily trend"], "hold", k0=2.0)
    b = t.bar.to_numpy()
    t["R"] = (t.pts - sp["comm"] / sp["usd"]) / t.R_pts
    t["usd"] = t.pts * sp["usd"] - sp["comm"]
    t["year"], t["sess"], t["hour"] = D.year[b], D.sess[b], D.tmin[b] // 60
    M = measures(sym)
    t = t.join(M, on="sess")
    print(f"\n################ {sp['micro']}: {len(t)} trades ################")
    print("Sanity: median 20-day vol by year (annualized %):",
          ", ".join(f"{y}: {v:.0f}" for y, v in t.groupby("year").vol20.median().items()))
    for col, label in (("vol20", "20-day realized vol (regime)"), ("vol_prev", "yesterday's realized vol"),
                       ("vol_change", "yesterday vs 20-day norm"), ("on_range", "overnight range vs 20-day norm")):
        x = t.dropna(subset=[col])
        rho, p = spearmanr(x[col], x.R)
        # quintiles over the whole sample (descriptive), and within each year (removes the 2011-17 vs 2018-26 split)
        x["q"] = pd.qcut(x[col], 5, labels=[1, 2, 3, 4, 5])
        x["qy"] = x.groupby("year")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
        tab = x.groupby("q").agg(trades=("R", "size"), lo=(col, "min"), hi=(col, "max"), avg_R=("R", "mean"),
                                 win=("R", lambda r: 100 * (r > 0).mean()), usd=("usd", "sum"))
        tab["avg_R within-year"] = x.groupby("qy").R.mean().values
        top, bot = x[x.q == 5].R, x[x.q == 1].R
        tdiff = (top.mean() - bot.mean()) / np.sqrt(top.var() / len(top) + bot.var() / len(bot))
        rho_y = np.mean([spearmanr(g[col], g.R)[0] for _, g in x.groupby("year") if len(g) > 20])
        print(f"\n-- {label}: Spearman rho with R = {rho:+.3f} (p {p:.3f}); average within-year rho {rho_y:+.3f}; "
              f"top vs bottom fifth t = {tdiff:+.2f}")
        print(tab.round(3).to_string())
        if col == "vol20":
            for era, g in (("2011-17", x[x.year <= 2017]), ("2018-26", x[x.year >= 2018])):
                g = g.assign(q=pd.qcut(g[col], 3, labels=["low", "mid", "high"]))
                print(f"   {era} by tercile (avg R, n): " + ", ".join(
                    f"{k}: {v.R.mean():+.3f} ({len(v)})" for k, v in g.groupby("q")))


print("\n################ CHECK: same relationships before costs (gross R), and cost per trade in R ################")
for sym in ("NQ", "ES"):
    D = ec.G[sym]; sp = ee.SPEC[sym]
    t = ee.run(D, ec.G[("sets", sym)]["Overnight break + daily trend"], "hold", k0=2.0)
    b = t.bar.to_numpy()
    t["gross_R"] = (t.pts + 2 * ee.SLIP) / t.R_pts
    t["cost_R"] = (2 * ee.SLIP + sp["comm"] / sp["usd"]) / t.R_pts
    t["R"] = t.gross_R - t.cost_R
    t["year"], t["sess"] = D.year[b], D.sess[b]
    t = t.join(measures(sym), on="sess")
    print(f"\n{sp['micro']}")
    for col in ("vol20", "vol_prev", "vol_change", "on_range"):
        x = t.dropna(subset=[col]).copy()
        x["qy"] = x.groupby("year")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
        g = x.groupby("qy").agg(gross_R=("gross_R", "mean"), cost_R=("cost_R", "mean"), net_R=("R", "mean"))
        top, bot = x[x.qy == 5].gross_R, x[x.qy == 1].gross_R
        tdiff = (top.mean() - bot.mean()) / np.sqrt(top.var() / len(top) + bot.var() / len(bot))
        rho = np.mean([spearmanr(gg[col], gg.gross_R)[0] for _, gg in x.groupby("year") if len(gg) > 20])
        print(f"  {col:10s} within-year fifths, gross R: " + "  ".join(f"{v:+.3f}" for v in g.gross_R) +
              f" | cost R: " + " ".join(f"{v:.3f}" for v in g.cost_R) + f" | top-bottom t {tdiff:+.2f}, within-year rho {rho:+.3f}")
