# Impact card: prior_day_range

prior session's range / its 20-session average [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -1.216 R20 over the rest of the session (to 16:45), p=0.44; we would catch an effect of 0.025 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.014 R20, CONFIRMED, q=2.42e-08, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $10.17 at recent bar sizes, 90% range up to $0.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.798 R20 over the rest of the session (to 16:45), p=0.28; we would catch an effect of 0.049 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $11.67 at recent bar sizes, 90% range up to $1.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.210 R20 over the rest of the session (to 16:45), p=0.89; we would catch an effect of 0.098 R20 or more 80% of the time).
- MES 60-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.029 R20, CONFIRMED, q=0.00111, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $6.20 at recent bar sizes, 90% range up to $5.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -1.454 R20 over the rest of the session (to 16:45), p=0.5; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.29).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $19.39 at recent bar sizes, 90% range up to $1.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.971 R20 over the rest of the session (to 16:45), p=0.46; we would catch an effect of 0.066 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.025).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $22.70 at recent bar sizes, 90% range up to $3.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.160 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.103 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.051 R20, CONFIRMED, q=3.98e-12, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.51 at recent bar sizes, 90% range up to $7.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -1.344 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.059 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.48 at recent bar sizes, 90% range up to $1.25); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.945 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.079 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.57 at recent bar sizes, 90% range up to $2.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.183 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.142 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.15).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.17 at recent bar sizes, 90% range up to $5.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.004 .. +0.004 | +0.0009 | 0.92 / 0.92 / 0.92 | 0.907 |  |  | 6/16 | +0.001 | -0.001 |  | -0.1 / -0.1 |  |
| MES | 5 | h2 | -0.003 | -0.012 .. +0.006 | +0.0003 | 0.51 / 0.51 / 0.51 | 0.511 |  |  | 5/16 | -0.000 | -0.006 |  | -0.9 / -0.7 |  |
| MES | 5 | h4 | -0.009 | -0.029 .. +0.010 | -0.0004 | 0.35 / 0.35 / 0.33 | 0.327 |  |  | 6/16 | -0.003 | -0.016 |  | -1.8 / -0.9 | 0.025 |
| MES | 5 | h8 | -0.023 | -0.064 .. +0.017 | -0.0011 | 0.26 / 0.26 / 0.24 | 0.232 |  |  | 9/16 | -0.010 | -0.037 |  | -3.2 / -1.1 |  |
| MES | 5 | h16 | -0.058 | -0.137 .. +0.021 | -0.0024 | 0.15 / 0.15 / 0.16 | 0.15 |  |  | 9/16 | -0.035 | -0.080 |  | -5.6 / -1.4 |  |
| MES | 5 | eod * | -1.216 | -2.455 .. +0.023 | -0.0160 | 0.054 / 0.055 / 0.079 | 0.0834 | 1 | 1 | 12/16 | -0.750 | -1.676 | False | -24.9 / -1.9 |  |
| MES | 15 | h1 | -0.001 | -0.008 .. +0.007 | +0.0011 | 0.81 / 0.82 / 0.83 | 0.823 |  |  | 8/16 | -0.002 | +0.001 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.009 | -0.024 .. +0.007 | -0.0005 | 0.28 / 0.28 / 0.33 | 0.321 |  |  | 9/16 | -0.005 | -0.012 |  | -1.3 / -1.1 |  |
| MES | 15 | h4 | -0.024 | -0.059 .. +0.010 | -0.0020 | 0.17 / 0.17 / 0.18 | 0.187 |  |  | 10/16 | -0.012 | -0.036 |  | -2.3 / -1.4 | 0.049 |
| MES | 15 | h8 | -0.056 | -0.125 .. +0.013 | -0.0037 | 0.11 / 0.12 / 0.14 | 0.133 |  |  | 10/16 | -0.032 | -0.080 |  | -3.9 / -1.6 |  |
| MES | 15 | h16 | -0.124 | -0.271 .. +0.022 | -0.0064 | 0.097 / 0.097 / 0.11 | 0.111 |  |  | 9/16 | -0.061 | -0.187 |  | -6.4 / -1.7 |  |
| MES | 15 | eod * | -0.798 | -1.586 .. -0.010 | -0.0209 | 0.047 / 0.045 / 0.043 | 0.0492 | 1 | 1 | 12/16 | -0.469 | -1.122 | False | -15.1 / -2.0 |  |
| MES | 60 | h1 | -0.005 | -0.021 .. +0.010 | +0.0013 | 0.5 / 0.52 / 0.56 | 0.558 |  |  | 10/16 | -0.010 | -0.001 |  | -0.6 / -0.7 |  |
| MES | 60 | h2 | -0.016 | -0.047 .. +0.015 | -0.0003 | 0.31 / 0.32 / 0.38 | 0.379 |  |  | 9/16 | -0.026 | -0.006 |  | -1.3 / -1.0 |  |
| MES | 60 | h4 | -0.038 | -0.099 .. +0.023 | -0.0022 | 0.22 / 0.24 / 0.3 | 0.288 |  |  | 10/16 | -0.059 | -0.017 |  | -2.3 / -1.2 | 0.098 |
| MES | 60 | h8 | -0.083 | -0.202 .. +0.036 | -0.0045 | 0.17 / 0.19 / 0.24 | 0.226 |  |  | 10/16 | -0.113 | -0.053 |  | -3.6 / -1.4 |  |
| MES | 60 | h16 | -0.159 | -0.377 .. +0.059 | -0.0089 | 0.15 / 0.16 / 0.21 | 0.196 |  |  | 10/16 | -0.210 | -0.108 |  | -5.3 / -1.4 |  |
| MES | 60 | eod * | -0.210 | -0.456 .. +0.035 | -0.0137 | 0.093 / 0.1 / 0.14 | 0.138 | 1 | 1 | 10/16 | -0.263 | -0.158 | False | -6.7 / -1.7 |  |
| MNQ | 5 | h1 | -0.004 | -0.011 .. +0.003 | -0.0014 | 0.27 / 0.25 / 0.17 | 0.169 |  |  | 8/16 | -0.001 | -0.006 |  | -1.3 / -1.1 |  |
| MNQ | 5 | h2 | -0.012 | -0.031 .. +0.007 | -0.0029 | 0.21 / 0.19 / 0.057 | 0.0602 |  |  | 11/16 | -0.004 | -0.019 |  | -2.2 / -1.2 |  |
| MNQ | 5 | h4 | -0.027 | -0.070 .. +0.016 | -0.0046 | 0.21 / 0.19 / 0.043 | 0.0414 |  |  | 10/16 | -0.010 | -0.045 |  | -3.1 / -1.2 | 0.032 |
| MNQ | 5 | h8 | -0.053 | -0.140 .. +0.033 | -0.0064 | 0.23 / 0.21 / 0.053 | 0.0542 |  |  | 8/16 | -0.019 | -0.087 |  | -4.3 / -1.2 |  |
| MNQ | 5 | h16 | -0.098 | -0.256 .. +0.059 | -0.0082 | 0.22 / 0.2 / 0.071 | 0.0727 |  |  | 8/16 | -0.044 | -0.152 |  | -5.8 / -1.2 |  |
| MNQ | 5 | eod * | -1.454 | -3.104 .. +0.195 | -0.0202 | 0.084 / 0.08 / 0.088 | 0.0865 | 1 | 1 | 12/16 | -1.614 | -1.297 | False | -20.1 / -1.7 |  |
| MNQ | 15 | h1 | -0.002 | -0.011 .. +0.007 | -0.0002 | 0.64 / 0.64 / 0.7 | 0.702 |  |  | 8/16 | -0.003 | -0.001 |  | -0.5 / -0.5 |  |
| MNQ | 15 | h2 | -0.016 | -0.046 .. +0.014 | -0.0034 | 0.31 / 0.29 / 0.19 | 0.204 |  |  | 8/16 | -0.008 | -0.024 |  | -1.6 / -1.0 |  |
| MNQ | 15 | h4 | -0.037 | -0.106 .. +0.031 | -0.0049 | 0.29 / 0.27 / 0.16 | 0.165 |  |  | 8/16 | -0.017 | -0.057 |  | -2.0 / -1.1 | 0.066 |
| MNQ | 15 | h8 | -0.058 | -0.170 .. +0.053 | -0.0059 | 0.3 / 0.29 / 0.22 | 0.229 |  |  | 8/16 | -0.039 | -0.077 |  | -2.4 / -1.0 |  |
| MNQ | 15 | h16 | -0.108 | -0.326 .. +0.111 | -0.0102 | 0.34 / 0.32 / 0.25 | 0.257 |  |  | 7/16 | -0.066 | -0.149 |  | -3.7 / -1.0 |  |
| MNQ | 15 | eod * | -0.971 | -2.047 .. +0.104 | -0.0253 | 0.077 / 0.069 / 0.04 | 0.0425 | 1 | 1 | 12/16 | -0.889 | -1.052 | False | -10.9 / -1.8 |  |
| MNQ | 60 | h1 | -0.002 | -0.019 .. +0.016 | -0.0002 | 0.86 / 0.86 / 0.86 | 0.861 |  |  | 7/16 | -0.011 | +0.008 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h2 | -0.008 | -0.042 .. +0.027 | -0.0017 | 0.66 / 0.67 / 0.68 | 0.681 |  |  | 8/16 | -0.029 | +0.014 |  | -0.6 / -0.4 |  |
| MNQ | 60 | h4 | -0.023 | -0.091 .. +0.045 | -0.0041 | 0.51 / 0.52 / 0.54 | 0.529 |  |  | 8/16 | -0.065 | +0.019 |  | -1.3 / -0.7 | 0.103 |
| MNQ | 60 | h8 | -0.054 | -0.184 .. +0.077 | -0.0067 | 0.42 / 0.43 / 0.46 | 0.452 |  |  | 8/16 | -0.127 | +0.019 |  | -2.2 / -0.8 |  |
| MNQ | 60 | h16 | -0.110 | -0.346 .. +0.126 | -0.0114 | 0.36 / 0.38 / 0.4 | 0.391 |  |  | 7/16 | -0.247 | +0.026 |  | -3.4 / -0.9 |  |
| MNQ | 60 | eod * | -0.160 | -0.419 .. +0.099 | -0.0166 | 0.23 / 0.24 / 0.27 | 0.258 | 1 | 1 | 8/16 | -0.322 | +0.001 | False | -4.8 / -1.2 |  |
| MYM | 5 | h1 | -0.004 | -0.016 .. +0.009 | -0.0008 | 0.56 / 0.56 / 0.39 | 0.386 |  |  | 3/8 | n/a | -0.004 |  | -0.8 / -0.6 |  |
| MYM | 5 | h2 | -0.014 | -0.050 .. +0.021 | -0.0022 | 0.42 / 0.42 / 0.18 | 0.175 |  |  | 3/8 | n/a | -0.014 |  | -1.5 / -0.8 |  |
| MYM | 5 | h4 | -0.038 | -0.120 .. +0.044 | -0.0038 | 0.37 / 0.37 / 0.12 | 0.119 |  |  | 3/8 | n/a | -0.038 |  | -2.4 / -0.9 | 0.059 |
| MYM | 5 | h8 | -0.070 | -0.222 .. +0.082 | -0.0051 | 0.37 / 0.38 / 0.13 | 0.134 |  |  | 3/8 | n/a | -0.070 |  | -3.2 / -0.9 |  |
| MYM | 5 | h16 | -0.103 | -0.329 .. +0.122 | -0.0050 | 0.37 / 0.38 / 0.2 | 0.201 |  |  | 3/8 | n/a | -0.103 |  | -4.0 / -0.9 |  |
| MYM | 5 | eod * | -1.344 | -3.385 .. +0.697 | -0.0105 | 0.2 / 0.21 / 0.24 | 0.241 | 1 | 1 | 4/8 | n/a | -1.344 | False | -13.7 / -1.3 |  |
| MYM | 15 | h1 | -0.005 | -0.019 .. +0.009 | -0.0001 | 0.49 / 0.5 / 0.48 | 0.468 |  |  | 3/8 | n/a | -0.005 |  | -0.7 / -0.7 |  |
| MYM | 15 | h2 | -0.024 | -0.070 .. +0.023 | -0.0032 | 0.32 / 0.33 / 0.18 | 0.188 |  |  | 3/8 | n/a | -0.024 |  | -1.4 / -1.0 |  |
| MYM | 15 | h4 | -0.055 | -0.155 .. +0.045 | -0.0048 | 0.28 / 0.29 / 0.14 | 0.15 |  |  | 3/8 | n/a | -0.055 |  | -1.9 / -1.1 | 0.079 |
| MYM | 15 | h8 | -0.102 | -0.278 .. +0.074 | -0.0069 | 0.25 / 0.27 / 0.15 | 0.155 |  |  | 3/8 | n/a | -0.102 |  | -2.7 / -1.1 |  |
| MYM | 15 | h16 | -0.222 | -0.579 .. +0.134 | -0.0116 | 0.22 / 0.24 / 0.16 | 0.159 |  |  | 3/8 | n/a | -0.222 |  | -4.5 / -1.2 |  |
| MYM | 15 | eod * | -0.945 | -2.297 .. +0.406 | -0.0172 | 0.17 / 0.18 / 0.14 | 0.139 | 1 | 1 | 5/8 | n/a | -0.945 | False | -7.6 / -1.4 |  |
| MYM | 60 | h1 | +0.000 | -0.022 .. +0.022 | +0.0053 | 0.98 / 0.98 / 1 | 1 |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 60 | h2 | -0.003 | -0.048 .. +0.041 | +0.0061 | 0.88 / 0.89 / 0.89 | 0.874 |  |  | 5/8 | n/a | -0.003 |  | -0.2 / -0.1 |  |
| MYM | 60 | h4 | -0.018 | -0.107 .. +0.072 | +0.0062 | 0.7 / 0.7 / 0.72 | 0.71 |  |  | 5/8 | n/a | -0.018 |  | -0.7 / -0.4 | 0.142 |
| MYM | 60 | h8 | -0.057 | -0.234 .. +0.120 | +0.0061 | 0.53 / 0.54 / 0.56 | 0.54 |  |  | 5/8 | n/a | -0.057 |  | -1.6 / -0.6 |  |
| MYM | 60 | h16 | -0.130 | -0.454 .. +0.194 | +0.0027 | 0.43 / 0.44 / 0.46 | 0.451 |  |  | 5/8 | n/a | -0.130 |  | -2.8 / -0.8 |  |
| MYM | 60 | eod * | -0.183 | -0.542 .. +0.175 | -0.0010 | 0.32 / 0.33 / 0.35 | 0.348 | 1 | 1 | 6/8 | n/a | -0.183 | False | -3.8 / -1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.014 | +0.010 .. +0.018 | +2.7% | +0.002 | 7.4e-11 | 2.42e-08 | 15/16 |
| MES | 5 | h2 | +0.023 | +0.014 .. +0.033 | +3.3% | +0.013 | 5.1e-07 |  | 14/16 |
| MES | 5 | h4 | +0.032 | +0.014 .. +0.050 | +3.2% | +0.030 | 0.00053 |  | 13/16 |
| MES | 5 | h8 | +0.037 | +0.003 .. +0.072 | +2.6% | +0.055 | 0.035 |  | 10/16 |
| MES | 5 | h16 | +0.025 | -0.034 .. +0.084 | +1.2% | +0.077 | 0.41 |  | 7/16 |
| MES | 5 | eod | +0.327 | -0.557 .. +1.210 | +3.3% | +0.002 | 0.47 |  | 8/16 |
| MES | 15 | h1 | -0.003 | -0.009 .. +0.003 | -0.5% | -0.021 | 0.39 |  | 10/16 |
| MES | 15 | h2 | -0.002 | -0.018 .. +0.014 | -0.3% | -0.021 | 0.89 |  | 10/16 |
| MES | 15 | h4 | -0.010 | -0.044 .. +0.025 | -0.9% | -0.024 | 0.64 |  | 12/16 |
| MES | 15 | h8 | -0.030 | -0.090 .. +0.029 | -2.0% | -0.031 | 0.36 |  | 12/16 |
| MES | 15 | h16 * | -0.071 | -0.172 .. +0.030 | -3.1% | -0.037 | 0.26 | 1 | 11/16 |
| MES | 15 | eod | +0.113 | -0.494 .. +0.719 | +2.1% | -0.331 | 0.72 |  | 8/16 |
| MES | 60 | h1 * | -0.029 | -0.040 .. -0.017 | -5.6% | -0.057 | 4.7e-06 | 0.00111 | 14/16 |
| MES | 60 | h2 | -0.050 | -0.070 .. -0.031 | -6.8% | -0.091 | 1.9e-05 |  | 15/16 |
| MES | 60 | h4 | -0.076 | -0.114 .. -0.037 | -7.1% | -0.142 | 0.00082 |  | 14/16 |
| MES | 60 | h8 | -0.103 | -0.173 .. -0.034 | -6.8% | -0.239 | 0.011 |  | 10/16 |
| MES | 60 | h16 | -0.119 | -0.245 .. +0.007 | -5.8% | -0.364 | 0.12 |  | 10/16 |
| MES | 60 | eod | -0.103 | -0.248 .. +0.041 | -4.8% | -0.372 | 0.25 |  | 9/16 |
| MNQ | 5 | h1 * | +0.006 | +0.000 .. +0.012 | +1.1% | -0.002 | 0.048 | 1 | 11/16 |
| MNQ | 5 | h2 | +0.009 | -0.010 .. +0.028 | +1.2% | -0.003 | 0.34 |  | 8/16 |
| MNQ | 5 | h4 | +0.010 | -0.031 .. +0.052 | +0.9% | +0.002 | 0.64 |  | 6/16 |
| MNQ | 5 | h8 | +0.000 | -0.084 .. +0.084 | +0.0% | +0.012 | 1 |  | 3/16 |
| MNQ | 5 | h16 | -0.050 | -0.195 .. +0.094 | -2.1% | +0.018 | 0.5 |  | 14/16 |
| MNQ | 5 | eod | -0.029 | -1.295 .. +1.237 | -0.2% | -1.226 | 0.96 |  | 8/16 |
| MNQ | 15 | h1 * | -0.012 | -0.019 .. -0.005 | -2.3% | -0.020 | 0.0041 | 0.618 | 12/16 |
| MNQ | 15 | h2 | -0.016 | -0.044 .. +0.012 | -2.1% | -0.025 | 0.27 |  | 14/16 |
| MNQ | 15 | h4 | -0.029 | -0.106 .. +0.048 | -2.5% | -0.031 | 0.47 |  | 15/16 |
| MNQ | 15 | h8 | -0.066 | -0.189 .. +0.057 | -3.9% | -0.039 | 0.29 |  | 14/16 |
| MNQ | 15 | h16 | -0.130 | -0.304 .. +0.044 | -5.1% | -0.067 | 0.14 |  | 13/16 |
| MNQ | 15 | eod | -0.012 | -0.895 .. +0.871 | -0.2% | -0.806 | 0.98 |  | 8/16 |
| MNQ | 60 | h1 * | -0.051 | -0.062 .. -0.039 | -9.6% | -0.076 | 9.7e-15 | 3.98e-12 | 15/16 |
| MNQ | 60 | h2 | -0.085 | -0.106 .. -0.064 | -11.1% | -0.127 | 8.4e-13 |  | 16/16 |
| MNQ | 60 | h4 | -0.115 | -0.155 .. -0.075 | -10.4% | -0.208 | 1.3e-07 |  | 15/16 |
| MNQ | 60 | h8 | -0.164 | -0.238 .. -0.090 | -10.3% | -0.361 | 8.2e-05 |  | 14/16 |
| MNQ | 60 | h16 | -0.216 | -0.358 .. -0.074 | -9.8% | -0.579 | 0.0051 |  | 10/16 |
| MNQ | 60 | eod | -0.210 | -0.372 .. -0.048 | -9.1% | -0.601 | 0.017 |  | 10/16 |
| MYM | 5 | h1 | +0.004 | -0.007 .. +0.015 | +0.8% | -0.007 | 0.48 |  | 2/8 |
| MYM | 5 | h2 | +0.014 | -0.020 .. +0.048 | +1.8% | -0.002 | 0.42 |  | 2/8 |
| MYM | 5 | h4 * | +0.037 | -0.042 .. +0.117 | +3.4% | +0.019 | 0.37 | 1 | 3/8 |
| MYM | 5 | h8 | +0.062 | -0.087 .. +0.211 | +3.9% | +0.060 | 0.42 |  | 4/8 |
| MYM | 5 | h16 | +0.043 | -0.162 .. +0.248 | +1.8% | +0.089 | 0.69 |  | 3/8 |
| MYM | 5 | eod | -0.845 | -2.453 .. +0.763 | -7.2% | -1.585 | 0.42 |  | 6/8 |
| MYM | 15 | h1 * | -0.004 | -0.017 .. +0.008 | -0.8% | -0.017 | 0.5 | 1 | 6/8 |
| MYM | 15 | h2 | +0.013 | -0.032 .. +0.058 | +1.7% | -0.005 | 0.57 |  | 2/8 |
| MYM | 15 | h4 | +0.031 | -0.079 .. +0.140 | +2.7% | +0.026 | 0.59 |  | 3/8 |
| MYM | 15 | h8 | +0.043 | -0.138 .. +0.224 | +2.6% | +0.089 | 0.65 |  | 3/8 |
| MYM | 15 | h16 | +0.047 | -0.255 .. +0.348 | +1.9% | +0.188 | 0.77 |  | 3/8 |
| MYM | 15 | eod | -0.220 | -1.363 .. +0.923 | -3.7% | -0.640 | 0.89 |  | 6/8 |
| MYM | 60 | h1 | -0.018 | -0.035 .. +0.000 | -3.4% | -0.048 | 0.051 |  | 6/8 |
| MYM | 60 | h2 | -0.031 | -0.061 .. -0.001 | -4.1% | -0.074 | 0.067 |  | 6/8 |
| MYM | 60 | h4 * | -0.069 | -0.126 .. -0.011 | -6.4% | -0.127 | 0.025 | 1 | 6/8 |
| MYM | 60 | h8 | -0.125 | -0.242 .. -0.009 | -8.1% | -0.233 | 0.035 |  | 6/8 |
| MYM | 60 | h16 | -0.222 | -0.450 .. +0.007 | -10.5% | -0.398 | 0.058 |  | 6/8 |
| MYM | 60 | eod | -0.258 | -0.522 .. +0.005 | -11.6% | -0.433 | 0.054 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.18 pts | -0.75 .. +0.40 | 0.56 |
| MES | 15 | -0.61 pts | -1.66 .. +0.44 | 0.26 |
| MES | 60 | -0.55 pts | -2.75 .. +1.64 | 0.62 |
| MNQ | 5 | -0.79 pts | -1.36 .. -0.22 | 0.0088 |
| MNQ | 15 | -1.30 pts | -2.32 .. -0.29 | 0.024 |
| MNQ | 60 | +0.64 pts | -1.55 .. +2.84 | 0.57 |
| MYM | 5 | +0.50 pts | -0.30 .. +1.30 | 0.27 |
| MYM | 15 | +0.14 pts | -1.15 .. +1.42 | 0.83 |
| MYM | 60 | -0.88 pts | -3.85 .. +2.10 | 0.57 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 206618 | +0.001 | 0.396 | +0.01 | -3.49 | -3.48 | -3.50 | -3.49 |
| MES | 5 | h2 | bottom fifth | long | 206618 | +0.004 | 0.396 | +0.04 | -3.46 | -3.45 | -3.47 | -3.48 |
| MES | 5 | h4 | bottom fifth | long | 206618 | +0.010 | 0.396 | +0.09 | -3.41 | -3.39 | -3.42 | -3.45 |
| MES | 5 | h8 | bottom fifth | long | 206618 | +0.023 | 0.396 | +0.21 | -3.29 | -3.26 | -3.32 | -3.39 |
| MES | 5 | h16 | bottom fifth | long | 206618 | +0.053 | 0.396 | +0.44 | -3.06 | -2.99 | -3.13 | -3.30 |
| MES | 5 | eod | bottom fifth | long | 206618 | +0.998 | 0.396 | +6.46 | +2.96 | +2.85 | +3.06 | +1.45 |
| MES | 15 | h1 | bottom fifth | long | 68233 | +0.004 | 0.232 | +0.06 | -3.44 | -3.42 | -3.46 | -3.48 |
| MES | 15 | h2 | bottom fifth | long | 68233 | +0.010 | 0.232 | +0.15 | -3.35 | -3.32 | -3.38 | -3.44 |
| MES | 15 | h4 | bottom fifth | long | 68233 | +0.023 | 0.232 | +0.32 | -3.18 | -3.12 | -3.23 | -3.34 |
| MES | 15 | h8 | bottom fifth | long | 68233 | +0.052 | 0.232 | +0.68 | -2.82 | -2.71 | -2.91 | -3.12 |
| MES | 15 | h16 | bottom fifth | long | 68233 | +0.111 | 0.232 | +1.33 | -2.17 | -1.94 | -2.37 | -2.69 |
| MES | 15 | eod | bottom fifth | long | 68233 | +0.570 | 0.232 | +6.43 | +2.93 | +2.83 | +3.02 | +1.74 |
| MES | 60 | h1 | bottom fifth | long | 16633 | +0.011 | 0.120 | +0.32 | -3.18 | -3.11 | -3.24 | -3.40 |
| MES | 60 | h2 | bottom fifth | long | 16633 | +0.024 | 0.120 | +0.68 | -2.82 | -2.71 | -2.92 | -3.26 |
| MES | 60 | h4 | bottom fifth | long | 16633 | +0.050 | 0.120 | +1.29 | -2.21 | -1.95 | -2.44 | -3.10 |
| MES | 60 | h8 | bottom fifth | long | 16633 | +0.104 | 0.120 | +2.66 | -0.84 | -0.47 | -1.19 | -2.48 |
| MES | 60 | h16 | bottom fifth | long | 16633 | +0.187 | 0.120 | +4.86 | +1.36 | +1.79 | +0.96 | -1.22 |
| MES | 60 | eod | bottom fifth | long | 16633 | +0.239 | 0.120 | +6.25 | +2.75 | +2.78 | +2.73 | -0.30 |
| MNQ | 5 | h1 | bottom fifth | long | 206288 | +0.004 | 0.165 | +0.03 | -1.97 | -1.96 | -1.97 | -1.98 |
| MNQ | 5 | h2 | bottom fifth | long | 206288 | +0.009 | 0.165 | +0.08 | -1.92 | -1.92 | -1.92 | -1.94 |
| MNQ | 5 | h4 | bottom fifth | long | 206288 | +0.019 | 0.165 | +0.17 | -1.83 | -1.83 | -1.83 | -1.86 |
| MNQ | 5 | h8 | bottom fifth | long | 206288 | +0.039 | 0.165 | +0.35 | -1.65 | -1.65 | -1.65 | -1.76 |
| MNQ | 5 | h16 | bottom fifth | long | 206288 | +0.077 | 0.165 | +0.68 | -1.32 | -1.29 | -1.34 | -1.63 |
| MNQ | 5 | eod | bottom fifth | long | 206288 | +1.596 | 0.165 | +8.64 | +6.64 | +5.98 | +7.32 | +4.71 |
| MNQ | 15 | h1 | bottom fifth | long | 68227 | +0.006 | 0.095 | +0.11 | -1.89 | -1.88 | -1.90 | -1.99 |
| MNQ | 15 | h2 | bottom fifth | long | 68227 | +0.013 | 0.095 | +0.25 | -1.75 | -1.74 | -1.76 | -1.90 |
| MNQ | 15 | h4 | bottom fifth | long | 68227 | +0.028 | 0.095 | +0.50 | -1.50 | -1.47 | -1.52 | -1.79 |
| MNQ | 15 | h8 | bottom fifth | long | 68227 | +0.057 | 0.095 | +0.98 | -1.02 | -0.94 | -1.10 | -1.63 |
| MNQ | 15 | h16 | bottom fifth | long | 68227 | +0.121 | 0.095 | +1.82 | -0.18 | +0.03 | -0.41 | -1.04 |
| MNQ | 15 | eod | bottom fifth | long | 68227 | +0.819 | 0.095 | +8.40 | +6.40 | +5.99 | +6.83 | +4.55 |
| MNQ | 60 | h1 | bottom fifth | long | 16637 | +0.016 | 0.050 | +0.45 | -1.55 | -1.45 | -1.65 | -1.97 |
| MNQ | 60 | h2 | bottom fifth | long | 16637 | +0.034 | 0.050 | +0.93 | -1.07 | -0.92 | -1.23 | -1.89 |
| MNQ | 60 | h4 | bottom fifth | long | 16637 | +0.070 | 0.050 | +1.70 | -0.30 | +0.07 | -0.69 | -1.86 |
| MNQ | 60 | h8 | bottom fifth | long | 16637 | +0.140 | 0.050 | +3.38 | +1.38 | +1.93 | +0.80 | -1.50 |
| MNQ | 60 | h16 | bottom fifth | long | 16637 | +0.264 | 0.050 | +6.32 | +4.32 | +5.00 | +3.60 | -0.60 |
| MNQ | 60 | eod | bottom fifth | long | 16637 | +0.322 | 0.050 | +8.25 | +6.25 | +6.05 | +6.46 | +0.36 |
| MYM | 5 | h1 | top fifth | short | 102725 | +0.006 | 0.127 | -0.01 | -2.01 | +nan | -2.01 | -2.01 |
| MYM | 5 | h2 | bottom fifth | long | 103013 | -0.005 | 0.211 | -0.01 | -2.01 | +nan | -2.01 | -2.00 |
| MYM | 5 | h4 | bottom fifth | long | 103013 | -0.009 | 0.211 | -0.01 | -2.01 | +nan | -2.01 | -1.98 |
| MYM | 5 | h8 | bottom fifth | long | 103013 | -0.016 | 0.211 | -0.01 | -2.01 | +nan | -2.01 | -1.99 |
| MYM | 5 | h16 | top fifth | short | 102725 | +0.131 | 0.127 | +0.01 | -1.99 | +nan | -1.99 | -1.85 |
| MYM | 5 | eod | top fifth | short | 102725 | +1.085 | 0.127 | +2.32 | +0.32 | +nan | +0.32 | +2.14 |
| MYM | 15 | h1 | bottom fifth | long | 34056 | -0.003 | 0.120 | -0.02 | -2.02 | +nan | -2.02 | -2.02 |
| MYM | 15 | h2 | bottom fifth | long | 34056 | -0.005 | 0.120 | -0.02 | -2.02 | +nan | -2.02 | -1.99 |
| MYM | 15 | h4 | bottom fifth | long | 34056 | -0.009 | 0.120 | -0.00 | -2.00 | +nan | -2.00 | -1.94 |
| MYM | 15 | h8 | top fifth | short | 33955 | +0.112 | 0.071 | +0.03 | -1.97 | +nan | -1.97 | -2.13 |
| MYM | 15 | h16 | top fifth | short | 33955 | +0.236 | 0.071 | +0.26 | -1.74 | +nan | -1.74 | -2.36 |
| MYM | 15 | eod | top fifth | short | 33955 | +0.831 | 0.071 | +2.70 | +0.70 | +nan | +0.70 | +0.09 |
| MYM | 60 | h1 | top fifth | long | 8252 | -0.004 | 0.034 | +0.02 | -1.98 | +nan | -1.98 | -2.16 |
| MYM | 60 | h2 | bottom fifth | long | 8278 | -0.011 | 0.062 | +0.13 | -1.87 | +nan | -1.87 | -1.96 |
| MYM | 60 | h4 | bottom fifth | long | 8278 | -0.019 | 0.062 | +0.27 | -1.73 | +nan | -1.73 | -1.83 |
| MYM | 60 | h8 | top fifth | short | 8252 | +0.051 | 0.034 | +1.11 | -0.89 | +nan | -0.89 | +0.94 |
| MYM | 60 | h16 | top fifth | short | 8252 | +0.096 | 0.034 | +2.78 | +0.78 | +nan | +0.78 | +4.94 |
| MYM | 60 | eod | top fifth | short | 8252 | +0.108 | 0.034 | +2.97 | +0.97 | +nan | +0.97 | +6.42 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.009 | +0.011 | +0.009 | +0.005 | +0.002 | +0.000 | -0.003 | -0.006 | -0.012 | -0.026 | -0.048 |
| MES | 15 | -0.067 | -0.027 | -0.004 | +0.003 | +0.004 | +0.000 | -0.008 | -0.017 | -0.031 | -0.055 | -0.117 |
| MES | 60 | -0.692 | -0.339 | -0.144 | -0.051 | -0.015 | +0.000 | -0.010 | -0.022 | -0.029 | -0.033 | -0.043 |
| MNQ | 5 | +0.037 | +0.023 | +0.012 | +0.007 | +0.004 | +0.000 | -0.009 | -0.016 | -0.028 | -0.058 | -0.101 |
| MNQ | 15 | -0.065 | -0.025 | -0.002 | +0.005 | +0.006 | +0.000 | -0.014 | -0.027 | -0.049 | -0.065 | -0.109 |
| MNQ | 60 | -0.792 | -0.403 | -0.176 | -0.065 | -0.020 | +0.000 | -0.008 | -0.019 | -0.020 | -0.026 | -0.068 |
| MYM | 5 | +0.015 | +0.014 | +0.007 | +0.004 | +0.003 | +0.000 | -0.011 | -0.023 | -0.047 | -0.081 | -0.103 |
| MYM | 15 | -0.058 | -0.021 | +0.001 | +0.007 | +0.007 | +0.000 | -0.021 | -0.040 | -0.069 | -0.098 | -0.197 |
| MYM | 60 | -0.706 | -0.349 | -0.166 | -0.066 | -0.020 | +0.000 | +0.002 | +0.004 | +0.028 | +0.079 | +0.193 |

## Calibration

- MES 5-min: 1032061 bars, 206202 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 340850 bars, 68109 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83103 bars, 16610 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1030342 bars, 206045 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340695 bars, 68110 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83101 bars, 16616 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 514796 bars, 102725 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170036 bars, 33955 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41326 bars, 8252 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
