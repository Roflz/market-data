"""
v2/eval_candidates.py - stage 5: the best stage-4 candidates through the LucidFlex 25K eval judge (v2/eval_sim.py),
with and without the user's ADD-ON rule, next to matched luck at the same trade frequency and size.

CANDIDATES (stage-4 OOS kept trades, v2/out/oos_<file>.parquet; the EMA50 setup of stage 2 did not survive, so it is
  not here)
  A  60m opp3_1b M3 cls   the only stage-4 rule 'winner' (+$3.04/trade, edge vs drift +5.29, tc 1.74)
  B  15m hold    M3 cls   the most consistent one (10/13 years > 0, all 3 markets > 0, ~3,800 trades/yr pooled)
  C  60m opp3_1b M3 reg   positive in all 3 markets (MNQ +4.66, MES +1.98, MYM +0.58)
  Each with the exit it was trained on (its best exit in stage 4).

ONE POSITION PER MARKET. Kept signals are taken in time order (entry minute, then higher model score first);
  while a market has an open position, later signals of that market are not new trades:
  mode 'none'     they are ignored.
  mode 'add1'     a SAME-direction signal adds 1 micro;  mode 'addsame': it adds as many micros as the first entry.
                  Opposite-direction signals are ignored (the exit rule is the 'opposite evidence').
  THE ADD RULE (all prices on the 1-minute path; entry = open of the bar after the signal bar, as for every trade):
    the new leg n (q_n micros at e_n, its own signal stop s_n) is taken at the open of its entry bar, and every
    leg already open (the 'core', Qc micros, average entry avg) moves its stop to S, the level at which the WHOLE
    position nets $0 after costs if the core is stopped at S and the new leg at s_n:
        S = avg + d * [ c + (q_n / Qc) * (d * (e_n - s_n) + c) ],   c = 1 tick + cost/$ per point
    (cost = $1 commission + 1 tick each way per micro; stop fills 1 tick worse). A stop is never loosened (long:
    max(old, S)). The add is skipped when S would not be at least 1 tick on the safe side of e_n (the position is not
    far enough in profit to fund the add), when s_n is not on the safe side of e_n, when the open micros are at 20,
    or (eval books) when the day's realized P&L is <= -$600. The whole position exits together on the exit rule
    (opp3_1b: at the next bar's open after 3+ opposite-evidence kinds at a bar close; hold: no rule) or at the close
    of the last bar closing by 16:45; each leg can also be stopped on its own.
  Size: the first entry is sized by the policy (1/2/3/5 micros, or floor($150/$250/$400 / risk per micro), skipped
    if 0 and then it does not block the market); an add of 'addsame' copies the first entry's micros. At most 20 open
    micros per market in the walk.
BOOKS  per market (MNQ, MES, MYM) and the 3-market book ALL. The walk output (legs with micros) goes through book(): in
  time order, a 20-micro cap over everything open and the $600 realized daily loss limit (eval_sim conventions:
  realized = legs closed at or before the entry). In ALL, a base leg can be skipped/clipped by the cap; its later
  adds are then skipped too. When book() clips or skips an ADD whose stop move was already applied in the walk, the
  earlier legs keep the moved stop (an approximation, counted as approx_adds).
LUCK (matched, at the same frequency and size): for every kept signal of the candidate a random signal is drawn from
  the same market and timeframe, and the whole procedure (one position per market, adds, sizing, books) is run on the
  drawn set:
  rskip (N_RSKIP draws): from ALL rule-union events (model-free), same side, year, time-of-day block, stop decile
                         (stage 4's matched random skip, as literal draws).
  drift (N_DRIFT draws): from the trend pool (being in the trend at that hour, no pullback rule), same side, year,
                         entry hour, stop quintile.
EVAL   eval_sim.daily_pnl / eval_daily from every start day, windows 2013+, 2018+, 2022+, plus robustness on 2013+
  starts: '2013-24' (data cut at 2024-12-31, i.e. without 2025H1) and '2013+ -top10' (the series' 10 best days set to
  0; each null draw loses its own 10 best days). Consistency 40% and 50%. worst_day_raw = worst day before the -$600
  floor (the eval itself uses the floored day).

PHASES   walk (heavy: loads 1-minute data, one market at a time) -> v2/out/evalc_legs_<cand>_<sym>.parquet
         eval -> v2/out/evalc_eval.csv (one row per set/draw x book x mode x policy x consistency x window)
         report -> v2/out/evalc_table.csv (candidate next to luck), evalc_pnl.csv ($ per micro-trade by year/span)
         check (heavy) -> v2/out/evalc_handcheck.csv, evalc_trunc.csv;   gui -> v2/out/gui/*.csv
  cd research/confidence && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:../signals:.:v2 python3 -u \
      v2/eval_candidates.py --phase walk|eval|report|check|gui [--cands A,B,C] [--markets NQ,ES,YM]
"""
import argparse
import gc
import heapq
import json
import os
import time
import zlib

import numpy as np
import pandas as pd

import lucid

lucid.install()                                         # flat 16:45-18:00 before labels / exits are used

import dataset as ds                                     # noqa: E402
import ema50_check as ec                                 # noqa: E402
import eval_sim as es                                    # noqa: E402
import labels as lb                                      # noqa: E402
import signals as sg                                     # noqa: E402
import walkforward as wf                                 # noqa: E402

OUT = es.OUT
GUI = os.path.join(OUT, "gui")
MARKETS = ("NQ", "ES", "YM")
MICRO = {"NQ": "MNQ", "ES": "MES", "YM": "MYM"}
CANDS = {
    "A": dict(file="oos_M3_cls_opp3_1b_60m_exp", tf=60, exit="opp3_1b", name="60m opp3_1b M3 cls"),
    "B": dict(file="oos_M3_cls_hold_15m_exp", tf=15, exit="hold", name="15m hold M3 cls"),
    "C": dict(file="oos_M3_reg_opp3_1b_60m_exp", tf=60, exit="opp3_1b", name="60m opp3_1b M3 reg"),
}
POLICIES = [("fixed", 1), ("fixed", 2), ("fixed", 3), ("fixed", 5), ("risk", 150), ("risk", 250), ("risk", 400)]
MODES = ("none", "add1", "addsame")
N_RSKIP, N_DRIFT = 20, 10
CAP, DLL = 20, 600.0
MIN_NS = 60 * 10 ** 9
K_STOP, K_RULE, K_TIME = 1, 3, 0
ROBUST = {"2013-24": ("2013-01-01", "2024-12-31"), "2013+ -top10": ("2013-01-01", "2025-06-30")}


# ================================================================================================ market arrays
class Mkt:
    """Everything the walk needs for one market and base timeframe (positional arrays)."""

    def __init__(self, sym, tf, O1, H1, L1, C1, tmin, first, last, ok, forced, Ob, Cb, bstart, rule):
        spec = sg.SPEC[sym]
        self.sym, self.tf = sym, tf
        self.tick, self.usd, self.cost = spec["tick"], spec["usd"], spec["cost"]
        self.O1, self.H1, self.L1, self.C1 = O1, H1, L1, C1
        self.tmin = tmin                                          # int64 ns, minute START of each 1-minute row
        self.first, self.last = first, last
        self.lastc = np.maximum.accumulate(last)                  # last row of bars up to j (bars without rows)
        self.ok, self.forced = ok, forced
        self.Ob, self.Cb = Ob, Cb
        self.bstart = bstart
        self.bend = bstart + tf * MIN_NS
        n = len(Ob)
        if rule is None:
            self.nt = None
        else:
            self.nt = {}
            for d, flag in ((1, rule[0]), (-1, rule[1])):
                idx = np.where(np.asarray(flag, bool), np.arange(n), n)
                self.nt[d] = np.minimum.accumulate(idx[::-1])[::-1]

    @classmethod
    def from_frames(cls, sym, tf, b, m1, rule):
        ok, forced = lb.eligible(b, tf)
        first, last = lb.map_1m(m1, b, tf)
        return cls(sym, tf, m1.O.to_numpy(np.float64), m1.H.to_numpy(np.float64), m1.L.to_numpy(np.float64),
                   m1.C.to_numpy(np.float64), m1.index.as_unit("ns").asi8, first, last, ok, forced,
                   b.O.to_numpy(np.float64), b.C.to_numpy(np.float64), b.index.as_unit("ns").asi8, rule)

    def contiguity_breaks(self, b_seg):
        """Number of consecutive same-segment bar pairs (both with rows) whose 1-minute rows are not adjacent."""
        f, l = self.first, self.last
        same = (b_seg[1:] == b_seg[:-1]) & (l[:-1] >= 0) & (f[1:] >= 0)
        return int((same & (f[1:] != l[:-1] + 1)).sum())


def stop_hit(M, d, s, a, b):
    """First row in [a, b] where a stop at s is touched (long: L1 <= s); returns (row, fill) or (-1, nan)."""
    if a > b or not np.isfinite(s):
        return -1, np.nan
    m = (M.L1[a:b + 1] <= s) if d > 0 else (M.H1[a:b + 1] >= s)
    k = int(m.argmax())
    if not m[k]:
        return -1, np.nan
    r = a + k
    o = M.O1[r]
    return r, (min(o, s) - M.tick) if d > 0 else (max(o, s) + M.tick)


# ================================================================================================ signals
def make_signals(M, i, d, stop, session, score, key=None):
    """Signal arrays (sorted by entry row, then score descending) with the stand-alone exit of every signal (one leg,
    its own stop, the exit rule, the 16:45 bar). Drops signals that cannot be entered."""
    i = np.asarray(i, np.int64)
    d = np.asarray(d, np.int64)
    stop = np.asarray(stop, np.float64)
    score = np.asarray(score, np.float64)
    sess = pd.DatetimeIndex(session).normalize().as_unit("ns").asi8
    key = np.arange(len(i)) if key is None else np.asarray(key)
    n_b = len(M.Ob)
    e = i + 1
    okk = (i >= 0) & (e < n_b)
    okk[okk] &= M.ok[i[okk]]
    T = np.where(okk, M.forced[np.minimum(i, n_b - 1)], -1)
    okk &= (T >= 0)
    okk[okk] &= (M.first[e[okk]] >= 0) & (M.last[T[okk]] >= 0)
    sel = np.flatnonzero(okk)
    order = sel[np.lexsort((-score[sel], M.first[e[sel]]))]
    i, d, stop, score, sess, key, e, T = (x[order] for x in (i, d, stop, score, sess, key, e, T))
    r0 = M.first[e]
    entry = M.Ob[e]
    if M.nt is None:
        jr = T.copy()
    else:
        jr = np.where(d > 0, M.nt[1][e], M.nt[-1][e])
    rule = jr < T
    jend = np.where(rule, jr, T)
    stop_end = M.lastc[jend]
    nxt = np.where(rule, M.first[np.minimum(jend + 1, n_b - 1)], -1)
    at_open = rule & (nxt >= 0)
    px_end = np.where(at_open, M.O1[np.maximum(nxt, 0)], M.Cb[jend])
    row_end = np.where(at_open, nxt, stop_end)
    t_end = np.where(at_open, M.tmin[np.maximum(nxt, 0)] + MIN_NS, M.bend[jend])
    kind_end = np.where(rule, K_RULE, K_TIME)
    risk = d * (entry - stop)
    stop_w = np.where(risk > 0, stop, np.nan)                   # past-stop signals are never used (filtered upstream)
    if len(i):
        kd, xpx, xrow = lb.walk_1m(M.O1, M.H1, M.L1, M.C1, r0, stop_end, d, stop_w,
                                   np.full((len(i), 1), np.nan), M.tick)
        kd, xpx, xrow = kd[:, 0], xpx[:, 0], xrow[:, 0]
    else:
        kd = xpx = xrow = np.zeros(0)
    hit = kd == 1
    S = dict(i=i, d=d, stop=stop, score=score, sess=sess, key=key, e=e, T=T, r0=r0, entry=entry,
             risk_usd=np.abs(risk) * M.usd, ok_risk=risk > 0, stop_end=stop_end, row_end=row_end, px_end=px_end,
             t_end=t_end, kind_end=kind_end, at_open=at_open,
             sa_row=np.where(hit, xrow, row_end).astype(np.int64), sa_px=np.where(hit, xpx, px_end),
             sa_kind=np.where(hit, K_STOP, kind_end),
             sa_t=np.where(hit, M.tmin[np.where(hit, xrow, 0).astype(np.int64)] + MIN_NS, t_end),
             t_entry=M.bstart[e], t_sig=M.bstart[i])
    S["sa_pnl"] = d * (S["sa_px"] - entry) * M.usd - M.cost
    S["n_dropped"] = int(len(okk) - len(sel))
    return S


# ================================================================================================ the walk
def want_micros(policy, risk_usd):
    kind, x = policy
    if kind == "fixed":
        return int(x)
    return int(np.floor(float(x) / risk_usd + 1e-9)) if risk_usd > 0 else 0


def walk_book(M, S, mode, policy, cap=CAP, gid0=0):
    """One position at a time in this market; returns (legs dict of lists, counters). See the module docstring."""
    n = len(S["i"])
    L = {c: [] for c in ("gid", "leg", "is_add", "d", "t_sig", "t_entry", "t_exit", "sess", "micros", "pnl_usd",
                         "risk_usd", "kind", "moved", "key", "entry", "exit_px", "stop0", "stop_last")}
    cnt = dict(signals=n, positions=0, busy=0, opp=0, size0=0, adds=0, add_cap=0, add_cushion=0, add_badstop=0)
    r0, d_, sa_row, sa_kind = S["r0"], S["d"], S["sa_row"], S["sa_kind"]
    at_open = S["at_open"]
    busy_row, busy_open = -1, False
    gid = gid0
    k = 0
    adding = mode != "none"
    while k < n:
        r = r0[k]
        if r < busy_row or (r == busy_row and not busy_open):
            cnt["busy"] += 1
            k += 1
            continue
        if not S["ok_risk"][k]:
            k += 1
            continue
        q0 = min(want_micros(policy, S["risk_usd"][k]), cap)
        if q0 <= 0:
            cnt["size0"] += 1
            k += 1
            continue
        cnt["positions"] += 1
        se = S["stop_end"][k]
        j = k + 1
        has_more = j < n and r0[j] <= se
        if not adding or not has_more:
            _leg(L, M, S, k, gid, 0, False, q0, S["sa_row"][k], S["sa_px"][k], S["sa_t"][k], sa_kind[k], False,
                 S["stop"][k])
            busy_row = sa_row[k]
            busy_open = sa_kind[k] == K_RULE and at_open[k]
            gid += 1
            k += 1
            continue
        legs, k, end_row, end_open = _walk_position(M, S, k, q0, mode, cap, cnt)
        for no, g in enumerate(legs):
            _leg(L, M, S, g["k"], gid, no, no > 0, g["q"], g["row"], g["px"], g["t"], g["kind"], g["moved"],
                 g["s"])
        busy_row, busy_open = end_row, end_open
        gid += 1
    return L, cnt


def _leg(L, M, S, k, gid, no, is_add, q, row, px, t_exit, kind, moved, stop_last):
    d = int(S["d"][k])
    L["gid"].append(gid); L["leg"].append(no); L["is_add"].append(is_add); L["d"].append(d)
    L["t_sig"].append(S["t_sig"][k]); L["t_entry"].append(S["t_entry"][k]); L["t_exit"].append(int(t_exit))
    L["sess"].append(S["sess"][k]); L["micros"].append(int(q))
    L["pnl_usd"].append(d * (px - S["entry"][k]) * M.usd - M.cost)
    L["risk_usd"].append(S["risk_usd"][k]); L["kind"].append(int(kind)); L["moved"].append(bool(moved))
    L["key"].append(S["key"][k]); L["entry"].append(S["entry"][k]); L["exit_px"].append(px)
    L["stop0"].append(S["stop"][k]); L["stop_last"].append(stop_last)


def _advance(M, d, legs, a, b):
    """Walk the open legs over rows a..b with their current stops (legs sharing a stop share one search)."""
    if a > b:
        return
    done = {}
    for g in legs:
        if not g["open"]:
            continue
        s = g["s"]
        if s not in done:
            done[s] = stop_hit(M, d, s, a, b)
        row, px = done[s]
        if row >= 0:
            g.update(open=False, row=row, px=px, t=M.tmin[row] + MIN_NS, kind=K_STOP)


def _walk_position(M, S, k, q0, mode, cap, cnt):
    """Walk the position opened by signal k, taking adds from the later signals. Returns (legs, next signal index,
    end row, end-at-open flag)."""
    d = int(S["d"][k])
    r0 = S["r0"]
    n = len(r0)
    se = S["stop_end"][k]
    legs = [dict(k=k, q=q0, e=S["entry"][k], s=S["stop"][k], open=True, moved=False)]
    cur = r0[k]
    c = M.tick + M.cost / M.usd
    j = k + 1
    while j < n and r0[j] <= se:
        r2 = r0[j]
        _advance(M, d, legs, cur, r2 - 1)
        if not any(g["open"] for g in legs):
            break                                              # stopped out before signal j: j may start anew
        cur = max(cur, r2)
        if int(S["d"][j]) != d:
            cnt["opp"] += 1
            j += 1
            continue
        if r2 == r0[k] or not S["ok_risk"][j]:
            cnt["busy"] += 1
            j += 1
            continue
        e_n, s_n = S["entry"][j], S["stop"][j]
        open_q = sum(g["q"] for g in legs if g["open"])
        q_n = min(1 if mode == "add1" else q0, cap - open_q)
        if q_n <= 0:
            cnt["add_cap"] += 1
            j += 1
            continue
        if d * (e_n - s_n) <= 0:
            cnt["add_badstop"] += 1
            j += 1
            continue
        core = [g for g in legs if g["open"]]
        Qc = sum(g["q"] for g in core)
        avg = sum(g["q"] * g["e"] for g in core) / Qc
        Sbe = avg + d * (c + (q_n / Qc) * (d * (e_n - s_n) + c))
        if d * (e_n - Sbe) < M.tick - 1e-9:
            cnt["add_cushion"] += 1
            j += 1
            continue
        for g in core:
            new = max(g["s"], Sbe) if d > 0 else min(g["s"], Sbe)
            if new != g["s"]:
                g["s"], g["moved"] = new, True
        legs.append(dict(k=j, q=q_n, e=e_n, s=s_n, open=True, moved=False))
        cnt["adds"] += 1
        j += 1
    if any(g["open"] for g in legs):
        _advance(M, d, legs, cur, se)
    end_open = False
    for g in legs:
        if g["open"]:
            g.update(open=False, row=S["row_end"][k], px=S["px_end"][k], t=S["t_end"][k], kind=S["kind_end"][k])
            end_open = bool(S["at_open"][k])
    end_row = max(g["row"] for g in legs)
    if end_open and any(g["row"] == end_row and g["kind"] == K_STOP for g in legs):
        end_open = False
    return legs, j, end_row, end_open


# ================================================================================================ books
def book(te, tx, sess, want, pnl, gid, is_add, cap=CAP, dll=DLL):
    """Sequential 20-micro cap + realized daily loss limit over legs (any markets). gid must be unique per position
    across markets. Returns (micros taken, approx count = adds clipped or skipped after their stop move)."""
    order = np.lexsort((np.asarray(is_add, np.int8), te))
    n = len(te)
    taken = np.zeros(n, np.int64)
    heap, realized, open_m = [], {}, 0
    dead = set()
    approx = 0
    te_l, tx_l, s_l, w_l, p_l, g_l, a_l = (np.asarray(x).tolist() for x in (te, tx, sess, want, pnl, gid, is_add))
    for k in order.tolist():
        now = te_l[k]
        while heap and heap[0][0] <= now:
            _, m, p, dy = heapq.heappop(heap)
            open_m -= m
            realized[dy] = realized.get(dy, 0.0) + p
        g = g_l[k]
        if a_l[k] and g in dead:
            continue
        if dll is not None and realized.get(s_l[k], 0.0) <= -dll:
            if a_l[k]:
                approx += 1
            else:
                dead.add(g)
            continue
        m = min(w_l[k], cap - open_m)
        if m <= 0:
            if a_l[k]:
                approx += 1
            else:
                dead.add(g)
            continue
        if a_l[k] and m < w_l[k]:
            approx += 1
        taken[k] = m
        open_m += m
        heapq.heappush(heap, (tx_l[k], m, m * p_l[k], s_l[k]))
    return taken, approx


def eval_book(sess, pnl_total, cal, consistencies=(0.40, 0.50), robust=True):
    """eval_daily rows for the windows + robustness windows; adds worst_day_raw / worst_day per window."""
    sized = pd.DataFrame({"session": pd.DatetimeIndex(sess), "pnl_total": pnl_total})
    sized = sized[sized.pnl_total != 0] if len(sized) else sized
    raw = sized.groupby("session").pnl_total.sum().reindex(cal, fill_value=0.0).astype(float)
    daily = es.daily_pnl(sized, cal, DLL)
    E = es.eval_daily(daily, consistencies, es.WINDOWS)
    rows = [E]
    if robust:
        cut = daily[daily.index <= pd.Timestamp("2024-12-31")]
        rows.append(es.eval_daily(cut, consistencies, {"2013-24": ROBUST["2013-24"]}))
        z = daily.copy()
        w = (z.index >= pd.Timestamp("2013-01-01"))
        top = z[w].sort_values(ascending=False).index[:10]
        z[top] = 0.0
        rows.append(es.eval_daily(z, consistencies, {"2013+ -top10": ROBUST["2013+ -top10"]}))
    E = pd.concat(rows, ignore_index=True)
    allw = dict(es.WINDOWS, **ROBUST)
    wr, wf_, um = {}, {}, {}
    for wn, (a, b) in allw.items():
        m = (raw.index >= pd.Timestamp(a)) & (raw.index <= pd.Timestamp(b))
        wr[wn] = float(raw[m].min()) if m.any() else np.nan
        wf_[wn] = float(daily[m].min()) if m.any() else np.nan
        um[wn] = float(daily[m].mean()) if m.any() else np.nan
    E["worst_day_raw"] = E.window.map(wr)
    E["worst_day"] = E.window.map(wf_)
    E["usd_day_mean"] = E.window.map(um)
    return E


# ================================================================================================ walk phase
def kept_set(cand, sym, E):
    """Candidate kept trades of one market joined with their event rows (i, cells)."""
    c = CANDS[cand]
    K = pd.read_parquet(os.path.join(OUT, c["file"] + ".parquet"))
    K = K[K.market == sym].reset_index(drop=True)
    J = K[["t", "d", "score", "pnl_usd", "t_exit", "stop"]].merge(
        E[["t", "d", "i", "stop", "year", "hour", "tod_block", "dec", "rb", "session", "risk_usd"]],
        on=["t", "d"], how="left", suffixes=("_k", ""))
    if J.i.isna().any():
        raise RuntimeError(f"{cand} {sym}: {int(J.i.isna().sum())} kept trades not found in the events")
    if (np.abs(J.stop - J.stop_k) > 1e-9).any():
        raise RuntimeError(f"{cand} {sym}: stop mismatch kept vs events")
    J["i"] = J.i.astype(np.int64)
    return J


def load_pools(sym, tf):
    """Events (as models.load_market filters them) with dec/rb, and the trend pool (risk > 0) with rb."""
    E = pd.read_parquet(ds.events_path(sym, tf), columns=["t", "i", "d", "stop", "risk_usd", "past_stop", "session",
                                                          "year", "hour", "tod_block", "t_entry"])
    E = E[(E.risk_usd > 0) & (E.past_stop == 0)].reset_index(drop=True)
    P = pd.read_parquet(ds.trend_path(sym, tf), columns=["t", "i", "d", "stop", "risk_usd", "past_stop", "session",
                                                         "year", "hour", "tod_block"])
    A = ec.add_risk_bucket(pd.concat([E[["session", "year", "risk_usd"]], P[["session", "year", "risk_usd"]]],
                                     ignore_index=True))
    E["rb"] = A.rb.to_numpy()[:len(E)]
    P["rb"] = A.rb.to_numpy()[len(E):]
    E["dec"] = E.groupby("year").risk_usd.transform(
        lambda s: pd.qcut(s.rank(method="first"), 10, labels=False)).astype(np.int8)
    P = P[(P.risk_usd > 0) & (P.past_stop == 0)].reset_index(drop=True)
    return E, P


def signal_sets(cand, sym, E, P):
    """[(set, draw, frame with i, d, stop, session, score)] for the candidate and its matched luck draws."""
    K = kept_set(cand, sym, E)
    out = [("cand", 0, K[["i", "d", "stop", "session", "score"]])]
    for name, pool, nd, keys in (("rskip", E, N_RSKIP, ("d", "year", "tod_block", "dec")),
                                 ("drift", P, N_DRIFT, ("d", "year", "hour", "rb"))):
        idx, level = ec.matched_draws(K, pool, n_draws=nd, seed=zlib.crc32(f"{cand}{sym}{name}".encode()),
                                      keys=keys)
        rng = np.random.default_rng(zlib.crc32(f"{cand}{sym}{name}score".encode()))
        for j in range(nd):
            R = pool.iloc[idx[:, j]][["i", "d", "stop", "session"]].drop_duplicates(["i", "d"])
            R = R.assign(score=rng.random(len(R))).reset_index(drop=True)
            out.append((name, j, R))
        print(f"    {name}: {nd} draws, full-key match {100 * (level == len(keys)).mean():.1f}%", flush=True)
    return K, out


LEG_COLS = ["gid", "leg", "is_add", "d", "t_entry", "t_exit", "sess", "micros", "pnl_usd"]


def walk_market(sym, cands, F, m1):
    rules_cache = {}
    for cand in cands:
        t0 = time.time()
        c = CANDS[cand]
        tf, x = c["tf"], c["exit"]
        if tf not in rules_cache:
            rules_cache[tf] = ds.exit_rules(F, tf)
        rx = rules_cache[tf][x][2]
        b = F[tf]["b"]
        M = Mkt.from_frames(sym, tf, b, m1, rx)
        brk = M.contiguity_breaks(b.seg.to_numpy())
        E, P = load_pools(sym, tf)
        K, sets = signal_sets(cand, sym, E, P)
        parts, stats, cand_legs = [], [], []
        for si, (sname, draw, R) in enumerate(sets):
            S = make_signals(M, R.i, R.d, R.stop, R.session, R.score, key=np.arange(len(R)))
            if sname == "cand":
                # stand-alone exits must reproduce the stage-3 labels exactly
                kk = S["key"]
                diff = np.abs(S["sa_pnl"] - K.pnl_usd.to_numpy()[kk])
                print(f"  {cand} {sym}: {len(kk)}/{len(K)} kept signals walkable, stand-alone vs label pnl max diff "
                      f"{diff.max():.2e}, 1-min contiguity breaks {brk}", flush=True)
                stats.append(dict(cand=cand, market=sym, set="cand", draw=0, mode="-", policy="-",
                                  check_max_diff=float(diff.max()), check_n=len(kk), contiguity_breaks=brk,
                                  dropped=S["n_dropped"]))
            for mode in MODES:
                for pi, pol in enumerate(POLICIES):
                    Lg, cnt = walk_book(M, S, mode, pol)
                    D = pd.DataFrame(Lg)
                    stats.append(dict(cand=cand, market=sym, set=sname, draw=draw, mode=mode,
                                      policy=es.policy_name(pol), **cnt))
                    if sname == "cand":
                        cand_legs.append(D.assign(mode=mode, policy=es.policy_name(pol)))
                    D = D[LEG_COLS].assign(si=np.int16(si), mode=np.int8(MODES.index(mode)), pol=np.int8(pi))
                    parts.append(D)
        Lall = pd.concat(parts, ignore_index=True)
        for col, dt in (("gid", np.int32), ("leg", np.int8), ("d", np.int8), ("micros", np.int8),
                        ("pnl_usd", np.float32)):
            Lall[col] = Lall[col].astype(dt)
        Lall.to_parquet(os.path.join(OUT, f"evalc_legs_{cand}_{sym}.parquet"), compression="zstd")
        CL = pd.concat(cand_legs, ignore_index=True)
        for col in ("t_sig", "t_entry", "t_exit", "sess"):
            CL[col] = pd.to_datetime(CL[col])
        CL.insert(0, "market", sym)
        CL.insert(0, "cand", cand)
        CL.to_parquet(os.path.join(OUT, f"evalc_candlegs_{cand}_{sym}.parquet"), compression="zstd")
        meta = pd.DataFrame([dict(si=i, set=s, draw=dr) for i, (s, dr, _) in enumerate(sets)])
        meta.to_csv(os.path.join(OUT, f"evalc_sets_{cand}_{sym}.csv"), index=False)
        pd.DataFrame(stats).to_csv(os.path.join(OUT, f"evalc_walkstats_{cand}_{sym}.csv"), index=False)
        print(f"  {cand} {sym}: {len(sets)} sets x {len(MODES)} modes x {len(POLICIES)} policies walked, "
              f"{len(Lall):,} legs ({time.time() - t0:.0f}s)", flush=True)
        del Lall, parts, CL, E, P, M
        gc.collect()


def load_market_frames(sym):
    t0 = time.time()
    F = ds.load_frames(sym, tfs=(5, 15, 60))
    m1 = lb.load_1m(sym)
    m1 = m1.loc[m1.index < wf.HOLDOUT_SESSION_START]
    print(f"  {sym}: frames + 1-minute data loaded ({time.time() - t0:.0f}s)", flush=True)
    return F, m1


def phase_walk(cands, markets):
    for sym in markets:
        F, m1 = load_market_frames(sym)
        walk_market(sym, cands, F, m1)
        del F, m1
        gc.collect()


# ================================================================================================ eval phase
def phase_eval(cands, robust_nulls=True):
    rows = []
    cals = {s: es.load_calendar([s]) for s in MARKETS}
    cals["ALL"] = es.load_calendar(list(MARKETS))
    for cand in cands:
        t0 = time.time()
        Ls, metas = {}, {}
        for sym in MARKETS:
            Ls[sym] = pd.read_parquet(os.path.join(OUT, f"evalc_legs_{cand}_{sym}.parquet"))
            metas[sym] = pd.read_csv(os.path.join(OUT, f"evalc_sets_{cand}_{sym}.csv"))
        meta = metas["NQ"]
        for sym in MARKETS:
            if not metas[sym][["set", "draw"]].equals(meta[["set", "draw"]]):
                raise RuntimeError("set lists differ between markets")
        groups = {sym: Ls[sym].groupby(["si", "mode", "pol"]).indices for sym in MARKETS}
        for si, srow in meta.iterrows():
            for mi, mode in enumerate(MODES):
                for pi, pol in enumerate(POLICIES):
                    per = {}
                    for sym in MARKETS:
                        ix = groups[sym].get((si, mi, pi), np.zeros(0, np.int64))
                        per[sym] = Ls[sym].iloc[ix]
                    for bk in list(MARKETS) + ["ALL"]:
                        if bk == "ALL":
                            G = pd.concat([per[s].assign(gid=per[s].gid.astype(np.int64) + 10 ** 7 * q)
                                           for q, s in enumerate(MARKETS)], ignore_index=True)
                        else:
                            G = per[bk]
                        te = G.t_entry.to_numpy(np.int64)
                        tx = G.t_exit.to_numpy(np.int64)
                        sess = G.sess.to_numpy(np.int64)
                        taken, approx = book(te, tx, sess, G.micros.to_numpy(np.int64),
                                             G.pnl_usd.to_numpy(np.float64), G.gid.to_numpy(np.int64),
                                             G.is_add.to_numpy(bool))
                        pt = taken * G.pnl_usd.to_numpy(np.float64)
                        is_cand = srow["set"] == "cand"
                        R = eval_book(sess.astype("datetime64[ns]"), pt, cals[bk],
                                      robust=is_cand or robust_nulls)
                        base = ~G.is_add.to_numpy(bool)
                        tk = taken > 0
                        R.insert(0, "policy", es.policy_name(pol))
                        R.insert(0, "mode", mode)
                        R.insert(0, "book", MICRO.get(bk, bk))
                        R.insert(0, "draw", srow["draw"])
                        R.insert(0, "set", srow["set"])
                        R.insert(0, "cand", cand)
                        R["positions"] = int((tk & base).sum())
                        R["adds"] = int((tk & ~base).sum())
                        R["micros_mean"] = float(taken[tk].mean()) if tk.any() else 0.0
                        R["approx_adds"] = approx
                        R["usd_position"] = float(pt.sum() / max(1, (tk & base).sum()))
                        rows.append(R)
            if si % 5 == 0:
                print(f"  {cand}: set {si + 1}/{len(meta)} done ({time.time() - t0:.0f}s)", flush=True)
        del Ls, groups
        gc.collect()
    Rall = pd.concat(rows, ignore_index=True)
    p = os.path.join(OUT, "evalc_eval.csv")
    if os.path.exists(p):
        old = pd.read_csv(p)
        old = old[~old.cand.isin(cands)]
        Rall = pd.concat([old, Rall], ignore_index=True)
    Rall.to_csv(p, index=False)
    return Rall


# ================================================================================================ report phase
METRICS = ["pass_pct", "fail_pct", "days_pass_median", "within_5", "within_10", "within_20", "worst_day_raw"]


def table(R):
    """Candidate next to the luck draws: mean / p90 per null and the share of draws the candidate beats."""
    key = ["cand", "book", "mode", "policy", "consistency", "window"]
    C = R[R.set == "cand"].set_index(key)
    out = C[METRICS + ["n_starts", "positions", "adds", "micros_mean", "usd_day_mean", "approx_adds"]].copy()
    for name in ("rskip", "drift"):
        N = R[R.set == name]
        g = N.groupby(key)
        for m in ("pass_pct", "within_5", "within_10", "within_20", "days_pass_median", "fail_pct", "positions",
                  "adds"):
            out[f"{name}_{m}_mean"] = g[m].mean()
        for m in ("pass_pct", "within_10", "within_20"):
            out[f"{name}_{m}_p90"] = g[m].quantile(0.9)
        for m in ("pass_pct", "within_10"):
            J = N.join(C[[m]].rename(columns={m: "_c"}), on=key)
            out[f"{name}_{m}_rank"] = (J._c > J[m]).groupby([J[k] for k in key]).mean() * 100
    return out.reset_index()


def pnl_tables(cands):
    """$ per position by year / span at 1 micro (mode none = net $ per micro-trade; add1 = the whole position's $,
    first entry 1 micro + 1 per add), per market and pooled, next to the matched-luck means (edge = cand - luck)."""
    reps = []
    for cand in cands:
        raws = []
        for sym in MARKETS:
            Lg = pd.read_parquet(os.path.join(OUT, f"evalc_legs_{cand}_{sym}.parquet"))
            meta = pd.read_csv(os.path.join(OUT, f"evalc_sets_{cand}_{sym}.csv"))
            Lg = Lg[(Lg.pol == 0) & (Lg["mode"].isin([0, 1]))]
            Lg = Lg.assign(tot=Lg.micros.astype(float) * Lg.pnl_usd.astype(float))
            for (si, mi), G in Lg.groupby(["si", "mode"]):
                P = G.groupby("gid").agg(sess=("sess", "first"), pnl=("tot", "sum"), t_entry=("t_entry", "first"))
                raws.append(pd.DataFrame({"t_entry": pd.to_datetime(P.t_entry.to_numpy()),
                                          "session": pd.to_datetime(P.sess.to_numpy()),
                                          "pnl_usd": P.pnl.to_numpy(float), "market": MICRO[sym],
                                          "set": meta.set.iloc[si], "draw": meta.draw.iloc[si],
                                          "mode": MODES[mi]}))
        raw = pd.concat(raws, ignore_index=True)
        for (mk, sname, draw, mode), g in list(raw.groupby(["market", "set", "draw", "mode"])) + \
                [(("pooled",) + k, g) for k, g in raw.groupby(["set", "draw", "mode"])]:
            r = es.pnl_report(g)
            reps.append(r.assign(cand=cand, market=mk, set=sname, draw=draw, mode=mode))
    rep = pd.concat(reps, ignore_index=True)
    key = ["cand", "market", "mode", "span"]
    C = rep[rep.set == "cand"].set_index(key)
    out = C[["n", "usd_trade", "t_stat"]].copy()
    for name in ("rskip", "drift"):
        g = rep[rep.set == name].groupby(key)
        out[f"{name}_usd"] = g.usd_trade.mean()
        out[f"{name}_n"] = g.n.mean()
        out[f"edge_{name}"] = out.usd_trade - out[f"{name}_usd"]
    return out.reset_index()


def phase_report(cands):
    R = pd.read_csv(os.path.join(OUT, "evalc_eval.csv"))
    R = R[R.cand.isin(cands)]
    T = table(R)
    T.to_csv(os.path.join(OUT, "evalc_table.csv"), index=False)
    Pn = pnl_tables(cands)
    Pn.to_csv(os.path.join(OUT, "evalc_pnl.csv"), index=False)
    return T, Pn


# ================================================================================================ checks (heavy)
def hand_walk_position(M, S, k, q0, mode, cap=CAP):
    """Independent minute-by-minute re-walk of the position opened by signal k (plain loops over raw rows; adds at
    the open of their entry bar). Returns the list of (signal index, micros, net $ per micro)."""
    d = int(S["d"][k])
    T = int(S["T"][k])
    e0 = int(S["e"][k])
    c = M.tick + M.cost / M.usd
    by_entry_bar = {}
    for j in range(k + 1, len(S["i"])):
        if S["e"][j] > T:
            break
        if int(S["d"][j]) == d and S["e"][j] > e0:
            by_entry_bar.setdefault(int(S["e"][j]), j)
    legs = [[k, q0, S["entry"][k], S["stop"][k], None]]                 # k, q, entry, stop, exit px
    rule = None if M.nt is None else (M.nt[d] == np.arange(len(M.nt[d])))
    for jb in range(e0, T + 1):
        r_a, r_b = M.first[jb], M.last[jb]
        if jb in by_entry_bar and any(g[4] is None for g in legs) and r_a >= 0:
            j = by_entry_bar[jb]
            e_n, s_n = S["entry"][j], S["stop"][j]
            core = [g for g in legs if g[4] is None]
            Qc = sum(g[1] for g in core)
            q_n = min(1 if mode == "add1" else q0, cap - Qc)
            if q_n > 0 and d * (e_n - s_n) > 0:
                avg = sum(g[1] * g[2] for g in core) / Qc
                Sbe = avg + d * (c + (q_n / Qc) * (d * (e_n - s_n) + c))
                if d * (e_n - Sbe) >= M.tick - 1e-9:
                    for g in core:
                        g[3] = max(g[3], Sbe) if d > 0 else min(g[3], Sbe)
                    legs.append([j, q_n, e_n, s_n, None])
        if r_a >= 0:
            for r in range(r_a, r_b + 1):
                for g in legs:
                    if g[4] is not None:
                        continue
                    if d > 0 and M.L1[r] <= g[3]:
                        g[4] = min(M.O1[r], g[3]) - M.tick
                    elif d < 0 and M.H1[r] >= g[3]:
                        g[4] = max(M.O1[r], g[3]) + M.tick
        if not any(g[4] is None for g in legs):
            break
        if jb >= T:
            for g in legs:
                if g[4] is None:
                    g[4] = M.Cb[jb]
            break
        if rule is not None and rule[jb]:
            nx = M.first[jb + 1]
            px = M.O1[nx] if nx >= 0 else M.Cb[jb]
            for g in legs:
                if g[4] is None:
                    g[4] = px
            break
    return [(g[0], g[1], d * (g[4] - g[2]) * M.usd - M.cost) for g in legs]


def phase_check(cands, markets, n_pos=30):
    """Hand re-walk of add positions + a real-data truncation test (1-minute data after a cut set to NaN)."""
    rows, trows = [], []
    for sym in markets:
        F, m1 = load_market_frames(sym)
        rules_cache = {}
        for cand in cands:
            c = CANDS[cand]
            tf = c["tf"]
            if tf not in rules_cache:
                rules_cache[tf] = ds.exit_rules(F, tf)
            M = Mkt.from_frames(sym, tf, F[tf]["b"], m1, rules_cache[tf][c["exit"]][2])
            E, _ = load_pools(sym, tf)
            K = kept_set(cand, sym, E)
            S = make_signals(M, K.i, K.d, K.stop, K.session, K.score)
            for mode, pol in (("add1", ("fixed", 1)), ("addsame", ("risk", 250))):
                Lg, _ = walk_book(M, S, mode, pol)
                D = pd.DataFrame(Lg)
                gids = D.groupby("gid").is_add.any()
                gids = gids[gids].index.to_numpy()
                rng = np.random.default_rng(zlib.crc32(f"{cand}{sym}{mode}".encode()))
                for g in rng.choice(gids, size=min(n_pos, len(gids)), replace=False):
                    P = D[D.gid == g].sort_values("leg")
                    k0 = int(np.flatnonzero(S["key"] == P.key.iloc[0])[0])
                    hw = hand_walk_position(M, S, k0, int(P.micros.iloc[0]), mode)
                    hand_total = sum(q * p for _, q, p in hw)
                    walk_total = float((P.micros * P.pnl_usd).sum())
                    rows.append(dict(cand=cand, market=sym, mode=mode, policy=es.policy_name(pol), gid=int(g),
                                     t_entry=pd.Timestamp(int(P.t_entry.iloc[0])), legs_walk=len(P), legs_hand=len(hw),
                                     walk_usd=walk_total, hand_usd=hand_total, diff=abs(walk_total - hand_total)))
            # truncation: NaN-out the 1-minute data from a cut on; positions finished before it must not change
            for cut in ("2016-03-01 10:07", "2020-03-09 03:31", "2023-11-14 13:52"):
                ct = pd.Timestamp(cut).as_unit("ns").value
                r_cut = int(np.searchsorted(M.tmin, ct))
                Mt = Mkt.from_frames(sym, tf, F[tf]["b"], m1, rules_cache[tf][c["exit"]][2])
                for arr in ("O1", "H1", "L1", "C1"):
                    a = getattr(Mt, arr).copy()
                    a[r_cut:] = np.nan
                    setattr(Mt, arr, a)
                cutoff = K.t < pd.Timestamp(cut)
                St = make_signals(Mt, K.i[cutoff], K.d[cutoff], K.stop[cutoff], K.session[cutoff],
                                  K.score[cutoff])
                for mode in MODES:
                    A_, _ = walk_book(M, S, mode, ("fixed", 1))
                    B_, _ = walk_book(Mt, St, mode, ("fixed", 1))
                    A_, B_ = pd.DataFrame(A_), pd.DataFrame(B_)
                    gok = A_.groupby("gid").t_exit.max() <= ct
                    fa = A_[A_.gid.isin(gok[gok].index)]
                    fb = B_[B_.gid.isin(fa.gid.unique())]
                    same = len(fa) == len(fb) and np.allclose(fa.pnl_usd.to_numpy(), fb.pnl_usd.to_numpy()) and \
                        np.array_equal(fa.t_exit.to_numpy(), fb.t_exit.to_numpy())
                    trows.append(dict(cand=cand, market=sym, cut=cut, mode=mode, legs_before=len(fa), same=same))
            print(f"  {cand} {sym}: hand + truncation checks done", flush=True)
        del F, m1
        gc.collect()
    H = pd.DataFrame(rows)
    H.to_csv(os.path.join(OUT, "evalc_handcheck.csv"), index=False)
    Tr = pd.DataFrame(trows)
    Tr.to_csv(os.path.join(OUT, "evalc_trunc.csv"), index=False)
    print(f"hand check: {len(H)} positions, max diff {H['diff'].max():.2e}; truncation: "
          f"{int(Tr.same.sum())}/{len(Tr)} identical", flush=True)
    return H, Tr


# ================================================================================================ GUI files
def phase_gui(cands):
    os.makedirs(GUI, exist_ok=True)
    for cand in cands:
        c = CANDS[cand]
        parts = []
        for sym in MARKETS:
            L = pd.read_parquet(os.path.join(OUT, f"evalc_candlegs_{cand}_{sym}.parquet"))
            usd = sg.SPEC[sym]["usd"]
            for mode, tag in (("none", ""), ("add1", " +adds")):
                G = L[(L["mode"] == mode) & (L.policy == "1 micro")].copy()
                G["pts"] = G.pnl_usd / usd * G.micros
                G["usd_tot"] = G.pnl_usd * G.micros
                kinds = {K_STOP: "stop", K_RULE: c["exit"], K_TIME: "16:45 close"}
                P = G.sort_values(["gid", "leg"]).groupby("gid").agg(
                    date=("sess", "first"), entry_time=("t_entry", "first"), exit_time=("t_exit", "max"),
                    d=("d", "first"), entry=("entry", "first"), net_pts=("pts", "sum"), net_usd=("usd_tot", "sum"),
                    risk_usd=("risk_usd", "first"), micros=("micros", "sum"), legs=("leg", "count"),
                    kind=("kind", "last"))
                P["net_bp"] = 1e4 * P.net_pts / P.entry
                P["R"] = P.net_usd / P.risk_usd
                P["side"] = np.where(P.d > 0, "long", "short")
                P["exit_reason"] = P.kind.map(kinds)
                P["model"] = f"v2 {cand} {c['name']} {MICRO[sym]}{tag}"
                P["market"] = MICRO[sym]
                P["date"] = pd.DatetimeIndex(P.date).strftime("%Y-%m-%d")
                parts.append(P[["model", "date", "entry_time", "exit_time", "market", "side", "entry", "net_bp",
                                "net_usd", "R", "risk_usd", "micros", "legs", "exit_reason"]])
        out = pd.concat(parts, ignore_index=True).sort_values(["model", "entry_time"])
        p = os.path.join(GUI, f"v2_{cand}_{c['name'].replace(' ', '_')}_trades.csv")
        out.to_csv(p, index=False)
        print(f"  wrote {p} ({len(out):,} rows)", flush=True)


# ================================================================================================ trials log
def log_trials(T, cands):
    import run_pipeline as rp                                            # noqa: PLC0415
    W = T[(T.window == "2013+") & (T.consistency == 0.4)]
    for r in W[W.cand.isin(cands)].itertuples():
        rp.log_trial(module="v2-eval_candidates", scope=f"{r.cand}|{r.book}", model=CANDS[r.cand]["name"],
                     target=f"{r.mode}|{r.policy}", oos_rows=int(r.positions),
                     parameters=json.dumps(dict(mode=r.mode, policy=r.policy, book=r.book, cap=CAP, dll=DLL,
                                                n_rskip=N_RSKIP, n_drift=N_DRIFT)),
                     note=f"eval 2013+ 40%: pass {r.pass_pct:.1f} within10 {r.within_10:.1f} (rskip mean "
                          f"{r.rskip_within_10_mean:.1f} p90 {r.rskip_within_10_p90:.1f}; drift mean "
                          f"{r.drift_within_10_mean:.1f}); adds {int(r.adds)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=["walk", "eval", "report", "check", "gui", "log"])
    ap.add_argument("--cands", default="A,B,C")
    ap.add_argument("--markets", default="NQ,ES,YM")
    ap.add_argument("--n-rskip", type=int, default=None)
    ap.add_argument("--n-drift", type=int, default=None)
    a = ap.parse_args()
    global N_RSKIP, N_DRIFT
    N_RSKIP = N_RSKIP if a.n_rskip is None else a.n_rskip
    N_DRIFT = N_DRIFT if a.n_drift is None else a.n_drift
    cands = a.cands.split(",")
    markets = a.markets.split(",")
    t0 = time.time()
    if a.phase == "walk":
        phase_walk(cands, markets)
    elif a.phase == "eval":
        phase_eval(cands)
    elif a.phase == "report":
        phase_report(cands)
    elif a.phase == "check":
        phase_check(cands, markets)
    elif a.phase == "gui":
        phase_gui(cands)
    elif a.phase == "log":
        log_trials(pd.read_csv(os.path.join(OUT, "evalc_table.csv")), cands)
    print(f"done ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
