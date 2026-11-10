# Impact card: noise0

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.053 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.20 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.586 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | +0.008 | -0.021 .. +0.037 | +0.0034 | 0.59 / 0.58 / 0.57 | 0.55 |  |  | 2/2 | +0.010 | +0.004 |  | +0.6 / +0.5 |  |
| MES | 15 | h2 | -0.003 | -0.041 .. +0.034 | -0.0021 | 0.87 / 0.88 / 0.88 | 0.884 |  |  | 1/2 | -0.016 | +0.021 |  | -0.2 / -0.2 |  |
| MES | 15 | h4 | -0.016 | -0.069 .. +0.036 | -0.0016 | 0.54 / 0.56 / 0.61 | 0.599 |  |  | 1/2 | -0.054 | +0.054 |  | -0.6 / -0.6 | 0.077 |
| MES | 15 | h8 | -0.007 | -0.080 .. +0.066 | +0.0009 | 0.86 / 0.86 / 0.88 | 0.876 |  |  | 1/2 | -0.034 | +0.044 |  | -0.2 / -0.2 |  |
| MES | 15 | h16 * | +0.053 | -0.056 .. +0.163 | +0.0048 | 0.34 / 0.38 / 0.34 | 0.345 | 1 | 1 | 2/2 | +0.008 | +0.137 | False | +1.0 / +1.0 |  |
| MES | 15 | eod | +0.007 | -0.218 .. +0.231 | +0.0006 | 0.95 / 0.95 / 0.92 | 0.898 |  |  | 1/2 | -0.089 | +0.184 |  | +0.1 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.000 | -0.018 .. +0.018 | -0.0% | -0.001 | 0.99 |  | 1/2 |
| MES | 15 | h2 | -0.010 | -0.034 .. +0.013 | -1.0% | -0.000 | 0.44 |  | 1/2 |
| MES | 15 | h4 | -0.019 | -0.050 .. +0.013 | -1.4% | -0.014 | 0.45 |  | 2/2 |
| MES | 15 | h8 | -0.023 | -0.065 .. +0.019 | -1.2% | -0.022 | 0.35 |  | 1/2 |
| MES | 15 | h16 * | -0.033 | -0.100 .. +0.034 | -1.3% | -0.038 | 0.35 | 1 | 1/2 |
| MES | 15 | eod | -0.050 | -0.186 .. +0.086 | -1.1% | +0.002 | 0.47 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.07 pts | -1.47 .. +1.33 | 0.93 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | short | 7197 | +0.010 | 0.588 | +0.05 | -3.45 | -3.50 | -3.37 | -3.46 |
| MES | 15 | h2 | top fifth | short | 7196 | +0.006 | 0.589 | +0.02 | -3.48 | -3.52 | -3.42 | -3.51 |
| MES | 15 | h4 | top fifth | short | 7196 | +0.012 | 0.589 | +0.06 | -3.44 | -3.38 | -3.56 | -3.51 |
| MES | 15 | h8 | top fifth | short | 7196 | +0.031 | 0.589 | +0.17 | -3.33 | -3.48 | -3.07 | -3.46 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.062 | 0.588 | +0.32 | -3.18 | -3.76 | -2.09 | -3.47 |
| MES | 15 | eod | bottom fifth | short | 7197 | +0.287 | 0.588 | +1.62 | -1.88 | -3.32 | +0.79 | -3.52 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.044 | -0.019 | -0.007 | +0.010 | -0.007 | +0.000 | +0.008 | -0.003 | -0.021 | +0.010 | +0.092 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
