"""
v3/exp_G4/eval_twins.py - A4 eval relevance (PREREG 0.8; descriptive only): H.eval with fixed 1/3/5 micros under the
40% and 50% consistency rules, against 200 C1 zero-timing-edge twins (same side and hours, random same-year sessions;
reps 0..199 of the primary C1 draws, seeds 4000/4001). Light. Writes v3/exp_G4/eval_twins_A4.csv.
"""
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H  # noqa: E402
import g4lib as G  # noqa: E402

SIZ = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
KEYS = ["policy", "consistency", "window"]
MET = ["pass_pct", "bust_pct", "within_10", "within_20", "days_pass_median"]


def main(hid="A4", k=4, fn=None, sym="NQ", n_twins=200):
    fn = fn or G.release_fade()
    S = H.sessions(sym)
    ent = fn(S, {})
    ent = ent[pd.DatetimeIndex(ent.session) <= G.END].reset_index(drop=True)
    L = G.run_leg(sym, ent, k, R=n_twins, nrep_ctrl=2)
    real = H.eval(L["trades"], sizing=SIZ, calendar_=G.CAL)
    t0 = time.time()
    tw = []
    c1 = L["c1"]
    for r in range(n_twins):
        x = c1[c1.rep == r]
        e = H.eval(x, sizing=SIZ, calendar_=G.CAL)
        e["rep"] = r
        tw.append(e[KEYS + MET + ["rep"]])
    tw = pd.concat(tw, ignore_index=True)
    rows = []
    for key, g in tw.groupby(KEYS, sort=False):
        rr = real.set_index(KEYS).loc[key]
        row = dict(zip(KEYS, key))
        for m in ("pass_pct", "within_10", "within_20"):
            row[f"{m}_real"] = rr[m]
            row[f"{m}_twin_mean"] = g[m].mean()
            row[f"{m}_rank_p"] = (1 + (g[m] >= rr[m]).sum()) / (1 + len(g))
        row["bust_real"] = rr["bust_pct"]
        row["bust_twin_mean"] = g["bust_pct"].mean()
        row["bust_rank_p_lower"] = (1 + (g["bust_pct"] <= rr["bust_pct"]).sum()) / (1 + len(g))
        row["days_pass_median_real"] = rr["days_pass_median"]
        row["days_pass_median_twin"] = g["days_pass_median"].median()
        row["luck_within_10"] = rr.get("luck_within_10", np.nan)
        row["luck_pass_pct"] = rr.get("luck_pass_pct", np.nan)
        rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(G.HERE, f"eval_twins_{hid}.csv"), index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    print(out.round(3).to_string(index=False))
    print(f"twins {n_twins}, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
