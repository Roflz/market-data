"""
How each chosen model does in different market states and around events (diagnostics, not rules).
Inputs: chosen_models_trades.csv (chosen_models.py), data/market_context.pkl (market_context.py), calendar_days.py.
Every condition is known before the trade's 9:30 open (see market_context.py), except the crisis episodes and the
labeled geopolitical events, which are defined with hindsight and are only for describing what happened.
For each model and condition: trades, average net $ and R per trade, total $, and a Welch t-test of "in the condition"
vs "not in it" on net $ per trade (|t| > 2 suggests the condition matters; many conditions are tested, so expect a few
|t| > 2 by chance).
Output: regime_report.txt
Usage:  PYTHONPATH=./pylib python3 regime_report.py
"""
import numpy as np
import pandas as pd

import calendar_days as cd

OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def welch_t(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 5 or len(b) < 5:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def crisis_episodes(ctx, threshold=-15.0, merge_days=40):
    """Periods when the S&P 500 closed at least 15% below its 52-week high (data-defined, hindsight)."""
    off = ctx.spx_off_52w_high_prev.shift(-1).loc["2010-06-01":]            # the day's own close vs its 52-week high
    hit = off[off <= threshold].index
    eps, start, last = [], None, None
    for d in hit:
        if start is None:
            start = last = d
        elif (d - last).days > merge_days:
            eps.append((start, last)); start = last = d
        else:
            last = d
    if start is not None:
        eps.append((start, last))
    return eps


def main():
    T = pd.read_csv("chosen_models_trades.csv", parse_dates=["date"])
    ctx = pd.read_pickle("data/market_context.pkl")
    T = T.join(ctx, on="date")
    fomc, cpi = cd.fomc_days(), cd.cpi_days()
    T["fomc_day"] = T.date.isin(fomc)
    T["cpi_day"] = T.date.isin(cpi)
    missing_ctx = T.vix_prev.isna() & ~T.date.isin(ctx.index)
    syms = ctx.attrs.get("cross_shock_syms") or [s for s in ("CL", "ZN", "6E", "GC") if f"on_{s}_z" in ctx]
    nan = pd.Series(np.nan, index=T.index)
    conds = {
        "VIX in the top third of its history": T.vix_tercile == 3,
        "VIX in the bottom third": T.vix_tercile == 1,
        "VIX rose 10%+ the prior day": T.vix_chg_prev / (T.vix_prev - T.vix_chg_prev) >= 0.10,
        "S&P below its 200-day average": T.trend_up == 0,
        "S&P 10%+ below its 52-week high": T.in_correction_10 == 1,
        "S&P fell 2%+ the prior day": T.spx_ret_1d_prev <= -2,
        "Policy uncertainty top 10% (5-yr window)": T.epu_top10 == 1,
        "Geopolitical risk top 10% (5-yr window)": T.gpr_top10 == 1,
        "Geopolitical risk spike (2x its 30-day avg) in last 3 days": T.gpr_spike_last3 == 1,
        f"Cross-market shock overnight ({'/'.join(syms)} 3+ sd)": T.get("cross_shock_3sd", nan) == 1,
        "Oil moved 2+ sd overnight": T.get("on_CL_z", nan).abs() >= 2,
        "Gold moved 2+ sd overnight": T.get("on_GC_z", nan).abs() >= 2,
        "Euro moved 2+ sd overnight": T.get("on_6E_z", nan).abs() >= 2,
        "10-yr note moved 2+ sd overnight": T.get("on_ZN_z", nan).abs() >= 2,
        "10-yr yield moved 10+ bp the prior day": T.us10y_chg_bp_prev.abs() >= 10,
        "Fed statement day": T.fomc_day,
        "CPI release day": T.cpi_day,
    }
    say("REGIME AND EVENT REPORT: chosen models (MNQ, 1 micro, after costs; expiry-Friday rule applied)")
    say(f"t = Welch t of net $/trade inside vs outside the condition. {len(conds)} conditions x 3 models are tested, so")
    say("a few |t| > 2 results are expected by chance alone. Conditions with no data for a model are listed as such.")
    say(f"Trades without a market-context row (not stock-market trading days): {int(missing_ctx.sum())}\n")
    rows = []
    for m, g in T.groupby("model", sort=False):
        say(f"######## {m}: {len(g)} trades, avg ${g.usd.mean():+.2f}/trade" +
            (f", {g.R.mean():+.3f} R/trade" if g.R.notna().any() else f", {g.bp.mean():+.2f} bp/trade"))
        say(f"{'condition':58s} {'trades':>6s} {'share':>6s} {'$/trade':>8s} {'R/trade':>8s} {'total $':>9s} {'t vs rest':>9s}")
        for name, mask in conds.items():
            mask = mask.reindex(g.index).fillna(False).astype(bool)
            known = g.index  # all trades; rows with unknown condition count as "not in it"
            a, b = g[mask], g[~mask]
            if len(a) == 0:
                say(f"{name:58s}   no trades / no data")
                continue
            t = welch_t(a.usd, b.usd)
            rows.append(dict(model=m, condition=name, trades=len(a), usd_per_trade=a.usd.mean(), R_per_trade=a.R.mean(),
                             total_usd=a.usd.sum(), t_vs_rest=t))
            flag = "  <--" if abs(t) >= 2 else ""
            say(f"{name:58s} {len(a):6d} {len(a) / len(g):6.1%} {a.usd.mean():+8.2f} "
                f"{a.R.mean() if a.R.notna().any() else np.nan:+8.3f} {a.usd.sum():+9,.0f} {t:+9.2f}{flag}")
        say()
    pd.DataFrame(rows).to_csv("regime_report.csv", index=False)

    say("######## Crisis periods (S&P 500 closing 15%+ below its 52-week high; defined with hindsight), net $ at 1 micro")
    say("(window = first to last such close, with gaps under 40 days merged; n/a = model not trading yet)")
    eps = crisis_episodes(ctx)
    models = list(T.model.unique())
    span = T.groupby("model").date.agg(["min", "max"])
    say(f"{'period':25s} " + " ".join(f"{m:>16s}" for m in models) + f" {'running models':>15s}")
    for s, e in eps:
        w = T[(T.date >= s) & (T.date <= e)]
        cells, tot = [], 0.0
        for m in models:
            if s < span.loc[m, "min"] or e > span.loc[m, "max"]:
                cells.append(f"{'n/a':>16s}")
            else:
                v = w[w.model == m].usd.sum(); tot += v; cells.append(f"{v:+16,.0f}")
        say(f"{s:%Y-%m-%d} -> {e:%Y-%m-%d}    " + " ".join(cells) + f" {tot:+15,.0f}")
    say("\n######## Labeled geopolitical events (Caldara-Iacoviello labels; hindsight), net $ in the 5 trading days from the event")
    lab = ctx.gpr_event_label_sameday_HINDSIGHT.dropna().loc["2010-06-01":]
    days = ctx.index
    for d, label in lab.items():
        i = days.searchsorted(d)
        w = T[(T.date >= days[i]) & (T.date <= days[min(i + 4, len(days) - 1)])]
        say(f"{d:%Y-%m-%d} {label[:50]:50s} " + ", ".join(f"{m} {w[w.model == m].usd.sum():+,.0f}" for m in T.model.unique()))
    open("regime_report.txt", "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
