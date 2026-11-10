"""Judge's own checks of skip rules R1/R2. Reads project files only; writes nothing to the project."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.getcwd())
import calendar_days as cd

def wt(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return (a.mean()-b.mean())/np.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))

T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
ctx = pd.read_pickle("data/market_context.pkl")
T = T.join(ctx[["spx_ret_1d_prev", "vix_prev", "spx_rv20_prev", "vix_tercile"]], on="date")
fomc = set(pd.to_datetime(list(cd.fomc_days())))
T["r1"] = T.spx_ret_1d_prev <= -2
T["r2"] = T.date.isin(fomc)
T["year"] = T.date.dt.year
print("ctx last rows:\n", ctx[["spx_ret_1d_prev", "vix_prev"]].tail(3))
print("next FOMC dates >= 2026-11-01:", sorted(d.date() for d in fomc if d >= pd.Timestamp("2026-11-01")))

cases = [("R1", "overnight_break", "r1"), ("R1", "opening_range", "r1"), ("R2", "opening_range", "r2")]
for rule, m, c in cases:
    d = T[T.model == m].copy()
    a, b = d[d[c]], d[~d[c]]
    print(f"\n===== {rule} {m}: n={len(a)} ${a.usd.mean():+.2f} vs {b.usd.mean():+.2f} t {wt(a.usd,b.usd):+.2f}; "
          f"bp {a.bp.mean():+.1f} vs {b.bp.mean():+.1f} t {wt(a.bp,b.bp):+.2f}; R {a.R.mean():+.3f} vs {b.R.mean():+.3f} t {wt(a.R,b.R):+.2f}")

    # 1. Vol confound: within VIX terciles and regression of bp on cond + vix
    if rule == "R1":
        for tcol in ["vix_tercile"]:
            for k, g in d.groupby(tcol):
                ga, gb = g[g[c]], g[~g[c]]
                if len(ga) >= 5:
                    print(f"  VIX tercile {k}: cond n={len(ga)} bp {ga.bp.mean():+.1f} R {ga.R.mean():+.3f} | other n={len(gb)} bp {gb.bp.mean():+.1f} R {gb.R.mean():+.3f} | t(bp) {wt(ga.bp,gb.bp):+.2f} t(R) {wt(ga.R,gb.R):+.2f}")
        hv = d[d.vix_prev >= 25]
        ga, gb = hv[hv[c]], hv[~hv[c]]
        print(f"  VIX_prev>=25: cond n={len(ga)} bp {ga.bp.mean():+.1f} R {ga.R.mean():+.3f} | other n={len(gb)} bp {gb.bp.mean():+.1f} R {gb.R.mean():+.3f} | t(bp) {wt(ga.bp,gb.bp):+.2f} t(R) {wt(ga.R,gb.R):+.2f}")
        # matched control: non-condition days with VIX in same range as condition days, using vix_prev rank matching
        X = np.column_stack([np.ones(len(d)), d[c].astype(float), np.log(d.vix_prev.astype(float)), d.spx_rv20_prev.astype(float)])
        ok = ~np.isnan(X).any(1)
        for ycol in ["bp", "R"]:
            y = d[ycol].values[ok]; Xo = X[ok]
            beta, *_ = np.linalg.lstsq(Xo, y, rcond=None)
            res = y - Xo @ beta
            # HC1 robust se
            XtXi = np.linalg.inv(Xo.T @ Xo)
            S = (Xo * res[:, None]**2).T @ Xo
            V = XtXi @ S @ XtXi * len(y)/(len(y)-Xo.shape[1])
            print(f"  OLS {ycol} ~ cond + log(vix_prev) + rv20: cond coef {beta[1]:+.3f} (robust t {beta[1]/np.sqrt(V[1,1]):+.2f}); logvix coef {beta[2]:+.3f} (t {beta[2]/np.sqrt(V[2,2]):+.2f})")

    # 2. Circular-shift permutation on the trading calendar (keeps clustering of condition days), stat = mean bp diff
    days = ctx.index[ctx.index >= d.date.min()]
    cond_series = pd.Series(False, index=days)
    if c == "r1":
        cond_series[:] = (ctx.loc[days, "spx_ret_1d_prev"] <= -2).values
    else:
        cond_series[:] = days.isin(fomc)
    pos = pd.Series(np.arange(len(days)), index=days)
    tp = pos.reindex(d.date).values
    keep = ~np.isnan(tp); tp = tp[keep].astype(int)
    for ycol in ["bp", "R"]:
        y = d[ycol].values[keep]
        cs = cond_series.values
        obs = y[cs[tp]].mean() - y[~cs[tp]].mean()
        sh = []
        for k in range(60, len(days)-60):
            cc = np.roll(cs, k)[tp]
            if cc.sum() >= 10:
                sh.append(y[cc].mean() - y[~cc].mean())
        sh = np.array(sh)
        print(f"  circular-shift ({ycol}): obs diff {obs:+.3f}; {len(sh)} shifts; share as bad or worse {np.mean(sh <= obs)*100:.2f}%; shift 1st pct {np.percentile(sh,1):+.3f}")

    # 3. pre-2018 vs 2018+ in bp and R
    for lab, g in [("2010-2017", d[d.year < 2018]), ("2018-2026", d[d.year >= 2018])]:
        ga, gb = g[g[c]], g[~g[c]]
        print(f"  {lab}: n={len(ga)} bp {ga.bp.mean():+.1f} vs {gb.bp.mean():+.1f} (t {wt(ga.bp,gb.bp):+.2f}); R {ga.R.mean():+.3f} vs {gb.R.mean():+.3f} (t {wt(ga.R,gb.R):+.2f})")

    # 4. Right tail: big winners on condition days
    q99 = d.R.quantile(0.99); q95 = d.R.quantile(0.95)
    print(f"  right tail: share of trades on cond days {len(a)/len(d)*100:.1f}%; of top-5% R trades {(d[d.R>=q95][c]).mean()*100:.1f}%; of top-1% {(d[d.R>=q99][c]).mean()*100:.1f}%; best cond-day trades (usd): {sorted(a.usd)[-3:]}")
    top20 = d.nlargest(20, "usd")
    print(f"  top-20 $ trades of model on cond days: {int(top20[c].sum())}; sum of cond-day positive trades ${a.usd[a.usd>0].sum():.0f}, negative ${a.usd[a.usd<0].sum():.0f}")

    # 5. Cost of being wrong (recent scale, 2021-2026)
    rec = d[d.year >= 2021]
    yrs = rec.year.nunique()
    na_ = rec[c].sum() / (rec.date.max() - rec.date.min()).days * 365.25
    other_mean = rec[~rec[c]].usd.mean(); cond_mean = rec[rec[c]].usd.mean()
    print(f"  2021-26: cond trades/yr {na_:.1f}; other-day mean ${other_mean:+.2f}; cond-day mean ${cond_mean:+.2f}")
    print(f"    if rule useless (cond days = other days): skipping costs ~${na_*other_mean:.0f}/yr; if real at observed size: keeping costs ~${-na_*cond_mean:.0f}/yr; break-even shrink: effect only needs cond mean < ${0:.0f}... ")
    # leave-one-year-out in bp
    loyo = []
    for y_ in sorted(d.year.unique()):
        g = d[d.year != y_]
        loyo.append(wt(g[g[c]].bp, g[~g[c]].bp))
    print(f"  leave-one-year-out t(bp): min {max(loyo):+.2f} (weakest) .. {min(loyo):+.2f}")
