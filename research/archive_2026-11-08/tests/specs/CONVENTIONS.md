# Shared conventions for all test builders

Project: /run/media/roflz/Disk 2/_/market_data (READ ONLY - never create, modify or delete anything there; you may import its modules read-only, e.g. calendar_days, lit_p5_orb, chosen_models, exits_engine).
Run Python as: cd "/run/media/roflz/Disk 2/_/market_data" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=./pylib python3 <your script in your own dir>
Memory: ~14 GB free shared by ~8 agents. Load 1-min CSVs with usecols (ts_event, Open, High, Low, Close, Volume, instrument_id) and float32 prices where safe; cache what you build as a pickle in YOUR dir and reuse it.

DATA
- data/NQ_fut_1m.csv, data/ES_fut_1m.csv: CME 1-minute bars, ts_event = bar OPEN time in UTC -> convert to America/New_York. Front contract by volume, raw (not back-adjusted) prices, instrument_id changes at rolls. Jun 2010 - 2026-11-06.
- data/{RTY,YM,CL,ZN,6E,GC,ES,NQ}_fut_1h.csv: hourly bars (RTY from 2017).
- data/daily_sessions_{NQ,ES}.pkl: one row per Globex session (index = session date): open/close raw & adjusted, inst, cash_holiday, early_close, cash_day (False on Globex-only holiday sessions), roll_since_prev.
- data/market_context.pkl: per trading day, everything known before 9:30 (vix_prev = prior VIX close, spx_ret_1d_prev, ...).
- data/yahoo_daily/*.csv: daily OHLC for SP500_index, NASDAQ100_index, RUSSELL2000_index, VIX_index, etc. (column Date, Open, High, Low, Close).
- calendar_days.py: expiry_fridays(trading_days), fomc_days() (scheduled statement days), cpi_days().
- chosen_models_trades.csv: the 3 live MNQ models' trades (model, date, side, exit, usd, R, bp), after skip rules; chosen_models.py builds it (the opening_range function = the existing 5-min ORB, using lit_p5_orb).

COSTS (per round trip, 1 micro): MNQ $2.00 = 1.0 NQ point ($2/pt: 1 tick 0.25 slippage each way + $1.00 commission). MES $3.50 = 0.70 ES point ($5/pt). M2K (if needed) $2.00 assumed. Micros began May 2019; earlier micro P&L is hypothetical, from E-mini prices.
bp per trade = 1e4 x net points / raw entry price. $ figures are at 1 micro.

RULES OF THE GAME
- Implement the pre-registered rule exactly. No tuning, no peeking at P&L to change a choice. Every judgment call goes into 'deviations' with the reason.
- No look-ahead: a decision at time T uses only bars that CLOSED before T (a bar stamped T-1 closes at T). Entries at the open of the bar stamped T.
- Never let a trade span a contract roll or compute a return across instrument_id changes.
- Controls with randomness use a fixed seed (12345) and 1,000 replications unless the spec says otherwise.
- Headline results in MNQ $ per trade, total $, bp per trade, trades per year, t, by era and by 2-year block, as the spec's evaluation section asks; evaluate EVERY pass criterion and say pass/fail for each.
- Save per-trade CSVs (one per rule/variant: date, entry time, exit time, side, entry, exit, exit reason, gross pts, net pts, net $, net bp, plus spec-specific fields) and a summary JSON in your dir.
