"""Shared helpers for builder Y, section 12 (NQ vs ES relative value).
Index conventions: 1-min RTH grid, minute index i = bar stamped 9:30 + i (ET). Bar i closes at 9:30 + i + 1.
  P(hh:mm) = close of bar (hh:mm - 1 min);  idx(14:29)=299, idx(14:30)=300, idx(15:29)=359, idx(15:30)=360,
  idx(15:59)=389, idx(12:59)=209, idx(10:00)=30, idx(14:59)=329."""
import os, pickle, math
import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = "/run/media/roflz/Disk 2/_/market_data"
SEED = 12345
NQ_PT, ES_PT, RTY_PT = 2.0, 5.0, 5.0             # micro $ per point
NQ_COST, ES_COST, RTY_COST = 2.00, 3.50, 2.00     # $ per micro round trip (1 tick each way + $1 commission)
IDX = lambda hh, mm: (hh * 60 + mm) - 570


def tm(i):
    """bar index -> 'HH:MM' of the bar stamp"""
    m = 570 + int(i)
    return f"{m // 60:02d}:{m % 60:02d}"


def load_cache(sym):
    with open(f"{HERE}/cache_{sym}.pkl", "rb") as f:
        return pickle.load(f)


class Sessions:
    """Cash sessions (both legs cash_day) with per-session arrays for NQ and ES."""

    def __init__(self):
        N, E = load_cache("NQ"), load_cache("ES")
        assert (N["days"] == E["days"]).all()
        dsN = pd.read_pickle(f"{PROJ}/data/daily_sessions_NQ.pkl")
        dsE = pd.read_pickle(f"{PROJ}/data/daily_sessions_ES.pkl")
        cash = dsN.index[dsN.cash_day & dsE.reindex(dsN.index).cash_day.fillna(False).astype(bool)]
        pos = np.searchsorted(N["days"], cash)
        assert (N["days"][pos] == cash).all()
        self.dates = pd.DatetimeIndex(cash)
        self.early = (dsN.early_close.reindex(cash).to_numpy() | dsE.early_close.reindex(cash).to_numpy())
        self.full = ~self.early
        self.n = len(cash)
        for leg, D in (("N", N), ("E", E)):
            for k in ("O", "H", "L", "C"):
                setattr(self, k + leg, D[k][pos])
            ins = D["inst"][pos]
            u = np.where(ins >= 0, ins, np.iinfo(np.int64).max).min(axis=1)   # RTH has one instrument per session
            setattr(self, "inst" + leg, u)
        # close-bar index of each session: 15:59 on full days, 12:59 on early closes
        self.cidx = np.where(self.full, 389, 209)
        # prior cash session's close (in that session's contract) and roll flag vs prior cash session
        self.pcN = np.full(self.n, np.nan); self.pcE = np.full(self.n, np.nan)
        self.roll = np.zeros(self.n, bool); self.roll[0] = True
        for t in range(1, self.n):
            self.pcN[t] = self.CN[t - 1, self.cidx[t - 1]]
            self.pcE[t] = self.CE[t - 1, self.cidx[t - 1]]
            self.roll[t] = (self.instN[t] != self.instN[t - 1]) or (self.instE[t] != self.instE[t - 1])
        self.pos_of = {d: i for i, d in enumerate(self.dates)}

    def asof_close(self, leg, t, i):
        """close of the last bar at or before index i in session t (NaN if none)"""
        C = getattr(self, "C" + leg)[t]
        j = i
        while j >= 0 and np.isnan(C[j]):
            j -= 1
        return (C[j], j) if j >= 0 else (np.nan, -1)

    def next_open(self, leg, t, i, last=389):
        """open of the first bar at or after index i in session t (fallback: none)"""
        O = getattr(self, "O" + leg)[t]
        j = i
        while j <= last and np.isnan(O[j]):
            j += 1
        return (O[j], j) if j <= last else (np.nan, -1)

    def max_gap(self, t):
        g = 0
        for leg in ("N", "E"):
            pres = np.flatnonzero(~np.isnan(getattr(self, "C" + leg)[t][: self.cidx[t] + 1]))
            if len(pres) == 0:
                return 999
            d = np.diff(np.concatenate([[0], pres, [self.cidx[t]]]))
            g = max(g, int(d.max()) if len(d) else 0, int(pres[0]))
        return g


def five_min_returns(S, t):
    """78 five-minute log returns 9:30-16:00 for both legs on full session t; NaN where a grid price is missing"""
    def grid(leg):
        O = getattr(S, "O" + leg)[t]; C = getattr(S, "C" + leg)[t]
        p = np.full(79, np.nan)
        p[0] = O[0]
        for k in range(1, 79):
            p[k] = S.asof_close(leg, t, 5 * k - 1)[0]
        return np.diff(np.log(p))
    return grid("N"), grid("E")


def hedge_betas(S, window=60):
    """b[t] = OLS slope (with intercept) of NQ 5-min log returns on ES over the prior `window` full cash sessions
    (today excluded); NaN until `window` prior full sessions exist. Defined for every cash session."""
    full_idx = np.flatnonzero(S.full)
    R = {}
    for t in full_idx:
        R[t] = five_min_returns(S, t)
    b = np.full(S.n, np.nan)
    for t in range(S.n):
        prior = full_idx[full_idx < t][-window:]
        if len(prior) < window:
            continue
        x = np.concatenate([R[p][1] for p in prior]); y = np.concatenate([R[p][0] for p in prior])
        ok = ~np.isnan(x) & ~np.isnan(y)
        x, y = x[ok], y[ok]
        xm, ym = x.mean(), y.mean()
        b[t] = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
    return b


def size_legs(k):
    """n_NQ = smallest integer 1..10 with |round(n*k) - n*k| <= 0.05*n*k; else smallest relative error.
    n_ES = max(1, round(n_NQ*k)). Rounding is half-up."""
    assert k > 0, k
    best, best_err = None, None
    for n in range(1, 11):
        x = n * k
        r = math.floor(x + 0.5)
        err = abs(r - x)
        if err <= 0.05 * x:
            return n, max(1, r)
        if best is None or err / x < best_err:
            best, best_err = n, err / x
    return best, max(1, math.floor(best * k + 0.5))


# ---------------------------------------------------------------- statistics
def tstat(x):
    x = np.asarray(x, float)
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


def nw_t(x, lags):
    x = np.asarray(x, float); n = len(x)
    if n < 3:
        return np.nan
    e = x - x.mean()
    lrv = (e @ e) / n
    for l in range(1, lags + 1):
        lrv += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / math.sqrt(lrv / n)


def p_two_sided(t, n):
    return float(2 * stats.t.sf(abs(t), df=max(n - 1, 1))) if np.isfinite(t) else 1.0


def holm(pvals):
    """Holm step-down adjusted p-values; input dict name->p"""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items); out = {}; running = 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        out[k] = running
    return out


def block_of(year):
    if year >= 2026:
        return "2026"
    s = 2010 + 2 * ((year - 2010) // 2)
    return f"{s}-{str(s + 1)[2:]}"


def summarize(df, col="net_bp", usd="net_usd", start=None, end=pd.Timestamp("2026-11-06"), min_block=10, nw_lags=5):
    """headline stats for a per-trade (or per-month) frame with a 'date' column"""
    x = df[col].to_numpy(float)
    yrs = ((end - start).days / 365.25) if start is not None else np.nan
    out = {
        "n": int(len(df)), "mean_net_bp": float(np.mean(x)) if len(x) else np.nan,
        "mean_gross_bp": float(df.gross_bp.mean()) if len(df) else np.nan,
        "mean_cost_bp": float(df.cost_bp.mean()) if len(df) else np.nan,
        "net_usd_per_trade": float(df[usd].mean()) if len(df) else np.nan,
        "total_usd": float(df[usd].sum()), "t": float(tstat(x)), f"t_nw{nw_lags}": float(nw_t(x, nw_lags)),
        "per_year": float(len(df) / yrs) if yrs == yrs else np.nan,
        "hit_rate": float((x > 0).mean()) if len(x) else np.nan,
    }
    d = pd.to_datetime(df.date)
    eras = {"2010-06..2020-05": d < "2020-06-01", "2020-06..2026-11": d >= "2020-06-01"}
    out["eras"] = {k: {"n": int(m.sum()), "mean_net_bp": float(x[m].mean()) if m.sum() else None,
                       "mean_gross_bp": float(df.gross_bp[m].mean()) if m.sum() else None,
                       "net_usd_per_trade": float(df[usd][m].mean()) if m.sum() else None,
                       "total_usd": float(df[usd][m].sum()), "t": float(tstat(x[m])) if m.sum() > 1 else None}
                   for k, m in eras.items()}
    blk = d.dt.year.map(block_of)
    out["blocks"] = {}
    for bname in sorted(blk.unique()):
        m = (blk == bname).to_numpy()
        out["blocks"][bname] = {"n": int(m.sum()), "mean_net_bp": float(x[m].mean()),
                                "net_usd_per_trade": float(df[usd][m].mean()), "total_usd": float(df[usd][m].sum()),
                                "t": float(tstat(x[m])) if m.sum() > 1 else None, "counted": bool(m.sum() >= min_block)}
    cb = [v for v in out["blocks"].values() if v["counted"]]
    out["blocks_counted"] = len(cb)
    out["blocks_positive"] = int(sum(v["mean_net_bp"] > 0 for v in cb))
    yr = d.dt.year
    out["by_year"] = {int(y): {"n": int((yr == y).sum()), "mean_net_bp": float(x[(yr == y).to_numpy()].mean()),
                               "total_usd": float(df[usd][(yr == y).to_numpy()].sum())} for y in sorted(yr.unique())}
    return out


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, pd.Timestamp):
        return o.strftime("%Y-%m-%d")
    return o


# ---------------------------------------------------------------- intraday two-leg simulator
def simulate_intraday(S, t, dec_idx, entry_idx, exit_idx, nq_dir, b, stop=None):
    """Bar-by-bar state machine for one two-leg day trade.
    dec_idx : bar whose CLOSE is the decision price (P(T) = close of bar T-1); entry at the OPEN of entry_idx.
    nq_dir  : +1 long MNQ / short MES, -1 short MNQ / long MES.
    stop    : None, or dict(o9N, o9E, s, z_entry) -> disaster stop on each 1-min close from entry_idx to exit_idx-1:
              z_t (same O(9:30), b, s) with the entry sign and |z_t| >= |z_entry| + 2 -> exit both legs at the next
              bar's open. Otherwise exit at the close of bar exit_idx.
    Returns dict with raw prices (no slippage); costs are charged separately (they include the 1-tick fills)."""
    assert dec_idx < entry_idx, "decision bar must have closed before the entry bar opens"
    pN, pE = S.CN[t, dec_idx], S.CE[t, dec_idx]
    k = b * (NQ_PT * pN) / (ES_PT * pE)
    n_nq, n_es = size_legs(k)
    state = "FLAT"
    rec = {}
    i = entry_idx
    while True:
        if state == "FLAT":
            eN, jN = S.next_open("N", t, entry_idx, exit_idx)
            eE, jE = S.next_open("E", t, entry_idx, exit_idx)
            rec.update(entry_bar_N=tm(jN), entry_bar_E=tm(jE), eN=eN, eE=eE)
            state = "LONG_SPREAD" if nq_dir > 0 else "SHORT_SPREAD"
            i = max(jN, jE)
            continue
        # in position: process the close of bar i
        if i >= exit_idx:
            xN, xE = S.CN[t, exit_idx], S.CE[t, exit_idx]
            if not (np.isfinite(xN) and np.isfinite(xE)):
                xN = S.asof_close("N", t, exit_idx)[0]; xE = S.asof_close("E", t, exit_idx)[0]
            rec.update(exit_bar_N=tm(exit_idx), exit_bar_E=tm(exit_idx), xN=xN, xE=xE, exit_reason="close",
                       exit_kind="close_of_bar")
            break
        if stop is not None:
            cN = S.asof_close("N", t, i)[0]; cE = S.asof_close("E", t, i)[0]
            zt = (np.log(cN / stop["o9N"]) - b * np.log(cE / stop["o9E"])) / stop["s"]
            ze = stop["z_entry"]
            if np.sign(zt) == np.sign(ze) and abs(zt) >= abs(ze) + 2.0:
                xN, jN = S.next_open("N", t, i + 1, exit_idx)
                xE, jE = S.next_open("E", t, i + 1, exit_idx)
                rec.update(exit_bar_N=tm(jN), exit_bar_E=tm(jE), xN=xN, xE=xE, exit_reason="stop",
                           exit_kind="open_of_bar", stop_signal_bar=tm(i), z_at_stop=zt)
                break
        i += 1
    # instruments at entry and exit must match the session's single RTH contract (no roll inside a trade)
    gross = n_nq * NQ_PT * nq_dir * (rec["xN"] - rec["eN"]) - n_es * ES_PT * nq_dir * (rec["xE"] - rec["eE"])
    gross_long = n_nq * NQ_PT * (rec["xN"] - rec["eN"]) - n_es * ES_PT * (rec["xE"] - rec["eE"])
    cost = n_nq * NQ_COST + n_es * ES_COST
    notional = n_nq * NQ_PT * rec["eN"]
    rec.update(k=k, n_nq=n_nq, n_es=n_es, nq_dir=nq_dir,
               side="long_NQ_short_ES" if nq_dir > 0 else "short_NQ_long_ES",
               nq_entry_fill=rec["eN"] + 0.25 * nq_dir, nq_exit_fill=rec["xN"] - 0.25 * nq_dir,
               es_entry_fill=rec["eE"] - 0.25 * nq_dir, es_exit_fill=rec["xE"] + 0.25 * nq_dir,
               gross_usd=gross, cost_usd=cost, net_usd=gross - cost, gross_long_usd=gross_long,
               notional_usd=notional, gross_bp=1e4 * gross / notional, cost_bp=1e4 * cost / notional,
               net_bp=1e4 * (gross - cost) / notional,
               gross_pts_nq_equiv=gross / (NQ_PT * n_nq), net_pts_nq_equiv=(gross - cost) / (NQ_PT * n_nq),
               inst_N=int(S.instN[t]), inst_E=int(S.instE[t]))
    return rec


def coin_control(df, draws=1000, seed=SEED):
    """C1: same days, bars and sizes with a fair-coin direction. Returns array of mean net bp per draw."""
    rng = np.random.default_rng(seed)
    G = df.gross_long_usd.to_numpy() / df.notional_usd.to_numpy() * 1e4
    c = df.cost_bp.to_numpy()
    D = rng.choice(np.array([-1.0, 1.0]), size=(draws, len(df)))
    return (D * G - c).mean(axis=1)
