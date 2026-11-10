"""Independent minute grid for the skeptic checks (does not reuse the map/events code).
grid(sym) -> dict with per-grid-minute arrays:
  C (close of bar at minute, NaN if none), O (open), I (instrument id, -1 if none),
  L (index of last bar at or before minute), et_date (ET calendar date as int yyyymmdd), et_min (ET minute of day),
  sess (session date as datetime64[D]: ET date, +1 day for times >= 18:00)
"""
import os
import numpy as np
import pandas as pd

ROOT = "/run/media/roflz/Disk 2/_/market_data"
OUT = os.path.dirname(os.path.abspath(__file__))


def grid(sym):
    cache = f"{OUT}/grid_{sym}.npz"
    if os.path.exists(cache):
        z = np.load(cache, allow_pickle=False)
        return {k: z[k] for k in z.files}
    d = pd.read_csv(f"{ROOT}/data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "instrument_id"],
                    engine="pyarrow")
    t = pd.to_datetime(d.ts_event, utc=True)
    m = (t.dt.as_unit("s").astype("int64") // 60).to_numpy()
    o = np.argsort(m, kind="stable")
    m = m[o]
    keep = np.r_[True, np.diff(m) > 0]
    m = m[keep]
    C0 = d.Close.to_numpy(float)[o][keep]
    O0 = d.Open.to_numpy(float)[o][keep]
    I0 = d.instrument_id.to_numpy()[o][keep]
    m0 = m[0]
    n = m[-1] - m0 + 1
    g = m - m0
    C = np.full(n, np.nan); C[g] = C0
    O = np.full(n, np.nan); O[g] = O0
    I = np.full(n, -1, dtype=np.int64); I[g] = I0
    has = np.zeros(n, bool); has[g] = True
    L = np.where(has, np.arange(n), -1)
    L = np.maximum.accumulate(L)
    ts = pd.DatetimeIndex((np.arange(n) + m0) * 60 * 1_000_000_000, tz="UTC").tz_convert("America/New_York")
    et_min = (ts.hour * 60 + ts.minute).to_numpy().astype(np.int16)
    et_date = ts.tz_localize(None).normalize().to_numpy().astype("datetime64[D]")
    sess = et_date + (et_min >= 18 * 60).astype("timedelta64[D]")
    out = dict(C=C, O=O, I=I, L=L, et_min=et_min, et_date=et_date, sess=sess, m0=np.array([m0]))
    np.savez(cache, **out)
    print(sym, "bars", len(m), "grid", n, "first", ts[g[0]], "last", ts[-1], flush=True)
    return out


def pclose(G, gi, maxstale=5):
    """close of last bar at or before grid index gi (array), NaN if older than maxstale minutes; also its instrument"""
    gi = np.asarray(gi)
    ok = (gi >= 0) & (gi < len(G["C"]))
    gc = np.clip(gi, 0, len(G["C"]) - 1)
    li = G["L"][gc]
    ok &= (li >= 0) & (gc - li <= maxstale)
    lc = np.clip(li, 0, None)
    return np.where(ok, G["C"][lc], np.nan), np.where(ok, G["I"][lc], -2), np.where(ok, lc, -1)


def pevent(G, gi, maxstale=5):
    """price at time t: open of the bar opening at t, else close of last bar within maxstale minutes"""
    gi = np.asarray(gi)
    gc = np.clip(gi, 0, len(G["C"]) - 1)
    hasbar = ~np.isnan(G["O"][gc])
    pc, ic, lc = pclose(G, gi - 1, maxstale - 1)
    p = np.where(hasbar, G["O"][gc], pc)
    ins = np.where(hasbar, G["I"][gc], ic)
    li = np.where(hasbar, gc, lc)
    return p, ins, li


def biggap_cum(G, maxgap=5):
    """cumulative count of bars preceded by more than maxgap missing minutes"""
    C = G["C"]
    has = ~np.isnan(C)
    idx = np.flatnonzero(has)
    gaps = np.diff(idx) - 1
    bg = np.zeros(len(C), np.int32)
    bg[idx[1:][gaps > maxgap]] = 1
    return np.cumsum(bg)


if __name__ == "__main__":
    for s in ("NQ", "ES"):
        G = grid(s)
        print(s, {k: v.shape for k, v in G.items()})
