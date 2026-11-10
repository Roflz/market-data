"""No-look-ahead checks for every G3 signal (PREREG 0.6). Light (v3/data only).
1) H.lookahead_check(fn, sym, n_cuts=20, seed=0) for every column x market (random cut points).
2) Targeted truncation: for 25 random EVENT sessions per column x market, cut the data exactly at each leg's entry
   mark (and one mark earlier) and require the entries at or before the cut to be identical.
3) TOM_DAYS (S3.7 schedule list) recomputed from the truncated calendar at each cut must give the same day.
Output: v3/exp_g3_expiry/lookahead_g3.csv"""
import os
import sys

import numpy as np
import pandas as pd

import g3
import harness as H

rows = []
ONLY = sys.argv[1:]                    # optional: re-check only these columns (rows merged into lookahead_g3.csv)
for hid, (desc, legs, which, mkts, tier) in g3.COLS.items():
    if ONLY and hid not in ONLY:
        continue
    for sym in mkts:
        fn = g3.sig_event(legs, which)
        r = H.lookahead_check(fn, sym, n_cuts=20, seed=0, tfs=(5,))
        rows.append(dict(hid=hid, sym=sym, kind="random_cuts", n=len(r), ok=bool(r.same.all())))
        S = H.sessions(sym)
        full = fn(S, {})
        full = full[pd.DatetimeIndex(full.session) <= g3.LAST]
        ev = pd.DatetimeIndex(full.session.unique())
        ev = ev[ev >= pd.Timestamp("2010-07-01")]
        rng = np.random.default_rng(3)
        pick = ev[rng.choice(len(ev), size=min(25, len(ev)), replace=False)]
        ok = True
        n = 0
        for c in pick:
            for (e, x, d) in legs:
                for k in {max(H.mark_index(e) - 1, 0), H.mark_index(e)}:
                    Sc, _ = H.truncate(sym, c, k, tfs=())
                    cut = fn(Sc, {})
                    T = H.mark_time(c, k)
                    def known(f):
                        t = H.mark_time(pd.DatetimeIndex(f.session), np.array([H.mark_index(v) for v in f.entry]))
                        g = f.loc[np.asarray(t <= T), ["session", "entry", "exit", "d"]].reset_index(drop=True)
                        return g.astype(str)
                    a, b = known(full[pd.DatetimeIndex(full.session) <= c]), known(cut)
                    ok &= bool(len(a) == len(b) and a.equals(b))
                    if which == "tom":
                        tom_c = g3.first_trading_days(Sc.index)     # v2 rule (NYSE holidays skipped)
                        ok &= bool((c in tom_c) == (c in g3.TOM_DAYS))
                    n += 1
        rows.append(dict(hid=hid, sym=sym, kind="event_cuts", n=n, ok=ok))
        print(rows[-2], rows[-1], flush=True)
out = pd.DataFrame(rows)
if ONLY:
    old = pd.read_csv(os.path.join(g3.HERE, "lookahead_g3.csv"))
    out = pd.concat([old[~old.hid.isin(ONLY)], out], ignore_index=True)
out.to_csv(os.path.join(g3.HERE, "lookahead_g3.csv"), index=False)
print(out.to_string())
assert out.ok.all(), "LOOK-AHEAD FAILURE"
print("ALL LOOK-AHEAD CHECKS PASSED")
