"""Re-run H.standard_report (100 reps: same sessions with random marks of the same length and random side; hour
drift; plain drift) for corrected S3.7 per market and replace the S3.7|<sym> keys of standard_report_controls.json.
Light (v3/data). Seed g3.SEED (the v1 seed was not recorded)."""
import json, os, sys
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import g3
import harness as H
p = os.path.join(g3.HERE, "standard_report_controls.json")
d = json.load(open(p))
for sym in g3.MKTS:
    r = H.standard_report(sym, g3.entries("S3.7", sym), n_rep=100, seed=g3.SEED, n_boot=1000)
    d[f"S3.7|{sym}"] = {k: r[k].round(3).to_dict(orient="records") for k in ("vs_random", "vs_hour_drift", "vs_drift")}
    v = r["vs_random"].set_index("window"); h = r["vs_hour_drift"].set_index("window")
    print(sym, "actual $/tr %.2f | random marks+side %.2f p %.3f | hour drift %.2f p %.3f | 2022+ actual %.2f" % (
        v.loc["all", "actual"], v.loc["all", "control"], v.loc["all", "p_ctrl"], h.loc["all", "control"],
        h.loc["all", "p_ctrl"], v.loc["2022+", "actual"]), flush=True)
json.dump(d, open(p, "w"), indent=0, default=str)
