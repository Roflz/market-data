"""
Dark trading-platform chart style shared by the galleries (black background, bright candles, dashed EMA 8/20/50,
cyan VWAP, price scale on the right, Momentum(14) panel underneath).
  fig, ax, axm = new_figure()
  draw_base(ax, axm, B, ctx_slice, sym)   # candles, EMAs, VWAP, session lines, momentum, time axis
"""
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

BG = "#000000"
GRID = "#1c1c1c"
TXT = "#d4d4d4"
TXT2 = "#8c8c8c"
UP = "#22e622"
DN = "#ff2b45"
EMA_STYLE = {8: dict(color="#ff3030", lw=1.5), 20: dict(color="#ffa500", lw=2.4), 50: dict(color="#2fd04a", lw=1.8)}
VWAP_COL = "#a8e8ff"
MOM_COL = "#7fd6ff"
HILITE = "#ffe14d"          # entry / setup marks
EXITC = "#ff5cf0"           # exit-signal marks
GOOD, BAD = "#22e622", "#ff2b45"


def fp(sym, x):
    return f"{x:,.0f}" if sym == "YM" else f"{x:,.2f}"


def new_figure(w=13.5, h=7.6):
    fig = plt.figure(figsize=(w, h), facecolor=BG)
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1.25], hspace=0.04)
    ax = fig.add_subplot(gs[0]); axm = fig.add_subplot(gs[1], sharex=ax)
    for a in (ax, axm):
        a.set_facecolor(BG)
        a.grid(color=GRID, linewidth=0.8)
        a.set_axisbelow(True)
        for sp in a.spines.values():
            sp.set_color("#333333")
        a.tick_params(colors=TXT, labelsize=10)
        a.yaxis.tick_right(); a.yaxis.set_label_position("right")
    return fig, ax, axm


def draw_base(ax, axm, B, C_, sym, mom_label="Momentum (14)"):
    """B: bar slice (O,H,L,C,vwap,sess); C_: context slice (ema8/20/50, mom14), same index. Returns x, O, H, L, C."""
    n = len(B); x = np.arange(n)
    O, H, L, C = (B[c].to_numpy() for c in "OHLC")
    rr = np.nanmax(H) - np.nanmin(L)
    col = np.where(C >= O, UP, DN)
    ax.vlines(x, L, H, color=col, linewidth=1.2, zorder=3)
    ax.bar(x, np.where(np.abs(C - O) > 0, C - O, rr * 0.003), bottom=O, width=0.62, color=col, edgecolor="none", zorder=3)
    for e, st in EMA_STYLE.items():
        ax.plot(x, C_[f"ema{e}"].to_numpy(), color=st["color"], linewidth=st["lw"], linestyle=(0, (5, 3)), zorder=2,
                label=f"EMA {e}")
    sess = B.sess.to_numpy(); br = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ax.plot(np.insert(x.astype(float), br, np.nan), np.insert(B.vwap.to_numpy(), br, np.nan), color=VWAP_COL,
            linewidth=1.3, zorder=2, label="VWAP")
    for j in br:
        for a in (ax, axm):
            a.axvline(j - 0.5, color="#555555", linewidth=0.9, linestyle=(0, (2, 3)))
    ax.set_ylim(np.nanmin(L) - rr * 0.12, np.nanmax(H) + rr * 0.18)
    ax.set_xlim(-0.8, n - 0.2)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: fp(sym, v)))
    ax.tick_params(labelbottom=False)
    leg = ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=4, fontsize=9.5, frameon=False, handlelength=2.4)
    for t in leg.get_texts():
        t.set_color(TXT)
    mom = C_.mom14.to_numpy()
    axm.plot(x, mom, color=MOM_COL, linewidth=1.5)
    axm.axhline(100, color="#666666", linewidth=0.9, linestyle=(0, (3, 3)))
    axm.text(0.005, 0.92, mom_label, transform=axm.transAxes, color=TXT2, fontsize=10, va="top")
    ticks = np.linspace(0, n - 1, 8).round().astype(int); prev_day = None; lab = []
    for t in ticks:
        ts = B.index[t]
        lab.append(ts.strftime("%H:%M\n%m/%d/%Y") if ts.date() != prev_day else ts.strftime("%H:%M")); prev_day = ts.date()
    axm.set_xticks(ticks); axm.set_xticklabels(lab, fontsize=9.5, color=TXT)
    return x, O, H, L, C


def label(ax, xi, y, txt, color, above=True, fs=10.5, ha="center"):
    ax.annotate(txt, (xi, y), xytext=(0, 16 if above else -16), textcoords="offset points", ha=ha,
                va="bottom" if above else "top", fontsize=fs, color=color, fontweight="bold", zorder=9,
                bbox=dict(boxstyle="round,pad=0.25", fc="#111111", ec=color, lw=0.8, alpha=0.92))


def ring(ax, x0, x1, lo, hi, color, rr):
    """rounded box around bars x0..x1 spanning prices lo..hi"""
    from matplotlib.patches import FancyBboxPatch
    pad_y = rr * 0.025
    ax.add_patch(FancyBboxPatch((x0 - 0.55, lo - pad_y), (x1 - x0) + 1.1, (hi - lo) + 2 * pad_y,
                                boxstyle="round,pad=0.05,rounding_size=0.6", fill=False, edgecolor=color, linewidth=2.2,
                                zorder=8))


def save(fig, path):
    fig.savefig(path, dpi=88, bbox_inches="tight", facecolor=BG, pil_kwargs={"quality": 82})
    plt.close(fig)


PAGE_STYLE = ("<style>body{font-family:system-ui,sans-serif;margin:0 auto;padding:16px;background:#0d0d0d;color:#e6e6e6;"
              "max-width:1650px}a{color:#7fd6ff}h1{font-size:24px}h2{margin-top:40px;font-size:20px;"
              "border-bottom:1px solid #333;padding-bottom:6px}p,li{max-width:1150px;line-height:1.5}"
              "nav{margin:10px 0}nav a{margin-right:14px;font-size:15px}"
              ".ex{display:grid;grid-template-columns:minmax(0,1fr) 370px;gap:16px;align-items:start;margin:16px 0 30px;"
              "padding:12px;background:#000;border:1px solid #2a2a2a;border-radius:8px}"
              "@media(max-width:1100px){.ex{grid-template-columns:1fr}}.ex img{width:100%;display:block}"
              ".card{font-size:14px}.card .hd{margin-bottom:10px;line-height:1.5}.mut{color:#8c8c8c;font-size:13px}"
              ".badge{display:inline-block;padding:2px 10px;border-radius:12px;font-weight:600;margin-right:6px;font-size:13px}"
              ".ok{background:#0f3d14;color:#5cff6a}.bad{background:#4a0f17;color:#ff7b8c}.mid{background:#2a2a2a;color:#cfcfcf}"
              ".kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 12px}"
              ".kpis div{background:#161616;border-radius:8px;padding:8px 10px}.kpis .k{display:block;font-size:20px;"
              "font-weight:650}.kpis .l{font-size:12px;color:#9a9a9a}"
              ".card table{width:100%;border-collapse:collapse;font-size:13px}.card td,.card th{border-bottom:1px solid #222;"
              "padding:4px 3px;text-align:left;vertical-align:top}.card th{color:#9a9a9a;font-size:12px;"
              "text-transform:uppercase;letter-spacing:.04em;padding-top:12px}.card td:last-child{text-align:right}"
              ".sig{color:#ff5cf0;font-weight:600}.ent{color:#ffe14d;font-weight:600}"
              "table.sum{border-collapse:collapse;font-size:13px;margin:6px 0}table.sum td,table.sum th{border:1px solid #333;"
              "padding:3px 7px;text-align:right}table.sum th{background:#1a1a1a}table.sum td:first-child{text-align:left}"
              "details{margin:8px 0}summary{cursor:pointer;color:#7fd6ff}</style>")


NAMES = {"five_lower_lows_higher_highs": ("5 lower lows in a row", "5 higher highs in a row"),
         "clv_extreme": ("close near the bar's low", "close near the bar's high"),
         "clv5_extreme": ("close near the 5-bar low", "close near the 5-bar high"),
         "bar_80_20": ("80/20 bar", "80/20 bar"), "morning_evening_star": ("morning star", "evening star"),
         "three_soldiers_crows": ("three white soldiers", "three black crows"),
         "three_inside": ("three inside up", "three inside down"), "tall_trend_bar": ("tall up bar", "tall down bar"),
         "inside_bar_breakout": ("inside-bar breakout up", "inside-bar breakout down"),
         "nr7_breakout": ("NR7 breakout up", "NR7 breakout down")}


def pname(name, d):
    """plain name with direction, e.g. 'bullish hammer', 'bearish 5 higher highs in a row'"""
    word = "bullish" if d > 0 else "bearish"
    if name in NAMES:
        return f"{word} {NAMES[name][0 if d > 0 else 1]}"
    return f"{word} {name.replace('_', ' ')}"
