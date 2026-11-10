# Impact card: dist_ema50

(close - EMA50) in R20 (average bars) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.021 R20, CONFIRMED, q=4.04e-14, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.28 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.217 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.043 R20 or more 80% of the time).
- MES 15-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.033 R20, CONFIRMED, q=3.42e-10, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.74 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.034 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.092 R20 or more 80% of the time).
- MES 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.053 R20, CONFIRMED, q=9.94e-11, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.93 at recent bar sizes, 90% range up to $3.58); about 1.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.021 R20 over the next 4 bars (20 min), p=0.51; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.020 R20, CONFIRMED, q=2.08e-07, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.28 at recent bar sizes, 90% range up to $0.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.434 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.052 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 2 bars (30 min) (-0.039 R20, CONFIRMED, q=0.00189, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.55 at recent bar sizes, 90% range up to $2.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.010 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.097 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.043 R20, CONFIRMED, q=2.92e-06, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.46 at recent bar sizes, 90% range up to $5.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.027 R20, CONFIRMED, q=0.00258, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.02 at recent bar sizes, 90% range up to $0.68); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.204 R20 over the next 16 bars (4 h), p=0.99; we would catch an effect of 0.079 R20 or more 80% of the time).
- MYM 15-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.035 R20, CONFIRMED, q=0.00397, 6 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.09 at recent bar sizes, 90% range up to $2.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.101 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.131 R20 or more 80% of the time).
- MYM 60-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.039 R20, possible, q=0.12, 5 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.12 at recent bar sizes, 90% range up to $4.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.008 .. +0.001 | -0.0032 | 0.16 / 0.15 / 0.17 | 0.176 | 1 | 1 | 11/16 | -0.006 | -0.000 | False | -1.4 / -1.4 |  |
| MES | 5 | h2 | -0.003 | -0.011 .. +0.005 | -0.0032 | 0.46 / 0.43 / 0.49 | 0.493 |  |  | 11/16 | -0.013 | +0.007 |  | -0.9 / -0.7 |  |
| MES | 5 | h4 | -0.003 | -0.019 .. +0.012 | -0.0023 | 0.68 / 0.67 / 0.71 | 0.707 |  |  | 9/16 | -0.026 | +0.019 |  | -0.7 / -0.4 | 0.024 |
| MES | 5 | h8 | -0.010 | -0.040 .. +0.020 | -0.0038 | 0.52 / 0.5 / 0.55 | 0.557 |  |  | 9/16 | -0.053 | +0.033 |  | -1.5 / -0.6 |  |
| MES | 5 | h16 | -0.008 | -0.066 .. +0.049 | -0.0020 | 0.78 / 0.76 / 0.79 | 0.788 |  |  | 7/16 | -0.071 | +0.054 |  | -0.9 / -0.3 |  |
| MES | 5 | eod | -0.002 | -0.635 .. +0.630 | +0.0025 | 0.99 / 0.99 / 0.99 | 0.991 |  |  | 11/16 | -0.140 | +0.135 |  | -0.0 / -0.0 |  |
| MES | 15 | h1 | +0.003 | -0.006 .. +0.012 | -0.0028 | 0.51 / 0.51 / 0.49 | 0.49 |  |  | 9/16 | -0.001 | +0.007 |  | +0.7 / +0.7 |  |
| MES | 15 | h2 * | +0.008 | -0.007 .. +0.023 | -0.0002 | 0.29 / 0.29 / 0.33 | 0.336 | 1 | 1 | 9/16 | -0.004 | +0.020 | False | +1.2 / +1.1 |  |
| MES | 15 | h4 | +0.003 | -0.026 .. +0.033 | -0.0005 | 0.83 / 0.83 / 0.84 | 0.846 |  |  | 6/16 | -0.025 | +0.032 |  | +0.4 / +0.2 | 0.043 |
| MES | 15 | h8 | +0.010 | -0.042 .. +0.061 | +0.0021 | 0.71 / 0.72 / 0.75 | 0.757 |  |  | 8/16 | -0.051 | +0.070 |  | +0.8 / +0.4 |  |
| MES | 15 | h16 | +0.015 | -0.086 .. +0.116 | +0.0038 | 0.77 / 0.78 / 0.81 | 0.807 |  |  | 9/16 | -0.107 | +0.136 |  | +0.8 / +0.3 |  |
| MES | 15 | eod | -0.022 | -0.539 .. +0.494 | +0.0050 | 0.93 / 0.93 / 0.94 | 0.939 |  |  | 10/16 | -0.307 | +0.260 |  | -0.4 / -0.1 |  |
| MES | 60 | h1 | +0.006 | -0.011 .. +0.023 | +0.0079 | 0.47 / 0.46 / 0.5 | 0.503 |  |  | 8/16 | -0.010 | +0.023 |  | +0.7 / +0.7 |  |
| MES | 60 | h2 | +0.010 | -0.021 .. +0.041 | +0.0075 | 0.52 / 0.51 / 0.57 | 0.564 |  |  | 8/16 | -0.019 | +0.039 |  | +0.8 / +0.6 |  |
| MES | 60 | h4 * | +0.034 | -0.025 .. +0.092 | +0.0088 | 0.26 / 0.26 / 0.31 | 0.315 | 1 | 1 | 9/16 | -0.026 | +0.093 | False | +1.9 / +1.1 | 0.092 |
| MES | 60 | h8 | +0.040 | -0.067 .. +0.147 | +0.0028 | 0.46 / 0.46 / 0.5 | 0.501 |  |  | 9/16 | -0.050 | +0.131 |  | +1.7 / +0.7 |  |
| MES | 60 | h16 | +0.022 | -0.159 .. +0.203 | -0.0007 | 0.81 / 0.81 / 0.83 | 0.829 |  |  | 9/16 | -0.096 | +0.140 |  | +0.7 / +0.2 |  |
| MES | 60 | eod | +0.003 | -0.198 .. +0.204 | -0.0013 | 0.98 / 0.98 / 0.97 | 0.972 |  |  | 8/16 | -0.091 | +0.097 |  | +0.1 / +0.0 |  |
| MNQ | 5 | h1 | +0.004 | -0.002 .. +0.010 | +0.0030 | 0.17 / 0.15 / 0.14 | 0.139 |  |  | 8/16 | -0.000 | +0.008 |  | +1.3 / +1.4 |  |
| MNQ | 5 | h2 | +0.010 | +0.000 .. +0.020 | +0.0032 | 0.045 / 0.039 / 0.078 | 0.0779 |  |  | 10/16 | -0.003 | +0.023 |  | +2.0 / +2.0 |  |
| MNQ | 5 | h4 * | +0.021 | +0.001 .. +0.042 | +0.0048 | 0.037 / 0.033 / 0.058 | 0.0594 | 1 | 0.999 | 11/16 | -0.006 | +0.049 | False | +2.7 / +2.1 | 0.030 |
| MNQ | 5 | h8 | +0.025 | -0.014 .. +0.064 | +0.0009 | 0.21 / 0.2 / 0.26 | 0.258 |  |  | 10/16 | -0.020 | +0.069 |  | +2.0 / +1.2 |  |
| MNQ | 5 | h16 | +0.036 | -0.046 .. +0.118 | -0.0023 | 0.39 / 0.39 / 0.39 | 0.386 |  |  | 8/16 | -0.019 | +0.090 |  | +2.0 / +0.9 |  |
| MNQ | 5 | eod | +0.144 | -0.949 .. +1.236 | +0.0126 | 0.8 / 0.79 / 0.72 | 0.715 |  |  | 6/16 | +0.017 | +0.269 |  | +1.9 / +0.3 |  |
| MNQ | 15 | h1 | +0.006 | -0.008 .. +0.019 | -0.0005 | 0.42 / 0.43 / 0.31 | 0.31 |  |  | 9/16 | +0.004 | +0.007 |  | +0.8 / +0.8 |  |
| MNQ | 15 | h2 | +0.003 | -0.034 .. +0.039 | -0.0037 | 0.88 / 0.88 / 0.81 | 0.809 |  |  | 12/16 | +0.008 | -0.003 |  | +0.2 / +0.1 |  |
| MNQ | 15 | h4 | -0.008 | -0.093 .. +0.078 | -0.0087 | 0.86 / 0.86 / 0.73 | 0.728 |  |  | 4/16 | +0.007 | -0.023 |  | -0.4 / -0.2 | 0.052 |
| MNQ | 15 | h8 | -0.012 | -0.128 .. +0.104 | -0.0094 | 0.84 / 0.84 / 0.76 | 0.754 |  |  | 5/16 | -0.000 | -0.024 |  | -0.5 / -0.2 |  |
| MNQ | 15 | h16 | -0.060 | -0.243 .. +0.122 | -0.0155 | 0.52 / 0.53 / 0.41 | 0.407 |  |  | 7/16 | -0.063 | -0.058 |  | -2.1 / -0.6 |  |
| MNQ | 15 | eod * | -0.434 | -1.304 .. +0.437 | -0.0352 | 0.33 / 0.33 / 0.21 | 0.207 | 1 | 1 | 11/16 | +0.049 | -0.913 | False | -4.6 / -1.0 |  |
| MNQ | 60 | h1 * | +0.010 | -0.008 .. +0.028 | +0.0087 | 0.27 / 0.27 / 0.3 | 0.304 | 1 | 1 | 9/16 | -0.001 | +0.021 | False | +1.0 / +1.1 |  |
| MNQ | 60 | h2 | +0.012 | -0.022 .. +0.046 | +0.0083 | 0.49 / 0.49 / 0.52 | 0.52 |  |  | 10/16 | -0.016 | +0.040 |  | +0.9 / +0.7 |  |
| MNQ | 60 | h4 | +0.024 | -0.037 .. +0.086 | +0.0078 | 0.44 / 0.45 / 0.48 | 0.485 |  |  | 11/16 | -0.018 | +0.066 |  | +1.3 / +0.8 | 0.097 |
| MNQ | 60 | h8 | +0.025 | -0.086 .. +0.136 | +0.0040 | 0.66 / 0.67 / 0.69 | 0.682 |  |  | 9/16 | -0.017 | +0.066 |  | +1.0 / +0.4 |  |
| MNQ | 60 | h16 | -0.013 | -0.203 .. +0.177 | -0.0007 | 0.89 / 0.9 / 0.92 | 0.913 |  |  | 8/16 | -0.018 | -0.008 |  | -0.4 / -0.1 |  |
| MNQ | 60 | eod | -0.045 | -0.254 .. +0.164 | -0.0049 | 0.67 / 0.68 / 0.72 | 0.715 |  |  | 8/16 | -0.010 | -0.081 |  | -1.3 / -0.4 |  |
| MYM | 5 | h1 * | -0.003 | -0.012 .. +0.005 | +0.0002 | 0.47 / 0.47 / 0.49 | 0.489 | 1 | 1 | 5/8 | n/a | -0.003 | False | -0.6 / -0.7 |  |
| MYM | 5 | h2 | +0.002 | -0.025 .. +0.029 | +0.0034 | 0.91 / 0.91 / 0.84 | 0.846 |  |  | 2/8 | n/a | +0.002 |  | +0.2 / +0.1 |  |
| MYM | 5 | h4 | +0.014 | -0.052 .. +0.079 | +0.0081 | 0.69 / 0.68 / 0.47 | 0.466 |  |  | 2/8 | n/a | +0.014 |  | +0.9 / +0.4 | 0.044 |
| MYM | 5 | h8 | +0.024 | -0.082 .. +0.131 | +0.0087 | 0.65 / 0.65 / 0.46 | 0.46 |  |  | 2/8 | n/a | +0.024 |  | +1.1 / +0.4 |  |
| MYM | 5 | h16 | +0.038 | -0.129 .. +0.205 | +0.0123 | 0.65 / 0.66 / 0.51 | 0.495 |  |  | 4/8 | n/a | +0.038 |  | +1.5 / +0.4 |  |
| MYM | 5 | eod | +0.507 | -0.962 .. +1.976 | +0.0309 | 0.5 / 0.49 / 0.33 | 0.339 |  |  | 3/8 | n/a | +0.507 |  | +5.0 / +0.7 |  |
| MYM | 15 | h1 | +0.009 | -0.006 .. +0.023 | +0.0108 | 0.26 / 0.25 / 0.21 | 0.213 |  |  | 4/8 | n/a | +0.009 |  | +1.1 / +1.1 |  |
| MYM | 15 | h2 | +0.017 | -0.006 .. +0.040 | +0.0110 | 0.15 / 0.15 / 0.27 | 0.265 |  |  | 5/8 | n/a | +0.017 |  | +1.6 / +1.4 |  |
| MYM | 15 | h4 | +0.035 | -0.008 .. +0.078 | +0.0089 | 0.11 / 0.12 / 0.26 | 0.256 |  |  | 5/8 | n/a | +0.035 |  | +2.4 / +1.6 | 0.079 |
| MYM | 15 | h8 | +0.095 | -0.038 .. +0.229 | +0.0091 | 0.16 / 0.17 / 0.1 | 0.102 |  |  | 4/8 | n/a | +0.095 |  | +2.7 / +1.4 |  |
| MYM | 15 | h16 * | +0.204 | -0.080 .. +0.488 | +0.0163 | 0.16 / 0.17 / 0.068 | 0.0664 | 1 | 1 | 4/8 | n/a | +0.204 | False | +4.4 / +1.4 |  |
| MYM | 15 | eod | +0.660 | -0.447 .. +1.766 | +0.0305 | 0.24 / 0.25 / 0.14 | 0.137 |  |  | 5/8 | n/a | +0.660 |  | +5.5 / +1.2 |  |
| MYM | 60 | h1 | +0.013 | -0.011 .. +0.038 | +0.0109 | 0.29 / 0.29 / 0.31 | 0.315 |  |  | 5/8 | n/a | +0.013 |  | +1.0 / +1.1 |  |
| MYM | 60 | h2 | +0.017 | -0.030 .. +0.064 | +0.0107 | 0.47 / 0.47 / 0.49 | 0.503 |  |  | 5/8 | n/a | +0.017 |  | +0.9 / +0.7 |  |
| MYM | 60 | h4 | +0.049 | -0.036 .. +0.135 | +0.0155 | 0.26 / 0.27 / 0.29 | 0.293 |  |  | 4/8 | n/a | +0.049 |  | +1.9 / +1.1 | 0.131 |
| MYM | 60 | h8 * | +0.101 | -0.060 .. +0.261 | +0.0208 | 0.22 / 0.22 / 0.24 | 0.243 | 1 | 1 | 5/8 | n/a | +0.101 | False | +2.9 / +1.2 |  |
| MYM | 60 | h16 | +0.155 | -0.113 .. +0.423 | +0.0206 | 0.26 / 0.27 / 0.29 | 0.302 |  |  | 5/8 | n/a | +0.155 |  | +3.4 / +1.1 |  |
| MYM | 60 | eod | +0.147 | -0.154 .. +0.448 | +0.0197 | 0.34 / 0.35 / 0.37 | 0.378 |  |  | 5/8 | n/a | +0.147 |  | +3.0 / +1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.021 | -0.026 .. -0.016 | -4.2% | -0.036 | 9e-17 | 4.04e-14 | 14/16 |
| MES | 5 | h2 | -0.028 | -0.036 .. -0.020 | -4.0% | -0.050 | 1.5e-12 |  | 14/16 |
| MES | 5 | h4 | -0.038 | -0.051 .. -0.024 | -3.8% | -0.071 | 2.8e-08 |  | 14/16 |
| MES | 5 | h8 | -0.047 | -0.069 .. -0.024 | -3.2% | -0.092 | 4.7e-05 |  | 14/16 |
| MES | 5 | h16 | -0.067 | -0.105 .. -0.029 | -3.2% | -0.118 | 0.00057 |  | 13/16 |
| MES | 5 | eod | +0.051 | -0.383 .. +0.485 | +0.5% | -0.112 | 0.82 |  | 7/16 |
| MES | 15 | h1 * | -0.033 | -0.042 .. -0.024 | -6.5% | -0.065 | 9.2e-13 | 3.42e-10 | 14/16 |
| MES | 15 | h2 | -0.046 | -0.063 .. -0.029 | -6.3% | -0.090 | 1.4e-07 |  | 12/16 |
| MES | 15 | h4 | -0.061 | -0.089 .. -0.033 | -5.8% | -0.123 | 1.7e-05 |  | 12/16 |
| MES | 15 | h8 | -0.074 | -0.115 .. -0.032 | -4.8% | -0.156 | 0.00056 |  | 11/16 |
| MES | 15 | h16 | -0.098 | -0.165 .. -0.031 | -4.3% | -0.208 | 0.0044 |  | 9/16 |
| MES | 15 | eod | -0.217 | -0.590 .. +0.155 | -4.0% | -0.360 | 0.25 |  | 10/16 |
| MES | 60 | h1 * | -0.053 | -0.067 .. -0.039 | -10.4% | -0.099 | 2.6e-13 | 9.94e-11 | 14/16 |
| MES | 60 | h2 | -0.075 | -0.097 .. -0.052 | -10.1% | -0.139 | 8.4e-11 |  | 15/16 |
| MES | 60 | h4 | -0.106 | -0.146 .. -0.066 | -10.0% | -0.188 | 2.2e-07 |  | 14/16 |
| MES | 60 | h8 | -0.162 | -0.233 .. -0.091 | -10.7% | -0.261 | 7.4e-06 |  | 14/16 |
| MES | 60 | h16 | -0.188 | -0.313 .. -0.064 | -9.1% | -0.319 | 0.003 |  | 12/16 |
| MES | 60 | eod | -0.178 | -0.322 .. -0.033 | -8.2% | -0.323 | 0.016 |  | 11/16 |
| MNQ | 5 | h1 * | -0.020 | -0.027 .. -0.014 | -3.8% | -0.036 | 6.8e-10 | 2.08e-07 | 14/16 |
| MNQ | 5 | h2 | -0.028 | -0.041 .. -0.015 | -3.7% | -0.053 | 1.5e-05 |  | 13/16 |
| MNQ | 5 | h4 | -0.038 | -0.062 .. -0.013 | -3.4% | -0.077 | 0.0026 |  | 12/16 |
| MNQ | 5 | h8 | -0.056 | -0.105 .. -0.008 | -3.5% | -0.112 | 0.024 |  | 12/16 |
| MNQ | 5 | h16 | -0.079 | -0.170 .. +0.012 | -3.3% | -0.169 | 0.09 |  | 12/16 |
| MNQ | 5 | eod | -0.251 | -1.123 .. +0.622 | -2.0% | -0.505 | 0.57 |  | 7/16 |
| MNQ | 15 | h1 | -0.032 | -0.048 .. -0.017 | -6.0% | -0.064 | 4.9e-05 |  | 13/16 |
| MNQ | 15 | h2 * | -0.039 | -0.056 .. -0.022 | -5.1% | -0.077 | 8.2e-06 | 0.00189 | 13/16 |
| MNQ | 15 | h4 | -0.039 | -0.076 .. -0.002 | -3.4% | -0.083 | 0.04 |  | 12/16 |
| MNQ | 15 | h8 | -0.024 | -0.106 .. +0.057 | -1.5% | -0.062 | 0.56 |  | 10/16 |
| MNQ | 15 | h16 | -0.018 | -0.167 .. +0.131 | -0.7% | -0.008 | 0.81 |  | 11/16 |
| MNQ | 15 | eod | +0.132 | -0.601 .. +0.864 | +2.1% | -0.006 | 0.73 |  | 5/16 |
| MNQ | 60 | h1 * | -0.043 | -0.057 .. -0.028 | -8.0% | -0.082 | 1e-08 | 2.92e-06 | 13/16 |
| MNQ | 60 | h2 | -0.060 | -0.083 .. -0.037 | -7.8% | -0.111 | 3.1e-07 |  | 13/16 |
| MNQ | 60 | h4 | -0.088 | -0.127 .. -0.048 | -7.9% | -0.150 | 1.3e-05 |  | 12/16 |
| MNQ | 60 | h8 | -0.136 | -0.204 .. -0.068 | -8.6% | -0.218 | 9.7e-05 |  | 13/16 |
| MNQ | 60 | h16 | -0.159 | -0.278 .. -0.040 | -7.2% | -0.288 | 0.01 |  | 11/16 |
| MNQ | 60 | eod | -0.144 | -0.279 .. -0.009 | -6.2% | -0.284 | 0.044 |  | 11/16 |
| MYM | 5 | h1 * | -0.027 | -0.039 .. -0.015 | -5.0% | -0.043 | 1.1e-05 | 0.00258 | 8/8 |
| MYM | 5 | h2 | -0.040 | -0.070 .. -0.011 | -5.3% | -0.070 | 0.0072 |  | 6/8 |
| MYM | 5 | h4 | -0.064 | -0.132 .. +0.005 | -5.8% | -0.112 | 0.068 |  | 6/8 |
| MYM | 5 | h8 | -0.098 | -0.217 .. +0.020 | -6.2% | -0.177 | 0.1 |  | 5/8 |
| MYM | 5 | h16 | -0.131 | -0.313 .. +0.050 | -5.6% | -0.280 | 0.16 |  | 6/8 |
| MYM | 5 | eod | -0.173 | -1.263 .. +0.917 | -1.5% | -0.315 | 0.76 |  | 4/8 |
| MYM | 15 | h1 * | -0.035 | -0.051 .. -0.019 | -6.6% | -0.070 | 1.8e-05 | 0.00397 | 6/8 |
| MYM | 15 | h2 | -0.053 | -0.079 .. -0.028 | -7.0% | -0.101 | 3.1e-05 |  | 6/8 |
| MYM | 15 | h4 | -0.072 | -0.112 .. -0.032 | -6.5% | -0.147 | 0.014 |  | 6/8 |
| MYM | 15 | h8 | -0.162 | -0.297 .. -0.026 | -9.9% | -0.303 | 0.021 |  | 6/8 |
| MYM | 15 | h16 | -0.267 | -0.515 .. -0.020 | -10.9% | -0.587 | 0.038 |  | 6/8 |
| MYM | 15 | eod | -0.475 | -1.393 .. +0.444 | -7.9% | -0.803 | 0.31 |  | 5/8 |
| MYM | 60 | h1 * | -0.039 | -0.062 .. -0.017 | -7.5% | -0.079 | 0.00068 | 0.12 | 5/8 |
| MYM | 60 | h2 | -0.052 | -0.089 .. -0.014 | -6.8% | -0.108 | 0.0071 |  | 5/8 |
| MYM | 60 | h4 | -0.074 | -0.136 .. -0.012 | -6.8% | -0.141 | 0.019 |  | 5/8 |
| MYM | 60 | h8 | -0.106 | -0.214 .. +0.001 | -6.8% | -0.195 | 0.057 |  | 4/8 |
| MYM | 60 | h16 | -0.144 | -0.342 .. +0.053 | -6.8% | -0.251 | 0.15 |  | 5/8 |
| MYM | 60 | eod | -0.148 | -0.376 .. +0.080 | -6.7% | -0.273 | 0.2 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.44 pts | -0.98 .. +0.10 | 0.18 |
| MES | 15 | +0.22 pts | -0.75 .. +1.18 | 0.66 |
| MES | 60 | +1.14 pts | -0.86 .. +3.15 | 0.28 |
| MNQ | 5 | +0.04 pts | -0.57 .. +0.65 | 0.89 |
| MNQ | 15 | +0.31 pts | -0.72 .. +1.35 | 0.55 |
| MNQ | 60 | +1.36 pts | -0.66 .. +3.38 | 0.2 |
| MYM | 5 | -0.18 pts | -0.93 .. +0.57 | 0.67 |
| MYM | 15 | +0.30 pts | -1.09 .. +1.69 | 0.67 |
| MYM | 60 | +1.43 pts | -1.33 .. +4.20 | 0.37 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 206870 | +0.005 | 0.276 | +0.07 | -3.43 | -3.45 | -3.41 | -3.46 |
| MES | 5 | h2 | bottom fifth | long | 206870 | +0.008 | 0.276 | +0.08 | -3.42 | -3.41 | -3.42 | -3.46 |
| MES | 5 | h4 | bottom fifth | long | 206870 | +0.011 | 0.276 | +0.08 | -3.42 | -3.36 | -3.47 | -3.47 |
| MES | 5 | h8 | bottom fifth | long | 206870 | +0.018 | 0.276 | +0.15 | -3.35 | -3.22 | -3.47 | -3.44 |
| MES | 5 | h16 | bottom fifth | long | 206870 | +0.042 | 0.276 | +0.44 | -3.06 | -2.97 | -3.15 | -3.33 |
| MES | 5 | eod | bottom fifth | long | 206870 | +0.080 | 0.276 | +2.78 | -0.72 | -0.45 | -0.97 | +0.62 |
| MES | 15 | h1 | top fifth | long | 68059 | +0.006 | 0.218 | +0.07 | -3.43 | -3.47 | -3.39 | -3.45 |
| MES | 15 | h2 | top fifth | long | 68059 | +0.015 | 0.218 | +0.17 | -3.33 | -3.39 | -3.27 | -3.41 |
| MES | 15 | h4 | top fifth | long | 68059 | +0.026 | 0.218 | +0.30 | -3.20 | -3.27 | -3.14 | -3.41 |
| MES | 15 | h8 | top fifth | long | 68059 | +0.048 | 0.218 | +0.40 | -3.10 | -2.97 | -3.21 | -3.48 |
| MES | 15 | h16 | top fifth | long | 68059 | +0.095 | 0.218 | +0.85 | -2.65 | -2.37 | -2.88 | -3.64 |
| MES | 15 | eod | bottom fifth | long | 68060 | +0.043 | 0.160 | +3.92 | +0.42 | +0.18 | +0.65 | +1.65 |
| MES | 60 | h1 | top fifth | long | 16323 | +0.012 | 0.113 | +0.35 | -3.15 | -3.39 | -2.93 | -3.43 |
| MES | 60 | h2 | top fifth | long | 16323 | +0.027 | 0.113 | +0.80 | -2.70 | -3.16 | -2.30 | -3.27 |
| MES | 60 | h4 | top fifth | long | 16323 | +0.060 | 0.113 | +2.00 | -1.50 | -2.86 | -0.27 | -2.50 |
| MES | 60 | h8 | top fifth | long | 16323 | +0.082 | 0.113 | +3.37 | -0.13 | -2.44 | +1.94 | -1.87 |
| MES | 60 | h16 | top fifth | long | 16323 | +0.096 | 0.113 | +3.64 | +0.14 | -2.45 | +2.47 | -2.64 |
| MES | 60 | eod | top fifth | long | 16323 | +0.096 | 0.113 | +3.44 | -0.06 | -2.61 | +2.23 | -3.22 |
| MNQ | 5 | h1 | top fifth | long | 206520 | +0.008 | 0.153 | +0.08 | -1.92 | -1.98 | -1.86 | -1.94 |
| MNQ | 5 | h2 | top fifth | long | 206520 | +0.016 | 0.153 | +0.15 | -1.85 | -1.94 | -1.76 | -1.90 |
| MNQ | 5 | h4 | top fifth | long | 206520 | +0.031 | 0.153 | +0.33 | -1.67 | -1.87 | -1.45 | -1.79 |
| MNQ | 5 | h8 | top fifth | long | 206520 | +0.051 | 0.153 | +0.56 | -1.44 | -1.75 | -1.10 | -1.72 |
| MNQ | 5 | h16 | top fifth | long | 206520 | +0.096 | 0.153 | +1.02 | -0.98 | -1.47 | -0.46 | -1.61 |
| MNQ | 5 | eod | top fifth | long | 206520 | +0.914 | 0.153 | +3.51 | +1.51 | +1.79 | +1.21 | -3.97 |
| MNQ | 15 | h1 | top fifth | long | 68028 | +0.015 | 0.094 | +0.23 | -1.77 | -1.90 | -1.65 | -1.86 |
| MNQ | 15 | h2 | top fifth | long | 68028 | +0.019 | 0.094 | +0.45 | -1.55 | -1.78 | -1.32 | -1.72 |
| MNQ | 15 | h4 | bottom fifth | long | 68028 | +0.029 | 0.065 | +0.13 | -1.87 | -1.64 | -2.10 | -2.31 |
| MNQ | 15 | h8 | bottom fifth | long | 68028 | +0.036 | 0.065 | +0.14 | -1.86 | -1.38 | -2.32 | -2.39 |
| MNQ | 15 | h16 | bottom fifth | long | 68028 | +0.055 | 0.065 | +0.08 | -1.92 | -0.82 | -3.02 | -1.97 |
| MNQ | 15 | eod | bottom fifth | long | 68028 | +0.248 | 0.065 | +7.23 | +5.23 | +1.86 | +8.57 | +6.97 |
| MNQ | 60 | h1 | top fifth | long | 16323 | +0.024 | 0.046 | +0.98 | -1.02 | -1.66 | -0.40 | -1.67 |
| MNQ | 60 | h2 | top fifth | long | 16323 | +0.044 | 0.046 | +1.87 | -0.13 | -1.47 | +1.20 | -1.36 |
| MNQ | 60 | h4 | top fifth | long | 16323 | +0.086 | 0.046 | +3.70 | +1.70 | -1.08 | +4.47 | -0.50 |
| MNQ | 60 | h8 | top fifth | long | 16323 | +0.124 | 0.046 | +4.97 | +2.97 | -0.52 | +6.45 | -0.28 |
| MNQ | 60 | h16 | bottom fifth | long | 16323 | +0.094 | 0.030 | +6.20 | +4.20 | +1.13 | +7.06 | +1.72 |
| MNQ | 60 | eod | bottom fifth | long | 16323 | +0.131 | 0.030 | +9.56 | +7.56 | +1.37 | +13.32 | +4.25 |
| MYM | 5 | h1 | bottom fifth | long | 103616 | -0.002 | 0.151 | +0.05 | -1.95 | +nan | -1.95 | -1.94 |
| MYM | 5 | h2 | top fifth | long | 103616 | -0.011 | 0.188 | -0.05 | -2.05 | +nan | -2.05 | -2.03 |
| MYM | 5 | h4 | bottom fifth | short | 103616 | +0.047 | 0.151 | -0.02 | -2.02 | +nan | -2.02 | -2.27 |
| MYM | 5 | h8 | bottom fifth | short | 103616 | +0.091 | 0.151 | +0.08 | -1.92 | +nan | -1.92 | -2.41 |
| MYM | 5 | h16 | bottom fifth | short | 103616 | +0.118 | 0.151 | -0.08 | -2.08 | +nan | -2.08 | -2.60 |
| MYM | 5 | eod | top fifth | long | 103616 | +0.327 | 0.188 | +3.50 | +1.50 | +nan | +1.50 | -0.50 |
| MYM | 15 | h1 | top fifth | long | 34093 | +0.003 | 0.114 | +0.03 | -1.97 | +nan | -1.97 | -2.00 |
| MYM | 15 | h2 | top fifth | long | 34093 | +0.010 | 0.114 | +0.09 | -1.91 | +nan | -1.91 | -2.01 |
| MYM | 15 | h4 | top fifth | long | 34093 | +0.026 | 0.114 | +0.27 | -1.73 | +nan | -1.73 | -1.95 |
| MYM | 15 | h8 | top fifth | long | 34093 | +0.034 | 0.114 | +0.32 | -1.68 | +nan | -1.68 | -1.97 |
| MYM | 15 | h16 | top fifth | long | 34093 | +0.055 | 0.114 | +0.66 | -1.34 | +nan | -1.34 | -1.91 |
| MYM | 15 | eod | top fifth | long | 34093 | +0.398 | 0.114 | +3.60 | +1.60 | +nan | +1.60 | -0.95 |
| MYM | 60 | h1 | top fifth | long | 8151 | +0.021 | 0.057 | +0.46 | -1.54 | +nan | -1.54 | -1.81 |
| MYM | 60 | h2 | top fifth | long | 8151 | +0.038 | 0.057 | +1.02 | -0.98 | +nan | -0.98 | -1.53 |
| MYM | 60 | h4 | top fifth | long | 8151 | +0.079 | 0.057 | +2.20 | +0.20 | +nan | +0.20 | -0.91 |
| MYM | 60 | h8 | top fifth | long | 8151 | +0.112 | 0.057 | +3.40 | +1.40 | +nan | +1.40 | -0.31 |
| MYM | 60 | h16 | top fifth | long | 8151 | +0.145 | 0.057 | +4.00 | +2.00 | +nan | +2.00 | -0.99 |
| MYM | 60 | eod | top fifth | long | 8151 | +0.142 | 0.057 | +3.81 | +1.81 | +nan | +1.81 | -1.72 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.993 | -1.583 | -1.136 | -0.722 | -0.422 | +0.000 | -0.021 | -0.023 | -0.023 | -0.029 | -0.029 |
| MES | 15 | -1.987 | -1.554 | -1.133 | -0.725 | -0.423 | +0.000 | -0.000 | +0.005 | +0.001 | +0.012 | +0.017 |
| MES | 60 | -2.634 | -1.880 | -1.302 | -0.823 | -0.475 | +0.000 | +0.008 | +0.012 | +0.035 | +0.031 | -0.009 |
| MNQ | 5 | -2.155 | -1.710 | -1.228 | -0.783 | -0.455 | +0.000 | -0.005 | -0.001 | +0.011 | +0.015 | +0.025 |
| MNQ | 15 | -2.071 | -1.589 | -1.156 | -0.747 | -0.437 | +0.000 | +0.003 | +0.000 | -0.009 | -0.008 | -0.067 |
| MNQ | 60 | -2.904 | -1.979 | -1.359 | -0.844 | -0.483 | +0.000 | +0.012 | +0.014 | +0.019 | +0.009 | -0.014 |
| MYM | 5 | -2.136 | -1.711 | -1.230 | -0.780 | -0.450 | +0.000 | -0.003 | -0.000 | +0.010 | +0.018 | +0.023 |
| MYM | 15 | -2.073 | -1.629 | -1.187 | -0.763 | -0.444 | +0.000 | +0.011 | +0.018 | +0.038 | +0.100 | +0.229 |
| MYM | 60 | -2.780 | -2.012 | -1.372 | -0.857 | -0.497 | +0.000 | +0.014 | +0.013 | +0.047 | +0.092 | +0.114 |

## Calibration

- MES 5-min: 1034349 bars, 206870 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 340296 bars, 68059 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81614 bars, 16323 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1032600 bars, 206520 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340140 bars, 68028 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81612 bars, 16323 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518078 bars, 103616 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170466 bars, 34093 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40755 bars, 8151 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
