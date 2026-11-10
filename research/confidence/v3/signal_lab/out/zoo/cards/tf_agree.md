# Impact card: tf_agree

5/15/60-min EMA stack agreement: +2 = all three up, -2 = all three down (levels -2..2) [controls: 15-min slot, weekday, year (trend state / volatility NOT controlled: they are the metric)]

Kind: state. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.004 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.040 R20, CONFIRMED, q=1.4e-65, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.40 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.225 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (15 min), p=0.77; we would catch an effect of 0.051 R20 or more 80% of the time).
- MES 15-min size: the market moves 12% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.060 R20, CONFIRMED, q=8.94e-43, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.11 at recent bar sizes, 90% range up to $0.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.044 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.087 R20 or more 80% of the time).
- MES 60-min size: the market moves 19% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.099 R20, CONFIRMED, q=1.97e-37, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.84 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.066 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.048 R20 over the next 8 bars (40 min), p=0.3; we would catch an effect of 0.034 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 6% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.031 R20, CONFIRMED, q=1.05e-19, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.62 at recent bar sizes, 90% range up to $1.14); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.026 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.059 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 10% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.056 R20, CONFIRMED, q=3.21e-29, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.57 at recent bar sizes, 90% range up to $2.07); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.018 R20 over the next 1 bar (1 h), p=0.53; we would catch an effect of 0.093 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 17% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.091 R20, CONFIRMED, q=1.19e-33, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $5.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.145 R20 over the next 16 bars (80 min), p=0.45; we would catch an effect of 0.052 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% LESS at the top level than at the bottom level over the next 1 bar (5 min) (-0.025 R20, CONFIRMED, q=9.22e-06, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.86 at recent bar sizes, 90% range up to $1.03); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MYM 15-min size: the market moves 11% LESS at the top level than at the bottom level over the next 1 bar (15 min) (-0.057 R20, CONFIRMED, q=2.31e-07, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.12 at recent bar sizes, 90% range up to $1.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.143 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.127 R20 or more 80% of the time).
- MYM 60-min size: the market moves 17% LESS at the top level than at the bottom level over the next 1 bar (1 h) (-0.089 R20, CONFIRMED, q=2.25e-14, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.96 at recent bar sizes, 90% range up to $4.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.004 | -0.008 .. +0.001 | -0.0013 | 0.15 / 0.15 / 0.16 | 0.165 | 1 | 1 | 12/16 | -0.008 | +0.001 | False | -1.4 / -1.4 |  |
| MES | 5 | h2 | -0.002 | -0.013 .. +0.009 | -0.0006 | 0.73 / 0.72 / 0.71 | 0.708 |  |  | 8/16 | -0.017 | +0.013 |  | -0.5 / -0.3 |  |
| MES | 5 | h4 | +0.003 | -0.020 .. +0.027 | +0.0002 | 0.79 / 0.79 / 0.75 | 0.753 |  |  | 9/16 | -0.033 | +0.039 |  | +0.5 / +0.3 | 0.028 |
| MES | 5 | h8 | +0.013 | -0.034 .. +0.060 | +0.0006 | 0.58 / 0.58 / 0.51 | 0.51 |  |  | 9/16 | -0.058 | +0.084 |  | +1.4 / +0.6 |  |
| MES | 5 | h16 | +0.026 | -0.061 .. +0.113 | +0.0010 | 0.55 / 0.55 / 0.5 | 0.511 |  |  | 9/16 | -0.111 | +0.163 |  | +2.1 / +0.6 |  |
| MES | 5 | eod | +0.438 | -0.566 .. +1.442 | +0.0072 | 0.39 / 0.36 / 0.38 | 0.381 |  |  | 10/16 | +0.037 | +0.837 |  | +8.2 / +0.9 |  |
| MES | 15 | h1 * | -0.008 | -0.018 .. +0.002 | -0.0017 | 0.13 / 0.12 / 0.1 | 0.103 | 1 | 1 | 9/16 | -0.015 | -0.001 | False | -1.5 / -1.5 |  |
| MES | 15 | h2 | +0.000 | -0.018 .. +0.019 | +0.0003 | 0.97 / 0.97 / 0.96 | 0.964 |  |  | 8/16 | -0.023 | +0.024 |  | +0.0 / +0.0 |  |
| MES | 15 | h4 | +0.008 | -0.033 .. +0.049 | +0.0012 | 0.71 / 0.71 / 0.67 | 0.678 |  |  | 8/16 | -0.045 | +0.060 |  | +0.6 / +0.4 | 0.051 |
| MES | 15 | h8 | +0.009 | -0.067 .. +0.085 | +0.0016 | 0.81 / 0.81 / 0.78 | 0.789 |  |  | 9/16 | -0.087 | +0.105 |  | +0.5 / +0.2 |  |
| MES | 15 | h16 | +0.050 | -0.084 .. +0.185 | +0.0054 | 0.46 / 0.45 / 0.45 | 0.452 |  |  | 10/16 | -0.100 | +0.200 |  | +2.3 / +0.7 |  |
| MES | 15 | eod | +0.347 | -0.263 .. +0.958 | +0.0119 | 0.26 / 0.24 / 0.22 | 0.222 |  |  | 10/16 | +0.058 | +0.635 |  | +6.2 / +1.1 |  |
| MES | 60 | h1 | -0.001 | -0.020 .. +0.019 | +0.0008 | 0.96 / 0.95 / 0.96 | 0.96 |  |  | 9/16 | -0.018 | +0.017 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 | -0.010 | -0.044 .. +0.025 | -0.0007 | 0.58 / 0.57 / 0.59 | 0.594 |  |  | 9/16 | -0.039 | +0.019 |  | -0.7 / -0.5 |  |
| MES | 60 | h4 | +0.003 | -0.059 .. +0.065 | +0.0016 | 0.93 / 0.93 / 0.92 | 0.929 |  |  | 8/16 | -0.042 | +0.047 |  | +0.1 / +0.1 | 0.087 |
| MES | 60 | h8 | +0.013 | -0.099 .. +0.125 | +0.0024 | 0.82 / 0.82 / 0.81 | 0.813 |  |  | 9/16 | -0.067 | +0.093 |  | +0.5 / +0.2 |  |
| MES | 60 | h16 * | +0.044 | -0.138 .. +0.226 | +0.0050 | 0.64 / 0.62 / 0.62 | 0.613 | 1 | 1 | 9/16 | -0.036 | +0.125 | False | +1.3 / +0.5 |  |
| MES | 60 | eod | +0.028 | -0.171 .. +0.227 | +0.0031 | 0.78 / 0.78 / 0.78 | 0.776 |  |  | 7/16 | -0.014 | +0.069 |  | +0.8 / +0.3 |  |
| MNQ | 5 | h1 | +0.006 | -0.001 .. +0.012 | +0.0016 | 0.074 / 0.067 / 0.072 | 0.0695 |  |  | 10/16 | -0.004 | +0.015 |  | +1.7 / +1.8 |  |
| MNQ | 5 | h2 | +0.014 | -0.002 .. +0.029 | +0.0025 | 0.092 / 0.078 / 0.042 | 0.0425 |  |  | 11/16 | -0.007 | +0.034 |  | +2.3 / +1.7 |  |
| MNQ | 5 | h4 | +0.029 | -0.001 .. +0.059 | +0.0035 | 0.061 / 0.051 / 0.032 | 0.0341 |  |  | 10/16 | -0.009 | +0.066 |  | +3.2 / +1.9 | 0.034 |
| MNQ | 5 | h8 * | +0.048 | +0.000 .. +0.097 | +0.0041 | 0.049 / 0.043 / 0.075 | 0.0748 | 1 | 1 | 10/16 | -0.012 | +0.108 | False | +4.4 / +2.0 |  |
| MNQ | 5 | h16 | +0.087 | -0.000 .. +0.175 | +0.0054 | 0.05 / 0.047 / 0.091 | 0.0893 |  |  | 11/16 | -0.003 | +0.177 |  | +6.2 / +2.0 |  |
| MNQ | 5 | eod | +0.880 | -0.339 .. +2.099 | +0.0107 | 0.16 / 0.15 / 0.16 | 0.157 |  |  | 10/16 | +1.091 | +0.671 |  | +12.6 / +1.4 |  |
| MNQ | 15 | h1 | +0.006 | -0.004 .. +0.015 | +0.0004 | 0.22 / 0.22 / 0.34 | 0.332 |  |  | 10/16 | -0.003 | +0.014 |  | +1.1 / +1.2 |  |
| MNQ | 15 | h2 | +0.012 | -0.007 .. +0.031 | +0.0017 | 0.21 / 0.2 / 0.34 | 0.338 |  |  | 10/16 | -0.003 | +0.027 |  | +1.6 / +1.3 |  |
| MNQ | 15 | h4 * | +0.026 | -0.012 .. +0.063 | +0.0029 | 0.18 / 0.17 / 0.31 | 0.299 | 1 | 1 | 10/16 | -0.004 | +0.055 | False | +2.4 / +1.4 | 0.059 |
| MNQ | 15 | h8 | +0.034 | -0.037 .. +0.104 | +0.0041 | 0.35 / 0.35 / 0.43 | 0.421 |  |  | 10/16 | -0.014 | +0.081 |  | +2.2 / +0.9 |  |
| MNQ | 15 | h16 | +0.037 | -0.093 .. +0.168 | +0.0067 | 0.58 / 0.58 / 0.63 | 0.629 |  |  | 11/16 | -0.036 | +0.110 |  | +1.7 / +0.6 |  |
| MNQ | 15 | eod | +0.401 | -0.171 .. +0.972 | +0.0120 | 0.17 / 0.17 / 0.24 | 0.238 |  |  | 10/16 | +0.512 | +0.289 |  | +6.9 / +1.4 |  |
| MNQ | 60 | h1 * | +0.018 | -0.003 .. +0.039 | +0.0046 | 0.088 / 0.085 / 0.082 | 0.0815 | 1 | 1 | 9/16 | +0.007 | +0.029 | False | +1.7 / +1.7 |  |
| MNQ | 60 | h2 | +0.014 | -0.023 .. +0.052 | +0.0036 | 0.45 / 0.44 / 0.45 | 0.454 |  |  | 9/16 | -0.005 | +0.034 |  | +1.0 / +0.7 |  |
| MNQ | 60 | h4 | +0.022 | -0.040 .. +0.085 | +0.0063 | 0.49 / 0.49 / 0.51 | 0.514 |  |  | 9/16 | +0.001 | +0.044 |  | +1.1 / +0.7 | 0.093 |
| MNQ | 60 | h8 | +0.040 | -0.067 .. +0.147 | +0.0064 | 0.46 / 0.47 / 0.48 | 0.479 |  |  | 9/16 | +0.021 | +0.059 |  | +1.5 / +0.7 |  |
| MNQ | 60 | h16 | +0.086 | -0.090 .. +0.263 | +0.0085 | 0.34 / 0.34 / 0.36 | 0.352 |  |  | 9/16 | +0.121 | +0.052 |  | +2.4 / +1.0 |  |
| MNQ | 60 | eod | +0.079 | -0.115 .. +0.273 | +0.0065 | 0.43 / 0.43 / 0.44 | 0.443 |  |  | 9/16 | +0.149 | +0.010 |  | +2.1 / +0.8 |  |
| MYM | 5 | h1 | +0.005 | -0.005 .. +0.015 | +0.0010 | 0.36 / 0.33 / 0.29 | 0.286 |  |  | 3/8 | n/a | +0.005 |  | +1.0 / +0.9 |  |
| MYM | 5 | h2 | +0.021 | -0.009 .. +0.051 | +0.0036 | 0.17 / 0.16 / 0.039 | 0.0342 |  |  | 2/8 | n/a | +0.021 |  | +2.2 / +1.4 |  |
| MYM | 5 | h4 | +0.051 | -0.014 .. +0.117 | +0.0059 | 0.12 / 0.12 / 0.022 | 0.0205 |  |  | 3/8 | n/a | +0.051 |  | +3.2 / +1.5 | 0.052 |
| MYM | 5 | h8 | +0.088 | -0.014 .. +0.191 | +0.0076 | 0.091 / 0.09 / 0.036 | 0.0332 |  |  | 4/8 | n/a | +0.088 |  | +4.4 / +1.7 |  |
| MYM | 5 | h16 * | +0.145 | -0.004 .. +0.294 | +0.0104 | 0.057 / 0.056 / 0.047 | 0.0479 | 1 | 1 | 5/8 | n/a | +0.145 | False | +6.6 / +1.9 |  |
| MYM | 5 | eod | +1.194 | -0.492 .. +2.880 | +0.0157 | 0.16 / 0.14 / 0.15 | 0.154 |  |  | 6/8 | n/a | +1.194 |  | +12.9 / +1.4 |  |
| MYM | 15 | h1 * | +0.011 | -0.008 .. +0.031 | +0.0040 | 0.25 / 0.22 / 0.11 | 0.111 | 1 | 1 | 2/8 | n/a | +0.011 | False | +1.2 / +1.1 |  |
| MYM | 15 | h2 | +0.018 | -0.011 .. +0.048 | +0.0053 | 0.23 / 0.2 / 0.28 | 0.276 |  |  | 4/8 | n/a | +0.018 |  | +1.4 / +1.2 |  |
| MYM | 15 | h4 | +0.021 | -0.030 .. +0.072 | +0.0057 | 0.41 / 0.41 / 0.53 | 0.53 |  |  | 4/8 | n/a | +0.021 |  | +1.2 / +0.8 | 0.077 |
| MYM | 15 | h8 | +0.038 | -0.059 .. +0.134 | +0.0082 | 0.44 / 0.44 / 0.55 | 0.543 |  |  | 4/8 | n/a | +0.038 |  | +1.7 / +0.8 |  |
| MYM | 15 | h16 | +0.090 | -0.090 .. +0.270 | +0.0114 | 0.33 / 0.32 / 0.45 | 0.462 |  |  | 4/8 | n/a | +0.090 |  | +3.0 / +1.0 |  |
| MYM | 15 | eod | +0.532 | -0.293 .. +1.357 | +0.0151 | 0.21 / 0.18 / 0.25 | 0.254 |  |  | 6/8 | n/a | +0.532 |  | +6.9 / +1.3 |  |
| MYM | 60 | h1 | +0.010 | -0.017 .. +0.037 | +0.0037 | 0.48 / 0.47 / 0.48 | 0.492 |  |  | 5/8 | n/a | +0.010 |  | +0.7 / +0.7 |  |
| MYM | 60 | h2 | +0.010 | -0.039 .. +0.059 | +0.0056 | 0.68 / 0.68 / 0.68 | 0.683 |  |  | 5/8 | n/a | +0.010 |  | +0.5 / +0.4 |  |
| MYM | 60 | h4 | +0.029 | -0.056 .. +0.115 | +0.0092 | 0.5 / 0.49 / 0.5 | 0.516 |  |  | 5/8 | n/a | +0.029 |  | +1.1 / +0.7 | 0.127 |
| MYM | 60 | h8 | +0.070 | -0.089 .. +0.229 | +0.0099 | 0.39 / 0.38 / 0.35 | 0.357 |  |  | 6/8 | n/a | +0.070 |  | +1.9 / +0.9 |  |
| MYM | 60 | h16 * | +0.143 | -0.122 .. +0.408 | +0.0139 | 0.29 / 0.27 / 0.26 | 0.261 | 1 | 1 | 6/8 | n/a | +0.143 | False | +2.9 / +1.1 |  |
| MYM | 60 | eod | +0.110 | -0.182 .. +0.402 | +0.0107 | 0.46 / 0.44 / 0.43 | 0.447 |  |  | 6/8 | n/a | +0.110 |  | +2.1 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.040 | -0.045 .. -0.036 | -8.1% | -0.035 | 1.1e-68 | 1.4e-65 | 16/16 |
| MES | 5 | h2 | -0.069 | -0.080 .. -0.058 | -9.8% | -0.071 | 9.2e-34 |  | 16/16 |
| MES | 5 | h4 | -0.100 | -0.124 .. -0.077 | -10.1% | -0.124 | 5.6e-17 |  | 15/16 |
| MES | 5 | h8 | -0.134 | -0.179 .. -0.089 | -9.3% | -0.184 | 4.2e-09 |  | 15/16 |
| MES | 5 | h16 | -0.151 | -0.223 .. -0.080 | -7.2% | -0.236 | 3.2e-05 |  | 14/16 |
| MES | 5 | eod | +0.052 | -0.636 .. +0.741 | +0.5% | +0.458 | 0.88 |  | 8/16 |
| MES | 15 | h1 * | -0.060 | -0.069 .. -0.052 | -11.8% | -0.088 | 9.1e-46 | 8.94e-43 | 16/16 |
| MES | 15 | h2 | -0.089 | -0.114 .. -0.065 | -12.3% | -0.139 | 1.3e-12 |  | 16/16 |
| MES | 15 | h4 | -0.114 | -0.167 .. -0.060 | -10.8% | -0.195 | 2.9e-05 |  | 16/16 |
| MES | 15 | h8 | -0.140 | -0.228 .. -0.051 | -9.1% | -0.269 | 0.0019 |  | 14/16 |
| MES | 15 | h16 | -0.104 | -0.202 .. -0.006 | -4.6% | -0.311 | 0.038 |  | 10/16 |
| MES | 15 | eod | -0.118 | -0.565 .. +0.329 | -2.2% | +0.044 | 0.6 |  | 9/16 |
| MES | 60 | h1 * | -0.099 | -0.113 .. -0.084 | -19.2% | -0.182 | 2.2e-40 | 1.97e-37 | 16/16 |
| MES | 60 | h2 | -0.125 | -0.149 .. -0.102 | -16.9% | -0.235 | 4.8e-26 |  | 16/16 |
| MES | 60 | h4 | -0.154 | -0.194 .. -0.114 | -14.5% | -0.282 | 6.9e-14 |  | 15/16 |
| MES | 60 | h8 | -0.217 | -0.284 .. -0.150 | -14.4% | -0.344 | 2e-10 |  | 16/16 |
| MES | 60 | h16 | -0.232 | -0.342 .. -0.122 | -11.3% | -0.357 | 3.5e-05 |  | 13/16 |
| MES | 60 | eod | -0.241 | -0.366 .. -0.115 | -11.1% | -0.365 | 0.00016 |  | 12/16 |
| MNQ | 5 | h1 * | -0.031 | -0.037 .. -0.025 | -5.8% | -0.027 | 1.8e-22 | 1.05e-19 | 15/16 |
| MNQ | 5 | h2 | -0.053 | -0.068 .. -0.037 | -6.9% | -0.046 | 2.9e-11 |  | 15/16 |
| MNQ | 5 | h4 | -0.078 | -0.109 .. -0.048 | -7.1% | -0.077 | 5.8e-07 |  | 15/16 |
| MNQ | 5 | h8 | -0.096 | -0.139 .. -0.053 | -5.9% | -0.112 | 1.7e-05 |  | 15/16 |
| MNQ | 5 | h16 | -0.098 | -0.157 .. -0.039 | -4.1% | -0.145 | 0.0055 |  | 12/16 |
| MNQ | 5 | eod | +0.813 | -0.013 .. +1.639 | +6.5% | +1.205 | 0.086 |  | 10/16 |
| MNQ | 15 | h1 * | -0.056 | -0.064 .. -0.047 | -10.4% | -0.077 | 4.2e-32 | 3.21e-29 | 16/16 |
| MNQ | 15 | h2 | -0.074 | -0.089 .. -0.060 | -9.6% | -0.109 | 1.4e-11 |  | 15/16 |
| MNQ | 15 | h4 | -0.088 | -0.111 .. -0.065 | -7.8% | -0.137 | 0.00016 |  | 15/16 |
| MNQ | 15 | h8 | -0.092 | -0.132 .. -0.052 | -5.5% | -0.154 | 0.011 |  | 14/16 |
| MNQ | 15 | h16 | -0.034 | -0.106 .. +0.039 | -1.3% | -0.115 | 0.45 |  | 10/16 |
| MNQ | 15 | eod | +0.337 | -0.022 .. +0.697 | +5.3% | +0.461 | 0.18 |  | 10/16 |
| MNQ | 60 | h1 * | -0.091 | -0.105 .. -0.077 | -17.2% | -0.163 | 1.4e-36 | 1.19e-33 | 16/16 |
| MNQ | 60 | h2 | -0.113 | -0.136 .. -0.089 | -14.6% | -0.202 | 4.7e-21 |  | 16/16 |
| MNQ | 60 | h4 | -0.121 | -0.159 .. -0.082 | -10.9% | -0.225 | 7.8e-10 |  | 16/16 |
| MNQ | 60 | h8 | -0.153 | -0.216 .. -0.091 | -9.6% | -0.257 | 1.5e-06 |  | 14/16 |
| MNQ | 60 | h16 | -0.105 | -0.206 .. -0.005 | -4.8% | -0.229 | 0.053 |  | 9/16 |
| MNQ | 60 | eod | -0.092 | -0.206 .. +0.022 | -4.0% | -0.226 | 0.14 |  | 9/16 |
| MYM | 5 | h1 * | -0.025 | -0.034 .. -0.016 | -4.7% | -0.029 | 3.3e-08 | 9.22e-06 | 8/8 |
| MYM | 5 | h2 | -0.052 | -0.081 .. -0.024 | -6.9% | -0.050 | 0.00054 |  | 8/8 |
| MYM | 5 | h4 | -0.082 | -0.145 .. -0.019 | -7.5% | -0.088 | 0.014 |  | 6/8 |
| MYM | 5 | h8 | -0.112 | -0.214 .. -0.010 | -7.1% | -0.134 | 0.037 |  | 6/8 |
| MYM | 5 | h16 | -0.082 | -0.198 .. +0.035 | -3.5% | -0.140 | 0.2 |  | 5/8 |
| MYM | 5 | eod | +1.052 | -0.014 .. +2.117 | +9.0% | +2.204 | 0.053 |  | 6/8 |
| MYM | 15 | h1 * | -0.057 | -0.075 .. -0.039 | -10.7% | -0.094 | 7.6e-10 | 2.31e-07 | 8/8 |
| MYM | 15 | h2 | -0.077 | -0.106 .. -0.047 | -10.1% | -0.126 | 9.3e-07 |  | 8/8 |
| MYM | 15 | h4 | -0.091 | -0.138 .. -0.044 | -8.2% | -0.164 | 0.0071 |  | 7/8 |
| MYM | 15 | h8 | -0.085 | -0.155 .. -0.015 | -5.2% | -0.184 | 0.21 |  | 6/8 |
| MYM | 15 | h16 | -0.042 | -0.150 .. +0.067 | -1.7% | -0.105 | 0.81 |  | 6/8 |
| MYM | 15 | eod | +0.287 | -0.214 .. +0.789 | +4.8% | +0.650 | 0.29 |  | 5/8 |
| MYM | 60 | h1 * | -0.089 | -0.110 .. -0.068 | -17.0% | -0.161 | 4.9e-17 | 2.25e-14 | 8/8 |
| MYM | 60 | h2 | -0.100 | -0.134 .. -0.067 | -13.2% | -0.199 | 5e-09 |  | 7/8 |
| MYM | 60 | h4 | -0.137 | -0.192 .. -0.081 | -12.6% | -0.233 | 1.3e-06 |  | 8/8 |
| MYM | 60 | h8 | -0.177 | -0.266 .. -0.088 | -11.4% | -0.273 | 0.00037 |  | 7/8 |
| MYM | 60 | h16 | -0.139 | -0.292 .. +0.013 | -6.6% | -0.245 | 0.09 |  | 5/8 |
| MYM | 60 | eod | -0.150 | -0.328 .. +0.027 | -6.7% | -0.263 | 0.12 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.84 pts | -1.48 .. -0.21 | 0.025 |
| MES | 15 | -1.17 pts | -2.25 .. -0.08 | 0.035 |
| MES | 60 | +0.55 pts | -1.36 .. +2.46 | 0.61 |
| MNQ | 5 | -0.13 pts | -0.75 .. +0.49 | 0.91 |
| MNQ | 15 | +0.38 pts | -0.74 .. +1.50 | 0.51 |
| MNQ | 60 | +1.40 pts | -0.46 .. +3.26 | 0.14 |
| MYM | 5 | +0.32 pts | -0.56 .. +1.20 | 0.48 |
| MYM | 15 | +0.89 pts | -0.55 .. +2.34 | 0.23 |
| MYM | 60 | +2.67 pts | +0.10 .. +5.23 | 0.06 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom level | long | 128071 | +0.003 | 0.239 | +0.09 | -3.41 | -3.47 | -3.35 | -3.41 |
| MES | 5 | h2 | bottom level | long | 128071 | +0.004 | 0.239 | +0.15 | -3.35 | -3.43 | -3.27 | -3.38 |
| MES | 5 | h4 | top level | long | 229052 | +0.011 | 0.403 | +0.11 | -3.39 | -3.47 | -3.31 | -3.44 |
| MES | 5 | h8 | top level | long | 229052 | +0.028 | 0.403 | +0.24 | -3.26 | -3.40 | -3.12 | -3.38 |
| MES | 5 | h16 | top level | long | 229052 | +0.059 | 0.403 | +0.45 | -3.05 | -3.31 | -2.81 | -3.33 |
| MES | 5 | eod | top level | long | 229052 | +0.574 | 0.403 | +3.82 | +0.32 | -0.63 | +1.23 | -1.75 |
| MES | 15 | h1 | bottom level | long | 43087 | +0.010 | 0.143 | +0.21 | -3.29 | -3.39 | -3.19 | -3.36 |
| MES | 15 | h2 | top level | long | 76804 | +0.011 | 0.227 | +0.17 | -3.33 | -3.44 | -3.21 | -3.44 |
| MES | 15 | h4 | top level | long | 76804 | +0.026 | 0.227 | +0.36 | -3.14 | -3.36 | -2.93 | -3.35 |
| MES | 15 | h8 | top level | long | 76804 | +0.046 | 0.227 | +0.56 | -2.94 | -3.25 | -2.65 | -3.34 |
| MES | 15 | h16 | top level | long | 76804 | +0.108 | 0.227 | +1.49 | -2.01 | -2.83 | -1.22 | -2.65 |
| MES | 15 | eod | top level | long | 76804 | +0.335 | 0.227 | +3.78 | +0.28 | -0.68 | +1.21 | -1.32 |
| MES | 60 | h1 | bottom level | long | 10972 | +0.009 | 0.079 | +0.46 | -3.04 | -2.94 | -3.13 | -3.24 |
| MES | 60 | h2 | bottom level | long | 10972 | +0.026 | 0.079 | +1.34 | -2.16 | -2.18 | -2.14 | -2.61 |
| MES | 60 | h4 | top level | long | 19395 | +0.045 | 0.109 | +1.49 | -2.01 | -2.75 | -1.28 | -2.93 |
| MES | 60 | h8 | top level | long | 19395 | +0.071 | 0.109 | +2.77 | -0.73 | -2.05 | +0.56 | -2.45 |
| MES | 60 | h16 | top level | long | 19395 | +0.107 | 0.109 | +3.62 | +0.12 | -1.06 | +1.26 | -2.61 |
| MES | 60 | eod | top level | long | 19395 | +0.115 | 0.109 | +3.46 | -0.04 | -0.58 | +0.49 | -3.26 |
| MNQ | 5 | h1 | top level | long | 233967 | +0.007 | 0.166 | +0.08 | -1.92 | -1.99 | -1.84 | -1.94 |
| MNQ | 5 | h2 | top level | long | 233967 | +0.015 | 0.166 | +0.18 | -1.82 | -1.96 | -1.68 | -1.85 |
| MNQ | 5 | h4 | top level | long | 233967 | +0.032 | 0.166 | +0.33 | -1.67 | -1.90 | -1.44 | -1.72 |
| MNQ | 5 | h8 | top level | long | 233967 | +0.067 | 0.166 | +0.64 | -1.36 | -1.78 | -0.92 | -1.49 |
| MNQ | 5 | h16 | top level | long | 233967 | +0.136 | 0.166 | +1.27 | -0.73 | -1.55 | +0.13 | -1.04 |
| MNQ | 5 | eod | top level | long | 233967 | +0.972 | 0.166 | +4.77 | +2.77 | +1.63 | +3.94 | -0.01 |
| MNQ | 15 | h1 | top level | long | 78467 | +0.011 | 0.092 | +0.25 | -1.75 | -1.92 | -1.58 | -1.88 |
| MNQ | 15 | h2 | top level | long | 78467 | +0.024 | 0.092 | +0.46 | -1.54 | -1.82 | -1.24 | -1.71 |
| MNQ | 15 | h4 | top level | long | 78467 | +0.047 | 0.092 | +0.97 | -1.03 | -1.67 | -0.37 | -1.36 |
| MNQ | 15 | h8 | top level | long | 78467 | +0.087 | 0.092 | +1.74 | -0.26 | -1.35 | +0.88 | -0.95 |
| MNQ | 15 | h16 | top level | long | 78467 | +0.151 | 0.092 | +3.25 | +1.25 | -0.86 | +3.43 | +0.39 |
| MNQ | 15 | eod | top level | long | 78467 | +0.523 | 0.092 | +4.82 | +2.82 | +1.57 | +4.12 | +0.88 |
| MNQ | 60 | h1 | top level | long | 19786 | +0.023 | 0.044 | +0.95 | -1.05 | -1.61 | -0.47 | -1.45 |
| MNQ | 60 | h2 | top level | long | 19786 | +0.039 | 0.044 | +1.57 | -0.43 | -1.32 | +0.50 | -1.22 |
| MNQ | 60 | h4 | top level | long | 19786 | +0.077 | 0.044 | +3.02 | +1.02 | -0.76 | +2.89 | -0.47 |
| MNQ | 60 | h8 | top level | long | 19786 | +0.114 | 0.044 | +3.93 | +1.93 | +0.13 | +3.81 | -0.71 |
| MNQ | 60 | h16 | top level | long | 19786 | +0.178 | 0.044 | +4.21 | +2.21 | +1.15 | +3.31 | -1.96 |
| MNQ | 60 | eod | top level | long | 19786 | +0.191 | 0.044 | +4.14 | +2.14 | +1.54 | +2.78 | -2.87 |
| MYM | 5 | h1 | top level | long | 107872 | +0.001 | 0.205 | -0.01 | -2.01 | +nan | -2.01 | -2.00 |
| MYM | 5 | h2 | top level | long | 107872 | +0.004 | 0.205 | +0.01 | -1.99 | +nan | -1.99 | -1.96 |
| MYM | 5 | h4 | top level | long | 107872 | +0.012 | 0.205 | +0.03 | -1.97 | +nan | -1.97 | -1.90 |
| MYM | 5 | h8 | top level | long | 107872 | +0.027 | 0.205 | +0.09 | -1.91 | +nan | -1.91 | -1.81 |
| MYM | 5 | h16 | top level | long | 107872 | +0.060 | 0.205 | +0.25 | -1.75 | +nan | -1.75 | -1.69 |
| MYM | 5 | eod | top level | long | 107872 | +0.699 | 0.205 | +4.37 | +2.37 | +nan | +2.37 | +1.68 |
| MYM | 15 | h1 | top level | long | 36199 | +0.004 | 0.113 | -0.01 | -2.01 | +nan | -2.01 | -2.04 |
| MYM | 15 | h2 | top level | long | 36199 | +0.010 | 0.113 | +0.03 | -1.97 | +nan | -1.97 | -1.97 |
| MYM | 15 | h4 | top level | long | 36199 | +0.020 | 0.113 | +0.19 | -1.81 | +nan | -1.81 | -1.80 |
| MYM | 15 | h8 | top level | long | 36199 | +0.034 | 0.113 | +0.32 | -1.68 | +nan | -1.68 | -1.61 |
| MYM | 15 | h16 | top level | long | 36199 | +0.105 | 0.113 | +1.47 | -0.53 | +nan | -0.53 | -0.15 |
| MYM | 15 | eod | top level | long | 36199 | +0.371 | 0.113 | +4.25 | +2.25 | +nan | +2.25 | +2.40 |
| MYM | 60 | h1 | top level | long | 9128 | +0.010 | 0.054 | +0.31 | -1.69 | +nan | -1.69 | -1.83 |
| MYM | 60 | h2 | top level | long | 9128 | +0.015 | 0.054 | +0.27 | -1.73 | +nan | -1.73 | -1.99 |
| MYM | 60 | h4 | top level | long | 9128 | +0.044 | 0.054 | +1.19 | -0.81 | +nan | -0.81 | -1.31 |
| MYM | 60 | h8 | top level | long | 9128 | +0.076 | 0.054 | +2.85 | +0.85 | +nan | +0.85 | -0.05 |
| MYM | 60 | h16 | top level | long | 9128 | +0.101 | 0.054 | +3.69 | +1.69 | +nan | +1.69 | +0.32 |
| MYM | 60 | eod | top level | long | 9128 | +0.104 | 0.054 | +3.57 | +1.57 | +nan | +1.57 | -0.31 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.068 | +0.040 | +0.017 | +0.009 | +0.004 | +0.000 | +0.002 | +0.003 | +0.006 | +0.019 | +0.041 |
| MES | 15 | -0.983 | -1.203 | -0.890 | -0.451 | -0.187 | +0.000 | -0.000 | +0.007 | +0.015 | +0.013 | +0.005 |
| MES | 60 | -2.150 | -1.992 | -1.738 | -1.304 | -0.754 | +0.000 | +0.000 | -0.008 | +0.003 | -0.011 | +0.035 |
| MNQ | 5 | +0.085 | +0.044 | +0.016 | +0.007 | +0.003 | +0.000 | +0.004 | +0.009 | +0.019 | +0.033 | +0.066 |
| MNQ | 15 | -1.060 | -1.253 | -0.916 | -0.468 | -0.192 | +0.000 | +0.006 | +0.014 | +0.032 | +0.036 | -0.000 |
| MNQ | 60 | -2.232 | -2.057 | -1.776 | -1.327 | -0.762 | +0.000 | +0.013 | +0.009 | +0.006 | +0.019 | +0.157 |
| MYM | 5 | +0.046 | +0.031 | +0.012 | +0.008 | +0.003 | +0.000 | +0.005 | +0.012 | +0.025 | +0.036 | +0.067 |
| MYM | 15 | -1.071 | -1.293 | -0.949 | -0.481 | -0.201 | +0.000 | +0.017 | +0.021 | +0.023 | +0.021 | +0.059 |
| MYM | 60 | -2.202 | -2.041 | -1.774 | -1.334 | -0.774 | +0.000 | +0.007 | +0.007 | +0.019 | +0.027 | +0.071 |

## Calibration

- MES 5-min: 1034349 bars, 229052 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 340296 bars, 76804 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81614 bars, 19395 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1032600 bars, 233967 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340140 bars, 78467 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81612 bars, 19786 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518078 bars, 107872 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170466 bars, 36199 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40755 bars, 9128 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
