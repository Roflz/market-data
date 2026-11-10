"""Shared helpers for section 12 (builder X)."""
import numpy as np
import pandas as pd
from scipy import stats as sst

SEED = 12345
NREP = 1000


def tstat(x):
    x = np.asarray(x, float)
    n = len(x)
    if n < 2:
        return np.nan
    sd = x.std(ddof=1)
    return x.mean() / (sd / np.sqrt(n)) if sd > 0 else np.nan


def nw_t(x, lags):
    """Newey-West (Bartlett) t of the mean."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return np.nan
    u = x - x.mean()
    s = (u @ u) / n
    for L in range(1, lags + 1):
        if L >= n:
            break
        w = 1 - L / (lags + 1)
        s += 2 * w * (u[L:] @ u[:-L]) / n
    se = np.sqrt(s / n)
    return x.mean() / se if se > 0 else np.nan


def p_two(t, n):
    if not np.isfinite(t) or n < 2:
        return 1.0
    return float(2 * sst.t.sf(abs(t), n - 1))


def holm(pvals):
    """Holm step-down adjusted p-values (dict name->p)."""
    names = list(pvals)
    p = np.array([pvals[k] for k in names])
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i]))
        adj[i] = run
    return {names[i]: float(adj[i]) for i in range(m)}


def block_label(year):
    if year >= 2026:
        return "2026"
    a = year - (year % 2)
    return f"{a}-{str(a + 1)[2:]}"


def summarize(df, col="net_bp", min_block=10):
    """Basic stats on a per-trade (or per-month) frame with columns date, net_bp, gross_bp, cost_bp, net_usd."""
    x = df[col].to_numpy()
    yrs = (df.date.max() - df.date.min()).days / 365.25 if len(df) > 1 else np.nan
    out = {
        "n": int(len(df)),
        "mean_net_bp": float(np.mean(x)) if len(x) else np.nan,
        "mean_gross_bp": float(df.gross_bp.mean()) if len(x) else np.nan,
        "mean_cost_bp": float(df.cost_bp.mean()) if len(x) else np.nan,
        "net_usd_per_trade": float(df.net_usd.mean()) if len(x) else np.nan,
        "total_usd": float(df.net_usd.sum()),
        "t": float(tstat(x)),
        "per_year": float(len(df) / yrs) if yrs and yrs > 0 else np.nan,
        "win_rate": float((x > 0).mean()) if len(x) else np.nan,
    }
    blk = df.assign(block=df.date.dt.year.map(block_label)).groupby("block")
    out["blocks"] = {k: {"n": int(len(g)), "mean_net_bp": float(g[col].mean()), "usd": float(g.net_usd.sum()),
                         "counted": bool(len(g) >= min_block)} for k, g in blk}
    out["by_year"] = {int(k): {"n": int(len(g)), "mean_net_bp": float(g[col].mean()), "mean_gross_bp": float(g.gross_bp.mean()),
                               "usd": float(g.net_usd.sum())} for k, g in df.groupby(df.date.dt.year)}
    return out


def era_stats(df, col="net_bp", split="2020-06-01"):
    a = df[df.date < split]
    b = df[df.date >= split]
    f = lambda g: {"n": int(len(g)), "mean_net_bp": float(g[col].mean()) if len(g) else np.nan,
                   "mean_gross_bp": float(g.gross_bp.mean()) if len(g) else np.nan,
                   "net_usd_per_trade": float(g.net_usd.mean()) if len(g) else np.nan,
                   "total_usd": float(g.net_usd.sum()), "t": float(tstat(g[col])) if len(g) > 1 else np.nan}
    return {"before": f(a), "after": f(b)}


def size_legs(k, nmax=10, tol=0.05):
    """Vectorized integer sizing: smallest n in 1..nmax with |round(n k) - n k| <= tol n k, else min relative error.
    round = half-up (floor(x+0.5)). Returns n_lead, n_es."""
    k = np.asarray(k, float)
    ns = np.arange(1, nmax + 1)[None, :]
    nk = ns * k[:, None]
    r = np.floor(nk + 0.5)
    rel = np.abs(r - nk) / nk
    ok = rel <= tol
    first_ok = np.where(ok.any(1), ok.argmax(1), rel.argmin(1))
    n_lead = first_ok + 1
    n_es = np.maximum(1, np.floor(n_lead * k + 0.5)).astype(int)
    return n_lead.astype(int), n_es
