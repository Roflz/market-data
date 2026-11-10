"""
v3/final_exam.py - ONE-SHOT final exam of the frozen v3 survivors on the LOCKED HOLDOUT (2025-06-30 18:00 ET onward).

  *** PREPARED, NOT RUN. Running it with --run spends the locked holdout. It needs the user's explicit approval. ***

What it does (only with --run and the approval flags; see GUARDS):
  1. Rebuilds the v3 session/bar files from the 1-minute data INCLUDING the holdout into v3/data_exam/ (never touches
     v3/data/), with exactly the same build code (build_data.py) and only the end date changed. HEAVY: takes the shared
     flock itself and checks free RAM first.
  2. Points the shared harness at v3/data_exam/ and regenerates the frozen survivors with the SAME signal code used
     in-sample (g1lib.make_signal + merge_legs for A1, the opex short for A3, g4lib.release_fade for A4).
  3. Reproduction check: the rebuilt trades for sessions <= 2025-06-27 must equal the saved in-sample trades
     (out/trades/<hid>.parquet); otherwise it stops before looking at any holdout number.
  4. Scores the holdout window only (sessions 2025-07-01 .. --last), with the pre-registered machinery: net $ per micro
     after costs, the matched control C1 (999 random same-year sessions, same marks/side; seeds 1000k + chunk as in
     PREREG), d = net - C1, Newey-West t, conservative stationary-bootstrap p (max over blocks 1/5/10/20, B 5000,
     seed 20261109), per component and for the P1 portfolio (1 micro per trade; and the $250 virtual-risk version).
  5. Applies the FROZEN decision rule below and writes v3/out/final_exam/*.json|csv + a marker that makes it one-shot.

FROZEN SURVIVORS (from v3/out/synthesis/tierA.csv, 2026-11-09): A1 noise-band momentum MNQ; A3 opex-Friday short
basket (1 MES + 1 MNQ + 1 MYM, 09:30 -> 16:00); A4 08:30 CPI/NFP fade MNQ (08:45 -> 09:45). Rules: PREREG.md section 1
(sha256 c9aef662...2460). A2 (PROMISING, not proven) is scored DESCRIPTIVELY only and never changes the verdict.

FROZEN DECISION RULE (one test, no multiplicity):
  PRIMARY  = P1 at 1 micro per trade (A1 + A3 basket + A4), daily d (net minus C1) over the holdout window.
  PASSED          : mean d > 0 with conservative bootstrap p <= 0.05  AND  P1 net $ > 0.
  NOT CONFIRMED   : P1 net $ > 0 but the PASSED test fails (sign consistent, not significant; the window is short).
  FAILED          : P1 net $ <= 0 (evidence against the edge; do not trade it, re-think).
  Components: reported with Holm at 0.05 over {A1, A3, A4} on p_d; descriptive, they never overturn the primary.
  Power warning (written before running): ~340 holdout sessions; in-sample P1 daily Sharpe 0.073 overall and higher in
  2018-25H1, so the expected t is only about 1.3-2.5: a NOT CONFIRMED result is likely even if the edge is real.
HONEST CAVEAT: earlier archive runs (2026-11-08) already looked at data through 2026-11 for A1-A4, so this holdout is
not clean for them. A PASSED exam is supporting evidence, not proof; the binding confirmation is the forward paper test
(from 2026-11-10, O'Brien-Fleming z 4.05 / 2.86 / 2.34 / 2.02).

GUARDS: default = print the plan and exit. --selftest = dress rehearsal on the pre-holdout v3/data only (pseudo-window
2024-07-01..2025-06-27, in-sample, clearly labelled; no 1-minute data, no holdout). --run needs ALL of:
  --run --approved-by "<user name + date>"  and env V3_FINAL_EXAM_APPROVED=YES_SPEND_THE_HOLDOUT
  and no v3/out/final_exam/STARTED.json (one-shot marker, written before any holdout number is computed).

Run (from research/confidence; the script takes the shared flock itself for the build step):
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2:v3 OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 \
      nice -n 5 python3 v3/final_exam.py --selftest
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import math
import os
import sys
import types
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "exp_g1_noiseband"))
sys.path.insert(0, os.path.join(HERE, "exp_G4"))
import harness as H  # noqa: E402
import stats_protocol as sp  # noqa: E402

PREREG_SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
LOCK = "/tmp/claude-1000/-run-media-roflz-Disk-2---market-data/47311ca1-698f-4e93-b1a0-0c6f0237ec7b/scratchpad/heavy.lock"
EXAM_DATA = os.path.join(HERE, "data_exam")
OUTD = os.path.join(HERE, "out", "final_exam")
IN_SAMPLE_LAST = pd.Timestamp("2025-06-27")
HOLDOUT_FIRST = pd.Timestamp("2025-07-01")          # first session = 2025-06-30 18:00 ET -> trading day 2025-07-01
HOLDOUT_START = pd.Timestamp("2025-06-30 18:00")
SEED = 20261109
B = 5000
R_C1 = 999
SURVIVORS = ["A1", "A3", "A4"]
DESCRIPTIVE = ["A2"]
K = {"A1": 1, "A2": 2, "A3": 3, "A4": 4}             # C1 seeds 1000*k + chunk (PREREG 0.3)
MKTS = {"A1": ("NQ",), "A3": ("ES", "NQ", "YM"), "A4": ("NQ",), "A2": ("NQ",)}
APPROVAL_ENV = ("V3_FINAL_EXAM_APPROVED", "YES_SPEND_THE_HOLDOUT")


# ============================================================================================ data switching
def use_data(path, last):
    """Point the shared harness at another data directory (same file names) and move its holdout guards to `last`."""
    H.DATA = path
    H._CACHE.clear()
    H.LAST_SESSION = pd.Timestamp(last)
    H.HOLDOUT_SESSION_START = pd.Timestamp(last) + pd.Timedelta(hours=18)


def free_mb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) // 1024
    return 0


def build_exam_data(end_ts):
    """build_data.build() for NQ/ES/YM with the holdout end moved to end_ts, written to v3/data_exam/ (HEAVY)."""
    import build_data as bd
    os.makedirs(EXAM_DATA, exist_ok=True)
    bd.DATA = EXAM_DATA
    bd.wf = types.SimpleNamespace(HOLDOUT_SESSION_START=pd.Timestamp(end_ts))
    with open(LOCK, "w") as lk:
        print("waiting for the shared heavy lock ...", flush=True)
        fcntl.flock(lk, fcntl.LOCK_EX)
        for s in ("NQ", "ES", "YM"):
            if free_mb() < 6000:
                raise SystemExit(f"only {free_mb()} MB available (< 6000): not starting the 1-minute build")
            bd.build(s)
        fcntl.flock(lk, fcntl.LOCK_UN)


# ============================================================================================ frozen signals
def entries(hid, sym):
    """The frozen PREREG section-1 rules, through the SAME code the groups used in-sample."""
    S = H.sessions(sym)
    if hid == "A1":
        import g1lib as G1
        fn = G1.make_signal(G1.early_set(sym))
        return G1.merge_legs(fn(S, {5: H.bars(sym, 5)}))
    if hid == "A3":
        idx = S.index[S["opex"].astype(bool).to_numpy()]
        return pd.DataFrame({"session": idx, "entry": "0930", "exit": "1600", "d": -1, "leg": 0})
    if hid == "A4":
        import g4lib as G4
        return G4.release_fade()(S, {}).reset_index(drop=True)
    raise ValueError(hid)


def a2_trades(last):
    """A2 (descriptive only) through G2's own 5-minute walker and its C1 (seeds 2000 + chunk)."""
    sys.path.insert(0, os.path.join(HERE, "exp_g2_onbreak"))
    import g2lib as G2
    G2.LAST_SESSION = pd.Timestamp(last)
    G2._C.clear()
    tr = G2.onbreak_trades("NQ").copy()
    c = G2.c1_draws("NQ", tr, R=R_C1, k=K["A2"])
    tr["c1"] = c["c_mean"]
    tr["comp"] = "A2"
    return tr


def trades_and_c1(hid, first, last, R=R_C1):
    """real trades (all sessions <= last) + per-trade C1 mean c1 for trades in [first, last]."""
    out = []
    for sym in MKTS[hid]:
        e = entries(hid, sym)
        e = e[pd.DatetimeIndex(e.session) <= last].reset_index(drop=True)
        e["tid"] = np.arange(len(e))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tr = H.time_trades(sym, e)
        win = tr[(pd.DatetimeIndex(tr.session) >= first) & (pd.DatetimeIndex(tr.session) <= last)]
        ek = e[e.tid.isin(win.tid)].reset_index(drop=True)
        acc = np.zeros(len(e))
        cnt = np.zeros(len(e))
        for c in range(int(math.ceil(R / 100))):
            nr = min(100, R - 100 * c)
            if len(ek) == 0:
                break
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                rd = H.random_time_trades(sym, ek, n_rep=nr, seed=1000 * K[hid] + c, keep_session=False,
                                          keep_marks=True, keep_side=True)
            rd = rd[pd.DatetimeIndex(rd.session) <= last]
            np.add.at(acc, rd.tid.to_numpy(), rd.pnl_usd.to_numpy())
            np.add.at(cnt, rd.tid.to_numpy(), 1)
        tr = tr.copy()
        tr["c1"] = np.where(cnt[tr.tid.to_numpy()] > 0, acc[tr.tid.to_numpy()] / np.maximum(cnt[tr.tid.to_numpy()], 1),
                            np.nan)
        tr["comp"] = hid
        out.append(tr)
    return pd.concat(out, ignore_index=True)


# ============================================================================================ checks + stats
def reproduce_in_sample(hid, tr):
    """trades with session <= 2025-06-27 must match the saved in-sample trade table."""
    ref = pd.read_parquet(os.path.join(HERE, "out", "trades", f"{hid}.parquet"))
    a = tr[pd.DatetimeIndex(tr.session) <= IN_SAMPLE_LAST]
    key = ["market", "session", "t_entry", "t_exit", "d"]
    a = a[key + ["pnl_usd"]].sort_values(key).reset_index(drop=True)
    b = ref[key + ["pnl_usd"]].sort_values(key).reset_index(drop=True)
    a["session"] = pd.DatetimeIndex(a.session)
    b["session"] = pd.DatetimeIndex(b.session)
    m = a.merge(b, on=key, how="outer", suffixes=("_new", "_ref"), indicator=True)
    both = m["_merge"] == "both"
    pnl_diff = float(np.nanmax(np.abs(m.loc[both, "pnl_usd_new"] - m.loc[both, "pnl_usd_ref"]))) if both.any() else 0.0
    res = dict(hid=hid, n_new=len(a), n_ref=len(b), only_new=int((m["_merge"] == "left_only").sum()),
               only_ref=int((m["_merge"] == "right_only").sum()), max_pnl_diff=pnl_diff,
               usd_per_trade_new=float(a.pnl_usd.mean()), usd_per_trade_ref=float(b.pnl_usd.mean()))
    res["ok"] = bool(res["only_new"] + res["only_ref"] <= max(2, 0.002 * len(b)) and pnl_diff < 1e-6)
    return res


def cp(x):
    x = np.asarray(x, float)
    if len(x) < 30 or np.allclose(x, 0):
        return float("nan"), {}
    return sp.conservative_p(sp.boot_pvalue_mean, x, B=B, seed=SEED)


def score(tr, cal, name):
    w = tr[(pd.DatetimeIndex(tr.session) >= cal[0]) & (pd.DatetimeIndex(tr.session) <= cal[-1])].copy()
    sess = pd.DatetimeIndex(w.session).normalize()
    net = w.pnl_usd.groupby(sess).sum().reindex(cal, fill_value=0.0)
    d = (w.pnl_usd - w.c1).groupby(sess).sum().reindex(cal, fill_value=0.0)
    p_d, pdb = cp(d)
    p_n, pnb = cp(net)
    n = len(w)
    return dict(name=name, sessions=len(cal), n_trades=n, usd_per_trade=float(w.pnl_usd.mean()) if n else float("nan"),
                total_usd=float(w.pnl_usd.sum()), gross_per_trade=float(w.gross_usd.mean()) if n else float("nan"),
                c1_per_trade=float(w.c1.mean()) if n else float("nan"),
                d_per_trade=float((w.pnl_usd - w.c1).mean()) if n else float("nan"),
                mean_net_day=float(net.mean()), mean_d_day=float(d.mean()),
                t_net=float(sp.hac_t(net.to_numpy())[0]) if n > 1 else float("nan"),
                t_d=float(sp.hac_t(d.to_numpy())[0]) if n > 1 else float("nan"),
                p_net=p_n, p_d=p_d, p_d_blocks=pdb, p_net_blocks=pnb,
                win_pct=float((w.pnl_usd > 0).mean() * 100) if n else float("nan"),
                by_market={m: dict(n=int((w.market == m).sum()), usd_per_trade=float(w.loc[w.market == m, "pnl_usd"].mean()))
                           for m in sorted(w.market.unique())},
                wo_best10_total=float(np.sort(net.to_numpy())[:-10].sum()) if len(net) > 10 else float("nan"))


def risk_column(tr):
    """virtual risk = sd of the component's per-micro net $ over its previous 100 trades (PREREG section 5)."""
    out = []
    for h, g in tr.groupby("comp"):
        g = g.sort_values(["t_entry", "market"], kind="stable").copy()
        g["risk_usd"] = g["pnl_usd"].shift(1).rolling(100, min_periods=100).std()
        out.append(g)
    return pd.concat(out, ignore_index=True)


def verdict(p1):
    if not (p1["total_usd"] > 0):
        return "FAILED"
    if p1["mean_d_day"] > 0 and p1["p_d"] <= 0.05:
        return "PASSED"
    return "NOT CONFIRMED"


def exam(first, last, label, outdir, check_reproduction=True):
    cal = H.calendar(("NQ", "ES"))
    cal = cal[(cal >= first) & (cal <= last)]
    res = dict(label=label, window=[str(first.date()), str(last.date())], sessions=len(cal), prereg_sha256=PREREG_SHA,
               script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), components={}, reproduction={})
    allt = []
    for h in SURVIVORS:
        tr = trades_and_c1(h, first, last)
        if check_reproduction:
            rep = reproduce_in_sample(h, tr)
            res["reproduction"][h] = rep
            print("reproduction", rep, flush=True)
            if not rep["ok"]:
                raise SystemExit(f"{h}: rebuilt in-sample trades differ from the saved ones; stopping before scoring")
        res["components"][h] = score(tr, cal, h)
        allt.append(tr)
    T = pd.concat(allt, ignore_index=True)
    p1 = score(T, cal, "P1 (1 micro per trade)")
    T = risk_column(T)
    mic = np.where(T.risk_usd > 0, np.minimum(np.floor(250 / T.risk_usd + 1e-9), 20), 0)
    TR = T.assign(pnl_usd=T.pnl_usd * mic, c1=T.c1 * mic, gross_usd=T.gross_usd * mic)
    TR = TR[mic > 0]
    res["P1"] = p1
    res["P1_risk250"] = score(TR, cal, "P1 sized at $250 virtual risk")
    comp_p = np.array([res["components"][h]["p_d"] for h in SURVIVORS], float)
    res["components_holm_005"] = dict(zip(SURVIVORS, map(float, sp.holm(np.nan_to_num(comp_p, nan=1.0)))))
    res["verdict"] = verdict(p1)
    for h in DESCRIPTIVE:
        try:
            res.setdefault("descriptive", {})[h] = score(a2_trades(last), cal, h)
        except Exception as e:  # noqa: BLE001  (descriptive only)
            res.setdefault("descriptive", {})[h] = f"skipped: {e}"
    try:   # Lucid eval of P1 over the window (descriptive; v2 judge floors days at -$600 on closing P&L)
        calf = H.calendar(("NQ", "ES", "YM"))
        calf = calf[calf <= last]
        ev = H.eval(T[T.risk_usd > 0][["market", "session", "t_entry", "t_exit", "risk_usd", "pnl_usd"]],
                    sizing=[("risk", 150), ("risk", 250), ("fixed", 1), ("fixed", 3)], calendar_=calf,
                    windows={label: (str(first.date()), str(last.date()))})
        ev.to_csv(os.path.join(outdir, f"eval_{label}.csv"), index=False)
        res["eval"] = ev.to_dict(orient="records")
    except Exception as e:  # noqa: BLE001
        res["eval"] = f"skipped: {e}"
    os.makedirs(outdir, exist_ok=True)
    T.to_parquet(os.path.join(outdir, f"trades_{label}.parquet"))
    json.dump(res, open(os.path.join(outdir, f"result_{label}.json"), "w"), indent=1, default=str)
    return res


def show(res):
    print(f"\n=== {res['label']}  window {res['window'][0]} .. {res['window'][1]}  ({res['sessions']} sessions) ===")
    for h, r in list(res["components"].items()) + [("P1", res["P1"]), ("P1 $250", res["P1_risk250"])]:
        print(f"{h:8s} n {r['n_trades']:5d}  net/trade {r['usd_per_trade']:8.2f}  d/trade {r['d_per_trade']:8.2f}  "
              f"total {r['total_usd']:10.1f}  t_d {r['t_d']:5.2f}  p_d {r['p_d']:.4f}  p_net {r['p_net']:.4f}")
    print("components Holm (0.05):", res["components_holm_005"])
    print("VERDICT (frozen rule):", res["verdict"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="dress rehearsal on pre-holdout v3/data only")
    ap.add_argument("--run", action="store_true", help="spend the holdout (needs approval)")
    ap.add_argument("--approved-by", default="")
    ap.add_argument("--last", default=None, help="last holdout session to score (YYYY-MM-DD); default = data end")
    ap.add_argument("--data-end", default=None, help="build end timestamp (default: tomorrow 00:00)")
    ap.add_argument("--skip-build", action="store_true", help="reuse an existing v3/data_exam (from an approved run)")
    a = ap.parse_args()
    assert hashlib.sha256(open(os.path.join(HERE, "PREREG.md"), "rb").read()).hexdigest() == PREREG_SHA
    if a.selftest:
        use_data(os.path.join(HERE, "data"), pd.Timestamp("2025-06-30"))
        res = exam(pd.Timestamp("2024-07-01"), IN_SAMPLE_LAST, "SELFTEST_in_sample_2024H2_2025H1",
                   os.path.join(OUTD, "selftest"))
        show(res)
        print("\nSELFTEST ONLY: in-sample pseudo-window, says nothing new about the edge.")
        return
    if not a.run:
        print(__doc__)
        return
    # ------------------------------------------------------------------ real run: every guard must hold
    if os.environ.get(APPROVAL_ENV[0]) != APPROVAL_ENV[1] or not a.approved_by.strip():
        raise SystemExit("refused: needs --approved-by '<user + date>' and env "
                         f"{APPROVAL_ENV[0]}={APPROVAL_ENV[1]} (the user's explicit approval)")
    os.makedirs(OUTD, exist_ok=True)
    marker = os.path.join(OUTD, "STARTED.json")
    if os.path.exists(marker):
        raise SystemExit(f"refused: {marker} exists - the final exam is one-shot")
    json.dump(dict(started=datetime.datetime.now().isoformat(timespec="seconds"), approved_by=a.approved_by,
                   script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), prereg_sha256=PREREG_SHA),
              open(marker, "x"), indent=1)
    end_ts = pd.Timestamp(a.data_end) if a.data_end else pd.Timestamp(datetime.date.today()) + pd.Timedelta(days=1)
    if not a.skip_build:
        build_exam_data(end_ts)
    S = pd.read_parquet(os.path.join(EXAM_DATA, "sessions_NQ.parquet"))
    full = S.index[(S.last_t >= 1320)] if "last_t" in S.columns else S.index
    last = pd.Timestamp(a.last) if a.last else pd.Timestamp(full.max())
    use_data(EXAM_DATA, S.index.max())         # harness guards moved to the exam data's end; scoring stops at `last`
    res = exam(HOLDOUT_FIRST, last, "HOLDOUT", OUTD)
    show(res)


if __name__ == "__main__":
    main()
