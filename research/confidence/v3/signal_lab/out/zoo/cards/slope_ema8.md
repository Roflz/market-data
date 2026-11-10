# Impact card: slope_ema8

5-bar change of EMA8 in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.005 R20 over the next 1 bar (5 min), p=0.13; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.039 R20, CONFIRMED, q=1.75e-40, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.34 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.217 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.010 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.046 R20, CONFIRMED, q=2.15e-20, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.95 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.124 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.086 R20 or more 80% of the time).
- MES 60-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.054 R20, CONFIRMED, q=4.1e-09, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.18 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (5 min), p=0.26; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.037 R20, CONFIRMED, q=3.02e-32, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.07 at recent bar sizes, 90% range up to $0.40); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.175 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.056 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.041 R20, CONFIRMED, q=3.67e-14, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.05 at recent bar sizes, 90% range up to $1.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.016 R20 over the next 1 bar (1 h), p=0.76; we would catch an effect of 0.092 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.046 R20, CONFIRMED, q=1.43e-06, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.71 at recent bar sizes, 90% range up to $4.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.068 R20 over the next 16 bars (80 min), p=0.52; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.042 R20, CONFIRMED, q=2.3e-15, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.48 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.168 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.049 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MYM 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.044 R20, CONFIRMED, q=7.57e-07, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.54 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.093 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.015 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.126 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.052 R20, CONFIRMED, q=0.00134, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $3.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.005 | -0.009 .. -0.001 | -0.0009 | 0.016 / 0.021 / 0.033 | 0.032 | 1 | 0.96 | 12/16 | -0.008 | -0.002 | False | -2.1 / -2.4 |  |
| MES | 5 | h2 | -0.007 | -0.014 .. +0.001 | -0.0004 | 0.09 / 0.093 / 0.14 | 0.134 |  |  | 11/16 | -0.015 | +0.002 |  | -2.0 / -1.7 |  |
| MES | 5 | h4 | -0.010 | -0.025 .. +0.005 | -0.0003 | 0.19 / 0.19 / 0.25 | 0.248 |  |  | 11/16 | -0.031 | +0.011 |  | -2.2 / -1.3 | 0.023 |
| MES | 5 | h8 | -0.019 | -0.047 .. +0.009 | -0.0025 | 0.18 / 0.17 / 0.23 | 0.216 |  |  | 12/16 | -0.060 | +0.021 |  | -2.9 / -1.4 |  |
| MES | 5 | h16 | -0.026 | -0.073 .. +0.022 | -0.0024 | 0.29 / 0.27 / 0.32 | 0.319 |  |  | 11/16 | -0.084 | +0.032 |  | -2.6 / -1.1 |  |
| MES | 5 | eod | -0.127 | -0.373 .. +0.118 | -0.0035 | 0.31 / 0.32 / 0.36 | 0.364 |  |  | 10/16 | -0.149 | -0.106 |  | -2.7 / -1.0 |  |
| MES | 15 | h1 | -0.004 | -0.013 .. +0.005 | -0.0022 | 0.4 / 0.37 / 0.37 | 0.363 |  |  | 10/16 | -0.012 | +0.004 |  | -0.9 / -0.8 |  |
| MES | 15 | h2 * | -0.010 | -0.027 .. +0.007 | -0.0023 | 0.24 / 0.22 / 0.24 | 0.239 | 1 | 1 | 10/16 | -0.024 | +0.003 | False | -1.6 / -1.2 |  |
| MES | 15 | h4 | -0.015 | -0.047 .. +0.017 | -0.0035 | 0.35 / 0.33 / 0.36 | 0.341 |  |  | 11/16 | -0.038 | +0.008 |  | -1.7 / -0.9 | 0.046 |
| MES | 15 | h8 | -0.022 | -0.076 .. +0.031 | -0.0045 | 0.41 / 0.39 / 0.44 | 0.428 |  |  | 11/16 | -0.061 | +0.016 |  | -1.7 / -0.8 |  |
| MES | 15 | h16 | -0.036 | -0.119 .. +0.047 | -0.0031 | 0.4 / 0.39 / 0.47 | 0.454 |  |  | 8/16 | -0.115 | +0.043 |  | -2.0 / -0.8 |  |
| MES | 15 | eod | +0.009 | -0.237 .. +0.254 | +0.0008 | 0.94 / 0.94 / 0.95 | 0.955 |  |  | 7/16 | -0.071 | +0.088 |  | +0.2 / +0.1 |  |
| MES | 60 | h1 * | -0.002 | -0.018 .. +0.014 | +0.0048 | 0.78 / 0.79 / 0.8 | 0.793 | 1 | 1 | 10/16 | -0.005 | +0.000 | False | -0.3 / -0.3 |  |
| MES | 60 | h2 | -0.001 | -0.031 .. +0.029 | +0.0043 | 0.93 / 0.93 / 0.94 | 0.936 |  |  | 12/16 | -0.009 | +0.006 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | +0.000 | -0.055 .. +0.055 | +0.0053 | 1 / 1 / 1 | 0.997 |  |  | 6/16 | -0.015 | +0.015 |  | +0.0 / +0.0 | 0.086 |
| MES | 60 | h8 | +0.002 | -0.089 .. +0.092 | +0.0028 | 0.97 / 0.97 / 0.97 | 0.976 |  |  | 8/16 | -0.040 | +0.044 |  | +0.1 / +0.0 |  |
| MES | 60 | h16 | -0.023 | -0.160 .. +0.115 | -0.0009 | 0.75 / 0.74 / 0.77 | 0.772 |  |  | 8/16 | -0.120 | +0.075 |  | -0.8 / -0.3 |  |
| MES | 60 | eod | -0.046 | -0.194 .. +0.102 | -0.0035 | 0.55 / 0.55 / 0.59 | 0.59 |  |  | 10/16 | -0.114 | +0.023 |  | -1.5 / -0.6 |  |
| MNQ | 5 | h1 * | +0.006 | +0.001 .. +0.010 | +0.0048 | 0.02 / 0.025 / 0.048 | 0.0461 | 1 | 0.986 | 12/16 | +0.000 | +0.011 | False | +2.1 / +2.3 |  |
| MNQ | 5 | h2 | +0.008 | -0.000 .. +0.017 | +0.0037 | 0.057 / 0.06 / 0.16 | 0.155 |  |  | 11/16 | -0.003 | +0.019 |  | +2.3 / +1.9 |  |
| MNQ | 5 | h4 | +0.010 | -0.007 .. +0.027 | +0.0040 | 0.25 / 0.25 / 0.38 | 0.38 |  |  | 8/16 | -0.014 | +0.033 |  | +1.9 / +1.1 | 0.030 |
| MNQ | 5 | h8 | -0.002 | -0.035 .. +0.031 | +0.0011 | 0.89 / 0.89 / 0.91 | 0.919 |  |  | 9/16 | -0.037 | +0.032 |  | -0.3 / -0.1 |  |
| MNQ | 5 | h16 | +0.004 | -0.055 .. +0.062 | +0.0005 | 0.91 / 0.9 / 0.92 | 0.91 |  |  | 6/16 | -0.052 | +0.059 |  | +0.3 / +0.1 |  |
| MNQ | 5 | eod | -0.270 | -0.606 .. +0.066 | -0.0043 | 0.12 / 0.12 / 0.16 | 0.156 |  |  | 9/16 | -0.418 | -0.124 |  | -4.2 / -1.6 |  |
| MNQ | 15 | h1 | +0.004 | -0.005 .. +0.013 | +0.0029 | 0.37 / 0.38 / 0.5 | 0.507 |  |  | 9/16 | -0.000 | +0.008 |  | +0.8 / +0.9 |  |
| MNQ | 15 | h2 | +0.006 | -0.011 .. +0.023 | +0.0024 | 0.51 / 0.52 / 0.65 | 0.655 |  |  | 8/16 | -0.004 | +0.016 |  | +0.8 / +0.7 |  |
| MNQ | 15 | h4 | +0.000 | -0.035 .. +0.036 | +0.0002 | 0.98 / 0.98 / 0.99 | 0.987 |  |  | 8/16 | -0.018 | +0.019 |  | +0.0 / +0.0 | 0.056 |
| MNQ | 15 | h8 | -0.021 | -0.085 .. +0.043 | -0.0027 | 0.52 / 0.52 / 0.61 | 0.604 |  |  | 8/16 | -0.050 | +0.009 |  | -1.3 / -0.6 |  |
| MNQ | 15 | h16 | -0.034 | -0.127 .. +0.059 | -0.0029 | 0.48 / 0.48 / 0.58 | 0.58 |  |  | 7/16 | -0.120 | +0.052 |  | -1.6 / -0.7 |  |
| MNQ | 15 | eod * | +0.175 | -0.168 .. +0.518 | +0.0062 | 0.32 / 0.31 / 0.36 | 0.373 | 1 | 1 | 7/16 | -0.035 | +0.383 | False | +2.7 / +1.0 |  |
| MNQ | 60 | h1 * | +0.016 | -0.002 .. +0.033 | +0.0050 | 0.086 / 0.088 / 0.11 | 0.105 | 1 | 1 | 11/16 | +0.004 | +0.027 | False | +1.6 / +1.7 |  |
| MNQ | 60 | h2 | +0.017 | -0.016 .. +0.049 | +0.0053 | 0.32 / 0.34 / 0.37 | 0.378 |  |  | 9/16 | -0.002 | +0.036 |  | +1.2 / +1.0 |  |
| MNQ | 60 | h4 | +0.023 | -0.035 .. +0.081 | +0.0058 | 0.43 / 0.45 / 0.48 | 0.478 |  |  | 10/16 | -0.006 | +0.053 |  | +1.3 / +0.8 | 0.092 |
| MNQ | 60 | h8 | +0.026 | -0.064 .. +0.117 | +0.0057 | 0.57 / 0.58 / 0.61 | 0.616 |  |  | 8/16 | -0.006 | +0.059 |  | +1.1 / +0.6 |  |
| MNQ | 60 | h16 | +0.002 | -0.139 .. +0.143 | +0.0006 | 0.98 / 0.98 / 0.97 | 0.976 |  |  | 8/16 | -0.018 | +0.023 |  | +0.1 / +0.0 |  |
| MNQ | 60 | eod | -0.045 | -0.199 .. +0.109 | -0.0047 | 0.57 / 0.58 / 0.61 | 0.617 |  |  | 10/16 | -0.032 | -0.058 |  | -1.4 / -0.6 |  |
| MYM | 5 | h1 | -0.003 | -0.012 .. +0.006 | +0.0009 | 0.47 / 0.46 / 0.46 | 0.471 |  |  | 4/8 | n/a | -0.003 |  | -0.7 / -0.7 |  |
| MYM | 5 | h2 | -0.012 | -0.025 .. +0.001 | -0.0026 | 0.072 / 0.061 / 0.2 | 0.199 |  |  | 6/8 | n/a | -0.012 |  | -2.4 / -1.8 |  |
| MYM | 5 | h4 | -0.024 | -0.049 .. +0.001 | -0.0027 | 0.06 / 0.048 / 0.21 | 0.214 |  |  | 6/8 | n/a | -0.024 |  | -3.2 / -1.9 | 0.048 |
| MYM | 5 | h8 | -0.044 | -0.088 .. -0.000 | -0.0049 | 0.048 / 0.045 / 0.14 | 0.153 |  |  | 6/8 | n/a | -0.044 |  | -4.1 / -2.0 |  |
| MYM | 5 | h16 * | -0.068 | -0.135 .. -0.001 | -0.0063 | 0.048 / 0.058 / 0.15 | 0.152 | 1 | 1 | 6/8 | n/a | -0.068 | False | -4.4 / -2.0 |  |
| MYM | 5 | eod | -0.132 | -0.588 .. +0.324 | -0.0030 | 0.57 / 0.58 / 0.59 | 0.6 |  |  | 5/8 | n/a | -0.132 |  | -1.6 / -0.6 |  |
| MYM | 15 | h1 | -0.004 | -0.016 .. +0.009 | +0.0020 | 0.59 / 0.6 / 0.65 | 0.654 |  |  | 5/8 | n/a | -0.004 |  | -0.5 / -0.5 |  |
| MYM | 15 | h2 | -0.011 | -0.032 .. +0.011 | -0.0000 | 0.33 / 0.36 / 0.54 | 0.55 |  |  | 5/8 | n/a | -0.011 |  | -1.1 / -1.0 |  |
| MYM | 15 | h4 | -0.029 | -0.072 .. +0.014 | -0.0032 | 0.18 / 0.21 / 0.36 | 0.366 |  |  | 6/8 | n/a | -0.029 |  | -2.1 / -1.3 | 0.077 |
| MYM | 15 | h8 * | -0.049 | -0.126 .. +0.028 | -0.0045 | 0.21 / 0.24 / 0.39 | 0.399 | 1 | 1 | 6/8 | n/a | -0.049 | False | -2.5 / -1.3 |  |
| MYM | 15 | h16 | -0.036 | -0.162 .. +0.089 | -0.0001 | 0.57 / 0.59 / 0.71 | 0.692 |  |  | 4/8 | n/a | -0.036 |  | -1.2 / -0.6 |  |
| MYM | 15 | eod | +0.152 | -0.315 .. +0.619 | +0.0042 | 0.52 / 0.54 / 0.55 | 0.57 |  |  | 4/8 | n/a | +0.152 |  | +1.8 / +0.6 |  |
| MYM | 60 | h1 * | +0.015 | -0.009 .. +0.039 | +0.0044 | 0.21 / 0.24 / 0.27 | 0.264 | 1 | 1 | 7/8 | n/a | +0.015 | False | +1.1 / +1.2 |  |
| MYM | 60 | h2 | +0.014 | -0.033 .. +0.061 | +0.0038 | 0.56 / 0.57 / 0.59 | 0.585 |  |  | 7/8 | n/a | +0.014 |  | +0.7 / +0.6 |  |
| MYM | 60 | h4 | +0.004 | -0.081 .. +0.088 | +0.0052 | 0.93 / 0.93 / 0.93 | 0.929 |  |  | 6/8 | n/a | +0.004 |  | +0.2 / +0.1 | 0.126 |
| MYM | 60 | h8 | +0.056 | -0.083 .. +0.195 | +0.0092 | 0.43 / 0.43 / 0.43 | 0.428 |  |  | 5/8 | n/a | +0.056 |  | +1.7 / +0.8 |  |
| MYM | 60 | h16 | +0.096 | -0.111 .. +0.304 | +0.0079 | 0.36 / 0.35 / 0.37 | 0.368 |  |  | 5/8 | n/a | +0.096 |  | +2.2 / +0.9 |  |
| MYM | 60 | eod | +0.079 | -0.147 .. +0.305 | +0.0063 | 0.49 / 0.48 / 0.5 | 0.489 |  |  | 5/8 | n/a | +0.079 |  | +1.7 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.039 | -0.045 .. -0.034 | -7.8% | -0.074 | 1.9e-43 | 1.75e-40 | 16/16 |
| MES | 5 | h2 | -0.050 | -0.058 .. -0.042 | -7.1% | -0.101 | 3.1e-31 |  | 15/16 |
| MES | 5 | h4 | -0.063 | -0.077 .. -0.049 | -6.3% | -0.135 | 3.5e-18 |  | 15/16 |
| MES | 5 | h8 | -0.082 | -0.104 .. -0.060 | -5.7% | -0.175 | 4.6e-13 |  | 14/16 |
| MES | 5 | h16 | -0.098 | -0.132 .. -0.064 | -4.7% | -0.198 | 1.4e-08 |  | 14/16 |
| MES | 5 | eod | -0.259 | -0.425 .. -0.093 | -2.6% | -0.426 | 0.0024 |  | 12/16 |
| MES | 15 | h1 * | -0.046 | -0.055 .. -0.037 | -8.9% | -0.096 | 3.6e-23 | 2.15e-20 | 15/16 |
| MES | 15 | h2 | -0.056 | -0.070 .. -0.042 | -7.6% | -0.117 | 3.3e-15 |  | 15/16 |
| MES | 15 | h4 | -0.063 | -0.086 .. -0.041 | -6.0% | -0.134 | 1.6e-07 |  | 13/16 |
| MES | 15 | h8 | -0.071 | -0.107 .. -0.035 | -4.6% | -0.137 | 0.0001 |  | 12/16 |
| MES | 15 | h16 | -0.061 | -0.121 .. -0.001 | -2.7% | -0.108 | 0.045 |  | 10/16 |
| MES | 15 | eod | -0.061 | -0.211 .. +0.089 | -1.1% | -0.119 | 0.42 |  | 9/16 |
| MES | 60 | h1 * | -0.054 | -0.069 .. -0.038 | -10.5% | -0.130 | 1.2e-11 | 4.1e-09 | 13/16 |
| MES | 60 | h2 | -0.069 | -0.092 .. -0.045 | -9.3% | -0.164 | 8.7e-09 |  | 12/16 |
| MES | 60 | h4 | -0.099 | -0.137 .. -0.060 | -9.3% | -0.202 | 4.9e-07 |  | 12/16 |
| MES | 60 | h8 | -0.104 | -0.161 .. -0.047 | -6.9% | -0.232 | 0.00038 |  | 13/16 |
| MES | 60 | h16 | -0.090 | -0.173 .. -0.007 | -4.4% | -0.244 | 0.033 |  | 10/16 |
| MES | 60 | eod | -0.094 | -0.190 .. +0.003 | -4.3% | -0.252 | 0.057 |  | 10/16 |
| MNQ | 5 | h1 * | -0.037 | -0.042 .. -0.031 | -6.9% | -0.072 | 3.7e-35 | 3.02e-32 | 15/16 |
| MNQ | 5 | h2 | -0.045 | -0.054 .. -0.037 | -5.9% | -0.096 | 7e-22 |  | 15/16 |
| MNQ | 5 | h4 | -0.057 | -0.072 .. -0.042 | -5.1% | -0.127 | 1.8e-12 |  | 14/16 |
| MNQ | 5 | h8 | -0.072 | -0.097 .. -0.046 | -4.4% | -0.158 | 3.8e-07 |  | 13/16 |
| MNQ | 5 | h16 | -0.082 | -0.122 .. -0.042 | -3.4% | -0.160 | 0.00084 |  | 14/16 |
| MNQ | 5 | eod | -0.233 | -0.447 .. -0.019 | -1.9% | -0.371 | 0.038 |  | 11/16 |
| MNQ | 15 | h1 * | -0.041 | -0.050 .. -0.032 | -7.6% | -0.090 | 8.1e-17 | 3.67e-14 | 14/16 |
| MNQ | 15 | h2 | -0.050 | -0.064 .. -0.035 | -6.4% | -0.111 | 1.6e-05 |  | 14/16 |
| MNQ | 15 | h4 | -0.045 | -0.070 .. -0.019 | -3.9% | -0.119 | 0.05 |  | 14/16 |
| MNQ | 15 | h8 | -0.039 | -0.087 .. +0.009 | -2.3% | -0.118 | 0.16 |  | 11/16 |
| MNQ | 15 | h16 | -0.006 | -0.075 .. +0.063 | -0.2% | -0.093 | 0.86 |  | 8/16 |
| MNQ | 15 | eod | -0.155 | -0.450 .. +0.140 | -2.4% | -0.207 | 0.31 |  | 9/16 |
| MNQ | 60 | h1 * | -0.046 | -0.061 .. -0.030 | -8.7% | -0.117 | 4.9e-09 | 1.43e-06 | 14/16 |
| MNQ | 60 | h2 | -0.059 | -0.083 .. -0.034 | -7.7% | -0.148 | 2e-06 |  | 13/16 |
| MNQ | 60 | h4 | -0.083 | -0.122 .. -0.044 | -7.5% | -0.182 | 2.6e-05 |  | 12/16 |
| MNQ | 60 | h8 | -0.110 | -0.166 .. -0.053 | -6.9% | -0.237 | 0.00016 |  | 13/16 |
| MNQ | 60 | h16 | -0.146 | -0.232 .. -0.061 | -6.7% | -0.313 | 0.00083 |  | 14/16 |
| MNQ | 60 | eod | -0.131 | -0.227 .. -0.034 | -5.7% | -0.312 | 0.0078 |  | 12/16 |
| MYM | 5 | h1 * | -0.042 | -0.052 .. -0.033 | -7.9% | -0.078 | 4.8e-18 | 2.3e-15 | 8/8 |
| MYM | 5 | h2 | -0.049 | -0.061 .. -0.037 | -6.4% | -0.100 | 3e-14 |  | 7/8 |
| MYM | 5 | h4 | -0.057 | -0.078 .. -0.037 | -5.2% | -0.122 | 8.3e-06 |  | 7/8 |
| MYM | 5 | h8 | -0.064 | -0.097 .. -0.031 | -4.0% | -0.131 | 0.0013 |  | 7/8 |
| MYM | 5 | h16 | -0.068 | -0.121 .. -0.016 | -2.9% | -0.123 | 0.039 |  | 6/8 |
| MYM | 5 | eod | -0.342 | -0.666 .. -0.017 | -2.9% | -0.507 | 0.039 |  | 7/8 |
| MYM | 15 | h1 * | -0.044 | -0.059 .. -0.030 | -8.3% | -0.096 | 2.6e-09 | 7.57e-07 | 8/8 |
| MYM | 15 | h2 | -0.055 | -0.074 .. -0.035 | -7.2% | -0.118 | 6.4e-06 |  | 8/8 |
| MYM | 15 | h4 | -0.059 | -0.091 .. -0.026 | -5.3% | -0.132 | 0.0083 |  | 7/8 |
| MYM | 15 | h8 | -0.088 | -0.144 .. -0.033 | -5.4% | -0.175 | 0.049 |  | 7/8 |
| MYM | 15 | h16 | -0.103 | -0.197 .. -0.009 | -4.2% | -0.192 | 0.17 |  | 6/8 |
| MYM | 15 | eod | -0.243 | -0.619 .. +0.133 | -4.0% | -0.436 | 0.23 |  | 6/8 |
| MYM | 60 | h1 * | -0.052 | -0.075 .. -0.030 | -10.0% | -0.116 | 5.6e-06 | 0.00134 | 7/8 |
| MYM | 60 | h2 | -0.066 | -0.101 .. -0.030 | -8.7% | -0.149 | 0.00028 |  | 7/8 |
| MYM | 60 | h4 | -0.094 | -0.151 .. -0.036 | -8.7% | -0.183 | 0.0014 |  | 7/8 |
| MYM | 60 | h8 | -0.073 | -0.161 .. +0.014 | -4.7% | -0.190 | 0.1 |  | 6/8 |
| MYM | 60 | h16 | -0.080 | -0.212 .. +0.052 | -3.8% | -0.200 | 0.24 |  | 5/8 |
| MYM | 60 | eod | -0.079 | -0.230 .. +0.073 | -3.5% | -0.217 | 0.32 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -1.06 pts | -1.52 .. -0.60 | 0.00017 |
| MES | 15 | -0.77 pts | -1.58 .. +0.04 | 0.063 |
| MES | 60 | +0.37 pts | -1.28 .. +2.01 | 0.66 |
| MNQ | 5 | -0.63 pts | -1.13 .. -0.12 | 0.023 |
| MNQ | 15 | -0.54 pts | -1.37 .. +0.29 | 0.2 |
| MNQ | 60 | +0.77 pts | -0.87 .. +2.41 | 0.36 |
| MYM | 5 | -0.63 pts | -1.27 .. +0.00 | 0.051 |
| MYM | 15 | -0.09 pts | -1.09 .. +0.91 | 0.86 |
| MYM | 60 | +1.28 pts | -0.88 .. +3.44 | 0.38 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207255 | +0.006 | 0.296 | +0.07 | -3.43 | -3.46 | -3.41 | -3.45 |
| MES | 5 | h2 | bottom fifth | long | 207255 | +0.008 | 0.296 | +0.09 | -3.41 | -3.44 | -3.39 | -3.45 |
| MES | 5 | h4 | bottom fifth | long | 207255 | +0.013 | 0.296 | +0.10 | -3.40 | -3.39 | -3.40 | -3.45 |
| MES | 5 | h8 | bottom fifth | long | 207255 | +0.022 | 0.296 | +0.18 | -3.32 | -3.27 | -3.36 | -3.43 |
| MES | 5 | h16 | bottom fifth | long | 207255 | +0.039 | 0.296 | +0.30 | -3.20 | -3.11 | -3.28 | -3.47 |
| MES | 5 | eod | bottom fifth | long | 207255 | +0.329 | 0.296 | +2.96 | -0.54 | -1.02 | -0.10 | -0.06 |
| MES | 15 | h1 | bottom fifth | long | 68444 | +0.004 | 0.171 | +0.04 | -3.46 | -3.48 | -3.44 | -3.55 |
| MES | 15 | h2 | bottom fifth | long | 68444 | +0.009 | 0.171 | +0.14 | -3.36 | -3.42 | -3.29 | -3.47 |
| MES | 15 | h4 | bottom fifth | long | 68444 | +0.020 | 0.171 | +0.31 | -3.19 | -3.22 | -3.17 | -3.38 |
| MES | 15 | h8 | bottom fifth | long | 68444 | +0.039 | 0.171 | +0.69 | -2.81 | -2.87 | -2.75 | -3.09 |
| MES | 15 | h16 | bottom fifth | long | 68444 | +0.065 | 0.171 | +1.15 | -2.35 | -2.31 | -2.38 | -2.49 |
| MES | 15 | eod | top fifth | long | 68444 | +0.245 | 0.188 | +3.77 | +0.27 | -0.07 | +0.59 | -2.22 |
| MES | 60 | h1 | bottom fifth | long | 16683 | +0.009 | 0.085 | +0.37 | -3.13 | -3.16 | -3.10 | -3.33 |
| MES | 60 | h2 | bottom fifth | long | 16683 | +0.014 | 0.085 | +0.61 | -2.89 | -2.81 | -2.97 | -3.33 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.028 | 0.098 | +0.62 | -2.88 | -2.40 | -3.33 | -3.63 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.039 | 0.098 | +1.28 | -2.22 | -1.89 | -2.52 | -3.69 |
| MES | 60 | h16 | bottom fifth | long | 16683 | +0.060 | 0.085 | +1.89 | -1.61 | -0.20 | -2.97 | -3.96 |
| MES | 60 | eod | bottom fifth | long | 16683 | +0.096 | 0.085 | +4.09 | +0.59 | +0.26 | +0.91 | -2.68 |
| MNQ | 5 | h1 | top fifth | long | 206905 | +0.007 | 0.137 | +0.05 | -1.95 | -1.99 | -1.89 | -1.96 |
| MNQ | 5 | h2 | top fifth | long | 206905 | +0.014 | 0.137 | +0.13 | -1.87 | -1.97 | -1.75 | -1.90 |
| MNQ | 5 | h4 | top fifth | long | 206905 | +0.023 | 0.137 | +0.28 | -1.72 | -1.95 | -1.48 | -1.80 |
| MNQ | 5 | h8 | bottom fifth | long | 206905 | +0.022 | 0.125 | +0.21 | -1.79 | -1.91 | -1.66 | -1.73 |
| MNQ | 5 | h16 | top fifth | long | 206905 | +0.068 | 0.137 | +0.78 | -1.22 | -1.65 | -0.76 | -1.66 |
| MNQ | 5 | eod | bottom fifth | long | 206905 | +0.553 | 0.125 | +3.27 | +1.27 | +0.54 | +2.04 | +5.22 |
| MNQ | 15 | h1 | top fifth | long | 68413 | +0.006 | 0.077 | +0.13 | -1.87 | -1.96 | -1.78 | -1.93 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.014 | 0.077 | +0.29 | -1.71 | -1.89 | -1.54 | -1.79 |
| MNQ | 15 | h4 | top fifth | long | 68413 | +0.028 | 0.077 | +0.61 | -1.39 | -1.71 | -1.07 | -1.61 |
| MNQ | 15 | h8 | bottom fifth | long | 68413 | +0.062 | 0.069 | +0.89 | -1.11 | -1.39 | -0.83 | -1.72 |
| MNQ | 15 | h16 | bottom fifth | long | 68413 | +0.087 | 0.069 | +0.84 | -1.16 | -0.81 | -1.52 | -1.17 |
| MNQ | 15 | eod | top fifth | long | 68413 | +0.426 | 0.077 | +6.16 | +4.16 | +1.13 | +7.25 | +1.56 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.019 | 0.039 | +0.74 | -1.26 | -1.69 | -0.83 | -1.71 |
| MNQ | 60 | h2 | top fifth | long | 16682 | +0.027 | 0.039 | +1.18 | -0.82 | -1.48 | -0.15 | -1.62 |
| MNQ | 60 | h4 | top fifth | long | 16682 | +0.049 | 0.039 | +1.93 | -0.07 | -1.07 | +0.92 | -1.58 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.072 | 0.039 | +2.24 | +0.24 | -0.56 | +1.05 | -2.01 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.108 | 0.039 | +2.02 | +0.02 | +0.28 | -0.23 | -2.70 |
| MNQ | 60 | eod | bottom fifth | long | 16683 | +0.137 | 0.033 | +7.42 | +5.42 | +2.27 | +8.40 | +1.45 |
| MYM | 5 | h1 | bottom fifth | long | 103808 | -0.001 | 0.163 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 5 | h2 | bottom fifth | long | 103808 | +0.002 | 0.163 | +0.05 | -1.95 | +nan | -1.95 | -1.89 |
| MYM | 5 | h4 | bottom fifth | long | 103808 | -0.004 | 0.163 | +0.02 | -1.98 | +nan | -1.98 | -1.80 |
| MYM | 5 | h8 | bottom fifth | long | 103808 | -0.016 | 0.163 | -0.03 | -2.03 | +nan | -2.03 | -1.73 |
| MYM | 5 | h16 | bottom fifth | long | 103808 | -0.016 | 0.163 | +0.08 | -1.92 | +nan | -1.92 | -1.60 |
| MYM | 5 | eod | bottom fifth | long | 103808 | +0.170 | 0.163 | +3.04 | +1.04 | +nan | +1.04 | +1.96 |
| MYM | 15 | h1 | top fifth | short | 34286 | +0.005 | 0.097 | +0.13 | -1.87 | +nan | -1.87 | -1.83 |
| MYM | 15 | h2 | top fifth | short | 34286 | +0.006 | 0.097 | +0.18 | -1.82 | +nan | -1.82 | -1.77 |
| MYM | 15 | h4 | bottom fifth | long | 34286 | +0.006 | 0.090 | +0.36 | -1.64 | +nan | -1.64 | -1.44 |
| MYM | 15 | h8 | bottom fifth | long | 34286 | +0.017 | 0.090 | +0.86 | -1.14 | +nan | -1.14 | -0.63 |
| MYM | 15 | h16 | bottom fifth | long | 34286 | -0.003 | 0.090 | +1.53 | -0.47 | +nan | -0.47 | +0.74 |
| MYM | 15 | eod | top fifth | long | 34286 | +0.139 | 0.097 | +3.28 | +1.28 | +nan | +1.28 | +1.01 |
| MYM | 60 | h1 | top fifth | long | 8331 | +0.015 | 0.049 | +0.33 | -1.67 | +nan | -1.67 | -1.84 |
| MYM | 60 | h2 | top fifth | long | 8331 | +0.021 | 0.049 | +0.38 | -1.62 | +nan | -1.62 | -2.01 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.027 | 0.049 | +0.61 | -1.39 | +nan | -1.39 | -2.22 |
| MYM | 60 | h8 | top fifth | long | 8331 | +0.083 | 0.049 | +2.67 | +0.67 | +nan | +0.67 | -0.83 |
| MYM | 60 | h16 | top fifth | long | 8331 | +0.127 | 0.049 | +4.46 | +2.46 | +nan | +2.46 | -0.03 |
| MYM | 60 | eod | top fifth | long | 8331 | +0.141 | 0.049 | +4.41 | +2.41 | +nan | +2.41 | -0.72 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -2.942 | -3.140 | -1.587 | -0.570 | -0.212 | +0.000 | -0.012 | -0.015 | -0.020 | -0.031 | -0.041 |
| MES | 15 | -3.018 | -3.182 | -1.651 | -0.601 | -0.224 | +0.000 | -0.010 | -0.018 | -0.025 | -0.035 | -0.066 |
| MES | 60 | -3.594 | -3.584 | -1.922 | -0.699 | -0.261 | +0.000 | -0.006 | -0.010 | -0.020 | -0.035 | -0.138 |
| MNQ | 5 | -3.263 | -3.457 | -1.757 | -0.638 | -0.240 | +0.000 | +0.000 | +0.002 | +0.004 | -0.008 | +0.005 |
| MNQ | 15 | -3.234 | -3.355 | -1.747 | -0.647 | -0.244 | +0.000 | +0.001 | +0.003 | -0.003 | -0.024 | -0.057 |
| MNQ | 60 | -3.816 | -3.794 | -2.043 | -0.755 | -0.286 | +0.000 | +0.011 | +0.007 | +0.000 | -0.047 | -0.084 |
| MYM | 5 | -3.162 | -3.377 | -1.710 | -0.615 | -0.228 | +0.000 | -0.007 | -0.016 | -0.028 | -0.046 | -0.074 |
| MYM | 15 | -3.149 | -3.319 | -1.746 | -0.650 | -0.247 | +0.000 | -0.003 | -0.009 | -0.021 | -0.035 | -0.026 |
| MYM | 60 | -3.657 | -3.689 | -1.987 | -0.727 | -0.277 | +0.000 | +0.014 | +0.008 | -0.013 | +0.083 | +0.101 |

## Calibration

- MES 5-min: 1036271 bars, 207254 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68444 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
