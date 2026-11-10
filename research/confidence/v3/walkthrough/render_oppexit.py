"""Render the two opposite-evidence exit examples (ex12, ex13): 5-panel figure centred on the EXIT decision + decision
card (PNG + JSON). Inputs: opp_cache/<example_id>.pkl written by opp_prep.py (the v2 evidence code re-run on a
1-minute window, under the heavy lock), examples.csv, v2/out/v2_events_{sym}_60.parquet, v2/out/models_folds.csv.
Run from research/confidence:  python3 v3/walkthrough/render_oppexit.py [ex12 ex13]"""
import os
import pickle
import shutil
import sys

import numpy as np
import pandas as pd

import chart_style as cs
import mtf_chart as mc
from mtf_chart import COST, MICRO, USD, fp

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.abspath(os.path.join(HERE, "..", ".."))
EX = pd.read_csv(os.path.join(HERE, "examples.csv"),
                 parse_dates=["decision_time", "entry_time", "exit_time", "signal_bar", "hold_exit_time"])
SHORT = ["1 reversal candle against", "2 Momentum moved against the trade since the previous 60-min bar", "3 close wrong side of EMA20",
         "4 EMA8 wrong side of EMA20", "5 close beyond last swing", "6 60-min trend not with us",
         "7 5-min trigger other way"]
SRC_EV = "v2/dataset.py:221-237"


def render(r):
    pk = os.path.join(HERE, "opp_cache", f"{r.example_id}.pkl")
    if not os.path.exists(pk):            # fallback: v3-bar recompute (opp_prep.py with OPP_V3=1)
        pk = os.path.join(HERE, "opp_cache", f"{r.example_id}_v3.pkl")
    with open(pk, "rb") as f:
        P = pickle.load(f)
    import features as fe
    REVF = set(fe.FAMILIES["reversal"])
    for g in P["grid"]:                   # kind 1 counts only REVERSAL-family patterns (v2/dataset.py:142-144, :233)
        g["pats_against"] = [p for p in g["pats_against"] if p in REVF]
    sym, d = r.sym, P["d"]
    row = pd.Series(P["row"])
    G = P["grid"]
    first3 = P["first3"]
    dec = pd.Timestamp(first3["close"])                        # the exit decision: 60-min close where count hit 3
    rx, hx = P["rule_exit"], P["hold_exit"]
    if "v3" in str(P.get("mode")):
        hx = dict(hx, how=hx["how"].replace("1-minute walk", "5-min bar walk"))
    folds = pd.read_csv(os.path.join(CONF, "v2", "out", "models_folds.csv"))
    fy = str(r.signal_bar.year) if r.signal_bar < pd.Timestamp("2025-01-01") else "2025H1"
    fr = folds[(folds.cfg == "60|opp3_1b|M3|cls|exp") & (folds.fold.astype(str) == fy)].iloc[0]
    thr = float(fr.threshold)
    side_w = "LONG" if d > 0 else "SHORT"
    trade = dict(side=d, entry_time=r.entry_time, entry_px=P["entry"], stop=P["stop"], exit_time=rx["t"],
                 exit_px=rx["px"], pnl=rx["pnl"],
                 extra=[dict(time=hx["t"], px=hx["px"], color="#ffffff", marker="D")])
    i_sig_close = r.signal_bar + pd.Timedelta(minutes=60)

    def hold_tag(ax, X, dy=40):
        xh = X(hx["t"])
        if np.isfinite(xh):
            ax.annotate(f"if HELD: {fp(sym, hx['px'])} at {hx['t']:%H:%M}\n{hx['pnl']:+.2f} $ ({'stop' if 'stop' in hx['how'] else '16:00 flat'})",
                        (xh, hx["px"]), xytext=(-20, dy), textcoords="offset points", ha="right", color="#ffffff",
                        fontsize=11.5, fontweight="bold", zorder=12, arrowprops=dict(arrowstyle="-", color="#ffffff"),
                        bbox=dict(boxstyle="round,pad=0.2", fc="#222244", ec="#ffffff", lw=0.8))

    def ov60(ax, axm, B, X):
        tr = ax.get_xaxis_transform()
        xs = X.i(r.signal_bar)
        if 0 <= xs < len(B):
            ax.axvspan(xs - 0.5, xs + 0.5, color="#3a3a10", alpha=0.7, zorder=0)
            ax.text(xs, 0.06, f"signal bar\n{r.signal_bar:%H:%M}", transform=tr, color=cs.HILITE, fontsize=10.5,
                    ha="center")
        # zoom inset: signal bar .. hold exit, evidence count above every 60-min bar
        z0 = max(0, X.i(r.signal_bar) - 3)
        z1 = min(len(B), X.i(hx["t"]) + 3)
        Z = B.iloc[z0:z1]
        import matplotlib.patches as mpatches
        ax.add_patch(mpatches.Rectangle((0.0, 0.24), 0.62, 0.76, transform=ax.transAxes, color=cs.BG, zorder=19,
                                        ec=cs.EXITC, lw=1.0))
        ai = ax.inset_axes([0.045, 0.43, 0.56, 0.50])
        ai.set_zorder(20)
        ai.set_facecolor("#050505")
        for sp in ai.spines.values():
            sp.set_color(cs.EXITC)
        zx = np.arange(len(Z))
        zc = np.where(Z.C >= Z.O, cs.UP, cs.DN)
        ai.vlines(zx, Z.L, Z.H, color=zc, lw=1.2)
        ai.bar(zx, (Z.C - Z.O).where((Z.C - Z.O).abs() > 0, 1e-9), bottom=Z.O, width=0.6, color=zc)
        for e in (8, 20):
            ai.plot(zx, Z[f"ema{e}"], color=cs.EMA_STYLE[e]["color"], lw=1.4, ls=(0, (5, 3)))
        zt = list(Z.index)
        lo, hi = float(Z.L.min()), float(Z.H.max())
        span = hi - lo
        ai.set_ylim(lo - span * 0.12, hi + span * 0.42)
        for g in G:
            if g["bar"] not in zt:
                continue
            k = zt.index(g["bar"])
            c = g["c1"]
            if g["bar"] == r.signal_bar:
                ai.text(k, hi + span * 0.30, "signal", color=cs.HILITE, fontsize=10, ha="center")
                continue
            colr = cs.BAD if c >= 3 else ("#ffa500" if c == 2 else cs.TXT)
            ai.text(k, hi + span * 0.16, str(c), color=colr, fontsize=14, fontweight="bold", ha="center")
        kx = zt.index(first3["bar"])
        ai.axvline(kx + 0.5, color=cs.EXITC, lw=1.6, ls="--")
        ai.plot(zt.index(r.signal_bar) + 1 - 0.5, P["entry"], ">", color=cs.HILITE, ms=11, mec="#000")
        ai.plot(kx + 0.5, rx["px"], "X", color="#ffffff", mec=cs.EXITC, ms=12)
        ai.hlines(P["stop"], zt.index(r.signal_bar) + 0.5, len(Z) - 0.5, color=cs.BAD, lw=1.5)
        xh = (hx["t"] - zt[0]) / pd.Timedelta(minutes=60) - 0.5
        ai.plot(xh, hx["px"], "D", color="#ffffff", ms=9)
        kinds = [SHORT[k].replace(" the trade since the previous 60-min bar", "") for k in range(7) if first3["ev"][k]]
        ai.set_xlabel(f"{first3['c1']} against at the {dec:%H:%M} close: " + "; ".join(k_[2:] for k_ in kinds)
                      + f"\n-> exit {fp(sym, rx['px'])} = {rx['pnl']:+.2f} $   (white diamond = if held: {hx['pnl']:+.2f} $)",
                      color=cs.EXITC, fontsize=10.5, fontweight="bold", labelpad=2)
        ai.set_xticks(zx[::2])
        ai.set_xticklabels([f"{t_:%H:%M}" for t_ in Z.index[::2]], color=cs.TXT2, fontsize=9.5)
        ai.tick_params(axis="y", colors=cs.TXT2, labelsize=9.5)
        ai.set_title("ZOOM, 60-min bars: number = opposite-evidence count (of 7) at that bar's close", color=cs.EXITC, fontsize=11.5, pad=3)
        ax.indicate_inset([z0 - 0.5, lo, z1 - z0, span], ai, edgecolor=cs.EXITC, alpha=0.6)
        xd = X(dec)
        sw = "swing_lo" if d > 0 else "swing_hi"
        lv = first3[sw]
        if np.isfinite(lv):
            ax.hlines(lv, X.i(r.entry_time) - 0.5, xd, color="#7fd6ff", lw=1.6, ls="--", zorder=8)
            ax.text(X.i(r.entry_time) - 0.5, lv, f"last confirmed swing {'low' if d > 0 else 'high'} {fp(sym, lv)} ",
                    color="#7fd6ff", fontsize=10.5, ha="right", va="center", zorder=12)

    def ov15(ax, axm, B, X):
        hold_tag(ax, X)

    def ov5(ax, axm, B, X):
        for g in G:
            for t_ in g["trig5_times"]:
                xi = X(pd.Timestamp(t_) + pd.Timedelta(minutes=5))
                if np.isfinite(xi):
                    ax.axvline(xi - 0.5, color="#ff8c00", lw=1.0, ls=":", zorder=5)
        ax.text(0.005, 0.86, "orange dotted = a 5-min pullback trigger fired the OTHER way (evidence kind 7, counted on "
                "the 60-min bar that contains it)", transform=ax.transAxes, color="#ff8c00", fontsize=10.5, zorder=12)
        hold_tag(ax, X)

    used = {1: (False, "NOT used for the decision; the stop is checked on these 1-minute bars"),
            5: (True, "USED for evidence kind 7 (5-min triggers the other way) and entry inputs"),
            15: (True, "used only for the ENTRY inputs (15-min features); not for the exit count"),
            60: (True, "USED: base chart. Entry signal + the 7-kind evidence count at every 60-min close"),
            120: (False, "NOT used (context only)")}
    title = (f"{r.example_id}: {MICRO[sym]} {side_w} exit {dec:%Y-%m-%d %H:%M}  ->  "
             f"{rx['pnl']:+.2f} $ (hold: {hx['pnl']:+.2f} $)")
    sub = (f"{r.category}. Config A = v2 M3 score on 60-min bars (score {r.score:.3f} vs {fy} threshold {thr:.3f} -> kept), "
           f"exit opp3_1b: leave at the next 60-min open once 3 of 7 kinds of evidence point against the trade on one "
           f"bar. 'decision' = the EXIT decision. Picked by: {r.selection_rule}, {r.seed}.")
    png = os.path.join(mc.OUTD, f"{r.example_id}_chart.png")
    mc.mtf_figure(png, r.example_id, sym, dec, trade, title, sub, used, overlays={60: ov60, 15: ov15, 5: ov5},
                  extend_to=pd.Timestamp(hx["t"]),
                  panel_notes={60: f"entry {r.entry_time:%H:%M} {fp(sym, P['entry'])}, stop {fp(sym, P['stop'])}\n"
                                   f"held {int((dec - r.entry_time) / pd.Timedelta(hours=1))} h before the exit decision"})
    # ------------------------------------------------------------------ card
    inputs = []
    for k in range(7):
        on = first3["ev"][k]
        extra = ""
        if k == 0 and first3["pats_against"]:
            extra = " (" + ", ".join(first3["pats_against"]) + ")"
        if k == 6 and first3["trig5_against"]:
            extra = " (" + ", ".join(first3["trig5_against"]) + ")"
        inputs.append(dict(plain=f"kind {SHORT[k]}{extra}", value="YES" if on else "no",
                           read="against" if on else "neutral", where=SRC_EV))
    detail = [("close", first3["C"]), ("EMA20", first3["ema20"]), ("EMA8", first3["ema8"]),
              ("Momentum(14) now", first3["mom"]),
              (f"last confirmed swing {'low' if d > 0 else 'high'}", first3["swing_lo" if d > 0 else "swing_hi"]),
              ("latest closed 60-min trend (+1 up, -1 down, 0 none)", first3["t60"])]
    for nm, v in detail:
        vs = ({1: "+1 (up)", -1: "-1 (down)", 0: "0 (none)"}.get(int(v), f"{v:.0f}") if "trend" in nm
              else f"{float(v):.2f}" if "Momentum" in nm else float(v))
        inputs.append(dict(plain=f"{first3['bar']:%H:%M} bar: {nm}", value=vs, read="info", where="signals.py:92-116"))
    for g in G:
        if g["bar"] > first3["bar"]:
            break
        tag = "signal bar" if g["bar"] == r.signal_bar else f"{g['bar']:%H:%M}-{g['close']:%H:%M}"
        ks = ",".join(str(k + 1) for k in range(7) if g["ev"][k]) or "-"
        inputs.append(dict(plain=f"count at {tag} close (kinds {ks})", value=f"{g['c1']} of 7",
                           read="against" if g["c1"] >= 3 else "neutral",
                           where="not checked (signal bar)" if g["bar"] == r.signal_bar else "exit if >= 3"))
    saved = rx["pnl"] - hx["pnl"]
    right = saved > 0
    why = ((f"Price kept going against the {side_w.lower()} after the exit and {'hit the stop' if 'stop' in hx['how'] else 'was worse at 16:00'}; "
            f"leaving on the evidence count cut the loss by {saved:.2f} $.") if right else
           (f"The evidence was a pause, not a reversal: after the exit the trend resumed and holding to 16:00 would have "
            f"made {hx['pnl']:+.2f} $, so the exit gave up {-saved:.2f} $."))
    card = dict(title=f"DECISION CARD  {r.example_id}  {MICRO[sym]} {side_w}  exit decision {dec:%Y-%m-%d %H:%M}",
                decision=f"Opposite evidence {first3['c1']} of 7 >= N=3 at the {dec:%H:%M} close  ->  EXIT at the next "
                         f"60-min open {fp(sym, rx['px'])} (entered {r.entry_time:%H:%M} at {fp(sym, P['entry'])})",
                drivers=[f"Entry: Config A kept the {r.signal_bar:%H:%M} 60-min signal ({', '.join(k for k in ['pb','ema8_pb','ema20_pb','ema50_pb','mom_turn','pb_break'] if row[k] == 1)}) "
                         f"with score {r.score:.3f} >= {fy} threshold {thr:.3f}; stop {fp(sym, P['stop'])}.",
                         "Exit: at each 60-min close the 7 kinds below are checked against the trade; this bar only "
                         "(_1b). 3 or more = leave at the next bar's first-minute open; the stop stays live meanwhile.",
                         "Kinds that fired at the exit bar: " + ", ".join(SHORT[k] for k in range(7) if first3["ev"][k])],
                outcome=f"OUTCOME: rule exit {rx['pnl']:+.2f} $ vs hold {hx['pnl']:+.2f} $ ({'stopped' if 'stop' in hx['how'] else 'flat'} {hx['t']:%H:%M}) "
                        f"-> exit {'saved' if right else 'gave up'} {abs(saved):.2f} $ = {'RIGHT' if right else 'WRONG'}",
                why=why, win=right,
                notes=[f"Recomputed with v2/dataset.py load_frames + evidence_types; data: {P.get('mode')} (stop first, +1 tick). Stored labels (v2_events_{sym}_60): opp3_1b "
                       f"{row['pnl_opp3_1b']:+.2f} $ exit {pd.Timestamp(row['t_exit_opp3_1b']):%H:%M}, hold "
                       f"{row['pnl_hold']:+.2f} $ exit {pd.Timestamp(row['t_exit_hold']):%H:%M}. Costs ${COST[sym]:.2f}/trade."],
                inputs=inputs, example=r.example_id,
                grid=[{**{k: v for k, v in g.items() if k not in ("ev",)},
                       **{SHORT[k]: g["ev"][k] for k in range(7)}} for g in G],
                rule_exit=rx, hold_exit=hx, threshold=thr)
    cpng = os.path.join(mc.OUTD, f"{r.example_id}_card.png")
    mc.decision_card(cpng, card)
    return png, cpng, card


def publish(ex_id, png, cpng):
    """copy to the names the task asked for: ex_<n>_mtf.png / ex_<n>_card.png (walkthrough root) + cards/ex_<n>_card.json"""
    n = ex_id[2:4]
    shutil.copy(png, os.path.join(HERE, f"ex_{n}_mtf.png"))
    shutil.copy(cpng, os.path.join(HERE, f"ex_{n}_card.png"))
    shutil.copy(os.path.splitext(cpng)[0] + ".json", os.path.join(HERE, "cards", f"ex_{n}_card.json"))


if __name__ == "__main__":
    want = sys.argv[1:] or ["ex12", "ex13", "ex14", "ex15"]
    for r in EX.itertuples():
        if not any(r.example_id.startswith(w) for w in want):
            continue
        if "oppexit" in r.example_id:
            png, cpng, card = render(r)
        else:            # A1 days: rendered by render_examples.render_a1; just publish under the task's names
            png = os.path.join(mc.OUTD, f"{r.example_id}_chart.png")
            cpng = os.path.join(mc.OUTD, f"{r.example_id}_card.png")
        publish(r.example_id, png, cpng)
        print(r.example_id, png, flush=True)
