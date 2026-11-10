"""
A STRONGER "after a decline / after a rise" context for the textbook reversal candle patterns (NEXT_STEPS item 20).

Today (signals.patterns) the reversal patterns only ask that the close of the pattern's reference bar is below
(bullish) / above (bearish) EMA 10 - and piercing / dark cloud / dragonfly / gravestone doji ask nothing at all.

prior_move(b, ctx, d, X, N, ...) -> bool per bar: was there a REAL move into the bar in direction -d?
For d = +1 (bullish reversal, we need a DECLINE into the pattern), ALL of:
  (a) the close of the reference bar r = t - lag is at least X average bars (X * R20_t) below the highest high of the
      N bars ending at r (bars r-N+1 .. r);
  (b) EMA 10 is falling over the last 3 bars: EMA10[r] < EMA10[r-3];
  (c) the pattern's low (lowest low of its `span` bars t-span+1 .. t) is within `near` (0.5) R20_t of the lowest low of
      the last `low_n` (10) bars t-9 .. t (the pattern sits at / near a fresh low).
d = -1 mirrors it (close >= X R20 above the lowest low of the N bars, EMA 10 rising, pattern high within 0.5 R20 of
the highest high of the last 10 bars).
R20_t = features.r20 (mean H-L of the 20 bars before t, same contract run). Every window must lie in one contract run
(else False). Everything uses bars <= t only (known at the signal bar's close).

Reference bar per pattern = the bar the existing loose EMA-10 rule looks at (so strong context is a tightening of the
same idea): one-bar patterns -> the bar before (lag 1); two-bar patterns (engulfing, harami, piercing, dark cloud,
tweezer) -> their first bar (lag 1); three-bar patterns (morning/evening star, three inside) -> their first bar (lag 2).

Study (python3 context_rule.py [NQ]): on out/entries_<SYM>_15.parquet
  * event-level flags: an event (t, d) is a REVERSAL event if one of the patterns below fired in its direction d;
    strong_<X> = at least one of those patterns has prior_move(d) true; 'loose only' = reversal and not strong.
  * unfiltered $/trade (pnl_usd_1.5, 1 micro, after costs), hit rate (y_1.5), count by year for each group;
  * v1 logit walk-forwards (same features / folds / threshold rule as run_pipeline, logged as module
    'entry-context'): (i) all events + feature strong_ctx (signed: +d when the event's own direction has strong
    context, so +1 after orienting by d), (ii) only the strong-context events, (iii) control: all reversal events.
Writes out/context_rule_<SYM>.csv and out/context_rule_<SYM>.md.
"""
import gc
import json
import sys
import time
import warnings

import numpy as np
import pandas as pd

import features as fe

# name -> (span = number of bars in the pattern, lag = reference bar of the loose EMA-10 rule, bars before t)
REVERSAL = {
    "hammer": (1, 1), "hanging_man": (1, 1), "inverted_hammer": (1, 1), "shooting_star": (1, 1),
    "dragonfly_doji": (1, 1), "gravestone_doji": (1, 1),
    "engulfing": (2, 1), "harami": (2, 1), "piercing": (2, 1), "dark_cloud": (2, 1), "tweezer": (2, 1),
    "morning_evening_star": (3, 2), "three_inside": (3, 2),
}
X_GRID = (1.5, 3.0)
N_GRID = (10,)
EMA_BARS = 3
NEAR = 0.5
LOW_N = 10


def _roll(a, w, how):
    s = pd.Series(a).rolling(w, min_periods=w)
    return (s.max() if how == "max" else s.min()).to_numpy()


def prior_move(b, ctx, d, X=1.5, N=10, lag=1, span=1, ema_bars=EMA_BARS, near=NEAR, low_n=LOW_N, R=None, tick=0.25):
    """Bool array (len(b)): a real move in direction -d into bar t (module docstring). b: signals.bars frame (H, L, C,
    run); ctx: signals.context (ema10); d: +1 (bullish reversal -> decline needed) or -1; R: R20 per bar (default
    features.r20(b, tick))."""
    if d not in (1, -1):
        raise ValueError("d must be +1 or -1")
    H, L, C = (b[c].to_numpy(np.float64) for c in ("H", "L", "C"))
    run = b["run"].to_numpy()
    n = len(b)
    R = fe.r20(b, tick) if R is None else np.asarray(R, np.float64)
    e = ctx["ema10"].to_numpy(np.float64)
    # (a) move into the reference bar r = t - lag, against the N bars ending at r
    ext = _roll(H, N, "max") if d == 1 else _roll(L, N, "min")       # at bar r
    move = d * (fe._lag(ext, lag) - fe._lag(C, lag))                  # >0 = close below the high (d=+1)
    a = (move >= X * R) & fe._run_ok(run, lag + N - 1)
    # (b) EMA 10 moving in direction -d over the last ema_bars bars, ending at r
    slope = fe._lag(e, lag) - fe._lag(e, lag + ema_bars)
    bb = (-d * slope > 0) & fe._run_ok(run, lag + ema_bars)
    # (c) pattern extreme near the fresh extreme of the last low_n bars (ending at t)
    if d == 1:
        pat = _roll(L, span, "min"); fresh = _roll(L, low_n, "min")
        gap = pat - fresh
    else:
        pat = _roll(H, span, "max"); fresh = _roll(H, low_n, "max")
        gap = fresh - pat
    c = (gap <= near * R) & fe._run_ok(run, max(low_n, span) - 1)
    with np.errstate(invalid="ignore"):
        out = a & bb & c & np.isfinite(R) & np.isfinite(move) & np.isfinite(slope) & np.isfinite(gap)
    return np.asarray(out, bool)


def strong_flags(b, ctx, E, X, N=10, R=None, tick=0.25):
    """Per event row of E (needs i, d and pat_<name> columns): (is_reversal, strong) bool arrays."""
    i = E["i"].to_numpy(np.int64)
    d = E["d"].to_numpy(np.int64)
    rev = np.zeros(len(E), bool); strong = np.zeros(len(E), bool)
    cache = {}
    for name, (span, lag) in REVERSAL.items():
        fired = E[f"pat_{name}"].to_numpy() == d                     # pattern fired in the event's direction
        if not fired.any():
            continue
        rev |= fired
        for dd in (1, -1):
            k = (dd, span, lag)
            if k not in cache:
                cache[k] = prior_move(b, ctx, dd, X=X, N=N, lag=lag, span=span, R=R, tick=tick)
            m = fired & (d == dd)
            strong[m] |= cache[k][i[m]]
    return rev, strong


# ============================================================================================ study
def wait_ram(need_mb=7000, every=60):
    while True:
        with open("/proc/meminfo") as f:
            av = next(int(l.split()[1]) // 1024 for l in f if l.startswith("MemAvailable"))
        if av >= need_mb:
            print(f"  RAM available {av} MB", flush=True)
            return
        print(f"  RAM available {av} MB < {need_mb}; waiting", flush=True)
        time.sleep(every)


def _grp(name, g):
    return dict(group=name, n=len(g), usd_per_trade=g["pnl_usd_1.5"].mean() if len(g) else np.nan,
                hit_rate=g["y_1.5"].mean() if len(g) else np.nan,
                usd_total=g["pnl_usd_1.5"].sum())


def main(sym="NQ"):
    import run_pipeline as rp
    import signals as sg
    import walkforward as wf
    warnings.filterwarnings("ignore")
    tick = sg.SPEC[sym]["tick"]
    feats = rp.feature_list("entry", sym)
    wait_ram()
    E = rp.load("entry", sym)
    wait_ram()
    b = sg.bars(sym, 15)
    ctx = sg.context(b, tick=tick)
    R = fe.r20(b, tick)
    ok = np.isfinite(E["R20"].to_numpy())
    assert np.allclose(E["R20"].to_numpy()[ok], R[E["i"].to_numpy()[ok]]), "bar index i does not match R20"
    assert (b.index[E["i"].to_numpy()] == pd.DatetimeIndex(E["t"])).all(), "bar index i does not match t"
    for X in X_GRID:
        for N in N_GRID:
            rev, st = strong_flags(b, ctx, E, X, N, R=R, tick=tick)
            E[f"strong_{X:g}_{N}"] = st
        E["reversal"] = rev
    del b, ctx, R; gc.collect()

    yr = pd.DatetimeIndex(E["t"]).year
    oos = E["t"] >= pd.Timestamp("2013-01-01")
    rows = []
    # ---- unfiltered
    for period, msk in (("2010-2025H1", np.ones(len(E), bool)), ("2013-2025H1", oos.to_numpy())):
        S = E.loc[msk]
        groups = [("all events", S), ("non-reversal events", S[~S.reversal]), ("reversal events (loose)", S[S.reversal])]
        for X in X_GRID:
            c = f"strong_{X:g}_10"
            groups += [(f"reversal strong X={X:g}", S[S[c]]), (f"reversal loose only X={X:g}", S[S.reversal & ~S[c]])]
        for name, g in groups:
            rows.append(dict(section="unfiltered", period=period, **_grp(name, g)))
        if period == "2013-2025H1":
            for y, gy in S.groupby(pd.DatetimeIndex(S["t"]).year):
                for name, sel in [("reversal events (loose)", gy.reversal)] + \
                        [(f"reversal strong X={X:g}", gy[f"strong_{X:g}_10"]) for X in X_GRID] + \
                        [(f"reversal loose only X={X:g}", gy.reversal & ~gy[f"strong_{X:g}_10"]) for X in X_GRID]:
                    rows.append(dict(section="unfiltered_by_year", period=str(y), **_grp(name, gy[sel])))
            for p in REVERSAL:
                fired = S[f"pat_{p}"].to_numpy() == S["d"].to_numpy()
                for X in X_GRID:
                    c = S[f"strong_{X:g}_10"].to_numpy()
                    rows.append(dict(section="by_pattern", period=period,
                                     **_grp(f"{p} strong X={X:g}", S[fired & c])))
                    rows.append(dict(section="by_pattern", period=period,
                                     **_grp(f"{p} loose only X={X:g}", S[fired & ~c])))
    pd.DataFrame(rows).to_csv(f"out/context_rule_{sym}.csv", index=False)
    print(pd.DataFrame([r for r in rows if r["section"] == "unfiltered"]).round(3).to_string(index=False), flush=True)

    # ---- walk-forwards
    signed = list(fe.SIGNED) + ["strong_ctx"]
    runs = []
    for X in X_GRID:
        runs.append((f"all events + strong_ctx X={X:g}", None, X))
    for X in X_GRID:
        runs.append((f"strong-context events only X={X:g}", f"strong_{X:g}_10", None))
    runs.append(("reversal events only (loose, control)", "reversal", None))
    for label, subset, Xf in runs:
        if subset is None:
            data = E
            data["strong_ctx"] = (E[f"strong_{Xf:g}_10"].astype(np.float32) * E["d"]).astype(np.float32)
            fl = feats + ["strong_ctx"]
        else:
            data = E.loc[E[subset]].copy()
            fl = feats
        wait_ram()
        t0 = time.time()
        res = wf.walk_forward(data, fl, model="logit", signed=signed, verbose=False, **rp.wf_args("entry"), **rp.WF_KW)
        rt = time.time() - t0
        s = res.pooled
        coef = np.nan
        if subset is None and len(res.coefs):
            cc = res.coefs[res.coefs.feature == "strong_ctx"]
            coef = cc.coef_raw.median() if len(cc) else np.nan
        rp.log_trial(module="entry-context", scope=sym, model="logit", target="y_1.5", n_folds=int(s.n_folds),
                     oos_rows=int(s.all_n), oos_auc=round(float(s.auc), 4), oos_kept=int(s.n_kept),
                     oos_keep_share=round(float(s.keep_share), 4), oos_usd_total=round(float(s.total_usd), 2),
                     oos_usd_per_trade=round(float(s.pnl_per_trade), 3),
                     oos_usd_per_year=round(float(s.usd_per_year), 1),
                     baseline_usd_per_trade=round(float(s.all_pnl_per_trade), 3), runtime_s=round(rt),
                     parameters=json.dumps(dict(run=label, X=Xf, N=10, ema_bars=EMA_BARS, near=NEAR, low_n=LOW_N,
                                                subset=subset, n_features=len(fl), lags={k: v for k, v in
                                                                                         REVERSAL.items()})),
                     note="strong prior-move context for reversal patterns; baseline = all events of this run")
        rows.append(dict(section="wf_pooled", group=label, period="2013-2025H1", n=int(s.all_n),
                         auc=s.auc, n_kept=int(s.n_kept), keep_share=s.keep_share, usd_per_trade=s.pnl_per_trade,
                         hit_rate=s.hit_rate, usd_total=s.total_usd, usd_per_year=s.usd_per_year,
                         all_usd_per_trade=s.all_pnl_per_trade, random_usd_per_trade=s.random_pnl_per_trade,
                         random_p5=s.random_p5, random_p95=s.random_p95, strong_ctx_coef_raw_median=coef,
                         runtime_s=rt))
        for _, f in res.folds.iterrows():
            rows.append(dict(section="wf_by_year", group=label, period=str(f["fold"]), n=int(f["n_test"]),
                             auc=f["auc"], n_kept=f["n_kept"], keep_share=f["keep_share"],
                             usd_per_trade=f["pnl_per_trade"], hit_rate=f["hit_rate"], usd_total=f["total_usd"],
                             all_usd_per_trade=f["all_pnl_per_trade"], random_usd_per_trade=f["random_pnl_per_trade"]))
        print(f"{label}: AUC {s.auc:.4f} kept {int(s.n_kept)} ({s.keep_share:.3f}) $/tr {s.pnl_per_trade:.3f} "
              f"all {s.all_pnl_per_trade:.3f} random {s.random_pnl_per_trade:.3f} coef {coef} ({rt:.0f}s)", flush=True)
        pd.DataFrame(rows).to_csv(f"out/context_rule_{sym}.csv", index=False)
        del res
        if subset is not None:
            del data
        gc.collect()
    v1 = pd.read_csv("out/entry_results.csv")
    v1 = v1[(v1.scope == sym) & (v1.model == "logit")].iloc[0]
    rows.append(dict(section="wf_pooled", group="v1 logit (out/entry_results.csv)", period="2013-2025H1",
                     n=int(v1.all_n), auc=v1.auc, n_kept=int(v1.n_kept), keep_share=v1.keep_share,
                     usd_per_trade=v1.pnl_per_trade, hit_rate=v1.hit_rate, usd_total=v1.total_usd,
                     usd_per_year=v1.usd_per_year, all_usd_per_trade=v1.all_pnl_per_trade,
                     random_usd_per_trade=v1.random_pnl_per_trade, random_p5=v1.random_p5,
                     random_p95=v1.random_p95))
    pd.DataFrame(rows).to_csv(f"out/context_rule_{sym}.csv", index=False)
    print("written", f"out/context_rule_{sym}.csv", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "NQ")
