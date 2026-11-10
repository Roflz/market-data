"""S1 calm-day NQ/ES residual fade (primary 14:30-16:00), V1 (15:30-16:00), V2 (no VIX filter), controls C1-C3."""
import os, sys, json, pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *

with open(f"{HERE}/sessions.pkl", "rb") as f:
    S = pickle.load(f)
F = pd.read_pickle(f"{HERE}/features.pkl")
models = pd.read_csv(f"{PROJ}/chosen_models_trades.csv", parse_dates=["date"])


def signal_days(window, use_f3=True, zgate="ge1"):
    z = F.z14 if window == "1430" else F.z15
    f2 = F.F2_14 if window == "1430" else F.F2_15
    base = F.elig & np.isfinite(z) & np.isfinite(F.zo) & f2 & F.F4
    if window == "1530":
        base &= F.bars15_ok
    if use_f3:
        base &= F.F3
    if zgate == "ge1":
        return base & (z.abs() >= 1.0)
    return base & (z.abs() < 1.0)


def run(window, use_f3=True, zgate="ge1"):
    z = F.z14 if window == "1430" else F.z15
    s = F.s14 if window == "1430" else F.s15
    dec, ent = (299, 300) if window == "1430" else (359, 360)
    days = signal_days(window, use_f3, zgate)
    rows = []
    for d in F.index[days]:
        t = S.pos_of[d]
        ze = z.loc[d]
        nq_dir = -1 if ze > 0 else 1                     # fade: z>0 -> short NQ / long ES
        rec = simulate_intraday(S, t, dec, ent, 389, nq_dir, F.b.loc[d],
                                stop=dict(o9N=S.ON[t, 0], o9E=S.OE[t, 0], s=s.loc[d], z_entry=ze))
        rec.update(date=d.strftime("%Y-%m-%d"), entry_time=rec["entry_bar_N"], exit_time=rec["exit_bar_N"],
                   z=ze, b=F.b.loc[d], s=s.loc[d], zo=F.zo.loc[d], vix_prev=F.vix_prev.loc[d],
                   vix_med252=F.vix_med252.loc[d], es_ret_prior_close=(F.es_ret14 if window == "1430" else F.es_ret15).loc[d],
                   expiry_friday=bool(F.expiry.loc[d]),
                   es_ret_window=np.log(S.CE[t, 389] / S.OE[t, ent]),
                   decision_bar=tm(dec))
        rows.append(rec)
    return pd.DataFrame(rows)


COLS = ["date", "entry_time", "exit_time", "side", "nq_entry_fill", "nq_exit_fill", "es_entry_fill", "es_exit_fill",
        "exit_reason", "gross_pts_nq_equiv", "net_pts_nq_equiv", "net_usd", "net_bp",
        "eN", "xN", "eE", "xE", "entry_bar_E", "exit_bar_E", "n_nq", "n_es", "k", "b", "s", "z", "zo",
        "vix_prev", "vix_med252", "es_ret_prior_close", "es_ret_window", "gross_usd", "cost_usd", "gross_bp",
        "cost_bp", "notional_usd", "gross_long_usd", "expiry_friday", "inst_N", "inst_E", "decision_bar",
        "stop_signal_bar", "z_at_stop"]


def report(df, name, start):
    out = summarize(df, start=start, nw_lags=5)
    c1 = coin_control(df)
    out["C1_coin_p95"] = float(np.percentile(c1, 95)); out["C1_coin_mean"] = float(c1.mean())
    out["stop_exits"] = int((df.exit_reason == "stop").sum())
    za = df.z.abs()
    out["by_z_bucket"] = {lab: {"n": int(m.sum()), "mean_net_bp": float(df.net_bp[m].mean()) if m.sum() else None,
                                "mean_gross_bp": float(df.gross_bp[m].mean()) if m.sum() else None,
                                "t": float(tstat(df.net_bp[m])) if m.sum() > 1 else None}
                          for lab, m in (("1-1.5", (za >= 1) & (za < 1.5)), ("1.5-2", (za >= 1.5) & (za < 2)),
                                         (">=2", za >= 2))}
    ex = df.expiry_friday
    out["expiry_fridays"] = {"n": int(ex.sum()), "mean_net_bp": float(df.net_bp[ex].mean()) if ex.sum() else None,
                             "total_usd": float(df.net_usd[ex].sum())}
    out["non_expiry"] = {"n": int((~ex).sum()), "mean_net_bp": float(df.net_bp[~ex].mean()),
                         "t": float(tstat(df.net_bp[~ex]))}
    y = pd.to_datetime(df.date).dt.year
    c26 = df.cost_bp[y == 2026].mean() if (y == 2026).any() else df.cost_bp[y >= 2025].mean()
    n26 = df.gross_bp - c26
    out["costs_at_2026_bp"] = {"cost_bp_2026": float(c26), "mean_net_bp": float(n26.mean()), "t": float(tstat(n26)),
                               "by_era": {"2010-06..2020-05": float(n26[pd.to_datetime(df.date) < "2020-06-01"].mean()),
                                          "2020-06..2026-11": float(n26[pd.to_datetime(df.date) >= "2020-06-01"].mean())}}
    # C3: residual market beta of trade return on ES 14:30(or 15:30)-16:00 return
    x = df.es_ret_window.to_numpy(); yv = df.net_bp.to_numpy() / 1e4
    beta = np.cov(x, yv, ddof=1)[0, 1] / np.var(x, ddof=1)
    out["C3_resid_market_beta"] = float(beta); out["C3_abs_beta_below_0.1"] = bool(abs(beta) < 0.1)
    # correlation with existing models (daily $)
    corr = {}
    sp = df.assign(date=pd.to_datetime(df.date)).groupby("date").net_usd.sum()
    alldays = F.index[F.index >= start]
    for m, g in models.groupby("model"):
        mp = g.groupby("date").usd.sum()
        both = sp.index.intersection(mp.index)
        a = sp.reindex(alldays, fill_value=0.0); bb = mp.reindex(alldays, fill_value=0.0)
        lost = mp[mp < 0].index.intersection(sp.index)
        corr[m] = {"overlap_days": int(len(both)),
                   "corr_overlap_days": float(np.corrcoef(sp[both], mp[both])[0, 1]) if len(both) > 2 else None,
                   "corr_all_days_zero_filled": float(np.corrcoef(a, bb)[0, 1]),
                   "days_model_lost_and_spec_traded": int(len(lost)),
                   "spec_mean_usd_on_model_loss_days": float(sp[lost].mean()) if len(lost) else None,
                   "spec_total_usd_on_model_loss_days": float(sp[lost].sum()) if len(lost) else None}
    out["model_correlation"] = corr
    return out


def criteria(out, primary):
    a = out["t"] >= 2.0
    crit = [
        {"name": "a: event-level t >= 2.0 (full sample)" if primary else "a: t >= 3 or Holm p < 0.05 (set in summary)",
         "value": f"t={out['t']:.3f} (NW5 t={out['t_nw5']:.3f})", "pass": bool(a)},
        {"name": "b: mean net > 0 in Jun 2020 - Nov 2026",
         "value": f"{out['eras']['2020-06..2026-11']['mean_net_bp']:.3f} bp (n={out['eras']['2020-06..2026-11']['n']})",
         "pass": bool(out['eras']['2020-06..2026-11']['mean_net_bp'] > 0)},
        {"name": "c: mean net > 0 in >= 2/3 of counted 2-yr blocks (>=10 trades)",
         "value": f"{out['blocks_positive']}/{out['blocks_counted']}",
         "pass": bool(out['blocks_counted'] > 0 and out['blocks_positive'] >= 2 / 3 * out['blocks_counted'])},
        {"name": "d: mean net > C1 coin 95th pct", "value": f"{out['mean_net_bp']:.3f} vs {out['C1_coin_p95']:.3f} bp",
         "pass": bool(out['mean_net_bp'] > out['C1_coin_p95'])},
        {"name": "e: mean gross >= 1.5 x mean cost",
         "value": f"gross {out['mean_gross_bp']:.3f} vs 1.5*cost {1.5 * out['mean_cost_bp']:.3f} bp",
         "pass": bool(out['mean_gross_bp'] >= 1.5 * out['mean_cost_bp'])},
    ]
    return crit


if __name__ == "__main__":
    start = F.index[np.isfinite(F.z14) & np.isfinite(F.zo)][0]
    start15 = F.index[np.isfinite(F.z15) & np.isfinite(F.zo)][0]
    res = {}
    specs = {"S1": ("1430", True, "ge1", start), "S1-V1": ("1530", True, "ge1", start15),
             "S1-V2": ("1430", False, "ge1", start), "S1-C2": ("1430", True, "lt1", start)}
    for name, (w, f3, zg, st) in specs.items():
        df = run(w, f3, zg)
        df[[c for c in COLS if c in df.columns]].to_csv(f"{HERE}/trades_{name}.csv", index=False)
        out = report(df, name, st)
        out["sample_start"] = st.strftime("%Y-%m-%d")
        out["entry_bar_mismatch"] = int((df.entry_bar_N != tm(300 if w == "1430" else 360)).sum()
                                        + (df.entry_bar_E != tm(300 if w == "1430" else 360)).sum())
        if name != "S1-C2":
            out["criteria"] = criteria(out, name == "S1")
        res[name] = out
        print(name, out["n"], f"per_yr={out['per_year']:.1f} net={out['mean_net_bp']:.2f}bp gross={out['mean_gross_bp']:.2f} "
              f"cost={out['mean_cost_bp']:.2f} t={out['t']:.2f} $/tr={out['net_usd_per_trade']:.2f} stops={out['stop_exits']}")
    # eligible-day accounting for the deviations
    res["S1_signal_days_primary"] = F.index[signal_days("1430", True, "ge1")].strftime("%Y-%m-%d").tolist()
    with open(f"{HERE}/s1_results.json", "w") as f:
        json.dump(jsonable(res), f, indent=1)
