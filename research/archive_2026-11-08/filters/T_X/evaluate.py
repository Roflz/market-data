"""
Builder X: apply T1-T4 to the live opening_range trades and evaluate the pre-registered pass rule (SPEC.md section T).
Outputs in T_X/: T{1..4}_decisions.csv, summary.json, report.txt
"""
import json
import numpy as np
import pandas as pd
from scipy import stats as st

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/T_X"
ERAS = [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020), ("2021-23", 2021, 2023),
        ("2024-26", 2024, 2026)]
T_MIN = 2.5
LINES = []


def say(s=""):
    print(s)
    LINES.append(s)


def maxdd(daily):
    eq = np.concatenate([[0.0], np.cumsum(daily)])           # equity starts at 0 before the first day
    return float((np.maximum.accumulate(eq) - eq).max())


def welch(a, b):
    """Welch t of mean(a) - mean(b), and its one-sided p (Welch-Satterthwaite df)."""
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    t = (a.mean() - b.mean()) / np.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return float(t), float(st.t.sf(t, df)), float(df)


def book_stats(tr):
    d = tr.groupby("date").usd.sum().sort_index()
    return dict(net=float(d.sum()), maxdd=maxdd(d.to_numpy()), worst_day=float(d.min()), n_days=int(len(d)))


def evaluate(orb, keep, all_trades, cost_extra=0.0):
    """pass-rule items for one filter. keep: boolean array aligned with orb."""
    usd = orb.usd.to_numpy() - cost_extra
    y = orb.date.dt.year.to_numpy()
    k, r = usd[keep], usd[~keep]
    res = dict(kept=int(keep.sum()), removed=int((~keep).sum()), kept_usd=float(k.sum()), removed_usd=float(r.sum()),
               removed_usd_2010_17=float(usd[~keep & (y <= 2017)].sum()),
               removed_usd_2018_26=float(usd[~keep & (y >= 2018)].sum()),
               kept_mean=float(k.mean()), removed_mean=float(r.mean()), share_removed=float((~keep).mean()))
    res["a"] = bool(res["removed_usd"] < 0 and res["removed_usd_2010_17"] < 0 and res["removed_usd_2018_26"] < 0)
    res["welch_t"], res["p_one_sided"], res["welch_df"] = welch(k, r)
    res["b"] = bool(res["welch_t"] >= T_MIN)
    # (c) the opening_range model alone: daily net $ (one trade per day)
    before = pd.Series(usd, index=orb.date).groupby(level=0).sum()
    after = pd.Series(k, index=orb.date[keep]).groupby(level=0).sum()
    res["dd_before"], res["dd_after"] = maxdd(before.to_numpy()), maxdd(after.to_numpy())
    res["worst_day_before"], res["worst_day_after"] = float(before.min()), float(after.min())
    res["c"] = bool(res["dd_after"] <= res["dd_before"] and res["worst_day_after"] >= res["worst_day_before"])
    res["passed"] = bool(res["a"] and res["b"] and res["c"])
    # report-only: eras, 2023-2026, years
    def split(mask):
        return dict(n_kept=int((keep & mask).sum()), n_removed=int((~keep & mask).sum()),
                    kept_usd=float(usd[keep & mask].sum()), removed_usd=float(usd[~keep & mask].sum()),
                    removed_per_trade=float(usd[~keep & mask].mean()) if (~keep & mask).any() else None,
                    kept_per_trade=float(usd[keep & mask].mean()) if (keep & mask).any() else None,
                    share_removed=float((~keep & mask).sum() / mask.sum()))
    res["eras"] = {nm: split((y >= a) & (y <= b)) for nm, a, b in ERAS}
    res["2023-2026"] = split(y >= 2023)
    res["years"] = {int(yy): split(y == yy) for yy in np.unique(y)}
    # report-only: combined 3-model book
    at = all_trades.copy()
    at["usd"] = at.usd - np.where(at.model == "opening_range", cost_extra, 0.0) if cost_extra else at.usd
    drop_dates = set(orb.date[~keep])
    filt = at[~((at.model == "opening_range") & at.date.isin(drop_dates))]
    res["book_before"], res["book_after"] = book_stats(at), book_stats(filt)
    return res


def main():
    inp = pd.read_pickle(f"{OUT}/inputs.pkl")
    allt = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    orb = allt[allt.model == "opening_range"].reset_index(drop=True)
    assert orb.date.is_unique
    d = orb.side.map({"long": 1, "short": -1}).to_numpy()
    x = inp.reindex(orb.date)
    assert x.index.notna().all() and len(x) == len(orb)
    say(f"base: {len(orb)} opening_range trades, net ${orb.usd.sum():,.2f}; all models {len(allt)} trades "
        f"${allt.usd.sum():,.2f}")

    filters = {}
    # T1 trend agreement
    tr = x.trend.to_numpy()
    filters["T1"] = (tr == d, dict(trend_diff=x.trend_diff, c934_adj=x.c934, prev_ema20_adj=x.prev_ema20, trend=tr))
    # T2 gap agreement (zero / missing -> disagree)
    gp = x.gap.to_numpy()
    sg = np.where(np.isnan(gp), 0, np.sign(gp))
    filters["T2"] = (sg == d, dict(open930_adj=x.open930_adj, prev_cash_date=x.prev_cash_date,
                                     prev_close_adj=x.prev_close_adj,
                                     prev_close_bar_tmin=inp.close_tmin_sess.shift().reindex(orb.date).to_numpy(),
                                     gap=gp))
    # T3 strong open
    fc, fm = x.fc_range.to_numpy(), x.fc_med20.to_numpy()
    filters["T3"] = (np.where(x.fc_nprior.to_numpy() < 20, True, fc >= fm),
                     dict(fc_range=fc, fc_med20=fm, fc_nprior=x.fc_nprior))
    # T4 quiet night (today's range missing -> keep: no rule can be applied; does not occur)
    on, om = x.on_range.to_numpy(), x.on_med20.to_numpy()
    filters["T4"] = (np.where((x.on_nprior.to_numpy() < 20) | np.isnan(on), True, on <= om),
                     dict(on_range=on, on_med20=om, on_nprior=x.on_nprior, on_first_bar=x.on_first))

    summary = {}
    for nm, (keep, cols) in filters.items():
        keep = np.asarray(keep, bool)
        df = orb[["date", "side", "exit", "usd", "R", "bp"]].copy()
        for c, v in cols.items():
            df[c] = np.asarray(v)
        df["decision"] = np.where(keep, "keep", "remove")
        path = f"{OUT}/{nm}_decisions.csv"
        df.to_csv(path, index=False, date_format="%Y-%m-%d")
        r = evaluate(orb, keep, allt)
        r2 = evaluate(orb, keep, allt, cost_extra=1.0)
        r["two_ticks"] = {k: r2[k] for k in ("kept_usd", "removed_usd", "removed_usd_2010_17", "removed_usd_2018_26",
                                             "a", "welch_t", "b", "dd_before", "dd_after", "worst_day_before",
                                             "worst_day_after", "c", "passed", "book_before", "book_after",
                                             "eras", "2023-2026")}
        r["decisions_csv"] = path
        summary[nm] = r
        say(f"\n=== {nm} ===  kept {r['kept']} (${r['kept_usd']:,.0f}, ${r['kept_mean']:.2f}/tr)  removed {r['removed']} "
            f"(${r['removed_usd']:,.0f}, ${r['removed_mean']:.2f}/tr)  share removed {r['share_removed']:.1%}")
        say(f"  (a) removed $: full {r['removed_usd']:,.0f}  2010-17 {r['removed_usd_2010_17']:,.0f}  "
            f"2018-26 {r['removed_usd_2018_26']:,.0f}  -> {'PASS' if r['a'] else 'FAIL'}")
        say(f"  (b) Welch t kept-removed {r['welch_t']:.2f} (one-sided p {r['p_one_sided']:.4f}) >= {T_MIN} -> "
            f"{'PASS' if r['b'] else 'FAIL'}")
        say(f"  (c) ORB maxDD {r['dd_before']:,.0f} -> {r['dd_after']:,.0f}; worst day {r['worst_day_before']:,.0f} -> "
            f"{r['worst_day_after']:,.0f} -> {'PASS' if r['c'] else 'FAIL'}")
        say(f"  overall: {'PASSED' if r['passed'] else 'FAILED'}")
        for e, v in r["eras"].items():
            say(f"    {e}: removed {v['n_removed']:4d} ({v['share_removed']:.0%}) ${v['removed_usd']:>8,.0f}  "
                f"kept {v['n_kept']:4d} ${v['kept_usd']:>8,.0f}")
        v = r["2023-2026"]
        say(f"    2023-26: removed {v['n_removed']:4d} ({v['share_removed']:.0%}) ${v['removed_usd']:>8,.0f}  "
            f"kept {v['n_kept']:4d} ${v['kept_usd']:>8,.0f}")
        say("    years (removed $ / kept $): " + "  ".join(
            f"{yy}:{vv['removed_usd']:+.0f}/{vv['kept_usd']:+.0f}" for yy, vv in r["years"].items()))
        t2 = r["two_ticks"]
        say(f"  2 ticks/fill: removed ${t2['removed_usd']:,.0f} (10-17 {t2['removed_usd_2010_17']:,.0f}, 18-26 "
            f"{t2['removed_usd_2018_26']:,.0f}) a={t2['a']}  t={t2['welch_t']:.2f}  DD {t2['dd_before']:,.0f}->"
            f"{t2['dd_after']:,.0f}  worst {t2['worst_day_before']:,.0f}->{t2['worst_day_after']:,.0f}  pass={t2['passed']}")
        b0, b1 = r["book_before"], r["book_after"]
        say(f"  3-model book: net ${b0['net']:,.0f} -> ${b1['net']:,.0f}; maxDD ${b0['maxdd']:,.0f} -> ${b1['maxdd']:,.0f}; "
            f"worst day ${b0['worst_day']:,.0f} -> ${b1['worst_day']:,.0f}")

    # Holm step-down on the four one-sided p-values (report only; the binding rule is t >= 2.5 each)
    ps = sorted((summary[k]["p_one_sided"], k) for k in summary)
    alpha, stop = 0.025, False
    for i, (p, k) in enumerate(ps):
        thr = alpha / (len(ps) - i)
        rej = (not stop) and p <= thr
        stop = stop or not rej
        summary[k]["holm_one_sided_0.025_reject"] = bool(rej)
        summary[k]["holm_adj_p"] = float(min(1.0, max(pp * (len(ps) - j) for j, (pp, _) in enumerate(ps[:i + 1]))))
    say("\nHolm (one-sided alpha 0.025, report only): " + ", ".join(
        f"{k} adj p {summary[k]['holm_adj_p']:.4f} reject={summary[k]['holm_one_sided_0.025_reject']}" for k in summary))
    with open(f"{OUT}/summary.json", "w") as f:
        json.dump(summary, f, indent=1, default=str)
    with open(f"{OUT}/report.txt", "w") as f:
        f.write("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
