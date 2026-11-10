"""S3 big-day close-flow spread continuation 15:30-16:00; V1 (1.5% gate), V2 (NQ-only 1% gate, ES same sign);
controls C1 (coin) and C2 (14:30-15:00 placebo)."""
import os, sys, json, pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *
import s1 as S1mod

with open(f"{HERE}/sessions.pkl", "rb") as f:
    S = pickle.load(f)
F = pd.read_pickle(f"{HERE}/features.pkl")
ctx = pd.read_pickle(f"{PROJ}/data/market_context.pkl")
S1_days = set(F.index[S1mod.signal_days("1430", True, "ge1")])

elig3 = (F.full & ~F.roll & F.pc_ok & np.isfinite(F.b) & F.bars15_ok
         & pd.Series([np.isfinite(S.CN[t, 389]) and np.isfinite(S.CE[t, 389]) for t in range(S.n)], index=F.index))
RN, RE = F.nq_ret15, F.es_ret15


def gate(kind):
    same = np.sign(RN) == np.sign(RE)
    if kind == "1.0":
        g = (RN.abs() >= 0.01) & (RE.abs() >= 0.01) & same
    elif kind == "1.5":
        g = (RN.abs() >= 0.015) & (RE.abs() >= 0.015) & same
    else:  # V2: |R_NQ| >= 1%, R_ES same sign, any size
        g = (RN.abs() >= 0.01) & same & (RE != 0)
    return elig3 & g & ~F.index.isin(list(S1_days))


def run(kind):
    rows = []
    for d in F.index[gate(kind)]:
        t = S.pos_of[d]
        nq_dir = 1 if RN.loc[d] > 0 else -1
        rec = simulate_intraday(S, t, 359, 360, 389, nq_dir, F.b.loc[d], stop=None)
        # C2 placebo: same day, same direction and sizing rule, held 14:30 -> 15:00 (close of the 14:59 bar)
        pl = simulate_intraday(S, t, 299, 300, 329, nq_dir, F.b.loc[d], stop=None)
        rec.update(date=d.strftime("%Y-%m-%d"), entry_time=rec["entry_bar_N"], exit_time=rec["exit_bar_N"],
                   R_NQ=RN.loc[d], R_ES=RE.loc[d], b=F.b.loc[d], fomc=bool(F.fomc.loc[d]), cpi=bool(F.cpi.loc[d]),
                   vix_tercile=float(ctx.vix_tercile.get(d, np.nan)), expiry_friday=bool(F.expiry.loc[d]),
                   placebo_net_bp=pl["net_bp"], placebo_gross_bp=pl["gross_bp"],
                   nq_last30_bp_dir=1e4 * nq_dir * np.log(S.CN[t, 389] / S.ON[t, 360]),
                   es_last30_bp_dir=1e4 * nq_dir * np.log(S.CE[t, 389] / S.OE[t, 360]),
                   decision_bar=tm(359))
        rows.append(rec)
    return pd.DataFrame(rows)


COLS = ["date", "entry_time", "exit_time", "side", "nq_entry_fill", "nq_exit_fill", "es_entry_fill", "es_exit_fill",
        "exit_reason", "gross_pts_nq_equiv", "net_pts_nq_equiv", "net_usd", "net_bp", "eN", "xN", "eE", "xE",
        "entry_bar_E", "exit_bar_E", "n_nq", "n_es", "k", "b", "R_NQ", "R_ES", "gross_usd", "cost_usd", "gross_bp",
        "cost_bp", "notional_usd", "gross_long_usd", "fomc", "cpi", "vix_tercile", "expiry_friday", "placebo_net_bp",
        "placebo_gross_bp", "nq_last30_bp_dir", "es_last30_bp_dir", "inst_N", "inst_E", "decision_bar"]


def report(df, primary):
    start = F.index[elig3][0]
    out = summarize(df, start=start, nw_lags=5)
    out["sample_start"] = start.strftime("%Y-%m-%d")
    c1 = coin_control(df)
    out["C1_coin_p95"] = float(np.percentile(c1, 95)); out["C1_coin_p5"] = float(np.percentile(c1, 5))
    out["C2_placebo_mean_net_bp"] = float(df.placebo_net_bp.mean())
    out["C2_placebo_mean_gross_bp"] = float(df.placebo_gross_bp.mean())
    out["two_sided_p"] = p_two_sided(out["t"], out["n"])
    rmin = np.minimum(df.R_NQ.abs(), df.R_ES.abs())
    out["by_R_bucket_min_abs"] = {lab: {"n": int(m.sum()), "mean_net_bp": float(df.net_bp[m].mean()) if m.sum() else None,
                                        "mean_gross_bp": float(df.gross_bp[m].mean()) if m.sum() else None}
                                  for lab, m in (("<1%", rmin < 0.01), ("1-1.5%", (rmin >= 0.01) & (rmin < 0.015)),
                                                 ("1.5-2%", (rmin >= 0.015) & (rmin < 0.02)), (">=2%", rmin >= 0.02))}
    out["by_vix_tercile"] = {str(int(k)) if k == k else "nan": {"n": int(len(g)), "mean_net_bp": float(g.net_bp.mean()),
                                                             "mean_gross_bp": float(g.gross_bp.mean())}
                             for k, g in df.groupby(df.vix_tercile.fillna(-1))}
    for lab, m in (("fomc_days", df.fomc), ("cpi_days", df.cpi), ("non_fomc_cpi", ~df.fomc & ~df.cpi),
                   ("expiry_fridays", df.expiry_friday)):
        out[lab] = {"n": int(m.sum()), "mean_net_bp": float(df.net_bp[m].mean()) if m.sum() else None,
                    "mean_gross_bp": float(df.gross_bp[m].mean()) if m.sum() else None}
    out["outright_last30_same_days"] = {"nq_mean_bp_in_trade_dir": float(df.nq_last30_bp_dir.mean()),
                                        "es_mean_bp_in_trade_dir": float(df.es_last30_bp_dir.mean()),
                                        "nq_t": float(tstat(df.nq_last30_bp_dir)), "es_t": float(tstat(df.es_last30_bp_dir))}
    y = pd.to_datetime(df.date).dt.year
    c26 = df.cost_bp[y == 2026].mean()
    n26 = df.gross_bp - c26
    out["costs_at_2026_bp"] = {"cost_bp_2026": float(c26), "mean_net_bp": float(n26.mean()), "t": float(tstat(n26))}
    out["criteria"] = [
        {"name": "a: event-level t >= 2 (net, full sample)" if primary else "a: t >= 3 or Holm p < 0.05 (set in summary)",
         "value": f"t={out['t']:.3f} (NW5 {out['t_nw5']:.3f}; two-sided p={out['two_sided_p']:.3g})", "pass": bool(out["t"] >= 2)},
        {"name": "b: mean net > 0 in Jun 2020 - Nov 2026",
         "value": f"{out['eras']['2020-06..2026-11']['mean_net_bp']:.3f} bp", "pass": bool(out['eras']['2020-06..2026-11']['mean_net_bp'] > 0)},
        {"name": "c: mean net > 0 in >= 2/3 counted blocks", "value": f"{out['blocks_positive']}/{out['blocks_counted']}",
         "pass": bool(out['blocks_counted'] > 0 and out['blocks_positive'] >= 2 / 3 * out['blocks_counted'])},
        {"name": "d: mean net > C1 coin 95th pct", "value": f"{out['mean_net_bp']:.3f} vs {out['C1_coin_p95']:.3f}",
         "pass": bool(out['mean_net_bp'] > out['C1_coin_p95'])},
        {"name": "e: C2 15:30-16:00 mean net > 14:30-15:00 placebo mean net",
         "value": f"{out['mean_net_bp']:.3f} vs {out['C2_placebo_mean_net_bp']:.3f}",
         "pass": bool(out['mean_net_bp'] > out['C2_placebo_mean_net_bp'])},
        {"name": "f: mean gross >= 1.5 x mean cost",
         "value": f"gross {out['mean_gross_bp']:.3f} vs 1.5*cost {1.5 * out['mean_cost_bp']:.3f}",
         "pass": bool(out['mean_gross_bp'] >= 1.5 * out['mean_cost_bp'])},
    ]
    return out


if __name__ == "__main__":
    res = {}
    res["S1_overlap_before_precedence"] = int(sum(1 for d in F.index[elig3 & (RN.abs() >= 0.01) & (RE.abs() >= 0.01)
                                                                      & (np.sign(RN) == np.sign(RE))] if d in S1_days))
    for name, kind in (("S3", "1.0"), ("S3-V1", "1.5"), ("S3-V2", "nq")):
        df = run(kind)
        df[[c for c in COLS if c in df.columns]].to_csv(f"{HERE}/trades_{name}.csv", index=False)
        out = report(df, name == "S3")
        out["share_after_2020_06"] = float((pd.to_datetime(df.date) >= "2020-06-01").mean())
        res[name] = out
        print(name, out["n"], f"per_yr={out['per_year']:.1f} net={out['mean_net_bp']:.2f} gross={out['mean_gross_bp']:.2f} "
              f"cost={out['mean_cost_bp']:.2f} t={out['t']:.2f} $/tr={out['net_usd_per_trade']:.2f} placebo={out['C2_placebo_mean_net_bp']:.2f}")
    print("S1 overlap before precedence:", res["S1_overlap_before_precedence"])
    with open(f"{HERE}/s3_results.json", "w") as f:
        json.dump(jsonable(res), f, indent=1)
