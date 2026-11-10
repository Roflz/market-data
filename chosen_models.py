"""
The three chosen MNQ models as one system (review doc, "Chosen models"), with the agreed expiry-Friday rule:
on monthly options-expiry days only the expiry fade trades; both breakout models skip those days.
Only stock-market trading days are traded (Globex-only holiday sessions are skipped by all three).
  1 overnight_break   first close beyond the overnight high/low 9:35-15:00 with the 20-day trend (setup_rule.py),
                      stop 2 x ATR(5-min), hold to the 5 PM close (exits_engine.py)
  2 opening_range     first 5-minute candle direction at 9:35, stop at the candle's other end, no target, exit at the
                      15:59 close (12:59 on early-close days); the published A5T rule of lit_p5_orb.py, but every
                      take/skip decision uses only what is known at 9:35 (lit_p5_orb.py itself also skips days with a
                      data gap anywhere in the session, which is hindsight; here a halt after entry is traded through,
                      and the stop fills at the first price after the gap)
  3 expiry_fade       third Friday of each month (calendar_days.expiry_fridays): short at the 9:30 bar open, cover at
                      the 15:59 bar close, no stop (Baltussen, Terstegge & Whelan, "The Derivative Payoff Bias")
Skip-day rules (adopted after a robustness check; review doc section 10):
  R1  no breakout trades (models 1 and 2) on the day after the S&P 500 closed down 2% or more (known before the open)
  R2  no opening_range trade on scheduled Fed statement days (calendar_days.fomc_days)
  The trades these rules remove are saved to chosen_models_skipped.csv so we can keep checking they stay bad.
Costs: 1 tick each way + $1.00 per round trip (exits_engine.SPEC / lit_p5_orb.COMM), 1 micro per trade.
Output: chosen_models_trades.csv (model, date, side, exit, usd, R where a stop defines risk, bp of the raw entry price)
Usage:  PYTHONPATH=./pylib python3 chosen_models.py
"""
import warnings

import numpy as np
import pandas as pd

import calendar_days as cd
import exits_compare as ec
import exits_engine as ee
import lit_p5_orb as p5

warnings.filterwarnings("ignore")
SYM = "NQ"
K = 5                                       # opening-range candle length (minutes)
SKIP_AFTER_SPX_DROP = -2.0                  # R1: % S&P 500 move on the prior day at or below which breakouts skip
SKIP_ORB_ON_FED = True                      # R2


def skip_days():
    """Dates on which each skip rule applies (all known before that day's open)."""
    ctx = pd.read_pickle("data/market_context.pkl")
    after_drop = set(ctx.index[ctx.spx_ret_1d_prev <= SKIP_AFTER_SPX_DROP])
    return after_drop, (cd.fomc_days() if SKIP_ORB_ON_FED else set())


def sessions():
    return pd.read_pickle(f"data/daily_sessions_{SYM}.pkl")


def overnight_break(expiry, cash_days, ds):
    ec.init()
    D, sp = ec.G[SYM], ee.SPEC[SYM]
    t = ee.run(D, ec.G[("sets", SYM)]["Overnight break + daily trend"], "hold", k0=2.0)
    b = t.bar.to_numpy()
    date = pd.to_datetime(D.sess[b])
    adj = (ds.close_adj - ds.close_raw).reindex(date).to_numpy()       # back-adjustment is constant within a session
    net_pts = t.pts - sp["comm"] / sp["usd"]
    out = pd.DataFrame({"model": "overnight_break", "date": date, "side": np.where(t.dir > 0, "long", "short"),
                        "exit": t.exit, "usd": net_pts * sp["usd"], "R": net_pts / t.R_pts,
                        "bp": 1e4 * net_pts / (D.Close[b] - adj)})
    return out[out.date.isin(cash_days) & ~out.date.isin(expiry)]


def opening_range(expiry, sess, g, Cff):
    ppt, min_R = p5.MARKETS[SYM]["ppt"], p5.MARKETS[SYM]["min_R"]
    O, H, L = g["Open"], g["High"], g["Low"]
    rows = []
    for r in sess.itertuples(index=False):
        i = r.di
        if r.date in expiry or np.isnan(O[i, 0]) or np.isnan(O[i, K]):   # need the 9:30 bar and the 9:35 entry bar
            continue                                                    # (as the published rule; candle = bars present)
        oc, cc = O[i, 0], Cff[i, K - 1]
        if cc == oc:
            continue
        d = 1 if cc > oc else -1
        stop = np.nanmin(L[i, :K]) if d > 0 else np.nanmax(H[i, :K])
        if d * (cc + d * p5.TICK - stop) < min_R:                      # cost filter judged on the 9:34 close (known)
            continue
        ref, fill = O[i, K], O[i, K] + d * p5.TICK
        s_x = r.exit_slot
        if d * (fill - stop) <= 0:                                      # opened through the stop: out at once
            xs, xfill, why, R = K, ref - d * p5.TICK, "stop", d * (cc + d * p5.TICK - stop)
        else:
            xs, _, xfill, why = p5.run_trade(H[i], L[i], O[i], Cff[i, s_x], K, s_x, d, stop, None, True)
            R = d * (fill - stop)
        net_pts = d * (xfill - fill) - p5.COMM / ppt
        rows.append(dict(model="opening_range", date=r.date, side="long" if d > 0 else "short", exit=why,
                         usd=net_pts * ppt, R=net_pts / R, bp=1e4 * net_pts / ref))
    return pd.DataFrame(rows)


def expiry_fade(expiry, sess, g, Cff):
    ppt = p5.MARKETS[SYM]["ppt"]
    rows = []
    for r in sess[sess.date.isin(expiry)].itertuples(index=False):
        ent, ext = g["Open"][r.di, 0], Cff[r.di, min(p5.FULL_EXIT_SLOT, r.exit_slot)]
        if np.isnan(ent) or np.isnan(ext):                              # needs the 9:30 bar (known at entry)
            continue
        net_pts = (ent - p5.TICK) - (ext + p5.TICK) - p5.COMM / ppt
        rows.append(dict(model="expiry_fade", date=r.date, side="short", exit="close", usd=net_pts * ppt, R=np.nan,
                         bp=1e4 * net_pts / ent))
    return pd.DataFrame(rows)


def main():
    ds = sessions()
    cash_days = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash_days)
    dates, g, inst = p5.load_market(SYM)
    sess, Cff, _ = p5.build_sessions(SYM, dates, g, inst)               # valid sessions (exchange holidays removed)
    sess = sess[sess.date.isin(cash_days)]
    T = pd.concat([overnight_break(expiry, cash_days, ds), opening_range(expiry, sess, g, Cff),
                   expiry_fade(expiry, sess, g, Cff)], ignore_index=True)
    T = T.sort_values(["date", "model"]).reset_index(drop=True)
    after_drop, fed = skip_days()
    breakout = T.model.isin(["overnight_break", "opening_range"])
    T["skip_rule"] = np.where(breakout & T.date.isin(after_drop), "R1 after S&P -2%",
                              np.where((T.model == "opening_range") & T.date.isin(fed), "R2 Fed day", ""))
    skipped = T[T.skip_rule != ""]
    skipped.to_csv("chosen_models_skipped.csv", index=False)
    T = T[T.skip_rule == ""].drop(columns="skip_rule").reset_index(drop=True)
    T.to_csv("chosen_models_trades.csv", index=False)
    print(f"{len(expiry)} expiry Fridays; saved chosen_models_trades.csv ({len(T):,} trades)")
    for (m, rule), g_ in skipped.groupby(["model", "skip_rule"]):
        print(f"  skipped {m} by {rule}: {len(g_)} trades that would have made ${g_.usd.sum():+,.0f}")
    for m, g_ in T.groupby("model", sort=False):
        y = g_.groupby(g_.date.dt.year).usd.sum()
        print(f"  {m:16s} {len(g_):5d} trades {g_.date.min():%Y-%m-%d} -> {g_.date.max():%Y-%m-%d}  net ${g_.usd.sum():>10,.0f}  "
              f"years up {(y > 0).sum()}/{len(y)}")
    d = T.groupby("date").usd.sum()
    print(f"  combined: net ${d.sum():,.0f} over {len(d)} trading days; worst day ${d.min():,.0f}; "
          f"max drawdown ${(d.cumsum().cummax() - d.cumsum()).max():,.0f}")


if __name__ == "__main__":
    main()
