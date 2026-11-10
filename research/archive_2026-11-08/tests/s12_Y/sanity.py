"""Sanity checks: spot-check trades against raw 1-min / hourly CSV lines; roll and look-ahead checks."""
import os, sys, json, subprocess, pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *

out = {"spot_checks": [], "roll_checks": {}, "lookahead_checks": {}}


def raw_bar(sym, date, hhmm, hourly=False):
    """grep the raw CSV line for a bar stamped `hhmm` ET on `date` (file stamps carry the ET offset)"""
    fn = f"{PROJ}/data/{sym}_fut_{'1h' if hourly else '1m'}.csv"
    for off in ("-04:00", "-05:00"):
        key = f"{date} {hhmm}:00{off},"
        r = subprocess.run(["grep", "-m1", "-F", key, fn], capture_output=True, text=True).stdout.strip()
        if r:
            p = r.split(",")
            return {"line": r, "O": float(p[1]), "H": float(p[2]), "L": float(p[3]), "C": float(p[4]), "inst": int(p[6])}
    return None


def minus1(hhmm):
    h, m = map(int, hhmm.split(":")); t = h * 60 + m - 1
    return f"{t // 60:02d}:{t % 60:02d}"


def check_intraday(name, row):
    d = row.date
    eN = raw_bar("NQ", d, row.entry_time); eE = raw_bar("ES", d, row.entry_bar_E)
    if row.exit_reason == "stop":
        xN = raw_bar("NQ", d, row.exit_time); xE = raw_bar("ES", d, row.exit_bar_E); xNp, xEp = xN["O"], xE["O"]
    else:
        xN = raw_bar("NQ", d, row.exit_time); xE = raw_bar("ES", d, row.exit_bar_E); xNp, xEp = xN["C"], xE["C"]
    dec = minus1(row.entry_time)
    dN = raw_bar("NQ", d, row.decision_bar); dE = raw_bar("ES", d, row.decision_bar)
    o9N = raw_bar("NQ", d, "09:30"); o9E = raw_bar("ES", d, "09:30")
    dirn = 1 if row.side.startswith("long") else -1
    gross = row.n_nq * 2 * dirn * (xNp - eN["O"]) - row.n_es * 5 * dirn * (xEp - eE["O"])
    net = gross - (row.n_nq * 2.0 + row.n_es * 3.5)
    net_bp = 1e4 * net / (row.n_nq * 2 * eN["O"])
    k = row.b * 2 * dN["C"] / (5 * dE["C"])
    ok = (abs(eN["O"] - row.eN) < 1e-6 and abs(eE["O"] - row.eE) < 1e-6 and abs(xNp - row.xN) < 1e-6
          and abs(xEp - row.xE) < 1e-6 and abs(net - row.net_usd) < 1e-6 and abs(net_bp - row.net_bp) < 1e-6
          and abs(k - row.k) < 1e-6 and eN["inst"] == xN["inst"] == row.inst_N and eE["inst"] == xE["inst"] == row.inst_E
          and dec == row.decision_bar)
    rec = {"rule": name, "date": d, "side": row.side, "n_nq": int(row.n_nq), "n_es": int(row.n_es),
           "NQ_entry_raw_line": eN["line"], "NQ_exit_raw_line": xN["line"], "ES_entry_raw_line": eE["line"],
           "ES_exit_raw_line": xE["line"], "decision_bar": row.decision_bar, "exit_reason": row.exit_reason,
           "hand_net_usd": round(net, 4), "csv_net_usd": round(row.net_usd, 4), "hand_net_bp": round(net_bp, 4),
           "match": bool(ok)}
    if "z" in row.index:
        zh = (np.log(dN["C"] / o9N["O"]) - row.b * np.log(dE["C"] / o9E["O"])) / row.s
        rec["hand_z"] = round(zh, 4); rec["csv_z"] = round(row.z, 4); rec["match"] = rec["match"] and abs(zh - row.z) < 1e-6
    out["spot_checks"].append(rec)
    print(name, d, row.side, row.exit_reason, "MATCH" if rec["match"] else "MISMATCH", round(net, 2), round(row.net_usd, 2))


s1 = pd.read_csv(f"{HERE}/trades_S1.csv"); v1 = pd.read_csv(f"{HERE}/trades_S1-V1.csv"); s3 = pd.read_csv(f"{HERE}/trades_S3.csv")
v2 = pd.read_csv(f"{HERE}/trades_S1-V2.csv")
rng = np.random.default_rng(SEED)
for nm, df, picks in (("S1", s1, [0, len(s1) - 1] + list(rng.choice(len(s1), 2, replace=False))),
                      ("S1", s1, list(np.flatnonzero(s1.exit_reason == "stop"))),
                      ("S1-V1", v1, [int(rng.integers(len(v1)))]), ("S1-V2", v2, list(np.flatnonzero(v2.exit_reason == "stop"))),
                      ("S3", s3, [0, int(rng.integers(len(s3))), len(s3) - 1])):
    for i in picks:
        check_intraday(nm, df.iloc[int(i)])

# S2 segments: month_end exit and roll exit, plus an RTY segment
for nm, sym in (("S2", "NQ"), ("S2-V2", "RTY")):
    sg = pd.read_csv(f"{HERE}/trades_{nm}.csv")
    for i in [0, int(np.flatnonzero(sg.exit_reason == "roll")[3]), int(np.flatnonzero(sg.entry_reason == "reopen_after_roll")[3])]:
        r = sg.iloc[i]
        hourly = sym == "RTY"
        ea = raw_bar(sym, r.date, r.entry_time[:5], hourly)
        eb = raw_bar("ES", r.date, r.es_entry_time)
        if r.exit_reason == "roll":
            xa = raw_bar(sym, r.exit_date, r.exit_time[:5], hourly); xb = raw_bar("ES", r.exit_date, r.es_exit_time)
            xap, xbp = xa["C"], xb["C"]
        else:
            xa = raw_bar(sym, r.exit_date, r.exit_time[:5], hourly); xb = raw_bar("ES", r.exit_date, r.es_exit_time)
            xap, xbp = xa["O"], xb["O"]
        pt = 5.0 if hourly else 2.0; ca = 2.0
        dirn = 1 if r.side.startswith("long") else -1
        g = dirn * (r.n_a * pt * (xap - ea["O"]) - r.n_es * 5 * (xbp - eb["O"]))
        net = g - (r.n_a * ca + r.n_es * 3.5)
        ok = (abs(ea["O"] - r.entry) < 1e-6 and abs(xap - r.exit) < 1e-6 and abs(eb["O"] - r.es_entry) < 1e-6
              and abs(xbp - r.es_exit) < 1e-6 and abs(net - r.net_usd) < 1e-6
              and ea["inst"] == xa["inst"] == r.inst_a and eb["inst"] == xb["inst"] == r.inst_es)
        out["spot_checks"].append({"rule": nm, "date": r.date, "exit_date": r.exit_date, "entry_reason": r.entry_reason,
                                   "exit_reason": r.exit_reason, "A_entry_raw_line": ea["line"], "A_exit_raw_line": xa["line"],
                                   "ES_entry_raw_line": eb["line"], "ES_exit_raw_line": xb["line"],
                                   "hand_net_usd": round(net, 4), "csv_net_usd": round(r.net_usd, 4), "match": bool(ok)})
        print(nm, r.date, r.exit_date, r.entry_reason, r.exit_reason, "MATCH" if ok else "MISMATCH", round(net, 2), round(r.net_usd, 2))

# ---------------------------------------------------------------- roll checks
with open(f"{HERE}/sessions.pkl", "rb") as f:
    S = pickle.load(f)
F = pd.read_pickle(f"{HERE}/features.pkl")
for nm in ("S1", "S1-V1", "S1-V2", "S1-C2", "S3", "S3-V1", "S3-V2"):
    df = pd.read_csv(f"{HERE}/trades_{nm}.csv")
    bad = 0
    for r in df.itertuples():
        t = S.pos_of[pd.Timestamp(r.date)]
        # one RTH instrument per session (verified in prep), same as prior cash session (no roll since prior session)
        bad += int(S.roll[t]) + int(S.instN[t] != r.inst_N) + int(S.instE[t] != r.inst_E)
        bad += int(S.instN[t - 1] != r.inst_N) + int(S.instE[t - 1] != r.inst_E)
    out["roll_checks"][nm] = {"trades": int(len(df)), "violations": int(bad)}
for nm in ("S2", "S2-V1", "S2-V2"):
    sg = pd.read_csv(f"{HERE}/trades_{nm}.csv")
    # simulate_months asserts every session in a segment carries the held instruments; re-verify here for NQ/ES legs
    bad = 0
    for r in sg.itertuples():
        u0, u1 = S.pos_of[pd.Timestamp(r.date)], S.pos_of[pd.Timestamp(r.exit_date)]
        bad += int(any(S.instE[u] != r.inst_es for u in range(u0, u1 + 1)))
        if nm != "S2-V2":
            bad += int(any(S.instN[u] != r.inst_a for u in range(u0, u1 + 1)))
    out["roll_checks"][nm] = {"segments": int(len(sg)), "violations": int(bad)}
print("roll checks", out["roll_checks"])

# ---------------------------------------------------------------- look-ahead checks
la = {}
for nm in ("S1", "S1-V1", "S1-V2", "S3", "S3-V1", "S3-V2"):
    df = pd.read_csv(f"{HERE}/trades_{nm}.csv")
    la[nm] = {"decision_bar_closes_at_or_before_entry_open": bool((df.decision_bar.map(lambda s: int(s[:2]) * 60 + int(s[3:]) + 1)
                                                                   <= df.entry_time.map(lambda s: int(s[:2]) * 60 + int(s[3:]))).all())}
# beta/s/zo use strictly prior sessions (checked by recomputing one day's b by hand from prior 60 full sessions)
from y12lib import five_min_returns
d0 = pd.Timestamp(s1.date.iloc[len(s1) // 2]); t0 = S.pos_of[d0]
fi = np.flatnonzero(S.full); prior = fi[fi < t0][-60:]
xs, ys = [], []
for p in prior:
    a, bq = five_min_returns(S, p); ok = np.isfinite(a) & np.isfinite(bq); ys.append(a[ok]); xs.append(bq[ok])
x = np.concatenate(xs); y = np.concatenate(ys)
bh = np.polyfit(x, y, 1)[0]
la["beta_recomputed"] = {"date": d0.strftime("%Y-%m-%d"), "hand_b": float(bh), "features_b": float(F.b.loc[d0]),
                         "last_session_in_window": S.dates[prior[-1]].strftime("%Y-%m-%d"), "match": bool(abs(bh - F.b.loc[d0]) < 1e-9)}
la["vix_date_before_trade_date"] = bool((pd.to_datetime(F.vix_date) < F.index).all())
for nm in ("S2", "S2-V1", "S2-V2"):
    m = pd.read_csv(f"{HERE}/months_{nm}.csv")
    la[nm] = {"signal_date_before_entry": bool((pd.to_datetime(m.signal_date) < pd.to_datetime(m.date)).all())}
out["lookahead_checks"] = la
print(json.dumps(la, indent=1))
with open(f"{HERE}/sanity.json", "w") as f:
    json.dump(jsonable(out), f, indent=1)
