"""
v3/exp_G4/run_g4.py - runs the pre-registered G4 columns (PREREG.md A4, S4.1-S4.9, neighbours N4.1-N4.3, C3).
Light (v3/data only). Usage: python3 v3/exp_G4/run_g4.py [hid ...]   (default: all)
Writes v3/out/{daily,trades,results}/<hid>.*, v3/exp_G4/daily_<hid>.csv, v3/exp_G4/summary_<hid>.txt and logs every
column with H.log (module v3-<hid>).
"""
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H  # noqa: E402
import g4lib as G  # noqa: E402

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)

COLS = [
    # hid, tier, [(sym, fn)], seed id k, extra ticks, R, description
    ("A4", "A", [("NQ", G.release_fade())], 4, 0, 999, "CPI/NFP 08:30-08:45 move fade 08:45-09:45 MNQ"),
    ("S4.1", "B", [("NQ", G.release_fade("nfp"))], 41, 0, 999, "A4 NFP only MNQ"),
    ("S4.2", "B", [("NQ", G.release_fade("cpi"))], 42, 0, 999, "A4 CPI only MNQ"),
    ("S4.3", "B", [("NQ", G.release_fade(bigmove=True))], 43, 0, 999, "A4 big |m| (> expanding median) MNQ"),
    ("S4.4", "B", [("ES", G.release_fade())], 44, 0, 999, "A4 on MES"),
    ("S4.5", "B", [("YM", G.release_fade())], 45, 0, 999, "A4 on MYM (2018+)"),
    ("S4.6", "B", [("NQ", G.release_fade(stop_mult=2.0))], 46, 0, 999, "A4 + disaster stop 2|m| MNQ"),
    ("S4.7", "B", [("NQ", G.nfp_930_fade)], 47, 0, 999, "NFP 09:30 fade of 08:30-09:30 move, exit 16:00 MNQ"),
    ("S4.8", "B", [("ES", G.fomc_reversal), ("NQ", G.fomc_reversal), ("YM", G.fomc_reversal)], 48, 1, 999,
     "FOMC reversal basket: statement-15min vs prior session same mark, faded to 16:00 (+1 tick exit)"),
    ("S4.9_ES", "B", [("ES", G.announcement_long)], 491, 0, 999, "long 18:00-16:45 FOMC/NFP/CPI sessions MES"),
    ("S4.9_NQ", "B", [("NQ", G.announcement_long)], 492, 0, 999, "long 18:00-16:45 FOMC/NFP/CPI sessions MNQ"),
    ("S4.9_YM", "B", [("YM", G.announcement_long)], 493, 0, 999, "long 18:00-16:45 FOMC/NFP/CPI sessions MYM"),
    ("N4.1", "N", [("NQ", G.release_fade(exit_="0930"))], 401, 0, 999, "A4 neighbour: exit 09:30"),
    ("N4.2", "N", [("NQ", G.release_fade(exit_="1000"))], 402, 0, 999, "A4 neighbour: exit 10:00"),
    ("N4.3", "N", [("NQ", G.release_fade(sig=("0830", "0900"), entry="0900"))], 403, 0, 999,
     "A4 neighbour: signal 08:30-09:00, entry 09:00, exit 09:45"),
    ("E4.1", "X", [("NQ", G.release_fade_close844)], 404, 0, 999,
     "EXPLORATORY A4 with the signal on the 08:44 close (5-min bar 08:40-08:45), fill 08:45"),
    ("S4.8x", "X", [("ES", G.fomc_reversal_chained), ("NQ", G.fomc_reversal_chained),
                    ("YM", G.fomc_reversal_chained)], 481, 1, 999,
     "EXPLORATORY S4.8 incl. roll sessions (24h signal chained within contracts)"),
    ("C3", "C", [("NQ", G.release_fade("non"))], 409, 0, 100, "control C3: A4 rule on all non-release sessions MNQ"),
]


def run(hid, tier, legs, k, xt, R, desc):
    t0 = time.time()
    outs = []
    la = {}
    for sym, fn in legs:
        S = H.sessions(sym)
        ent = fn(S, {5: H.bars(sym, 5)})
        ent = ent[pd.DatetimeIndex(ent.session) <= G.END].reset_index(drop=True)
        # no-look-ahead: harness random cuts (20) + targeted cuts at 20 actual entry marks
        r = H.lookahead_check(fn, sym, n_cuts=20, seed=0, tfs=(5,))
        n_t = G.check_trunc(fn, sym, ent, n=20, seed=k)
        la[sym] = dict(random_cuts=int(r.same.sum()), targeted_cuts=n_t)
        outs.append(G.run_leg(sym, ent, k, R=R, extra_ticks=xt))
    n_eff = 9 if hid == "A4" else G.N_EFF_F2
    res = G.analyze(hid, outs, tier=tier, n_eff=n_eff, desc=desc,
                    params=dict(seed_k=k, extra_exit_ticks=xt, R=R, legs=[s for s, _ in legs]))
    res["lookahead"] = la
    tr = res["_trades"]
    # eval odds (descriptive): fixed 1/3/5 micros, 40% and 50% consistency
    ev = H.eval(tr.drop(columns=["c1", "c1_n", "d_i", "net_U2"]), sizing=[("fixed", 1), ("fixed", 3), ("fixed", 5)],
                calendar_=G.CAL)
    res["eval"] = ev.round(3).to_dict(orient="records")
    res["runtime_s"] = round(time.time() - t0, 1)
    # rewrite results json with eval + lookahead
    path = os.path.join(G.OUT, "results", f"{hid}.json")
    js = {k_: v for k_, v in res.items() if not k_.startswith("_")}
    with open(path, "w") as f:
        json.dump(js, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    # log the column
    scope = "+".join(G.MICRO[s] for s, _ in legs)
    if not os.environ.get("G4_NOLOG"):
      H.log(hid, scope, desc, trades=tr, baseline=float(tr.c1.mean()),
          params=dict(tier=tier, seed_k=k, R_C1=R, extra_exit_ticks=xt),
          note=(os.environ.get("G4_NOTE", "") + f"prereg sha256 {G.PREREG_SHA}; p_d={res['p_d']:.4f} p_net={res['p_net']:.4f} "
                f"t_d={res['t_d_nw']:.2f} t_net={res['t_net_nw']:.2f} d/trade={res['mean_d_per_trade']:.2f} "
                f"failed={res['failed_gates']} killed={res['killed']}"))
    # summary text
    lines = [f"{hid} [{tier}] {desc}", f"trades {res['n_trades']} ({res['trades_per_year']:.1f}/yr), "
             f"net/trade ${res['mean_net_per_trade']:.2f}, C1/trade ${res['mean_c1_per_trade']:.2f}, "
             f"d/trade ${res['mean_d_per_trade']:.2f}, gross/trade ${res['mean_gross_per_trade']:.2f}, "
             f"U2/trade ${res['mean_u2_per_trade']:.2f}, win {res['win_pct']:.1f}%",
             f"p_d {res['p_d']:.4f} {res['p_d_blocks']}  p_net {res['p_net']:.4f}  NW t(d) {res['t_d_nw']:.2f}  "
             f"NW t(net) {res['t_net_nw']:.2f}  Sharpe(ann) {res['sharpe_ann_net']:.2f}  DSR(d,N={n_eff}) "
             f"{res['dsr_d']:.3f}  mc_rank_p {res['mc_rank_p']:.3f}  gross/cost(2018+) {res['gross_over_cost_2018']:.2f}",
             f"net total ${res['net_total']:.0f}, w/o 10 best days ${res['net_wo_10_best_total']:.0f}; "
             f"cost +1 tick each way: ${res['cost_stress_plus1tick']['mean_per_trade']:.2f}/trade "
             f"(p {res['cost_stress_plus1tick']['p_net']:.3f})",
             "by window (per trade): " + json.dumps({w: {k_: round(v, 2) for k_, v in x.items()}
                                                     for w, x in res["by_window_per_trade"].items()}),
             "2-yr blocks: " + json.dumps({b: {k_: round(v, 1) for k_, v in x.items()} for b, x in res["blocks_2yr"].items()}),
             "by year net/trade: " + json.dumps({y: round(x["net"], 1) for y, x in res["by_year_per_trade"].items()}),
             "controls per trade: " + json.dumps({w: {k_: round(v, 2) for k_, v in x.items()}
                                                 for w, x in res["controls_per_trade"].items()}),
             "per market: " + json.dumps(res["per_market"]),
             f"gates failed: {res['failed_gates']}  killed: {res['killed']}  lookahead: {la}",
             "eval:", ev.to_string(index=False), f"runtime {res['runtime_s']} s"]
    txt = "\n".join(lines)
    with open(os.path.join(G.HERE, f"summary_{hid}.txt"), "w") as f:
        f.write(txt + "\n")
    print(txt, flush=True)
    return res


if __name__ == "__main__":
    want = set(sys.argv[1:])
    for c in COLS:
        if not want or c[0] in want:
            run(*c)
