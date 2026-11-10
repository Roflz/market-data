"""
Section 11, rule C: ORB failed-breakout stop-and-reverse (exit rule on the existing MNQ 5-min ORB). Builder Y.

B0  = the existing ORB exactly as chosen_models.opening_range builds it (cash days, expiry-Friday skip, R1, R2),
      re-simulated here bar by bar and checked against chosen_models_trades.csv (count and total $).
B1  = B0 with a plain exit at the failure signal (control book).
B2  = B0 with stop-and-reverse at the failure signal (primary).  B2 - B1 = reverse leg.
Variants: C1 calm-only reverse leg (plain exit on non-calm days); C2 reverse leg with a target at ORL-0.5W / ORH+0.5W.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s11y_common as c  # noqa: E402

TICK = c.TICK
K = 5
S_ENTRY = c.S0930 + K                   # 09:35
LAST_FAIL_CLOSE = c.slot_of(10, 59)     # last 5-min bar 10:55-10:59
S1400 = c.slot_of(14, 0)
FULL_EXIT = c.S1559                     # 15:59 close
EARLY_EXIT = c.slot_of(12, 59)          # chosen_models / lit_p5_orb early-close exit
HOLIDAY_LAST = c.slot_of(13, 5)
MIN_R = 2.5                             # lit_p5_orb.MARKETS['NQ']['min_R']
ORB_COMM_PTS = 0.5                      # $1.00 / $2 per point
REV_COST = 1.0                          # reverse leg, NQ points per round trip
USD = 2.0


def first_open_at_or_after(O, i, s, last):
    for t in range(s, last + 1):
        if not np.isnan(O[i, t]):
            return t, O[i, t]
    return None, np.nan


def orb_day(g, i, exit_slot, mode, calm, rev_target, stress_ticks=0):
    """Bar-by-bar state machine for one day.
    mode: 'B0' (baseline), 'B1' (plain exit at failure), 'B2' (stop-and-reverse).
    rev_target: True for variant C2.  calm: VIX filter for variant C1 (None = not used).
    Returns dict or None if the ORB does not trade."""
    O, H, L, Cff = g["O"], g["H"], g["L"], g["Cff"]
    oc = O[i, c.S0930]
    if np.isnan(oc) or np.isnan(O[i, S_ENTRY]):
        return None
    cc = Cff[i, S_ENTRY - 1]
    if cc == oc:
        return None
    d = 1 if cc > oc else -1
    orh = np.nanmax(H[i, c.S0930:S_ENTRY])
    orl = np.nanmin(L[i, c.S0930:S_ENTRY])
    stop = orl if d > 0 else orh
    if d * (cc + d * TICK - stop) < MIN_R:
        return None
    ref = O[i, S_ENTRY]
    fill = ref + d * TICK
    mid, W = (orh + orl) / 2.0, orh - orl
    rec = dict(d=d, orb_entry_ref=ref, orb_entry_fill=fill, orb_stop=stop, orh=orh, orl=orl, mid=mid, W=W,
               fail_slot=None, rev=None)
    if d * (fill - stop) <= 0:                                   # opened through the stop: out at once
        rec.update(orb_exit_slot=S_ENTRY, orb_exit_fill=ref - d * TICK, orb_exit="stop")
        return rec

    # ---- ORB leg -------------------------------------------------------------------------------------------
    in_orb, action_slot = True, None
    t = S_ENTRY
    while t <= exit_slot:
        if action_slot is not None and t == action_slot:
            break
        if not np.isnan(L[i, t]):
            hit = (L[i, t] <= stop) if d > 0 else (H[i, t] >= stop)
            if hit:
                px = stop
                o = O[i, t]
                if t > S_ENTRY and ((d > 0 and o < stop) or (d < 0 and o > stop)):
                    px = o
                rec.update(orb_exit_slot=t, orb_exit_fill=px - d * TICK, orb_exit="stop")
                in_orb = False
                break
        # 5-minute bar close check (only bars closing 09:39 .. 10:59; the ORB's 5-min bars start 09:35)
        if mode != "B0" and t <= LAST_FAIL_CLOSE and (t - S_ENTRY) % 5 == 4:
            close5 = g["Cff"][i, t]
            if d * (close5 - mid) < 0:
                rec["fail_slot"] = t - 4                         # stamp of the failing 5-min bar
                rec["fail_close"] = close5
                action_slot = t + 1
        t += 1
    if in_orb and action_slot is None:
        rec.update(orb_exit_slot=exit_slot, orb_exit_fill=Cff[i, exit_slot] - d * TICK, orb_exit="close")
        return rec
    if not in_orb:
        return rec

    # ---- failure action at the open of bar f+5 --------------------------------------------------------------
    a, a_open = first_open_at_or_after(O, i, action_slot, exit_slot)
    rec["action_slot"] = a
    rec["action_late_bars"] = (a - action_slot) if a is not None else None
    rec.update(orb_exit_slot=a, orb_exit_fill=a_open - d * TICK, orb_exit="failure")
    if mode == "B1" or (calm is not None and not calm):
        return rec
    # ---- reverse leg -------------------------------------------------------------------------------------
    rd = -d
    entry = a_open
    if d > 0:
        rstop = np.nanmax(H[i, S_ENTRY:a]) + 2 * TICK            # highest high entry bar .. failure bar, + 2 ticks
    else:
        rstop = np.nanmin(L[i, S_ENTRY:a]) - 2 * TICK
    tgt = (orl - 0.5 * W) if d > 0 else (orh + 0.5 * W)
    if rev_target:
        tgt = np.ceil(tgt / TICK - 1e-9) * TICK if rd > 0 else np.floor(tgt / TICK + 1e-9) * TICK
    rev = simulate_leg(g, i, a, rd, entry, rstop, tgt if rev_target else None, S1400, stress_ticks)
    rev["stop_dist"] = abs(entry - rstop)
    rev["tgt_dist"] = abs(entry - tgt) if rev_target else None
    rec["rev"] = rev
    return rec


def simulate_leg(g, i, a, rd, entry, rstop, tgt, time_exit_slot, stress_ticks=0):
    """Reverse leg from the open of bar a; exits: stop (stop-market), optional target (1-tick trade-through),
    time exit at the open of time_exit_slot. Same bar stop+target -> stop."""
    O, H, L, Cff = g["O"], g["H"], g["L"], g["Cff"]
    t = a
    while True:
        if t >= time_exit_slot:
            s2, px = first_open_at_or_after(O, i, time_exit_slot, c.S1559)
            if s2 is None:
                s2, px = c.S1559, Cff[i, c.S1559]
            return dict(entry_slot=a, entry=entry, stop=rstop, target=tgt, exit_slot=s2, exit=px, reason="time")
        if not np.isnan(L[i, t]):
            o = O[i, t]
            sh = (L[i, t] <= rstop) if rd > 0 else (H[i, t] >= rstop)
            th = False
            if tgt is not None:
                th = (H[i, t] >= tgt + TICK) if rd > 0 else (L[i, t] <= tgt - TICK)
            if sh:
                px = rstop
                if (rd > 0 and o < rstop) or (rd < 0 and o > rstop):
                    px = o
                px = px - rd * stress_ticks * TICK
                return dict(entry_slot=a, entry=entry, stop=rstop, target=tgt, exit_slot=t, exit=px, reason="stop")
            if th:
                return dict(entry_slot=a, entry=entry, stop=rstop, target=tgt, exit_slot=t, exit=tgt, reason="target")
        t += 1


def sessions(g):
    """lit_p5_orb.build_sessions logic: valid (cash session exists) and exit slot (15:59 if the 15:59 bar exists,
    else 12:59)."""
    C = g["C"][:, c.S0930:]
    present = ~np.isnan(C)
    anyp = present.any(axis=1)
    last = np.where(anyp, C.shape[1] - 1 - np.argmax(present[:, ::-1], axis=1), -1) + c.S0930
    holiday = (~anyp) | (last <= HOLIDAY_LAST)
    exit_slot = np.where(last == FULL_EXIT, FULL_EXIT, EARLY_EXIT)
    return pd.DataFrame({"date": g["dates"], "di": np.arange(len(g["dates"])), "valid": ~holiday,
                         "exit_slot": exit_slot, "last": last, "inst": g["inst"]})


def main():
    g = c.load_grid("NQ")
    ds, fomc, _ = c.calendar("NQ")
    cash = set(ds.index[ds.cash_day])
    import calendar_days as cdays
    expiry = cdays.expiry_fridays(sorted(cash))
    ctx = pd.read_pickle(os.path.join(c.PROJ, "data", "market_context.pkl"))
    after_drop = set(pd.DatetimeIndex(ctx.index[ctx.spx_ret_1d_prev <= -2.0]).normalize())
    early = set(ds.index[ds.early_close])
    vixf = c.vix_calm()
    S = sessions(g)
    S = S[S.valid & S.date.isin(cash)].reset_index(drop=True)
    S["calm"] = vixf(S.date).calm.to_numpy()

    books = {"B0": [], "B1": [], "B2": [], "C1_B2": [], "C2_B2": [], "B2_stress": []}
    rows = []
    for r in S.itertuples(index=False):
        if r.date in expiry or r.date in after_drop or r.date in fomc:       # opening_range skip set
            continue
        b0 = orb_day(g, r.di, r.exit_slot, "B0", None, False)
        if b0 is None:
            continue
        applies = (r.date not in early) and (r.exit_slot == FULL_EXIT)
        if applies:
            b1 = orb_day(g, r.di, r.exit_slot, "B1", None, False)
            b2 = orb_day(g, r.di, r.exit_slot, "B2", None, False)
            v1 = orb_day(g, r.di, r.exit_slot, "B2", bool(r.calm), False)
            v2 = orb_day(g, r.di, r.exit_slot, "B2", None, True)
            b2s = orb_day(g, r.di, r.exit_slot, "B2", None, False, stress_ticks=2)
        else:
            b1 = b2 = v1 = v2 = b2s = b0
        rows.append(dict(date=r.date, di=r.di, calm=bool(r.calm), applies=applies, b0=b0, b1=b1, b2=b2, v1=v1,
                         v2=v2, b2s=b2s, exit_slot=r.exit_slot))

    def orb_pts(rec):
        return rec["d"] * (rec["orb_exit_fill"] - rec["orb_entry_fill"]) - ORB_COMM_PTS

    def rev_pts(rec, cost=REV_COST):
        if rec.get("rev") is None:
            return None
        rv = rec["rev"]
        return -rec["d"] * (rv["exit"] - rv["entry"]), -rec["d"] * (rv["exit"] - rv["entry"]) - cost

    # ---- B0 check against chosen_models_trades.csv ---------------------------------------------------------
    b0 = pd.DataFrame([dict(date=x["date"], side="long" if x["b0"]["d"] > 0 else "short", exit=x["b0"]["orb_exit"],
                            usd=orb_pts(x["b0"]) * USD) for x in rows])
    ref = pd.read_csv(os.path.join(c.PROJ, "chosen_models_trades.csv"), parse_dates=["date"])
    ref = ref[ref.model == "opening_range"].reset_index(drop=True)
    mg = b0.merge(ref, on="date", how="outer", suffixes=("_y", "_ref"), indicator=True)
    both = mg[mg._merge == "both"]
    check = {"B0_trades": int(len(b0)), "ref_trades": int(len(ref)), "B0_total_usd": float(b0.usd.sum()),
             "ref_total_usd": float(ref.usd.sum()), "only_in_B0": int((mg._merge == "left_only").sum()),
             "only_in_ref": int((mg._merge == "right_only").sum()),
             "side_mismatch": int((both.side_y != both.side_ref).sum()),
             "exit_mismatch": int((both.exit_y != both.exit_ref).sum()),
             "usd_mismatch_gt_1c": int((np.abs(both.usd_y - both.usd_ref) > 0.01).sum())}
    check["match"] = (check["B0_trades"] == check["ref_trades"] and abs(check["B0_total_usd"] - check["ref_total_usd"]) < 0.01
                      and check["only_in_B0"] == 0 and check["only_in_ref"] == 0)
    print("B0 check:", check)

    # ---- per-trade CSVs ------------------------------------------------------------------------------------
    def leg_rows(key, cost=REV_COST):
        out = []
        for x in rows:
            rec = x[key]
            if rec.get("rev") is None:
                continue
            rv = rec["rev"]
            gross, net = rev_pts(rec, cost)
            out.append(dict(date=x["date"], entry_time=c.hhmm(rv["entry_slot"]), exit_time=c.hhmm(rv["exit_slot"]),
                            side="long" if rec["d"] < 0 else "short", entry=rv["entry"], exit=rv["exit"],
                            exit_reason=rv["reason"], gross_pts=gross, net_pts=net, net_usd=net * USD,
                            gross_usd=gross * USD, net_bp=1e4 * net / rv["entry"], gross_bp=1e4 * gross / rv["entry"],
                            stop=rv["stop"], target=rv["target"], stop_dist=rv["stop_dist"], orb_side=rec["d"],
                            orh=rec["orh"], orl=rec["orl"], mid=rec["mid"], fail_bar=c.hhmm(rec["fail_slot"]),
                            fail_close=rec["fail_close"], calm=x["calm"], action_late_bars=rec["action_late_bars"]))
        return pd.DataFrame(out)

    def book_rows(key):
        out = []
        for x in rows:
            rec = x[key]
            orbp = orb_pts(rec)
            rv = rev_pts(rec) if rec.get("rev") is not None else (0.0, 0.0)
            out.append(dict(date=x["date"], orb_side=rec["d"], orb_entry_time="09:35",
                            orb_exit_time=c.hhmm(rec["orb_exit_slot"]), orb_entry=rec["orb_entry_fill"],
                            orb_exit=rec["orb_exit_fill"], orb_exit_reason=rec["orb_exit"], orb_net_pts=orbp,
                            rev_net_pts=rv[1], day_net_pts=orbp + rv[1], day_net_usd=(orbp + rv[1]) * USD,
                            day_net_bp=1e4 * (orbp + rv[1]) / rec["orb_entry_ref"], failure=rec["fail_slot"] is not None,
                            applies=x["applies"]))
        return pd.DataFrame(out)

    rev = leg_rows("b2")
    rev_c1 = leg_rows("v1")
    rev_c2 = leg_rows("v2")
    rev_st = leg_rows("b2s")
    B = {k: book_rows(kk) for k, kk in [("B0", "b0"), ("B1", "b1"), ("B2", "b2"), ("B2_C1", "v1"), ("B2_C2", "v2"),
                                         ("B2_stress", "b2s")]}
    rev.to_csv(os.path.join(c.OUT, "C_reverse_leg_trades.csv"), index=False)
    rev_c1.to_csv(os.path.join(c.OUT, "C1_calm_reverse_leg_trades.csv"), index=False)
    rev_c2.to_csv(os.path.join(c.OUT, "C2_target_reverse_leg_trades.csv"), index=False)
    rev_st.to_csv(os.path.join(c.OUT, "C_stress_reverse_leg_trades.csv"), index=False)
    for k, v in B.items():
        v.to_csv(os.path.join(c.OUT, f"C_book_{k}.csv"), index=False)
    pd.to_pickle(rows, os.path.join(c.OUT, "C_rows.pkl"))

    # ---- random-direction control on the reverse leg ---------------------------------------------------------
    def control(key, events, subset_target):
        """Each event re-simulated in both directions with the same stop distance (and target distance)."""
        rng = np.random.default_rng(c.SEED)
        both_dirs = []
        for x in rows:
            rec = x[key]
            if rec.get("rev") is None:
                continue
            rv = rec["rev"]
            res = []
            for rd in (+1, -1):
                st = rv["entry"] - rd * rv["stop_dist"]
                tg = (rv["entry"] + rd * rv["tgt_dist"]) if subset_target else None
                leg = simulate_leg(g, x["di"], rv["entry_slot"], rd, rv["entry"], st, tg, S1400)
                gross = rd * (leg["exit"] - leg["entry"])
                res.append(1e4 * (gross - REV_COST) / leg["entry"])
            both_dirs.append(res)
        A = np.array(both_dirs)                          # n x 2 (long, short)
        n = len(A)
        coins = rng.integers(0, 2, size=(c.NREP, n))
        means = A[np.arange(n)[None, :], coins].mean(axis=1)
        return {"n": n, "p95": float(np.percentile(means, 95)), "mean": float(means.mean()),
                "p50": float(np.percentile(means, 50)), "p05": float(np.percentile(means, 5))}

    ctrl = {"C": control("b2", rev, False), "C1": control("v1", rev_c1, False), "C2": control("v2", rev_c2, True)}

    # ---- evaluation ----------------------------------------------------------------------------------------------
    def evaluate(name, R, book, ctl, t_req):
        h = c.headline(R)
        t_plain, t_nw = h["t_trade_plain"], h["t_trade_nw5"]
        t_used = min(t_plain, t_nw)
        post18 = R[R.date >= "2018-01-01"].net_usd.sum()
        post25 = R[R.date >= "2025-01-01"].net_usd.sum()
        blocks = c.by_period(R, c.BLOCKS)
        nblk = sum(1 for b in blocks if b["net_usd"] > 0)
        b0 = B["B0"].set_index("date").day_net_usd
        b2 = book.set_index("date").day_net_usd
        diff = (b2 - b0)
        crit = [
            dict(name="(i) reverse-leg event-level t >= %.1f (min of plain and NW5 t on net bp)" % t_req,
                 value=f"t_plain={t_plain:.2f}, t_nw5={t_nw:.2f}", passed=bool(t_used >= t_req)),
            dict(name="(ii) reverse-leg net $ > 0 Jan2018-latest", value=f"${post18:,.0f} (Jan2025-latest ${post25:,.0f}, report)",
                 passed=bool(post18 > 0)),
            dict(name="(iii) net > 0 in >= 6 of 8 two-year blocks", value=f"{nblk}/8", passed=bool(nblk >= 6)),
            dict(name="(iv) mean net bp > random-direction 95th pct", value=f"{h['net_bp_per_trade']:.2f} vs p95 {ctl['p95']:.2f}",
                 passed=bool(h["net_bp_per_trade"] > ctl["p95"])),
            dict(name="(v) book: mean daily (B2-B0) > 0 and maxDD(B2) <= maxDD(B0)",
                 value=f"mean diff ${diff.mean():.3f}/day; maxDD B2 ${c.max_dd(b2.to_numpy()):,.0f} vs B0 ${c.max_dd(b0.to_numpy()):,.0f}",
                 passed=bool(diff.mean() > 0 and c.max_dd(b2.to_numpy()) <= c.max_dd(b0.to_numpy()))),
        ]
        return dict(rule=name, headline=h, criteria=crit, passed=all(x["passed"] for x in crit), blocks=blocks,
                    eras=c.by_period(R, c.ERAS), control=ctl, post2018_usd=float(post18), post2025_usd=float(post25),
                    book_mean_daily_diff_vs_B0=float(diff.mean()), book_total=float(b2.sum()))

    res = {"B0_check": check}
    res["C"] = evaluate("C", rev, B["B2"], ctrl["C"], 2.0)
    res["C1"] = evaluate("C1", rev_c1, B["B2_C1"], ctrl["C1"], 2.4)
    res["C2"] = evaluate("C2", rev_c2, B["B2_C2"], ctrl["C2"], 2.4)
    res["C_stress_report"] = c.headline(rev_st)
    b0d = B["B0"].set_index("date").day_net_usd
    books_sum = {}
    for k, v in B.items():
        dd = v.set_index("date").day_net_usd
        books_sum[k] = {"days": int(len(dd)), "total_usd": float(dd.sum()), "mean_daily_usd": float(dd.mean()),
                        "max_dd_usd": c.max_dd(dd.to_numpy()), "mean_daily_minus_B0": float((dd - b0d).mean()),
                        "total_minus_B0": float((dd - b0d).sum())}
    res["books"] = books_sum
    b1d = B["B1"].set_index("date").day_net_usd
    res["B1_minus_B0_by_block"] = [{"block": n, "usd": float((b1d - b0d)[(b0d.index >= a) & (b0d.index <= z)].sum())}
                                   for n, a, z in c.BLOCKS]
    fails = B["B1"][B["B1"].failure]
    res["failure_days"] = int(len(fails))
    res["failure_days_with_late_action_bar"] = int((rev.action_late_bars > 0).sum()) if len(rev) else 0
    res["applies_days"] = int(B["B0"].applies.sum())
    with open(os.path.join(c.OUT, "C_summary.json"), "w") as f:
        json.dump(c.jsonable(res), f, indent=1, default=str)
    for k in ("C", "C1", "C2"):
        h = res[k]["headline"]
        print(k, h["trades"], f"${h['net_usd_per_trade']:.2f}/tr total ${h['total_usd']:,.0f} bp {h['net_bp_per_trade']:.2f}",
              "PASS" if res[k]["passed"] else "FAIL", [(x["value"], x["passed"]) for x in res[k]["criteria"]])
    print(json.dumps(c.jsonable(books_sum), indent=1))


if __name__ == "__main__":
    os.chdir(c.PROJ)
    main()
