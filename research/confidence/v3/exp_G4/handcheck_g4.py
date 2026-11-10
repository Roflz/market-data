"""
v3/exp_G4/handcheck_g4.py - HEAVY (raw 1-minute data; run under the shared flock).
Re-prices 10 G4 trades by hand from the raw research_lib.bars_1m rows (handcheck_harness.hand: entry/exit = open of
the 1-minute bar at the mark, else the last close before it; stop walked on 5-minute clock buckets), and re-derives
the A4 signal m = open(08:45 bar) - open(08:30 bar) from the raw rows. Only sessions <= 2025-06-27 are looked up.
Writes v3/exp_G4/handcheck_10.csv.
"""
import gc
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H  # noqa: E402
import handcheck_harness as HC  # noqa: E402
import research_lib as rl  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.path.join(H.HERE, "out", "trades")


def pick():
    rng = np.random.default_rng(20261109)
    out = []
    a4 = pd.read_parquet(os.path.join(TR, "A4.parquet"))
    out += [("A4", r) for _, r in a4.iloc[rng.choice(len(a4), 4, replace=False)].iterrows()]
    s6 = pd.read_parquet(os.path.join(TR, "S4.6.parquet"))
    out += [("S4.6", s6[s6.exit_kind == "stop"].iloc[int(rng.integers((s6.exit_kind == "stop").sum()))])]
    s4 = pd.read_parquet(os.path.join(TR, "S4.4.parquet"))
    out += [("S4.4", r) for _, r in s4.iloc[rng.choice(len(s4), 2, replace=False)].iterrows()]
    s5 = pd.read_parquet(os.path.join(TR, "S4.5.parquet"))
    out += [("S4.5", s5.iloc[int(rng.integers(len(s5)))])]
    s8 = pd.read_parquet(os.path.join(TR, "S4.8.parquet"))
    y8 = s8[s8.market == "YM"]
    out += [("S4.8", y8.iloc[int(rng.integers(len(y8)))])]
    s7 = pd.read_parquet(os.path.join(TR, "S4.7.parquet"))
    out += [("S4.7", s7.iloc[int(rng.integers(len(s7)))])]
    return out


def main():
    trades = pick()
    rows = []
    for sym in ("NQ", "ES", "YM"):
        mine = [(h, t) for h, t in trades if t.market == sym]
        if not mine:
            continue
        m = rl.bars_1m(sym)
        for hid, t in mine:
            D = pd.Timestamp(t.session)
            assert D <= pd.Timestamp("2025-06-27")
            ke, kx = H.mark_index(t.entry), H.mark_index(t.exit)
            sp_ = float(t.stop_pts) if np.isfinite(t.stop_pts) else np.nan
            e, x, kind, pnl, pnl1, kind1 = HC.hand(m, sym, D, ke, kx, int(t.d), sp_)
            extra = float(t.cost_usd) - H.SPEC[sym]["cost"]           # S4.8 exit tick
            pnl -= extra
            sig = np.nan
            if hid in ("A4", "S4.6", "S4.4", "S4.5"):
                r, body = HC.raw_session(m, D)
                p830 = HC.px_at(r, body, D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * 58), False)
                p845 = HC.px_at(r, body, D - pd.Timedelta(hours=6) + pd.Timedelta(minutes=15 * 59), False)
                sig = p845 - p830
            rows.append(dict(hid=hid, market=sym, session=D.date(), entry=t.entry, exit=t.exit, d=int(t.d),
                             stop_pts=t.stop_pts, h_entry_px=t.entry_px, hand_entry_px=e, h_exit_px=t.exit_px,
                             hand_exit_px=x, h_kind=t.exit_kind, hand_kind=kind, h_pnl=t.pnl_usd, hand_pnl=pnl,
                             hand_pnl_1min=pnl1 - extra, hand_m=sig,
                             side_ok=bool(np.isnan(sig) or -np.sign(sig) == int(t.d)),
                             match=bool(abs(pnl - t.pnl_usd) < 1e-6 and kind == t.exit_kind)))
        del m
        gc.collect()
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "handcheck_10.csv"), index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print(out.to_string(index=False))
    print(f"hand-check: {out.match.sum()} / {len(out)} trades match; signal side ok {out.side_ok.sum()} / {len(out)}")


if __name__ == "__main__":
    main()
