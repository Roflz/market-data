"""v3 internal-evidence re-cuts of EXISTING trade lists (no new backtests, no 1-min data).
Every row is cut at the locked holdout (dates < 2025-06-30). Logs each cut to out/trials.csv (module='v3-internal').
Run from research/confidence with the standard PYTHONPATH."""
import json, numpy as np, pandas as pd
R = "/run/media/roflz/Disk 2/_/market_data/"
S13 = R + "research/archive_2026-11-08/tests/s13_X/"
H = pd.Timestamp("2025-06-30")
OUT = R + "research/confidence/v3/exp_internal/recut_results.csv"

def t(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan

def stats(df, col, label, src):
    df = df.copy(); df["date"] = pd.to_datetime(df["date"]); df = df[df.date < H]
    assert df.date.max() < H  # no-look-ahead / holdout truncation check
    y = df.date.dt.year; g = df.groupby("date")[col].sum()
    keep = g.sort_values().iloc[:-10].index
    r = dict(label=label, source=src, n=len(df), usd=df[col].mean(), t_day=t(g),
             usd_1017=df[y <= 2017][col].mean(), t_1017=t(df[y <= 2017].groupby("date")[col].sum()),
             usd_18=df[y >= 2018][col].mean(), t_18=t(df[y >= 2018].groupby("date")[col].sum()),
             usd_22=df[y >= 2022][col].mean(), t_22=t(df[y >= 2022].groupby("date")[col].sum()),
             usd_no10=df[df.date.isin(keep)][col].mean(), t_no10=t(g.loc[keep]))
    return r

rows = []
nb = pd.read_csv(R + "lit_p1_noiseband_trades.csv", usecols=["date", "market", "variant", "side", "net_usd", "vol_tercile", "rand_net_usd"])
for m in ["NQ", "ES"]:
    x = nb[(nb.market == m) & (nb.variant == "A")]
    rows.append(stats(x, "net_usd", f"noiseband {m} A", "lit_p1"))
    rows.append(stats(x, "rand_net_usd", f"noiseband {m} A random-direction control", "lit_p1"))
    rows.append(stats(x[x.vol_tercile >= 2], "net_usd", f"noiseband {m} A vol tercile 2+3", "lit_p1"))
    for s in ["long", "short"]:
        rows.append(stats(x[x.side == s], "net_usd", f"noiseband {m} A {s}", "lit_p1"))
cm = pd.read_csv(R + "chosen_models_trades.csv")
for mdl in cm.model.unique():
    rows.append(stats(cm[cm.model == mdl], "usd", f"chosen {mdl} MNQ", "chosen_models"))
e = cm[cm.model == "expiry_fade"]; q = pd.to_datetime(e.date).dt.month.isin([3, 6, 9, 12])
rows.append(stats(e[q], "usd", "expiry fade MNQ quarterly", "chosen_models"))
rows.append(stats(e[~q], "usd", "expiry fade MNQ monthly non-quarter", "chosen_models"))
for mk in ["MNQ", "MES"]:
    for ev in ["NFP", "CPI", "control_nonrelease_days"]:
        rows.append(stats(pd.read_csv(S13 + f"L1_primary_time_{mk}_{ev}.csv"), "net_usd", f"8:30 fade {mk} {ev}", "s13"))
    a = pd.concat([pd.read_csv(S13 + f"L1_primary_time_{mk}_{ev}.csv") for ev in ["NFP", "CPI"]]).drop_duplicates("date")
    a["date"] = pd.to_datetime(a.date); a = a[a.date < H].sort_values("date")
    mv = a.move_830_signal.abs() / a.o845 * 1e4
    big = mv > mv.expanding().median().shift(1)          # threshold from PRIOR events only
    rows.append(stats(a, "net_usd", f"8:30 fade {mk} NFP+CPI", "s13"))
    rows.append(stats(a[big], "net_usd", f"8:30 fade {mk} NFP+CPI big move (prior-median)", "s13"))
res = pd.DataFrame(rows).round(2)
res.to_csv(OUT, index=False)
print(res.to_string())
try:
    from run_pipeline import log_trial
    for r in rows:
        log_trial(module="v3-internal", scope=r["label"], model="recut of existing trade list", target="net $/micro",
                  oos_kept=r["n"], oos_usd_per_trade=round(r["usd"], 2),
                  parameters=json.dumps({"source": r["source"], "cut": "< 2025-06-30"}),
                  note=f"t_day {r['t_day']:.2f}; 2010-17 ${r['usd_1017']:.2f} t {r['t_1017']:.2f}; 2018+ ${r['usd_18']:.2f} t {r['t_18']:.2f}; 2022+ ${r['usd_22']:.2f}; no10best ${r['usd_no10']:.2f} t {r['t_no10']:.2f}")
    print("logged", len(rows), "trials")
except Exception as ex:
    print("log_trial failed:", ex)

# --- added 12:15: do the R1 (day after S&P <= -2%) / R2 (FOMC day) skip rules, chosen on ORB/overnight-break,
# replicate on a DIFFERENT strategy (noise band A)?  Logged as 4 more trials.
