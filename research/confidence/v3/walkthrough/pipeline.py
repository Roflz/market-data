"""pipeline.png: the flow every run follows, from 1-minute data to eval odds (dark style, research/signals/chart_style.py)."""
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../signals"))
import chart_style as cs
plt.rcParams["text.usetex"] = False
plt.rcParams["text.parse_math"] = False

STEPS = [
    ("1-minute data", "CME front contract by volume (ES/NQ/YM), raw prices,\nNew York time. Trading day starts 18:00 ET.",
     "research_lib.py:223-239"),
    ("Bars 5 / 15 / 60 / 120 min", "Grouped by day + contract + clock. Stamped by START time,\nknown only when the bar closes.",
     "signals.py:39-60"),
    ("Indicators", "EMA 8/20/50, Momentum(14) = 100 x C/C[14], session VWAP (from 18:00),\nswings (known 3 bars late), candle patterns, R20 = avg bar range.",
     "signals.py:92-311; features.py:176-183"),
    ("Signals / events", "Model B: 6 pullback rules (pullback detector + 5 triggers).\nv3: clock rules (A1 noise band, A4 08:30 fade, A3 expiry Friday).",
     "trigger_scan.py:70-74; pullbacks.py; g1lib/g4lib/g3"),
    ("Features", "69 numbers measured 'with the trade', in R20 units, closed bars only\n(trend, EMA gaps, Momentum, swings, day high/low, VWAP, candles, cost).",
     "v2/dataset.py:122-403"),
    ("Model score  OR  rule", "Model B: tree score >= that year's threshold -> KEEP.\nv3 rules: fixed condition (band break, 08:30 move, expiry day).",
     "v2/models.py:306-341; PREREG.md"),
    ("Decision", "Enter at the NEXT bar's open (v3: at the 15-min mark price).\nStop: beyond the pullback / 5-bar low, at least 1 R20 away.",
     "labels.py:337-358; harness.py:207-232"),
    ("Exit walk", "Minute by minute: stop checked FIRST (+1 tick slip), target needs 1 tick\nthrough; else rule exit or flat by 16:45 (v3: 16:00 / 09:45 marks).",
     "labels.py:295-334; exit_study.py:80-150"),
    ("Costs", "$1 + 1 tick each way per micro: MNQ $2.00, MES $3.50, MYM $2.00.\nAll results = net $ per 1 micro.",
     "signals.py:30-33; harness.py:114-117"),
    ("Statistics", "Compare with drift / random-day controls, block bootstrap p,\nHolm correction across the 6 tested ideas, robustness gates.",
     "v2/models.py:500-545; stats_protocol.py:90-142"),
    ("Eval odds", "Lucid 25K judge from every start day: sizing, -$600 day limit,\n$1,000 trailing drawdown, +$1,250 target -> pass %.",
     "v2/eval_sim.py:90-222; prop_sim.py:81-123"),
]

fig = plt.figure(figsize=(12, 22), facecolor=cs.BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
ax.text(0.5, 0.985, "How every run turns raw data into a trade and a verdict", color=cs.TXT, fontsize=22,
        fontweight="bold", ha="center", va="top")
ax.text(0.5, 0.962, "Read top to bottom. Only things known at the decision feed the decision; the exit walk, costs and "
        "statistics use what happened after.", color=cs.TXT2, fontsize=12.5, ha="center", va="top", wrap=True)
n = len(STEPS); top, bot = 0.935, 0.02; h = (top - bot) / n
for k, (name, txt, src) in enumerate(STEPS):
    y = top - k * h
    after = k >= 7
    ec = "#7f8fff" if after else cs.HILITE
    ax.add_patch(FancyBboxPatch((0.05, y - h * 0.78), 0.90, h * 0.74, boxstyle="round,pad=0.006,rounding_size=0.01",
                                fc="#0d0d14" if after else "#141208", ec=ec, lw=1.6))
    ax.text(0.07, y - h * 0.13, f"{k + 1}. {name}", color=ec, fontsize=17, fontweight="bold", va="top")
    ax.text(0.07, y - h * 0.38, txt, color=cs.TXT, fontsize=12.8, va="top", linespacing=1.3)
    ax.text(0.93, y - h * 0.13, src, color=cs.TXT2, fontsize=10, va="top", ha="right")
    if k < n - 1:
        ax.annotate("", (0.5, y - h * 1.02), (0.5, y - h * 0.80),
                    arrowprops=dict(arrowstyle="-|>", color=cs.TXT2, lw=2))
    if k == 6:
        ax.plot([0.03, 0.97], [y - h * 0.91] * 2, color="#7f8fff", lw=1.2, ls=(0, (6, 4)))
        ax.text(0.97, y - h * 0.87, "below this line: what happened next (not known at the decision)",
                color="#9fa8ff", fontsize=11, ha="right", va="center", bbox=dict(fc=cs.BG, ec="none", pad=1))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline.png")
fig.savefig(out, dpi=110, facecolor=cs.BG); print(out)
