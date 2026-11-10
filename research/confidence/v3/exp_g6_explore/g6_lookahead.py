"""
v3/exp_g6_explore/g6_lookahead.py - no-look-ahead checks for X1-X5 (PREREG 0.6). Light.
1) H.lookahead_check(fn, sym, n_cuts=20, seed=0) for every signal and market.
2) X1 on MNQ / MYM reads ES prev_ret_cc: cross check with BOTH the market's and the ES table truncated at 20 cuts.
3) Entry-time re-run: 20 random trades per signal (MES and MNQ): data cut at the trade's entry mark must reproduce the
   same trade (session, entry, exit, side, stop, target).
Output: exp_g6_explore/lookahead.csv
"""
import os
import warnings

import numpy as np
import pandas as pd

import harness as H
import g6_signals as G

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ["session", "entry", "exit", "d", "stop_pts", "target_pts"]


def norm(e):
    e = H._as_frame(e)
    e = e[[c for c in COLS if c in e.columns]].copy()
    e["session"] = pd.DatetimeIndex(e["session"]).normalize()
    e["entry"] = H._marks(e["entry"]) if len(e) else e["entry"]
    e["exit"] = H._marks(e["exit"]) if len(e) else e["exit"]
    for c in ("stop_pts", "target_pts"):
        e[c] = np.round(e[c].astype(float), 9)
    return e.reset_index(drop=True)


def main():
    rows = []
    es = H.sessions("ES")
    for sym in ("ES", "NQ", "YM"):
        for hid, (fn, fam, use15) in G.signal_fns(sym, es).items():
            r = H.lookahead_check(fn, sym, n_cuts=20, seed=0, tfs=(15,), start="2012-01-01" if sym != "YM" else "2018-06-01")
            rows.append(dict(check="lookahead_check", sym=sym, hid=hid, n=len(r), ok=bool(r.same.all()),
                             n_entries_compared=int(r.n_full.sum())))
            print(sym, hid, "lookahead_check ok", int(r.n_full.sum()), flush=True)
    # 2) cross check for X1 on NQ / YM (ES table also truncated)
    rng = np.random.default_rng(7)
    for sym in ("NQ", "YM"):
        S = H.sessions(sym)
        for name, mk in (("X1a", G.x1a_fn), ("X1b", G.x1b_fn)):
            full = norm(mk(es)(S, {}))
            ev = full["session"].unique()
            ok = True
            n_cmp = 0
            for i in range(20):
                c = pd.Timestamp(ev[rng.integers(len(ev))]) if i % 2 == 0 else S.index[rng.integers(len(S) - 1)]
                k = int(rng.integers(0, 92))
                T = H.mark_time(c, k)
                Sc, _ = H.truncate(sym, c, k, tfs=())
                Ec, _ = H.truncate("ES", c, k, tfs=()) if c in es.index else (es.loc[es.index < c], None)
                cut = norm(mk(Ec)(Sc, {}))
                tf = H.mark_time(full["session"], full["entry"].to_numpy())
                tc = H.mark_time(cut["session"], cut["entry"].to_numpy()) if len(cut) else pd.DatetimeIndex([])
                a = full.loc[np.asarray(tf <= T)].reset_index(drop=True)
                b = cut.loc[np.asarray(tc <= T)].reset_index(drop=True) if len(cut) else cut
                same = len(a) == len(b) and a.astype(str).equals(b.astype(str))
                n_cmp += len(a)
                ok &= same
            rows.append(dict(check="cross_ES_truncated", sym=sym, hid=name, n=20, ok=bool(ok), n_entries_compared=n_cmp))
            print(sym, name, "cross check", ok, flush=True)
            assert ok
    # 3) entry-time re-run, 20 random trades per signal
    for sym in ("ES", "NQ"):
        S = H.sessions(sym)
        for hid, (fn, fam, use15) in G.signal_fns(sym, es).items():
            tfs = (15,) if use15 else ()
            full = norm(fn(S, {15: H.bars(sym, 15)} if use15 else {}))
            pick = rng.choice(len(full), size=min(20, len(full)), replace=False)
            ok = True
            for i in pick:
                tr = full.iloc[i]
                Sc, Bc = H.truncate(sym, tr["session"], int(tr["entry"]), tfs=tfs)
                Ec = H.truncate("ES", tr["session"], int(tr["entry"]), tfs=())[0] if (hid.startswith("X1") and sym != "ES") else None
                f2 = fn if Ec is None else (G.x1a_fn(Ec) if hid == "X1a" else G.x1b_fn(Ec))
                cut = norm(f2(Sc, Bc))
                m = cut[(cut["session"] == tr["session"]) & (cut["entry"] == tr["entry"])]
                same = len(m) == 1 and m.iloc[0].astype(str).equals(tr.astype(str))
                if not same:
                    print("MISMATCH", sym, hid, tr.to_dict(), m.to_dict("records"))
                ok &= same
            rows.append(dict(check="entry_time_rerun", sym=sym, hid=hid, n=len(pick), ok=bool(ok), n_entries_compared=len(pick)))
            print(sym, hid, "entry-time re-run", ok, flush=True)
            assert ok
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "lookahead.csv"), index=False)
    print(out.to_string())
    print("ALL OK" if out.ok.all() else "FAILURES")


if __name__ == "__main__":
    main()
