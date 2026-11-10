"""
v3/signal_lab/reverse_confirm.py - the ONE confirmation run of the frozen reverse-engineered candidates
(out/reverse_candidates.md) on 2018-01-01 .. 2025-06-30 sessions only (ES, NQ, YM 15-min), signal lab v1.1.
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness as H  # noqa: E402
import lab as L  # noqa: E402
import reverse_signals as RS  # noqa: E402

OUT = os.path.join(HERE, "out", "reverse", "confirm")
START = pd.Timestamp("2018-01-01")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    panels = {}
    for sym in ("ES", "NQ", "YM"):
        b = H.bars(sym, 15)
        b = b[pd.DatetimeIndex(b.session) >= START]
        assert b.index.max() < H.HOLDOUT_SESSION_START
        panels[(sym, 15)] = L.Panel(b, sym, 15)
    sig = {k: dict(fn=v["fn"], kind=v["kind"], desc=v["desc"]) for k, v in RS.CANDIDATES.items()}
    batch, res = L.evaluate_many(sig, panels=panels, out_dir=OUT, log_tag="reverse-confirm")
    # pre-registered checks: sign and primary hold
    rows = []
    for r in res:
        c = RS.CANDIDATES[r["name"]]
        t = r["table"]
        hold = c["hold"]
        rows.append(dict(metric=r["name"], market=r["sym"], claim=c["claim"], exp_sign=c["sign"], hold=hold,
                         hold_effect=t.at[hold, "effect"], hold_lo=t.at[hold, "ci_lo"], hold_hi=t.at[hold, "ci_hi"],
                         hold_p=t.at[hold, "p"] if "p" in t else np.nan,
                         hold_usd=t.at[hold, "trade_usd_B"] if "trade_usd_B" in t else np.nan))
    pre = pd.DataFrame(rows)
    out = batch.merge(pre, on=["metric", "market"])
    out["dir_sign_ok"] = np.sign(out.dir_effect) == out.exp_sign
    out["size_sign_ok"] = np.sign(out.size_effect) == out.exp_sign
    out["survived"] = np.where(out.claim == "direction", (out.dir_verdict == "CONFIRMED") & out.dir_sign_ok,
                               (out.size_verdict == "CONFIRMED") & out.size_sign_ok)
    out.to_csv(os.path.join(OUT, "confirm_summary.csv"), index=False)
    pd.set_option("display.width", 250, "display.max_columns", 40, "display.max_rows", 100)
    print(out[["metric", "market", "claim", "exp_sign", "best_dir", "dir_effect", "q_dir", "dir_verdict", "dir_class",
               "edge_usd_B", "edge_usd_B_lo80", "cost_usd", "best_size", "size_effect", "size_pct", "q_size",
               "size_verdict", "hold", "hold_effect", "hold_lo", "hold_hi", "hold_usd", "lookahead", "survived"]]
          .round(4).to_string(index=False))
