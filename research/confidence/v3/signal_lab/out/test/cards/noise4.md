# Impact card: noise4

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.021 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.081 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.27).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.23 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.587 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.021 | -0.012 .. +0.055 | +0.0039 | 0.21 / 0.17 / 0.12 | 0.0939 | 1 | 0.995 | 2/2 | +0.016 | +0.031 | False | +1.5 / +1.3 |  |
| MES | 15 | h2 | +0.014 | -0.029 .. +0.057 | +0.0021 | 0.53 / 0.53 / 0.49 | 0.506 |  |  | 2/2 | +0.009 | +0.023 |  | +0.7 / +0.6 |  |
| MES | 15 | h4 | -0.020 | -0.081 .. +0.041 | -0.0032 | 0.52 / 0.51 / 0.47 | 0.483 |  |  | 2/2 | -0.020 | -0.020 |  | -0.7 / -0.6 | 0.081 |
| MES | 15 | h8 | +0.001 | -0.090 .. +0.092 | +0.0002 | 0.98 / 0.98 / 0.97 | 0.975 |  |  | 1/2 | +0.026 | -0.045 |  | +0.0 / +0.0 |  |
| MES | 15 | h16 | -0.052 | -0.141 .. +0.038 | -0.0050 | 0.26 / 0.31 / 0.36 | 0.376 |  |  | 2/2 | -0.062 | -0.032 |  | -0.9 / -1.1 |  |
| MES | 15 | eod | +0.057 | -0.110 .. +0.224 | +0.0020 | 0.5 / 0.53 / 0.55 | 0.564 |  |  | 2/2 | +0.048 | +0.073 |  | +0.6 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.013 | -0.030 .. +0.004 | -1.9% | -0.014 | 0.18 |  | 2/2 |
| MES | 15 | h2 | -0.019 | -0.044 .. +0.006 | -1.9% | -0.013 | 0.15 |  | 2/2 |
| MES | 15 | h4 | -0.008 | -0.046 .. +0.030 | -0.6% | -0.003 | 0.68 |  | 2/2 |
| MES | 15 | h8 * | -0.057 | -0.105 .. -0.008 | -3.0% | -0.054 | 0.045 | 1 | 2/2 |
| MES | 15 | h16 | -0.042 | -0.106 .. +0.021 | -1.6% | -0.038 | 0.21 |  | 2/2 |
| MES | 15 | eod | +0.010 | -0.112 .. +0.131 | +0.2% | -0.004 | 0.9 |  | 1/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.40 pts | -1.08 .. +1.89 | 0.61 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | short | 7197 | +0.012 | 0.588 | +0.06 | -3.44 | -3.49 | -3.35 | -3.45 |
| MES | 15 | h2 | bottom fifth | short | 7197 | +0.017 | 0.588 | +0.09 | -3.41 | -3.46 | -3.30 | -3.43 |
| MES | 15 | h4 | top fifth | short | 7196 | +0.017 | 0.589 | +0.08 | -3.42 | -3.52 | -3.23 | -3.48 |
| MES | 15 | h8 | bottom fifth | short | 7197 | +0.014 | 0.588 | +0.07 | -3.43 | -3.64 | -3.02 | -3.55 |
| MES | 15 | h16 | top fifth | short | 7196 | +0.070 | 0.589 | +0.41 | -3.09 | -3.54 | -2.25 | -3.39 |
| MES | 15 | eod | bottom fifth | short | 7197 | +0.279 | 0.588 | +1.66 | -1.84 | -2.98 | +0.26 | -3.45 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.001 | -0.026 | -0.007 | -0.017 | -0.022 | +0.000 | +0.022 | +0.012 | -0.023 | +0.005 | -0.065 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
