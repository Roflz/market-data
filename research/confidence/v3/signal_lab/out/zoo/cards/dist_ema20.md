# Impact card: dist_ema20

(close - EMA20) in R20 (average bars) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (5 min), p=0.012; we would catch an effect of 0.022 R20 or more 80% of the time).
- MES 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.033 R20, CONFIRMED, q=5.28e-27, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.40 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.216 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.010 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.046 R20, CONFIRMED, q=6e-18, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.74 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.125 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.015 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.085 R20 or more 80% of the time).
- MES 60-min size: the market moves 14% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.073 R20, CONFIRMED, q=1.18e-15, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.60 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.033 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.033 R20, CONFIRMED, q=2.44e-24, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.375 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.056 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.047 R20, CONFIRMED, q=3.12e-09, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.59 at recent bar sizes, 90% range up to $1.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.091 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.057 R20, CONFIRMED, q=3.93e-10, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.32 at recent bar sizes, 90% range up to $3.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.095 R20 over the next 16 bars (80 min), p=0.2; we would catch an effect of 0.051 R20 or more 80% of the time).
- MYM 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.041 R20, CONFIRMED, q=1.97e-10, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.53 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.167 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.568 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MYM 15-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.057 R20, CONFIRMED, q=5.55e-05, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.02 at recent bar sizes, 90% range up to $2.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.017 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.124 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.055 R20, CONFIRMED, q=0.00228, 6 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.36 at recent bar sizes, 90% range up to $4.25); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.007 | -0.012 .. -0.003 | -0.0044 | 0.002 / 0.002 / 0.0025 | 0.00287 | 0.318 | 0.406 | 10/16 | -0.010 | -0.005 | False | -3.0 / -3.1 |  |
| MES | 5 | h2 | -0.009 | -0.017 .. -0.001 | -0.0032 | 0.027 / 0.025 / 0.041 | 0.0406 |  |  | 11/16 | -0.017 | -0.001 |  | -2.7 / -2.2 |  |
| MES | 5 | h4 | -0.008 | -0.023 .. +0.007 | -0.0014 | 0.28 / 0.27 / 0.33 | 0.334 |  |  | 10/16 | -0.024 | +0.007 |  | -1.8 / -1.1 | 0.022 |
| MES | 5 | h8 | -0.025 | -0.054 .. +0.004 | -0.0035 | 0.093 / 0.08 / 0.11 | 0.106 |  |  | 12/16 | -0.065 | +0.015 |  | -3.7 / -1.7 |  |
| MES | 5 | h16 | -0.042 | -0.095 .. +0.011 | -0.0039 | 0.12 / 0.1 / 0.13 | 0.124 |  |  | 12/16 | -0.100 | +0.016 |  | -4.3 / -1.5 |  |
| MES | 5 | eod | -0.050 | -0.380 .. +0.279 | -0.0017 | 0.76 / 0.77 / 0.78 | 0.773 |  |  | 11/16 | -0.129 | +0.028 |  | -1.0 / -0.3 |  |
| MES | 15 | h1 | -0.000 | -0.010 .. +0.010 | -0.0018 | 0.98 / 0.98 / 0.97 | 0.965 |  |  | 9/16 | -0.012 | +0.012 |  | -0.0 / -0.0 |  |
| MES | 15 | h2 | -0.002 | -0.019 .. +0.015 | -0.0007 | 0.83 / 0.82 / 0.81 | 0.809 |  |  | 9/16 | -0.025 | +0.021 |  | -0.3 / -0.2 |  |
| MES | 15 | h4 * | -0.010 | -0.042 .. +0.023 | -0.0016 | 0.55 / 0.53 / 0.53 | 0.526 | 1 | 1 | 9/16 | -0.045 | +0.025 | False | -1.1 / -0.6 | 0.044 |
| MES | 15 | h8 | -0.010 | -0.062 .. +0.042 | -0.0025 | 0.71 / 0.71 / 0.73 | 0.724 |  |  | 9/16 | -0.072 | +0.052 |  | -0.7 / -0.4 |  |
| MES | 15 | h16 | -0.016 | -0.102 .. +0.069 | -0.0007 | 0.71 / 0.71 / 0.75 | 0.747 |  |  | 8/16 | -0.141 | +0.108 |  | -0.9 / -0.4 |  |
| MES | 15 | eod | +0.088 | -0.330 .. +0.507 | +0.0090 | 0.68 / 0.67 / 0.61 | 0.608 |  |  | 7/16 | -0.135 | +0.311 |  | +1.8 / +0.4 |  |
| MES | 60 | h1 | +0.006 | -0.011 .. +0.023 | +0.0080 | 0.5 / 0.5 / 0.53 | 0.52 |  |  | 7/16 | -0.015 | +0.026 |  | +0.6 / +0.7 |  |
| MES | 60 | h2 * | +0.015 | -0.016 .. +0.045 | +0.0069 | 0.35 / 0.35 / 0.4 | 0.395 | 1 | 1 | 6/16 | -0.021 | +0.050 | False | +1.1 / +0.9 |  |
| MES | 60 | h4 | +0.020 | -0.034 .. +0.075 | +0.0079 | 0.47 / 0.47 / 0.51 | 0.515 |  |  | 7/16 | -0.042 | +0.083 |  | +1.1 / +0.7 | 0.085 |
| MES | 60 | h8 | +0.014 | -0.081 .. +0.109 | +0.0026 | 0.77 / 0.77 / 0.78 | 0.777 |  |  | 9/16 | -0.074 | +0.102 |  | +0.6 / +0.3 |  |
| MES | 60 | h16 | -0.017 | -0.170 .. +0.136 | -0.0040 | 0.82 / 0.82 / 0.84 | 0.841 |  |  | 9/16 | -0.142 | +0.108 |  | -0.6 / -0.2 |  |
| MES | 60 | eod | -0.041 | -0.208 .. +0.126 | -0.0054 | 0.63 / 0.63 / 0.67 | 0.671 |  |  | 10/16 | -0.139 | +0.057 |  | -1.3 / -0.5 |  |
| MNQ | 5 | h1 * | +0.003 | -0.002 .. +0.008 | +0.0037 | 0.27 / 0.27 / 0.27 | 0.272 | 1 | 1 | 11/16 | -0.003 | +0.009 | False | +1.0 / +1.1 |  |
| MNQ | 5 | h2 | +0.005 | -0.005 .. +0.014 | +0.0025 | 0.34 / 0.34 / 0.42 | 0.435 |  |  | 9/16 | -0.008 | +0.017 |  | +1.1 / +1.0 |  |
| MNQ | 5 | h4 | +0.011 | -0.006 .. +0.028 | +0.0039 | 0.22 / 0.22 / 0.33 | 0.338 |  |  | 8/16 | -0.013 | +0.034 |  | +1.9 / +1.2 | 0.033 |
| MNQ | 5 | h8 | -0.002 | -0.038 .. +0.034 | +0.0001 | 0.91 / 0.91 / 0.93 | 0.928 |  |  | 9/16 | -0.043 | +0.038 |  | -0.2 / -0.1 |  |
| MNQ | 5 | h16 | -0.016 | -0.093 .. +0.061 | -0.0015 | 0.68 / 0.66 / 0.66 | 0.646 |  |  | 9/16 | -0.059 | +0.026 |  | -1.3 / -0.4 |  |
| MNQ | 5 | eod | -0.049 | -0.625 .. +0.527 | +0.0020 | 0.87 / 0.87 / 0.84 | 0.853 |  |  | 10/16 | -0.323 | +0.222 |  | -0.7 / -0.2 |  |
| MNQ | 15 | h1 | +0.002 | -0.014 .. +0.018 | -0.0002 | 0.82 / 0.81 / 0.75 | 0.765 |  |  | 10/16 | -0.003 | +0.007 |  | +0.3 / +0.2 |  |
| MNQ | 15 | h2 | +0.008 | -0.014 .. +0.030 | -0.0009 | 0.48 / 0.47 / 0.51 | 0.521 |  |  | 9/16 | -0.006 | +0.022 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h4 | +0.017 | -0.026 .. +0.061 | -0.0045 | 0.44 / 0.44 / 0.46 | 0.476 |  |  | 8/16 | -0.008 | +0.043 |  | +0.8 / +0.8 | 0.056 |
| MNQ | 15 | h8 | +0.007 | -0.066 .. +0.080 | -0.0065 | 0.85 / 0.85 / 0.86 | 0.846 |  |  | 9/16 | -0.037 | +0.051 |  | +0.3 / +0.2 |  |
| MNQ | 15 | h16 | +0.035 | -0.102 .. +0.173 | +0.0039 | 0.62 / 0.62 / 0.59 | 0.577 |  |  | 8/16 | -0.125 | +0.195 |  | +1.2 / +0.5 |  |
| MNQ | 15 | eod * | +0.375 | -0.422 .. +1.171 | +0.0215 | 0.36 / 0.35 / 0.1 | 0.101 | 1 | 1 | 7/16 | -0.001 | +0.748 | False | +4.1 / +0.9 |  |
| MNQ | 60 | h1 * | +0.007 | -0.012 .. +0.026 | +0.0097 | 0.47 / 0.47 / 0.48 | 0.466 | 1 | 1 | 9/16 | -0.016 | +0.030 | False | +0.7 / +0.7 |  |
| MNQ | 60 | h2 | +0.010 | -0.024 .. +0.044 | +0.0093 | 0.56 / 0.57 / 0.58 | 0.578 |  |  | 10/16 | -0.021 | +0.041 |  | +0.7 / +0.6 |  |
| MNQ | 60 | h4 | +0.014 | -0.044 .. +0.073 | +0.0086 | 0.64 / 0.64 / 0.66 | 0.659 |  |  | 10/16 | -0.034 | +0.062 |  | +0.7 / +0.5 | 0.091 |
| MNQ | 60 | h8 | +0.001 | -0.094 .. +0.097 | +0.0045 | 0.98 / 0.98 / 0.98 | 0.978 |  |  | 8/16 | -0.046 | +0.048 |  | +0.0 / +0.0 |  |
| MNQ | 60 | h16 | -0.038 | -0.196 .. +0.121 | -0.0018 | 0.64 / 0.65 / 0.68 | 0.678 |  |  | 11/16 | -0.069 | -0.007 |  | -1.2 / -0.5 |  |
| MNQ | 60 | eod | -0.071 | -0.245 .. +0.103 | -0.0062 | 0.42 / 0.44 / 0.48 | 0.483 |  |  | 11/16 | -0.066 | -0.076 |  | -2.1 / -0.8 |  |
| MYM | 5 | h1 | -0.008 | -0.016 .. +0.000 | -0.0006 | 0.065 / 0.057 / 0.097 | 0.0991 |  |  | 5/8 | n/a | -0.008 |  | -1.5 / -1.8 |  |
| MYM | 5 | h2 | -0.016 | -0.030 .. -0.002 | -0.0035 | 0.027 / 0.025 / 0.099 | 0.0948 |  |  | 6/8 | n/a | -0.016 |  | -2.4 / -2.2 |  |
| MYM | 5 | h4 | -0.025 | -0.054 .. +0.003 | -0.0028 | 0.075 / 0.068 / 0.18 | 0.176 |  |  | 6/8 | n/a | -0.025 |  | -2.5 / -1.8 | 0.051 |
| MYM | 5 | h8 | -0.047 | -0.092 .. -0.001 | -0.0061 | 0.044 / 0.041 / 0.12 | 0.131 |  |  | 7/8 | n/a | -0.047 |  | -3.4 / -2.0 |  |
| MYM | 5 | h16 * | -0.095 | -0.172 .. -0.017 | -0.0068 | 0.017 / 0.02 / 0.062 | 0.0632 | 1 | 0.949 | 6/8 | n/a | -0.095 | False | -5.5 / -2.4 |  |
| MYM | 5 | eod | +0.115 | -0.739 .. +0.968 | +0.0075 | 0.79 / 0.8 / 0.72 | 0.742 |  |  | 3/8 | n/a | +0.115 |  | +1.2 / +0.3 |  |
| MYM | 15 | h1 | -0.003 | -0.017 .. +0.011 | -0.0014 | 0.64 / 0.65 / 0.67 | 0.682 |  |  | 4/8 | n/a | -0.003 |  | -0.4 / -0.5 |  |
| MYM | 15 | h2 | +0.011 | -0.026 .. +0.047 | +0.0023 | 0.56 / 0.57 / 0.54 | 0.548 |  |  | 3/8 | n/a | +0.011 |  | +0.6 / +0.6 |  |
| MYM | 15 | h4 | +0.033 | -0.044 .. +0.111 | +0.0020 | 0.4 / 0.42 / 0.3 | 0.313 |  |  | 3/8 | n/a | +0.033 |  | +1.1 / +0.8 | 0.076 |
| MYM | 15 | h8 | +0.066 | -0.086 .. +0.219 | +0.0068 | 0.39 / 0.41 / 0.24 | 0.234 |  |  | 4/8 | n/a | +0.066 |  | +1.7 / +0.9 |  |
| MYM | 15 | h16 | +0.186 | -0.201 .. +0.574 | +0.0290 | 0.35 / 0.36 / 0.063 | 0.0638 |  |  | 4/8 | n/a | +0.186 |  | +3.5 / +0.9 |  |
| MYM | 15 | eod * | +0.568 | -0.578 .. +1.714 | +0.0337 | 0.33 / 0.33 / 0.059 | 0.0532 | 1 | 1 | 4/8 | n/a | +0.568 | False | +4.5 / +1.0 |  |
| MYM | 60 | h1 * | +0.017 | -0.007 .. +0.041 | +0.0070 | 0.16 / 0.19 / 0.21 | 0.224 | 1 | 1 | 5/8 | n/a | +0.017 | False | +1.2 / +1.4 |  |
| MYM | 60 | h2 | +0.019 | -0.028 .. +0.066 | +0.0055 | 0.43 / 0.45 / 0.45 | 0.453 |  |  | 5/8 | n/a | +0.019 |  | +1.0 / +0.8 |  |
| MYM | 60 | h4 | +0.050 | -0.035 .. +0.135 | +0.0086 | 0.25 / 0.26 / 0.25 | 0.257 |  |  | 6/8 | n/a | +0.050 |  | +1.9 / +1.2 | 0.124 |
| MYM | 60 | h8 | +0.078 | -0.069 .. +0.225 | +0.0113 | 0.3 / 0.29 / 0.28 | 0.29 |  |  | 5/8 | n/a | +0.078 |  | +2.3 / +1.0 |  |
| MYM | 60 | h16 | +0.102 | -0.132 .. +0.337 | +0.0094 | 0.39 / 0.38 / 0.39 | 0.386 |  |  | 5/8 | n/a | +0.102 |  | +2.3 / +0.9 |  |
| MYM | 60 | eod | +0.086 | -0.174 .. +0.346 | +0.0086 | 0.52 / 0.5 / 0.51 | 0.507 |  |  | 5/8 | n/a | +0.086 |  | +1.9 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.033 | -0.039 .. -0.028 | -6.7% | -0.065 | 7.5e-30 | 5.28e-27 | 14/16 |
| MES | 5 | h2 | -0.045 | -0.054 .. -0.036 | -6.4% | -0.089 | 2.1e-24 |  | 13/16 |
| MES | 5 | h4 | -0.057 | -0.071 .. -0.043 | -5.7% | -0.118 | 9.6e-16 |  | 13/16 |
| MES | 5 | h8 | -0.074 | -0.096 .. -0.051 | -5.1% | -0.152 | 1.5e-10 |  | 14/16 |
| MES | 5 | h16 | -0.092 | -0.126 .. -0.058 | -4.4% | -0.172 | 1.7e-07 |  | 14/16 |
| MES | 5 | eod | -0.186 | -0.410 .. +0.037 | -1.9% | -0.371 | 0.1 |  | 12/16 |
| MES | 15 | h1 * | -0.046 | -0.055 .. -0.036 | -9.0% | -0.098 | 1.1e-20 | 6e-18 | 14/16 |
| MES | 15 | h2 | -0.057 | -0.072 .. -0.042 | -7.8% | -0.122 | 2.6e-13 |  | 14/16 |
| MES | 15 | h4 | -0.067 | -0.091 .. -0.043 | -6.4% | -0.146 | 3.7e-08 |  | 13/16 |
| MES | 15 | h8 | -0.082 | -0.121 .. -0.043 | -5.3% | -0.172 | 4.2e-05 |  | 12/16 |
| MES | 15 | h16 | -0.085 | -0.151 .. -0.019 | -3.7% | -0.205 | 0.011 |  | 9/16 |
| MES | 15 | eod | -0.136 | -0.456 .. +0.183 | -2.5% | -0.326 | 0.4 |  | 10/16 |
| MES | 60 | h1 * | -0.073 | -0.089 .. -0.057 | -14.2% | -0.147 | 2.4e-18 | 1.18e-15 | 15/16 |
| MES | 60 | h2 | -0.084 | -0.108 .. -0.059 | -11.3% | -0.184 | 2.2e-11 |  | 15/16 |
| MES | 60 | h4 | -0.111 | -0.149 .. -0.073 | -10.5% | -0.228 | 1.2e-08 |  | 13/16 |
| MES | 60 | h8 | -0.139 | -0.199 .. -0.079 | -9.2% | -0.279 | 6.2e-06 |  | 14/16 |
| MES | 60 | h16 | -0.149 | -0.246 .. -0.052 | -7.2% | -0.313 | 0.0026 |  | 13/16 |
| MES | 60 | eod | -0.141 | -0.256 .. -0.026 | -6.5% | -0.317 | 0.016 |  | 13/16 |
| MNQ | 5 | h1 * | -0.033 | -0.039 .. -0.027 | -6.2% | -0.064 | 3.8e-27 | 2.44e-24 | 15/16 |
| MNQ | 5 | h2 | -0.040 | -0.049 .. -0.032 | -5.3% | -0.084 | 3.1e-19 |  | 14/16 |
| MNQ | 5 | h4 | -0.049 | -0.064 .. -0.035 | -4.5% | -0.109 | 2e-10 |  | 14/16 |
| MNQ | 5 | h8 | -0.058 | -0.086 .. -0.031 | -3.6% | -0.128 | 8.7e-05 |  | 14/16 |
| MNQ | 5 | h16 | -0.078 | -0.119 .. -0.037 | -3.3% | -0.139 | 0.003 |  | 13/16 |
| MNQ | 5 | eod | -0.351 | -0.786 .. +0.083 | -2.8% | -0.519 | 0.12 |  | 10/16 |
| MNQ | 15 | h1 * | -0.047 | -0.061 .. -0.034 | -8.9% | -0.098 | 8.8e-12 | 3.12e-09 | 15/16 |
| MNQ | 15 | h2 | -0.068 | -0.102 .. -0.033 | -8.7% | -0.144 | 0.00014 |  | 14/16 |
| MNQ | 15 | h4 | -0.096 | -0.185 .. -0.007 | -8.5% | -0.211 | 0.034 |  | 13/16 |
| MNQ | 15 | h8 | -0.118 | -0.270 .. +0.035 | -7.0% | -0.307 | 0.13 |  | 12/16 |
| MNQ | 15 | h16 | -0.096 | -0.266 .. +0.074 | -3.8% | -0.441 | 0.27 |  | 10/16 |
| MNQ | 15 | eod | -0.419 | -1.253 .. +0.414 | -6.6% | -0.665 | 0.32 |  | 10/16 |
| MNQ | 60 | h1 * | -0.057 | -0.073 .. -0.042 | -10.9% | -0.129 | 1.1e-12 | 3.93e-10 | 15/16 |
| MNQ | 60 | h2 | -0.063 | -0.087 .. -0.039 | -8.2% | -0.158 | 1.7e-07 |  | 14/16 |
| MNQ | 60 | h4 | -0.077 | -0.114 .. -0.041 | -7.0% | -0.190 | 3.3e-05 |  | 13/16 |
| MNQ | 60 | h8 | -0.123 | -0.181 .. -0.065 | -7.8% | -0.258 | 3.2e-05 |  | 14/16 |
| MNQ | 60 | h16 | -0.165 | -0.261 .. -0.070 | -7.5% | -0.351 | 0.00075 |  | 13/16 |
| MNQ | 60 | eod | -0.156 | -0.264 .. -0.047 | -6.8% | -0.356 | 0.006 |  | 11/16 |
| MYM | 5 | h1 * | -0.041 | -0.053 .. -0.030 | -7.8% | -0.073 | 5.2e-13 | 1.97e-10 | 8/8 |
| MYM | 5 | h2 | -0.048 | -0.062 .. -0.035 | -6.4% | -0.097 | 4.2e-12 |  | 7/8 |
| MYM | 5 | h4 | -0.062 | -0.091 .. -0.034 | -5.7% | -0.129 | 1.4e-05 |  | 7/8 |
| MYM | 5 | h8 | -0.067 | -0.106 .. -0.028 | -4.2% | -0.154 | 0.00084 |  | 7/8 |
| MYM | 5 | h16 | -0.074 | -0.133 .. -0.015 | -3.2% | -0.167 | 0.044 |  | 5/8 |
| MYM | 5 | eod | -0.464 | -1.125 .. +0.196 | -4.0% | -0.784 | 0.17 |  | 5/8 |
| MYM | 15 | h1 * | -0.057 | -0.078 .. -0.035 | -10.7% | -0.112 | 2.2e-07 | 5.55e-05 | 8/8 |
| MYM | 15 | h2 | -0.093 | -0.151 .. -0.036 | -12.2% | -0.177 | 0.0015 |  | 7/8 |
| MYM | 15 | h4 | -0.147 | -0.275 .. -0.019 | -13.2% | -0.283 | 0.025 |  | 6/8 |
| MYM | 15 | h8 | -0.214 | -0.418 .. -0.009 | -13.0% | -0.463 | 0.045 |  | 7/8 |
| MYM | 15 | h16 | -0.319 | -0.694 .. +0.057 | -12.9% | -0.717 | 0.1 |  | 6/8 |
| MYM | 15 | eod | -0.588 | -1.630 .. +0.454 | -9.8% | -0.989 | 0.28 |  | 5/8 |
| MYM | 60 | h1 * | -0.055 | -0.079 .. -0.030 | -10.4% | -0.119 | 9.9e-06 | 0.00228 | 6/8 |
| MYM | 60 | h2 | -0.067 | -0.104 .. -0.030 | -8.9% | -0.153 | 0.00037 |  | 7/8 |
| MYM | 60 | h4 | -0.094 | -0.152 .. -0.036 | -8.7% | -0.189 | 0.0015 |  | 6/8 |
| MYM | 60 | h8 | -0.099 | -0.195 .. -0.004 | -6.4% | -0.214 | 0.041 |  | 6/8 |
| MYM | 60 | h16 | -0.113 | -0.268 .. +0.041 | -5.3% | -0.234 | 0.15 |  | 5/8 |
| MYM | 60 | eod | -0.115 | -0.291 .. +0.062 | -5.1% | -0.247 | 0.21 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.93 pts | -1.41 .. -0.46 | 0.0019 |
| MES | 15 | -0.52 pts | -1.37 .. +0.33 | 0.26 |
| MES | 60 | +0.62 pts | -1.13 .. +2.37 | 0.55 |
| MNQ | 5 | -0.55 pts | -1.09 .. +0.00 | 0.084 |
| MNQ | 15 | -0.02 pts | -0.93 .. +0.89 | 0.97 |
| MNQ | 60 | +0.90 pts | -0.88 .. +2.69 | 0.32 |
| MYM | 5 | -0.58 pts | -1.24 .. +0.09 | 0.089 |
| MYM | 15 | +0.02 pts | -1.08 .. +1.12 | 0.97 |
| MYM | 60 | +1.39 pts | -1.01 .. +3.80 | 0.37 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207242 | +0.010 | 0.290 | +0.11 | -3.39 | -3.43 | -3.36 | -3.45 |
| MES | 5 | h2 | bottom fifth | long | 207242 | +0.013 | 0.290 | +0.13 | -3.37 | -3.41 | -3.34 | -3.46 |
| MES | 5 | h4 | bottom fifth | long | 207242 | +0.015 | 0.290 | +0.11 | -3.39 | -3.40 | -3.38 | -3.49 |
| MES | 5 | h8 | bottom fifth | long | 207242 | +0.026 | 0.290 | +0.19 | -3.31 | -3.26 | -3.36 | -3.46 |
| MES | 5 | h16 | bottom fifth | long | 207242 | +0.052 | 0.290 | +0.37 | -3.13 | -3.01 | -3.25 | -3.45 |
| MES | 5 | eod | bottom fifth | long | 207242 | +0.264 | 0.290 | +2.65 | -0.85 | -0.70 | -0.99 | -0.15 |
| MES | 15 | h1 | bottom fifth | long | 68432 | +0.009 | 0.167 | +0.14 | -3.36 | -3.39 | -3.32 | -3.49 |
| MES | 15 | h2 | bottom fifth | long | 68432 | +0.012 | 0.167 | +0.20 | -3.30 | -3.32 | -3.28 | -3.47 |
| MES | 15 | h4 | bottom fifth | long | 68432 | +0.024 | 0.167 | +0.33 | -3.17 | -3.13 | -3.22 | -3.40 |
| MES | 15 | h8 | bottom fifth | long | 68432 | +0.036 | 0.167 | +0.63 | -2.87 | -2.81 | -2.93 | -3.16 |
| MES | 15 | h16 | bottom fifth | long | 68432 | +0.047 | 0.167 | +1.02 | -2.48 | -2.20 | -2.74 | -2.62 |
| MES | 15 | eod | top fifth | long | 68431 | +0.221 | 0.194 | +2.98 | -0.52 | -0.41 | -0.62 | -3.23 |
| MES | 60 | h1 | top fifth | long | 16670 | +0.014 | 0.102 | +0.41 | -3.09 | -3.25 | -2.94 | -3.30 |
| MES | 60 | h2 | top fifth | long | 16670 | +0.027 | 0.102 | +0.74 | -2.76 | -3.00 | -2.53 | -3.20 |
| MES | 60 | h4 | top fifth | long | 16670 | +0.048 | 0.102 | +1.27 | -2.23 | -2.70 | -1.79 | -3.08 |
| MES | 60 | h8 | top fifth | long | 16670 | +0.067 | 0.102 | +2.20 | -1.30 | -2.00 | -0.67 | -2.83 |
| MES | 60 | h16 | bottom fifth | long | 16671 | +0.066 | 0.083 | +2.01 | -1.49 | -0.40 | -2.52 | -3.76 |
| MES | 60 | eod | bottom fifth | long | 16671 | +0.097 | 0.083 | +3.82 | +0.32 | -0.00 | +0.63 | -2.85 |
| MNQ | 5 | h1 | top fifth | long | 206892 | +0.005 | 0.141 | +0.04 | -1.96 | -1.99 | -1.92 | -1.96 |
| MNQ | 5 | h2 | top fifth | long | 206892 | +0.011 | 0.141 | +0.12 | -1.88 | -1.96 | -1.79 | -1.89 |
| MNQ | 5 | h4 | top fifth | long | 206892 | +0.024 | 0.141 | +0.30 | -1.70 | -1.92 | -1.46 | -1.78 |
| MNQ | 5 | h8 | bottom fifth | long | 206892 | +0.022 | 0.123 | +0.13 | -1.87 | -1.92 | -1.81 | -1.81 |
| MNQ | 5 | h16 | bottom fifth | long | 206892 | +0.059 | 0.123 | +0.25 | -1.75 | -1.74 | -1.76 | -1.81 |
| MNQ | 5 | eod | bottom fifth | long | 206892 | +0.385 | 0.123 | +2.23 | +0.23 | +0.95 | -0.54 | +4.78 |
| MNQ | 15 | h1 | top fifth | long | 68400 | +0.009 | 0.082 | +0.18 | -1.82 | -1.93 | -1.71 | -1.87 |
| MNQ | 15 | h2 | top fifth | long | 68400 | +0.016 | 0.082 | +0.36 | -1.64 | -1.86 | -1.42 | -1.75 |
| MNQ | 15 | h4 | top fifth | long | 68400 | +0.033 | 0.082 | +0.78 | -1.22 | -1.65 | -0.77 | -1.51 |
| MNQ | 15 | h8 | top fifth | long | 68400 | +0.055 | 0.082 | +1.15 | -0.85 | -1.37 | -0.32 | -1.59 |
| MNQ | 15 | h16 | top fifth | long | 68400 | +0.096 | 0.082 | +2.08 | +0.08 | -1.00 | +1.19 | -1.24 |
| MNQ | 15 | eod | top fifth | long | 68400 | +0.393 | 0.082 | +3.98 | +1.98 | +1.08 | +2.90 | -1.67 |
| MNQ | 60 | h1 | top fifth | long | 16670 | +0.022 | 0.042 | +1.12 | -0.88 | -1.69 | -0.08 | -1.42 |
| MNQ | 60 | h2 | top fifth | long | 16670 | +0.035 | 0.042 | +1.69 | -0.31 | -1.43 | +0.80 | -1.30 |
| MNQ | 60 | h4 | top fifth | long | 16670 | +0.068 | 0.042 | +3.06 | +1.06 | -0.89 | +3.00 | -0.72 |
| MNQ | 60 | h8 | top fifth | long | 16670 | +0.084 | 0.042 | +3.16 | +1.16 | -0.48 | +2.78 | -1.45 |
| MNQ | 60 | h16 | bottom fifth | long | 16670 | +0.097 | 0.032 | +4.56 | +2.56 | +0.84 | +4.19 | +0.30 |
| MNQ | 60 | eod | bottom fifth | long | 16670 | +0.138 | 0.032 | +7.64 | +5.64 | +1.48 | +9.60 | +2.38 |
| MYM | 5 | h1 | bottom fifth | long | 103802 | +0.003 | 0.159 | +0.07 | -1.93 | +nan | -1.93 | -1.95 |
| MYM | 5 | h2 | bottom fifth | long | 103802 | +0.003 | 0.159 | +0.08 | -1.92 | +nan | -1.92 | -1.89 |
| MYM | 5 | h4 | bottom fifth | long | 103802 | -0.005 | 0.159 | +0.08 | -1.92 | +nan | -1.92 | -1.76 |
| MYM | 5 | h8 | top fifth | short | 103802 | +0.036 | 0.176 | +0.12 | -1.88 | +nan | -1.88 | -1.68 |
| MYM | 5 | h16 | top fifth | short | 103802 | +0.050 | 0.176 | +0.32 | -1.68 | +nan | -1.68 | -1.28 |
| MYM | 5 | eod | top fifth | long | 103802 | +0.234 | 0.176 | +3.23 | +1.23 | +nan | +1.23 | -1.00 |
| MYM | 15 | h1 | bottom fifth | long | 34280 | +0.002 | 0.088 | +0.15 | -1.85 | +nan | -1.85 | -1.86 |
| MYM | 15 | h2 | top fifth | long | 34279 | -0.002 | 0.102 | -0.08 | -2.08 | +nan | -2.08 | -2.13 |
| MYM | 15 | h4 | top fifth | long | 34279 | +0.001 | 0.102 | -0.10 | -2.10 | +nan | -2.10 | -2.28 |
| MYM | 15 | h8 | top fifth | long | 34279 | +0.008 | 0.102 | -0.03 | -2.03 | +nan | -2.03 | -2.30 |
| MYM | 15 | h16 | top fifth | long | 34279 | +0.028 | 0.102 | +0.37 | -1.63 | +nan | -1.63 | -2.01 |
| MYM | 15 | eod | top fifth | long | 34279 | +0.183 | 0.102 | +3.47 | +1.47 | +nan | +1.47 | +0.09 |
| MYM | 60 | h1 | top fifth | long | 8325 | +0.014 | 0.052 | +0.31 | -1.69 | +nan | -1.69 | -1.92 |
| MYM | 60 | h2 | top fifth | long | 8325 | +0.020 | 0.052 | +0.50 | -1.50 | +nan | -1.50 | -1.94 |
| MYM | 60 | h4 | top fifth | long | 8325 | +0.047 | 0.052 | +1.13 | -0.87 | +nan | -0.87 | -1.81 |
| MYM | 60 | h8 | top fifth | long | 8325 | +0.094 | 0.052 | +2.60 | +0.60 | +nan | +0.60 | -0.99 |
| MYM | 60 | h16 | top fifth | long | 8325 | +0.137 | 0.052 | +3.78 | +1.78 | +nan | +1.78 | -1.00 |
| MYM | 60 | eod | top fifth | long | 8325 | +0.145 | 0.052 | +3.79 | +1.79 | +nan | +1.79 | -1.52 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -3.107 | -2.818 | -2.012 | -1.251 | -0.717 | +0.000 | -0.036 | -0.043 | -0.043 | -0.063 | -0.084 |
| MES | 15 | -3.207 | -2.872 | -2.084 | -1.298 | -0.737 | +0.000 | -0.014 | -0.018 | -0.029 | -0.033 | -0.053 |
| MES | 60 | -3.782 | -3.276 | -2.309 | -1.409 | -0.791 | +0.000 | +0.004 | +0.009 | -0.003 | -0.031 | -0.096 |
| MNQ | 5 | -3.439 | -3.097 | -2.204 | -1.365 | -0.776 | +0.000 | -0.014 | -0.016 | -0.008 | -0.016 | -0.027 |
| MNQ | 15 | -3.453 | -3.035 | -2.188 | -1.366 | -0.777 | +0.000 | +0.003 | +0.010 | +0.022 | +0.013 | +0.031 |
| MNQ | 60 | -3.986 | -3.449 | -2.408 | -1.456 | -0.821 | +0.000 | +0.006 | +0.005 | +0.002 | -0.047 | -0.045 |
| MYM | 5 | -3.330 | -3.019 | -2.160 | -1.335 | -0.757 | +0.000 | -0.016 | -0.026 | -0.037 | -0.057 | -0.114 |
| MYM | 15 | -3.345 | -2.995 | -2.175 | -1.359 | -0.770 | +0.000 | +0.010 | +0.026 | +0.056 | +0.097 | +0.247 |
| MYM | 60 | -3.884 | -3.395 | -2.399 | -1.470 | -0.819 | +0.000 | +0.018 | +0.016 | +0.050 | +0.071 | +0.061 |

## Calibration

- MES 5-min: 1036209 bars, 207242 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342156 bars, 68431 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83351 bars, 16670 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034460 bars, 206892 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342000 bars, 68400 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83349 bars, 16670 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519008 bars, 103802 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171396 bars, 34279 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41624 bars, 8325 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
