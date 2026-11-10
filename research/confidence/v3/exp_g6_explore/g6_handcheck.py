"""
v3/exp_g6_explore/g6_handcheck.py - HEAVY (raw 1-minute data; run under the shared flock).
Re-prices 10 G6 trades (mix of X1a/X1b/X2/X3/X4/X5, all three markets, time / stop / target exits) by hand from the RAW
research_lib.bars_1m rows (no harness pricing code): entry / exit = open of the 1-minute bar at the mark (else last close
before it), stop and target walked on 5-minute clock buckets of the raw minutes (stop first; target needs a trade
1 tick through). Also recomputes each trade's SIGNAL from raw minutes (gap, 10:00 move, Asian range, 12:00 stretch side).
Output: exp_g6_explore/handcheck_10.csv
"""
import os
import pickle

import numpy as np
import pandas as pd

import harness as H
import research_lib as rl
from handcheck_harness import raw_session, px_at

HERE = os.path.dirname(os.path.abspath(__file__))


def hand_trade(m, sym, D, ke, kx, d, stop_pts, tgt_pts):
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
    st = e - d * stop_pts if np.isfinite(stop_pts) else np.nan
    tg = e + d * tgt_pts if np.isfinite(tgt_pts) else np.nan
    if np.isfinite(st) or np.isfinite(tg):
        w = body[(body.index >= te) & (body.index < tx)]
        for _, g in w.groupby(w.index.floor("5min")):
            o, hi, lo = g.Open.iloc[0], g.High.max(), g.Low.min()
            if np.isfinite(st) and ((d > 0 and lo <= st) or (d < 0 and hi >= st)):
                x = min(o, st) - tick if d > 0 else max(o, st) + tick
                kind = "stop"
                break
            if np.isfinite(tg) and ((d > 0 and hi >= tg + tick) or (d < 0 and lo <= tg - tick)):
                x, kind = tg, "target"
                break
    return e, x, kind, d * (x - e) * usd - cost, body


def main():
    st = pickle.load(open(os.path.join(HERE, "g6_stage1.pkl"), "rb"))
    T = st["trades"]
    rng = np.random.default_rng(20261109)
    picks = []

    def pick(col, cond=None, n=1):
        t = T[col]
        if cond is not None:
            t = t[cond(t)]
        for i in rng.choice(len(t), size=n, replace=False):
            picks.append((col, t.iloc[i]))
    pick("X1a_MES"); pick("X1b_MYM"); pick("X2_MNQ", lambda t: t.exit_kind == "target")
    pick("X2_MES", lambda t: t.exit_kind == "stop"); pick("X3_MNQ", lambda t: t.exit_kind == "stop")
    pick("X3_MES", lambda t: t.exit_kind == "time"); pick("X4_MES"); pick("X4_MYM"); pick("X5_MNQ"); pick("X5_MES")
    rows = []
    for sym in ("ES", "NQ", "YM"):
        mine = [(c, t) for c, t in picks if t["market"] == sym]
        if not mine:
            continue
        m = rl.bars_1m(sym)
        for col, t in mine:
            D = pd.Timestamp(t["session"])
            ke, kx = H.mark_index(t["entry"]), H.mark_index(t["exit"])
            e, x, kind, pnl, body = hand_trade(m, sym, D, ke, kx, int(t["d"]), float(t["stop_pts"]), float(t["target_pts"]))
            # signal re-derivation from raw minutes
            base = D - pd.Timedelta(hours=6)
            def p(hhmm):
                k = H.mark_index(hhmm)
                return px_at(*raw_session(m, D), base + pd.Timedelta(minutes=15 * k), False)
            sig = ""
            hyp = col.split("_")[0]
            if hyp == "X2":
                prev = m.loc[(m.index >= (D - pd.Timedelta(days=5)).tz_localize("America/New_York"))
                             & (m.index < base.tz_localize("America/New_York"))]
                prev = prev.set_axis(prev.index.tz_localize(None))
                prev = prev[(prev.index.hour * 60 + prev.index.minute < 16 * 60)
                            & (prev.index.hour * 60 + prev.index.minute >= 9 * 60 + 30)]
                pc = float(prev.Close.iloc[-1])
                g = e / pc - 1
                sig = f"prev 16:00 close {pc} gap {g:.5f} side {-int(np.sign(g))} pts {abs(e - pc)}"
            elif hyp == "X1b":
                mv = p("1000") - p("0930")
                sig = f"px_1000-px_0930 {mv} side {-int(np.sign(mv))}"
            elif hyp == "X5":
                mv = p("1200") / p("0930") - 1
                sig = f"09:30->12:00 move {mv:.5f} side {-int(np.sign(mv))}"
            elif hyp == "X3":
                rr = body[(body.index >= base) & (body.index < base + pd.Timedelta(hours=8))]
                rh, rl_ = rr.High.max(), rr.Low.min()
                sig = f"range {rl_}-{rh} mid {(rh + rl_) / 2} stop_pts_hand {int(t['d']) * (e - (rh + rl_) / 2)}"
            rows.append(dict(col=col, market=sym, session=D.date(), entry=t["entry"], exit=t["exit"], d=int(t["d"]),
                             stop_pts=t["stop_pts"], target_pts=t["target_pts"], h_entry_px=t["entry_px"],
                             hand_entry_px=e, h_exit_px=t["exit_px"], hand_exit_px=x, h_kind=t["exit_kind"],
                             hand_kind=kind, h_pnl=t["pnl_usd"], hand_pnl=pnl, signal_check=sig,
                             match=bool(abs(pnl - t["pnl_usd"]) < 1e-6 and kind == t["exit_kind"])))
        del m
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "handcheck_10.csv"), index=False)
    pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 90)
    print(out.to_string())
    print(f"hand-check: {out.match.sum()} / {len(out)} trades match")


if __name__ == "__main__":
    main()
