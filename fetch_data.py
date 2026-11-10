"""Download intraday futures bars from Yahoo Finance (free, limited history)."""
import yfinance as yf

SYMBOLS = {"ES": "ES=F", "NQ": "NQ=F"}
# Yahoo limits: 1m ~ last 7-8 days, 5m ~ last 60 days
for name, ticker in SYMBOLS.items():
    for interval, period in [("5m", "60d"), ("1m", "8d")]:
        df = yf.download(ticker, interval=interval, period=period, progress=False, auto_adjust=False, multi_level_index=False)
        df.index = df.index.tz_convert("America/New_York")
        out = f"data/{name}_{interval}.csv"
        df.to_csv(out)
        print(out, len(df), df.index.min(), "->", df.index.max())
