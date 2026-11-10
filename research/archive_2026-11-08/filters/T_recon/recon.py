"""Reconcile builders X and Y for T1-T4; re-evaluate the pass rule from the agreed per-trade decisions."""
import json, numpy as np, pandas as pd
from scipy import stats as sst
B = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/filters/"
OUT = B + "T_recon/"
book = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
orb = book[book.model == "opening_range"].reset_index()          # keep book row index in column 'index'
COLS = {"T1": [("c934_adj", "c934"), ("prev_ema20_adj", "ema20_prev"), ("trend", "trend")],
        "T2": [("open930_adj", "open930"), ("prev_close_adj", "prev_close1600"), ("gap", "gap")],
        "T3": [("fc_range", "fc_range"), ("fc_med20", "fc_med20")],
        "T4": [("on_range", "on_range"), ("on_med20", "on_med20")]}

def maxdd(s):
    eq = np.r_[0.0, np.cumsum(s)]
    return float((np.maximum.accumulate(eq) - eq).max())

def welch(a, b):
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    t = (a.mean() - b.mean()) / np.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return float(t), float(df), float(sst.t.sf(t, df))

def ev(keep, extra):
    o = orb.copy(); o["usd"] -= extra
    bk = book.copy(); bk["usd"] -= extra                          # 2 ticks: every trade of every model pays it
    K, R = o[keep], o[~keep]
    yr = o.date.dt.year
    days = sorted(o.date.unique())
    d0 = o.groupby("date").usd.sum().reindex(days, fill_value=0.0)
    d1 = K.groupby("date").usd.sum().reindex(days, fill_value=0.0)
    t, df, p = welch(K.usd.to_numpy(), R.usd.to_numpy())
    bdays = sorted(bk.date.unique())
    b0 = bk.groupby("date").usd.sum().reindex(bdays, fill_value=0.0)
    b1 = bk.drop(index=o.loc[~keep, "index"]).groupby("date").usd.sum().reindex(bdays, fill_value=0.0)
    r = dict(kept=int(keep.sum()), removed=int((~keep).sum()), share_removed=float((~keep).mean()),
             kept_usd=float(K.usd.sum()), removed_usd=float(R.usd.sum()),
             rem_10_17=float(R[yr[~keep] <= 2017].usd.sum()), rem_18_26=float(R[yr[~keep] >= 2018].usd.sum()),
             kept_pt=float(K.usd.mean()), rem_pt=float(R.usd.mean()), t=t, df=df, p1=p,
             dd0=maxdd(d0), dd1=maxdd(d1), w0=float(d0.min()), w1=float(d1.min()),
             book=dict(net0=float(b0.sum()), net1=float(b1.sum()), dd0=maxdd(b0), dd1=maxdd(b1),
                       w0=float(b0.min()), w1=float(b1.min())))
    r["a"] = r["removed_usd"] < 0 and r["rem_10_17"] < 0 and r["rem_18_26"] < 0
    r["b"] = t >= 2.5
    r["c"] = r["dd1"] <= r["dd0"] and r["w1"] >= r["w0"]
    return r, o

res, rows, agree = {}, [], {}
for f in COLS:
    x = pd.read_csv(B + f"T_X/{f}_decisions.csv"); y = pd.read_csv(B + f"T_Y/{f}_decisions.csv")
    assert (x.date.values == orb.date.dt.strftime("%Y-%m-%d").values).all() and (x.side.values == orb.side.values).all()
    assert (y.date.values == x.date.values).all() and np.allclose(x.usd, orb.usd) and np.allclose(y.usd, orb.usd)
    a = dict(decisions_equal=int((x.decision == y.decision).sum()), n=len(x))
    for cx, cy in COLS[f]:
        d = (x[cx] - y[cy]).abs()
        a[cx] = dict(max_abs_diff=float(np.nanmax(d)), nan_mismatch=int((x[cx].isna() != y[cy].isna()).sum()))
    agree[f] = a
    keep = (x.decision == "keep").to_numpy()
    r, o = ev(keep, 0.0); r2, o2 = ev(keep, 1.0)
    r["holm_rule_b"] = None; r["two_tick"] = r2; r["passed"] = r["a"] and r["b"] and r["c"]
    r2["passed"] = r2["a"] and r2["b"] and r2["c"]
    eras = {}
    for lab, y0, y1 in [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020),
                        ("2021-23", 2021, 2023), ("2024-26", 2024, 2026), ("2023-26", 2023, 2026)]:
        m = (o.date.dt.year >= y0) & (o.date.dt.year <= y1)
        eras[lab] = dict(n=int(m.sum()), removed=int((m & ~keep).sum()), kept_usd=float(o[m & keep].usd.sum()),
                         removed_usd=float(o[m & ~keep].usd.sum()),
                         removed_usd_2tick=float(o2[m & ~keep].usd.sum()))
    r["eras"] = eras
    for yv in sorted(o.date.dt.year.unique()):
        m = (o.date.dt.year == yv).to_numpy()
        rows.append(dict(filter=f, year=int(yv), trades=int(m.sum()), kept=int((m & keep).sum()),
                         removed=int((m & ~keep).sum()), share_removed=round((m & ~keep).sum() / m.sum(), 4),
                         kept_usd=o[m & keep].usd.sum(), removed_usd=o[m & ~keep].usd.sum(),
                         kept_usd_per_trade=round(o[m & keep].usd.mean(), 3),
                         removed_usd_per_trade=round(o[m & ~keep].usd.mean(), 3),
                         kept_usd_2tick=o2[m & keep].usd.sum(), removed_usd_2tick=o2[m & ~keep].usd.sum()))
    res[f] = r
# Holm (report): one-sided p, step-down over 4
ps = np.array([res[f]["p1"] for f in COLS]); order = np.argsort(ps); run = 0
for rank, j in enumerate(order):
    run = max(run, min(1.0, (4 - rank) * ps[j])); res[list(COLS)[j]]["p_holm"] = float(run)
pd.DataFrame(rows).to_csv(OUT + "per_year.csv", index=False)
json.dump(dict(agreement=agree, results=res), open(OUT + "summary.json", "w"), indent=1, default=float)
for f in COLS:
    r = res[f]; t2 = r["two_tick"]
    print(f, agree[f]["decisions_equal"], "/", agree[f]["n"],
          f"kept {r['kept']} ${r['kept_usd']:.1f} ({r['kept_pt']:.2f}/tr) removed {r['removed']} ({r['share_removed']:.1%}) "
          f"${r['removed_usd']:.1f} ({r['rem_pt']:.2f}/tr) 10-17 {r['rem_10_17']:.1f} 18-26 {r['rem_18_26']:.1f} "
          f"t {r['t']:.3f} p {r['p1']:.4f} holm {r['p_holm']:.3f} DD {r['dd0']}->{r['dd1']} worst {r['w0']}->{r['w1']} "
          f"a{r['a']} b{r['b']} c{r['c']} PASS {r['passed']}")
    print("   book", r["book"])
    print("   2tick", {k: t2[k] for k in ("removed_usd", "rem_10_17", "rem_18_26", "t", "dd0", "dd1", "w0", "w1", "a", "b", "c", "passed")}, t2["book"],
          "model", t2["kept_usd"] + t2["removed_usd"], "->", t2["kept_usd"])
    print("   eras", {k: (v['removed'], round(v['removed_usd'], 1)) for k, v in r["eras"].items()})
print(json.dumps(agree, indent=0)[:1500])
