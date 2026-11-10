# Impact card: sess_range_pos

close position in the session's range so far (0 = at low, 1 = at high) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.016 R20 over the next 4 bars (20 min), p=0.34; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.013 R20, CONFIRMED, q=2.03e-06, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.42 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.214 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.016 R20 over the next 2 bars (30 min), p=0.24; we would catch an effect of 0.042 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.037 R20, CONFIRMED, q=3.9e-15, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.08 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.124 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.023 R20 over the next 1 bar (1 h), p=0.091; we would catch an effect of 0.075 R20 or more 80% of the time).
- MES 60-min size: the market moves 13% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.064 R20, CONFIRMED, q=4.65e-15, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.44 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.062 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.027 R20 over the next 4 bars (20 min), p=0.22; we would catch an effect of 0.028 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.016 R20, CONFIRMED, q=0.00294, 11 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.37 at recent bar sizes, 90% range up to $0.84); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.019 R20 over the next 2 bars (30 min), p=0.48; we would catch an effect of 0.058 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.042 R20, CONFIRMED, q=1.82e-07, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.45 at recent bar sizes, 90% range up to $1.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.127 R20 over the next 16 bars (16 h), p=0.32; we would catch an effect of 0.081 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.052 R20, CONFIRMED, q=8.15e-09, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.89 at recent bar sizes, 90% range up to $7.16); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.070 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.020 R20, possible, q=0.0753, 6 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.81 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.162 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.056 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.050 R20, CONFIRMED, q=0.000211, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.60 at recent bar sizes, 90% range up to $2.44); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.019 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.113 R20 or more 80% of the time).
- MYM 60-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.058 R20, CONFIRMED, q=2.52e-06, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.41 at recent bar sizes, 90% range up to $3.01); about 3.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.005 .. +0.003 | -0.0022 | 0.71 / 0.72 / 0.74 | 0.744 |  |  | 9/16 | -0.005 | +0.003 |  | -0.3 / -0.4 |  |
| MES | 5 | h2 | +0.004 | -0.004 .. +0.012 | +0.0003 | 0.29 / 0.3 / 0.32 | 0.332 |  |  | 7/16 | -0.006 | +0.014 |  | +1.2 / +1.1 |  |
| MES | 5 | h4 * | +0.016 | +0.000 .. +0.032 | +0.0029 | 0.046 / 0.049 / 0.055 | 0.0508 | 1 | 0.999 | 9/16 | -0.003 | +0.035 | False | +3.2 / +2.0 | 0.023 |
| MES | 5 | h8 | +0.025 | -0.006 .. +0.056 | +0.0026 | 0.11 / 0.11 / 0.12 | 0.123 |  |  | 9/16 | -0.015 | +0.065 |  | +3.4 / +1.6 |  |
| MES | 5 | h16 | +0.040 | -0.018 .. +0.098 | +0.0033 | 0.18 / 0.18 / 0.21 | 0.21 |  |  | 9/16 | -0.030 | +0.109 |  | +3.9 / +1.3 |  |
| MES | 5 | eod | +0.170 | -0.646 .. +0.985 | +0.0071 | 0.68 / 0.68 / 0.62 | 0.614 |  |  | 6/16 | +0.028 | +0.311 |  | +3.4 / +0.4 |  |
| MES | 15 | h1 | +0.005 | -0.004 .. +0.013 | -0.0010 | 0.32 / 0.31 / 0.29 | 0.292 |  |  | 9/16 | -0.001 | +0.010 |  | +1.0 / +1.0 |  |
| MES | 15 | h2 * | +0.016 | +0.001 .. +0.030 | +0.0027 | 0.031 / 0.035 / 0.049 | 0.0511 | 1 | 0.996 | 11/16 | -0.001 | +0.032 | False | +2.2 / +2.2 |  |
| MES | 15 | h4 | +0.025 | -0.003 .. +0.053 | +0.0038 | 0.078 / 0.082 / 0.1 | 0.105 |  |  | 10/16 | -0.008 | +0.058 |  | +2.4 / +1.8 | 0.042 |
| MES | 15 | h8 | +0.031 | -0.023 .. +0.084 | +0.0043 | 0.26 / 0.27 / 0.28 | 0.278 |  |  | 9/16 | -0.038 | +0.099 |  | +2.1 / +1.1 |  |
| MES | 15 | h16 | +0.055 | -0.062 .. +0.173 | +0.0086 | 0.36 / 0.36 / 0.31 | 0.311 |  |  | 8/16 | -0.064 | +0.174 |  | +2.7 / +0.9 |  |
| MES | 15 | eod | +0.241 | -0.365 .. +0.846 | +0.0175 | 0.44 / 0.42 / 0.23 | 0.233 |  |  | 6/16 | +0.024 | +0.456 |  | +4.5 / +0.8 |  |
| MES | 60 | h1 * | +0.023 | +0.007 .. +0.038 | +0.0046 | 0.0055 / 0.0072 / 0.01 | 0.00912 | 1 | 0.699 | 13/16 | +0.006 | +0.039 | False | +2.6 / +2.8 |  |
| MES | 60 | h2 | +0.028 | +0.001 .. +0.055 | +0.0047 | 0.044 / 0.052 / 0.073 | 0.0701 |  |  | 11/16 | +0.002 | +0.054 |  | +2.3 / +2.0 |  |
| MES | 60 | h4 | +0.037 | -0.010 .. +0.084 | +0.0068 | 0.13 / 0.14 / 0.18 | 0.179 |  |  | 8/16 | +0.000 | +0.073 |  | +2.1 / +1.5 | 0.075 |
| MES | 60 | h8 | +0.053 | -0.028 .. +0.134 | +0.0076 | 0.2 / 0.2 / 0.24 | 0.233 |  |  | 8/16 | +0.039 | +0.067 |  | +2.2 / +1.3 |  |
| MES | 60 | h16 | +0.028 | -0.091 .. +0.146 | +0.0048 | 0.64 / 0.64 / 0.68 | 0.678 |  |  | 7/16 | +0.027 | +0.028 |  | +0.9 / +0.5 |  |
| MES | 60 | eod | +0.032 | -0.094 .. +0.158 | +0.0048 | 0.62 / 0.61 / 0.65 | 0.65 |  |  | 6/16 | +0.036 | +0.029 |  | +1.0 / +0.5 |  |
| MNQ | 5 | h1 | +0.005 | -0.000 .. +0.010 | +0.0036 | 0.074 / 0.083 / 0.078 | 0.0774 |  |  | 9/16 | -0.003 | +0.012 |  | +1.5 / +1.8 |  |
| MNQ | 5 | h2 | +0.013 | +0.001 .. +0.026 | +0.0059 | 0.03 / 0.031 / 0.02 | 0.0216 |  |  | 11/16 | -0.004 | +0.030 |  | +2.4 / +2.2 |  |
| MNQ | 5 | h4 * | +0.027 | +0.002 .. +0.053 | +0.0074 | 0.036 / 0.032 / 0.017 | 0.0172 | 1 | 0.997 | 10/16 | -0.008 | +0.062 | False | +3.1 / +2.1 | 0.028 |
| MNQ | 5 | h8 | +0.028 | -0.014 .. +0.069 | +0.0043 | 0.2 / 0.19 / 0.23 | 0.229 |  |  | 9/16 | -0.031 | +0.086 |  | +2.1 / +1.3 |  |
| MNQ | 5 | h16 | +0.018 | -0.062 .. +0.098 | +0.0002 | 0.66 / 0.66 / 0.68 | 0.667 |  |  | 8/16 | -0.052 | +0.087 |  | +1.0 / +0.4 |  |
| MNQ | 5 | eod | +0.441 | -0.719 .. +1.602 | +0.0166 | 0.46 / 0.45 / 0.32 | 0.32 |  |  | 6/16 | +0.003 | +0.876 |  | +6.0 / +0.7 |  |
| MNQ | 15 | h1 | +0.009 | -0.005 .. +0.023 | +0.0017 | 0.22 / 0.21 / 0.1 | 0.0998 |  |  | 12/16 | +0.002 | +0.016 |  | +1.3 / +1.2 |  |
| MNQ | 15 | h2 * | +0.019 | -0.001 .. +0.040 | +0.0037 | 0.066 / 0.065 / 0.093 | 0.0925 | 1 | 1 | 12/16 | -0.000 | +0.039 | False | +1.6 / +1.8 |  |
| MNQ | 15 | h4 | +0.028 | -0.013 .. +0.070 | +0.0028 | 0.18 / 0.18 / 0.23 | 0.233 |  |  | 12/16 | -0.001 | +0.057 |  | +1.3 / +1.3 | 0.058 |
| MNQ | 15 | h8 | +0.015 | -0.056 .. +0.086 | +0.0010 | 0.68 / 0.67 / 0.71 | 0.705 |  |  | 11/16 | -0.034 | +0.064 |  | +0.6 / +0.4 |  |
| MNQ | 15 | h16 | +0.072 | -0.067 .. +0.211 | +0.0080 | 0.31 / 0.32 / 0.29 | 0.287 |  |  | 10/16 | -0.066 | +0.209 |  | +2.4 / +1.0 |  |
| MNQ | 15 | eod | +0.575 | -0.266 .. +1.415 | +0.0282 | 0.18 / 0.17 / 0.03 | 0.0263 |  |  | 9/16 | +0.191 | +0.956 |  | +6.3 / +1.3 |  |
| MNQ | 60 | h1 | +0.019 | +0.002 .. +0.037 | +0.0063 | 0.033 / 0.033 / 0.041 | 0.0438 |  |  | 11/16 | +0.006 | +0.033 |  | +2.1 / +2.1 |  |
| MNQ | 60 | h2 | +0.024 | -0.006 .. +0.055 | +0.0066 | 0.12 / 0.12 / 0.14 | 0.147 |  |  | 12/16 | -0.009 | +0.058 |  | +1.9 / +1.6 |  |
| MNQ | 60 | h4 | +0.040 | -0.010 .. +0.090 | +0.0069 | 0.11 / 0.12 / 0.17 | 0.172 |  |  | 10/16 | -0.011 | +0.091 |  | +2.2 / +1.6 | 0.081 |
| MNQ | 60 | h8 | +0.082 | -0.003 .. +0.167 | +0.0105 | 0.058 / 0.063 / 0.086 | 0.0784 |  |  | 10/16 | +0.047 | +0.117 |  | +3.3 / +1.9 |  |
| MNQ | 60 | h16 * | +0.127 | -0.001 .. +0.255 | +0.0154 | 0.052 / 0.054 / 0.075 | 0.0727 | 1 | 0.993 | 10/16 | +0.108 | +0.146 | False | +3.9 / +1.9 |  |
| MNQ | 60 | eod | +0.116 | -0.020 .. +0.252 | +0.0134 | 0.094 / 0.098 / 0.12 | 0.121 |  |  | 10/16 | +0.087 | +0.145 |  | +3.4 / +1.7 |  |
| MYM | 5 | h1 | -0.001 | -0.010 .. +0.007 | -0.0004 | 0.75 / 0.76 / 0.78 | 0.779 |  |  | 4/8 | n/a | -0.001 |  | -0.3 / -0.3 |  |
| MYM | 5 | h2 | +0.006 | -0.021 .. +0.033 | +0.0051 | 0.67 / 0.66 / 0.49 | 0.488 |  |  | 4/8 | n/a | +0.006 |  | +0.6 / +0.4 |  |
| MYM | 5 | h4 | +0.021 | -0.046 .. +0.089 | +0.0093 | 0.53 / 0.52 / 0.25 | 0.26 |  |  | 3/8 | n/a | +0.021 |  | +1.4 / +0.6 | 0.048 |
| MYM | 5 | h8 | +0.041 | -0.070 .. +0.152 | +0.0103 | 0.47 / 0.46 / 0.23 | 0.234 |  |  | 3/8 | n/a | +0.041 |  | +1.9 / +0.7 |  |
| MYM | 5 | h16 * | +0.070 | -0.104 .. +0.244 | +0.0117 | 0.43 / 0.43 / 0.23 | 0.238 | 1 | 1 | 4/8 | n/a | +0.070 | False | +2.7 / +0.8 |  |
| MYM | 5 | eod | +0.002 | -1.561 .. +1.565 | +0.0079 | 1 / 1 / 1 | 0.996 |  |  | 3/8 | n/a | +0.002 |  | +0.0 / +0.0 |  |
| MYM | 15 | h1 | -0.003 | -0.016 .. +0.011 | -0.0013 | 0.7 / 0.71 / 0.71 | 0.732 |  |  | 3/8 | n/a | -0.003 |  | -0.3 / -0.4 |  |
| MYM | 15 | h2 | +0.022 | -0.016 .. +0.061 | +0.0074 | 0.25 / 0.25 / 0.17 | 0.178 |  |  | 5/8 | n/a | +0.022 |  | +1.3 / +1.2 |  |
| MYM | 15 | h4 * | +0.056 | -0.026 .. +0.138 | +0.0101 | 0.18 / 0.18 / 0.09 | 0.0896 | 1 | 1 | 4/8 | n/a | +0.056 | False | +1.8 / +1.3 | 0.078 |
| MYM | 15 | h8 | +0.091 | -0.070 .. +0.252 | +0.0150 | 0.27 / 0.27 / 0.098 | 0.0985 |  |  | 4/8 | n/a | +0.091 |  | +2.4 / +1.1 |  |
| MYM | 15 | h16 | +0.199 | -0.202 .. +0.601 | +0.0266 | 0.33 / 0.33 / 0.051 | 0.0506 |  |  | 3/8 | n/a | +0.199 |  | +3.8 / +1.0 |  |
| MYM | 15 | eod | +0.373 | -0.835 .. +1.582 | +0.0263 | 0.54 / 0.54 / 0.27 | 0.264 |  |  | 3/8 | n/a | +0.373 |  | +3.0 / +0.6 |  |
| MYM | 60 | h1 * | +0.019 | -0.005 .. +0.043 | +0.0071 | 0.12 / 0.12 / 0.16 | 0.157 | 1 | 1 | 5/8 | n/a | +0.019 | False | +1.4 / +1.5 |  |
| MYM | 60 | h2 | +0.026 | -0.016 .. +0.068 | +0.0074 | 0.22 / 0.21 / 0.26 | 0.267 |  |  | 6/8 | n/a | +0.026 |  | +1.4 / +1.2 |  |
| MYM | 60 | h4 | +0.027 | -0.047 .. +0.101 | +0.0050 | 0.47 / 0.45 / 0.5 | 0.513 |  |  | 6/8 | n/a | +0.027 |  | +1.1 / +0.7 | 0.113 |
| MYM | 60 | h8 | +0.010 | -0.108 .. +0.127 | +0.0007 | 0.87 / 0.87 / 0.89 | 0.884 |  |  | 4/8 | n/a | +0.010 |  | +0.3 / +0.2 |  |
| MYM | 60 | h16 | -0.033 | -0.205 .. +0.140 | -0.0030 | 0.71 / 0.71 / 0.72 | 0.73 |  |  | 5/8 | n/a | -0.033 |  | -0.7 / -0.4 |  |
| MYM | 60 | eod | -0.041 | -0.221 .. +0.140 | -0.0036 | 0.66 / 0.66 / 0.68 | 0.688 |  |  | 6/8 | n/a | -0.041 |  | -0.9 / -0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.013 | -0.018 .. -0.009 | -2.6% | -0.019 | 7e-09 | 2.03e-06 | 12/16 |
| MES | 5 | h2 | -0.017 | -0.025 .. -0.010 | -2.5% | -0.029 | 1.1e-05 |  | 10/16 |
| MES | 5 | h4 | -0.020 | -0.035 .. -0.005 | -2.0% | -0.040 | 0.0096 |  | 11/16 |
| MES | 5 | h8 | -0.026 | -0.053 .. +0.002 | -1.8% | -0.056 | 0.064 |  | 11/16 |
| MES | 5 | h16 | -0.037 | -0.082 .. +0.009 | -1.7% | -0.074 | 0.11 |  | 9/16 |
| MES | 5 | eod | +0.088 | -0.501 .. +0.677 | +0.9% | -0.060 | 0.77 |  | 10/16 |
| MES | 15 | h1 * | -0.037 | -0.045 .. -0.028 | -7.2% | -0.078 | 8.1e-18 | 3.9e-15 | 14/16 |
| MES | 15 | h2 | -0.048 | -0.067 .. -0.029 | -6.6% | -0.106 | 5.8e-07 |  | 14/16 |
| MES | 15 | h4 | -0.066 | -0.103 .. -0.028 | -6.2% | -0.141 | 0.00071 |  | 13/16 |
| MES | 15 | h8 | -0.083 | -0.145 .. -0.021 | -5.4% | -0.185 | 0.0085 |  | 11/16 |
| MES | 15 | h16 | -0.097 | -0.197 .. +0.003 | -4.2% | -0.249 | 0.057 |  | 9/16 |
| MES | 15 | eod | -0.156 | -0.653 .. +0.342 | -2.8% | -0.428 | 0.54 |  | 7/16 |
| MES | 60 | h1 * | -0.064 | -0.079 .. -0.050 | -12.5% | -0.136 | 9.7e-18 | 4.65e-15 | 16/16 |
| MES | 60 | h2 | -0.083 | -0.105 .. -0.061 | -11.2% | -0.176 | 1.2e-13 |  | 16/16 |
| MES | 60 | h4 | -0.113 | -0.147 .. -0.080 | -10.7% | -0.223 | 4e-11 |  | 15/16 |
| MES | 60 | h8 | -0.129 | -0.181 .. -0.077 | -8.6% | -0.264 | 1.4e-06 |  | 15/16 |
| MES | 60 | h16 | -0.088 | -0.166 .. -0.010 | -4.3% | -0.245 | 0.026 |  | 11/16 |
| MES | 60 | eod | -0.080 | -0.164 .. +0.003 | -3.7% | -0.242 | 0.06 |  | 12/16 |
| MNQ | 5 | h1 * | -0.016 | -0.023 .. -0.009 | -3.0% | -0.023 | 1.3e-05 | 0.00294 | 11/16 |
| MNQ | 5 | h2 | -0.024 | -0.041 .. -0.007 | -3.1% | -0.038 | 0.0054 |  | 11/16 |
| MNQ | 5 | h4 | -0.034 | -0.068 .. +0.000 | -3.1% | -0.059 | 0.052 |  | 9/16 |
| MNQ | 5 | h8 | -0.045 | -0.105 .. +0.016 | -2.8% | -0.088 | 0.15 |  | 10/16 |
| MNQ | 5 | h16 | -0.047 | -0.141 .. +0.047 | -2.0% | -0.125 | 0.33 |  | 9/16 |
| MNQ | 5 | eod | -0.088 | -1.005 .. +0.830 | -0.7% | -0.188 | 0.85 |  | 7/16 |
| MNQ | 15 | h1 * | -0.042 | -0.056 .. -0.029 | -7.9% | -0.084 | 5.9e-10 | 1.82e-07 | 14/16 |
| MNQ | 15 | h2 | -0.063 | -0.099 .. -0.028 | -8.2% | -0.129 | 0.00046 |  | 13/16 |
| MNQ | 15 | h4 | -0.087 | -0.177 .. +0.003 | -7.7% | -0.191 | 0.058 |  | 12/16 |
| MNQ | 15 | h8 | -0.113 | -0.267 .. +0.041 | -6.8% | -0.292 | 0.15 |  | 11/16 |
| MNQ | 15 | h16 | -0.117 | -0.291 .. +0.056 | -4.6% | -0.435 | 0.18 |  | 9/16 |
| MNQ | 15 | eod | -0.418 | -1.266 .. +0.431 | -6.6% | -0.668 | 0.33 |  | 10/16 |
| MNQ | 60 | h1 * | -0.052 | -0.067 .. -0.037 | -9.8% | -0.123 | 2.3e-11 | 8.15e-09 | 14/16 |
| MNQ | 60 | h2 | -0.065 | -0.088 .. -0.042 | -8.5% | -0.154 | 2.2e-08 |  | 14/16 |
| MNQ | 60 | h4 | -0.088 | -0.121 .. -0.055 | -7.9% | -0.191 | 1.6e-07 |  | 14/16 |
| MNQ | 60 | h8 | -0.110 | -0.162 .. -0.059 | -7.0% | -0.234 | 7.5e-05 |  | 14/16 |
| MNQ | 60 | h16 | -0.087 | -0.169 .. -0.006 | -4.0% | -0.230 | 0.036 |  | 12/16 |
| MNQ | 60 | eod | -0.089 | -0.176 .. -0.002 | -3.9% | -0.231 | 0.046 |  | 12/16 |
| MYM | 5 | h1 * | -0.020 | -0.031 .. -0.009 | -3.7% | -0.028 | 0.00041 | 0.0753 | 6/8 |
| MYM | 5 | h2 | -0.031 | -0.060 .. -0.003 | -4.1% | -0.048 | 0.029 |  | 5/8 |
| MYM | 5 | h4 | -0.052 | -0.119 .. +0.015 | -4.8% | -0.077 | 0.13 |  | 4/8 |
| MYM | 5 | h8 | -0.075 | -0.191 .. +0.041 | -4.7% | -0.120 | 0.21 |  | 4/8 |
| MYM | 5 | h16 | -0.088 | -0.266 .. +0.090 | -3.8% | -0.191 | 0.34 |  | 4/8 |
| MYM | 5 | eod | -0.141 | -1.247 .. +0.965 | -1.2% | -0.295 | 0.81 |  | 3/8 |
| MYM | 15 | h1 * | -0.050 | -0.069 .. -0.030 | -9.3% | -0.095 | 8.5e-07 | 0.000211 | 8/8 |
| MYM | 15 | h2 | -0.083 | -0.138 .. -0.028 | -10.8% | -0.155 | 0.0032 |  | 8/8 |
| MYM | 15 | h4 | -0.126 | -0.252 .. -0.001 | -11.3% | -0.250 | 0.051 |  | 5/8 |
| MYM | 15 | h8 | -0.182 | -0.384 .. +0.019 | -11.1% | -0.424 | 0.083 |  | 5/8 |
| MYM | 15 | h16 | -0.307 | -0.679 .. +0.065 | -12.5% | -0.681 | 0.11 |  | 5/8 |
| MYM | 15 | eod | -0.586 | -1.627 .. +0.455 | -9.7% | -1.076 | 0.29 |  | 6/8 |
| MYM | 60 | h1 * | -0.058 | -0.078 .. -0.038 | -11.1% | -0.121 | 8.9e-09 | 2.52e-06 | 7/8 |
| MYM | 60 | h2 | -0.068 | -0.099 .. -0.037 | -9.0% | -0.155 | 1.4e-05 |  | 7/8 |
| MYM | 60 | h4 | -0.097 | -0.144 .. -0.050 | -9.0% | -0.197 | 8e-05 |  | 8/8 |
| MYM | 60 | h8 | -0.099 | -0.175 .. -0.024 | -6.4% | -0.233 | 0.0095 |  | 7/8 |
| MYM | 60 | h16 | -0.070 | -0.176 .. +0.036 | -3.3% | -0.225 | 0.21 |  | 6/8 |
| MYM | 60 | eod | -0.060 | -0.174 .. +0.053 | -2.7% | -0.226 | 0.31 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.53 pts | -1.08 .. +0.02 | 0.079 |
| MES | 15 | -0.40 pts | -1.27 .. +0.47 | 0.36 |
| MES | 60 | +0.40 pts | -1.13 .. +1.94 | 0.92 |
| MNQ | 5 | -0.32 pts | -0.89 .. +0.26 | 0.29 |
| MNQ | 15 | -0.54 pts | -1.48 .. +0.39 | 0.25 |
| MNQ | 60 | +0.34 pts | -1.18 .. +1.85 | 0.66 |
| MYM | 5 | -0.79 pts | -1.48 .. -0.09 | 0.035 |
| MYM | 15 | -0.21 pts | -1.40 .. +0.99 | 0.74 |
| MYM | 60 | +0.66 pts | -1.40 .. +2.72 | 0.66 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 209254 | +0.007 | 0.287 | +0.07 | -3.43 | -3.45 | -3.41 | -3.47 |
| MES | 5 | h2 | top fifth | long | 205765 | +0.004 | 0.338 | +0.11 | -3.39 | -3.47 | -3.32 | -3.36 |
| MES | 5 | h4 | top fifth | long | 205765 | +0.017 | 0.338 | +0.28 | -3.22 | -3.39 | -3.07 | -3.22 |
| MES | 5 | h8 | top fifth | long | 205765 | +0.030 | 0.338 | +0.49 | -3.01 | -3.31 | -2.75 | -3.08 |
| MES | 5 | h16 | top fifth | long | 205765 | +0.053 | 0.338 | +0.79 | -2.71 | -3.17 | -2.31 | -2.93 |
| MES | 5 | eod | top fifth | long | 205765 | +0.530 | 0.338 | +4.31 | +0.81 | +0.46 | +1.10 | -1.66 |
| MES | 15 | h1 | top fifth | long | 68146 | +0.008 | 0.189 | +0.20 | -3.30 | -3.46 | -3.15 | -3.27 |
| MES | 15 | h2 | top fifth | long | 68146 | +0.018 | 0.189 | +0.44 | -3.06 | -3.37 | -2.80 | -3.09 |
| MES | 15 | h4 | top fifth | long | 68146 | +0.032 | 0.189 | +0.72 | -2.78 | -3.25 | -2.37 | -2.93 |
| MES | 15 | h8 | top fifth | long | 68146 | +0.050 | 0.189 | +1.04 | -2.46 | -3.01 | -1.98 | -2.81 |
| MES | 15 | h16 | top fifth | long | 68146 | +0.108 | 0.189 | +1.90 | -1.60 | -2.14 | -1.13 | -2.46 |
| MES | 15 | eod | top fifth | long | 68146 | +0.302 | 0.189 | +4.56 | +1.06 | +0.47 | +1.58 | -1.40 |
| MES | 60 | h1 | top fifth | long | 16682 | +0.024 | 0.090 | +0.96 | -2.54 | -3.20 | -1.96 | -2.73 |
| MES | 60 | h2 | top fifth | long | 16682 | +0.035 | 0.090 | +1.38 | -2.12 | -2.94 | -1.41 | -2.50 |
| MES | 60 | h4 | top fifth | long | 16682 | +0.059 | 0.090 | +2.24 | -1.26 | -2.23 | -0.41 | -2.05 |
| MES | 60 | h8 | top fifth | long | 16682 | +0.094 | 0.090 | +3.60 | +0.10 | -0.85 | +0.93 | -1.41 |
| MES | 60 | h16 | top fifth | long | 16682 | +0.111 | 0.090 | +4.93 | +1.43 | +0.45 | +2.29 | -1.25 |
| MES | 60 | eod | top fifth | long | 16682 | +0.115 | 0.090 | +4.84 | +1.34 | +0.65 | +1.93 | -1.60 |
| MNQ | 5 | h1 | top fifth | long | 206900 | +0.008 | 0.139 | +0.14 | -1.86 | -1.98 | -1.75 | -1.88 |
| MNQ | 5 | h2 | top fifth | long | 206900 | +0.016 | 0.139 | +0.27 | -1.73 | -1.92 | -1.55 | -1.77 |
| MNQ | 5 | h4 | top fifth | long | 206900 | +0.033 | 0.139 | +0.51 | -1.49 | -1.84 | -1.16 | -1.60 |
| MNQ | 5 | h8 | top fifth | long | 206900 | +0.056 | 0.139 | +0.90 | -1.10 | -1.70 | -0.52 | -1.37 |
| MNQ | 5 | h16 | top fifth | long | 206900 | +0.090 | 0.139 | +1.52 | -0.48 | -1.47 | +0.47 | -1.07 |
| MNQ | 5 | eod | top fifth | long | 206900 | +1.133 | 0.139 | +8.15 | +6.15 | +2.15 | +10.00 | +1.84 |
| MNQ | 15 | h1 | top fifth | long | 68410 | +0.016 | 0.076 | +0.46 | -1.54 | -1.87 | -1.22 | -1.59 |
| MNQ | 15 | h2 | top fifth | long | 68410 | +0.028 | 0.076 | +0.77 | -1.23 | -1.78 | -0.69 | -1.36 |
| MNQ | 15 | h4 | top fifth | long | 68410 | +0.048 | 0.076 | +1.26 | -0.74 | -1.54 | +0.03 | -1.07 |
| MNQ | 15 | h8 | top fifth | long | 68410 | +0.073 | 0.076 | +1.82 | -0.18 | -1.28 | +0.88 | -0.97 |
| MNQ | 15 | h16 | top fifth | long | 68410 | +0.144 | 0.076 | +3.40 | +1.40 | -0.65 | +3.38 | +0.10 |
| MNQ | 15 | eod | top fifth | long | 68410 | +0.573 | 0.076 | +8.43 | +6.43 | +2.04 | +10.65 | +3.40 |
| MNQ | 60 | h1 | top fifth | long | 16681 | +0.028 | 0.036 | +1.25 | -0.75 | -1.51 | -0.02 | -1.13 |
| MNQ | 60 | h2 | top fifth | long | 16681 | +0.045 | 0.036 | +2.12 | +0.12 | -1.31 | +1.48 | -0.49 |
| MNQ | 60 | h4 | top fifth | long | 16681 | +0.077 | 0.036 | +3.79 | +1.79 | -0.67 | +4.14 | +0.64 |
| MNQ | 60 | h8 | top fifth | long | 16681 | +0.130 | 0.036 | +6.01 | +4.01 | +0.78 | +7.11 | +2.01 |
| MNQ | 60 | h16 | top fifth | long | 16681 | +0.209 | 0.036 | +9.52 | +7.52 | +2.55 | +12.29 | +4.37 |
| MNQ | 60 | eod | top fifth | long | 16681 | +0.212 | 0.036 | +9.43 | +7.43 | +2.56 | +12.09 | +3.81 |
| MYM | 5 | h1 | bottom fifth | long | 103822 | +0.002 | 0.148 | +0.09 | -1.91 | +nan | -1.91 | -1.91 |
| MYM | 5 | h2 | top fifth | long | 103807 | -0.001 | 0.180 | +0.06 | -1.94 | +nan | -1.94 | -1.93 |
| MYM | 5 | h4 | top fifth | long | 103807 | +0.004 | 0.180 | +0.17 | -1.83 | +nan | -1.83 | -1.85 |
| MYM | 5 | h8 | top fifth | long | 103807 | +0.008 | 0.180 | +0.35 | -1.65 | +nan | -1.65 | -1.76 |
| MYM | 5 | h16 | top fifth | long | 103807 | +0.024 | 0.180 | +0.60 | -1.40 | +nan | -1.40 | -1.70 |
| MYM | 5 | eod | top fifth | long | 103807 | +0.174 | 0.180 | +3.12 | +1.12 | +nan | +1.12 | -0.46 |
| MYM | 15 | h1 | bottom fifth | long | 34286 | +0.006 | 0.088 | +0.17 | -1.83 | +nan | -1.83 | -1.85 |
| MYM | 15 | h2 | top fifth | long | 34283 | +0.011 | 0.098 | +0.23 | -1.77 | +nan | -1.77 | -1.83 |
| MYM | 15 | h4 | top fifth | long | 34283 | +0.027 | 0.098 | +0.56 | -1.44 | +nan | -1.44 | -1.58 |
| MYM | 15 | h8 | top fifth | long | 34283 | +0.027 | 0.098 | +0.71 | -1.29 | +nan | -1.29 | -1.51 |
| MYM | 15 | h16 | top fifth | long | 34283 | +0.041 | 0.098 | +1.18 | -0.82 | +nan | -0.82 | -1.17 |
| MYM | 15 | eod | top fifth | long | 34283 | +0.134 | 0.098 | +3.39 | +1.39 | +nan | +1.39 | +0.21 |
| MYM | 60 | h1 | top fifth | long | 8327 | +0.017 | 0.046 | +0.55 | -1.45 | +nan | -1.45 | -1.62 |
| MYM | 60 | h2 | top fifth | long | 8327 | +0.015 | 0.046 | +0.59 | -1.41 | +nan | -1.41 | -1.55 |
| MYM | 60 | h4 | top fifth | long | 8327 | +0.020 | 0.046 | +0.91 | -1.09 | +nan | -1.09 | -1.48 |
| MYM | 60 | h8 | top fifth | long | 8327 | +0.041 | 0.046 | +2.23 | +0.23 | +nan | +0.23 | -0.63 |
| MYM | 60 | h16 | bottom fifth | long | 8332 | +0.038 | 0.046 | +1.65 | -0.35 | +nan | -0.35 | -1.38 |
| MYM | 60 | eod | bottom fifth | long | 8332 | +0.046 | 0.046 | +1.50 | -0.50 | +nan | -0.50 | -2.26 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.406 | -1.292 | -1.031 | -0.702 | -0.427 | +0.000 | -0.022 | -0.021 | -0.011 | -0.007 | +0.003 |
| MES | 15 | -2.665 | -2.272 | -1.737 | -1.168 | -0.712 | +0.000 | -0.011 | -0.004 | +0.002 | +0.001 | +0.004 |
| MES | 60 | -4.294 | -3.512 | -2.637 | -1.794 | -1.146 | +0.000 | +0.015 | +0.012 | -0.001 | -0.025 | -0.093 |
| MNQ | 5 | -1.621 | -1.466 | -1.158 | -0.781 | -0.469 | +0.000 | -0.004 | +0.004 | +0.018 | +0.022 | +0.017 |
| MNQ | 15 | -2.913 | -2.455 | -1.863 | -1.250 | -0.758 | +0.000 | +0.011 | +0.024 | +0.036 | +0.025 | +0.069 |
| MNQ | 60 | -4.514 | -3.652 | -2.734 | -1.868 | -1.194 | +0.000 | +0.017 | +0.016 | +0.017 | +0.006 | +0.102 |
| MYM | 5 | -1.490 | -1.376 | -1.098 | -0.740 | -0.443 | +0.000 | -0.002 | +0.003 | +0.015 | +0.031 | +0.057 |
| MYM | 15 | -2.788 | -2.379 | -1.813 | -1.215 | -0.734 | +0.000 | +0.010 | +0.036 | +0.075 | +0.114 | +0.249 |
| MYM | 60 | -4.422 | -3.608 | -2.738 | -1.870 | -1.188 | +0.000 | +0.021 | +0.021 | +0.013 | -0.035 | -0.130 |

## Calibration

- MES 5-min: 1036271 bars, 205765 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68146 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034517 bars, 206900 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342061 bars, 68410 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16681 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103807 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34283 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8327 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
