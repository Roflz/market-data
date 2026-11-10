"""Combine S1/S2/S3 results, Holm across the 9 family tests, final pass/fail -> summary.json"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from y12lib import *

R = {}
for f in ("s1_results.json", "s2_results.json", "s3_results.json"):
    R.update(json.load(open(f"{HERE}/{f}")))
fam = ["S1", "S1-V1", "S1-V2", "S2", "S2-V1", "S2-V2", "S3", "S3-V1", "S3-V2"]
p = {k: p_two_sided(R[k]["t"], R[k]["n"]) for k in fam}
hp = holm(p)
rules = []
for k in fam:
    o = R[k]
    primary = k in ("S1", "S2", "S3")
    crit = [dict(c) for c in o["criteria"]]
    if not primary:
        ok = (o["t"] >= 3.0) or (hp[k] < 0.05 and o["t"] > 0)
        crit[0] = {"name": "a (variant): t >= 3 or Holm-adjusted p < 0.05 across 9 family tests (positive mean)",
                   "value": f"t={o['t']:.3f}, raw two-sided p={p[k]:.3g}, Holm p={hp[k]:.3g}", "pass": bool(ok)}
    else:
        crit[0]["value"] += f"; Holm p (9 tests)={hp[k]:.3g}"
    passed = all(c["pass"] for c in crit)
    inst = "M2K vs MES" if k == "S2-V2" else "MNQ vs MES"
    csv = f"{HERE}/trades_{k}.csv"
    rules.append({"rule": k, "instrument": inst, "primary": primary, "trades": o["n"],
                  "net_usd_per_trade": o["net_usd_per_trade"], "total_usd": o["total_usd"], "t": o["t"],
                  "gross_bp_per_trade": o["mean_gross_bp"], "net_bp_per_trade": o["mean_net_bp"],
                  "trades_per_year": o["per_year"], "criteria": crit, "passed": bool(passed), "trades_csv": csv,
                  "raw_p_two_sided": p[k], "holm_p": hp[k]})
    print(f"{k:6s} n={o['n']:4d} net={o['mean_net_bp']:7.2f}bp gross={o['mean_gross_bp']:6.2f} t={o['t']:6.2f} "
          f"holm={hp[k]:.3g} $/tr={o['net_usd_per_trade']:8.2f} tot=${o['total_usd']:10.0f} pass={passed} "
          + " ".join(f"{c['name'][:2]}{'Y' if c['pass'] else 'N'}" for c in crit))
summ = {"rules": rules, "details": R, "holm": hp, "raw_p": p,
        "sanity": json.load(open(f"{HERE}/sanity.json"))}
with open(f"{HERE}/summary.json", "w") as f:
    json.dump(jsonable(summ), f, indent=1)
