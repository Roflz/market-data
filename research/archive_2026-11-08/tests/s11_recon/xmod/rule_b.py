"""Section 11 rule B (midday drift-burst fade). PRIMARY = MNQ (NQ bars), variant B-MES (ES), B1 long-only (MNQ),
controls C1 (random direction), C2 (enter at the arming bar), B1 drift control (random long entries)."""
import numpy as np
import pandas as pd

import s11common as sc
import simlib as sl

ARM0, ARM1 = sc.slot(1029), sc.slot(1429)
LAST_ENTRY = sc.slot(1430)
TH = 4.0


def tstat(Cff):
    lc = np.log(Cff)
    r = np.zeros_like(lc)
    r[:, 1:] = lc[:, 1:] - lc[:, :-1]
    r[np.isnan(r)] = 0.0                                # missing bar (or before the first bar) -> r = 0
    nd, ns = r.shape
    D = np.zeros_like(r)
    V = np.zeros_like(r)
    r2 = r * r
    for j in range(30):
        D[:, j:] += np.exp(-j / 5) * r[:, :ns - j]
    for j in range(120):
        V[:, j:] += np.exp(-j / 25) * r2[:, :ns - j]
    V /= np.exp(-np.arange(120) / 25).sum()
    k2 = np.exp(-2 * np.arange(30) / 5).sum()
    with np.errstate(invalid="ignore", divide="ignore"):
        T = D / np.sqrt(V * k2)
    T[~np.isfinite(T)] = 0.0
    return T


def prep(sym):
    c = sc.load(sym)
    days, g, info = c["days"], c["g"], c["info"]
    O, H, L, C = g["Open"], g["High"], g["Low"], g["Close"]
    Cff = sc.ffill_close(C)
    NV = sc.next_valid(O)
    fomc, opex = sc.calendar_flags(days)
    calm, _, _ = sc.vix_calm(days)
    tradable = np.ones(len(info), bool)  # RECON: use the file contract of day D (Databento .v.0 = prior-day volume leader)
    elig = info.full.to_numpy() & ~fomc & ~opex & tradable
    T = tstat(Cff)
    return dict(sym=sym, days=days, O=O, H=H, L=L, Cff=Cff, NV=NV, elig=elig, calm=calm.to_numpy(), T=T)


def events(P, mode="peak"):
    """one event per day: first arming bar 10:29-14:29 with |T| >= 4; entry after the peak (or at arming, C2)."""
    T, Cff, NV = P["T"], P["Cff"], P["NV"]
    nd, ns = T.shape
    win = np.zeros(ns, bool)
    win[ARM0:ARM1 + 1] = True
    hit = (np.abs(T) >= TH) & win[None, :]
    armed = hit.any(1) & P["elig"]
    di = np.where(armed)[0]
    a = hit[di].argmax(1)
    s = np.sign(T[di, a])
    if mode == "peak":
        # t' = first bar after a with s*T[t'] < s*T[t'-1]; peak p = t'-1; entry bar t'+1
        dec = np.zeros((len(di), ns), bool)
        dec[:, 1:] = s[:, None] * T[di, 1:] < s[:, None] * T[di, :-1]
        dec &= np.arange(ns)[None, :] > a[:, None]
        has = dec.any(1)
        tp = np.where(has, dec.argmax(1), ns + 5)
        p = tp - 1
        e = tp + 1
    else:
        p = a
        e = a + 1
        has = np.ones(len(di), bool)
    take = has & (e <= LAST_ENTRY)
    ev = pd.DataFrame({"di": di, "arm_slot": a, "s": s, "T_arm": T[di, a], "peak_slot": p, "e": e, "tk": take})
    ev = ev[ev.tk].reset_index(drop=True)
    d, pp = ev.di.to_numpy(), ev.peak_slot.to_numpy()
    ev["pre_move"] = Cff[d, pp] - Cff[d, pp - 5]
    ev["pre_bp"] = 1e4 * ev.pre_move / Cff[d, pp - 5]
    ev["M"] = np.abs(ev.pre_move)
    ev["ea"] = NV[d, ev.e.to_numpy()]
    return ev, int(armed.sum())


def sim(P, ev, dirn):
    d = ev.di.to_numpy()
    ea = ev.ea.to_numpy()
    return sl.simulate(P["O"], P["H"], P["L"], P["Cff"], P["NV"], d, ea, ea + 15, dirn, stop_dist=ev.M.to_numpy())


def to_trades(P, ev, res, sym):
    sp = sc.SPEC[sym]
    res = sl.finish(res, sp["cost"], sp["usd"])
    tr = ev.copy()
    tr["date"] = P["days"][tr.di.to_numpy()]
    tr["dir"] = -tr.s
    tr["side"] = np.where(tr.dir > 0, "long", "short")
    for k_out, k in [("entry", "entry"), ("exit", "exit"), ("exit_reason", "reason"), ("gross_pts", "gross"),
                     ("net_pts", "net"), ("net_usd", "usd"), ("net_bp", "bp"), ("gross_bp", "gross_bp"),
                     ("stress_usd", "stress_usd"), ("stress_bp", "stress_bp"), ("entry_slot", "entry_slot"),
                     ("exit_slot", "exit_slot"), ("stop", "stop"), ("ok", "ok"), ("fallback", "fallback")]:
        tr[k_out] = res[k]
    tr["gross_usd"] = tr.gross_pts * sp["usd"]
    tr["arm_time"] = [sc.slot_time(x) for x in tr.arm_slot]
    tr["peak_time"] = [sc.slot_time(x) for x in tr.peak_slot]
    tr["entry_time"] = [sc.slot_time(x) for x in tr.entry_slot]
    tr["exit_time"] = [sc.slot_time(x) for x in tr.exit_slot]
    tr["calm_vix"] = P["calm"][tr.di.to_numpy()]
    tr["burst"] = np.where(tr.s < 0, "negative", "positive")
    return tr[tr.ok].reset_index(drop=True)


COLS = ["date", "entry_time", "exit_time", "side", "entry", "exit", "exit_reason", "gross_pts", "net_pts", "net_usd",
        "net_bp", "arm_time", "T_arm", "peak_time", "burst", "pre_move", "pre_bp", "M", "stop", "gross_usd",
        "gross_bp", "stress_usd", "stress_bp", "calm_vix", "di", "entry_slot", "exit_slot", "fallback"]


def c1(P, ev, tr, sym):
    sp = sc.SPEC[sym]
    out = {}
    for s in (1, -1):
        r = sl.finish(sim(P, ev, np.full(len(ev), s)), sp["cost"], sp["usd"])
        out[s] = r["bp"][r["ok"]]
    own = np.where(tr.dir.to_numpy() > 0, out[1], out[-1])
    assert np.allclose(own, tr.net_bp.to_numpy())
    m = sl.coin_control(out[1], out[-1], sc.NREP, sc.SEED)
    return dict(p95=float(np.percentile(m, 95)), mean=float(m.mean()), actual=float(tr.net_bp.mean()))


def drift_control(P, tr, sym):
    """B1: random long entries at random bars 10:31-14:30 on eligible days, 15-min hold, M drawn from B1 events."""
    sp = sc.SPEC[sym]
    rng = np.random.default_rng(sc.SEED)
    eld = np.where(P["elig"])[0]
    eld = eld[P["days"][eld] >= tr.date.min()]
    n = len(tr)
    d = rng.choice(eld, size=(sc.NREP, n))
    e = rng.integers(sc.slot(1031), LAST_ENTRY + 1, size=(sc.NREP, n))
    M = rng.choice(tr.M.to_numpy(), size=(sc.NREP, n))
    d, e, M = d.ravel(), e.ravel(), M.ravel()
    ea = P["NV"][d, e]
    res = sl.simulate(P["O"], P["H"], P["L"], P["Cff"], P["NV"], d, ea, ea + 15, np.ones(len(d)), stop_dist=M)
    res = sl.finish(res, sp["cost"], sp["usd"])
    bp = np.where(res["ok"], res["bp"], np.nan).reshape(sc.NREP, n)
    m = np.nanmean(bp, 1)
    return dict(p95=float(np.percentile(m, 95)), mean=float(m.mean()), actual=float(tr.net_bp.mean()))


def evaluate(tr, ctl, tthr, extra_ctl=None):
    h = sc.headline(tr, "2010-06-07")
    t_nw = sc.nw_t(tr.net_bp.to_numpy())
    t_iid = sc.iid_t(tr.net_bp.to_numpy())
    t = min(t_nw, t_iid)
    h["t_event_nw5_bp"], h["t_event_iid_bp"] = t_nw, t_iid
    post18 = tr[tr.date >= "2018-01-01"].net_usd.sum()
    crit = [
        dict(name="power: >= 200 events", value=str(len(tr)), pass_=bool(len(tr) >= 200)),
        dict(name=f"(i) event-level t >= {tthr} (min of NW5 and iid, net bps)", value=f"NW5 {t_nw:.2f}, iid {t_iid:.2f}",
             pass_=bool(t >= tthr)),
        dict(name="(ii) net P&L Jan 2018-latest > 0", value=f"${post18:,.0f}", pass_=bool(post18 > 0)),
        dict(name="(iii) net > 0 in >= 6 of 8 blocks", value=f"{h['blocks_positive']}/8",
             pass_=bool(h["blocks_positive"] >= 6)),
        dict(name="(iv) mean net bps > C1 95th pct", value=f"{ctl['actual']:.2f} vs {ctl['p95']:.2f}",
             pass_=bool(ctl["actual"] > ctl["p95"])),
    ]
    if extra_ctl is not None:
        crit.append(dict(name="(iv-b) B1 mean net bps > drift-control 95th pct",
                         value=f"{extra_ctl['actual']:.2f} vs {extra_ctl['p95']:.2f}",
                         pass_=bool(extra_ctl["actual"] > extra_ctl["p95"])))
    return h, crit


def splits(tr):
    q = tr.M.quantile(0.9)
    out = {}
    for name, m in [("calm", tr.calm_vix), ("not_calm", ~tr.calm_vix), ("negative_burst", tr.s < 0),
                    ("positive_burst", tr.s > 0), ("without_top10pct_M", tr.M <= q), ("top10pct_M", tr.M > q)]:
        t = tr[m]
        out[name] = dict(trades=int(len(t)), net_usd=float(t.net_usd.sum()), bp_per_trade=float(t.net_bp.mean()),
                         usd_per_trade=float(t.net_usd.mean()), t_iid=sc.iid_t(t.net_bp.to_numpy()))
    return out


def main():
    summary = {}
    for name, sym, longonly in [("B", "NQ", False), ("B-MES", "ES", False), ("B1", "NQ", True)]:
        P = prep(sym)
        ev, n_armed = events(P)
        if longonly:
            ev = ev[ev.s < 0].reset_index(drop=True)
        tr = to_trades(P, ev, sim(P, ev, -ev.s.to_numpy()), sym)
        ev = ev[ev.di.isin(tr.di)].reset_index(drop=True)
        ctl = c1(P, ev, tr, sym)
        dctl = drift_control(P, tr, sym) if longonly else None
        h, crit = evaluate(tr, ctl, 2.0 if name == "B" else 2.4, dctl)
        # C2 diagnostic: enter at the arming bar
        ev2, _ = events(P, "arm")
        if longonly:
            ev2 = ev2[ev2.s < 0].reset_index(drop=True)
        tr2 = to_trades(P, ev2, sim(P, ev2, -ev2.s.to_numpy()), sym)
        h2 = sc.headline(tr2, "2010-06-07")
        tr[COLS].to_csv(f"{sc.OUT}/trades_{name}.csv", index=False)
        tr2[COLS].to_csv(f"{sc.OUT}/trades_{name}_C2arm.csv", index=False)
        calib = dict(armed_days=n_armed, events_traded=int(len(tr)),
                     mean_pre_bp_negative=float(tr[tr.s < 0].pre_bp.mean()),
                     mean_pre_bp_positive=float(tr[tr.s > 0].pre_bp.mean()),
                     n_negative=int((tr.s < 0).sum()), n_positive=int((tr.s > 0).sum()),
                     source_ES_means="about -37 / +36 bps (Christensen-Oomen-Reno, cv 4.0, one event per day)")
        summary[name] = dict(instrument=sc.SPEC[sym]["micro"], calibration=calib, headline=h, C1=ctl,
                             drift_control=dctl, criteria=crit, passed=bool(all(c["pass_"] for c in crit)),
                             C2_arming_entry=h2, splits=splits(tr), fallback_exits=int(tr.fallback.sum()))
        print(name, calib)
        print(f"  trades {h['trades']} $/tr {h['net_usd_per_trade']:.2f} total ${h['total_usd']:,.0f} bp {h['net_bp_per_trade']:.2f} "
              f"gross bp {h['gross_bp_per_trade']:.2f} blocks+ {h['blocks_positive']} pass {summary[name]['passed']} mix {h['exit_mix']}")
        for c in crit:
            print("   ", c)
        print("   C2 arm entry:", h2["trades"], round(h2["net_bp_per_trade"], 2), round(h2["total_usd"]))
    sc.dump("summary_B.json", summary)


if __name__ == "__main__":
    main()
