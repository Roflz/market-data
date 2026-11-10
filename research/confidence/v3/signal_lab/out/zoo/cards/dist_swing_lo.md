# Impact card: dist_swing_lo

(close - last swing low) in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=0.85; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.022 R20, CONFIRMED, q=1.2e-15, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.36 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.227 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.077 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.038 R20, CONFIRMED, q=7.62e-15, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.03 at recent bar sizes, 90% range up to $1.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.050 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.093 R20 or more 80% of the time).
- MES 60-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.043 R20, CONFIRMED, q=2.52e-06, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.86 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.064 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.084 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.031 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.027 R20, CONFIRMED, q=4.81e-15, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.09 at recent bar sizes, 90% range up to $1.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (15 min), p=0.3; we would catch an effect of 0.055 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.040 R20, CONFIRMED, q=3.83e-17, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.21 at recent bar sizes, 90% range up to $2.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.010 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.098 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.052 R20, CONFIRMED, q=6.93e-10, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.44 at recent bar sizes, 90% range up to $6.51); about 16760.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.038 R20, CONFIRMED, q=2.33e-06, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.69 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.171 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.252 R20 over the next 16 bars (4 h), p=0.83; we would catch an effect of 0.095 R20 or more 80% of the time).
- MYM 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.048 R20, CONFIRMED, q=4.74e-07, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.62 at recent bar sizes, 90% range up to $2.89); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.053 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.126 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.074).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.11 at recent bar sizes, 90% range up to $4.13); about 17.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.008 .. +0.001 | -0.0019 | 0.14 / 0.13 / 0.15 | 0.138 | 1 | 1 | 9/16 | -0.005 | -0.001 | False | -1.4 / -1.5 |  |
| MES | 5 | h2 | -0.003 | -0.012 .. +0.006 | -0.0025 | 0.52 / 0.51 / 0.52 | 0.518 |  |  | 9/16 | -0.009 | +0.003 |  | -0.8 / -0.6 |  |
| MES | 5 | h4 | -0.005 | -0.023 .. +0.013 | -0.0025 | 0.57 / 0.56 / 0.56 | 0.564 |  |  | 10/16 | -0.018 | +0.008 |  | -1.0 / -0.6 | 0.024 |
| MES | 5 | h8 | -0.015 | -0.053 .. +0.023 | -0.0052 | 0.44 / 0.43 / 0.37 | 0.369 |  |  | 11/16 | -0.039 | +0.009 |  | -2.0 / -0.8 |  |
| MES | 5 | h16 | -0.020 | -0.092 .. +0.052 | -0.0059 | 0.58 / 0.58 / 0.53 | 0.53 |  |  | 10/16 | -0.070 | +0.029 |  | -1.9 / -0.6 |  |
| MES | 5 | eod | -0.225 | -0.801 .. +0.351 | -0.0102 | 0.44 / 0.46 / 0.42 | 0.411 |  |  | 10/16 | -0.108 | -0.341 |  | -4.3 / -0.8 |  |
| MES | 15 | h1 | -0.003 | -0.012 .. +0.007 | -0.0024 | 0.55 / 0.53 / 0.53 | 0.526 |  |  | 9/16 | -0.008 | +0.002 |  | -0.6 / -0.6 |  |
| MES | 15 | h2 | -0.007 | -0.026 .. +0.013 | -0.0044 | 0.5 / 0.48 / 0.42 | 0.419 |  |  | 9/16 | -0.020 | +0.006 |  | -1.0 / -0.7 |  |
| MES | 15 | h4 | -0.019 | -0.063 .. +0.024 | -0.0082 | 0.38 / 0.35 / 0.23 | 0.231 |  |  | 9/16 | -0.044 | +0.005 |  | -1.8 / -0.9 | 0.045 |
| MES | 15 | h8 | -0.038 | -0.109 .. +0.033 | -0.0087 | 0.29 / 0.27 / 0.21 | 0.218 |  |  | 10/16 | -0.085 | +0.009 |  | -2.6 / -1.1 |  |
| MES | 15 | h16 * | -0.077 | -0.197 .. +0.043 | -0.0101 | 0.21 / 0.21 / 0.19 | 0.186 | 1 | 1 | 9/16 | -0.174 | +0.020 | False | -3.8 / -1.3 |  |
| MES | 15 | eod | -0.260 | -0.779 .. +0.259 | -0.0205 | 0.33 / 0.32 / 0.22 | 0.223 |  |  | 11/16 | -0.112 | -0.407 |  | -4.7 / -1.0 |  |
| MES | 60 | h1 | -0.001 | -0.018 .. +0.017 | +0.0026 | 0.94 / 0.94 / 0.94 | 0.942 |  |  | 10/16 | -0.004 | +0.003 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 | -0.005 | -0.039 .. +0.029 | +0.0003 | 0.79 / 0.79 / 0.8 | 0.794 |  |  | 9/16 | -0.013 | +0.004 |  | -0.4 / -0.3 |  |
| MES | 60 | h4 | +0.002 | -0.062 .. +0.066 | +0.0002 | 0.96 / 0.96 / 0.96 | 0.958 |  |  | 8/16 | -0.024 | +0.028 |  | +0.1 / +0.1 | 0.093 |
| MES | 60 | h8 | -0.009 | -0.123 .. +0.106 | -0.0046 | 0.88 / 0.88 / 0.88 | 0.885 |  |  | 10/16 | -0.050 | +0.032 |  | -0.4 / -0.2 |  |
| MES | 60 | h16 | -0.029 | -0.206 .. +0.147 | -0.0060 | 0.74 / 0.74 / 0.76 | 0.759 |  |  | 9/16 | -0.125 | +0.066 |  | -1.0 / -0.3 |  |
| MES | 60 | eod * | -0.050 | -0.240 .. +0.141 | -0.0071 | 0.61 / 0.61 / 0.65 | 0.644 | 1 | 1 | 9/16 | -0.136 | +0.036 | False | -1.6 / -0.5 |  |
| MNQ | 5 | h1 | +0.001 | -0.006 .. +0.008 | -0.0007 | 0.72 / 0.72 / 0.61 | 0.601 |  |  | 9/16 | +0.001 | +0.001 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h2 | +0.002 | -0.012 .. +0.015 | -0.0011 | 0.82 / 0.82 / 0.76 | 0.76 |  |  | 10/16 | +0.002 | +0.002 |  | +0.3 / +0.2 |  |
| MNQ | 5 | h4 | -0.004 | -0.036 .. +0.028 | -0.0032 | 0.82 / 0.82 / 0.75 | 0.744 |  |  | 8/16 | +0.001 | -0.008 |  | -0.4 / -0.2 | 0.031 |
| MNQ | 5 | h8 | -0.033 | -0.116 .. +0.050 | -0.0103 | 0.43 / 0.43 / 0.12 | 0.127 |  |  | 8/16 | -0.014 | -0.053 |  | -2.5 / -0.8 |  |
| MNQ | 5 | h16 * | -0.084 | -0.256 .. +0.088 | -0.0165 | 0.34 / 0.33 / 0.031 | 0.031 | 1 | 1 | 8/16 | -0.038 | -0.129 | False | -4.6 / -1.0 |  |
| MNQ | 5 | eod | -0.252 | -0.988 .. +0.483 | -0.0094 | 0.5 / 0.52 / 0.41 | 0.406 |  |  | 10/16 | +0.043 | -0.546 |  | -3.2 / -0.7 |  |
| MNQ | 15 | h1 * | +0.009 | +0.000 .. +0.018 | +0.0023 | 0.044 / 0.049 / 0.037 | 0.0359 | 1 | 0.999 | 11/16 | -0.002 | +0.021 | False | +2.0 / +2.0 |  |
| MNQ | 15 | h2 | +0.002 | -0.027 .. +0.032 | -0.0058 | 0.89 / 0.89 / 0.83 | 0.825 |  |  | 9/16 | -0.006 | +0.010 |  | +0.2 / +0.1 |  |
| MNQ | 15 | h4 | -0.019 | -0.086 .. +0.049 | -0.0104 | 0.59 / 0.58 / 0.38 | 0.387 |  |  | 7/16 | -0.029 | -0.009 |  | -1.0 / -0.5 | 0.055 |
| MNQ | 15 | h8 | -0.044 | -0.146 .. +0.059 | -0.0117 | 0.4 / 0.4 / 0.26 | 0.256 |  |  | 9/16 | -0.077 | -0.011 |  | -1.8 / -0.8 |  |
| MNQ | 15 | h16 | -0.122 | -0.313 .. +0.069 | -0.0197 | 0.21 / 0.21 / 0.072 | 0.0748 |  |  | 10/16 | -0.169 | -0.076 |  | -4.2 / -1.3 |  |
| MNQ | 15 | eod | -0.262 | -1.050 .. +0.526 | -0.0268 | 0.51 / 0.52 / 0.3 | 0.296 |  |  | 9/16 | +0.172 | -0.694 |  | -2.9 / -0.7 |  |
| MNQ | 60 | h1 * | +0.010 | -0.010 .. +0.029 | +0.0082 | 0.33 / 0.33 / 0.32 | 0.317 | 1 | 1 | 10/16 | +0.010 | +0.010 | False | +1.0 / +1.0 |  |
| MNQ | 60 | h2 | +0.013 | -0.023 .. +0.050 | +0.0073 | 0.47 / 0.46 / 0.47 | 0.455 |  |  | 6/16 | +0.016 | +0.011 |  | +1.0 / +0.7 |  |
| MNQ | 60 | h4 | +0.020 | -0.045 .. +0.086 | +0.0062 | 0.54 / 0.54 / 0.55 | 0.549 |  |  | 9/16 | +0.017 | +0.024 |  | +1.1 / +0.6 | 0.098 |
| MNQ | 60 | h8 | +0.044 | -0.077 .. +0.164 | +0.0036 | 0.48 / 0.47 / 0.47 | 0.468 |  |  | 8/16 | +0.054 | +0.034 |  | +1.7 / +0.7 |  |
| MNQ | 60 | h16 | +0.025 | -0.173 .. +0.223 | +0.0027 | 0.8 / 0.8 / 0.8 | 0.797 |  |  | 8/16 | +0.051 | -0.001 |  | +0.8 / +0.2 |  |
| MNQ | 60 | eod | +0.003 | -0.211 .. +0.218 | -0.0002 | 0.98 / 0.97 / 0.97 | 0.969 |  |  | 8/16 | +0.056 | -0.049 |  | +0.1 / +0.0 |  |
| MYM | 5 | h1 | -0.003 | -0.012 .. +0.005 | +0.0002 | 0.44 / 0.43 / 0.45 | 0.456 |  |  | 6/8 | n/a | -0.003 |  | -0.6 / -0.8 |  |
| MYM | 5 | h2 * | -0.011 | -0.029 .. +0.007 | -0.0040 | 0.22 / 0.26 / 0.21 | 0.218 | 1 | 1 | 6/8 | n/a | -0.011 | False | -1.2 / -1.2 |  |
| MYM | 5 | h4 | -0.018 | -0.055 .. +0.019 | -0.0044 | 0.34 / 0.37 / 0.32 | 0.332 |  |  | 6/8 | n/a | -0.018 |  | -1.1 / -1.0 | 0.046 |
| MYM | 5 | h8 | -0.045 | -0.126 .. +0.036 | -0.0108 | 0.27 / 0.31 / 0.13 | 0.136 |  |  | 6/8 | n/a | -0.045 |  | -2.1 / -1.1 |  |
| MYM | 5 | h16 | -0.092 | -0.242 .. +0.059 | -0.0174 | 0.23 / 0.27 / 0.08 | 0.079 |  |  | 6/8 | n/a | -0.092 |  | -3.5 / -1.2 |  |
| MYM | 5 | eod | -0.317 | -1.191 .. +0.557 | -0.0174 | 0.48 / 0.5 / 0.38 | 0.385 |  |  | 5/8 | n/a | -0.317 |  | -3.0 / -0.7 |  |
| MYM | 15 | h1 | +0.000 | -0.014 .. +0.015 | +0.0063 | 0.97 / 0.97 / 0.97 | 0.974 |  |  | 3/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | h2 | -0.019 | -0.054 .. +0.015 | -0.0070 | 0.27 / 0.3 / 0.22 | 0.226 |  |  | 6/8 | n/a | -0.019 |  | -1.2 / -1.1 |  |
| MYM | 15 | h4 | -0.062 | -0.170 .. +0.046 | -0.0181 | 0.26 / 0.28 / 0.048 | 0.0464 |  |  | 6/8 | n/a | -0.062 |  | -2.1 / -1.1 | 0.095 |
| MYM | 15 | h8 | -0.125 | -0.304 .. +0.055 | -0.0248 | 0.17 / 0.18 / 0.03 | 0.0316 |  |  | 6/8 | n/a | -0.125 |  | -3.2 / -1.4 |  |
| MYM | 15 | h16 * | -0.252 | -0.585 .. +0.081 | -0.0354 | 0.14 / 0.14 / 0.013 | 0.0121 | 1 | 1 | 5/8 | n/a | -0.252 | False | -5.1 / -1.5 |  |
| MYM | 15 | eod | -0.692 | -1.667 .. +0.284 | -0.0439 | 0.16 / 0.19 / 0.031 | 0.0321 |  |  | 6/8 | n/a | -0.692 |  | -5.5 / -1.4 |  |
| MYM | 60 | h1 | -0.004 | -0.030 .. +0.023 | +0.0017 | 0.79 / 0.79 / 0.79 | 0.799 |  |  | 5/8 | n/a | -0.004 |  | -0.3 / -0.3 |  |
| MYM | 60 | h2 | -0.014 | -0.063 .. +0.035 | -0.0002 | 0.57 / 0.57 / 0.58 | 0.575 |  |  | 5/8 | n/a | -0.014 |  | -0.7 / -0.6 |  |
| MYM | 60 | h4 | -0.030 | -0.121 .. +0.061 | -0.0002 | 0.52 / 0.52 / 0.53 | 0.522 |  |  | 5/8 | n/a | -0.030 |  | -1.1 / -0.6 | 0.126 |
| MYM | 60 | h8 * | -0.053 | -0.219 .. +0.114 | -0.0030 | 0.54 / 0.52 / 0.54 | 0.545 | 1 | 1 | 6/8 | n/a | -0.053 | False | -1.5 / -0.6 |  |
| MYM | 60 | h16 | -0.020 | -0.283 .. +0.243 | -0.0026 | 0.88 / 0.87 / 0.89 | 0.883 |  |  | 5/8 | n/a | -0.020 |  | -0.5 / -0.2 |  |
| MYM | 60 | eod | -0.022 | -0.308 .. +0.264 | -0.0021 | 0.88 / 0.88 / 0.89 | 0.894 |  |  | 4/8 | n/a | -0.022 |  | -0.5 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.022 | -0.027 .. -0.017 | -4.4% | -0.051 | 2.4e-18 | 1.2e-15 | 14/16 |
| MES | 5 | h2 | -0.027 | -0.035 .. -0.019 | -3.8% | -0.066 | 3.7e-11 |  | 14/16 |
| MES | 5 | h4 | -0.032 | -0.047 .. -0.018 | -3.2% | -0.081 | 1.4e-05 |  | 14/16 |
| MES | 5 | h8 | -0.034 | -0.061 .. -0.007 | -2.4% | -0.090 | 0.013 |  | 12/16 |
| MES | 5 | h16 | -0.041 | -0.088 .. +0.006 | -1.9% | -0.094 | 0.09 |  | 11/16 |
| MES | 5 | eod | +0.199 | -0.277 .. +0.675 | +2.0% | -0.042 | 0.41 |  | 8/16 |
| MES | 15 | h1 * | -0.038 | -0.046 .. -0.029 | -7.4% | -0.083 | 1.6e-17 | 7.62e-15 | 14/16 |
| MES | 15 | h2 | -0.046 | -0.060 .. -0.031 | -6.2% | -0.101 | 8.8e-10 |  | 12/16 |
| MES | 15 | h4 | -0.049 | -0.074 .. -0.025 | -4.7% | -0.112 | 9.8e-05 |  | 12/16 |
| MES | 15 | h8 | -0.049 | -0.092 .. -0.005 | -3.2% | -0.106 | 0.03 |  | 12/16 |
| MES | 15 | h16 | -0.062 | -0.147 .. +0.022 | -2.7% | -0.100 | 0.15 |  | 9/16 |
| MES | 15 | eod | +0.178 | -0.245 .. +0.600 | +3.2% | +0.136 | 0.41 |  | 6/16 |
| MES | 60 | h1 * | -0.043 | -0.057 .. -0.028 | -8.3% | -0.092 | 8.9e-09 | 2.52e-06 | 14/16 |
| MES | 60 | h2 | -0.056 | -0.080 .. -0.033 | -7.6% | -0.118 | 2.6e-06 |  | 13/16 |
| MES | 60 | h4 | -0.074 | -0.116 .. -0.033 | -7.0% | -0.144 | 0.00049 |  | 12/16 |
| MES | 60 | h8 | -0.088 | -0.160 .. -0.016 | -5.8% | -0.184 | 0.017 |  | 12/16 |
| MES | 60 | h16 | -0.126 | -0.240 .. -0.013 | -6.1% | -0.263 | 0.029 |  | 12/16 |
| MES | 60 | eod | -0.113 | -0.240 .. +0.014 | -5.2% | -0.267 | 0.081 |  | 12/16 |
| MNQ | 5 | h1 * | -0.027 | -0.033 .. -0.021 | -5.1% | -0.064 | 1e-17 | 4.81e-15 | 15/16 |
| MNQ | 5 | h2 | -0.030 | -0.041 .. -0.019 | -3.9% | -0.076 | 4.9e-08 |  | 14/16 |
| MNQ | 5 | h4 | -0.034 | -0.056 .. -0.012 | -3.1% | -0.086 | 0.0027 |  | 14/16 |
| MNQ | 5 | h8 | -0.029 | -0.076 .. +0.018 | -1.8% | -0.082 | 0.23 |  | 12/16 |
| MNQ | 5 | h16 | -0.018 | -0.105 .. +0.069 | -0.8% | -0.053 | 0.71 |  | 10/16 |
| MNQ | 5 | eod | +0.326 | -0.299 .. +0.952 | +2.6% | +0.218 | 0.32 |  | 8/16 |
| MNQ | 15 | h1 * | -0.040 | -0.049 .. -0.031 | -7.5% | -0.074 | 7.3e-20 | 3.83e-17 | 14/16 |
| MNQ | 15 | h2 | -0.036 | -0.060 .. -0.012 | -4.6% | -0.079 | 0.0036 |  | 12/16 |
| MNQ | 15 | h4 | -0.008 | -0.080 .. +0.065 | -0.7% | -0.051 | 0.84 |  | 12/16 |
| MNQ | 15 | h8 | +0.011 | -0.110 .. +0.132 | +0.7% | +0.027 | 0.86 |  | 5/16 |
| MNQ | 15 | h16 | +0.007 | -0.155 .. +0.170 | +0.3% | +0.145 | 0.93 |  | 5/16 |
| MNQ | 15 | eod | +0.345 | -0.387 .. +1.078 | +5.4% | +0.484 | 0.36 |  | 9/16 |
| MNQ | 60 | h1 * | -0.052 | -0.067 .. -0.038 | -9.9% | -0.102 | 1.9e-12 | 6.93e-10 | 15/16 |
| MNQ | 60 | h2 | -0.069 | -0.092 .. -0.046 | -9.0% | -0.137 | 8.9e-09 |  | 14/16 |
| MNQ | 60 | h4 | -0.088 | -0.127 .. -0.049 | -8.0% | -0.177 | 1.8e-05 |  | 13/16 |
| MNQ | 60 | h8 | -0.128 | -0.195 .. -0.060 | -8.1% | -0.243 | 0.00026 |  | 12/16 |
| MNQ | 60 | h16 | -0.171 | -0.281 .. -0.060 | -7.8% | -0.336 | 0.0032 |  | 12/16 |
| MNQ | 60 | eod | -0.173 | -0.294 .. -0.052 | -7.5% | -0.345 | 0.0077 |  | 10/16 |
| MYM | 5 | h1 * | -0.038 | -0.051 .. -0.025 | -7.1% | -0.074 | 8.2e-09 | 2.33e-06 | 8/8 |
| MYM | 5 | h2 | -0.040 | -0.057 .. -0.023 | -5.2% | -0.092 | 7.8e-06 |  | 7/8 |
| MYM | 5 | h4 | -0.049 | -0.084 .. -0.014 | -4.5% | -0.112 | 0.0095 |  | 7/8 |
| MYM | 5 | h8 | -0.042 | -0.111 .. +0.026 | -2.7% | -0.126 | 0.26 |  | 6/8 |
| MYM | 5 | h16 | -0.041 | -0.158 .. +0.076 | -1.7% | -0.119 | 0.55 |  | 6/8 |
| MYM | 5 | eod | -0.035 | -0.762 .. +0.692 | -0.3% | -0.254 | 0.93 |  | 5/8 |
| MYM | 15 | h1 * | -0.048 | -0.063 .. -0.032 | -9.0% | -0.102 | 1.6e-09 | 4.74e-07 | 8/8 |
| MYM | 15 | h2 | -0.051 | -0.081 .. -0.021 | -6.7% | -0.110 | 0.00085 |  | 8/8 |
| MYM | 15 | h4 | -0.037 | -0.120 .. +0.045 | -3.4% | -0.096 | 0.4 |  | 6/8 |
| MYM | 15 | h8 | -0.027 | -0.181 .. +0.127 | -1.6% | -0.046 | 0.8 |  | 5/8 |
| MYM | 15 | h16 | +0.023 | -0.283 .. +0.329 | +1.0% | +0.096 | 0.88 |  | 2/8 |
| MYM | 15 | eod | +0.445 | -0.448 .. +1.339 | +7.4% | +0.479 | 0.35 |  | 5/8 |
| MYM | 60 | h1 * | -0.028 | -0.051 .. -0.006 | -5.4% | -0.072 | 0.012 | 1 | 6/8 |
| MYM | 60 | h2 | -0.022 | -0.059 .. +0.014 | -3.0% | -0.077 | 0.22 |  | 4/8 |
| MYM | 60 | h4 | -0.036 | -0.094 .. +0.022 | -3.3% | -0.091 | 0.22 |  | 5/8 |
| MYM | 60 | h8 | -0.017 | -0.119 .. +0.085 | -1.1% | -0.092 | 0.75 |  | 4/8 |
| MYM | 60 | h16 | -0.055 | -0.212 .. +0.102 | -2.6% | -0.128 | 0.49 |  | 5/8 |
| MYM | 60 | eod | -0.048 | -0.225 .. +0.130 | -2.1% | -0.147 | 0.6 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.33 pts | -0.88 .. +0.22 | 0.27 |
| MES | 15 | -0.24 pts | -1.18 .. +0.71 | 0.62 |
| MES | 60 | +0.02 pts | -1.87 .. +1.91 | 0.99 |
| MNQ | 5 | -0.47 pts | -1.04 .. +0.10 | 0.16 |
| MNQ | 15 | -0.33 pts | -1.27 .. +0.60 | 0.49 |
| MNQ | 60 | +0.36 pts | -1.44 .. +2.16 | 0.71 |
| MYM | 5 | -0.29 pts | -0.97 .. +0.39 | 0.41 |
| MYM | 15 | -0.44 pts | -1.68 .. +0.79 | 0.48 |
| MYM | 60 | -0.53 pts | -3.08 .. +2.03 | 0.71 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | short | 206858 | +0.003 | 0.390 | +0.05 | -3.45 | -3.48 | -3.43 | -3.47 |
| MES | 5 | h2 | top fifth | short | 206858 | +0.003 | 0.390 | +0.04 | -3.46 | -3.47 | -3.46 | -3.47 |
| MES | 5 | h4 | bottom fifth | long | 206971 | +0.007 | 0.297 | +0.02 | -3.48 | -3.43 | -3.53 | -3.55 |
| MES | 5 | h8 | bottom fifth | long | 206971 | +0.020 | 0.297 | +0.08 | -3.42 | -3.30 | -3.54 | -3.54 |
| MES | 5 | h16 | bottom fifth | long | 206971 | +0.047 | 0.297 | +0.24 | -3.26 | -3.02 | -3.51 | -3.56 |
| MES | 5 | eod | bottom fifth | long | 206971 | +0.263 | 0.297 | +2.43 | -1.07 | -1.25 | -0.89 | -0.24 |
| MES | 15 | h1 | bottom fifth | long | 68318 | +0.009 | 0.168 | +0.12 | -3.38 | -3.42 | -3.34 | -3.49 |
| MES | 15 | h2 | bottom fifth | long | 68318 | +0.016 | 0.168 | +0.26 | -3.24 | -3.29 | -3.20 | -3.40 |
| MES | 15 | h4 | bottom fifth | long | 68318 | +0.033 | 0.168 | +0.55 | -2.95 | -3.05 | -2.85 | -3.17 |
| MES | 15 | h8 | bottom fifth | long | 68318 | +0.062 | 0.168 | +1.20 | -2.30 | -2.64 | -1.96 | -2.59 |
| MES | 15 | h16 | bottom fifth | long | 68318 | +0.077 | 0.168 | +1.66 | -1.84 | -2.08 | -1.61 | -1.97 |
| MES | 15 | eod | bottom fifth | long | 68318 | +0.112 | 0.168 | +3.73 | +0.23 | -0.38 | +0.83 | +1.50 |
| MES | 60 | h1 | bottom fifth | long | 16623 | +0.015 | 0.084 | +0.60 | -2.90 | -3.10 | -2.71 | -3.13 |
| MES | 60 | h2 | bottom fifth | long | 16623 | +0.028 | 0.084 | +1.14 | -2.36 | -2.68 | -2.05 | -2.84 |
| MES | 60 | h4 | top fifth | long | 16623 | +0.051 | 0.107 | +1.53 | -1.97 | -3.05 | -0.89 | -2.86 |
| MES | 60 | h8 | bottom fifth | long | 16623 | +0.064 | 0.084 | +2.61 | -0.89 | -1.40 | -0.41 | -2.62 |
| MES | 60 | h16 | bottom fifth | long | 16623 | +0.081 | 0.084 | +3.31 | -0.19 | -0.32 | -0.07 | -2.43 |
| MES | 60 | eod | bottom fifth | long | 16623 | +0.114 | 0.084 | +4.65 | +1.15 | +0.44 | +1.83 | -1.94 |
| MNQ | 5 | h1 | top fifth | long | 206800 | +0.003 | 0.161 | +0.02 | -1.98 | -1.99 | -1.97 | -1.99 |
| MNQ | 5 | h2 | top fifth | long | 206800 | +0.007 | 0.161 | +0.06 | -1.94 | -1.96 | -1.90 | -1.98 |
| MNQ | 5 | h4 | bottom fifth | long | 206828 | +0.005 | 0.120 | +0.16 | -1.84 | -2.01 | -1.66 | -1.78 |
| MNQ | 5 | h8 | bottom fifth | long | 206828 | +0.031 | 0.120 | +0.37 | -1.63 | -1.93 | -1.33 | -1.57 |
| MNQ | 5 | h16 | bottom fifth | long | 206828 | +0.080 | 0.120 | +0.60 | -1.40 | -1.72 | -1.07 | -1.43 |
| MNQ | 5 | eod | bottom fifth | long | 206828 | +0.343 | 0.120 | +2.61 | +0.61 | +0.71 | +0.51 | +5.63 |
| MNQ | 15 | h1 | top fifth | long | 68337 | +0.011 | 0.090 | +0.19 | -1.81 | -1.91 | -1.70 | -1.87 |
| MNQ | 15 | h2 | top fifth | long | 68337 | +0.012 | 0.090 | +0.44 | -1.56 | -1.82 | -1.25 | -1.68 |
| MNQ | 15 | h4 | bottom fifth | long | 68342 | +0.026 | 0.067 | +0.41 | -1.59 | -1.56 | -1.61 | -1.96 |
| MNQ | 15 | h8 | bottom fifth | long | 68342 | +0.060 | 0.067 | +0.94 | -1.06 | -1.15 | -0.97 | -1.65 |
| MNQ | 15 | h16 | bottom fifth | long | 68342 | +0.104 | 0.067 | +1.21 | -0.79 | -0.51 | -1.06 | -0.79 |
| MNQ | 15 | eod | bottom fifth | long | 68342 | +0.150 | 0.067 | +3.29 | +1.29 | +1.62 | +0.97 | +4.13 |
| MNQ | 60 | h1 | top fifth | long | 16630 | +0.031 | 0.042 | +0.89 | -1.11 | -1.44 | -0.77 | -1.61 |
| MNQ | 60 | h2 | top fifth | long | 16630 | +0.057 | 0.042 | +1.61 | -0.39 | -1.08 | +0.29 | -1.35 |
| MNQ | 60 | h4 | top fifth | long | 16630 | +0.095 | 0.042 | +2.83 | +0.83 | -0.60 | +2.25 | -0.95 |
| MNQ | 60 | h8 | top fifth | long | 16630 | +0.142 | 0.042 | +4.13 | +2.13 | +0.06 | +4.19 | -0.61 |
| MNQ | 60 | h16 | top fifth | long | 16630 | +0.170 | 0.042 | +4.60 | +2.60 | +0.23 | +4.97 | -1.40 |
| MNQ | 60 | eod | top fifth | long | 16630 | +0.178 | 0.042 | +4.67 | +2.67 | +0.20 | +5.14 | -2.07 |
| MYM | 5 | h1 | top fifth | short | 103759 | +0.008 | 0.185 | +0.06 | -1.94 | +nan | -1.94 | -1.96 |
| MYM | 5 | h2 | top fifth | short | 103759 | +0.016 | 0.185 | +0.07 | -1.93 | +nan | -1.93 | -1.93 |
| MYM | 5 | h4 | top fifth | short | 103759 | +0.026 | 0.185 | +0.04 | -1.96 | +nan | -1.96 | -1.90 |
| MYM | 5 | h8 | top fifth | short | 103759 | +0.047 | 0.185 | +0.01 | -1.99 | +nan | -1.99 | -1.80 |
| MYM | 5 | h16 | bottom fifth | long | 103760 | -0.025 | 0.158 | +0.01 | -1.99 | +nan | -1.99 | -1.61 |
| MYM | 5 | eod | bottom fifth | long | 103760 | -0.093 | 0.158 | +1.74 | -0.26 | +nan | -0.26 | +0.89 |
| MYM | 15 | h1 | top fifth | long | 34235 | -0.001 | 0.105 | -0.07 | -2.07 | +nan | -2.07 | -2.10 |
| MYM | 15 | h2 | bottom fifth | long | 34236 | -0.001 | 0.089 | +0.25 | -1.75 | +nan | -1.75 | -1.66 |
| MYM | 15 | h4 | bottom fifth | long | 34236 | +0.011 | 0.089 | +0.54 | -1.46 | +nan | -1.46 | -1.31 |
| MYM | 15 | h8 | bottom fifth | long | 34236 | +0.024 | 0.089 | +1.19 | -0.81 | +nan | -0.81 | -0.34 |
| MYM | 15 | h16 | bottom fifth | long | 34236 | +0.034 | 0.089 | +1.80 | -0.20 | +nan | -0.20 | +0.86 |
| MYM | 15 | eod | bottom fifth | long | 34236 | +0.074 | 0.089 | +4.49 | +2.49 | +nan | +2.49 | +4.14 |
| MYM | 60 | h1 | bottom fifth | long | 8319 | +0.009 | 0.044 | +0.54 | -1.46 | +nan | -1.46 | -1.60 |
| MYM | 60 | h2 | bottom fifth | long | 8319 | +0.024 | 0.044 | +1.26 | -0.74 | +nan | -0.74 | -1.05 |
| MYM | 60 | h4 | bottom fifth | long | 8319 | +0.051 | 0.044 | +2.41 | +0.41 | +nan | +0.41 | -0.21 |
| MYM | 60 | h8 | bottom fifth | long | 8319 | +0.089 | 0.044 | +3.76 | +1.76 | +nan | +1.76 | +0.78 |
| MYM | 60 | h16 | bottom fifth | long | 8319 | +0.066 | 0.044 | +2.80 | +0.80 | +nan | +0.80 | -0.19 |
| MYM | 60 | eod | bottom fifth | long | 8319 | +0.086 | 0.044 | +3.66 | +1.66 | +nan | +1.66 | -0.27 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.886 | -1.343 | -0.886 | -0.541 | -0.310 | +0.000 | -0.012 | -0.012 | -0.015 | -0.023 | -0.030 |
| MES | 15 | -2.312 | -1.620 | -1.071 | -0.641 | -0.362 | +0.000 | -0.009 | -0.013 | -0.028 | -0.051 | -0.097 |
| MES | 60 | -2.850 | -1.834 | -1.265 | -0.766 | -0.427 | +0.000 | -0.001 | -0.007 | +0.005 | +0.018 | -0.066 |
| MNQ | 5 | -2.625 | -1.867 | -1.190 | -0.701 | -0.391 | +0.000 | -0.008 | -0.008 | -0.013 | -0.040 | -0.087 |
| MNQ | 15 | -2.791 | -1.951 | -1.265 | -0.747 | -0.415 | +0.000 | -0.008 | -0.015 | -0.036 | -0.063 | -0.164 |
| MNQ | 60 | -3.170 | -2.044 | -1.412 | -0.852 | -0.475 | +0.000 | +0.011 | +0.013 | +0.015 | +0.026 | -0.060 |
| MYM | 5 | -2.699 | -1.948 | -1.232 | -0.721 | -0.403 | +0.000 | -0.006 | -0.016 | -0.025 | -0.053 | -0.110 |
| MYM | 15 | -2.876 | -2.043 | -1.316 | -0.777 | -0.433 | +0.000 | -0.005 | -0.024 | -0.066 | -0.137 | -0.312 |
| MYM | 60 | -3.096 | -2.108 | -1.431 | -0.850 | -0.472 | +0.000 | -0.002 | -0.016 | -0.034 | -0.083 | -0.012 |

## Calibration

- MES 5-min: 1034605 bars, 206858 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341571 bars, 68306 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83113 bars, 16623 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034138 bars, 206800 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341703 bars, 68337 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83147 bars, 16630 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518800 bars, 103759 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171180 bars, 34235 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41591 bars, 8318 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
