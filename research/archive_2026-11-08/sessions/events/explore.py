import numpy as np, pandas as pd
OUT = "/tmp/claude-1000/-home-roflz--claude-spares-spare-NhXWo6/fb7c622e-dc01-4189-9bb7-9001db03cb79/scratchpad/sessions/events"
for sym in ("NQ","ES"):
    d = pd.read_parquet(f"{OUT}/{sym}_1m.parquet")
    et = pd.to_datetime(d.m * 60, unit="s", utc=True).dt.tz_convert("America/New_York")
    d["yr"] = et.dt.year.values; d["tod"] = (et.dt.hour*60 + et.dt.minute).values; d["dow"] = et.dt.dayofweek.values
    wk = d[d.dow.isin([1,2,3])]
    ndays = wk.groupby("yr").apply(lambda g: g.assign(dt=0).shape[0])
    days = pd.Series(et.dt.date.values)[d.dow.isin([1,2,3]).values].groupby(d.yr[d.dow.isin([1,2,3])].values).nunique()
    cov = wk.groupby(["yr", wk.tod//30]).size().unstack().div(days, axis=0) / 30
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
    print(sym, "coverage fraction of minutes with a bar, Tue-Thu, by 30-min ET slot (col = slot*30 min)")
    print(cov.round(2).iloc[:, :].to_string())
