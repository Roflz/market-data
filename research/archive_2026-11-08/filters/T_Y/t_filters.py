"""
Builder Y - Section 15 T1-T4 trend-day filters for the opening_range model (SPEC.md, pre-registered).
Every input is computed per cash session in an explicit loop over the raw 1-minute NQ bars (data/NQ_fut_1m.csv),
using only bars that CLOSED by 9:35 ET on the trade day (bar stamped 9:34 closes at 9:35).

Prices: additively back-adjusted exactly as fut_build.load_raw / daily_sessions.py do (roll jump = new contract's
first open - old contract's last close, removed from all earlier bars). A later roll adds the same constant to every
bar of a contract, so differences / ranges inside one contract are identical to raw prices (checked below).

Run: cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this>
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats as sst

warnings.filterwarnings("ignore")
OUT = os.path.dirname(os.path.abspath(__file__))
CACHE_BARS = os.path.join(OUT, "nq_1m_adj.pkl")
CACHE_INPUTS = os.path.join(OUT, "session_inputs.pkl")
LOOKBACK = 20


# ---------------------------------------------------------------------------------------------------------------
# 1. raw bars -> back-adjusted bars with session labels
# ---------------------------------------------------------------------------------------------------------------
def load_bars():
    if os.path.exists(CACHE_BARS):
        return pd.read_pickle(CACHE_BARS)
    d = pd.read_csv("data/NQ_fut_1m.csv", usecols=["ts_event", "Open", "High", "Low", "Close", "instrument_id"])
    d.index = pd.to_datetime(d.pop("ts_event"), utc=True).dt.tz_convert("America/New_York")
    d = d[~d.index.duplicated()].sort_index()
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)          # sum of all LATER roll jumps
    d["adj"] = adj
    for c in ("Open", "High", "Low", "Close"):
        d["raw_" + c] = d[c]
        d[c] = d[c] + adj
    d["sess"] = pd.to_datetime((d.index + pd.Timedelta(hours=6)).date)  # Globex day 18:00 -> 17:00, label = end day
    d["tmin"] = d.index.hour * 60 + d.index.minute
    pd.to_pickle(d, CACHE_BARS)
    return d


# ---------------------------------------------------------------------------------------------------------------
# 2. per-session inputs, explicit loop
# ---------------------------------------------------------------------------------------------------------------
def session_inputs(d, ds):
    if os.path.exists(CACHE_INPUTS):
        return pd.read_pickle(CACHE_INPUTS)
    ts_ns = d.index.as_unit("ns").asi8                              # int64 nanoseconds (match Timestamp.value)
    sess_vals = d.sess.to_numpy()
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    rH, rL = d.raw_High.to_numpy(float), d.raw_Low.to_numpy(float)
    inst = d.instrument_id.to_numpy()
    tmin = d.tmin.to_numpy()
    # session boundaries (bars are time-sorted and each Globex session is contiguous)
    starts = np.flatnonzero(np.r_[True, sess_vals[1:] != sess_vals[:-1]])
    ends = np.r_[starts[1:], len(d)]
    sess_dates = pd.DatetimeIndex(sess_vals[starts])
    assert sess_dates.is_monotonic_increasing and sess_dates.is_unique

    # daily EMA20 of session closes (fut_build: daily.c = last Close of each Globex session, ewm span 20 adjust=False)
    alpha = 2 / (20 + 1)
    ema_after = np.empty(len(starts))
    e = None
    for k in range(len(starts)):
        c_last = C[ends[k] - 1]
        e = c_last if e is None else (1 - alpha) * e + alpha * c_last
        ema_after[k] = e
    k_of = {dt: k for k, dt in enumerate(sess_dates)}

    cash = ds[ds.cash_day]
    rows = []
    for D, r in cash.iterrows():
        k = k_of[D]
        a, b = starts[k], ends[k]
        t9 = (D + pd.Timedelta(hours=9, minutes=35)).tz_localize("America/New_York").value  # decision time 9:35
        eve = (D - pd.Timedelta(days=1) + pd.Timedelta(hours=18)).tz_localize("America/New_York").value
        ts_s, tm_s = ts_ns[a:b], tmin[a:b]
        day = (ts_s >= D.tz_localize("America/New_York").value)            # bars on the calendar day D
        # ---- T3: first 5-minute candle 9:30-9:34
        fc = np.flatnonzero(day & (tm_s >= 570) & (tm_s <= 574)) + a
        fc_range = H[fc].max() - L[fc].min() if len(fc) else np.nan
        fc_raw = rH[fc].max() - rL[fc].min() if len(fc) else np.nan
        # ---- T4: overnight 18:00 prior evening through the 9:29 bar
        on = np.flatnonzero((ts_s >= eve) & ~(day & (tm_s >= 570))) + a
        on = on[ts_ns[on] < t9 - 5 * 60_000_000_000]                    # strictly before the 9:30 bar
        on_range = H[on].max() - L[on].min() if len(on) else np.nan
        on_raw = rH[on].max() - rL[on].min() if len(on) else np.nan
        n_pre_eve = int((ts_s < eve).sum())                              # session bars before 18:00 prior evening
        # ---- T2: 9:30 open (adjusted)
        o930 = np.flatnonzero(day & (tm_s == 570)) + a
        open930 = O[o930[0]] if len(o930) else np.nan
        # ---- 16:00 close of this session (15:59 bar, or 12:59 on early-close days); last close at/before that bar
        close_slot = 779 if r.early_close else 959
        cl = np.flatnonzero(day & (tm_s >= 570) & (tm_s <= close_slot)) + a
        close1600 = C[cl[-1]] if len(cl) else np.nan
        close_tmin = int(tmin[cl[-1]]) if len(cl) else -1
        # ---- T1: trend = sign(close of the 9:34 bar - EMA20 of daily closes through the PREVIOUS session)
        pre = np.flatnonzero(day & (tm_s >= 570) & (tm_s <= 574)) + a       # RTH bars that closed by 9:35
        c934 = C[pre[-1]] if len(pre) else np.nan
        c934_tmin = int(tmin[pre[-1]]) if len(pre) else -1
        ema_prev = ema_after[k - 1] if k > 0 else np.nan
        used = np.r_[fc, on, o930, pre]
        last_used_close = (ts_ns[used].max() + 60_000_000_000) if len(used) else 0  # bar close time
        rows.append(dict(date=D, early_close=bool(r.early_close), fc_range=fc_range, fc_range_raw=fc_raw,
                         fc_nbars=len(fc), fc_inst_n=len(set(inst[fc])), on_range=on_range, on_range_raw=on_raw,
                         on_nbars=len(on), on_inst_n=len(set(inst[on])), n_pre_eve=n_pre_eve,
                         open930=open930, close1600=close1600, close_tmin=close_tmin, c934=c934, c934_tmin=c934_tmin,
                         ema20_prev=ema_prev, prev_sess=sess_dates[k - 1] if k > 0 else pd.NaT,
                         last_used_close_ok=bool(last_used_close <= t9)))
    S = pd.DataFrame(rows).set_index("date")
    pd.to_pickle(S, CACHE_INPUTS)
    return S


def rolling_prior_median(S, col):
    """median of the previous LOOKBACK cash sessions' values (strictly before), NaN when fewer than LOOKBACK exist"""
    vals = S[col].to_numpy()
    out = np.full(len(vals), np.nan)
    hist = []
    for i, v in enumerate(vals):
        if len(hist) >= LOOKBACK:
            out[i] = np.median(hist[-LOOKBACK:])
        if np.isfinite(v):
            hist.append(v)
    return out


# ---------------------------------------------------------------------------------------------------------------
# 3. evaluation helpers
# ---------------------------------------------------------------------------------------------------------------
def max_dd(daily):
    eq = np.r_[0.0, np.cumsum(daily)]
    return float((np.maximum.accumulate(eq) - eq).max())


def daily_series(T, all_days):
    return T.groupby("date").usd.sum().reindex(all_days, fill_value=0.0)


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    t = (a.mean() - b.mean()) / np.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return float(t), float(df)


ERAS = [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020), ("2021-23", 2021, 2023),
        ("2024-26", 2024, 2026), ("2023-26", 2023, 2026), ("2010-17", 2010, 2017), ("2018-26", 2018, 2026)]


def split_stats(x):
    return dict(n=int(len(x)), usd=round(float(x.usd.sum()), 2),
                per_trade=round(float(x.usd.mean()), 3) if len(x) else None)


def evaluate(name, orb, keep, all_book, cost_extra=0.0):
    o = orb.copy()
    o["usd"] = o.usd - cost_extra
    book = all_book.copy()
    book["usd"] = book.usd - cost_extra
    K, R = o[keep], o[~keep]
    yr = o.date.dt.year
    t, df = welch(K.usd, R.usd)
    orb_days = pd.DatetimeIndex(sorted(o.date.unique()))
    d0, d1 = daily_series(o, orb_days), daily_series(K, orb_days)
    rem_full, rem_a, rem_b = R.usd.sum(), R[yr[~keep] <= 2017].usd.sum(), R[yr[~keep] >= 2018].usd.sum()
    book_days = pd.DatetimeIndex(sorted(book.date.unique()))
    removed_idx = o.index[~keep]
    book_f = book.drop(index=removed_idx)
    b0, b1 = daily_series(book, book_days), daily_series(book_f, book_days)
    res = dict(filter=name, cost_extra_per_trade=cost_extra, kept=int(len(K)), removed=int(len(R)),
               share_removed=round(len(R) / len(o), 4), kept_usd=round(float(K.usd.sum()), 2),
               removed_usd=round(float(rem_full), 2), removed_usd_2010_17=round(float(rem_a), 2),
               removed_usd_2018_26=round(float(rem_b), 2), kept_per_trade=float(K.usd.mean()),
               removed_per_trade=float(R.usd.mean()), welch_t=round(t, 4), welch_df=round(df, 1),
               p_one_sided=float(sst.t.sf(t, df)),
               dd_before=round(max_dd(d0.to_numpy()), 2), dd_after=round(max_dd(d1.to_numpy()), 2),
               worst_day_before=round(float(d0.min()), 2), worst_day_after=round(float(d1.min()), 2),
               model_net_before=round(float(o.usd.sum()), 2), model_net_after=round(float(K.usd.sum()), 2))
    res["a_removed_lose"] = bool(rem_full < 0 and rem_a < 0 and rem_b < 0)
    res["b_welch"] = bool(t >= 2.5)
    res["c_dd_worst"] = bool(res["dd_after"] <= res["dd_before"] and res["worst_day_after"] >= res["worst_day_before"])
    res["passed"] = bool(res["a_removed_lose"] and res["b_welch"] and res["c_dd_worst"])
    res["eras"] = {}
    for lab, y0, y1 in ERAS:
        m = (yr >= y0) & (yr <= y1)
        res["eras"][lab] = dict(kept=split_stats(o[m & keep]), removed=split_stats(o[m & ~keep]),
                                share_removed=round(float((m & ~keep).sum() / max(m.sum(), 1)), 4))
    res["years"] = {int(y): dict(kept=split_stats(o[(yr == y) & keep]), removed=split_stats(o[(yr == y) & ~keep]))
                    for y in sorted(yr.unique())}
    res["book"] = dict(net_before=round(float(b0.sum()), 2), net_after=round(float(b1.sum()), 2),
                       dd_before=round(max_dd(b0.to_numpy()), 2), dd_after=round(max_dd(b1.to_numpy()), 2),
                       worst_day_before=round(float(b0.min()), 2), worst_day_after=round(float(b1.min()), 2))
    return res


# ---------------------------------------------------------------------------------------------------------------
def main():
    ds = pd.read_pickle("data/daily_sessions_NQ.pkl")
    d = load_bars()
    S = session_inputs(d, ds)
    S["fc_med20"] = rolling_prior_median(S, "fc_range")
    S["on_med20"] = rolling_prior_median(S, "on_range")
    # gap: today's 9:30 open - previous CASH session's 16:00 close (both back-adjusted)
    S["prev_cash"] = pd.Series(S.index, index=S.index).shift()
    S["prev_close1600"] = S.close1600.shift()
    S["gap"] = S.open930 - S.prev_close1600
    S["trend"] = np.sign(S.c934 - S.ema20_prev)

    book = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    orb = book[book.model == "opening_range"].copy()
    print(f"base opening_range: {len(orb)} trades, ${orb.usd.sum():,.2f}; book {len(book)} trades ${book.usd.sum():,.2f}")
    assert S.index.isin(ds.index[ds.cash_day]).all() and orb.date.isin(S.index).all()

    # ---------------- per-trade loop: decisions at 9:35 ----------------
    recs = []
    for idx, tr in orb.iterrows():
        s = S.loc[tr.date]
        dirn = 1 if tr.side == "long" else -1
        t1_keep = bool(s.trend == dirn)
        gsign = np.sign(s.gap) if np.isfinite(s.gap) else 0.0
        t2_keep = bool(gsign == dirn)                                    # zero / missing gap = disagree
        t3_keep = True if not np.isfinite(s.fc_med20) else bool(s.fc_range >= s.fc_med20)
        t4_keep = True if not np.isfinite(s.on_med20) else bool(s.on_range <= s.on_med20)
        recs.append(dict(idx=idx, date=tr.date.date(), side=tr.side, dir=dirn, exit=tr.exit, usd=tr.usd, R=tr.R,
                         bp=tr.bp, c934=s.c934, c934_tmin=s.c934_tmin, ema20_prev=s.ema20_prev, trend=s.trend,
                         open930=s.open930, prev_cash=s.prev_cash.date() if pd.notna(s.prev_cash) else None,
                         prev_close1600=s.prev_close1600, gap=s.gap, fc_range=s.fc_range, fc_med20=s.fc_med20,
                         on_range=s.on_range, on_med20=s.on_med20, on_nbars=s.on_nbars,
                         inputs_before_935=s.last_used_close_ok,
                         T1=t1_keep, T2=t2_keep, T3=t3_keep, T4=t4_keep))
    P = pd.DataFrame(recs).set_index("idx")
    assert P.inputs_before_935.all()

    specs = {"T1": ["c934", "c934_tmin", "ema20_prev", "trend"], "T2": ["open930", "prev_cash", "prev_close1600", "gap"],
             "T3": ["fc_range", "fc_med20"], "T4": ["on_range", "on_med20", "on_nbars"]}
    results, results2 = [], []
    for f, cols in specs.items():
        keep = P[f].to_numpy()
        out = P[["date", "side", "exit", "usd", "R", "bp"] + cols].copy()
        out["decision"] = np.where(keep, "keep", "remove")
        path = os.path.join(OUT, f"{f}_decisions.csv")
        out.to_csv(path, index=False)
        r = evaluate(f, orb, pd.Series(keep, index=orb.index).to_numpy(), book)
        r["decisions_csv"] = path
        results.append(r)
        results2.append(evaluate(f, orb, keep, book, cost_extra=1.0))
    # Holm on one-sided Welch p-values across the four tries (report)
    ps = np.array([r["p_one_sided"] for r in results])
    order = np.argsort(ps)
    adj = np.empty(4)
    run = 0.0
    for rank, j in enumerate(order):
        run = max(run, min(1.0, (4 - rank) * ps[j]))
        adj[j] = run
    for r, a in zip(results, adj):
        r["p_holm"] = float(a)
    P.to_csv(os.path.join(OUT, "all_inputs_per_trade.csv"))
    S.to_csv(os.path.join(OUT, "session_inputs.csv"))
    json.dump({"base": dict(n=len(orb), usd=float(orb.usd.sum())), "results": results, "results_2tick": results2},
              open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=str)
    for r, r2 in zip(results, results2):
        print(f"\n{r['filter']}: kept {r['kept']} (${r['kept_usd']:,.0f})  removed {r['removed']} "
              f"({r['share_removed']:.1%}, ${r['removed_usd']:,.0f}; 10-17 ${r['removed_usd_2010_17']:,.0f}, "
              f"18-26 ${r['removed_usd_2018_26']:,.0f})  per trade kept {r['kept_per_trade']:.2f} vs removed "
              f"{r['removed_per_trade']:.2f}  Welch t {r['welch_t']:.2f} (Holm p {r['p_holm']:.3f})")
        print(f"   DD {r['dd_before']:,.0f} -> {r['dd_after']:,.0f}; worst day {r['worst_day_before']:,.0f} -> "
              f"{r['worst_day_after']:,.0f};  (a) {r['a_removed_lose']} (b) {r['b_welch']} (c) {r['c_dd_worst']} "
              f"=> PASS {r['passed']}")
        print(f"   book: net {r['book']['net_before']:,.0f} -> {r['book']['net_after']:,.0f}; DD "
              f"{r['book']['dd_before']:,.0f} -> {r['book']['dd_after']:,.0f}; worst {r['book']['worst_day_before']:,.0f}"
              f" -> {r['book']['worst_day_after']:,.0f}")
        print(f"   2-tick: removed ${r2['removed_usd']:,.0f} ({r2['removed_usd_2010_17']:,.0f}/{r2['removed_usd_2018_26']:,.0f})"
              f" t {r2['welch_t']:.2f} DD {r2['dd_before']:,.0f}->{r2['dd_after']:,.0f} worst {r2['worst_day_before']:,.0f}"
              f"->{r2['worst_day_after']:,.0f} pass {r2['passed']}; model net {r2['model_net_before']:,.0f}->"
              f"{r2['model_net_after']:,.0f}")
        print("   eras: " + "  ".join(f"{k}: K {v['kept']['usd']:,.0f}/{v['kept']['n']} R {v['removed']['usd']:,.0f}/"
                                       f"{v['removed']['n']}" for k, v in r["eras"].items()))
        print("   years removed $: " + " ".join(f"{y}:{v['removed']['usd']:.0f}" for y, v in r["years"].items()))


if __name__ == "__main__":
    main()
