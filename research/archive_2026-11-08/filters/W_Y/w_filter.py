"""
Builder Y, Filter W: skip wide-stop overnight-break trades (SPEC.md section W, pre-registered; no tuning).

  width(trade) = stop distance in points (R_pts = 2 x ATR(5-min) at the signal bar, from exits_engine.run "hold" k0=2)
                 / raw price (signal-bar close minus the session's back-adjustment, as chosen_models uses for bp)
  For each trade (explicit loop over trade days):
    history = trading days (cash days) of the model's data strictly before the trade date
    if fewer than 250 -> keep (warm-up)
    window  = the previous 250 trading days (strictly before the trade date)
    thr     = 67th percentile (numpy default, linear interpolation) of the widths of ALL live overnight-break trades
              dated inside the window
    remove if width > thr, else keep
Then the pass rule (a)(b)(c) and the report-only items.
Inputs: base_overnight_break.pkl, calendar.pkl (w_build_base.py), chosen_models_trades.csv (other two models).
Outputs: W_trades.csv, W_summary.json
"""
import json
import os

import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
LOOKBACK = 250
PCTL = 67
T_MIN = 2.0
ERAS = [("2010-13", 2010, 2013), ("2014-17", 2014, 2017), ("2018-20", 2018, 2020), ("2021-23", 2021, 2023),
        ("2024-26", 2024, 2026)]


# ----------------------------------------------------------------------------------------------- the filter
def decide(base, cal):
    cash_days = pd.DatetimeIndex(cal["cash_days"])
    model_days = cash_days[(cash_days >= cal["model_first_sess"]) & (cash_days <= cal["model_last_sess"])]
    base = base.copy()
    base["width"] = base.R_pts / base.raw_ref_price
    rows = []
    for day in sorted(base.date.unique()):
        day = pd.Timestamp(day)
        todays = base[base.date == day]
        pos = model_days.get_loc(day)                       # number of model trading days strictly before `day`
        if pos < LOOKBACK:
            thr, n_win, w_start, w_end = np.nan, 0, pd.NaT, pd.NaT
        else:
            w_start, w_end = model_days[pos - LOOKBACK], model_days[pos - 1]
            window = base[(base.date >= w_start) & (base.date <= w_end)]
            assert (window.date < day).all()                # only earlier days' trades
            n_win = len(window)
            thr = np.percentile(window.width.to_numpy(), PCTL) if n_win else np.nan
        for _, tr in todays.iterrows():
            remove = bool(pos >= LOOKBACK and n_win > 0 and tr.width > thr)
            rows.append({"idx": tr.name, "hist_days": pos, "window_start": w_start, "window_end": w_end,
                         "window_trades": n_win, "p67_width": thr, "decision": "remove" if remove else "keep"})
    dec = pd.DataFrame(rows).set_index("idx").sort_index()
    return base.join(dec)


# ----------------------------------------------------------------------------------------------- evaluation
def welch_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def daily_stats(trades):
    d = trades.groupby("date").usd.sum().sort_index()
    eq = d.cumsum()
    dd = float((eq.cummax() - eq).max())                     # chosen_models' formula
    eq0 = np.r_[0.0, eq.to_numpy()]                           # same, with the equity peak allowed at the 0 start
    dd0 = float((np.maximum.accumulate(eq0) - eq0).max())
    return {"net_usd": float(d.sum()), "max_dd": dd, "max_dd_from_zero": dd0, "worst_day": float(d.min()),
            "days": int(len(d))}


def block(t):
    return {"n": int(len(t)), "usd": float(t.usd.sum()), "usd_per_trade": float(t.usd.mean()) if len(t) else None,
            "bp_per_trade": float(t.bp.mean()) if len(t) else None}


def evaluate(T, cost_extra=0.0):
    T = T.copy()
    T["usd"] = T.usd - cost_extra
    T["bp"] = 1e4 * (T.usd / 2.0) / T.raw_ref_price
    kept, rem = T[T.decision == "keep"], T[T.decision == "remove"]
    yr = T.date.dt.year
    r_full = rem.usd.sum()
    r_a = rem[rem.date.dt.year <= 2017].usd.sum()
    r_b = rem[rem.date.dt.year >= 2018].usd.sum()
    a = bool(r_full < 0 and r_a < 0 and r_b < 0)
    t = welch_t(kept.usd, rem.usd)
    b = t >= T_MIN
    base_s, filt_s = daily_stats(T), daily_stats(kept)
    c = bool(filt_s["max_dd"] <= base_s["max_dd"] and filt_s["worst_day"] >= base_s["worst_day"])
    out = {
        "kept": block(kept), "removed": block(rem), "share_removed": len(rem) / len(T),
        "removed_usd_full": float(r_full), "removed_usd_2010_17": float(r_a), "removed_usd_2018_26": float(r_b),
        "a_removed_lose_everywhere": a, "welch_t_kept_minus_removed": t, "b_t_ge_2": bool(b),
        "unfiltered_model": base_s, "filtered_model": filt_s, "c_dd_and_worst_day_no_worse": c,
        "PASS": bool(a and b and c),
    }
    # warm-up excluded variant of (b) (report only: only trades the filter could act on)
    elig = T[T.hist_days >= LOOKBACK]
    out["welch_t_after_warmup_only"] = welch_t(elig[elig.decision == "keep"].usd, elig[elig.decision == "remove"].usd)
    per = {}
    for name, y0, y1 in ERAS + [("2023-2026", 2023, 2026)]:
        m = (yr >= y0) & (yr <= y1)
        per[name] = {"kept": block(T[m & (T.decision == "keep")]), "removed": block(T[m & (T.decision == "remove")]),
                     "share_removed": float((T[m].decision == "remove").mean()) if m.any() else None,
                     "unfiltered_usd": float(T[m].usd.sum()), "filtered_usd": float(T[m & (T.decision == "keep")].usd.sum())}
    out["by_period"] = per
    out["by_year"] = {int(y): {"n": int(len(g)), "removed_n": int((g.decision == "remove").sum()),
                               "removed_usd": float(g[g.decision == "remove"].usd.sum()),
                               "kept_usd": float(g[g.decision == "keep"].usd.sum()),
                               "unfiltered_usd": float(g.usd.sum())} for y, g in T.groupby(yr)}
    return out


def combined_book(T, cost_extra=0.0):
    allt = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    allt["usd"] = allt.usd - cost_extra
    others = allt[allt.model != "overnight_break"][["date", "usd"]]
    ob = T[["date", "usd", "decision"]].copy()
    ob["usd"] = ob.usd - cost_extra
    before = daily_stats(pd.concat([others, ob[["date", "usd"]]]))
    after = daily_stats(pd.concat([others, ob[ob.decision == "keep"][["date", "usd"]]]))
    return {"before": before, "after": after}


def main():
    base = pd.read_pickle(os.path.join(OUT, "base_overnight_break.pkl"))
    cal = pd.read_pickle(os.path.join(OUT, "calendar.pkl"))
    T = decide(base, cal)

    # sanity: the base set is chosen_models_trades.csv's overnight_break rows
    ref = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ref = ref[ref.model == "overnight_break"]
    assert len(T) == len(ref) == 1731 and abs(T.usd.sum() - ref.usd.sum()) < 1e-6
    # no look-ahead: width is known at the signal-bar close (< entry), thresholds only from earlier dates
    assert (T.signal_bar_time < T.entry_time).all()
    assert (T.window_end.isna() | (T.window_end < T.date)).all()

    T["exit_px_raw"] = T.entry_fill_raw + np.where(T.side == "long", 1, -1) * T.gross_pts
    csv = T[["date", "side", "usd", "width", "R_pts", "raw_ref_price", "atr5_signal", "p67_width", "window_start",
             "window_end", "window_trades", "hist_days", "decision", "signal_bar_time", "entry_time", "exit_time",
             "entry_fill_raw", "exit_px_raw", "exit", "gross_pts", "net_pts", "bp", "R"]].rename(
        columns={"exit": "exit_reason", "net_pts": "net_pts", "bp": "net_bp", "entry_fill_raw": "entry_raw",
                 "exit_px_raw": "exit_raw", "raw_ref_price": "raw_price_signal_close"})
    csv.to_csv(os.path.join(OUT, "W_trades.csv"), index=False)

    res = {"filter": "W skip wide-stop overnight breaks", "n_trades": len(T), "total_usd": float(T.usd.sum()),
           "first_filter_day": str(T[T.hist_days >= LOOKBACK].date.min().date()),
           "warmup_trades_kept": int((T.hist_days < LOOKBACK).sum()),
           "at_1tick": evaluate(T), "at_2ticks": evaluate(T, 1.0),
           "combined_book_1tick": combined_book(T), "combined_book_2ticks": combined_book(T, 1.0)}
    with open(os.path.join(OUT, "W_summary.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)
    r = res["at_1tick"]
    print(json.dumps({k: r[k] for k in r if k not in ("by_period", "by_year")}, indent=1, default=str))
    print("2 ticks:", {k: res["at_2ticks"][k] for k in ("PASS", "a_removed_lose_everywhere", "welch_t_kept_minus_removed",
                                                         "c_dd_and_worst_day_no_worse", "removed_usd_full")})
    print("book 1t", res["combined_book_1tick"]); print("book 2t", res["combined_book_2ticks"])
    for k, v in r["by_period"].items():
        print(k, v["kept"]["n"], round(v["kept"]["usd"]), v["removed"]["n"], round(v["removed"]["usd"]),
              round(v["share_removed"] or 0, 3))
    for y, v in r["by_year"].items():
        print(y, v)


if __name__ == "__main__":
    main()
