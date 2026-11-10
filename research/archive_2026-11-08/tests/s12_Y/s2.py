"""S2 monthly NQ-ES beta-neutral spread momentum (12-month), V1 (1-month), V2 (RTY-ES); controls C1 (circular shift),
C2 (static long spread), drop-best-regime check, 1990-2009 index diagnostic."""
import os, sys, json, pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *

with open(f"{HERE}/sessions.pkl", "rb") as f:
    S = pickle.load(f)
models = pd.read_csv(f"{PROJ}/chosen_models_trades.csv", parse_dates=["date"])


# ------------------------------------------------------------------ signal from cash indexes
def yahoo(name):
    return pd.read_csv(f"{PROJ}/data/yahoo_daily/{name}.csv", parse_dates=["Date"]).set_index("Date").Close.dropna()


def monthly_signal(lead_name):
    """returns DataFrame indexed by month-end date: b (250d OLS slope), R (spread return), S12, d12, d1"""
    P = pd.concat([yahoo(lead_name).rename("A"), yahoo("SP500_index").rename("B")], axis=1, join="inner").dropna()
    P = P[P.index >= "1985-01-01"]
    r = np.log(P).diff()
    # rolling 250-return OLS slope
    cov = r.A.rolling(250).cov(r.B); var = r.B.rolling(250).var()
    beta = cov / var
    me = P.groupby([P.index.year, P.index.month]).tail(1).index      # last common trading day of each month
    M = pd.DataFrame({"A": P.A.reindex(me), "B": P.B.reindex(me), "b": beta.reindex(me)}, index=me)
    M["R"] = np.log(M.A / M.A.shift()) - M.b.shift() * np.log(M.B / M.B.shift())
    M["S12"] = M.R.rolling(12).sum()            # NaN if any of the 12 R's is NaN
    M["d12"] = np.sign(M.S12); M["d1"] = np.sign(M.R)
    M["ym"] = [(d.year, d.month) for d in M.index]
    # daily spread (for the live vol-scaling report only)
    daily_spread = r.A - beta.shift() * r.B
    return M, daily_spread


# ------------------------------------------------------------------ leg price access
class FutLegs:
    """NQ (or RTY) as leg A, ES as leg B, on S's cash sessions."""

    def __init__(self, which):
        self.which = which
        if which == "RTY":
            r = pd.read_csv(f"{PROJ}/data/RTY_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
            ts = pd.to_datetime(r.ts_event, utc=True).dt.tz_convert("America/New_York")
            r["d"] = ts.dt.tz_localize(None).dt.normalize(); r["h"] = ts.dt.hour
            r = r[(r.h >= 9) & (r.h <= 15)]
            self.R = {(d, h): (o, c, i) for d, h, o, c, i in zip(r.d, r.h, r.Open, r.Close, r.instrument_id)}
            self.rdays = set(r.d)
            self.ptA, self.costA = RTY_PT, RTY_COST
        else:
            self.ptA, self.costA = NQ_PT, NQ_COST

    def has(self, u):
        return self.which != "RTY" or S.dates[u] in self.rdays

    def inst(self, u):
        if self.which == "RTY":
            d = S.dates[u]
            for h in range(10, 16):
                if (d, h) in self.R:
                    return (int(self.R[(d, h)][2]), int(S.instE[u]))
            return (None, int(S.instE[u]))
        return (int(S.instN[u]), int(S.instE[u]))

    def entry(self, u):
        """open of the 10:00 bar (next available if missing). Returns (pA, pB, timeA, timeB)"""
        if self.which == "RTY":
            d = S.dates[u]
            for h in range(10, 16):
                if (d, h) in self.R:
                    pB, jB = S.next_open("E", u, IDX(h, 0))
                    return self.R[(d, h)][0], pB, f"{h:02d}:00", tm(jB)
            raise RuntimeError("no RTY bar")
        pA, jA = S.next_open("N", u, 30); pB, jB = S.next_open("E", u, 30)
        return pA, pB, tm(jA), tm(jB)

    def close(self, u):
        """close of the session's last cash bar: 15:59 (12:59 early); RTY: close of 15:00 (12:00 early) hourly bar"""
        ci = S.cidx[u]
        pB, jB = S.asof_close("E", u, ci)
        if self.which == "RTY":
            h = 15 if S.full[u] else 12
            while (S.dates[u], h) not in self.R:
                h -= 1
            return self.R[(S.dates[u], h)][1], pB, f"{h:02d}:00h-close", tm(jB)
        pA, jA = S.asof_close("N", u, ci)
        return pA, pB, tm(jA), tm(jB)


def first_sessions_of_months():
    out = {}
    for u, d in enumerate(S.dates):
        out.setdefault((d.year, d.month), u)
    return out


def simulate_months(M, dcol, legs, first_hold=(2010, 7), last_hold=(2026, 10)):
    """Month-by-month state machine. Returns (segments DataFrame, months DataFrame, daily P&L Series for d as given)."""
    fs = first_sessions_of_months()
    keys = sorted(fs)
    segs, months, daily = [], [], {}
    sig = {ym: (row[dcol], row.b, d) for d, row in M.iterrows() for ym in [row.ym]}
    for ki in range(len(keys) - 1):
        H = keys[ki]
        if H < first_hold or H > last_hold:
            continue
        prev = (H[0] - 1, 12) if H[1] == 1 else (H[0], H[1] - 1)
        d, bm, sigdate = sig[prev]
        E, X = fs[H], fs[keys[ki + 1]]
        if not legs.has(E):
            continue
        mrec = {"month": f"{H[0]}-{H[1]:02d}", "date": S.dates[E].strftime("%Y-%m-%d"), "d": d, "b": bm,
                "signal_date": sigdate.strftime("%Y-%m-%d"), "segments": 0, "gross_bp": 0.0, "cost_bp": 0.0,
                "net_bp": 0.0, "gross_long_bp": 0.0, "net_usd": 0.0, "gross_usd": 0.0, "cost_usd": 0.0,
                "roll_exits": 0}
        if d == 0 or not np.isfinite(d):
            months.append(mrec); continue
        state, pos, pending_old = "FLAT", None, None
        for u in range(E, X + 1):
            ins = legs.inst(u)
            # ---- open position: roll check first (instrument changed vs held -> exit at prior session close)
            if state == "IN" and u > pos["u0"] and ins != pos["inst"]:
                xA, xB, tA, tB = legs.close(u - 1)
                pos.update(x_day=u - 1, xA=xA, xB=xB, exit_time=tA, exit_time_B=tB, exit_reason="roll")
                segs.append(close_seg(pos, legs, daily)); mrec["roll_exits"] += 1
                pending_old, state = pos["inst"], "WAIT_ROLL"
            if state == "IN" and u == X:
                xA, xB, tA, tB = legs.entry(u)
                pos.update(x_day=u, xA=xA, xB=xB, exit_time=tA, exit_time_B=tB, exit_reason="month_end")
                segs.append(close_seg(pos, legs, daily)); state = "DONE"
            if u == X:
                break
            # ---- flat: open at month start, or reopen after a roll once both legs are in new contracts
            if state == "FLAT" and u == E:
                pos = open_seg(u, legs, d, bm, ins, "month_start", mrec["month"]); state = "IN"
            elif state == "WAIT_ROLL" and ins[0] != pending_old[0] and ins[1] != pending_old[1]:
                pos = open_seg(u, legs, d, bm, ins, "reopen_after_roll", mrec["month"]); state = "IN"
        for sgm in [s_ for s_ in segs if s_["month"] == mrec["month"]]:
            mrec["segments"] += 1
            for kx in ("gross_bp", "cost_bp", "net_bp", "gross_long_bp", "net_usd", "gross_usd", "cost_usd"):
                mrec[kx] += sgm[kx]
        months.append(mrec)
    return pd.DataFrame(segs), pd.DataFrame(months), pd.Series(daily).sort_index()


def open_seg(u, legs, d, bm, ins, why, month):
    pA, pB, tA, tB = legs.entry(u)
    k = bm * legs.ptA * pA / (ES_PT * pB)
    nA, nB = size_legs(k)
    return dict(u0=u, eA=pA, eB=pB, entry_time=tA, entry_time_B=tB, d=d, b=bm, k=k, nA=nA, nB=nB, inst=ins,
                entry_reason=why, month=month)


def close_seg(p, legs, daily):
    d, nA, nB = p["d"], p["nA"], p["nB"]
    # no trade spans a roll: every session in the segment has the held instruments
    for u in range(p["u0"], p["x_day"] + 1):
        assert legs.inst(u) == p["inst"], ("roll inside segment", S.dates[u])
    gl = nA * legs.ptA * (p["xA"] - p["eA"]) - nB * ES_PT * (p["xB"] - p["eB"])
    g = d * gl
    cost = nA * legs.costA + nB * ES_COST
    notional = nA * legs.ptA * p["eA"]
    # daily mark-to-market (for correlation with the existing models) on session closes
    if legs.which == "NQ":
        prevA, prevB = p["eA"], p["eB"]
        for u in range(p["u0"], p["x_day"] + 1):
            if u == p["x_day"]:
                cA, cB = p["xA"], p["xB"]
            else:
                cA, cB = legs.close(u)[:2]
            pnl = d * (nA * legs.ptA * (cA - prevA) - nB * ES_PT * (cB - prevB))
            if u == p["u0"]:
                pnl -= cost                                # charge the round trip on the entry day
            daily[S.dates[u]] = daily.get(S.dates[u], 0.0) + pnl
            prevA, prevB = cA, cB
    side = "long_A_short_ES" if d > 0 else "short_A_long_ES"
    return dict(month=p["month"], date=S.dates[p["u0"]].strftime("%Y-%m-%d"), entry_time=p["entry_time"],
                exit_date=S.dates[p["x_day"]].strftime("%Y-%m-%d"), exit_time=p["exit_time"], side=side,
                entry=p["eA"], exit=p["xA"], es_entry=p["eB"], es_exit=p["xB"], es_entry_time=p["entry_time_B"],
                es_exit_time=p["exit_time_B"], a_entry_fill=p["eA"] + d * (0.25 if legs.which == "NQ" else 0.1),
                a_exit_fill=p["xA"] - d * (0.25 if legs.which == "NQ" else 0.1),
                es_entry_fill=p["eB"] - d * 0.25, es_exit_fill=p["xB"] + d * 0.25,
                entry_reason=p["entry_reason"], exit_reason=p["exit_reason"], n_a=nA, n_es=nB, k=p["k"], b=p["b"],
                gross_pts=g / (legs.ptA * nA), net_pts=(g - cost) / (legs.ptA * nA), gross_usd=g, cost_usd=cost,
                net_usd=g - cost, notional_usd=notional, gross_bp=1e4 * g / notional, cost_bp=1e4 * cost / notional,
                net_bp=1e4 * (g - cost) / notional, gross_long_bp=1e4 * gl / notional,
                inst_a=p["inst"][0], inst_es=p["inst"][1])


def evaluate(months, name, primary, start_b="2016-01-01"):
    m = months.copy()
    out = summarize(m, start=pd.Timestamp(m.date.iloc[0]), min_block=10, nw_lags=3)
    out["per_year"] = 12.0 * float((m.d != 0).mean())
    out["t_nw3"] = float(nw_t(m.net_bp, 3))
    x = m.net_bp.to_numpy()
    post = pd.to_datetime(m.date) >= start_b
    out["post_2016"] = {"n": int(post.sum()), "mean_net_bp": float(x[post].mean()), "t": float(tstat(x[post]))}
    # C1 circular shift
    dser = m.d.to_numpy(); G = m.gross_long_bp.to_numpy(); C = m.cost_bp.to_numpy(); N = len(m)
    means = []
    for off in range(12, N - 12 + 1):
        ds = np.roll(dser, off)
        means.append(np.where(ds != 0, ds * G - C, 0.0).mean())
    means = np.array(means)
    out["C1_shift_offsets"] = int(len(means)); out["C1_shift_p95"] = float(np.percentile(means, 95))
    out["C1_shift_mean"] = float(means.mean())
    # C2 static long spread
    out["C2_static_long_mean_net_bp"] = float((G - C).mean())
    # drop best sign regime
    reg = (m.d != m.d.shift()).cumsum()
    tot = m.groupby(reg).net_bp.sum()
    best = tot.idxmax()
    keep = (reg != best).to_numpy()
    rm = m[reg == best]
    out["regimes"] = int(len(tot))
    out["best_regime"] = {"from": rm.month.iloc[0], "to": rm.month.iloc[-1], "months": int(len(rm)),
                          "d": float(rm.d.iloc[0]), "total_net_bp": float(tot.max())}
    out["mean_net_bp_ex_best_regime"] = float(x[keep].mean())
    out["long_share"] = float((m.d > 0).mean()); out["sign_changes"] = int((m.d != m.d.shift()).sum() - 1)
    out["roll_exits"] = int(m.roll_exits.sum())
    out["criteria"] = [
        {"name": "a: month-level t >= 2.0 (plain and NW3)" if primary else "a: t >= 3 or Holm p < 0.05 (set in summary)",
         "value": f"t={out['t']:.3f}, NW3 t={out['t_nw3']:.3f}", "pass": bool(out["t"] >= 2.0 and out["t_nw3"] >= 2.0)},
        {"name": "b: mean net > 0 in Jan 2016 - Nov 2026", "value": f"{out['post_2016']['mean_net_bp']:.3f} bp",
         "pass": bool(out["post_2016"]["mean_net_bp"] > 0)},
        {"name": "c: mean net > 0 in >= 2/3 counted 2-yr blocks (>=10 months)",
         "value": f"{out['blocks_positive']}/{out['blocks_counted']}",
         "pass": bool(out["blocks_counted"] > 0 and out["blocks_positive"] >= 2 / 3 * out["blocks_counted"])},
        {"name": "d1: mean net > 95th pct of circular-shift placebo (C1)",
         "value": f"{out['mean_net_bp']:.3f} vs {out['C1_shift_p95']:.3f} bp", "pass": bool(out["mean_net_bp"] > out["C1_shift_p95"])},
        {"name": "d2: mean net > static long-spread benchmark (C2)",
         "value": f"{out['mean_net_bp']:.3f} vs {out['C2_static_long_mean_net_bp']:.3f} bp",
         "pass": bool(out["mean_net_bp"] > out["C2_static_long_mean_net_bp"])},
        {"name": "e: mean net > 0 after dropping best sign regime",
         "value": f"{out['mean_net_bp_ex_best_regime']:.3f} bp (dropped {out['best_regime']['from']}..{out['best_regime']['to']})",
         "pass": bool(out["mean_net_bp_ex_best_regime"] > 0)},
    ]
    return out


def index_diag(M, dcol, lo, hi):
    """gross cash-index proxy: d_m * R_{m+1} in bp for holding months in [lo, hi]"""
    g = (M[dcol] * M.R.shift(-1)) * 1e4
    hold = pd.Series([(d + pd.offsets.MonthBegin(1)) for d in M.index], index=M.index)
    sel = (hold >= lo) & (hold <= hi) & g.notna() & (M[dcol] != 0)
    x = g[sel].to_numpy()
    return {"months": int(len(x)), "mean_gross_bp": float(x.mean()), "t": float(tstat(x)),
            "sign_changes": int((M[dcol][sel] != M[dcol][sel].shift()).sum() - 1)}


if __name__ == "__main__":
    res = {}
    Mn, spread_n = monthly_signal("NASDAQ100_index")
    Mr, spread_r = monthly_signal("RUSSELL2000_index")
    nq, rty = FutLegs("NQ"), FutLegs("RTY")
    runs = {"S2": (Mn, "d12", nq, (2010, 7)), "S2-V1": (Mn, "d1", nq, (2010, 7)), "S2-V2": (Mr, "d12", rty, (2017, 7))}
    for name, (M, dc, legs, fh) in runs.items():
        segs, months, daily = simulate_months(M, dc, legs, first_hold=fh)
        segs.to_csv(f"{HERE}/trades_{name}.csv", index=False)
        months.to_csv(f"{HERE}/months_{name}.csv", index=False)
        out = evaluate(months, name, name == "S2")
        out["segments"] = int(len(segs))
        out["net_usd_per_segment"] = float(segs.net_usd.mean())
        out["first_month"] = months.month.iloc[0]; out["last_month"] = months.month.iloc[-1]
        if name == "S2":
            corr = {}
            for mdl, g in models.groupby("model"):
                mp = g.groupby("date").usd.sum()
                alld = daily.index
                a = daily; bb = mp.reindex(alld, fill_value=0.0)
                both = daily.index.intersection(mp.index)
                lost = mp[mp < 0].index.intersection(daily.index)
                corr[mdl] = {"corr_all_S2_days_model_zero_filled": float(np.corrcoef(a, bb)[0, 1]),
                             "corr_overlap_days": float(np.corrcoef(daily[both], mp[both])[0, 1]),
                             "overlap_days": int(len(both)),
                             "S2_mean_usd_on_model_loss_days": float(daily[lost].mean())}
                # split by S2 direction
                for sgn, lab in ((1, "S2_long_spread"), (-1, "S2_short_spread")):
                    dd = pd.Series({pd.Timestamp(r.date): r.d for r in months.itertuples()})
                    dir_daily = dd.reindex(daily.index, method="ffill")
                    sel = both[(dir_daily.reindex(both) == sgn).to_numpy()]
                    corr[mdl][f"corr_overlap_{lab}"] = float(np.corrcoef(daily[sel], mp[sel])[0, 1]) if len(sel) > 2 else None
            out["model_correlation"] = corr
            last = segs.iloc[-1]
            out["margin_note"] = (f"last position: {int(last.n_a)} MNQ vs {int(last.n_es)} MES, NQ-leg notional "
                                  f"${last.notional_usd:,.0f}; held continuously all month")
            sd60 = spread_n.dropna().iloc[-60:].std() * np.sqrt(252)
            out["live_vol_scale_latest"] = {"spread_vol_ann": float(sd60), "scale": float(min(2.0, 0.08 / sd60)),
                                            "note": "index-based daily spread vol (Yahoo); reported only, not tested"}
            out["diag_index_1990_2009_gross"] = index_diag(Mn, "d12", pd.Timestamp("1990-01-01"), pd.Timestamp("2009-12-31"))
        if name == "S2-V1":
            out["diag_index_1990_2009_gross"] = index_diag(Mn, "d1", pd.Timestamp("1990-01-01"), pd.Timestamp("2009-12-31"))
        if name == "S2-V2":
            out["index_proxy_2010_07_to_2017_07_not_counted"] = index_diag(Mr, "d12", pd.Timestamp("2010-07-01"), pd.Timestamp("2017-07-31"))
            out["diag_index_1990_2009_gross"] = index_diag(Mr, "d12", pd.Timestamp("1990-01-01"), pd.Timestamp("2009-12-31"))
        # signal sign-change count over Jun 2010 - Oct 2026 (spec's measured property)
        sel = (M.index >= "2010-06-01") & (M.index <= "2026-10-31")
        out["signal_sign_changes_2010_2026"] = int((M[dc][sel] != M[dc][sel].shift()).sum() - 1)
        out["signal_long_share_2010_2026"] = float((M[dc][sel] > 0).mean())
        res[name] = out
        print(name, f"months={out['n']} segs={len(segs)} net={out['mean_net_bp']:.2f}bp gross={out['mean_gross_bp']:.2f} "
              f"cost={out['mean_cost_bp']:.2f} t={out['t']:.2f} nw3={out['t_nw3']:.2f} C1p95={out['C1_shift_p95']:.2f} "
              f"C2={out['C2_static_long_mean_net_bp']:.2f} exbest={out['mean_net_bp_ex_best_regime']:.2f} "
              f"flips={out['signal_sign_changes_2010_2026']} long={out['signal_long_share_2010_2026']:.2f} rolls={out['roll_exits']}")
    with open(f"{HERE}/s2_results.json", "w") as f:
        json.dump(jsonable(res), f, indent=1)
