"""Skeptic re-run of event-continuation headline numbers (independent code)."""
import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from grid import grid, pevent, biggap_cum, ROOT

ds = pd.read_pickle(f"{ROOT}/data/daily_sessions_NQ.pkl")
cash = np.array(sorted(pd.to_datetime(ds.index[ds.cash_day]).normalize().to_numpy().astype("datetime64[D]")))
cpi = set(pd.to_datetime(pd.read_csv(f"{ROOT}/data/cpi_dates.csv").date).to_numpy().astype("datetime64[D]"))
MULT = {"NQ": 2.0, "ES": 5.0}
COST = {"NQ": 2.0, "ES": 3.5}
_cache = {}


def G_(sym):
    if sym not in _cache:
        G = grid(sym)
        G["bgc"] = biggap_cum(G)
        _cache[sym] = G
    return _cache[sym]


def nw_t(x, y, L=5):
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    u = X * e[:, None]
    S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        g = u[l:].T @ u[:-l]
        S += w * (g + g.T)
    V = XtX_inv @ S @ XtX_inv
    return b[1], b[1] / np.sqrt(V[1, 1])


def event(sym, t0, k, h, days=None, prior_session=False):
    """t0 = ET minute of day; session date = ET date (or ET date + 1 when t0 >= 18:00)."""
    G = G_(sym)
    gi = np.flatnonzero(G["et_min"] == t0)
    sess = G["sess"][gi]
    sel = np.isin(sess, cash if days is None else np.array(sorted(days)))
    gi, sess = gi[sel], sess[sel]
    p0, i0, l0 = pevent(G, gi)
    p1, i1, l1 = pevent(G, gi + k)
    p2, i2, l2 = pevent(G, gi + k + h)
    ok = ~np.isnan(p0) & ~np.isnan(p1) & ~np.isnan(p2) & (i0 == i1) & (i1 == i2)
    lo = np.clip(np.minimum(l0, gi), 0, None)
    ok &= (G["bgc"][np.clip(l2, 0, None)] - G["bgc"][lo]) == 0
    df = pd.DataFrame({"sess": sess, "p0": p0, "p1": p1, "p2": p2})[ok]
    df["imp"] = np.log(df.p1 / df.p0)
    df["fol"] = np.log(df.p2 / df.p1)
    df["fol_pts"] = df.p2 - df.p1
    df["yr"] = pd.DatetimeIndex(df.sess).year
    return df


def report(name, sym, t0, k, h, days=None):
    df = event(sym, t0, k, h, days)
    out = {"name": name, "sym": sym, "n": len(df)}
    b, t = nw_t(df.imp.to_numpy(), df.fol.to_numpy())
    out.update(slope=round(b, 4), t=round(t, 2))
    for lab, sub in (("10-17", df[df.yr <= 2017]), ("18-26", df[df.yr >= 2018])):
        b2, t2 = nw_t(sub.imp.to_numpy(), sub.fol.to_numpy())
        out[f"t_{lab}"] = round(t2, 2)
    tr = df[df.imp != 0]
    gross = np.sign(tr.imp) * tr.fol_pts * MULT[sym]
    out["follow_net"] = round(gross.mean() - COST[sym], 2)
    out["fade_net"] = round(-gross.mean() - COST[sym], 2)
    out["follow_net_10-17"] = round(gross[tr.yr <= 2017].mean() - COST[sym], 2)
    out["follow_net_18-26"] = round(gross[tr.yr >= 2018].mean() - COST[sym], 2)
    out["fade_net_10-17"] = round(-gross[tr.yr <= 2017].mean() - COST[sym], 2)
    out["fade_net_18-26"] = round(-gross[tr.yr >= 2018].mean() - COST[sym], 2)
    # t of the follow-rule gross P&L (simple, iid)
    out["t_follow_gross"] = round(gross.mean() / (gross.std() / np.sqrt(len(gross))), 2)
    print(out, flush=True)
    return df


if __name__ == "__main__":
    H = lambda h, m: h * 60 + m
    # E1: NQ cash open best-of-9 k5/h120, and ES; pre-specified k15/h60
    report("cash open k5 h120", "NQ", H(9, 30), 5, 120)
    report("cash open k5 h120", "ES", H(9, 30), 5, 120)
    report("cash open k15 h60", "NQ", H(9, 30), 15, 60)
    report("cash open k15 h60", "ES", H(9, 30), 15, 60)
    # E2: 08:00 ET (06:00 Denver)
    report("08:00 k30 h60", "ES", H(8, 0), 30, 60)
    report("08:00 k30 h60", "NQ", H(8, 0), 30, 60)
    report("08:00 k15 h60", "NQ", H(8, 0), 15, 60)
    report("08:00 k15 h60", "ES", H(8, 0), 15, 60)
    # E3: CPI
    report("CPI 08:30 k15 h60", "NQ", H(8, 30), 15, 60, days=cpi)
    report("CPI 08:30 k15 h60", "ES", H(8, 30), 15, 60, days=cpi)
    # E4: Globex reopen ES k15/h60 (session = next ET date)
    report("reopen 18:00 k15 h60", "ES", H(18, 0), 15, 60)
    report("reopen 18:00 k15 h60", "NQ", H(18, 0), 15, 60)
