"""
v2/models_final.py - summary of the model ladder (v2/models.py outputs) and the 3 best configurations.

SELECTION RULE (fixed before looking at the 15/5-min results; M4 and the all-events rows are never candidates):
  a config 'wins' when, pooled over MNQ/MES/MYM (OOS 2013..2025H1), its kept trades beat BOTH the matched drift null
  and the matched random skip (edge > 0) overall, in 2013-20 AND in 2021-25H1, and still beat the drift null
  without its 10 best days. score = min(tc_drift, tc_rskip) pooled. Ranking: winners first, by score; then the
  ladder rule: a simpler model (M0 < M1 < M2 < M3) within 0.3 of the best score replaces a more complex one.
  Non-winners are ranked by score after the winners (stage 5 needs 3 files even when nothing wins).
OUTPUTS (v2/out)  models_summary.csv (one row per config: pooled + per-market key numbers), models_best.csv,
  oos_<name>.parquet (kept OOS trades of the best 3: market (raw sym), micro, tf, exit, cfg, t, d, t_entry, t_exit,
  session, risk_usd, pnl_usd, R, score, drift_usd, rskip_usd), models_handcheck_<name>.csv (re-walked trades).
"""
import os
import re

import numpy as np
import pandas as pd

import dataset as ds
import models as M
import walkforward as wf

OUT = M.OUT
RANK = {"M0": 0, "M1": 1, "M2": 2, "M3": 3, "M4": 4}


def summary(R=None):
    R = pd.read_csv(os.path.join(OUT, "models_results.csv")) if R is None else R
    F = pd.read_csv(os.path.join(OUT, "models_folds.csv"))
    auc = F.groupby("cfg").auc.mean()
    kq = F.groupby("cfg").keep_q.median()
    rows = []
    for cfg, g in R.groupby("cfg", sort=False):
        a = {(r.market, r.side, r.span): r for r in g.itertuples()}
        P = a[("pooled", "all", "all")]
        allcfg = f"{int(P.tf)}|{P.exit}|ALL|-|-"
        A = R[(R.cfg == allcfg) & (R.market == "pooled") & (R.side == "all")].set_index("span")
        row = dict(cfg=cfg, tf=P.tf, exit=P.exit, model=P.model, target=P.target, variant=P.variant,
                   n=P.n, per_year=P.per_year, usd=P.usd, R=P.R, edge_drift=P.edge_drift, tc_drift=P.tc_drift,
                   edge_rskip=P.edge_rskip, tc_rskip=P.tc_rskip, auc=auc.get(cfg, np.nan), keep_q=kq.get(cfg, np.nan),
                   all_events_usd=A.usd.get("all", np.nan))
        for sp, tag in (("2013-20", "13_20"), ("2021-25H1", "21_25"), ("all w/o top 10 days", "notop10"),
                        ("all w/o 2025H1", "no2025"), ("2018+", "2018"), ("2022+", "2022")):
            r = a.get(("pooled", "all", sp))
            if r is not None:
                row[f"usd_{tag}"] = r.usd
                row[f"edge_drift_{tag}"] = r.edge_drift
                row[f"edge_rskip_{tag}"] = r.edge_rskip
        row["all_events_usd_notop10"] = A.usd.get("all w/o top 10 days", np.nan)
        for side in ("long", "short"):
            r = a.get(("pooled", side, "all"))
            if r is not None:
                row[f"usd_{side}"], row[f"n_{side}"], row[f"edge_drift_{side}"] = r.usd, r.n, r.edge_drift
        for mk in ("MNQ", "MES", "MYM"):
            r = a.get((mk, "all", "all"))
            if r is not None:
                row[f"{mk}_usd"], row[f"{mk}_per_year"] = r.usd, r.per_year
                row[f"{mk}_edge_drift"], row[f"{mk}_tc_drift"] = r.edge_drift, r.tc_drift
                row[f"{mk}_edge_rskip"] = r.edge_rskip
                r2 = a.get((mk, "all", "all w/o top 10 days"))
                row[f"{mk}_usd_notop10"] = r2.usd if r2 is not None else np.nan
                for sp, tag in (("2013-20", "13_20"), ("2021-25H1", "21_25")):
                    r3 = a.get((mk, "all", sp))
                    row[f"{mk}_edge_drift_{tag}"] = r3.edge_drift if r3 is not None else np.nan
        rows.append(row)
    S = pd.DataFrame(rows)
    cand = ~S.model.isin(["ALL", "M4"])
    S["wins"] = cand & (S.edge_drift > 0) & (S.edge_rskip > 0) & (S.edge_drift_13_20 > 0) & \
        (S.edge_drift_21_25 > 0) & (S.edge_rskip_13_20 > 0) & (S.edge_rskip_21_25 > 0) & \
        (S.edge_drift_notop10 > 0)
    S["score"] = np.minimum(S.tc_drift, S.tc_rskip)
    S["candidate"] = cand
    S.to_csv(os.path.join(OUT, "models_summary.csv"), index=False)
    return S


def pick_best(S, k=3, tol=0.3):
    C = S[S.candidate].copy()
    C["rank_m"] = C.model.map(RANK)
    C = C.sort_values(["wins", "score"], ascending=[False, False])
    out = []
    pool = C.copy()
    while len(out) < k and len(pool):
        top = pool.iloc[0]
        near = pool[(pool.wins == top.wins) & (pool.score >= top.score - tol)]
        pick = near.sort_values(["rank_m", "score"], ascending=[True, False]).iloc[0]
        out.append(pick)
        pool = pool[pool.cfg != pick.cfg]
    return pd.DataFrame(out)


def short_name(cfg):
    tf, x, m, t, v = cfg.split("|")
    return re.sub(r"[^A-Za-z0-9_]", "", f"{m}_{t}_{x}_{tf}m_{v}")


def oos_trades(cfg, D=None):
    tf, x = int(cfg.split("|")[0]), cfg.split("|")[1]
    D = M.load_tf(tf, M.EXITS_BY_TF[tf]) if D is None else D
    S = pd.read_parquet(os.path.join(OUT, f"models_scores_{tf}.parquet"))
    assert (S.t.to_numpy() == D.t.to_numpy()).all() and (S.market.to_numpy() == D.market.to_numpy()).all()
    k = S[f"k|{cfg}"].to_numpy(bool)
    T = D.loc[k, ["market", "t", "d", "t_entry", f"t_exit_{x}", "session", "risk_usd", f"pnl_{x}", f"R_{x}",
                  f"nm_{x}", f"rs_{x}", "stop"]].copy()
    T.columns = ["market", "t", "d", "t_entry", "t_exit", "session", "risk_usd", "pnl_usd", "R", "drift_usd",
                 "rskip_usd", "stop"]
    T.insert(1, "micro", T.market.map(M.MICRO))
    T.insert(2, "tf", tf)
    T.insert(3, "exit", x)
    T.insert(4, "cfg", cfg)
    T["score"] = S.loc[k, f"s|{cfg}"].to_numpy()
    T = T.sort_values(["t_entry", "market"], kind="stable").reset_index(drop=True)
    assert (pd.DatetimeIndex(T.t_exit) < wf.HOLDOUT_SESSION_START).all()
    return T


def hand_check(T, n=15, seed=11):
    """Re-walk n kept trades per market from the raw 1-minute bars (dataset.hand_check on the matching event rows)."""
    import labels as lb                                                    # noqa: PLC0415
    import features as fe                                                  # noqa: PLC0415
    tf, x = int(T.tf.iloc[0]), T.exit.iloc[0]
    out = []
    for sym in M.MARKETS:
        Ts = T[T.market == sym]
        if not len(Ts):
            continue
        E = pd.read_parquet(ds.events_path(sym, tf))
        E = E.merge(Ts[["t", "d"]].sample(min(n, len(Ts)), random_state=seed), on=["t", "d"])
        F = ds.load_frames(sym)
        m1 = lb.load_1m(sym)
        m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
        H = ds.hand_check(sym, tf, F, m1, E, n=len(E), seed=seed, exits=(x,))
        out.append(H)
        del F, m1, E
        fe.clear_cache()
    return pd.concat(out, ignore_index=True)


EXTRA = ["15|hold|M3|cls|exp"]       # best 15-min config (more trades per day for stage 5's speed goal), not top-3


def main(do_hand=True, extra=EXTRA):
    S = summary()
    B = pick_best(S)
    B["role"] = "best3"
    X = S[S.cfg.isin([c for c in extra if c not in set(B.cfg)])].assign(role="extra")
    B = pd.concat([B, X], ignore_index=True)
    B.to_csv(os.path.join(OUT, "models_best.csv"), index=False)
    print(B[["cfg", "role", "wins", "score", "n", "per_year", "usd", "edge_drift", "tc_drift", "edge_rskip", "tc_rskip"]]
          .to_string(), flush=True)
    for cfg in B.cfg:
        T = oos_trades(cfg)
        name = short_name(cfg)
        T.to_parquet(os.path.join(OUT, f"oos_{name}.parquet"), index=False)
        print(f"oos_{name}.parquet: {len(T):,} trades", flush=True)
        if do_hand:
            H = hand_check(T)
            H.to_csv(os.path.join(OUT, f"models_handcheck_{name}.csv"), index=False)
            print(f"  hand check {len(H)} trades: max |diff| {H['diff'].max():.6f}, "
                  f"{int((H['diff'] > 1e-6).sum())} differ", flush=True)


if __name__ == "__main__":
    import sys
    main(do_hand="--no-hand" not in sys.argv)
