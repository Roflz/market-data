# Impact card: rev_last_hour

last hour's move in average bars; up hour -> next hour down

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.068 R20 or more 80% of the time).
- MES 15-min size: the market moves 12% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.062 R20, CONFIRMED, q=5.44e-17, 7 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.02 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (15 min), p=0.24; we would catch an effect of 0.099 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.054 R20, CONFIRMED, q=5.72e-13, 7 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.56 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.045 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.009 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.066 R20 or more 80% of the time).
- MYM 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.048 R20, CONFIRMED, q=8.08e-15, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.80 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.097 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.006 | -0.007 .. +0.019 | +0.0012 | 0.37 / 0.39 / 0.39 | 0.386 | 1 | 1 | 6/8 | n/a | +0.006 | False | +0.8 / +0.9 |  |
| MES | 15 | h2 | +0.012 | -0.011 .. +0.034 | +0.0032 | 0.31 / 0.32 / 0.34 | 0.335 |  |  | 5/8 | n/a | +0.012 |  | +1.1 / +1.0 |  |
| MES | 15 | h4 | +0.018 | -0.020 .. +0.055 | +0.0041 | 0.36 / 0.37 / 0.4 | 0.415 |  |  | 4/8 | n/a | +0.018 |  | +1.3 / +0.9 | 0.068 |
| MES | 15 | h8 | +0.001 | -0.063 .. +0.065 | +0.0004 | 0.98 / 0.98 / 0.98 | 0.98 |  |  | 4/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MES | 15 | h16 | +0.009 | -0.074 .. +0.093 | +0.0033 | 0.83 / 0.83 / 0.84 | 0.849 |  |  | 4/8 | n/a | +0.009 |  | +0.3 / +0.2 |  |
| MES | 15 | eod | +0.008 | -0.200 .. +0.215 | +0.0034 | 0.94 / 0.94 / 0.95 | 0.948 |  |  | 3/8 | n/a | +0.008 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h1 * | +0.014 | +0.001 .. +0.026 | +0.0063 | 0.029 / 0.04 / 0.051 | 0.0495 | 1 | 0.51 | 7/8 | n/a | +0.014 | False | +2.0 / +2.2 |  |
| MNQ | 15 | h2 | +0.017 | -0.003 .. +0.038 | +0.0068 | 0.098 / 0.12 / 0.18 | 0.179 |  |  | 6/8 | n/a | +0.017 |  | +1.8 / +1.7 |  |
| MNQ | 15 | h4 | +0.021 | -0.017 .. +0.059 | +0.0051 | 0.28 / 0.29 / 0.31 | 0.332 |  |  | 4/8 | n/a | +0.021 |  | +1.5 / +1.1 | 0.099 |
| MNQ | 15 | h8 | +0.004 | -0.059 .. +0.068 | +0.0007 | 0.9 / 0.9 / 0.9 | 0.909 |  |  | 4/8 | n/a | +0.004 |  | +0.2 / +0.1 |  |
| MNQ | 15 | h16 | +0.012 | -0.075 .. +0.099 | +0.0015 | 0.79 / 0.79 / 0.81 | 0.816 |  |  | 5/8 | n/a | +0.012 |  | +0.4 / +0.3 |  |
| MNQ | 15 | eod | +0.087 | -0.138 .. +0.311 | +0.0059 | 0.45 / 0.47 / 0.48 | 0.489 |  |  | 5/8 | n/a | +0.087 |  | +1.2 / +0.8 |  |
| MYM | 15 | h1 | +0.005 | -0.009 .. +0.019 | +0.0006 | 0.5 / 0.47 / 0.5 | 0.489 |  |  | 4/8 | n/a | +0.005 |  | +0.7 / +0.7 |  |
| MYM | 15 | h2 * | +0.009 | -0.014 .. +0.033 | +0.0009 | 0.44 / 0.43 / 0.48 | 0.486 | 1 | 1 | 4/8 | n/a | +0.009 | False | +1.0 / +0.8 |  |
| MYM | 15 | h4 | +0.011 | -0.027 .. +0.049 | +0.0007 | 0.57 / 0.57 / 0.54 | 0.536 |  |  | 5/8 | n/a | +0.011 |  | +0.8 / +0.6 | 0.066 |
| MYM | 15 | h8 | -0.016 | -0.077 .. +0.045 | -0.0030 | 0.61 / 0.64 / 0.59 | 0.597 |  |  | 5/8 | n/a | -0.016 |  | -0.8 / -0.5 |  |
| MYM | 15 | h16 | -0.021 | -0.110 .. +0.068 | -0.0017 | 0.64 / 0.66 / 0.66 | 0.666 |  |  | 5/8 | n/a | -0.021 |  | -0.7 / -0.5 |  |
| MYM | 15 | eod | +0.005 | -0.227 .. +0.237 | +0.0006 | 0.97 / 0.97 / 0.97 | 0.966 |  |  | 2/8 | n/a | +0.005 |  | +0.1 / +0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.062 | -0.076 .. -0.049 | -12.0% | -0.125 | 2.3e-19 | 5.44e-17 | 7/8 |
| MES | 15 | h2 | -0.081 | -0.100 .. -0.061 | -10.9% | -0.157 | 5.8e-16 |  | 7/8 |
| MES | 15 | h4 | -0.084 | -0.113 .. -0.056 | -7.8% | -0.184 | 1.3e-08 |  | 7/8 |
| MES | 15 | h8 | -0.096 | -0.138 .. -0.054 | -6.1% | -0.206 | 1.8e-05 |  | 8/8 |
| MES | 15 | h16 | -0.104 | -0.170 .. -0.037 | -4.4% | -0.197 | 0.0023 |  | 7/8 |
| MES | 15 | eod | -0.078 | -0.216 .. +0.060 | -1.3% | -0.183 | 0.37 |  | 5/8 |
| MNQ | 15 | h1 * | -0.054 | -0.067 .. -0.040 | -10.3% | -0.109 | 4.4e-15 | 5.72e-13 | 7/8 |
| MNQ | 15 | h2 | -0.066 | -0.086 .. -0.046 | -8.7% | -0.136 | 3.8e-11 |  | 7/8 |
| MNQ | 15 | h4 | -0.064 | -0.094 .. -0.034 | -5.8% | -0.154 | 3.7e-05 |  | 7/8 |
| MNQ | 15 | h8 | -0.058 | -0.103 .. -0.013 | -3.6% | -0.154 | 0.011 |  | 6/8 |
| MNQ | 15 | h16 | -0.071 | -0.145 .. +0.002 | -2.9% | -0.150 | 0.058 |  | 7/8 |
| MNQ | 15 | eod | -0.127 | -0.272 .. +0.019 | -2.0% | -0.168 | 0.11 |  | 6/8 |
| MYM | 15 | h1 * | -0.048 | -0.060 .. -0.037 | -9.2% | -0.099 | 4.8e-17 | 8.08e-15 | 7/8 |
| MYM | 15 | h2 | -0.073 | -0.090 .. -0.056 | -9.6% | -0.132 | 5e-17 |  | 7/8 |
| MYM | 15 | h4 | -0.074 | -0.100 .. -0.047 | -6.7% | -0.151 | 8.7e-08 |  | 7/8 |
| MYM | 15 | h8 | -0.088 | -0.133 .. -0.044 | -5.4% | -0.176 | 0.0001 |  | 7/8 |
| MYM | 15 | h16 | -0.124 | -0.191 .. -0.057 | -5.1% | -0.199 | 0.00029 |  | 7/8 |
| MYM | 15 | eod | -0.128 | -0.293 .. +0.037 | -2.2% | -0.231 | 0.2 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.43 pts | -0.42 .. +1.27 | 0.47 |
| MNQ | 15 | +1.27 pts | +0.41 .. +2.14 | 0.0088 |
| MYM | 15 | -0.09 pts | -0.97 .. +0.80 | 0.85 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | long | 34299 | +0.002 | 0.131 | +0.14 | -3.36 | +nan | -3.36 | -3.36 |
| MES | 15 | h2 | top fifth | long | 34299 | +0.008 | 0.131 | +0.32 | -3.18 | +nan | -3.18 | -3.28 |
| MES | 15 | h4 | top fifth | long | 34299 | +0.017 | 0.131 | +0.51 | -2.99 | +nan | -2.99 | -3.27 |
| MES | 15 | h8 | top fifth | long | 34299 | +0.019 | 0.131 | +0.43 | -3.07 | +nan | -3.07 | -3.75 |
| MES | 15 | h16 | top fifth | long | 34299 | +0.071 | 0.131 | +1.42 | -2.08 | +nan | -2.08 | -3.32 |
| MES | 15 | eod | top fifth | long | 34299 | +0.214 | 0.131 | +5.58 | +2.08 | +nan | +2.08 | +0.23 |
| MNQ | 15 | h1 | top fifth | long | 34299 | +0.011 | 0.046 | +0.25 | -1.75 | +nan | -1.75 | -1.93 |
| MNQ | 15 | h2 | top fifth | long | 34299 | +0.018 | 0.046 | +0.53 | -1.47 | +nan | -1.47 | -1.78 |
| MNQ | 15 | h4 | top fifth | long | 34299 | +0.028 | 0.046 | +0.99 | -1.01 | +nan | -1.01 | -1.73 |
| MNQ | 15 | h8 | top fifth | long | 34299 | +0.043 | 0.046 | +1.33 | -0.67 | +nan | -0.67 | -2.40 |
| MNQ | 15 | h16 | top fifth | long | 34299 | +0.090 | 0.046 | +2.96 | +0.96 | +nan | +0.96 | -1.20 |
| MNQ | 15 | eod | top fifth | long | 34299 | +0.303 | 0.046 | +9.57 | +7.57 | +nan | +7.57 | +3.81 |
| MYM | 15 | h1 | bottom fifth | short | 34286 | +0.004 | 0.096 | +0.07 | -1.93 | +nan | -1.93 | -1.88 |
| MYM | 15 | h2 | top fifth | long | 34275 | -0.003 | 0.098 | +0.14 | -1.86 | +nan | -1.86 | -1.81 |
| MYM | 15 | h4 | bottom fifth | short | 34286 | +0.019 | 0.096 | +0.16 | -1.84 | +nan | -1.84 | -1.89 |
| MYM | 15 | h8 | bottom fifth | long | 34286 | -0.003 | 0.096 | +0.40 | -1.60 | +nan | -1.60 | -1.44 |
| MYM | 15 | h16 | bottom fifth | long | 34286 | +0.002 | 0.096 | +0.98 | -1.02 | +nan | -1.02 | -0.28 |
| MYM | 15 | eod | top fifth | long | 34275 | +0.151 | 0.098 | +4.17 | +2.17 | +nan | +2.17 | +2.79 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -2.486 | -3.002 | -3.396 | -1.785 | -0.932 | +0.000 | -0.004 | +0.001 | +0.008 | -0.019 | -0.017 |
| MNQ | 15 | -2.529 | -3.052 | -3.428 | -1.805 | -0.938 | +0.000 | +0.009 | +0.017 | +0.023 | +0.010 | +0.006 |
| MYM | 15 | -2.532 | -3.062 | -3.468 | -1.825 | -0.952 | +0.000 | -0.002 | +0.003 | +0.010 | -0.021 | -0.032 |

## Calibration

- MES 15-min: 171502 bars, 34299 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171495 bars, 34299 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171402 bars, 34275 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
