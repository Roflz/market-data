"""Print a compact digest of every G5 result json (for the group report). Light."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness as H   # noqa: E402
import g5             # noqa: E402

for c in g5.COL_LIST:
    p = os.path.join(H.HERE, "out", "results", f"{c}.json")
    if not os.path.exists(p):
        print(c, "missing"); continue
    r = json.load(open(p))
    wn = {k: (float('nan') if v is None else v) for k, v in r["windows_net_trade"].items()}
    ev = r.get("eval")
    evs = ""
    if isinstance(ev, list):
        for e in ev:
            if e["consistency"] == 0.4 and e["window"] == "2018+":
                evs += (f" | {e['policy']}: pass {e['pass_pct']:.0f}% w10 {e['within_10']:.1f}% bust {e['bust_pct']:.0f}%"
                        + (f" (luck w10 {e['luck_within_10']:.1f})" if e.get("luck_within_10") is not None else ""))
    lab = r.get("tierB", {}).get("label") or r.get("tierA", {}).get("label")
    print(f"{c}: n {r['n_trades']} ({r['trades_per_year']:.0f}/yr) net/tr {r['usd_per_trade']:.2f} d/tr {r['d_per_trade']:.2f} "
          f"C1/tr {r['ctrl_C1_per_trade']:.2f} t_d {r['t_nw_d']:.2f} p_d {r['p_d']:.4f} t_net {r['t_nw_net']:.2f} "
          f"p_net {r['p_net']:.3f} | 10-17 {wn['2010-17']:.2f} 18-25 {wn['2018-25H1']:.2f} 22+ {wn['2022+']:.2f} "
          f"wo10 {r['net_wo_top10_per_trade']:.2f} stress {r['stress']['usd_per_trade']:.2f} drift {r['drift_per_trade']:.2f} "
          f"hdrift {r['hour_drift_per_trade']:.2f} mc_p {r['mc_rank_p']:.3f} fails {r['failed_gates']} kill {r['kill']} "
          f"label {lab}{evs}")
    if "legs" in r and c.startswith("A5"):
        print("   legs:", {k: (v['n'], round(v['usd_per_trade'], 2), round(v['d_per_trade'], 2)) for k, v in r['legs'].items()})
    if len(r["markets"]) > 1:
        print("   per market $/tr:", {k: round(v["usd_per_trade"], 2) for k, v in r["per_market"].items()},
              "d/tr:", {k: round(v["d_per_trade"], 2) for k, v in r["per_market"].items()})
