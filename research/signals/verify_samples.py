"""
Pattern verification samples: for 10 classic candle patterns, re-check every rule condition of every detection and
measure HOW CLOSE each condition came to failing (its margin, in fractions of an average bar's range). Then show, per
pattern, a textbook reference drawing next to three real detections: a clean one (top 10% margin), a typical one
(middle) and THE most borderline one we claim. Under each sample, every rule condition with its actual numbers; the
tightest condition is highlighted.
Also an exactness check: the conditions re-implemented here must reproduce the detector's output on every bar.
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../../pylib:../..:. python3 verify_samples.py [SYM] [TF]
Writes verify/patterns_N.html
"""
import base64
import warnings
import html
import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

import chart_style as cs
import signals as sg

warnings.filterwarnings("ignore")
SYM = sys.argv[1] if len(sys.argv) > 1 else "NQ"
TF = int(sys.argv[2]) if len(sys.argv) > 2 else 15
OUT = "verify"; os.makedirs(OUT, exist_ok=True)
rng_ = np.random.default_rng(3)
spec = sg.SPEC[SYM]
b = sg.bars(SYM, TF); c = sg.context(b, tick=spec["tick"]); p = sg.patterns(b, c, tick=spec["tick"])
O, H, L, C = (b[x].to_numpy() for x in "OHLC")
seg = b.seg.to_numpy(); runa = b.run.to_numpy(); n = len(b)
body = np.abs(C - O); rngb = H - L
up = H - np.maximum(O, C); lo = np.minimum(O, C) - L


def prev(a, k=1):
    out = np.full(n, np.nan); out[k:] = a[:-k]; return out


def avg_before(a, w, lag=1):
    s = pd.Series(a).shift(lag).rolling(w).mean().to_numpy()
    same = np.r_[np.zeros(w + lag - 1, bool), runa[w + lag - 1:] == runa[:-(w + lag - 1)]]
    return np.where(same, s, np.nan)


def same_seg(k):
    out = np.zeros(n, bool); out[k:] = seg[k:] == seg[:-k]; return out


avgB10, avgR10 = avg_before(body, 10), avg_before(rngb, 10)
avgB10_1, avgB10_2 = avg_before(body, 10, 2), avg_before(body, 10, 3)
ema10 = c.ema10.to_numpy()
O1, H1, L1, C1 = prev(O), prev(H), prev(L), prev(C)
O2, C2 = prev(O, 2), prev(C, 2)
body1, body2 = np.abs(C1 - O1), np.abs(C2 - O2)
up1 = prev(up); up2 = prev(up, 2)
ema10_1, ema10_2 = prev(ema10), prev(ema10, 2)
mid1 = (O1 + C1) / 2
s1, s2 = same_seg(1), same_seg(2)
R = avgR10                                    # "an average bar" = mean range of the 10 bars before

# a condition: (plain-English label, left side, op, right side). Margin = how far it passes, in average-bar units.
def cond(label, lhs, op, rhs):
    return dict(label=label, lhs=np.asarray(lhs, float), op=op, rhs=np.asarray(rhs, float))


PATTERNS = [
    ("hammer", 1, "Hammer (bullish)", 1, [
        cond("Bar range at least the 10-bar average range", rngb, ">=", avgR10),
        cond("Lower wick at least 2x the body", lo, ">=", 2 * body),
        cond("Upper wick at most 10% of the range", up, "<=", 0.1 * rngb),
        cond("Prior bar closed below EMA 10 (after a decline)", C1, "<", ema10_1)]),
    ("shooting_star", -1, "Shooting star (bearish)", 1, [
        cond("Bar range at least the 10-bar average range", rngb, ">=", avgR10),
        cond("Upper wick at least 2x the body", up, ">=", 2 * body),
        cond("Lower wick at most 10% of the range", lo, "<=", 0.1 * rngb),
        cond("Prior bar closed above EMA 10 (after a rise)", C1, ">", ema10_1)]),
    ("engulfing", 1, "Bullish engulfing", 2, [
        cond("Bar 1 is a down bar", C1, "<", O1),
        cond("Bar 2 is an up bar", C, ">", O),
        cond("Bar 2 opens at or below bar 1's close", O, "<=", C1),
        cond("Bar 2 closes at or above bar 1's open", C, ">=", O1),
        cond("Engulfs strictly on at least one side", np.maximum(C1 - O, C - O1), ">", 0 * O),
        cond("Bar 2 body bigger than the 10-bar average body", body, ">", avgB10),
        cond("Bar 1 closed below EMA 10 (after a decline)", C1, "<", ema10_1)]),
    ("harami", 1, "Bullish harami", 2, [
        cond("Bar 1 is a down bar", C1, "<", O1),
        cond("Bar 1 body bigger than its 10-bar average body", body1, ">", avgB10_1),
        cond("Bar 2 body no bigger than the 10-bar average body", body, "<=", avgB10),
        cond("Bar 2 body top below bar 1 body top", np.maximum(O, C), "<", np.maximum(O1, C1)),
        cond("Bar 2 body bottom above bar 1 body bottom", np.minimum(O, C), ">", np.minimum(O1, C1)),
        cond("Bar 1 closed below EMA 10 (after a decline)", C1, "<", ema10_1)]),
    ("piercing", 1, "Piercing line (bullish)", 2, [
        cond("Bar 1 is a down bar", C1, "<", O1),
        cond("Bar 1 body bigger than its 10-bar average body", body1, ">", avgB10_1),
        cond("Bar 2 is an up bar", C, ">", O),
        cond("Bar 2 opens at or below bar 1's close", O, "<=", C1),
        cond("Bar 2 closes above the middle of bar 1's body", C, ">", mid1),
        cond("Bar 2 closes below bar 1's open", C, "<", O1)]),
    ("dark_cloud", -1, "Dark cloud cover (bearish)", 2, [
        cond("Bar 1 is an up bar", C1, ">", O1),
        cond("Bar 1 body bigger than its 10-bar average body", body1, ">", avgB10_1),
        cond("Bar 2 is a down bar", C, "<", O),
        cond("Bar 2 opens at or above bar 1's close", O, ">=", C1),
        cond("Bar 2 closes below the middle of bar 1's body", C, "<", mid1),
        cond("Bar 2 closes above bar 1's open", C, ">", O1)]),
    ("morning_evening_star", 1, "Morning star (bullish)", 3, [
        cond("Bar 1 is a down bar", C2, "<", O2),
        cond("Bar 1 body bigger than its 10-bar average body", body2, ">", avgB10_2),
        cond("Bar 2 body no bigger than its 10-bar average body", body1, "<=", avgB10_1),
        cond("Bar 2 body sits entirely below bar 1's body (gap)", np.maximum(O1, C1), "<", np.minimum(O2, C2)),
        cond("Bar 3 is an up bar", C, ">", O),
        cond("Bar 3 body bigger than the 10-bar average body", body, ">", avgB10),
        cond("Bar 3 closes over 30% into bar 1's body", C, ">", C2 + 0.3 * body2),
        cond("Bar 1 closed below EMA 10 (after a decline)", C2, "<", ema10_2)]),
    ("three_soldiers_crows", 1, "Three white soldiers (bullish)", 3, None),   # built below
    ("pin_bar", 1, "Bullish pin bar", 1, [
        cond("Bar range at least the 10-bar average range", rngb, ">=", avgR10),
        cond("Lower wick at least 2/3 of the range", lo, ">=", 2 / 3 * rngb),
        cond("Upper wick under 2/3 of the range (rules out flat, zero-range bars)", up, "<", 2 / 3 * rngb)]),
    ("tweezer", 1, "Tweezer bottom (bullish)", 2, [
        cond("Lows within 5% of an average bar of each other", np.abs(L - L1), "<=", 0.05 * avgR10),
        cond("Bar 1 is a down bar", C1, "<", O1),
        cond("Bar 2 is an up bar", C, ">", O),
        cond("Bar 1 closed below EMA 10 (after a decline)", C1, "<", ema10_1)]),
]
# three white soldiers: each of the 3 bars up, body > half the average body, small upper wick; each opens inside the
# previous body and closes higher
ts = []
for k, nm in ((2, "1"), (1, "2"), (0, "3")):
    Ok, Ck = (prev(O, k), prev(C, k)) if k else (O, C)
    bk = np.abs(Ck - Ok); shk = prev(up, k) if k else up
    ab = prev(avgB10, k) if k else avgB10
    ts += [cond(f"Bar {nm} is an up bar", Ck, ">", Ok),
           cond(f"Bar {nm} body more than half the 10-bar average body", bk, ">", 0.5 * ab),
           cond(f"Bar {nm} upper wick at most 30% of its body", shk, "<=", 0.3 * bk)]
    if k < 2:
        Ck1, Ok1 = prev(C, k + 1), prev(O, k + 1)
        ts += [cond(f"Bar {nm} closes above bar {int(nm) - 1}'s close", Ck, ">", Ck1),
               cond(f"Bar {nm} opens at/above bar {int(nm) - 1}'s body bottom", Ok, ">=", np.minimum(Ok1, Ck1)),
               cond(f"Bar {nm} opens at/below bar {int(nm) - 1}'s body top", Ok, "<=", np.maximum(Ok1, Ck1))]
PATTERNS[7] = ("three_soldiers_crows", 1, "Three white soldiers (bullish)", 3, ts)
SAMEBARS = {1: s1, 2: s1, 3: s2}


def margins(conds):
    """per condition: signed margin in average-bar units (>= 0 passes for non-strict, > 0 for strict)."""
    M, PASS = [], []
    for cd in conds:
        d = (cd["lhs"] - cd["rhs"]) if cd["op"] in (">=", ">") else (cd["rhs"] - cd["lhs"])
        m = d / R
        ok = (d > 0) if cd["op"] in (">", "<") else (d >= 0)
        M.append(m); PASS.append(ok & np.isfinite(d) & np.isfinite(R))
    return np.vstack(M), np.vstack(PASS)


# ------------------------------------------------------------------ exactness check + sample picks
results = []
for name, d0, title, span, conds in PATTERNS:
    M, PASS = margins(conds)
    mine = PASS.all(axis=0) & (SAMEBARS[span] if name != "pin_bar" else True)   # pin bar: single bar, no session check
    if name in ("hammer", "shooting_star", "tweezer"):
        mine &= s1
    live = (rngb > 0) & (avgR10 > 0)                      # hard requirement: no flat bars, no dead market
    for j in range(1, span):
        live &= np.r_[np.zeros(j, bool), (rngb > 0)[:-j]]
    mine &= live
    det = p[name].to_numpy() == d0
    agree = (mine == det)
    mm = np.where(np.isfinite(M), M, np.inf).min(axis=0)       # tightest condition's margin
    idx = np.flatnonzero(det & mine)
    idx = idx[(idx > 20) & (idx < n - 6)]
    order = idx[np.argsort(mm[idx])]
    k = len(order)
    pick = {"Clean (top 10% margin)": order[rng_.integers(int(k * 0.9), k)],
            "Typical (middle)": order[rng_.integers(int(k * 0.45), int(k * 0.55))],
            "Most borderline we claim": order[0]}
    results.append(dict(name=name, d=d0, title=title, span=span, conds=conds, M=M, mm=mm, pick=pick,
                        n_det=int(det.sum()), n_mine=int(mine.sum()), n_disagree=int((~agree).sum()),
                        disagree_idx=np.flatnonzero(~agree)[:5],
                        q=np.percentile(mm[idx], [2, 10, 50, 90]) if k else None))
    print(f"{name:22s} detected {det.sum():7,d}  re-checked {mine.sum():7,d}  disagree {(~agree).sum():,d}", flush=True)

# ------------------------------------------------------------------ drawings
REF = {   # textbook reference shapes (O, H, L, C); last `span` bars are the pattern
    "hammer": [(110, 111, 106, 107), (107, 108, 103, 104), (104, 105, 100, 101), (100.5, 101.6, 93, 101.3)],
    "shooting_star": [(90, 94, 89, 93), (93, 97, 92, 96), (96, 100, 95, 99), (99.5, 107, 98.9, 99.2)],
    "engulfing": [(110, 111, 105, 106), (106, 107, 102, 103), (103, 103.5, 100, 101), (100.5, 106, 100, 105)],
    "harami": [(110, 111, 106, 107), (107, 108, 103, 104), (104, 104.5, 96, 97), (99, 101.5, 98.5, 101)],
    "piercing": [(110, 111, 106, 107), (107, 108, 103, 104), (104, 104.5, 97, 98), (97, 102.5, 96, 102)],
    "dark_cloud": [(90, 94, 89, 93), (93, 97, 92, 96), (96, 103.5, 95.5, 103), (104, 105, 98, 99)],
    "morning_evening_star": [(110, 111, 106, 107), (107, 107.5, 100, 101), (99, 99.8, 97.5, 98.6), (99.5, 106, 99, 105)],
    "three_soldiers_crows": [(104, 105, 100, 101), (101, 102, 99, 100), (100, 103.4, 99.6, 103), (102, 106.4, 101.6, 106),
                             (105, 109.4, 104.6, 109)],
    "pin_bar": [(110, 111, 106, 107), (107, 108, 103, 104), (104, 105, 100, 101), (100.8, 101.6, 92, 101.2)],
    "tweezer": [(110, 111, 106, 107), (107, 108, 103, 104), (104, 104.5, 99, 100), (100.2, 104, 99, 103.5)],
}
DESC = {
    "hammer": "After a decline: a bar with a small body near the top and a long lower wick (at least 2x the body), almost no upper wick, and a range at least as big as the average bar.",
    "shooting_star": "After a rise: a small body near the bottom, a long upper wick (at least 2x the body), almost no lower wick, a full-size range.",
    "engulfing": "After a decline: a down bar, then an up bar whose body covers the whole down body, and that body is bigger than average.",
    "harami": "After a decline: a big down bar, then a small bar whose body sits inside the down bar's body.",
    "piercing": "After a decline: a big down bar, then an up bar that opens at/below its close and closes above the middle of its body (but not above its open).",
    "dark_cloud": "After a rise: a big up bar, then a down bar that opens at/above its close and closes below the middle of its body (but not below its open).",
    "morning_evening_star": "After a decline: a big down bar, a small bar whose body is entirely below it, then a big up bar closing well into the first bar's body.",
    "three_soldiers_crows": "Three up bars in a row, each opening inside the previous body and closing higher, with solid bodies and small upper wicks.",
    "pin_bar": "A full-size bar whose lower wick is at least 2/3 of its whole range (price was rejected from the lows).",
    "tweezer": "After a decline: a down bar, then an up bar with the same low (within 5% of an average bar).",
}
BG = cs.BG


def fig_png(fig, dpi=90):
    buf = io.BytesIO(); fig.savefig(buf, format="jpeg", dpi=dpi, bbox_inches="tight", facecolor=BG,
                                    pil_kwargs={"quality": 82}); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def candles(ax, x, Oa, Ha, La, Ca, w=0.62):
    col = np.where(Ca >= Oa, cs.UP, cs.DN)
    rr = np.nanmax(Ha) - np.nanmin(La)
    ax.vlines(x, La, Ha, color=col, linewidth=1.4, zorder=3)
    ax.bar(x, np.where(np.abs(Ca - Oa) > 0, Ca - Oa, rr * 0.004), bottom=Oa, width=w, color=col, edgecolor="none", zorder=3)


def style(ax):
    ax.set_facecolor(BG); ax.grid(color=cs.GRID, linewidth=0.7)
    for sp in ax.spines.values():
        sp.set_color("#333")
    ax.tick_params(colors=cs.TXT, labelsize=9); ax.yaxis.tick_right()


def box(ax, x0, x1, lo_, hi_, rr, color):
    ax.add_patch(FancyBboxPatch((x0 - 0.5, lo_ - rr * 0.03), (x1 - x0) + 1.0, (hi_ - lo_) + rr * 0.06,
                                boxstyle="round,pad=0.05,rounding_size=0.4", fill=False, edgecolor=color, lw=2, zorder=5))


def draw_ref(name, span):
    a = np.array(REF[name], float); x = np.arange(len(a))
    fig, ax = plt.subplots(figsize=(3.4, 3.3), facecolor=BG); style(ax)
    candles(ax, x, a[:, 0], a[:, 1], a[:, 2], a[:, 3], w=0.55)
    rr = a[:, 1].max() - a[:, 2].min()
    box(ax, len(a) - span, len(a) - 1, a[-span:, 2].min(), a[-span:, 1].max(), rr, cs.HILITE)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-0.7, len(a) - 0.3)
    ax.set_title("textbook shape", color=cs.TXT2, fontsize=10, loc="left")
    return fig_png(fig, 85)


def draw_sample(i, span, lab):
    a = max(0, i - span - 12); z = min(n, i + 5)
    x = np.arange(z - a)
    fig, ax = plt.subplots(figsize=(5.6, 3.3), facecolor=BG); style(ax)
    candles(ax, x, O[a:z], H[a:z], L[a:z], C[a:z])
    ax.plot(x, ema10[a:z], color="#ffa500", lw=1.4, ls=(0, (5, 3)), label="EMA 10 (used by the rule)")
    i0 = i - a; rr = np.nanmax(H[a:z]) - np.nanmin(L[a:z])
    box(ax, i0 - span + 1, i0, L[i - span + 1:i + 1].min(), H[i - span + 1:i + 1].max(), rr, cs.HILITE)
    sess = seg[a:z]
    for j in np.flatnonzero(sess[1:] != sess[:-1]) + 1:
        ax.axvline(j - 0.5, color="#555", lw=0.9, ls=(0, (2, 3)))
    leg = ax.legend(loc="upper left", fontsize=8, frameon=False)
    for t in leg.get_texts():
        t.set_color(cs.TXT)
    ticks = [0, i0, len(x) - 1]
    ax.set_xticks(ticks); ax.set_xticklabels([b.index[a + t].strftime("%m/%d %H:%M") for t in ticks], fontsize=8.5)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: cs.fp(SYM, v)))
    ax.set_title(f"{lab}: {b.index[i]:%Y-%m-%d %H:%M} ET", color=cs.TXT, fontsize=10, loc="left")
    return fig_png(fig, 85)


def cond_table(r, i):
    dec = 0 if SYM == "YM" else 2
    M = r["M"][:, i]; tight = int(np.nanargmin(np.where(np.isfinite(M), M, np.inf)))
    rows = []
    for k, cd in enumerate(r["conds"]):
        lv, rv = cd["lhs"][i], cd["rhs"][i]
        diff = (lv - rv) if cd["op"] in (">=", ">") else (rv - lv)
        cls = " class='tight'" if k == tight else ""
        rows.append(f"<tr{cls}><td>{html.escape(cd['label'])}</td><td>{lv:,.{dec}f} {html.escape(cd['op'])} "
                    f"{rv:,.{dec}f}</td><td>passes by {diff:,.{dec}f} pts<br><span class='mut'>{M[k]:.2f} of an "
                    f"avg bar</span></td></tr>")
    return ("<table class='cond'><tr><th>Rule condition</th><th>Actual</th><th>Margin</th></tr>" + "".join(rows) +
            f"</table><p class='mut'>Average bar (10-bar mean range) here: {R[i]:,.{dec}f} pts. Highlighted = the "
            f"tightest condition, the one that makes this example iffy or not.</p>")


STYLE = cs.PAGE_STYLE.replace("</style>", (
    ".pat{margin:22px 0 36px;padding:14px;border:1px solid #2a2a2a;border-radius:8px;background:#050505}"
    ".row{display:grid;grid-template-columns:260px repeat(3,minmax(0,1fr));gap:14px;align-items:start}"
    "@media(max-width:1300px){.row{grid-template-columns:1fr 1fr}}"
    ".row img{width:100%;display:block;border-radius:4px}.ref p{font-size:13px;color:#cfcfcf;line-height:1.45}"
    "table.cond{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}"
    "table.cond td,table.cond th{border-bottom:1px solid #222;padding:3px 4px;text-align:left;vertical-align:top}"
    "table.cond th{color:#9a9a9a;font-weight:600}tr.tight td{background:#3a3000;color:#ffe14d}"
    ".stat{font-size:13px;color:#bdbdbd}</style>"))
PER = 4
pages = [results[k:k + PER] for k in range(0, len(results), PER)]
nav = "<nav>" + "".join(f"<a href='patterns_{j}.html'>page {j}</a>" for j in range(1, len(pages) + 1)) + "</nav>"
for pi, page in enumerate(pages, 1):
    parts = [f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,"
             f"initial-scale=1'><title>Pattern check {pi}</title>{STYLE}</head><body>",
             f"<h1>Candle pattern check: {spec['micro']} {TF}-minute, page {pi} of {len(pages)}</h1>{nav}",
             "<p>For each pattern: the textbook shape, then three real detections picked by how comfortably they pass "
             "the rules: a <b>clean</b> one (top 10%), a <b>typical</b> one, and the <b>most borderline</b> detection "
             "in 16 years. Yellow box = the pattern's bars. Each condition shows the real numbers and how far it "
             "passes; an <span style='color:#ffe14d'>iffy</span> example passes one condition by a hair.</p>"]
    for r in page:
        ok = "matches on every bar" if r["n_disagree"] == 0 else f"<b style='color:#ff7b8c'>{r['n_disagree']} bars disagree</b>"
        parts.append(f"<div class='pat'><h2>{html.escape(r['title'])}</h2><p class='stat'>{r['n_det']:,} detections in "
                     f"{spec['micro']} {TF}-min data. Independent re-check of every rule condition: {ok}. Tightest-margin "
                     f"distribution (avg-bar units): 2% {r['q'][0]:.3f}, 10% {r['q'][1]:.3f}, median {r['q'][2]:.3f}, "
                     f"90% {r['q'][3]:.3f}.</p><div class='row'>")
        parts.append(f"<div class='ref'><img src='data:image/jpeg;base64,{draw_ref(r['name'], r['span'])}'>"
                     f"<p>{html.escape(DESC[r['name']])}</p></div>")
        for lab, i in r["pick"].items():
            parts.append(f"<div><img src='data:image/jpeg;base64,{draw_sample(i, r['span'], lab)}'>{cond_table(r, i)}</div>")
        parts.append("</div></div>")
    parts.append(nav + "</body></html>")
    open(f"{OUT}/patterns_{pi}.html", "w").write("\n".join(parts))
    print(f"patterns_{pi}.html {os.path.getsize(f'{OUT}/patterns_{pi}.html') / 1e6:.2f} MB")
