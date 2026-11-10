# Impact card: above_vwap

close above session VWAP (1) or below (0)

Kind: state. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 60-min: no measurable direction effect (best +0.032 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MES 60-min size: the market moves 8% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.039 R20, CONFIRMED, q=2.99e-18, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.28 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | -0.001 | -0.011 .. +0.009 | -0.0008 | 0.82 / 0.83 / 0.83 | 0.823 |  |  | 9/16 | -0.010 | +0.008 |  | -0.2 / -0.2 |  |
| MES | 60 | h2 | -0.004 | -0.021 .. +0.014 | -0.0019 | 0.68 / 0.69 / 0.7 | 0.708 |  |  | 8/16 | -0.019 | +0.012 |  | -0.5 / -0.4 |  |
| MES | 60 | h4 | +0.013 | -0.015 .. +0.042 | +0.0049 | 0.35 / 0.37 / 0.42 | 0.42 |  |  | 8/16 | -0.016 | +0.042 |  | +1.2 / +0.9 | 0.046 |
| MES | 60 | h8 * | +0.032 | -0.018 .. +0.082 | +0.0085 | 0.21 / 0.21 / 0.24 | 0.235 | 1 | 0.807 | 8/16 | +0.003 | +0.061 | False | +2.1 / +1.3 |  |
| MES | 60 | h16 | +0.038 | -0.037 .. +0.113 | +0.0077 | 0.32 / 0.31 / 0.34 | 0.343 |  |  | 9/16 | +0.028 | +0.047 |  | +1.9 / +1.0 |  |
| MES | 60 | eod | +0.038 | -0.041 .. +0.117 | +0.0074 | 0.34 / 0.33 / 0.36 | 0.358 |  |  | 9/16 | +0.034 | +0.043 |  | +1.9 / +1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 * | -0.039 | -0.047 .. -0.031 | -7.6% | -0.079 | 4.6e-20 | 2.99e-18 | 15/16 |
| MES | 60 | h2 | -0.043 | -0.055 .. -0.030 | -5.8% | -0.096 | 2.1e-10 |  | 15/16 |
| MES | 60 | h4 | -0.058 | -0.079 .. -0.037 | -5.5% | -0.119 | 1.3e-07 |  | 14/16 |
| MES | 60 | h8 | -0.069 | -0.102 .. -0.036 | -4.6% | -0.143 | 3.7e-05 |  | 13/16 |
| MES | 60 | h16 | -0.055 | -0.100 .. -0.009 | -2.7% | -0.139 | 0.018 |  | 11/16 |
| MES | 60 | eod | -0.046 | -0.095 .. +0.004 | -2.1% | -0.134 | 0.072 |  | 9/16 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 60 | -0.38 pts | -1.37 .. +0.61 | 0.47 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | bottom level | long | 37306 | +0.009 | 0.094 | +0.15 | -3.35 | -3.26 | -3.44 | -3.53 |
| MES | 60 | h2 | bottom level | long | 37306 | +0.021 | 0.094 | +0.52 | -2.98 | -2.97 | -2.99 | -3.42 |
| MES | 60 | h4 | top level | long | 46107 | +0.041 | 0.094 | +1.80 | -1.70 | -2.60 | -0.83 | -2.49 |
| MES | 60 | h8 | top level | long | 46107 | +0.081 | 0.094 | +3.61 | +0.11 | -1.38 | +1.56 | -1.46 |
| MES | 60 | h16 | top level | long | 46107 | +0.129 | 0.094 | +5.57 | +2.07 | +0.16 | +3.94 | -0.68 |
| MES | 60 | eod | top level | long | 46107 | +0.143 | 0.094 | +5.98 | +2.48 | +0.40 | +4.50 | -0.70 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | -2.468 | -2.148 | -1.669 | -1.114 | -0.672 | +0.000 | -0.005 | -0.013 | -0.008 | -0.011 | +0.009 |

## Calibration

- MES 60-min: 83413 bars, 46107 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
