#!/usr/bin/env python3
"""
Implementer A: pre-registered calendar tests 5-14 (weak-rated ideas the user asked to test anyway).
Run from the project folder:
  cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this file>
Reads project data read-only; writes only into OUT.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.getcwd())
from calendar_days import expiry_fridays  # noqa: E402

OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests2/A"
os.makedirs(OUT, exist_ok=True)

MULT = {"ES": 5.0, "NQ": 2.0, "RTY": 5.0}
TICK = 0.25
COMM_RT = 1.00


def side_cost(sym, ticks=1):
    """Cost of trading one contract one way: slippage `ticks` ticks + half the $1 round-trip commission."""
    return ticks * TICK * MULT[sym] + COMM_RT / 2


def rt_cost(sym, ticks=1):
    return 2 * side_cost(sym, ticks)


assert abs(rt_cost("ES") - 3.5) < 1e-9 and abs(rt_cost("NQ") - 2.0) < 1e-9
assert abs(rt_cost("ES", 2) - 6.0) < 1e-9 and abs(rt_cost("NQ", 2) - 3.0) < 1e-9

LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ----------------------------------------------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------------------------------------------
S = {}
for sym in ("ES", "NQ"):
    d = pd.read_pickle(f"data/daily_sessions_{sym}.pkl").sort_index()
    S[sym] = d[d.cash_day].copy()
days = S["ES"].index
assert S["NQ"].index.equals(days)
N = len(days)
POS = pd.Series(np.arange(N), index=days)
DATA_END = days[-1]

A = {}
for sym in ("ES", "NQ"):
    d = S[sym]
    A[sym] = dict(cA=d.close_adj.values.astype(float), cR=d.close_raw.values.astype(float),
                  oA=d.open_adj.values.astype(float), oR=d.open_raw.values.astype(float),
                  inst=d.inst.values, early=d.early_close.values.astype(bool))

# month ends T (last cash_day of each month); last complete month = Oct 2026
ym = days.year * 100 + days.month
me = pd.Series(np.arange(N), index=days).groupby(np.asarray(ym)).max()
me = me[me.index <= 202610]
TIDX = me.values.astype(int)            # position of T for every complete month, Jun 2010 .. Oct 2026
TMONTH = me.index.values.astype(int)
END = days[TIDX[-1]]                    # 2026-10-30, last cash day of the last complete month
log(f"cash days {N}: {days[0].date()} .. {DATA_END.date()}; months {len(TIDX)} ({TMONTH[0]}..{TMONTH[-1]}); END={END.date()}")
EXP = set(pd.Timestamp(x) for x in expiry_fridays(days))


def idx_on_or_before(d):
    """Position of the last cash_day <= d (-1 if none)."""
    return int(days.searchsorted(pd.Timestamp(d), side="right") - 1)


def nth_friday(y, m, n):
    first = pd.Timestamp(y, m, 1)
    return first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 7 * (n - 1))


# --- 1-minute bars: closes of selected bars per session date --------------------------------------------------
def minute_closes(sym, targets):
    """For each target bar-open minute (minutes after midnight ET), the Close of that 1-min bar per date.
    Falls back to the last bar within the 10 minutes before the target if that exact bar is missing."""
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Close", "instrument_id"])
    ts = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York")
    tmin = (ts.dt.hour * 60 + ts.dt.minute).values
    date = ts.dt.tz_localize(None).dt.normalize().values
    out, fb = {}, {}
    for m in targets:
        msk = (tmin <= m) & (tmin >= m - 10)
        x = pd.DataFrame({"date": date[msk], "tmin": tmin[msk], "Close": d.Close.values[msk],
                          "inst": d.instrument_id.values[msk]}).sort_values(["date", "tmin"])
        last = x.groupby("date").tail(1).set_index("date")
        out[m] = last
        fb[m] = int((last.tmin != m).sum())
    del d
    return out, fb


log("loading 1-minute bars ...")
M1 = {}
M1["ES"], fbES = minute_closes("ES", [599, 779, 899, 954])
M1["NQ"], fbNQ = minute_closes("NQ", [899])
log("1-min fallbacks (target bar missing, used last bar within 10 min before):", {"ES": fbES, "NQ": fbNQ})


def minute_price(sym, m, i):
    """(raw close, instrument) of target bar m on cash day position i, or (nan, None)."""
    t = M1[sym][m]
    dt = days[i]
    if dt in t.index:
        r = t.loc[dt]
        return float(r.Close), int(r.inst)
    return np.nan, None


# --- hourly bars -------------------------------------------------------------------------------------------------
def load_hourly(sym):
    d = pd.read_csv(f"data/{sym}_fut_1h.csv")
    d["ts"] = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert("America/New_York")
    d = d.sort_values("ts").reset_index(drop=True)
    d["date"] = d.ts.dt.tz_localize(None).dt.normalize()
    d["hour"] = d.ts.dt.hour
    return d


# ----------------------------------------------------------------------------------------------------------------
# Statistics helpers
# ----------------------------------------------------------------------------------------------------------------
def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return float("nan")
    sd = x.std(ddof=1)
    return float(x.mean() / (sd / np.sqrt(len(x)))) if sd > 0 else float("nan")


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def block_id(years):
    return (np.asarray(years) - 2010) // 2


def blocks_positive(dates, vals):
    s = pd.Series(np.asarray(vals, float)).groupby(block_id(pd.DatetimeIndex(dates).year)).sum()
    return f"{int((s > 0).sum())}/{len(s)}"


def by_year(dates, vals):
    s = pd.Series(np.asarray(vals, float)).groupby(pd.DatetimeIndex(dates).year).sum()
    return {str(k): round(float(v), 2) for k, v in s.items()}


def fnum(x, nd=4):
    if x is None:
        return None
    x = float(x)
    if np.isnan(x) or np.isinf(x):
        return None
    return round(x, nd)


RESULTS = []


def trade_summary(tid, market, ev, post_start, bench_col=None, notes="", extra_notes=None):
    """ev columns: date (year/period assignment), net_usd, net_usd2, gross_bp, net_bp, [bench_col]."""
    ev = ev.reset_index(drop=True)
    n = len(ev)
    t = tstat(ev[bench_col]) if bench_col else tstat(ev.net_usd)
    post = ev[ev.date > post_start] if post_start is not None else ev.iloc[0:0]
    r = dict(id=tid, market=market, events=int(n),
             gross_bp_mean=fnum(ev.gross_bp.mean()),
             net_bp_mean=fnum(ev.net_bp.mean()),
             net_usd_mean=fnum(ev.net_usd.mean(), 3),
             net_usd_total=fnum(ev.net_usd.sum(), 2),
             net_usd_mean_2ticks=fnum(ev.net_usd2.mean(), 3),
             benchmark_excess_bp=fnum(ev[bench_col].mean()) if bench_col else None,
             t_event=fnum(t),
             post_paper_events=int(len(post)),
             post_paper_net_usd_mean=fnum(post.net_usd.mean(), 3) if len(post) else 0.0,
             two_year_blocks_positive=blocks_positive(ev.date, ev.net_usd),
             by_year_net_usd=by_year(ev.date, ev.net_usd),
             notes=notes)
    if r["benchmark_excess_bp"] is None:
        r.pop("benchmark_excess_bp")
    RESULTS.append(r)
    log(f"[{tid}] {market} n={n} gross={r['gross_bp_mean']}bp net={r['net_bp_mean']}bp net$={r['net_usd_mean']} "
        f"tot$={r['net_usd_total']} 2tk$={r['net_usd_mean_2ticks']} excess={r.get('benchmark_excess_bp')} "
        f"t={r['t_event']} post n={r['post_paper_events']} post$={r['post_paper_net_usd_mean']} "
        f"blocks={r['two_year_blocks_positive']}")
    if notes:
        log("    notes:", notes)
    return r


def desc_summary(tid, market, ev_bp, ev_usd, ev_dates, cmp_bp, cmp_dates, notes=""):
    """Descriptive: mean bp, Welch t vs comparison days. $ fields are GROSS moves of 1 long micro (no costs)."""
    ev_bp, cmp_bp = np.asarray(ev_bp, float), np.asarray(cmp_bp, float)
    ev_dates, cmp_dates = pd.DatetimeIndex(ev_dates), pd.DatetimeIndex(cmp_dates)
    t = welch(ev_bp, cmp_bp)
    # 2-year blocks: event mean bp minus comparison mean bp inside the same block > 0
    eb = pd.Series(ev_bp).groupby(block_id(ev_dates.year)).mean()
    cb = pd.Series(cmp_bp).groupby(block_id(cmp_dates.year)).mean()
    diff = (eb - cb.reindex(eb.index)).dropna()
    r = dict(id=tid, market=market, events=int(len(ev_bp)),
             gross_bp_mean=fnum(ev_bp.mean()), net_bp_mean=fnum(ev_bp.mean()),
             net_usd_mean=fnum(np.mean(ev_usd), 3), net_usd_total=fnum(np.sum(ev_usd), 2),
             benchmark_excess_bp=fnum(ev_bp.mean() - cmp_bp.mean()),
             t_event=fnum(t), post_paper_events=0, post_paper_net_usd_mean=0.0,
             two_year_blocks_positive=f"{int((diff > 0).sum())}/{len(diff)}",
             by_year_net_usd=by_year(ev_dates, ev_usd),
             notes=(f"DESCRIPTIVE (no direction, no costs): $ fields are gross $ of 1 long micro; "
                    f"comparison mean {cmp_bp.mean():.3f} bp (sd {cmp_bp.std(ddof=1):.2f}, n={len(cmp_bp)}); "
                    f"event sd {ev_bp.std(ddof=1):.2f} bp; t = two-sided Welch t vs comparison; "
                    f"|t|>=2 notable: {'YES' if abs(t) >= 2 else 'no'}; blocks = 2-yr blocks where event mean > "
                    f"comparison mean in that block; no paper sample end so post_paper fields are 0. " + notes))
    RESULTS.append(r)
    log(f"[{tid}] {market} n={len(ev_bp)} mean={ev_bp.mean():.3f}bp cmp={cmp_bp.mean():.3f}bp (n={len(cmp_bp)}) "
        f"diff={ev_bp.mean() - cmp_bp.mean():.3f} welch t={t:.3f} blocks={r['two_year_blocks_positive']}")
    return r


def ev_frame(rows):
    return pd.DataFrame(rows, columns=["date", "net_usd", "net_usd2", "gross_bp", "net_bp", "excess_bp",
                                       "gross_excess_bp", "extra"])


# ================================================================================================================
# 5. End-of-month reversal held one month (Graziani TSR)
# ================================================================================================================
log("\n=== 5. End-of-month reversal held one month ===")
es = A["ES"]
rows5, rows5a, rowsBH, allm = [], [], [], []
for k in range(len(TIDX) - 1):
    iT, iT1 = TIDX[k], TIDX[k + 1]
    Tm = days[iT]
    i4 = idx_on_or_before(nth_friday(Tm.year, Tm.month, 4))
    r_w4 = (es["cA"][iT] - es["cA"][i4]) / es["cR"][i4]
    p = -int(np.sign(r_w4))
    pts = es["cA"][iT1] - es["cA"][iT]
    rolls = int((es["inst"][iT + 1:iT1 + 1] != es["inst"][iT:iT1]).sum())
    cost, cost2 = rt_cost("ES") * (1 + rolls), rt_cost("ES", 2) * (1 + rolls)
    base = es["cR"][iT]
    exit_date = days[iT1]

    def mk(pp):
        g = pp * pts * MULT["ES"]
        return [exit_date, g - cost, g - cost2, pp * pts / base * 1e4, (g - cost) / (MULT["ES"] * base) * 1e4,
                np.nan, np.nan, rolls]
    bh = mk(1)
    rowsBH.append(bh)
    s_row = mk(p) if p != 0 else None
    l_row = mk(1) if p == 1 else None
    if s_row:
        rows5.append(s_row)
    if l_row:
        rows5a.append(l_row)
    allm.append(dict(date=exit_date, bh=bh[1], strat=s_row[1] if s_row else 0.0, lo=l_row[1] if l_row else 0.0,
                     p=p))
e5, e5a, eBH = ev_frame(rows5), ev_frame(rows5a), ev_frame(rowsBH)
am = pd.DataFrame(allm)
d_s, d_l = am.strat - am.bh, am.lo - am.bh
POST5 = pd.Timestamp("2019-12-31")
amp = am[am.date > POST5]
note5 = (f"Year/period by exit month (holding month). Months {len(am)} (holding Jul 2010..Oct 2026); zero-signal months "
         f"{int((am.p == 0).sum())}; rolls charged in {int((eBH.extra > 0).sum())} months. Buy-and-hold (1 MES long "
         f"every month, same cost rule): mean ${am.bh.mean():.2f}/month, total ${am.bh.sum():.0f}, t {tstat(am.bh):.2f}; "
         f"post-2019 B&H ${amp.bh.mean():.2f}/month. Strategy per calendar month (flat=0): ${am.strat.mean():.2f}; "
         f"minus B&H ${d_s.mean():.2f}/month (paired t {tstat(d_s):.2f}); post-2019 strategy ${amp.strat.mean():.2f} vs "
         f"B&H ${amp.bh.mean():.2f}. Months long {int((am.p == 1).sum())}, short {int((am.p == -1).sum())}.")
pass5 = (e5.net_usd.mean() > 0 and tstat(e5.net_usd) >= 2 and e5[e5.date > POST5].net_usd.mean() > 0
         and d_s.mean() > 0)
trade_summary("5-primary", "MES", e5, POST5, notes=note5 + f" PASS={pass5}")
note5a = (f"Long-only (r_w4<0 months). Per calendar month incl. flat months: ${am.lo.mean():.2f} vs B&H "
          f"${am.bh.mean():.2f} (diff ${d_l.mean():.2f}, paired t {tstat(d_l):.2f}); post-2019 per month "
          f"${amp.lo.mean():.2f} vs B&H ${amp.bh.mean():.2f}. Long-only months mean ${e5a.net_usd.mean():.2f} vs B&H "
          f"mean over the same months ${eBH.net_usd[am.p.values == 1].mean():.2f}.")
pass5a = (e5a.net_usd.mean() > 0 and tstat(e5a.net_usd) >= 2 and
          e5a[e5a.date > POST5].net_usd.mean() > 0 and d_l.mean() > 0)
trade_summary("5a-longonly", "MES", e5a, POST5, notes=note5a + f" PASS={pass5a}")
trade_summary("5-buyhold-reference", "MES", eBH, POST5,
              notes="Reference only (not a trial): 1 MES long every month T(m)->T(m+1), 1 RT + 1 RT per roll.")


# ================================================================================================================
# 6. Classic turn-of-month window [-1,+3]
# ================================================================================================================
log("\n=== 6. Turn-of-month [-1,+3] ===")
tom_ret_days = set()
for iT in TIDX:
    tom_ret_days.update(range(iT, iT + 4))
for sym, tid in (("ES", "6-MES"), ("NQ", "6a-MNQ")):
    a = A[sym]
    # benchmark: all 4-session windows (close s -> close s+4) whose return days s+1..s+4 avoid every T..T+3
    bm = []
    for s in range(N - 4):
        if days[s] > END:
            break
        if any(j in tom_ret_days for j in range(s + 1, s + 5)):
            continue
        bm.append((days[s].year, (a["cA"][s + 4] - a["cA"][s]) / a["cR"][s] * 1e4))
    bm = pd.DataFrame(bm, columns=["year", "bp"]).groupby("year").bp.agg(["mean", "size"])
    rows = []
    for iT in TIDX:
        i0, i1 = iT - 1, iT + 3
        if i1 >= N or i0 < 0:
            continue
        pts = a["cA"][i1] - a["cA"][i0]
        base = a["cR"][i0]
        g = pts * MULT[sym]
        gbp = pts / base * 1e4
        nbp = (g - rt_cost(sym)) / (MULT[sym] * base) * 1e4
        b = bm.loc[days[i0].year, "mean"]
        rows.append([days[i0], g - rt_cost(sym), g - rt_cost(sym, 2), gbp, nbp, nbp - b, gbp - b, b])
    ev = ev_frame(rows)
    exb = blocks_positive(ev.date, ev.excess_bp)
    ok = ev.excess_bp.mean() > 0 and tstat(ev.excess_bp) >= 2
    bl = pd.Series(ev.net_usd.values).groupby(block_id(ev.date.dt.year)).mean()
    ok = ok and 3 * int((bl > 0).sum()) >= 2 * len(bl)
    trade_summary(tid, "M" + sym, ev, None, bench_col="excess_bp",
                  notes=(f"Excess = net bp - same-year benchmark (mean gross bp of 4-session windows not overlapping "
                         f"any [T-1,T+3] holding period; {int(bm['size'].sum())} windows, yearly means "
                         f"{bm['mean'].min():.1f}..{bm['mean'].max():.1f} bp). Gross excess mean "
                         f"{ev.gross_excess_bp.mean():.3f} bp (t {tstat(ev.gross_excess_bp):.2f}). Blocks field = "
                         f"net $; blocks of net excess positive {exb}. t_event is on net excess bp. Paper sample "
                         f"ended 2005 so all events are post-paper (post_paper fields = full sample). PASS={ok}"))
    RESULTS[-1]["post_paper_events"] = int(len(ev))
    RESULTS[-1]["post_paper_net_usd_mean"] = fnum(ev.net_usd.mean(), 3)


# ================================================================================================================
# 7. VIX-settlement Wednesday (descriptive)
# ================================================================================================================
log("\n=== 7. VIX-settlement Wednesday ===")
W = []
non_wed = []
for y in range(2010, 2027):
    for m in range(1, 13):
        Fcal = nth_friday(y, m, 3)
        if Fcal > DATA_END:
            # beyond the data: cannot check cash_day status; F taken as the calendar 3rd Friday (Nov 20 2026 is a
            # normal NYSE day). Only matters for W = Oct 21 2026.
            F = Fcal
            iW = idx_on_or_before(F - pd.Timedelta(days=30))
            if 1 <= iW and days[iW] <= END and days[iW] > F - pd.Timedelta(days=37):
                W.append(iW)
                if days[iW].weekday() != 2:
                    non_wed.append(str(days[iW].date()))
            continue
        iF = idx_on_or_before(Fcal)
        if iF < 0:
            continue
        F = days[iF]
        iW = idx_on_or_before(F - pd.Timedelta(days=30))
        if iW < 1 or days[iW] > END:
            continue
        if days[iW] < days[0] + pd.Timedelta(days=1):
            continue
        W.append(iW)
        if days[iW].weekday() != 2:
            non_wed.append(str(days[iW].date()))
W = sorted(set(W))
Wset = set(W)
log(f"VIX settlement days: {len(W)} ({days[W[0]].date()}..{days[W[-1]].date()}); not Wednesday: {non_wed}")
for sym in ("ES", "NQ"):
    a = A[sym]
    on = (a["oA"][1:] - a["cA"][:-1]) / a["cR"][:-1] * 1e4          # overnight into day i (i>=1)
    on_usd = (a["oA"][1:] - a["cA"][:-1]) * MULT[sym]
    idd = (a["cA"] - a["oA"]) / a["oR"] * 1e4
    idd_usd = (a["cA"] - a["oA"]) * MULT[sym]
    ii = np.arange(1, N)
    keep = days[ii] <= END
    isW = np.array([i in Wset for i in ii])
    desc_summary(f"7-{sym}-overnight", sym, on[isW & keep], on_usd[isW & keep], days[ii[isW & keep]],
                 on[~isW & keep], days[ii[~isW & keep]],
                 notes="Leg: close of cash_day before W -> 09:30 open of W (back-adjusted points / raw prior close).")
    ii = np.arange(N)
    keep = days <= END
    isW = np.array([i in Wset for i in ii])
    desc_summary(f"7-{sym}-intraday", sym, idd[isW & keep], idd_usd[isW & keep], days[isW & keep],
                 idd[~isW & keep], days[~isW & keep],
                 notes="Leg: 09:30 open -> close (15:59 bar; 13:14 bar on early-close days) of W.")


# ================================================================================================================
# 8. Overnight long into QUARTERLY expiry only
# ================================================================================================================
log("\n=== 8. Overnight into quarterly expiry ===")
Elist = sorted(i for i in (POS[e] for e in EXP if e in POS.index) if i >= 1 and days[i] <= END)
for sym in ("ES", "NQ"):
    a = A[sym]
    ii = np.arange(1, N)
    keep = (days[ii] <= END) & np.array([days[i] not in EXP for i in ii])
    bench = ((a["oA"][ii] - a["cA"][ii - 1]) / a["cR"][ii - 1] * 1e4)[keep]
    bmean = bench.mean()
    for quarterly, tid in ((True, f"8-M{sym}-quarterly"), (False, f"8a-M{sym}-offquarterly")):
        rows, skipped = [], []
        for i in Elist:
            if (days[i].month in (3, 6, 9, 12)) != quarterly:
                continue
            if a["inst"][i - 1] != a["inst"][i]:
                skipped.append(str(days[i].date()))
                continue
            pts = a["oR"][i] - a["cR"][i - 1]
            base = a["cR"][i - 1]
            g = pts * MULT[sym]
            gbp = pts / base * 1e4
            nbp = (g - rt_cost(sym)) / (MULT[sym] * base) * 1e4
            rows.append([days[i - 1], g - rt_cost(sym), g - rt_cost(sym, 2), gbp, nbp, gbp - bmean, gbp - bmean,
                         nbp - bmean])
        ev = ev_frame(rows)
        tg = tstat(ev.gross_excess_bp)
        ok = ev.gross_excess_bp.mean() > 0 and tg >= 2 and ev.net_usd2.mean() > 0
        trade_summary(tid, "M" + sym, ev, pd.Timestamp("2021-12-31"), bench_col="gross_excess_bp",
                      notes=(f"Benchmark: all other cash_day overnights excl. all pre-expiry nights, mean {bmean:.3f} bp "
                             f"(n={len(bench)}, full sample). benchmark_excess_bp/t_event are GROSS excess (pass rule); "
                             f"net excess mean {ev.extra.mean():.3f} bp. Skipped (instrument changed): {skipped}. "
                             f"Period by entry date; post-paper = E after 2021-12. PASS={ok}"))


# ================================================================================================================
# 9. Index-rebalance close on quarterly-expiry Fridays (descriptive)
# ================================================================================================================
log("\n=== 9. Quarterly-expiry close (rebalance) ===")
for sym in ("ES", "NQ"):
    a = A[sym]
    lh_bp, lh_usd, on_bp, on_usd = {}, {}, {}, {}
    for i in range(N):
        if days[i] > END:
            break
        if not a["early"][i]:
            p15, ins = minute_price(sym, 899, i)
            if not np.isnan(p15) and ins == a["inst"][i]:
                lh_bp[i] = (a["cR"][i] - p15) / p15 * 1e4
                lh_usd[i] = (a["cR"][i] - p15) * MULT[sym]
        if i + 1 < N:
            on_bp[i] = (a["oA"][i + 1] - a["cA"][i]) / a["cR"][i] * 1e4
            on_usd[i] = (a["oA"][i + 1] - a["cA"][i]) * MULT[sym]
    Q = [i for i in Elist if days[i].month in (3, 6, 9, 12)]
    Qd = [i for i in Q if days[i].month == 12]
    cmp_ = [i for i in range(N) if days[i] <= END and days[i].weekday() == 4 and days[i] not in EXP]
    for leg, bp, usd, desc in (("lasthour", lh_bp, lh_usd, "15:00 (14:59-bar close) -> 16:00 (15:59-bar close)"),
                               ("overnight", on_bp, on_usd, "close of Q -> 09:30 open of next cash_day (adj)")):
        cmp_i = [i for i in cmp_ if i in bp]
        for evs, sfx in ((Q, ""), (Qd, "-Dec")):
            ev_i = [i for i in evs if i in bp]
            desc_summary(f"9-{sym}-{leg}{sfx}", sym, [bp[i] for i in ev_i], [usd[i] for i in ev_i],
                         days[ev_i], [bp[i] for i in cmp_i], days[cmp_i],
                         notes=(f"Leg {desc}. Q = expiry days in {'Dec only' if sfx else 'Mar/Jun/Sep/Dec'}; "
                                f"comparison = cash_day Fridays that are not expiry days"
                                f"{', excluding early-close Fridays (no 15-16h)' if leg == 'lasthour' else ''}."))


# ================================================================================================================
# 10. Russell reconstitution day (descriptive)
# ================================================================================================================
log("\n=== 10. Russell reconstitution ===")
rty = load_hourly("RTY")
rty_first = rty.date.min()
H = {}
for h in (9, 14, 15):
    x = rty[rty.hour == h].groupby("date").tail(1).set_index("date")
    H[h] = x
R = []
for y in range(2017, 2027):
    iR = idx_on_or_before(nth_friday(y, 6, 4))
    R.append(iR)
Rset = set(R)
log("R days:", [str(days[i].date()) for i in R])


def rty_px(h, i):
    dt = days[i]
    if dt in H[h].index:
        r = H[h].loc[dt]
        return float(r.Close), int(r.instrument_id)
    return np.nan, None


rlh, rlh_usd, ron, ron_usd = {}, {}, {}, {}
for i in range(N):
    if days[i] < rty_first or days[i] > END:
        continue
    p14, i14 = rty_px(14, i)
    p15, i15 = rty_px(15, i)
    if not A["ES"]["early"][i] and not np.isnan(p14) and not np.isnan(p15) and i14 == i15:
        rlh[i] = (p15 - p14) / p14 * 1e4
        rlh_usd[i] = (p15 - p14) * MULT["RTY"]
    if i + 1 < N and not np.isnan(p15):
        p9, i9 = rty_px(9, i + 1)
        if not np.isnan(p9) and i9 == i15:
            ron[i] = (p9 - p15) / p15 * 1e4
            ron_usd[i] = (p9 - p15) * MULT["RTY"]
elh, elh_usd, eon, eon_usd = {}, {}, {}, {}
a = A["ES"]
ES_CMP_START = pd.Timestamp("2017-01-01")
for i in range(N):
    if days[i] < ES_CMP_START or days[i] > END:
        continue
    if not a["early"][i]:
        p15, ins = minute_price("ES", 899, i)
        if not np.isnan(p15) and ins == a["inst"][i]:
            elh[i] = (a["cR"][i] - p15) / p15 * 1e4
            elh_usd[i] = (a["cR"][i] - p15) * MULT["ES"]
    if i + 1 < N:
        p10, ins = minute_price("ES", 599, i + 1)
        if not np.isnan(p10) and ins == a["inst"][i + 1]:
            p10a = p10 + (a["oA"][i + 1] - a["oR"][i + 1])
            eon[i] = (p10a - a["cA"][i]) / a["cR"][i] * 1e4
            eon_usd[i] = (p10a - a["cA"][i]) * MULT["ES"]
for sym, leg, bp, usd, desc in (
        ("RTY", "lasthour", rlh, rlh_usd, "15:00 (close of 14:00 hourly bar) -> 16:00 (close of 15:00 bar)"),
        ("RTY", "close-to-10am", ron, ron_usd, "16:00 of R -> next cash_day 10:00 (close of 09:00 bar), same contract"),
        ("ES", "lasthour", elh, elh_usd, "15:00 (14:59 1-min close) -> 16:00 (15:59 close)"),
        ("ES", "close-to-10am", eon, eon_usd, "16:00 close of R -> next cash_day 10:00 (09:59 1-min close, adj)")):
    ev_i = [i for i in R if i in bp]
    cmp_i = [i for i in bp if days[i].weekday() == 4 and i not in Rset]
    desc_summary(f"10-{sym}-{leg}", sym, [bp[i] for i in ev_i], [usd[i] for i in ev_i], days[ev_i],
                 [bp[i] for i in cmp_i], days[cmp_i],
                 notes=(f"Leg {desc}. Events: {[str(days[i].date()) for i in ev_i]}. Comparison: all other cash_day "
                        f"Fridays {'with RTY data (2017-07-10+)' if sym == 'RTY' else 'from 2017-01-01'} to {END.date()}"
                        f"{', excl. early-close Fridays' if leg == 'lasthour' else ''}. RTY $ = M2K $5/pt. Anecdotal n."))


# ================================================================================================================
# 11. Quarter-end window dressing
# ================================================================================================================
log("\n=== 11. Quarter-end window dressing ===")
a = A["ES"]
rows = []
for iT in TIDX:
    i0 = iT - 3
    pts = a["cA"][iT] - a["cA"][i0]
    base = a["cR"][i0]
    g = pts * MULT["ES"]
    rows.append(dict(date=days[i0], qe=days[iT].month in (3, 6, 9, 12), net_usd=g - rt_cost("ES"),
                     net_usd2=g - rt_cost("ES", 2), gross_bp=pts / base * 1e4,
                     net_bp=(g - rt_cost("ES")) / (MULT["ES"] * base) * 1e4))
w11 = pd.DataFrame(rows)
w11["year"] = w11.date.dt.year
nq_mean = w11[~w11.qe].groupby("year").gross_bp.mean()
qe = w11[w11.qe].copy()
qe["bench"] = qe.year.map(nq_mean)
qe["excess_bp"] = qe.net_bp - qe.bench
qe["gross_excess_bp"] = qe.gross_bp - qe.bench
qe["extra"] = qe.bench
ok11 = qe.excess_bp.mean() > 0 and tstat(qe.excess_bp) >= 2
trade_summary("11-QE", "MES", qe[["date", "net_usd", "net_usd2", "gross_bp", "net_bp", "excess_bp",
                                  "gross_excess_bp", "extra"]], None, bench_col="excess_bp",
              notes=(f"Excess = QE net bp - same-year mean gross bp of the T-3->T window in non-quarter-end months "
                     f"(mean benchmark {qe.bench.mean():.2f} bp). Gross excess {qe.gross_excess_bp.mean():.3f} bp "
                     f"(t {tstat(qe.gross_excess_bp):.2f}). Paper sample ended 1998: all events post-paper. PASS={ok11}"))
RESULTS[-1]["post_paper_events"] = int(len(qe))
RESULTS[-1]["post_paper_net_usd_mean"] = fnum(qe.net_usd.mean(), 3)
nqe = w11[~w11.qe].copy()
for c in ("excess_bp", "gross_excess_bp", "extra"):
    nqe[c] = np.nan
trade_summary("11a-nonQE", "MES", nqe[["date", "net_usd", "net_usd2", "gross_bp", "net_bp", "excess_bp",
                                       "gross_excess_bp", "extra"]], None,
              notes=("Same T-3->T long window in the 8 non-quarter-end months (comparison). Welch t of QE vs non-QE "
                     f"gross bp: {welch(qe.gross_bp, nqe.gross_bp):.2f}. All post-paper."))
RESULTS[-1]["post_paper_events"] = int(len(nqe))
RESULTS[-1]["post_paper_net_usd_mean"] = fnum(nqe.net_usd.mean(), 3)


# ================================================================================================================
# 12. Daily threshold-rebalancing signal
# ================================================================================================================
log("\n=== 12. Threshold-rebalancing signal ===")
zn = load_hourly("ZN")
roll = zn.instrument_id.ne(zn.instrument_id.shift()) & zn.instrument_id.shift().notna()
jump = (zn.Open - zn.Close.shift()).where(roll, 0.0)
zn["adj"] = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
zn["aC"] = zn.Close + zn.adj
# ZN 16:00 price for cash day d = close of the last bar opening at or before d 15:00 ET (the 15:00 bar normally)
tgt = pd.DataFrame({"tgt": (days + pd.Timedelta(hours=15)).tz_localize("America/New_York"), "i": np.arange(N)})
zz = zn[["ts", "Close", "aC"]].rename(columns={"ts": "bar"})
zz["tgt"] = zz.bar
tgt["tgt"] = tgt.tgt.astype(zz.tgt.dtype)
mz = pd.merge_asof(tgt.sort_values("tgt"), zz.sort_values("tgt"), on="tgt", direction="backward",
                   allow_exact_matches=True)   # last bar whose OPEN time is <= day 15:00 ET
mz = mz.sort_values("i").reset_index(drop=True)
not15 = mz[(mz.bar.dt.hour != 15) | (mz.bar.dt.tz_localize(None).dt.normalize() != days[mz.i].values)]
log(f"ZN: days without a 15:00 ET bar (used last earlier bar): {len(not15)}; of which bar not on same date: "
    f"{int((mz.bar.dt.tz_localize(None).dt.normalize() != days[mz.i].values).sum())}")
znR, znA = mz.Close.values, mz.aC.values
rZN = np.full(N, np.nan)
rZN[1:] = (znA[1:] - znA[:-1]) / znR[:-1]
es = A["ES"]
rES = np.full(N, np.nan)
rES[1:] = (es["cA"][1:] - es["cA"][:-1]) / es["cR"][:-1]
nq = A["NQ"]
rNQ = np.full(N, np.nan)
rNQ[1:] = (nq["cA"][1:] - nq["cA"][:-1]) / nq["cR"][:-1]
deltas = np.round(np.arange(26) * 0.001, 4)
w = np.full(len(deltas), 0.60)
sig = np.full(N, np.nan)
for t in range(1, N):
    gE, gZ = 1 + rES[t], 1 + rZN[t]
    wpre = w * gE / (w * gE + (1 - w) * gZ)
    dev = wpre - 0.60
    sig[t] = dev.mean()
    w = np.where(np.abs(dev) >= deltas - 1e-12, 0.60, wpre)


def ols_nw(y, x, L=5):
    X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    u = y - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    Xu = X * u[:, None]
    Sm = Xu.T @ Xu
    for lag in range(1, L + 1):
        G = Xu[lag:].T @ Xu[:-lag]
        Sm += (1 - lag / (L + 1)) * (G + G.T)
    V = XtXi @ Sm @ XtXi
    ols_se = np.sqrt(np.sum(u ** 2) / (len(y) - 2) * XtXi[1, 1])
    return float(beta[1]), float(beta[1] / np.sqrt(V[1, 1])), float(beta[1] / ols_se)


tt = np.arange(1, N - 1)
tt = tt[days[tt + 1] <= END]
log(f"signal: n={len(tt)} mean={np.nanmean(sig[tt]) * 100:.4f}% sd={np.nanstd(sig[tt]) * 100:.4f}% "
    f"|sig|>=0.5% days: {int((np.abs(sig[tt]) >= 0.005).sum())}")
for sym, ret, tid in (("ES", rES, "12-forecast-ES"), ("NQ", rNQ, "12a-forecast-NQ")):
    y = ret[tt + 1] * 1e4
    x = sig[tt]
    b, tnw, tols = ols_nw(y, x)
    post = tt[days[tt] > pd.Timestamp("2023-03-31")]
    bp_, tp_, _ = ols_nw(ret[post + 1] * 1e4, sig[post])
    sub = {}
    for nm, lo, hi in (("2010-2016", "2010-01-01", "2016-12-31"), ("2017-2023Q1", "2017-01-01", "2023-03-31")):
        m = tt[(days[tt] >= pd.Timestamp(lo)) & (days[tt] <= pd.Timestamp(hi))]
        sub[nm] = ols_nw(ret[m + 1] * 1e4, sig[m])[:2]
    RESULTS.append(dict(
        id=tid, market=sym, events=int(len(tt)), net_usd_mean=0.0, net_usd_total=0.0, net_bp_mean=0.0,
        t_event=fnum(tnw), post_paper_events=int(len(post)), post_paper_net_usd_mean=0.0,
        two_year_blocks_positive="n/a",
        notes=(f"FORECAST REGRESSION (not a trade; $ fields set to 0): r_{sym}(t+1) in bp on signal_t (decimal). "
               f"slope = {b:.2f} bp per unit signal (= {b / 100:.3f} bp per 1% signal); NW(5) t = {tnw:.3f} "
               f"(plain OLS t {tols:.2f}); support (slope<0 and |t|>=2): {b < 0 and abs(tnw) >= 2}. "
               f"Post 2023-03: slope {bp_:.2f}, NW t {tp_:.2f}, n={len(post)}. Subperiods: "
               + "; ".join(f"{k}: slope {v[0]:.2f}, t {v[1]:.2f}" for k, v in sub.items()))))
    log(f"[{tid}] slope={b:.3f} bp/unit NW t={tnw:.3f} OLS t={tols:.3f}; post-2023Q1 slope={bp_:.3f} t={tp_:.3f}")

# tradable rule
posn = np.zeros(N)
thr = 0.005
for t in tt:
    if abs(sig[t]) >= thr:
        posn[t] = -np.sign(sig[t])
rows, rows_nr, n_roll = [], [], 0
cost_day = np.zeros(N)
cost_day2 = np.zeros(N)
roll_day = np.zeros(N)
prev = 0.0
tlist = list(tt)
for k, t in enumerate(tlist):
    p = posn[t]
    traded = abs(p - prev)
    if traded:
        tgt_day = t if p != 0 else tlist[k - 1]
        cost_day[tgt_day] += traded * side_cost("ES")
        cost_day2[tgt_day] += traded * side_cost("ES", 2)
    if p != 0 and es["inst"][t + 1] != es["inst"][t]:
        roll_day[t] = 1
        n_roll += 1
    prev = p
if prev != 0:
    cost_day[tlist[-1]] += abs(prev) * side_cost("ES")
    cost_day2[tlist[-1]] += abs(prev) * side_cost("ES", 2)
ev_rows, ev_nr = [], []
for t in tlist:
    if posn[t] == 0:
        continue
    pts = es["cA"][t + 1] - es["cA"][t]
    g = posn[t] * pts * MULT["ES"]
    base = es["cR"][t]
    c = cost_day[t] + roll_day[t] * rt_cost("ES")
    c2 = cost_day2[t] + roll_day[t] * rt_cost("ES", 2)
    ev_rows.append([days[t], g - c, g - c2, posn[t] * pts / base * 1e4, (g - c) / (MULT["ES"] * base) * 1e4,
                    np.nan, np.nan, g - cost_day[t]])
e12 = ev_frame(ev_rows)
ok12 = e12.net_usd.mean() > 0 and tstat(e12.net_usd) >= 2
bl = pd.Series(e12.net_usd.values).groupby(block_id(e12.date.dt.year)).sum()
ok12 = ok12 and 3 * int((bl > 0).sum()) >= 2 * len(bl)
n_changes = int(np.sum(np.abs(np.diff(np.r_[0, posn[tt], 0])) > 0))
trade_summary("12-tradable", "MES", e12, pd.Timestamp("2023-03-31"),
              notes=(f"Day-level: events = days in position (long {int((posn[tt] > 0).sum())}, short "
                     f"{int((posn[tt] < 0).sum())}); position -sign(signal_t) when |signal_t|>=0.5%, close t->close t+1; "
                     f"costs per contract traded ($1.75/side) assigned to the new position's day (exit costs to the last "
                     f"day held); position changes {n_changes}; plus 1 RT whenever a held position crosses a contract "
                     f"roll ({n_roll} times). Without roll costs: mean ${e12.extra.mean():.3f}/day, "
                     f"t {tstat(e12.extra):.2f}. PASS={ok12}"))


# ================================================================================================================
# 13. Stock-only month-end rebalancing fade
# ================================================================================================================
log("\n=== 13. Stock-only month-end fade ===")
a = A["ES"]
rows, nflip_tot, zero_days = [], 0, 0
early_used = []
for k in range(1, len(TIDX)):
    iTp, iT = TIDX[k - 1], TIDX[k]
    if iT + 1 >= N:
        continue
    ps = []
    for t in range(iT - 4, iT + 1):
        m = 779 if a["early"][t] else 954
        if a["early"][t]:
            early_used.append(str(days[t].date()))
        p, ins = minute_price("ES", m, t)
        assert ins == a["inst"][t]
        p_adj = p + (a["cA"][t] - a["cR"][t])
        cal = np.sign(p_adj - a["cA"][iTp])
        ps.append(-cal)
        zero_days += int(cal == 0)
    ps = np.array(ps)
    trades = np.abs(np.diff(np.r_[0.0, ps, 0.0]))
    nflip_tot += int(np.sum(np.abs(np.diff(ps)) == 2))
    gross_pts = sum(ps[j] * (a["cA"][iT - 4 + j + 1] - a["cA"][iT - 4 + j]) for j in range(5))
    g = gross_pts * MULT["ES"]
    c, c2 = trades.sum() * side_cost("ES"), trades.sum() * side_cost("ES", 2)
    base = a["cR"][iT - 4]
    rows.append([days[iT - 4], g - c, g - c2, gross_pts / base * 1e4, (g - c) / (MULT["ES"] * base) * 1e4,
                 np.nan, np.nan, trades.sum()])
e13 = ev_frame(rows)
POST13 = pd.Timestamp("2023-03-31")
bl = pd.Series(e13.net_usd.values).groupby(block_id(e13.date.dt.year)).sum()
ok13 = (e13.net_usd.mean() > 0 and tstat(e13.net_usd) >= 2 and e13[e13.date > POST13].net_usd.mean() > 0
        and 3 * int((bl > 0).sum()) >= 2 * len(bl))
trade_summary("13", "MES", e13, POST13,
              notes=(f"Months Jul 2010..Oct 2026 (Jun 2010 lacks T_prev). Position -sign(G_ES-1) held close t->close t+1 "
                     f"for t=T-4..T, exit close T+1; G_ES from the 15:55 price (15:54-bar close; 12:59-bar close on "
                     f"early-close days: {early_used}) vs close of T_prev, back-adjusted. Flips {nflip_tot}; "
                     f"contracts traded per month avg {e13.extra.mean():.2f}; zero-signal days {zero_days}. "
                     f"bp base = raw close of T-4. Post-paper = months after 2023-03. PASS={ok13}"))


# ================================================================================================================
# 14. Dash-for-cash entry-day scan
# ================================================================================================================
log("\n=== 14. Dash-for-cash entry-day scan ===")
a = A["ES"]
R1_END, R2_START, R3_START = pd.Timestamp("2017-09-04"), pd.Timestamp("2017-09-05"), pd.Timestamp("2024-05-28")


def regime_k(dt):
    return 4 if dt < R2_START else (3 if dt < R3_START else 2)


excl_start = set()
for iT in TIDX:
    excl_start.update(range(iT - 8, iT + 4))
bench_cache = {}


def bench14(nlen, year):
    key = (nlen, year)
    if key not in bench_cache:
        v = []
        for s in range(N - nlen):
            if days[s].year != year or days[s] > END or s in excl_start:
                continue
            v.append((a["cA"][s + nlen] - a["cA"][s]) / a["cR"][s] * 1e4)
        bench_cache[key] = (float(np.mean(v)), len(v))
    return bench_cache[key]


Ls, amb = [], []
for iT in TIDX:
    cands = [iT - k for k in (4, 3, 2) if regime_k(days[iT - k]) == k]
    if len(cands) != 1:
        amb.append((str(days[iT].date()), [str(days[c].date()) for c in cands]))
    Ls.append((iT, cands[0], regime_k(days[cands[0]])))
log("L ambiguities:", amb)
peak, ev14 = {}, {}
for shift, tid in ((-1, "14-L-1"), (0, "14-L"), (1, "14-L+1")):
    rows, regs, skipped, mon14 = [], [], 0, []
    for iT, iL, k in Ls:
        i0 = iL + shift
        i1 = iT - 1
        if i0 >= i1:
            skipped += 1
            continue
        nlen = i1 - i0
        pts = a["cA"][i1] - a["cA"][i0]
        base = a["cR"][i0]
        g = pts * MULT["ES"]
        gbp = pts / base * 1e4
        nbp = (g - rt_cost("ES")) / (MULT["ES"] * base) * 1e4
        b, nb = bench14(nlen, days[i0].year)
        rows.append([days[i0], g - rt_cost("ES"), g - rt_cost("ES", 2), gbp, nbp, nbp - b, gbp - b, k])
        mon14.append(iT)
    ev = ev_frame(rows)
    reg_txt = []
    for k, nm in ((4, "T+3 era (L=T-4)"), (3, "T+2 era (L=T-3)"), (2, "T+1 era (L=T-2)")):
        x = ev[ev.extra == k]
        if len(x):
            reg_txt.append(f"{nm}: n={len(x)} net excess {x.excess_bp.mean():.2f} bp t {tstat(x.excess_bp):.2f}, "
                           f"net ${x.net_usd.mean():.2f}")
        else:
            reg_txt.append(f"{nm}: n=0 (skipped)")
    peak[tid] = ev.excess_bp.mean()
    ev14[tid] = pd.Series(ev.excess_bp.values, index=mon14)
    trade_summary(tid, "MES", ev, pd.Timestamp("2013-12-31"), bench_col="excess_bp",
                  notes=(f"Entry = L{shift:+d} close, exit close of T-1; regime from L's date; months skipped "
                         f"(entry not before T-1): {skipped}. Excess = net bp - same-year mean gross bp of all "
                         f"same-length close-to-close windows starting outside every T-8..T+3. Gross excess "
                         f"{ev.gross_excess_bp.mean():.3f} bp. By regime: " + " | ".join(reg_txt)))
best = max(peak, key=peak.get)
common = ev14["14-L+1"].index
lfl = {k: float(v.loc[common].mean()) for k, v in ev14.items()}
lfl_t = {k: tstat(v.loc[common]) for k, v in ev14.items()}
log("14 like-for-like on the", len(common), "months where L+1 exists:", {k: round(v, 3) for k, v in lfl.items()})
log("14 peak (mean net excess):", {k: round(v, 3) for k, v in peak.items()}, "-> peak at", best)
for r in RESULTS:
    if r["id"].startswith("14-"):
        r["notes"] += f" Scan: mean net excess L-1 {peak['14-L-1']:.2f}, L {peak['14-L']:.2f}, L+1 {peak['14-L+1']:.2f} bp; L is peak: {best == '14-L'}. Like-for-like on the {len(common)} months where L+1 exists (pre-2024-05-28): L-1 {lfl['14-L-1']:.2f} (t {lfl_t['14-L-1']:.2f}), L {lfl['14-L']:.2f} (t {lfl_t['14-L']:.2f}), L+1 {lfl['14-L+1']:.2f} (t {lfl_t['14-L+1']:.2f}) bp; L is peak there: {max(lfl, key=lfl.get) == '14-L'}."

# ----------------------------------------------------------------------------------------------------------------
with open(os.path.join(OUT, "results_A.json"), "w") as f:
    json.dump(RESULTS, f, indent=1, default=str)
with open(os.path.join(OUT, "log_A.txt"), "w") as f:
    f.write("\n".join(LOG) + "\n")
log(f"\nwrote {len(RESULTS)} result rows to {OUT}/results_A.json")
