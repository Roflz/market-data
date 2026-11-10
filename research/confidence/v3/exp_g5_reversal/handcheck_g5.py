"""HEAVY (raw 1-minute data): run under the shared flock.
Hand-check 10 G5 trades priced by harness.time_trades against the RAW research_lib.bars_1m rows
(re-uses v3/handcheck_harness.hand: entry/exit = open of the 1-minute bar at the mark, else the last close before it).
Trades: 7 from A5 (MES 3 incl. an early-close exit if any, MNQ 2, MYM 2), 1 S5.5 (02:00-03:00), 1 S5.6 (02:00-09:30),
1 A5 day-part neighbour (09:30-16:00). Also re-checks the A5 signal for those trades from the raw data:
side = -sign(4r1+3r2+2r3+r4) with r_k = last price / previous session's last price - 1 (same contract)."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H                      # noqa: E402
import handcheck_harness as HC           # noqa: E402
import research_lib as rl                # noqa: E402
import g5                                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def pick():
    rng = np.random.default_rng(20261109)
    A5 = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "A5.parquet"))
    rows = []
    for m, n in (("ES", 3), ("NQ", 2), ("YM", 2)):
        t = A5[A5.market == m]
        ii = list(rng.choice(len(t), size=n, replace=False))
        cl = np.flatnonzero(t.exit_kind.to_numpy() == "close")
        if m == "ES" and len(cl):
            ii[0] = int(rng.choice(cl))
        for i in ii:
            rows.append(("A5", t.iloc[i]))
    for cid, fn, m in (("S5.5", g5.sig_S55, "ES"), ("S5.6", g5.sig_S56, "NQ"), ("A5_N4_daypart", g5.sig_N_day, "YM")):
        e = g5.entries_for(fn, m)
        tr = H.time_trades(m, e)
        rows.append((cid, tr.iloc[int(rng.integers(len(tr)))]))
    return rows


def raw_signal(m1, D, S):
    """A5 signal recomputed from raw last prices (16:45 open or last close before 16:45) of the previous 5 sessions."""
    i = S.index.get_loc(D)
    prev = S.index[max(i - 5, 0): i]
    px, inst = [], []
    for P in prev:
        r, body = HC.raw_session(m1, P)
        px.append(HC.px_at(r, body, P + pd.Timedelta(hours=16, minutes=45), True))
        inst.append(body.instrument_id.iloc[-1])
    rets = []
    for k in range(1, len(px)):
        rets.append(px[k] / px[k - 1] - 1 if inst[k] == inst[k - 1] else 0.0)
    rets = rets[::-1] + [0.0] * 4                         # r1 = most recent
    s = 4 * rets[0] + 3 * rets[1] + 2 * rets[2] + rets[3]
    return int(-np.sign(s))


def main():
    picks = pick()
    out = []
    for sym in ("ES", "NQ", "YM"):
        mine = [(c, t) for c, t in picks if t.market == sym]
        if not mine:
            continue
        m1 = rl.bars_1m(sym)
        S = H.sessions(sym)
        for cid, t in mine:
            D = pd.Timestamp(t.session)
            ke, kx = H.mark_index(t.entry), H.mark_index(t.exit)
            e, x, kind, pnl, _, _ = HC.hand(m1, sym, D, ke, kx, int(t.d), np.nan)
            sd = raw_signal(m1, D, S) if cid.startswith("A5") else None
            out.append(dict(col=cid, market=sym, session=D.date(), entry=t.entry, exit=t.exit, d=int(t.d),
                            h_entry_px=t.entry_px, hand_entry_px=e, h_exit_px=t.exit_px, hand_exit_px=x,
                            h_kind=t.exit_kind, hand_kind=kind, h_pnl=round(t.pnl_usd, 4), hand_pnl=round(pnl, 4),
                            raw_side=sd, side_ok=(sd is None or sd == int(t.d)),
                            match=bool(abs(pnl - t.pnl_usd) < 1e-6 and kind == t.exit_kind)))
        del m1
    o = pd.DataFrame(out)
    o.to_csv(os.path.join(HERE, "handcheck_10.csv"), index=False)
    pd.set_option("display.width", 250)
    print(o.to_string())
    print(f"hand-check: {o.match.sum()} / {len(o)} prices+P&L match; A5 sides from raw data match: "
          f"{o.side_ok.sum()} / {len(o)}")


if __name__ == "__main__":
    main()
