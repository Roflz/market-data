"""Builder X - Section 13 (L1 release-day fade, L2 release-day filter on the overnight breakout). Vectorized.
Run from the project dir:  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this> <outdir>
"""
import json, sys
import numpy as np
import pandas as pd
from scipy import stats

import calendar_days as cd

X = sys.argv[1].rstrip("/") + "/"
A = pd.read_pickle(X + "arrays.pkl")
T0 = 8 * 60
S = lambda h, m: h * 60 + m - T0           # slot of the bar stamped h:m ET
S830, S844, S845, S944, S945 = S(8, 30), S(8, 44), S(8, 45), S(9, 44), S(9, 45)
SPEC = {"NQ": dict(micro="MNQ", ppt=2.0, cost_usd=2.00), "ES": dict(micro="MES", ppt=5.0, cost_usd=3.50)}
TICK = 0.25
DATA_END = pd.Timestamp("2026-11-06")
ERA = {"2010-2017": (pd.Timestamp("2010-01-01"), pd.Timestamp("2017-12-31")),
       "2018-2026": (pd.Timestamp("2018-01-01"), pd.Timestamp("2026-12-31"))}
ERA_YEARS = {"2010-2017": (pd.Timestamp("2017-12-31") - pd.Timestamp("2010-06-07")).days / 365.25,
             "2018-2026": (DATA_END - pd.Timestamp("2018-01-01")).days / 365.25 + 1 / 365.25,
             "all": (DATA_END - pd.Timestamp("2010-06-07")).days / 365.25 + 1 / 365.25}
GAP_MAX_MISSING = 4    # skip if 5+ consecutive 1-min bars are missing in 8:30-9:45 (= consecutive bar opens >5 min apart)

nfp = set(pd.to_datetime(pd.read_csv(X + "nfp_dates.csv").date))
cpi = set(cd.cpi_days())


def l1_arrays(sym, signal):
    """All days at once. signal: 'close844' (primary: 8:30 open -> 8:44 close, the last price known before 8:45:00)
    or 'open845' (literal spec wording: 8:30 open -> 8:45 open). Returns a per-day DataFrame for every day in the data."""
    a = A[sym]
    O, H, L, C, inst, days = a["Open"], a["High"], a["Low"], a["Close"], a["inst"], a["days"]
    w = slice(S830, S945 + 1)                                    # bars stamped 8:30 .. 9:45 inclusive
    present = ~np.isnan(O[:, w])
    # longest run of missing bars inside 8:30-9:45 (vectorized run-length via cumulative trick)
    miss = (~present).astype(np.int32)
    run = np.zeros_like(miss)
    for j in range(miss.shape[1]):                               # 76 columns; per-column vector op over all days
        run[:, j] = (run[:, j - 1] + 1) * miss[:, j] if j else miss[:, j]
    maxgap = run.max(axis=1)
    iw = np.where(present, inst[:, w], -1)
    imax, imin = iw.max(axis=1), np.where(present, inst[:, w], np.iinfo(np.int64).max).min(axis=1)
    roll = present.any(axis=1) & (imax != imin)
    need = ~np.isnan(O[:, S830]) & ~np.isnan(C[:, S844]) & ~np.isnan(O[:, S845]) & ~np.isnan(O[:, S945])
    gap = maxgap > GAP_MAX_MISSING
    ok = need & ~gap & ~roll
    endp = C[:, S844] if signal == "close844" else O[:, S845]
    move = endp - O[:, S830]
    d = -np.sign(move)                                           # fade
    ent = O[:, S845]
    ext_t = O[:, S945]
    # disaster stop: 2 x |move| beyond entry, snapped to a tick away from entry (never better than formula)
    raw_stop = ent - d * 2 * np.abs(move)
    stop = np.where(d > 0, np.floor(raw_stop / TICK + 1e-9) * TICK, np.ceil(raw_stop / TICK - 1e-9) * TICK)
    hs = slice(S845, S944 + 1)                                   # bars held: 8:45 .. 9:44 (exit at 9:45 open)
    Hh, Lh, Oh = H[:, hs], L[:, hs], O[:, hs]
    hit = np.where(d[:, None] > 0, Lh <= stop[:, None], Hh >= stop[:, None]) & ~np.isnan(Hh)
    anyhit = hit.any(axis=1)
    k = np.where(anyhit, hit.argmax(axis=1), -1)
    ko = np.take_along_axis(Oh, np.maximum(k, 0)[:, None], 1)[:, 0]
    gapthru = np.where(d > 0, ko < stop, ko > stop)               # bar opened beyond the stop: fill at that open
    stop_fill = np.where(gapthru, ko, stop)
    ext_s = np.where(anyhit, stop_fill, ext_t)
    t_stop = np.where(anyhit, k + S845, S945)
    df = pd.DataFrame({"date": days, "ok": ok, "need": need, "gap": gap, "roll": roll, "maxgap": maxgap,
                       "inst": inst[:, S845], "o830": O[:, S830], "c844": C[:, S844], "o845": ent, "o945": ext_t,
                       "move": move, "d": d, "stop": stop, "stop_hit": anyhit, "stop_slot": t_stop,
                       "exit_stop": ext_s})
    return df


def hhmm(slot):
    m = T0 + int(slot)
    return f"{m // 60:02d}:{m % 60:02d}"


def trades(df, sym, use_stop, mask):
    sp = SPEC[sym]
    t = df[mask & df.ok & (df.move != 0)].copy()
    t["side"] = np.where(t.d > 0, "long", "short")
    t["entry_time"] = "08:45"
    t["entry"] = t.o845
    if use_stop:
        t["exit"] = t.exit_stop
        t["exit_time"] = [hhmm(s) for s in t.stop_slot]
        t["exit_reason"] = np.where(t.stop_hit, "disaster_stop", "time_9:45")
    else:
        t["exit"] = t.o945
        t["exit_time"] = "09:45"
        t["exit_reason"] = "time_9:45"
    t["gross_pts"] = t.d * (t.exit - t.entry)
    t["cost_pts"] = sp["cost_usd"] / sp["ppt"]
    t["net_pts"] = t.gross_pts - t.cost_pts
    t["gross_usd"] = t.gross_pts * sp["ppt"]
    t["net_usd"] = t.net_pts * sp["ppt"]
    t["net_bp"] = 1e4 * t.net_pts / t.entry
    t["gross_bp"] = 1e4 * t.gross_pts / t.entry
    t["is_cpi"] = t.date.isin(cpi)
    t["is_nfp"] = t.date.isin(nfp)
    t["instrument"] = sp["micro"]
    t["move_830_signal"] = t.move
    cols = ["date", "entry_time", "exit_time", "side", "entry", "exit", "exit_reason", "gross_pts", "net_pts",
            "gross_usd", "net_usd", "net_bp", "gross_bp", "instrument", "inst", "o830", "c844", "o845", "o945",
            "move_830_signal", "stop", "is_cpi", "is_nfp"]
    return t[cols].reset_index(drop=True)


def tstat(x):
    x = np.asarray(x, float)
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std(ddof=1) > 0 else float("nan")


def summ(t, years=None):
    if len(t) == 0:
        return dict(n=0)
    x = t.net_usd.to_numpy()
    srt = np.sort(x)[::-1]
    out = dict(n=int(len(t)), mean_net_usd=float(x.mean()), total_net_usd=float(x.sum()),
               mean_gross_usd=float(t.gross_usd.mean()), total_gross_usd=float(t.gross_usd.sum()),
               mean_net_bp=float(t.net_bp.mean()), median_net_usd=float(np.median(x)), t=tstat(x),
               hit_rate=float((x > 0).mean()), worst_usd=float(x.min()), best_usd=float(x.max()),
               best5_sum_usd=float(srt[:5].sum()),
               best5_share_of_total=float(srt[:5].sum() / x.sum()) if x.sum() != 0 else float("nan"))
    if years:
        out["trades_per_year"] = len(t) / years
    if "exit_reason" in t:
        out["stop_exits"] = int((t.exit_reason == "disaster_stop").sum())
    return out


def by_period(t):
    y = t.date.dt.year
    blk = (y - (y % 2)).astype(str) + "-" + (y - (y % 2) + 1).astype(str)
    by_year = {int(k): summ(g) for k, g in t.groupby(y)}
    by_blk = {k: summ(g) for k, g in t.groupby(blk)}
    by_year = {k: {kk: v[kk] for kk in ("n", "mean_net_usd", "total_net_usd", "t") if kk in v} for k, v in by_year.items()}
    by_blk = {k: {kk: v[kk] for kk in ("n", "mean_net_usd", "total_net_usd", "t") if kk in v} for k, v in by_blk.items()}
    return by_year, by_blk


def era_mask(dates, era):
    if era == "all":
        return np.ones(len(dates), bool)
    a, b = ERA[era]
    return (dates >= a) & (dates <= b)


def main():
    out = {"L1": {}, "L2": {}, "meta": {}}
    D = {}
    for sym in ("NQ", "ES"):
        for sig in ("close844", "open845"):
            D[(sym, sig)] = l1_arrays(sym, sig)
    # ---- day accounting for release days
    acct = {}
    for sym in ("NQ", "ES"):
        df = D[(sym, "close844")]
        dd = set(df.date)
        for name, s in (("NFP", nfp), ("CPI", cpi)):
            s_in = sorted(x for x in s if pd.Timestamp("2010-06-07") <= x <= DATA_END)
            sub = df[df.date.isin(s_in)]
            acct[f"{sym}_{name}"] = dict(release_days_in_data_period=len(s_in), with_bars=int(len(sub)),
                                         missing_bars_needed=int((~sub.need).sum()), gap_skip=int((sub.need & sub.gap).sum()),
                                         roll_skip=int((sub.need & ~sub.gap & sub.roll).sum()), ok=int(sub.ok.sum()),
                                         zero_move=int((sub.ok & (sub.move == 0)).sum()),
                                         no_bars_dates=[str(x.date()) for x in s_in if x not in dd],
                                         skipped_dates=[str(x.date()) for x in sub.date[~sub.ok]])
    out["meta"]["day_accounting"] = acct
    both = sorted(cpi & nfp)
    out["meta"]["cpi_and_nfp_same_day"] = [str(x.date()) for x in both]
    sess = pd.read_pickle("data/daily_sessions_NQ.pkl")
    noncash = set(sess.index[~sess.cash_day])
    out["meta"]["nfp_on_globex_only_sessions"] = [str(x.date()) for x in sorted(nfp & noncash)]

    # ---- L1 sets
    sets = {"NFP": lambda d: d.isin(nfp), "CPI": lambda d: d.isin(cpi),
            "CPI_or_NFP_once": lambda d: d.isin(cpi | nfp), "CPI_and_NFP": lambda d: d.isin(cpi & nfp),
            "control_nonrelease_days": lambda d: ~d.isin(cpi | nfp)}
    variants = {"primary_time": ("close844", False), "disaster_stop": ("close844", True),
                "literal_open845_time": ("open845", False), "literal_open845_stop": ("open845", True)}
    allT = {}
    for vname, (sig, st) in variants.items():
        for sym in ("NQ", "ES"):
            df = D[(sym, sig)]
            for sname, f in sets.items():
                m = f(df.date)
                t = trades(df, sym, st, m.to_numpy())
                allT[(vname, sym, sname)] = t
                for era in ("2010-2017", "2018-2026", "all"):
                    te = t[era_mask(t.date, era)]
                    r = summ(te, ERA_YEARS[era])
                    if sname != "control_nonrelease_days" and len(te):
                        r["by_year"], r["by_2yr_block"] = by_period(te)
                    out["L1"].setdefault(vname, {}).setdefault(SPEC[sym]["micro"], {}).setdefault(sname, {})[era] = r
                if sname != "control_nonrelease_days" or vname == "primary_time":
                    fn = f"L1_{vname}_{SPEC[sym]['micro']}_{sname}.csv"
                    t.to_csv(X + fn, index=False)

    # ---- judged test: NFP 2018+ primary
    tq = allT[("primary_time", "NQ", "NFP")]; tq = tq[tq.date >= "2018-01-01"]
    te = allT[("primary_time", "ES", "NFP")]; te = te[te.date >= "2018-01-01"]
    mq, tt, me = tq.net_usd.mean(), tstat(tq.net_usd), te.net_usd.mean()
    crit = [dict(name="MNQ mean net $/trade > 0 (NFP 2018-2026)", value=f"{mq:+.2f}", pass_=bool(mq > 0)),
            dict(name="MNQ t > 2", value=f"{tt:.2f}", pass_=bool(tt > 2)),
            dict(name="MES mean net same sign as MNQ", value=f"{me:+.2f}", pass_=bool(np.sign(me) == np.sign(mq)))]
    # MES on common days only (report)
    common = set(tq.date) & set(te.date)
    out["L1_judged"] = dict(MNQ=summ(tq, ERA_YEARS["2018-2026"]), MES=summ(te, ERA_YEARS["2018-2026"]), criteria=crit,
                            passed=all(c["pass_"] for c in crit),
                            common_days=dict(n=len(common), MNQ_mean=float(tq[tq.date.isin(common)].net_usd.mean()),
                                             MES_mean=float(te[te.date.isin(common)].net_usd.mean())))
    tq.to_csv(X + "L1-NFP_judged_MNQ_2018_2026.csv", index=False)
    te.to_csv(X + "L1-NFP_judged_MES_2018_2026.csv", index=False)
    # sign-randomization control (report only): random fade/follow direction per trade, seed 12345, 1000 reps
    rng = np.random.default_rng(12345)
    g = tq.gross_usd.to_numpy(); c = SPEC["NQ"]["cost_usd"]
    sims = np.array([(g * rng.choice([-1, 1], len(g)) - c).mean() for _ in range(1000)])
    out["L1_judged"]["control_random_direction"] = dict(reps=1000, seed=12345, mean_of_sims=float(sims.mean()),
                                                        p_one_sided=float((sims >= mq).mean()))

    # ---- overlap with existing strategies (report only)
    cm = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    l1 = allT[("primary_time", "NQ", "CPI_or_NFP_once")]
    ov = {}
    for mdl in ("opening_range", "overnight_break", "expiry_fade"):
        g_ = cm[cm.model == mdl].set_index("date")
        j = l1.set_index("date").join(g_[["side", "usd"]].rename(columns={"side": "m_side", "usd": "m_usd"}), how="inner")
        ov[mdl] = dict(days_both=int(len(j)), same_side=int((j.side == j.m_side).sum()),
                       L1_usd_on_those=float(j.net_usd.sum()), model_usd_on_those=float(j.m_usd.sum()))
    out["L1_overlap"] = ov

    # ---- L2
    rel = cpi | nfp
    for mdl in ("overnight_break", "opening_range"):
        g_ = cm[cm.model == mdl].copy()
        g_["release"] = g_.date.isin(rel)
        g_["is_cpi"] = g_.date.isin(cpi); g_["is_nfp"] = g_.date.isin(nfp)
        g_.to_csv(X + f"L2_{mdl}_trades_flagged.csv", index=False)
        res = {}
        for era in ("2010-2017", "2018-2026", "all"):
            e = g_[era_mask(g_.date, era)]
            r_ = {}
            for lab, sel in (("release", e.release), ("cpi_only_flag", e.is_cpi), ("nfp_only_flag", e.is_nfp)):
                a_, b_ = e[sel], e[~e.release] if lab == "release" else e[~sel]
                w = stats.ttest_ind(a_.usd, b_.usd, equal_var=False)
                r_[lab] = dict(n_release=int(len(a_)), n_other=int(len(b_)),
                               mean_usd_release=float(a_.usd.mean()), mean_usd_other=float(b_.usd.mean()),
                               diff=float(a_.usd.mean() - b_.usd.mean()), welch_t=float(w.statistic), p_two_sided=float(w.pvalue),
                               mean_R_release=float(a_.R.mean()), mean_R_other=float(b_.R.mean()),
                               mean_bp_release=float(a_.bp.mean()), mean_bp_other=float(b_.bp.mean()),
                               total_usd_release=float(a_.usd.sum()), t_release_alone=tstat(a_.usd),
                               welch_t_R=float(stats.ttest_ind(a_.R, b_.R, equal_var=False).statistic),
                               p_R=float(stats.ttest_ind(a_.R, b_.R, equal_var=False).pvalue))
            res[era] = r_
        if mdl == "overnight_break":
            c1 = [dict(name=f"release-day trades worse with two-sided Welch p<0.05 in {era}",
                       value=f"diff {res[era]['release']['diff']:+.2f} $/trade, p={res[era]['release']['p_two_sided']:.3f}",
                       pass_=bool(res[era]["release"]["diff"] < 0 and res[era]["release"]["p_two_sided"] < 0.05))
                  for era in ("2010-2017", "2018-2026")]
            res["criteria"] = c1
            res["adopt_skip"] = all(c["pass_"] for c in c1)
        out["L2"][mdl] = res
    json.dump(out, open(X + "summary.json", "w"), indent=1, default=str)
    print(json.dumps(dict(judged=out["L1_judged"], L2=out["L2"]["overnight_break"]["criteria"],
                          adopt=out["L2"]["overnight_break"]["adopt_skip"], acct=acct, both=out["meta"]["cpi_and_nfp_same_day"],
                          noncash=out["meta"]["nfp_on_globex_only_sessions"], overlap=ov), indent=1, default=str))


main()
