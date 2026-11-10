"""Merge per-rule summaries into summary.json and print the compact rule table."""
import json

import s11common as sc

S = {k: json.load(open(f"{sc.OUT}/summary_{k}.json")) for k in ("A", "B", "C", "overlap")}
S["checks"] = open(f"{sc.OUT}/checks_output.txt").read().splitlines()
rows = []
for sec, names in [("A", ["A", "A1-MES", "A2-VWAP"]), ("B", ["B", "B-MES", "B1"]), ("C", ["C", "C1-calm", "C2-target"])]:
    for n in names:
        r = S[sec][n]
        h = r["headline"]
        t = h.get("t_nw5_daily_bp") if sec == "A" else min(h["t_event_nw5_bp"], h["t_event_iid_bp"])
        csv = f"{sc.OUT}/trades_{n}.csv" if sec != "C" else f"{sc.OUT}/trades_{n}_reverse_leg.csv"
        rows.append(dict(rule=n, instrument=r["instrument"], primary=n in ("A", "B", "C"), trades=h["trades"],
                         net_usd_per_trade=round(h["net_usd_per_trade"], 3), total_usd=round(h["total_usd"], 2),
                         gross_bp_per_trade=round(h["gross_bp_per_trade"], 3), net_bp_per_trade=round(h["net_bp_per_trade"], 3),
                         trades_per_year=round(h["trades_per_year"], 1), t=round(t, 3), passed=r["passed"],
                         criteria=[dict(name=c["name"], value=c["value"], **{"pass": c["pass_"]}) for c in r["criteria"]],
                         trades_csv=csv))
S["rule_table"] = rows
sc.dump("summary.json", S)
print(json.dumps(rows, indent=1))
