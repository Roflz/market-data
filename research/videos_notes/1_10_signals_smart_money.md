# Video 1 - "10 Trading Signals Smart Money Uses (Beginner to Advanced)"

Channel: Pro Trading School, 20 min (1221 s), uploaded 2025-05-03.
Sources used: full transcript plus 15 frames (01:10, 02:10, 03:00, 04:20, 05:10, 06:00, 08:00, 09:40, 10:50, 12:10, 13:20, 13:30 (transition, blank), 14:30, 15:50, 17:20, 19:40).

## 1. Summary

The video lists ten price-action and indicator setups, each with one to three hand-picked chart examples. Ten setups are named and nine distinct mechanisms are shown: fakey (inside-bar false break), Fibonacci "golden zone" (50-61.8%) pullback, 20/50 SMA crossover (plain, then filtered by an S/R breakout), Wyckoff spring and upthrust (false break of a range), Bollinger Band squeeze breakout, Bollinger Band touch-and-reject reversal (plain, then with horizontal S/R), triple top/bottom neckline break, and a "stop hunt" OCO bracket around an obvious level. The common idea is "false break, then reversal." Almost every example is on a daily or 1h forex/crypto chart. Only the BB breakout example is on a 5-minute chart (frame 12:10, USDJPY 5). Every example shown is a winner.

The frames show TradingView long/short tool boxes with a constant "Amount: 750" on the stop side, so every example risks a fixed $750. That is fixed-dollar risk per trade, but the video never says so out loud.

## 2. Testable concepts (1-minute OHLCV; resample to higher TF where noted)

General ambiguity across all setups: "key level", "next key level" and "strong candle" are never defined. Suggested defaults are given per setup. Swing high/low default: a fractal pivot with N=5 bars on each side (or N=3 on the resampled TF), confirmed only after N bars have closed, to avoid look-ahead.

### 2.1 Fakey (inside-bar false breakout) - 00:51-03:45
- Definition, quoted: "the market forms an inside bar, a small candle completely inside the previous candle's range" (01:07); then price breaks out and "closes back inside the inside bars range" (01:19). At 02:47 the speaker instead says "closed back inside the mother bar". Frame 01:10 draws the lines at the **mother bar** high/low, and the fake-break candle wicks beyond the mother-bar low and closes back inside.
- Variation: "two or three small candles after the inside bar before the fake breakout" (01:41).
- Direction: bullish fakey = false break to the downside, go long. Bearish fakey = false break up, go short.
- Entry: "at the close of the candle that made the false break" (02:14, 02:55, 03:26).
- Stop: "below it" / "above it" (02:18, 02:58), i.e. beyond the false-break candle's extreme. Frame 03:00 shows the stop just above that candle's high.
- Target: "the next key level" (03:00). Frames show R:R 1.0 (02:10) and 3.87 (03:00).
- Context filter in the examples: it forms at a prior S/R level (02:05) or at a trend-line retest within a downtrend (03:12, "end of the retracement").
- Ambiguous: whether the close must come back inside the inside bar's range or the mother bar's range; how many bars may pass between the inside bar and the false break; the target.
- Precise default: bar[i-1] high <= bar[i-2] high and bar[i-1] low >= bar[i-2] low (inside bar). Within the next 1-3 bars, a bar b trades beyond the mother-bar (bar[i-2]) low and closes back above it (bullish case; the mirror for bearish). Enter at b.close. Stop at b.low minus 1 tick. Target = 2R, or the nearest prior confirmed swing high, whichever is closer. Optional filter: trade only in the direction of the EMA20/EMA50 trend, or only when b's extreme is within X ticks of a prior swing level. Test on 5m/15m resamples of the 1-minute data.
- Overlap with the trader: high. A bullish fakey at swing support in an uptrend is a pullback entry with a candle-shape confirmation.

### 2.2 Fibonacci golden-zone pullback - 03:46-05:37
- Long: after "a strong move up", draw the Fib "from the low to the high of the move". The pullback enters "between the 50% and 61.8% levels" (04:00). Don't enter on touch: "wait for a bullish confirmation like a strong bullish candle" (04:13).
- Entry "at the confirmation"; "stop loss just below the 61.8% level"; target "the next resistance or the previous high" (04:19-04:26).
- Short (mirror): entry "at the close of the bearish candle", stop "just above the 61.8% level", target "the previous low" (05:06-05:14).
- Frames (04:20, 05:10; GBPUSD 1h): the long entered on a bullish close near 38.2% after a wick into the zone, stop slightly below 61.8%, target above the prior high, R:R 3.56. The short entered at about 55%, stop between 61.8% and 78.6%, target = prior low (0%), R:R 3.9.
- Ambiguous: what counts as a "strong move" (swing selection); what a "strong bullish candle" is; how far below 61.8% "just below" means.
- Precise default: an impulse is the leg between confirmed swing low L and swing high H (pivot N=5 on the working TF) with (H-L) >= k*ATR(14) (k=3 default). Arm the setup when low <= H - 0.5*(H-L) and low > H - 0.786*(H-L) (no close below 61.8%; invalidate if price closes below 78.6%). Trigger on the first bullish bar where close > open, body >= 50% of range, and close > previous bar high. Enter at that close. Stop = L + 0.382*(H-L) minus 2 ticks (i.e. just below the 61.8% retracement). Target = H (previous high), or H + 0.272*(H-L) as a variant. Cancel if not triggered within M bars (default 20).
- Overlap: very high. This is the trader's "pullback to swing support with candle confirmation" with a quantitative zone.

### 2.3 SMA 20/50 crossover - 05:37-08:43
- Raw rule: "20 simple moving average crosses above the 50 simple moving average, it gives us a buy signal" (05:51), mirror for sell (06:15). Stop "below the recent swing low" (06:05) / "above the recent swing high" (06:22). No target stated.
- The speaker warns against it: raw crossovers lead to a blown account (06:34). It "only works well in trending markets" (06:50) and should not be traded on lower timeframes; use "1 hour, 4 hour or daily charts" (07:17), not 5 or 15 min (07:21).
- Improved rule: crossover, then wait for a "breakout of that resistance" above price (07:58-08:02), and the same with support for shorts (08:20-08:30). Frame 08:00 (GBPJPY 1h): the resistance is the most recent prior swing high above price at crossover time. Entry is when price breaks through it.
- Ambiguous: entry bar (crossover close or breakout close); target; how long after the crossover the breakout may come.
- Precise default (1h resample, as the video recommends): when SMA20 crosses above SMA50, set R = the most recent confirmed swing high above the close. Go long on the first close > R within 30 bars while SMA20 > SMA50. Stop = most recent confirmed swing low before entry. Target 2R/3R or a trailing exit on the opposite crossover. Mirror for shorts.
- Overlap: medium. The trader uses EMA 8/20/50 as a trend filter, and this is a trend-start trigger rather than a pullback. The video explicitly discourages using it on low timeframes.

### 2.4 Wyckoff spring - 08:45-10:02
- Context: "a ranging market after a downtrend" (08:50). Price bounces between support and resistance.
- Signal: a break below support, then "the price quickly closes back inside the range" (09:20-09:24).
- Entry "at the close of the candle that made the false breakout" (09:39); stop "just below the lowest point of the range" (09:43). The frame shows the stop below the spring wick. Target "the next resistance level above" (09:48). Frame 09:40 (USDJPY daily): target = range top, R:R 2.45.
- Ambiguous: range detection; how far the break must go; "quickly" (same bar or within N bars).
- Precise default: range = the last W bars (default 40 on the working TF) whose high-low span <= m*ATR (m=4), preceded by a downtrend (close W bars earlier at least 2*ATR above the range high, or SMA50 sloping down). Spring = a bar whose low < range low and whose close > range low (same-bar reclaim), or a reclaim within 3 bars. Enter at that close. Stop = spring low minus 1 tick. Target = range high. Skip if R:R < 1.5.
- Overlap: medium. It is a counter-trend range reversal, though the false-break-at-support candle is similar to the trader's support confirmations.

### 2.5 Wyckoff upthrust - 10:02-11:00
- Mirror of the spring after an uptrend. Enter "at the close of the candle that falls back below the resistance level" (10:39). The stop is said to be "just above the resistance level" (10:43), but frame 10:50 places it above the upthrust high. Target "the next major support zone below the range" (10:47). In the frame it is the range bottom, R:R 2.32.
- Precise default: the mirror of 2.4, with the stop above the upthrust bar's high (as shown, which is safer than the spoken rule).

### 2.6 Bollinger Band squeeze breakout - 11:00-12:47
- Indicator: BB with a 20-period middle line (11:14). Frame 12:10 shows "BB 20 SMA close 2" (20, 2 standard deviations) on a USDJPY **5-minute** chart.
- Rule: identify a sideways market where the bands "are squeezed tightly together" (11:40). Price stays within the bands. Wait for "a strong breakout candle that closes outside the bands" (11:56): above the upper band means long, below the lower band means short.
- No stop or target is given beyond "very tight stop-loss" (11:31).
- Precise default: squeeze = BB width (upper-lower)/middle in the lowest 20th percentile of the last 120 bars, and no close outside the bands during the last 20 bars. Signal = a close above the upper band (long) or below the lower band (short) with body >= 60% of range. Enter at close. Stop = the opposite side of the signal bar (its low for longs) or the BB middle line; test both. Target = 2R, or trail with the middle band.
- Overlap: low-medium. It is a breakout rather than a pullback, but it fits a "trade all hours" 1m/5m approach and is fully mechanical.

### 2.7 Bollinger Band reversal (range) - 12:47-15:08
- Context: "the market is moving sideways" (13:06). "Price touches the upper band and right after that it gets rejected" (13:13).
- Entry "after the rejection candle"; stop "just above the high"; target "the lower band" (13:24-13:29). Mirror for longs (13:45-13:52).
- Advanced filter: the band touch must coincide with a horizontal S/R level drawn from earlier touches (13:57-15:06).
- Frame 13:20 (USDCHF daily): R:R 4.62. Frame 14:30 (GBPUSD daily): the rejection is at both the upper band and a prior high.
- Ambiguous: "rejection candle"; how to detect "ranging".
- Precise default: range filter = |SMA50 slope over 20 bars| < 0.5*ATR, or ADX(14) < 20. Short when bar high >= upper BB(20,2), close < open, and close back below the upper band; enter at close. Stop = bar high + 1 tick. Target = lower band value at entry (fixed) or the middle band (variant). Advanced variant: additionally require the bar high to be within 0.25*ATR of a prior confirmed swing high.
- Overlap: low. It is counter-trend, mean reversion.

### 2.8 Triple top / triple bottom neckline break - 15:08-17:36
- Triple top: "three distinct peaks" after an uptrend (15:24). The neckline connects the lows between the tops (15:40). Enter "as soon as the candle closes below the neckline" (15:48). Stop "above the neckline" (15:50). Target "the next major support level" (15:54). Frame 15:50 (NZDUSD daily): stop above the breakout candle's open, R:R 3.65.
- Triple bottom: enter when "the breakout candle closes above the neckline" (17:03). Stop "below the neckline or under the third bottom" (17:07). Target "the next resistance level or a projected move equal to the height of the pattern" (17:10). Frame 17:20: R:R 2.08.
- Precise default: three confirmed swing lows within a tolerance of 0.5*ATR of each other, separated by swing highs. Neckline = the max of the intermediate swing highs. Long on the first close above the neckline. Stop = neckline - 0.5*(neckline - avg bottom), or below the third bottom (test both). Target = neckline + (neckline - min bottom) (measured move).
- Overlap: low-medium. Pattern detection is fiddly and rare on intraday futures.

### 2.9 Stop hunt OCO bracket - 17:36-20:08
- Pick "a support or resistance level that's clear and obvious" (18:27), e.g. one that was rejected before (18:42).
- When price breaks above resistance, "place a limit sell order just below the key level" (18:57-19:00) and also "a limit buy order above the breakout candle" (19:16-19:20). The speaker says limit, but a buy above price is really a stop order. Once one fills, "we cancel the other" (19:35).
- Stop "above the resistance level"; target "a minimum of three times the stop-loss distance" (19:42-19:47). Frame 19:40 (NZDUSD daily) shows R:R 2.8 and a stop above the breakout high, so the example itself does not meet the 3x minimum.
- Precise default: level = a confirmed swing high touched at least twice (within 0.25*ATR). Breakout bar = first close above the level. Then place a sell-stop at level - 1 tick (the video says limit, which would fill immediately when price is above; a sell-stop is the executable reading) and a buy-stop at breakout bar high + 1 tick, valid for N bars (default 10), OCO. Short: stop = max high since the breakout + 1 tick, target 3R. Long: stop = level - 1 tick (assumed; the video gives no stop for the long leg), target 3R.
- Overlap: medium. It brackets an obvious swing level, and the short leg is a false-break reversal.

## 3. Risk / position sizing relevant to a prop evaluation
- No sizing numbers are spoken. Generic warnings only: "not a holy grail ... proper money management is essential" (03:38-03:44); "smart money management is not optional" (05:31).
- Visible in the frames: every trade risks a fixed $750 ("Amount: 750" on the stop side at 02:10, 05:10, 09:40, 10:50, 13:20, 15:50, 17:20, 19:40), with size varying to match. That is fixed-dollar risk per trade regardless of stop distance. For a $1,000 trailing-drawdown evaluation the absolute number is irrelevant. The method transfers: size contracts = floor(risk$ / (stop ticks * tick value)), which for MES/MNQ/MYM means choosing the micro count from the stop distance.
- Target 3x stop for the stop hunt (19:45).

## 4. Numeric claims and backing
- No win-rate claims. Words like "high probability" (05:06, 10:02) and "high confident" (15:04) are not quantified.
- R:R values shown on the drawn trades: 1.0, 3.87, 3.56, 3.9, 2.45, 2.32, 4.62, 3.65, 2.08, 2.8. These are single hand-picked winning examples. Nothing backs them statistically: no backtest, trade count, or losing examples apart from the crossover-in-a-range illustration (06:57).
- "Minimum of three times the stop-loss" (19:46) is contradicted by the 2.8 R:R in its own example.

## 5. Not relevant / not testable
- "Smart money" / institutional intent narratives (e.g. 09:02-09:07, 18:16) are interpretation, not rules.
- "Key level" and "next key level" as targets are discretionary. They can only be approximated with swing pivots.
- Trend lines (03:12) are discretionary. Approximate with "in a downtrend, pullback to EMA" if needed.
- The timeframe advice (crossovers only on 1h+, 07:17) suggests most setups were shown on daily/1h forex. Behaviour on 1-minute MES/MNQ/MYM is untested and may differ. Resampling 1-minute data to 5m/15m/1h is the natural way to test.
- Triple patterns on daily charts happen too rarely within a 23-hour intraday evaluation window to matter much.
