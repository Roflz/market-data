"""
Section 11, rule A: calm-day 60-minute fade (MNQ primary), A1 (ES/MES), A2 (VWAP trigger, MNQ). Builder Y.
Controls: C1 random direction (1,000 reps, seed 12345); C2 (report only) the fade on full days failing VIX or H1.
Stress (report only): +2 ticks on stop fills.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402

TICK = c.TICK
DEC = [c.slot_of(h, m) for h, m in [(11, 0), (11, 30), (12, 0), (12, 30), (13, 0), (13, 30), (14, 0)]]


def snap_tgt(x, d):
    return np.ceil(x / TICK - 1e-9) * TICK if d > 0 else np.floor(x / TICK + 1e-9) * TICK


def snap_stop(x, d):
    return np.floor(x / TICK + 1e-9) * TICK if d > 0 else np.ceil(x / TICK - 1e-9) * TICK


def day_table(sym):
    """Per-date inputs: full-day flag, eligibility flags, H1, H1 median (prior 20 full days), s60(T) and
    S(T) for VWAP (prior 14 full days), VWAP and P at each decision time."""
    g = c.load_grid(sym)
    ds, fomc, opex = c.calendar("NQ")         # NYSE calendar flags (same for ES and NQ)
    dates = g["dates"]
    D = pd.DataFrame({"date": dates, "di": np.arange(len(dates))})
    D["cash"] = D.date.isin(ds.index[ds.cash_day])
    D["early"] = D.date.isin(ds.index[ds.early_close])
    O, H, L, Cff, V = g["O"], g["H"], g["L"], g["Cff"], g["V"]
    has_rth = ~np.isnan(O[:, c.S0930])
    D["full"] = D.cash & ~D.early & has_rth
    D["fomc"] = D.date.isin(fomc)
    D["opex"] = D.date.isin(opex)
    D["h1"] = (np.nanmax(H[:, c.S0930:c.S1030], axis=1) - np.nanmin(L[:, c.S0930:c.S1030], axis=1)) / O[:, c.S0930]
    # r60 and |P - VWAP| at each decision time (prices known at T = close of bar T-1, forward filled)
    tp = (H + L + g["C"]) / 3.0
    for T in DEC:
        p, p60 = Cff[:, T - 1], Cff[:, T - 61]
        D[f"r60_{T}"] = np.log(p / p60)
        D[f"P_{T}"] = p
        D[f"dP_{T}"] = p - p60
        w = np.where(np.isnan(V[:, c.S0930:T]) | np.isnan(tp[:, c.S0930:T]), 0.0, V[:, c.S0930:T])
        tpv = np.where(w > 0, tp[:, c.S0930:T], 0.0)
        vw = (w * tpv).sum(axis=1) / np.where(w.sum(axis=1) > 0, w.sum(axis=1), np.nan)
        D[f"vwap_{T}"] = vw
        D[f"dev_{T}"] = np.abs(p - vw)
    # trailing stats over prior N full trading days (rows with full == True, NaN values skipped)
    F = D[D.full].copy()
    def prior(col, n, fn):
        vals = F[col].to_numpy()
        out = np.full(len(F), np.nan)
        ok = []                                                 # non-NaN values of strictly prior full days
        for k in range(len(F)):
            if len(ok) >= n:
                out[k] = fn(np.array(ok[-n:]))
            if not np.isnan(vals[k]):
                ok.append(vals[k])
        return pd.Series(out, index=F.index)
    D["h1_med20"] = prior("h1", 20, np.median)
    for T in DEC:
        D[f"s60_{T}"] = prior(f"r60_{T}", 20, lambda a: np.sqrt(np.mean(a ** 2)))
        D[f"S_{T}"] = prior(f"dev_{T}", 14, np.mean)
    vix = c.vix_calm()(D.date)
    D["vix_prev"] = vix.vix_prev.to_numpy()
    D["vix_med252"] = vix.vix_med252.to_numpy()
    D["calm_vix"] = vix.calm.to_numpy()
    D["calm_h1"] = D.h1 <= D.h1_med20
    D["base_ok"] = D.full & ~D.fomc & ~D.opex & D.h1_med20.notna() & D[f"s60_{DEC[0]}"].notna()
    D["eligible"] = D.base_ok & D.calm_vix & D.calm_h1
    D["c2_days"] = D.base_ok & ~(D.calm_vix & D.calm_h1)
    return g, D


def run_trade(g, i, T, d, entry, stop, tgt, stress_ticks=0):
    """Bar-by-bar state machine from the open of bar T. Exits: (c) open of bar T+60, (d) open of 15:00 bar,
    (b) stop-market (gap -> bar open), (a) target limit needing a 1-tick trade-through. Stop wins ties."""
    O, H, L = g["O"], g["H"], g["L"]
    t = T
    t_exit = min(T + 60, c.S1500)
    while True:
        if t >= t_exit:                                         # time exits are processed at the bar open
            s2 = t
            while s2 <= c.S1559 and np.isnan(O[i, s2]):
                s2 += 1
            if s2 > c.S1559:
                return dict(exit_slot=c.S1559, exit=g["Cff"][i, c.S1559], reason="time_fallback")
            return dict(exit_slot=s2, exit=O[i, s2], reason="time60" if t_exit == T + 60 else "flat1500")
        if not np.isnan(L[i, t]):
            o = O[i, t]
            stop_hit = (L[i, t] <= stop) if d > 0 else (H[i, t] >= stop)
            tgt_hit = (H[i, t] >= tgt + TICK) if d > 0 else (L[i, t] <= tgt - TICK)
            if stop_hit:
                px = o if ((d > 0 and o < stop) or (d < 0 and o > stop)) else stop
                return dict(exit_slot=t, exit=px - d * stress_ticks * TICK, reason="stop")
            if tgt_hit:
                return dict(exit_slot=t, exit=tgt, reason="target")
        t += 1


def run_rule(sym, g, D, days_col, trigger, stress_ticks=0):
    """Explicit day loop, decision times in order, one position at a time."""
    O = g["O"]
    cost = c.SPEC[sym]["cost_pts"]
    usd = c.SPEC[sym]["usd"]
    out = []
    skipped_missing_entry = 0
    for r in D[D[days_col]].itertuples(index=False):
        i = r.di
        free_from = -1                                          # first slot at which we are flat again
        for T in DEC:
            if T < free_from:                                   # still in a position at T -> not checked
                continue
            P = getattr(r, f"P_{T}")
            if trigger == "r60":
                r60, s60, dP = getattr(r, f"r60_{T}"), getattr(r, f"s60_{T}"), getattr(r, f"dP_{T}")
                if np.isnan(r60) or np.isnan(s60) or abs(r60) < 1.0 * s60 or dP == 0:
                    continue
                d = -int(np.sign(dP))
                dist = abs(dP)
                tgt_raw = P - 0.5 * dP
                sig = dict(r60=r60, s60=s60, dP=dP)
            else:                                               # A2: VWAP trigger
                vw, S = getattr(r, f"vwap_{T}"), getattr(r, f"S_{T}")
                if np.isnan(vw) or np.isnan(S) or abs(P - vw) < 2.0 * S or P == vw:
                    continue
                d = int(np.sign(vw - P))
                dist = abs(P - vw)
                tgt_raw = vw
                sig = dict(vwap=vw, S=S, dev=P - vw)
            entry = O[i, T]
            if np.isnan(entry):
                skipped_missing_entry += 1
                continue
            stop = snap_stop(entry - d * dist, d)
            tgt = snap_tgt(tgt_raw, d)
            x = run_trade(g, i, T, d, entry, stop, tgt, stress_ticks)
            gross = d * (x["exit"] - entry)
            net = gross - cost
            out.append(dict(date=r.date, di=i, entry_time=c.hhmm(T), exit_time=c.hhmm(x["exit_slot"]),
                            entry_slot=T, exit_slot=x["exit_slot"], side="long" if d > 0 else "short", dir=d,
                            entry=entry, exit=x["exit"], exit_reason=x["reason"], gross_pts=gross, net_pts=net,
                            gross_usd=gross * usd, net_usd=net * usd, gross_bp=1e4 * gross / entry,
                            net_bp=1e4 * net / entry, P_T=P, stop=stop, target=tgt, stop_dist=abs(entry - stop),
                            tgt_dist_from_P=abs(tgt - P), vix_prev=r.vix_prev, h1=r.h1, h1_med20=r.h1_med20, **sig))
            free_from = x["exit_slot"] if x["reason"] != "stop" and x["reason"] != "target" else x["exit_slot"] + 1
    return pd.DataFrame(out), skipped_missing_entry


def random_direction_control(g, T_, trigger, sym):
    """C1: same entry bars, same target/stop distances (target measured from P(T), stop from entry), same time
    exits; direction by a fair coin. Both directions simulated once per trade, then 1,000 coin draws."""
    cost = c.SPEC[sym]["cost_pts"]
    A = np.zeros((len(T_), 2))
    for k, r in enumerate(T_.itertuples(index=False)):
        for j, d in enumerate((+1, -1)):
            if trigger == "r60":
                tgt_raw = r.P_T + d * 0.5 * abs(r.dP)
                dist = abs(r.dP)
            else:
                tgt_raw = r.P_T + d * abs(r.dev)
                dist = abs(r.dev)
            stop = snap_stop(r.entry - d * dist, d)
            tgt = snap_tgt(tgt_raw, d)
            x = run_trade(g, r.di, r.entry_slot, d, r.entry, stop, tgt)
            A[k, j] = 1e4 * (d * (x["exit"] - r.entry) - cost) / r.entry
    rng = np.random.default_rng(c.SEED)
    coins = rng.integers(0, 2, size=(c.NREP, len(A)))
    means = A[np.arange(len(A))[None, :], coins].mean(axis=1)
    return {"n": int(len(A)), "p95": float(np.percentile(means, 95)), "p50": float(np.percentile(means, 50)),
            "p05": float(np.percentile(means, 5)), "mean": float(means.mean())}


def evaluate(name, T_, ctl, t_req):
    h = c.headline(T_)
    day = T_.groupby("date").net_bp.sum()
    t_day = c.nw_t(day.to_numpy())
    post25 = float(T_[T_.date >= "2025-01-01"].net_usd.sum())
    blocks = c.by_period(T_, c.BLOCKS)
    nblk = sum(1 for b in blocks if b["net_usd"] > 0)
    crit = [dict(name=f"(i) day-level NW5 t on daily net bp >= {t_req}", value=f"{t_day:.2f}", passed=bool(t_day >= t_req)),
            dict(name="(ii) total net $ > 0 Jan2025-latest", value=f"${post25:,.0f}", passed=bool(post25 > 0)),
            dict(name="(iii) net > 0 in >= 6 of 8 blocks", value=f"{nblk}/8", passed=bool(nblk >= 6)),
            dict(name="(iv) mean net bp/trade > C1 95th pct", value=f"{h['net_bp_per_trade']:.2f} vs p95 {ctl['p95']:.2f}",
                 passed=bool(h["net_bp_per_trade"] > ctl["p95"]))]
    return dict(rule=name, headline=h, t_day_nw5=t_day, criteria=crit, passed=all(x["passed"] for x in crit),
                blocks=blocks, eras=c.by_period(T_, c.ERAS), control_C1=ctl, post2025_usd=post25,
                pts_per_trade_by_era={e["period"]: e["net_pts_per_trade"] for e in c.by_period(T_, c.ERAS)})


def main():
    res = {}
    for sym, name, trig, t_req in [("NQ", "A", "r60", 2.0), ("ES", "A1", "r60", 2.4), ("NQ", "A2", "r60x", 2.4)]:
        g, D = day_table(sym)
        trigger = "r60" if trig == "r60" else "vwap"
        T_, miss = run_rule(sym, g, D, "eligible", trigger)
        T_.to_csv(os.path.join(c.OUT, f"{name}_trades.csv"), index=False)
        ctl = random_direction_control(g, T_, trigger, sym)
        ev = evaluate(name, T_, ctl, t_req)
        ev["eligible_days"] = int(D.eligible.sum())
        ev["base_days"] = int(D.base_ok.sum())
        ev["missing_entry_bar_skips"] = miss
        Ts, _ = run_rule(sym, g, D, "eligible", trigger, stress_ticks=2)
        Ts.to_csv(os.path.join(c.OUT, f"{name}_stress_trades.csv"), index=False)
        ev["stress_report"] = c.headline(Ts)
        T2, _ = run_rule(sym, g, D, "c2_days", trigger)
        T2.to_csv(os.path.join(c.OUT, f"{name}_C2_uncalm_trades.csv"), index=False)
        ev["C2_report_uncalm_days"] = dict(headline=c.headline(T2), blocks=c.by_period(T2, c.BLOCKS),
                                           t_day_nw5=c.nw_t(T2.groupby("date").net_bp.sum().to_numpy()))
        res[name] = ev
        h = ev["headline"]
        print(name, sym, h["trades"], f"${h['net_usd_per_trade']:.2f}/tr total ${h['total_usd']:,.0f} bp {h['net_bp_per_trade']:.2f} tday {ev['t_day_nw5']:.2f}",
              "PASS" if ev["passed"] else "FAIL", [(x["value"], x["passed"]) for x in ev["criteria"]], "missing", miss)
        if name == "A":
            D.to_pickle(os.path.join(c.OUT, "A_day_table.pkl"))
    with open(os.path.join(c.OUT, "A_summary.json"), "w") as f:
        json.dump(c.jsonable(res), f, indent=1, default=str)


if __name__ == "__main__":
    os.chdir(c.PROJ)
    main()
