"""Does recent pullback structure predict the next pullback?  (light, no look-ahead, pre-holdout only)

For every pullback event (research/signals/out/pullbacks_{mkt}_{tf}.csv) build features ONLY from earlier events of the
same market/timeframe whose whole outcome window had ended at or before this event's bar
(i_event_j + n_window_j <= i_event_i; no_time events are skipped because they have no outcome):
  share_K   share of continuations among the last K resolved SAME-direction events (K = 3, 5, 10)
  dep3      mean depth of the last 3 same-direction pullbacks (known at their own event bars)
  since_ok  bars since the last resolved same-direction continuation finished its window
Targets: cont (1 = continuation, 0 = failure/neither), mfeR = mfe_pts / leg_pts (best move in units of the impulse leg).
Test: high history (share >= 0.6) minus low history (share <= 0.4); 95% interval from a session-block bootstrap
(Poisson(1) weights per session); placebo = the same statistic when each event's history is taken from a random
event on another session (A: any session, B: another session of the same year, which keeps slow regime drift).
"""
import sys
import numpy as np
import pandas as pd

OUT = "v3/regime/"
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
RNG = np.random.default_rng(7)
NB = 1000
NP = 300
SETS = [("ES", 15), ("NQ", 15), ("YM", 15), ("NQ", 5), ("NQ", 60)]
COLS = ["direction", "i_event", "n_window", "outcome", "t_event", "depth", "leg_pts", "mfe_pts", "to_SH_pts",
        "to_PL_pts", "year"]


def block(h):
    return np.select([(h >= 18) & (h <= 22), (h >= 23) | (h <= 2), (h >= 3) & (h <= 8), (h >= 9) & (h <= 11),
                      (h >= 12) & (h <= 16)], ["18-22", "23-02", "03-08", "09-11", "12-16"], "17")


def load(m, tf):
    d = pd.read_csv(f"../signals/out/pullbacks_{m}_{tf}.csv", usecols=COLS)
    d["t_event"] = pd.to_datetime(d.t_event)
    d = d[d.t_event < HOLDOUT].reset_index(drop=True)
    d["end"] = d.i_event + d.n_window
    d["sess"] = (d.t_event + pd.Timedelta(hours=6)).dt.normalize()
    d["blk"] = block(d.t_event.dt.hour.to_numpy())
    d["cont"] = (d.outcome == "continuation").astype(float)
    d["mfeR"] = (d.mfe_pts / d.leg_pts).clip(upper=5)
    return d


def features(d):
    for K in (3, 5, 10):
        d[f"share_{K}"] = np.nan
    d["dep3"] = np.nan
    d["since_ok"] = np.nan
    for dr in (1, -1):
        s = d[d.direction == dr]
        idx = s.index.to_numpy()
        ev = s.i_event.to_numpy()
        res = s[s.outcome != "no_time"]
        r_end = res.end.to_numpy()
        o = np.argsort(r_end, kind="stable")
        r_end, r_cont = r_end[o], res.cont.to_numpy()[o]
        cum = np.concatenate([[0], np.cumsum(r_cont)])
        nres = np.searchsorted(r_end, ev, side="right")          # resolved events with end <= this event bar
        for K in (3, 5, 10):
            ok = nres >= K
            v = np.full(len(ev), np.nan)
            v[ok] = (cum[nres[ok]] - cum[nres[ok] - K]) / K
            d.loc[idx, f"share_{K}"] = v
        okend = r_end[r_cont == 1]
        j = np.searchsorted(okend, ev, side="right") - 1
        d.loc[idx, "since_ok"] = np.where(j >= 0, ev - okend[np.maximum(j, 0)], np.nan)
        dep = s.depth.to_numpy()
        prev3 = pd.Series(dep).shift(1).rolling(3).mean().to_numpy()   # earlier events' depth is known at their bar
        d.loc[idx, "dep3"] = prev3
    return d


def diff_stat(x, y, sess_codes, w=None):
    """mean(y | x>=.6) - mean(y | x<=.4), session weights w"""
    hi, lo = (x >= 0.6), (x <= 0.4)
    ns = sess_codes.max() + 1
    if w is None:
        w = np.ones(ns)
    ww = w[sess_codes]
    a = (ww * hi * y).sum() / max((ww * hi).sum(), 1e-9)
    b = (ww * lo * y).sum() / max((ww * lo).sum(), 1e-9)
    return a - b, a, b, hi.sum(), lo.sum()


def boot(x, y, sc):
    ns = sc.max() + 1
    W = RNG.poisson(1.0, size=(NB, ns)).astype(float)
    hi, lo = (x >= 0.6).astype(float), (x <= 0.4).astype(float)
    # per-session sums -> fast
    def ss(v):
        return np.bincount(sc, weights=v, minlength=ns)
    Hn, Hy, Ln, Ly = ss(hi), ss(hi * y), ss(lo), ss(lo * y)
    st = (W @ Hy) / (W @ Hn) - (W @ Ly) / (W @ Ln)
    return np.percentile(st, [2.5, 97.5]), (st <= 0).mean()


def placebo(d, col, ycol, same_year):
    """history of a random event from another session (optionally same year)"""
    x = d[col].to_numpy()
    y = d[ycol].to_numpy()
    ok = ~np.isnan(x) & ~np.isnan(y)
    x, y = x[ok], y[ok]
    sess = d.sess.to_numpy()[ok]
    yr = d.year.to_numpy()[ok]
    res = []
    grp = {g: np.flatnonzero(yr == g) for g in np.unique(yr)} if same_year else {0: np.arange(len(x))}
    for _ in range(NP):
        xp = np.empty_like(x)
        for g, ii in grp.items():
            pick = RNG.integers(0, len(ii), size=len(ii))
            src = ii[pick]
            bad = sess[src] == sess[ii]
            while bad.any():                              # must come from a different session
                src[bad] = ii[RNG.integers(0, len(ii), size=bad.sum())]
                bad = sess[src] == sess[ii]
            xp[ii] = x[src]
        hi, lo = xp >= 0.6, xp <= 0.4
        res.append(y[hi].mean() - y[lo].mean())
    return np.array(res)


def test_rows(d, tag):
    rows = []
    for col in ("share_3", "share_5", "share_10"):
        for ycol in ("cont", "mfeR"):
            for half, sub in (("all", d), ("2010-17", d[d.year <= 2017]), ("2018-25H1", d[d.year >= 2018])):
                s = sub[~sub[col].isna() & ~sub[ycol].isna()]
                if len(s) < 200:
                    continue
                sc = pd.factorize(s.sess)[0]
                x, y = s[col].to_numpy(), s[ycol].to_numpy()
                dlt, a, b, nh, nl = diff_stat(x, y, sc)
                ci, p = boot(x, y, sc)
                r = dict(set=tag, feature=col, target=ycol, period=half, n=len(s), n_hi=nh, n_lo=nl,
                         base=y.mean(), hi=a, lo=b, diff=dlt, ci_lo=ci[0], ci_hi=ci[1], p_boot_le0=p)
                if half == "all":
                    pa = placebo(s, col, ycol, False)
                    pb = placebo(s, col, ycol, True)
                    r.update(plc_any_mean=pa.mean(), plc_any_p=(pa >= dlt).mean(),
                             plc_year_mean=pb.mean(), plc_year_p=(pb >= dlt).mean())
                rows.append(r)
    return rows


def main():
    allrows, years, tods, other = [], [], [], []
    for m, tf in SETS:
        tag = f"{m}_{tf}"
        d = features(load(m, tf))
        d.to_parquet(f"{OUT}pb_features_{tag}.parquet")
        allrows += test_rows(d, tag)
        # by year (share_5, continuation)
        for yv, s in d[~d.share_5.isna()].groupby("year"):
            hi, lo = s.share_5 >= 0.6, s.share_5 <= 0.4
            years.append(dict(set=tag, year=yv, n=len(s), base=s.cont.mean(), hi=s.cont[hi].mean(),
                              lo=s.cont[lo].mean(), diff=s.cont[hi].mean() - s.cont[lo].mean(),
                              mfe_diff=s.mfeR[hi].mean() - s.mfeR[lo].mean()))
        # time-of-day blocks
        for half, sub in (("all", d), ("2010-17", d[d.year <= 2017]), ("2018-25H1", d[d.year >= 2018])):
            for bk, s in sub.groupby("blk"):
                tods.append(dict(set=tag, period=half, block=bk, n=len(s), cont=s.cont.mean(),
                                 fail=(s.outcome == "failure").mean(), mfeR=s.mfeR.mean(),
                                 mfe_pts=s.mfe_pts.mean(), leg_pts=s.leg_pts.mean()))
        # other features: depth and time since last success (terciles, continuation)
        for col in ("dep3", "since_ok"):
            s = d[~d[col].isna()]
            q = pd.qcut(s[col], 3, labels=["low", "mid", "high"])
            for lab, g in s.groupby(q, observed=True):
                other.append(dict(set=tag, feature=col, tercile=lab, lo_edge=g[col].min(), hi_edge=g[col].max(),
                                  n=len(g), cont=g.cont.mean(), mfeR=g.mfeR.mean()))
        print(tag, len(d), "events", flush=True)
    pd.DataFrame(allrows).to_csv(f"{OUT}pb_memory_tests.csv", index=False)
    pd.DataFrame(years).to_csv(f"{OUT}pb_memory_by_year.csv", index=False)
    pd.DataFrame(tods).to_csv(f"{OUT}pb_tod_blocks.csv", index=False)
    pd.DataFrame(other).to_csv(f"{OUT}pb_depth_since.csv", index=False)


if __name__ == "__main__":
    main()
