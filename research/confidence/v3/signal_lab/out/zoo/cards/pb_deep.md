# Impact card: pb_deep

pullback setups with depth >= 61.8% [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.016 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.047 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.31 at recent bar sizes, 90% range up to $0.96); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.031 R20 over the next 1 bar (15 min), p=0.15; we would catch an effect of 0.079 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.23).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.99 at recent bar sizes, 90% range up to $3.54); about 1.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.104 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.140 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.19).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $6.20 at recent bar sizes, 90% range up to $6.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.041 R20 over the next 4 bars (20 min), p=0.47; we would catch an effect of 0.044 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.42).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.11 at recent bar sizes, 90% range up to $2.28); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.018 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.19).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.88 at recent bar sizes, 90% range up to $4.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.240 R20 over the rest of the session (to 16:45), p=0.22; we would catch an effect of 0.155 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $22.60 at recent bar sizes, 90% range up to $14.95); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.025 R20 over the next 2 bars (10 min), p=0.9; we would catch an effect of 0.056 R20 or more 80% of the time).
- MYM 5-min size: the market moves 6% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.668 R20, possible, q=0.252, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.92 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.158 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.061 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.100 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.38).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.37 at recent bar sizes, 90% range up to $4.09); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.063 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.203 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.48).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.77 at recent bar sizes, 90% range up to $11.30); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.004 | -0.018 .. +0.010 | -0.0004 | 0.61 / 0.62 / 0.67 | 0.667 |  |  | 10/16 | -0.007 | -0.001 |  | -0.5 / -0.5 |  |
| MES | 5 | h2 * | -0.016 | -0.037 .. +0.004 | -0.0013 | 0.12 / 0.12 / 0.18 | 0.161 | 1 | 1 | 9/16 | -0.003 | -0.030 | False | -1.5 / -1.6 |  |
| MES | 5 | h4 | -0.001 | -0.033 .. +0.030 | -0.0001 | 0.93 / 0.93 / 0.94 | 0.932 |  |  | 10/16 | -0.017 | +0.014 |  | -0.1 / -0.1 | 0.047 |
| MES | 5 | h8 | +0.006 | -0.043 .. +0.055 | +0.0002 | 0.8 / 0.79 / 0.81 | 0.8 |  |  | 7/16 | -0.018 | +0.030 |  | +0.3 / +0.3 |  |
| MES | 5 | h16 | -0.012 | -0.085 .. +0.060 | -0.0003 | 0.74 / 0.73 / 0.74 | 0.74 |  |  | 12/16 | -0.011 | -0.014 |  | -0.3 / -0.3 |  |
| MES | 5 | eod | -0.187 | -0.542 .. +0.168 | -0.0010 | 0.3 / 0.29 / 0.29 | 0.285 |  |  | 9/16 | -0.012 | -0.360 |  | -1.2 / -1.0 |  |
| MES | 15 | h1 * | -0.031 | -0.058 .. -0.004 | -0.0037 | 0.022 / 0.026 / 0.031 | 0.0318 | 1 | 0.985 | 14/16 | -0.032 | -0.031 | False | -2.1 / -2.3 |  |
| MES | 15 | h2 | -0.032 | -0.070 .. +0.006 | -0.0025 | 0.094 / 0.096 / 0.14 | 0.131 |  |  | 10/16 | -0.011 | -0.053 |  | -1.7 / -1.7 |  |
| MES | 15 | h4 | -0.014 | -0.063 .. +0.035 | -0.0007 | 0.58 / 0.59 / 0.66 | 0.647 |  |  | 10/16 | +0.008 | -0.036 |  | -0.5 / -0.6 | 0.079 |
| MES | 15 | h8 | -0.025 | -0.102 .. +0.053 | -0.0009 | 0.54 / 0.54 / 0.58 | 0.56 |  |  | 10/16 | +0.026 | -0.075 |  | -0.6 / -0.6 |  |
| MES | 15 | h16 | +0.067 | -0.049 .. +0.182 | +0.0017 | 0.26 / 0.26 / 0.31 | 0.309 |  |  | 11/16 | +0.068 | +0.066 |  | +1.1 / +1.1 |  |
| MES | 15 | eod | +0.075 | -0.184 .. +0.334 | +0.0008 | 0.57 / 0.58 / 0.65 | 0.648 |  |  | 6/16 | -0.231 | +0.379 |  | +0.6 / +0.6 |  |
| MES | 60 | h1 | +0.007 | -0.044 .. +0.057 | +0.0008 | 0.79 / 0.79 / 0.81 | 0.8 |  |  | 8/16 | +0.027 | -0.014 |  | +0.3 / +0.3 |  |
| MES | 60 | h2 | +0.006 | -0.066 .. +0.078 | +0.0005 | 0.87 / 0.87 / 0.88 | 0.872 |  |  | 9/16 | +0.043 | -0.032 |  | +0.2 / +0.2 |  |
| MES | 60 | h4 | -0.018 | -0.113 .. +0.077 | -0.0011 | 0.71 / 0.7 / 0.73 | 0.725 |  |  | 9/16 | +0.034 | -0.070 |  | -0.4 / -0.4 | 0.140 |
| MES | 60 | h8 | -0.008 | -0.122 .. +0.106 | -0.0004 | 0.89 / 0.89 / 0.91 | 0.911 |  |  | 7/16 | +0.126 | -0.142 |  | -0.1 / -0.1 |  |
| MES | 60 | h16 | -0.010 | -0.175 .. +0.156 | -0.0003 | 0.91 / 0.91 / 0.92 | 0.919 |  |  | 8/16 | +0.155 | -0.174 |  | -0.1 / -0.1 |  |
| MES | 60 | eod * | +0.104 | -0.094 .. +0.302 | +0.0034 | 0.3 / 0.3 / 0.33 | 0.329 | 1 | 1 | 12/16 | +0.255 | -0.047 | False | +1.0 / +1.0 |  |
| MNQ | 5 | h1 | -0.011 | -0.024 .. +0.002 | -0.0013 | 0.084 / 0.078 / 0.19 | 0.154 |  |  | 10/16 | -0.011 | -0.012 |  | -1.7 / -1.7 |  |
| MNQ | 5 | h2 | -0.023 | -0.043 .. -0.003 | -0.0016 | 0.028 / 0.024 / 0.11 | 0.0818 |  |  | 11/16 | -0.015 | -0.030 |  | -2.4 / -2.2 |  |
| MNQ | 5 | h4 * | -0.041 | -0.071 .. -0.011 | -0.0019 | 0.0077 / 0.0073 / 0.051 | 0.0542 | 1 | 0.826 | 12/16 | -0.035 | -0.047 | False | -2.8 / -2.7 | 0.044 |
| MNQ | 5 | h8 | -0.032 | -0.075 .. +0.011 | -0.0010 | 0.15 / 0.14 / 0.31 | 0.266 |  |  | 10/16 | -0.013 | -0.051 |  | -1.5 / -1.4 |  |
| MNQ | 5 | h16 | -0.031 | -0.095 .. +0.033 | -0.0007 | 0.35 / 0.35 / 0.5 | 0.477 |  |  | 10/16 | -0.042 | -0.020 |  | -0.9 / -0.9 |  |
| MNQ | 5 | eod | -0.088 | -0.490 .. +0.314 | -0.0004 | 0.67 / 0.66 / 0.69 | 0.706 |  |  | 9/16 | -0.038 | -0.137 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h1 * | -0.018 | -0.043 .. +0.007 | -0.0019 | 0.15 / 0.15 / 0.26 | 0.185 | 1 | 1 | 9/16 | -0.015 | -0.022 | False | -1.4 / -1.4 |  |
| MNQ | 15 | h2 | -0.025 | -0.058 .. +0.009 | -0.0015 | 0.15 / 0.17 / 0.37 | 0.239 |  |  | 9/16 | -0.023 | -0.027 |  | -1.4 / -1.4 |  |
| MNQ | 15 | h4 | -0.014 | -0.065 .. +0.037 | -0.0005 | 0.58 / 0.59 / 0.76 | 0.635 |  |  | 8/16 | -0.036 | +0.008 |  | -0.5 / -0.5 | 0.076 |
| MNQ | 15 | h8 | -0.035 | -0.115 .. +0.046 | -0.0010 | 0.4 / 0.39 / 0.57 | 0.484 |  |  | 9/16 | -0.059 | -0.011 |  | -0.9 / -0.8 |  |
| MNQ | 15 | h16 | +0.013 | -0.106 .. +0.133 | +0.0003 | 0.82 / 0.82 / 0.86 | 0.838 |  |  | 9/16 | -0.031 | +0.058 |  | +0.2 / +0.2 |  |
| MNQ | 15 | eod | -0.090 | -0.431 .. +0.250 | -0.0007 | 0.6 / 0.61 / 0.7 | 0.656 |  |  | 9/16 | -0.234 | +0.053 |  | -0.6 / -0.5 |  |
| MNQ | 60 | h1 | -0.017 | -0.066 .. +0.031 | -0.0020 | 0.48 / 0.47 / 0.52 | 0.525 |  |  | 11/16 | +0.002 | -0.037 |  | -0.7 / -0.7 |  |
| MNQ | 60 | h2 | +0.017 | -0.069 .. +0.102 | +0.0013 | 0.7 / 0.69 / 0.68 | 0.684 |  |  | 6/16 | +0.088 | -0.055 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h4 | -0.053 | -0.179 .. +0.074 | -0.0030 | 0.41 / 0.41 / 0.34 | 0.332 |  |  | 10/16 | +0.019 | -0.125 |  | -0.9 / -0.8 | 0.155 |
| MNQ | 60 | h8 | +0.034 | -0.102 .. +0.171 | +0.0014 | 0.62 / 0.63 / 0.62 | 0.615 |  |  | 12/16 | +0.123 | -0.054 |  | +0.5 / +0.5 |  |
| MNQ | 60 | h16 | +0.083 | -0.119 .. +0.285 | +0.0026 | 0.42 / 0.42 / 0.42 | 0.417 |  |  | 10/16 | +0.205 | -0.040 |  | +0.8 / +0.8 |  |
| MNQ | 60 | eod * | +0.240 | +0.020 .. +0.461 | +0.0073 | 0.032 / 0.036 / 0.033 | 0.0359 | 1 | 0.993 | 12/16 | +0.387 | +0.094 | False | +2.1 / +2.1 |  |
| MYM | 5 | h1 | -0.001 | -0.018 .. +0.016 | -0.0001 | 0.94 / 0.93 / 0.95 | 0.943 |  |  | 5/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 5 | h2 * | -0.025 | -0.048 .. -0.001 | -0.0017 | 0.041 / 0.046 / 0.24 | 0.141 | 1 | 1 | 6/8 | n/a | -0.025 | False | -1.8 / -2.0 |  |
| MYM | 5 | h4 | -0.010 | -0.043 .. +0.023 | -0.0004 | 0.54 / 0.57 / 0.77 | 0.684 |  |  | 5/8 | n/a | -0.010 |  | -0.5 / -0.6 | 0.056 |
| MYM | 5 | h8 | -0.013 | -0.063 .. +0.036 | -0.0004 | 0.6 / 0.62 / 0.79 | 0.723 |  |  | 6/8 | n/a | -0.013 |  | -0.4 / -0.5 |  |
| MYM | 5 | h16 | -0.024 | -0.113 .. +0.065 | -0.0005 | 0.6 / 0.6 / 0.7 | 0.653 |  |  | 4/8 | n/a | -0.024 |  | -0.5 / -0.5 |  |
| MYM | 5 | eod | -0.078 | -0.535 .. +0.379 | -0.0004 | 0.74 / 0.75 / 0.79 | 0.777 |  |  | 5/8 | n/a | -0.078 |  | -0.4 / -0.3 |  |
| MYM | 15 | h1 | -0.009 | -0.041 .. +0.023 | -0.0010 | 0.6 / 0.6 / 0.68 | 0.633 |  |  | 6/8 | n/a | -0.009 |  | -0.5 / -0.5 |  |
| MYM | 15 | h2 | +0.009 | -0.040 .. +0.057 | +0.0005 | 0.73 / 0.74 / 0.83 | 0.742 |  |  | 4/8 | n/a | +0.009 |  | +0.3 / +0.3 |  |
| MYM | 15 | h4 | -0.000 | -0.070 .. +0.069 | -0.0000 | 0.99 / 0.99 / 1 | 0.994 |  |  | 3/8 | n/a | -0.000 |  | -0.0 / -0.0 | 0.100 |
| MYM | 15 | h8 * | -0.061 | -0.170 .. +0.047 | -0.0018 | 0.27 / 0.25 / 0.52 | 0.338 | 1 | 1 | 6/8 | n/a | -0.061 | False | -1.2 / -1.1 |  |
| MYM | 15 | h16 | -0.015 | -0.179 .. +0.148 | -0.0003 | 0.85 / 0.85 / 0.9 | 0.872 |  |  | 5/8 | n/a | -0.015 |  | -0.2 / -0.2 |  |
| MYM | 15 | eod | -0.160 | -0.559 .. +0.240 | -0.0013 | 0.43 / 0.43 / 0.58 | 0.545 |  |  | 6/8 | n/a | -0.160 |  | -0.8 / -0.8 |  |
| MYM | 60 | h1 | -0.041 | -0.121 .. +0.039 | -0.0049 | 0.32 / 0.32 / 0.3 | 0.299 |  |  | 6/8 | n/a | -0.041 |  | -1.0 / -1.0 |  |
| MYM | 60 | h2 * | -0.063 | -0.158 .. +0.032 | -0.0053 | 0.19 / 0.2 / 0.24 | 0.247 | 1 | 1 | 5/8 | n/a | -0.063 | False | -1.2 / -1.3 |  |
| MYM | 60 | h4 | -0.076 | -0.194 .. +0.042 | -0.0046 | 0.21 / 0.21 / 0.3 | 0.292 |  |  | 5/8 | n/a | -0.076 |  | -1.2 / -1.3 | 0.203 |
| MYM | 60 | h8 | -0.083 | -0.241 .. +0.076 | -0.0036 | 0.31 / 0.33 / 0.38 | 0.374 |  |  | 6/8 | n/a | -0.083 |  | -1.0 / -1.0 |  |
| MYM | 60 | h16 | -0.146 | -0.380 .. +0.088 | -0.0049 | 0.22 / 0.22 / 0.3 | 0.301 |  |  | 6/8 | n/a | -0.146 |  | -1.2 / -1.2 |  |
| MYM | 60 | eod | -0.116 | -0.402 .. +0.170 | -0.0037 | 0.43 / 0.41 / 0.46 | 0.465 |  |  | 5/8 | n/a | -0.116 |  | -0.8 / -0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.008 | -0.019 .. +0.002 | -1.6% | -0.024 | 0.18 | 1 | 8/16 |
| MES | 5 | h2 | -0.006 | -0.020 .. +0.008 | -0.9% | -0.026 | 0.59 |  | 8/16 |
| MES | 5 | h4 | +0.010 | -0.012 .. +0.031 | +1.0% | -0.020 | 0.46 |  | 9/16 |
| MES | 5 | h8 | +0.005 | -0.030 .. +0.040 | +0.3% | -0.011 | 0.89 |  | 9/16 |
| MES | 5 | h16 | -0.000 | -0.052 .. +0.052 | -0.0% | -0.023 | 0.99 |  | 10/16 |
| MES | 5 | eod | -0.183 | -0.460 .. +0.094 | -1.8% | -0.380 | 0.2 |  | 9/16 |
| MES | 15 | h1 | +0.014 | -0.006 .. +0.034 | +2.7% | -0.011 | 0.17 |  | 9/16 |
| MES | 15 | h2 | +0.003 | -0.023 .. +0.030 | +0.4% | -0.013 | 0.81 |  | 8/16 |
| MES | 15 | h4 | -0.018 | -0.054 .. +0.018 | -1.7% | -0.033 | 0.57 |  | 12/16 |
| MES | 15 | h8 | +0.004 | -0.056 .. +0.063 | +0.2% | -0.037 | 0.91 |  | 6/16 |
| MES | 15 | h16 | -0.001 | -0.077 .. +0.076 | -0.0% | -0.054 | 0.98 |  | 9/16 |
| MES | 15 | eod * | -0.237 | -0.419 .. -0.054 | -4.3% | -0.291 | 0.039 | 1 | 12/16 |
| MES | 60 | h1 | -0.009 | -0.042 .. +0.024 | -1.8% | -0.028 | 0.97 |  | 11/16 |
| MES | 60 | h2 | -0.016 | -0.063 .. +0.031 | -2.2% | -0.047 | 0.86 |  | 9/16 |
| MES | 60 | h4 | -0.024 | -0.091 .. +0.042 | -2.3% | -0.031 | 0.6 |  | 10/16 |
| MES | 60 | h8 | -0.079 | -0.154 .. -0.005 | -5.3% | -0.051 | 0.13 |  | 11/16 |
| MES | 60 | h16 * | -0.132 | -0.234 .. -0.031 | -6.4% | -0.062 | 0.032 | 1 | 13/16 |
| MES | 60 | eod | -0.036 | -0.153 .. +0.081 | -1.7% | -0.032 | 0.6 |  | 9/16 |
| MNQ | 5 | h1 | -0.012 | -0.021 .. -0.003 | -2.3% | -0.028 | 0.13 |  | 12/16 |
| MNQ | 5 | h2 * | -0.022 | -0.035 .. -0.009 | -2.9% | -0.039 | 0.069 | 1 | 12/16 |
| MNQ | 5 | h4 | -0.010 | -0.033 .. +0.012 | -0.9% | -0.041 | 0.68 |  | 9/16 |
| MNQ | 5 | h8 | -0.016 | -0.050 .. +0.018 | -1.0% | -0.048 | 0.53 |  | 8/16 |
| MNQ | 5 | h16 | -0.010 | -0.066 .. +0.046 | -0.4% | -0.076 | 0.74 |  | 6/16 |
| MNQ | 5 | eod | -0.283 | -0.604 .. +0.039 | -2.2% | -0.550 | 0.085 |  | 11/16 |
| MNQ | 15 | h1 * | -0.020 | -0.036 .. -0.004 | -3.8% | -0.039 | 0.031 | 1 | 13/16 |
| MNQ | 15 | h2 | -0.026 | -0.051 .. +0.000 | -3.3% | -0.060 | 0.34 |  | 13/16 |
| MNQ | 15 | h4 | -0.007 | -0.049 .. +0.036 | -0.6% | -0.061 | 0.76 |  | 9/16 |
| MNQ | 15 | h8 | -0.016 | -0.079 .. +0.047 | -1.0% | -0.101 | 0.63 |  | 9/16 |
| MNQ | 15 | h16 | -0.033 | -0.120 .. +0.055 | -1.3% | -0.185 | 0.47 |  | 9/16 |
| MNQ | 15 | eod | -0.117 | -0.379 .. +0.145 | -1.8% | -0.241 | 0.42 |  | 7/16 |
| MNQ | 60 | h1 * | -0.029 | -0.061 .. +0.003 | -5.5% | -0.041 | 0.18 | 1 | 12/16 |
| MNQ | 60 | h2 | -0.003 | -0.064 .. +0.057 | -0.4% | -0.005 | 0.92 |  | 9/16 |
| MNQ | 60 | h4 | +0.022 | -0.068 .. +0.113 | +2.0% | +0.032 | 0.69 |  | 8/16 |
| MNQ | 60 | h8 | +0.003 | -0.090 .. +0.097 | +0.2% | +0.060 | 0.95 |  | 8/16 |
| MNQ | 60 | h16 | +0.042 | -0.080 .. +0.165 | +1.9% | +0.112 | 0.51 |  | 10/16 |
| MNQ | 60 | eod | +0.053 | -0.084 .. +0.190 | +2.3% | +0.097 | 0.45 |  | 9/16 |
| MYM | 5 | h1 | -0.009 | -0.021 .. +0.003 | -1.7% | -0.030 | 0.16 |  | 6/8 |
| MYM | 5 | h2 | -0.023 | -0.042 .. -0.005 | -3.0% | -0.042 | 0.072 |  | 7/8 |
| MYM | 5 | h4 | -0.012 | -0.042 .. +0.017 | -1.1% | -0.044 | 0.53 |  | 4/8 |
| MYM | 5 | h8 | +0.006 | -0.045 .. +0.056 | +0.4% | -0.051 | 0.86 |  | 5/8 |
| MYM | 5 | h16 | +0.020 | -0.057 .. +0.097 | +0.8% | -0.061 | 0.97 |  | 5/8 |
| MYM | 5 | eod * | -0.668 | -1.001 .. -0.336 | -5.7% | -0.943 | 0.0015 | 0.252 | 8/8 |
| MYM | 15 | h1 | -0.014 | -0.035 .. +0.006 | -2.7% | -0.038 | 0.61 |  | 7/8 |
| MYM | 15 | h2 | -0.010 | -0.043 .. +0.024 | -1.3% | -0.047 | 0.93 |  | 5/8 |
| MYM | 15 | h4 | -0.049 | -0.102 .. +0.005 | -4.4% | -0.097 | 0.49 |  | 6/8 |
| MYM | 15 | h8 | -0.071 | -0.149 .. +0.008 | -4.3% | -0.130 | 0.36 |  | 5/8 |
| MYM | 15 | h16 | -0.010 | -0.136 .. +0.116 | -0.4% | -0.144 | 0.88 |  | 3/8 |
| MYM | 15 | eod * | -0.368 | -0.683 .. -0.053 | -6.1% | -0.439 | 0.063 | 1 | 7/8 |
| MYM | 60 | h1 | +0.037 | -0.019 .. +0.093 | +7.0% | +0.001 | 0.22 |  | 6/8 |
| MYM | 60 | h2 | -0.020 | -0.088 .. +0.048 | -2.6% | -0.027 | 0.81 |  | 6/8 |
| MYM | 60 | h4 | -0.039 | -0.120 .. +0.041 | -3.6% | -0.029 | 0.53 |  | 6/8 |
| MYM | 60 | h8 | -0.017 | -0.121 .. +0.088 | -1.1% | -0.039 | 0.89 |  | 3/8 |
| MYM | 60 | h16 * | -0.198 | -0.350 .. -0.047 | -9.3% | -0.099 | 0.08 | 1 | 6/8 |
| MYM | 60 | eod | -0.142 | -0.319 .. +0.035 | -6.4% | -0.055 | 0.23 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.20 pts | -0.83 .. +1.23 | 0.71 |
| MES | 15 | +1.28 pts | -0.36 .. +2.92 | 0.17 |
| MES | 60 | +0.22 pts | -2.87 .. +3.31 | 0.89 |
| MNQ | 5 | -0.39 pts | -1.30 .. +0.52 | 0.63 |
| MNQ | 15 | -0.60 pts | -2.15 .. +0.94 | 0.58 |
| MNQ | 60 | +0.00 pts | -3.31 .. +3.31 | 1 |
| MYM | 5 | -0.59 pts | -1.77 .. +0.59 | 0.34 |
| MYM | 15 | -0.59 pts | -2.71 .. +1.52 | 0.59 |
| MYM | 60 | -2.84 pts | -7.23 .. +1.55 | 0.22 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 7303 | +0.005 | 0.240 | -0.08 | -3.58 | -3.37 | -3.71 | -3.60 |
| MES | 5 | h2 | event | against signal | 7303 | +0.017 | 0.240 | +0.16 | -3.34 | -3.42 | -3.29 | -3.35 |
| MES | 5 | h4 | event | against signal | 7303 | +0.002 | 0.240 | -0.14 | -3.64 | -3.26 | -3.86 | -3.64 |
| MES | 5 | h8 | event | with signal | 7303 | +0.006 | 0.240 | +0.25 | -3.25 | -3.68 | -2.99 | -3.24 |
| MES | 5 | h16 | event | against signal | 7303 | +0.013 | 0.240 | -0.17 | -3.67 | -3.12 | -4.00 | -3.70 |
| MES | 5 | eod | event | against signal | 7303 | +0.089 | 0.240 | +2.18 | -1.32 | -2.97 | -0.35 | +0.32 |
| MES | 15 | h1 | event | against signal | 2874 | +0.032 | 0.151 | +0.74 | -2.76 | -3.09 | -2.51 | -2.78 |
| MES | 15 | h2 | event | against signal | 2874 | +0.032 | 0.151 | +1.29 | -2.21 | -3.44 | -1.30 | -2.22 |
| MES | 15 | h4 | event | against signal | 2874 | +0.013 | 0.151 | +0.98 | -2.52 | -3.60 | -1.72 | -2.50 |
| MES | 15 | h8 | event | against signal | 2874 | +0.021 | 0.151 | +1.76 | -1.74 | -3.71 | -0.28 | -1.67 |
| MES | 15 | h16 | event | with signal | 2874 | +0.083 | 0.151 | +0.76 | -2.74 | -2.58 | -2.86 | -3.13 |
| MES | 15 | eod | event | with signal | 2874 | +0.135 | 0.151 | +0.18 | -3.32 | -4.74 | -2.26 | -4.76 |
| MES | 60 | h1 | event | with signal | 773 | +0.007 | 0.089 | -0.33 | -3.83 | -2.57 | -5.19 | -3.83 |
| MES | 60 | h2 | event | with signal | 773 | +0.009 | 0.089 | -0.18 | -3.68 | -2.69 | -4.74 | -3.75 |
| MES | 60 | h4 | event | against signal | 773 | +0.014 | 0.089 | +1.28 | -2.22 | -3.61 | -0.73 | -2.16 |
| MES | 60 | h8 | event | against signal | 773 | +0.001 | 0.089 | +2.39 | -1.11 | -6.01 | +4.14 | -1.03 |
| MES | 60 | h16 | event | against signal | 773 | -0.003 | 0.089 | +1.56 | -1.94 | -6.69 | +3.16 | -1.73 |
| MES | 60 | eod | event | with signal | 773 | +0.111 | 0.089 | +3.78 | +0.28 | +2.20 | -1.78 | +0.40 |
| MNQ | 5 | h1 | event | against signal | 10974 | +0.011 | 0.106 | +0.16 | -1.84 | -1.88 | -1.82 | -1.83 |
| MNQ | 5 | h2 | event | against signal | 10974 | +0.021 | 0.106 | +0.53 | -1.47 | -1.85 | -1.24 | -1.43 |
| MNQ | 5 | h4 | event | against signal | 10974 | +0.038 | 0.106 | +0.57 | -1.43 | -1.71 | -1.25 | -1.34 |
| MNQ | 5 | h8 | event | against signal | 10974 | +0.025 | 0.106 | +1.23 | -0.77 | -1.86 | -0.08 | -0.63 |
| MNQ | 5 | h16 | event | against signal | 10974 | +0.019 | 0.106 | +0.62 | -1.38 | -1.70 | -1.18 | -1.18 |
| MNQ | 5 | eod | event | against signal | 10974 | -0.141 | 0.106 | +0.10 | -1.90 | -1.15 | -2.37 | +2.46 |
| MNQ | 15 | h1 | event | against signal | 3551 | +0.018 | 0.063 | +0.14 | -1.86 | -1.83 | -1.88 | -1.89 |
| MNQ | 15 | h2 | event | against signal | 3551 | +0.025 | 0.063 | +0.85 | -1.15 | -1.65 | -0.78 | -1.19 |
| MNQ | 15 | h4 | event | against signal | 3551 | +0.013 | 0.063 | +0.42 | -1.58 | -1.42 | -1.71 | -1.55 |
| MNQ | 15 | h8 | event | against signal | 3551 | +0.027 | 0.063 | +1.13 | -0.87 | -1.28 | -0.57 | -0.74 |
| MNQ | 15 | h16 | event | with signal | 3551 | +0.038 | 0.063 | +1.63 | -0.37 | -2.16 | +0.96 | -1.07 |
| MNQ | 15 | eod | event | against signal | 3551 | +0.012 | 0.063 | +1.33 | -0.67 | -0.19 | -1.02 | +1.92 |
| MNQ | 60 | h1 | event | against signal | 750 | +0.015 | 0.034 | +3.11 | +1.11 | -2.11 | +4.11 | +1.20 |
| MNQ | 60 | h2 | event | with signal | 750 | +0.022 | 0.034 | -2.09 | -4.09 | -1.26 | -6.73 | -4.31 |
| MNQ | 60 | h4 | event | against signal | 750 | +0.042 | 0.034 | +5.74 | +3.74 | -0.76 | +7.93 | +4.21 |
| MNQ | 60 | h8 | event | with signal | 750 | +0.051 | 0.034 | +0.43 | -1.57 | -0.94 | -2.15 | -2.29 |
| MNQ | 60 | h16 | event | with signal | 750 | +0.112 | 0.034 | +4.11 | +2.11 | +1.73 | +2.47 | +0.56 |
| MNQ | 60 | eod | event | with signal | 750 | +0.273 | 0.034 | +11.22 | +9.22 | +4.84 | +13.31 | +7.76 |
| MYM | 5 | h1 | event | against signal | 6051 | +0.001 | 0.158 | +0.06 | -1.94 | +nan | -1.94 | -1.95 |
| MYM | 5 | h2 | event | against signal | 6051 | +0.023 | 0.158 | +0.23 | -1.77 | +nan | -1.77 | -1.75 |
| MYM | 5 | h4 | event | against signal | 6051 | +0.004 | 0.158 | +0.12 | -1.88 | +nan | -1.88 | -1.78 |
| MYM | 5 | h8 | event | against signal | 6051 | +0.001 | 0.158 | +0.12 | -1.88 | +nan | -1.88 | -1.68 |
| MYM | 5 | h16 | event | against signal | 6051 | +0.006 | 0.158 | +0.23 | -1.77 | +nan | -1.77 | -1.47 |
| MYM | 5 | eod | event | against signal | 6051 | -0.022 | 0.158 | -0.04 | -2.04 | +nan | -2.04 | -0.72 |
| MYM | 15 | h1 | event | against signal | 1918 | +0.008 | 0.090 | +0.65 | -1.35 | +nan | -1.35 | -1.35 |
| MYM | 15 | h2 | event | with signal | 1918 | +0.009 | 0.090 | -0.52 | -2.52 | +nan | -2.52 | -2.53 |
| MYM | 15 | h4 | event | against signal | 1918 | -0.002 | 0.090 | +0.56 | -1.44 | +nan | -1.44 | -1.37 |
| MYM | 15 | h8 | event | against signal | 1918 | +0.056 | 0.090 | +1.84 | -0.16 | +nan | -0.16 | +0.03 |
| MYM | 15 | h16 | event | against signal | 1918 | +0.008 | 0.090 | +0.57 | -1.43 | +nan | -1.43 | -1.16 |
| MYM | 15 | eod | event | against signal | 1918 | +0.125 | 0.090 | +2.98 | +0.98 | +nan | +0.98 | +1.28 |
| MYM | 60 | h1 | event | against signal | 398 | +0.040 | 0.045 | +2.15 | +0.15 | +nan | +0.15 | +0.17 |
| MYM | 60 | h2 | event | against signal | 398 | +0.061 | 0.045 | +2.83 | +0.83 | +nan | +0.83 | +0.90 |
| MYM | 60 | h4 | event | against signal | 398 | +0.076 | 0.045 | +4.42 | +2.42 | +nan | +2.42 | +2.39 |
| MYM | 60 | h8 | event | against signal | 398 | +0.077 | 0.045 | +5.01 | +3.01 | +nan | +3.01 | +3.15 |
| MYM | 60 | h16 | event | against signal | 398 | +0.138 | 0.045 | +8.38 | +6.38 | +nan | +6.38 | +6.61 |
| MYM | 60 | eod | event | against signal | 398 | +0.113 | 0.045 | +7.72 | +5.72 | +nan | +5.72 | +5.60 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.898 | +0.910 | -0.304 | -0.189 | -0.051 | +0.000 | -0.003 | -0.017 | -0.003 | +0.003 | -0.026 |
| MES | 15 | +0.932 | +1.080 | -0.249 | -0.161 | -0.037 | +0.000 | -0.030 | -0.032 | -0.013 | -0.038 | +0.080 |
| MES | 60 | +1.133 | +1.068 | -0.206 | -0.118 | -0.024 | +0.000 | +0.009 | +0.019 | -0.030 | +0.000 | +0.059 |
| MNQ | 5 | +0.984 | +1.043 | -0.250 | -0.156 | -0.032 | +0.000 | -0.011 | -0.023 | -0.041 | -0.032 | -0.034 |
| MNQ | 15 | +0.980 | +1.131 | -0.210 | -0.142 | -0.033 | +0.000 | -0.016 | -0.024 | -0.016 | -0.031 | +0.031 |
| MNQ | 60 | +1.250 | +1.154 | -0.234 | -0.154 | -0.032 | +0.000 | -0.016 | +0.016 | -0.080 | +0.034 | +0.102 |
| MYM | 5 | +0.956 | +1.037 | -0.291 | -0.169 | -0.047 | +0.000 | -0.002 | -0.027 | -0.013 | -0.018 | -0.038 |
| MYM | 15 | +0.978 | +1.110 | -0.230 | -0.138 | -0.026 | +0.000 | -0.007 | +0.010 | -0.004 | -0.078 | -0.068 |
| MYM | 60 | +1.095 | +1.144 | -0.198 | -0.088 | +0.009 | +0.000 | -0.044 | -0.065 | -0.092 | -0.028 | -0.284 |

## Calibration

- MES 5-min: 1036271 bars, 7303 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 2874 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 773 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 10974 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 3551 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 750 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 6051 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1918 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 398 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 20000 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
