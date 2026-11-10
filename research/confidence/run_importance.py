"""
Feature importance of the MNQ (NQ) v1 entry model: MDA (single feature, correlation cluster, feature family) and SFI
under the purged walk-forward (definitions: importance.py). Never touches the 2025-07-01+ holdout.

    python3 run_importance.py [--sym NQ] [--models logit,gbm] [--n-rep 3] [--report-only]

Outputs (out/):
    importance_<SYM>.csv        one row per (model, level, name): level = feature / cluster / family; MDA mean, sd, t,
                                share of folds > 0 for log loss, AUC, $ per kept trade, total $; SFI (features only,
                                model-free: logit1 and bin1) mean / t / AUC; family, cluster, members.
    importance_<SYM>_folds.csv  the same per fold (= per test year), long format.
    importance_<SYM>_base.csv   per model and fold: the full model's OOS scores vs all events and random skip.
    importance_<SYM>.md         plain-English ranked list.
Each model run is logged to out/trials.csv (module 'entry-importance').

Run: cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:. python3 run_importance.py
"""
import argparse
import json
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd

import importance as im
import run_pipeline as rp
import walkforward as wf

MIN_AVAIL_MB = 7000
SEED = 0


def say(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def mem_wait(min_mb=MIN_AVAIL_MB):
    """Block until MemAvailable (= `free -m` 'available') >= min_mb."""
    while True:
        with open("/proc/meminfo") as fh:
            avail = int(next(l for l in fh if l.startswith("MemAvailable")).split()[1]) // 1024
        if avail >= min_mb:
            return avail
        say(f"available {avail} MB < {min_mb} MB, waiting 60s")
        time.sleep(60)


def out(name):
    return os.path.join(rp.OUT, name)


def upsert_model(name, df, model):
    p = out(name)
    if os.path.exists(p):
        old = pd.read_csv(p)
        df = pd.concat([old[old.model != model], df], ignore_index=True)
    df.to_csv(p, index=False)


# ============================================================================================ compute
def run_model(S, feats, clusters, fams, model, n_rep, sfi_df):
    t0 = time.time()
    mem_wait()
    say(f"{model}: fitting {len(feats)} features on the walk-forward folds")
    fits, skipped = im.fit_folds(S, model, verbose=True)
    base = im.base_table(S, fits, n_random=rp.N_RANDOM, seed=SEED)
    say(f"{model}: MDA ({len(feats)} features, {len(clusters)} clusters, {len(fams)} families, {n_rep} shuffles)")
    levels = (("feature", {f: [f] for f in feats}), ("cluster", clusters), ("family", fams))
    longs, sums = [], []
    for level, groups in levels:
        L = im.mda(S, fits, groups, feats, n_rep=n_rep, seed=SEED, verbose=False)
        L.insert(0, "level", level)
        longs.append(L)
        sm = im.summarize(L, "group", ["mda_ll", "mda_auc", "mda_usd", "mda_tot"])
        sm.insert(0, "level", level)
        sm["members"] = ["|".join(groups[g]) for g in sm.index]
        sm["n_cols"] = [len(groups[g]) for g in sm.index]
        sums.append(sm)
    long = pd.concat(longs, ignore_index=True)
    summ = pd.concat(sums).rename_axis("name").reset_index()
    if sfi_df is None:
        say("SFI (single-feature logit and bins, model-free)")
        sfi_df = im.sfi(S, fits, feats, verbose=False)
    rt = time.time() - t0
    # ------------------------------------------------------------- trials.csv
    tot_k = int(base.n_kept.sum())
    usd_tot = float(base.tot_kept.sum())
    yrs = float(base.years.sum())
    oos_p = np.concatenate([f.p for f in fits]); oos_y = np.concatenate([S["y"][f.test] for f in fits])
    from sklearn.metrics import roc_auc_score
    top = summ[summ.level == "cluster"].sort_values("mda_ll_mean", ascending=False).head(3)
    rp.log_trial(module="entry-importance", scope=S["sym"], model=model,
                 target="y_1.5", n_folds=len(fits), oos_rows=int(base.n_test.sum()),
                 oos_auc=round(float(roc_auc_score(oos_y, oos_p)), 4), oos_kept=tot_k,
                 oos_keep_share=round(tot_k / float(base.n_test.sum()), 4), oos_usd_total=round(usd_tot, 2),
                 oos_usd_per_trade=round(usd_tot / tot_k, 3) if tot_k else np.nan,
                 oos_usd_per_year=round(usd_tot / yrs, 1),
                 baseline_usd_per_trade=round(float(base.all_total.sum() / base.n_test.sum()), 3), runtime_s=round(rt),
                 parameters=json.dumps(dict(features="v1 entry (feature_list('entry','NQ'))", n_features=len(feats),
                                            n_clusters=len(clusters), n_families=len(fams), n_rep=n_rep, seed=SEED,
                                            cluster_cut="avg-linkage 1-|corr|, dist<=0.7, k clipped to [15,30]",
                                            permutation="joint within test fold", folds="2013..2024 + 2025H1",
                                            purge_days=1, min_keep=0.05)),
                 note="MDA/SFI importance; base model = walk-forward fold models; top clusters by MDA logloss: " +
                      "; ".join(f"{r['name']}={r['mda_ll_mean'] * 1000:.2f}mn" for _, r in top.iterrows()))
    say(f"{model}: done in {rt:.0f}s; skipped folds {skipped}")
    return long, summ, base, sfi_df


def attach_sfi(summ, sfi_df, cluster_of):
    s = im.summarize(sfi_df, "feature", ["sfi_ll_logit1", "sfi_ll_bin1"])
    auc = sfi_df.groupby("feature")[["auc_logit1", "auc_bin1"]].mean()
    keep = ["sfi_ll_logit1_mean", "sfi_ll_logit1_t", "sfi_ll_logit1_pos", "sfi_ll_bin1_mean", "sfi_ll_bin1_t",
            "sfi_ll_bin1_pos"]
    s = s[keep].join(auc.rename(columns={"auc_logit1": "sfi_auc_logit1", "auc_bin1": "sfi_auc_bin1"}))
    summ = summ.merge(s, left_on="name", right_index=True, how="left")
    summ.loc[summ.level != "feature", list(s.columns)] = np.nan
    summ["family"] = [im.family_of(n) if lv == "feature" else "" for n, lv in zip(summ.name, summ.level)]
    summ["cluster"] = [cluster_of.get(n, "") if lv == "feature" else "" for n, lv in zip(summ.name, summ.level)]
    return summ


# ============================================================================================ report
def mn(v):
    """log-loss change in milli-nats."""
    return "" if pd.isna(v) else f"{v * 1000:+.2f}"


def usd(v):
    return "" if pd.isna(v) else f"{v:+.2f}"


def tt(v):
    return "" if pd.isna(v) else f"{v:+.1f}"


def pct(v):
    return "" if pd.isna(v) else f"{v * 100:.0f}%"


def md_table(rows, header):
    s = "| " + " | ".join(header) + " |\n|" + "|".join("---" for _ in header) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(x) for x in r) + " |\n"
    return s


def verdict(r):
    ll_ok = r.mda_ll_t >= 2 and r.mda_ll_pos >= 0.7
    usd_ok = r.mda_usd_t >= 2 and r.mda_usd_pos >= 0.6
    if ll_ok and usd_ok:
        return "matters (probability and $)"
    if ll_ok:
        return "matters for the probability, not clearly for $"
    if usd_ok:
        return "helps $ only (weak on probability)"
    if r.mda_ll_mean <= 0 or r.mda_ll_t < 1:
        return "dead weight"
    return "weak"


def report(sym, models):
    S = pd.read_csv(out(f"importance_{sym}.csv"))
    B = pd.read_csv(out(f"importance_{sym}_base.csv"))
    L = pd.read_csv(out(f"importance_{sym}_folds.csv"))
    models = [m for m in models if m in set(S.model)]
    m0 = models[0]
    lines = [f"# Feature importance: {sym} 15-minute entry model (v1 features)", "",
             f"Generated {datetime.now():%Y-%m-%d %H:%M} by run_importance.py. Out of sample only: walk-forward test "
             "years 2013-2024 + 2025H1, training purged (labels must end 1 day before the test year), the "
             "2025-07-01+ holdout never used. Money = net $ per 1 MNQ micro after costs (stop fills slip 1 extra "
             "tick). Target = 1.5R target before the stop within 16 bars.", "",
             "How to read it:", "",
             "* **MDA log loss** (milli-nats, mn): how much WORSE the model's probabilities get on the unseen year when "
             "this feature (or cluster / family) is shuffled across that year's trades. Positive = the model uses it "
             "and it is real; ~0 or negative = the model does not need it. **t** = mean / standard error across the 13 "
             "test years; 'yrs+' = share of years where it helped.",
             "* **MDA $/trade**: drop in the average $ of the trades the model keeps (p >= its threshold) when the "
             "feature is shuffled. Positive = it makes the kept trades better. Much noisier than log loss.",
             "* **SFI**: the feature ALONE (logistic on it, or a 10-bin win-rate table), improvement in log loss over "
             "the plain base rate on the unseen year. Judges each feature on its own, so overlap with other features "
             "does not hide it.",
             "* **Clusters**: groups of features with average |correlation| >= 0.3 (cut adjusted to give 15-30 "
             "groups). Shuffling a whole cluster avoids the trap where two near-copies each look useless because "
             "the other one covers for it.", ""]
    for m in models:
        b = B[B.model == m]
        n_k, tot = b.n_kept.sum(), b.tot_kept.sum()
        rnd = (b.random_usd * b.n_kept).sum() / n_k if n_k else np.nan
        lines += [f"## Full {m} model, by test year", "",
                  f"Pooled: keeps {int(n_k):,} of {int(b.n_test.sum()):,} events ({n_k / b.n_test.sum():.1%}), "
                  f"{usd(tot / n_k)} $/trade kept vs all events {usd(b.all_total.sum() / b.n_test.sum())} $/trade and "
                  f"random skip at the same count {usd(rnd)} $/trade; total {tot:+,.0f} $ "
                  f"({tot / b.years.sum():+,.0f} $/year). Mean OOS AUC {b.auc.mean():.3f}.", ""]
        lines.append(md_table(
            [[r.fold, f"{int(r.n_test):,}", f"{int(r.n_kept):,}", f"{r.auc:.3f}", usd(r.usd_kept), usd(r.all_usd),
              usd(r.random_usd), f"{r.random_p5:+.2f} .. {r.random_p95:+.2f}", f"{r.tot_kept:+,.0f}"]
             for r in b.itertuples()],
            ["year", "events", "kept", "AUC", "$/kept", "$/all events", "$/random skip", "random 5-95%", "total $"]))
    for m in models:
        s = S[S.model == m]
        lines += [f"## {m}: correlation clusters, ranked by MDA log loss", ""]
        c = s[s.level == "cluster"].sort_values("mda_ll_mean", ascending=False)
        lines.append(md_table(
            [[r.name, im.cluster_label(r.members.split("|"), 5), mn(r.mda_ll_mean), tt(r.mda_ll_t), pct(r.mda_ll_pos),
              usd(r.mda_usd_mean), tt(r.mda_usd_t), pct(r.mda_usd_pos), verdict(r)] for r in c.itertuples()],
            ["cluster", "members", "MDA ll (mn)", "t", "yrs+", "MDA $/trade", "t", "yrs+", "verdict"]))
        lines += ["", f"## {m}: feature families, ranked by MDA log loss", ""]
        f = s[s.level == "family"].sort_values("mda_ll_mean", ascending=False)
        lines.append(md_table(
            [[r.name, int(r.n_cols), mn(r.mda_ll_mean), tt(r.mda_ll_t), pct(r.mda_ll_pos), usd(r.mda_usd_mean),
              tt(r.mda_usd_t), pct(r.mda_usd_pos), verdict(r)] for r in f.itertuples()],
            ["family", "cols", "MDA ll (mn)", "t", "yrs+", "MDA $/trade", "t", "yrs+", "verdict"]))
        # by-year $ of the top clusters
        top = c.head(5).name.tolist()
        y = L[(L.model == m) & (L.level == "cluster") & L.group.isin(top)].pivot(index="group", columns="fold",
                                                                                values="mda_usd")
        y = y.loc[top]
        lines += ["", f"MDA $/kept trade by test year, top 5 clusters ({m}):", ""]
        lines.append(md_table([[g] + [usd(v) for v in y.loc[g]] for g in top], ["cluster"] + list(y.columns)))
    s = S[(S.model == m0) & (S.level == "feature")].copy()
    s["verdict"] = [verdict(r) for r in s.itertuples()]
    lines += ["", f"## Single features ({m0} MDA + model-free SFI), ranked by MDA log loss", ""]
    s = s.sort_values("mda_ll_mean", ascending=False)
    lines.append(md_table(
        [[r.name, r.family, r.cluster, mn(r.mda_ll_mean), tt(r.mda_ll_t), usd(r.mda_usd_mean), tt(r.mda_usd_t),
          mn(r.sfi_ll_logit1_mean), tt(r.sfi_ll_logit1_t), mn(r.sfi_ll_bin1_mean), tt(r.sfi_ll_bin1_t),
          f"{r.sfi_auc_bin1:.3f}" if pd.notna(r.sfi_auc_bin1) else "", r.verdict] for r in s.itertuples()],
        ["feature", "family", "cluster", "MDA ll (mn)", "t", "MDA $", "t", "SFI logit (mn)", "t", "SFI bins (mn)",
         "t", "SFI AUC", "verdict"]))
    dead = s[(s.verdict == "dead weight") & ~((s.sfi_ll_bin1_t >= 2) | (s.sfi_ll_logit1_t >= 2))]
    lines += ["", "## Plain English", ""]
    c = S[(S.model == m0) & (S.level == "cluster")].sort_values("mda_ll_mean", ascending=False)
    fam = S[(S.model == m0) & (S.level == "family")].sort_values("mda_ll_mean", ascending=False)
    good = [r for r in fam.itertuples() if verdict(r).startswith("matters")]
    lines.append("* Families the model really leans on (shuffling them hurts the probabilities in most test years, "
                 f"t >= 2): {', '.join(f'{r.name} ({mn(r.mda_ll_mean)} mn, $ {usd(r.mda_usd_mean)})' for r in good) or 'none'}.")
    weak = [r.name for r in fam.itertuples() if verdict(r) in ("dead weight",)]
    lines.append(f"* Families that are dead weight in the {m0} model (shuffling them changes nothing or helps): "
                 f"{', '.join(weak) or 'none'}.")
    lines.append(f"* Single features that are dead weight both inside the model (MDA) and alone (SFI t < 2): "
                 f"{len(dead)} of {len(s)}: {', '.join(dead.name)}.")
    usdc = [r for r in c.itertuples() if r.mda_usd_t >= 2 and r.mda_usd_pos >= 0.6]
    lines.append(f"* Clusters that measurably raise the $ of the kept trades (MDA $ t >= 2, >= 60% of years): "
                 f"{', '.join(f'{r.name} [{im.cluster_label(r.members.split(chr(124)), 3)}] {usd(r.mda_usd_mean)} $/trade' for r in usdc) or 'none'}.")
    lines.append("* Caveat: importance says what the model uses, not that the model makes money; compare the "
                 "full-model $/kept with the all-events and random-skip columns above.")
    lines += ["", "## Notes on reading the numbers", "",
              "* `cost_R` = round-trip cost / planned risk ($ distance close -> stop). It is largely MECHANICAL: when "
              "the stop is very close, costs are a big share of the 1.5R target, so the trade almost cannot win after "
              "costs. Its huge log-loss importance means the model mostly learns 'skip trades whose stop is too tight "
              "for the costs', not a market pattern.",
              "* `x_YM_*` are empty (NaN) before YM's data starts, so the 10-bin SFI (NaN = its own bin) can use them "
              "as an 'which era is this' flag; their large SFI-bins numbers with ~0 SFI-logit and ~0 MDA are that "
              "artifact, not a cross-market signal.",
              "* The correlation cut naturally gives more than 30 groups; it was forced down to 30, so the largest "
              "cluster (average linkage) mixes several families that are only loosely correlated. Read the family "
              "table for the cleaner 'which kind of information matters' view.",
              "* MDA $ per kept trade is noisy (a few hundred to a few thousand kept trades per year); one year "
              "(2024) dominates many $ numbers - see the by-year table."]
    with open(out(f"importance_{sym}.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    say(f"wrote out/importance_{sym}.md")


# ============================================================================================ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sym", default="NQ")
    ap.add_argument("--models", default="logit")
    ap.add_argument("--n-rep", type=int, default=3)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args(argv)
    sym = a.sym
    models = a.models.split(",")
    if a.report_only:
        report(sym, ["logit", "gbm"])
        return
    feats = rp.feature_list("entry", sym)
    a_ = rp.wf_args("entry")
    cols = ["t", "d", "market", a_["label"], a_["pnl"], a_["t_end"]] + feats
    avail = mem_wait()
    say(f"loading out/entries_{sym}_{rp.TF}.parquet ({len(feats)} features; {avail} MB available)")
    data = rp.load("entry", sym, columns=cols)
    S = im.prepare(data, feats, label=a_["label"], pnl=a_["pnl"], t_end=a_["t_end"])
    S["sym"] = sym
    del data
    say(f"{len(S['y']):,} labelled events before the holdout ({S['t'].min()} .. {S['t'].max()})")
    clusters, info = im.correlation_clusters(S["Xo"], min_k=15, max_k=30)
    say(f"{info['k']} clusters (natural cut {info['k_natural']}, silhouette {info['silhouette']:.3f})")
    cluster_of = {f: c for c, m in clusters.items() for f in m}
    fams = im.families(feats)
    sfi_df = None
    p_sfi = out(f"importance_{sym}_sfi.parquet")
    if os.path.exists(p_sfi):
        sfi_df = pd.read_parquet(p_sfi)
        if set(sfi_df.feature) != set(feats):
            sfi_df = None
    for m in models:
        long, summ, base, sfi_df = run_model(S, feats, clusters, fams, m, a.n_rep, sfi_df)
        sfi_df.to_parquet(p_sfi)
        summ = attach_sfi(summ, sfi_df, cluster_of)
        summ.insert(0, "model", m)
        long.insert(0, "model", m)
        base.insert(0, "model", m)
        upsert_model(f"importance_{sym}.csv", summ, m)
        upsert_model(f"importance_{sym}_folds.csv", long, m)
        upsert_model(f"importance_{sym}_base.csv", base, m)
    report(sym, ["logit", "gbm"])


if __name__ == "__main__":
    main()
