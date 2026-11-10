"""
G1 noise-band intraday momentum (PREREG.md section 1 A1 and section 2 G1) - signal, controls, statistics.

Signal written as fn(S, B) -> LEGS: one row per (session, decision time) at which a position is HELD after the
decision, with exit = the next scheduled decision time (or the final exit mark). The leg's exit is fixed by the
calendar (decision clock + the pre-built early-close list), so H.lookahead_check can compare legs exactly.
Trades = consecutive legs of the same side merged (a reversal starts a new trade; flat ends one).
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
if V3 not in sys.path:
    sys.path.insert(0, V3)
import harness as H                      # noqa: E402
import stats_protocol as sp              # noqa: E402

PREREG_SHA = "c9aef6629ccc2da406c76355302bce241faba444d893678de2a3a38c3e682460"
PREF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
LAST = pd.Timestamp("2025-06-27")
SEED_BOOT = 20261109

DEC_HALF = ["1000", "1030", "1100", "1130", "1200", "1230", "1300", "1330", "1400", "1430", "1500", "1530"]
DEC_HOUR = ["1000", "1100", "1200", "1300", "1400", "1500"]


def cal():
    """the common v3 calendar: H.calendar(('NQ','ES')) restricted to sessions <= 2025-06-27 (3,876 sessions)."""
    c = H.calendar(("NQ", "ES"))
    return c[c <= LAST]


def early_set(sym):
    """early-close sessions (exchange schedule ends before 16:00), identified ONCE outside the signal from last_t."""
    S = H.sessions(sym)
    return frozenset(S.index[S.last_t < 1320])


def _to_min(hhmm):
    return int(hhmm[:2]) * 60 + int(hhmm[2:])


def decision_grid(S, B5, dec):
    """C[n, m] = close of the latest 5-minute bar of the session ending at or before t (the bar ending at t when it
    exists), VW[n, m] = RTH VWAP (typical price x volume of 5-minute bars starting >= 09:30 and ending <= t)."""
    b = B5[["session", "H", "L", "C", "V"]].copy()
    ts = b.index
    b["end"] = ts + pd.Timedelta(minutes=5)
    tod = ts.hour * 60 + ts.minute
    sd = pd.DatetimeIndex(b["session"]).normalize()
    rth = (ts >= sd + pd.Timedelta(hours=9, minutes=30)) & (tod >= 570) & (tod < 960)
    tpv = np.where(rth, (b.H + b.L + b.C) / 3.0 * b.V, 0.0)
    vv = np.where(rth, b.V, 0.0)
    b["ctpv"] = pd.Series(tpv, index=b.index).groupby(b["session"].to_numpy()).cumsum().to_numpy()
    b["cv"] = pd.Series(vv, index=b.index).groupby(b["session"].to_numpy()).cumsum().to_numpy()
    b = b.reset_index(drop=True)[["session", "end", "C", "ctpv", "cv"]]
    b["session"] = pd.DatetimeIndex(b["session"]).astype("datetime64[ns]")
    b["end"] = pd.DatetimeIndex(b["end"]).astype("datetime64[ns]")
    sess = pd.DatetimeIndex(S.index).astype("datetime64[ns]")
    m = len(dec)
    g = pd.DataFrame({"session": np.repeat(sess, m), "j": np.tile(np.arange(m), len(sess))})
    g["T"] = g["session"] + pd.to_timedelta(np.tile([_to_min(x) for x in dec], len(sess)), unit="min")
    g = g.sort_values("T", kind="stable")
    b = b.sort_values("end", kind="stable")
    mg = pd.merge_asof(g, b, left_on="T", right_on="end", by="session", direction="backward")
    mg = mg.sort_values(["session", "j"])
    C = mg["C"].to_numpy(np.float64).reshape(len(sess), m)
    cv = mg["cv"].to_numpy(np.float64).reshape(len(sess), m)
    VW = np.where(cv > 0, mg["ctpv"].to_numpy(np.float64).reshape(len(sess), m) / np.where(cv > 0, cv, 1), np.nan)
    return C, VW


def make_signal(early, lookback=14, dec=DEC_HALF, final_exit="1600", early_last_dec="1230", early_exit="1300",
                skip=None):
    """returns fn(S, B) -> legs DataFrame (session, entry, exit, d). `early` = fixed early-close session set;
    `skip` = optional fixed set of sessions not traded (filters known at the open, built outside)."""
    dec = list(dec)
    m = len(dec)
    dec_ok_early = np.array([_to_min(x) <= _to_min(early_last_dec) for x in dec])

    def fn(S, B):
        n = len(S)
        if n == 0:
            return pd.DataFrame(columns=["session", "entry", "exit", "d"])
        C, VW = decision_grid(S, B[5], dec)
        O = S["px_0930"].to_numpy(np.float64)
        pc = S["prev_close_1600"].to_numpy(np.float64)
        pl = S["prev_last_px"].to_numpy(np.float64)
        cprev = np.where(np.isfinite(pc), pc, pl)
        is_early = np.array([s in early for s in S.index])
        move = np.abs(C / O[:, None] - 1.0)
        full_ok = (~is_early) & np.isfinite(O) & np.isfinite(move).all(axis=1)
        fidx = np.flatnonzero(full_ok)
        nb = np.searchsorted(fidx, np.arange(n), side="left")            # full sessions strictly before i
        sig = np.full((n, m), np.nan)
        cs = np.vstack([np.zeros((1, m)), np.cumsum(np.where(np.isfinite(move[fidx]), move[fidx], 0), axis=0)])
        has = nb >= lookback
        sig[has] = (cs[nb[has]] - cs[nb[has] - lookback]) / lookback
        tradable = has & np.isfinite(O) & np.isfinite(cprev)
        if skip is not None:
            tradable &= ~np.array([s in skip for s in S.index])
        UB = np.maximum(O, cprev)[:, None] * (1 + sig)
        LB = np.minimum(O, cprev)[:, None] * (1 - sig)
        pos = np.zeros(n, np.int64)
        legs = []
        for j in range(m):
            act = tradable & (~is_early | dec_ok_early[j])
            c, vw, u, lo = C[:, j], VW[:, j], UB[:, j], LB[:, j]
            okc = act & np.isfinite(c)
            new = pos.copy()
            lng = okc & (pos == 1)
            sht = okc & (pos == -1)
            flat = okc & (pos == 0)
            hi_l = np.fmax(u, vw)                                         # max(UB, VWAP), VWAP NaN -> UB
            lo_s = np.fmin(lo, vw)
            new[lng] = np.where(c[lng] < lo[lng], -1, np.where(c[lng] < hi_l[lng], 0, 1))
            new[sht] = np.where(c[sht] > u[sht], 1, np.where(c[sht] > lo_s[sht], 0, -1))
            new[flat] = np.where(c[flat] > u[flat], 1, np.where(c[flat] < lo[flat], -1, 0))
            # inactive sessions (early after 12:30) keep their position until the final exit
            pos = np.where(okc, new, pos)
            holding = act & (pos != 0)
            if holding.any():
                # exit of this leg = next decision of the session's schedule, else the final exit
                nxt_full = dec[j + 1] if j + 1 < m else final_exit
                nxt_early = next((dec[k] for k in range(j + 1, m) if dec_ok_early[k]), early_exit)
                idx = np.flatnonzero(holding)
                legs.append(pd.DataFrame({"session": S.index[idx], "entry": dec[j],
                                          "exit": np.where(is_early[idx], nxt_early, nxt_full),
                                          "d": pos[idx]}))
            pos = np.where(act, pos, 0)                                   # no carry beyond the schedule
        if not legs:
            return pd.DataFrame(columns=["session", "entry", "exit", "d"])
        L = pd.concat(legs, ignore_index=True)
        L["_k"] = [H.mark_index(x) for x in L["entry"]]
        L = L.sort_values(["session", "_k"]).drop(columns="_k").reset_index(drop=True)
        return L

    return fn


def merge_legs(L):
    """consecutive legs of one session with the same side and contiguous marks -> one trade."""
    if len(L) == 0:
        return pd.DataFrame(columns=["session", "entry", "exit", "d"])
    L = L.copy()
    L["ke"] = [H.mark_index(x) for x in L["entry"]]
    L["kx"] = [H.mark_index(x) for x in L["exit"]]
    L = L.sort_values(["session", "ke"]).reset_index(drop=True)
    s = L["session"].to_numpy()
    newt = np.ones(len(L), bool)
    newt[1:] = ~((s[1:] == s[:-1]) & (L.d.to_numpy()[1:] == L.d.to_numpy()[:-1])
                 & (L.ke.to_numpy()[1:] == L.kx.to_numpy()[:-1]))
    gid = np.cumsum(newt)
    T = L.groupby(gid).agg(session=("session", "first"), ke=("ke", "first"), kx=("kx", "last"), d=("d", "first"),
                           n_legs=("d", "size"))
    T = T.rename(columns={"ke": "entry", "kx": "exit"}).reset_index(drop=True)
    T["d"] = T["d"].astype(int)
    return T


def u2(tr, sym):
    sp_ = H.SPEC[sym]
    gr = tr["d"].to_numpy() * (tr["exit_px"].to_numpy() - tr["entry_px"].to_numpy()) / tr["entry_px"].to_numpy()
    return gr * PREF[sym] * sp_["usd"] - tr["cost_usd"].to_numpy()


def c1_matrix(sym, ent, R=999, k=1, chunk=100, keep_tables=200, seed_base=None):
    """C1 matched control: each trade re-placed on a random session of the same calendar year, same entry/exit
    marks, side (and stop distance). R draws in chunks of <= 100 (seed = seed_base + chunk; seed_base = 1000 k).
    Returns (M, tables): M = (n_trades x R) net $ per micro (NaN = draw dropped: no price at the mark),
    tables = list of the first `keep_tables` draws as trade tables (for the eval twins)."""
    seed_base = 1000 * k if seed_base is None else seed_base
    e = ent[["session", "entry", "exit", "d"]].copy().reset_index(drop=True)
    e["tid"] = np.arange(len(e))
    M = np.full((len(e), R), np.nan)
    tables = []
    for c in range((R + chunk - 1) // chunk):
        nrep = min(chunk, R - c * chunk)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rt = H.random_time_trades(sym, e, n_rep=nrep, seed=seed_base + c, keep_session=False, keep_marks=True,
                                      keep_side=True)
        M[rt["tid"].to_numpy(), c * chunk + rt["rep"].to_numpy()] = rt["pnl_usd"].to_numpy()
        if len(tables) < keep_tables:
            for r, g in rt.groupby("rep"):
                if len(tables) < keep_tables:
                    tables.append(g.drop(columns=["rep"]).reset_index(drop=True))
        del rt
    return M, tables


def daily(x_by_trade, sessions_, calendar_):
    s = pd.Series(np.asarray(x_by_trade, np.float64), index=pd.DatetimeIndex(sessions_).normalize())
    out = s.groupby(level=0).sum().reindex(calendar_, fill_value=0.0)
    out.index.name = "session"
    return out


def cons_p(x):
    p, ps = sp.conservative_p(sp.boot_pvalue_mean, np.asarray(x, np.float64), B=5000, seed=SEED_BOOT)
    return float(p), {int(k): float(v) for k, v in ps.items()}


def window_means(x):
    """mean per session of a daily series by window (2010-17, 2018-25H1, 2018+, 2022+, all) and NW t."""
    idx = pd.DatetimeIndex(x.index)
    out = {}
    for nm, (a, b) in {"all": ("1900", "2100"), **H.SPANS}.items():
        v = x[(idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b))].to_numpy()
        out[nm] = dict(mean=float(v.mean()), total=float(v.sum()), t_nw=float(sp.hac_t(v)[0]) if v.std() > 0 else None,
                       n=len(v))
    return out


def per_trade_windows(tr, col="pnl_usd"):
    s = pd.DatetimeIndex(tr["session"])
    out = {}
    for nm, (a, b) in {"all": ("1900", "2100"), **H.SPANS}.items():
        m = (s >= pd.Timestamp(a)) & (s <= pd.Timestamp(b))
        out[nm] = dict(n=int(m.sum()), mean=float(tr.loc[m, col].mean()) if m.any() else None)
    return out
