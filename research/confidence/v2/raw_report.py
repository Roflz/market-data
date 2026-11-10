"""
v2/raw_report.py - raw results of the v2 dataset (NO model): net $ per micro-trade and trades per year by exit, by
agreement score, by rule, by time-of-day block and by side, per market and timeframe, in the research rules' windows,
without the top 10 days, and against the DRIFT BENCHMARK = being in the trend at the same hours.

DRIFT BENCHMARK: each event trade is matched with 100 random rows of the trend pool (v2_trend_{sym}_{tf}.parquet:
  trend bars that are not events, same stop rule family, same exit) of the same side, session year, entry hour and
  stop-size quintile (risk_usd quintile within the year, over events + pool); null = the mean of its matches
  (ema50_check.matched_draws). edge = $/trade - null; tc = week-clustered t of the per-trade edge (ema50_check.cluster_t;
  |tc| > 2 is roughly 'unlikely to be luck', before counting how many things were tried).
'w/o top 10 days' drops the group's own 10 best days (by summed $) and compares with the null of the SAME remaining
  trades (the null keeps its lucky days: conservative for the setup).
Outputs (v2/out):
  v2_raw_exits.csv   market, tf, exit, side (all/long/short), span (2013..2025H1, 2018+, 2022+, 2010-20, 2021-25H1,
                     all, all w/o top 10 days, all w/o 2025H1): n, per_year, usd, null_usd, edge, tc, bars, R
  v2_raw_groups.csv  market, tf, exit, dim (rule / n_tf_agree / mtf_score / tod_block / side), value, span (all,
                     2010-20, 2021-25H1, 2018+, 2022+, all w/o top 10 days, all w/o 2025H1): same columns
Every (market, tf, exit, dim, value) cell is logged to out/trials.csv (module v2-dataset) unless --no-log.
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/raw_report.py [--no-log]
"""
import argparse
import json
import os
import time
import zlib

import numpy as np
import pandas as pd

import dataset as ds
import ema50_check as ec

OUT = ds.OUT
MARKETS = ("NQ", "ES", "YM")
N_DRAWS = 100
YEAR_SPANS = [str(y) for y in range(2013, 2025)] + ["2025H1"]
WIN_SPANS = ["2018+", "2022+", "2010-20", "2021-25H1", "all", "all w/o top 10 days", "all w/o 2025H1"]
GROUP_SPANS = ["all", "2010-20", "2021-25H1", "2018+", "2022+", "all w/o top 10 days", "all w/o 2025H1"]
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}


def span_masks(session):
    s = pd.DatetimeIndex(session)
    y = s.year
    out = {str(yy): np.asarray(y == yy) for yy in range(2013, 2025)}
    out["2025H1"] = np.asarray(y == 2025)
    out.update({"2018+": np.asarray(s >= "2018-01-01"), "2022+": np.asarray(s >= "2022-01-01"),
                "2010-20": np.asarray(s < "2021-01-01"), "2021-25H1": np.asarray(s >= "2021-01-01"),
                "all": np.ones(len(s), bool), "all w/o 2025H1": np.asarray(s < "2025-01-01")})
    return out


def years_of(session):
    s = pd.DatetimeIndex(session)
    return max((s.max() - s.min()).days / 365.25, 0.5)


def stats(p, nm, sess, week, m, n_years):
    """One cell: p = $ per trade, nm = matched null mean per trade, restricted to mask m."""
    n = int(m.sum())
    if n == 0:
        return dict(n=0, per_year=0.0, usd=np.nan, null_usd=np.nan, edge=np.nan, tc=np.nan)
    e = p[m] - nm[m]
    return dict(n=n, per_year=n / n_years, usd=p[m].mean(), null_usd=nm[m].mean(), edge=e.mean(),
                tc=ec.cluster_t(e, week[m]))


def top10_mask(p, sess, m, k=10):
    """m minus the k best days (by summed p) of the trades in m."""
    day = pd.Series(p[m]).groupby(sess[m]).sum()
    top = day.sort_values(ascending=False).index[:k]
    return m & ~np.isin(sess, top.to_numpy())


def cells(p, nm, sess, week, m, n_years, spans, SP):
    rows = []
    for sp in spans:
        if sp == "all w/o top 10 days":
            mm = top10_mask(p, sess, m)
            ny = n_years
        else:
            mm = m & SP[sp]
            ny = 1.0 if sp in YEAR_SPANS[:-1] else (0.5 if sp == "2025H1" else span_years(sp, n_years))
        rows.append(dict(span=sp, **stats(p, nm, sess, week, mm, ny)))
    return rows


_SPAN_YEARS = {"2018+": 7.5, "2022+": 3.5, "2021-25H1": 4.5, "all w/o 2025H1": None}


def span_years(sp, n_years):
    """Calendar years covered by a span (data: 2010 (YM 2018) .. 2025-06-30)."""
    if sp in ("all", "all w/o top 10 days"):
        return n_years
    if sp == "2010-20":
        return max(n_years - 4.5, 0.5)
    if sp == "all w/o 2025H1":
        return n_years - 0.5
    return min(_SPAN_YEARS[sp], n_years)


def run(log=True):
    if log:
        import run_pipeline as rp                                         # noqa: PLC0415
    ex_rows, gr_rows = [], []
    for sym in MARKETS:
        for tf in ds.TFS:
            t0 = time.time()
            pe, pt = ds.events_path(sym, tf), ds.trend_path(sym, tf)
            if not (os.path.exists(pe) and os.path.exists(pt)):
                print(f"skip {sym} {tf}: missing", flush=True)
                continue
            E = pd.read_parquet(pe)
            P = pd.read_parquet(pt)
            A = ec.add_risk_bucket(pd.concat([E[["session", "year", "risk_usd"]], P[["session", "year", "risk_usd"]]],
                                             ignore_index=True))
            E["rb"] = A.rb.to_numpy()[:len(E)]
            P["rb"] = A.rb.to_numpy()[len(E):]
            idx, level = ec.matched_draws(E, P, n_draws=N_DRAWS, seed=zlib.crc32(f"{sym}{tf}".encode()))
            sess = pd.DatetimeIndex(E.session).to_numpy()
            week = pd.factorize(pd.DatetimeIndex(E.session).to_period("W"))[0]
            SP = span_masks(E.session)
            n_years = years_of(pd.concat([E.session, P.session]))
            groups = {"side": {"long": E.d.to_numpy() > 0, "short": E.d.to_numpy() < 0}}
            groups["rule"] = {r: E[r].to_numpy() == 1 for r in ds.FLAGS}
            groups["rule"]["pb only"] = (E.pb.to_numpy() == 1) & (E.n_rules.to_numpy() == 1)
            groups["rule"]["2+ rules"] = E.n_rules.to_numpy() >= 2
            groups["n_tf_agree"] = {str(k): E.n_tf_agree.to_numpy() == k for k in range(4)}
            groups["mtf_score"] = {str(k): E.mtf_score.to_numpy() == k for k in range(4)}
            groups["tod_block"] = {k: E.tod_block.to_numpy() == k for k in ds.TOD_BLOCKS}
            allm = np.ones(len(E), bool)
            for x in ds.EXITS:
                p = E[f"pnl_{x}"].to_numpy(np.float64)
                nm = P[f"pnl_{x}"].to_numpy(np.float64)[idx].mean(1)
                bars = E[f"bars_{x}"].to_numpy(np.float64)
                Rr = E[f"R_{x}"].to_numpy(np.float64)
                key = dict(market=MICRO[sym], tf=tf, exit=x)
                for side, m in (("all", allm), ("long", groups["side"]["long"]), ("short", groups["side"]["short"])):
                    for c in cells(p, nm, sess, week, m, n_years, YEAR_SPANS + WIN_SPANS, SP):
                        mm = (m & SP[c["span"]]) if c["span"] in SP else top10_mask(p, sess, m)
                        ex_rows.append(dict(key, side=side, **c, bars=np.nanmean(bars[mm]) if mm.any() else np.nan,
                                            R=np.nanmean(Rr[mm]) if mm.any() else np.nan))
                for dim, G in groups.items():
                    for val, m in G.items():
                        cc = cells(p, nm, sess, week, m, n_years, GROUP_SPANS, SP)
                        for c in cc:
                            gr_rows.append(dict(key, dim=dim, value=val, **c))
                        if log:
                            a = {c["span"]: c for c in cc}
                            rp.log_trial(module="v2-dataset", scope=f"{sym}{tf}", model="no model (raw rule union)",
                                         target=x, oos_rows=a["all"]["n"],
                                         oos_usd_per_trade=round(float(a["all"]["usd"]), 2) if a["all"]["n"] else "",
                                         oos_usd_per_year=round(float(a["all"]["usd"] * a["all"]["per_year"]), 1)
                                         if a["all"]["n"] else "",
                                         baseline_usd_per_trade=round(float(a["all"]["null_usd"]), 2)
                                         if a["all"]["n"] else "",
                                         parameters=json.dumps(dict(tf=tf, exit=x, dim=dim, value=val)),
                                         note=f"baseline = trend-pool null (side/year/hour/stop matched); edge "
                                              f"{a['all']['edge']:.2f} tc {a['all']['tc']:.2f}; 2010-20 edge "
                                              f"{a['2010-20']['edge']:.2f}; 2021-25H1 edge {a['2021-25H1']['edge']:.2f}")
            print(f"{sym} {tf}m: {len(E):,} events, matched {np.mean(level == 4):.1%} on all 4 keys "
                  f"({time.time() - t0:.0f}s)", flush=True)
            pd.DataFrame(ex_rows).to_csv(os.path.join(OUT, "v2_raw_exits.csv"), index=False)
            pd.DataFrame(gr_rows).to_csv(os.path.join(OUT, "v2_raw_groups.csv"), index=False)
            del E, P, idx
    return pd.DataFrame(ex_rows), pd.DataFrame(gr_rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    run(log=not a.no_log)
