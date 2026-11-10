"""EXPLORATORY (not pre-registered; logged as a trial): a fairer zero-timing-edge eval twin for an every-session rule.
The pre-registered C1 twin draws sessions WITH replacement, so a twin trades on only ~63% of sessions and stacks
2-3 trades on others; that alone changes 'pass within 10 days'. Here each twin keeps the real sessions, marks and
yearly long/short mix and only PERMUTES the sides across the year's trades (no timing information left).
200 twins per market, same seeds for all three markets so the basket's sides stay as correlated as the real ones'
are not (independent per market). Light."""
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


def main(n_twins=200):
    t0 = time.time()
    real_tr = pd.read_parquet(os.path.join(H.HERE, "out", "trades", "A5.parquet"))
    real = H.eval(real_tr, POL, calendar_=g5.CAL)
    rng = np.random.default_rng(20261109 + 77)
    ents = {m: g5.entries_for(g5.sig_A5, m) for m in g5.MK_ORDER}
    rows, means = [], []
    for r in range(n_twins):
        parts = []
        for m, e in ents.items():
            c = e.copy()
            yr = pd.DatetimeIndex(c["session"]).year.to_numpy()
            dd = c["d"].to_numpy().copy()
            for y in np.unique(yr):
                ix = np.flatnonzero(yr == y)
                dd[ix] = dd[rng.permutation(ix)]
            c["d"] = dd
            parts.append(H.time_trades(m, c))
        tw = pd.concat(parts, ignore_index=True)
        means.append(float(tw.pnl_usd.sum() / len(g5.CAL)))
        e = H.eval(tw, POL, calendar_=g5.CAL)
        e["rep"] = r
        rows.append(e[KEYS + VALS + ["rep"]])
    T = pd.concat(rows, ignore_index=True)
    T.to_csv(os.path.join(HERE, "work", "A5_permtwin_evals.csv"), index=False)
    out = []
    for _, rr in real.iterrows():
        msk = (T.policy == rr.policy) & (T.consistency == rr.consistency) & (T.window == rr.window)
        row = {k: rr[k] for k in KEYS}
        for v in VALS:
            tv = T.loc[msk, v].to_numpy(float)
            row[f"real_{v}"] = float(rr[v]); row[f"perm_{v}_mean"] = float(tv.mean())
            sgn = -1 if v == "bust_pct" else 1
            row[f"rank_p_{v}"] = float((1 + np.sum(sgn * tv >= sgn * rr[v])) / (1 + len(tv)))
        out.append(row)
    O = pd.DataFrame(out)
    O.to_csv(os.path.join(H.HERE, "exp_G5", "A5_eval_vs_permtwins_EXPLORATORY.csv"), index=False)
    real_mean = float(real_tr.pnl_usd.sum() / len(g5.CAL))
    p_perm = float((1 + np.sum(np.array(means) >= real_mean)) / (1 + len(means)))
    print(f"side-permutation test of mean daily net: real {real_mean:.2f}, perm mean {np.mean(means):.2f}, "
          f"sd {np.std(means, ddof=1):.2f}, rank p {p_perm:.3f}")
    H.log("A5_permtwin_EXPLORATORY", "MES+MNQ+MYM", "A5 eval vs side-permutation twins (exploratory control)",
          trades=real_tr, baseline=float(np.mean(means) * len(g5.CAL) / len(real_tr)),
          params=dict(n_twins=n_twins, p_perm_mean=p_perm), note="exploratory eval control, not a new rule")
    pd.set_option("display.width", 250)
    print(O.to_string())
    print(f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
