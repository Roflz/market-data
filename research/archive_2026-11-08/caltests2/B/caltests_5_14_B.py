#!/usr/bin/env python3
"""
Implementer B -- pre-registered calendar tests 5-14 (user-requested "weaker" ideas; ~22 trials; nothing tuned).
Run:  cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this script>
Reads the project data read-only; writes only into OUTDIR.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

PROJ = "/run/media/roflz/Disk 2/_/market_data"
OUTDIR = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests2/B"
os.makedirs(OUTDIR, exist_ok=True)
sys.path.append(PROJ)
os.chdir(PROJ)
from calendar_days import expiry_fridays  # noqa: E402

NY = "America/New_York"
MULT = {"ES": 5.0, "NQ": 2.0}
MICRO = {"ES": "MES", "NQ": "MNQ"}
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def side_cost(sym, ticks=1):
    """Cost of one contract-side: `ticks` ticks of slippage + half of the $1.00 round-trip commission."""
    return ticks * 0.25 * MULT[sym] + 0.50


def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return float("nan")
    sd = x.std(ddof=1)
    return float(x.mean() / (sd / np.sqrt(len(x)))) if sd > 0 else float("nan")


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def blocks(years, vals):
    s = pd.Series(np.asarray(vals, float)).groupby(np.asarray(years)).sum()
    b = s.groupby((s.index.values - 2010) // 2).sum()
    return int((b > 0).sum()), int(len(b))


def fnum(x, nd=4):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    return round(float(x), nd)


# ----------------------------------------------------------------------------------------------------------------
# Calendar
# ----------------------------------------------------------------------------------------------------------------
D = {s: pd.read_pickle(f"data/daily_sessions_{s}.pkl") for s in ("ES", "NQ")}
CAL = D["ES"].index[D["ES"].cash_day]
assert CAL.equals(D["NQ"].index[D["NQ"].cash_day])
NC = len(CAL)
POS = pd.Series(np.arange(NC), index=CAL)
S = {s: D[s].reindex(CAL) for s in ("ES", "NQ")}
ROLLS = {s: D[s].index[D[s].roll_since_prev] for s in ("ES", "NQ")}


def n_rolls(sym, a, b):
    """Contract rolls flagged on any session row (cash or Globex-only) in (a, b]."""
    r = ROLLS[sym]
    return int(((r > a) & (r <= b)).sum())


_me = pd.Series(CAL, index=CAL).groupby([CAL.year, CAL.month]).max()
TS = pd.DatetimeIndex([t for t in _me.values if pd.Timestamp(t) <= pd.Timestamp("2026-10-31")])  # complete months
LAST_ENTRY = TS[-1]  # 2026-10-30: last complete month-end; legs/windows must be entered on or before this close
log(f"cash days {NC} {CAL[0].date()}..{CAL[-1].date()}; month-ends {len(TS)} {TS[0].date()}..{TS[-1].date()}")
gaps = pd.bdate_range(CAL[0], CAL[-1]).difference(D["ES"].index)
log("weekday dates with no session row at all (holidays + data gaps):", len(gaps))

EXPIRY = pd.DatetimeIndex(sorted(expiry_fridays(CAL)))
EXPSET = set(EXPIRY)


def third_friday(y, m):
    first = pd.Timestamp(y, m, 1)
    return first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)


def nth_friday(y, m, n):
    first = pd.Timestamp(y, m, 1)
    return first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 7 * (n - 1))


def cash_on_or_before(d):
    if d in POS.index:
        return d
    c = CAL[CAL < d]
    return c.max() if len(c) else None


# ----------------------------------------------------------------------------------------------------------------
# 1-minute bars (ES, NQ): back-adjusted exactly like daily_sessions.py, RTH bars only kept
# ----------------------------------------------------------------------------------------------------------------
def load_1m(sym):
    df = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
    df.index = pd.to_datetime(df.ts_event, utc=True).dt.tz_convert(NY)
    df = df.drop(columns="ts_event")
    df = df[~df.index.duplicated()].sort_index()
    roll = df.instrument_id.ne(df.instrument_id.shift()) & df.instrument_id.shift().notna()
    jump = (df.Open - df.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    df["aC"] = df.Close + adj
    tmin = df.index.hour * 60 + df.index.minute
    rth = df[(tmin >= 570) & (tmin < 960)].copy()
    rth["tmin"] = (rth.index.hour * 60 + rth.index.minute).values
    rth["date"] = rth.index.tz_localize(None).normalize()
    rth = rth.reset_index(drop=True)

    def pick(lo, hi):
        sub = rth[(rth.tmin >= lo) & (rth.tmin <= hi)]
        return sub.groupby("date").tail(1).set_index("date")[["Close", "aC", "instrument_id", "tmin"]]

    out = {"p1459": pick(890, 899), "p1554": pick(945, 954), "p1259": pick(770, 779),
           "last": rth.groupby("date").tail(1).set_index("date")[["Close", "aC", "instrument_id", "tmin"]]}
    return out


M1 = {}
for s in ("ES", "NQ"):
    M1[s] = load_1m(s)
    lst = M1[s]["last"].reindex(CAL)
    dc = (lst.Close - S[s].close_raw).abs().max()
    da = (lst.aC - S[s].close_adj).abs().max()
    log(f"{s} 1m check: max |last RTH close - close_raw| = {dc:.6f}; max |adj diff| = {da:.6f}")
    for k in ("p1459", "p1554", "p1259"):
        x = M1[s][k].reindex(CAL)
        log(f"  {s} {k}: present {x.Close.notna().sum()}/{NC}; not exact minute: "
            f"{int((x.tmin.notna() & (x.tmin != {'p1459': 899, 'p1554': 954, 'p1259': 779}[k])).sum())}")


# ----------------------------------------------------------------------------------------------------------------
# Hourly loader
# ----------------------------------------------------------------------------------------------------------------
def load_1h(name):
    df = pd.read_csv(f"data/{name}_fut_1h.csv")
    df.index = pd.to_datetime(df.ts_event, utc=True).dt.tz_convert(NY)
    df = df.drop(columns="ts_event")
    df = df[~df.index.duplicated()].sort_index()
    df["date"] = df.index.tz_localize(None).normalize()
    df["hr"] = df.index.hour
    df["mi"] = df.index.minute
    return df


# ----------------------------------------------------------------------------------------------------------------
# Generic event summariser for trading tests
# ----------------------------------------------------------------------------------------------------------------
RESULTS = []


def finalize(ev, sym):
    """ev needs: date, pts (gross points), sides (contract-sides traded), entry_raw."""
    m = MULT[sym]
    ev = ev.copy()
    ev["gross_usd"] = ev.pts * m
    ev["net_usd"] = ev.gross_usd - ev.sides * side_cost(sym, 1)
    ev["net_usd2"] = ev.gross_usd - ev.sides * side_cost(sym, 2)
    ev["gross_bp"] = ev.pts / ev.entry_raw * 1e4
    ev["net_bp"] = ev.net_usd / m / ev.entry_raw * 1e4
    ev["net_bp2"] = ev.net_usd2 / m / ev.entry_raw * 1e4
    return ev


def trade_cell(cid, market, ev, post_start, notes, use_excess=False, extra=None):
    yrs = ev.date.dt.year.values
    by_year = ev.groupby(yrs).net_usd.sum()
    bp, bt = blocks(yrs, ev.net_usd)
    post = ev[ev.date >= pd.Timestamp(post_start)] if post_start else ev.iloc[0:0]
    cell = dict(id=cid, market=market, events=int(len(ev)),
                gross_bp_mean=fnum(ev.gross_bp.mean()), net_bp_mean=fnum(ev.net_bp.mean()),
                net_usd_mean=fnum(ev.net_usd.mean(), 3), net_usd_mean_2ticks=fnum(ev.net_usd2.mean(), 3),
                net_usd_total=fnum(ev.net_usd.sum(), 2),
                t_event=fnum(tstat(ev.excess_bp) if use_excess else tstat(ev.net_usd), 3),
                by_year_net_usd={str(k): round(float(v), 2) for k, v in by_year.items()},
                two_year_blocks_positive=f"{bp}/{bt}",
                post_paper_events=int(len(post)),
                post_paper_net_usd_mean=fnum(post.net_usd.mean(), 3) if len(post) else 0.0)
    if use_excess:
        cell["benchmark_excess_bp"] = fnum(ev.excess_bp.mean())
    cell["notes"] = notes
    if extra:
        cell.update(extra)
    RESULTS.append(cell)
    log(f"[{cid}] {market} n={cell['events']} gross_bp={cell['gross_bp_mean']} net_bp={cell['net_bp_mean']} "
        f"net$={cell['net_usd_mean']} (2tk {cell['net_usd_mean_2ticks']}) total={cell['net_usd_total']} "
        f"t={cell['t_event']} blocks={cell['two_year_blocks_positive']} post n={cell['post_paper_events']} "
        f"mean={cell['post_paper_net_usd_mean']}" + (f" excess_bp={cell['benchmark_excess_bp']}" if use_excess else ""))
    log("    by year:", cell["by_year_net_usd"])
    log("    notes:", notes)
    return cell


def desc_cell(cid, market, mult, ev_dates, ev_bp, ev_pts, cmp_bp, notes):
    """Descriptive cell: gross long-side move, no costs; t_event = two-sided Welch t vs comparison days."""
    ev_bp = np.asarray(ev_bp, float)
    ev_pts = np.asarray(ev_pts, float)
    cmp_bp = np.asarray(cmp_bp, float)
    yrs = pd.DatetimeIndex(ev_dates).year.values
    usd = ev_pts * mult
    by_year = pd.Series(usd).groupby(yrs).sum()
    bp, bt = blocks(yrs, usd)
    wt = welch(ev_bp, cmp_bp) if len(ev_bp) > 1 else float("nan")
    full_notes = (f"DESCRIPTIVE (no costs, no direction; *_usd fields = gross long-side move in $ per micro, "
                  f"net_bp = gross bp). event mean {ev_bp.mean():.3f} bp (sd {ev_bp.std(ddof=1):.2f}) vs "
                  f"comparison mean {cmp_bp.mean():.3f} bp (sd {cmp_bp.std(ddof=1):.2f}, n={len(cmp_bp)}); "
                  f"Welch t={wt:.2f} ({'NOTABLE |t|>=2' if abs(wt) >= 2 else 'not notable'}); one-sample t of "
                  f"event bp vs 0 = {tstat(ev_bp):.2f}. " + notes)
    cell = dict(id=cid, market=market, events=int(len(ev_bp)), gross_bp_mean=fnum(ev_bp.mean()),
                net_bp_mean=fnum(ev_bp.mean()), net_usd_mean=fnum(usd.mean(), 3), net_usd_total=fnum(usd.sum(), 2),
                t_event=fnum(wt, 3), benchmark_excess_bp=fnum(ev_bp.mean() - cmp_bp.mean()),
                by_year_net_usd={str(k): round(float(v), 2) for k, v in by_year.items()},
                two_year_blocks_positive=f"{bp}/{bt}", post_paper_events=0, post_paper_net_usd_mean=0.0,
                notes=full_notes)
    RESULTS.append(cell)
    log(f"[{cid}] {market} n={len(ev_bp)} mean_bp={ev_bp.mean():.3f} cmp_bp={cmp_bp.mean():.3f} (n={len(cmp_bp)}) "
        f"welch_t={wt:.2f} blocks={bp}/{bt}")
    return cell


# ================================================================================================================
# TEST 5: Graziani TSR -- end-of-month reversal held one month
# ================================================================================================================
log("\n===== TEST 5 =====")
rows = []
for k in range(len(TS) - 1):
    Tm, Tn = TS[k], TS[k + 1]
    f4 = cash_on_or_before(nth_friday(Tm.year, Tm.month, 4))
    es = S["ES"]
    r_w4 = (es.close_adj[Tm] - es.close_adj[f4]) / es.close_raw[f4]
    pts = es.close_adj[Tn] - es.close_adj[Tm]
    nr = n_rolls("ES", Tm, Tn)
    rows.append(dict(sig_month=Tm, date=Tn, f4=f4, r_w4=r_w4, pts_long=pts, rolls=nr, entry_raw=es.close_raw[Tm]))
t5 = pd.DataFrame(rows)
t5["dir"] = np.where(t5.r_w4 < 0, 1, np.where(t5.r_w4 > 0, -1, 0))
n_months = len(t5)
log(f"holding months {n_months} ({t5.date.min().date()}..{t5.date.max().date()}); r_w4==0 months: "
    f"{int((t5.dir == 0).sum())} {t5[t5.dir == 0].sig_month.dt.strftime('%Y-%m').tolist()}; months with roll: "
    f"{int((t5.rolls > 0).sum())}")
bh = finalize(t5.assign(pts=t5.pts_long, sides=2 * (1 + t5.rolls)), "ES")
bh_mean = bh.net_usd.mean()
bh_post = bh[bh.date >= "2020-01-01"].net_usd.mean()
for cid, mask, label in (("5-primary", t5.dir != 0, "long if r_w4<0, short if r_w4>0"),
                         ("5a", t5.dir == 1, "long-only (r_w4<0 months)")):
    ev = t5[mask].copy()
    ev["pts"] = ev.dir * ev.pts_long
    ev["sides"] = 2 * (1 + ev.rolls)
    ev = finalize(ev, "ES")
    per_month = ev.net_usd.sum() / n_months
    post = ev[ev.date >= "2020-01-01"]
    n_post_months = int((t5.date >= "2020-01-01").sum())
    per_month_post = post.net_usd.sum() / n_post_months
    base_ok = (ev.net_usd.mean() > 0) and (tstat(ev.net_usd) >= 2) and (post.net_usd.mean() > 0)
    passed = base_ok and (per_month > bh_mean)
    passed_held = base_ok and (ev.net_usd.mean() > bh_mean)
    notes = (f"PASS reading A (strategy $ per CALENDAR month vs B&H $ per month) = {'YES' if passed else 'NO'}; "
             f"reading B (strategy $ per month HELD vs B&H $ per month) = {'YES' if passed_held else 'NO'}. "
             f"Timing check (long B&H net $ by signal): r_w4<0 months {bh[t5.dir == 1].net_usd.mean():.2f} "
             f"(n={int((t5.dir == 1).sum())}) vs r_w4>0 months {bh[t5.dir == -1].net_usd.mean():.2f} "
             f"(n={int((t5.dir == -1).sum())}), Welch t={welch(bh[t5.dir == 1].net_usd, bh[t5.dir == -1].net_usd):.2f}; "
             f"r_w4=0 months {bh[t5.dir == 0].net_usd.mean():.2f} (n={int((t5.dir == 0).sum())}). "
             f"{label}; each month = 1 trade close T(m)->close T(m+1), 1 RT $3.50 + 1 extra RT per roll inside the "
             f"month. Per CALENDAR month (flat months = 0): strategy {per_month:.2f} $/month vs buy-and-hold "
             f"{bh_mean:.2f} $/month (B&H = long every month, same cost rule; B&H gross {bh.gross_usd.mean():.2f}, "
             f"t={tstat(bh.net_usd):.2f}). 2020-2026: strategy {per_month_post:.2f} $/month (per event "
             f"{post.net_usd.mean():.2f}, n={len(post)}, t={tstat(post.net_usd):.2f}) vs B&H {bh_post:.2f} $/month. "
             f"Long months n={int((ev.dir == 1).sum())} mean {ev[ev.dir == 1].net_usd.mean():.2f}; short months "
             f"n={int((ev.dir == -1).sum())} mean {ev[ev.dir == -1].net_usd.mean() if (ev.dir == -1).any() else float('nan'):.2f}. "
             f"16 months have r_w4 = 0 exactly (4th Friday is T itself) and are flat. PASS rule: net mean>0 & t>=2, "
             f"post-2019 mean>0, beats B&H per month.")
    trade_cell(cid, "MES", ev, "2020-01-01", notes)
    ev.to_csv(f"{OUTDIR}/t5_{cid}.csv", index=False)

# ================================================================================================================
# TEST 6: Turn-of-month [-1,+3]
# ================================================================================================================
log("\n===== TEST 6 =====")
TPOS = POS[TS].values
event_held6 = set()
for i in TPOS:
    event_held6.update(range(i, i + 4))  # sessions T..T+3 held by the event
for sym in ("ES", "NQ"):
    x = S[sym]
    ca, cr = x.close_adj.values, x.close_raw.values
    # benchmark: all 4-session windows close j -> close j+4 whose held sessions j+1..j+4 avoid every event's T..T+3
    bw = []
    for j in range(NC - 4):
        if CAL[j] > LAST_ENTRY:
            break
        if any((j + q) in event_held6 for q in range(1, 5)):
            continue
        bw.append((CAL[j].year, (ca[j + 4] - ca[j]) / cr[j] * 1e4))
    bw = pd.DataFrame(bw, columns=["year", "bp"])
    bench = bw.groupby("year").bp.mean()
    rows = []
    for T, i in zip(TS, TPOS):
        if i - 1 < 0 or i + 3 >= NC:
            continue
        a, b = CAL[i - 1], CAL[i + 3]
        nr = n_rolls(sym, a, b)
        rows.append(dict(date=a, T=T, pts=ca[i + 3] - ca[i - 1], sides=2 * (1 + nr), rolls=nr, entry_raw=cr[i - 1]))
    ev = finalize(pd.DataFrame(rows), sym)
    ev["bench_bp"] = ev.date.dt.year.map(bench)
    ev["excess_bp"] = ev.net_bp - ev.bench_bp
    ev["gross_excess_bp"] = ev.gross_bp - ev.bench_bp
    yrs = ev.date.dt.year.values
    xb_p, xb_t = blocks(yrs, ev.excess_bp)
    nb_p, nb_t = blocks(yrs, ev.net_usd)
    passed = ev.excess_bp.mean() > 0 and tstat(ev.excess_bp) >= 2 and nb_p >= 2 / 3 * nb_t
    notes = (f"Long close T-1 -> close T+3; rolls inside windows: {int(ev.rolls.sum())}. Benchmark = mean of "
             f"{len(bw)} 4-session windows (by start-year) whose held sessions avoid T..T+3 of every month; benchmark "
             f"mean {ev.bench_bp.mean():.2f} bp/window. t_event = t of per-event NET excess bp (net bp - same-year "
             f"gross benchmark). Gross excess {ev.gross_excess_bp.mean():.2f} bp (t={tstat(ev.gross_excess_bp):.2f}). "
             f"t of net $ = {tstat(ev.net_usd):.2f}. Blocks positive on net $ = {nb_p}/{nb_t}; on net excess = "
             f"{xb_p}/{xb_t}. PASS={'YES' if passed else 'NO'}.")
    trade_cell(f"6-{MICRO[sym]}", MICRO[sym], ev, "2006-01-01", notes, use_excess=True)
    ev.to_csv(f"{OUTDIR}/t6_{sym}.csv", index=False)

# ================================================================================================================
# TEST 7: VIX-settlement Wednesday (descriptive)
# ================================================================================================================
log("\n===== TEST 7 =====")
W = []
for y in range(2010, 2027):
    for m in range(1, 13):
        if (y, m) < (2010, 6) or (y, m) > (2026, 10):
            continue
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        F = third_friday(ny, nm)
        if F <= CAL[-1]:
            F = cash_on_or_before(F)
        w = F - pd.Timedelta(days=30)
        w = cash_on_or_before(w)
        W.append(w)
W = pd.DatetimeIndex(W)
assert W.is_unique
log("W days:", len(W), "non-Wednesday:", [d.strftime("%Y-%m-%d %a") for d in W if d.weekday() != 2])
WSET = set(W)
for sym in ("ES", "NQ"):
    x = S[sym]
    on_bp = pd.Series(np.nan, index=CAL)
    on_pts = pd.Series(np.nan, index=CAL)
    prev = CAL[:-1]
    on_pts.iloc[1:] = x.open_adj.values[1:] - x.close_adj.values[:-1]
    on_bp.iloc[1:] = on_pts.values[1:] / x.close_raw.values[:-1] * 1e4
    id_pts = x.close_adj - x.open_adj
    id_bp = id_pts / x.open_raw * 1e4
    prev_day = pd.Series(np.r_[pd.NaT, CAL[:-1]], index=CAL)
    on_ok = (prev_day <= LAST_ENTRY) & on_bp.notna()
    id_ok = CAL <= LAST_ENTRY
    isW = CAL.isin(W)
    wdates = CAL[isW & on_ok.values]
    desc_cell(f"7-{sym}-overnight", sym, MULT[sym], wdates, on_bp[wdates], on_pts[wdates],
              on_bp[(~isW) & on_ok.values].values,
              "Overnight = close of cash_day before W -> 09:30 open of W (adj points / raw prior close). Comparison = "
              "all other cash_day overnights.")
    wdates2 = CAL[isW & id_ok]
    desc_cell(f"7-{sym}-intraday", sym, MULT[sym], wdates2, id_bp[wdates2], id_pts[wdates2],
              id_bp[(~isW) & id_ok].values,
              "Intraday = 09:30 open of W -> close of W (15:59 bar; 13:14 bar on early closes). Comparison = all "
              "other cash_day sessions.")

# ================================================================================================================
# TEST 8: Overnight long into quarterly expiry only
# ================================================================================================================
log("\n===== TEST 8 =====")
QMONTHS = (3, 6, 9, 12)
for sym in ("ES", "NQ"):
    x = S[sym]
    last_inst = M1[sym]["last"].instrument_id.reindex(CAL)
    # benchmark: all other cash-day overnights (close of previous cash day -> 09:30 open), excluding pre-expiry nights
    on_bp = (x.open_adj.values[1:] - x.close_adj.values[:-1]) / x.close_raw.values[:-1] * 1e4
    nights = pd.DataFrame({"s": CAL[1:], "p": CAL[:-1], "bp": on_bp})
    nights = nights[(nights.p <= LAST_ENTRY) & (~nights.s.isin(EXPIRY))]
    bench = nights.bp.mean()
    rows, skipped = [], []
    for E in EXPIRY:
        i = POS[E]
        if i == 0:
            continue
        p = CAL[i - 1]
        if p > LAST_ENTRY:
            continue
        if last_inst[p] != x.inst[E]:
            skipped.append(E.strftime("%Y-%m-%d"))
            continue
        rows.append(dict(date=E, quarterly=E.month in QMONTHS, pts=x.open_raw[E] - x.close_raw[p], sides=2,
                         entry_raw=x.close_raw[p]))
    allev = finalize(pd.DataFrame(rows), sym)
    allev["excess_bp"] = allev.net_bp - bench
    allev["gross_excess_bp"] = allev.gross_bp - bench
    log(f"{sym}: expiry events {len(allev)} (skipped for instrument change: {skipped}); benchmark overnights "
        f"n={len(nights)} mean {bench:.3f} bp")
    for cid, sel, lab in ((f"8-{MICRO[sym]}-quarterly", allev.quarterly, "Mar/Jun/Sep/Dec expiries"),
                          (f"8a-{MICRO[sym]}-offquarterly", ~allev.quarterly, "other 8 months (comparison)")):
        ev = allev[sel].copy()
        passed = ev.gross_excess_bp.mean() > 0 and tstat(ev.gross_excess_bp) >= 2 and ev.net_usd2.mean() > 0
        notes = (f"{lab}: long close of cash_day before E -> 09:30 open of E (raw prices, same instrument). Benchmark "
                 f"= all other cash-day overnights excl. all pre-expiry nights, mean {bench:.3f} bp (n={len(nights)}). "
                 f"GROSS excess {ev.gross_excess_bp.mean():.3f} bp, t={tstat(ev.gross_excess_bp):.2f}; NET excess "
                 f"{ev.excess_bp.mean():.3f} bp (t_event field = t of net excess); Welch t of gross bp vs benchmark "
                 f"nights = {welch(ev.gross_bp, nights.bp):.2f}. Net $ t={tstat(ev.net_usd):.2f}; 2-tick net mean "
                 f"{ev.net_usd2.mean():.2f}. PASS={'YES' if passed else 'NO'} (gross excess t>=2 and 2-tick net>0).")
        trade_cell(cid, MICRO[sym], ev, "2022-01-01", notes, use_excess=True)
    allev.to_csv(f"{OUTDIR}/t8_{sym}.csv", index=False)

# ================================================================================================================
# TEST 9: Quarterly-expiry Friday rebalance close (descriptive)
# ================================================================================================================
log("\n===== TEST 9 =====")
Q = pd.DatetimeIndex([e for e in EXPIRY if e.month in QMONTHS and e <= LAST_ENTRY])
log("Q days:", len(Q), "non-Friday:", [d.strftime("%Y-%m-%d %a") for d in Q if d.weekday() != 4])
FRI_CMP = pd.DatetimeIndex([d for d in CAL if d.weekday() == 4 and d not in EXPSET and d <= LAST_ENTRY])
for sym in ("ES", "NQ"):
    x = S[sym]
    p14 = M1[sym]["p1459"].reindex(CAL)
    lst = M1[sym]["last"].reindex(CAL)
    ok1 = (~x.early_close.astype(bool)) & p14.Close.notna() & (p14.instrument_id == lst.instrument_id)
    lh_pts = (x.close_raw - p14.Close).where(ok1)
    lh_bp = lh_pts / p14.Close * 1e4
    nxt_open_adj = pd.Series(np.r_[x.open_adj.values[1:], np.nan], index=CAL)
    co_pts = nxt_open_adj - x.close_adj
    co_bp = co_pts / x.close_raw * 1e4
    for sub, qd in (("", Q), ("-Dec", Q[Q.month == 12])):
        q1 = qd[lh_bp[qd].notna().values]
        c1 = FRI_CMP[lh_bp[FRI_CMP].notna().values]
        desc_cell(f"9-{sym}-lasthour{sub}", sym, MULT[sym], q1, lh_bp[q1], lh_pts[q1], lh_bp[c1].values,
                  f"{'December only. ' if sub else ''}Last hour = close of 14:59 1-min bar -> 16:00 close (15:59 "
                  f"bar), same instrument; early-close days excluded (no 15:00-16:00 hour). Comparison = cash-day "
                  f"Fridays that are not expiry days (n={len(c1)}).")
        q2 = qd[co_bp[qd].notna().values]
        c2 = FRI_CMP[co_bp[FRI_CMP].notna().values]
        desc_cell(f"9-{sym}-closeToNextOpen{sub}", sym, MULT[sym], q2, co_bp[q2], co_pts[q2], co_bp[c2].values,
                  f"{'December only. ' if sub else ''}Close of Q -> 09:30 open of next cash_day (adj points / raw "
                  f"close). Comparison = non-expiry cash-day Fridays.")

# ================================================================================================================
# TEST 10: Russell reconstitution day (descriptive)
# ================================================================================================================
log("\n===== TEST 10 =====")
R = pd.DatetimeIndex([cash_on_or_before(nth_friday(y, 6, 4)) for y in range(2017, 2027)])
log("R days:", [d.strftime("%Y-%m-%d") for d in R])
for name in ("RTY", "ES"):
    h = load_1h(name)
    top = h[h.mi == 0]

    def hour_tab(hr):
        t = top[top.hr == hr].groupby("date").tail(1).set_index("date")
        return t[["Close", "instrument_id"]]

    c14, c15, c09 = hour_tab(14).reindex(CAL), hour_tab(15).reindex(CAL), hour_tab(9).reindex(CAL)
    if name == "ES":
        dd = (c15.Close - S["ES"].close_raw).dropna()
        log(f"ES hourly 15:00-bar close vs close_raw: max abs diff {dd.abs().max():.4f} over {len(dd)} days")
    first = h.date.min()
    start = max(first + pd.Timedelta(days=1), pd.Timestamp("2017-01-01"))
    ok1 = c14.Close.notna() & c15.Close.notna() & (c14.instrument_id == c15.instrument_id)
    lh_pts = (c15.Close - c14.Close).where(ok1)
    lh_bp = lh_pts / c14.Close * 1e4
    n09 = pd.DataFrame({"Close": np.r_[c09.Close.values[1:], np.nan],
                        "inst": np.r_[c09.instrument_id.values[1:], np.nan]}, index=CAL)
    ok2 = c15.Close.notna() & n09.Close.notna() & (c15.instrument_id == n09.inst)
    on_pts = (n09.Close - c15.Close).where(ok2)
    on_bp = on_pts / c15.Close * 1e4
    fr = pd.DatetimeIndex([d for d in CAL if d.weekday() == 4 and d >= start and d <= LAST_ENTRY and d not in set(R)])
    r1 = R[lh_bp[R].notna().values]
    c1 = fr[lh_bp[fr].notna().values]
    desc_cell(f"10-{name}-lasthour", name, {"RTY": 5.0, "ES": 5.0}[name], r1, lh_bp[r1], lh_pts[r1], lh_bp[c1].values,
              f"Events {[d.year for d in r1]}. Last hour = close of 14:00 ET hourly bar -> close of 15:00 ET bar "
              f"(hourly file), same instrument. Comparison = all other cash-day Fridays from {start.date()} with "
              f"both bars (n={len(c1)}). $ uses $5/pt (M2K and MES both $5/pt). Anecdotal sample.")
    r2 = R[on_bp[R].notna().values]
    c2 = fr[on_bp[fr].notna().values]
    r1x, r2x = r1[r1.year >= 2018], r2[r2.year >= 2018]
    desc_cell(f"10-{name}-closeTo10am", name, 5.0, r2, on_bp[r2], on_pts[r2], on_bp[c2].values,
              f"Events {[d.year for d in r2]}. 16:00 price of R (close of 15:00 ET bar) -> next cash_day 10:00 "
              f"(close of 09:00 ET bar), same instrument required. Comparison = all other cash-day Fridays from "
              f"{start.date()} (n={len(c2)}). Anecdotal sample. Event bp by year: "
              f"{ {d.year: round(float(on_bp[d]), 1) for d in r2} }; last-hour bp by year: "
              f"{ {d.year: round(float(lh_bp[d]), 1) for d in r1} }. 2018+ only: last hour {lh_bp[r1x].mean():.2f} bp, "
              f"close->10am {on_bp[r2x].mean():.2f} bp.")

# ================================================================================================================
# TEST 11: Quarter-end window dressing
# ================================================================================================================
log("\n===== TEST 11 =====")
x = S["ES"]
rows = []
for T in TS:
    i = POS[T]
    if i - 3 < 0:
        continue
    a = CAL[i - 3]
    nr = n_rolls("ES", a, T)
    rows.append(dict(date=T, entry=a, quarter=T.month in QMONTHS, pts=x.close_adj[T] - x.close_adj[a],
                     sides=2 * (1 + nr), rolls=nr, entry_raw=x.close_raw[a]))
t11 = finalize(pd.DataFrame(rows), "ES")
bench11 = t11[~t11.quarter].groupby(t11[~t11.quarter].date.dt.year).gross_bp.mean()
qev = t11[t11.quarter].copy()
qev["bench_bp"] = qev.date.dt.year.map(bench11)
qev["excess_bp"] = qev.net_bp - qev.bench_bp
qev["gross_excess_bp"] = qev.gross_bp - qev.bench_bp
passed = qev.excess_bp.mean() > 0 and tstat(qev.excess_bp) >= 2
trade_cell("11-MES-quarterend", "MES", qev, "1999-01-01",
           f"Long close T-3 -> close T in Mar/Jun/Sep/Dec; rolls inside windows {int(qev.rolls.sum())}. Benchmark = "
           f"same-year mean GROSS bp of the same window in non-quarter-end months (mean {qev.bench_bp.mean():.2f}). "
           f"t_event = t of net excess. Gross excess {qev.gross_excess_bp.mean():.2f} bp (t="
           f"{tstat(qev.gross_excess_bp):.2f}); net $ t={tstat(qev.net_usd):.2f}. Blocks on net excess "
           f"{'%d/%d' % blocks(qev.date.dt.year.values, qev.excess_bp)}. PASS={'YES' if passed else 'NO'}.",
           use_excess=True)
nq = t11[~t11.quarter].copy()
trade_cell("11a-MES-nonquarter", "MES", nq, "1999-01-01",
           f"Same T-3 -> T long window in the 8 non-quarter-end months (comparison, no benchmark). Net $ t shown.")
t11.to_csv(f"{OUTDIR}/t11.csv", index=False)

# ================================================================================================================
# TEST 12: Threshold-rebalancing signal
# ================================================================================================================
log("\n===== TEST 12 =====")
z = load_1h("ZN")
zroll = z.instrument_id.ne(z.instrument_id.shift()) & z.instrument_id.shift().notna()
zjump = (z.Open - z.Close.shift()).where(zroll, 0.0)
z["aC"] = z.Close + zjump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
# ZN "16:00 price" of day t = close of the last hourly bar opening at or before 15:00 ET on day t (normally the
# 15:00 bar itself; early-close days / data gaps fall back to the latest earlier bar)
zt = z.reset_index().rename(columns={"index": "ts"})
zt = zt.rename(columns={zt.columns[0]: "ts"})
tgt = pd.DataFrame({"tgt": (CAL + pd.Timedelta(hours=15)).tz_localize(NY), "day": CAL})
zd = pd.merge_asof(tgt.sort_values("tgt"), zt[["ts", "Close", "aC", "instrument_id", "hr", "date"]].sort_values("ts"),
                   left_on="tgt", right_on="ts", direction="backward").set_index("day")
not15 = zd[(zd.date != zd.index) | (zd.hr != 15)]
log(f"ZN daily 16:00 price: {int(zd.Close.notna().sum())}/{NC} days; days NOT using the 15:00 bar of that day: "
    f"{len(not15)} {[(d.strftime('%Y-%m-%d'), str(r.ts)[:16]) for d, r in not15.iterrows()]}")
assert zd.Close.notna().all()
es = S["ES"]
rES = pd.Series(np.r_[np.nan, (es.close_adj.values[1:] - es.close_adj.values[:-1]) / es.close_raw.values[:-1]],
                index=CAL)
rZN = pd.Series(np.r_[np.nan, (zd.aC.values[1:] - zd.aC.values[:-1]) / zd.Close.values[:-1]], index=CAL)
nq = S["NQ"]
rNQ = pd.Series(np.r_[np.nan, (nq.close_adj.values[1:] - nq.close_adj.values[:-1]) / nq.close_raw.values[:-1]],
                index=CAL)
deltas = np.round(np.arange(26) * 0.001, 4)
w = np.full(26, 0.60)
sig = np.full(NC, np.nan)
for k in range(1, NC):
    a = w * (1 + rES.iloc[k])
    b = (1 - w) * (1 + rZN.iloc[k])
    wpre = a / (a + b)
    dev = wpre - 0.60
    sig[k] = dev.mean()
    w = np.where(np.abs(dev) >= deltas - 1e-12, 0.60, wpre)
sig = pd.Series(sig, index=CAL)
log(f"signal: mean {sig.mean():.5f} sd {sig.std():.5f}; |signal|>=0.5% on {(sig.abs() >= 0.005).mean() * 100:.1f}% of days")


def nw_ols(y, xv, lags=5):
    X = np.column_stack([np.ones(len(xv)), xv])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    u = X * e[:, None]
    Sm = u.T @ u
    for L in range(1, lags + 1):
        wl = 1 - L / (lags + 1)
        G = u[L:].T @ u[:-L]
        Sm += wl * (G + G.T)
    V = XtX_inv @ Sm @ XtX_inv
    se = np.sqrt(np.diag(V))
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return beta, se, r2


idx = np.arange(1, NC - 1)
idx = idx[CAL[idx] <= LAST_ENTRY]
for cid, rr, mk in (("12-forecast-ES", rES, "ES"), ("12a-forecast-NQ", rNQ, "NQ")):
    yv = rr.values[idx + 1]
    xv = sig.values[idx]
    beta, se, r2 = nw_ols(yv, xv)
    tsl = beta[1] / se[1]
    post = CAL[idx] >= pd.Timestamp("2023-04-01")
    bpst, sepst, _ = nw_ols(yv[post], xv[post])
    yrs = CAL[idx].year.values
    bpos = 0
    btot = 0
    for blk in sorted(set((yrs - 2010) // 2)):
        mm = (yrs - 2010) // 2 == blk
        bb, _, _ = nw_ols(yv[mm], xv[mm])
        btot += 1
        bpos += int(bb[1] < 0)
    cell = dict(id=cid, market=mk, events=int(len(idx)), gross_bp_mean=0.0, net_bp_mean=0.0, net_usd_mean=0.0,
                net_usd_total=0.0, t_event=fnum(tsl, 3), by_year_net_usd={},
                two_year_blocks_positive=f"{bpos}/{btot}", post_paper_events=int(post.sum()),
                post_paper_net_usd_mean=0.0,
                notes=(f"FORECAST REGRESSION (no P&L; $ fields set to 0). r_{mk}(t->t+1) = a + b*signal_t, OLS, "
                       f"Newey-West 5 lags (Bartlett, no small-sample correction). slope b = {beta[1]:.5f} (return "
                       f"per unit of weight deviation; i.e. {beta[1] * 0.01 * 1e4:.2f} bp of next-day return per 1 "
                       f"pp of signal), NW se {se[1]:.5f}, t = {tsl:.2f}, intercept {beta[0] * 1e4:.2f} bp, R2 "
                       f"{r2:.5f}, n={len(idx)} days {CAL[idx[0]].date()}..{CAL[idx[-1]].date()}. Post-Mar-2023 "
                       f"slope {bpst[1]:.5f} t={bpst[1] / sepst[1]:.2f} (n={int(post.sum())}). 2-year-block field "
                       f"counts blocks with NEGATIVE slope (the predicted sign). "
                       f"{'SUPPORT (slope<0, |t|>=2)' if (beta[1] < 0 and abs(tsl) >= 2) else 'no support'}."))
    RESULTS.append(cell)
    log(f"[{cid}] slope {beta[1]:.5f} NW t {tsl:.2f} R2 {r2:.5f} n {len(idx)}; post slope {bpst[1]:.5f} "
        f"t {bpst[1] / sepst[1]:.2f}; negative-slope blocks {bpos}/{btot}")

# tradable rule
posn = pd.Series(0, index=CAL, dtype=int)
sel = sig.abs() >= 0.005
posn[sel] = -np.sign(sig[sel]).astype(int)
posn[CAL > LAST_ENTRY] = 0
posn.iloc[0] = 0
pv = posn.values
rows = []
for k in idx:
    if pv[k] == 0:
        continue
    prev = pv[k - 1]
    nxt = pv[k + 1] if (k + 1 < NC and CAL[k + 1] <= LAST_ENTRY) else 0
    sides = abs(pv[k] - prev) + (abs(pv[k]) if nxt == 0 else 0)
    nr = n_rolls("ES", CAL[k], CAL[k + 1])
    sides += 2 * nr
    rows.append(dict(date=CAL[k], pos=pv[k], pts=pv[k] * (es.close_adj.values[k + 1] - es.close_adj.values[k]),
                     sides=sides, rolls=nr, entry_raw=es.close_raw.values[k]))
t12 = finalize(pd.DataFrame(rows), "ES")
yrs12 = t12.date.dt.year.values
bp12, bt12 = blocks(yrs12, t12.net_usd)
passed = t12.net_usd.mean() > 0 and tstat(t12.net_usd) >= 2 and bp12 >= 2 / 3 * bt12
n_changes = int(np.abs(np.diff(np.r_[0, pv[idx], 0])).sum())
trade_cell("12-tradable-MES", "MES", t12, "2023-04-01",
           f"Hold 1 MES close t -> close t+1 in direction -sign(signal_t) when |signal_t| >= 0.5%. Days in position "
           f"{len(t12)} of {len(idx)} (long {int((t12.pos > 0).sum())}, short {int((t12.pos < 0).sum())}); events = "
           f"days in position; costs: $1.75 per contract-side on every position change (entry, exit, flip = 2 "
           f"sides) attributed to the day entering the new position (exit-to-flat side attributed to the last day "
           f"held) + 1 RT per contract roll while in position (rolls {int(t12.rolls.sum())}); total sides "
           f"{int(t12.sides.sum())}. Gross $/day {t12.gross_usd.mean():.2f} (t={tstat(t12.gross_usd):.2f}). "
           f"PASS={'YES' if passed else 'NO'} (net/day>0, day-level t>=2, 2/3 blocks).")
t12.to_csv(f"{OUTDIR}/t12_days.csv", index=False)
pd.DataFrame({"rES": rES, "rZN": rZN, "signal": sig, "pos": posn}).to_csv(f"{OUTDIR}/t12_signal.csv")

# ================================================================================================================
# TEST 13: Stock-only month-end fade (Cal_t = sign of ES month-to-date return at 15:55)
# ================================================================================================================
log("\n===== TEST 13 =====")
p1554 = M1["ES"]["p1554"].reindex(CAL)
p1259 = M1["ES"]["p1259"].reindex(CAL)
ec = es.early_close.astype(bool)
sig_adj = pd.Series(np.where(ec, p1259.aC, p1554.aC), index=CAL)
assert sig_adj.notna().all()
rows = []
for k in range(1, len(TS)):
    T, Tp = TS[k], TS[k - 1]
    i = POS[T]
    if i + 1 >= NC:
        continue
    days = [CAL[i + q] for q in range(-4, 1)]
    base = es.close_adj[Tp]
    cal = [np.sign(sig_adj[d] - base) for d in days]
    pos_ = [-int(c) for c in cal]
    seq = days + [CAL[i + 1]]
    pts = sum(pos_[q] * (es.close_adj[seq[q + 1]] - es.close_adj[seq[q]]) for q in range(5))
    sides = abs(pos_[0]) + sum(abs(pos_[q] - pos_[q - 1]) for q in range(1, 5)) + abs(pos_[4])
    nr = sum(n_rolls("ES", seq[q], seq[q + 1]) for q in range(5) if pos_[q] != 0)
    rows.append(dict(date=T, pts=pts, sides=sides + 2 * nr, rolls=nr, entry_raw=es.close_raw[days[0]],
                     positions="".join({1: "+", -1: "-", 0: "0"}[p] for p in pos_),
                     flips=sum(1 for q in range(1, 5) if pos_[q] * pos_[q - 1] < 0)))
t13 = finalize(pd.DataFrame(rows), "ES")
yrs13 = t13.date.dt.year.values
bp13, bt13 = blocks(yrs13, t13.net_usd)
post13 = t13[t13.date >= "2023-04-01"]
passed = t13.net_usd.mean() > 0 and tstat(t13.net_usd) >= 2 and post13.net_usd.mean() > 0 and bp13 >= 2 / 3 * bt13
trade_cell("13-MES", "MES", t13, "2023-04-01",
           f"Positions -sign(ES MTD return since close of T_prev, using the 15:55 price (15:54-bar close; 12:59-bar "
           f"close on early-close days) for day t), held close t -> close t+1 for t=T-4..T, exit close T+1. "
           f"Patterns: {t13.positions.value_counts().head(6).to_dict()}; months with >=1 flip "
           f"{int((t13.flips > 0).sum())}; mean contract-sides/month {t13.sides.mean():.2f}. Gross $/month "
           f"{t13.gross_usd.mean():.2f}. PASS={'YES' if passed else 'NO'}.")
t13.to_csv(f"{OUTDIR}/t13.csv", index=False)

# ================================================================================================================
# TEST 14: Dash-for-cash entry-day scan (L-1, L, L+1)
# ================================================================================================================
log("\n===== TEST 14 =====")
REG = [(4, pd.Timestamp("1900-01-01"), pd.Timestamp("2017-09-04"), "T+3 (L=T-4)"),
       (3, pd.Timestamp("2017-09-05"), pd.Timestamp("2024-05-27"), "T+2 (L=T-3)"),
       (2, pd.Timestamp("2024-05-28"), pd.Timestamp("2100-01-01"), "T+1 (L=T-2)")]
excl = set()
for i in TPOS:
    excl.update(range(i - 8, i + 4))
ca, cr = es.close_adj.values, es.close_raw.values
bench_cache = {}


def bench14(year, n):
    key = (year, n)
    if key not in bench_cache:
        vals = [(ca[j + n] - ca[j]) / cr[j] * 1e4 for j in range(NC - n)
                if CAL[j].year == year and CAL[j] <= LAST_ENTRY and j not in excl]
        bench_cache[key] = (float(np.mean(vals)), len(vals))
    return bench_cache[key]


rows = []
for T, i in zip(TS, TPOS):
    m = [(k, lab) for (k, lo, hi, lab) in REG if i - k >= 0 and lo <= CAL[i - k] <= hi]
    assert len(m) == 1, (T, m)
    k, lab = m[0]
    for shift, name in ((-1, "L-1"), (0, "L"), (1, "L+1")):
        e = i - k + shift
        if e >= i - 1 or e < 0:
            continue
        n = (i - 1) - e
        bmean, bn = bench14(CAL[e].year, n)
        nr = n_rolls("ES", CAL[e], CAL[i - 1])
        rows.append(dict(scan=name, date=CAL[e], T=T, regime=lab, hold=n, pts=ca[i - 1] - ca[e], sides=2 * (1 + nr),
                         rolls=nr, entry_raw=cr[e], bench_bp=bmean, bench_n=bn))
t14 = finalize(pd.DataFrame(rows), "ES")
t14["excess_bp"] = t14.net_bp - t14.bench_bp
t14["gross_excess_bp"] = t14.gross_bp - t14.bench_bp
scan_summary = {}
for name in ("L-1", "L", "L+1"):
    ev = t14[t14.scan == name].copy()
    reg_txt = "; ".join(
        f"{lab}: n={len(g)} net$ {g.net_usd.mean():.2f} net excess {g.excess_bp.mean():.2f}bp t={tstat(g.excess_bp):.2f}"
        for lab, g in ev.groupby("regime", sort=False))
    scan_summary[name] = (ev.excess_bp.mean(), tstat(ev.excess_bp))
    trade_cell(f"14-{name}", "MES", ev, "2014-01-01",
               f"Entry {name} (L = T-4 / T-3 / T-2 by settlement regime of L's date), long to close of T-1; "
               f"L+1 skipped when it is T-1 or later (all T+1-regime months). Benchmark = same-year mean gross bp of "
               f"all same-length windows starting outside T-8..T+3 (mean {ev.bench_bp.mean():.2f}). t_event = t of "
               f"net excess. Gross excess {ev.gross_excess_bp.mean():.2f}bp (t={tstat(ev.gross_excess_bp):.2f}). "
               f"Net $ t={tstat(ev.net_usd):.2f}. By regime: {reg_txt}. Blocks on net excess "
               f"{'%d/%d' % blocks(ev.date.dt.year.values, ev.excess_bp)}.", use_excess=True)
peak = max(scan_summary, key=lambda q: scan_summary[q][0])
common = t14[t14.regime != REG[2][3]]
cs = {q: (common[common.scan == q].excess_bp.mean(), tstat(common[common.scan == q].excess_bp)) for q in ("L-1", "L", "L+1")}
peak_c = max(cs, key=lambda q: cs[q][0])
log(f"TEST 14 scan: net excess by entry {[(q, round(v[0], 2), round(v[1], 2)) for q, v in scan_summary.items()]}; "
    f"peak = {peak}; like-for-like (T+3/T+2 regimes only, n={int((common.scan == 'L').sum())}): "
    f"{[(q, round(v[0], 2), round(v[1], 2)) for q, v in cs.items()]} peak = {peak_c}")
for c in RESULTS:
    if c["id"].startswith("14-"):
        c["notes"] += (f" SCAN: mean net excess L-1 {scan_summary['L-1'][0]:.2f} / L {scan_summary['L'][0]:.2f} / "
                       f"L+1 {scan_summary['L+1'][0]:.2f} bp; peak at {peak} ({'L IS' if peak == 'L' else 'L is NOT'} "
                       f"the peak). Like-for-like on the T+3/T+2-regime months where all three exist "
                       f"(n={int((common.scan == 'L').sum())}): L-1 {cs['L-1'][0]:.2f} (t={cs['L-1'][1]:.2f}) / L "
                       f"{cs['L'][0]:.2f} (t={cs['L'][1]:.2f}) / L+1 {cs['L+1'][0]:.2f} (t={cs['L+1'][1]:.2f}) bp; "
                       f"peak at {peak_c}. Note the shorter holds (L+1) are compared with shorter-window benchmarks.")
t14.to_csv(f"{OUTDIR}/t14.csv", index=False)

with open(f"{OUTDIR}/results_B.json", "w") as f:
    json.dump(RESULTS, f, indent=1)
with open(f"{OUTDIR}/log_B.txt", "w") as f:
    f.write("\n".join(LOG))
log(f"\nwrote {len(RESULTS)} cells to {OUTDIR}/results_B.json")
