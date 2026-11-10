# Impact card: pat_hammer

candle pattern hammer in its textbook direction: range >= avgR10, lower shadow >= 2 x body, upper <= 0.1 x range, prior close < EMA10 -> bullish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.036 R20 over the next 2 bars (10 min), p=0.06; we would catch an effect of 0.049 R20 or more 80% of the time).
- MES 5-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.030 R20, CONFIRMED, q=0.000206, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.86 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.264 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.052 R20 over the next 1 bar (15 min), p=0.026; we would catch an effect of 0.101 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.047 R20, CONFIRMED, q=0.0357, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.30 at recent bar sizes, 90% range up to $4.13); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.324 R20 over the next 16 bars (16 h), p=0.23; we would catch an effect of 0.229 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.023).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $17.75 at recent bar sizes, 90% range up to $21.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.045 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.055 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 6% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.043 R20, CONFIRMED, q=0.0129, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.67 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.091 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.040 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.117 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.069).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.58 at recent bar sizes, 90% range up to $5.96); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.217 R20 over the rest of the session (to 16:45), p=0.98; we would catch an effect of 0.243 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.45).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $18.87 at recent bar sizes, 90% range up to $29.04); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.761 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.080 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.057 R20, possible, q=0.251, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.57 at recent bar sizes, 90% range up to $1.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.105 R20 over the next 2 bars (30 min), p=0.024; we would catch an effect of 0.154 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.92 at recent bar sizes, 90% range up to $4.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.051 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.312 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.45).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.94 at recent bar sizes, 90% range up to $15.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.011 | -0.027 .. +0.006 | -0.0013 | 0.2 / 0.22 / 0.21 | 0.214 |  |  | 10/16 | -0.018 | -0.003 |  | -1.2 / -1.3 |  |
| MES | 5 | h2 * | -0.036 | -0.059 .. -0.013 | -0.0030 | 0.0025 / 0.003 / 0.0033 | 0.00313 | 1 | 0.499 | 13/16 | -0.051 | -0.021 | False | -2.9 / -3.0 |  |
| MES | 5 | h4 | -0.033 | -0.066 .. +0.001 | -0.0019 | 0.056 / 0.056 / 0.063 | 0.0591 |  |  | 10/16 | -0.053 | -0.012 |  | -1.9 / -1.9 | 0.049 |
| MES | 5 | h8 | -0.005 | -0.054 .. +0.043 | -0.0002 | 0.82 / 0.83 / 0.83 | 0.818 |  |  | 9/16 | -0.003 | -0.008 |  | -0.2 / -0.2 |  |
| MES | 5 | h16 | -0.030 | -0.107 .. +0.046 | -0.0009 | 0.43 / 0.43 / 0.43 | 0.434 |  |  | 11/16 | -0.077 | +0.016 |  | -0.9 / -0.8 |  |
| MES | 5 | eod | +0.162 | -0.419 .. +0.743 | +0.0009 | 0.58 / 0.6 / 0.41 | 0.404 |  |  | 11/16 | +0.022 | +0.301 |  | +0.9 / +0.5 |  |
| MES | 15 | h1 * | -0.052 | -0.088 .. -0.017 | -0.0057 | 0.0038 / 0.0044 / 0.0026 | 0.00599 | 0.655 | 0.634 | 10/16 | -0.030 | -0.075 | False | -2.9 / -2.9 |  |
| MES | 15 | h2 | -0.038 | -0.087 .. +0.011 | -0.0028 | 0.13 / 0.14 / 0.16 | 0.15 |  |  | 8/16 | +0.001 | -0.077 |  | -1.6 / -1.5 |  |
| MES | 15 | h4 | -0.062 | -0.134 .. +0.009 | -0.0031 | 0.088 / 0.091 / 0.13 | 0.117 |  |  | 9/16 | +0.033 | -0.157 |  | -1.8 / -1.7 | 0.101 |
| MES | 15 | h8 | -0.044 | -0.159 .. +0.071 | -0.0015 | 0.46 / 0.45 / 0.44 | 0.441 |  |  | 9/16 | +0.054 | -0.141 |  | -0.8 / -0.7 |  |
| MES | 15 | h16 | -0.008 | -0.162 .. +0.146 | -0.0002 | 0.92 / 0.92 / 0.92 | 0.916 |  |  | 9/16 | +0.109 | -0.125 |  | -0.1 / -0.1 |  |
| MES | 15 | eod | +0.126 | -0.296 .. +0.548 | +0.0012 | 0.56 / 0.56 / 0.53 | 0.539 |  |  | 10/16 | +0.253 | -0.001 |  | +0.7 / +0.6 |  |
| MES | 60 | h1 | +0.004 | -0.085 .. +0.094 | +0.0005 | 0.92 / 0.92 / 0.91 | 0.909 |  |  | 8/16 | +0.033 | -0.024 |  | +0.1 / +0.1 |  |
| MES | 60 | h2 | -0.017 | -0.145 .. +0.112 | -0.0013 | 0.8 / 0.79 / 0.76 | 0.764 |  |  | 8/16 | -0.036 | +0.002 |  | -0.3 / -0.3 |  |
| MES | 60 | h4 | -0.045 | -0.219 .. +0.129 | -0.0024 | 0.61 / 0.6 / 0.56 | 0.554 |  |  | 9/16 | -0.131 | +0.041 |  | -0.5 / -0.5 | 0.229 |
| MES | 60 | h8 | -0.173 | -0.438 .. +0.092 | -0.0067 | 0.2 / 0.2 / 0.095 | 0.0974 |  |  | 10/16 | -0.236 | -0.110 |  | -1.5 / -1.3 |  |
| MES | 60 | h16 * | -0.324 | -0.632 .. -0.017 | -0.0096 | 0.039 / 0.038 / 0.0053 | 0.00417 | 1 | 0.998 | 12/16 | -0.329 | -0.319 | False | -2.4 / -2.1 |  |
| MES | 60 | eod | -0.326 | -0.637 .. -0.016 | -0.0092 | 0.039 / 0.038 / 0.0052 | 0.00469 |  |  | 11/16 | -0.354 | -0.298 |  | -2.4 / -2.1 |  |
| MNQ | 5 | h1 | +0.002 | -0.016 .. +0.020 | +0.0002 | 0.81 / 0.81 / 0.86 | 0.857 |  |  | 8/16 | +0.006 | -0.002 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h2 | +0.011 | -0.015 .. +0.038 | +0.0007 | 0.4 / 0.41 / 0.47 | 0.415 |  |  | 9/16 | +0.013 | +0.010 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h4 | +0.002 | -0.036 .. +0.041 | +0.0001 | 0.9 / 0.9 / 0.92 | 0.909 |  |  | 8/16 | +0.005 | -0.000 |  | +0.1 / +0.1 | 0.055 |
| MNQ | 5 | h8 | +0.029 | -0.026 .. +0.084 | +0.0008 | 0.3 / 0.31 / 0.44 | 0.381 |  |  | 10/16 | +0.044 | +0.015 |  | +1.0 / +1.0 |  |
| MNQ | 5 | h16 * | +0.045 | -0.050 .. +0.139 | +0.0009 | 0.35 / 0.35 / 0.41 | 0.39 | 1 | 1 | 9/16 | +0.035 | +0.054 | False | +1.0 / +0.9 |  |
| MNQ | 5 | eod | +0.043 | -0.754 .. +0.839 | +0.0002 | 0.92 / 0.92 / 0.87 | 0.869 |  |  | 9/16 | -0.004 | +0.089 |  | +0.2 / +0.1 |  |
| MNQ | 15 | h1 | +0.012 | -0.027 .. +0.052 | +0.0010 | 0.55 / 0.56 / 0.61 | 0.543 |  |  | 9/16 | +0.009 | +0.015 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h2 * | +0.040 | -0.014 .. +0.094 | +0.0020 | 0.15 / 0.17 / 0.32 | 0.192 | 1 | 1 | 11/16 | +0.070 | +0.009 | False | +1.4 / +1.4 |  |
| MNQ | 15 | h4 | +0.050 | -0.029 .. +0.128 | +0.0015 | 0.22 / 0.23 / 0.46 | 0.285 |  |  | 12/16 | +0.084 | +0.015 |  | +1.2 / +1.2 | 0.117 |
| MNQ | 15 | h8 | +0.053 | -0.062 .. +0.168 | +0.0012 | 0.37 / 0.37 / 0.52 | 0.455 |  |  | 12/16 | -0.001 | +0.107 |  | +0.9 / +0.9 |  |
| MNQ | 15 | h16 | +0.074 | -0.101 .. +0.249 | +0.0014 | 0.41 / 0.41 / 0.48 | 0.45 |  |  | 10/16 | +0.032 | +0.116 |  | +0.9 / +0.8 |  |
| MNQ | 15 | eod | +0.117 | -0.361 .. +0.596 | +0.0008 | 0.63 / 0.64 / 0.68 | 0.658 |  |  | 9/16 | +0.315 | -0.079 |  | +0.6 / +0.5 |  |
| MNQ | 60 | h1 | +0.037 | -0.057 .. +0.130 | +0.0038 | 0.45 / 0.43 / 0.38 | 0.381 |  |  | 9/16 | +0.069 | +0.004 |  | +0.8 / +0.8 |  |
| MNQ | 60 | h2 | +0.067 | -0.056 .. +0.190 | +0.0048 | 0.28 / 0.27 / 0.27 | 0.26 |  |  | 11/16 | +0.067 | +0.068 |  | +1.2 / +1.1 |  |
| MNQ | 60 | h4 | -0.048 | -0.228 .. +0.132 | -0.0024 | 0.6 / 0.58 / 0.57 | 0.573 |  |  | 7/16 | -0.165 | +0.069 |  | -0.6 / -0.5 | 0.243 |
| MNQ | 60 | h8 | -0.111 | -0.376 .. +0.154 | -0.0041 | 0.41 / 0.38 / 0.31 | 0.316 |  |  | 10/16 | -0.214 | -0.008 |  | -1.0 / -0.8 |  |
| MNQ | 60 | h16 | -0.208 | -0.510 .. +0.094 | -0.0059 | 0.18 / 0.14 / 0.088 | 0.0906 |  |  | 12/16 | -0.224 | -0.191 |  | -1.6 / -1.3 |  |
| MNQ | 60 | eod * | -0.217 | -0.521 .. +0.088 | -0.0059 | 0.16 / 0.13 / 0.076 | 0.0763 | 1 | 1 | 11/16 | -0.253 | -0.180 | False | -1.7 / -1.4 |  |
| MYM | 5 | h1 | -0.003 | -0.031 .. +0.024 | -0.0003 | 0.82 / 0.82 / 0.85 | 0.786 |  |  | 2/8 | n/a | -0.003 |  | -0.2 / -0.2 |  |
| MYM | 5 | h2 | -0.001 | -0.041 .. +0.039 | -0.0001 | 0.95 / 0.95 / 0.97 | 0.965 |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 5 | h4 | +0.001 | -0.063 .. +0.066 | +0.0001 | 0.96 / 0.96 / 0.98 | 0.963 |  |  | 5/8 | n/a | +0.001 |  | +0.0 / +0.0 | 0.080 |
| MYM | 5 | h8 | -0.002 | -0.094 .. +0.089 | -0.0000 | 0.96 / 0.96 / 0.96 | 0.953 |  |  | 4/8 | n/a | -0.002 |  | -0.0 / -0.0 |  |
| MYM | 5 | h16 | +0.061 | -0.070 .. +0.192 | +0.0011 | 0.36 / 0.36 / 0.45 | 0.412 |  |  | 4/8 | n/a | +0.061 |  | +1.0 / +0.9 |  |
| MYM | 5 | eod * | -0.761 | -1.922 .. +0.401 | -0.0031 | 0.2 / 0.19 / 0.045 | 0.039 | 1 | 1 | 6/8 | n/a | -0.761 | False | -2.2 / -1.3 |  |
| MYM | 15 | h1 | -0.087 | -0.138 .. -0.036 | -0.0075 | 0.0008 / 0.0014 / 0.0077 | 0.0258 |  |  | 7/8 | n/a | -0.087 |  | -3.3 / -3.4 |  |
| MYM | 15 | h2 * | -0.105 | -0.174 .. -0.037 | -0.0052 | 0.0026 / 0.0041 / 0.06 | 0.0443 | 0.611 | 0.202 | 5/8 | n/a | -0.105 | False | -2.8 / -3.0 |  |
| MYM | 15 | h4 | -0.090 | -0.191 .. +0.011 | -0.0026 | 0.08 / 0.086 / 0.32 | 0.159 |  |  | 5/8 | n/a | -0.090 |  | -1.7 / -1.8 | 0.154 |
| MYM | 15 | h8 | +0.006 | -0.157 .. +0.169 | +0.0001 | 0.94 / 0.94 / 0.95 | 0.953 |  |  | 5/8 | n/a | +0.006 |  | +0.1 / +0.1 |  |
| MYM | 15 | h16 | +0.029 | -0.213 .. +0.272 | +0.0005 | 0.81 / 0.81 / 0.86 | 0.836 |  |  | 3/8 | n/a | +0.029 |  | +0.3 / +0.2 |  |
| MYM | 15 | eod | +0.367 | -0.359 .. +1.093 | +0.0024 | 0.32 / 0.33 / 0.39 | 0.356 |  |  | 6/8 | n/a | +0.367 |  | +1.3 / +1.0 |  |
| MYM | 60 | h1 * | +0.051 | -0.066 .. +0.168 | +0.0053 | 0.39 / 0.39 / 0.35 | 0.347 | 1 | 1 | 5/8 | n/a | +0.051 | False | +0.8 / +0.9 |  |
| MYM | 60 | h2 | +0.017 | -0.133 .. +0.166 | +0.0012 | 0.83 / 0.83 / 0.84 | 0.835 |  |  | 5/8 | n/a | +0.017 |  | +0.2 / +0.2 |  |
| MYM | 60 | h4 | -0.045 | -0.273 .. +0.184 | -0.0023 | 0.7 / 0.72 / 0.7 | 0.702 |  |  | 5/8 | n/a | -0.045 |  | -0.4 / -0.4 | 0.312 |
| MYM | 60 | h8 | -0.022 | -0.361 .. +0.317 | -0.0008 | 0.9 / 0.9 / 0.89 | 0.874 |  |  | 4/8 | n/a | -0.022 |  | -0.1 / -0.1 |  |
| MYM | 60 | h16 | -0.134 | -0.509 .. +0.240 | -0.0039 | 0.48 / 0.5 / 0.42 | 0.429 |  |  | 4/8 | n/a | -0.134 |  | -0.7 / -0.7 |  |
| MYM | 60 | eod | -0.138 | -0.512 .. +0.237 | -0.0038 | 0.47 / 0.49 / 0.41 | 0.416 |  |  | 4/8 | n/a | -0.138 |  | -0.7 / -0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.030 | +0.018 .. +0.041 | +6.0% | +0.063 | 8.3e-07 | 0.000206 | 14/16 |
| MES | 5 | h2 | +0.034 | +0.017 .. +0.051 | +4.8% | +0.085 | 0.00018 |  | 13/16 |
| MES | 5 | h4 | +0.042 | +0.018 .. +0.065 | +4.2% | +0.107 | 0.00058 |  | 12/16 |
| MES | 5 | h8 | +0.065 | +0.029 .. +0.101 | +4.5% | +0.141 | 0.0024 |  | 13/16 |
| MES | 5 | h16 | +0.044 | -0.007 .. +0.094 | +2.1% | +0.154 | 0.22 |  | 10/16 |
| MES | 5 | eod | +0.029 | -0.285 .. +0.344 | +0.3% | +0.427 | 0.85 |  | 10/16 |
| MES | 15 | h1 * | +0.047 | +0.027 .. +0.068 | +9.2% | +0.091 | 0.00018 | 0.0357 | 16/16 |
| MES | 15 | h2 | +0.027 | -0.002 .. +0.057 | +3.8% | +0.096 | 0.13 |  | 12/16 |
| MES | 15 | h4 | +0.020 | -0.026 .. +0.066 | +1.9% | +0.092 | 0.39 |  | 11/16 |
| MES | 15 | h8 | +0.051 | -0.019 .. +0.121 | +3.3% | +0.093 | 0.25 |  | 11/16 |
| MES | 15 | h16 | +0.045 | -0.058 .. +0.148 | +2.0% | +0.060 | 0.39 |  | 9/16 |
| MES | 15 | eod | -0.160 | -0.417 .. +0.097 | -2.9% | +0.010 | 0.28 |  | 9/16 |
| MES | 60 | h1 | +0.087 | +0.021 .. +0.152 | +16.9% | +0.142 | 0.01 |  | 12/16 |
| MES | 60 | h2 | +0.097 | +0.010 .. +0.184 | +13.1% | +0.187 | 0.029 |  | 10/16 |
| MES | 60 | h4 | +0.107 | -0.017 .. +0.232 | +10.1% | +0.186 | 0.09 |  | 9/16 |
| MES | 60 | h8 | +0.220 | +0.043 .. +0.398 | +14.6% | +0.295 | 0.016 |  | 14/16 |
| MES | 60 | h16 | +0.285 | +0.090 .. +0.481 | +13.9% | +0.321 | 0.0043 |  | 14/16 |
| MES | 60 | eod * | +0.292 | +0.094 .. +0.490 | +13.5% | +0.322 | 0.0038 | 0.584 | 15/16 |
| MNQ | 5 | h1 | +0.028 | +0.016 .. +0.040 | +5.2% | +0.066 | 0.00086 |  | 13/16 |
| MNQ | 5 | h2 * | +0.043 | +0.025 .. +0.061 | +5.6% | +0.104 | 6.1e-05 | 0.0129 | 16/16 |
| MNQ | 5 | h4 | +0.059 | +0.031 .. +0.087 | +5.3% | +0.140 | 0.01 |  | 14/16 |
| MNQ | 5 | h8 | +0.089 | +0.047 .. +0.130 | +5.5% | +0.169 | 0.027 |  | 15/16 |
| MNQ | 5 | h16 | +0.122 | +0.054 .. +0.190 | +5.1% | +0.211 | 0.0047 |  | 14/16 |
| MNQ | 5 | eod | +0.558 | +0.113 .. +1.002 | +4.4% | +1.231 | 0.024 |  | 12/16 |
| MNQ | 15 | h1 * | +0.041 | +0.016 .. +0.066 | +7.7% | +0.071 | 0.011 | 1 | 13/16 |
| MNQ | 15 | h2 | +0.024 | -0.012 .. +0.059 | +3.1% | +0.090 | 0.19 |  | 10/16 |
| MNQ | 15 | h4 | +0.006 | -0.049 .. +0.061 | +0.5% | +0.081 | 0.83 |  | 10/16 |
| MNQ | 15 | h8 | -0.034 | -0.120 .. +0.051 | -2.0% | +0.004 | 0.58 |  | 9/16 |
| MNQ | 15 | h16 | -0.058 | -0.164 .. +0.048 | -2.3% | -0.034 | 0.55 |  | 10/16 |
| MNQ | 15 | eod | -0.219 | -0.521 .. +0.083 | -3.4% | -0.184 | 0.32 |  | 12/16 |
| MNQ | 60 | h1 * | +0.055 | -0.004 .. +0.114 | +10.4% | +0.118 | 0.075 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.003 | -0.067 .. +0.073 | +0.3% | +0.118 | 0.94 |  | 6/16 |
| MNQ | 60 | h4 | +0.041 | -0.069 .. +0.151 | +3.7% | +0.162 | 0.68 |  | 11/16 |
| MNQ | 60 | h8 | +0.139 | -0.021 .. +0.299 | +8.8% | +0.213 | 0.15 |  | 11/16 |
| MNQ | 60 | h16 | +0.146 | -0.033 .. +0.325 | +6.7% | +0.239 | 0.13 |  | 11/16 |
| MNQ | 60 | eod | +0.160 | -0.023 .. +0.343 | +7.0% | +0.250 | 0.087 |  | 12/16 |
| MYM | 5 | h1 | +0.042 | +0.018 .. +0.066 | +7.9% | +0.080 | 0.0069 |  | 8/8 |
| MYM | 5 | h2 * | +0.057 | +0.028 .. +0.085 | +7.5% | +0.104 | 0.0015 | 0.251 | 7/8 |
| MYM | 5 | h4 | +0.047 | +0.006 .. +0.088 | +4.3% | +0.125 | 0.19 |  | 7/8 |
| MYM | 5 | h8 | +0.077 | +0.014 .. +0.139 | +4.8% | +0.156 | 0.068 |  | 6/8 |
| MYM | 5 | h16 | +0.069 | -0.025 .. +0.164 | +3.0% | +0.132 | 0.41 |  | 7/8 |
| MYM | 5 | eod | +0.192 | -0.350 .. +0.733 | +1.6% | +0.704 | 0.52 |  | 5/8 |
| MYM | 15 | h1 | +0.023 | -0.011 .. +0.057 | +4.4% | +0.075 | 0.49 |  | 6/8 |
| MYM | 15 | h2 | +0.024 | -0.023 .. +0.072 | +3.2% | +0.103 | 0.33 |  | 5/8 |
| MYM | 15 | h4 | +0.015 | -0.061 .. +0.090 | +1.3% | +0.078 | 0.71 |  | 5/8 |
| MYM | 15 | h8 * | +0.062 | -0.042 .. +0.166 | +3.8% | +0.095 | 0.25 | 1 | 6/8 |
| MYM | 15 | h16 | -0.042 | -0.207 .. +0.122 | -1.7% | -0.048 | 0.76 |  | 5/8 |
| MYM | 15 | eod | -0.144 | -0.571 .. +0.284 | -2.4% | +0.017 | 0.62 |  | 5/8 |
| MYM | 60 | h1 | +0.052 | -0.020 .. +0.125 | +10.0% | +0.039 | 0.18 |  | 5/8 |
| MYM | 60 | h2 | +0.096 | -0.010 .. +0.201 | +12.6% | +0.117 | 0.08 |  | 5/8 |
| MYM | 60 | h4 | +0.139 | -0.028 .. +0.307 | +12.9% | +0.183 | 0.11 |  | 7/8 |
| MYM | 60 | h8 * | +0.207 | -0.007 .. +0.421 | +13.4% | +0.234 | 0.075 | 1 | 7/8 |
| MYM | 60 | h16 | +0.158 | -0.075 .. +0.392 | +7.5% | +0.190 | 0.23 |  | 7/8 |
| MYM | 60 | eod | +0.161 | -0.068 .. +0.391 | +7.2% | +0.187 | 0.22 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -1.56 pts | -2.67 .. -0.45 | 0.0067 |
| MES | 15 | -2.58 pts | -4.35 .. -0.81 | 0.0072 |
| MES | 60 | +2.06 pts | -1.83 .. +5.94 | 0.31 |
| MNQ | 5 | +0.62 pts | -0.36 .. +1.60 | 0.23 |
| MNQ | 15 | +1.99 pts | +0.07 .. +3.92 | 0.046 |
| MNQ | 60 | +0.89 pts | -2.82 .. +4.60 | 0.64 |
| MYM | 5 | +0.79 pts | -0.92 .. +2.50 | 0.63 |
| MYM | 15 | -3.06 pts | -5.73 .. -0.40 | 0.044 |
| MYM | 60 | +0.75 pts | -4.22 .. +5.71 | 0.99 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 7986 | +0.008 | 0.409 | +0.13 | -3.37 | -3.49 | -3.21 | -3.35 |
| MES | 5 | h2 | event | against signal | 7986 | +0.029 | 0.409 | +0.41 | -3.09 | -3.40 | -2.69 | -3.06 |
| MES | 5 | h4 | event | against signal | 7986 | +0.019 | 0.409 | +0.32 | -3.18 | -3.47 | -2.81 | -3.11 |
| MES | 5 | h8 | event | against signal | 7986 | -0.022 | 0.409 | +0.19 | -3.31 | -3.77 | -2.72 | -3.17 |
| MES | 5 | h16 | event | against signal | 7986 | -0.026 | 0.409 | -0.13 | -3.63 | -3.65 | -3.61 | -3.33 |
| MES | 5 | eod | event | with signal | 7986 | +0.782 | 0.409 | +3.96 | +0.46 | -1.08 | +2.43 | -1.67 |
| MES | 15 | h1 | event | against signal | 2436 | +0.045 | 0.207 | +0.89 | -2.61 | -3.33 | -1.87 | -2.52 |
| MES | 15 | h2 | event | against signal | 2436 | +0.025 | 0.207 | +0.73 | -2.77 | -3.75 | -1.79 | -2.65 |
| MES | 15 | h4 | event | against signal | 2436 | +0.039 | 0.207 | +1.77 | -1.73 | -3.91 | +0.45 | -1.53 |
| MES | 15 | h8 | event | against signal | 2436 | -0.002 | 0.207 | +1.90 | -1.60 | -4.03 | +0.85 | -1.21 |
| MES | 15 | h16 | event | against signal | 2436 | -0.074 | 0.207 | -0.37 | -3.87 | -5.67 | -2.06 | -3.30 |
| MES | 15 | eod | event | with signal | 2436 | +0.381 | 0.207 | +6.31 | +2.81 | +1.15 | +4.48 | +2.11 |
| MES | 60 | h1 | event | with signal | 568 | +0.016 | 0.096 | +1.19 | -2.31 | -3.10 | -1.52 | -2.60 |
| MES | 60 | h2 | event | against signal | 568 | -0.008 | 0.096 | -2.05 | -5.55 | -3.02 | -8.09 | -4.83 |
| MES | 60 | h4 | event | against signal | 568 | -0.002 | 0.096 | -3.50 | -7.00 | -1.36 | -12.64 | -5.71 |
| MES | 60 | h8 | event | against signal | 568 | +0.089 | 0.096 | +2.56 | -0.94 | -0.83 | -1.05 | +1.21 |
| MES | 60 | h16 | event | against signal | 568 | +0.217 | 0.096 | +6.12 | +2.62 | +0.03 | +5.21 | +5.09 |
| MES | 60 | eod | event | against signal | 568 | +0.214 | 0.096 | +5.94 | +2.44 | +0.59 | +4.29 | +5.01 |
| MNQ | 5 | h1 | event | with signal | 8163 | +0.007 | 0.177 | +0.01 | -1.99 | -1.94 | -2.07 | -2.00 |
| MNQ | 5 | h2 | event | with signal | 8163 | +0.021 | 0.177 | -0.01 | -2.01 | -1.90 | -2.17 | -2.04 |
| MNQ | 5 | h4 | event | with signal | 8163 | +0.019 | 0.177 | -0.13 | -2.13 | -1.95 | -2.37 | -2.16 |
| MNQ | 5 | h8 | event | with signal | 8163 | +0.063 | 0.177 | +0.11 | -1.89 | -1.87 | -1.90 | -1.98 |
| MNQ | 5 | h16 | event | with signal | 8163 | +0.112 | 0.177 | +0.54 | -1.46 | -1.86 | -0.87 | -1.70 |
| MNQ | 5 | eod | event | with signal | 8163 | +0.879 | 0.177 | +1.60 | -0.40 | +0.23 | -1.30 | -1.90 |
| MNQ | 15 | h1 | event | with signal | 2378 | +0.022 | 0.088 | -0.12 | -2.12 | -1.89 | -2.38 | -2.25 |
| MNQ | 15 | h2 | event | with signal | 2378 | +0.055 | 0.088 | +0.41 | -1.59 | -1.57 | -1.62 | -1.78 |
| MNQ | 15 | h4 | event | with signal | 2378 | +0.080 | 0.088 | +0.25 | -1.75 | -1.42 | -2.13 | -2.14 |
| MNQ | 15 | h8 | event | with signal | 2378 | +0.114 | 0.088 | +2.01 | +0.01 | -1.40 | +1.63 | -0.77 |
| MNQ | 15 | h16 | event | with signal | 2378 | +0.167 | 0.088 | +3.33 | +1.33 | -0.77 | +3.72 | +0.61 |
| MNQ | 15 | eod | event | with signal | 2378 | +0.480 | 0.088 | +3.97 | +1.97 | +1.69 | +2.29 | +0.42 |
| MNQ | 60 | h1 | event | with signal | 595 | +0.047 | 0.038 | +3.32 | +1.32 | -0.88 | +3.38 | +1.05 |
| MNQ | 60 | h2 | event | with signal | 595 | +0.090 | 0.038 | +5.45 | +3.45 | -0.61 | +7.26 | +2.61 |
| MNQ | 60 | h4 | event | against signal | 595 | +0.002 | 0.038 | -6.62 | -8.62 | -0.76 | -15.99 | -6.97 |
| MNQ | 60 | h8 | event | against signal | 595 | +0.027 | 0.038 | -2.97 | -4.97 | -1.10 | -8.60 | -2.04 |
| MNQ | 60 | h16 | event | against signal | 595 | +0.095 | 0.038 | +2.76 | +0.76 | -1.93 | +3.27 | +4.16 |
| MNQ | 60 | eod | event | against signal | 595 | +0.102 | 0.038 | +2.64 | +0.64 | -1.54 | +2.68 | +3.84 |
| MYM | 5 | h1 | event | against signal | 3643 | +0.004 | 0.201 | +0.19 | -1.81 | +nan | -1.81 | -1.82 |
| MYM | 5 | h2 | event | against signal | 3643 | +0.006 | 0.201 | +0.37 | -1.63 | +nan | -1.63 | -1.67 |
| MYM | 5 | h4 | event | with signal | 3643 | -0.012 | 0.201 | -0.49 | -2.49 | +nan | -2.49 | -2.38 |
| MYM | 5 | h8 | event | against signal | 3643 | +0.022 | 0.201 | +0.91 | -1.09 | +nan | -1.09 | -1.24 |
| MYM | 5 | h16 | event | with signal | 3643 | +0.039 | 0.201 | -0.52 | -2.52 | +nan | -2.52 | -2.39 |
| MYM | 5 | eod | event | against signal | 3643 | +0.578 | 0.201 | +2.37 | +0.37 | +nan | +0.37 | +1.01 |
| MYM | 15 | h1 | event | against signal | 1195 | +0.087 | 0.109 | +1.66 | -0.34 | +nan | -0.34 | -0.37 |
| MYM | 15 | h2 | event | against signal | 1195 | +0.109 | 0.109 | +2.00 | +0.00 | +nan | +0.00 | -0.09 |
| MYM | 15 | h4 | event | against signal | 1195 | +0.095 | 0.109 | +2.65 | +0.65 | +nan | +0.65 | +0.54 |
| MYM | 15 | h8 | event | with signal | 1195 | +0.002 | 0.109 | -0.83 | -2.83 | +nan | -2.83 | -2.71 |
| MYM | 15 | h16 | event | with signal | 1195 | -0.016 | 0.109 | -0.04 | -2.04 | +nan | -2.04 | -1.26 |
| MYM | 15 | eod | event | with signal | 1195 | +0.388 | 0.109 | +4.36 | +2.36 | +nan | +2.36 | +3.15 |
| MYM | 60 | h1 | event | with signal | 292 | +0.053 | 0.053 | +2.54 | +0.54 | +nan | +0.54 | +0.41 |
| MYM | 60 | h2 | event | with signal | 292 | +0.022 | 0.053 | +3.17 | +1.17 | +nan | +1.17 | +0.87 |
| MYM | 60 | h4 | event | against signal | 292 | +0.038 | 0.053 | -2.89 | -4.89 | +nan | -4.89 | -4.45 |
| MYM | 60 | h8 | event | against signal | 292 | +0.006 | 0.053 | -3.55 | -5.55 | +nan | -5.55 | -4.74 |
| MYM | 60 | h16 | event | against signal | 292 | +0.124 | 0.053 | -0.37 | -2.37 | +nan | -2.37 | -1.55 |
| MYM | 60 | eod | event | against signal | 292 | +0.129 | 0.053 | +0.04 | -1.96 | +nan | -1.96 | -1.10 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.870 | +0.973 | +0.723 | +0.329 | -0.047 | +0.000 | -0.073 | -0.097 | -0.094 | -0.061 | -0.083 |
| MES | 15 | +0.945 | +1.066 | +0.851 | +0.395 | -0.001 | +0.000 | -0.074 | -0.060 | -0.089 | -0.051 | +0.016 |
| MES | 60 | +1.465 | +1.243 | +1.034 | +0.577 | +0.041 | +0.000 | +0.006 | -0.014 | -0.035 | -0.272 | -1.268 |
| MNQ | 5 | +1.040 | +1.161 | +0.893 | +0.449 | +0.015 | +0.000 | -0.031 | -0.021 | -0.029 | +0.001 | +0.017 |
| MNQ | 15 | +1.106 | +1.198 | +0.958 | +0.451 | +0.012 | +0.000 | +0.006 | +0.037 | +0.044 | +0.056 | +0.070 |
| MNQ | 60 | +1.482 | +1.330 | +1.108 | +0.677 | +0.011 | +0.000 | +0.036 | +0.069 | -0.051 | -0.091 | -1.319 |
| MYM | 5 | +1.049 | +1.150 | +0.866 | +0.437 | +0.020 | +0.000 | -0.007 | -0.006 | -0.002 | -0.007 | +0.074 |
| MYM | 15 | +0.972 | +1.099 | +0.843 | +0.389 | -0.010 | +0.000 | -0.083 | -0.103 | -0.094 | +0.008 | +0.048 |
| MYM | 60 | +1.196 | +0.988 | +0.786 | +0.453 | +0.018 | +0.000 | +0.047 | +0.005 | +0.044 | +0.083 | +0.448 |

## Calibration

- MES 5-min: 1036271 bars, 7986 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 2436 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 568 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 8163 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 2378 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 595 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 3643 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1195 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 292 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39500 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
