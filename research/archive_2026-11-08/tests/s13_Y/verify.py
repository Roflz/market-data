# independent re-check: every L1 trade's 8:30..9:45 bars share one instrument_id, and recomputed vectorised prices match
import sys, os, glob
import pandas as pd, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for sym, inst in [("NQ", "MNQ"), ("ES", "MES")]:
    b = pd.read_pickle(f"{HERE}/bars_{sym}_0800_1100.pkl")
    T = pd.read_csv(f"{HERE}/trades/L1-CPIorNFP-2010-2026-{inst}-time.csv", parse_dates=["date"])
    w = b[(b.tmin >= 510) & (b.tmin <= 585)]
    g = w.groupby("date")
    nid = g.instrument_id.nunique()
    o830 = w[w.tmin == 510].set_index("date").Open; o845 = w[w.tmin == 525].set_index("date").Open; o945 = w[w.tmin == 585].set_index("date").Open
    d = T.date
    assert (nid.reindex(d).to_numpy() == 1).all(), "roll inside window"
    assert np.allclose(o830.reindex(d).to_numpy(), T.o830) and np.allclose(o845.reindex(d).to_numpy(), T.entry) and np.allclose(o945.reindex(d).to_numpy(), T.exit)
    side = np.where(o845.reindex(d).to_numpy() > o830.reindex(d).to_numpy(), "short", "long")
    assert (side == T.side).all()
    print(sym, "ok", len(T), "trades; all single-instrument windows; prices/sides match vectorised recompute")
