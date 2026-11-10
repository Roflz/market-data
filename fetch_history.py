"""
Download multi-year 1-minute S&P 500 / Nasdaq 100 index data from Dukascopy's free datafeed,
then resample to 5-minute bars in US/Eastern time.

These are index CFD prices, not futures prices. Intraday moves track ES/NQ closely; the price
level differs by the futures basis, which doesn't matter for trades that are flat by the close.
"Volume" is Dukascopy's tick volume, a proxy for activity rather than real contract volume.

Usage:  PYTHONPATH=./pylib python3 fetch_history.py [years]
"""
import datetime as dt
import lzma
import os
import struct
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

INSTRUMENTS = {"ES": "USA500IDXUSD", "NQ": "USATECHIDXUSD"}
YEARS = float(sys.argv[1]) if len(sys.argv) > 1 else 3
CACHE_ONLY = "--cache-only" in sys.argv          # build CSVs from already-downloaded days, no network
END = dt.date.today() - dt.timedelta(days=1)
START = END - dt.timedelta(days=int(365 * YEARS))
CACHE = "data/raw"


def fetch_day(inst, day):
    path = f"{CACHE}/{inst}/{day}.bin"
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
    elif CACHE_ONLY:
        return []
    else:
        # Dukascopy months are 0-based
        url = f"https://datafeed.dukascopy.com/datafeed/{inst}/{day.year}/{day.month - 1:02d}/{day.day:02d}/BID_candles_min_1.bi5"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (backtest data download)"})
        for attempt in range(6):
            try:
                time.sleep(0.3)                          # be polite: the server rate-limits bursts
                raw = urllib.request.urlopen(req, timeout=30).read()
                break
            except Exception:
                if attempt == 5:
                    print(f"  gave up on {inst} {day} (re-run later to retry)", flush=True)
                    return []
                time.sleep(15 * 2 ** attempt)            # 15s, 30s, 60s, 120s, 240s backoff
        data = lzma.decompress(raw) if raw else b""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    base = dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc)
    out = []
    for i in range(0, len(data), 24):
        t, o, c, lo, hi, v = struct.unpack(">5if", data[i:i + 24])
        if v > 0:  # skip flat filler bars when the market is closed
            out.append((base + dt.timedelta(seconds=t), o / 1000, hi / 1000, lo / 1000, c / 1000, v))
    return out


def main():
    days = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    for name, inst in INSTRUMENTS.items():
        rows, done = [], 0
        with ThreadPoolExecutor(max_workers=2) as ex:
            for day_rows in ex.map(lambda d: fetch_day(inst, d), days):
                rows.extend(day_rows)
                done += 1
                if done % 50 == 0:
                    print(f"  {name}: {done}/{len(days)} days", flush=True)
        if not rows:
            print(f"{name}: no data yet, skipped")
            continue
        m1 = pd.DataFrame(rows, columns=["Datetime", "Open", "High", "Low", "Close", "Volume"]).set_index("Datetime")
        m1.index = m1.index.tz_convert("America/New_York")
        m5 = m1.resample("5min", label="left", closed="left").agg(
            {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}).dropna()
        out = f"data/{name}_hist_5m.csv"
        m5.to_csv(out)
        print(f"{out}: {len(m5):,} bars, {m5.index.min()} -> {m5.index.max()}")


if __name__ == "__main__":
    main()
