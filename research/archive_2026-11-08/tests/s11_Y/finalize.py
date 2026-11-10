import json, os
O = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(f"{O}/A_summary.json")); B = json.load(open(f"{O}/B_summary.json")); C = json.load(open(f"{O}/C_summary.json"))
OV = json.load(open(f"{O}/overlap_summary.json"))
spec = [("A", A["A"], "MNQ", True, "A_trades.csv"), ("A1-MES", A["A1"], "MES", False, "A1_trades.csv"),
        ("A2-VWAP", A["A2"], "MNQ", False, "A2_trades.csv"), ("B", B["B"], "MNQ", True, "B_trades.csv"),
        ("B-MES", B["B-MES"], "MES", False, "B-MES_trades.csv"), ("B1", B["B1"], "MNQ", False, "B1_trades.csv"),
        ("B1-MES", B["B1-MES"], "MES", False, "B1-MES_trades.csv"), ("C", C["C"], "MNQ", True, "C_reverse_leg_trades.csv"),
        ("C1", C["C1"], "MNQ", False, "C1_calm_reverse_leg_trades.csv"), ("C2", C["C2"], "MNQ", False, "C2_target_reverse_leg_trades.csv")]
rules = []
for nm, s, inst, prim, f in spec:
    h = s["headline"]
    t = s.get("t_day_nw5") if nm.startswith("A") else min(h["t_trade_plain"], h["t_trade_nw5"])
    rules.append(dict(rule=nm, instrument=inst, primary=prim, trades=h["trades"], net_usd_per_trade=round(h["net_usd_per_trade"], 3),
                      total_usd=round(h["total_usd"], 2), t=round(t, 3), gross_bp_per_trade=round(h["gross_bp_per_trade"], 3),
                      net_bp_per_trade=round(h["net_bp_per_trade"], 3), trades_per_year=round(h["trades_per_year"], 2),
                      criteria=[dict(name=c["name"], value=c["value"], **{"pass": c["passed"]}) for c in s["criteria"]],
                      passed=s["passed"], trades_csv=f"{O}/{f}"))
json.dump({"rules": rules, "A": A, "B": B, "C": C, "overlap": OV}, open(f"{O}/summary.json", "w"), indent=1)
print(json.dumps(rules, indent=0)[:200000])
