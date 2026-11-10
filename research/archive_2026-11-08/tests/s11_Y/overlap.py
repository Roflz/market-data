"""Overlap diagnostics for section 11 (report only): daily P&L correlation with the three existing MNQ models,
share of trades taken while the ORB / overnight-break position is open (same vs opposite direction), combined
drawdown, B vs A overlap, and for C how often strategy 1 holds the same direction as the failed ORB."""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402

P = lambda f: os.path.join(c.OUT, f)  # noqa: E731


def load():
    ex = pd.read_csv(os.path.join(c.PROJ, "chosen_models_trades.csv"), parse_dates=["date"])
    daily_ex = ex.pivot_table(index="date", columns="model", values="usd", aggfunc="sum").fillna(0.0)
    orb = pd.read_csv(P("C_book_B0.csv"), parse_dates=["date"])
    on = pd.read_csv(P("onbreak_trades_with_times.csv"), parse_dates=["date"])
    on["entry_min"] = on.entry_ts.str[11:16].map(lambda s: int(s[:2]) * 60 + int(s[3:]))
    on["exit_min"] = on.exit_bar_ts.str[11:16].map(lambda s: int(s[:2]) * 60 + int(s[3:])) + 5
    on.loc[on.exit_bar_ts.str[:10] != on.date.dt.strftime("%Y-%m-%d"), "exit_min"] = 24 * 60
    orb["entry_min"] = 9 * 60 + 35
    orb["exit_min"] = orb.orb_exit_time.map(lambda s: int(s[:2]) * 60 + int(s[3:]))
    orb.loc[orb.orb_exit_reason == "close", "exit_min"] += 1          # held through the close of that bar
    return daily_ex, orb, on


def tmin(s):
    return int(s[:2]) * 60 + int(s[3:])


def open_at(book, date, minute, side_col):
    g = book[book.date == date]
    for r in g.itertuples(index=False):
        if r.entry_min <= minute < r.exit_min:
            return int(getattr(r, side_col))
    return 0


def overlap_for(T, name, daily_ex, orb, on, usd_col="net_usd"):
    T = T.copy()
    T["emin"] = T.entry_time.map(tmin)
    sides = []
    for r in T.itertuples(index=False):
        o = open_at(orb, r.date, r.emin, "orb_side")
        n = open_at(on, r.date, r.emin, "dir")
        sides.append((o, n))
    o = np.array([s[0] for s in sides])
    n = np.array([s[1] for s in sides])
    d = T.dir.to_numpy()
    res = {"trades": int(len(T)),
           "share_while_ORB_open": float((o != 0).mean()), "share_ORB_same_dir": float((o == d).mean()),
           "share_ORB_opposite_dir": float((o == -d).mean()),
           "share_while_ONbreak_open": float((n != 0).mean()), "share_ONbreak_same_dir": float((n == d).mean()),
           "share_ONbreak_opposite_dir": float((n == -d).mean())}
    day = T.groupby("date")[usd_col].sum().rename(name)
    lo, hi = T.date.min(), T.date.max()
    allday = daily_ex.loc[(daily_ex.index >= lo) & (daily_ex.index <= hi)].copy()
    J = allday.join(day, how="outer").fillna(0.0)
    corr = {m: float(J[name].corr(J[m])) for m in daily_ex.columns}
    corr_traded = {m: float(J.loc[(J[name] != 0) & (J[m] != 0), name].corr(J.loc[(J[name] != 0) & (J[m] != 0), m]))
                   for m in daily_ex.columns}
    res["daily_corr_zero_filled"] = corr
    res["daily_corr_days_both_traded"] = corr_traded
    ex_only = J[list(daily_ex.columns)].sum(axis=1)
    comb = ex_only + J[name]
    res["existing_maxdd_usd"] = c.max_dd(ex_only.to_numpy())
    res["combined_maxdd_usd"] = c.max_dd(comb.to_numpy())
    res["existing_total_usd"] = float(ex_only.sum())
    res["combined_total_usd"] = float(comb.sum())
    return res


def main():
    daily_ex, orb, on = load()
    out = {}
    for f, nm in [("A_trades.csv", "A"), ("A1_trades.csv", "A1"), ("A2_trades.csv", "A2"), ("B_trades.csv", "B"),
                  ("B-MES_trades.csv", "B-MES"), ("B1_trades.csv", "B1")]:
        T = pd.read_csv(P(f), parse_dates=["date"])
        out[nm] = overlap_for(T, nm, daily_ex, orb, on)
    # C reverse leg: offsets strategy 1 when strategy 1 holds the same direction as the failed ORB
    R = pd.read_csv(P("C_reverse_leg_trades.csv"), parse_dates=["date"])
    R["dir"] = np.where(R.side == "long", 1, -1)
    R["emin"] = R.entry_time.map(tmin)
    same = []
    for r in R.itertuples(index=False):
        n = open_at(on, r.date, r.emin, "dir")
        same.append(n == r.orb_side)
    oc = overlap_for(R, "C_rev", daily_ex, orb, on)
    oc["share_ONbreak_same_dir_as_failed_ORB"] = float(np.mean(same))
    oc["n_ONbreak_same_dir_as_failed_ORB"] = int(np.sum(same))
    out["C_reverse_leg"] = oc
    # B vs A overlap
    A = pd.read_csv(P("A_trades.csv"), parse_dates=["date"])
    B = pd.read_csv(P("B_trades.csv"), parse_dates=["date"])
    sd = sorted(set(A.date) & set(B.date))
    simult = 0
    for r in B.itertuples(index=False):
        g = A[A.date == r.date]
        for a in g.itertuples(index=False):
            if a.entry_slot <= r.entry_slot < a.exit_slot + 1 or r.entry_slot <= a.entry_slot < r.exit_slot + 1:
                simult += 1
    out["B_vs_A"] = {"days_both_trade": len(sd), "B_trades_overlapping_an_A_trade_in_time": simult}
    with open(P("overlap_summary.json"), "w") as f:
        json.dump(c.jsonable(out), f, indent=1)
    print(json.dumps(c.jsonable(out), indent=1))


if __name__ == "__main__":
    main()
