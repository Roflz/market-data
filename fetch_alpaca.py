"""
Download multi-year 5-minute SPY / QQQ bars from Alpaca's market data API (free account works)
and convert them to ES / NQ-equivalent points for the futures backtest.

Why SPY/QQQ: they track the S&P 500 / Nasdaq 100 (what ES / NQ are based on) with real,
consolidated volume. Prices are multiplied by a constant ratio so 1 "point" ~ 1 futures point;
the ratio is measured on the period where we also have real futures bars (data/ES_5m.csv etc).

Keys are read from environment variables ALPACA_KEY_ID / ALPACA_SECRET_KEY, or from the file
~/.alpaca_keys containing those two lines. They are never printed or written anywhere else.

Usage:  PYTHONPATH=./pylib python3 fetch_alpaca.py [start-date] [5Min|1Min] [ES,NQ,RTY,YM]   (default 2019-01-01 5Min ES,NQ)
        1Min bars are kept for regular trading hours only (9:30-16:00 ET) to keep files manageable.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import pandas as pd

START = sys.argv[1] if len(sys.argv) > 1 else "2019-01-01"
TIMEFRAME = sys.argv[2] if len(sys.argv) > 2 else "5Min"
LABEL = {"5Min": "5m", "1Min": "1m"}[TIMEFRAME]
ALL_PAIRS = {"ES": ("SPY", 10.0), "NQ": ("QQQ", 41.0),   # default ratios if no futures overlap is available
             "RTY": ("IWM", 10.0), "YM": ("DIA", 100.0)}
PAIRS = {k: ALL_PAIRS[k] for k in (sys.argv[3].split(",") if len(sys.argv) > 3 else ["ES", "NQ"])}
URL = "https://data.alpaca.markets/v2/stocks/bars"


def load_keys():
    keys = {k: os.environ.get(k) for k in ("ALPACA_KEY_ID", "ALPACA_SECRET_KEY")}
    path = os.path.expanduser("~/.alpaca_keys")
    if not all(keys.values()) and os.path.exists(path):
        for line in open(path):
            if "=" in line:
                k, v = line.strip().split("=", 1)
                if k in keys and not keys[k]:
                    keys[k] = v.strip().strip('"').strip("'")
    if not all(keys.values()):
        sys.exit("No Alpaca keys found. Set ALPACA_KEY_ID / ALPACA_SECRET_KEY or create ~/.alpaca_keys.")
    return keys


def get_bars(symbol, keys):
    headers = {"APCA-API-KEY-ID": keys["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": keys["ALPACA_SECRET_KEY"]}
    end = (pd.Timestamp.now(tz="UTC") - pd.Timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {"symbols": symbol, "timeframe": TIMEFRAME, "start": f"{START}T00:00:00Z", "end": end,
              "limit": 10000, "adjustment": "raw", "feed": "sip"}
    chunks, page, total = [], 0, 0
    while True:
        req = urllib.request.Request(f"{URL}?{urllib.parse.urlencode(params)}", headers=headers)
        for attempt in range(5):
            try:
                body = json.load(urllib.request.urlopen(req, timeout=60))
                break
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    sys.exit(f"Alpaca rejected the keys (HTTP {e.code}). Check ~/.alpaca_keys.")
                if attempt == 4:
                    raise
                time.sleep(5 * 2 ** attempt)                     # 429 / 5xx: back off
        bars = body.get("bars", {}).get(symbol, [])
        if bars:
            c = pd.DataFrame(bars)[["t", "o", "h", "l", "c", "v"]]
            c["t"] = pd.to_datetime(c.t, utc=True).dt.tz_convert("America/New_York")
            if TIMEFRAME == "1Min":
                mins = c.t.dt.hour * 60 + c.t.dt.minute
                c = c[(mins >= 570) & (mins < 960)]
            chunks.append(c)
            total += len(c)
        page += 1
        if page % 25 == 0 and bars:
            print(f"  {symbol}: {total:,} bars kept, up to {bars[-1]['t'][:10]}", flush=True)
        token = body.get("next_page_token")
        if not token:
            return pd.concat(chunks, ignore_index=True)
        params["page_token"] = token
        time.sleep(0.35)                                         # stay well under 200 requests/min


def futures_ratio(sym, etf_close, default):
    """Median futures/ETF price ratio over timestamps where both exist (real futures bars from Yahoo)."""
    path = f"data/{sym}_5m.csv"
    if not os.path.exists(path):
        return default, "default"
    fut = pd.read_csv(path, index_col=0)
    fut.index = pd.to_datetime(fut.index, utc=True).tz_convert("America/New_York")
    both = pd.concat([fut.Close, etf_close], axis=1, keys=["fut", "etf"]).dropna()
    both = both.between_time("09:30", "15:55")
    if len(both) < 500:
        return default, "default"
    return float((both.fut / both.etf).median()), f"measured on {len(both):,} overlapping bars"


def main():
    keys = load_keys()
    for sym, (etf, default_ratio) in PAIRS.items():
        df = get_bars(etf, keys).rename(columns={"t": "Datetime", "o": "Open", "h": "High", "l": "Low",
                                                 "c": "Close", "v": "Volume"})
        df = df.set_index("Datetime")[["Open", "High", "Low", "Close", "Volume"]]
        ratio, how = futures_ratio(sym, df.Close, default_ratio)
        df[["Open", "High", "Low", "Close"]] *= ratio
        out = f"data/{sym}_alpaca_{LABEL}.csv"
        df.to_csv(out)
        print(f"{out}: {len(df):,} bars of {etf} x {ratio:.3f} ({how}), {df.index.min()} -> {df.index.max()}")


if __name__ == "__main__":
    main()
