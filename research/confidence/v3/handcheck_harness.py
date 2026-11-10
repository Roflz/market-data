"""
v3/handcheck_harness.py - HEAVY (loads the raw 1-minute data; run under the shared flock).

1) 20 random time trades (8 MES, 7 MNQ, 5 MYM; half with a stop) priced by harness.time_trades are re-priced
   by hand from the RAW research_lib.bars_1m rows (tz-aware New York index, no v3 code): entry / exit = open of the
   1-minute bar at the mark (else the last close before it, same contract, market still open), stop walked on
   5-minute clock buckets of the raw minutes (and, for information, minute by minute). Output:
   v3/out/handcheck_20.csv.
2) v3 15-minute bars vs signals.bars(sym, 15): O H L C V vwap identical on every common bar (same session and
   contract, start before 16:45).
"""
import os

import numpy as np
import pandas as pd

import harness as H
import research_lib as rl
import signals as sg

HERE = os.path.dirname(os.path.abspath(__file__))
NY = "America/New_York"


def raw_session(m, D):
    """raw 1-minute rows of session D (kept contract = contract of the session's last row before 16:45),
    tz-naive wall clock, rows from 18:00 to 16:44 plus the 16:45 row."""
    a = (D - pd.Timedelta(hours=6)).tz_localize(NY)
    b = (D + pd.Timedelta(hours=16, minutes=46)).tz_localize(NY)
    r = m.loc[(m.index >= a) & (m.index < b)]
    r = r.set_axis(r.index.tz_localize(None))
    body = r[r.index < D + pd.Timedelta(hours=16, minutes=45)]
    inst = body.instrument_id.iloc[-1]
    return r[r.instrument_id == inst], body[body.instrument_id == inst]


def px_at(r, body, t, last):
    if last and t in r.index:
        return float(r.loc[t, "Open"])
    if last:
        return float(body.Close.iloc[-1])
    if t < body.index[0] or t > body.index[-1]:
        return np.nan
    if t in body.index:
        return float(body.loc[t, "Open"])
    return float(body.Close[body.index < t].iloc[-1])


def hand(m, sym, D, ke, kx, d, stop_pts):
    tick, usd, cost = H.SPEC[sym]["tick"], H.SPEC[sym]["usd"], H.SPEC[sym]["cost"]
    r, body = raw_session(m, D)
    te = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * ke)
    tx = D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * kx)
    e = px_at(r, body, te, False)
    last_off = (body.index[-1] - (D - pd.Timedelta(hours=6))) / pd.Timedelta(minutes=1)
    if 15 * kx > last_off + 15 or not np.isfinite(px_at(r, body, tx, kx == 91)):
        x, kind = px_at(r, body, tx, True), "close"
    else:
        x, kind = px_at(r, body, tx, kx == 91), "time"
    x1, kind1 = x, kind
    if np.isfinite(stop_pts):
        st = e - d * stop_pts
        w = body[(body.index >= te) & (body.index < tx)]
        for _, g in w.groupby(w.index.floor("5min")):
            o, hi, lo = g.Open.iloc[0], g.High.max(), g.Low.min()
            if (d > 0 and lo <= st) or (d < 0 and hi >= st):
                x = min(o, st) - tick if d > 0 else max(o, st) + tick
                kind = "stop"
                break
        for _, row in w.iterrows():                                   # minute-precise, for information
            if (d > 0 and row.Low <= st) or (d < 0 and row.High >= st):
                x1 = min(row.Open, st) - tick if d > 0 else max(row.Open, st) + tick
                kind1 = "stop"
                break
    return e, x, kind, d * (x - e) * usd - cost, d * (x1 - e) * usd - cost, kind1


def main():
    rng = np.random.default_rng(20261109)
    rows = []
    for sym, n in (("ES", 8), ("NQ", 7), ("YM", 5)):
        S = H.sessions(sym)
        si = rng.choice(len(S), size=n, replace=False)
        ke = rng.integers(0, 85, size=n)
        kx = np.minimum(ke + rng.integers(1, 60, size=n), 91)
        kx[0] = 91
        d = rng.choice([-1, 1], size=n)
        stop = np.where(np.arange(n) % 2 == 0, np.round(rng.uniform(0.001, 0.004, n) * S.px_0930.iloc[si].to_numpy()
                                                        / H.SPEC[sym]["tick"]) * H.SPEC[sym]["tick"], np.nan)
        ent = pd.DataFrame({"session": S.index[si], "entry": ke, "exit": kx, "d": d, "stop_pts": stop})
        tr = H.time_trades(sym, ent)
        m = rl.bars_1m(sym)
        for _, t in tr.iterrows():
            D = pd.Timestamp(t.session)
            k_e, k_x = H.mark_index(t.entry), H.mark_index(t.exit)
            e, x, kind, pnl, pnl1, kind1 = hand(m, sym, D, k_e, k_x, int(t.d), t.stop_pts)
            rows.append(dict(market=sym, session=D.date(), entry=t.entry, exit=t.exit, d=int(t.d), stop_pts=t.stop_pts,
                             h_entry_px=t.entry_px, hand_entry_px=e, h_exit_px=t.exit_px, hand_exit_px=x,
                             h_kind=t.exit_kind, hand_kind=kind, h_pnl=t.pnl_usd, hand_pnl=pnl,
                             hand_pnl_1min=pnl1, hand_kind_1min=kind1,
                             match=bool(abs(pnl - t.pnl_usd) < 1e-9 and kind == t.exit_kind)))
        del m
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "out", "handcheck_20.csv"), index=False)
    pd.set_option("display.width", 250)
    print(out.to_string())
    print(f"hand-check: {out.match.sum()} / {len(out)} trades match")
    # 2) bars vs signals.bars
    for sym in ("NQ", "ES", "YM"):
        sb = sg.bars(sym, 15)
        sb = sb[sb.index < H.HOLDOUT_SESSION_START]
        vb = H.bars(sym, 15)
        k1 = pd.MultiIndex.from_arrays([sb.index, sb.inst])
        k2 = pd.MultiIndex.from_arrays([vb.index, vb.inst])
        common = k2.isin(k1)
        a = vb[common]
        b = sb.set_axis(k1).loc[k2[common]]
        same = all(np.allclose(a[c].to_numpy(), b[c].to_numpy(), equal_nan=True) for c in ("O", "H", "L", "C", "V", "vwap"))
        print(f"{sym} 15-min: v3 bars {len(vb):,}, signals.bars {len(sb):,}, common {common.sum():,}, "
              f"v3-only {(~common).sum()}, OHLCV+vwap identical on common bars: {same}")
        del sb


if __name__ == "__main__":
    main()
