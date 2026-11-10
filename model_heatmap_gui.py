"""
Model heatmap: one row per trading model, with summary columns, a running total and a heat strip over time.
In the heat strip green = the model made money in that period, red = it lost, hatched = no trades that period.
Hover a cell for its numbers; click it to list that period's trades under the table.

Input  chosen_models_trades.csv (written by chosen_models.py): columns model, date, bp (required); usd, R, side,
       exit (optional). Any CSV with those columns works, so new models show up as new rows by themselves.
       chosen_models_skipped.csv (optional): trades the skip rules removed; a checkbox adds them back.
       Extra trade files (--extra, or the 'Add trades file...' button): any per-trade CSV with a date and a net bp
       (or net points and an entry price). Common column names are understood (net_bp, net_usd, exit_reason,
       entry_time, ...); a file without a model column becomes one row named after the file. Extra rows are labelled
       with the file name and are left out of the all-models row unless that checkbox is ticked.
Measures (all after costs, 1 micro per trade):
  bp   basis points of the entry price (1 bp = 0.01%). A 20-point gain is 10 bp at NQ 20,000 but 100 bp at NQ 2,000,
       so bp compares 2010 and 2026 fairly; $ at one contract makes the recent, higher-priced years dominate.
  R    profit divided by the risk taken at entry (entry to stop): equal-risk comparison; only for models with a stop.
  $    net dollars at 1 MNQ micro ($2 per NQ point), for reference.
Cumulative column: running total of net $ (1 micro per trade) or of bp (View menu / --cum), on the same time axis as
       the heat strip.
Studies tab: charts of data/analysis/studies.csv (built by analysis_studies.py; other scripts may append studies).
       Pick a model and a study; numeric x is drawn as lines, text x as grouped bars. The live setting is shaded and
       labelled 'current'; the highest point of the first series is ringed and labelled 'best' (studies with a current
       setting) or 'highest', and the text under the chart says how much more it made than the current setting.
       A light band is a range given by the study (e.g. random skips). Hover a point or bar for its values.
Eval sandbox tab: LucidFlex 25K pass odds for any settings of the three models (on/off, micros, stops, caps, entry
       and exit times, slippage, money at today's NQ price or as traded) and of the evaluation rules (target, max loss,
       consistency 40/50%, daily loss limit, start years), simulated by prop_sim.py with an evaluation started on
       every trading day. The chart sweeps one setting (x axis menu) with everything else as set: pass odds of all
       starts and of the 2018-21 and 2022-26 starts, median days to pass below; hover for the numbers, click a
       point to use that value. Computed in a background thread; presets: current live models, the eval plan
       (overnight break 9:xx entries, stop cap 0.15%) and overnight break + expiry fade.
Usage  PYTHONPATH=./pylib python3 model_heatmap_gui.py [--trades FILE] [--skipped FILE] [--extra FILE ...]
       [--include-extra] [--metric avg_bp|total_bp|avg_R|usd] [--period M|Q|Y] [--smooth 0|3|6|12]
       [--scale row|shared] [--colors greenred|bluered] [--cum usd|bp] [--theme auto|light|dark]
       [--size WIDTHxHEIGHT] [--screenshot out.png] [--click MODEL:INDEX]
       [--tab heatmap|studies|sandbox] [--model overnight_break|opening_range|expiry_fade|all]
       [--study "TITLE or ID"] [--studies FILE] [--preset NAME] [--sweep SETTING]
       e.g. --tab studies --model opening_range --study "Stop size" --screenshot stop_size.png
            --tab sandbox --preset "ONB + expiry fade" --sweep onb_exit --screenshot sandbox.png
"""
import argparse
import html
import math
import os
import sys
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

HERE = os.path.dirname(os.path.abspath(__file__))

MODEL_INFO = {     # display name, one-line rule; models not listed here show their CSV name and no rule
    "overnight_break": ("Overnight break",
                        "First close beyond the overnight high/low, 9:35-15:00 ET, with the 20-day trend; "
                        "stop 2 x ATR; held to the 5 PM close"),
    "opening_range": ("Opening range (5-min)",
                      "Direction of the first 5-minute candle, entered at 9:35 ET; stop at the candle's other "
                      "end; out at the 15:59 close"),
    "expiry_fade": ("Expiry-Friday fade",
                    "Short at the 9:30 open on monthly options-expiry Fridays, cover at the 15:59 close; no stop"),
}
COMBINED = "__all__"

METRICS = {        # key: (menu label, unit, kind) - kind "avg" = per trade, "total" = summed over the period
    "avg_bp": ("Avg bp per trade", "bp", "avg"),
    "total_bp": ("Total bp per period", "bp", "total"),
    "avg_R": ("Avg R per trade", "R", "avg"),
    "usd": ("Net $ per period (1 micro)", "$", "total"),
}
PERIODS = {"M": ("Month", "months"), "Q": ("Quarter", "quarters"), "Y": ("Year", "years")}
SMOOTH = [0, 3, 6, 12]
CUM_UNITS = {"usd": ("Net $ (1 micro per trade)", "$"), "bp": ("Basis points (sum of bp per trade)", "bp")}

# diverging ramps: neutral gray midpoint -> pole, lightness moving away from the midpoint (interpolated in OKLab)
RAMPS = {
    "greenred": {"label": "Green / red",
                 "light": {"pos": ["#f0efec", "#a6d9a3", "#3f9f52", "#0e6630"],
                           "neg": ["#f0efec", "#f4b0a4", "#d8564b", "#9a2222"]},
                 "dark": {"pos": ["#383835", "#2b5e36", "#3a9a50", "#79d487"],
                          "neg": ["#383835", "#6a2c27", "#bf4a41", "#f5897b"]}},
    "bluered": {"label": "Blue / red (colorblind-safe)",
                "light": {"pos": ["#f0efec", "#9ec5f4", "#3987e5", "#184f95"],
                          "neg": ["#f0efec", "#f4b0a4", "#d8564b", "#9a2222"]},
                "dark": {"pos": ["#383835", "#1c4a80", "#3987e5", "#9ec5f4"],
                         "neg": ["#383835", "#6a2c27", "#bf4a41", "#f5897b"]}},
}
PAD = 8            # px of empty space at each side of the heat column, shared by the header axis and the strips
VPAD = 9           # px above and below each strip
COLS = ["Model", "Trades", "Per\nyear", "Win\n%", "Avg bp\n/trade", "t\n(bp)", "Avg R\n/trade", "Net $\n1 micro",
        "Max\ndrawdown $", "Years\nup", "Color\nscale ±", "", ""]
COL_MODEL, COL_SCALE, COL_CUM, COL_HEAT = 0, len(COLS) - 3, len(COLS) - 2, len(COLS) - 1
COL_TIPS = {
    1: "Number of trades",
    2: "Trades per year over the model's own date range",
    3: "Share of trades that made money after costs",
    4: "Average net basis points per trade (1 bp = 0.01% of the entry price)",
    5: "t-statistic of the average bp: the average divided by its standard error. Above about 2 suggests the "
       "average is not just luck, before allowing for how many ideas were tried",
    6: "Average net profit in units of the risk taken at entry (entry to stop); blank for models with no stop",
    7: "Net dollars at one MNQ micro per trade, after costs",
    8: "Largest drop from a running peak in cumulative net $ (one micro per trade, by day)",
    9: "Calendar years with a positive net result / years traded (first and last years may be partial)",
    10: "Values at or beyond this size get the full color; smaller ones are paler",
    11: "Running total after costs, day by day, on the same time axis as the heat strip: net $ at one micro per "
        "trade, or the sum of bp per trade (View menu). Each row has its own vertical scale; the dashed line is zero",
}

# column names understood in extra trade files (lower case; first match wins)
ALIASES = {
    "model": ["model", "strategy", "variant", "system", "model_name"],
    "date": ["date", "trade_date", "session", "session_date", "day"],
    "date_ts": ["entry_ts", "entry_time", "entry_datetime", "entry_timestamp", "timestamp", "ts_event", "time"],
    "bp": ["bp", "net_bp", "bp_net", "pnl_bp", "net_bps", "ret_bp"],
    "usd": ["usd", "net_usd", "usd_net", "pnl_usd", "net_$", "net_dollars", "pnl"],
    "R": ["r", "net_r", "r_net", "r_multiple", "r_mult"],
    "side": ["side", "direction", "dir"],
    "exit": ["exit_reason", "exit_type", "reason", "why", "exit"],
    "pts": ["net_pts", "pts_net", "net_points"],
    "entry": ["entry", "entry_price", "entry_px", "entry_fill", "fill"],
}


# ---------------------------------------------------------------------------------------------- colors (OKLab)
def _hex_lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def _lin_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _oklab_qcolor(L, a, b):
    l, m, s = ((L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
               (L - 0.0894841775 * a - 1.2914855480 * b) ** 3)
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    out = []
    for x in rgb:
        x = min(1.0, max(0.0, x))
        out.append(round(255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)))
    return QtGui.QColor(*out)


def ramp_lut(stops, n=101):
    """n colors from stops[0] (t=0) to stops[-1] (t=1), evenly spaced stops, interpolated in OKLab."""
    labs = [_lin_oklab(*_hex_lin(h)) for h in stops]
    seg = len(labs) - 1
    lut = []
    for k in range(n):
        t = k / (n - 1) * seg
        j = min(int(t), seg - 1)
        f = t - j
        lut.append(_oklab_qcolor(*(labs[j][c] + f * (labs[j + 1][c] - labs[j][c]) for c in range(3))))
    return lut


class Colors:
    def __init__(self, scheme, dark):
        r = RAMPS[scheme]["dark" if dark else "light"]
        self.pos, self.neg = ramp_lut(r["pos"]), ramp_lut(r["neg"])
        self.mid = self.pos[0]

    def color(self, v, limit):
        t = min(1.0, abs(v) / limit) if limit > 0 else 1.0
        lut = self.pos if v > 0 else self.neg
        return lut[int(round(t * (len(lut) - 1)))]


# ---------------------------------------------------------------------------------------------- data
def load_trades(trades_path, skipped_path):
    T = pd.read_csv(trades_path)
    missing = {"model", "date", "bp"} - set(T.columns)
    if missing:
        raise ValueError(f"{trades_path} is missing column(s): {', '.join(sorted(missing))}")
    T["skip_rule"] = ""
    n_skipped = 0
    if skipped_path and os.path.exists(skipped_path):
        S = pd.read_csv(skipped_path)
        if {"model", "date", "bp"} <= set(S.columns):
            S["skip_rule"] = S["skip_rule"].fillna("skip rule") if "skip_rule" in S else "skip rule"
            n_skipped = len(S)
            T = pd.concat([T, S], ignore_index=True)
    T["date"] = pd.to_datetime(T["date"]).dt.normalize()
    for c in ("usd", "R", "bp"):
        T[c] = pd.to_numeric(T[c], errors="coerce") if c in T else np.nan
    for c in ("side", "exit"):
        T[c] = T[c].fillna("").astype(str) if c in T else ""
    T["model"] = T["model"].astype(str)
    T = T.dropna(subset=["date", "bp"]).sort_values(["date", "model"]).reset_index(drop=True)
    return T, n_skipped


def file_stem_model(path):
    """Row name for a file without a model column: 'B_trades.csv' -> 'B', 'trades_S1.csv' -> 'S1'."""
    s = os.path.splitext(os.path.basename(path))[0]
    for pre in ("trades_", "trades-"):
        if s.lower().startswith(pre) and len(s) > len(pre):
            s = s[len(pre):]
    for suf in ("_trades", "-trades"):
        if s.lower().endswith(suf) and len(s) > len(suf):
            s = s[:-len(suf)]
    return s


def to_dates(col):
    """Trade dates from a date or timestamp column. A leading YYYY-MM-DD is taken as written (the local trading
    date, whatever time zone follows); anything else goes through pandas' parser."""
    s = col.astype(str).str.strip()
    if len(s) and s.str.match(r"^\d{4}-\d{2}-\d{2}").mean() > 0.8:
        return pd.to_datetime(s.str[:10], errors="coerce", format="%Y-%m-%d")
    try:
        d = pd.to_datetime(s, errors="coerce", format="mixed")
    except (ValueError, TypeError):
        d = pd.to_datetime(s, errors="coerce", utc=True).dt.tz_convert("America/New_York")
    if getattr(d.dt, "tz", None) is not None:
        d = d.dt.tz_localize(None)
    return d.dt.normalize()


def load_extra(path):
    """Read a per-trade CSV with free-form column names. Returns (frame with model, date, bp, usd, R, side, exit,
    skip_rule; list of plain-language notes on which columns were used). Raises ValueError with a clear message."""
    name = os.path.basename(path)
    if not os.path.exists(path):
        raise ValueError(f"{path}: file not found")
    try:
        head = pd.read_csv(path, nrows=50)
    except Exception as ex:
        raise ValueError(f"{name}: could not be read as a CSV file ({ex})")
    cols = {str(c).strip().lower(): c for c in head.columns}
    def numeric(c):                      # blanks ignored (e.g. R is empty for models without a stop); None = all blank
        v = head[c].dropna()
        return pd.to_numeric(v, errors="coerce").notna().mean() > 0.8 if len(v) else None

    def find(kind, suffix=None, want_numeric=None):
        for a in ALIASES[kind]:
            if a in cols and (want_numeric is None or numeric(cols[a]) in (want_numeric, None)):
                return cols[a]
        if suffix:                       # e.g. 'day_net_bp': accept a single column ending in the suffix
            hits = [c for lc, c in cols.items() if lc.endswith(suffix) and not lc.startswith("gross")]
            if len(hits) == 1:
                return hits[0]
        return None

    c_model, c_date, c_ts = find("model"), find("date"), None
    c_bp = find("bp", suffix="net_bp", want_numeric=True)
    c_pts, c_entry = find("pts", suffix="net_pts", want_numeric=True), find("entry", want_numeric=True)
    c_usd, c_R = find("usd", suffix="net_usd", want_numeric=True), find("R", want_numeric=True)
    c_side, c_exit = find("side"), find("exit", want_numeric=False)
    if c_date is None:                   # fall back to an entry timestamp that carries the date
        for a in ALIASES["date_ts"]:
            if a in cols and to_dates(head[cols[a]]).dt.year.gt(1990).mean() > 0.8:
                c_ts = cols[a]
                break
        if c_ts is None:
            raise ValueError(f"{name}: no trade date found. Looked for a column named "
                             f"{', '.join(ALIASES['date'])} (or an entry timestamp that includes the date, such as "
                             f"entry_ts).\nColumns in the file: {', '.join(map(str, head.columns))}")
    if c_bp is None and (c_pts is None or c_entry is None):
        gross = [c for c in head.columns if "gross" in str(c).lower()]
        raise ValueError(
            f"{name}: no net bp per trade. Looked for a column named {', '.join(ALIASES['bp'])}, and could not "
            f"compute bp because that needs a net points column (net_pts) and an entry price column (entry)."
            + (f"\n({', '.join(map(str, gross))} {'is' if len(gross) == 1 else 'are'} before costs, so not used.)"
               if gross else "")
            + f"\nColumns in the file: {', '.join(map(str, head.columns))}")
    use = [c for c in (c_model, c_date, c_ts, c_bp, c_usd, c_R, c_side, c_exit) if c is not None]
    if c_bp is None:
        use += [c_pts, c_entry]
    D = pd.read_csv(path, usecols=list(dict.fromkeys(use)))
    notes = []
    out = pd.DataFrame(index=D.index)
    out["model"] = D[c_model].astype(str) if c_model else file_stem_model(path)
    out["date"] = to_dates(D[c_date or c_ts])
    if not c_date:
        notes.append(f"date from {c_ts}")
    if c_bp is not None:
        out["bp"] = pd.to_numeric(D[c_bp], errors="coerce")
        notes.append(f"bp from {c_bp}")
    else:
        e = pd.to_numeric(D[c_entry], errors="coerce")
        out["bp"] = 1e4 * pd.to_numeric(D[c_pts], errors="coerce") / e.where(e > 0)
        notes.append(f"bp = 10,000 x {c_pts} / {c_entry}")
    out["usd"] = pd.to_numeric(D[c_usd], errors="coerce") if c_usd else np.nan
    notes.append(f"$ from {c_usd}" if c_usd else "no $ column")
    out["R"] = pd.to_numeric(D[c_R], errors="coerce") if c_R else np.nan
    if c_R:
        notes.append(f"R from {c_R}")
    if c_side:
        s = D[c_side]
        if pd.to_numeric(s, errors="coerce").notna().all():
            s = np.where(pd.to_numeric(s) > 0, "long", np.where(pd.to_numeric(s) < 0, "short", ""))
        out["side"] = pd.Series(s, index=D.index).fillna("").astype(str)
    else:
        out["side"] = ""
    out["exit"] = D[c_exit].fillna("").astype(str) if c_exit else ""
    out["skip_rule"] = ""
    if c_model is None:
        notes.append("no model column: one row for the file")
    n0 = len(out)
    out = out.dropna(subset=["date", "bp"]).sort_values("date").reset_index(drop=True)
    if not len(out):
        raise ValueError(f"{name}: no usable trades (every row is missing its date or bp).")
    if len(out) < n0:
        notes.append(f"{n0 - len(out)} row(s) without a date or bp ignored")
    return out, notes


def short_path(path, parts):
    """Last `parts` components of a path ('s12_recon/S1_trades.csv'), with '…/' in front if anything was cut."""
    comps = [c for c in os.path.normpath(path).split(os.sep) if c]
    s = "/".join(comps[-parts:])
    return s if len(comps) <= parts else "…/" + s


def period_label(p, freq):
    return {"M": lambda: p.strftime("%b %Y"), "Q": lambda: f"{p.year} Q{p.quarter}", "Y": lambda: str(p.year)}[freq]()


def bin_table(df, periods, freq):
    """Per-period sums for one model on the shared period axis (missing periods = zeros)."""
    p = df.date.dt.to_period(freq)
    g = df.assign(p=p, win=(df.bp > 0).astype(int)).groupby("p")
    agg = pd.DataFrame({"n": g.size(), "sum_bp": g.bp.sum(), "nR": g.R.count(), "sum_R": g.R.sum(),
                        "n_usd": g.usd.count(), "sum_usd": g.usd.sum(), "wins": g.win.sum()})
    return agg.reindex(periods, fill_value=0)


def metric_values(agg, metric, smooth, active):
    """Value per period. smooth > 1: trailing window of that many periods (per-trade measures are pooled over the
    window's trades; per-period totals are averaged over the window's periods within the model's active span).
    NaN = no trades counted in the window."""
    w = max(1, smooth)
    roll = lambda a: pd.Series(np.asarray(a, float)).rolling(w, min_periods=1).sum().to_numpy()
    kind = METRICS[metric][2]
    if metric == "avg_bp":
        num, den = agg.sum_bp, agg.n
    elif metric == "avg_R":
        num, den = agg.sum_R, agg.nR
    elif metric == "total_bp":
        num, den = agg.sum_bp, agg.n
    else:
        num, den = agg.sum_usd, agg.n_usd
    N, D = roll(num), roll(den)
    if kind == "avg":
        val = np.where(D > 0, N / np.where(D > 0, D, 1), np.nan)
    else:
        nb = roll(active.astype(float))                       # periods in the window that the model was running
        val = np.where(D > 0, N / np.where(nb > 0, nb, 1), np.nan)
    val[~active] = np.nan
    return val


def nice_limit(values):
    v = np.abs(np.asarray(values, float))
    v = v[np.isfinite(v) & (v > 0)]
    if not len(v):
        return 1.0
    q = float(np.percentile(v, 95))
    e = 10 ** math.floor(math.log10(q))
    for m in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * e >= q * 0.999:
            return m * e
    return 10 * e


def fmt(v, unit):
    if v is None or not np.isfinite(v):
        return "–"
    if unit == "$":
        return ("+" if v > 0 else "-" if v < 0 else "") + f"${abs(v):,.0f}"
    if unit == "R":
        return f"{v:+.2f} R"
    return f"{v:+.1f} bp" if abs(v) < 100 else f"{v:+,.0f} bp"


def summary(df):
    n = len(df)
    bp = df.bp
    span = max((df.date.max() - df.date.min()).days / 365.25, 1 / 12)
    sd = bp.std(ddof=1) if n > 2 else np.nan
    has_usd = df.usd.notna().any()
    money = df.usd if has_usd else df.bp
    daily = money.groupby(df.date).sum()
    cum = daily.cumsum().to_numpy()
    peak = np.maximum.accumulate(np.r_[0.0, cum])[1:]
    yearly = money.groupby(df.date.dt.year).sum()
    return {"n": n, "per_year": n / span, "win": (bp > 0).mean(), "avg_bp": bp.mean(),
            "t": bp.mean() / (sd / math.sqrt(n)) if sd and np.isfinite(sd) and sd > 0 else np.nan,
            "avg_R": df.R.mean() if df.R.notna().any() else np.nan,
            "net": df.usd.sum() if has_usd else np.nan,
            "dd": float((peak - cum).max()) if has_usd and len(cum) else np.nan,
            "yrs": f"{int((yearly > 0).sum())}/{len(yearly)}"}


def cumulative(df, axis0, axis_days):
    """Day-by-day running totals for the sparkline. x = fraction of the shared time axis at the END of each trading
    day (index 0 is the start of the first trading day, value 0), so the line lines up with the heat strip."""
    g = df.groupby("date")
    day_usd, day_bp, day_n = g.usd.sum(min_count=1), g.bp.sum(), g.size()
    dates = day_bp.index
    x = ((dates - axis0) / pd.Timedelta(days=1)).to_numpy(float)
    return {"x": np.r_[x[0], x + 1] / axis_days, "dates": dates,
            "usd": np.r_[0.0, day_usd.fillna(0).cumsum().to_numpy(float)],
            "bp": np.r_[0.0, day_bp.cumsum().to_numpy(float)],
            "day_usd": day_usd.to_numpy(float), "day_bp": day_bp.to_numpy(float), "day_n": day_n.to_numpy(int),
            "has_usd": bool(df.usd.notna().any()), "usd_partial": bool(df.usd.isna().any() and df.usd.notna().any())}


@dataclass
class Row:
    key: str
    name: str
    rule: str
    df: pd.DataFrame
    agg: pd.DataFrame
    active: np.ndarray
    values: np.ndarray
    limit: float
    note: str
    stats: dict
    cum: dict = None
    label_html: str = ""
    label_tip: str = ""
    extra: bool = False


# ---------------------------------------------------------------------------------------------- widgets
class FlowLayout(QtWidgets.QLayout):
    """Lays its items out left to right and wraps to a new line when the window is too narrow."""

    def __init__(self, parent=None, hspace=10, vspace=4):
        super().__init__(parent)
        self._items, self.hspace, self.vspace = [], hspace, vspace

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, i):
        return self._items[i] if 0 <= i < len(self._items) else None

    def takeAt(self, i):
        return self._items.pop(i) if 0 <= i < len(self._items) else None

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return self._place(QtCore.QRect(0, 0, w, 0), False)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._place(rect, True)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        s = QtCore.QSize()
        for it in self._items:
            s = s.expandedTo(it.minimumSize())
        m = self.contentsMargins()
        return s + QtCore.QSize(m.left() + m.right(), m.top() + m.bottom())

    def _place(self, rect, apply):
        m = self.contentsMargins()
        r = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        lines, cur, x = [], [], r.x()
        for it in self._items:
            if it.widget() is not None and not it.widget().isVisibleTo(it.widget().parentWidget()):
                continue
            w = it.sizeHint().width()
            if cur and x + w > r.right() + 1:
                lines.append(cur)
                cur, x = [], r.x()
            cur.append(it)
            x += w + self.hspace
        if cur:
            lines.append(cur)
        y = r.y()
        for line in lines:
            lh = max(it.sizeHint().height() for it in line)
            x = r.x()
            for it in line:
                sh = it.sizeHint()
                if apply:
                    it.setGeometry(QtCore.QRect(QtCore.QPoint(x, y + (lh - sh.height()) // 2), sh))
                x += sh.width() + self.hspace
            y += lh + self.vspace
        return max(0, y - self.vspace - r.y()) + m.top() + m.bottom()


def year_axis_step(fm, xs):
    """Label every 1, 2 or 5 years so the labels fit; short labels ('15) when even that is too tight."""
    label_w = fm.horizontalAdvance("2026") + 6
    widths = np.diff(xs) if len(xs) > 1 else np.array([1e9])
    med = float(np.median(widths)) if widths.size else 1e9
    step = 1 if med >= label_w else (2 if med * 2 >= label_w else 5)
    return step, med * step < label_w


class TimeHeader(QtWidgets.QHeaderView):
    """Column header that draws the heat and cumulative columns' titles and the shared year axis."""

    def __init__(self, win):
        super().__init__(Qt.Horizontal)
        self.win = win
        self.setDefaultAlignment(Qt.AlignCenter)
        self.setSectionsClickable(False)

    def paintSection(self, painter, rect, idx):
        painter.save()
        super().paintSection(painter, rect, idx)
        painter.restore()
        if idx not in (COL_HEAT, COL_CUM) or self.win.fracs is None:
            return
        painter.save()
        fm = painter.fontMetrics()
        r = rect.adjusted(PAD, 4, -PAD, -4)
        painter.setPen(self.win.ink)
        title = self.win.heat_title if idx == COL_HEAT else self.win.cum_title
        painter.drawText(QtCore.QRect(r.left(), r.top(), r.width(), fm.height()), Qt.AlignLeft | Qt.AlignVCenter,
                         fm.elidedText(title, Qt.ElideRight, r.width()))
        ybase = r.bottom() - fm.height()
        years, fr = self.win.year_fracs
        xs = [r.left() + f * r.width() for f in fr]
        step, short = year_axis_step(fm, xs)
        painter.setPen(self.win.muted)
        for k, (y, x0) in enumerate(zip(years, xs[:-1])):
            x1 = xs[k + 1]
            # a tick at every year boundary; when only every 2nd/5th year is labelled, the others are short ticks
            # below the labels so they do not cross the text
            if x0 >= r.left() - 0.5:
                painter.drawLine(QtCore.QPointF(x0, ybase - 2 if y % step == 0 else r.bottom()),
                                 QtCore.QPointF(x0, r.bottom() + 4))
            if y % step == 0 and x1 - x0 > 4:
                txt = f"'{y % 100:02d}" if short else str(y)
                lx0, lx1 = max(x0, r.left()), min(x0 + (x1 - x0) * step, r.right())
                if lx1 - lx0 >= fm.horizontalAdvance(txt):
                    painter.drawText(QtCore.QRectF(lx0, ybase, lx1 - lx0, fm.height() + 2),
                                     Qt.AlignHCenter | Qt.AlignVCenter, txt)
        painter.restore()


class HeatStrip(QtWidgets.QWidget):
    def __init__(self, win, row):
        super().__init__()
        self.win, self.row, self.hover = win, row, None
        self.setMouseTracking(True)
        self.setMinimumHeight(28)
        self.setCursor(Qt.PointingHandCursor)

    def _edges(self):
        r = QtCore.QRectF(self.rect()).adjusted(PAD, VPAD, -PAD, -VPAD)
        return r, np.round(r.left() + self.win.fracs * r.width()).astype(int)

    def bin_at(self, x):
        _, xi = self._edges()
        i = int(np.searchsorted(xi, x, side="right")) - 1
        if 0 <= i < len(xi) - 1 and self.row.active[i]:
            return i
        return None

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        row, win = self.row, self.win
        r, xi = self._edges()
        top, h = int(r.top()), max(1, int(r.height()))
        if row.note:                           # measure not available for this model (e.g. R without a stop)
            p.setPen(win.muted)
            p.drawText(r, Qt.AlignCenter, row.note)
            return
        hatch = QtGui.QBrush(win.muted, Qt.BDiagPattern)
        act = np.flatnonzero(row.active)
        for i in act:
            x0, x1 = xi[i], xi[i + 1]
            w = max(1, x1 - x0 - (1 if x1 - x0 >= 6 else 0))
            v = row.values[i]
            if np.isfinite(v):
                p.fillRect(x0, top, w, h, win.colors.color(v, row.limit))
            else:
                p.fillRect(x0, top, w, h, win.colors.mid)
                p.fillRect(x0, top, w, h, hatch)
            if win.partial is not None and win.partial[i]:      # partly covered period: dashed outline
                p.setPen(QtGui.QPen(win.ink, 1, Qt.DashLine))
                p.drawRect(QtCore.QRectF(x0 + 0.5, top + 0.5, max(1, w - 1), h - 1))
        if len(act):
            p.setPen(QtGui.QPen(win.hairline, 1))
            p.drawRect(QtCore.QRectF(xi[act[0]] - 0.5, top - 0.5, xi[act[-1] + 1] - xi[act[0]], h))
        if self.hover is not None and self.hover < len(xi) - 1:
            x0, x1 = xi[self.hover], xi[self.hover + 1]
            p.setPen(QtGui.QPen(win.ink, 2))
            p.drawRect(QtCore.QRectF(x0 - 1, top - 1, max(2, x1 - x0) + 1, h + 1))

    def mouseMoveEvent(self, e):
        i = self.bin_at(e.position().x())
        if i != self.hover:
            self.hover = i
            self.update()
        if i is None:
            QtWidgets.QToolTip.hideText()
        else:
            QtWidgets.QToolTip.showText(e.globalPosition().toPoint(), self.win.tooltip(self.row, i), self)

    def leaveEvent(self, _):
        self.hover = None
        self.update()

    def mousePressEvent(self, e):
        i = self.bin_at(e.position().x())
        if i is not None and e.button() == Qt.LeftButton:
            self.win.show_detail(self.row.key, i)


class CumSpark(QtWidgets.QWidget):
    """Running total of one row (net $ at 1 micro, or bp) over the shared time axis; hover for date and value."""

    def __init__(self, win, row):
        super().__init__()
        self.win, self.row, self.hover = win, row, None
        self.setMouseTracking(True)
        self.setMinimumHeight(28)

    def _series(self):
        c, unit = self.row.cum, self.win.cum_unit
        if c is None or (unit == "usd" and not c["has_usd"]):
            return None
        return c[unit]

    def _geom(self):
        fm = self.fontMetrics()
        r = QtCore.QRectF(self.rect()).adjusted(PAD, VPAD - 3, -PAD, -VPAD)
        lab = QtCore.QRectF(r.left(), r.top(), r.width(), fm.height())
        plot = QtCore.QRectF(r.left(), lab.bottom() + 3, r.width(), max(6.0, r.bottom() - lab.bottom() - 3))
        return lab, plot

    def _points(self, plot, y):
        xs = plot.left() + self.row.cum["x"] * plot.width()
        lo, hi = min(0.0, float(y.min())), max(0.0, float(y.max()))
        if hi - lo < 1e-9:
            hi = lo + 1.0
        ys = plot.bottom() - (y - lo) / (hi - lo) * plot.height()
        y0 = plot.bottom() - (0 - lo) / (hi - lo) * plot.height()
        return xs, ys, y0

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        win = self.win
        lab, plot = self._geom()
        y = self._series()
        if y is None:
            p.setPen(win.muted)
            p.drawText(QtCore.QRectF(self.rect()).adjusted(PAD, 0, -PAD, 0), Qt.AlignCenter | Qt.TextWordWrap,
                       "no $ column" if self.row.cum is not None else "no trades")
            return
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        xs, ys, y0 = self._points(plot, y)
        # faint guides at the labelled years of the header axis
        years, fr = win.year_fracs
        gx = [plot.left() + f * plot.width() for f in fr]
        step, _ = year_axis_step(self.fontMetrics(), gx)
        grid = QtGui.QColor(win.muted)
        grid.setAlpha(55)
        p.setPen(QtGui.QPen(grid, 1))
        for yr, x in zip(years, gx[:-1]):
            if yr % step == 0 and x > plot.left() + 1:
                p.drawLine(QtCore.QPointF(round(x) + 0.5, plot.top()), QtCore.QPointF(round(x) + 0.5, plot.bottom()))
        # light area between the line and zero: green-ish above, red-ish below
        poly = QtGui.QPolygonF([QtCore.QPointF(xs[0], y0)] + [QtCore.QPointF(a, b) for a, b in zip(xs, ys)] +
                               [QtCore.QPointF(xs[-1], y0)])
        path = QtGui.QPainterPath()
        path.addPolygon(poly)
        p.setPen(Qt.NoPen)
        for clip, col in ((QtCore.QRectF(plot.left() - 2, plot.top() - 2, plot.width() + 4, y0 - plot.top() + 2),
                           win.colors.pos[70]),
                          (QtCore.QRectF(plot.left() - 2, y0, plot.width() + 4, plot.bottom() - y0 + 2),
                           win.colors.neg[70])):
            c = QtGui.QColor(col)
            c.setAlpha(70)
            p.save()
            p.setClipRect(clip)
            p.fillPath(path, c)
            p.restore()
        zero = QtGui.QPen(win.muted, 1, Qt.DashLine)
        p.setPen(zero)
        p.drawLine(QtCore.QPointF(plot.left(), y0), QtCore.QPointF(plot.right(), y0))
        p.setPen(QtGui.QPen(win.ink, 1.2))
        p.drawPolyline(QtGui.QPolygonF([QtCore.QPointF(a, b) for a, b in zip(xs, ys)]))
        last = float(y[-1])
        end_col = win.colors.pos[90] if last >= 0 else win.colors.neg[90]
        p.setPen(Qt.NoPen)
        p.setBrush(end_col)
        p.drawEllipse(QtCore.QPointF(xs[-1], ys[-1]), 2.6, 2.6)
        if self.hover is not None:
            hx, hy = xs[self.hover], ys[self.hover]
            p.setPen(QtGui.QPen(win.muted, 1))
            p.drawLine(QtCore.QPointF(hx, plot.top()), QtCore.QPointF(hx, plot.bottom()))
            p.setPen(QtGui.QPen(win.ink, 1.5))
            p.setBrush(win.palette().color(QtGui.QPalette.Base))
            p.drawEllipse(QtCore.QPointF(hx, hy), 3, 3)
        p.setRenderHint(QtGui.QPainter.Antialiasing, False)
        p.setPen(win.ink)
        unit = "$" if win.cum_unit == "usd" else "bp"
        txt = fmt(last, unit) if self.hover is None else fmt(float(y[self.hover]), unit)
        p.drawText(lab, Qt.AlignRight | Qt.AlignVCenter, txt)
        if self.hover is not None:
            p.setPen(win.muted)
            d = self.row.cum["dates"][max(0, self.hover - 1)]
            p.drawText(lab, Qt.AlignLeft | Qt.AlignVCenter, f"{d:%b %Y}")

    def _index_at(self, x):
        y = self._series()
        if y is None:
            return None
        _, plot = self._geom()
        xs = plot.left() + self.row.cum["x"] * plot.width()
        if x < xs[0] - 4 or x > xs[-1] + 4:
            return None
        k = int(np.clip(np.searchsorted(xs, x), 1, len(xs) - 1))
        if k > 1 and abs(xs[k - 1] - x) < abs(xs[k] - x):
            k -= 1
        return max(1, k)

    def mouseMoveEvent(self, e):
        k = self._index_at(e.position().x())
        if k != self.hover:
            self.hover = k
            self.update()
        if k is None:
            QtWidgets.QToolTip.hideText()
        else:
            QtWidgets.QToolTip.showText(e.globalPosition().toPoint(), self.win.cum_tooltip(self.row, k), self)

    def leaveEvent(self, _):
        self.hover = None
        self.update()


class Legend(QtWidgets.QWidget):
    def __init__(self, win):
        super().__init__()
        self.win = win
        self.setMinimumHeight(40)

    def _stacked(self):
        """Too narrow for the explanation beside the color bar: it goes on two lines below it instead."""
        fm = self.fontMetrics()
        need = 8 + fm.horizontalAdvance("losing") + 12 + 280 + 12 + fm.horizontalAdvance("making money") + 36
        need += fm.horizontalAdvance("Each row has its own color scale (Color scale ± column); values at or beyond "
                                     "the scale get the full color.")
        return need > self.width() - 8

    def resizeEvent(self, e):
        fm = self.fontMetrics()
        self.setMinimumHeight(6 + 12 + fm.height() + 10 + 2 * fm.height() + 14 if self._stacked() else 40)
        super().resizeEvent(e)

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        win = self.win
        if win.colors is None:
            return
        fm = p.fontMetrics()
        p.setPen(win.ink)
        p.drawText(QtCore.QPointF(8, 6 + 11), "losing")
        x, y, w, h = 8 + fm.horizontalAdvance("losing") + 12, 6, 280, 12
        neg, pos = win.colors.neg, win.colors.pos
        n = len(neg)
        cells = [neg[n - 1 - k] for k in range(n)] + pos[1:]
        cw = w / len(cells)
        for k, c in enumerate(cells):
            p.fillRect(QtCore.QRectF(x + k * cw, y, cw + 0.6, h), c)
        p.setPen(QtGui.QPen(win.hairline, 1))
        p.drawRect(QtCore.QRectF(x - 0.5, y - 0.5, w + 1, h + 1))
        p.setPen(win.muted)
        unit = METRICS[win.cur_metric][1]
        lim = win.legend_limit
        lo, hi = (fmt(-lim, unit), fmt(lim, unit)) if lim else ("-scale", "+scale")
        ty = y + h + 2
        p.drawText(QtCore.QRectF(x - 40, ty, 80 + 0, fm.height()), Qt.AlignHCenter, lo)
        p.drawText(QtCore.QRectF(x + w / 2 - 30, ty, 60, fm.height()), Qt.AlignHCenter, "0")
        p.drawText(QtCore.QRectF(x + w - 40, ty, 80, fm.height()), Qt.AlignHCenter, hi)
        p.setPen(win.ink)
        p.drawText(QtCore.QPointF(x + w + 12, y + 11), "making money")
        tx = x + w + 12 + fm.horizontalAdvance("making money") + 36
        txt = (("Each row has its own color scale (Color scale ± column)" if win.scale_mode == "row"
                else "One color scale for all rows") + "; values at or beyond the scale get the full color.")
        # narrow window: the explanation goes on two lines below the color bar instead of beside it
        if self._stacked():
            tx, ty0 = 8, y + h + fm.height() + 10
        else:
            ty0 = y
        p.drawText(QtCore.QPointF(tx, ty0 + 11), txt)
        sx = tx
        sy = ty0 + h + 4
        p.fillRect(QtCore.QRectF(sx, sy, 22, 12), win.colors.mid)
        p.fillRect(QtCore.QRectF(sx, sy, 22, 12), QtGui.QBrush(win.muted, Qt.BDiagPattern))
        p.drawText(QtCore.QPointF(sx + 30, sy + 11), "no trades in that period.   Dashed outline = period only partly covered by the data (first and last)")


# ---------------------------------------------------------------------------------------------- studies tab
def load_studies(path):
    """Long-format study rows (analysis_studies.py and any script that appends to the same file)."""
    S = pd.read_csv(path, dtype={"x": str, "model": str, "study": str, "series": str})
    missing = {"model", "study", "x", "y"} - set(S.columns)
    if missing:
        raise ValueError(f"{path} is missing column(s): {', '.join(sorted(missing))}")
    for c in ("title", "x_label", "y_label", "series", "note", "source"):
        S[c] = S[c].fillna("").astype(str) if c in S else ""
    S["title"] = S.title.where(S.title != "", S.study)
    S["series"] = S.series.where(S.series != "", "value")
    for c in ("y", "y_lo", "y_hi", "x_order"):
        S[c] = pd.to_numeric(S[c], errors="coerce") if c in S else np.nan
    S["is_current"] = (S.is_current.astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
                       if "is_current" in S else False)
    S["x"] = S.x.fillna("").astype(str)
    S["_row"] = np.arange(len(S))
    return S.dropna(subset=["y"])


def study_sort_key(sid):
    """Natural order: S1, S2, S3, S3b, ..., S10, then anything else by name."""
    import re
    parts = re.split(r"(\d+)", str(sid))
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def fmt_money(v, compact=False, sign=False):
    if v is None or not np.isfinite(v):
        return "–"
    a = abs(v)
    s = "-" if v < 0 else ("+" if sign and v > 0 else "")
    if compact and a > 0:                    # axis reaching 10,000: every tick in K (one style per axis)
        t = f"{a / 1000:,.1f}".rstrip("0").rstrip(".")
        return f"{s}${t}K"
    return f"{s}${a:,.0f}"


def fmt_x(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    return f"{f:g}" if np.isfinite(f) else str(v)


STUDY_MODELS = [("overnight_break", "Overnight break"), ("opening_range", "Opening range"),
                ("expiry_fade", "Expiry fade"), ("all", "All models")]
SERIES_COLORS = {"light": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"],
                 "dark": ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]}
STUDIES_CMD = 'cd "{here}" && PYTHONPATH=./pylib python3 analysis_studies.py'


class StudiesPanel(QtWidgets.QWidget):
    """Tab 2: pick a model and a study from data/analysis/studies.csv; the chart is drawn with matplotlib."""

    def __init__(self, win, path):
        super().__init__()
        self.win, self.path = win, path
        self.S, self.fig, self.canvas, self.ax = None, None, None, None
        self.hits, self.hover_ann, self.hover_ring, self._cur_key = [], None, None, None
        self._pending = None
        left = QtWidgets.QWidget()
        left.setFixedWidth(250)
        lv = QtWidgets.QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.addWidget(QtWidgets.QLabel("Model:"))
        self.cb_model = QtWidgets.QComboBox()
        lv.addWidget(self.cb_model)
        lv.addSpacing(6)
        lv.addWidget(QtWidgets.QLabel("Studies:"))
        self.lst = QtWidgets.QListWidget()
        self.lst.setWordWrap(True)
        lv.addWidget(self.lst, 1)
        b = QtWidgets.QPushButton("Reload studies")
        b.setToolTip("Re-read " + path)
        b.clicked.connect(self.reload)
        lv.addWidget(b)
        self.info = QtWidgets.QLabel()
        self.info.setWordWrap(True)
        lv.addWidget(self.info)

        self.stack = QtWidgets.QStackedWidget()
        self.msg = QtWidgets.QLabel()
        self.msg.setWordWrap(True)
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.stack.addWidget(self.msg)
        page = QtWidgets.QWidget()
        pv = self.page_layout = QtWidgets.QVBoxLayout(page)
        pv.setContentsMargins(0, 0, 0, 0)
        pv.setSpacing(2)
        self.title = QtWidgets.QLabel()
        f = self.title.font()
        f.setPointSizeF(f.pointSizeF() * 1.3)
        f.setBold(True)
        self.title.setFont(f)
        self.subtitle = QtWidgets.QLabel()
        self.summary = QtWidgets.QLabel()
        self.summary.setWordWrap(True)
        self.note = QtWidgets.QLabel()
        self.note.setWordWrap(True)
        self.source = QtWidgets.QLabel()
        self.source.setWordWrap(True)
        for w_ in (self.title, self.subtitle, self.summary, self.note, self.source):
            w_.setTextFormat(Qt.PlainText)
            w_.setTextInteractionFlags(Qt.TextSelectableByMouse)
        pv.addWidget(self.title)
        pv.addWidget(self.subtitle)
        self.canvas_slot = pv.count()
        pv.addSpacing(4)
        pv.addWidget(self.summary)
        pv.addWidget(self.note)
        pv.addWidget(self.source)
        self.stack.addWidget(page)

        h = QtWidgets.QHBoxLayout(self)
        h.addWidget(left)
        h.addSpacing(8)
        h.addWidget(self.stack, 1)
        self.cb_model.currentIndexChanged.connect(self._fill_list)
        self.lst.currentRowChanged.connect(lambda _: self.draw())
        self.reload()

    # ------------------------------------------------------------------ data
    def reload(self, *_):
        model = self.cb_model.currentData()
        study = self._cur_key[1] if self._cur_key else None
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError
            self.S = load_studies(self.path)
        except FileNotFoundError:
            self.S = None
            self._message(f"No studies file yet ({self.path}).\n\nBuild it with:\n\n"
                          f"{STUDIES_CMD.format(here=HERE)}\n\nthen press 'Reload studies'.")
        except Exception as ex:
            self.S = None
            self._message(f"Could not read {self.path}:\n\n{ex}\n\nRebuild it with:\n\n{STUDIES_CMD.format(here=HERE)}")
        self.cb_model.blockSignals(True)
        self.cb_model.clear()
        known = [k for k, _ in STUDY_MODELS]
        models = list(STUDY_MODELS)
        if self.S is not None:
            models += [(m, m) for m in sorted(set(self.S.model) - set(known))]
        for k, name in models:
            n = 0 if self.S is None else self.S[self.S.model == k].study.nunique()
            self.cb_model.addItem(f"{name} ({n})", k)
        self.cb_model.setCurrentIndex(max(0, self.cb_model.findData(model)))
        self.cb_model.blockSignals(False)
        if self.S is not None:
            mt = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(self.path)))
            shown = (os.path.relpath(self.path, HERE) if os.path.abspath(self.path).startswith(HERE + os.sep)
                     else self.path)
            self.info.setText(f"{shown}\n{self.S.groupby(['model', 'study']).ngroups} "
                              f"studies, updated {mt}")
        else:
            self.info.setText("")
        self._fill_list(keep=study)

    def _message(self, txt):
        self.msg.setText(txt)
        self.stack.setCurrentIndex(0)

    def _studies_of(self, model):
        d = self.S[self.S.model == model]
        g = d.groupby("study", sort=False).agg(title=("title", "first"), note=("note", "first"))
        return g.loc[sorted(g.index, key=study_sort_key)]

    def _fill_list(self, *_, keep=None):
        keep = keep or (self.lst.currentItem().data(Qt.UserRole) if self.lst.currentItem() else None)
        self.lst.blockSignals(True)
        self.lst.clear()
        if self.S is None:
            self.lst.blockSignals(False)
            return
        model = self.cb_model.currentData()
        st = self._studies_of(model)
        for sid, r in st.iterrows():
            it = QtWidgets.QListWidgetItem(r.title)
            it.setData(Qt.UserRole, sid)
            it.setToolTip(r.note)
            self.lst.addItem(it)
        row = 0
        for k in range(self.lst.count()):        # same study (by id or title) as before, if this model has it
            it = self.lst.item(k)
            if keep is not None and keep in (it.data(Qt.UserRole), it.text()):
                row = k
        if self.lst.count():
            self.lst.setCurrentRow(row)
        self.lst.blockSignals(False)
        if not self.lst.count():
            self._message(f"No studies for {self.cb_model.currentText().rsplit(' (', 1)[0]} in {self.path}.")
        else:
            self.draw()

    def select(self, model=None, study=None):
        """For --model / --study: model key or display name, study title or id (case-insensitive)."""
        if model:
            m = model.strip().lower().replace(" ", "_")
            i = next((k for k in range(self.cb_model.count())
                      if m in (str(self.cb_model.itemData(k)).lower(),
                               self.cb_model.itemText(k).rsplit(" (", 1)[0].lower().replace(" ", "_"))), -1)
            if i < 0:
                print(f"--model {model}: not found; models: "
                      f"{', '.join(str(self.cb_model.itemData(k)) for k in range(self.cb_model.count()))}",
                      file=sys.stderr)
            else:
                self.cb_model.setCurrentIndex(i)
        if study:
            s = study.strip().lower()
            hit = [k for k in range(self.lst.count())
                   if s in (self.lst.item(k).text().lower(), str(self.lst.item(k).data(Qt.UserRole)).lower())]
            if hit:
                self.lst.setCurrentRow(hit[0])
            else:
                print(f"--study {study}: not found for this model; studies: "
                      f"{'; '.join(self.lst.item(k).text() for k in range(self.lst.count()))}", file=sys.stderr)
        self.draw()

    # ------------------------------------------------------------------ chart
    def _ensure_canvas(self):
        if self.canvas is not None:
            return
        import logging
        import matplotlib
        matplotlib.use("QtAgg")
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        from matplotlib import font_manager
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
        matplotlib.rcParams["text.parse_math"] = False          # '$' in labels is a dollar sign, not math
        fam = QtGui.QFontInfo(self.font()).family()
        names = {f.name for f in font_manager.fontManager.ttflist}
        matplotlib.rcParams["font.family"] = [fam] if fam in names else ["sans-serif"]
        matplotlib.rcParams["font.size"] = self.font().pointSizeF() or 9.0
        self.fig = Figure(dpi=self.logicalDpiX() or 96)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setMinimumHeight(220)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.page_layout.insertWidget(self.canvas_slot, self.canvas, 1)
        self.canvas.mpl_connect("motion_notify_event", self._hover)
        self.canvas.mpl_connect("figure_leave_event", lambda _: self._hide_hover())
        self.canvas.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.canvas and e.type() == QtCore.QEvent.Resize:
            QtCore.QTimer.singleShot(0, self.draw)          # bar widths and label wrapping follow the size
        return super().eventFilter(obj, e)

    def showEvent(self, e):
        super().showEvent(e)
        QtCore.QTimer.singleShot(0, self.draw)

    def _theme(self):
        pal = self.palette()
        dark = pal.color(QtGui.QPalette.Window).lightness() < 128
        c = {"dark": dark, "bg": pal.color(QtGui.QPalette.Window).name(),
             "base": pal.color(QtGui.QPalette.Base).name(), "ink": pal.color(QtGui.QPalette.WindowText).name(),
             "muted": "#898781", "grid": "#3a3a37" if dark else "#e4e3df",
             "series": SERIES_COLORS["dark" if dark else "light"]}
        c["axis"] = "#b5b3ad" if dark else "#5f5d58"           # tick labels: secondary text
        return c

    def current_rows(self):
        if self.S is None or self.lst.currentItem() is None:
            return None
        sid = self.lst.currentItem().data(Qt.UserRole)
        model = self.cb_model.currentData()
        return self.S[(self.S.model == model) & (self.S.study == sid)].sort_values("_row")

    def draw(self):
        if not self.isVisible():
            return
        d = self.current_rows()
        if d is None or not len(d):
            return
        self._ensure_canvas()
        self.stack.setCurrentIndex(1)
        self._cur_key = (self.cb_model.currentData(), self.lst.currentItem().data(Qt.UserRole))
        try:
            self._plot(d)
        except Exception as ex:                  # a malformed study must not take the GUI down
            self._message(f"Could not draw this study:\n{ex}")

    def _plot(self, d):
        c = self._theme()
        r0 = d.iloc[0]
        model_name = self.cb_model.currentText().rsplit(" (", 1)[0]
        money = "$" in r0.y_label or "usd" in r0.y_label.lower()
        yfmt = (lambda v, compact=False, sign=False: fmt_money(v, compact, sign)) if money else \
            (lambda v, compact=False, sign=False: (f"{v:+,.0f}" if sign else f"{v:,.0f}") if abs(v) >= 100
             else (f"{v:+,.2f}" if sign else f"{v:,.2f}").rstrip("0").rstrip("."))
        self.title.setText(r0.title)
        self.subtitle.setText(f"{model_name}  ·  {r0.y_label}" if r0.y_label else model_name)
        for w_, col in ((self.title, c["ink"]), (self.subtitle, c["muted"]), (self.summary, c["ink"]),
                        (self.note, c["ink"]), (self.source, c["muted"])):
            w_.setStyleSheet(f"color: {col}")

        fig = self.fig
        fig.clear()
        fig.set_facecolor(c["bg"])
        ax = self.ax = fig.add_subplot(111)
        ax.set_facecolor(c["bg"])
        series = list(dict.fromkeys(d.series))
        colors = {s: c["series"][k] if k < len(c["series"]) else c["muted"] for k, s in enumerate(series)}
        lv = d.assign(o=d.x_order.fillna(d._row)).groupby("x", sort=False).o.min().sort_values(kind="stable")
        xs = list(lv.index)
        num = pd.to_numeric(pd.Series(xs, dtype=object), errors="coerce").to_numpy(float)
        isnum = np.isfinite(num)
        mode = "lines" if isnum.any() else "bars"
        W, H = self.canvas.width(), self.canvas.height()
        plot_w = max(200.0, W - 110.0)                             # rough plot width in px before layout
        # positions: numeric x on a numeric axis; text levels next to it (after a gap) or one slot each for bars
        if mode == "lines":
            nv = np.unique(num[isnum])
            step = float(np.median(np.diff(nv))) if len(nv) > 1 else 1.0
            pos, extra = {}, 0
            for x, v in zip(xs, num):
                if np.isfinite(v):
                    pos[x] = v
            for x, v in zip(xs, num):
                if not np.isfinite(v):
                    extra += 1
                    pos[x] = nv.max() + step * (0.6 + extra)
            lo_x, hi_x = min(pos.values()), max(pos.values())
            pad = 0.4 * step
            ax.set_xlim(lo_x - pad, hi_x + pad)
            ppu = plot_w / max(1e-9, hi_x - lo_x + 2 * pad)
            slot = step
        else:
            pos = {x: float(k) for k, x in enumerate(xs)}
            ax.set_xlim(-0.6, len(xs) - 0.4)
            ppu = plot_w / (len(xs) + 0.2)
            slot = 1.0
        ns = len(series)
        self.hits = []
        ys_all = list(d.y) + list(d.y_lo.dropna()) + list(d.y_hi.dropna())

        # current setting: a quiet column behind the marks
        cur_x = list(dict.fromkeys(d[d.is_current].x))
        for x in cur_x:
            ax.axvspan(pos[x] - 0.42 * slot, pos[x] + 0.42 * slot, color=c["ink"], alpha=0.06, lw=0, zorder=0)
        band_label_done = False
        if mode == "lines":
            textx = [x for x, v in zip(xs, num) if not np.isfinite(v)]
            if textx:
                sep = (max(v for v in num if np.isfinite(v)) + min(pos[x] for x in textx)) / 2
                ax.axvline(sep, color=c["grid"], lw=1, zorder=1)
            for s in series:
                q = d[d.series == s].assign(p=lambda t: t.x.map(pos)).sort_values("p")
                qn = q[pd.to_numeric(q.x, errors="coerce").notna()]
                qt = q[pd.to_numeric(q.x, errors="coerce").isna()]
                kw = dict(color=colors[s], lw=2, marker="o", ms=6.5, mec=c["bg"], mew=1.5, solid_capstyle="round",
                          solid_joinstyle="round", zorder=3)
                ax.plot(qn.p, qn.y, label=s, **kw)
                if len(qt):
                    ax.plot(qt.p, qt.y, ls="none", **{k: v for k, v in kw.items() if k != "lw"})
                band = q.dropna(subset=["y_lo", "y_hi"])
                if len(band):
                    bl = "range band" if not band_label_done else None
                    band_label_done = True
                    bn = band[pd.to_numeric(band.x, errors="coerce").notna()]
                    ax.fill_between(bn.p, bn.y_lo, bn.y_hi, color=colors[s], alpha=0.2 if c["dark"] else 0.12, lw=0, zorder=2, label=bl)
                    for r in band[pd.to_numeric(band.x, errors="coerce").isna()].itertuples():
                        ax.fill_between([r.p - 0.15 * slot, r.p + 0.15 * slot], r.y_lo, r.y_hi, color=colors[s],
                                        alpha=0.12, lw=0, zorder=2)
                for r in q.itertuples():
                    self.hits.append(dict(kind="pt", series=s, x=r.x, y=r.y, px=r.p, lo=r.y_lo, hi=r.y_hi,
                                          color=colors[s]))
        else:
            gap = 2.0 / ppu                                      # 2 px surface gap between touching bars
            bw = min(0.78 / ns - gap, 24.0 / ppu)                # bars at most 24 px wide
            for j, s in enumerate(series):
                q = d[d.series == s].assign(p=lambda t: t.x.map(pos))
                off = (j - (ns - 1) / 2) * (bw + gap)
                xs_b = q.p + off
                band = q.dropna(subset=["y_lo", "y_hi"])
                if len(band):
                    bl = "range band" if not band_label_done else None
                    band_label_done = True
                    ax.bar(band.p + off, band.y_hi - band.y_lo, bottom=band.y_lo, width=min(bw * 2.2, 0.9 / ns),
                           color=colors[s], alpha=0.24 if c["dark"] else 0.14, lw=0, zorder=1, label=bl)
                ax.bar(xs_b, q.y, width=bw, color=colors[s], lw=0, zorder=3, label=s)
                for r, xb in zip(q.itertuples(), xs_b):
                    self.hits.append(dict(kind="bar", series=s, x=r.x, y=r.y, px=xb, x0=r.p - 0.5 * slot,
                                          x1=r.p + 0.5 * slot, j=j, lo=r.y_lo, hi=r.y_hi, color=colors[s]))
            ys_all.append(0.0)

        # y range: room above for the labels; zero line when the values cross zero (bars: always the baseline)
        y_min, y_max = float(np.nanmin(ys_all)), float(np.nanmax(ys_all))
        span = (y_max - y_min) or max(1.0, abs(y_max))
        ax.set_ylim(y_min - 0.06 * span if y_min < 0 or mode == "lines" else 0, y_max + 0.2 * span)
        if mode == "bars" or (y_min < 0 < y_max):
            ax.axhline(0, color=c["muted"], lw=1, zorder=2.5)

        # best point of the first series and the current setting
        first = d[d.series == series[0]]
        best = first.loc[first.y.idxmax()]
        curr = first[first.is_current]
        # 'best' where the study compares settings (it has a current one); otherwise just the highest value
        word = "best" if d.is_current.any() else "highest"
        bx = pos[best.x] + (self.hits[0]["px"] - pos[self.hits[0]["x"]] if mode == "bars" else 0)
        by = best.y if mode == "lines" else max(best.y, 0.0)
        if mode == "lines":
            ax.plot([bx], [best.y], ls="none", marker="o", ms=13, mfc="none", mec=c["ink"], mew=1.5, zorder=4)
        if len(curr):
            cr = curr.iloc[0]
            cxp = pos[cr.x] + (self.hits[0]["px"] - pos[self.hits[0]["x"]] if mode == "bars" else 0)
            if cr.x != best.x and mode == "lines":
                ax.plot([cxp], [cr.y], ls="none", marker="D", ms=10, mfc="none", mec=c["ink"], mew=1.5, zorder=4)
        for x in cur_x:
            ax.annotate("current", xy=(pos[x], 1), xycoords=("data", "axes fraction"), xytext=(0, -4),
                        textcoords="offset points", ha="center", va="top", color=c["muted"], fontsize="small")
        btxt = f"{word} {yfmt(best.y)}"
        if len(curr) and cr.x == best.x:
            btxt = f"{word} = current {yfmt(best.y)}"
        frac = (bx - ax.get_xlim()[0]) / (ax.get_xlim()[1] - ax.get_xlim()[0])
        ha = "left" if frac < 0.15 else ("right" if frac > 0.85 else "center")
        ax.annotate(btxt, xy=(bx, by), xytext=(0, 11 if mode == "lines" else 4), textcoords="offset points", ha=ha, va="bottom",
                    color=c["ink"], fontsize="small", fontweight="bold", zorder=5, annotation_clip=False)

        # axes, ticks, grid
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(c["grid"])
        ax.spines["bottom"].set_visible(not (mode == "bars" or y_min < 0 < y_max))
        ax.yaxis.grid(True, color=c["grid"], lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.tick_params(axis="both", length=0, colors=c["axis"], labelcolor=c["axis"], pad=6)
        from matplotlib.ticker import FuncFormatter, MaxNLocator
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, steps=[1, 2, 2.5, 5, 10]))
        big = max(abs(v) for v in ax.get_ylim()) >= 10000
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: yfmt(v, compact=big)))
        labels = [fmt_x(x) for x in xs]
        ax.set_xticks([pos[x] for x in xs])
        ax.set_xticklabels(self._fit_labels(labels, ppu * slot if mode == "bars" else ppu * slot * 0.95))
        ax.set_xlabel(r0.x_label, color=c["muted"], labelpad=8)
        if ns >= 2 or band_label_done:
            hs, ls = ax.get_legend_handles_labels()
            order = [ls.index(s) for s in series if s in ls] + [k for k, l in enumerate(ls) if l not in series]
            # as many entries per row as fit; matplotlib fills column by column, so reorder to read row by row
            fm = QtGui.QFontMetrics(self.font())
            ew = max(fm.horizontalAdvance(ls[k]) for k in order) * 0.9 + 48
            ncol = int(max(1, min(len(order), (W - 90) // ew)))
            order = [k for c_ in range(ncol) for k in order[c_::ncol]]
            leg = ax.legend([hs[k] for k in order], [ls[k] for k in order], loc="lower left",
                            bbox_to_anchor=(0, 1.02), ncol=ncol, frameon=False,
                            handlelength=1.6, columnspacing=1.4, borderaxespad=0, fontsize="small")
            for t in leg.get_texts():
                t.set_color(c["ink"])
        fig.set_layout_engine("constrained", h_pad=0.08, w_pad=0.12)
        self.hover_ann = ax.annotate("", xy=(0, 0), xytext=(12, 12), textcoords="offset points", fontsize="small",
                                     color=c["ink"], zorder=10, visible=False, annotation_clip=False,
                                     bbox=dict(boxstyle="round,pad=0.45", fc=c["base"], ec=c["grid"], lw=1))
        self.hover_ring, = ax.plot([], [], ls="none", marker="o", ms=11, mfc="none", mec=c["ink"], mew=1.5,
                                   zorder=6, visible=False)
        self._yfmt = yfmt

        # text under the chart
        if len(curr):
            if cr.x == best.x:
                summ = (f"The current setting ({fmt_x(cr.x)}) is the {word} of those tested for "
                        f"'{series[0]}': {yfmt(cr.y)}.")
            else:
                summ = (f"{word.capitalize()} for '{series[0]}': {fmt_x(best.x)} at {yfmt(best.y)}, "
                        f"{yfmt(best.y - cr.y)} more than the current setting {fmt_x(cr.x)} ({yfmt(cr.y)}).")
        else:
            summ = f"{word.capitalize()} for '{series[0]}': {fmt_x(best.x)} at {yfmt(best.y)}."
        self.summary.setText(summ)
        self.note.setText(r0.note)
        self.note.setVisible(bool(r0.note))
        self.source.setText(f"Source: {r0.source}" if r0.source else "")
        self.source.setVisible(bool(r0.source))
        self.canvas.draw_idle()

    def _fit_labels(self, labels, px_per_slot):
        """Category labels that fit their slot: as they are, else wrapped at spaces and hyphens (at most 3 lines)."""
        fm = QtGui.QFontMetrics(self.font())
        cw = fm.averageCharWidth() or 6
        def width(t):
            return max(fm.horizontalAdvance(line) for line in t.split("\n"))
        if all(width(t) <= px_per_slot - 6 for t in labels):
            return labels
        import textwrap
        n = max(4, int((px_per_slot - 6) / cw))
        out = []
        for t in labels:                         # once any label must wrap, two-word labels all wrap alike
            if len(t.split(" ")) == 2:
                out.append(t.replace(" ", "\n"))
            elif width(t) <= px_per_slot - 6:
                out.append(t)
            else:
                out.append("\n".join(textwrap.wrap(t, n, break_long_words=False)[:3]))
        return out

    def _hide_hover(self):
        if self.hover_ann is not None and self.hover_ann.get_visible():
            self.hover_ann.set_visible(False)
            self.hover_ring.set_visible(False)
            self.canvas.draw_idle()

    def _hover(self, e):
        ax = self.ax
        if ax is None or e.inaxes is not ax or not self.hits:
            self._hide_hover()
            return
        best, bd = None, 1e9
        for h in self.hits:
            if h["kind"] == "pt":
                px, py = ax.transData.transform((h["px"], h["y"]))
                dist = math.hypot(px - e.x, py - e.y)
                if dist < bd and dist <= 28:
                    best, bd = h, dist
            else:                                        # bars: the whole column slot is the hit area
                if h["x0"] <= e.xdata <= h["x1"]:
                    px, _ = ax.transData.transform((h["px"], 0))
                    dist = abs(px - e.x)
                    if dist < bd:
                        best, bd = h, dist
        if best is None:
            self._hide_hover()
            return
        lines = [best["series"], f"{fmt_x(best['x'])}:  {self._yfmt(best['y'])}"]
        if np.isfinite(best.get("lo", np.nan)):
            lines.append(f"range {self._yfmt(best['lo'])} to {self._yfmt(best['hi'])}")
        a = self.hover_ann
        a.set_text("\n".join(lines))
        a.xy = (best["px"], best["y"])
        fx = (e.x - ax.bbox.x0) / max(1, ax.bbox.width)
        fy = (e.y - ax.bbox.y0) / max(1, ax.bbox.height)
        a.set_ha("right" if fx > 0.6 else "left")
        a.set_va("top" if fy > 0.6 else "bottom")
        a.set_position((-14 if fx > 0.6 else 14, -14 if fy > 0.6 else 14))
        a.set_visible(True)
        self.hover_ring.set_data([best["px"]], [best["y"]])
        self.hover_ring.set_visible(best["kind"] == "pt")
        self.canvas.draw_idle()


# ---------------------------------------------------------------------------------------------- eval sandbox tab
SANDBOX_GROUPS = [("onb", "Overnight break", "onb_on"), ("orb", "Opening range (5-min)", "orb_on"),
                  ("exp", "Expiry-Friday fade", "exp_on"), ("cost", "Costs and money", None),
                  ("rules", "Evaluation rules (LucidFlex 25K)", None)]
SANDBOX_GROUP_NAMES = {"onb": "Overnight break", "orb": "Opening range", "exp": "Expiry fade", "cost": "", "rules": ""}
SANDBOX_DEFAULT_SWEEP = "onb_cap_pct"
SANDBOX_DEBOUNCE_MS, SANDBOX_BUSY_MS = 150, 200


def _same_value(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) < 1e-9


class ParamRow(QtWidgets.QWidget):
    """One parameter: its name and current value on one line, a slider over the parameter's grid of values below.
    An optional row (the daily loss limit) has a check box in place of the name: unticked = None (off)."""
    changed = QtCore.Signal()

    def __init__(self, key, spec, optional=False):
        super().__init__()
        self.key, self.spec, self.optional = key, spec, optional
        self.grid = [g for g in spec["grid"] if not (optional and g is None)]
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(0, 1, 0, 1)
        v.setSpacing(0)
        top = QtWidgets.QHBoxLayout()
        top.setSpacing(6)
        if optional:
            self.check = QtWidgets.QCheckBox(spec["label"])
            self.check.toggled.connect(self._toggled)
            top.addWidget(self.check)
        else:
            self.check = None
            top.addWidget(QtWidgets.QLabel(spec["label"]))
        top.addStretch(1)
        self.val = QtWidgets.QLabel()
        self.val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        f = self.val.font()
        f.setBold(True)
        self.val.setFont(f)
        top.addWidget(self.val)
        v.addLayout(top)
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setRange(0, len(self.grid) - 1)
        self.slider.setPageStep(max(1, len(self.grid) // 8))
        self.slider.valueChanged.connect(self._moved)
        v.addWidget(self.slider)
        self.setToolTip(spec.get("tip", ""))
        if optional:
            self.slider.setEnabled(False)
        self._label()

    def value(self):
        if self.check is not None and not self.check.isChecked():
            return None
        return self.grid[self.slider.value()]

    def index_of(self, x):
        if x is None:
            return len(self.grid) - 1
        return min((abs(g - float(x)), k) for k, g in enumerate(self.grid) if g is not None)[1]

    def set_value(self, x):
        if self.check is not None:
            self.check.setChecked(x is not None)
            if x is None:
                self._label()
                return
        self.slider.setValue(self.index_of(x))
        self._label()

    def _moved(self, _):
        self._label()
        self.changed.emit()

    def _toggled(self, on):
        self.slider.setEnabled(on)
        self._label()
        self.changed.emit()

    def _label(self):
        self.val.setText(self.spec["fmt"](self.value()))


class ChoiceRow(QtWidgets.QWidget):
    """A parameter with a few named choices (money: today's NQ price or as traded)."""
    changed = QtCore.Signal()

    def __init__(self, key, spec):
        super().__init__()
        self.key, self.spec = key, spec
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(0, 1, 0, 1)
        h.addWidget(QtWidgets.QLabel(spec["label"]))
        self.cb = QtWidgets.QComboBox()
        for data, text in spec["choices"]:
            self.cb.addItem(text, data)
        self.cb.currentIndexChanged.connect(lambda _: self.changed.emit())
        h.addWidget(self.cb, 1)
        self.setToolTip(spec.get("tip", ""))

    def value(self):
        return self.cb.currentData()

    def set_value(self, x):
        self.cb.setCurrentIndex(max(0, self.cb.findData(x)))


class SandboxWorker(QtCore.QObject):
    """Runs in its own QThread: evaluates the current settings (-> current) and then the sweep (-> swept). A job
    that is no longer the latest stops at the next value. Results are cached by (params, rules, window)."""
    current = QtCore.Signal(int, object)
    swept = QtCore.Signal(int, object)
    failed = QtCore.Signal(int, str)

    def __init__(self):
        super().__init__()
        self.latest, self.ps = 0, None
        from collections import OrderedDict
        self._cache = OrderedDict()

    def _eval(self, p, r, win):
        k = (p, r, win)
        hit = self._cache.get(k)
        if hit is not None:
            self._cache.move_to_end(k)
            return hit
        res = self.ps.evaluate(p, r, win[0], win[1], outcomes=False)
        self._cache[k] = res
        if len(self._cache) > 4000:
            self._cache.popitem(last=False)
        return res

    @QtCore.Slot(int, object)
    def run(self, job, req):
        if job != self.latest:
            return
        try:
            if self.ps is None:
                import prop_sim
                prop_sim.calendar()
                self.ps = prop_sim
            t0 = time.perf_counter()
            res = dict(self._eval(req["params"], req["rules"], req["window"]))
            res["seconds"] = time.perf_counter() - t0
            self.current.emit(job, res)
            rows = []
            for v in req["values"]:
                if job != self.latest:
                    return
                p, r = self.ps.with_value(req["params"], req["rules"], req["key"], v)
                rows.append(self._eval(p, r, req["window"]))
            self.swept.emit(job, dict(req=req, key=req["key"], values=list(req["values"]), rows=rows,
                                      seconds=time.perf_counter() - t0))
        except Exception:
            import traceback
            self.failed.emit(job, traceback.format_exc())


class SandboxPanel(QtWidgets.QWidget):
    """Tab 3: every setting of the three models and the evaluation rules on sliders; LucidFlex pass odds for those
    settings (prop_sim.py: an evaluation started on every trading day of the window) and a chart of the pass odds
    as one setting sweeps across its range with everything else as set. Click the chart to use a value."""
    request = QtCore.Signal(int, object)

    def __init__(self, win, preset=None, sweep=None):
        super().__init__()
        self.win = win
        self.ps, self.rows, self.groups = None, {}, {}
        self.job, self.res, self.sw, self.res_job = 0, None, None, 0
        self.fig = self.canvas = self.ax = self.ax2 = None
        self.thread = self.worker = None
        self._loading, self._started, self._pending_draw = False, False, False
        self.hover_k, self.hov = None, {}
        self.error = ""
        try:
            import prop_sim
            self.ps = prop_sim
        except Exception as ex:                      # the other tabs must keep working
            h = QtWidgets.QVBoxLayout(self)
            lab = QtWidgets.QLabel(f"The Eval sandbox needs prop_sim.py next to this script ({HERE}).\n\n{ex}")
            lab.setWordWrap(True)
            lab.setAlignment(Qt.AlignCenter)
            h.addWidget(lab)
            return
        ps = self.ps

        # ---- left: presets and every parameter
        form = QtWidgets.QWidget()
        fh = QtWidgets.QHBoxLayout(form)
        fh.setContentsMargins(0, 0, 8, 0)
        fh.setSpacing(12)
        self._cols = (QtWidgets.QVBoxLayout(), QtWidgets.QVBoxLayout())
        for col in self._cols:
            col.setSpacing(6)
            fh.addLayout(col, 1)
        pw = QtWidgets.QWidget()
        ph = QtWidgets.QHBoxLayout(pw)
        ph.setContentsMargins(0, 0, 0, 0)
        ph.addWidget(QtWidgets.QLabel("Preset:"))
        self.cb_preset = QtWidgets.QComboBox()
        self.cb_preset.addItem("Custom settings", None)
        for name in ps.PRESETS:
            self.cb_preset.addItem(name, name)
        self.cb_preset.setToolTip("Load a set of settings; any change afterwards shows 'Custom settings'")
        self.cb_preset.activated.connect(lambda i: self.apply_preset(self.cb_preset.itemData(i)))
        ph.addWidget(self.cb_preset, 1)
        self._blocks = [pw]
        for gkey, title, onkey in SANDBOX_GROUPS:
            box = QtWidgets.QGroupBox(title)
            if onkey:
                box.setCheckable(True)
                box.setToolTip(f"Tick to trade the {title.lower()} model")
                box.toggled.connect(self._changed)
            bl = QtWidgets.QVBoxLayout(box)
            bl.setContentsMargins(8, 4, 8, 6)
            bl.setSpacing(3)
            for key, spec in ps.SPECS.items():
                if spec["group"] != gkey or spec["kind"] == "bool":
                    continue
                row = ChoiceRow(key, spec) if spec["kind"] == "choice" else ParamRow(key, spec, optional=key == "dll")
                row.changed.connect(self._changed)
                bl.addWidget(row)
                self.rows[key] = row
            if gkey == "rules":
                wl = QtWidgets.QHBoxLayout()
                wl.addWidget(QtWidgets.QLabel("Starts from"))
                this_year = time.localtime().tm_year
                self.sp_from, self.sp_to = QtWidgets.QSpinBox(), QtWidgets.QSpinBox()
                for sp, v in ((self.sp_from, 2018), (self.sp_to, this_year)):
                    sp.setRange(2011, this_year)
                    sp.setValue(v)
                    sp.valueChanged.connect(self._changed)
                wl.addWidget(self.sp_from)
                wl.addWidget(QtWidgets.QLabel("to"))
                wl.addWidget(self.sp_to)
                wl.addStretch(1)
                ww = QtWidgets.QWidget()
                ww.setLayout(wl)
                wl.setContentsMargins(0, 4, 0, 0)
                ww.setToolTip("An evaluation is started on every trading day of these years (the headline odds); "
                              "the 2018-21 and 2022-26 odds always use their own years")
                bl.addWidget(ww)
                self.rule_note = QtWidgets.QLabel()
                self.rule_note.setWordWrap(True)
                bl.addWidget(self.rule_note)
            self._blocks.append(box)
            self.groups[gkey] = box
        scroll = self.scroll = QtWidgets.QScrollArea()
        scroll.setWidget(form)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._two = None
        self._arrange(False)

        # ---- right: results card, chart controls, chart, text
        right = QtWidgets.QWidget()
        rv = self.page_layout = QtWidgets.QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(4)
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("sandboxCard")
        g = QtWidgets.QGridLayout(self.card)
        g.setContentsMargins(14, 10, 14, 10)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(8)
        hero = QtWidgets.QWidget()
        hv = QtWidgets.QVBoxLayout(hero)
        hv.setContentsMargins(0, 0, 0, 0)
        hv.setSpacing(0)
        self.hero_lab = QtWidgets.QLabel("Pass odds")
        self.hero_val = QtWidgets.QLabel("–")
        f = self.hero_val.font()
        f.setPointSizeF(f.pointSizeF() * 2.5)
        self.hero_val.setFont(f)
        self.hero_sub = QtWidgets.QLabel()
        self.hero_sub.setWordWrap(True)
        for w_ in (self.hero_lab, self.hero_val, self.hero_sub):
            hv.addWidget(w_)
        hv.addStretch(1)
        hero.setMinimumWidth(170)
        hero.setMaximumWidth(230)
        g.addWidget(hero, 0, 0, 2, 1)
        self.tiles = {}
        tiles = [("fail", "Fail odds", "Share of the finished evaluations that hit the max loss"),
                 ("days", "Median days to pass", "Trading days from the start to passing (middle half in brackets)"),
                 ("worst", "Worst day", "Worst day's net $ in the start window (after any daily loss limit)"),
                 ("dd", "Max drawdown", "Largest drop of the running total of daily net $ in the start window"),
                 ("era1", "Started 2018-21", "Pass odds of the evaluations started in 2018-2021"),
                 ("era2", "Started 2022-26", "Pass odds of the evaluations started in 2022-2026"),
                 ("net", "Net $ / year", "Net $ per year over the start window, at the micros set"),
                 ("trades", "Trades / year", "Trades per year over the start window")]
        for k, (key, name, tip) in enumerate(tiles):
            w_ = QtWidgets.QWidget()
            tv = QtWidgets.QVBoxLayout(w_)
            tv.setContentsMargins(0, 0, 0, 0)
            tv.setSpacing(1)
            lab, val = QtWidgets.QLabel(name), QtWidgets.QLabel("–")
            lab.setTextFormat(Qt.RichText)
            f = val.font()
            f.setPointSizeF(f.pointSizeF() * 1.3)
            val.setFont(f)
            tv.addWidget(lab)
            tv.addWidget(val)
            w_.setToolTip(tip)
            g.addWidget(w_, k // 4, 1 + k % 4)
            self.tiles[key] = (lab, val, name)
        for c in range(1, 5):
            g.setColumnStretch(c, 1)
        rv.addWidget(self.card)
        self.warn = QtWidgets.QLabel()
        self.warn.setWordWrap(True)
        self.warn.setVisible(False)
        rv.addWidget(self.warn)
        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 6, 0, 0)
        hdr.addWidget(QtWidgets.QLabel("Chart x axis:"))
        self.cb_sweep = QtWidgets.QComboBox()
        for key in ps.SWEEPABLE:
            self.cb_sweep.addItem(ps.SPECS[key]["axis"], key)
        self.cb_sweep.setCurrentIndex(max(0, self.cb_sweep.findData(SANDBOX_DEFAULT_SWEEP)))
        self.cb_sweep.setToolTip("The setting swept across the chart; every other setting stays as in the panel")
        self.cb_sweep.currentIndexChanged.connect(self._sweep_changed)
        hdr.addWidget(self.cb_sweep)
        hdr.addStretch(1)
        self.busy_lab = QtWidgets.QLabel("")
        hdr.addWidget(self.busy_lab)
        rv.addLayout(hdr)
        self.title = QtWidgets.QLabel()
        f = self.title.font()
        f.setPointSizeF(f.pointSizeF() * 1.15)
        f.setBold(True)
        self.title.setFont(f)
        self.subtitle = QtWidgets.QLabel()
        self.subtitle.setWordWrap(True)
        rv.addWidget(self.title)
        rv.addWidget(self.subtitle)
        self.canvas_slot = rv.count()
        self.summary = QtWidgets.QLabel()
        self.summary.setWordWrap(True)
        self.note = QtWidgets.QLabel()
        self.note.setWordWrap(True)
        for w_ in (self.title, self.subtitle, self.summary, self.note, self.hero_sub, self.warn):
            w_.setTextInteractionFlags(Qt.TextSelectableByMouse)
        rv.addWidget(self.summary)
        rv.addWidget(self.note)

        h = QtWidgets.QHBoxLayout(self)
        h.addWidget(scroll)
        h.addSpacing(6)
        h.addWidget(right, 1)
        # an explicit minimum width, or this tab's layout (~1,000 px, ~1,350 px with two settings columns) becomes the
        # minimum width of the whole window on every tab; narrower than that, the right edge is cut off instead
        self.setMinimumWidth(300)

        self.debounce = QtCore.QTimer(self)
        self.debounce.setSingleShot(True)
        self.debounce.setInterval(SANDBOX_DEBOUNCE_MS)
        self.debounce.timeout.connect(self._send)
        self.busy_timer = QtCore.QTimer(self)
        self.busy_timer.setSingleShot(True)
        self.busy_timer.setInterval(SANDBOX_BUSY_MS)
        self.busy_timer.timeout.connect(lambda: self._show_busy(True))
        self.apply_preset(preset if preset in ps.PRESETS else "Current live models", schedule=False)
        if sweep:
            self.select_sweep(sweep)
        self._apply_theme()

    # ------------------------------------------------------------------ settings
    def params(self):
        from dataclasses import fields as dc_fields
        ps, v = self.ps, {k: r.value() for k, r in self.rows.items()}
        kw = {f.name: v[f.name] for f in dc_fields(ps.Params) if f.name in v}
        kw.update(onb_on=self.groups["onb"].isChecked(), orb_on=self.groups["orb"].isChecked(),
                  exp_on=self.groups["exp"].isChecked())
        return ps.Params(**kw)

    def rules(self):
        from dataclasses import fields as dc_fields
        ps, v = self.ps, {k: r.value() for k, r in self.rows.items()}
        return ps.Rules(**{f.name: v[f.name] for f in dc_fields(ps.Rules) if f.name in v})

    def window(self):
        a, b = sorted((self.sp_from.value(), self.sp_to.value()))
        return (f"{a}-01-01", f"{b}-12-31")

    def window_label(self):
        a, b = sorted((self.sp_from.value(), self.sp_to.value()))
        return str(a) if a == b else f"{a}–{b}"

    def apply_preset(self, name, schedule=True):
        if name is None or name not in self.ps.PRESETS:
            return
        p, r = self.ps.PRESETS[name]
        self._loading = True
        try:
            for gkey, on in (("onb", p.onb_on), ("orb", p.orb_on), ("exp", p.exp_on)):
                self.groups[gkey].setChecked(on)
            for key, row in self.rows.items():
                row.set_value(self.ps.get_value(p, r, key))
        finally:
            self._loading = False
        self._changed() if schedule else self._sync_texts()

    def select_sweep(self, key):
        k = key.strip()
        i = self.cb_sweep.findData(k)
        if i < 0:
            i = next((j for j in range(self.cb_sweep.count()) if k.lower() in self.cb_sweep.itemText(j).lower()), -1)
        if i < 0:
            print(f"--sweep {key}: not found; choose from {', '.join(self.ps.SWEEPABLE)}", file=sys.stderr)
            return
        self.cb_sweep.setCurrentIndex(i)

    def set_param(self, key, value):
        """Chart click: give `key` that value (its slider/check box follows)."""
        self.rows[key].set_value(value)
        self._changed()
        self.draw()

    def _sync_texts(self):
        if self.ps is None:
            return
        p, r = self.params(), self.rules()
        match = next((n for n, (pp, rr) in self.ps.PRESETS.items() if pp == p and rr == r), None)
        self.cb_preset.setCurrentIndex(max(0, self.cb_preset.findData(match)) if match else 0)
        self.rule_note.setText(
            f"Start {fmt_money(r.start)}; the max loss trails the highest end-of-day balance and locks at "
            f"{fmt_money(r.lock_level)} once a day closes above {fmt_money(r.lock_trigger_level)}. "
            f"Balances are checked at each day's close.")
        warn = []
        if not (p.onb_on or p.orb_on or p.exp_on):
            warn.append("Every model is switched off: tick a model's box to trade it.")
        if p.micros_open() > r.max_micros:
            warn.append(f"Up to {p.micros_open()} micros could be open at once (the models can overlap); "
                        f"Lucid allows {r.max_micros}.")
        key = self.cb_sweep.currentData()
        g = self.ps.SPECS[key]["group"]
        if g in ("onb", "orb", "exp") and not self.groups[g].isChecked():
            warn.append(f"The chart sweeps a {SANDBOX_GROUP_NAMES[g].lower()} setting but that model is switched "
                        f"off, so the line is flat.")
        if key == "nq_price" and p.money == "actual":
            warn.append("Money is 'as traded', so the NQ price setting has no effect.")
        if r.dll is not None or key == "dll":
            warn.append("Daily loss limit: modelled by capping each day's net loss at the limit. That flatters "
                        "small limits: a day that dips through the limit and then recovers really ends at the limit "
                        "too, which this cannot see. Trust the odds with the limit off more.")
        self.warn.setText(("Note: " if warn else "") + "  ".join(warn))
        self.warn.setVisible(bool(warn))

    def _changed(self, *_):
        if self._loading or self.ps is None:
            return
        self._sync_texts()
        if self._started:
            self.debounce.start()
            if not self.busy_timer.isActive() and not self.busy_lab.text():
                self.busy_timer.start()

    def _sweep_changed(self, *_):
        self._sync_texts()
        self._changed()

    # ------------------------------------------------------------------ background work
    def _start(self):
        if self._started or self.ps is None:
            return
        self._started = True
        self.thread = QtCore.QThread(self)
        self.worker = SandboxWorker()
        self.worker.moveToThread(self.thread)
        self.request.connect(self.worker.run)
        self.worker.current.connect(self._got_current)
        self.worker.swept.connect(self._got_sweep)
        self.worker.failed.connect(self._failed)
        self.thread.start()
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.shutdown)
        self.busy_lab.setText("loading the trade cache…")
        self._send()

    def shutdown(self):
        if self.thread is not None:
            self.worker.latest = -1
            self.thread.quit()
            self.thread.wait(10000)
            self.thread = None

    def _send(self):
        if not self._started:
            return
        p, r, win = self.params(), self.rules(), self.window()
        key = self.cb_sweep.currentData()
        vals = list(self.ps.SPECS[key]["sweep"])
        cur = self.ps.get_value(p, r, key)
        if not any(_same_value(cur, v) for v in vals):
            vals.append(cur)
        self.job += 1
        self.worker.latest = self.job
        self.request.emit(self.job, dict(params=p, rules=r, window=win, key=key, values=vals))
        if not self.busy_timer.isActive() and not self.busy_lab.text():
            self.busy_timer.start()

    def idle(self):
        return (self._started and not self.debounce.isActive() and self.sw is not None and
                self.sw.get("job") == self.job) or bool(self.error)

    def _show_busy(self, on):
        if on and self.sw is not None and self.sw.get("job") == self.job and not self.debounce.isActive():
            return
        self.busy_lab.setText("computing…" if on else "")
        for w_ in (self.card, self.canvas):
            if w_ is None:
                continue
            if on:
                eff = QtWidgets.QGraphicsOpacityEffect(w_)
                eff.setOpacity(0.5)
                w_.setGraphicsEffect(eff)
            else:
                w_.setGraphicsEffect(None)

    def _got_current(self, job, res):
        if job != self.job:
            return
        self.res, self.res_job = res, job
        self._fill_card()

    def _got_sweep(self, job, sw):
        if job != self.job:
            return
        self.error = ""
        sw["job"] = job
        self.sw = sw
        self.busy_timer.stop()
        self._show_busy(False)
        self.draw()

    def _failed(self, job, msg):
        if job != self.job:
            return
        self.error = msg
        self.busy_timer.stop()
        self._show_busy(False)
        print(msg, file=sys.stderr)
        self.summary.setText("Could not compute these settings:\n" + msg.strip().splitlines()[-1])

    # ------------------------------------------------------------------ results card
    def _fill_card(self):
        res, c = self.res, self._theme()
        pct = lambda x: "–" if x is None or not np.isfinite(x) else f"{100 * x:.1f}%"
        self.hero_val.setText(pct(res["pass_rate"]))
        n_done = res["n_pass"] + res["n_fail"]
        self.hero_sub.setText(f"of {n_done:,} finished evaluations started {self.window_label()}"
                              + (f" ({res['n_open']:,} still open)" if res["n_open"] else ""))
        q1, med, q3 = res["days_pass"]
        e1, e2 = res["eras"]["2018-21"], res["eras"]["2022-26"]
        vals = {"fail": pct(res["fail_rate"]),
                "days": "–" if not np.isfinite(med) else f"{med:.0f}  ({q1:.0f}–{q3:.0f})",
                "worst": fmt_money(res["worst_day"]), "dd": fmt_money(res["max_dd"]),
                "era1": pct(e1["pass_rate"]), "era2": pct(e2["pass_rate"]),
                "net": fmt_money(res["net_yr"]), "trades": "–" if not np.isfinite(res["trades_yr"])
                else f"{res['trades_yr']:.0f}"}
        for key, (lab, val, name) in self.tiles.items():
            val.setText(vals[key])
            if key in ("era1", "era2"):
                col = c["series"][1 if key == "era1" else 2]
                lab.setText(f"<span style='color:{col}'>&#9644;</span> <span style='color:{c['muted']}'>"
                            f"{html.escape(name)}</span>")
            else:
                lab.setText(f"<span style='color:{c['muted']}'>{html.escape(name)}</span>")
        self.hero_lab.setText(f"<span style='color:{c['muted']}'>Pass odds</span>")

    # ------------------------------------------------------------------ chart
    def _theme(self):
        return StudiesPanel._theme(self)

    def _apply_theme(self):
        if self.ps is None:
            return
        c = self._theme()
        self.card.setStyleSheet(f"#sandboxCard {{ background: {c['base']}; border: 1px solid {c['grid']}; "
                                f"border-radius: 6px; }}")
        base = QtWidgets.QApplication.palette().color(QtGui.QPalette.Base)
        for w_ in [self.groups[g] for g in ("onb", "orb", "exp")] + [self.rows["dll"].check]:
            pal = QtGui.QPalette(w_.palette())          # an unticked box must stay visible on the dark surface
            pal.setColor(QtGui.QPalette.Base, QtGui.QColor("#55554f") if c["dark"] else base)
            w_.setPalette(pal)
        for w_, col in ((self.title, c["ink"]), (self.subtitle, c["muted"]), (self.summary, c["ink"]),
                        (self.note, c["muted"]), (self.hero_sub, c["muted"]), (self.busy_lab, c["muted"]),
                        (self.rule_note, c["muted"]), (self.warn, "#d95926" if c["dark"] else "#b4441b")):
            w_.setStyleSheet(f"color: {col}")
        if self.res is not None:
            self._fill_card()

    def on_palette(self):
        self._apply_theme()
        self.draw()

    def _arrange(self, two):
        """Settings in one scrolling column, or two side by side when the window is wide enough to show them all."""
        if two == self._two:
            return
        self._two = two
        for col in self._cols:
            while col.count():
                col.takeAt(0)
        a, b = self._cols
        split = 4 if two else len(self._blocks)       # preset + the three models | costs + rules
        for k, w_ in enumerate(self._blocks):
            (a if k < split else b).addWidget(w_)
        a.addStretch(1)
        b.addStretch(1)
        self.scroll.setFixedWidth(2 * 330 + 20 if two else 338)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.ps is not None:
            self._arrange(self.width() >= 1500)

    def showEvent(self, e):
        super().showEvent(e)
        self._start()
        QtCore.QTimer.singleShot(0, self.draw)

    def eventFilter(self, obj, e):
        if obj is self.canvas and e.type() == QtCore.QEvent.Resize:
            QtCore.QTimer.singleShot(0, self.draw)          # tick-label thinning follows the width
        return super().eventFilter(obj, e)

    def _ensure_canvas(self):
        if self.canvas is not None:
            return
        import logging
        import matplotlib
        matplotlib.use("QtAgg")
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        from matplotlib import font_manager
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
        matplotlib.rcParams["text.parse_math"] = False          # '$' in labels is a dollar sign, not math
        fam = QtGui.QFontInfo(self.font()).family()
        names = {f.name for f in font_manager.fontManager.ttflist}
        matplotlib.rcParams["font.family"] = [fam] if fam in names else ["sans-serif"]
        matplotlib.rcParams["font.size"] = self.font().pointSizeF() or 9.0
        self.fig = Figure(dpi=self.logicalDpiX() or 96)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setMinimumHeight(260)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.canvas.setCursor(Qt.PointingHandCursor)
        self.page_layout.insertWidget(self.canvas_slot, self.canvas, 1)
        self.canvas.mpl_connect("motion_notify_event", self._hover)
        self.canvas.mpl_connect("figure_leave_event", lambda _: self._hide_hover())
        self.canvas.mpl_connect("button_press_event", self._click)
        self.canvas.installEventFilter(self)

    @staticmethod
    def _xinfo(values, cur):
        """Evenly spaced x positions for the tested values (ascending, None = 'no cap' / 'off' / 'close' / 'no rule'
        last), so close values (9:35, 9:45, 9:55) stay apart and clickable; the tick labels carry the values.
        Returns (position of each value, position of `cur`: interpolated while a new sweep is on its way)."""
        nums = sorted({float(v) for v in values if v is not None})
        rank = {v: float(k) for k, v in enumerate(nums)}
        none_x = float(len(nums))
        xs = np.array([none_x if v is None else rank[float(v)] for v in values])
        if cur is None:
            cx = none_x
        elif nums:
            cx = float(np.interp(float(cur), nums, np.arange(len(nums), dtype=float)))
        else:
            cx = 0.0
        return xs, cx

    def _thin_ticks(self, xs, labels, keep_first, ppu, x0):
        """Indices of the tick labels to show: the current value first, then the ends, then the rest, each only if
        it does not overlap a label already kept."""
        fm = QtGui.QFontMetrics(self.font())
        order = list(keep_first) + [0, len(xs) - 1] + list(range(1, len(xs) - 1))
        kept = []
        for k in dict.fromkeys(order):
            if k is None or not 0 <= k < len(xs):
                continue
            px, w = (xs[k] - x0) * ppu, fm.horizontalAdvance(labels[k]) + 12
            if all(abs(px - (xs[j] - x0) * ppu) >= (w + fm.horizontalAdvance(labels[j]) + 12) / 2 for j in kept):
                kept.append(k)
        return sorted(kept)

    def draw(self):
        if not self.isVisible() or self.sw is None or self.ps is None:
            return
        self._ensure_canvas()
        try:
            self._plot()
        except Exception as ex:                  # a drawing problem must not take the GUI down
            import traceback
            traceback.print_exc()
            self.summary.setText(f"Could not draw the chart: {ex}")

    def _plot(self):
        ps, c, sw = self.ps, self._theme(), self.sw
        key, spec = sw["key"], ps.SPECS[sw["key"]]
        vals, rows = sw["values"], sw["rows"]
        p_now, r_now = self.params(), self.rules()
        cur = ps.get_value(p_now, r_now, key)
        xs, cur_x = self._xinfo(vals, cur)
        step = 1.0
        order = np.argsort(xs, kind="stable")
        vals = [vals[k] for k in order]
        rows = [rows[k] for k in order]
        xs = xs[order]
        self.plot_vals, self.plot_rows, self.plot_xs, self.plot_key = vals, rows, xs, key
        tick = spec.get("tick", spec["fmt"])
        wl = self.window_label()
        group = SANDBOX_GROUP_NAMES[spec["group"]]
        self.title.setText(f"Pass odds against {spec['axis'][0].lower() + spec['axis'][1:]}")
        self.subtitle.setText("Share of the finished evaluations that passed; everything else as in the panel. "
                              "Hover for the numbers, click a point to use its value.")
        series = [("all", f"All starts {wl}", c["series"][0], np.array([r["pass_rate"] for r in rows], float)),
                  ("2018-21", "Started 2018–21", c["series"][1],
                   np.array([r["eras"]["2018-21"]["pass_rate"] for r in rows], float)),
                  ("2022-26", "Started 2022–26", c["series"][2],
                   np.array([r["eras"]["2022-26"]["pass_rate"] for r in rows], float))]
        med = np.array([r["days_pass"][1] for r in rows], float)
        q1 = np.array([r["days_pass"][0] for r in rows], float)
        q3 = np.array([r["days_pass"][2] for r in rows], float)
        isnum = np.array([v is not None for v in vals])

        fig = self.fig
        fig.clear()
        fig.set_facecolor(c["bg"])
        gs = fig.add_gridspec(2, 1, height_ratios=[2.6, 1])
        ax = self.ax = fig.add_subplot(gs[0])
        ax2 = self.ax2 = fig.add_subplot(gs[1], sharex=ax)
        lo_x, hi_x = min(xs.min(), cur_x), max(xs.max(), cur_x)
        pad = 0.5 * step
        ax.set_xlim(lo_x - pad, hi_x + pad)
        for a in (ax, ax2):
            a.set_facecolor(c["bg"])
            a.axvspan(cur_x - 0.42 * step, cur_x + 0.42 * step, color=c["ink"], alpha=0.06, lw=0, zorder=0)
        kw = dict(lw=2, marker="o", ms=6.5, mec=c["bg"], mew=1.5, solid_capstyle="round", solid_joinstyle="round")
        for j, (sid, lab, col, y) in enumerate(series):
            z = 4 if sid == "all" else 3
            ax.plot(xs[isnum], 100 * y[isnum], color=col, label=lab, zorder=z, **kw)
            if (~isnum).any():          # 'no cap' / 'off': a point of its own, not joined to the line
                ax.plot(xs[~isnum], 100 * y[~isnum], ls="none", color=col, zorder=z,
                        **{k: v for k, v in kw.items() if k not in ("lw", "solid_capstyle", "solid_joinstyle")})
        ax.set_ylim(0, 112)
        # the current setting: label at the top of its column and its value on the main line
        self._cur_ann = ax.annotate("current", xy=(cur_x, 1), xycoords=("data", "axes fraction"), xytext=(0, -4),
                                    textcoords="offset points", ha="center", va="top", color=c["muted"],
                                    fontsize="small")
        k_cur = next((k for k, v in enumerate(vals) if _same_value(v, cur)), None)
        y_all = series[0][3]
        if k_cur is not None and np.isfinite(y_all[k_cur]):
            ax.plot([cur_x], [100 * y_all[k_cur]], ls="none", marker="D", ms=10, mfc="none", mec=c["ink"], mew=1.5,
                    zorder=5)
        fin = np.isfinite(y_all)
        k_best = int(np.nanargmax(np.where(fin, y_all, -1))) if fin.any() else None
        if k_best is not None:
            if k_cur is None or not np.isclose(y_all[k_best], y_all[k_cur]):
                ax.plot([xs[k_best]], [100 * y_all[k_best]], ls="none", marker="o", ms=13, mfc="none",
                        mec=c["ink"], mew=1.5, zorder=5)
                txt = f"highest {100 * y_all[k_best]:.1f}%"
                bx = xs[k_best]
            else:
                txt = f"current {100 * y_all[k_cur]:.1f}% = highest"
                bx = cur_x
            best_lab = (txt, bx, 100 * y_all[k_best])
        else:
            best_lab = None

        # median days to pass, with the middle half of the passes as a band
        fd = isnum & np.isfinite(med)
        ax2.fill_between(xs[fd], q1[fd], q3[fd], color=c["series"][0], alpha=0.2 if c["dark"] else 0.13, lw=0,
                         zorder=1)
        ax2.plot(xs[fd], med[fd], color=c["series"][0], zorder=3, **kw)
        nd = ~isnum & np.isfinite(med)
        for k in np.flatnonzero(nd):
            ax2.fill_between([xs[k] - 0.15 * step, xs[k] + 0.15 * step], q1[k], q3[k], color=c["series"][0],
                             alpha=0.2 if c["dark"] else 0.13, lw=0, zorder=1)
        if nd.any():
            ax2.plot(xs[nd], med[nd], ls="none", color=c["series"][0], zorder=3,
                     **{k: v for k, v in kw.items() if k not in ("lw", "solid_capstyle", "solid_joinstyle")})
        top = np.nanmax(q3) if np.isfinite(q3).any() else 10.0
        ax2.set_ylim(0, max(10.0, top * 1.12))
        ax2.set_title("Median trading days to pass  (band: middle half of the passes)", loc="left",
                      fontsize="small", color=c["ink"], pad=4)

        from matplotlib.ticker import FuncFormatter, MaxNLocator
        for a in (ax, ax2):
            for side in ("top", "right", "left"):
                a.spines[side].set_visible(False)
            a.spines["bottom"].set_color(c["grid"])
            a.yaxis.grid(True, color=c["grid"], lw=0.8, zorder=0)
            a.set_axisbelow(True)
            a.tick_params(axis="both", length=0, colors=c["axis"], labelcolor=c["axis"], pad=6)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
        ax2.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True, steps=[1, 2, 2.5, 5, 10]))
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
        ax.tick_params(axis="x", labelbottom=False)
        labels = [tick(v) for v in vals]
        W = self.canvas.width()
        ppu = max(150.0, W - 120.0) / max(1e-9, ax.get_xlim()[1] - ax.get_xlim()[0])
        shown = self._thin_ticks(xs, labels, [k_cur], ppu, ax.get_xlim()[0])
        ax2.set_xticks([xs[k] for k in shown])
        ax2.set_xticklabels([labels[k] for k in shown])
        ax2.set_xlabel(spec["axis"], color=c["muted"], labelpad=8)
        hs, ls = ax.get_legend_handles_labels()
        leg = ax.legend(hs, ls, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=3, frameon=False, handlelength=1.6,
                        columnspacing=1.4, borderaxespad=0, fontsize="small")
        for t in leg.get_texts():
            t.set_color(c["ink"])
        fig.set_layout_engine("constrained", h_pad=0.06, w_pad=0.12)
        if best_lab is not None:
            self._place_label(ax, best_lab, series, xs, isnum, c)

        # hover layer: a crosshair through both charts, rings on the points, one tooltip
        self.hov = {"lines": [a.axvline(xs[0], color=c["muted"], lw=1, zorder=2, visible=False) for a in (ax, ax2)],
                    "rings": [ax.plot([], [], ls="none", marker="o", ms=11, mfc="none", mec=c["ink"], mew=1.5,
                                      zorder=7, visible=False)[0] for _ in series] +
                             [ax2.plot([], [], ls="none", marker="o", ms=11, mfc="none", mec=c["ink"], mew=1.5,
                                       zorder=7, visible=False)[0]],
                    "ann": ax.annotate("", xy=(0, 0), xytext=(12, 12), textcoords="offset points", fontsize="small",
                                       color=c["ink"], zorder=10, visible=False, annotation_clip=False,
                                       bbox=dict(boxstyle="round,pad=0.45", fc=c["base"], ec=c["grid"], lw=1)),
                    "series": series, "med": med, "q": (q1, q3)}
        self.hover_k = None

        # text under the chart
        res = self.res
        fmtv = spec["fmt"]
        name = (group + " " + spec["label"].lower()) if group else spec["label"].lower()
        lines = []
        if res is not None and np.isfinite(res["pass_rate"]):
            lines.append(f"At these settings {100 * res['pass_rate']:.1f}% of the {res['n_pass'] + res['n_fail']:,} "
                         f"finished evaluations started {wl} passed (2018–21: "
                         f"{100 * res['eras']['2018-21']['pass_rate']:.1f}%, 2022–26: "
                         f"{100 * res['eras']['2022-26']['pass_rate']:.1f}%).")
        if k_best is not None:
            if k_cur is not None and np.isclose(y_all[k_best], y_all[k_cur]):
                lines.append(f"On this chart the current {name} ({fmtv(cur)}) has the highest pass odds.")
            elif k_cur is not None and np.isfinite(y_all[k_cur]):
                lines.append(f"On this chart the highest pass odds are at {name} {fmtv(vals[k_best])}: "
                             f"{100 * y_all[k_best]:.1f}%, {100 * (y_all[k_best] - y_all[k_cur]):+.1f} points vs the "
                             f"current {fmtv(cur)}. Check both eras before switching: a peak in one era only is "
                             f"often luck.")
        self.summary.setText(" ".join(lines))
        money = ("each trade's points rescaled to NQ " + f"{p_now.nq_price:,.0f}" if p_now.money == "today"
                 else "$ as traded")
        self.note.setText(
            f"Every trading day starts an evaluation, run until it passes, fails or the data ends (still-open ones "
            f"are left out). Engine fills at {p_now.slippage_ticks} tick(s) per fill + $1 commission; money: {money}. "
            f"Limits: the balance is checked at each day's close (an intraday dip through the max loss is missed); "
            f"the daily loss limit is approximated by capping each day's loss; past data, many settings tried. "
            f"{len(rows)} settings in {sw['seconds']:.2f} s.")
        self.canvas.draw_idle()

    def _place_label(self, ax, lab, series, xs, isnum, c):
        """The 'highest' label next to its point, at the candidate spot that covers no line or point and keeps the
        most room (measured in pixels after the layout); when every spot beside the point is crowded, in the empty
        band above 100% with a thin leader line."""
        txt, x, y = lab
        self.fig.draw_without_rendering()
        T = ax.transData
        lines, marks = [], []
        for _, _, _, yy in series:
            ok = isnum & np.isfinite(yy)
            P = T.transform(np.c_[xs[ok], 100 * yy[ok]]) if ok.any() else np.zeros((0, 2))
            for (x0, y0), (x1, y1) in zip(P[:-1], P[1:]):
                t = np.linspace(0, 1, 24)
                lines.append(np.c_[x0 + t * (x1 - x0), y0 + t * (y1 - y0)])
            fin = np.isfinite(yy)
            if fin.any():
                marks.append(T.transform(np.c_[xs[fin], 100 * yy[fin]]))
        cb = self._cur_ann.get_window_extent()                 # the 'current' tag is an obstacle too
        gx, gy = np.meshgrid(np.linspace(cb.x0, cb.x1, 8), np.linspace(cb.y0, cb.y1, 3))
        lines.append(np.c_[gx.ravel(), gy.ravel()])
        lines = np.vstack(lines) if lines else np.zeros((0, 2))
        marks = np.vstack(marks) if marks else np.zeros((0, 2))
        px, py = T.transform((x, y))
        k = self.fig.dpi / 72.0
        fm = QtGui.QFontMetrics(self.font())
        w = fm.horizontalAdvance(txt) * 0.92 + 6
        h = fm.height() * 0.85 + 2
        bb = ax.bbox
        head_y = T.transform((x, 106.0))[1]                    # middle of the empty band above 100%

        def box(cx, cy, ha, va):
            x0 = cx - (w / 2 if ha == "center" else (w if ha == "right" else 0))
            y0 = cy - (h / 2 if va == "center" else (h if va == "top" else 0))
            return x0, y0, x0 + w, y0 + h

        def score(b, pref):
            x0, y0, x1, y1 = b
            sc = 12.0
            for P, weight, r in ((lines, 1.0, 1.5), (marks, 40.0, 5.0)):
                if not len(P):
                    continue
                ddx = np.maximum(np.maximum(x0 - P[:, 0], 0), P[:, 0] - x1)
                ddy = np.maximum(np.maximum(y0 - P[:, 1], 0), P[:, 1] - y1)
                d = np.hypot(ddx, ddy) - r
                hit = d < 0
                sc = min(sc, float(d.min())) if not hit.any() else sc - 100 * weight * hit.sum()
            out = max(0, bb.x0 - x0) + max(0, x1 - bb.x1) + max(0, bb.y0 - y0) + max(0, y1 - bb.y1)
            return sc - 20 * out - pref

        cands = []
        for dx, dy, ha, va in ((0, 11, "center", "bottom"), (0, -13, "center", "top"), (13, 0, "left", "center"),
                               (-13, 0, "right", "center"), (9, 9, "left", "bottom"), (-9, 9, "right", "bottom"),
                               (9, -9, "left", "top"), (-9, -9, "right", "top")):
            b = box(px + dx * k, py + dy * k, ha, va)
            cands.append((score(b, 0.5 if dy <= 0 else 0.0), ("near", dx, dy, ha, va)))
        for off in (0, w * 0.6, -w * 0.6, w * 1.2, -w * 1.2):
            b = box(px + off, head_y, "center", "center")
            cands.append((score(b, 4.0), ("head", off)))       # only when nothing beside the point is clear
        best = max(cands, key=lambda t: t[0])[1]
        kw = dict(color=c["ink"], fontsize="small", fontweight="bold", zorder=6, annotation_clip=False,
                  bbox=dict(boxstyle="round,pad=0.15", fc=c["bg"], ec="none"))
        if best[0] == "near":
            _, dx, dy, ha, va = best
            ax.annotate(txt, xy=(x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, **kw)
        else:
            tx = T.inverted().transform((px + best[1], head_y))[0]
            ax.annotate(txt, xy=(x, y), xytext=(tx, 106.0), textcoords="data", ha="center", va="center",
                        arrowprops=dict(arrowstyle="-", color=c["muted"], lw=0.8, shrinkA=0, shrinkB=7), **kw)

    def _nearest(self, e):
        if self.ax is None or e.inaxes not in (self.ax, self.ax2) or e.xdata is None:
            return None
        return int(np.argmin(np.abs(self.plot_xs - e.xdata)))

    def _hide_hover(self):
        if self.hov and self.hover_k is not None:
            for a in self.hov["lines"] + self.hov["rings"] + [self.hov["ann"]]:
                a.set_visible(False)
            self.hover_k = None
            self.canvas.draw_idle()

    def _hover(self, e):
        k = self._nearest(e)
        if k is None:
            self._hide_hover()
            return
        if k == self.hover_k:
            return
        self.hover_k = k
        ps, spec, x = self.ps, self.ps.SPECS[self.plot_key], self.plot_xs[k]
        row, v = self.plot_rows[k], self.plot_vals[k]
        for ln in self.hov["lines"]:
            ln.set_xdata([x, x])
            ln.set_visible(True)
        for ring, (_, _, _, y) in zip(self.hov["rings"], self.hov["series"]):
            ring.set_data([x], [100 * y[k]])
            ring.set_visible(bool(np.isfinite(y[k])))
        med = self.hov["med"][k]
        self.hov["rings"][-1].set_data([x], [med])
        self.hov["rings"][-1].set_visible(bool(np.isfinite(med)))
        pct = lambda z: "–" if not np.isfinite(z) else f"{100 * z:.1f}%"
        group = SANDBOX_GROUP_NAMES[spec["group"]]
        q1, _, q3 = row["days_pass"]
        cur = ps.get_value(self.params(), self.rules(), self.plot_key)
        lines = [f"{group + ' · ' if group else ''}{spec['label']}: {spec['fmt'](v)}",
                 f"pass {pct(row['pass_rate'])}   (2018–21 {pct(row['eras']['2018-21']['pass_rate'])}, "
                 f"2022–26 {pct(row['eras']['2022-26']['pass_rate'])})",
                 "median days to pass " + ("–" if not np.isfinite(med) else f"{med:.0f}  (middle half "
                                                                            f"{q1:.0f}–{q3:.0f})"),
                 f"worst day {fmt_money(row['worst_day'])}, max drawdown {fmt_money(row['max_dd'])}",
                 f"net {fmt_money(row['net_yr'])} a year",
                 "current setting" if _same_value(v, cur) else "click to use this value"]
        a = self.hov["ann"]
        a.set_text("\n".join(lines))
        ya = self.hov["series"][0][3][k]
        a.xy = (x, 100 * ya if np.isfinite(ya) else 50)
        fx = (x - self.ax.get_xlim()[0]) / (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
        fy = (a.xy[1] - self.ax.get_ylim()[0]) / (self.ax.get_ylim()[1] - self.ax.get_ylim()[0])
        a.set_ha("right" if fx > 0.55 else "left")
        a.set_va("top" if fy > 0.55 else "bottom")
        a.set_position((-14 if fx > 0.55 else 14, -14 if fy > 0.55 else 14))
        a.set_visible(True)
        self.canvas.draw_idle()

    def _click(self, e):
        if getattr(e, "button", None) != 1:
            return
        k = self._nearest(e)
        if k is None:
            return
        self.set_param(self.plot_key, self.plot_vals[k])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setWindowTitle("Model heatmap")
        w, h = 1680, 860
        if getattr(args, "size", None):
            w, h = (int(v) for v in args.size.lower().split("x"))
        self.resize(w, h)
        self.T, self.n_skipped = None, 0
        self.rows, self.fracs, self.periods, self.colors = [], None, None, None
        self.partial, self.data_span = None, None
        self.year_fracs, self.heat_title, self.legend_limit = ([], []), "", None
        self.cur_metric, self.scale_mode, self.detail_key = args.metric, args.scale, None
        self.cum_unit = getattr(args, "cum", "usd") or "usd"
        self.cum_title = ""
        self.extras, self.xinfo, self._xid = [], {}, 0       # extra trade files, key -> (name, rule, tip, html)
        self.load_errors = []
        self._split_rows = None

        self._build_menus()
        bar = FlowLayout(hspace=10, vspace=4)
        self.cb_metric = self._combo(bar, "Measure", [(v[0], k) for k, v in METRICS.items()], args.metric)
        self.cb_period = self._combo(bar, "Period", [(v[0], k) for k, v in PERIODS.items()], args.period)
        self.cb_smooth = self._combo(bar, "Smoothing", [("None", 0)] + [(f"Last {n} periods", n) for n in SMOOTH[1:]],
                                     args.smooth)
        self.cb_scale = self._combo(bar, "Color scale", [("Each row on its own", "row"), ("Shared by all rows", "shared")],
                                    args.scale)
        self.cb_colors = self._combo(bar, "Colors", [(v["label"], k) for k, v in RAMPS.items()], args.colors)
        self.ck_skipped = QtWidgets.QCheckBox("Include trades the skip rules removed")
        self.ck_skipped.setToolTip("Adds back the trades removed by rules R1 (day after the S&P fell 2%+) and R2 "
                                   "(opening range on Fed days), to see how they did")
        self.ck_all = QtWidgets.QCheckBox("All-models row")
        self.ck_all.setChecked(True)
        self.ck_extra = QtWidgets.QCheckBox("Include extra files in all-models row")
        self.ck_extra.setToolTip("Off: the all-models row is only the main trades file's models. On: it also adds "
                                 "every trade of the extra files' rows, one micro each")
        self.ck_extra.setChecked(bool(getattr(args, "include_extra", False)))
        for w_ in (self.ck_skipped, self.ck_all, self.ck_extra):
            bar.addWidget(w_)
            w_.toggled.connect(self.refresh)
        b_add = QtWidgets.QPushButton("Add trades file…")
        b_add.setToolTip("Show the trades of another per-trade CSV as extra rows (needs a date and a net bp, or net "
                         "points and an entry price)")
        b_reload, b_save = QtWidgets.QPushButton("Reload files"), QtWidgets.QPushButton("Save image…")
        b_add.clicked.connect(self.add_file_dialog)
        b_reload.clicked.connect(self.reload)
        b_save.clicked.connect(self.save_image)
        for b in (b_add, b_reload, b_save):
            bar.addWidget(b)

        self.table = QtWidgets.QTableWidget(0, len(COLS))
        self.header = TimeHeader(self)
        self.table.setHorizontalHeader(self.header)
        for c, name in enumerate(COLS):
            it = QtWidgets.QTableWidgetItem(name)
            if c in COL_TIPS:
                it.setToolTip(COL_TIPS[c])
            self.table.setHorizontalHeaderItem(c, it)
        self.header.setFixedHeight(2 * self.fontMetrics().height() + 14)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(COL_MODEL, QtWidgets.QHeaderView.Fixed)
        self.header.setSectionResizeMode(COL_CUM, QtWidgets.QHeaderView.Fixed)
        self.header.setSectionResizeMode(COL_HEAT, QtWidgets.QHeaderView.Stretch)
        self.table.setColumnWidth(COL_MODEL, 300)
        self.table.setColumnWidth(COL_CUM, 170)
        self.header.setMinimumSectionSize(30)
        self.table.installEventFilter(self)

        self.detail_label = QtWidgets.QLabel("Click a heatmap cell to list that period's trades here.")
        self.detail_label.setTextFormat(Qt.PlainText)
        self.detail = QtWidgets.QTableWidget(0, 8)
        self.detail.setHorizontalHeaderLabels(["Model", "Date", "Side", "Exit", "bp", "R", "Net $", "Removed by"])
        self.detail.verticalHeader().setVisible(False)
        self.detail.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.detail.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.detail.horizontalHeader().setStretchLastSection(True)
        low = QtWidgets.QWidget()
        lv = QtWidgets.QVBoxLayout(low)
        lv.setContentsMargins(0, 4, 0, 0)
        lv.addWidget(self.detail_label)
        lv.addWidget(self.detail)

        top = QtWidgets.QWidget()
        tv = QtWidgets.QVBoxLayout(top)
        tv.setContentsMargins(0, 0, 0, 0)
        tv.addWidget(self.table)
        self.legend = Legend(self)
        tv.addWidget(self.legend)
        tv.addStretch(1)
        split = self.split = QtWidgets.QSplitter(Qt.Vertical)
        split.addWidget(top)
        split.addWidget(low)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 1)
        split.setChildrenCollapsible(False)

        central = self.heat_page = QtWidgets.QWidget()
        cv = QtWidgets.QVBoxLayout(central)
        cv.addLayout(bar)
        cv.addWidget(split, 1)
        self.studies = StudiesPanel(self, getattr(args, "studies", None) or
                                    os.path.join(HERE, "data", "analysis", "studies.csv"))
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.addTab(central, "Heatmap")
        self.tabs.addTab(self.studies, "Studies")
        self.sandbox = SandboxPanel(self, getattr(args, "preset", None), getattr(args, "sweep", None))
        self.tabs.addTab(self.sandbox, "Eval sandbox")
        self.setCentralWidget(self.tabs)
        if getattr(args, "tab", "heatmap") == "studies":
            self.tabs.setCurrentWidget(self.studies)
        elif getattr(args, "tab", "heatmap") == "sandbox":
            self.tabs.setCurrentWidget(self.sandbox)
        if getattr(args, "model", None) or getattr(args, "study", None):
            self.studies.select(args.model, args.study)
        self.status = QtWidgets.QLabel()
        self.statusBar().addWidget(self.status, 1)
        for path in getattr(args, "extra", None) or []:
            self.add_extra(path, refresh=False)
        self.reload()

    def _build_menus(self):
        mb = self.menuBar()
        mf = mb.addMenu("&File")
        mf.addAction("Add trades file…", self.add_file_dialog)
        self.act_remove = mf.addAction("Remove extra files", self.remove_extras)
        mf.addSeparator()
        mf.addAction("Reload files", self.reload)
        mf.addAction("Reload studies", lambda: self.studies.reload())
        mf.addAction("Save image…", self.save_image)
        mf.addSeparator()
        mf.addAction("Quit", self.close)
        mv = mb.addMenu("&View")
        sub = mv.addMenu("Cumulative column shows")
        grp = QtGui.QActionGroup(self)
        grp.setExclusive(True)
        self.cum_actions = {}
        for key, (label, _) in CUM_UNITS.items():
            a = sub.addAction(label)
            a.setCheckable(True)
            a.setChecked(key == self.cum_unit)
            a.triggered.connect(lambda _=False, k=key: self.set_cum_unit(k))
            grp.addAction(a)
            self.cum_actions[key] = a

    def set_cum_unit(self, key):
        self.cum_unit = key
        self.cum_actions[key].setChecked(True)
        self.refresh()

    def _combo(self, bar, label, items, current):
        box = QtWidgets.QWidget()           # label + combo stay together when the toolbar wraps
        h = QtWidgets.QHBoxLayout(box)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)
        h.addWidget(QtWidgets.QLabel(label + ":"))
        cb = QtWidgets.QComboBox()
        for text, data in items:
            cb.addItem(text, data)
        i = cb.findData(current)
        cb.setCurrentIndex(max(0, i))
        cb.currentIndexChanged.connect(self.refresh)
        h.addWidget(cb)
        bar.addWidget(box)
        return cb

    # ------------------------------------------------------------------ theme
    def _theme(self):
        pal = self.palette()
        dark = pal.color(QtGui.QPalette.Window).lightness() < 128
        self.ink = pal.color(QtGui.QPalette.WindowText)
        self.muted = QtGui.QColor("#898781")
        self.hairline = QtGui.QColor(255, 255, 255, 40) if dark else QtGui.QColor(11, 11, 11, 40)
        self.colors = Colors(self.cb_colors.currentData(), dark)

    def changeEvent(self, e):
        if e.type() in (QtCore.QEvent.PaletteChange, QtCore.QEvent.ApplicationPaletteChange) and self.T is not None:
            self.refresh()
            if hasattr(self, "studies"):
                QtCore.QTimer.singleShot(0, self.studies.draw)
            if hasattr(self, "sandbox"):
                QtCore.QTimer.singleShot(0, self.sandbox.on_palette)
        super().changeEvent(e)

    def closeEvent(self, e):
        if hasattr(self, "sandbox"):
            self.sandbox.shutdown()                 # stop its worker thread before the window goes
        super().closeEvent(e)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        QtCore.QTimer.singleShot(0, self._fit_layout)

    def eventFilter(self, obj, e):
        if obj is self.table and e.type() == QtCore.QEvent.Resize:
            QtCore.QTimer.singleShot(0, self._fit_layout)
        return super().eventFilter(obj, e)

    # ------------------------------------------------------------------ extra trade files
    def add_extra(self, path, refresh=True):
        """Load one extra per-trade CSV (replacing it if it is already shown). Returns True on success."""
        path = os.path.abspath(path)
        try:
            df, notes = load_extra(path)
        except Exception as ex:
            msg = str(ex)
            self.load_errors.append(msg)
            print(f"Could not add {path}:\n{msg}", file=sys.stderr)
            if refresh:
                QtWidgets.QMessageBox.critical(self, "Could not add trades file", msg)
            return False
        old = next((x for x in self.extras if x["path"] == path), None)
        xid = old["id"] if old else self._xid
        if not old:
            self._xid += 1
        shown, longer = short_path(path, 2).removeprefix("…/"), short_path(path, 3)
        keys = []
        for m in dict.fromkeys(df.model):        # models in file order
            key = f"x{xid}:{m}"
            keys.append(key)
            n = int((df.model == m).sum())
            name = f"{m} ({shown})"
            rule = f"from {longer} · {n:,} trades"
            tip = (f"{html.escape(str(m))}<br>from {html.escape(path)}<br>" +
                   html.escape("; ".join(notes)) + "<br>Not in the all-models row unless "
                   "'Include extra files in all-models row' is ticked")
            lab = (f"<b>{html.escape(str(m))}</b> ({html.escape(shown).replace('/', '/&#8203;')})"
                   f"<br><span style='color:{{muted}}'>{html.escape(rule).replace('/', '/&#8203;')}</span>")
            self.xinfo[key] = (name, rule, tip, lab)
        df = df.assign(model=df.model.map(dict(zip(dict.fromkeys(df.model), keys))))
        entry = {"id": xid, "path": path, "df": df, "keys": keys, "notes": notes}
        if old:
            self.extras[self.extras.index(old)] = entry
        else:
            self.extras.append(entry)
        if refresh:
            self.refresh()
        return True

    def add_file_dialog(self):
        start = os.path.dirname(self.extras[-1]["path"]) if self.extras else HERE
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Add trades file", start,
                                                          "CSV files (*.csv);;All files (*)")
        for p in paths:
            self.add_extra(p)

    def remove_extras(self):
        self.extras, self.xinfo = [], {}
        self.refresh()

    # ------------------------------------------------------------------ data -> rows
    def reload(self):
        a = self.args
        try:
            self.T, self.n_skipped = load_trades(a.trades, a.skipped)
        except Exception as ex:          # show the problem instead of crashing
            QtWidgets.QMessageBox.critical(self, "Could not read trades", str(ex))
            if self.T is None:
                self.T = pd.DataFrame(columns=["model", "date", "bp", "usd", "R", "side", "exit", "skip_rule"])
        if self.sender() is not None:     # Reload button / menu: re-read the extra files too
            for x in list(self.extras):
                self.add_extra(x["path"], refresh=False)
        self.ck_skipped.setEnabled(self.n_skipped > 0)
        self.refresh()

    def refresh(self, *_):
        if self.T is None:
            return
        self._theme()
        self.cur_metric = self.cb_metric.currentData()
        freq, smooth = self.cb_period.currentData(), int(self.cb_smooth.currentData())
        self.scale_mode = self.cb_scale.currentData()
        T = self.T if self.ck_skipped.isChecked() else self.T[self.T.skip_rule == ""]
        X = pd.concat([x["df"] for x in self.extras], ignore_index=True) if self.extras else T.iloc[:0]
        A = pd.concat([T, X], ignore_index=True) if len(X) else T          # everything on screen: sets the time axis
        self.ck_extra.setEnabled(bool(self.extras))
        self.act_remove.setEnabled(bool(self.extras))
        include_x = self.ck_extra.isChecked() and len(X) > 0
        self.rows = []
        if len(A):
            periods = pd.period_range(A.date.min().to_period(freq), A.date.max().to_period(freq), freq=freq)
            starts = periods.start_time
            end = (periods[-1] + 1).start_time
            total = (end - starts[0]) / pd.Timedelta(days=1)
            self.axis0, self.axis_days = starts[0], total
            self.fracs = np.r_[((starts - starts[0]) / pd.Timedelta(days=1)).to_numpy(float), total] / total
            years = list(range(starts[0].year, end.year + (1 if end > pd.Timestamp(end.year, 1, 1) else 0)))
            yb = [max(pd.Timestamp(y, 1, 1), starts[0]) for y in years] + [end]
            self.year_fracs = (years, [((t - starts[0]) / pd.Timedelta(days=1)) / total for t in yb])
            self.periods, self.freq = periods, freq
            # first/last periods only partly covered by the data (e.g. a quarter holding only its first few days)
            self.data_span = (A.date.min(), A.date.max())
            self.partial = np.asarray((periods.start_time < A.date.min()) |
                                      ((periods + 1).start_time - pd.Timedelta(days=1) > A.date.max()))
            groups = [(m, T[T.model == m]) for m in self._model_order(T)]
            xgroups = [(k, X[X.model == k]) for x in self.extras for k in x["keys"]]
            if self.ck_all.isChecked() and not include_x and len(groups) > 1:
                groups.append((COMBINED, T))       # all-models row = main file only, placed above the extra rows
            groups += xgroups
            if self.ck_all.isChecked() and include_x and len(groups) > 1:
                groups.append((COMBINED, A))
            for key, df in groups:
                self.rows.append(self._make_row(key, df, periods, freq, smooth))
            if self.scale_mode == "shared":
                lim = nice_limit(np.concatenate([r.values for r in self.rows]))
                for r in self.rows:
                    r.limit = lim
                self.legend_limit = lim
            else:
                self.legend_limit = None
        else:
            self.fracs, self.periods = None, None
        unit_label, pl = METRICS[self.cur_metric][0], PERIODS[freq]
        self.heat_title = (f"{unit_label} by {pl[0].lower()}" +
                           (f", trailing {smooth} {pl[1]}" if smooth > 1 else "") + "  ·  after costs")
        self.cum_title = "Cumulative $" if self.cum_unit == "usd" else "Cumulative bp"
        self._fill_table()
        self.legend.update()
        n_inc = int((T.skip_rule != "").sum()) if len(T) else 0
        src = os.path.basename(self.args.trades)
        extra_txt = ""
        if self.extras:
            nf = len(self.extras)
            extra_txt = (f"  + {nf} extra file{'s' if nf != 1 else ''} ({len(X):,} trades, "
                         f"{'in' if include_x else 'not in'} the all-models row).")
        status = (
            f"{src}: {len(T):,} trades" + (f" (incl. {n_inc} removed by skip rules)" if n_inc else "") +
            (f", {T.date.min():%Y-%m-%d} to {T.date.max():%Y-%m-%d}" if len(T) else "") + "." + extra_txt +
            "  After costs: 1 tick each way + $1.00 per round trip, 1 micro per trade.  "
            "1 bp = 0.01% of the entry price.")
        self.status.setText(status)
        self.status.setToolTip(status)          # the full line, when a narrow window cuts it off
        if self.detail_key is not None:
            key, per = self.detail_key
            row = next((r for r in self.rows if r.key == key), None)
            if row is not None and self.periods is not None and per.freqstr == self.periods.freqstr and per in self.periods:
                self.show_detail(key, self.periods.get_loc(per))
            else:
                self._clear_detail()

    @staticmethod
    def _model_order(T):
        known = [m for m in MODEL_INFO if m in set(T.model)]
        return known + sorted(set(T.model) - set(known))

    def _make_row(self, key, df, periods, freq, smooth):
        label_html = tip = ""
        if key == COMBINED:
            name, rule = "All models", "Every trade of the models above, one micro each"
            if self.extras:
                rule = ("Every trade of all the rows above, extra files included, one micro each"
                        if self.ck_extra.isChecked() else
                        "Every trade of the models above, one micro each; extra files not included")
        elif key in self.xinfo:
            name, rule, tip, label_html = self.xinfo[key]
        else:
            name, rule = MODEL_INFO.get(key, (key, ""))
        agg = bin_table(df, periods, freq)
        nz = np.flatnonzero(agg.n.to_numpy() > 0)
        active = np.zeros(len(periods), bool)
        if len(nz):
            active[nz[0]:nz[-1] + 1] = True
        vals = metric_values(agg, self.cur_metric, smooth, active)
        note = ""
        if active.any() and not np.isfinite(vals).any():
            note = {"avg_R": "no R: this model has no stop", "usd": "no $ column for this model"}.get(
                self.cur_metric, "no data")
        cum = cumulative(df, self.axis0, self.axis_days) if len(df) else None
        return Row(key, name, rule, df, agg, active, vals, nice_limit(vals), note, summary(df), cum,
                   label_html.replace("{muted}", self.muted.name()), tip, key in self.xinfo)

    def _fill_table(self):
        t = self.table
        t.setRowCount(0)
        t.setRowCount(len(self.rows))
        unit = METRICS[self.cur_metric][1]
        for k, r in enumerate(self.rows):
            s = r.stats
            lab = QtWidgets.QLabel(r.label_html or (
                f"<b>{html.escape(r.name)}</b>" +
                (f"<br><span style='color:{self.muted.name()}'>{html.escape(r.rule)}</span>" if r.rule else "")))
            lab.setWordWrap(True)
            lab.setTextFormat(Qt.RichText)
            lab.setContentsMargins(6, 2, 4, 2)
            lab.setToolTip(r.label_tip or html.escape(f"{r.name}: {r.rule}" if r.rule else r.name))
            t.setCellWidget(k, COL_MODEL, lab)
            cells = [f"{s['n']:,}", f"{s['per_year']:.0f}", f"{s['win']:.0%}", fmt(s["avg_bp"], "bp").replace(" bp", ""),
                     "–" if not np.isfinite(s["t"]) else f"{s['t']:+.1f}",
                     "–" if not np.isfinite(s["avg_R"]) else f"{s['avg_R']:+.2f}",
                     fmt(s["net"], "$"), "–" if not np.isfinite(s["dd"]) else f"${s['dd']:,.0f}", s["yrs"],
                     "–" if r.note else fmt(r.limit, unit).lstrip("+")]
            for c, txt in enumerate(cells, start=1):
                it = QtWidgets.QTableWidgetItem(txt)
                it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if r.key == COMBINED:
                    f = it.font()
                    f.setItalic(True)
                    it.setFont(f)
                t.setItem(k, c, it)
            t.setCellWidget(k, COL_CUM, CumSpark(self, r))
            t.setCellWidget(k, COL_HEAT, HeatStrip(self, r))
        self._fit_layout()
        self.header.viewport().update()

    def _fit_layout(self):
        """Column widths follow the window (a narrower Model and Cumulative column in small windows); row heights
        fit the wrapped model text; the table shows every row without scrolling (up to a cap)."""
        t = self.table
        vw = t.viewport().width()
        model_w = 300 if vw >= 1400 else max(210, int(vw * 0.21))
        cum_w = int(min(190, max(110, vw * 0.11)))
        if t.columnWidth(COL_MODEL) != model_w:
            t.setColumnWidth(COL_MODEL, model_w)
        if t.columnWidth(COL_CUM) != cum_w:
            t.setColumnWidth(COL_CUM, cum_w)
        fm = self.fontMetrics()
        for k in range(t.rowCount()):
            lab = t.cellWidget(k, COL_MODEL)
            # the cell widget is 1 px narrower than the column when the grid is drawn
            need = lab.heightForWidth(model_w - int(t.showGrid())) + 4 if lab is not None else 0
            h = max(4 * fm.height() + 6, 62, need)
            if t.rowHeight(k) != h:
                t.setRowHeight(k, h)
        full = self.header.height() + sum(t.rowHeight(k) for k in range(t.rowCount())) + 2 * t.frameWidth() + 2
        if t.horizontalScrollBar().isVisible():
            full += t.horizontalScrollBar().height()
        # many rows: the table may grow until about 190 px are left for the trade list (the splitter can move it)
        cap = max(420, self.split.height() - self.legend.minimumHeight() - 190)
        t.setMinimumHeight(min(full, cap))
        t.setMaximumHeight(full)
        # when the rows change, the trade list takes the space under the legend (a later drag of the splitter stays)
        if self.split.isVisible() and self.split.height() > 0 and self._split_rows != t.rowCount():
            need = self.split.widget(0).minimumSizeHint().height()
            self.split.setSizes([need, max(1, self.split.height() - need - self.split.handleWidth())])
            self._split_rows = t.rowCount()

    # ------------------------------------------------------------------ hover / click
    def tooltip(self, row, i):
        unit = METRICS[self.cur_metric][1]
        kind = METRICS[self.cur_metric][2]
        smooth = int(self.cb_smooth.currentData())
        per = period_label(self.periods[i], self.freq)
        a = row.agg.iloc[i]
        v = row.values[i]
        what = {"avg_bp": "per trade", "avg_R": "per trade", "total_bp": "in the period", "usd": "in the period"}[self.cur_metric]
        head = f"<b>{html.escape(fmt(v, unit))}</b> {what}" if np.isfinite(v) else "<b>no trades</b>"
        if smooth > 1 and np.isfinite(v):
            head += f" (trailing {smooth} {PERIODS[self.freq][1]}" + (", per period" if kind == "total" else "") + ")"
        lines = [head, html.escape(f"{row.name} · {per}")]
        if self.partial is not None and self.partial[i]:
            d0, d1 = self.data_span
            lines.append(f"<i>partial period: the data runs {d0:%Y-%m-%d} to {d1:%Y-%m-%d}</i>")
        n = int(a.n)
        if n:
            alone = []
            if smooth > 1:
                lines.append("this period alone:")
            lines.append(f"{n} trade{'s' if n != 1 else ''}, {int(a.wins)} won ({a.wins / n:.0%})")
            alone.append(f"avg {fmt(a.sum_bp / n, 'bp')}, total {fmt(a.sum_bp, 'bp')}")
            if a.nR:
                alone.append(f"avg {fmt(a.sum_R / a.nR, 'R')}")
            if a.n_usd:
                alone.append(f"net {fmt(a.sum_usd, '$')}")
            lines.append(html.escape(", ".join(alone)))
            lines.append(f"<span style='color:{self.muted.name()}'>click to list the trades</span>")
        elif smooth <= 1:
            lines.append("no trades in this period")
        return "<br>".join(lines)

    def cum_tooltip(self, row, k):
        c, u = row.cum, self.cum_unit
        unit = "$" if u == "usd" else "bp"
        d = c["dates"][k - 1]
        day = c["day_usd" if u == "usd" else "day_bp"][k - 1]
        n = int(c["day_n"][k - 1])
        lines = [f"<b>{html.escape(fmt(float(c[u][k]), unit))}</b> cumulative to {d:%Y-%m-%d %a}",
                 html.escape(row.name),
                 html.escape(f"that day: {fmt(day, unit)} from {n} trade{'s' if n != 1 else ''}")]
        if u == "usd":
            lines.append(f"<span style='color:{self.muted.name()}'>net $ at one micro per trade, after costs</span>")
            if c["usd_partial"]:
                lines.append("<i>some rows in this total have no $ column and are left out of it</i>")
        else:
            lines.append(f"<span style='color:{self.muted.name()}'>sum of net bp per trade, after costs</span>")
        return "<br>".join(lines)

    def _clear_detail(self):
        self.detail_key = None
        self.detail.setRowCount(0)
        self.detail_label.setText("Click a heatmap cell to list that period's trades here.")

    def show_detail(self, key, i):
        row = next((r for r in self.rows if r.key == key), None)
        if row is None:
            return
        per = self.periods[i]
        self.detail_key = (key, per)
        d = row.df[row.df.date.dt.to_period(self.freq) == per]
        a = row.agg.iloc[i]
        n = len(d)
        txt = f"{row.name} · {period_label(per, self.freq)}: {n} trade{'s' if n != 1 else ''}"
        if n:
            txt += (f", avg {fmt(d.bp.mean(), 'bp')}, total {fmt(d.bp.sum(), 'bp')}, {int(a.wins)} won" +
                    (f", net {fmt(d.usd.sum(), '$')}" if d.usd.notna().any() else ""))
        self.detail_label.setText(txt)
        self.detail.setRowCount(n)
        for k, tr in enumerate(d.itertuples(index=False)):
            name = self.xinfo[tr.model][0] if tr.model in self.xinfo else MODEL_INFO.get(tr.model, (tr.model,))[0]
            vals = [name, f"{tr.date:%Y-%m-%d %a}", tr.side, tr.exit, f"{tr.bp:+.1f}",
                    "" if not np.isfinite(tr.R) else f"{tr.R:+.2f}", fmt(tr.usd, "$") if np.isfinite(tr.usd) else "",
                    tr.skip_rule]
            for c, v in enumerate(vals):
                it = QtWidgets.QTableWidgetItem(str(v))
                if c in (4, 5, 6):
                    it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.detail.setItem(k, c, it)

    def save_image(self):
        on_studies = self.tabs.currentWidget() is self.studies
        on_sandbox = self.tabs.currentWidget() is getattr(self, "sandbox", None)
        name = "model_heatmap.png"
        if on_studies and self.studies._cur_key:
            name = f"study_{self.studies._cur_key[0]}_{self.studies._cur_key[1]}.png"
        elif on_sandbox and self.sandbox.sw is not None:
            name = f"eval_sandbox_{self.sandbox.sw['key']}.png"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save image", os.path.join(HERE, name),
                                                        "PNG image (*.png)")
        if path:
            (self.studies if on_studies else self.sandbox if on_sandbox else self.heat_page).grab().save(path)


def apply_theme(app, theme):
    if theme == "auto":
        return
    app.setStyle("Fusion")
    if hasattr(app.styleHints(), "setColorScheme"):
        app.styleHints().setColorScheme(Qt.ColorScheme.Dark if theme == "dark" else Qt.ColorScheme.Light)
    pal = QtGui.QPalette()
    if theme == "dark":
        for role, c in ((QtGui.QPalette.Window, "#1f1f1e"), (QtGui.QPalette.WindowText, "#f0efec"),
                        (QtGui.QPalette.Base, "#1a1a19"), (QtGui.QPalette.AlternateBase, "#242423"),
                        (QtGui.QPalette.Text, "#f0efec"), (QtGui.QPalette.Button, "#2c2c2a"),
                        (QtGui.QPalette.ButtonText, "#f0efec"), (QtGui.QPalette.ToolTipBase, "#2c2c2a"),
                        (QtGui.QPalette.ToolTipText, "#f0efec"), (QtGui.QPalette.Highlight, "#3987e5"),
                        (QtGui.QPalette.HighlightedText, "#ffffff")):
            pal.setColor(role, QtGui.QColor(c))
    else:
        for role, c in ((QtGui.QPalette.Window, "#f9f9f7"), (QtGui.QPalette.WindowText, "#0b0b0b"),
                        (QtGui.QPalette.Base, "#fcfcfb"), (QtGui.QPalette.Text, "#0b0b0b"),
                        (QtGui.QPalette.Button, "#f0efec"), (QtGui.QPalette.ButtonText, "#0b0b0b")):
            pal.setColor(role, QtGui.QColor(c))
    app.setPalette(pal)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--trades", default=os.path.join(HERE, "chosen_models_trades.csv"))
    ap.add_argument("--skipped", default=os.path.join(HERE, "chosen_models_skipped.csv"))
    ap.add_argument("--extra", action="append", default=[], metavar="FILE",
                    help="another per-trade CSV to show as extra rows (repeat for several files)")
    ap.add_argument("--include-extra", action="store_true", help="add the extra files' trades to the all-models row")
    ap.add_argument("--metric", default="avg_bp", choices=list(METRICS))
    ap.add_argument("--period", default="Q", choices=list(PERIODS))
    ap.add_argument("--smooth", default=0, type=int, choices=SMOOTH)
    ap.add_argument("--scale", default="row", choices=["row", "shared"])
    ap.add_argument("--colors", default="greenred", choices=list(RAMPS))
    ap.add_argument("--cum", default="usd", choices=list(CUM_UNITS), help="cumulative column in net $ or bp")
    ap.add_argument("--theme", default="auto", choices=["auto", "light", "dark"])
    ap.add_argument("--size", default="1680x860", help="window size, WIDTHxHEIGHT")
    ap.add_argument("--screenshot", help="render the window to this PNG and exit (for checking the layout)")
    ap.add_argument("--click", help="with --screenshot: MODEL:INDEX of a heatmap cell to open in the trade list")
    ap.add_argument("--tab", default="heatmap", choices=["heatmap", "studies", "sandbox"], help="tab shown at start")
    ap.add_argument("--model", help="Studies tab: model to show (overnight_break, opening_range, expiry_fade, all)")
    ap.add_argument("--study", help="Studies tab: study to show, by title (e.g. 'Stop size') or id (S1)")
    ap.add_argument("--studies", default=os.path.join(HERE, "data", "analysis", "studies.csv"),
                    help="studies file for the Studies tab (written by analysis_studies.py)")
    ap.add_argument("--preset", help="Eval sandbox: preset to load ('Current live models', 'Eval plan: ONB 9:xx "
                                     "entries, cap 0.15%%', 'ONB + expiry fade')")
    ap.add_argument("--sweep", help="Eval sandbox: setting on the chart's x axis, e.g. onb_cap_pct, onb_exit, "
                                    "onb_stop_mult, onb_latest_entry, target, max_loss, consistency, dll")
    args = ap.parse_args()
    # silence harmless Wayland input-method focus messages
    os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.wayland.textinput=false")
    app = QtWidgets.QApplication(sys.argv[:1])
    apply_theme(app, args.theme)
    win = MainWindow(args)
    win.show()
    if win.load_errors and not args.screenshot:
        QtCore.QTimer.singleShot(0, lambda: QtWidgets.QMessageBox.critical(
            win, "Could not add trades file", "\n\n".join(win.load_errors)))
    if args.screenshot:
        def shoot():
            if args.click:
                key, idx = args.click.rsplit(":", 1)
                win.show_detail(key, int(idx))
            if args.tab == "studies":
                win.studies.draw()
                app.processEvents()
                if win.studies.canvas is not None:
                    win.studies.canvas.draw()
            if args.tab == "sandbox":                # wait for the background computation, then draw
                t_end = time.time() + 120
                while not win.sandbox.idle() and time.time() < t_end:
                    app.processEvents()
                    time.sleep(0.02)
                win.sandbox.draw()
                app.processEvents()
                if win.sandbox.canvas is not None:
                    win.sandbox.canvas.draw()
            app.processEvents()
            win.grab().save(args.screenshot)
            app.quit()
        QtCore.QTimer.singleShot(500, shoot)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
