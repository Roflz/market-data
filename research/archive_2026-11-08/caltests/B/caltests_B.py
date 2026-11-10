#!/usr/bin/env python3
"""
Implementer B: four pre-registered calendar tests (month-end 60/40 fade, pre-expiry overnight, settlement-aligned
month-end reversal, turn-of-month +1) on MES/MNQ.  Reads the project data read-only; writes only to OUT.
Run:  cd "<project>" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this script>
"""
import os
import sys
import json
import numpy as np
import pandas as pd

PROJ = "/run/media/roflz/Disk 2/_/market_data"
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/caltests/B"
os.chdir(PROJ)
sys.path.insert(0, PROJ)
from calendar_days import expiry_fridays  # noqa: E402

os.makedirs(OUT, exist_ok=True)
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


MULT = {"ES": 5.0, "NQ": 2.0}
TICK = 0.25
COMM_SIDE = 0.50


def side_cost(sym, ticks):
    """$ per contract per side: `ticks` ticks of slippage + $0.50 commission."""
    return ticks * TICK * MULT[sym] + COMM_SIDE


FIRST_MONTH = pd.Period("2010-06", "M")
LAST_MONTH = pd.Period("2026-10", "M")          # last complete month
# NYSE trading days that are absent from the session tables because the 1-minute ES/NQ files have no bars at all
# (found by comparing weekdays with the NYSE holiday list; ZN trades normally on them).  Calendar offsets follow the
# table (cash_day sessions) as instructed; benchmark observations that straddle one of these days are dropped.
GAP_DAYS = pd.DatetimeIndex(["2014-06-12", "2014-06-13", "2014-09-23", "2014-09-24", "2014-09-25", "2014-12-31"])

# ---------------------------------------------------------------- calendar
sessES = pd.read_pickle("data/daily_sessions_ES.pkl")
sessNQ = pd.read_pickle("data/daily_sessions_NQ.pkl")
cash = sessES.index[sessES.cash_day]
assert cash.equals(sessNQ.index[sessNQ.cash_day])
early = sessES.early_close.reindex(cash).values.astype(bool)
N = len(cash)
IDX = {d: i for i, d in enumerate(cash)}
for g in GAP_DAYS:
    assert g not in IDX
months = pd.PeriodIndex(cash, freq="M")
TIDX = {}                                       # month -> index of T (last cash day of month)
for m in pd.period_range(FIRST_MONTH, LAST_MONTH, freq="M"):
    ii = np.where(months == m)[0]
    TIDX[m] = int(ii.max())
PERIOD_END = cash[TIDX[LAST_MONTH]]              # 2026-10-30
log("cash days", N, cash[0].date(), "->", cash[-1].date(), "| early closes", int(early.sum()),
    "| period end", PERIOD_END.date())


def spans_gap(i0, i1):
    """True if a GAP_DAY lies strictly between cash[i0] and cash[i1]."""
    a, b = cash[i0], cash[i1]
    return bool(((GAP_DAYS > a) & (GAP_DAYS < b)).any())


# ---------------------------------------------------------------- minute prices (ES, NQ)
def minute_prices(sym):
    d = pd.read_csv(f"data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"], index_col=0)
    d.index = pd.to_datetime(d.index, utc=True).tz_convert("America/New_York")
    d = d[~d.index.duplicated()].sort_index()
    # identical additive back-adjustment to daily_sessions.py
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    d["aO"], d["aC"] = d.Open + adj, d.Close + adj
    loc = d.index.tz_localize(None)
    d["date"] = loc.normalize()
    d["tmin"] = loc.hour * 60 + loc.minute
    r = d[(d.tmin >= 570) & (d.tmin <= 959)]
    r = r[r.date.isin(cash)]
    del d
    out = pd.DataFrame(index=cash)
    o = r[r.tmin == 570].set_index("date")
    out["O_raw"], out["O_adj"], out["O_inst"] = o.Open, o.aO, o.instrument_id
    tg = pd.DataFrame({"date": cash, "C_t": np.where(early, 779, 959), "P_t": np.where(early, 774, 954)})
    r = r.merge(tg, on="date", how="left")
    for nm in ("C", "P"):
        s = r[r.tmin <= r[f"{nm}_t"]].groupby("date").tail(1).set_index("date")
        out[f"{nm}_raw"], out[f"{nm}_adj"], out[f"{nm}_inst"], out[f"{nm}_tmin"] = s.Close, s.aC, s.instrument_id, s.tmin
        miss = (out[f"{nm}_tmin"] != tg.set_index("date")[f"{nm}_t"]).sum()
        log(f"{sym} {nm}: target bar missing on {int(miss)} days (as-of fallback used)")
    assert out.notna().all().all(), out[out.isna().any(axis=1)]
    # validation against the session table on normal days
    st = (sessES if sym == "ES" else sessNQ).reindex(cash)
    nm_ = ~early
    log(f"{sym} check vs table: max|C_adj-close_adj| normal days = {np.abs(out.C_adj[nm_] - st.close_adj[nm_]).max():.4f}; "
        f"max|O_adj-open_adj| = {np.abs(out.O_adj - st.open_adj).max():.4f}; inst==table inst: {(out.O_inst == st.inst).all()}")
    return out


ES = minute_prices("ES")
NQ = minute_prices("NQ")
PX = {"ES": ES, "NQ": NQ}

# ---------------------------------------------------------------- ZN hourly
z = pd.read_csv("data/ZN_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"], index_col=0)
z.index = pd.to_datetime(z.index, utc=True).tz_convert("America/New_York")
z = z[~z.index.duplicated()].sort_index()
zroll = z.instrument_id.ne(z.instrument_id.shift()) & z.instrument_id.shift().notna()
zjump = (z.Open - z.Close.shift()).where(zroll, 0.0)
zadj = zjump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
z["aC"] = z.Close + zadj


def zn_asof(hours):
    """Close of the last ZN hourly bar whose open is <= date + hours (ET), for every cash day."""
    tg = pd.DatetimeIndex([d + pd.Timedelta(hours=int(h)) for d, h in zip(cash, hours)]).tz_localize("America/New_York")
    pos = z.index.searchsorted(tg, side="right") - 1
    assert (pos >= 0).all()
    stale = (tg - z.index[pos]) > pd.Timedelta(0)
    return z.aC.values[pos], z.Close.values[pos], z.instrument_id.values[pos], stale, tg - z.index[pos]


# 16:00 price = close of the 15:00 bar; 15:00 price = close of the 14:00 bar.
# Early-close days: the equity close is 13:00, so the "close" is the 12:00 bar close and the own-day price is the
# 11:00 bar close (one hour before the close, as on normal days).
ZC_adj, ZC_raw, ZC_inst, ZC_stale, ZC_lag = zn_asof(np.where(early, 12, 15))
ZP_adj, ZP_raw, ZP_inst, ZP_stale, ZP_lag = zn_asof(np.where(early, 11, 14))
log("ZN close (16:00 / 13:00 early) stale on", int(ZC_stale.sum()), "days:",
    [f"{cash[i].date()}({ZC_lag[i]})" for i in np.where(ZC_stale)[0]])
log("ZN own-day (15:00 / 12:00 early) stale on", int(ZP_stale.sum()), "days:",
    [f"{cash[i].date()}({ZP_lag[i]})" for i in np.where(ZP_stale)[0]])


# ---------------------------------------------------------------- stats helpers
def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 3 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def se(x):
    x = np.asarray(x, float)
    return float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else float("nan")


def blocks(dates, vals):
    """2-year calendar blocks 2010-11, 2012-13, ..., 2024-25, 2026: count of blocks with mean > 0."""
    s = pd.Series(np.asarray(vals, float), index=pd.DatetimeIndex(dates))
    b = s.groupby((s.index.year - 2010) // 2).mean()
    return int((b > 0).sum()), int(len(b)), {f"{2010 + 2 * k}-{2011 + 2 * k}": round(float(v), 2) for k, v in b.items()}


def by_year(dates, vals):
    s = pd.Series(np.asarray(vals, float), index=pd.DatetimeIndex(dates))
    return {str(k): round(float(v), 2) for k, v in s.groupby(s.index.year).sum().items()}


def r2(x, n=3):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


RESULTS = []


def make_result(tid, market, ev, post_mask, notes, excess=False):
    """ev columns: key (date), gross_usd, net_usd, net2_usd, gross_bp, net_bp, [ex_bp, netex_usd]."""
    nb, nt, bdet = blocks(ev.key, ev.net_usd)
    res = dict(id=tid, market=market, events=int(len(ev)),
               gross_bp_mean=r2(ev.gross_bp.mean()), net_bp_mean=r2(ev.net_bp.mean()),
               net_usd_mean=r2(ev.net_usd.mean()), net_usd_mean_2ticks=r2(ev.net2_usd.mean()),
               net_usd_total=r2(ev.net_usd.sum(), 2),
               t_event=r2(tstat(ev.netex_usd if excess else ev.net_usd)),
               post_paper_events=int(post_mask.sum()), post_paper_net_usd_mean=r2(ev.net_usd[post_mask].mean()),
               two_year_blocks_positive=f"{nb}/{nt}", by_year_net_usd=by_year(ev.key, ev.net_usd), notes=notes)
    if excess:
        res["benchmark_excess_bp"] = r2(ev.ex_bp.mean())
    RESULTS.append(res)
    log(f"\n=== {tid} [{market}] events={len(ev)} gross$={ev.gross_usd.mean():.2f} net$={ev.net_usd.mean():.2f} "
        f"net2$={ev.net2_usd.mean():.2f} netbp={ev.net_bp.mean():.2f} t={res['t_event']} blocks {nb}/{nt} {bdet}")
    log("   notes:", notes)
    return res


# ================================================================ TEST 1: month-end 60/40 fade
def spec1(sym, reversal_leg=False):
    P = PX[sym]
    C_adj, C_raw, P_adj, C_inst = P.C_adj.values, P.C_raw.values, P.P_adj.values, P.C_inst.values
    m_list = list(pd.period_range(FIRST_MONTH + 1, LAST_MONTH, freq="M"))   # June 2010 skipped (no prior T)
    # trailing 20-day realized vol of daily returns (r_d definition) and its expanding median
    r = np.full(N, np.nan)
    r[1:] = (C_adj[1:] - C_adj[:-1]) / C_raw[:-1]
    rv = pd.Series(r).rolling(20).std().values * np.sqrt(252)
    rv_med = pd.Series(rv).expanding().median().values
    rows = []
    roll_viol = []
    for m in m_list:
        iT, iTp = TIDX[m], TIDX[m - 1]
        cal = {}
        for k in range(4, -1, -1):
            t = iT - k
            ge = 1.0
            gz = 1.0
            for dd in range(iTp + 1, t):
                ge *= 1.0 + (C_adj[dd] - C_adj[dd - 1]) / C_raw[dd - 1]
                gz *= 1.0 + (ZC_adj[dd] - ZC_adj[dd - 1]) / ZC_raw[dd - 1]
            ge *= 1.0 + (P_adj[t] - C_adj[t - 1]) / C_raw[t - 1]           # 15:55 price on day t
            gz *= 1.0 + (ZP_adj[t] - ZC_adj[t - 1]) / ZC_raw[t - 1]        # 15:00 price on day t
            cal[k] = float(np.sign(ge - gz))
        legs = [(iT - k, -cal[k]) for k in range(4, -1, -1)]               # (start index, position) to next close
        if reversal_leg:
            legs.append((iT + 1, cal[4]))
        pos = [p for _, p in legs]
        pts_legs = [p * (C_adj[s + 1] - C_adj[s]) for s, p in legs]
        contracts = abs(pos[0]) + sum(abs(pos[j] - pos[j - 1]) for j in range(1, len(pos))) + abs(pos[-1])
        i0, i1 = legs[0][0], legs[-1][0] + 1
        insts = set(C_inst[i0:i1 + 1])
        if len(insts) > 1:
            roll_viol.append(str(m))
        gross_pts = float(sum(pts_legs))
        raw_entry = C_raw[i0]
        spread_ret = (C_adj[iT + 1] - C_adj[iT - 4]) / C_raw[iT - 4]
        rows.append(dict(month=str(m), key=cash[iT], T=cash[iT].date(), entry=cash[i0].date(), exit=cash[i1].date(),
                         cal_m4=cal[4], cal_m3=cal[3], cal_m2=cal[2], cal_m1=cal[1], cal_0=cal[0],
                         contracts=contracts, gross_pts=gross_pts,
                         gross_usd=gross_pts * MULT[sym],
                         net_usd=gross_pts * MULT[sym] - contracts * side_cost(sym, 1),
                         net2_usd=gross_pts * MULT[sym] - contracts * side_cost(sym, 2),
                         gross_bp=gross_pts / raw_entry * 1e4,
                         net_bp=(gross_pts - contracts * side_cost(sym, 1) / MULT[sym]) / raw_entry * 1e4,
                         legT_usd=pts_legs[3] * MULT[sym], legT1_usd=pts_legs[4] * MULT[sym],
                         ret_T4_T1_bp=spread_ret * 1e4, rv20=rv[iT - 4], rv_med=rv_med[iT - 4],
                         moq=(m.month - 1) % 3 + 1))
    ev = pd.DataFrame(rows)
    return ev, roll_viol


def report1(tid, sym, ev, roll_viol, extra=""):
    rt = 2 * side_cost(sym, 1)
    post = ev.key >= pd.Timestamp("2023-03-01")
    inp = ~post
    full_mean, full_t = ev.net_usd.mean(), tstat(ev.net_usd)
    spread = ev.ret_T4_T1_bp[ev.cal_m4 < 0].mean() - ev.ret_T4_T1_bp[ev.cal_m4 > 0].mean()
    nb, nt, _ = blocks(ev.key, ev.net_usd)
    no2020 = ev[~ev.month.isin(["2020-02", "2020-03"])].net_usd.mean()
    hi = ev.rv20 > ev.rv_med
    c1 = full_mean > 0 and full_t >= 2.0
    c2 = ev.net_usd[post].mean() > 0
    c3 = spread > 0
    c4 = (nb / nt >= 2 / 3) and (ev.gross_usd.mean() >= 1.5 * rt) and (no2020 > 0)
    moq = ev.groupby("moq").net_usd.mean()
    notes = (f"PASS={'YES' if (c1 and c2 and c3 and c4) else 'NO'} [c1 full net mean>0&t>=2: {c1} (mean ${full_mean:.2f}, t {full_t:.2f}); "
             f"c2 post-paper net mean>0: {c2} (${ev.net_usd[post].mean():.2f}, SE ${se(ev.net_usd[post]):.2f}, n={int(post.sum())}); "
             f"c3 signal spread (ES ret T-4..T+1, Cal<0 minus Cal>0) = {spread:.1f} bp: {c3} "
             f"(n Cal<0={int((ev.cal_m4 < 0).sum())}, Cal>0={int((ev.cal_m4 > 0).sum())}); "
             f"c4 blocks {nb}/{nt}, gross mean ${ev.gross_usd.mean():.2f} vs 1.5xRT ${1.5 * rt:.2f}, net mean ex Feb-Mar 2020 ${no2020:.2f}: {c4}]. "
             f"In-paper (Jul2010-Feb2023) n={int(inp.sum())} net ${ev.net_usd[inp].mean():.2f} t {tstat(ev.net_usd[inp]):.2f}. "
             f"Gross mean ${ev.gross_usd.mean():.2f}; mean contracts traded {ev.contracts.mean():.2f} (mean cost ${(ev.gross_usd - ev.net_usd).mean():.2f}). "
             f"2-tick net mean ${ev.net2_usd.mean():.2f}. "
             f"Diag (i) RV20 at T-4 above expanding median: n={int(hi.sum())} net ${ev.net_usd[hi].mean():.2f}; below: n={int((~hi).sum())} net ${ev.net_usd[~hi].mean():.2f}. "
             f"(ii) month-of-quarter net $: {', '.join(f'm{k}={v:.2f}' for k, v in moq.items())}. "
             f"(iii) gross $ on day T leg {ev.legT_usd.mean():.2f}, day T+1 leg {ev.legT1_usd.mean():.2f}. "
             f"Contract changes inside hold: {roll_viol if roll_viol else 'none'}." + extra)
    return make_result(tid, f"M{sym}", ev, post.values, notes)


ev1, rv1 = spec1("ES")
ev1.to_csv(f"{OUT}/t1_primary_events.csv", index=False)
report1("1-primary", "ES", ev1, rv1)
ev1a, rv1a = spec1("ES", reversal_leg=True)
ev1a.to_csv(f"{OUT}/t1a_events.csv", index=False)
report1("1a", "ES", ev1a, rv1a, extra=" Variant: reversal leg +Cal_{T-4} held T+1 close -> T+2 close appended to primary.")
ev1b, rv1b = spec1("NQ")
ev1b.to_csv(f"{OUT}/t1b_events.csv", index=False)
report1("1b", "NQ", ev1b, rv1b, extra=" Variant: NQ substituted for ES in both the signal (G_NQ vs G_ZN) and the traded leg; "
        f"Cal_(T-4) agrees with the ES signal in {(ev1b.cal_m4 == ev1.cal_m4).mean() * 100:.0f}% of months.")
# sensitivity: ES-signal traded on NQ (not a trial; reported only)
_alt = ev1.copy()
_C = NQ.C_adj.values
_alt_pts = []
for _, row in ev1.iterrows():
    iT = IDX[pd.Timestamp(row["T"])]
    cals = [row.cal_m4, row.cal_m3, row.cal_m2, row.cal_m1, row.cal_0]
    _alt_pts.append(sum(-c * (_C[iT - k + 1] - _C[iT - k]) for k, c in zip(range(4, -1, -1), cals)))
_alt_net = np.array(_alt_pts) * 2.0 - ev1.contracts.values * side_cost("NQ", 1)
RESULTS[-1]["notes"] += f" Sensitivity (not a trial): ES-based signal traded on MNQ: net mean ${_alt_net.mean():.2f}, t {tstat(_alt_net):.2f}."

# data-gap sensitivity for test 1
_gm = ["2014-09", "2014-12"]
RESULTS[0]["notes"] += (f" Months whose T-4..T+1 window touches a missing-data NYSE day ({', '.join(_gm)}): kept per the table calendar; "
                        f"excluding them net mean ${ev1[~ev1.month.isin(_gm)].net_usd.mean():.2f}, t {tstat(ev1[~ev1.month.isin(_gm)].net_usd):.2f}.")


# ================================================================ TEST 2: pre-expiry overnight
E_all = sorted(expiry_fridays(cash))
E_ev = [e for e in E_all if FIRST_MONTH <= pd.Period(e, "M") <= LAST_MONTH]
for chk in ["2014-04-17", "2019-04-18", "2022-04-14", "2025-04-17", "2026-06-18"]:
    assert pd.Timestamp(chk) in E_all, chk
log("\nExpiry check: Good Friday / Juneteenth cases ->", [str(pd.Timestamp(c).date()) for c in
                                                         ["2014-04-17", "2019-04-18", "2022-04-14", "2025-04-17", "2026-06-18"]],
    "all present; n expiries in period", len(E_ev))
E_idx_set = set(IDX[e] for e in E_all)


def night_bench(sym):
    P = PX[sym]
    rows = []
    for i in range(N - 1):
        if cash[i] > PERIOD_END:
            break
        if (i + 1) in E_idx_set or spans_gap(i, i + 1):
            continue
        pts = P.O_adj.values[i + 1] - P.C_adj.values[i]
        rows.append(dict(d=cash[i], usd=pts * MULT[sym], bp=pts / P.C_raw.values[i] * 1e4))
    return pd.DataFrame(rows)


def spec2(sym):
    P = PX[sym]
    rows, skipped = [], []
    for e in E_ev:
        iE = IDX[e]
        ie = iE - 1
        if early[ie]:
            log("WARNING early-close entry day", cash[ie].date())
        if P.C_inst.values[ie] != P.O_inst.values[iE]:
            skipped.append(str(e.date()))
            continue
        pts = P.O_raw.values[iE] - P.C_raw.values[ie]
        assert abs(pts - (P.O_adj.values[iE] - P.C_adj.values[ie])) < 1e-6
        fade = -(P.C_adj.values[iE] - P.O_adj.values[iE])
        rows.append(dict(key=e, E=e.date(), entry=cash[ie].date(), flag=(e - cash[ie]).days > 1,
                         gross_pts=pts, gross_usd=pts * MULT[sym],
                         net_usd=pts * MULT[sym] - 2 * side_cost(sym, 1),
                         net2_usd=pts * MULT[sym] - 2 * side_cost(sym, 2),
                         gross_bp=pts / P.C_raw.values[ie] * 1e4,
                         net_bp=(pts - 2 * side_cost(sym, 1) / MULT[sym]) / P.C_raw.values[ie] * 1e4,
                         fade_usd=fade * MULT[sym], quarterly=e.month in (3, 6, 9, 12)))
    return pd.DataFrame(rows), skipped


def report2(tid, sym):
    ev, skipped = spec2(sym)
    nb_ = night_bench(sym)
    post = ev.key >= pd.Timestamp("2022-01-01")
    bfull_usd, bfull_bp = nb_.usd.mean(), nb_.bp.mean()
    bpost = nb_[nb_.d >= pd.Timestamp("2022-01-01")]
    bin_ = nb_[nb_.d < pd.Timestamp("2022-01-01")]
    ev["ex_usd"] = ev.gross_usd - bfull_usd
    ev["netex_usd"] = ev.net_usd - bfull_usd
    ev["ex_bp"] = ev.gross_bp - bfull_bp
    ev["netex_bp"] = ev.net_bp - bfull_bp
    ev.to_csv(f"{OUT}/t2_{tid}_events.csv", index=False)
    t_gex = tstat(ev.ex_usd)
    post_ex = (ev.gross_usd[post] - bpost.usd.mean()).mean()
    post_ex_bp = (ev.gross_bp[post] - bpost.bp.mean()).mean()
    nb, nt, _ = blocks(ev.key, ev.net_usd)
    c1 = ev.ex_usd.mean() > 0 and t_gex >= 2.0
    c2 = ev.net_usd[post].mean() > 0 and post_ex > 0
    c3 = ev.net2_usd.mean() > 0
    c4 = nb / nt >= 2 / 3
    nf = ev[~ev.flag]
    q = ev[ev.quarterly]
    oq = ev[~ev.quarterly]
    upn = ev.gross_usd >= 0
    notes = (f"PASS={'YES' if (c1 and c2 and c3 and c4) else 'NO'} [c1 full gross excess mean ${ev.ex_usd.mean():.2f} "
             f"({ev.ex_bp.mean():.2f} bp), t {t_gex:.2f} (bp t {tstat(ev.ex_bp):.2f}): {c1}; "
             f"c2 post-paper net ${ev.net_usd[post].mean():.2f} (SE {se(ev.net_usd[post]):.2f}) and post-paper gross excess vs post-paper nights "
             f"${post_ex:.2f} ({post_ex_bp:.2f} bp): {c2}; c3 full net mean at 2 ticks ${ev.net2_usd.mean():.2f}: {c3}; "
             f"c4 blocks {nb}/{nt}: {c4}]. Benchmark nights: full n={len(nb_)} mean ${bfull_usd:.3f} ({bfull_bp:.3f} bp); "
             f"in-paper ${bin_.usd.mean():.3f} ({bin_.bp.mean():.3f} bp); post-paper ${bpost.usd.mean():.3f} ({bpost.bp.mean():.3f} bp). "
             f"Gross mean ${ev.gross_usd.mean():.2f}. Net excess mean ${ev.netex_usd.mean():.2f} (t_event field = t of net excess $). "
             f"In-paper (Jun2010-Dec2021) n={int((~post).sum())} gross ${ev.gross_usd[~post].mean():.2f}, gross excess vs in-paper nights "
             f"${(ev.gross_usd[~post] - bin_.usd.mean()).mean():.2f} (t {tstat(ev.gross_usd[~post] - bin_.usd.mean()):.2f}), "
             f"{(ev.gross_bp[~post] - bin_.bp.mean()).mean():.2f} bp (t {tstat(ev.gross_bp[~post] - bin_.bp.mean()):.2f}). "
             f"Skipped for contract mismatch: {skipped if skipped else 'none'}. Flagged holiday-span events: "
             f"{[str(x) for x in ev.E[ev.flag]]}; without flagged: n={len(nf)} net ${nf.net_usd.mean():.2f}, gross excess ${nf.ex_usd.mean():.2f} t {tstat(nf.ex_usd):.2f}, "
             f"2-tick net ${nf.net2_usd.mean():.2f}, post net ${nf.net_usd[nf.key >= pd.Timestamp('2022-01-01')].mean():.2f}. "
             f"Diag (i) quarterly n={len(q)} net ${q.net_usd.mean():.2f} gross bp {q.gross_bp.mean():.2f}; off-quarterly n={len(oq)} net ${oq.net_usd.mean():.2f} gross bp {oq.gross_bp.mean():.2f}. "
             f"(iii) expiry-day fade (short 9:30 open E, cover 15:59 close E) gross mean ${ev.fade_usd.mean():.2f}; corr(overnight $, fade $) = {np.corrcoef(ev.gross_usd, ev.fade_usd)[0, 1]:.3f}; "
             f"fade gross when overnight>=0 (n={int(upn.sum())}) ${ev.fade_usd[upn].mean():.2f}, when <0 (n={int((~upn).sum())}) ${ev.fade_usd[~upn].mean():.2f}; "
             f"overnight net when >=0 ${ev.net_usd[upn].mean():.2f}, <0 ${ev.net_usd[~upn].mean():.2f}.")
    return make_result(tid, f"M{sym}", ev, post.values, notes, excess=True)


report2("2-primary", "ES")
report2("2a", "NQ")


# ================================================================ TEST 3: settlement-aligned month-end reversal
def k_of(d):
    if d < pd.Timestamp("2017-09-05"):
        return 3
    if d <= pd.Timestamp("2024-05-27"):
        return 2
    return 1


EXCL = set()
for m, iT in TIDX.items():
    EXCL.update(range(iT - 8, iT + 4))

_bench3_cache = {}


def bench3(sym, year, h):
    key = (sym, year, h)
    if key in _bench3_cache:
        return _bench3_cache[key]
    P = PX[sym]
    us, bps = [], []
    for i in range(N - h):
        d = cash[i]
        if d.year != year or d > PERIOD_END or i in EXCL or spans_gap(i, i + h):
            continue
        pts = P.C_adj.values[i + h] - P.C_adj.values[i]
        us.append(pts * MULT[sym])
        bps.append(pts / P.C_raw.values[i] * 1e4)
    _bench3_cache[key] = (float(np.mean(us)), float(np.mean(bps)), len(us))
    return _bench3_cache[key]


def spec3(sym, mode):
    P = PX[sym]
    C_adj, C_raw, P_adj, C_inst = P.C_adj.values, P.C_raw.values, P.P_adj.values, P.C_inst.values
    rows = []
    for m in pd.period_range(FIRST_MONTH, LAST_MONTH, freq="M"):
        iT = TIDX[m]
        tgt = iT - 1
        if mode == "fixed":
            iL = iT - 4
        else:
            iL = None
            for i in range(tgt, tgt - 10, -1):
                if i + k_of(cash[i]) <= tgt:
                    iL = i
                    break
            assert iL == iT - (k_of(cash[iL]) + 1)
        h = tgt - iL
        S = (P_adj[iL] - C_adj[iL - 5]) / C_raw[iL - 5]
        if mode == "filter" and not S < 0:
            continue
        pts = C_adj[tgt] - C_adj[iL]
        bu, bb, bn = bench3(sym, cash[iT].year, h)
        rc = 2 * side_cost(sym, 1)
        rows.append(dict(month=str(m), key=cash[iT], T=cash[iT].date(), L=cash[iL].date(), exit=cash[tgt].date(),
                         h=h, k=k_of(cash[iL]), regime_L=f"T+{k_of(cash[iL])}",
                         regime="T+3" if m <= pd.Period("2017-08", "M") else ("T+2" if m <= pd.Period("2024-04", "M") else "T+1"),
                         S=S,
                         inst_change=C_inst[iL] != C_inst[tgt],
                         gross_usd=pts * MULT[sym], net_usd=pts * MULT[sym] - rc,
                         net2_usd=pts * MULT[sym] - 2 * side_cost(sym, 2),
                         gross_bp=pts / C_raw[iL] * 1e4, net_bp=(pts - rc / MULT[sym]) / C_raw[iL] * 1e4,
                         bench_usd=bu, bench_bp=bb, bench_n=bn))
    ev = pd.DataFrame(rows)
    if mode != "fixed":
        assert (ev.regime == ev.regime_L).all()
    ev["ex_usd"] = ev.gross_usd - ev.bench_usd
    ev["netex_usd"] = ev.net_usd - ev.bench_usd
    ev["ex_bp"] = ev.gross_bp - ev.bench_bp
    ev["netex_bp"] = ev.net_bp - ev.bench_bp
    return ev


# worked cases
_ev3 = spec3("ES", "primary")
for mm, LL in [("2017-08", "2017-08-25"), ("2017-09", "2017-09-26"), ("2024-05", "2024-05-29")]:
    got = _ev3[_ev3.month == mm].L.iloc[0]
    assert str(got) == LL, (mm, got)
log("\nTest 3 worked cases OK: Aug 2017 L=2017-08-25, Sep 2017 L=2017-09-26, May 2024 L=2024-05-29")


def report3(tid, sym, mode, evb=None):
    ev = spec3(sym, mode)
    ev.to_csv(f"{OUT}/t3_{tid}_events.csv", index=False)
    post = ev.key >= pd.Timestamp("2014-01-01")
    pe = ev[post]
    regs = {}
    for rg in ("T+3", "T+2", "T+1"):
        x = pe[pe.regime == rg]
        regs[rg] = (len(x), x.netex_usd.mean() if len(x) else float("nan"), x.netex_bp.mean() if len(x) else float("nan"),
                    tstat(x.netex_usd))
    nreg = sum(1 for v in regs.values() if v[0] > 0 and v[1] > 0)
    nb, nt, _ = blocks(ev.key, ev.net_usd)
    tpost = tstat(pe.netex_usd)
    c1 = pe.netex_usd.mean() > 0 and tpost >= 2.0
    c2 = nreg >= 2
    c3 = nb / nt >= 2 / 3
    ip = ev[~post]
    allreg = ev.groupby("regime").netex_usd.agg(["count", "mean"])
    notes = (f"PASS={'YES' if (c1 and c2 and c3) else 'NO'} [c1 post-paper (2014-01..2026-10) net excess mean ${pe.netex_usd.mean():.2f} "
             f"({pe.netex_bp.mean():.2f} bp), t {tpost:.2f} (bp t {tstat(pe.netex_bp):.2f}), n={len(pe)}: {c1}; "
             f"c2 post-paper regimes with net excess>0: {nreg}/3 "
             f"({'; '.join(f'{k} n={v[0]} ${v[1]:.2f} ({v[2]:.2f} bp) t {v[3]:.2f}' for k, v in regs.items())}): {c2}; "
             f"c3 blocks {nb}/{nt}: {c3}]. Full-sample net excess ${ev.netex_usd.mean():.2f} (t_event field = full-sample t of net excess $), "
             f"gross excess {ev.ex_bp.mean():.2f} bp. In-paper (Jun2010-Dec2013) n={len(ip)} net ${ip.net_usd.mean():.2f} net excess ${ip.netex_usd.mean():.2f} "
             f"t {tstat(ip.netex_usd):.2f}. All-sample regimes net excess $: "
             f"{', '.join(f'{k} n={int(r_["count"])} {r_["mean"]:.2f}' for k, r_ in allreg.iterrows())}. "
             f"Hold lengths {ev.h.value_counts().sort_index().to_dict()}. Contract change inside hold: {int(ev.inst_change.sum())}.")
    if evb is not None:
        s17 = pd.Timestamp("2017-09-01")
        a, b = ev[ev.key >= s17], evb[evb.key >= s17]
        notes += (f" Sep2017-Oct2026 primary vs (b) fixed T-4->T-1: primary n={len(a)} net ${a.net_usd.mean():.2f} net excess ${a.netex_usd.mean():.2f} "
                  f"({a.netex_bp.mean():.2f} bp, t {tstat(a.netex_usd):.2f}); (b) n={len(b)} net ${b.net_usd.mean():.2f} net excess ${b.netex_usd.mean():.2f} "
                  f"({b.netex_bp.mean():.2f} bp, t {tstat(b.netex_usd):.2f}); primary beats (b) on net excess $: {a.netex_usd.mean() > b.netex_usd.mean()}, "
                  f"on net $: {a.net_usd.mean() > b.net_usd.mean()}. Pre-Sep2017 identical: "
                  f"{np.allclose(ev[ev.key < s17].net_usd.values, evb[evb.key < s17].net_usd.values)}.")
    return make_result(tid, f"M{sym}", ev, post.values, notes, excess=True), ev


_evb = spec3("ES", "fixed")
report3("3-primary", "ES", "primary", evb=_evb)
r3a, ev3a = report3("3a", "ES", "filter")
RESULTS[-1]["notes"] += " Variant (a): only months with S=(ES 15:55 on L)/(close L-5)-1 < 0."
report3("3b", "ES", "fixed")
RESULTS[-1]["notes"] += " Variant (b): fixed T-4 close -> T-1 close every month (h=3); benchmark uses h=3."


# ================================================================ TEST 4: turn-of-month +1
TP1 = set(TIDX[m] + 1 for m in TIDX)


def spec4(sym, intraday_only=False):
    P = PX[sym]
    C_adj, C_raw, O_adj, O_raw, C_inst, O_inst = (P.C_adj.values, P.C_raw.values, P.O_adj.values, P.O_raw.values,
                                                  P.C_inst.values, P.O_inst.values)
    # benchmark
    bu, bb = [], []
    for i in range(1, N):
        if i in TP1:
            continue
        if intraday_only:
            if cash[i] > PERIOD_END:
                continue
            pts = C_adj[i] - O_adj[i]
            base = O_raw[i]
        else:
            if cash[i - 1] > PERIOD_END or spans_gap(i - 1, i):
                continue
            pts = C_adj[i] - C_adj[i - 1]
            base = C_raw[i - 1]
        bu.append(pts * MULT[sym])
        bb.append(pts / base * 1e4)
    b_usd, b_bp = float(np.mean(bu)), float(np.mean(bb))
    rows = []
    rc = 2 * side_cost(sym, 1)
    for m in pd.period_range(FIRST_MONTH, LAST_MONTH, freq="M"):
        iT = TIDX[m]
        i1 = iT + 1
        on = O_adj[i1] - C_adj[iT]
        intr = C_adj[i1] - O_adj[i1]
        if intraday_only:
            pts, base = intr, O_raw[i1]
        else:
            pts, base = C_adj[i1] - C_adj[iT], C_raw[iT]
        rows.append(dict(month=str(m), key=cash[iT], T=cash[iT].date(), T1=cash[i1].date(), early_T=bool(early[iT]),
                         inst_change=(C_inst[iT] != C_inst[i1]),
                         on_usd=on * MULT[sym], intra_usd=intr * MULT[sym],
                         on_bp=on / C_raw[iT] * 1e4, intra_bp=intr / O_raw[i1] * 1e4,
                         gross_usd=pts * MULT[sym], net_usd=pts * MULT[sym] - rc, net2_usd=pts * MULT[sym] - 2 * side_cost(sym, 2),
                         gross_bp=pts / base * 1e4, net_bp=(pts - rc / MULT[sym]) / base * 1e4))
    ev = pd.DataFrame(rows)
    ev["ex_usd"] = ev.gross_usd - b_usd
    ev["netex_usd"] = ev.net_usd - b_usd
    ev["ex_bp"] = ev.gross_bp - b_bp
    ev["netex_bp"] = ev.net_bp - b_bp
    return ev, b_usd, b_bp, len(bu)


def report4(tid, sym, intraday_only):
    ev, b_usd, b_bp, bn = spec4(sym, intraday_only)
    ev.to_csv(f"{OUT}/t4_{tid}_events.csv", index=False)
    nb, nt, _ = blocks(ev.key, ev.net_usd)
    t = tstat(ev.netex_usd)
    c1 = ev.netex_usd.mean() > 0 and t >= 2.0
    c2 = nb / nt >= 2 / 3
    gm = ["2014-12"]
    ng = ev[~ev.month.isin(gm)]
    notes = (f"PASS={'YES' if (c1 and c2) else 'NO'} [mean net excess ${ev.netex_usd.mean():.2f} ({ev.netex_bp.mean():.2f} bp), "
             f"t {t:.2f} (bp t {tstat(ev.netex_bp):.2f}): {c1}; blocks {nb}/{nt}: {c2}]. Benchmark: n={bn} other "
             f"{'open-to-close' if intraday_only else 'close-to-close'} days, mean ${b_usd:.3f} ({b_bp:.3f} bp). "
             f"Gross mean ${ev.gross_usd.mean():.2f} ({ev.gross_bp.mean():.2f} bp), gross excess t {tstat(ev.ex_usd):.2f}. "
             f"Legs (gross): overnight T close->T+1 open ${ev.on_usd.mean():.2f} ({ev.on_bp.mean():.2f} bp, t {tstat(ev.on_usd):.2f}); "
             f"intraday T+1 open->close ${ev.intra_usd.mean():.2f} ({ev.intra_bp.mean():.2f} bp, t {tstat(ev.intra_usd):.2f}). "
             f"Early-close T months: {int(ev.early_T.sum())}. Contract change inside hold: {int(ev.inst_change.sum())}. "
             f"All events post-date the source sample. Dec 2014 uses T=2014-12-30 (2014-12-31 missing from data); excluding it net excess "
             f"${ng.netex_usd.mean():.2f} t {tstat(ng.netex_usd):.2f}.")
    return make_result(tid, "MES", ev, np.ones(len(ev), bool), notes, excess=True)


report4("4-primary", "ES", False)
report4("4a", "ES", True)

# ---------------------------------------------------------------- output
with open(f"{OUT}/results_B.json", "w") as f:
    json.dump(RESULTS, f, indent=1, default=str)
with open(f"{OUT}/log_B.txt", "w") as f:
    f.write("\n".join(LOG))
log("\nwrote", f"{OUT}/results_B.json")
