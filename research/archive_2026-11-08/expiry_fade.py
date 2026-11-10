"""Research only: options-expiry Friday reversal (Baltussen, Terstegge & Whelan, "The Derivative Payoff Bias").
Rules written down 2026-11-08 before running; 3 trials per market. Run from the project folder.

Expiry day = the third Friday of each month; if that is not a trading day, the trading day before it.
Data = CME 1-min bars, regular hours, unadjusted prices of the contract trading that day (lit_p5_orb.py loaders;
abnormal days with gaps in the data are skipped, as in P5).
  PRIMARY  short at the 9:30 bar open (1 tick adverse), cover at the 15:59 bar close (1 tick adverse); no stop
  A        same, but cover at the 11:59 bar close (12:00 ET), where the paper says the reversal is complete
  B        PRIMARY, only when the overnight move (prior close of the same contract -> 9:30 open) is positive
Costs: 1 tick each way + $1.00 per round trip (MES $3.50, MNQ $2.00). Results per 1 micro, and in bp of the entry
price (the size-free measure here, since there is no stop to define R).
Periods: 2010-2021 (inside the paper's 2003-2021 sample) and 2022-2026 (after it).
Control: the PRIMARY trade on every non-expiry day."""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import lit_p5_orb as p5

TK = p5.TICK
EXIT = {"PRIMARY": 389, "A": 149, "B": 389}


def expiry_days(dates):
    """Third Friday of each month, or the last trading day before it in that week."""
    ds = pd.DatetimeIndex(sorted(dates))
    out = []
    for (y, m), _ in pd.Series(ds, index=ds).groupby([ds.year, ds.month]):
        first = pd.Timestamp(y, m, 1)
        third_fri = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
        cand = ds[(ds <= third_fri) & (ds >= third_fri - pd.Timedelta(days=4))]
        if len(cand):
            out.append(cand.max())
    return set(out)


def tstat(x):
    x = np.asarray(x, float)
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan


rows, yearly = [], {}
for sym in ("NQ", "ES"):
    mk = p5.MARKETS[sym]
    dates, g, inst = p5.load_market(sym)
    sess, Cff, _ = p5.build_sessions(sym, dates, g, inst)
    sess = sess.reset_index(drop=True)
    prev_close = sess.day_close.shift().where(sess.same_prev)
    sess["overnight_bp"] = 1e4 * (sess.day_open / prev_close - 1)
    exp = expiry_days(sess.date[sess.trade_ok])
    sess["expiry"] = sess.date.isin(exp)
    O = g["Open"]
    recs = []
    for r in sess[sess.trade_ok].itertuples(index=False):
        ent = O[r.di, 0]
        if np.isnan(ent):
            continue
        for var, xs in EXIT.items():
            xs = min(xs, r.exit_slot)
            ext = Cff[r.di, xs]
            gross_pts = ent - ext                               # short
            net_pts = (ent - TK) - (ext + TK)
            recs.append(dict(date=r.date, expiry=r.expiry, var=var, on_bp=r.overnight_bp,
                             gross_bp=1e4 * gross_pts / ent, net_bp=1e4 * (net_pts - p5.COMM / mk["ppt"]) / ent,
                             usd=net_pts * mk["ppt"] - p5.COMM))
    d = pd.DataFrame(recs)
    d = d[~((d["var"] == "B") & ~(d.on_bp > 0))]
    d["year"] = pd.DatetimeIndex(d.date).year
    for per, lo, hi in (("2010-2021", 2010, 2021), ("2022-2026", 2022, 2026), ("ALL", 2010, 2026)):
        for var in ("PRIMARY", "A", "B"):
            x = d[d.expiry & (d["var"] == var) & d.year.between(lo, hi)]
            rows.append(dict(market=mk["micro"], period=per, rule=var, trades=len(x),
                             gross_bp=x.gross_bp.mean(), net_bp=x.net_bp.mean(), t_net=tstat(x.net_bp),
                             win_pct=100 * (x.usd > 0).mean(), usd_total=x.usd.sum(),
                             years_up=f"{int((x.groupby('year').usd.sum() > 0).sum())}/{x.year.nunique()}"))
        c = d[~d.expiry & (d["var"] == "PRIMARY") & d.year.between(lo, hi)]
        rows.append(dict(market=mk["micro"], period=per, rule="control: same trade, all other days", trades=len(c),
                         gross_bp=c.gross_bp.mean(), net_bp=c.net_bp.mean(), t_net=tstat(c.net_bp),
                         win_pct=100 * (c.usd > 0).mean(), usd_total=c.usd.sum(), years_up=""))
    e = d[d.expiry & (d["var"] == "PRIMARY")]
    for var in ("PRIMARY", "A"):
        x = d[d.expiry & (d["var"] == var)].sort_values("date")
        eq = x.usd.cumsum(); dd = (eq.cummax() - eq).max()
        w = x.nsmallest(3, "net_bp")
        print(f"{mk['micro']} {var}: worst trades " + ", ".join(f"{r.date:%Y-%m-%d} {r.net_bp:+.0f} bp (${r.usd:+,.0f})" for r in w.itertuples())
              + f"; max drawdown ${dd:,.0f}; longest losing run {int((x.usd <= 0).astype(int).groupby((x.usd > 0).cumsum()).sum().max())} trades")
    yearly[mk["micro"]] = e.groupby("year").usd.sum()
    on = sess[sess.expiry & sess.trade_ok].overnight_bp
    on_other = sess[~sess.expiry & sess.trade_ok].overnight_bp
    print(f"{mk['micro']}: overnight move into expiry days avg {on.mean():+.1f} bp (n {on.notna().sum()}, "
          f"positive {100 * (on > 0).mean():.0f}%); other days {on_other.mean():+.1f} bp")

r = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print(r.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))
print("\nPRIMARY, net $ per year at 1 micro:")
for k, v in yearly.items():
    print(f"  {k}: " + "  ".join(f"{y}:{u:+,.0f}" for y, u in v.items()))
