"""Pick the 19 walkthrough examples by fixed-seed random draws inside each category -> examples.csv.

Rule (same for every category): take the category's candidate trades (pre-holdout, decision before 2025-06-30 18:00 ET,
session at least 6 sessions after the start of its contract run so every panel's EMAs are warmed up, and at least 45
calendar days after the market's first v3 bar so the 120-min panel has history), split them by outcome, keep only the
middle half of the outcome measure (25th-75th percentile inside that group: typical trades, never the best/worst
outliers), then draw ONE row with numpy.random.default_rng([20261109, k]) where k = the example number below.
Run from research/confidence with the project PYTHONPATH."""
import math
import os

import numpy as np
import pandas as pd

import models as mdl          # v2/models.py: SIGNALS (M1 yes/no signals), lines 101-127

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.abspath(os.path.join(HERE, "..", ".."))
V2O = os.path.join(CONF, "v2", "out")
V3 = os.path.join(CONF, "v3")
HOLDOUT = pd.Timestamp("2025-06-30 18:00")
SEED = 20261109
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
PTS = math.log(2) / 20          # M1 points = coef / (ln2/20)  (v2/models.py:150-155)

# ------------------------------------------------------------------------------------------- eligibility
_sess = {s: pd.read_parquet(os.path.join(V3, "data", f"sessions_{s}.parquet"), columns=["inst", "roll"]) for s in MICRO}
_first = {s: pd.read_parquet(os.path.join(V3, "data", f"bars_{s}_60.parquet"), columns=["C"]).index.min() for s in MICRO}


def ok(sym, session, decision):
    s = _sess[sym]
    session = pd.Timestamp(session).normalize()
    if decision >= HOLDOUT or session not in s.index or decision < _first[sym] + pd.Timedelta(days=45):
        return False
    pos = s.index.get_loc(session)
    inst = s.inst.to_numpy()
    k = pos
    while k > 0 and inst[k - 1] == inst[pos]:
        k -= 1
    return (pos - k) >= 6


def mid(df, col):
    lo, hi = df[col].quantile([0.25, 0.75])
    return df[(df[col] >= lo) & (df[col] <= hi)]


def draw(df, k):
    rng = np.random.default_rng([SEED, k])
    return df.iloc[int(rng.integers(len(df)))]


rows = []


def add(k, category, system, sym, decision, side, pnl, rule, src, **extra):
    rows.append(dict(example=k, category=category, system=system, market=MICRO[sym], sym=sym,
                     decision_time=pd.Timestamp(decision), side="LONG" if side > 0 else "SHORT",
                     outcome="RIGHT (win)" if pnl > 0 else "WRONG (loss)", pnl_usd_per_micro=round(float(pnl), 2),
                     selection_rule=rule, seed=f"default_rng([{SEED}, {k}])", source=src, **extra))


# ------------------------------------------------------------------------------------------- 1-6 Model B kept
oos = pd.read_parquet(os.path.join(V2O, "oos_M3_cls_hold_15m_exp.parquet"))
oos["dec"] = oos.t + pd.Timedelta(minutes=15)
oos = oos[[ok(m, s, t) for m, s, t in zip(oos.market, oos.session, oos.dec)]]
folds = pd.read_csv(os.path.join(V2O, "models_folds.csv"))
thr = folds[folds.cfg == "15|hold|M3|cls|exp"].set_index("fold").threshold
k = 0
for sym in ("ES", "NQ", "YM"):
    for win in (True, False):
        k += 1
        g = oos[(oos.market == sym) & ((oos.pnl_usd > 0) == win)]
        r = draw(mid(g, "R"), k)
        fy = str(r.t.year) if r.t < pd.Timestamp("2025-01-01") else "2025H1"
        add(k, f"Model B kept, {'win' if win else 'loss'}", "Model B (v2 M3 tree score, 15-min, hold to 16:45)", sym,
            r.dec, r.d, r.pnl_usd,
            f"kept OOS trades of {MICRO[sym]} with pnl {'>' if win else '<='} 0, R in the 25-75th pct of that group",
            "v2/out/oos_M3_cls_hold_15m_exp.parquet", signal_bar=r.t, entry_time=r.t_entry, exit_time=r.t_exit,
            stop=r.stop, score=float(r.score), threshold=float(thr.get(fy, np.nan)), R=float(r.R))

# ------------------------------------------------------------------------------------------- 7-8 Model B skips
sc = pd.read_parquet(os.path.join(V2O, "models_scores_15.parquet"),
                     columns=["market", "t", "d", "s|15|hold|M3|cls|exp", "k|15|hold|M3|cls|exp",
                              "s|15|hold|M1|cls|exp", "k|15|hold|M1|cls|exp"])
sc = sc[sc["s|15|hold|M3|cls|exp"].notna()]
EVC = ["t", "d", "entry", "stop", "t_entry", "t_exit_hold", "pnl_hold", "R_hold", "past_stop", "session"]
sigsrc = sorted({c for c in ["m5_trend", "m15_trend", "m60_trend", "m15_struct", "m60_struct", "m5_mslope3",
                             "m15_mslope3", "m60_mslope3", "vwap_side", "pat_with3", "pat_against3", "rev_at_low",
                             "m60_sw_room", "day_room", "mtf_trig5", "mtf_mom5", "n_rules", "pb_div", "cost_R"]})
ev = []
for sym in MICRO:
    e = pd.read_parquet(os.path.join(V2O, f"v2_events_{sym}_15.parquet"), columns=EVC + sigsrc)
    e["market"] = sym
    ev.append(e)
ev = pd.concat(ev, ignore_index=True)
ev = ev[ev.past_stop != 1] if "past_stop" in ev else ev
J = sc.merge(ev, on=["market", "t", "d"], how="inner")
J["dec"] = J.t + pd.Timedelta(minutes=15)
J = J[J.R_hold.notna()]
J = J[[ok(m, s, t) for m, s, t in zip(J.market, J.session, J.dec)]]
J["fy"] = np.where(J.t < pd.Timestamp("2025-01-01"), J.t.dt.year.astype(str), "2025H1")
skips = J[~J["k|15|hold|M3|cls|exp"]]
for win in (True, False):
    k += 1
    g = skips[(skips.pnl_hold > 0) == win]
    r = draw(mid(g, "R_hold"), k)
    add(k, f"Model B SKIP that would have {'won' if win else 'lost'}", "Model B (v2 M3), event REJECTED (score < threshold)",
        r.market, r.dec, r.d, r.pnl_hold,
        f"OOS events of all 3 markets the model did NOT keep, hold-label pnl {'>' if win else '<='} 0, R_hold in 25-75th pct",
        "v2/out/models_scores_15.parquet + v2/out/v2_events_{sym}_15.parquet (pnl_hold)", signal_bar=r.t,
        entry_time=r.t_entry, exit_time=r.t_exit_hold, stop=r.stop, score=float(r["s|15|hold|M3|cls|exp"]),
        threshold=float(thr.get(r.fy, np.nan)), R=float(r.R_hold))

# ------------------------------------------------------------------------------------------- 9-11 M1 points
pts = pd.read_csv(os.path.join(V2O, "models_points.csv"))
pts = pts[pts.cfg == "15|hold|M1|cls|exp"]
coef = pts.pivot(index="fold", columns="column", values="coef")
m1 = J[J["k|15|hold|M1|cls|exp"]].copy()
S = mdl.signal_frame(m1)
cols = list(mdl.SIG_COLS) + ["cost_R"]
X = pd.concat([S, m1[["cost_R"]]], axis=1)[cols]
C = coef.loc[m1.fy.to_numpy(), cols].to_numpy()
P = X.to_numpy() * C / PTS
best = np.nanargmax(np.abs(P), axis=1)
m1["driver"] = np.array(cols)[best]
m1["driver_pts"] = P[np.arange(len(P)), best]
m1["pts_json"] = [";".join(f"{c}={v:+.1f}" for c, v in zip(cols, p) if abs(v) >= 0.05) for p in P]
print("M1 driver counts:\n", m1.driver.value_counts().head(12))
groups = [("VWAP side", ["sig_vwap"], True), ("60-min trend", ["sig_trend60", "sig_x_trend60"], False),
          ("day high/low or cost vs stop", ["sig_room_day", "sig_x_hod", "cost_R"], True)]
for name, dcols, win in groups:
    k += 1
    g = m1[m1.driver.isin(dcols) & ((m1.pnl_hold > 0) == win)]
    r = draw(mid(g, "R_hold"), k)
    add(k, f"M1 points scorecard, biggest contributor = {name}, {'win' if win else 'loss'}",
        "M1 points scorecard (v2 bounded logistic on 25 yes/no signals, 15-min, hold)", r.market, r.dec, r.d, r.pnl_hold,
        f"OOS trades KEPT by M1 whose largest |points| input is {'/'.join(dcols)} (fold's own coefficients), "
        f"{'win' if win else 'loss'}, R_hold in 25-75th pct; group size {len(g)}",
        "v2/out/models_scores_15.parquet (k|15|hold|M1|cls|exp) + v2/out/models_points.csv + v2_events",
        signal_bar=r.t, entry_time=r.t_entry, exit_time=r.t_exit_hold, stop=r.stop, score=float(r["s|15|hold|M1|cls|exp"]),
        R=float(r.R_hold), driver=r.driver, driver_points=round(float(r.driver_pts), 2), points=r.pts_json)

# ------------------------------------------------------------------------------------------- 12-13 opposite evidence (60-min, N=3)
o60 = pd.read_parquet(os.path.join(V2O, "oos_M3_cls_opp3_1b_60m_exp.parquet"))
E60 = []
for sym in MICRO:
    e = pd.read_parquet(os.path.join(V2O, f"v2_events_{sym}_60.parquet"),
                        columns=["t", "d", "entry", "stop", "t_entry", "pnl_hold", "t_exit_hold", "pnl_opp3_1b",
                                 "kind_opp3_1b", "t_exit_opp3_1b", "R_opp3_1b", "session"])
    e["market"] = sym
    E60.append(e)
E60 = pd.concat(E60, ignore_index=True)
O = o60.merge(E60, on=["market", "t", "d"], how="inner", suffixes=("", "_ev"))
O["dec"] = O.t + pd.Timedelta(minutes=60)
O = O[(O.kind_opp3_1b == 3) & O.pnl_hold.notna()]
O = O[[ok(m, s, t) for m, s, t in zip(O.market, O.session, O.dec)]]
O["saved"] = O.pnl_opp3_1b - O.pnl_hold
for name, mask in (("exit SAVED money vs holding", (O.pnl_hold < 0) & (O.saved > 0)),
                   ("exit CUT A WINNER short", (O.pnl_hold > 0) & (O.saved < 0))):
    k += 1
    g = O[mask]
    r = draw(mid(g, "saved"), k)
    add(k, f"Opposite-evidence exit (60-min, N=3): {name}", "Config A: v2 M3 60-min + opp3_1b exit", r.market, r.dec, r.d,
        r.pnl_opp3_1b, f"kept OOS trades of 60|opp3_1b|M3|cls|exp that exited on the rule (kind 3); "
        f"{'hold lost and rule exit did better' if 'SAVED' in name else 'hold won and rule exit did worse'}; "
        f"(opp3 pnl - hold pnl) in 25-75th pct; group size {len(g)}",
        "v2/out/oos_M3_cls_opp3_1b_60m_exp.parquet + v2/out/v2_events_{sym}_60.parquet", signal_bar=r.t,
        entry_time=r.t_entry, exit_time=r.t_exit_opp3_1b, stop=r.stop, score=float(r.score), hold_pnl=float(r.pnl_hold),
        hold_exit_time=r.t_exit_hold, exit_saved_usd=round(float(r.saved), 2))

# ------------------------------------------------------------------------------------------- 14-15 A1 noise band (day level)
a1 = pd.read_parquet(os.path.join(V3, "out", "trades", "A1.parquet"))
day = a1.groupby("session").agg(pnl=("pnl_usd", "sum"), n=("pnl_usd", "size"), first=("t_entry", "min"),
                                 last=("t_exit", "max"), d0=("d", "first")).reset_index()
day = day[[ok("NQ", s, t) for s, t in zip(day.session, day["first"])]]
for win in (True, False):
    k += 1
    g = day[(day.pnl > 0) == win]
    r = draw(mid(g, "pnl"), k)
    tr = a1[a1.session == r.session]
    add(k, f"A1 noise band, {'winning' if win else 'losing'} day", "A1 noise-band breakout (v3 confirmed rule), MNQ", "NQ",
        r["first"], r.d0, r.pnl, f"A1 trading days (sum of that day's trades), {'pnl > 0' if win else 'pnl <= 0'}, "
        f"day pnl in 25-75th pct; group size {len(g)}", "v3/out/trades/A1.parquet", entry_time=r["first"],
        exit_time=r["last"], n_trades=int(r.n),
        legs=";".join(f"{a:%H:%M}->{b:%H:%M} {'L' if dd > 0 else 'S'} {p:+.1f}" for a, b, dd, p in
                      zip(tr.t_entry, tr.t_exit, tr.d, tr.pnl_usd)))

# ------------------------------------------------------------------------------------------- 16-17 A4
a4 = pd.read_parquet(os.path.join(V3, "out", "trades", "A4.parquet"))
a4 = a4[[ok("NQ", s, t) for s, t in zip(a4.session, a4.t_entry)]]
for win in (True, False):
    k += 1
    g = a4[(a4.pnl_usd > 0) == win]
    r = draw(mid(g, "pnl_usd"), k)
    add(k, f"A4 CPI/NFP 08:30 fade, {'win' if win else 'loss'}", "A4 release fade (v3 confirmed rule), MNQ", "NQ",
        r.t_entry, r.d, r.pnl_usd, f"A4 trades, {'pnl > 0' if win else 'pnl <= 0'}, pnl in 25-75th pct; group size {len(g)}",
        "v3/out/trades/A4.parquet", entry_time=r.t_entry, exit_time=r.t_exit, m_pts=float(r.m_pts),
        entry_px=float(r.entry_px), exit_px=float(r.exit_px))

# ------------------------------------------------------------------------------------------- 18-19 A3 (MES leg)
a3 = pd.read_parquet(os.path.join(V3, "out", "trades", "A3.parquet"))
a3 = a3[a3.market == "ES"]
a3 = a3[[ok("ES", s, t) for s, t in zip(a3.session, a3.t_entry)]]
for win in (True, False):
    k += 1
    g = a3[(a3.pnl_usd > 0) == win]
    r = draw(mid(g, "pnl_usd"), k)
    add(k, f"A3 options-expiry Friday short (MES leg), {'win' if win else 'loss'}", "A3 opex-Friday short (v3 confirmed rule)",
        "ES", r.t_entry, r.d, r.pnl_usd, f"A3 MES trades, {'pnl > 0' if win else 'pnl <= 0'}, pnl in 25-75th pct; "
        f"group size {len(g)}", "v3/out/trades/A3.parquet", entry_time=r.t_entry, exit_time=r.t_exit,
        entry_px=float(r.entry_px), exit_px=float(r.exit_px))

out = pd.DataFrame(rows)
assert len(out) == 19 and (out.decision_time < HOLDOUT).all()
TAG = {1: "modelB", 2: "modelB", 3: "modelB", 4: "modelB", 5: "modelB", 6: "modelB", 7: "modelBskip", 8: "modelBskip",
       9: "m1", 10: "m1", 11: "m1", 12: "oppexit", 13: "oppexit", 14: "a1", 15: "a1", 16: "a4", 17: "a4", 18: "a3", 19: "a3"}
out.insert(1, "example_id", [f"ex{r.example:02d}_{TAG[r.example]}_{r.market.lower()}_"
                             f"{'win' if r.pnl_usd_per_micro > 0 else 'loss'}" for r in out.itertuples()])
m = out.example.isin([12, 13])
out.loc[m, "outcome"] = [f"exit RIGHT (saved ${v:.2f} vs holding)" if v > 0 else f"exit WRONG (gave up ${-v:.2f} vs holding)"
                         for v in out.loc[m, "exit_saved_usd"]]
out.to_csv(os.path.join(HERE, "examples.csv"), index=False)
print(out[["example_id", "category", "market", "decision_time", "side", "pnl_usd_per_micro"]].to_string())
