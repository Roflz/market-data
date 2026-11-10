"""v4 ONE-SHOT confirmation (2022-01-01..2025-06-27) of the frozen states/motifs + global predictability benchmarks.

Frozen models are hash-checked against out/frozen/FROZEN.md and only applied (no refit). Benchmarks (ridge, kNN) are
trained on DISCOVERY 2018-2021 only; their tuning (alpha, k) uses 2018-20 -> 2021 inside discovery.
Nothing at/after the locked holdout (2025-06-30 18:00 ET) is loaded.

usage: python3 v4/confirm.py
"""
import hashlib, os, pickle, re, sys, time
import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.linear_model import Ridge

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from discover import state_matrix, _usable, shape_matrix  # noqa: E402

OUT = os.path.join(HERE, "out"); FROZ = os.path.join(OUT, "frozen")
SYMS = ["ES", "NQ", "YM"]
HOLD = pd.Timestamp("2025-06-30 18:00"); CONF_END = pd.Timestamp("2025-06-27")
DISC_END = pd.Timestamp("2021-12-31"); CONF_START = pd.Timestamp("2022-01-01"); SPLIT = pd.Timestamp("2024-01-01")
HZ = ["5", "15", "60", "eod"]; HOLD_MIN = {"5": 5, "15": 15, "60": 60, "eod": 10 ** 6}
SZ = ["15", "60"]
B = 2000; MEAN_BLOCK = 5.0; MIN_N, MIN_SESS = 200, 30
NG = 12 + 10 + 120
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def boot_counts(T, mean_block=MEAN_BLOCK, B=B, seed=0):
    """Stationary (Politis-Romano) bootstrap over sessions in time order -> (B,T) draw counts (= lab.boot_counts)."""
    rng = np.random.default_rng(seed)
    new = rng.random((B, T)) < 1.0 / mean_block; new[:, 0] = True
    pos = np.broadcast_to(np.arange(T), (B, T))
    last = np.maximum.accumulate(np.where(new, pos, 0), axis=1)
    first = np.take_along_axis(rng.integers(0, T, (B, T)), last, axis=1)
    idx = (first + pos - last) % T
    flat = (np.arange(B)[:, None] * T + idx).ravel()
    return np.bincount(flat, minlength=B * T).reshape(B, T).astype(np.float64)


def by(p):
    p = np.asarray(p, float); out = np.full(len(p), np.nan); ok = np.isfinite(p); K = int(ok.sum())
    if K == 0: return out
    c = np.sum(1.0 / np.arange(1, K + 1)); pv = p[ok]; o = np.argsort(pv)
    raw = pv[o] * K * c / np.arange(1, K + 1)
    adj = np.minimum(1, np.minimum.accumulate(raw[::-1])[::-1]); q = np.empty(K); q[o] = adj; out[ok] = q
    return out


# ------------------------------------------------------------------ frozen models
def frozen():
    txt = open(os.path.join(FROZ, "FROZEN.md")).read()
    objs = {}
    for f in ("state_prep.pkl", "state_gmm.pkl", "shape_kmeans.pkl"):
        want = re.search(rf"\| {re.escape(f)} \| ([0-9a-f]{{64}}) \|", txt).group(1)
        raw = open(os.path.join(FROZ, f), "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        assert got == want, f"HASH MISMATCH {f}"
        objs[f] = pickle.loads(raw)
    src = re.search(r"\| v4/discover.py \(source\) \| ([0-9a-f]{64}) \|", txt).group(1)
    assert hashlib.sha256(open(os.path.join(HERE, "discover.py"), "rb").read()).hexdigest() == src, "discover.py changed"
    say("sha256 verified: state_prep, state_gmm, shape_kmeans, discover.py")
    return objs


def load(sym):
    d = pd.read_parquet(os.path.join(OUT, f"feat_{sym}.parquet"))
    d["sess"] = pd.to_datetime(d.sess); d["ts"] = pd.to_datetime(d.ts)
    assert d.ts.max() < HOLD and d.sess.max() <= CONF_END, "holdout leak"
    xc = [c for c in d.columns if c.startswith("x") and c.endswith("_z") and c[1:3] in SYMS]
    for h in (15, 60):
        d[f"xavg_ret_{h}_z"] = d[[c for c in xc if c.endswith(f"_ret_{h}_z")]].mean(1)
    return d.sort_values("ts").reset_index(drop=True)


def label(d, objs):
    P, G, K = objs["state_prep.pkl"], objs["state_gmm.pkl"], objs["shape_kmeans.pkl"]
    F = state_matrix(d); ok = _usable(F)
    Z = np.nan_to_num(P["scaler"].transform(F[P["cols"]].clip(P["lo"], P["hi"], axis=1)), nan=0.0)
    state = np.full(len(d), -1); state[ok] = G["remap"][G["model"].predict(P["pca"].transform(Z[ok]))]
    S, sok = shape_matrix(d)
    motif = np.full(len(d), -1); motif[sok] = K["remap"][K["model"].predict(S[sok])]
    return state, motif, ok, Z, np.nan_to_num(S, nan=0.0)


# ------------------------------------------------------------------ (1) state / motif tests
def group_tests(d, state, motif, sym):
    c = d.period.eq("confirmation").to_numpy() & (d.sess >= CONF_START).to_numpy()
    sess = d.sess.to_numpy()[c]; usess, sc = np.unique(sess, return_inverse=True); T = len(usess)
    h2 = (sess >= np.datetime64(SPLIT))
    st, mo = state[c], motif[c]
    g1 = np.where(st >= 0, st, -1); g2 = np.where(mo >= 0, 12 + mo, -1)
    g3 = np.where((st >= 0) & (mo >= 0), 22 + st * 10 + mo, -1)
    slot = (d.clock_min.to_numpy()[c] // 15); yr = d.sess.dt.year.to_numpy()[c]
    key = pd.Series(slot * 10000 + yr)
    C = boot_counts(T, seed=SYMS.index(sym) + 1)
    rows = []
    targets = [("dir_mean", h, d[f"fwd_{h}_z"].to_numpy()[c]) for h in HZ]
    targets += [("dir_hit", h, (d[f"fwd_{h}_z"].to_numpy()[c] > 0).astype(float)
                 * np.where(np.isfinite(d[f"fwd_{h}_z"].to_numpy()[c]), 1, np.nan)) for h in HZ]
    targets += [("size", h, np.log(d[f"frng_{h}_z"].to_numpy()[c] + 0.5)) for h in SZ]
    usd = {h: d[f"fwd_{h}_usd"].to_numpy()[c] for h in HZ}
    for kind, h, y in targets:
        fin = np.isfinite(y)
        base = key.where(fin).map(pd.Series(y).where(fin).groupby(key.where(fin)).mean()).to_numpy()
        e = y - base
        eu = None
        if kind == "dir_mean":
            u = usd[h]; bu = key.where(fin).map(pd.Series(u).where(fin).groupby(key.where(fin)).mean()).to_numpy()
            eu = u - bu
        S = np.zeros((T, NG)); N = np.zeros((T, NG)); SH = np.zeros((2, NG)); NH = np.zeros((2, NG))
        SU = np.zeros(NG); BS = np.zeros(NG)
        for g in (g1, g2, g3):
            m = fin & (g >= 0)
            np.add.at(S, (sc[m], g[m]), e[m]); np.add.at(N, (sc[m], g[m]), 1)
            np.add.at(SH, (h2[m].astype(int), g[m]), e[m]); np.add.at(NH, (h2[m].astype(int), g[m]), 1)
            np.add.at(BS, g[m], base[m])
            if eu is not None: np.add.at(SU, g[m], eu[m])
        n = N.sum(0); ns = (N > 0).sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            mean = S.sum(0) / n; mb = (C @ S) / (C @ N)
            sd = np.nanstd(mb, 0, ddof=1); z = mean / sd; p = 2 * norm.sf(np.abs(z))
            mh = SH / NH
        for g in range(NG):
            valid = n[g] >= MIN_N and ns[g] >= MIN_SESS
            rows.append(dict(kind=kind, sym=sym, h=h, group=gname(g), gtype="state" if g < 12 else "motif" if g < 22 else "joint",
                             n=int(n[g]), n_sess=int(ns[g]), base=BS[g] / n[g] if n[g] else np.nan, excess=mean[g],
                             excess_usd=SU[g] / n[g] if (eu is not None and n[g]) else np.nan,
                             se=sd[g], z=z[g], p=p[g] if valid else np.nan, ex_2223=mh[0, g], ex_2425=mh[1, g]))
    return pd.DataFrame(rows)


def gname(g):
    return f"S{g}" if g < 12 else f"M{g-12}" if g < 22 else f"S{(g-22)//10}xM{(g-22)%10}"


def nonoverlap(sc, m18, hold):
    """Greedy non-overlapping selection within each session (rows sorted by time)."""
    keep = np.zeros(len(sc), bool); last_s, free = -1, -1
    for i in range(len(sc)):
        if sc[i] != last_s: last_s, free = sc[i], -1
        if m18[i] >= free:
            keep[i] = True; free = m18[i] + hold
    return keep


def boot_mean_ci(x, sc, seed=0):
    usess, s = np.unique(sc, return_inverse=True); T = len(usess)
    S = np.bincount(s, x, T); N = np.bincount(s, minlength=T).astype(float)
    C = boot_counts(T, seed=seed); mb = (C @ S) / (C @ N)
    return x.mean(), np.nanpercentile(mb, 2.5), np.nanpercentile(mb, 97.5), np.nanstd(mb, ddof=1)


def trade(d, rows_mask, side, h, sym):
    """Trade side (+1/-1 per row) at sample entry, hold h, non-overlapping per session; plain $ per micro after cost."""
    idx = np.flatnonzero(rows_mask & np.isfinite(d[f"fwd_{h}_usd"].to_numpy()))
    if len(idx) == 0: return None
    sess = d.sess.to_numpy()[idx]; _, sc = np.unique(sess, return_inverse=True)
    m18 = ((d.clock_min.to_numpy()[idx].astype(int) - 1080) % 1440)
    k = nonoverlap(sc, m18, HOLD_MIN[h]); sd = side[idx][k]; idx = idx[k]
    gross = sd * d[f"fwd_{h}_usd"].to_numpy()[idx]; net = gross - d.cost_rt_usd.to_numpy()[idx]
    yrs = (CONF_END - CONF_START).days / 365.25
    m, lo, hi, _ = boot_mean_ci(net, sc[k], seed=11)
    return dict(sym=sym, h=h, n_trades=len(idx), trades_per_yr=len(idx) / yrs, gross_usd=gross.mean(),
                net_usd=m, net_lo95=lo, net_hi95=hi, usd_per_yr=net.sum() / yrs, win_rate=(net > 0).mean())


# ------------------------------------------------------------------ (3)/(4) benchmarks
def design(d, Z, Sh, kind):
    hr = d.clock_min.to_numpy() // 60
    if kind == "ridge":
        oh = np.eye(24)[hr]; wd = np.eye(7)[np.clip(d.weekday.to_numpy(), 0, 6)]
        return np.hstack([Z, Sh, oh, wd]).astype(np.float64)
    ang = 2 * np.pi * d.clock_min.to_numpy() / 1440
    return np.hstack([Z, Sh, 2 * np.sin(ang)[:, None], 2 * np.cos(ang)[:, None]]).astype(np.float32)


def knn_pred(Xtr, Ytr, Xq, ks, chunk=300):
    """Brute-force Euclidean kNN; returns {k: (nq, ntargets)} neighbour means (targets may be NaN -> nanmean)."""
    K = max(ks); tn = (Xtr ** 2).sum(1); out = {k: np.empty((len(Xq), Ytr.shape[1]), np.float32) for k in ks}
    Yf = np.nan_to_num(Ytr).astype(np.float32); Yv = np.isfinite(Ytr).astype(np.float32)
    for a in range(0, len(Xq), chunk):
        q = Xq[a:a + chunk]; D = tn[None, :] - 2 * q @ Xtr.T
        I = np.argpartition(D, K - 1, axis=1)[:, :K]
        o = np.argsort(np.take_along_axis(D, I, 1), 1); I = np.take_along_axis(I, o, 1)
        cs, cv = np.cumsum(Yf[I], 1), np.cumsum(Yv[I], 1)
        for k in ks:
            out[k][a:a + chunk] = cs[:, k - 1] / np.maximum(cv[:, k - 1], 1)
    return out


def score(y, p, sc, ybar, seed=0):
    m = np.isfinite(y) & np.isfinite(p); y, p, sc = y[m], p[m], sc[m]
    _, s = np.unique(sc, return_inverse=True); T = s.max() + 1
    cols = [np.ones_like(y), y, p, y * y, p * p, y * p, (y - p) ** 2, (y - ybar) ** 2]
    A = np.stack([np.bincount(s, c, T) for c in cols], 1); C = boot_counts(T, seed=seed)

    def f(M):
        n, sy, sp, syy, spp, syp, sse, sst = M.T
        cov = syp / n - sy * sp / n ** 2; vy = syy / n - (sy / n) ** 2; vp = spp / n - (sp / n) ** 2
        return cov / np.sqrt(vy * vp), 1 - sse / sst
    r, r2 = f(A[None, :].sum(1)); rb, r2b = f(C @ A)
    return dict(n=int(m.sum()), corr=float(r[0]) if np.ndim(r) else float(r), corr_lo=np.nanpercentile(rb, 2.5),
                corr_hi=np.nanpercentile(rb, 97.5), r2=float(np.ravel(r2)[0]), r2_lo=np.nanpercentile(r2b, 2.5),
                r2_hi=np.nanpercentile(r2b, 97.5))


def causal_extremes(pred, sess, q=0.10, warm=20):
    """+1/-1/0: prediction above/below the 90/10% quantile of all predictions made in EARLIER test sessions."""
    us, sc = np.unique(sess, return_inverse=True); side = np.zeros(len(pred)); o = np.argsort(sc, kind="stable")
    bounds = np.searchsorted(sc[o], np.arange(len(us) + 1))
    for t in range(warm, len(us)):
        past = pred[o[:bounds[t]]]; past = past[np.isfinite(past)]
        lo, hi = np.quantile(past, [q, 1 - q]); cur = o[bounds[t]:bounds[t + 1]]
        side[cur] = np.where(pred[cur] >= hi, 1, np.where(pred[cur] <= lo, -1, 0))
    return side


def benchmarks(d, Z, Sh, ok, sym):
    disc = ok & d.period.eq("discovery").to_numpy() & (d.sess <= DISC_END).to_numpy()
    conf = ok & d.period.eq("confirmation").to_numpy() & (d.sess >= CONF_START).to_numpy()
    tr_a = disc & (d.sess < pd.Timestamp("2021-01-01")).to_numpy(); va = disc & (d.sess >= pd.Timestamp("2021-01-01")).to_numpy()
    tn = [f"fwd_{h}_z" for h in HZ] + [f"frng_{h}_z" for h in SZ]
    Y = np.column_stack([d[f"fwd_{h}_z"].to_numpy() for h in HZ] + [np.log(d[f"frng_{h}_z"].to_numpy() + 0.5) for h in SZ])
    lo_q, hi_q = np.nanquantile(Y[disc], 0.005, 0), np.nanquantile(Y[disc], 0.995, 0)
    Yc = np.clip(Y, lo_q, hi_q)
    sess = d.sess.to_numpy(); res, preds = [], {}
    # clock-only reference: discovery mean per 15-min slot
    slot = d.clock_min.to_numpy() // 15
    for j, t in enumerate(tn):
        mm = disc & np.isfinite(Yc[:, j])
        ref = pd.Series(Yc[mm, j]).groupby(slot[mm]).mean().reindex(range(96)).to_numpy()[slot]
        preds[("clock", t)] = ref
    # ridge: alpha by 2018-20 -> 2021
    Xr = design(d, Z, Sh, "ridge"); alphas = [1, 10, 100, 1e3, 1e4, 1e5]
    for j, t in enumerate(tn):
        mtr, mva = tr_a & np.isfinite(Yc[:, j]), va & np.isfinite(Y[:, j])
        cs = [np.corrcoef(Ridge(alpha=a).fit(Xr[mtr], Yc[mtr, j]).predict(Xr[mva]), Y[mva, j])[0, 1] for a in alphas]
        a = alphas[int(np.nanargmax(cs))]; mfit = disc & np.isfinite(Yc[:, j])
        preds[("ridge", t)] = np.where(conf, Ridge(alpha=a).fit(Xr[mfit], Yc[mfit, j]).predict(Xr), np.nan)
        say(f"  {sym} ridge {t}: alpha={a:g} val corr={np.nanmax(cs):+.4f}")
    del Xr
    # kNN: train every 2nd discovery row, k by 2018-20 -> 2021 (every 6th 2021 row), test every 3rd confirmation row
    Xk = design(d, Z, Sh, "knn"); ks = [50, 200, 1000]
    itr = np.flatnonzero(tr_a)[::2]; iva = np.flatnonzero(va)[::6]
    V = knn_pred(Xk[itr], Yc[itr], Xk[iva], ks)
    kbest = {}
    for j, t in enumerate(tn):
        yv = Y[iva, j]; f = np.isfinite(yv)
        cs = [np.corrcoef(V[k][f, j], yv[f])[0, 1] for k in ks]; kbest[t] = ks[int(np.nanargmax(cs))]
        say(f"  {sym} knn {t}: k={kbest[t]} val corr={np.nanmax(cs):+.4f}")
    ifit = np.flatnonzero(disc)[::2]; iq = np.flatnonzero(conf)[::3]
    P = knn_pred(Xk[ifit], Yc[ifit], Xk[iq], sorted(set(kbest.values())))
    for j, t in enumerate(tn):
        p = np.full(len(d), np.nan); p[iq] = P[kbest[t]][:, j]; preds[("knn", t)] = p
    del Xk
    for (model, t), p in preds.items():
        j = tn.index(t); ybar = np.nanmean(Yc[disc, j]); m = conf & np.isfinite(p)
        r = score(Y[m, j], p[m], sess[m], ybar, seed=3)
        r.update(sym=sym, model=model, target=t, param=(kbest.get(t) if model == "knn" else ""))
        if t.startswith("fwd_"):
            h = t.split("_")[1]
            side = np.zeros(len(d)); side[m] = causal_extremes(p[m], sess[m])
            tr = trade(d, side != 0, side, h, sym)
            if tr: r.update({f"top10_{k}": v for k, v in tr.items() if k not in ("sym", "h")})
        res.append(r)
    return pd.DataFrame(res)


def main():
    t0 = time.time(); objs = frozen()
    # pipeline check: re-label discovery rows and compare with labels_discovery.parquet
    ref = pd.read_parquet(os.path.join(OUT, "labels_discovery.parquet"))
    tests, bench, labs, econ = [], [], [], []
    for sym in SYMS:
        ts = time.time(); d = load(sym); state, motif, ok, Z, Sh = label(d, objs)
        r = ref[ref.sym == sym]; mrg = d[["ts"]].assign(state=state, motif=motif).merge(r[["ts", "state", "motif"]], on="ts", suffixes=("", "_ref"))
        say(f"{sym}: rows={len(d)} discovery relabel agreement state={np.mean(mrg.state == mrg.state_ref):.5f} "
            f"motif={np.mean(mrg.motif == mrg.motif_ref):.5f} (n={len(mrg)})")
        c = d.period.eq("confirmation").to_numpy()
        say(f"  confirmation rows={c.sum()} sessions={d.sess[c].nunique()} labelled state={np.mean(state[c] >= 0):.3f} motif={np.mean(motif[c] >= 0):.3f}")
        say("  conf state freq:", np.round(np.bincount(state[c][state[c] >= 0], minlength=12) / (state[c] >= 0).sum(), 3).tolist())
        labs.append(d.loc[c, ["ts", "sess", "sym", "clock_min"]].assign(state=state[c], motif=motif[c]))
        tests.append(group_tests(d, state, motif, sym)); say(f"  group tests done {time.time()-ts:.0f}s")
        bench.append(benchmarks(d, Z, Sh, ok, sym)); say(f"  benchmarks done {time.time()-ts:.0f}s")
        econ.append((sym, d[["ts", "sess", "clock_min", "cost_rt_usd", "period"] + [f"fwd_{h}_usd" for h in HZ]].copy(), state, motif))
        del Z, Sh
    pd.concat(labs).to_parquet(os.path.join(OUT, "labels_confirmation.parquet"), index=False)
    T = pd.concat(tests, ignore_index=True)
    dm = T.kind.isin(["dir_mean", "dir_hit"]); T["q_by"] = np.nan
    T.loc[dm, "q_by"] = by(T.loc[dm, "p"].to_numpy()); T.loc[~dm, "q_by"] = by(T.loc[~dm, "p"].to_numpy())
    sgn = np.sign(T.excess)
    T["n_mkt_same_sign"] = 0
    for (k, h, g), grp in T.groupby(["kind", "h", "group"]):
        s = np.sign(grp.excess.to_numpy())
        T.loc[grp.index, "n_mkt_same_sign"] = [(s == x).sum() for x in s]
    T["halves_agree"] = (np.sign(T.ex_2223) == sgn) & (np.sign(T.ex_2425) == sgn)
    T["survives"] = (T.q_by < 0.05) & (T.n_mkt_same_sign >= 2) & T.halves_agree
    T.to_csv(os.path.join(OUT, "confirm_tests.csv"), index=False)
    say(f"\ntests: dir={dm.sum()} (valid p {T.loc[dm,'p'].notna().sum()}), size={(~dm).sum()} (valid {T.loc[~dm,'p'].notna().sum()})")
    for k in ("dir_mean", "dir_hit", "size"):
        s = T[T.kind == k]
        say(f"  {k}: p<0.05 {int((s.p<0.05).sum())}/{s.p.notna().sum()}, q_BY<0.05 {int((s.q_by<0.05).sum())}, survive {int(s.survives.sum())}")
    S = T[T.survives].sort_values(["kind", "q_by"]); S.to_csv(os.path.join(OUT, "confirm_survivors.csv"), index=False)
    # ------------- (2) economics for surviving direction effects (union of mean/hit survivors)
    E = []
    dirs = S[S.kind.isin(["dir_mean", "dir_hit"])][["sym", "h", "group"]].drop_duplicates()
    for sym, d, state, motif in econ:
        c = d.period.eq("confirmation").to_numpy() & (d.sess >= CONF_START).to_numpy()
        for _, r in dirs[dirs.sym == sym].iterrows():
            g = r.group
            if "x" in g: si, mi = int(g.split("x")[0][1:]), int(g.split("x")[1][1:]); m = (state == si) & (motif == mi)
            elif g[0] == "S": m = state == int(g[1:])
            else: m = motif == int(g[1:])
            row = T[(T.kind == "dir_mean") & (T.sym == sym) & (T.h == r.h) & (T.group == g)].iloc[0]
            sd = np.sign(row.excess) or 1.0
            tr = trade(d, c & m, np.full(len(d), sd), r.h, sym)
            if tr: tr.update(group=g, side="long" if sd > 0 else "short", excess_z=row.excess, excess_usd=row.excess_usd); E.append(tr)
    E = pd.DataFrame(E); E.to_csv(os.path.join(OUT, "confirm_econ.csv"), index=False)
    Bm = pd.concat(bench, ignore_index=True); Bm.to_csv(os.path.join(OUT, "confirm_bench.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    say("\nSURVIVORS (top 40):\n" + S.head(40)[["kind", "sym", "h", "group", "n", "n_sess", "base", "excess", "excess_usd", "z", "q_by", "ex_2223", "ex_2425", "n_mkt_same_sign"]].round(4).to_string(index=False))
    if len(E): say("\nECON:\n" + E.round(3).to_string(index=False))
    say("\nBENCH:\n" + Bm.round(4).to_string(index=False))
    rt = time.time() - t0
    from run_pipeline import log_trial
    for k in ("dir_mean", "dir_hit", "size"):
        s = T[T.kind == k]
        log_trial(module="v4-confirm", scope="ES,NQ,YM 2022-01-01..2025-06-27 (one-shot)", model="frozen GMM12 states + KMeans10 motifs + joint",
                  target=k, oos_rows=int(s.n.sum()), runtime_s=round(rt), parameters=f"tests={s.p.notna().sum()} BY q<0.05; session stationary bootstrap B={B} block={MEAN_BLOCK}",
                  note=f"q<0.05: {int((s.q_by<0.05).sum())}; survive(2/3 mkts, both halves): {int(s.survives.sum())}")
    if len(E):
        log_trial(module="v4-confirm", scope="econ survivors", model="state/motif direction, non-overlap", target="net $/micro",
                  oos_rows=int(E.n_trades.sum()), oos_usd_per_trade=round(float((E.net_usd * E.n_trades).sum() / E.n_trades.sum()), 3), runtime_s=round(rt),
                  note=f"{len(E)} cells; net>0 with CI lo>0: {int((E.net_lo95>0).sum())}")
    for _, r in Bm.iterrows():
        log_trial(module="v4-confirm", scope=f"{r.sym} 2022-25H1 (trained 2018-21)", model=f"bench-{r.model}", target=r.target,
                  oos_rows=int(r.n), oos_auc=round(float(r["corr"]), 5),
                  oos_usd_per_trade=round(float(r.get("top10_net_usd", np.nan)), 3) if pd.notna(r.get("top10_net_usd", np.nan)) else "",
                  runtime_s=round(rt), parameters=f"param={r.param}", note=f"oos_auc column = OOS corr; R2={r.r2:.5f}")
    say(f"done {rt:.0f}s")
    open(os.path.join(OUT, "confirm.log"), "w").write("\n".join(LOG))


if __name__ == "__main__":
    main()
