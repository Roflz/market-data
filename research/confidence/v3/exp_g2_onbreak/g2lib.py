"""
v3/exp_g2_onbreak/g2lib.py - G2 (overnight-range break with trend, family F3): signal, 5-minute walker, C1 control.

Frozen rules: v3/PREREG.md section 1 A2 and section 2 G2 (sha256 c9aef662...). Light: reads v3/data only.

Conventions (identical to harness.time_trades, but the entry may be at any 5-minute bar start, not only a mark):
  entry price  = O of the 5-minute bar starting at the entry time (== px_HHMM at 15-minute marks, checked)
  stop         = entry_px - d * stop_pts, walked on the 5-minute bars starting in [entry time, exit time):
                 long: L <= stop -> fill min(O, stop) - 1 tick (short mirror); t_exit = that bar's end
  time exit    = px at the exit mark (sessions table); market closed before the mark -> px_1645 (kind 'close')
  costs        = harness SPEC cost ($1 + 1 tick each way) + extra_ticks (each way) for the cost stress
Slots: 5-minute slot j of a session = bar start at 18:00 + 5j minutes (j = 0 .. 272; 186 = 09:30, 264 = 16:00).
"""
import os

import numpy as np
import pandas as pd

import harness as H

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LAST_SESSION = pd.Timestamp("2025-06-27")             # calendar end (2025-06-30 dropped, see PREREG 0.1)
N_SLOTS = 273
P_REF = {"NQ": 20789.6, "ES": 5843.2, "YM": 42516.3}
_C = {}


def slot_of_hhmm(hhmm):
    h, m = int(hhmm[:2]), int(hhmm[2:])
    mins = (h * 60 + m - 18 * 60) % (24 * 60)
    return mins // 5


def data(sym):
    """(S, b, M): sessions table, 5-minute bars, M[session row, slot] = bar row (-1 = no bar)."""
    if sym not in _C:
        S = H.sessions(sym)
        b = H.bars(sym, 5)
        si = S.index.get_indexer(pd.DatetimeIndex(b["session"]))
        off = ((b.index - (pd.DatetimeIndex(b["session"]) - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1))
        off = np.asarray(off, np.int64)
        assert (si >= 0).all() and (off % 5 == 0).all() and off.max() < 1365
        M = np.full((len(S), N_SLOTS), -1, np.int64)
        M[si, off // 5] = np.arange(len(b))
        arr = dict(O=b.O.to_numpy(np.float64), H=b.H.to_numpy(np.float64), L=b.L.to_numpy(np.float64),
                   C=b.C.to_numpy(np.float64), atr=b.atr14.to_numpy(np.float64))
        PX = S[[f"px_{m}" for m in H.MARKS]].to_numpy(np.float64)
        _C[sym] = (S, b, M, arr, PX, S["last_t"].to_numpy(np.int64), S.index.year.to_numpy())
    return _C[sym]


def fomc_blackout():
    """{session date: (start offset, end offset)} in minutes from 18:00: [statement - 30, statement + 15],
    scheduled meetings only (known in advance; a fixed calendar, never a price)."""
    f = pd.read_csv(os.path.join(R, "data", "fomc_dates.csv"))
    f = f[f["scheduled"].astype(str).str.lower() == "true"]
    out = {}
    for dt, tm in zip(f["date"], f["statement_time_et"]):
        h, m = map(int, str(tm).split(":"))
        o = h * 60 + m + 6 * 60                                 # offset from 18:00 of the previous evening
        out[pd.Timestamp(dt)] = (o - 30, o + 15)
    return out


# ============================================================================================ walker
def walk(sym, si, slot, kx, d, stop_pts, target_pts=None, extra_ticks=0, need_bar=True):
    """Vectorised trade walker. si: session rows, slot: entry slots, kx: exit marks (0..91), d: +1/-1,
    stop_pts: points from entry (NaN = no stop). Returns dict of arrays (entry_px, exit_px, kind 0 time /1 stop /
    2 target /3 close, exit_off minutes from 18:00, ok, pnl_pts, gross, cost, net)."""
    S, b, M, A, PX, last_t, _ = data(sym)
    sp = H.SPEC[sym]
    tick, usd = sp["tick"], sp["usd"]
    cost = sp["cost"] + 2 * extra_ticks * tick * usd
    si = np.asarray(si, np.int64); slot = np.asarray(slot, np.int64); kx = np.asarray(kx, np.int64)
    d = np.asarray(d, np.int64); stop_pts = np.asarray(stop_pts, np.float64)
    tg = np.full(len(si), np.nan) if target_pts is None else np.asarray(target_pts, np.float64)
    n = len(si)
    ent_bar = M[si, slot]
    exit_slot = 3 * kx                                          # bars starting before the exit mark
    ok = (ent_bar >= 0) & (slot < exit_slot)
    epx = np.full(n, np.nan)
    epx[ok] = A["O"][ent_bar[ok]]
    xpx = PX[si, kx].copy()
    kind = np.zeros(n, np.int8)
    xoff = 15 * kx.astype(np.float64)
    closed = ~np.isfinite(xpx) | (15 * kx > last_t[si] + 15)
    xpx[closed] = PX[si[closed], 91]
    xoff[closed] = np.minimum(last_t[si[closed]] + 1, 15 * kx[closed])
    kind[closed] = 3
    stop = epx - d * stop_pts
    tgt = epx + d * tg
    act = np.flatnonzero(ok & (np.isfinite(stop_pts) | np.isfinite(tg)))
    j = slot[act].copy()
    while len(act):
        live = j < exit_slot[act]
        act, j = act[live], j[live]
        if not len(act):
            break
        bi = M[si[act], j]
        has = bi >= 0
        a2, b2 = act[has], bi[has]
        if len(a2):
            dd = d[a2]
            s_ = stop[a2]; g_ = tgt[a2]
            Lo, Hi, Op = A["L"][b2], A["H"][b2], A["O"][b2]
            hs = np.where(dd > 0, Lo <= s_, Hi >= s_)
            sfill = np.where(dd > 0, np.minimum(Op, s_) - tick, np.maximum(Op, s_) + tick)
            ht = ~hs & np.where(dd > 0, Hi >= g_ + tick, Lo <= g_ - tick)
            done = hs | ht
            if done.any():
                ww = a2[done]
                xpx[ww] = np.where(hs[done], sfill[done], g_[done])
                kind[ww] = np.where(hs[done], 1, 2)
                xoff[ww] = np.minimum(5 * (j[has][done] + 1), 15 * kx[ww])
                keep = np.ones(len(act), bool)
                keep[np.flatnonzero(has)[done]] = False
                act, j = act[keep], j[keep]
        j = j + 1
    pnl_pts = d * (xpx - epx)
    gross = pnl_pts * usd
    return dict(ok=ok & np.isfinite(epx) & np.isfinite(xpx), entry_px=epx, exit_px=xpx, kind=kind, exit_off=xoff,
                pnl_pts=pnl_pts, gross=gross, cost=np.full(n, cost), net=gross - cost)


def to_frame(sym, si, slot, kx, d, stop_pts, w, extra=None):
    S = data(sym)[0]
    sess = S.index[si]
    base = sess - pd.Timedelta(hours=6)
    out = pd.DataFrame({"market": sym, "session": sess,
                        "t_entry": base + pd.to_timedelta(5 * np.asarray(slot), unit="min"),
                        "t_exit": base + pd.to_timedelta(w["exit_off"], unit="min"),
                        "d": np.asarray(d, np.int8),
                        "entry": [f"{((18 * 60 + 5 * s) // 60) % 24:02d}{(5 * s) % 60:02d}" for s in slot],
                        "exit": np.array(H.MARKS)[np.asarray(kx)],
                        "entry_px": w["entry_px"], "exit_px": w["exit_px"],
                        "exit_kind": np.array(["time", "stop", "target", "close"])[w["kind"]],
                        "stop_pts": np.asarray(stop_pts, np.float64), "target_pts": np.nan,
                        "risk_usd": np.asarray(stop_pts, np.float64) * H.SPEC[sym]["usd"],
                        "pnl_pts": w["pnl_pts"], "gross_usd": w["gross"], "cost_usd": w["cost"],
                        "pnl_usd": w["net"]})
    if extra is not None:
        for k, v in extra.items():
            out[k] = v
    return out


# ============================================================================================ signal (A2 family)
def trend_inputs(S):
    """per session: I_prev (chained index through d-1), ema_prev (EMA20 of I through d-1), I_prev6 (index through
    d-6, for the 5-session-return neighbour), C_prev (prev_close_1600, else prev_last_px). Uses only earlier rows."""
    r = S["ret_cc"].where(S["ret_cc"].notna(), S["ret_oc"]).fillna(0.0).to_numpy(np.float64)
    I = np.cumprod(1.0 + r)
    ema = pd.Series(I).ewm(span=20, adjust=False).mean().to_numpy()
    I_prev = np.r_[np.nan, I[:-1]]
    ema_prev = np.r_[np.nan, ema[:-1]]
    I_prev6 = np.r_[np.full(6, np.nan), I[:-6]] if len(I) > 6 else np.full(len(I), np.nan)
    C_prev = S["prev_close_1600"].where(S["prev_close_1600"].notna(), S["prev_last_px"]).to_numpy(np.float64)
    return I_prev, ema_prev, I_prev6, C_prev


def onbreak_candidates(S, b, last_end=1260, trend_kind="ema20", stop_mult=2.0, blackout=None, skip=None, trend_mode="with"):
    """All candidate signals (first close beyond the overnight range per side), with their trend filter applied.
    S, b: (possibly truncated) sessions table and 5-minute bars. Returns DataFrame: session, side, sig_end (offset
    minutes from 18:00 of the signal bar END), atr, stop_pts, P, trend. Uses only bars that ended by sig_end, earlier
    sessions' returns, and the prev_* columns."""
    blackout = fomc_blackout() if blackout is None else blackout
    sess = pd.DatetimeIndex(b["session"])
    off = np.asarray((b.index - (sess - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1), np.int64)
    on = off < 930
    g = pd.DataFrame({"session": sess[on], "H": b["H"].to_numpy()[on], "L": b["L"].to_numpy()[on]}).groupby("session")
    onh, onl = g["H"].max(), g["L"].min()
    rth = ~on
    R_ = pd.DataFrame({"session": sess[rth], "end": off[rth] + 5, "C": b["C"].to_numpy()[rth],
                       "atr": b["atr14"].to_numpy()[rth]})
    R_["onh"] = onh.reindex(R_["session"]).to_numpy()
    R_["onl"] = onl.reindex(R_["session"]).to_numpy()
    I_prev, ema_prev, I_prev6, C_prev = trend_inputs(S)
    T = pd.DataFrame({"I_prev": I_prev, "ema_prev": ema_prev, "I_prev6": I_prev6, "C_prev": C_prev}, index=S.index)
    rows = []
    for side, cond in ((1, R_["C"] > R_["onh"]), (-1, R_["C"] < R_["onl"])):
        f = R_[cond].groupby("session", sort=True).head(1).copy()     # FIRST break bar per session (bars in order)
        f["side"] = side
        rows.append(f)
    c = pd.concat(rows).sort_values(["session", "end"]).reset_index(drop=True)
    c = c.join(T, on="session")
    if trend_kind == "ema20":
        c["trend"] = np.sign(c["I_prev"] * c["C"] / c["C_prev"] - c["ema_prev"])
    elif trend_kind == "ret5":
        c["trend"] = np.sign(c["I_prev"] * c["C"] / c["C_prev"] - c["I_prev6"])
    else:
        raise ValueError(trend_kind)
    c["stop_pts"] = stop_mult * c["atr"]
    bo = np.array([blackout[s][0] <= e <= blackout[s][1] if s in blackout else False
                   for s, e in zip(c["session"], c["end"])], bool)
    tf = {"with": c["trend"] == c["side"], "none": np.isfinite(c["trend"]), "against": c["trend"] == -c["side"]}[trend_mode]
    keep = (c["end"] >= 935) & (c["end"] <= last_end) & tf & ~bo     # trend_mode 'none'/'against': EXPLORATORY only
    keep &= np.isfinite(c["C_prev"]) & np.isfinite(c["stop_pts"]) & (c["stop_pts"] > 0)
    if skip is not None:
        keep &= ~c["session"].isin(skip)
    c["blackout"] = bo
    return c[keep].rename(columns={"C": "P", "end": "sig_end"})[
        ["session", "side", "sig_end", "P", "atr", "stop_pts", "trend"]].reset_index(drop=True)


def onbreak_trades(sym, kx=91, extra_ticks=0, cand=None, **kw):
    """A2-type trades: candidates -> entry at the next 5-minute bar of the session -> walker; one position at a time
    (the second side's signal is taken only if its entry time >= the first trade's exit time)."""
    S, b, M, A, PX, last_t, _ = data(sym)
    c = onbreak_candidates(S, b, **kw) if cand is None else cand
    c = c[c["session"] <= LAST_SESSION].reset_index(drop=True)
    si = S.index.get_indexer(c["session"])
    sslot = c["sig_end"].to_numpy(np.int64) // 5                   # slot right after the signal bar
    # next existing bar of the session at or after that slot (normally the very next 5-minute bar)
    eslot = np.full(len(c), -1, np.int64)
    for i, (r_, s0) in enumerate(zip(si, sslot)):
        row = M[r_, s0:3 * kx]
        nz = np.flatnonzero(row >= 0)
        if len(nz):
            eslot[i] = s0 + nz[0]
    c["si"], c["eslot"] = si, eslot
    c = c[c["eslot"] >= 0].reset_index(drop=True)
    c["order"] = c.groupby("session").cumcount()
    first = c[c["order"] == 0]
    sec = c[c["order"] == 1]
    kxa = np.full(len(first), kx)
    w1 = walk(sym, first.si, first.eslot, kxa, first.side, first.stop_pts, extra_ticks=extra_ticks)
    f1 = to_frame(sym, first.si.to_numpy(), first.eslot.to_numpy(), kxa, first.side.to_numpy(),
                  first.stop_pts.to_numpy(), w1, extra=dict(sig_end=first.sig_end.to_numpy(), atr=first.atr.to_numpy(),
                                                             P=first.P.to_numpy(), seq=0))
    f1 = f1[w1["ok"]]
    ex1 = pd.Series(w1["exit_off"], index=first["session"].to_numpy())[w1["ok"]]
    if len(sec):
        sec = sec[sec["session"].isin(ex1.index)]
        sec = sec[5 * sec["eslot"].to_numpy() >= ex1.reindex(sec["session"]).to_numpy()]
    if len(sec):
        kxb = np.full(len(sec), kx)
        w2 = walk(sym, sec.si, sec.eslot, kxb, sec.side, sec.stop_pts, extra_ticks=extra_ticks)
        f2 = to_frame(sym, sec.si.to_numpy(), sec.eslot.to_numpy(), kxb, sec.side.to_numpy(),
                      sec.stop_pts.to_numpy(), w2, extra=dict(sig_end=sec.sig_end.to_numpy(), atr=sec.atr.to_numpy(),
                                                               P=sec.P.to_numpy(), seq=1))
        f1 = pd.concat([f1, f2[w2["ok"]]])
    tr = f1.sort_values(["session", "t_entry"]).reset_index(drop=True)
    tr["slot"] = ((tr["t_entry"] - (tr["session"] - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=5)).astype(int)
    tr["kx"] = kx
    tr["tid"] = np.arange(len(tr))
    return tr


def orb_trades(sym, kx=88, extra_ticks=0):
    """S2.5/S2.6: 5-minute opening-range breakout. side = sign(C - O) of the 09:30 bar; enter at the 09:35 bar open;
    stop at the other end of the 09:30 bar (distance from the entry, may be <= 0 -> stopped at once); exit 16:00."""
    S, b, M, A, PX, last_t, _ = data(sym)
    keep = S.index <= LAST_SESSION
    si = np.flatnonzero(keep)
    b0 = M[si, 186]; b1 = M[si, 187]
    ok = (b0 >= 0) & (b1 >= 0)
    si, b0, b1 = si[ok], b0[ok], b1[ok]
    side = np.sign(A["C"][b0] - A["O"][b0]).astype(np.int64)
    nz = side != 0
    si, b0, b1, side = si[nz], b0[nz], b1[nz], side[nz]
    entry = A["O"][b1]
    stop_px = np.where(side > 0, A["L"][b0], A["H"][b0])
    stop_pts = side * (entry - stop_px)
    slot = np.full(len(si), 187)
    kxa = np.full(len(si), kx)
    w = walk(sym, si, slot, kxa, side, stop_pts, extra_ticks=extra_ticks)
    tr = to_frame(sym, si, slot, kxa, side, stop_pts, w)[w["ok"]].reset_index(drop=True)
    tr["slot"] = 187
    tr["kx"] = kx
    tr["tid"] = np.arange(len(tr))
    return tr


# ============================================================================================ controls
def sessions_by_year(sym):
    S = data(sym)[0]
    rows = np.flatnonzero(S.index <= LAST_SESSION)
    yrs = S.index.year.to_numpy()[rows]
    return {y: rows[yrs == y] for y in np.unique(yrs)}


def c1_draws(sym, tr, R=999, k=2, chunk=100, side_mode="same", keep_twins=0, extra_ticks=0):
    """Matched control C1: each trade re-placed on a random session of the same calendar year, same entry slot, exit
    mark, side and stop points (side_mode 'long' = hour drift; 'random' with same_session=True would be C2).
    Seeds 1000*k + chunk. Returns dict(c_mean per trade (NaN if no valid draw), n_valid per trade, strat_total[R]
    = total net of each random strategy, twins = list of trade frames for the first keep_twins reps)."""
    byy = sessions_by_year(sym)
    yrs = pd.DatetimeIndex(tr["session"]).year.to_numpy()
    slot = tr["slot"].to_numpy(np.int64); kx = tr["kx"].to_numpy(np.int64)
    d = tr["d"].to_numpy(np.int64); sp = tr["stop_pts"].to_numpy(np.float64)
    n = len(tr)
    ssum = np.zeros(n); scnt = np.zeros(n)
    strat = np.zeros(R)
    twins = []
    for ci, r0 in enumerate(range(0, R, chunk)):
        nr = min(chunk, R - r0)
        rng = np.random.default_rng(1000 * k + ci)
        si = np.empty((nr, n), np.int64)
        for y in np.unique(yrs):
            m = yrs == y
            pool = byy[y]
            si[:, m] = pool[rng.integers(0, len(pool), size=(nr, m.sum()))]
        dd = np.tile(d, nr)
        if side_mode == "long":
            dd = np.ones_like(dd)
        w = walk(sym, si.ravel(), np.tile(slot, nr), np.tile(kx, nr), dd, np.tile(sp, nr), extra_ticks=extra_ticks)
        net = np.where(w["ok"], w["net"], np.nan).reshape(nr, n)
        v = np.isfinite(net)
        ssum += np.where(v, net, 0).sum(0); scnt += v.sum(0)
        strat[r0:r0 + nr] = np.where(v, net, 0).sum(1)
        for rr in range(nr):
            if len(twins) < keep_twins:
                ii = slice(rr * n, (rr + 1) * n)
                wsub = {kk: vv[ii] for kk, vv in w.items()}
                f = to_frame(sym, si[rr], slot, kx, dd[ii], sp, wsub)
                twins.append(f[wsub["ok"]].reset_index(drop=True))
    c = np.where(scnt > 0, ssum / np.maximum(scnt, 1), np.nan)
    return dict(c_mean=c, n_valid=scnt, strat_total=strat, twins=twins)


def same_session_controls(sym, tr, n_rep=100, seed=7, mode="random_side", slot_range=None):
    """C2 random side (same session, slot, stop) or random entry slot in slot_range on the same session (same side,
    stop, exit). Returns per-rep mean net per trade (array n_rep) and per-trade mean."""
    S = data(sym)[0]
    si = S.index.get_indexer(pd.DatetimeIndex(tr["session"]))
    slot = tr["slot"].to_numpy(np.int64); kx = tr["kx"].to_numpy(np.int64)
    d = tr["d"].to_numpy(np.int64); sp = tr["stop_pts"].to_numpy(np.float64)
    n = len(tr)
    rng = np.random.default_rng(seed)
    per_rep = np.zeros(n_rep); ssum = np.zeros(n); scnt = np.zeros(n)
    for r in range(n_rep):
        dd, sl = d, slot
        if mode == "random_side":
            dd = rng.choice(np.array([-1, 1]), size=n)
        elif mode == "random_slot":
            sl = rng.integers(slot_range[0], slot_range[1] + 1, size=n)
        w = walk(sym, si, sl, kx, dd, sp)
        net = np.where(w["ok"], w["net"], np.nan)
        per_rep[r] = np.nanmean(net)
        v = np.isfinite(net)
        ssum += np.where(v, net, 0); scnt += v
    return per_rep, ssum / np.maximum(scnt, 1)


def drift_paired(sym, tr):
    """plain drift: long at the same session, slot, stop and exit (paired)."""
    S = data(sym)[0]
    si = S.index.get_indexer(pd.DatetimeIndex(tr["session"]))
    w = walk(sym, si, tr["slot"].to_numpy(), tr["kx"].to_numpy(), np.ones(len(tr), np.int64),
             tr["stop_pts"].to_numpy())
    return np.where(w["ok"], w["net"], np.nan)


def u2(tr):
    sym = tr["market"].iloc[0]
    gr = tr["d"] * (tr["exit_px"] - tr["entry_px"]) / tr["entry_px"]
    return gr * P_REF[sym] * H.SPEC[sym]["usd"] - tr["cost_usd"]
