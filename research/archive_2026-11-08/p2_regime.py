"""Research only: last-half-hour momentum (P2) by volatility regime. Rules written down before running (2026-11-08).
Uses lit_p2_lasthalfhour_trades.csv, variant (a) rows = every eligible day: side = sign of the prior close -> 15:30
return, entry 15:30 bar open, exit 15:59 bar close, 1 tick each way + $1.00 per round trip (MES $3.50, MNQ $2.00).
Regime = trailing 20-day realized volatility of 5-min RTH returns, known at the prior close, tercile against all
earlier days (250-session burn-in) -- the vol20_tercile column, so no future data.
Variants (3 new trials):
  M3  follow P2's side only in the most volatile third of days (literature: momentum when dealers are short gamma,
      which goes with high volatility)
  F1  take the OPPOSITE side only in the calmest third (the 2023-26 data looked like reversal; this idea came from
      looking at data, so only the years before June 2020 are a fair check of it)
  SW  M3 + F1 together, flat in the middle third
Reported by era: 2010-06..2013-12, 2014-01..2020-05, 2020-06..2026-11, and by year. Run from the project folder."""
import numpy as np
import pandas as pd

TICK, COMM = 0.25, 1.00
MULT = {"ES": 5.0, "NQ": 2.0}
ERAS = [("2010-13", "2010-01-01", "2013-12-31"), ("2014-20/05", "2014-01-01", "2020-05-31"),
        ("2020/06-26", "2020-06-01", "2026-12-31")]


def nw_t(x, lags=5):
    x = np.asarray(x, float)
    if len(x) < 10:
        return np.nan
    u = x - x.mean(); T = len(x); s = u @ u / T
    for j in range(1, lags + 1):
        s += 2 * (1 - j / (lags + 1)) * (u[j:] @ u[:-j]) / T
    return x.mean() / np.sqrt(s / T)


t = pd.read_csv("lit_p2_lasthalfhour_trades.csv", parse_dates=["date"])
a = t[(t.variant == "a") & t.vol20_tercile.notna()].copy()
a["M"] = a.market.map(MULT)
a["dir"] = np.where(a.side == "long", 1, -1)
a["entry_bp_base"] = a.entry_ref_price
fade_g = -a.gross_points
a["mom_net"] = a.net_usd
a["fade_net"] = (fade_g - 2 * TICK) * a.M - COMM
a["mom_gbp"] = a.gross_bp
a["fade_gbp"] = -a.gross_bp
a["drift_gbp"] = a.gross_bp * a.dir                                # always-long 15:30-16:00 move in bp


def pick(df, var):
    if var == "M3":
        d = df[df.vol20_tercile == 3]; return d.mom_net, d.mom_gbp, d
    if var == "F1":
        d = df[df.vol20_tercile == 1]; return d.fade_net, d.fade_gbp, d
    m = df.vol20_tercile == 3; f = df.vol20_tercile == 1
    d = df[m | f]
    return (np.where(d.vol20_tercile == 3, d.mom_net, d.fade_net),
            np.where(d.vol20_tercile == 3, d.mom_gbp, d.fade_gbp), d)


rows = []
for mkt in ("NQ", "ES"):
    for era, lo, hi in ERAS + [("ALL", "2010-01-01", "2026-12-31")]:
        df = a[(a.market == mkt) & (a.date >= lo) & (a.date <= hi)]
        for var in ("M3", "F1", "SW"):
            net, gbp, d = pick(df, var)
            net = pd.Series(np.asarray(net), index=d.date.values).sort_index()
            yrs = net.groupby(net.index.year).sum()
            rows.append({"market": mkt, "era": era, "variant": var, "trades": len(net),
                         "gross bp/tr": np.mean(gbp), "net $/tr": net.mean(), "net $ total": net.sum(),
                         "t (NW5)": nw_t(net.values), "years up": f"{int((yrs > 0).sum())}/{len(yrs)}",
                         "always-long bp": d.drift_gbp.mean()})
r = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print(r.to_string(index=False, float_format=lambda v: f"{v:,.2f}"))

print("\nSW (momentum when volatile, fade when calm), net $ per year at 1 micro:")
for mkt in ("NQ", "ES"):
    net, gbp, d = pick(a[a.market == mkt], "SW")
    s = pd.Series(np.asarray(net), index=d.date.values)
    print(f"  {mkt}: " + "  ".join(f"{y}:{v:+,.0f}" for y, v in s.groupby(s.index.year).sum().items()))

print("\nLong and short legs of M3 (most volatile third), net $/trade, all years:")
for mkt in ("NQ", "ES"):
    d = a[(a.market == mkt) & (a.vol20_tercile == 3)]
    print(f"  {mkt}: long {d[d.dir > 0].mom_net.mean():+.2f} (n {(d.dir > 0).sum()}), "
          f"short {d[d.dir < 0].mom_net.mean():+.2f} (n {(d.dir < 0).sum()})")
