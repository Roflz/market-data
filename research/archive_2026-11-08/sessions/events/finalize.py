import json, numpy as np, pandas as pd
from scipy.stats import norm
O = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events/"
a = pd.read_csv(O + "event_continuation_all_gap5.csv")
g15 = pd.read_csv(O + "event_continuation_all_gap15.csv")[["event", "market", "k", "h", "n_days", "t_nw"]]
p = pd.read_csv(O + "placebo_clock_times.csv")
N_ALL = len(a); N_PRE = a.groupby(["event", "market"]).ngroups
TH_ALL = norm.ppf(1 - 0.025 / N_ALL); TH_PRE = norm.ppf(1 - 0.025 / N_PRE)
a = a.merge(g15.rename(columns={"n_days": "n_days_gap15", "t_nw": "t_nw_gap15"}), on=["event", "market", "k", "h"])
a["is_prespecified"] = (a.k == 15) & (a.h == 60)
best_idx = a.groupby(["event", "market"]).t_nw.apply(lambda s: s.abs().idxmax())
a["is_best_in_scan"] = a.index.isin(best_idx.values)
pb = p.groupby(["event", "market"]).t_nw.apply(lambda s: s.abs().max()).to_numpy()
a["placebo_pct_of_abs_t_vs_best_of_9"] = a.t_nw.abs().apply(lambda v: (pb < v).mean())
a["threshold_abs_t"] = np.where(a.is_prespecified, TH_PRE, TH_ALL)
a["bonferroni_p"] = np.minimum(1, 2 * norm.sf(a.t_nw.abs()) * np.where(a.is_prespecified, N_PRE, N_ALL))

def verdict(r):
    if not np.isfinite(r.t_nw) or abs(r.t_nw) < r.threshold_abs_t:
        return "nothing"
    s = np.sign(r.t_nw)
    if np.sign(r.t_2010_2017) != s or np.sign(r.t_2018_2026) != s or np.sign(r.t_nw_wins) != s:
        return "nothing"
    return "continuation" if s > 0 else "reversal"
a["verdict"] = a.apply(verdict, axis=1)

def dominant(s):
    parts = [x.split("(") for x in s.split(";")]
    return [(t, int(c.rstrip(")"))) for t, c in parts]

def clock(t, add):
    h, m = map(int, t.split(":")); m0 = (h * 60 + m + add) % 1440
    return f"{m0 // 60:02d}:{m0 % 60:02d}"

def window(r, a0, a1, zone_col, zone):
    ts = dominant(r[zone_col])
    main = ts[0][0]
    s = f"{clock(main, a0)}-{clock(main, a1)} {zone}"
    if len(ts) > 1:
        s += " (" + ", ".join(f"{clock(t, a0)}-{clock(t, a1)} on {c}d" for t, c in ts[1:]) + ")"
    return s

rows = []
for (ev, mk), g in a.groupby(["event", "market"], sort=False):
    for lab, r in (("pre-specified k15/h60", g[g.is_prespecified].iloc[0]), ("best of 9 (k,h) by |NW t|", g.loc[g.t_nw.abs().idxmax()])):
        k, h = int(r.k), int(r.h)
        trunc = f"; cut at session stop on {r.frac_follow_truncated:.0%} of days" if r.frac_follow_truncated > 0 else ""
        rows.append(dict(
            event=f"{ev} [{lab}]",
            market=mk,
            impulse_window=f"{k}m: {window(r, 0, k, 'et_times', 'ET')}; starts {'/'.join(t for t, _ in dominant(r.denver_times))} Denver MST/MDT, {'/'.join(t for t, _ in dominant(r.arizona_times))} Arizona MST",
            follow_window=f"{h}m: {window(r, k, k + h, 'et_times', 'ET')}{trunc}",
            slope=round(float(r.slope), 4), t_newey_west=round(float(r.t_nw), 2),
            t_2010_2017=round(float(r.t_2010_2017), 2) if np.isfinite(r.t_2010_2017) else 0.0,
            t_2018_2026=round(float(r.t_2018_2026), 2),
            follow_rule_net_usd_per_trade=round(float(r.follow_net_usd), 2),
            fade_rule_net_usd_per_trade=round(float(r.fade_net_usd), 2),
            n_days=int(r.n_days), verdict=r.verdict))
json.dump(rows, open(O + "events_struct.json", "w"), indent=1)
cols = ["event", "market", "k", "h", "is_prespecified", "is_best_in_scan", "n_days", "n_2010_2017", "n_2018_2026", "first", "last",
        "slope", "t_nw", "slope_2010_2017", "t_2010_2017", "slope_2018_2026", "t_2018_2026", "slope_wins", "t_nw_wins",
        "t_nw_gap15", "n_days_gap15", "corr", "hit_rate_follow", "follow_gross_usd", "follow_net_usd", "fade_net_usd",
        "t_follow_gross_nw", "follow_net_usd_2010_2017", "follow_net_usd_2018_2026", "frac_follow_truncated",
        "threshold_abs_t", "bonferroni_p", "placebo_pct_of_abs_t_vs_best_of_9", "verdict",
        "abs_impulse_pts_2024_26", "abs_impulse_ratio_vs_hour_before", "et_times", "denver_times", "arizona_times"]
a[cols].to_csv(O + "event_continuation_results.csv", index=False, float_format="%.5g")
print("N_ALL", N_ALL, "N_PRE", N_PRE, "TH", TH_ALL, TH_PRE, "verdicts", a.verdict.value_counts().to_dict())
print("min bonferroni p", a.bonferroni_p.min())
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 200)
print(pd.DataFrame(rows)[["event", "market", "t_newey_west", "t_2010_2017", "t_2018_2026", "follow_rule_net_usd_per_trade", "fade_rule_net_usd_per_trade", "n_days"]].to_string(index=False))
print(pd.DataFrame(rows).iloc[[0, 1, 20, 21]][["impulse_window", "follow_window"]].to_string())
sel = a[a.is_best_in_scan][["event", "market", "k", "h", "follow_net_usd_2010_2017", "follow_net_usd_2018_2026", "t_follow_gross_nw", "t_nw_gap15", "placebo_pct_of_abs_t_vs_best_of_9"]]
print(sel.round(2).to_string(index=False))
