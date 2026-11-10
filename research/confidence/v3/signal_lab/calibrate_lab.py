"""
calibrate_lab.py - REAL-DATA SELF-TEST of signal lab v1: does the lab tell true from false on our own pre-holdout data?

For one market x timeframe panel (bars cut before the locked holdout 2025-06-30 18:00 ET):
  A. NULL (must NOT be detected beyond the nominal 5%): 200 random signals with no information by construction,
     cycling 3 shapes: continuous AR(0.95)-within-session, clustered +-1 events (~23% of bars), rare +-1 events
     (~1 per session). Reports the share with p < 0.05 for each p method and target, the per-metric decision p,
     the share of 20-metric batches with ANY q < 0.10 (family-wise), and how many get a CONFIRMED / REAL verdict.
  B. NEGATIVE CONTROLS with REAL signals (7 textbook metrics): (i) circularly shifted by whole sessions (5 random
     shifts >= 20 sessions), (ii) computed on ANOTHER market's bars and pasted onto random days of this market.
     Same structure as the real signal (time-of-day pattern, persistence), but no timing link to these prices.
  C. LOOK-AHEAD (v1.1): 7 leaky metrics must fail the truncation check at every seed - 3 that change every row (next
     bar's direction, whole-sample z-score, centred moving average) and 4 RARE yes/no candle-style leaks that change
     only their own event bars (inside bar labelled with its next bar's breakout, big bar whose next bar closes beyond
     it, big bar traded in the next bar's opening-gap direction, ~1% 'next bar continues' flag); 2 honest metrics and
     the 7 textbook metrics must pass at every seed; in a batch every leaky metric must come out INVALID.
  D. POSITIVE CONTROLS (must be detected, with sensible size):
       range_ratio  last bar's range / R20 -> next bar's range (volatility clustering)
       range4_ratio mean range of the last 4 bars / R20 -> next 4 bars' range
       time_of_day  typical next-bar range of this time-of-day slot (profile from the FIRST half of sessions,
                    tested on the second half only; slot control removed) -> next bar's range (U-shape)
       news_830     decision bar right before 8:30 ET on jobs-report (NFP) or CPI days -> next bar's range, vs the
                    same time of day on other days (dates: research/archive_2026-11-08/tests/s13_X/nfp_dates_src.txt,
                    data/cpi_dates.csv)
       reversal     this bar's return -> next bar's return (direction, tiny but real; last-bar control removed)
  E. POWER by injection into REAL prices: a known extra move of delta R20 is added after the events of random
     signals (rare +-1 events, and top-vs-bottom fifth of a continuous signal), the FULL pipeline is re-run, and the
     detection rate is recorded per delta -> power curve and the minimum detectable effect (MDE80, 80% detection),
     in R20 and in $ per micro, for (a) a single pre-registered metric (p < 0.05) and (b) as if it were one of 100
     metrics in a batch (BY-corrected p and replication in both halves = the lab's CONFIRMED rule).

  F. (v1.1, 'classes' pass) FOUR-WAY CLASSES in $: edges planted so that their TRUE $ per trade at 2018-25 bar sizes
     is 0, 1x, 2x the round trip (and two reviewer cases at 1.5x) -> how often each class is given (run_classes).

Outputs: v3/signal_lab/out/calibration/calib_{SYM}_{TF}_{null,neg,pos,power,real}.csv + calib_{SYM}_{TF}.json
         summary step: self_test_status.json (read by the impact cards) + calibration_report.md

  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3:v3/signal_lab \
      OMP_NUM_THREADS=3 nice -n 5 python3 v3/signal_lab/calibrate_lab.py run ES,NQ 15,60
  ... python3 v3/signal_lab/calibrate_lab.py lookahead|classes|mde ES,NQ,YM 15,60   (single passes, v1.1)
  ... python3 v3/signal_lab/calibrate_lab.py summary [log]        (log = append the real-signal rows to trials.csv)
Light: one 15-min panel at a time (~1.5 GB peak); about 3-4 minutes per 15-min panel, ~1 minute per 60-min panel.
"""
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd

import harness as H
import lab as L
from test_lab import _ar_within

OUTD = os.path.join(L.OUT, "calibration")
ROOT = os.path.abspath(os.path.join(L.HERE, "..", "..", "..", ".."))
FAST = dict(power=False, event_study=False, ic=False)
N_NULL, N_SHIFT = 200, 5
DELTAS = (0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20)
N_REP = 8
if os.environ.get("CAL_QUICK"):                  # plumbing check only
    N_NULL, N_SHIFT, N_REP, DELTAS = 21, 1, 1, (0.02, 0.2)
    OUTD = os.path.join(L.OUT, "calibration_quick")
BY_M = 200                                       # 100 metrics x (direction + size) p-values in a batch
BY_CUT = 0.05 / (BY_M * (np.log(BY_M) + 0.5772))  # ~4.3e-5: p needed for BY q < 0.05 as the best of 100 metrics


# ------------------------------------------------------------------------------------------------ real signals
def r20_of(b):
    r = (b.H - b.L)
    return r.groupby(b.run).transform(lambda s: s.rolling(20, min_periods=20).mean()).clip(lower=1e-9)


def sig_ema_gap(b):
    return (b.C - b.ema20) / b.atr14


def sig_mom(b):
    return b.mom14 - 100.0


def sig_vwap(b):
    return (b.C > b.vwap).astype(float).where(b.vwap.notna())


def sig_big_bar(b):
    r = (b.H - b.L)
    avg = r.groupby(b.run).transform(lambda s: s.rolling(20, min_periods=20).mean().shift(1))
    return pd.Series(np.where(r > 2 * avg, np.sign(b.C - b.O), 0.0), index=b.index).where(avg.notna())


def sig_bar_ret(b):
    return (b.C - b.O) / r20_of(b)


def sig_back4(b):
    same = b.seg.eq(b.seg.shift(4))
    return ((b.C - b.C.shift(4)) / r20_of(b)).where(same)


def sig_range_ratio(b):
    return (b.H - b.L) / r20_of(b)


def sig_range4_ratio(b):
    r4 = (b.H - b.L).groupby(b.run).transform(lambda s: s.rolling(4, min_periods=4).mean())
    return r4 / r20_of(b)


REAL = {"ema20_gap": (sig_ema_gap, "continuous"), "momentum14": (sig_mom, "continuous"),
        "above_vwap": (sig_vwap, "state"), "big_bar_follow": (sig_big_bar, "sided"),
        "bar_return": (sig_bar_ret, "continuous"), "back4_return": (sig_back4, "continuous"),
        "range_ratio": (sig_range_ratio, "continuous")}
OTHER = {"ES": "NQ", "NQ": "YM", "YM": "ES"}


def flat_of(b, tf):
    sess = pd.DatetimeIndex(b["session"]).normalize()
    code, uni = pd.factorize(sess, sort=True)
    mins = ((b.index.hour * 60 + b.index.minute).to_numpy() - 18 * 60) % 1440
    Pn = int(math.ceil(L.SESSION_MIN / tf))
    return code * Pn + mins // tf, len(uni), Pn


def to_grid(flat, T, Pn, x):
    g = np.full(T * Pn, np.nan)
    g[flat] = np.asarray(x, float)
    return g.reshape(T, Pn)


# ------------------------------------------------------------------------------------------------ helpers
def news_dates():
    nfp = pd.read_csv(os.path.join(ROOT, "research/archive_2026-11-08/tests/s13_X/nfp_dates_src.txt"), sep=" ",
                      header=None, usecols=[0]).iloc[:, 0]
    cpi = pd.read_csv(os.path.join(ROOT, "data/cpi_dates.csv")).date
    return (set(pd.to_datetime(nfp).dt.normalize()), set(pd.to_datetime(cpi).dt.normalize()))


def rows_of(r, tag, extra=None):
    t = r["table"]
    d = dict(name=r["name"], tag=tag, kind=r["kind"], n=r["n_valid"], n_sig=r["n_top"], p_dir=r["p_dir"],
             p_size=r["p_size"], best_dir=r["best_dir"], dir_effect=t.at[r["best_dir"], "effect"],
             best_size=r["best_size"], size_pct=t.at[r["best_size"], "pct_vs_avg"], cost_r20=r["cost_r20"],
             dir_inside_cost=r["dir_inside_cost"])
    for c in ("dir_h1", "dir_h4", "dir_h16", "abs_h4", "rng_h1", "path"):
        for pc in ("p_boot", "p_nw", "p_placebo", "p_repair", "p"):
            if pc in t:
                d[f"{c}:{pc}"] = t.at[c, pc]
        d[f"{c}:t"] = t.at[c, "effect"] / t.at[c, "se_boot"]
        d[f"{c}:t_naive"] = t.at[c, "t_iid_bar"]
    d.update(extra or {})
    return d


def null_signal(i, P, rng):
    a = _ar_within(rng, P.sess_code, 0.95)
    k = i % 3
    if k == 0:
        return a, "continuous", "ar_cont"
    if k == 1:
        return np.where(a > 1.2, 1.0, np.where(a < -1.2, -1.0, 0.0)), "sided", "clustered_events"
    ev = rng.random(P.n) < 1.0 / P.P
    return np.where(ev, np.where(rng.random(P.n) < 0.5, 1.0, -1.0), 0.0), "sided", "rare_events"


def fwer_batches(results, size=20):
    hits = []
    for i0 in range(0, len(results) - size + 1, size):
        Bb = L.batch_table(results[i0:i0 + size])
        hits.append(bool((Bb.q_dir < 0.10).any() or (Bb.q_size < 0.10).any()))
    return hits


def mde_from_curve(deltas, rates, target=0.8):
    d, r = np.asarray(deltas, float), np.asarray(rates, float)
    ok = np.flatnonzero(r >= target)
    if not len(ok):
        return np.nan
    j = ok[0]
    if j == 0:
        return float(d[0])
    x0, x1, y0, y1 = np.log(d[j - 1]), np.log(d[j]), r[j - 1], r[j]
    return float(np.exp(x0 + (target - y0) * (x1 - x0) / max(y1 - y0, 1e-9)))


# ------------------------------------------------------------------------------------------------ one panel
def run_panel(sym, tf):
    t0 = time.time()
    os.makedirs(OUTD, exist_ok=True)
    tag = f"{sym}_{tf}"
    b = H.bars(sym, tf)
    assert b.index.max() < pd.Timestamp("2025-06-30 18:00"), "holdout leak"
    P = L.Panel(b, sym, tf)
    b = P.bars
    log = [f"[{sym} {tf}m] panel {P.n} bars, {P.T} sessions, build {P.build_s:.1f}s"]
    print(log[-1], flush=True)
    summ = dict(sym=sym, tf=tf, n_bars=P.n, n_sessions=P.T, date=f"{pd.Timestamp.now():%Y-%m-%d %H:%M}")
    era_of = P.year_s[P.sess_code]
    eraB = era_of >= 2018

    # ---------------- A. null
    rng = np.random.default_rng(1000 + tf + {"ES": 0, "NQ": 1, "YM": 2}[sym] * 7)
    nres, nrows = [], []
    for i in range(N_NULL):
        x, kind, shape = null_signal(i, P, rng)
        r = L.evaluate(P, x, kind, name=f"null{i}_{shape}", **FAST)
        nres.append(r)
        nrows.append(rows_of(r, shape))
    Bn = L.batch_table(nres)
    N = pd.DataFrame(nrows)
    N["dir_verdict"], N["size_verdict"], N["dir_class"] = Bn.dir_verdict.values, Bn.size_verdict.values, Bn.dir_class.values
    N.to_csv(os.path.join(OUTD, f"calib_{tag}_null.csv"), index=False)
    hits = fwer_batches(nres)
    pcols = [c for c in N.columns if ":" in c and c.split(":")[1].startswith("p")]
    summ["null"] = dict(
        n=N_NULL, fpr_p_dir=float((N.p_dir < 0.05).mean()), fpr_p_size=float((N.p_size < 0.05).mean()),
        fpr_by_col={c: float((N[c] < 0.05).mean()) for c in pcols},
        sd_t_h16_honest=float(N["dir_h16:t"].std()), sd_t_h16_naive=float(N["dir_h16:t_naive"].std()),
        fwer_batches_any_q10=float(np.mean(hits)), n_batches=len(hits),
        n_dir_confirmed=int((N.dir_verdict == "CONFIRMED").sum()), n_dir_possible=int((N.dir_verdict == "possible").sum()),
        n_size_confirmed=int((N.size_verdict == "CONFIRMED").sum()),
        class_counts=N.dir_class.value_counts().to_dict(),
        fpr_p_dir_by_shape=N.groupby("tag").p_dir.apply(lambda s: float((s < 0.05).mean())).to_dict())
    print(f"[{sym} {tf}m] null done {time.time() - t0:.0f}s: p_dir<0.05 {summ['null']['fpr_p_dir']:.3f}, "
          f"classes {summ['null']['class_counts']}", flush=True)

    # ---------------- real textbook signals (reference) + B. negative controls
    xs = {k: np.asarray(fn(b), float) for k, (fn, kind) in REAL.items()}
    rres, rrows = [], []
    for k, (fn, kind) in REAL.items():
        r = L.evaluate(P, xs[k], kind, name=k, power=True, n_power=20, event_study=False)
        rres.append(r)
        rrows.append(rows_of(r, "real", dict(mde80_h4=(r["power"] or {}).get("mde80", np.nan))))
    Br = L.batch_table(rres)
    Br.to_csv(os.path.join(OUTD, f"calib_{tag}_real.csv"), index=False)
    G = {k: to_grid(P.flat, P.T, P.P, v) for k, v in xs.items()}
    neg, negrows = [], []
    for k, (fn, kind) in REAL.items():
        for s in rng.choice(P.shifts, N_SHIFT, replace=False):
            x = np.roll(G[k], int(s), axis=0).ravel()[P.flat]
            r = L.evaluate(P, x, kind, name=f"{k}_shift{s}", **FAST)
            neg.append(r)
            negrows.append(rows_of(r, "session_shift", dict(signal=k, shift=int(s))))
    ob = H.bars(OTHER[sym], tf)
    ofl, oT, oP = flat_of(ob, tf)
    for k, (fn, kind) in REAL.items():
        Go = to_grid(ofl, oT, oP, np.asarray(fn(ob), float))
        for j in range(3):
            pick = rng.choice(oT, P.T, replace=oT < P.T)
            x = Go[pick].ravel()[P.flat]
            r = L.evaluate(P, x, kind, name=f"{k}_from{OTHER[sym]}{j}", **FAST)
            neg.append(r)
            negrows.append(rows_of(r, "other_market_days", dict(signal=k, source=OTHER[sym])))
    del ob, Go
    Bg = L.batch_table(neg)
    NG = pd.DataFrame(negrows)
    for c in ("dir_verdict", "size_verdict", "dir_class"):
        NG[c] = Bg[c].values
    NG.to_csv(os.path.join(OUTD, f"calib_{tag}_neg.csv"), index=False)
    summ["neg"] = dict(n=len(NG), fpr_p_dir=float((NG.p_dir < 0.05).mean()), fpr_p_size=float((NG.p_size < 0.05).mean()),
                       fpr_p_dir_by_type=NG.groupby("tag").p_dir.apply(lambda s: float((s < 0.05).mean())).to_dict(),
                       fpr_p_size_by_type=NG.groupby("tag").p_size.apply(lambda s: float((s < 0.05).mean())).to_dict(),
                       n_dir_confirmed=int((NG.dir_verdict == "CONFIRMED").sum()),
                       n_size_confirmed=int((NG.size_verdict == "CONFIRMED").sum()),
                       class_counts=NG.dir_class.value_counts().to_dict(),
                       size_fpr_by_signal=NG.groupby("signal").p_size.apply(lambda s: float((s < 0.05).mean())).to_dict())
    summ["real"] = Br[["metric", "kind", "best_dir", "dir_effect", "p_dir", "q_dir", "dir_verdict", "dir_class",
                       "cost_r20", "best_size", "size_pct", "p_size", "size_verdict", "mde80"]].to_dict("records")
    print(f"[{sym} {tf}m] negatives done {time.time() - t0:.0f}s: dir p<0.05 {summ['neg']['fpr_p_dir']:.3f}, "
          f"size p<0.05 {summ['neg']['fpr_p_size']:.3f}", flush=True)

    # ---------------- C. look-ahead (v1.1: rare yes/no leaks, 100 cuts per check, verdict override)
    summ["lookahead"] = lookahead_section(P, sym, tf)

    # ---------------- D. positive controls
    pos, posrows = [], []

    def add_pos(name, PP, x, kind, col, expect, note=""):
        r = L.evaluate(PP, x, kind, name=name, power=False, event_study=False)
        t = r["table"]
        Bp = L.batch_table([r]).iloc[0]
        posrows.append(dict(control=name, kind=kind, col=col, expect=expect, n=r["n_valid"], n_sig=r["n_top"],
                            effect=t.at[col, "effect"], ci_lo=t.at[col, "ci_lo"], ci_hi=t.at[col, "ci_hi"],
                            pct_vs_avg=t.at[col, "pct_vs_avg"], p=t.at[col, "p"],
                            p_repair_emp=t.at[col, "p_repair_emp"],
                            years_same=int(t.at[col, "years_same"]), years_n=int(t.at[col, "years_n"]),
                            raw_sig=t.at[col, "raw_top"], raw_base=t.at[col, "raw_base"],
                            size_verdict=Bp.size_verdict, dir_verdict=Bp.dir_verdict, dir_class=Bp.dir_class,
                            detected=bool((np.sign(t.at[col, "effect"]) == expect) and t.at[col, "p"] < 0.001
                                          and t.at[col, "years_same"] >= 0.6 * t.at[col, "years_n"]), note=note))
        pos.append(r)

    add_pos("range_ratio", P, xs["range_ratio"], "continuous", "rng_h1", +1, "top vs bottom fifth of last bar range/R20")
    add_pos("range4_ratio", P, np.asarray(sig_range4_ratio(b), float), "continuous", "rng_h4", +1)
    # time of day: profile of next-bar range by slot from the first half of sessions, tested on the second half
    first = P.sess_code < P.T // 2
    Yr1 = P.Y[:, L.COL["rng_h1"]]
    prof = pd.Series(Yr1[first & P.ok]).groupby(P.pos[first & P.ok]).median()
    x_tod = np.where(~first, prof.reindex(P.pos).to_numpy(), np.nan)
    P_ns = L.Panel(b, sym, tf, fe=tuple(f for f in L.FE_DEFAULT if f != "slot"))
    add_pos("time_of_day", P_ns, x_tod, "continuous", "rng_h1", +1,
            "slot profile from sessions 1..T/2, tested on T/2..T, slot control removed")
    del P_ns
    # 8:30 news
    nfp, cpi = news_dates()
    mins = (b.index.hour * 60 + b.index.minute).to_numpy()
    end = mins + tf
    pre830 = (end <= 8 * 60 + 30) & (8 * 60 + 30 < end + tf)
    day = b.index.normalize()
    isn = pd.Index(day).isin(list(nfp | cpi))
    ev = (pre830 & isn).astype(float)
    ev_slot = pre830.astype(float)
    add_pos("news_830", P, np.where(pre830, ev, 0.0), "event", "rng_h1", +1,
            f"decision bar closing just before 8:30 ET on NFP/CPI days ({int(ev.sum())} events) vs all other bars "
            "(slot control compares with the same time of day)")
    # reversal (direction), last-bar control removed
    P_np = L.Panel(b, sym, tf, fe=tuple(f for f in L.FE_DEFAULT if f != "prev"))
    add_pos("reversal", P_np, xs["bar_return"], "continuous", "dir_h1", -1, "last-bar-sign control removed")
    del P_np
    PS = pd.DataFrame(posrows)
    # U-shape in points (second half of sessions): median bar range by bar start time
    rngpts = pd.Series((b.H - b.L).to_numpy()[~first], index=mins[~first])
    ushape = rngpts.groupby(level=0).median()
    pick = [3 * 60, 8 * 60 + 15, 8 * 60 + 30, 9 * 60 + 30, 12 * 60, 15 * 60 + 45, 20 * 60] if tf == 15 else \
        [3 * 60, 8 * 60, 9 * 60, 12 * 60, 15 * 60, 20 * 60]
    summ["ushape_pts"] = {f"{m // 60:02d}:{m % 60:02d}": float(ushape.get(m, np.nan)) for m in pick}
    nm = pd.Series((b.H - b.L).to_numpy(), index=b.index)
    nb = nm[np.r_[False, pre830[:-1]].astype(bool)]              # the bar AFTER the decision bar (contains 8:30)
    nb_day = pd.Index(nb.index.normalize()).isin(list(nfp | cpi))
    summ["news_bar_pts"] = dict(news_median=float(nb[nb_day].median()), other_median=float(nb[~nb_day].median()),
                                n_news=int(nb_day.sum()))
    PS.to_csv(os.path.join(OUTD, f"calib_{tag}_pos.csv"), index=False)
    summ["pos"] = PS.to_dict("records")
    print(f"[{sym} {tf}m] positives done {time.time() - t0:.0f}s: " +
          ", ".join(f"{r.control} {r.effect:+.3f} ({r.pct_vs_avg:+.0f}%) p={r.p:.2g} det={r.detected}"
                    for r in PS.itertuples()), flush=True)

    # ---------------- E. power by injection into real prices
    prow = []
    medr20_B = None
    for shape in ("rare_events", "continuous"):
        for rep in range(N_REP):
            rg = np.random.default_rng(5000 + rep + (0 if shape == "rare_events" else 100))
            if shape == "rare_events":
                evm = rg.random(P.n) < 1.0 / P.P
                x = np.where(evm, np.where(rg.random(P.n) < 0.5, 1.0, -1.0), 0.0)
                kind, inj = "sided", x
                sig_rows = P.ok & (x != 0)
            else:
                x = _ar_within(rg, P.sess_code, 0.95)
                kind = "continuous"
                q = np.quantile(x[P.ok], [0.2, 0.8])
                top, bot = P.ok & (x > q[1]), P.ok & (x <= q[0])
                inj = 0.5 * top - 0.5 * bot                     # top-minus-bottom contrast = delta
                sig_rows = top | bot
            usd_B = float(np.mean(P.r20[sig_rows & eraB]) * P.usd)     # v1.1: MEAN R20 of the trades (was median)
            cost_B = P.cost_usd / usd_B                                 # break-even per trade in R20 (was mean cost/R20)
            for dl in DELTAS:
                Q = P.injected(dl * inj)
                r = L.evaluate(Q, x, kind, name=f"pw_{shape}_{rep}_{dl}", placebo=False, **FAST)
                t = r["table"]
                bd = r["best_dir"]
                e = t.at[bd, "effect"]
                # replication in both halves (chronological if both exist, else alternate quarters), one-sided 5%
                zs = [t.at[bd, f"z_{h}"] for h in (("2010-17", "2018-25H1") if np.isfinite(t.at[bd, "z_2010-17"])
                                                   else ("Qodd", "Qeven"))]
                rep_ok = all(np.isfinite(z) and z > 1.645 for z in zs)
                strict = (r["p_dir"] < BY_CUT and e > 0 and rep_ok and t.at[bd, "years_same"] >= 0.6 * t.at[bd, "years_n"]
                          and t.at[bd, "p_repair_emp"] < 0.05)
                prow.append(dict(shape=shape, rep=rep, delta=dl, effect_h4=t.at["dir_h4", "effect"],
                                 se_h4=t.at["dir_h4", "se_boot"], p_dir=r["p_dir"], best=bd,
                                 detect_single=bool(r["p_dir"] < 0.05 and e > 0), detect_strict=bool(strict),
                                 cost_r20_B=cost_B, usd_per_r20_B=usd_B, n_sig=int(sig_rows.sum())))
                del Q
            print(f"[{sym} {tf}m] power {shape} rep {rep} done {time.time() - t0:.0f}s", flush=True)
    PW = pd.DataFrame(prow)
    PW.to_csv(os.path.join(OUTD, f"calib_{tag}_power.csv"), index=False)
    # recovered injection: effect at h4 minus the delta=0 baseline is approximated by the mean over reps
    curve = PW.groupby(["shape", "delta"]).agg(single=("detect_single", "mean"), strict=("detect_strict", "mean"),
                                               eff=("effect_h4", "mean"), se=("se_h4", "median"),
                                               cost_B=("cost_r20_B", "mean"), usd_B=("usd_per_r20_B", "mean"),
                                               n_sig=("n_sig", "mean")).reset_index()
    summ["power"] = {}
    for shape, g in curve.groupby("shape"):
        g = g.sort_values("delta")
        m1 = mde_from_curve(g.delta, g.single)
        m2 = mde_from_curve(g.delta, g.strict)
        scale = 0.5 if shape == "continuous" else 1.0
        usd = float(g.usd_B.mean())
        summ["power"][shape] = dict(
            curve=g[["delta", "single", "strict", "eff"]].to_dict("records"), n_sig=float(g.n_sig.mean()),
            mde80_single_r20=m1, mde80_strict_r20=m2, se_h4_r20=float(g.se.median()),
            mde80_single_usd_per_trade=scale * m1 * usd if np.isfinite(m1) else np.nan,
            mde80_strict_usd_per_trade=scale * m2 * usd if np.isfinite(m2) else np.nan,
            cost_r20_B=float(g.cost_B.mean()), usd_per_r20_B=usd, cost_usd=P.cost_usd,
            recovered_slope=float(np.polyfit(g.delta, g.eff, 1)[0]))
    print(f"[{sym} {tf}m] power done {time.time() - t0:.0f}s: " + json.dumps(
        {k: (round(v['mde80_single_r20'], 4), round(v['mde80_strict_r20'], 4)) for k, v in summ["power"].items()}),
        flush=True)
    summ["seconds"] = time.time() - t0
    with open(os.path.join(OUTD, f"calib_{tag}.json"), "w") as f:
        json.dump(summ, f, indent=1, default=float)
    return summ


# ------------------------------------------------------------------------------------------------ look-ahead (v1.1)
def _avg20(bb):
    r = bb.H - bb.L
    return r, r.groupby(bb.run).transform(lambda s: s.rolling(20, min_periods=20).mean().shift(1))


def leak_inside_breakout(bb):       # inside bar labelled with the side its NEXT bar closes beyond it (~6% of bars)
    ins = (bb.H < bb.H.shift(1)) & (bb.L > bb.L.shift(1)) & bb.run.eq(bb.run.shift(1))
    up, dn = ins & (bb.C.shift(-1) > bb.H), ins & (bb.C.shift(-1) < bb.L)
    return pd.Series(np.where(up, 1.0, np.where(dn, -1.0, 0.0)), index=bb.index)


def leak_bigbar_follow(bb):         # big bar (> 2x average) whose NEXT bar closes beyond it, stamped on the big bar
    r, avg = _avg20(bb)
    big = r > 2.0 * avg
    up, dn = big & (bb.C > bb.O) & (bb.C.shift(-1) > bb.H), big & (bb.C < bb.O) & (bb.C.shift(-1) < bb.L)
    return pd.Series(np.where(up, 1.0, np.where(dn, -1.0, 0.0)), index=bb.index).where(avg.notna())


def leak_next_open_gap(bb):         # big bar (> 1.5x average) traded in the direction of the NEXT bar's opening gap
    r, avg = _avg20(bb)
    return pd.Series(np.where(r > 1.5 * avg, np.sign(bb.O.shift(-1) - bb.C), 0.0), index=bb.index).where(avg.notna())


def leak_very_rare(bb):             # very rare: range > 3x average AND the next bar continues (~1% of bars)
    r, avg = _avg20(bb)
    big = r > 3.0 * avg
    s = np.sign(bb.C - bb.O)
    cont = np.sign(bb.C.shift(-1) - bb.C) == s
    return pd.Series(np.where(big & cont, s, 0.0), index=bb.index).where(avg.notna())


def honest_inside_bar(bb):          # honest twin: inside bar in the direction of its own close vs its midpoint
    ins = (bb.H < bb.H.shift(1)) & (bb.L > bb.L.shift(1)) & bb.run.eq(bb.run.shift(1))
    mid = (bb.H + bb.L) / 2
    return pd.Series(np.where(ins & (bb.C > mid), 1.0, np.where(ins & (bb.C < mid), -1.0, 0.0)), index=bb.index)


LEAKY = {"next_bar_direction": (lambda bb: np.sign(bb.C.shift(-1) - bb.C), "sided"),
         "whole_sample_zscore": (lambda bb: (bb.C - bb.ema20) / (bb.C - bb.ema20).std(), "continuous"),
         "centred_average": (lambda bb: bb.C.rolling(5, center=True).mean() - bb.C, "continuous"),
         "inside_bar_next_breakout": (leak_inside_breakout, "sided"),
         "big_bar_next_close_beyond": (leak_bigbar_follow, "sided"),
         "big_bar_next_open_gap": (leak_next_open_gap, "sided"),
         "very_rare_next_bar_continues": (leak_very_rare, "sided")}
HONEST = {"honest_ema20_gap": (sig_ema_gap, "continuous"), "honest_inside_bar": (honest_inside_bar, "sided")}


def run_lookahead(sym, tf, n_seeds=5):
    """Re-run only section C (look-ahead) and update the 'lookahead' section of calib_{SYM}_{TF}.json."""
    b = H.bars(sym, tf)
    assert b.index.max() < pd.Timestamp("2025-06-30 18:00"), "holdout leak"
    out = lookahead_section(L.Panel(b, sym, tf), sym, tf, n_seeds)
    f = os.path.join(OUTD, f"calib_{sym}_{tf}.json")
    s = json.load(open(f)) if os.path.exists(f) else {}
    s["lookahead"] = out
    with open(f, "w") as fh:
        json.dump(s, fh, indent=1, default=float)
    return out


def lookahead_section(P, sym, tf, n_seeds=5):
    """(C, v1.1) Look-ahead guard on real bars: 7 leaky metrics (3 that change every row + 4 rare yes/no candle-style
    leaks that change only their event bars) must be flagged at EVERY seed; 2 honest metrics and the 7 textbook metrics
    must pass at every seed; in a batch every leaky metric must come out INVALID. Also records how often the old 3-cut
    test missed each one."""
    t0 = time.time()
    b = P.bars
    allm = {**{k: (fn, kd, "leaky") for k, (fn, kd) in LEAKY.items()},
            **{k: (fn, kd, "honest") for k, (fn, kd) in HONEST.items()},
            **{k: (fn, kd, "textbook") for k, (fn, kd) in REAL.items()}}
    res = {}
    for k, (fn, kd, grp) in allm.items():
        ns = n_seeds if grp != "textbook" else 2
        chk = [L.lookahead_check(fn, b, seed=s) for s in range(ns)]
        x = np.asarray(fn(b), float)
        d = dict(group=grp, kind=kd, event_share=float(np.mean(np.nan_to_num(x) != 0)), seeds=ns,
                 flagged_seeds=int(sum(not c["ok"] for c in chk)), first_bad=chk[0]["first_bad"],
                 bad_target_cuts=f"{chk[0]['n_bad_target']}/{chk[0]['n_target']}",
                 bad_random_cuts=f"{chk[0]['n_bad_random']}/{chk[0]['n_random']}", seconds=chk[0]["seconds"])
        if grp == "leaky":
            d["old3_missed_of_10"] = int(sum(L.lookahead_check(fn, b, n_cuts=3, seed=s)["ok"] for s in range(10)))
        res[k] = d
        print(f"[{sym} {tf}m lookahead] {k}: flagged {d['flagged_seeds']}/{ns} seeds, share {d['event_share']:.4f}"
              + (f", old 3-cut test missed {d['old3_missed_of_10']}/10" if grp == "leaky" else ""), flush=True)
    sig = {k: dict(fn=fn, kind=kd) for k, (fn, kd, grp) in allm.items() if grp in ("leaky", "honest")}
    Bv, rv = L.evaluate_many(sig, panels={(sym, tf): P}, write=False, verbose=False, power=False, event_study=False)
    ov = {r_.metric: dict(lookahead=r_.lookahead, dir_verdict=r_.dir_verdict, size_verdict=r_.size_verdict,
                          dir_class=r_.dir_class, raw_p_dir=float(r_.p_dir), raw_effect=float(r_.dir_effect))
          for r_ in Bv.itertuples()}
    rpk = L.evaluate(P, np.asarray(LEAKY["next_bar_direction"][0](b), float), "sided", name="peek", **FAST)
    out = dict(version="1.1", metrics=res, override=ov, peek_effect_h1_r20=float(rpk["table"].at["dir_h1", "effect"]),
               seconds=time.time() - t0)
    print(f"[{sym} {tf}m lookahead] done {time.time() - t0:.0f}s: " + ", ".join(
        f"{k} {v['dir_class']}" for k, v in ov.items()), flush=True)
    return out


# ------------------------------------------------------------------------------------------------ verdict calibration
def _rare(P, seed):
    rg = np.random.default_rng(seed)
    evm = rg.random(P.n) < 1.0 / P.P
    return np.where(evm, np.where(rg.random(P.n) < 0.5, 1.0, -1.0), 0.0)


def _inject_usd(P, x, mult, build=1, long_only=False):
    """Plant an R20-constant edge on the trades of x (+-1 events) whose TRUE $ per trade at recent bar sizes is
    mult x the round-trip cost: e = mult x cost / (mean R20 of the trades in 2018-25H1 (or all, if larger) x $/pt).
    build = number of bars over which it builds linearly (1 = all at the first bar). long_only = only long trades."""
    eraB = P.year_s[P.sess_code] >= 2018
    sig = P.ok & (x != 0)
    usd_rec = max(np.mean(P.r20[sig & eraB]), np.mean(P.r20[sig])) * P.usd
    e = mult * P.cost_usd / usd_rec
    tgt = np.where(x > 0, 1.0, 0.0) if long_only else x
    Q = P
    fr = {c: min(1.0, (int(c.split("_h")[1]) if c != "dir_eod" else 10 ** 6) / build) for c in L.DIR}
    for f in sorted(set(fr.values())):
        Q = Q.injected(f * e * tgt, cols=[c for c, v in fr.items() if v == f])
    lg = sig & (x > 0) if long_only else sig
    return Q, e, float(np.mean(e * P.r20[lg & eraB]) * P.usd) if (lg & eraB).any() else np.nan


def run_classes(sym, tf, n_rep=100):
    """(v1.1) How trustworthy are the four-way classes ($ per trade vs the real $ cost)? Rare +-1 events (~1 per
    session) with a planted R20-constant edge whose TRUE $ per trade at recent bar sizes is a known multiple of the
    round-trip cost, full pipeline (session re-pairing placebo included):
      random     the same 200 random signals as run_panel          -> share CONFIDENTLY NOTHING
      zero       no edge                                           -> share CONFIDENTLY NOTHING
      cost1x     edge = cost (the boundary)                        -> wrongly NOTHING (<= 10%), wrongly TRADABLE (<= 15%)
      cost2x     edge = 2x cost                                    -> share TRADABLE (power), never NOTHING
      long8      1.5x cost on LONG trades only, building over 8 bars (reviewer case): the long side alone and pooled
      build16    1.5x cost on both sides, building over 16 bars (reviewer case: 0.75x cost at 8 bars)
    plus the textbook signals' four-way verdicts (single pre-registered metrics, truncation-tested)."""
    t0 = time.time()
    P = L.Panel(H.bars(sym, tf), sym, tf)
    rng = np.random.default_rng(1000 + tf + {"ES": 0, "NQ": 1, "YM": 2}[sym] * 7)
    fast = dict(FAST, placebo=False, repair=False)
    full = dict(FAST, placebo=False)                     # session re-pairing placebo on (part of CONFIRMED)
    rows = []

    def rec(test, r, extra=None):
        Bq = L.batch_table([r]).iloc[0]
        rows.append(dict(test=test, cls=Bq.dir_class.replace(L.UNCHECKED_TAG, ""), verdict=Bq.dir_verdict,
                         nothing=r["dir_inside_cost"], p_dir=r["p_dir"], best_dir=r["best_dir"],
                         breakeven_r20=r["breakeven_r20"], usd_per_r20_rec=r["usd_per_r20_recent"],
                         edge_usd_ci90_max_h1_8=r["edge_usd_ci90_max_h1_8"], edge_usd_B=Bq.edge_usd_B,
                         edge_usd_B_lo80=Bq.edge_usd_B_lo80, data_needed_x=r["data_needed_x"],
                         long_ok=r["long_holds_below_cost"], **(extra or {})))

    for i in range(N_NULL):
        x, kind, shape = null_signal(i, P, rng)
        rec("random", L.evaluate(P, x, kind, name=f"null{i}", **fast), dict(shape=shape))
    print(f"[{sym} {tf}m classes] nulls done {time.time() - t0:.0f}s", flush=True)
    for rep in range(n_rep):
        x = _rare(P, 9000 + rep)
        rec("zero", L.evaluate(P, x, "sided", name="zero", **fast))
        for mult, test in ((1.0, "cost1x"), (2.0, "cost2x")):
            Q, e, usd = _inject_usd(P, x, mult)
            rec(test, L.evaluate(Q, x, "sided", name=test, **full), dict(planted_r20=e, planted_usd_B=usd))
            del Q
        x = _rare(P, 9500 + rep)
        Q, e, usd = _inject_usd(P, x, 1.5, build=8, long_only=True)
        rec("long8_pooled", L.evaluate(Q, x, "sided", name="long8", **full), dict(planted_r20=e, planted_usd_B=usd))
        rec("long8_long_alone", L.evaluate(Q, np.where(x > 0, 1.0, 0.0), "sided", name="long8L", **full),
            dict(planted_r20=e, planted_usd_B=usd))
        del Q
        x = _rare(P, 9800 + rep)
        Q, e, usd = _inject_usd(P, x, 1.5, build=16)
        rec("build16", L.evaluate(Q, x, "sided", name="build16", **full), dict(planted_r20=e, planted_usd_B=usd))
        del Q
        if rep % 10 == 9:
            print(f"[{sym} {tf}m classes] rep {rep + 1}/{n_rep} {time.time() - t0:.0f}s", flush=True)
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(OUTD, f"classes_{sym}_{tf}.csv"), index=False)
    b = P.bars
    real = {}
    for k, (fn, kind) in REAL.items():
        r = L.evaluate(P, fn, kind, name=k, power=False, event_study=False)       # function -> truncation-tested
        Bq = L.batch_table([r]).iloc[0]
        real[k] = dict(dir_class=Bq.dir_class, dir_verdict=Bq.dir_verdict, best_dir=Bq.best_dir,
                       lookahead=Bq.lookahead, dir_effect=float(Bq.dir_effect), p_dir=float(Bq.p_dir),
                       breakeven_r20=float(r["breakeven_r20"]), edge_usd_rec=float(Bq.edge_usd_rec),
                       edge_usd_B=float(Bq.edge_usd_B), edge_usd_ci90_max_h1_8=float(r["edge_usd_ci90_max_h1_8"]),
                       holds_inside=r["holds_inside"], size_verdict=Bq.size_verdict, size_pct=float(Bq.size_pct),
                       best_size=Bq.best_size)
    share = lambda t, c: float((D[D.test == t].cls == c).mean())         # noqa: E731
    out = dict(sym=sym, tf=tf, version="1.1", n_rep=n_rep, cost_usd=P.cost_usd,
               null_nothing_share=float(D[D.test == "random"].nothing.mean()),
               null_nothing_by_shape=D[D.test == "random"].groupby("shape").nothing.mean().to_dict(),
               null_real=int(D[D.test == "random"].cls.str.startswith("REAL").sum()),
               zero_nothing_share=float(D[D.test == "zero"].nothing.mean()),
               class_shares={t: g.cls.value_counts(normalize=True).round(3).to_dict() for t, g in D.groupby("test")},
               false_no_rate_edge_eq_cost=share("cost1x", "CONFIDENTLY NOTHING"),
               false_tradable_rate_edge_eq_cost=share("cost1x", "REAL & TRADABLE"),
               tradable_rate_edge_2x_cost=share("cost2x", "REAL & TRADABLE"),
               nothing_rate_edge_2x_cost=share("cost2x", "CONFIDENTLY NOTHING"),
               nothing_rate_long8_long_alone=share("long8_long_alone", "CONFIDENTLY NOTHING"),
               nothing_rate_long8_pooled=share("long8_pooled", "CONFIDENTLY NOTHING"),
               nothing_rate_build16=share("build16", "CONFIDENTLY NOTHING"),
               median_breakeven_r20_rare=float(D[D.test == "zero"].breakeven_r20.median()),
               median_usd_per_r20_rare=float(D[D.test == "zero"].usd_per_r20_rec.median()),
               median_ruled_out_usd_rare=float(D[D.test == "zero"].edge_usd_ci90_max_h1_8.median()),
               planted_usd_B_cost1x=float(D[D.test == "cost1x"].planted_usd_B.median()),
               real=real, seconds=time.time() - t0)
    with open(os.path.join(OUTD, f"classes_{sym}_{tf}.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"[{sym} {tf}m classes] {time.time() - t0:.0f}s null NOTHING {out['null_nothing_share']:.2f}, zero NOTHING "
          f"{out['zero_nothing_share']:.2f}, false-no at edge=cost {out['false_no_rate_edge_eq_cost']:.2f}, "
          f"false-tradable at edge=cost {out['false_tradable_rate_edge_eq_cost']:.2f}, tradable at 2x "
          f"{out['tradable_rate_edge_2x_cost']:.2f}, NOTHING long8-alone {out['nothing_rate_long8_long_alone']:.2f} "
          f"build16 {out['nothing_rate_build16']:.2f}", flush=True)
    return out


def run_null_single(sym, tf):
    """(v1.1) False 'yes' for ONE metric tested on its own (q = p, no correction for other metrics): the same 200 random
    signals as run_panel / run_classes through the FULL pipeline (session re-pairing placebo on), each judged as a batch
    of one. Writes 'null_single' into classes_{SYM}_{TF}.json."""
    t0 = time.time()
    P = L.Panel(H.bars(sym, tf), sym, tf)
    rng = np.random.default_rng(1000 + tf + {"ES": 0, "NQ": 1, "YM": 2}[sym] * 7)
    rows = []
    for i in range(N_NULL):
        x, kind, shape = null_signal(i, P, rng)
        r = L.evaluate(P, x, kind, name=f"null{i}", **dict(FAST, placebo=False))
        Bq = L.batch_table([r]).iloc[0]
        rows.append(dict(shape=shape, p_dir=r["p_dir"], verdict=Bq.dir_verdict,
                         cls=Bq.dir_class.replace(L.UNCHECKED_TAG, ""), size_verdict=Bq.size_verdict))
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(OUTD, f"nullsingle_{sym}_{tf}.csv"), index=False)
    out = dict(n=len(D), p_dir_below_05=float((D.p_dir < 0.05).mean()), n_confirmed=int((D.verdict == "CONFIRMED").sum()),
               n_real=int(D.cls.str.startswith("REAL").sum()), n_tradable=int((D.cls == "REAL & TRADABLE").sum()),
               n_size_confirmed=int((D.size_verdict == "CONFIRMED").sum()),
               class_counts=D.cls.value_counts().to_dict(), seconds=time.time() - t0)
    f = os.path.join(OUTD, f"classes_{sym}_{tf}.json")
    k = json.load(open(f))
    k["null_single"] = out
    with open(f, "w") as fh:
        json.dump(k, fh, indent=1, default=float)
    print(f"[{sym} {tf}m null single] {time.time() - t0:.0f}s: p_dir<0.05 {out['p_dir_below_05']:.3f}, CONFIRMED "
          f"{out['n_confirmed']}/{out['n']}, REAL {out['n_real']}, TRADABLE {out['n_tradable']}", flush=True)
    return out


# ------------------------------------------------------------------------------------------------ analytic MDE cross-check
def run_mde(sym, tf, n_rep=12):
    """Analytic minimum detectable effect from the measured standard errors (cross-check of the 8-rep simulated
    curve): MDE80 = (z* + 0.84) x the smallest per-hold se, z* = 2.64 for one pre-registered metric (5% over 6 holds),
    4.49 for 'best of 100 metrics' (BY q < 0.05). se = max(session bootstrap, Newey-West) median over random signals."""
    from scipy.stats import norm
    P = L.Panel(H.bars(sym, tf), sym, tf)
    eraB = P.year_s[P.sess_code] >= 2018
    z1, z2 = norm.isf(0.05 / 6 / 2), norm.isf(BY_CUT / 6 / 2)
    out = {}
    for shape in ("rare_events", "continuous"):
        se, usd = [], []
        for rep in range(n_rep):
            rg = np.random.default_rng(7000 + rep)
            if shape == "rare_events":
                evm = rg.random(P.n) < 1.0 / P.P
                x = np.where(evm, np.where(rg.random(P.n) < 0.5, 1.0, -1.0), 0.0)
                kind, sig = "sided", P.ok & (x != 0)
            else:
                x = _ar_within(rg, P.sess_code, 0.95)
                kind = "continuous"
                q = np.quantile(x[P.ok], [0.2, 0.8])
                sig = P.ok & ((x > q[1]) | (x <= q[0]))
            r = L.evaluate(P, x, kind, name="mde", placebo=False, repair=False, **FAST)
            t = r["table"].loc[L.DIR]
            se.append(np.maximum(t.se_boot.to_numpy(), t.se_nw.to_numpy()))
            usd.append(float(np.mean(P.r20[sig & eraB]) * P.usd))   # v1.1: MEAN R20 (an R20 edge earns e x mean R20)
        se = np.median(np.array(se), axis=0)
        j = int(np.argmin(se))
        scale = 0.5 if shape == "continuous" else 1.0
        # the same conversion for the exact signals of the simulated power curves (run_panel seeds 5000 / 5100 + rep)
        upw = []
        for rep in range(N_REP):
            rg = np.random.default_rng(5000 + rep + (0 if shape == "rare_events" else 100))
            if shape == "rare_events":
                evm = rg.random(P.n) < 1.0 / P.P
                xx = np.where(evm, np.where(rg.random(P.n) < 0.5, 1.0, -1.0), 0.0)
                sg = P.ok & (xx != 0)
            else:
                xx = _ar_within(rg, P.sess_code, 0.95)
                qq = np.quantile(xx[P.ok], [0.2, 0.8])
                sg = P.ok & ((xx > qq[1]) | (xx <= qq[0]))
            upw.append(float(np.mean(P.r20[sg & eraB]) * P.usd))
        u = float(np.median(usd))
        out[shape] = dict(se_by_hold=dict(zip(L.DIR, se.tolist())), best_hold=L.DIR[j],
                          mde80_single_r20=float((z1 + 0.8416) * se[j]), mde80_strict_r20=float((z2 + 0.8416) * se[j]),
                          usd_per_r20_B=u, usd_per_r20_B_power=float(np.mean(upw)),
                          breakeven_trade_r20=P.cost_usd / u, cost_usd=P.cost_usd,
                          breakeven_effect_r20=P.cost_usd / u / scale)
        for k in ("single", "strict"):
            out[shape][f"mde80_{k}_usd_per_trade"] = scale * out[shape][f"mde80_{k}_r20"] * out[shape]["usd_per_r20_B"]
    with open(os.path.join(OUTD, f"mde_{sym}_{tf}.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"[{sym} {tf}m mde] " + json.dumps({k: (round(v["mde80_single_r20"], 4), round(v["mde80_strict_r20"], 4),
                                                   v["best_hold"]) for k, v in out.items()}), flush=True)
    return out


# ------------------------------------------------------------------------------------------------ pass / fail + report
def judge(s, k=None):
    """Pass rules for one panel (all must hold). k = classes_{SYM}_{TF}.json (v1.1 four-way class calibration)."""
    n = s["null"]
    sd = math.sqrt(0.05 * 0.95 / n["n"])
    ng = s["neg"]
    sdn = math.sqrt(0.05 * 0.95 / ng["n"])
    pos = {p["control"]: p for p in s["pos"]}
    pw = s["power"]
    la = s["lookahead"]
    if la.get("version") == "1.1":
        lm, ov = la["metrics"], la["override"]
        la_ok = (all(v["flagged_seeds"] == v["seeds"] for v in lm.values() if v["group"] == "leaky")
                 and all(v["flagged_seeds"] == 0 for v in lm.values() if v["group"] != "leaky")
                 and all(ov[m]["dir_class"] == "INVALID (LOOK-AHEAD)" for m, v in lm.items() if v["group"] == "leaky")
                 and all(ov[m]["dir_verdict"] != "INVALID" for m, v in lm.items() if v["group"] == "honest"))
    else:
        la_ok = False                                   # v1 3-cut test: superseded, re-run 'lookahead'
    checks = {
        "null: decision p < 0.05 at most nominal (<= 5% + 2 sd)": n["fpr_p_dir"] <= 0.05 + 2 * sd,
        "null: each single-hold p method within 5% +- 2.6 sd": all(
            0.05 - 2.6 * sd <= v <= 0.05 + 2.6 * sd for k_, v in n["fpr_by_col"].items()
            if k_.split(":")[1] in ("p_boot", "p_nw", "p_repair") and k_.startswith("dir")),
        "null: honest t spread at 16 bars 0.8-1.25": 0.8 <= n["sd_t_h16_honest"] <= 1.25,
        "null: no random signal CONFIRMED or called REAL in the 200-metric batch": n["n_dir_confirmed"] == 0,
        "null: 20-metric batches with any q < 0.10 at most 10%": n["fwer_batches_any_q10"] <= 0.10,
        "negative: shifted / other-market direction p < 0.05 at most nominal + 2 sd": ng["fpr_p_dir"] <= 0.05 + 2 * sdn,
        "negative: no direction CONFIRMED": ng["n_dir_confirmed"] == 0,
        "look-ahead (v1.1): all 7 leaky metrics (4 of them rare yes/no candle-style leaks) flagged at every seed, 2 honest "
        "+ 7 textbook metrics pass at every seed, every leaky metric INVALID in a batch": la_ok,
        "positive: range_ratio (last-bar range), time_of_day, news_830 detected": all(
            pos[k_]["detected"] for k_ in ("range_ratio", "time_of_day", "news_830")),
        "power: injected effect recovered (slope 0.85-1.15)": all(0.85 <= v["recovered_slope"] <= 1.15
                                                                  for v in pw.values()),
        "power: 80% detection reached within the tested range": all(np.isfinite(v["mde80_single_r20"])
                                                                    for v in pw.values()),
    }
    if k is not None and k.get("version") == "1.1":
        checks.update({
            "classes ($, v1.1): edge = cost wrongly called CONFIDENTLY NOTHING <= 10%": k["false_no_rate_edge_eq_cost"] <= 0.10,
            "classes ($, v1.1): edge = cost wrongly called REAL & TRADABLE <= 15%": k["false_tradable_rate_edge_eq_cost"] <= 0.15,
            "classes ($, v1.1): edge = 2x cost called CONFIDENTLY NOTHING <= 5%": k["nothing_rate_edge_2x_cost"] <= 0.05,
            "classes ($, v1.1): reviewer cases (1.5x cost on long trades over 8 bars, tested alone; 1.5x cost building "
            "over 16 bars) called CONFIDENTLY NOTHING <= 10%": max(k["nothing_rate_long8_long_alone"],
                                                                    k["nothing_rate_build16"]) <= 0.10})
    else:
        checks["classes ($, v1.1): calibration run"] = False
    ns_ = (k or {}).get("null_single")
    checks["null, ONE metric at a time (q = p, full pipeline incl. placebo): CONFIRMED at most 5% (the nominal level)"] = (
        ns_ is not None and ns_["n_confirmed"] <= 0.05 * ns_["n"])
    info = {"positive: reversal (direction, tiny) detected": pos["reversal"]["detected"],
            "positive: range4_ratio (extra, weaker by design) detected": pos["range4_ratio"]["detected"],
            "negative: shifted / other-market SIZE p < 0.05 at most nominal + 2 sd": ng["fpr_p_size"] <= 0.05 + 2 * sdn}
    return checks, info


def _usd(x):
    return "n/a" if x is None or not np.isfinite(x) else f"${x:.2f}"


def summary(log=False):
    files = sorted(f for f in os.listdir(OUTD) if f.startswith("calib_") and f.endswith(".json"))
    S = [json.load(open(os.path.join(OUTD, f))) for f in files]
    status, L_ = {}, []
    L_ += ["# Signal lab v1.1: real-data self-test", "",
           "Data: ES / NQ / YM continuous futures, 15-min and 60-min bars, cut before the locked holdout "
           "(2025-06-30 18:00 ET). YM starts 2018. Units: R20 = 'average bar' (mean high-low of the last 20 bars). "
           "$ = per ONE micro (MES $5/pt, MNQ $2/pt, MYM $0.5/pt). Round-trip cost = $1 + 1 tick each way "
           "(MES $3.50, MNQ $2.00, MYM $2.00).", "",
           "v1.1 (after an adversarial review): (1) the look-ahead test now cuts the data at 40 of the metric's own "
           "signal bars plus 60 random bars (was 3 random bars) and a failed test makes every verdict INVALID; "
           "(2) tradability is judged in $ per trade against the real $ cost. An edge of e R20 on every trade earns "
           "e x MEAN R20 x $/pt, so the break-even edge is cost / mean R20. The old bar (mean of cost / R20) was "
           "1.3-1.7x too high. $ per R20 below uses the MEAN R20 of the signal's trades in 2018-25 (v1 used the "
           "median of all bars).", ""]
    for s in S:
        kf = os.path.join(OUTD, f"classes_{s['sym']}_{s['tf']}.json")
        k = json.load(open(kf)) if os.path.exists(kf) else None
        mf = os.path.join(OUTD, f"mde_{s['sym']}_{s['tf']}.json")
        m = json.load(open(mf)) if os.path.exists(mf) else None
        ch, info = judge(s, k)
        key = f"{s['sym']} {s['tf']}"
        n, ng, pw = s["null"], s["neg"], s["power"]
        status[key] = dict(passed=all(ch.values()), date=s["date"], version="1.1", fpr_dir=n["fpr_p_dir"],
                           mde80_rare=pw["rare_events"]["mde80_single_r20"],
                           mde80_rare_strict=pw["rare_events"]["mde80_strict_r20"],
                           mde80_cont=pw["continuous"]["mde80_single_r20"], failed=[k_ for k_, v in ch.items() if not v])
        mk = f"{L.MICRO[s['sym']]} {s['tf']}-min"
        L_ += [f"## {mk}: {'PASSED' if all(ch.values()) else 'FAILED'} ({s['n_sessions']} sessions, {s['n_bars']} bars)", ""]
        for k_, v in ch.items():
            L_.append(f"- [{'x' if v else ' '}] {k_}")
        for k_, v in info.items():
            L_.append(f"- (info) {k_}: {v}")
        L_ += ["", f"**False positives (200 random signals):** decision p < 0.05 for {n['fpr_p_dir']:.1%} "
                   f"(direction) and {n['fpr_p_size']:.1%} (size); 20-metric batches with any q < 0.10: "
                   f"{n['fwer_batches_any_q10']:.0%} of {n['n_batches']}; CONFIRMED direction: {n['n_dir_confirmed']}; "
                   f"CONFIRMED size: {n['n_size_confirmed']}. Honest t spread at 16 bars {n['sd_t_h16_honest']:.2f} "
                   f"(naive bar-by-bar {n['sd_t_h16_naive']:.2f}).",
               f"**Real signals moved to the wrong days ({ng['n']}):** direction p < 0.05 {ng['fpr_p_dir']:.1%} "
               f"(by type {ng['fpr_p_dir_by_type']}), size p < 0.05 {ng['fpr_p_size']:.1%} (by signal "
               f"{ng['size_fpr_by_signal']}); CONFIRMED direction {ng['n_dir_confirmed']}, size {ng['n_size_confirmed']}.",
               ""]
        la = s["lookahead"]
        if la.get("version") == "1.1":
            L_ += [f"**Look-ahead (v1.1 test, 100 cuts per check; a next-bar peek fakes a "
                   f"{la['peek_effect_h1_r20']:+.2f} R20 'edge'):**", "",
                   "| metric | kind | share of bars with a signal | flagged (seeds) | old 3-cut test missed it | "
                   "batch verdict |", "|---|---|---|---|---|---|"]
            for nm, v in la["metrics"].items():
                o = la["override"].get(nm, {})
                L_.append(f"| {nm} ({v['group']}) | {v['kind']} | {v['event_share']:.1%} | {v['flagged_seeds']}/{v['seeds']} | "
                          f"{(str(v['old3_missed_of_10']) + '/10') if 'old3_missed_of_10' in v else ''} | "
                          f"{o.get('dir_class', '')}"
                          + (f" (raw p {o['raw_p_dir']:.2g}, raw effect {o['raw_effect']:+.2f} R20)" if o else "") + " |")
            status[key]["lookahead_leaks_flagged"] = sum(v["flagged_seeds"] == v["seeds"] for v in la["metrics"].values()
                                                         if v["group"] == "leaky")
            status[key]["lookahead_false_alarms"] = sum(v["flagged_seeds"] > 0 for v in la["metrics"].values()
                                                        if v["group"] != "leaky")
            L_.append("")
        L_ += ["**Positive controls:**", "", "| control | target | effect R20 | 95% CI | % vs avg | p | years same sign | "
               "detected |", "|---|---|---|---|---|---|---|---|"]
        for p in s["pos"]:
            L_.append(f"| {p['control']} | {p['col']} | {p['effect']:+.3f} | {p['ci_lo']:+.3f} .. {p['ci_hi']:+.3f} | "
                      f"{p['pct_vs_avg']:+.0f}% | {p['p']:.2g} | {p['years_same']}/{p['years_n']} | {p['detected']} |")
        L_ += ["", f"U-shape, median bar range in points (2nd half of sessions) by bar start: {s['ushape_pts']}. "
                   f"Bar containing 8:30 ET: median {s['news_bar_pts']['news_median']:.2f} pts on NFP/CPI days "
                   f"({s['news_bar_pts']['n_news']}) vs {s['news_bar_pts']['other_median']:.2f} on other days.", "",
               "**Power (injected direction effect, full pipeline):**", "",
               "| signal | delta R20 | detected (single metric, p<0.05) | detected (as 1 of 100 metrics, CONFIRMED rule) |",
               "|---|---|---|---|"]
        for shape, v in pw.items():
            for c in v["curve"]:
                L_.append(f"| {shape} | {c['delta']:.2f} | {c['single']:.0%} | {c['strict']:.0%} |")
        for shape, v in pw.items():
            sc = 0.5 if shape == "continuous" else 1.0
            u = m[shape]["usd_per_r20_B_power"] if m else np.nan          # v1.1: mean R20 of these trades, 2018-25H1
            be = v["cost_usd"] / u if np.isfinite(u) else np.nan
            L_.append(f"\n- {shape} ({v['n_sig']:.0f} signal bars): MDE80 single {v['mde80_single_r20']:.3f} R20 "
                      f"({_usd(sc * v['mde80_single_r20'] * u)}/micro/trade), as 1 of 100 "
                      f"{v['mde80_strict_r20']:.3f} R20 ({_usd(sc * v['mde80_strict_r20'] * u)}); break-even per trade "
                      f"{be:.3f} R20 = ${v['cost_usd']:.2f} at the mean 2018-25 bar of these trades "
                      f"({_usd(u)} per R20)" + (f" (a top-vs-bottom spread of {2 * be:.3f} R20)" if sc < 1 else "")
                      + f"; injected effect recovered with slope {v['recovered_slope']:.2f}.")
            status[key][f"usd_per_r20_{'rare' if sc == 1 else 'cont'}"] = u
            status[key][f"breakeven_trade_r20_{'rare' if sc == 1 else 'cont'}"] = be
            status[key][f"mde80_{'rare' if sc == 1 else 'cont'}_usd"] = sc * v["mde80_single_r20"] * u
            status[key][f"mde80_{'rare' if sc == 1 else 'cont'}_strict_usd"] = sc * v["mde80_strict_r20"] * u
        if m:
            for shape, v in m.items():
                L_.append(f"- analytic cross-check, {shape}: smallest se at {v['best_hold']}; MDE80 single "
                          f"{v['mde80_single_r20']:.3f} R20 ({_usd(v['mde80_single_usd_per_trade'])}/micro/trade), as 1 "
                          f"of 100 {v['mde80_strict_r20']:.3f} R20 ({_usd(v['mde80_strict_usd_per_trade'])}).")
            status[key].update(mde80_rare_analytic=m["rare_events"]["mde80_single_r20"],
                               mde80_rare_strict_analytic=m["rare_events"]["mde80_strict_r20"],
                               mde80_cont_analytic=m["continuous"]["mde80_single_r20"],
                               mde80_rare_analytic_usd=m["rare_events"]["mde80_single_usd_per_trade"],
                               mde80_rare_strict_analytic_usd=m["rare_events"]["mde80_strict_usd_per_trade"],
                               mde80_cont_analytic_usd=m["continuous"]["mde80_single_usd_per_trade"],
                               mde80_cont_strict_analytic_usd=m["continuous"]["mde80_strict_usd_per_trade"])
        if k is not None and k.get("version") == "1.1":
            status[key].update(null_nothing_share=k["null_nothing_share"], zero_nothing_share=k["zero_nothing_share"],
                               false_no_rate=k["false_no_rate_edge_eq_cost"],
                               false_tradable_rate=k["false_tradable_rate_edge_eq_cost"],
                               tradable_rate_2x=k["tradable_rate_edge_2x_cost"],
                               ruled_out_edge_usd=k["median_ruled_out_usd_rare"],
                               ruled_out_edge_r20=k["median_ruled_out_usd_rare"] / k["median_usd_per_r20_rare"],
                               breakeven_r20_rare=k["median_breakeven_r20_rare"])
            ns_ = k.get("null_single")
            if ns_:
                status[key].update(single_null_confirmed=ns_["n_confirmed"], single_null_real=ns_["n_real"],
                                   single_null_tradable=ns_["n_tradable"], single_null_n=ns_["n"])
                L_ += ["", f"**One metric tested on its own (q = p, no correction for other metrics, full pipeline incl. "
                           f"placebo), 200 random signals:** p < 0.05 for {ns_['p_dir_below_05']:.1%}; CONFIRMED "
                           f"{ns_['n_confirmed']}, called REAL {ns_['n_real']} (REAL & TRADABLE {ns_['n_tradable']}); "
                           f"size CONFIRMED {ns_['n_size_confirmed']}. (Same signals judged without the placebo gate: "
                           f"called REAL {k['null_real']}.)"]
            cs = k["class_shares"]
            L_ += ["", f"**How trustworthy are the four-way classes? ({k['n_rep']} runs per case, rare +-1 events about "
                       f"once per session, edge planted so that its TRUE $ per trade at 2018-25 bar sizes is a known "
                       f"multiple of the ${k['cost_usd']:.2f} round trip; full pipeline incl. placebo for the planted-edge cases; the "
                       f"two no-edge rows skip the placebo, which a 'no' does not use, so their few REAL calls are "
                       f"single metrics judged without the placebo gate)**", "",
                   "| case | REAL & TRADABLE | REAL BUT TOO SMALL | CONFIDENTLY NOTHING | INCONCLUSIVE |",
                   "|---|---|---|---|---|"]
            names = {"random": "200 random signals (no edge)", "zero": "no edge (rare events)",
                     "cost1x": "edge = cost (the boundary)", "cost2x": "edge = 2x cost",
                     "long8_long_alone": "1.5x cost on long trades, builds over 8 bars: long side tested alone",
                     "long8_pooled": "same, both sides pooled (true pooled edge 0.75x cost)",
                     "build16": "1.5x cost both sides, builds over 16 bars (0.75x cost at 8 bars)"}
            for t_, nm in names.items():
                c = cs.get(t_, {})
                L_.append(f"| {nm} | " + " | ".join(f"{c.get(x, 0):.0%}" for x in
                                                   ("REAL & TRADABLE", "REAL BUT TOO SMALL", "CONFIDENTLY NOTHING",
                                                    "INCONCLUSIVE")) + " |")
            L_ += ["", f"For a signal firing about once per session with no edge, the lab can rule out per-trade edges "
                       f"bigger than about {_usd(k['median_ruled_out_usd_rare'])} per micro (median 90% range at holds of "
                       f"1-8 bars, at recent bar sizes); break-even is {k['median_breakeven_r20_rare']:.3f} R20 = "
                       f"${k['cost_usd']:.2f}.", "",
                   "**Textbook signals, four-way verdict as SINGLE pre-registered metrics (q = p, no correction for "
                   "the 7 looked at; in the 7-metric batch of the main run none is CONFIRMED, see calib_*_real.csv):** "
                   + "; ".join(
                       f"{n_}: {v['dir_class']} (best dir {v['dir_effect']:+.3f} R20 at {v['best_dir']}, p={v['p_dir']:.2g}, "
                       f"per-trade edge now {_usd(v['edge_usd_rec'])}, 90% range up to {_usd(v['edge_usd_ci90_max_h1_8'])} "
                       f"at 1-8 bars, look-ahead {v['lookahead']}), size {v['size_verdict']} {v['size_pct']:+.0f}% at "
                       f"{v['best_size']}" for n_, v in k["real"].items()), ""]
        else:
            L_ += ["", "**Four-way classes: v1.1 calibration not run for this panel.**", ""]
    with open(os.path.join(OUTD, "self_test_status.json"), "w") as f:
        json.dump(status, f, indent=1, default=float)
    with open(os.path.join(OUTD, "calibration_report.md"), "w") as f:
        f.write("\n".join(L_) + "\n")
    print("\n".join(L_))
    if log:
        for s in S:
            Br = pd.read_csv(os.path.join(OUTD, f"calib_{s['sym']}_{s['tf']}_real.csv"))
            L.log_trials(Br, "calib")
    return status


if __name__ == "__main__":
    if sys.argv[1] == "run":
        syms = sys.argv[2].split(",")
        tfs = [int(x) for x in sys.argv[3].split(",")]
        for sym in syms:
            for tf in tfs:
                run_panel(sym, tf)
    elif sys.argv[1] == "mde":
        for sym in sys.argv[2].split(","):
            for tf in [int(x) for x in sys.argv[3].split(",")]:
                run_mde(sym, tf)
    elif sys.argv[1] == "lookahead":
        for sym in sys.argv[2].split(","):
            for tf in [int(x) for x in sys.argv[3].split(",")]:
                run_lookahead(sym, tf)
    elif sys.argv[1] == "nullsingle":
        for sym in sys.argv[2].split(","):
            for tf in [int(x) for x in sys.argv[3].split(",")]:
                run_null_single(sym, tf)
    elif sys.argv[1] == "classes":
        nr = int(sys.argv[4]) if len(sys.argv) > 4 else 100      # v1.1 final run: 100 runs per case
        for sym in sys.argv[2].split(","):
            for tf in [int(x) for x in sys.argv[3].split(",")]:
                run_classes(sym, tf, n_rep=nr)
    else:
        summary(log="log" in sys.argv)
