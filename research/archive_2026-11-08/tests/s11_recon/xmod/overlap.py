"""Overlap diagnostics with the three existing MNQ strategies (chosen_models_trades.csv) for rules A, B, C.
Holding intervals: ORB from this builder's B0 reproduction; overnight_break by re-running chosen_models'
exits_engine call (count checked against the CSV)."""
import numpy as np
import pandas as pd

import chosen_models as cm
import exits_compare as ec
import exits_engine as ee
import calendar_days as cd
import s11common as sc


def overnight_intervals():
    ds = cm.sessions()
    cash_days = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash_days)
    ec.init()
    D = ec.G["NQ"]
    t = ee.run(D, ec.G[("sets", "NQ")]["Overnight break + daily trend"], "hold", k0=2.0)
    b = t.bar.to_numpy()
    date = pd.to_datetime(D.sess[b])
    ent = D.idx[b + 1]
    ext = D.idx[b + t.hold_bars.to_numpy()] + pd.Timedelta(minutes=5)
    out = pd.DataFrame({"date": date, "dir": t.dir.to_numpy(), "t0": ent, "t1": ext})
    out = out[out.date.isin(cash_days) & ~out.date.isin(expiry)]
    after_drop, _ = cm.skip_days()
    out = out[~out.date.isin(after_drop)].reset_index(drop=True)
    return out


def minute_ts(dates, hhmm):
    return pd.DatetimeIndex([pd.Timestamp(f"{d.date()} {h}").tz_localize("America/New_York") for d, h in zip(dates, hhmm)])


def exposure(tr, side_col, ob, orb):
    """share of trades entered while the overnight break / ORB is open, same vs opposite direction."""
    ts = minute_ts(tr.date, tr.entry_time)
    d = np.where(tr[side_col] == "long", 1, -1)
    res = {}
    for name, iv in [("overnight_break", ob), ("opening_range", orb)]:
        same = opp = 0
        g = {k: v for k, v in iv.groupby("date")}
        for k in range(len(tr)):
            x = g.get(tr.date.iloc[k])
            if x is None:
                continue
            m = (x.t0 <= ts[k]) & (ts[k] < x.t1)
            if m.any():
                if (x.dir[m] == d[k]).any():
                    same += 1
                else:
                    opp += 1
        res[name] = dict(trades=int(len(tr)), while_open_same_dir=same, while_open_opposite=opp,
                         share_same=same / max(len(tr), 1), share_opposite=opp / max(len(tr), 1))
    return res


def correlations(tr, ex):
    cal = pd.DatetimeIndex(sorted(set(ex.date) | set(tr.date)))
    a = tr.groupby("date").net_usd.sum().reindex(cal, fill_value=0.0)
    out = {}
    for m, g in ex.groupby("model"):
        s = g.groupby("date").usd.sum().reindex(cal, fill_value=0.0)
        on = a.index.isin(tr.date)
        out[m] = dict(corr_all_days=float(np.corrcoef(a, s)[0, 1]), corr_on_rule_days=float(np.corrcoef(a[on], s[on])[0, 1]))
    three = ex.groupby("date").usd.sum().reindex(cal, fill_value=0.0)
    out["combined_three"] = dict(corr_all_days=float(np.corrcoef(a, three)[0, 1]),
                                 maxdd_three=sc.max_dd(three.to_numpy()), maxdd_three_plus_rule=sc.max_dd((three + a).to_numpy()),
                                 total_three=float(three.sum()), total_three_plus_rule=float((three + a).sum()))
    return out


def main():
    ex = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ob = overnight_intervals()
    n_csv = int((ex.model == "overnight_break").sum())
    print("overnight_break intervals", len(ob), "csv rows", n_csv)
    b0 = pd.read_csv(f"{sc.OUT}/trades_C_B0_orb.csv", parse_dates=["date"])
    orb = pd.DataFrame({"date": b0.date, "dir": b0.d, "t0": minute_ts(b0.date, b0.entry_time),
                        "t1": minute_ts(b0.date, b0.exit_time) + pd.Timedelta(minutes=1)})
    res = dict(overnight_interval_count=len(ob), overnight_csv_count=n_csv)
    for name in ["A", "A1-MES", "A2-VWAP", "B", "B-MES", "B1"]:
        tr = pd.read_csv(f"{sc.OUT}/trades_{name}.csv", parse_dates=["date"])
        res[name] = dict(exposure=exposure(tr, "side", ob, orb), correlation=correlations(tr, ex))
    # B vs A day overlap
    a = pd.read_csv(f"{sc.OUT}/trades_A.csv", parse_dates=["date"])
    b = pd.read_csv(f"{sc.OUT}/trades_B.csv", parse_dates=["date"])
    res["B_days_also_A"] = int(b.date.isin(a.date).sum())
    # C: how often the overnight break holds the same direction as the failed ORB during the reverse leg
    r = pd.read_csv(f"{sc.OUT}/trades_C_reverse_leg.csv", parse_dates=["date"])
    rr = r.assign(side=r.orb_side)               # direction of the failed ORB
    res["C"] = dict(overnight_same_dir_as_failed_orb_at_reverse_entry=exposure(rr, "side", ob, orb)["overnight_break"])
    sc.dump("summary_overlap.json", res)
    for k, v in res.items():
        print(k, v)


if __name__ == "__main__":
    main()
