"""Synthetic checks for importance.py: a planted feature ranks first (MDA log loss, MDA $, SFI), near-duplicate
planted features are clustered together and share their importance as a cluster, purging and holdout refusal."""
import numpy as np
import pandas as pd

import importance as im
import walkforward as wf

ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok &= bool(cond)


FOLDS = wf.make_folds(test_years=(2012, 2013, 2014), h1_2025=False)


def synth(n=14000, seed=1, dup=False):
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2008-01-01", "2014-12-31")
    t = days[rng.integers(0, len(days), n)] + pd.to_timedelta(rng.integers(10, 15, n), unit="h")
    t = pd.DatetimeIndex(np.sort(t.to_numpy()))
    df = pd.DataFrame({"t": t, "t_end_1.5": t + pd.Timedelta(hours=2), "d": rng.choice([-1, 1], n), "market": "NQ"})
    z = rng.normal(size=n)
    b = rng.normal(size=n)
    if dup:                                            # the signal is carried by 3 near-identical columns
        for k in range(3):
            df[f"a{k + 1}"] = z + 0.05 * rng.normal(size=n)
        df["b"] = b
        logit = -0.2 + 1.5 * z + 0.6 * b
    else:
        df["sig"] = z
        logit = -0.2 + 1.2 * z
    for k in range(5):
        df[f"n{k + 1}"] = rng.normal(size=n)
    df.loc[rng.random(n) < 0.02, "n1"] = np.nan        # a few missing values
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df["y_1.5"] = y
    df["pnl_usd_1.5"] = np.where(y == 1, 15.0, -10.0) - 1.0 + rng.normal(0, 1, n)
    return df


# ------------------------------------------------------------------ single planted feature
df = synth()
feats = ["sig"] + [f"n{k + 1}" for k in range(5)]
S = im.prepare(df, feats, signed=[], mirror={})
fits, skipped = im.fit_folds(S, "logit", folds=FOLDS)
check("three folds fitted", len(fits) == 3)
ok_purge = all((S["t_end"][f.tr] <= (pd.Timestamp(f.name + "-01-01") - wf.PURGE).to_datetime64()).all() and
               (S["t"][f.tr] < pd.Timestamp(f.name + "-01-01")).all() for f in fits)
check("training rows purged (t_end <= test start - 1 day, t before the test)", ok_purge)
groups = {f: [f] for f in feats}
M = im.mda(S, fits, groups, feats, n_rep=3, seed=0)
sm = im.summarize(M, "group", ["mda_ll", "mda_usd", "mda_auc"])
print(sm[["mda_ll_mean", "mda_usd_mean", "mda_auc_mean"]].round(4).to_string())
check("MDA log loss: planted feature ranks first", im.rank(sm, "mda_ll_mean").index[0] == "sig")
check("MDA $ per kept trade: planted feature ranks first", im.rank(sm, "mda_usd_mean").index[0] == "sig")
check("MDA log loss: planted >= 10x every noise feature",
      sm.loc["sig", "mda_ll_mean"] > 10 * sm.drop("sig")["mda_ll_mean"].abs().max())
check("MDA: planted feature helps in every fold", sm.loc["sig", "mda_ll_pos"] == 1.0)
SF = im.sfi(S, fits, feats)
ss = im.summarize(SF, "feature", ["sfi_ll_logit1", "sfi_ll_bin1"])
print(ss[["sfi_ll_logit1_mean", "sfi_ll_bin1_mean"]].round(4).to_string())
check("SFI logit: planted feature ranks first", im.rank(ss, "sfi_ll_logit1_mean").index[0] == "sig")
check("SFI bins: planted feature ranks first", im.rank(ss, "sfi_ll_bin1_mean").index[0] == "sig")
check("SFI: noise features do not help (logit sfi <= 0.002 nats)", (ss.drop("sig")["sfi_ll_logit1_mean"] < 0.002).all())
auc_sig = SF.loc[SF.feature == "sig", "auc_logit1"].mean()
check(f"SFI AUC of the planted feature well above 0.5 ({auc_sig:.3f})", auc_sig > 0.7)
B = im.base_table(S, fits, n_random=50)
check("full model beats all events and random skip in $ per trade",
      (B.usd_kept > B.all_usd).all() and (B.usd_kept > B.random_p95).all())

# ------------------------------------------------------------------ duplicated planted features
dd = synth(seed=2, dup=True)
feats2 = ["a1", "a2", "a3", "b"] + [f"n{k + 1}" for k in range(5)]
S2 = im.prepare(dd, feats2, signed=[], mirror={})
cl, info = im.correlation_clusters(S2["Xo"], min_k=2, max_k=8)
print("clusters:", cl, "silhouette", round(info["silhouette"], 3))
dup_cluster = [k for k, v in cl.items() if "a1" in v]
check("the three duplicates form one cluster, alone", len(dup_cluster) == 1 and
      sorted(cl[dup_cluster[0]]) == ["a1", "a2", "a3"])
check("every other feature is a singleton", all(len(v) == 1 for k, v in cl.items() if k != dup_cluster[0]))
fits2, _ = im.fit_folds(S2, "logit", folds=FOLDS)
M1 = im.mda(S2, fits2, {f: [f] for f in feats2}, feats2, n_rep=3, seed=0)
M2 = im.mda(S2, fits2, cl, feats2, n_rep=3, seed=0)
s1 = im.summarize(M1, "group", ["mda_ll", "mda_usd"])
s2 = im.summarize(M2, "group", ["mda_ll", "mda_usd"])
print(s1[["mda_ll_mean", "mda_usd_mean"]].round(4).to_string())
print(s2[["mda_ll_mean", "mda_usd_mean"]].round(4).to_string())
c = dup_cluster[0]
check("clustered MDA: the duplicate cluster ranks first", im.rank(s2, "mda_ll_mean").index[0] == c)
mem = s1.loc[["a1", "a2", "a3"], "mda_ll_mean"]
check("cluster MDA exceeds 2x the best single member's MDA (importance was split by substitution)",
      s2.loc[c, "mda_ll_mean"] > 2 * mem.max())
check("the members share the importance (each > 0, none carries more than half of the cluster's)",
      mem.min() > 0 and mem.max() < 0.5 * s2.loc[c, "mda_ll_mean"])
check("clustered MDA $: the duplicate cluster ranks first", im.rank(s2, "mda_usd_mean").index[0] == c)
check("noise singletons ~0 in clustered MDA (< 5% of the duplicate cluster)",
      s2.drop([c, [k for k, v in cl.items() if v == ["b"]][0]])["mda_ll_mean"].abs().max()
      < 0.05 * s2.loc[c, "mda_ll_mean"])

# ------------------------------------------------------------------ holdout refusal
try:
    im.fit_folds(S, "logit", folds=[wf.Fold("2025", pd.Timestamp("2025-01-01"), pd.Timestamp("2026-01-01"))])
    check("holdout fold refused", False)
except wf.HoldoutError:
    check("holdout fold refused", True)
check("families map", im.family_of("pat_hammer") == "candle pattern" and im.family_of("x_ES_ret") == "cross-market"
      and im.family_of("dist_swhi_5") == "swing structure" and im.family_of("tod_open") == "time of day")

print("ALL PASS" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
