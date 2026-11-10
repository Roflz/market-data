"""G1 finalize: adds the pre-registered labels (PREREG 0.4/0.5) to v3/out/results/<hid>.json.
A1: Holm at alpha 0.03, K = 6, on p_d. With the other Tier A p_d values available now (A2..A5; P0 is computed at
synthesis), A1 has the smallest p_d; even if P0 were smaller A1's Holm threshold would be 0.006, so the Holm decision
for A1 is fixed (Holm-adjusted p <= 6 x p_d). Secondaries: Tier B with the G1-only StepM (tierB_G1.csv) - the binding
F3 StepM over all F3 secondary columns is the synthesis step."""
import glob
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "out", "results")
pa = {}
for k in ("A1", "A2", "A3", "A4", "A5", "P0"):
    p = os.path.join(OUT, f"{k}.json")
    if os.path.exists(p):
        pa[k] = json.load(open(p)).get("p_d")
r = json.load(open(os.path.join(OUT, "A1.json")))
ranked = sorted([(v, k) for k, v in pa.items() if v is not None])
rank = [k for _, k in ranked].index("A1")
thr = 0.03 / (6 - rank)
holm_reject = r["p_d"] <= thr and all(v <= 0.03 / (6 - i) for i, (v, _) in enumerate(ranked[:rank]))
worst_case_thr = 0.03 / 5                                # if P0 (unknown yet) had a smaller p_d
fails = list(r["failed_gates"])
if not holm_reject:
    fails.append("Holm")
if r["p_net"] > 0.05:
    fails.append("intersection p_net > 0.05")
label = ("SIGNIFICANT" if not fails else
         "PROMISING" if (r["t_nw_d"] >= 2 and len(fails) <= 2) else "NOT SIGNIFICANT")
if r["kill"]:
    label = "KILLED"
hc = pd.read_csv(os.path.join(HERE, "handcheck_10.csv"))
r.update(label=label, holm=dict(tierA_p_d_now=pa, rank=rank + 1, threshold=thr, reject=bool(holm_reject),
                                 worst_case_threshold_if_P0_smaller=worst_case_thr,
                                 holm_adjusted_p_upper_bound=min(1.0, 6 * r["p_d"])),
         failed_all=fails,
         handcheck=dict(n=len(hc), prices_match=int(hc.px_match.sum()), signals_match=int(hc.signal_match.sum())),
         lookahead="H.lookahead_check 20 cuts on the decision legs (A1, S1.1, S1.2, S1.6, N1.hour, S1.4): OK; "
                   "merged A1 trades re-built on data truncated at their exit mark: 20/20 identical")
json.dump(r, open(os.path.join(OUT, "A1.json"), "w"), indent=1, default=str)
print("A1", label, r["holm"])
tb = pd.read_csv(os.path.join(HERE, "tierB_G1.csv")).set_index("col")
for c in tb.index:
    p = os.path.join(OUT, f"{c}.json")
    x = json.load(open(p))
    row = tb.loc[c]
    if x["kill"]:
        lab = "KILLED"
    elif row.tierB_pass_prelim:
        lab = "TIER B PASS (prelim, G1-only StepM)"
    else:
        lab = "descriptive (Tier B not met)"
    if x["kind"] == "neighbour":
        lab = f"neighbour: same sign as A1 = {bool(row.same_sign_as_A1)}"
    x.update(label=lab, tierB=dict(stepm_p_G1=row.stepm_p_G1, dsr45=row.dsr45, t_nw_d=row.t_nw_d,
                                   p_net=row.p_net, pass_prelim=bool(row.tierB_pass_prelim)))
    json.dump(x, open(p, "w"), indent=1, default=str)
    print(c, lab)
