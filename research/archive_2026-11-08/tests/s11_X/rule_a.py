"""Section 11 rule A (calm-day 60-minute fade, MNQ) + A1 (MES) + A2 (VWAP trigger) + controls C1, C2."""
import numpy as np
import pandas as pd

import s11common as sc
import simlib as sl

DEC = [1100, 1130, 1200, 1230, 1300, 1330, 1400]
FLAT = sc.slot(1500)


def prep(sym):
    c = sc.load(sym)
    days, g, info = c["days"], c["g"], c["info"]
    O, H, L, C, V = g["Open"], g["High"], g["Low"], g["Close"], g["Volume"]
    Cff = sc.ffill_close(C)
    NV = sc.next_valid(O)
    full = info.full.to_numpy()
    fomc, opex = sc.calendar_flags(days)
    calm, vixp, vixmed = sc.vix_calm(days)
    tradable = (info.inst == info.prev_inst).to_numpy()
    # H1 and its median over the prior 20 full days
    s930, s1029 = sc.slot(930), sc.slot(1029)
    h1 = (np.nanmax(H[:, s930:s1029 + 1], 1) - np.nanmin(L[:, s930:s1029 + 1], 1)) / O[:, s930]
    fpos = np.where(full)[0]
    h1med = np.full(len(days), np.nan)
    # value for every day = median of the 20 full days strictly before it
    cnt = np.searchsorted(fpos, np.arange(len(days)), side="left")        # number of full days before day i
    okc = cnt >= 20
    hfull = pd.Series(h1[fpos]).rolling(20, min_periods=20).median().to_numpy()   # ending at full day k
    h1med[okc] = hfull[cnt[okc] - 1]
    return dict(sym=sym, days=days, O=O, H=H, L=L, C=C, V=V, Cff=Cff, NV=NV, full=full, fomc=fomc, opex=opex,
                calm=calm.to_numpy(), vixp=vixp.to_numpy(), vixmed=vixmed.to_numpy(), tradable=tradable,
                h1=h1, h1med=h1med, fpos=fpos, cnt=cnt)


def s60_table(P):
    Cff = P["Cff"]
    r = np.stack([np.log(Cff[:, sc.slot(T) - 1] / Cff[:, sc.slot(T) - 61]) for T in DEC], 1)
    fpos, cnt = P["fpos"], P["cnt"]
    ms = pd.DataFrame(r[fpos] ** 2).rolling(20, min_periods=20).mean().to_numpy()
    s = np.full(r.shape, np.nan)
    okc = cnt >= 20
    s[okc] = np.sqrt(ms[cnt[okc] - 1])
    return r, s


def vwap_table(P):
    O, H, L, C, V, Cff = P["O"], P["H"], P["L"], P["C"], P["V"], P["Cff"]
    s930 = sc.slot(930)
    tp = (H + L + C) / 3.0
    pv = np.where(np.isnan(tp) | np.isnan(V), 0.0, tp * V)
    vv = np.where(np.isnan(tp) | np.isnan(V), 0.0, V)
    cpv = np.cumsum(pv[:, s930:], 1)
    cv = np.cumsum(vv[:, s930:], 1)
    vw = np.stack([cpv[:, sc.slot(T) - 1 - s930] / cv[:, sc.slot(T) - 1 - s930] for T in DEC], 1)
    p = np.stack([Cff[:, sc.slot(T) - 1] for T in DEC], 1)
    dev = np.abs(p - vw)
    fpos, cnt = P["fpos"], P["cnt"]
    m = pd.DataFrame(dev[fpos]).rolling(14, min_periods=14).mean().to_numpy()
    S = np.full(dev.shape, np.nan)
    okc = cnt >= 14
    S[okc] = m[cnt[okc] - 1]
    return p, vw, S


def run_book(P, day_mask, kind, sym):
    """sequential decision times, one position at a time. kind 'fade' (rule A) or 'vwap' (A2)."""
    O, H, L, Cff, NV = P["O"], P["H"], P["L"], P["Cff"], P["NV"]
    nd = len(P["days"])
    free = np.zeros(nd, int)              # first slot at which the day is flat (exits at a bar open free that bar)
    if kind == "fade":
        r60, s60 = s60_table(P)
    else:
        pT, vw, S = vwap_table(P)
    recs = []
    for k, T in enumerate(DEC):
        e = sc.slot(T)
        P_T = Cff[:, e - 1]
        if kind == "fade":
            dP = P_T - Cff[:, e - 61]
            with np.errstate(invalid="ignore"):
                sig = np.abs(r60[:, k]) >= 1.0 * s60[:, k]
            sig &= dP != 0
            dirn = -np.sign(dP)
            tgt = P_T - 0.5 * dP
            sdist = np.abs(dP)
        else:
            dev = P_T - vw[:, k]
            with np.errstate(invalid="ignore"):
                sig = np.abs(dev) >= 2.0 * S[:, k]
            sig &= dev != 0
            dirn = -np.sign(dev)
            tgt = vw[:, k]
            sdist = np.abs(dev)
        cand = np.where(day_mask & sig & (free <= e) & ~np.isnan(P_T))[0]
        if len(cand) == 0:
            continue
        x = np.full(len(cand), min(e + 60, FLAT))
        res = sl.simulate(O, H, L, Cff, NV, cand, np.full(len(cand), e), x, dirn[cand], stop_dist=sdist[cand],
                          target=tgt[cand])
        okm = res["ok"]
        nxt = np.where(res["at_open"], res["exit_slot"], res["exit_slot"] + 1)
        free[cand[okm]] = nxt[okm]
        df = pd.DataFrame({"di": cand, "decision": sc.slot_time(e), "dec_slot": e, "dir": dirn[cand],
                           "P_T": P_T[cand], "move": (dP if kind == "fade" else dev)[cand],
                           "stop_dist": sdist[cand], "target": res["target"], "stop": res["stop"],
                           "entry_slot": res["entry_slot"], "exit_slot": res["exit_slot"], "entry": res["entry"],
                           "exit": res["exit"], "exit_reason": res["reason"], "gross_pts": res["gross"],
                           "at_open": res["at_open"], "ok": okm, "fallback": res["fallback"]})
        if kind == "fade":
            df["r60"] = r60[cand, k]
            df["s60"] = s60[cand, k]
        else:
            df["vwap"] = vw[cand, k]
            df["S"] = S[cand, k]
        recs.append(df[df.ok])
    tr = pd.concat(recs, ignore_index=True).sort_values(["di", "entry_slot"]).reset_index(drop=True)
    return add_money(tr, P, sym)


def add_money(tr, P, sym):
    sp = sc.SPEC[sym]
    tr["date"] = P["days"][tr.di.to_numpy()]
    tr["side"] = np.where(tr.dir > 0, "long", "short")
    tr["entry_time"] = [sc.slot_time(s) for s in tr.entry_slot]
    tr["exit_time"] = [sc.slot_time(s) for s in tr.exit_slot]
    tr["net_pts"] = tr.gross_pts - sp["cost"]
    tr["net_usd"] = tr.net_pts * sp["usd"]
    tr["gross_usd"] = tr.gross_pts * sp["usd"]
    tr["net_bp"] = 1e4 * tr.net_pts / tr.entry
    tr["gross_bp"] = 1e4 * tr.gross_pts / tr.entry
    st = tr.net_pts - np.where(tr.exit_reason == "stop", 2 * sc.TICK, 0.0)
    tr["stress_usd"] = st * sp["usd"]
    tr["stress_bp"] = 1e4 * st / tr.entry
    tr["calm_vix"] = P["calm"][tr.di.to_numpy()]
    return tr


def c1_control(P, tr, sym):
    """random direction: same entry bars, same stop distance, target offset mirrored, same time exits."""
    O, H, L, Cff, NV = P["O"], P["H"], P["L"], P["Cff"], P["NV"]
    d = tr.di.to_numpy()
    e = tr.dec_slot.to_numpy()
    x = np.minimum(e + 60, FLAT)
    off = (tr.target - tr.entry).to_numpy() * tr.dir.to_numpy()
    out = {}
    for s in (1, -1):
        res = sl.simulate(O, H, L, Cff, NV, d, e, x, np.full(len(d), s), stop_dist=tr.stop_dist.to_numpy(),
                          target_off=off)
        assert np.allclose(res["entry"], tr.entry.to_numpy())
        res = sl.finish(res, sc.SPEC[sym]["cost"], sc.SPEC[sym]["usd"])
        out[s] = res["bp"]
    # consistency: the realised direction reproduces the primary
    own = np.where(tr.dir.to_numpy() > 0, out[1], out[-1])
    assert np.allclose(own, tr.net_bp.to_numpy()), "control does not reproduce primary"
    means = sl.coin_control(out[1], out[-1], sc.NREP, sc.SEED)
    return dict(p95=float(np.percentile(means, 95)), mean=float(means.mean()), p50=float(np.median(means)),
                actual=float(tr.net_bp.mean()))


def evaluate(tr, c1, tthr, first_day):
    h = sc.headline(tr, first_day)
    t = h["t_nw5_daily_bp"]
    post25 = tr[tr.date >= "2025-01-01"].net_usd.sum()
    crit = [
        dict(name=f"(i) day-level NW5 t on daily net bps >= {tthr}", value=f"{t:.2f}", pass_=bool(t >= tthr)),
        dict(name="(ii) net P&L Jan 2025-latest > 0", value=f"${post25:,.0f}", pass_=bool(post25 > 0)),
        dict(name="(iii) net > 0 in >= 6 of 8 two-year blocks", value=f"{h['blocks_positive']}/8",
             pass_=bool(h["blocks_positive"] >= 6)),
        dict(name="(iv) mean net bps/trade > C1 95th pct", value=f"{c1['actual']:.2f} vs p95 {c1['p95']:.2f}",
             pass_=bool(c1["actual"] > c1["p95"])),
    ]
    return h, crit


def main():
    summary = {}
    for name, sym, kind in [("A", "NQ", "fade"), ("A1-MES", "ES", "fade"), ("A2-VWAP", "NQ", "vwap")]:
        P = prep(sym)
        base = P["full"] & ~P["fomc"] & ~P["opex"] & P["tradable"] & (P["cnt"] >= 20) & ~np.isnan(P["h1med"])
        with np.errstate(invalid="ignore"):
            filt = P["calm"] & (P["h1"] <= P["h1med"])
        elig = base & filt
        first_day = P["days"][np.where(elig)[0][0]]
        tr = run_book(P, elig, kind, sym)
        c1 = c1_control(P, tr, sym)
        h, crit = evaluate(tr, c1, 2.0 if name == "A" else 2.4, first_day)
        # C2 report-only: same rule on full days failing VIX or H1 filter
        c2days = base & ~filt & ~np.isnan(P["h1"])
        tr2 = run_book(P, c2days, kind, sym)
        h2 = sc.headline(tr2, first_day)
        cols = ["date", "entry_time", "exit_time", "side", "entry", "exit", "exit_reason", "gross_pts", "net_pts",
                "net_usd", "net_bp", "decision", "P_T", "move", "stop_dist", "target", "stop"] + \
               (["r60", "s60"] if kind == "fade" else ["vwap", "S"]) + \
               ["gross_usd", "gross_bp", "stress_usd", "stress_bp", "calm_vix", "di", "dec_slot", "entry_slot",
                "exit_slot", "at_open", "fallback"]
        tr[cols].to_csv(f"{sc.OUT}/trades_{name}.csv", index=False)
        tr2[cols].to_csv(f"{sc.OUT}/trades_{name}_C2control.csv", index=False)
        summary[name] = dict(instrument=sc.SPEC[sym]["micro"], first_day=str(first_day.date()),
                             eligible_days=int(elig.sum()), base_days=int(base.sum()),
                             roll_days_skipped=int((P["full"] & ~P["fomc"] & ~P["opex"] & ~P["tradable"]).sum()),
                             headline=h, C1=c1, criteria=crit, passed=bool(all(c["pass_"] for c in crit)),
                             C2_report=h2, fallback_exits=int(tr.fallback.sum()))
        print(name, f"trades {h['trades']} $/tr {h['net_usd_per_trade']:.2f} total ${h['total_usd']:,.0f} "
              f"bp/tr {h['net_bp_per_trade']:.2f} t {h['t_nw5_daily_bp']:.2f} blocks+ {h['blocks_positive']} "
              f"C1p95 {c1['p95']:.2f}  pass {summary[name]['passed']}")
        for c in crit:
            print("   ", c)
        print("   C2:", h2["trades"], round(h2["net_bp_per_trade"], 2), round(h2["total_usd"]), round(h2["t_nw5_daily_bp"], 2))
    sc.dump("summary_A.json", summary)


if __name__ == "__main__":
    main()
