"""Section 11 rule C: failed-breakout stop-and-reverse on the existing MNQ 5-min ORB (chosen_models.opening_range).
B0 = baseline ORB reproduced (vectorized) from lit_p5_orb arrays exactly as chosen_models builds it, checked against
chosen_models_trades.csv. B1 = plain exit at the failure signal. B2 = stop-and-reverse. Variants C1 (calm-only
reverse leg), C2 (reverse leg with target)."""
import numpy as np
import pandas as pd

import calendar_days as cd
import chosen_models as cm
import lit_p5_orb as p5
import s11common as sc
import simlib as sl

K = 5
REV_EXIT = 270          # 14:00 bar in p5 slots (slot 0 = 09:30)
PPT = 2.0


def load():
    ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
    cash_days = ds.index[ds.cash_day]
    expiry = cd.expiry_fridays(cash_days)
    dates, g, inst = p5.load_market("NQ")
    sess, Cff, _ = p5.build_sessions("NQ", dates, g, inst)
    sess = sess[sess.date.isin(cash_days)].reset_index(drop=True)
    return ds, expiry, g, Cff, sess


def baseline(ds, expiry, g, Cff, sess):
    O, H, L = g["Open"], g["High"], g["Low"]
    i = sess.di.to_numpy()
    ns = O.shape[1]
    keep = ~sess.date.isin(expiry).to_numpy() & ~np.isnan(O[i, 0]) & ~np.isnan(O[i, K])
    oc, cc = O[i, 0], Cff[i, K - 1]
    keep &= cc != oc
    d = np.where(cc > oc, 1, -1)
    orh, orl = np.nanmax(H[i, :K], 1), np.nanmin(L[i, :K], 1)
    stop = np.where(d > 0, orl, orh)
    keep &= ~(d * (cc + d * p5.TICK - stop) < p5.MARKETS["NQ"]["min_R"])
    ref = O[i, K]
    fill = ref + d * p5.TICK
    s_x = sess.exit_slot.to_numpy()
    at_once = d * (fill - stop) <= 0
    cols = np.arange(ns)[None, :]
    win = (cols >= K) & (cols <= s_x[:, None])
    with np.errstate(invalid="ignore"):
        sh = np.where(d[:, None] > 0, L[i] <= stop[:, None], H[i] >= stop[:, None]) & win
    hs = sh.any(1)
    i_s = sh.argmax(1)
    o_s = O[i, i_s]
    gapped = (i_s > K) & ~np.isnan(o_s) & np.where(d > 0, o_s < stop, o_s > stop)
    sref = np.where(gapped, o_s, stop)
    xs = np.where(at_once, K, np.where(hs, i_s, s_x))
    xref = np.where(at_once, ref, np.where(hs, sref, Cff[i, s_x]))
    why = np.where(at_once | hs, "stop", "close")
    xfill = xref - d * p5.TICK
    net = d * (xfill - fill) - p5.COMM / PPT
    B0 = pd.DataFrame({"date": sess.date, "di": i, "d": d, "orh": orh, "orl": orl, "stop": stop, "ref": ref,
                       "fill": fill, "xs": xs, "xref": xref, "why": why, "net_pts": net, "usd": net * PPT,
                       "bp": 1e4 * net / ref, "exit_slot_day": s_x})[keep].reset_index(drop=True)
    after_drop, fed = cm.skip_days()
    B0 = B0[~B0.date.isin(after_drop) & ~B0.date.isin(fed)].reset_index(drop=True)
    return B0


def check_b0(B0):
    ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ref = ref[ref.model == "opening_range"].reset_index(drop=True)
    m = ref.merge(B0[["date", "usd", "why", "bp"]], on="date", how="outer", indicator=True)
    both = m[m._merge == "both"]
    res = dict(csv_count=int(len(ref)), b0_count=int(len(B0)), csv_total_usd=float(ref.usd.sum()),
               b0_total_usd=float(B0.usd.sum()), only_csv=int((m._merge == "left_only").sum()),
               only_b0=int((m._merge == "right_only").sum()),
               max_abs_usd_diff=float((both.usd_x - both.usd_y).abs().max()),
               exit_label_mismatch=int((both.exit != both.why).sum()))
    res["match"] = bool(res["csv_count"] == res["b0_count"] and abs(res["csv_total_usd"] - res["b0_total_usd"]) < 1e-6
                        and res["only_csv"] == 0 and res["only_b0"] == 0 and res["max_abs_usd_diff"] < 1e-9)
    return res


def failure(B0, g, Cff, ds):
    """failure test on 5-min bars 9:35..10:55; action slot f+5; returns event table."""
    H, L = g["High"], g["Low"]
    i = B0.di.to_numpy()
    d = B0.d.to_numpy()
    mid = (B0.orh.to_numpy() + B0.orl.to_numpy()) / 2.0
    fs = np.arange(K, 90, 5)                                   # 5-min bar stamps 9:35 .. 10:55 (slots 5..85)
    cl = Cff[i][:, fs + 4]                                     # close of each 5-min bar = close of bar f+4
    with np.errstate(invalid="ignore"):
        far = d[:, None] * (cl - mid[:, None]) < 0
    has = far.any(1)
    f = fs[far.argmax(1)]
    early = B0.date.isin(ds.index[ds.early_close]).to_numpy()
    open_at = B0["xs"].to_numpy() > f + 4                         # ORB position still open when the 5-min bar closes
    ev = has & open_at & ~early
    E = B0[ev].copy().reset_index(drop=True)
    E["f"] = f[ev]
    E["mid"] = mid[ev]
    E["W"] = (E.orh - E.orl)
    ii, ff, dd = E.di.to_numpy(), E.f.to_numpy(), E.d.to_numpy()
    seg = np.arange(H.shape[1])[None, :]
    inseg = (seg >= K) & (seg <= (ff + 4)[:, None])
    hh = np.nanmax(np.where(inseg, H[ii], np.nan), 1)
    ll = np.nanmin(np.where(inseg, L[ii], np.nan), 1)
    E["rev_stop"] = np.where(dd > 0, hh + 0.5, ll - 0.5)
    E["act"] = ff + 5
    n_info = dict(orb_days=int(len(B0)), failure_signal_days=int(has.sum()),
                  stopped_before_or_in_failure_bar=int((has & ~open_at & ~early).sum()),
                  early_close_days_excluded=int((has & open_at & early).sum()), events=int(ev.sum()))
    return E, n_info


def legs(E, g, Cff, NV, use_target=False):
    O, H, L = g["Open"], g["High"], g["Low"]
    ii = E.di.to_numpy()
    act = E.act.to_numpy()
    ea = NV[ii, act]
    # ORB plain exit at the open of the action bar (chosen_models fills: 1 tick adverse, $1 commission)
    d = E.d.to_numpy()
    xref = O[ii, ea]
    orb_net = d * ((xref - d * p5.TICK) - E.fill.to_numpy()) - p5.COMM / PPT
    tgt = np.where(d > 0, E.orl - 0.5 * E.W, E.orh + 0.5 * E.W) if use_target else None
    res = sl.simulate(O, H, L, Cff, NV, ii, ea, np.full(len(ii), REV_EXIT), -d, stop_abs=E.rev_stop.to_numpy(),
                      target=tgt)
    res = sl.finish(res, 1.0, PPT)
    return orb_net, res, ea


def rev_frame(E, res, ea, orb_net, P_days_col):
    R = pd.DataFrame({"date": E.date, "entry_time": [p5_time(s) for s in res["entry_slot"]],
                      "exit_time": [p5_time(s) for s in res["exit_slot"]],
                      "side": np.where(E.d > 0, "short", "long"), "entry": res["entry"], "exit": res["exit"],
                      "exit_reason": res["reason"], "gross_pts": res["gross"], "net_pts": res["net"],
                      "net_usd": res["usd"], "net_bp": res["bp"], "orb_side": np.where(E.d > 0, "long", "short"),
                      "ORH": E.orh, "ORL": E.orl, "mid": E.mid, "failure_bar": [p5_time(s) for s in E.f],
                      "stop": res["stop"], "target": res["target"], "orb_exit_net_usd": orb_net * PPT,
                      "orb_baseline_net_usd": E.usd, "gross_usd": res["gross"] * PPT, "gross_bp": res["gross_bp"],
                      "stress_usd": res["stress_usd"], "stress_bp": res["stress_bp"], "di": E.di,
                      "entry_slot": res["entry_slot"], "exit_slot": res["exit_slot"], "ok": res["ok"]})
    return R


def p5_time(s):
    m = int(s) + 570
    return f"{m // 60:02d}:{m % 60:02d}"


def rand_ctl(E, res, ea, g, Cff, NV, use_target=False):
    O, H, L = g["Open"], g["High"], g["Low"]
    ii = E.di.to_numpy()
    d = -E.d.to_numpy()
    dist = d * (res["entry"] - res["stop"])
    off = d * (res["target"] - res["entry"]) if use_target else None
    out = {}
    for s in (1, -1):
        kw = dict(stop_dist=dist)
        if use_target:
            kw["target_off"] = off
        r = sl.finish(sl.simulate(O, H, L, Cff, NV, ii, ea, np.full(len(ii), REV_EXIT), np.full(len(ii), s), **kw),
                      1.0, PPT)
        out[s] = r["bp"]
    own = np.where(d > 0, out[1], out[-1])
    assert np.allclose(own, res["bp"]), "random control does not reproduce the reverse leg"
    m = sl.coin_control(out[1], out[-1], sc.NREP, sc.SEED)
    return dict(p95=float(np.percentile(m, 95)), mean=float(m.mean()), actual=float(np.mean(res["bp"])))


def books(B0, E, orb_net, rev_usd, take_rev):
    b0 = B0.set_index("date").usd
    b1 = b0.copy()
    b1.loc[E.date.to_numpy()] = orb_net * PPT
    b2 = b1.copy()
    add = pd.Series(np.where(take_rev, rev_usd, 0.0), index=E.date.to_numpy())
    b2.loc[add.index] += add.to_numpy()
    return b0, b1, b2


def evaluate(R, ctl, b0, b2, tthr):
    h = sc.headline(R, "2010-06-07")
    t_nw, t_iid = sc.nw_t(R.net_bp.to_numpy()), sc.iid_t(R.net_bp.to_numpy())
    h["t_event_nw5_bp"], h["t_event_iid_bp"] = t_nw, t_iid
    t = min(t_nw, t_iid)
    p18 = R[R.date >= "2018-01-01"].net_usd.sum()
    p25 = R[R.date >= "2025-01-01"].net_usd.sum()
    diff = (b2 - b0).mean()
    dd0, dd2 = sc.max_dd(b0.to_numpy()), sc.max_dd(b2.to_numpy())
    crit = [
        dict(name=f"(i) reverse-leg event-level t >= {tthr} (min NW5/iid, net bps)",
             value=f"NW5 {t_nw:.2f}, iid {t_iid:.2f}", pass_=bool(t >= tthr)),
        dict(name="(ii) reverse-leg net Jan 2018-latest > 0", value=f"${p18:,.0f} (Jan 2025-latest ${p25:,.0f})",
             pass_=bool(p18 > 0)),
        dict(name="(iii) reverse-leg net > 0 in >= 6 of 8 blocks", value=f"{h['blocks_positive']}/8",
             pass_=bool(h["blocks_positive"] >= 6)),
        dict(name="(iv) mean net bps > random-direction 95th pct", value=f"{ctl['actual']:.2f} vs {ctl['p95']:.2f}",
             pass_=bool(ctl["actual"] > ctl["p95"])),
        dict(name="(v) mean daily (book - B0) > 0 and book maxDD <= B0 maxDD",
             value=f"mean diff ${diff:.3f}/day; maxDD book ${dd2:,.0f} vs B0 ${dd0:,.0f}",
             pass_=bool(diff > 0 and dd2 <= dd0)),
    ]
    return h, crit, dict(post2025_usd=float(p25))


def book_stats(b):
    return dict(days=int(len(b)), total_usd=float(b.sum()), mean_daily_usd=float(b.mean()), max_dd_usd=sc.max_dd(b.to_numpy()),
                t_iid=sc.iid_t(b.to_numpy()))


def main():
    ds, expiry, g, Cff, sess = load()
    NV = sc.next_valid(g["Open"])
    B0 = baseline(ds, expiry, g, Cff, sess)
    chk = check_b0(B0)
    print("B0 check:", chk)
    assert chk["match"], "B0 does not reproduce chosen_models opening_range"
    E, ninfo = failure(B0, g, Cff, ds)
    print("failure:", ninfo)
    days_index = pd.DatetimeIndex(E.date)
    calm, _, _ = sc.vix_calm(days_index)
    calm = calm.to_numpy()
    summary = dict(B0_check=chk, failure_counts=ninfo)
    B0.assign(entry_time="09:35", exit_time=[p5_time(s) for s in B0["xs"]]).to_csv(f"{sc.OUT}/trades_C_B0_orb.csv", index=False)
    out_books = {}
    for name, use_t, calm_only in [("C", False, False), ("C1-calm", False, True), ("C2-target", True, False)]:
        orb_net, res, ea = legs(E, g, Cff, NV, use_t)
        assert res["ok"].all()
        R = rev_frame(E, res, ea, orb_net, None)
        R["calm_vix"] = calm
        take = calm if calm_only else np.ones(len(R), bool)
        Rk = R[take].reset_index(drop=True)
        resk = {k: (v[take] if isinstance(v, np.ndarray) else v) for k, v in res.items()}
        Ek = E[take].reset_index(drop=True)
        ctl = rand_ctl(Ek, resk, ea[take], g, Cff, NV, use_t)
        b0, b1, b2 = books(B0, E, orb_net, res["usd"], take)
        h, crit, extra = evaluate(Rk, ctl, b0, b2, 2.0 if name == "C" else 2.4)
        R.to_csv(f"{sc.OUT}/trades_{name}_reverse_leg.csv", index=False) if not calm_only else \
            Rk.to_csv(f"{sc.OUT}/trades_{name}_reverse_leg.csv", index=False)
        bk = pd.DataFrame({"B0": b0, "B1_plain_exit": b1, "book": b2})
        bk.to_csv(f"{sc.OUT}/books_daily_{name}.csv")
        out_books[name] = bk
        summary[name] = dict(instrument="MNQ", headline=h, random_ctl=ctl, criteria=crit,
                             passed=bool(all(c["pass_"] for c in crit)), extra=extra,
                             books=dict(B0=book_stats(b0), B1_plain_exit=book_stats(b1), B2_or_variant=book_stats(b2),
                                        B1_minus_B0=book_stats(b1 - b0), B2_minus_B0=book_stats(b2 - b0),
                                        B1_minus_B0_on_event_days=book_stats((b1 - b0).loc[E.date.to_numpy()])),
                             orb_early_exit_stats=dict(events=int(len(E)), orb_exit_usd=float(orb_net.sum() * PPT),
                                                       orb_baseline_usd_same_days=float(E.usd.sum())))
        print(name, f"rev trades {h['trades']} $/tr {h['net_usd_per_trade']:.2f} total ${h['total_usd']:,.0f} "
              f"bp {h['net_bp_per_trade']:.2f} blocks+ {h['blocks_positive']} pass {summary[name]['passed']} mix {h['exit_mix']}")
        for c in crit:
            print("   ", c)
        print("   books", {k: round(v["total_usd"]) for k, v in summary[name]["books"].items()})
    sc.dump("summary_C.json", summary)


if __name__ == "__main__":
    main()
