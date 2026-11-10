"""
Bring all data up to date cheaply, then rebuild everything the live models and the paper log need.

  1. Databento (paid credit, but only the NEW bars): appends 1-minute ES and NQ bars, and hourly bars for the
     cross-market symbols, from the last bar already on disk to the latest data Databento has. It asks Databento
     for the price first and stops if it is above --max-cost (default $1.00). A day of ES+NQ 1-minute bars costs
     about half a cent, a month about $0.22, a year about $2.58. (Re-downloading the full 2010-now history, which
     'fetch_databento.py ohlcv' does, costs about $41 - do not do that for a refresh.)
  2. Yahoo Finance (free): appends the daily index files in data/yahoo_daily/ (S&P 500, Nasdaq-100, VIX, 10-yr
     yield, ...). The last stored day is re-downloaded and must agree with what is on disk (a check that the file
     and the ticker match); recent days are replaced with Yahoo's latest values.
  3. Rebuilds, in order: daily_sessions.py, exits_data.py, fut_build.py, market_context.py, chosen_models.py,
     then runs paper_log.py (the forward-test log).

Usage:  PYTHONPATH=./pylib python3 refresh_data.py              everything
        PYTHONPATH=./pylib python3 refresh_data.py --check      only show what would be downloaded and its price
        options: --max-cost 1.00   --skip-databento   --skip-yahoo   --skip-rebuild   --no-hourly
The Databento key is read as in fetch_databento.py (env DATABENTO_API_KEY or ~/.databento_key); never printed.
"""
import argparse
import io
import os
import subprocess
import sys
import time
import warnings

import pandas as pd

warnings.filterwarnings("ignore", message=".*inplace keyword.*")          # pandas 3 notice inside the databento library
warnings.filterwarnings("ignore", message=".*reduced quality.*")          # Databento flags the current, unfinished day

import fetch_databento as fd

MINUTE = ["ES", "NQ", "YM"]                                      # data/{SYM}_fut_1m.csv
HOURLY = ["ES", "NQ", "CL", "ZN", "ZB", "6E", "GC", "RTY", "YM"]   # data/{SYM}_fut_1h.csv
YAHOO = {                                                  # data/yahoo_daily/{file}.csv -> Yahoo ticker
    "SP500_index": "^GSPC", "NASDAQ100_index": "^NDX", "NASDAQ_composite": "^IXIC", "DOW_index": "^DJI",
    "RUSSELL2000_index": "^RUT", "VIX_index": "^VIX", "US10Y_yield": "^TNX", "dollar_index": "DX-Y.NYB",
    "crude_oil_front": "CL=F", "gold_front": "GC=F", "SPY_etf": "SPY", "QQQ_etf": "QQQ",
}
REBUILD = ["daily_sessions.py", "exits_data.py", "fut_build.py", "market_context.py", "chosen_models.py", "paper_log.py"]
COLS = ["Open", "High", "Low", "Close", "Volume", "instrument_id"]


def last_timestamp(path):
    """Timestamp of the last row of a large CSV without reading the whole file."""
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - 4096))
        last = f.read().decode().strip().splitlines()[-1]
    return pd.Timestamp(last.split(",")[0]).tz_convert("UTC")


def databento_jobs(hourly):
    jobs = [(s, "ohlcv-1m", f"data/{s}_fut_1m.csv") for s in MINUTE]
    if hourly:
        jobs += [(s, "ohlcv-1h", f"data/{s}_fut_1h.csv") for s in HOURLY if os.path.exists(f"data/{s}_fut_1h.csv")]
    return jobs


def databento(args):
    c = fd.client()
    avail_end = pd.Timestamp(c.metadata.get_dataset_range(dataset=fd.DATASET)["end"]).tz_convert("UTC")
    plan, total = [], 0.0
    for sym, schema, path in databento_jobs(not args.no_hourly):
        step = pd.Timedelta(minutes=1) if schema == "ohlcv-1m" else pd.Timedelta(hours=1)
        start = last_timestamp(path) + step
        if start >= avail_end:
            print(f"  {path}: already up to date ({start - step:%Y-%m-%d %H:%M} UTC)")
            continue
        kw = dict(dataset=fd.DATASET, symbols=[f"{sym}.v.0"], stype_in="continuous", schema=schema,
                  start=start.isoformat(), end=avail_end.isoformat())
        usd = c.metadata.get_cost(**kw)
        total += usd
        plan.append((path, kw, usd))
        print(f"  {path}: {start:%Y-%m-%d %H:%M} -> {avail_end:%Y-%m-%d %H:%M} UTC, price ${usd:.4f}")
    print(f"  Databento total: ${total:.4f} (limit ${args.max_cost:.2f})")
    if args.check or not plan:
        return
    if total > args.max_cost:
        sys.exit(f"Stopped: ${total:.2f} is above --max-cost ${args.max_cost:.2f}. Nothing was downloaded.")
    for path, kw, _ in plan:
        df = c.timeseries.get_range(**kw).to_df()
        if df.empty:
            print(f"  {path}: no new bars")
            continue
        df.index = df.index.tz_convert("America/New_York")
        df.index.name = "ts_event"
        df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})[COLS]
        df = df[df.index.tz_convert("UTC") > last_timestamp(path)]          # never duplicate a bar
        buf = io.StringIO()
        df.to_csv(buf, header=False)
        with open(path, "a") as f:
            f.write(buf.getvalue())
        print(f"  {path}: +{len(df):,} bars, now to {df.index.max()}")


def yahoo(args):
    import yfinance as yf
    for name, ticker in YAHOO.items():
        path = f"data/yahoo_daily/{name}.csv"
        if not os.path.exists(path):
            continue
        old = pd.read_csv(path, parse_dates=["Date"])
        last = old.Date.max()
        if args.check:
            print(f"  {path}: last day {last:%Y-%m-%d} ({ticker}, free)")
            continue
        new = yf.download(ticker, start=(last - pd.Timedelta(days=10)).strftime("%Y-%m-%d"), progress=False,
                          auto_adjust=False, multi_level_index=False)
        if new is None or new.empty:
            print(f"  {path}: Yahoo returned nothing for {ticker}; left unchanged")
            continue
        new.index = pd.to_datetime(new.index).tz_localize(None).normalize()
        new = new.reset_index().rename(columns={"index": "Date", "Datetime": "Date"})[old.columns]
        # keep only finished weekdays: Yahoo shows a row for today (and for Sunday on futures) before the day is over
        today = pd.Timestamp.now(tz="America/New_York").tz_localize(None).normalize()
        new = new[(new.Date < today) & (new.Date.dt.day_of_week < 5)]
        if new.empty:
            print(f"  {path}: nothing new")
            continue
        same = new[new.Date == last]
        if len(same):
            a, b = float(old.loc[old.Date == last, "Close"].iloc[-1]), float(same.Close.iloc[0])
            if abs(a / b - 1) > 0.02:
                print(f"  {path}: SKIPPED - Yahoo's {ticker} close on {last:%Y-%m-%d} is {b:.2f} vs {a:.2f} on disk")
                continue
        merged = pd.concat([old[old.Date < new.Date.min()], new]).drop_duplicates("Date", keep="last").sort_values("Date")
        merged.to_csv(path, index=False, date_format="%Y-%m-%d")
        print(f"  {path}: now to {merged.Date.max():%Y-%m-%d} (+{len(merged) - len(old)} days)")


def rebuild():
    env = dict(os.environ, PYTHONPATH="./pylib")
    for script in REBUILD:
        t0 = time.time()
        print(f"\n== {script}", flush=True)
        r = subprocess.run([sys.executable, script], env=env)
        if r.returncode:
            sys.exit(f"{script} failed (exit {r.returncode}); stopping. Fix it and run refresh_data.py --skip-databento --skip-yahoo")
        print(f"   ({time.time() - t0:.0f}s)")


def main():
    ap = argparse.ArgumentParser(description="Cheap incremental data refresh + rebuild")
    ap.add_argument("--check", action="store_true", help="show what would be downloaded and its price; change nothing")
    ap.add_argument("--max-cost", type=float, default=1.00, help="stop if the Databento price is above this ($)")
    ap.add_argument("--skip-databento", action="store_true")
    ap.add_argument("--skip-yahoo", action="store_true")
    ap.add_argument("--skip-rebuild", action="store_true")
    ap.add_argument("--no-hourly", action="store_true", help="only the ES/NQ 1-minute bars from Databento")
    args = ap.parse_args()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not args.skip_databento:
        print("Databento (only new bars):")
        databento(args)
    if not args.skip_yahoo:
        print("Yahoo daily files (free):")
        yahoo(args)
    if not (args.check or args.skip_rebuild):
        rebuild()


if __name__ == "__main__":
    main()
