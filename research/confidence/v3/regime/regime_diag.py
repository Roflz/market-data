"""
v3/regime/regime_diag.py - light regime diagnostics (pre-holdout only, 2010-06 .. 2025-06-30 16:45 ET).

How much did the market's behaviour change, in quantities that matter to an EMA 8/20/50 pullback day trader?
Per market (ES, NQ, YM) by year and by quarter:
  rng_cost     median 15-min bar range in $ per micro / round-trip cost (signals.SPEC cost)  (RTH 09:30-16:00)
  vol_ann      annualised realised vol from 15-min RTH log returns (%)
  ac15, ac60   lag-1 autocorrelation of RTH 15-min / 60-min log returns (within session; + = trendy, - = choppy)
  vr4          variance ratio of 1-hour vs 4 x 15-min RTH returns (>1 trendy, <1 mean-reverting)
  ema_persist  P(EMA 8/20/50 still stacked the same way 4 bars later | stacked now), 15-min bars, all hours
  ema_run      mean length (15-min bars) of a stacked EMA 8/20/50 run
  stacked      share of 15-min bars with EMAs stacked (either way)
  pb_cont      pullback continuation rate = cont / (cont + fail), research/signals/out/pullbacks_{sym}_15.csv
  ushape       mean |15-min return| 09:30-10:00 / 12:00-14:00 (opening burst vs lunch)
  on_rth_vol   mean |15-min return| overnight (18:00-09:30) / RTH
  on_ret, day_ret  mean overnight (18:00 -> 09:30) and day (09:30 -> 16:00) return per session in $ per micro
  corr_es_nq   correlation of RTH 15-min returns ES vs NQ (and ES vs YM)
Then: change points (optimal partitioning, mean shift, BIC penalty) on each quarterly series, and a similarity score
of every past quarter / 4-quarter window to the last 12 months before the holdout (2024Q3 .. 2025Q2).
Output: v3/regime/out/*.csv and REGIME_TABLES.md
"""
import os
import numpy as np
import pandas as pd
import signals

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
PB = os.path.join(HERE, "..", "..", "..", "signals", "out")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
SYMS = ["ES", "NQ", "YM"]
RECENT = [pd.Period(q, "Q") for q in ("2024Q3", "2024Q4", "2025Q1", "2025Q2")]


def load(sym, tf):
    b = pd.read_parquet(os.path.join(DATA, f"bars_{sym}_{tf}.parquet"))
    if "ts" in b.columns:
        b = b.set_index("ts")
    b = b[b.index < HOLDOUT].copy()
    b["r"] = np.log(b.C / b.O)  # within-bar return (O..C) avoids the cross-session gap
    b["r_cc"] = np.log(b.C).groupby(b.session).diff()  # close-to-close inside the session
    b["q"] = b.session.dt.to_period("Q")
    b["y"] = b.session.dt.year
    t = b.index.hour * 100 + b.index.minute
    b["rth"] = (t >= 930) & (t < 1600)
    b["tod"] = t
    return b


def lag1(x):
    x = x.dropna()
    if len(x) < 30:
        return np.nan
    return float(np.corrcoef(x.values[1:], x.values[:-1])[0, 1])


def ac_within(df, col):
    """lag-1 autocorr of col, pairs only inside one session."""
    d = df[[col, "session"]].dropna()
    prev = d[col].shift(1)
    same = d.session.eq(d.session.shift(1))
    a, p = d[col][same], prev[same]
    if len(a) < 30:
        return np.nan
    return float(np.corrcoef(a, p)[0, 1])


def per_period(b15, b60, pb, sess, sym, key):
    spec = signals.SPEC[sym]
    usd, cost = spec["usd"], spec["cost"]
    rows = {}
    rth15 = b15[b15.rth]
    rth60 = b60[b60.rth]
    g15 = dict(tuple(b15.groupby(key)))
    g15r = dict(tuple(rth15.groupby(key)))
    g60r = dict(tuple(rth60.groupby(key)))
    for k, d in g15r.items():
        rng_usd = (d.H - d.L) * usd
        r = d.r_cc.dropna()
        dall = g15[k]
        # EMA stack persistence (all hours, 15-min)
        tr = dall.trend.values
        sess_arr = dall.session.values
        st = tr != 0
        fut = np.roll(tr, -4)
        same_sess = np.roll(sess_arr, -4) == sess_arr
        ok = st & same_sess
        ok[-4:] = False
        persist = float(np.mean(fut[ok] == tr[ok])) if ok.sum() else np.nan
        chg = np.r_[True, (tr[1:] != tr[:-1]) | (sess_arr[1:] != sess_arr[:-1])]
        runid = np.cumsum(chg)
        rl = pd.Series(st).groupby(runid).agg(["first", "size"])
        ema_run = float(rl.loc[rl["first"], "size"].mean())
        # variance ratio 60 vs 15 (RTH, within session): var of sums of 4 consecutive 15-min returns
        r4 = d.r.groupby([d.session, (d.tod // 100)]).sum()  # clock-hour blocks
        n4 = d.r.groupby([d.session, (d.tod // 100)]).size()
        r4 = r4[n4 == 4]
        vr4 = float(r4.var() / (4 * d.r.var())) if len(r4) > 30 else np.nan
        # U-shape and overnight/RTH vol
        open_ = d.r[(d.tod >= 930) & (d.tod < 1000)].abs().mean()
        lunch = d.r[(d.tod >= 1200) & (d.tod < 1400)].abs().mean()
        on = dall.r[~dall.rth & ((dall.tod >= 1800) | (dall.tod < 930))].abs().mean()
        rows[k] = dict(
            n_rth_bars=len(d),
            rng_usd=float(rng_usd.median()),
            rng_cost=float(rng_usd.median() / cost),
            vol_ann=float(r.std() * np.sqrt(26 * 252) * 100),
            ac15=ac_within(d, "r_cc"),
            ac60=ac_within(g60r[k], "r_cc") if k in g60r else np.nan,
            vr4=vr4,
            ema_persist=persist,
            ema_run=ema_run,
            stacked=float(st.mean()),
            ushape=float(open_ / lunch),
            on_rth_vol=float(on / d.r.abs().mean()),
        )
    out = pd.DataFrame.from_dict(rows, orient="index")
    # pullbacks
    p = pb[pb.outcome.isin(["continuation", "failure"])].copy()
    pk = p.year if key == "y" else p.q
    cont = p.groupby(pk).outcome.apply(lambda s: (s == "continuation").mean())
    out["pb_n"] = p.groupby(pk).size()
    out["pb_cont"] = cont
    # overnight vs day returns in $ per micro
    s = sess.copy()
    s["on"] = (s.px_0930 - s.px_1800) * usd
    s["day"] = (s.px_1600 - s.px_0930) * usd
    sk = s.index.year if key == "y" else s.index.to_period("Q")
    out["on_ret"] = s.groupby(sk).on.mean()
    out["day_ret"] = s.groupby(sk).day.mean()
    out["on_share_absmove"] = s.groupby(sk).apply(lambda x: x.on.abs().mean() / (x.on.abs().mean() + x.day.abs().mean()))
    return out


def corr_table(bars, key):
    res = {}
    rr = {s: bars[s][bars[s].rth].set_index("session", append=True)["r"] for s in bars}
    j = pd.concat(rr, axis=1).dropna(subset=["ES"])
    j[key] = j.index.get_level_values(1).year if key == "y" else pd.PeriodIndex(j.index.get_level_values(1), freq="Q")
    for k, d in j.groupby(key):
        res[k] = dict(corr_es_nq=d.ES.corr(d.NQ), corr_es_ym=d.ES.corr(d.YM) if d.YM.notna().sum() > 100 else np.nan)
    return pd.DataFrame.from_dict(res, orient="index")


def opt_partition(x, min_seg=4, pen=None):
    """Optimal partitioning for mean shifts in x (Gaussian, variance from MAD of diffs), BIC penalty."""
    x = np.asarray(x, float)
    n = len(x)
    sig = np.median(np.abs(np.diff(x))) / 0.6745 / np.sqrt(2) if n > 2 else 1.0
    sig = sig if sig > 0 else np.std(x) + 1e-12
    pen = pen if pen is not None else 3 * np.log(n)  # a bit stricter than BIC (2 log n) for robustness
    cs, cs2 = np.r_[0, np.cumsum(x)], np.r_[0, np.cumsum(x * x)]

    def cost(i, j):  # segment x[i:j]
        m = j - i
        s = cs[j] - cs[i]
        return (cs2[j] - cs2[i] - s * s / m) / sig ** 2

    F = np.full(n + 1, np.inf)
    F[0] = -pen
    last = np.zeros(n + 1, int)
    for j in range(min_seg, n + 1):
        for i in range(0, j - min_seg + 1):
            if i != 0 and i < min_seg:
                continue
            if not np.isfinite(F[i]):
                continue
            v = F[i] + cost(i, j) + pen
            if v < F[j]:
                F[j], last[j] = v, i
    cps, j = [], n
    while j > 0:
        i = last[j]
        if i > 0:
            cps.append(i)
        j = i
    return sorted(cps)


def main():
    bars15, bars60, sess, pbs = {}, {}, {}, {}
    for s in SYMS:
        bars15[s] = load(s, 15)
        bars60[s] = load(s, 60)
        ss = pd.read_parquet(os.path.join(DATA, f"sessions_{s}.parquet"))
        if "session" in ss.columns:
            ss = ss.set_index("session")
        sess[s] = ss[ss.index < pd.Timestamp("2025-06-30 18:00")]
        pb = pd.read_csv(os.path.join(PB, f"pullbacks_{s}_15.csv"), parse_dates=["t_event"])
        pb = pb[pb.t_event < HOLDOUT]
        pb["q"] = pb.t_event.dt.to_period("Q")  # approx: event clock date (evening events -> previous day)
        pbs[s] = pb
    tabs = {}
    for key in ("y", "q"):
        parts = []
        for s in SYMS:
            t = per_period(bars15[s], bars60[s], pbs[s], sess[s], s, key)
            t.insert(0, "sym", s)
            parts.append(t)
        T = pd.concat(parts)
        C = corr_table(bars15, key)
        T = T.join(C, how="left")
        T.index.name = "period"
        T.to_csv(os.path.join(OUT, f"by_{'year' if key == 'y' else 'quarter'}.csv"))
        tabs[key] = T
    Q = tabs["q"].reset_index()
    Q = Q[Q.n_rth_bars > 300]  # drop the stub 2010Q2 and a partial last quarter if any
    # ---- change points per series (quarterly)
    series = ["vol_ann", "rng_cost", "ac15", "ac60", "vr4", "ema_persist", "pb_cont", "ushape", "on_rth_vol",
              "corr_es_nq"]
    cp_rows = []
    for s in SYMS:
        d = Q[Q.sym == s].sort_values("period").reset_index(drop=True)
        for c in series:
            x = d[c].values
            if np.isnan(x).any():
                ok = ~np.isnan(x)
                d2, x = d[ok].reset_index(drop=True), x[ok]
            else:
                d2 = d
            y = np.log(x) if c in ("vol_ann", "rng_cost") else x
            cps = opt_partition(y)
            bounds = [0] + cps + [len(x)]
            segs = []
            for a, b_ in zip(bounds[:-1], bounds[1:]):
                segs.append(f"{d2.period[a]}..{d2.period[b_ - 1]}: {np.mean(x[a:b_]):.3g}")
            cp_rows.append(dict(sym=s, series=c, n_changes=len(cps),
                                change_at=", ".join(str(d2.period[i]) for i in cps), segments=" | ".join(segs)))
    CP = pd.DataFrame(cp_rows)
    CP.to_csv(os.path.join(OUT, "changepoints.csv"), index=False)
    # ---- similarity to the last 12 months (2024Q3..2025Q2), on standardised state variables
    state = ["vol_ann", "rng_cost", "ac15", "vr4", "ema_persist", "corr_es_nq"]
    sim_rows, win_rows = [], []
    for s in SYMS:
        d = Q[Q.sym == s].sort_values("period").set_index("period")[state].copy()
        d["vol_ann"] = np.log(d.vol_ann)
        d["rng_cost"] = np.log(d.rng_cost)
        z = (d - d.mean()) / d.std()
        rec = z.loc[[q for q in RECENT if q in z.index]].mean()
        dist = np.sqrt(((z - rec) ** 2).mean(axis=1))
        # without cost/range (which drifts mechanically with the price level)
        st2 = [c for c in state if c != "rng_cost"]
        dist2 = np.sqrt(((z[st2] - rec[st2]) ** 2).mean(axis=1))
        S = pd.DataFrame(dict(sym=s, dist_all=dist, dist_no_cost=dist2))
        S = S.join(z.add_prefix("z_"))
        sim_rows.append(S)
        # rolling 4-quarter windows vs the recent 4-quarter window (profile = mean z of the 4 quarters)
        zz = z.copy()
        for i in range(0, len(zz) - 3):
            w = zz.iloc[i:i + 4]
            win_rows.append(dict(sym=s, window=f"{w.index[0]}..{w.index[-1]}",
                                 dist_all=float(np.sqrt(((w.mean() - rec) ** 2).mean())),
                                 dist_no_cost=float(np.sqrt(((w[st2].mean() - rec[st2]) ** 2).mean()))))
    SIM = pd.concat(sim_rows)
    SIM.index.name = "quarter"
    SIM.to_csv(os.path.join(OUT, "similarity_quarters.csv"))
    W = pd.DataFrame(win_rows)
    W.to_csv(os.path.join(OUT, "similarity_windows.csv"), index=False)

    # ---- markdown tables
    fmt = {"rng_usd": "{:.1f}", "rng_cost": "{:.1f}", "vol_ann": "{:.1f}", "ac15": "{:+.3f}", "ac60": "{:+.3f}",
           "vr4": "{:.2f}", "ema_persist": "{:.2f}", "ema_run": "{:.1f}", "stacked": "{:.2f}", "pb_cont": "{:.2f}",
           "pb_n": "{:.0f}", "ushape": "{:.2f}", "on_rth_vol": "{:.2f}", "on_ret": "{:+.1f}", "day_ret": "{:+.1f}",
           "on_share_absmove": "{:.2f}", "corr_es_nq": "{:.2f}", "corr_es_ym": "{:.2f}", "n_rth_bars": "{:.0f}"}

    def md(df, cols):
        h = "| " + " | ".join([df.index.name or ""] + cols) + " |\n|" + "---|" * (len(cols) + 1) + "\n"
        for i, r in df.iterrows():
            h += "| " + str(i) + " | " + " | ".join(
                ("" if pd.isna(r[c]) else fmt.get(c, "{}").format(r[c])) for c in cols) + " |\n"
        return h

    Y = tabs["y"]
    cols = ["rng_usd", "rng_cost", "vol_ann", "ac15", "ac60", "vr4", "ema_persist", "ema_run", "pb_cont", "pb_n",
            "ushape", "on_rth_vol", "on_ret", "day_ret", "corr_es_nq"]
    txt = "# Regime diagnostics (pre-holdout, 2010-06 .. 2025-06-30)\n\n"
    for s in SYMS:
        txt += f"## {s} by year\n\n" + md(Y[Y.sym == s], cols) + "\n"
    txt += "## Change points (quarterly, mean shift, penalty 3 log n, min 4 quarters per segment)\n\n"
    for _, r in CP.iterrows():
        txt += f"- {r.sym} {r.series}: {r.n_changes} change(s) at [{r.change_at}] -> {r.segments}\n"
    txt += "\n## Quarters most similar to 2024Q3..2025Q2 (RMS distance in z-units; lower = more alike)\n\n"
    for s in SYMS:
        S = SIM[SIM.sym == s]
        S = S[~S.index.isin(RECENT)].sort_values("dist_no_cost")
        txt += f"### {s} top 12 (by distance without cost/range)\n\n" + md(S.head(12), ["dist_all", "dist_no_cost"]) + "\n"
    txt += "## 4-quarter windows most similar to the last 12 months\n\n"
    for s in SYMS:
        w = W[W.sym == s].sort_values("dist_no_cost").head(10).set_index("window")
        txt += f"### {s}\n\n" + md(w, ["dist_all", "dist_no_cost"]) + "\n"
    with open(os.path.join(OUT, "REGIME_TABLES.md"), "w") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
