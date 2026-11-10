"""Compare the backed-up (original) engine with the updated one on the current BASE signals."""
import importlib.util, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
spec = importlib.util.spec_from_file_location("ee_old", sys.argv[1])
ee_old = importlib.util.module_from_spec(spec); spec.loader.exec_module(ee_old)
import exits_compare as ec, exits_engine as ee
ec.init()
for sym in ("NQ", "ES"):
    D = ec.G[sym]; sigs = ec.G[("sets", sym)]["Overnight break + daily trend"]
    for rule, k in (("hold", 2.0), ("trail_6", 2.0), ("target_2", 3.0), ("scale", 2.0), ("ema60", 2.0), ("flow", 2.0)):
        a, b = ee_old.run(D, sigs, rule, k0=k), ee.run(D, sigs, rule, k0=k)
        same = len(a) == len(b) and np.allclose(a.pts, b.pts) and (a.exit.values == b.exit.values).all() and (a.bar.values == b.bar.values).all()
        print(f"{sym} {rule:8s} k0={k}: old {len(a)} trades {a.pts.sum():.2f} pts | new {len(b)} trades {b.pts.sum():.2f} pts | identical: {same}")
