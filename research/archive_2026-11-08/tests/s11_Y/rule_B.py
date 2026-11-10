"""
Section 11, rule B: midday drift-burst fade. Primary = NQ/MNQ (change note), variant B-MES (ES), B1 long-only
(MNQ primary instrument; B1-MES also reported). Builder Y.
Controls: C1 random direction (1,000 reps); C2 (diagnostic) entry at the arming bar; B1 drift control (random long
entries, same window, 15-min hold, stop distances drawn from the B1 events' M distribution).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402

TICK = c.TICK
ARM_FIRST, ARM_LAST = c.slot_of(10, 29), c.slot_of(14, 29)
ENTRY_LAST = c.slot_of(14, 30)
HOLD = 15
KD = np.exp(-np.arange(30) / 5.0)
KV = np.exp(-np.arange(120) / 25.0)
KV_NORM = KV.sum()
KD2 = np.exp(-2.0 * np.arange(30) / 5.0).sum()
CV = 4.0


def burst_stat(Cff_row):
    """T_t for every slot of one day (08:00 .. 15:59), from 1-min log returns of forward-filled closes.
    r at 08:00 = 0 (series starts 08:00), a missing bar gives r = 0. Uses only closes up to bar t."""
    p = Cff_row.copy()
    r = np.zeros(c.NSLOT)
    ok = ~np.isnan(p)
    lp = np.where(ok, np.log(np.where(ok, p, 1.0)), np.nan)
    rr = np.diff(lp)
    r[1:] = np.where(np.isnan(rr), 0.0, rr)
    Dt = np.zeros(c.NSLOT)
    Vt = np.zeros(c.NSLOT)
    for t in range(c.NSLOT):
        j = np.arange(min(30, t + 1))
        Dt[t] = (KD[j] * r[t - j]).sum()
        j2 = np.arange(min(120, t + 1))
        Vt[t] = (KV[j2] * r[t - j2] ** 2).sum() / KV_NORM
    with np.errstate(divide="ignore", invalid="ignore"):
        Tt = np.where(Vt > 0, Dt / np.sqrt(Vt * KD2), 0.0)
    return Tt


def eligible_days(g):
    ds, fomc, opex = c.calendar("NQ")
    dates = g["dates"]
    D = pd.DataFrame({"date": dates, "di": np.arange(len(dates))})
    full = D.date.isin(ds.index[ds.cash_day & ~ds.early_close]) & ~np.isnan(g["O"][:, c.S0930])
    D["eligible"] = full & ~D.date.isin(fomc) & ~D.date.isin(opex)
    D["calm"] = c.vix_calm()(D.date).calm.to_numpy()
    return D


def find_events(g, D):
    """Explicit per-day scan: first arming in 10:29-14:29, then the peak, then the entry bar."""
    Cff, O = g["Cff"], g["O"]
    ev = []
    stats_cache = {}
    for r in D[D.eligible].itertuples(index=False):
        i = r.di
        Tt = burst_stat(Cff[i])
        stats_cache[i] = Tt
        arm = None
        for t in range(ARM_FIRST, ARM_LAST + 1):
            if abs(Tt[t]) >= CV:
                arm = t
                break
        if arm is None:
            continue
        s = int(np.sign(Tt[arm]))
        tp = None
        for t2 in range(arm + 1, c.NSLOT):
            if s * Tt[t2] < s * Tt[t2 - 1]:
                tp = t2
                break
        rec = dict(date=r.date, di=i, calm=r.calm, arm_slot=arm, arm_T=Tt[arm], s=s, peak_slot=None, entry_slot=None)
        # C2 diagnostic: entry at the open of the bar after the arming bar, M from the arming bar
        rec["c2_entry_slot"] = arm + 1
        rec["c2_M"] = abs(Cff[i, arm] - Cff[i, arm - 5])
        if tp is not None:
            p = tp - 1
            e = tp + 1
            rec.update(peak_slot=p, peak_T=Tt[p], tprime=tp)
            if e <= ENTRY_LAST:
                rec["entry_slot"] = e
                rec["M"] = abs(Cff[i, p] - Cff[i, p - 5])
                rec["pre_bp"] = 1e4 * np.log(Cff[i, p] / Cff[i, p - 5])
                rec["pre_bp_arm"] = 1e4 * np.log(Cff[i, arm] / Cff[i, arm - 5])
        ev.append(rec)
    return pd.DataFrame(ev), stats_cache


def run_trade(g, i, e, d, M, stress_ticks=0):
    """Bar-by-bar: entry at open of bar e; stop-market at entry -/+ M (gap -> open); time exit at open of e+15."""
    O, H, L = g["O"], g["H"], g["L"]
    entry = O[i, e]
    stop = entry - d * M
    t = e
    while True:
        if t >= e + HOLD:
            s2 = t
            while s2 <= c.S1559 and np.isnan(O[i, s2]):
                s2 += 1
            o = O[i, s2]
            # time exit due; if that open is beyond the stop it is a stop fill at the open (same price, label stop)
            if (d > 0 and o <= stop) or (d < 0 and o >= stop):
                return dict(entry=entry, stop=stop, exit_slot=s2, exit=o - d * stress_ticks * TICK, reason="stop")
            return dict(entry=entry, stop=stop, exit_slot=s2, exit=o, reason="time15")
        if not np.isnan(L[i, t]):
            hit = (L[i, t] <= stop) if d > 0 else (H[i, t] >= stop)
            if hit:
                o = O[i, t]
                px = o if ((d > 0 and o < stop) or (d < 0 and o > stop)) else stop
                return dict(entry=entry, stop=stop, exit_slot=t, exit=px - d * stress_ticks * TICK, reason="stop")
        t += 1


def trades_from_events(g, E, sym, which="main", only_side=None, stress_ticks=0):
    cost, usd = c.SPEC[sym]["cost_pts"], c.SPEC[sym]["usd"]
    rows, skipped = [], 0
    for r in E.itertuples(index=False):
        if which == "main":
            if pd.isna(r.entry_slot):
                continue
            e, M = int(r.entry_slot), r.M
        else:
            e, M = int(r.c2_entry_slot), r.c2_M
        d = -int(r.s)
        if only_side is not None and d != only_side:
            continue
        if np.isnan(g["O"][r.di, e]):
            skipped += 1
            continue
        x = run_trade(g, r.di, e, d, M, stress_ticks)
        gross = d * (x["exit"] - x["entry"])
        net = gross - cost
        rows.append(dict(date=r.date, di=r.di, entry_time=c.hhmm(e), exit_time=c.hhmm(x["exit_slot"]), entry_slot=e,
                         exit_slot=x["exit_slot"], side="long" if d > 0 else "short", dir=d, entry=x["entry"],
                         exit=x["exit"], exit_reason=x["reason"], gross_pts=gross, net_pts=net, gross_usd=gross * usd,
                         net_usd=net * usd, gross_bp=1e4 * gross / x["entry"], net_bp=1e4 * net / x["entry"],
                         stop=x["stop"], M=M, burst_sign=int(r.s), arm_time=c.hhmm(r.arm_slot), arm_T=r.arm_T,
                         peak_time=c.hhmm(r.peak_slot) if not pd.isna(r.peak_slot) else None,
                         pre_bp=getattr(r, "pre_bp", np.nan), calm=bool(r.calm)))
    return pd.DataFrame(rows), skipped


def random_dir_control(g, T_, sym):
    cost = c.SPEC[sym]["cost_pts"]
    A = np.zeros((len(T_), 2))
    for k, r in enumerate(T_.itertuples(index=False)):
        for j, d in enumerate((+1, -1)):
            x = run_trade(g, r.di, r.entry_slot, d, r.M)
            A[k, j] = 1e4 * (d * (x["exit"] - x["entry"]) - cost) / x["entry"]
    rng = np.random.default_rng(c.SEED)
    coins = rng.integers(0, 2, size=(c.NREP, len(A)))
    means = A[np.arange(len(A))[None, :], coins].mean(axis=1)
    return {"n": int(len(A)), "p95": float(np.percentile(means, 95)), "p50": float(np.percentile(means, 50)),
            "p05": float(np.percentile(means, 5)), "mean": float(means.mean())}


def drift_control(g, D, T_, sym):
    """B1 drift check: per replication, N random long entries (N = B1 trade count) on eligible days at random
    entry bars in the B entry window (10:31 .. 14:30), 15-min hold, stop distance M drawn from the B1 events'
    M distribution expressed as a fraction of the price at the peak (rescaled to the entry price, snapped down
    to a tick, minimum 1 tick)."""
    cost = c.SPEC[sym]["cost_pts"]
    rng = np.random.default_rng(c.SEED)
    days = D[D.eligible].di.to_numpy()
    mfrac = (T_.M / T_.entry).to_numpy()
    n = len(T_)
    lo_e, hi_e = c.slot_of(10, 31), ENTRY_LAST
    means = np.zeros(c.NREP)
    for rep in range(c.NREP):
        vals = []
        while len(vals) < n:
            i = int(rng.choice(days))
            e = int(rng.integers(lo_e, hi_e + 1))
            mf = float(rng.choice(mfrac))
            if np.isnan(g["O"][i, e]):
                continue
            M = max(TICK, np.floor(mf * g["O"][i, e] / TICK) * TICK)
            x = run_trade(g, i, e, +1, M)
            vals.append(1e4 * ((x["exit"] - x["entry"]) - cost) / x["entry"])
        means[rep] = np.mean(vals)
    return {"n_per_rep": n, "p95": float(np.percentile(means, 95)), "p50": float(np.percentile(means, 50)),
            "p05": float(np.percentile(means, 5)), "mean": float(means.mean())}


def evaluate(name, T_, ctl, t_req, extra_ctl=None):
    h = c.headline(T_)
    t_used = min(h["t_trade_plain"], h["t_trade_nw5"])
    post18 = float(T_[T_.date >= "2018-01-01"].net_usd.sum())
    blocks = c.by_period(T_, c.BLOCKS)
    nblk = sum(1 for b in blocks if b["net_usd"] > 0)
    crit = [dict(name="(cal) >= 200 events in total (else underpowered = fail)", value=f"{len(T_)}", passed=bool(len(T_) >= 200)),
            dict(name=f"(i) event-level t >= {t_req} (min of plain and NW5 on net bp)",
                 value=f"t_plain={h['t_trade_plain']:.2f}, t_nw5={h['t_trade_nw5']:.2f}", passed=bool(t_used >= t_req)),
            dict(name="(ii) net $ > 0 Jan2018-latest", value=f"${post18:,.0f}", passed=bool(post18 > 0)),
            dict(name="(iii) net > 0 in >= 6 of 8 blocks", value=f"{nblk}/8", passed=bool(nblk >= 6)),
            dict(name="(iv) mean net bp > C1 95th pct", value=f"{h['net_bp_per_trade']:.2f} vs p95 {ctl['p95']:.2f}",
                 passed=bool(h["net_bp_per_trade"] > ctl["p95"]))]
    if extra_ctl is not None:
        crit.append(dict(name="(iv-b) mean net bp > drift-control 95th pct (B1 only)",
                         value=f"{h['net_bp_per_trade']:.2f} vs p95 {extra_ctl['p95']:.2f}",
                         passed=bool(h["net_bp_per_trade"] > extra_ctl["p95"])))
    return dict(rule=name, headline=h, criteria=crit, passed=all(x["passed"] for x in crit), blocks=blocks,
                eras=c.by_period(T_, c.ERAS), pre2018=c.by_period(T_, [("2010-2017", "2010-01-01", "2017-12-31"),
                                                                        ("2018-latest", "2018-01-01", "2026-12-31")]),
                control_C1=ctl, drift_control=extra_ctl, post2018_usd=post18)


def splits(T_):
    out = {}
    for nm, m in [("calm", T_.calm), ("not_calm", ~T_.calm), ("negative_burst_long", T_.burst_sign < 0),
                  ("positive_burst_short", T_.burst_sign > 0)]:
        out[nm] = c.headline(T_[m])
    q = T_.M.quantile(0.9)
    out["without_top10pct_M_points"] = c.headline(T_[T_.M <= q])
    out["top10pct_M_points_only"] = c.headline(T_[T_.M > q])
    out["top10pct_M_threshold_pts"] = float(q)
    return out


def main():
    res = {}
    for sym, name in [("NQ", "B"), ("ES", "B-MES")]:
        g = c.load_grid(sym)
        D = eligible_days(g)
        E, _ = find_events(g, D)
        E.to_csv(os.path.join(c.OUT, f"{name}_events_all_armings.csv"), index=False)
        T_, sk = trades_from_events(g, E, sym)
        T_.to_csv(os.path.join(c.OUT, f"{name}_trades.csv"), index=False)
        ctl = random_dir_control(g, T_, sym)
        ev = evaluate(name, T_, ctl, 2.0 if name == "B" else 2.4)
        cal = {"eligible_days": int(D.eligible.sum()), "armings": int(len(E)),
               "armings_neg": int((E.s < 0).sum()), "armings_pos": int((E.s > 0).sum()),
               "no_peak_found": int(E.peak_slot.isna().sum()),
               "peak_too_late_no_trade": int((E.peak_slot.notna() & E.entry_slot.isna()).sum()),
               "trades": int(len(T_)), "missing_entry_bar_skips": sk,
               "mean_pre_burst_bp_negative": float(T_[T_.burst_sign < 0].pre_bp.mean()),
               "mean_pre_burst_bp_positive": float(T_[T_.burst_sign > 0].pre_bp.mean()),
               "n_negative": int((T_.burst_sign < 0).sum()), "n_positive": int((T_.burst_sign > 0).sum()),
               "source_ES_means_bp": "-37.39 (neg) / +36.41 (pos)", "events_per_year": ev["headline"]["trades_per_year"]}
        ev["calibration"] = cal
        ev["splits_report"] = splits(T_)
        Ts, _ = trades_from_events(g, E, sym, stress_ticks=2)
        Ts.to_csv(os.path.join(c.OUT, f"{name}_stress_trades.csv"), index=False)
        ev["stress_report"] = c.headline(Ts)
        T2, _ = trades_from_events(g, E, sym, which="c2")
        T2.to_csv(os.path.join(c.OUT, f"{name}_C2_arming_entry_trades.csv"), index=False)
        ev["C2_arming_entry_report"] = dict(headline=c.headline(T2), blocks=c.by_period(T2, c.BLOCKS))
        res[name] = ev
        # B1 long-only (negative bursts only; first arming of the day only)
        nm1 = "B1" if sym == "NQ" else "B1-MES"
        T1, _ = trades_from_events(g, E, sym, only_side=+1)
        T1.to_csv(os.path.join(c.OUT, f"{nm1}_trades.csv"), index=False)
        ctl1 = random_dir_control(g, T1, sym)
        dc = drift_control(g, D, T1, sym)
        ev1 = evaluate(nm1, T1, ctl1, 2.4, extra_ctl=dc)
        res[nm1] = ev1
        for nm, e_ in [(name, ev), (nm1, ev1)]:
            h = e_["headline"]
            print(nm, sym, h["trades"], f"${h['net_usd_per_trade']:.2f}/tr total ${h['total_usd']:,.0f} bp {h['net_bp_per_trade']:.2f}",
                  "PASS" if e_["passed"] else "FAIL", [(x["value"], x["passed"]) for x in e_["criteria"]])
        print("  calibration", cal)
    with open(os.path.join(c.OUT, "B_summary.json"), "w") as f:
        json.dump(c.jsonable(res), f, indent=1, default=str)


if __name__ == "__main__":
    os.chdir(c.PROJ)
    main()
