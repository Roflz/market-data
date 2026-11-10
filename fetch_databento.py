"""
Real CME futures data from Databento (dataset GLBX.MDP3), nearly 24 hours a day.

  cost      : ask Databento what each download would cost (free; downloads nothing)
  ohlcv     : 1-minute bars, continuous front contract by volume (ES.v.0 etc), 2010 -> now
  trades    : every trade with aggressor side (order flow) for a date range, summarized to 1-minute
              buy volume / sell volume / delta / trade counts

Key: env DATABENTO_API_KEY or ~/.databento_key (line DATABENTO_API_KEY=...). Never printed.

Usage:
  PYTHONPATH=./pylib python3 fetch_databento.py cost
  PYTHONPATH=./pylib python3 fetch_databento.py ohlcv ES,NQ
  PYTHONPATH=./pylib python3 fetch_databento.py trades ES 2025-11-01 2026-11-07
"""
import os
import sys

import pandas as pd

DATASET = "GLBX.MDP3"
START = "2010-06-07"
END = (pd.Timestamp.now(tz="UTC").normalize() - pd.Timedelta(days=1)).strftime("%Y-%m-%d")   # data runs to ~yesterday


def client():
    import databento as db
    key = os.environ.get("DATABENTO_API_KEY")
    path = os.path.expanduser("~/.databento_key")
    if not key and os.path.exists(path):
        for line in open(path):
            if line.startswith("DATABENTO_API_KEY="):
                key = line.strip().split("=", 1)[1]
    if not key:
        sys.exit("No Databento key. Set DATABENTO_API_KEY or create ~/.databento_key.")
    return db.Historical(key)


def cost():
    c = client()
    jobs = [
        ("ohlcv-1m", ["ES.v.0"], START, END, "ES 1-min bars, 2010-now"),
        ("ohlcv-1m", ["NQ.v.0"], START, END, "NQ 1-min bars, 2010-now"),
        ("ohlcv-1m", ["RTY.v.0"], "2017-07-10", END, "RTY 1-min bars, 2017-now"),
        ("ohlcv-1m", ["YM.v.0"], START, END, "YM 1-min bars, 2010-now"),
        # correlated markets (the article's "relationships between correlated assets")
        ("ohlcv-1m", ["ZN.v.0"], START, END, "10-yr Treasury note 1-min, 2010-now"),
        ("ohlcv-1m", ["6E.v.0"], START, END, "Euro FX (dollar proxy) 1-min, 2010-now"),
        ("ohlcv-1m", ["CL.v.0"], START, END, "Crude oil 1-min, 2010-now"),
        ("ohlcv-1m", ["GC.v.0"], START, END, "Gold 1-min, 2010-now"),
        # order flow and order book
        ("tbbo", ["ES.v.0"], "2025-11-01", END, "ES trades + best bid/ask, last 12 months"),
        ("trades", ["ES.v.0"], "2025-11-01", END, "ES every trade, last 12 months"),
        ("trades", ["ES.v.0"], "2023-11-01", END, "ES every trade, last 3 years"),
        ("trades", ["NQ.v.0"], "2025-11-01", END, "NQ every trade, last 12 months"),
    ]
    print(f"{'download':40s} {'est. cost':>10s} {'est. size':>10s}")
    for schema, syms, s, e, label in jobs:
        kw = dict(dataset=DATASET, symbols=syms, stype_in="continuous", schema=schema, start=s, end=e)
        usd = c.metadata.get_cost(**kw)
        size = c.metadata.get_billable_size(**kw)
        print(f"{label:40s} ${usd:9.2f} {size / 1e9:8.2f} GB", flush=True)


def ohlcv(syms):
    """Full re-download from 2010 (about $20 per symbol). For routine refreshes use refresh_data.py instead."""
    c = client()
    total = sum(c.metadata.get_cost(dataset=DATASET, symbols=[f"{s}.v.0"], stype_in="continuous", schema="ohlcv-1m",
                                    start="2017-07-10" if s == "RTY" else START, end=END) for s in syms)
    if "--yes-full-download" not in sys.argv:
        sys.exit(f"This re-downloads the FULL history for {','.join(syms)} and costs ${total:.2f} of Databento credit.\n"
                 f"For a routine refresh use:  PYTHONPATH=./pylib python3 refresh_data.py   (new bars only, cents)\n"
                 f"To really re-download everything, add --yes-full-download.")
    for sym in syms:
        start = "2017-07-10" if sym == "RTY" else START
        data = c.timeseries.get_range(dataset=DATASET, symbols=[f"{sym}.v.0"], stype_in="continuous",
                                      schema="ohlcv-1m", start=start, end=END)
        df = data.to_df()
        df.index = df.index.tz_convert("America/New_York")
        df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
        df = df[["Open", "High", "Low", "Close", "Volume", "instrument_id"]]
        out = f"data/{sym}_fut_1m.csv"
        df.to_csv(out)
        print(f"{out}: {len(df):,} bars, {df.index.min()} -> {df.index.max()}, "
              f"{df.instrument_id.nunique()} contracts", flush=True)


def trades(sym, start, end):
    c = client()
    days = pd.date_range(start, end, freq="MS").tolist() + [pd.Timestamp(end)]
    parts = []
    for a, b in zip(days[:-1], days[1:]):
        data = c.timeseries.get_range(dataset=DATASET, symbols=[f"{sym}.v.0"], stype_in="continuous",
                                      schema="trades", start=a.strftime("%Y-%m-%d"), end=b.strftime("%Y-%m-%d"))
        t = data.to_df()
        if t.empty:
            continue
        t.index = t.index.tz_convert("America/New_York")
        buy = t["size"].where(t.side == "B", 0)          # buyer was the aggressor (lifted the offer)
        sell = t["size"].where(t.side == "A", 0)         # seller was the aggressor (hit the bid)
        big = t["size"] >= t["size"].quantile(0.99)
        m = pd.DataFrame({"buy_vol": buy, "sell_vol": sell, "n_trades": 1,
                          "big_buy": buy.where(big, 0), "big_sell": sell.where(big, 0)}).resample("1min").sum()
        m = m[m.n_trades > 0]
        parts.append(m)
        print(f"  {sym} trades {a.date()} -> {b.date()}: {len(t):,} trades", flush=True)
    out = pd.concat(parts)
    out["delta"] = out.buy_vol - out.sell_vol
    path = f"data/{sym}_flow_1m.csv"
    out.to_csv(path)
    print(f"{path}: {len(out):,} minutes of order flow", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "cost"
    if cmd == "cost":
        cost()
    elif cmd == "ohlcv":
        ohlcv(sys.argv[2].split(",") if len(sys.argv) > 2 else ["ES", "NQ"])
    elif cmd == "trades":
        trades(sys.argv[2], sys.argv[3], sys.argv[4])
