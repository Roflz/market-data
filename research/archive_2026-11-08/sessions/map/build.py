"""
Build 5-minute slot moves from CME 1-minute bars (NQ, ES). Read-only on the project; writes to this folder.

Slot = 5 clock minutes [s, s+4] (bar OPEN times). Move = log(C_end / C_ref) in bp where
  C_ref = close of the last bar at or before s-1, required within 5 minutes (<= 5 missing minutes) and same instrument_id,
  C_end = close of the last bar at or before s+4 (same instrument_id as C_ref).
  Empty slot (no trades) inside a continuous stretch (a bar within 5 minutes after s+4) -> move 0.
  If C_ref is stale (session reopen: 18:00 ET daily, or after a halt), fall back to the OPEN of the bar at minute s
  (only when a bar exists exactly at s): flagged ref_open=1. This keeps the reopen slot measurable without ever
  spanning the closed hour/weekend.
Also: 1-minute abs moves for 07:00-10:59 ET (zoom around 8:30), same rules.
"""
import os
import sys

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "/run/media/roflz/Disk 2/_/market_data"
MAXGAP = 5


def load(sym):
    d = pd.read_csv(f"{ROOT}/data/{sym}_fut_1m.csv", usecols=["ts_event", "Open", "Close", "Volume", "instrument_id"],
                    engine="pyarrow")
    t = pd.to_datetime(d.ts_event, utc=True)
    d = d.assign(t=t).drop(columns="ts_event")
    d = d[~d.t.duplicated()].sort_values("t").reset_index(drop=True)
    return d


def build(sym):
    d = load(sym)
    m = (d.t.dt.as_unit("s").astype("int64") // 60).to_numpy()  # epoch minutes UTC
    C = d.Close.to_numpy(float)
    O = d.Open.to_numpy(float)
    V = d.Volume.to_numpy(float)
    I = d.instrument_id.to_numpy()
    cv = np.concatenate([[0.0], np.cumsum(V)])
    print(sym, len(d), d.t.min(), d.t.max(), flush=True)

    # all 5-min slot starts from first to last bar
    s = np.arange((m[0] // 5) * 5, m[-1] + 1, 5)
    r = np.searchsorted(m, s - 1, side="right") - 1          # last bar <= s-1
    e = np.searchsorted(m, s + 4, side="right") - 1          # last bar <= s+4
    f = np.searchsorted(m, s, side="left")                    # first bar >= s
    nxt = np.searchsorted(m, s + 5, side="left")              # first bar >= s+5
    has = e >= f                                              # at least one bar in slot
    rc = np.clip(r, 0, None)
    ec = np.clip(e, 0, None)
    fc = np.clip(f, 0, len(m) - 1)
    nc = np.clip(nxt, 0, len(m) - 1)
    ref_ok = (r >= 0) & ((s - 1) - m[rc] <= MAXGAP)
    nxt_ok = (nxt < len(m)) & (m[nc] - (s + 4) <= MAXGAP + 1)
    # main definition
    mv = np.full(len(s), np.nan)
    ok1 = ref_ok & has & (I[rc] == I[ec])
    mv[ok1] = 1e4 * np.log(C[ec[ok1]] / C[rc[ok1]])
    ok0 = ref_ok & ~has & nxt_ok & (I[rc] == I[nc]) & (m[nc] - m[rc] <= 2 * MAXGAP + 1)  # no trades, market open
    # (the bracket around an empty slot may span at most 10 missing minutes: excludes the old 16:15-16:30 halt)
    mv[ok0] = 0.0
    # reopen fallback: stale ref, bar exactly at s
    ok2 = ~ref_ok & has & (m[fc] == s) & (I[fc] == I[ec])
    mv[ok2] = 1e4 * np.log(C[ec[ok2]] / O[fc[ok2]])
    vol = np.where(has, cv[ec + 1] - cv[fc], 0.0)
    nb = np.where(has, e - f + 1, 0)
    valid = ok1 | ok0 | ok2
    S = pd.DataFrame({"t": pd.to_datetime(s[valid] * 60, unit="s", utc=True), "mv": mv[valid], "vol": vol[valid],
                      "nbars": nb[valid].astype(np.int16), "ref_open": ok2[valid].astype(np.int8),
                      "px": np.where(has, C[ec], C[rc])[valid]})
    S.to_parquet(f"{OUT}/slots5_{sym}.parquet")
    print(sym, "slots valid", valid.sum(), "empty-slot zeros", ok0.sum(), "reopen-fallback", ok2.sum(), flush=True)

    # 1-minute moves 07:00-10:59 ET (C[t]/C[t-1] with the same gap/roll rules)
    tet = d.t.dt.tz_convert("America/New_York")
    hm = (tet.dt.hour * 60 + tet.dt.minute).to_numpy()
    keep = (hm >= 420) & (hm < 660)
    prev = np.arange(len(m)) - 1
    pc = np.clip(prev, 0, None)
    ok = (prev >= 0) & (m - m[pc] <= MAXGAP + 1) & (I == I[pc])
    mv1 = np.where(ok, 1e4 * np.log(C / C[pc]), np.nan)
    M = pd.DataFrame({"t": d.t[keep].to_numpy(), "mv": mv1[keep], "vol": V[keep]})
    M = M[np.isfinite(M.mv)]
    M.to_parquet(f"{OUT}/min1_{sym}.parquet")
    print(sym, "1m rows", len(M), flush=True)


if __name__ == "__main__":
    for sym in sys.argv[1:] or ["NQ", "ES"]:
        build(sym)
