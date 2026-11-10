"""v4 unsupervised discovery (DISCOVERY period 2018-2021 only; no targets are ever loaded here).

States : scale-free raw market statistics -> winsorise (0.5/99.5%) -> standardise -> PCA (90% var) -> GaussianMixture.
Motifs : 12-point path shapes, re-z-normalised per row -> KMeans.
k is chosen by a rule fixed before fitting: maximise min(seed-stability ARI, cross-market ARI); ties (within 0.01)
go to the lower held-out BIC.  All fitted objects are pickled to out/frozen and hashed into FROZEN.md.

usage: python3 v4/discover.py select | final
"""
import hashlib, json, os, pickle, sys, time
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score as ari
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FROZ = os.path.join(OUT, "frozen")
SYMS = ["ES", "NQ", "YM"]
DISC_END = pd.Timestamp("2021-12-31")
K_STATE = [10, 12, 15, 18, 21, 24, 28, 32, 36, 40]
K_SHAPE = [8, 10, 12, 14, 16, 18, 20, 22, 24]
SEEDS = [0, 1, 2]
N_FIT, N_EVAL = 50_000, 50_000
SHAPES = [f"shape_{j:02d}" for j in range(12)]
RET_H = [1, 5, 15, 30, 60, 120, 240]
OPT_NAN = {"ret_240_h", "rv_240_log", "rng_240_log", "pos_240"}   # 240-min windows: NaN early in the session -> mean


def load(sym):
    cols = (["ts", "sess", "sym", "period", "clock_min", "weekday"] + [f"ret_{h}_z" for h in RET_H]
            + ["ret_sess_z", "ret_prev_z", "rv_15", "rv_60", "rv_240", "rng_15_z", "rng_60_z", "rng_240_z",
               "pos_15", "pos_60", "pos_240", "dist_shi_z", "dist_slo_z", "pos_sess", "dist_vwap_z",
               "relvol_5", "relvol_15", "relvol_60", "imb_15", "imb_60", "upshare_30", "ac1_60"] + SHAPES)
    d = pd.read_parquet(os.path.join(OUT, f"feat_{sym}.parquet"))
    xc = [c for c in d.columns if c.startswith("x") and c.endswith("_z")]
    d = d[cols + xc]
    d = d[(d.period == "discovery") & (pd.to_datetime(d.sess) <= DISC_END)].reset_index(drop=True)
    assert d.ts.max() < pd.Timestamp("2022-01-01"), "discovery leak"
    for h in (15, 60):
        d[f"xavg_ret_{h}_z"] = d[[c for c in xc if c.endswith(f"_ret_{h}_z")]].mean(1)
    return d.drop(columns=xc)


def state_matrix(d):
    """Scale-free raw statistics (no indicators, no composite scores). Returns per sqrt(minutes) so horizons align."""
    F = pd.DataFrame(index=d.index)
    for h in RET_H:
        F[f"ret_{h}_h"] = d[f"ret_{h}_z"] / np.sqrt(h)
    mins = np.maximum((d.clock_min.to_numpy(float) - 1080) % 1440, 5.0)   # clock_min = ET minute of day
    F["ret_sess_h"] = d.ret_sess_z / np.sqrt(mins)
    F["ret_prev_h"] = d.ret_prev_z / np.sqrt(1380.0)
    for w in (15, 60, 240):
        F[f"rv_{w}_log"] = np.log(d[f"rv_{w}"] + 0.05)
        F[f"rng_{w}_log"] = np.log(d[f"rng_{w}_z"] + 0.5)
        F[f"pos_{w}"] = d[f"pos_{w}"]
    F["dist_shi_log"] = np.log1p(d.dist_shi_z)
    F["dist_slo_log"] = np.log1p(d.dist_slo_z)
    F["pos_sess"] = d.pos_sess
    F["dist_vwap_h"] = d.dist_vwap_z / np.sqrt(mins)
    for w in (5, 15, 60):
        F[f"relvol_{w}_log"] = np.log(d[f"relvol_{w}"] + 0.05)
    for c in ("imb_15", "imb_60", "upshare_30", "ac1_60"):
        F[c] = d[c]
    F["xavg_ret_15_h"] = d.xavg_ret_15_z / np.sqrt(15)
    F["xavg_ret_60_h"] = d.xavg_ret_60_z / np.sqrt(60)
    return F.astype(float)


class Prep:
    """winsorise -> standardise -> (optional NaN -> 0) -> PCA. Fit on discovery only."""
    def fit(self, F, var=0.90):
        self.cols = list(F.columns)
        self.lo, self.hi = F.quantile(0.005), F.quantile(0.995)
        X = F.clip(self.lo, self.hi, axis=1)
        self.scaler = StandardScaler().fit(X)
        Z = self._z(F)
        self.pca = PCA(n_components=var, svd_solver="full", random_state=0).fit(Z)
        return self

    def usable(self, F):
        need = [c for c in self.cols if c not in OPT_NAN]
        return F[need].notna().all(1).to_numpy()

    def _z(self, F):
        Z = self.scaler.transform(F[self.cols].clip(self.lo, self.hi, axis=1))
        return np.nan_to_num(Z, nan=0.0)

    def transform(self, F):
        return self.pca.transform(self._z(F))


def shape_matrix(d):
    S = d[SHAPES].to_numpy(float)
    sd = S.std(1, keepdims=True)
    ok = np.isfinite(S).all(1) & (sd[:, 0] > 1e-9)
    Z = np.full_like(S, np.nan)
    Z[ok] = (S[ok] - S[ok].mean(1, keepdims=True)) / sd[ok]
    return Z, ok


def gmm(k, seed):
    return GaussianMixture(k, covariance_type="full", reg_covar=1e-4, max_iter=300, tol=1e-3, random_state=seed)


def km(k, seed):
    return KMeans(k, n_init=3, random_state=seed)


def select(kind, X, sym, ks, make):
    """X pooled discovery matrix, sym labels. Seed stability: 3 fits on different random subsamples + inits, ARI of
    their labels on a common eval set. Market stability: one fit per market, ARI on the same pooled eval set."""
    rng = np.random.default_rng(123)
    ev = rng.choice(len(X), N_EVAL, replace=False)
    pool = np.setdiff1d(np.arange(len(X)), ev)
    rows = []
    for k in ks:
        t0 = time.time()
        lab_s, bic, ll = [], [], []
        for s in SEEDS:
            idx = np.random.default_rng(1000 + s).choice(pool, N_FIT, replace=False)
            m = make(k, s).fit(X[idx])
            lab_s.append(m.predict(X[ev]))
            if kind == "state":
                bic.append(m.bic(X[ev])); ll.append(m.score(X[ev]))
            else:
                bic.append(-m.score(X[ev]) / N_EVAL)      # held-out within-cluster SS per row
        lab_m = []
        for j, mk in enumerate(SYMS):
            p = np.intersect1d(pool, np.nonzero(sym == mk)[0])
            idx = np.random.default_rng(2000 + j).choice(p, min(N_FIT, len(p)), replace=False)
            lab_m.append(make(k, 0).fit(X[idx]).predict(X[ev]))
        a_s = np.mean([ari(lab_s[i], lab_s[j]) for i in range(3) for j in range(i + 1, 3)])
        a_m = np.mean([ari(lab_m[i], lab_m[j]) for i in range(3) for j in range(i + 1, 3)])
        rows.append(dict(kind=kind, k=k, ari_seed=a_s, ari_market=a_m, stab=min(a_s, a_m),
                         heldout_bic=np.mean(bic), heldout_ll=np.mean(ll) if ll else np.nan, sec=time.time() - t0))
        print(rows[-1], flush=True)
    r = pd.DataFrame(rows)
    best = r.stab.max()
    pick = r[r.stab >= best - 0.01].sort_values("heldout_bic").iloc[0]
    r["chosen"] = r.k == pick.k
    return r, int(pick.k)


def build():
    d = pd.concat([load(s) for s in SYMS], ignore_index=True)
    F = state_matrix(d)
    return d, F


def words_state(zm, raw):
    """Plain-language description from standardised feature means zm (Series) and raw means."""
    out = []
    def add(score, txt): out.append((abs(score), txt))
    r60 = zm["ret_60_h"]; r15 = zm["ret_15_h"]
    if abs(r60) > 0.4: add(r60, f"{'rising' if r60 > 0 else 'falling'} over the last hour")
    if abs(r15) > 0.4 and np.sign(r15) != np.sign(r60) and abs(r60) > 0.2:
        add(r15, f"last 15 min {'bouncing up' if r15 > 0 else 'pulling back'} against the hour")
    elif abs(r15) > 0.5: add(r15, f"{'up' if r15 > 0 else 'down'} sharply in the last 15 min")
    rs = zm["ret_sess_h"]
    if abs(rs) > 0.5: add(rs, f"session {'up' if rs > 0 else 'down'} so far")
    v = zm["rv_60_log"]
    if abs(v) > 0.4: add(v, "volatile" if v > 0 else "quiet")
    rg = zm["rng_60_log"]
    if abs(rg) > 0.5 and np.sign(rg) != np.sign(v): add(rg, f"{'wide' if rg > 0 else 'narrow'} hourly range")
    rv = zm["relvol_15_log"]
    if abs(rv) > 0.4: add(rv, f"volume {'high' if rv > 0 else 'low'} for the time of day")
    ps = raw["pos_sess"]
    if ps > 0.75: add(2 * (ps - 0.5) / 0.3, "near the session high")
    elif ps < 0.30: add(2 * (0.5 - ps) / 0.3, "near the session low")
    p60 = raw["pos_60"]
    if p60 > 0.75: add((p60 - 0.5) / 0.3, "at the top of the hour's range")
    elif p60 < 0.25: add((0.5 - p60) / 0.3, "at the bottom of the hour's range")
    vw = zm["dist_vwap_h"]
    if abs(vw) > 0.5: add(vw, f"{'above' if vw > 0 else 'below'} VWAP")
    ac = zm["ac1_60"]
    if abs(ac) > 0.4: add(ac, "minute returns trending (positive autocorr.)" if ac > 0 else "minute returns choppy (neg. autocorr.)")
    im = zm["imb_15"]
    if abs(im) > 0.6: add(im, f"volume on {'up' if im > 0 else 'down'} minutes")
    xd = zm["xavg_ret_60_h"] - zm["ret_60_h"]
    if abs(xd) > 0.6: add(xd, f"{'lagging' if xd > 0 else 'leading'} the other index futures over the hour")
    pr = zm["ret_prev_h"]
    if abs(pr) > 0.6: add(pr, f"after a {'strong' if pr > 0 else 'weak'} previous session")
    out.sort(key=lambda t: -t[0])
    return ", ".join(t[1] for t in out[:5]) or "average on every statistic"


def words_shape(c):
    n = len(c); net = c[-1] - c[0]
    imax, imin = int(np.argmax(c)), int(np.argmin(c))
    third = lambda i: "early" if i < n / 3 else ("mid-hour" if i < 2 * n / 3 else "late")
    rough = np.abs(np.diff(c)).sum() / max(abs(net), 1e-9)
    if abs(net) > 2.4 and rough < 1.3:
        return f"steady {'rise' if net > 0 else 'fall'} through the hour"
    if 0 < imin < n - 1 and c[0] - c[imin] > 0.8 and c[-1] - c[imin] > 0.8:
        return f"V: fall then recover, low {third(imin)}" + (", ends higher" if net > 0.8 else ", ends lower" if net < -0.8 else "")
    if 0 < imax < n - 1 and c[imax] - c[0] > 0.8 and c[imax] - c[-1] > 0.8:
        return f"inverted V: rise then fall, high {third(imax)}" + (", ends higher" if net > 0.8 else ", ends lower" if net < -0.8 else "")
    if abs(net) > 1.5:
        k = "rise" if net > 0 else "fall"
        a = np.abs(np.diff(c)); late = a[n // 2:].sum() > 1.4 * a[: n // 2].sum(); early = a[: n // 2].sum() > 1.4 * a[n // 2:].sum()
        return f"{k}, " + ("accelerating late" if late else "mostly early then flat" if early else "with a pause")
    return "range: back and forth with little net change"


def final():
    t0 = time.time()
    sel = pd.read_csv(os.path.join(OUT, "kselect.csv"))
    k_st = int(sel[(sel.kind == "state") & sel.chosen].k.iloc[0])
    k_sh = int(sel[(sel.kind == "shape") & sel.chosen].k.iloc[0])
    d, F = build()
    ok = _usable(F)
    prep = Prep().fit(F.loc[ok])
    X = prep.transform(F.loc[ok])
    rng = np.random.default_rng(7)
    idx = rng.choice(len(X), min(300_000, len(X)), replace=False)
    best = None
    for s in SEEDS:                     # 3 inits on the same 300k fit sample, keep the best likelihood
        m = gmm(k_st, s).fit(X[idx]); sc = m.score(X[idx])
        if best is None or sc > best[0]: best = (sc, m)
    g = best[1]
    # relabel states by frequency (0 = most common) for readability
    lab = g.predict(X)
    order = np.argsort(-np.bincount(lab, minlength=k_st)); remap = np.empty(k_st, int); remap[order] = np.arange(k_st)
    state = np.full(len(d), -1); state[ok] = remap[lab]

    S, sok = shape_matrix(d)
    kmod = KMeans(k_sh, n_init=10, random_state=0).fit(S[sok][rng.choice(sok.sum(), min(300_000, sok.sum()), replace=False)])
    ml = kmod.predict(S[sok])
    ordm = np.argsort(-np.bincount(ml, minlength=k_sh)); rm = np.empty(k_sh, int); rm[ordm] = np.arange(k_sh)
    motif = np.full(len(d), -1); motif[sok] = rm[ml]

    # ---------------- freeze BEFORE anything else is derived
    os.makedirs(FROZ, exist_ok=True)
    objs = {"state_prep.pkl": dict(cols=prep.cols, lo=prep.lo, hi=prep.hi, scaler=prep.scaler, pca=prep.pca,
                                   opt_nan=sorted(OPT_NAN), note="state_matrix() in v4/discover.py builds the input"),
            "state_gmm.pkl": dict(model=g, remap=remap, k=k_st),
            "shape_kmeans.pkl": dict(model=kmod, remap=rm, k=k_sh, note="input: shape_00..11 re-z-normalised per row")}
    hashes = {}
    for fn, o in objs.items():
        p = os.path.join(FROZ, fn)
        with open(p, "wb") as f: pickle.dump(o, f)
        hashes[fn] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    src = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
    with open(os.path.join(FROZ, "FROZEN.md"), "w") as f:
        f.write(f"# v4 frozen unsupervised models\n\nFrozen {time.strftime('%Y-%m-%d %H:%M')} local, fitted on DISCOVERY "
                f"2018-01-01..2021-12-31 only (ES+NQ+YM pooled). No forward return / target column was loaded or "
                f"examined before freezing (load() reads feature columns only).\n\n"
                f"- states: GaussianMixture(k={k_st}, full cov) on PCA({prep.pca.n_components_} comps, "
                f"{prep.pca.explained_variance_ratio_.sum():.3f} var) of {len(prep.cols)} standardised, winsorised features\n"
                f"- motifs: KMeans(k={k_sh}) on 12-point path shapes, re-z-normalised per row\n"
                f"- k chosen by max min(seed ARI, market ARI), ties within 0.01 -> lower held-out BIC/SSE (out/kselect.csv)\n\n"
                f"| file | sha256 |\n|---|---|\n" + "".join(f"| {k} | {v} |\n" for k, v in hashes.items())
                + f"| v4/discover.py (source) | {src} |\n")
    print("frozen", hashes, flush=True)

    # ---------------- descriptions (no outcomes)
    lab_df = d[["ts", "sess", "sym", "clock_min", "weekday"]].copy()
    lab_df["state"], lab_df["motif"] = state, motif
    lab_df.to_parquet(os.path.join(OUT, "labels_discovery.parquet"), index=False)

    Zs = pd.DataFrame(prep.scaler.transform(F.loc[ok, prep.cols].clip(prep.lo, prep.hi, axis=1)), columns=prep.cols)
    Zs["state"] = state[ok]
    zmean = Zs.groupby("state").mean()
    raw = F.loc[ok].assign(state=state[ok]).groupby("state").mean()

    def trans(lbl, K):
        dd = lab_df.assign(lbl=lbl).sort_values(["sym", "ts"])
        nxt = dd.groupby(["sym", "sess"]).lbl.shift(-1)
        gap = dd.groupby(["sym", "sess"]).ts.shift(-1) - dd.ts
        m = (dd.lbl >= 0) & (nxt >= 0) & (gap == pd.Timedelta("5min"))
        T = pd.crosstab(dd.lbl[m], nxt[m].astype(int)).reindex(index=range(K), columns=range(K), fill_value=0)
        return T.div(T.sum(1), axis=0)

    def when(lbl, K):
        cm = lab_df.clock_min.to_numpy()
        hr = cm // 60
        rth = (cm >= 570) & (cm < 960)
        rows = []
        for s in range(K):
            m = lbl == s
            h = pd.Series(hr[m]).value_counts(normalize=True)
            base = pd.Series(hr[lbl >= 0]).value_counts(normalize=True)
            lift = (h / base).sort_values(ascending=False)
            rows.append(dict(rth_share=rth[m].mean(), peak_hours_et=",".join(f"{int(x):02d}h" for x in lift.index[:3]),
                             peak_lift=round(lift.iloc[0], 2)))
        return pd.DataFrame(rows)

    res = {}
    for name, lbl, K in (("state", state, k_st), ("motif", motif, k_sh)):
        T = trans(lbl, K); T.to_csv(os.path.join(OUT, f"{name}_transitions.csv"))
        W = when(lbl, K)
        fr = pd.crosstab(lbl[lbl >= 0], lab_df.sym[lbl >= 0], normalize="columns")
        tab = pd.DataFrame({name: range(K)})
        for s in SYMS: tab[f"freq_{s}"] = fr[s].reindex(range(K)).to_numpy().round(4)
        p = np.diag(T.to_numpy()); tab["p_stay"] = p.round(3); tab["mean_dwell_min"] = (5 / (1 - p)).round(1)
        top = T.to_numpy().copy(); np.fill_diagonal(top, 0)
        tab["next_most_likely"] = [f"{j}({top[i, j]:.2f})" for i, j in enumerate(top.argmax(1))]
        tab = pd.concat([tab, W], axis=1)
        if name == "state":
            tab["words"] = [words_state(zmean.loc[s], raw.loc[s]) for s in range(K)]
            keep = ["ret_15_h", "ret_60_h", "ret_sess_h", "rv_60_log", "rng_60_log", "relvol_15_log", "pos_sess",
                    "pos_60", "dist_vwap_h", "ac1_60", "imb_15", "xavg_ret_60_h", "ret_prev_h"]
            for c in keep: tab[f"z_{c}"] = zmean[c].reindex(range(K)).round(2).to_numpy()
            zmean.to_csv(os.path.join(OUT, "state_feature_means_z.csv"))
        else:
            C = kmod.cluster_centers_[ordm]
            tab["words"] = [words_shape(c) for c in C]
            tab["centroid"] = [" ".join(f"{v:+.1f}" for v in c) for c in C]
        tab.to_csv(os.path.join(OUT, f"discovery_{name}s.csv"), index=False)
        res[name] = tab
    ct = pd.crosstab(lab_df.state[(state >= 0) & (motif >= 0)], lab_df.motif[(state >= 0) & (motif >= 0)], normalize="index")
    ct.round(3).to_csv(os.path.join(OUT, "state_x_motif.csv"))
    print(f"labelled rows: state {np.mean(state >= 0):.3f}, motif {np.mean(motif >= 0):.3f}; {time.time() - t0:.0f}s")
    pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 140)
    for n, t in res.items():
        print(t[[n, "freq_ES", "freq_NQ", "freq_YM", "p_stay", "mean_dwell_min", "rth_share", "peak_hours_et", "words"]].to_string(index=False))
    return k_st, k_sh, prep, hashes


def _usable(F):
    need = [c for c in F.columns if c not in OPT_NAN]
    return F[need].notna().all(1).to_numpy()


def run_select():
    t0 = time.time()
    d, F = build()
    ok = _usable(F)
    prep = Prep().fit(F.loc[ok])
    X = prep.transform(F.loc[ok]); sym = d.sym.to_numpy()[ok]
    print(f"rows {len(d)}, usable {ok.mean():.3f}, PCA comps {prep.pca.n_components_} "
          f"({prep.pca.explained_variance_ratio_.sum():.3f})", flush=True)
    S, sok = shape_matrix(d)
    r1, k1 = select("state", X, sym, K_STATE, gmm)
    r2, k2 = select("shape", S[sok], d.sym.to_numpy()[sok], K_SHAPE, km)
    r = pd.concat([r1, r2]); r.to_csv(os.path.join(OUT, "kselect.csv"), index=False)
    print(r.round(4).to_string(index=False)); print("chosen", k1, k2, f"{time.time() - t0:.0f}s")
    return prep, k1, k2, time.time() - t0


if __name__ == "__main__":
    from run_pipeline import log_trial
    cmd = sys.argv[1]
    if cmd == "select":
        prep, k1, k2, sec = run_select()
        log_trial(module="v4-discovery", scope="discovery 2018-2021 ES+NQ+YM pooled", model="GMM states / KMeans motifs",
                  target="none (unsupervised)", runtime_s=round(sec),
                  parameters=json.dumps(dict(stage="select", K_STATE=K_STATE, K_SHAPE=K_SHAPE, n_fit=N_FIT,
                                             pca_comps=int(prep.pca.n_components_))),
                  note=f"k chosen: states {k1}, motifs {k2}")
    elif cmd == "final":
        t = time.time()
        k1, k2, prep, h = final()
        log_trial(module="v4-discovery", scope="discovery 2018-2021 ES+NQ+YM pooled", model="GMM states / KMeans motifs",
                  target="none (unsupervised)", runtime_s=round(time.time() - t),
                  parameters=json.dumps(dict(stage="final+freeze", k_state=k1, k_shape=k2)),
                  note="frozen sha256: " + ",".join(f"{a}:{b[:12]}" for a, b in h.items()))
