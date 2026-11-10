"""Evaluate every S1/S2/S3 rule + variant against the pre-registered criteria; write summary.json. Builder X."""
import json, os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import *
import load

st13 = pd.read_pickle(os.path.join(HERE, "s1s3_state.pkl"))
st2 = pd.read_pickle(os.path.join(HERE, "s2_state.pkl"))
T = st13["trades"]
dsN = pd.read_pickle("data/daily_sessions_NQ.pkl"); dsE = pd.read_pickle("data/daily_sessions_ES.pkl")
cash_days = dsN.index[dsN.cash_day & dsE.cash_day]
cm = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
cm_daily = cm.groupby(["model", "date"]).usd.sum().unstack(0)

def c1_random(df, seed=SEED, nrep=NREP):
    rng = np.random.default_rng(seed)
    g = df.gross_bp.to_numpy(); c = df.cost_bp.to_numpy()
    sg = np.where(df.side.str.startswith("long").to_numpy(), 1, -1)
    g_long = g * sg                       # gross if long NQ/short ES
    signs = rng.choice([-1, 1], size=(nrep, len(df)))
    means = (signs * g_long[None, :] - c[None, :]).mean(1)
    return {"p95": float(np.percentile(means, 95)), "mean": float(means.mean()),
            "share_ge_real": float((means >= df.net_bp.mean()).mean())}

def blocks_pass(blocks):
    cnt = [v for v in blocks.values() if v["counted"]]
    pos = sum(v["mean_net_bp"] > 0 for v in cnt)
    return pos, len(cnt), (len(cnt) > 0 and pos >= 2 / 3 * len(cnt))

def cost2026(df):
    c = df[df.date.dt.year == 2026].cost_bp.mean()
    x = df.gross_bp - c
    return {"cost_bp_2026": float(c), "mean_net_bp_at_2026_cost": float(x.mean()), "t": float(tstat(x)),
            "after_2020_mean_net_bp_at_2026_cost": float(x[df.date >= "2020-06-01"].mean())}

def corr_models(daily, start, end):
    """daily: Series date->usd for this rule (zero on cash days without a position)."""
    idx = cash_days[(cash_days >= start) & (cash_days <= end)]
    s = daily.reindex(idx).fillna(0.0)
    out = {}
    for m in cm_daily.columns:
        mm = cm_daily[m].reindex(idx)
        both = s[(s != 0) & mm.notna()]
        lost = mm[mm < 0].index
        sl = daily.reindex(lost).dropna()
        out[m] = {"corr_zero_filled": float(np.corrcoef(s, mm.fillna(0.0))[0, 1]),
                  "corr_overlap_days": float(np.corrcoef(s[both.index], mm[both.index])[0, 1]) if len(both) > 2 else None,
                  "n_overlap_days": int(len(both)),
                  "on_model_loss_days": {"n": int((sl != 0).sum()), "mean_usd": float(sl[sl != 0].mean()) if (sl != 0).any() else None,
                                         "total_usd": float(sl.sum())}}
    return out

def trade_daily(df):
    return df.groupby("date").net_usd.sum()

def bucket_stats(df, key, bins, labels):
    b = pd.cut(key, bins=bins, labels=labels, right=False)
    return {str(k): {"n": int(len(g)), "mean_net_bp": float(g.net_bp.mean()) if len(g) else None,
                     "mean_gross_bp": float(g.gross_bp.mean()) if len(g) else None, "usd": float(g.net_usd.sum())}
            for k, g in df.groupby(b, observed=False)}

def sub(df, mask):
    g = df[mask]
    return {"n": int(len(g)), "mean_net_bp": float(g.net_bp.mean()) if len(g) else None,
            "mean_gross_bp": float(g.gross_bp.mean()) if len(g) else None, "usd": float(g.net_usd.sum()),
            "t": float(tstat(g.net_bp)) if len(g) > 2 else None}

R = {}
# ---------------- S1 family ----------------
for nm in ("S1", "S1-V1", "S1-V2"):
    df = T[nm].copy()
    s = summarize(df); s["nw_t5"] = float(nw_t(df.net_bp, 5)); s["era"] = era_stats(df)
    s["C1"] = c1_random(df)
    s["C3_beta_net_bp_on_ES_ret_bp"] = float(np.polyfit(df.es_ret_entry_to_close_bp, df.net_bp, 1)[0])
    s["C3_beta_gross_bp_on_ES_ret_bp"] = float(np.polyfit(df.es_ret_entry_to_close_bp, df.gross_bp, 1)[0])
    s["z_buckets"] = bucket_stats(df, df.z_entry.abs(), [1, 1.5, 2, np.inf], ["1-1.5", "1.5-2", ">=2"])
    s["stop_exits"] = int((df.exit_reason == "stop").sum())
    s["expiry_fridays"] = sub(df, df.expiry_friday); s["non_expiry"] = sub(df, ~df.expiry_friday)
    s["costs_held_at_2026_bps"] = cost2026(df)
    s["corr_existing_models"] = corr_models(trade_daily(df), df.date.min(), df.date.max())
    R[nm] = s
c2 = T["S1-C2"]; R["S1"]["C2_absz_lt_1"] = {**summarize(c2), "era": era_stats(c2)}
for k in ("blocks", "by_year"):
    R["S1"]["C2_absz_lt_1"].pop(k)
R["S1"]["C2_absz_lt_1"]["mean_net_bp_S1_minus_C2"] = R["S1"]["mean_net_bp"] - R["S1"]["C2_absz_lt_1"]["mean_net_bp"]

# ---------------- S3 family ----------------
for nm in ("S3", "S3-V1", "S3-V2"):
    df = T[nm].copy()
    s = summarize(df); s["nw_t5"] = float(nw_t(df.net_bp, 5)); s["era"] = era_stats(df)
    s["C1"] = c1_random(df)
    s["C2_placebo_1430_1500"] = {"mean_net_bp": float(df.placebo_net_bp.mean()), "mean_gross_bp": float(df.placebo_gross_bp.mean()),
                                 "t": float(tstat(df.placebo_net_bp))}
    s["absR_buckets_RNQ"] = bucket_stats(df, df.R_NQ.abs() * 100, [1, 1.5, 2, 3, np.inf], ["1-1.5%", "1.5-2%", "2-3%", ">=3%"])
    s["vix_tercile"] = {str(int(k)): sub(df, df.vix_tercile == k) for k in (1, 2, 3)}
    s["fomc_days"] = sub(df, df.fomc); s["cpi_days"] = sub(df, df.cpi); s["non_fomc_cpi"] = sub(df, ~df.fomc & ~df.cpi)
    s["outright_last_half_hour_dir_bp"] = {"NQ_mean": float(df.NQ_outright_lasthalf_bp_dir.mean()), "NQ_t": float(tstat(df.NQ_outright_lasthalf_bp_dir)),
                                           "ES_mean": float(df.ES_outright_lasthalf_bp_dir.mean()), "ES_t": float(tstat(df.ES_outright_lasthalf_bp_dir)),
                                           "NQ_minus_b_ES_mean": float((df.NQ_outright_lasthalf_bp_dir - df.b * df.ES_outright_lasthalf_bp_dir).mean())}
    s["two_sided_note"] = "negative significant mean would be fade evidence only, not a pass"
    s["costs_held_at_2026_bps"] = cost2026(df)
    s["corr_existing_models"] = corr_models(trade_daily(df), df.date.min(), df.date.max())
    s["expiry_fridays"] = sub(df, df.expiry_friday)
    R[nm] = s

# ---------------- S2 family ----------------
o = load.get()
days = o["NQ"]["days"]
early = (dsN.early_close | dsE.early_close).to_numpy()
slot = np.where(early, 209, 389)
NQc = pd.DataFrame(o["NQ"]["Close"]).ffill(axis=1).to_numpy()[np.arange(len(days)), slot]
ESc = pd.DataFrame(o["ES"]["Close"]).ffill(axis=1).to_numpy()[np.arange(len(days)), slot]
r = pd.read_csv("data/RTY_fut_1h.csv")
ts = pd.to_datetime(r.ts_event, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
r["date"] = ts.dt.normalize(); r["h"] = ts.dt.hour
RTYc = pd.Series(np.nan, index=days)
for hh, msk in ((15, ~early), (12, early)):
    x = r[r.h == hh].set_index("date").Close
    x = x[~x.index.duplicated()]
    RTYc[msk] = x.reindex(days[msk]).to_numpy()
cidx = pd.Series(np.arange(len(days)), index=days)
cash_mask = (dsN.cash_day & dsE.cash_day).to_numpy()

def s2_daily(S, lead):
    """Daily mark-to-market $ of the S2 segments (cash-session closes), costs charged on entry day."""
    Lc = NQc if lead == "NQ" else RTYc.to_numpy()
    mult = 2.0 if lead == "NQ" else 5.0
    out = {}
    for _, g in S.iterrows():
        i0, i1 = cidx[pd.Timestamp(g.entry_date)], cidx[pd.Timestamp(g.exit_date)]
        ss = [i for i in range(i0, i1 + 1) if cash_mask[i]]
        pL, pE = g.lead_entry, g.ES_entry
        for j, i in enumerate(ss):
            last = (j == len(ss) - 1)
            eL, eE = (g.lead_exit, g.ES_exit) if last else (Lc[i], ESc[i])
            v = g.d * (g.n_lead * mult * (eL - pL) - g.n_ES * 5 * (eE - pE))
            if j == 0:
                v -= g.cost_usd
            out[days[i]] = out.get(days[i], 0.0) + v
            pL, pE = eL, eE
    return pd.Series(out).sort_index()

for nm in ("S2", "S2-V1", "S2-V2"):
    S, Mo = st2["out"][nm]
    Mo = Mo.copy(); Mo["date"] = pd.to_datetime(Mo.date)
    s = summarize(Mo); s["nw_t3"] = float(nw_t(Mo.net_bp, 3)); s["era"] = era_stats(Mo, split="2016-01-01")
    s["era_2020"] = era_stats(Mo)
    # C1 circular shift
    d = Mo.d.to_numpy(); gl = Mo.gross_long_bp.to_numpy(); c = Mo.cost_bp.to_numpy(); n = len(d)
    shifts = np.array([np.mean(np.roll(d, k) * gl - c) for k in range(12, n - 12 + 1)])
    s["C1_circular"] = {"n_shifts": int(len(shifts)), "p95": float(np.percentile(shifts, 95)), "mean": float(shifts.mean()),
                        "share_ge_real": float((shifts >= Mo.net_bp.mean()).mean())}
    s["C2_static_long_spread"] = {"mean_net_bp": float(np.mean(gl - c)), "t": float(tstat(gl - c))}
    # drop best sign regime
    reg = (pd.Series(d).diff().fillna(0) != 0).cumsum().to_numpy()
    rs = pd.Series(Mo.net_bp.to_numpy()).groupby(reg).sum()
    best = rs.idxmax()
    keep = reg != best
    s["drop_best_regime"] = {"n_regimes": int(len(rs)), "best_regime_months": int((~keep).sum()),
                             "best_regime_start": str(Mo.hold_month[~keep].iloc[0]), "best_regime_sum_bp": float(rs.max()),
                             "mean_net_bp_after_drop": float(Mo.net_bp[keep].mean())}
    s["share_long_months"] = float((d > 0).mean())
    s["sign_changes"] = int((np.diff(d) != 0).sum())
    s["roll_segments"] = int((S.exit_reason == "roll").sum())
    s["costs_held_at_2026_bps"] = cost2026(Mo)
    lead = "NQ" if nm != "S2-V2" else "RTY"
    dd = s2_daily(S, lead)
    s["daily_mtm_check_total_usd"] = float(dd.sum())
    s["corr_existing_models"] = corr_models(dd, Mo.date.min(), pd.Timestamp(S.exit_date.max()))
    s["avg_micros_held"] = {"lead": float(S.n_lead.mean()), "MES": float(S.n_ES.mean())}
    R[nm] = s
R["S2"]["index_diagnostics"] = st2["diag"]; R["S2"]["live_vol_scaling_reported_only"] = st2["live"]

# ---------------- criteria, Holm ----------------
fam = ["S1", "S1-V1", "S1-V2", "S2", "S2-V1", "S2-V2", "S3", "S3-V1", "S3-V2"]
pv = {k: p_two(R[k]["t"], R[k]["n"]) for k in fam}
hp = holm(pv)
for k in fam:
    R[k]["p_two_sided"] = pv[k]; R[k]["holm_p"] = hp[k]

def sig_crit(k, primary):
    s = R[k]
    if k.startswith("S2"):
        tt = min(s["t"], s["nw_t3"])
        val = f"t={s['t']:.2f}, NW3 t={s['nw_t3']:.2f}"
    else:
        tt = s["t"]; val = f"t={s['t']:.2f} (NW5 t={s['nw_t5']:.2f})"
    if primary:
        return {"name": "(a) t >= 2.0 full sample" + (" (plain and NW3)" if k.startswith("S2") else ""), "value": val, "pass": bool(tt >= 2.0)}
    ok = (s["mean_net_bp"] > 0) and (tt >= 3.0 or s["holm_p"] < 0.05)
    return {"name": "(a-variant) t >= 3 or Holm p < 0.05 (9 tests), mean > 0", "value": val + f", Holm p={s['holm_p']:.3g}", "pass": bool(ok)}

for k in fam:
    s = R[k]; primary = k in ("S1", "S2", "S3")
    cr = [sig_crit(k, primary)]
    pos, cnt, bp_ = blocks_pass(s["blocks"])
    if k.startswith("S1"):
        aft = s["era"]["after"]["mean_net_bp"]
        cr.append({"name": "(b) mean net > 0 Jun 2020 - Nov 2026", "value": f"{aft:.3f} bp (n={s['era']['after']['n']})", "pass": bool(aft > 0)})
        cr.append({"name": "(c) mean net > 0 in >= 2/3 of counted 2-yr blocks", "value": f"{pos}/{cnt}", "pass": bool(bp_)})
        cr.append({"name": "(d) mean net > C1 95th pct", "value": f"{s['mean_net_bp']:.3f} vs {s['C1']['p95']:.3f}", "pass": bool(s['mean_net_bp'] > s['C1']['p95'])})
        cr.append({"name": "(e) mean gross >= 1.5 x mean cost", "value": f"{s['mean_gross_bp']:.3f} vs {1.5 * s['mean_cost_bp']:.3f}", "pass": bool(s['mean_gross_bp'] >= 1.5 * s['mean_cost_bp'])})
    elif k.startswith("S3"):
        aft = s["era"]["after"]["mean_net_bp"]
        cr.append({"name": "(b) mean net > 0 Jun 2020 - Nov 2026", "value": f"{aft:.3f} bp (n={s['era']['after']['n']})", "pass": bool(aft > 0)})
        cr.append({"name": "(c) mean net > 0 in >= 2/3 of counted 2-yr blocks", "value": f"{pos}/{cnt}", "pass": bool(bp_)})
        cr.append({"name": "(d) mean net > C1 95th pct", "value": f"{s['mean_net_bp']:.3f} vs {s['C1']['p95']:.3f}", "pass": bool(s['mean_net_bp'] > s['C1']['p95'])})
        pl = s["C2_placebo_1430_1500"]["mean_net_bp"]
        cr.append({"name": "(e) mean net > C2 placebo (14:30-15:00) mean net", "value": f"{s['mean_net_bp']:.3f} vs {pl:.3f}", "pass": bool(s['mean_net_bp'] > pl)})
        cr.append({"name": "(f) mean gross >= 1.5 x mean cost", "value": f"{s['mean_gross_bp']:.3f} vs {1.5 * s['mean_cost_bp']:.3f}", "pass": bool(s['mean_gross_bp'] >= 1.5 * s['mean_cost_bp'])})
    else:
        aft = s["era"]["after"]["mean_net_bp"]
        cr.append({"name": "(b) mean net > 0 Jan 2016 - Nov 2026", "value": f"{aft:.3f} bp (n={s['era']['after']['n']})", "pass": bool(aft > 0)})
        cr.append({"name": "(c) mean net > 0 in >= 2/3 of counted 2-yr blocks (>=10 months)", "value": f"{pos}/{cnt}", "pass": bool(bp_)})
        cr.append({"name": "(d1) C1 mean net > 95th pct of circular shifts", "value": f"{s['mean_net_bp']:.3f} vs {s['C1_circular']['p95']:.3f}", "pass": bool(s['mean_net_bp'] > s['C1_circular']['p95'])})
        cr.append({"name": "(d2) C2 mean net > static long-spread mean net", "value": f"{s['mean_net_bp']:.3f} vs {s['C2_static_long_spread']['mean_net_bp']:.3f}", "pass": bool(s['mean_net_bp'] > s['C2_static_long_spread']['mean_net_bp'])})
        db = s["drop_best_regime"]["mean_net_bp_after_drop"]
        cr.append({"name": "(e) mean net > 0 after dropping best sign regime", "value": f"{db:.3f}", "pass": bool(db > 0)})
    s["criteria"] = cr
    s["passed"] = bool(all(c["pass"] for c in cr))

def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    return x
json.dump(clean(R), open(os.path.join(HERE, "summary.json"), "w"), indent=1)
for k in fam:
    s = R[k]
    print(f"{k:6s} n={s['n']:4d} /yr={s['per_year']:.1f} net$={s['net_usd_per_trade']:.2f} tot$={s['total_usd']:.0f} "
          f"gross={s['mean_gross_bp']:.2f} cost={s['mean_cost_bp']:.2f} net={s['mean_net_bp']:.2f} t={s['t']:.2f} holm={s['holm_p']:.3f} PASS={s['passed']}")
    for c in s["criteria"]:
        print("     ", c["pass"], c["name"], "|", c["value"])
