# Impact card: noise3

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.041 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.56).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.31 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.586 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.012 | -0.033 .. +0.010 | -0.0030 | 0.28 / 0.34 / 0.42 | 0.428 |  |  | 2/2 | -0.002 | -0.031 |  | -0.8 / -1.1 |  |
| MES | 15 | h2 | -0.004 | -0.039 .. +0.032 | -0.0030 | 0.84 / 0.86 / 0.87 | 0.848 |  |  | 1/2 | -0.007 | +0.002 |  | -0.2 / -0.2 |  |
| MES | 15 | h4 | +0.019 | -0.044 .. +0.081 | +0.0024 | 0.55 / 0.53 / 0.49 | 0.5 |  |  | 1/2 | -0.007 | +0.067 |  | +0.7 / +0.6 | 0.078 |
| MES | 15 | h8 * | +0.041 | -0.034 .. +0.116 | +0.0062 | 0.28 / 0.3 / 0.28 | 0.273 | 1 | 1 | 2/2 | +0.044 | +0.035 | False | +1.0 / +1.1 |  |
| MES | 15 | h16 | +0.039 | -0.072 .. +0.149 | +0.0069 | 0.49 / 0.5 / 0.45 | 0.417 |  |  | 2/2 | +0.048 | +0.021 |  | +0.7 / +0.7 |  |
| MES | 15 | eod | -0.016 | -0.183 .. +0.150 | +0.0018 | 0.85 / 0.86 / 0.88 | 0.892 |  |  | 2/2 | -0.006 | -0.037 |  | -0.2 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.014 | -0.032 .. +0.004 | -2.1% | -0.008 | 0.12 |  | 2/2 |
| MES | 15 | h2 | -0.017 | -0.039 .. +0.004 | -1.8% | -0.013 | 0.18 |  | 2/2 |
| MES | 15 | h4 | -0.013 | -0.043 .. +0.018 | -0.9% | -0.011 | 0.49 |  | 1/2 |
| MES | 15 | h8 * | -0.049 | -0.090 .. -0.008 | -2.6% | -0.036 | 0.094 | 1 | 2/2 |
| MES | 15 | h16 | +0.014 | -0.047 .. +0.075 | +0.5% | +0.011 | 0.69 |  | 2/2 |
| MES | 15 | eod | +0.045 | -0.056 .. +0.146 | +1.0% | +0.025 | 0.38 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.54 pts | -2.12 .. +1.03 | 0.5 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | short | 7196 | +0.007 | 0.589 | +0.05 | -3.45 | -3.50 | -3.37 | -3.46 |
| MES | 15 | h2 | top fifth | short | 7196 | +0.005 | 0.589 | +0.03 | -3.47 | -3.52 | -3.37 | -3.49 |
| MES | 15 | h4 | bottom fifth | short | 7197 | +0.017 | 0.588 | +0.09 | -3.41 | -3.62 | -3.02 | -3.48 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.034 | 0.588 | +0.18 | -3.32 | -3.61 | -2.79 | -3.47 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.046 | 0.588 | +0.25 | -3.25 | -3.80 | -2.24 | -3.58 |
| MES | 15 | eod | top fifth | short | 7196 | +0.228 | 0.589 | +1.34 | -2.16 | -3.22 | -0.10 | -3.82 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.038 | +0.021 | -0.016 | +0.003 | -0.002 | +0.000 | -0.014 | -0.005 | +0.018 | +0.041 | +0.019 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
