"""A5 eval (descriptive): H.eval of the real A5 basket at fixed 1/3/5 micros per market vs the same eval on 200 C1
realisations (zero-timing-edge twins: same side, hours, sizes, random same-year sessions). Light."""
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H   # noqa: E402
import g5             # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
POL = [("fixed", 1), ("fixed", 3), ("fixed", 5)]
KEYS = ["policy", "consistency", "window"]
VALS = ["pass_pct", "within_10", "within_20", "bust_pct"]


def main():
    t0 = time.time()
    tr = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "A5.parquet"))
    real = H.eval(tr, POL, calendar_=g5.CAL)
    tw = pd.read_parquet(os.path.join(HERE, "work", "A5_twins200.parquet"))
    rows = []
    for r in sorted(tw.rep.unique()):
        e = H.eval(tw[tw.rep == r], POL, calendar_=g5.CAL)
        e["rep"] = r
        rows.append(e[KEYS + VALS + ["rep"]])
    T = pd.concat(rows, ignore_index=True)
    T.to_csv(os.path.join(HERE, "work", "A5_twin_evals.csv"), index=False)
    out = []
    for _, rr in real.iterrows():
        m = (T.policy == rr.policy) & (T.consistency == rr.consistency) & (T.window == rr.window)
        row = {k: rr[k] for k in KEYS}
        for v in VALS:
            tv = T.loc[m, v].to_numpy(float)
            row[f"real_{v}"] = float(rr[v])
            row[f"twin_{v}_mean"] = float(tv.mean())
            row[f"twin_{v}_p90"] = float(np.quantile(tv, 0.9))
            sgn = -1 if v == "bust_pct" else 1
            row[f"rank_p_{v}"] = float((1 + np.sum(sgn * tv >= sgn * rr[v])) / (1 + len(tv)))
        out.append(row)
    O = pd.DataFrame(out)
    O.to_csv(os.path.join(H.HERE, "exp_G5", "A5_eval_vs_twins.csv"), index=False)
    pd.set_option("display.width", 250)
    print(O.to_string())
    print(f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
