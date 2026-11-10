"""Re-run both controls with the builder's two incidental choices (full 2010-start segment path; coin via rng.random<0.5)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import check as C
W = C.W
sig = C.build_signal("ES"); days = sig.index
segs = {s: pd.read_pickle(f"{W}/seg_{s}.pkl") for s in ("NQ", "ES")}
pos, _, dec = C.positions(sig, segs["NQ"])
first = int(np.argmax(dec))
for sym, ppt, sc, lbl in (("NQ", 2.0, 1.0, "MNQ"), ("ES", 5.0, 1.75, "MES")):
    for r in ("P", "A", "B"):
        sgf = segs[sym]                                     # full path from 2010-06-07
        print(lbl, r, "full-path flat-forced:", sgf.status.value_counts().to_dict() if r == "P" else "")
        T, q, gu, sn, d = C.run(sgf, pos[r], ppt, sc)
        ok = (sgf.status == "ok").to_numpy()
        tot = T.net_usd.sum()
        rng = np.random.default_rng(12345)
        g, c = T.gross_usd.to_numpy(), T.cost.to_numpy()
        rd = np.array([(np.where(rng.random(len(g)) < 0.5, 1, -1) * g - c).sum() for _ in range(1000)])
        rng2 = np.random.default_rng(12345); M = len(q)
        offs = rng2.integers(252, M - 252 + 1, 1000)
        pl = np.array([(np.roll(q, k) * ok * d * ppt).sum() - sc * np.abs(np.diff(np.r_[0, np.roll(q, k) * ok, 0])).sum() for k in offs])
        print(f"   total {tot:.2f}  randdir p95 {np.percentile(rd,95):.2f} pct {100*(rd<tot).mean():.1f} | "
              f"placebo p95 {np.percentile(pl,95):.2f} mean {pl.mean():.2f} pct {100*(pl<tot).mean():.1f}")
