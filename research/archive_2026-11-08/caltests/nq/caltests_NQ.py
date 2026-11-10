"""
RECONCILED COPY of implementer A's script (caltests/A/caltests_A.py). Event-level P&L is unchanged (A and B agree to the
cent on every event except the 1b interpretation). Changes vs A, all marked "RECONCILE":
  * Benchmarks (tests 2, 3, 4-primary) drop observations that straddle one of the six missing-data NYSE days (they are
    not a single night / an h-session window / a single day) -- B's treatment.
  * Test 2 benchmark includes the ~66 roll nights, measured on back-adjusted prices ("all other NYSE nights") -- B's
    treatment; A had dropped them.
  * Test 4a benchmark keeps 2010-06-07 (A was right; B's loop started at index 1 and dropped it).
  * t_event = the t-statistic that pass criterion (1) uses: test 1 full-sample net $; test 2 full-sample GROSS excess bp;
    test 3 POST-PAPER net excess bp; test 4 full-sample net excess bp.
Original docstring follows.
Implementer A: four pre-registered calendar tests (month-end 60/40 fade, pre-expiry overnight, settlement-aligned
month-end reversal, turn-of-month day+1), each primary rule and variant, exactly as specified.

Run:  cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <this file>
Reads the project data read-only; writes only into this script's directory.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

PROJ = "/run/media/roflz/Disk 2/_/market_data"
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJ)
from calendar_days import expiry_fridays  # noqa: E402

NY = "America/New_York"
LAST_MONTH = pd.Period("2026-10", "M")          # last complete month
FIRST_MONTH = pd.Period("2010-06", "M")
TICK = 0.25
MULT = {"ES": 5.0, "NQ": 2.0}
COMM_RT = 1.00                                     # $ per round trip (0.50 per side)


def per_side(sym, ticks):
    return ticks * TICK * MULT[sym] + COMM_RT / 2


LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


# ----------------------------------------------------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------------------------------------------------
def backadjust(d):
    """Additive back-adjustment exactly as in daily_sessions.py (gap at each instrument change removed)."""
    roll = d.instrument_id.ne(d.instrument_id.shift()) & d.instrument_id.shift().notna()
    jump = (d.Open - d.Close.shift()).where(roll, 0.0)
    adj = jump[::-1].cumsum()[::-1].shift(-1).fillna(0.0)
    d["aO"], d["aC"] = d.Open + adj, d.Close + adj
    return d


def load_1m_daily(sym, cash_days, early_days):
    """Per cash day: close bar (15:59, or 12:59 on early-close days) and pre-close bar (15:54, or 12:54 on early-close
    days) values from the 1-minute bars, back-adjusted the same way as daily_sessions.py. Cached in OUT."""
    cache = f"{OUT}/cache_{sym}_daily.pkl"
    if os.path.exists(cache):
        return pd.read_pickle(cache)
    d = pd.read_csv(f"{PROJ}/data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
    d.index = pd.to_datetime(d.ts_event, utc=True).dt.tz_convert(NY)
    d = d.drop(columns="ts_event")
    d = d[~d.index.duplicated()].sort_index()
    d = backadjust(d)
    tmin = d.index.hour * 60 + d.index.minute
    d["tmin"] = tmin
    d["date"] = d.index.tz_localize(None).normalize()
    rth = d[(tmin >= 570) & (tmin < 960)]
    rth = rth[rth.date.isin(cash_days)]
    is_early = rth.date.isin(early_days).values
    out = pd.DataFrame(index=pd.DatetimeIndex(cash_days, name="date"))
    for name, tn, te in (("C", 959, 779), ("P", 954, 774), ("C1559", 959, 959)):
        tgt = np.where(is_early, te, tn)
        sub = rth[rth.tmin.values <= tgt]
        last = sub.groupby("date").tail(1).set_index("date")
        out[f"{name}_adj"] = last.aC
        out[f"{name}_raw"] = last.Close
        out[f"{name}_inst"] = last.instrument_id
        out[f"{name}_tmin"] = last.tmin
        out[f"{name}_tgt"] = np.where(out.index.isin(early_days), te, tn)
    first = rth[rth.tmin == 570].groupby("date").head(1).set_index("date")
    out["O_adj"], out["O_raw"], out["O_inst"] = first.aO, first.Open, first.instrument_id
    out.to_pickle(cache)
    return out


def load_zn_daily(cash_days, early_days):
    """ZN hourly: 'close' of NYSE day d = close of the hourly bar ending at the ES close time (16:00 ET; 13:00 ET on
    early-close days); 'pre-close' = close of the bar ending one hour earlier (15:00 ET; 12:00 ET on early close).
    As-of lookup (last bar ending at or before the target time) when the bar is missing. Back-adjusted like
    daily_sessions.py."""
    z = pd.read_csv(f"{PROJ}/data/ZN_fut_1h.csv", usecols=["ts_event", "Open", "Close", "instrument_id"])
    z.index = pd.to_datetime(z.ts_event, utc=True).dt.tz_convert(NY)
    z = z.drop(columns="ts_event")
    z = z[~z.index.duplicated()].sort_index()
    z = backadjust(z)
    end_ns = (z.index + pd.Timedelta(hours=1)).as_unit("ns").asi8
    out = pd.DataFrame(index=pd.DatetimeIndex(cash_days, name="date"))
    early = out.index.isin(early_days)
    for name, hn, he in (("C", 16, 13), ("P", 15, 12)):
        hrs = np.where(early, he, hn)
        tgt = pd.DatetimeIndex([pd.Timestamp(x) + pd.Timedelta(hours=int(h)) for x, h in zip(out.index, hrs)]
                               ).tz_localize(NY).as_unit("ns")
        pos = np.searchsorted(end_ns, tgt.asi8, side="right") - 1
        out[f"{name}_adj"] = z.aC.values[pos]
        out[f"{name}_raw"] = z.Close.values[pos]
        out[f"{name}_inst"] = z.instrument_id.values[pos]
        out[f"{name}_exact"] = end_ns[pos] == tgt.asi8
        out[f"{name}_barend"] = pd.DatetimeIndex(end_ns[pos]).tz_localize("UTC").tz_convert(NY)
    return out


# ----------------------------------------------------------------------------------------------------------------------
# Stats helpers
# ----------------------------------------------------------------------------------------------------------------------
def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def se(x):
    x = np.asarray(x, float)
    return float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else float("nan")


def block_of(year):
    b = 2010 + 2 * ((year - 2010) // 2)
    return f"{b}-{b + 1}"


def blocks(ev, col):
    g = ev.groupby(ev.date.dt.year.map(block_of))[col].mean()
    return int((g > 0).sum()), int(len(g)), {k: round(float(v), 2) for k, v in g.items()}


def by_year(ev, col="net_usd"):
    return {str(k): round(float(v), 2) for k, v in ev.groupby(ev.date.dt.year)[col].sum().items()}


def r2(x, n=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def base_record(tid, market, ev, post_col="post", excess_col=None, bench_excess_bp=None, notes=""):
    """ev columns: date, gross_usd, net_usd, net_usd_2t, gross_bp, net_bp, post (bool), optional excess columns."""
    post = ev[ev[post_col]]
    nb_pos, nb, _ = blocks(ev, "net_usd")
    t = tstat(ev[excess_col]) if excess_col else tstat(ev.net_usd)
    return {
        "id": tid, "market": market, "events": int(len(ev)),
        "gross_bp_mean": r2(ev.gross_bp.mean()), "net_bp_mean": r2(ev.net_bp.mean()),
        "net_usd_mean": r2(ev.net_usd.mean()), "net_usd_mean_2ticks": r2(ev.net_usd_2t.mean()),
        "net_usd_total": r2(ev.net_usd.sum(), 2), "t_event": r2(t),
        "post_paper_events": int(len(post)), "post_paper_net_usd_mean": r2(post.net_usd.mean()) if len(post) else 0.0,
        "two_year_blocks_positive": f"{nb_pos}/{nb}", "by_year_net_usd": by_year(ev),
        "benchmark_excess_bp": r2(bench_excess_bp) if bench_excess_bp is not None else None,
        "notes": notes,
    }


# ----------------------------------------------------------------------------------------------------------------------
# Calendar
# ----------------------------------------------------------------------------------------------------------------------
ses = pd.read_pickle(f"{PROJ}/data/daily_sessions_ES.pkl")
sesN = pd.read_pickle(f"{PROJ}/data/daily_sessions_NQ.pkl")
CASH = ses.index[ses.cash_day]
assert CASH.equals(sesN.index[sesN.cash_day])
EARLY = ses.index[ses.cash_day & ses.early_close]
N = len(CASH)
POS = {d: i for i, d in enumerate(CASH)}

# data gaps: weekdays inside the sample that are NYSE trading days but have no data at all (rule: we still count only
# the table's cash_day sessions, as instructed; affected events are flagged)
NYSE_OPEN_GAPS = pd.DatetimeIndex(["2014-06-12", "2014-06-13", "2014-09-23", "2014-09-24", "2014-09-25", "2014-12-31"])
for g in NYSE_OPEN_GAPS:
    assert g not in POS


def spans_gap(i0, i1):          # RECONCILE: a missing-data NYSE day lies strictly between cash days i0 and i1
    a, b = CASH[i0], CASH[i1]
    return bool(((NYSE_OPEN_GAPS > a) & (NYSE_OPEN_GAPS < b)).any())


GAPSPAN = np.array([spans_gap(i, i + 1) for i in range(N - 1)])
assert GAPSPAN.sum() == 3, GAPSPAN.sum()

mp = pd.Series(CASH.to_period("M"), index=CASH)
TMAP = {m: grp.index.max() for m, grp in pd.Series(CASH, index=CASH).groupby(mp.to_numpy())}
MONTHS = [m for m in sorted(TMAP) if m <= LAST_MONTH]          # complete months only (Nov 2026 excluded)
T_ALL = {m: TMAP[m] for m in MONTHS}

ES = load_1m_daily("ES", CASH, EARLY)
NQ = load_1m_daily("NQ", CASH, EARLY)
ZN = load_zn_daily(CASH, EARLY)

# ---- sanity checks against the session table
for sym, X, S in (("ES", ES, ses), ("NQ", NQ, sesN)):
    S = S.loc[CASH]
    norm = ~X.index.isin(EARLY)
    assert X.notna().all().all(), f"{sym}: missing values"
    assert np.allclose(X.C_adj[norm], S.close_adj[norm]), f"{sym}: 15:59 adj close mismatch vs table"
    assert np.allclose(X.C_raw[norm], S.close_raw[norm])
    assert np.allclose(X.O_adj, S.open_adj) and np.allclose(X.O_raw, S.open_raw)
    assert (X.O_inst == S.inst).all()
    nfb_c = int((X.C_tmin != X.C_tgt).sum())
    nfb_p = int((X.P_tmin != X.P_tgt).sum())
    log(f"{sym}: {len(X)} cash days; close-bar fallbacks {nfb_c}; pre-close (15:54/12:54) fallbacks {nfb_p}; "
        f"early-close days {len(EARLY)} (12:59 bar used)")
zfb = ZN[~(ZN.C_exact & ZN.P_exact)]
log(f"ZN: as-of fallbacks (target hourly bar missing) on {len(zfb)} cash days: "
    + ", ".join(f"{d:%Y-%m-%d}(C->{r.C_barend:%m-%d %H:%M},P->{r.P_barend:%m-%d %H:%M})" for d, r in zfb.iterrows()))


# ---- NQ RUN: swap the markets so every test labelled MES/ES below runs on MNQ/NQ ($2/pt, $2.00 round trip).
# (Tests labelled MNQ (1b, 2a) then run on MES and are ignored in this run.)
ES, NQ = NQ, ES
ses, sesN = sesN, ses
MULT = {"ES": 2.0, "NQ": 5.0}
log("NQ RUN: markets swapped; 'MES' results below are MNQ")


def C(X, i):          # adjusted close of cash day index i
    return X.C_adj.values[i]


# ======================================================================================================================
# TEST 1: Month-end 60/40 rebalancing fade (HMM timing), MES; variants (a) reversal leg, (b) MNQ
# ======================================================================================================================
SRC1_END = pd.Timestamp("2023-03-17")
es_cA, es_cR, es_pA = ES.C_adj.values, ES.C_raw.values, ES.P_adj.values
zn_cA, zn_cR, zn_pA = ZN.C_adj.values, ZN.C_raw.values, ZN.P_adj.values
es_r = np.r_[np.nan, (es_cA[1:] - es_cA[:-1]) / es_cR[:-1]]      # r_d with 16:00 closes
zn_r = np.r_[np.nan, (zn_cA[1:] - zn_cA[:-1]) / zn_cR[:-1]]


def growth(cA, cR, pA, rr, i_prev, t):
    """Product of (1+r_d), d = T_prev+1 .. t, with day t's own return measured to the pre-close price."""
    g = np.prod(1 + rr[i_prev + 1:t]) if t > i_prev + 1 else 1.0
    return g * (1 + (pA[t] - cA[t - 1]) / cR[t - 1])


# trailing 20-day realized vol of ES close-to-close returns, and its expanding median (diagnostic i)
rv20 = pd.Series(es_r, index=CASH).rolling(20).std() * np.sqrt(252)
rv20_med = rv20.expanding().median()

rows1 = []
for k, m in enumerate(MONTHS):
    if k == 0:
        continue                                              # June 2010: prior month-end close missing
    iT, iP = POS[T_ALL[m]], POS[T_ALL[MONTHS[k - 1]]]
    assert MONTHS[k - 1] == m - 1
    ts = list(range(iT - 4, iT + 1))
    cal = {}
    for t in ts:
        gE = growth(es_cA, es_cR, es_pA, es_r, iP, t)
        gZ = growth(zn_cA, zn_cR, zn_pA, zn_r, iP, t)
        cal[t] = int(np.sign(gE - gZ))
    rows1.append(dict(month=m, date=CASH[iT], iT=iT, iP=iP, **{f"cal{j}": cal[iT - j] for j in range(4, -1, -1)}))
ev1 = pd.DataFrame(rows1)
assert (ev1[[f"cal{j}" for j in range(5)]] != 0).all().all()


def run_fade(ev, X, sym, reversal=False):
    cA, cR = X.C_adj.values, X.C_raw.values
    inst = X.C_inst.values
    out = []
    for _, e in ev.iterrows():
        iT = e.iT
        days = list(range(iT - 4, iT + 2))                    # closes T-4 .. T+1
        pos = [-e[f"cal{iT - t}"] for t in range(iT - 4, iT + 1)]   # held from close t to close t+1
        if reversal:
            days.append(iT + 2)
            pos.append(e.cal4)                                # +Cal_{T-4} from T+1 close to T+2 close
        legs = [p * (cA[days[j + 1]] - cA[days[j]]) for j, p in enumerate(pos)]
        seq = [0] + pos + [0]
        sides = sum(abs(seq[j + 1] - seq[j]) for j in range(len(seq) - 1))
        flips = sum(1 for j in range(len(pos) - 1) if pos[j + 1] != pos[j])
        insts = set(inst[days])
        if len(insts) > 1:
            log(f"T1 {sym} {e.month}: instrument changes over hold {insts} (adjusted legs = booked per contract)")
        gross_pts = float(sum(legs))
        entry_raw = cR[days[0]]
        m = MULT[sym]
        out.append(dict(
            month=e.month, date=e.date, gross_pts=gross_pts, gross_usd=gross_pts * m,
            net_usd=gross_pts * m - sides * per_side(sym, 1), net_usd_2t=gross_pts * m - sides * per_side(sym, 2),
            sides=sides, flips=flips, entry_raw=entry_raw,
            gross_bp=gross_pts / entry_raw * 1e4, net_bp=(gross_pts - sides * per_side(sym, 1) / m) / entry_raw * 1e4,
            leg_T=legs[3], leg_T1=legs[4], leg_rev=legs[5] if reversal else np.nan,
            cal_T4=e.cal4, spread_ret=(cA[iT + 1] - cA[iT - 4]) / cR[iT - 4],
            post=e.date > SRC1_END,
            rv_hi=bool(rv20.iloc[iT - 4] > rv20_med.iloc[iT - 4]),
            moq=(e.month.month - 1) % 3 + 1, multi_inst=len(insts) > 1,
            gap_affected=str(e.month) in ("2014-06", "2014-09", "2014-12", "2015-01"),
        ))
    return pd.DataFrame(out)


def eval_fade(tid, market, sym, ev):
    m = MULT[sym]
    rt = 2 * per_side(sym, 1)
    full_mean, t = ev.net_usd.mean(), tstat(ev.net_usd)
    post = ev[ev.post]
    pre = ev[~ev.post]
    sp_neg = ev[ev.cal_T4 < 0].spread_ret.mean() * 1e4
    sp_pos = ev[ev.cal_T4 > 0].spread_ret.mean() * 1e4
    nb_pos, nb, bl = blocks(ev, "net_usd")
    no_covid = ev[~ev.month.astype(str).isin(["2020-02", "2020-03"])]
    c1 = full_mean > 0 and t >= 2.0
    c2 = post.net_usd.mean() > 0
    c3 = sp_neg - sp_pos > 0
    c4a = nb_pos >= np.ceil(2 / 3 * nb)
    c4b = ev.gross_usd.mean() >= 1.5 * rt
    c4c = no_covid.net_usd.mean() > 0
    vol = ev.groupby("rv_hi").net_usd.agg(["count", "mean"])
    moq = ev.groupby("moq").net_usd.agg(["count", "mean"])
    notes = (
        f"PASS={'YES' if all([c1, c2, c3, c4a, c4b, c4c]) else 'NO'}. "
        f"(1) full net mean ${full_mean:.2f}, t={t:.2f} -> {c1} (net bp mean {ev.net_bp.mean():.2f}, bp t={tstat(ev.net_bp):.2f}). "
        f"(2) post-paper (T>2023-03-17) n={len(post)} net mean ${post.net_usd.mean():.2f} SE ${se(post.net_usd):.2f} -> {c2}; "
        f"in-paper n={len(pre)} net mean ${pre.net_usd.mean():.2f} t={tstat(pre.net_usd):.2f}. "
        f"(3) signal spread {('NQ' if sym == 'NQ' else 'ES')} ret T-4->T+1: Cal<0 {sp_neg:.1f}bp (n={int((ev.cal_T4 < 0).sum())}) "
        f"minus Cal>0 {sp_pos:.1f}bp (n={int((ev.cal_T4 > 0).sum())}) = {sp_neg - sp_pos:.1f}bp -> {c3}. "
        f"(4) blocks {nb_pos}/{nb} -> {c4a}; gross mean ${ev.gross_usd.mean():.2f} vs 1.5xRT ${1.5 * rt:.2f} -> {c4b}; "
        f"ex Feb-Mar2020 net mean ${no_covid.net_usd.mean():.2f} -> {c4c}. "
        f"Costs: mean sides/event {ev.sides.mean():.2f} (mean flips {ev.flips.mean():.2f}), mean cost ${(ev.gross_usd - ev.net_usd).mean():.2f}. "
        f"Diagnostics: (i) RV20 at T-4 above expanding median: n={int(vol.loc[True, 'count']) if True in vol.index else 0} "
        f"net ${vol['mean'].get(True, np.nan):.2f}; below: n={int(vol.loc[False, 'count']) if False in vol.index else 0} "
        f"net ${vol['mean'].get(False, np.nan):.2f}. (ii) month-of-quarter net $: "
        + ", ".join(f"m{int(k)}={v['mean']:.2f}(n={int(v['count'])})" for k, v in moq.iterrows())
        + f". (iii) gross $ leg day T (T-1->T close) mean {ev.leg_T.mean() * m:.2f} t={tstat(ev.leg_T):.2f}; "
        f"day T+1 (T->T+1 close) mean {ev.leg_T1.mean() * m:.2f} t={tstat(ev.leg_T1):.2f}"
        + (f"; reversal leg T+1->T+2 mean {ev.leg_rev.mean() * m:.2f} t={tstat(ev.leg_rev):.2f}" if ev.leg_rev.notna().any() else "")
        + f". Blocks: {bl}. Events touching 2014 data gaps (Jun/Sep/Dec 2014, Jan 2015): "
        f"{int(ev.gap_affected.sum())}, net mean without them ${ev[~ev.gap_affected].net_usd.mean():.2f}."
    )
    rec = base_record(tid, market, ev, notes=notes)
    return rec


ev1p = run_fade(ev1, ES, "ES")
ev1a = run_fade(ev1, ES, "ES", reversal=True)
ev1b = run_fade(ev1, NQ, "NQ")
R = []
R.append(eval_fade("1-primary", "MES", "ES", ev1p))
R.append(eval_fade("1a", "MES", "ES", ev1a))
R.append(eval_fade("1b", "MNQ", "NQ", ev1b))
log(f"T1 events {len(ev1p)} (in-paper {int((~ev1p.post).sum())}, post {int(ev1p.post.sum())}); "
    f"first {ev1p.month.iloc[0]} last {ev1p.month.iloc[-1]}")

# side calculation (not a trial): MNQ with the signal rebuilt from NQ instead of ES
nq_cA, nq_cR, nq_pA = NQ.C_adj.values, NQ.C_raw.values, NQ.P_adj.values
nq_r = np.r_[np.nan, (nq_cA[1:] - nq_cA[:-1]) / nq_cR[:-1]]
alt = ev1.copy()
for idx, e in alt.iterrows():
    for j in range(5):
        t = e.iT - j
        alt.loc[idx, f"cal{j}"] = int(np.sign(growth(nq_cA, nq_cR, nq_pA, nq_r, e.iP, t)
                                              - growth(zn_cA, zn_cR, zn_pA, zn_r, e.iP, t)))
ev1b_alt = run_fade(alt, NQ, "NQ")
# RECONCILE: criterion (3) as literally written uses ES returns; for 1b (same ES/ZN signal) it equals the primary's spread
_sp_es = (ev1p[ev1p.cal_T4 < 0].spread_ret.mean() - ev1p[ev1p.cal_T4 > 0].spread_ret.mean()) * 1e4
R[-1]["notes"] += f" Criterion (3) with ES returns as literally written: {_sp_es:.1f}bp."
_pa = ev1b_alt[ev1b_alt.post]
_nb_alt = blocks(ev1b_alt, "net_usd")
R[-1]["notes"] += (f" B's reading (NQ in the signal too): post-paper n={len(_pa)} net ${_pa.net_usd.mean():.2f}, blocks "
                   f"{_nb_alt[0]}/{_nb_alt[1]}, gross mean ${ev1b_alt.gross_usd.mean():.2f}, net bp {ev1b_alt.net_bp.mean():.2f}.")
R[-1]["notes"] += (f" Side calc (not a trial): MNQ with Cal built from NQ instead of ES: net mean "
                   f"${ev1b_alt.net_usd.mean():.2f}, t={tstat(ev1b_alt.net_usd):.2f}, total ${ev1b_alt.net_usd.sum():.0f}; "
                   f"signal agreement with ES-based Cal at T-4: {(alt.cal4 == ev1.cal4).mean():.1%}.")

# ======================================================================================================================
# TEST 2: Pre-expiry overnight long (close of day before monthly expiry -> 09:30 open on E)
# ======================================================================================================================
SRC2_END = pd.Timestamp("2021-12-31")
EXP = sorted(d for d in expiry_fridays(CASH) if FIRST_MONTH <= d.to_period("M") <= LAST_MONTH)
for chk, want in (("2014-04", "2014-04-17"), ("2019-04", "2019-04-18"), ("2022-04", "2022-04-14"),
                  ("2025-04", "2025-04-17"), ("2026-06", "2026-06-18"), ("2025-06", "2025-06-20")):
    got = [d for d in EXP if d.to_period("M") == pd.Period(chk, "M")]
    assert got == [pd.Timestamp(want)], (chk, got)
EXPSET = set(EXP)


def run_overnight(X, S, sym):
    S = S.loc[CASH]
    cR, cI = X.C_raw.values, X.C_inst.values
    oR, oI = S.open_raw.values, S.inst.values
    ev, skipped = [], []
    for E in EXP:
        iE = POS[E]
        iP = iE - 1
        Pd = CASH[iP]
        if cI[iP] != oI[iE]:
            skipped.append(f"{E:%Y-%m-%d}({cI[iP]}->{oI[iE]})")
            continue
        between = pd.bdate_range(Pd + pd.Timedelta(days=1), E - pd.Timedelta(days=1))
        flag = len(between) > 0                               # a non-NYSE weekday between entry day and E
        g = oR[iE] - cR[iP]
        m = MULT[sym]
        # expiry-day fade (diagnostic): short at the 09:30 open on E, cover at the close on E
        fade_pts = -(cR[iE] - oR[iE]) if X.C_inst.values[iE] == oI[iE] else np.nan
        ev.append(dict(date=E, entry=Pd, gross_pts=g, gross_usd=g * m, net_usd=g * m - 2 * per_side(sym, 1),
                       net_usd_2t=g * m - 2 * per_side(sym, 2), entry_raw=cR[iP],
                       gross_bp=g / cR[iP] * 1e4, net_bp=(g - 2 * per_side(sym, 1) / m) / cR[iP] * 1e4,
                       flag=flag, post=E > SRC2_END, quarterly=E.month in (3, 6, 9, 12),
                       fade_bp=fade_pts / oR[iE] * 1e4))
    ev = pd.DataFrame(ev)
    # benchmark: all other NYSE nights (close of cash day d -> 09:30 open of next cash day), same instrument,
    # excluding pre-expiry nights; dated by the evening (start) date
    # RECONCILE: back-adjusted night returns so roll nights are kept ("all other NYSE nights"); drop the 3 nights that
    # straddle a missing-data NYSE day
    oA_, cA_ = X.O_adj.values, X.C_adj.values
    nights = pd.DataFrame(dict(start=CASH[:-1], end=CASH[1:],
                               ret_bp=(oA_[1:] - cA_[:-1]) / cR[:-1] * 1e4, same=cI[:-1] == oI[1:], gap=GAPSPAN))
    nights = nights[~nights.gap & ~nights.end.isin(EXPSET)]
    nights = nights[(nights.start.dt.to_period("M") >= FIRST_MONTH) & (nights.start.dt.to_period("M") <= LAST_MONTH)]
    return ev, nights, skipped


def eval_overnight(tid, market, sym, ev, nights, skipped):
    m = MULT[sym]
    b_full = nights.ret_bp.mean()
    b_post = nights[nights.start > SRC2_END].ret_bp.mean()
    b_pre = nights[nights.start <= SRC2_END].ret_bp.mean()
    ev = ev.copy()
    ev["ex_gross_bp"] = ev.gross_bp - b_full
    ev["ex_net_bp"] = ev.net_bp - b_full
    post = ev[ev.post]
    pre = ev[~ev.post]
    t_gx = tstat(ev.ex_gross_bp)
    c1 = ev.ex_gross_bp.mean() > 0 and t_gx >= 2.0
    post_ex = (post.gross_bp - b_post).mean()
    c2 = post.net_usd.mean() > 0 and post_ex > 0
    c3 = ev.net_usd_2t.mean() > 0
    nb_pos, nb, bl = blocks(ev, "net_usd")
    c4 = nb_pos >= np.ceil(2 / 3 * nb)
    nf = ev[~ev.flag]
    q = ev.groupby("quarterly").agg(n=("net_usd", "size"), net=("net_usd", "mean"), gbp=("gross_bp", "mean"))
    corr = ev[["gross_bp", "fade_bp"]].corr().iloc[0, 1]
    up, dn = ev[ev.gross_bp >= 0], ev[ev.gross_bp < 0]
    notes = (
        f"PASS={'YES' if all([c1, c2, c3, c4]) else 'NO'}. Benchmark nights (adjusted prices, roll nights kept, "
        f"gap-straddling nights dropped, ex pre-expiry): full n={len(nights)} (roll nights {int((~nights.same).sum())}) "
        f"mean {b_full:.3f}bp; in-paper {b_pre:.3f}bp; post-paper {b_post:.3f}bp; same-instrument-only (A's choice) mean "
        f"{nights[nights.same].ret_bp.mean():.3f}bp. "
        f"(1) full mean gross excess {ev.ex_gross_bp.mean():.2f}bp t={t_gx:.2f} -> {c1}. "
        f"(2) post-paper (E>=2022-01) n={len(post)} net ${post.net_usd.mean():.2f} SE ${se(post.net_usd):.2f}, "
        f"gross excess vs post-paper benchmark {post_ex:.2f}bp (net excess {(post.net_bp - b_post).mean():.2f}bp) -> {c2}; "
        f"in-paper n={len(pre)} net ${pre.net_usd.mean():.2f}, gross excess vs in-paper bench {(pre.gross_bp - b_pre).mean():.2f}bp "
        f"t={tstat(pre.gross_bp - b_pre):.2f}. "
        f"(3) full net mean at 2 ticks ${ev.net_usd_2t.mean():.2f} -> {c3}. (4) blocks {nb_pos}/{nb} -> {c4}. "
        f"t_event = t of GROSS excess bp (criterion 1); t of net excess bp = {tstat(ev.ex_net_bp):.3f}; "
        f"mean net excess {ev.ex_net_bp.mean():.3f}bp; post-paper SE of net $ {se(post.net_usd):.2f}, post-paper "
        f"gross excess t {tstat(post.gross_bp - b_post):.2f}. "
        f"Holiday-span flagged events: {int(ev.flag.sum())} ({', '.join(ev[ev.flag].date.dt.strftime('%Y-%m-%d'))}); "
        f"without flagged: n={len(nf)} net ${nf.net_usd.mean():.2f}, gross excess {nf.ex_gross_bp.mean():.2f}bp "
        f"t={tstat(nf.ex_gross_bp):.2f}, 2-tick net ${nf.net_usd_2t.mean():.2f}. "
        f"Skipped (instrument change): {skipped if skipped else 'none'}. "
        f"Diagnostics: (i) quarterly n={int(q.loc[True, 'n'])} net ${q.loc[True, 'net']:.2f} ({q.loc[True, 'gbp']:.1f}bp gross); "
        f"off-quarterly n={int(q.loc[False, 'n'])} net ${q.loc[False, 'net']:.2f} ({q.loc[False, 'gbp']:.1f}bp gross). "
        f"(iii) corr(overnight gross bp, expiry-day fade gross bp)={corr:.3f}; fade mean {ev.fade_bp.mean():.2f}bp; "
        f"after overnight>=0 (n={len(up)}): fade {up.fade_bp.mean():.2f}bp; after overnight<0 (n={len(dn)}): "
        f"fade {dn.fade_bp.mean():.2f}bp. Blocks: {bl}."
    )
    return base_record(tid, market, ev, excess_col="ex_gross_bp", bench_excess_bp=ev.ex_gross_bp.mean(), notes=notes), ev


ev2, n2, sk2 = run_overnight(ES, ses, "ES")
rec, ev2 = eval_overnight("2-primary", "MES", "ES", ev2, n2, sk2)
R.append(rec)
ev2a, n2a, sk2a = run_overnight(NQ, sesN, "NQ")
rec, ev2a = eval_overnight("2a", "MNQ", "NQ", ev2a, n2a, sk2a)
R.append(rec)
log(f"T2 events {len(ev2)} (in-paper {int((~ev2.post).sum())}, post {int(ev2.post.sum())}); skipped {sk2}; NQ skipped {sk2a}")

# ======================================================================================================================
# TEST 3: Settlement-aligned month-end liquidity reversal, MES long
# ======================================================================================================================
SRC3_END = pd.Timestamp("2013-12-31")


def k_settle(d):
    if d < pd.Timestamp("2017-09-05"):
        return 3
    if d <= pd.Timestamp("2024-05-27"):
        return 2
    return 1


def find_L(iT):
    """Last NYSE trading day x whose sale (settling k(x) trading days later) settles on or before T-1."""
    i = iT - 1
    while i + k_settle(CASH[i]) > iT - 1:
        i -= 1
    return i


# worked cases from the spec
assert CASH[find_L(POS[T_ALL[pd.Period("2017-08", "M")]])] == pd.Timestamp("2017-08-25")
assert CASH[find_L(POS[T_ALL[pd.Period("2017-09", "M")]])] == pd.Timestamp("2017-09-26")
assert CASH[find_L(POS[T_ALL[pd.Period("2024-05", "M")]])] == pd.Timestamp("2024-05-29")

# benchmark: h-session close-to-close windows starting in the same calendar year outside T-8..T+3 of every month
EXCL = set()
for m in MONTHS:
    iT = POS[T_ALL[m]]
    EXCL.update(range(max(iT - 8, 0), min(iT + 3, N - 1) + 1))
BENCH3 = {}
for h in (1, 2, 3):
    # RECONCILE: an h-session window must not straddle a missing-data NYSE day
    starts = np.array([i for i in range(N - h) if i not in EXCL and not spans_gap(i, i + h)])
    ret = (es_cA[starts + h] - es_cA[starts]) / es_cR[starts] * 1e4
    s = pd.Series(ret, index=CASH[starts])
    s = s[(s.index.to_period("M") >= FIRST_MONTH) & (s.index.to_period("M") <= LAST_MONTH)]
    for y, v in s.groupby(s.index.year):
        BENCH3[(y, h)] = (float(v.mean()), int(len(v)))


def regime(m):
    if m <= pd.Period("2017-08", "M"):
        return "T+3"
    if m <= pd.Period("2024-04", "M"):
        return "T+2"
    return "T+1"


rows3 = []
for m in MONTHS:
    iT = POS[T_ALL[m]]
    iL = find_L(iT)
    k = k_settle(CASH[iL])
    assert iL == iT - (k + 1)
    S = (es_pA[iL] - es_cA[iL - 5]) / es_cR[iL - 5]       # sign identical to P_L/C_{L-5}-1 (additive adj)
    rows3.append(dict(month=m, date=T_ALL[m], iT=iT, iL=iL, k=k, S=S, regime=regime(m)))
base3 = pd.DataFrame(rows3)


def run_hold(rows, entry_col, exit_off, sym="ES"):
    X = ES if sym == "ES" else NQ
    cA, cR, inst = X.C_adj.values, X.C_raw.values, X.C_inst.values
    m = MULT[sym]
    out = []
    for _, e in rows.iterrows():
        i0 = e[entry_col]
        i1 = e.iT + exit_off
        h = i1 - i0
        if inst[i0] != inst[i1]:
            log(f"T3 {e.month}: instrument change {inst[i0]}->{inst[i1]} (adjusted prices used)")
        g = cA[i1] - cA[i0]
        b, nb = BENCH3[(e.date.year, h)]
        gross_bp = g / cR[i0] * 1e4
        net_bp = (g - 2 * per_side(sym, 1) / m) / cR[i0] * 1e4
        out.append(dict(month=e.month, date=e.date, entry=CASH[i0], exit=CASH[i1], h=h, regime=e.regime, S=e.S,
                        gross_pts=g, gross_usd=g * m, net_usd=g * m - 2 * per_side(sym, 1),
                        net_usd_2t=g * m - 2 * per_side(sym, 2), gross_bp=gross_bp, net_bp=net_bp,
                        bench_bp=b, bench_n=nb, ex_gross_bp=gross_bp - b, ex_net_bp=net_bp - b,
                        post=e.date > SRC3_END))
    return pd.DataFrame(out)


ev3 = run_hold(base3, "iL", -1)
ev3a = run_hold(base3[base3.S < 0], "iL", -1)
b3 = base3.copy()
b3["i4"] = b3.iT - 4
ev3b = run_hold(b3, "i4", -1)


def eval_settle(tid, ev, extra=""):
    post = ev[ev.post]
    pre = ev[~ev.post]
    t_post = tstat(post.ex_net_bp)
    c1 = post.ex_net_bp.mean() > 0 and t_post >= 2.0
    reg_post = post.groupby("regime").ex_net_bp.agg(["count", "mean"]).reindex(["T+3", "T+2", "T+1"])
    reg_full = ev.groupby("regime").ex_net_bp.agg(["count", "mean"]).reindex(["T+3", "T+2", "T+1"])
    c2 = int((reg_post["mean"] > 0).sum()) >= 2
    nb_pos, nb, bl = blocks(ev, "net_usd")
    c3 = nb_pos >= np.ceil(2 / 3 * nb)
    notes = (
        f"PASS={'YES' if all([c1, c2, c3]) else 'NO'}. (1) post-paper (2014-01..2026-10) n={len(post)} mean net excess "
        f"{post.ex_net_bp.mean():.2f}bp t={t_post:.2f} (net ${post.net_usd.mean():.2f}) -> {c1}. "
        f"(2) post-paper regimes net excess bp: "
        + ", ".join(f"{r} n={int(v['count']) if v['count'] == v['count'] else 0} {v['mean']:.2f}" for r, v in reg_post.iterrows())
        + f" -> {c2} (full-sample regimes: "
        + ", ".join(f"{r} n={int(v['count']) if v['count'] == v['count'] else 0} {v['mean']:.2f}" for r, v in reg_full.iterrows())
        + f"). (3) blocks (net $) {nb_pos}/{nb} -> {c3}. In-paper (2010-06..2013-12) n={len(pre)} net ${pre.net_usd.mean():.2f}, "
        f"net excess {pre.ex_net_bp.mean():.2f}bp t={tstat(pre.ex_net_bp):.2f}. Full-sample mean net excess "
        f"{ev.ex_net_bp.mean():.2f}bp t={tstat(ev.ex_net_bp):.3f} (t_event field = POST-PAPER t). Hold lengths: {ev.h.value_counts().sort_index().to_dict()}. "
        f"Blocks: {bl}." + extra
    )
    gap = ev.month.astype(str).isin(["2014-09", "2014-12"])
    notes += (f" Data-gap sensitivity: {int(gap.sum())} events touch the 2014 no-data NYSE days (Sep 23-25, Dec 31); "
              f"without them post-paper net excess {post[~gap[ev.post]].ex_net_bp.mean():.2f}bp "
              f"t={tstat(post[~gap[ev.post]].ex_net_bp):.2f}.")
    rec = base_record(tid, "MES", ev, excess_col="ex_net_bp", bench_excess_bp=ev.ex_gross_bp.mean(), notes=notes)
    rec["t_event"] = r2(t_post)                      # RECONCILE: criterion-1 statistic (post-paper net excess t)
    rec["post_paper_net_excess_bp"] = r2(post.ex_net_bp.mean())
    return rec


since = pd.Period("2017-09", "M")
p_s, b_s = ev3[ev3.month >= since], ev3b[ev3b.month >= since]
mrg = p_s.merge(b_s, on="month", suffixes=("_p", "_b"))
cmp_txt = (f" Sep 2017-Oct 2026 primary vs (b): n={len(p_s)}; primary net ${p_s.net_usd.mean():.2f} "
           f"(net excess {p_s.ex_net_bp.mean():.2f}bp t={tstat(p_s.ex_net_bp):.2f}) vs (b) net ${b_s.net_usd.mean():.2f} "
           f"(net excess {b_s.ex_net_bp.mean():.2f}bp t={tstat(b_s.ex_net_bp):.2f}); paired diff primary-(b) "
           f"${(mrg.net_usd_p - mrg.net_usd_b).mean():.2f} t={tstat(mrg.net_usd_p - mrg.net_usd_b):.2f}; "
           f"mechanism supported (primary beats b): {p_s.net_usd.mean() > b_s.net_usd.mean()}.")
R.append(eval_settle("3-primary", ev3, cmp_txt))
R.append(eval_settle("3a", ev3a, f" Filter S<0 kept {len(ev3a)}/{len(ev3)} months."))
R.append(eval_settle("3b", ev3b, cmp_txt + " Identical to primary before 2017-09."))
assert (ev3[ev3.month < since].net_usd.values == ev3b[ev3b.month < since].net_usd.values).all()
log(f"T3 events {len(ev3)} (in-paper {int((~ev3.post).sum())}, post {int(ev3.post.sum())}); 3a {len(ev3a)}")

# ======================================================================================================================
# TEST 4: Turn-of-month day+1 long (control)
# ======================================================================================================================
oA, oR_ = ES.O_adj.values, ES.O_raw.values
rows4 = []
for m in MONTHS:
    iT = POS[T_ALL[m]]
    i1 = iT + 1
    insts = {ES.C_inst.values[iT], ES.O_inst.values[i1], ES.C_inst.values[i1]}
    if len(insts) > 1:
        log(f"T4 {m}: instrument change {insts}")
    g = es_cA[i1] - es_cA[iT]
    on = oA[i1] - es_cA[iT]
    intra = es_cA[i1] - oA[i1]
    rows4.append(dict(month=m, date=T_ALL[m], t1=CASH[i1], g=g, on=on, intra=intra, c_raw=es_cR[iT], o_raw=oR_[i1]))
r4 = pd.DataFrame(rows4)
T1SET = set(r4.t1)
cc = pd.DataFrame(dict(day=CASH[1:], start=CASH[:-1], ret_bp=(es_cA[1:] - es_cA[:-1]) / es_cR[:-1] * 1e4,
                       gap=GAPSPAN))
cc = cc[~cc.gap & ~cc.day.isin(T1SET)]           # RECONCILE: drop the close-to-close "days" that straddle a data gap
cc = cc[(cc.start.dt.to_period("M") >= FIRST_MONTH) & (cc.start.dt.to_period("M") <= LAST_MONTH)]
oc = pd.DataFrame(dict(day=CASH, ret_bp=(es_cA - oA) / oR_ * 1e4))
oc = oc[~oc.day.isin(T1SET)]
oc = oc[(oc.day.dt.to_period("M") >= FIRST_MONTH) & (oc.day.dt.to_period("M") <= LAST_MONTH)]


def mk4(pts, entry_raw, bench):
    m = MULT["ES"]
    ev = pd.DataFrame(dict(month=r4.month, date=r4.date, gross_pts=pts, gross_usd=pts * m,
                           net_usd=pts * m - 2 * per_side("ES", 1), net_usd_2t=pts * m - 2 * per_side("ES", 2),
                           gross_bp=pts / entry_raw * 1e4,
                           net_bp=(pts - 2 * per_side("ES", 1) / m) / entry_raw * 1e4, post=True))
    ev["ex_gross_bp"] = ev.gross_bp - bench
    ev["ex_net_bp"] = ev.net_bp - bench
    return ev


def eval4(tid, ev, bench, bench_n, extra):
    t = tstat(ev.ex_net_bp)
    c1 = ev.ex_net_bp.mean() > 0 and t >= 2.0
    nb_pos, nb, bl = blocks(ev, "net_usd")
    c2 = nb_pos >= np.ceil(2 / 3 * nb)
    notes = (f"PASS={'YES' if c1 and c2 else 'NO'}. Benchmark n={bench_n} mean {bench:.2f}bp. Mean net excess "
             f"{ev.ex_net_bp.mean():.2f}bp t={t:.2f} -> {c1}; gross excess {ev.ex_gross_bp.mean():.2f}bp "
             f"t={tstat(ev.ex_gross_bp):.2f}; blocks (net $) {nb_pos}/{nb} -> {c2}. All events post-source-sample. "
             f"Blocks: {bl}." + extra)
    gap = ev.month.astype(str) == "2014-12"
    notes += (f" Data-gap sensitivity: Dec 2014 T is 2014-12-30 because 2014-12-31 has no data; without it net excess "
              f"{ev[~gap].ex_net_bp.mean():.2f}bp t={tstat(ev[~gap].ex_net_bp):.2f}.")
    return base_record(tid, "MES", ev, excess_col="ex_net_bp", bench_excess_bp=ev.ex_gross_bp.mean(), notes=notes)


b4, b4a = cc.ret_bp.mean(), oc.ret_bp.mean()
ev4 = mk4(r4.g.values, r4.c_raw.values, b4)
on_bp = r4.on / r4.c_raw * 1e4
in_bp = r4.intra / r4.o_raw * 1e4
legs_txt = (f" Legs (gross): overnight T close->T+1 09:30 open mean {on_bp.mean():.2f}bp (${(r4.on * 5).mean():.2f}, "
            f"t={tstat(on_bp):.2f}); intraday T+1 open->close mean {in_bp.mean():.2f}bp (${(r4.intra * 5).mean():.2f}, "
            f"t={tstat(in_bp):.2f}).")
R.append(eval4("4-primary", ev4, b4, len(cc), legs_txt))
ev4a = mk4(r4.intra.values, r4.o_raw.values, b4a)
R.append(eval4("4a", ev4a, b4a, len(oc), ""))
log(f"T4 events {len(ev4)}")

# ----------------------------------------------------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------------------------------------------------
for name, ev in (("1_primary", ev1p), ("1a", ev1a), ("1b", ev1b), ("2_primary", ev2), ("2a", ev2a),
                 ("3_primary", ev3), ("3a", ev3a), ("3b", ev3b), ("4_primary", ev4), ("4a", ev4a)):
    ev.to_csv(f"{OUT}/events_{name}.csv", index=False)
with open(f"{OUT}/results.json", "w") as f:
    json.dump({"tests": R, "log": LOG}, f, indent=1, default=str)
for r in R:
    print("\n" + "=" * 100)
    print({k: v for k, v in r.items() if k not in ("notes", "by_year_net_usd")})
    print("by_year:", r["by_year_net_usd"])
    print("notes:", r["notes"])
