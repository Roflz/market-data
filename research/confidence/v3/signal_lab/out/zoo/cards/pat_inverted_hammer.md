# Impact card: pat_inverted_hammer

candle pattern inverted_hammer in its textbook direction: range >= avgR10, upper >= 2 x body, lower <= 0.1 x range, prior close < EMA10 -> bullish (textbook) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.034 R20 over the next 4 bars (20 min), p=0.81; we would catch an effect of 0.055 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.038 R20, CONFIRMED, q=0.0063, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.08 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.252 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.155 R20 over the next 16 bars (4 h), p=0.95; we would catch an effect of 0.130 R20 or more 80% of the time).
- MES 15-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.060 R20, CONFIRMED, q=0.0485, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.37 at recent bar sizes, 90% range up to $4.89); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.119 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.281 R20 or more 80% of the time).
- MES 60-min size: the market moves 28% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.209 R20, possible, q=0.135, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $7.32 at recent bar sizes, 90% range up to $19.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.062 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.067 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.066 R20, CONFIRMED, q=1.09e-07, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.46 at recent bar sizes, 90% range up to $1.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.063 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.150 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 17% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.089 R20, CONFIRMED, q=0.0015, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.99 at recent bar sizes, 90% range up to $7.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.180 R20 over the next 2 bars (2 h), p=0.16; we would catch an effect of 0.311 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $18.33 at recent bar sizes, 90% range up to $34.62); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.058 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.106 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.19).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.65 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.195 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.225 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.215 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.80 at recent bar sizes, 90% range up to $6.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.107 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.413 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.17).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.56 at recent bar sizes, 90% range up to $26.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.005 | -0.018 .. +0.027 | +0.0005 | 0.69 / 0.69 / 0.65 | 0.648 |  |  | 9/16 | +0.031 | -0.022 |  | +0.4 / +0.4 |  |
| MES | 5 | h2 | +0.015 | -0.016 .. +0.046 | +0.0011 | 0.34 / 0.34 / 0.3 | 0.303 |  |  | 8/16 | +0.033 | -0.004 |  | +1.0 / +0.9 |  |
| MES | 5 | h4 * | +0.034 | -0.007 .. +0.075 | +0.0017 | 0.1 / 0.11 / 0.099 | 0.0904 | 1 | 1 | 10/16 | +0.063 | +0.006 | False | +1.6 / +1.6 | 0.055 |
| MES | 5 | h8 | +0.027 | -0.033 .. +0.088 | +0.0009 | 0.38 / 0.38 / 0.37 | 0.361 |  |  | 11/16 | +0.084 | -0.030 |  | +0.9 / +0.9 |  |
| MES | 5 | h16 | +0.021 | -0.068 .. +0.110 | +0.0005 | 0.64 / 0.64 / 0.64 | 0.633 |  |  | 9/16 | +0.106 | -0.063 |  | +0.5 / +0.5 |  |
| MES | 5 | eod | +0.009 | -0.677 .. +0.695 | +0.0000 | 0.98 / 0.98 / 0.96 | 0.954 |  |  | 10/16 | +0.639 | -0.617 |  | +0.0 / +0.0 |  |
| MES | 15 | h1 | +0.011 | -0.035 .. +0.056 | +0.0009 | 0.65 / 0.65 / 0.65 | 0.641 |  |  | 9/16 | +0.003 | +0.018 |  | +0.4 / +0.5 |  |
| MES | 15 | h2 | -0.021 | -0.085 .. +0.044 | -0.0012 | 0.53 / 0.53 / 0.55 | 0.529 |  |  | 8/16 | -0.020 | -0.022 |  | -0.6 / -0.6 |  |
| MES | 15 | h4 | +0.030 | -0.066 .. +0.127 | +0.0012 | 0.54 / 0.55 / 0.55 | 0.518 |  |  | 9/16 | +0.034 | +0.027 |  | +0.6 / +0.6 | 0.130 |
| MES | 15 | h8 | +0.054 | -0.088 .. +0.196 | +0.0015 | 0.46 / 0.46 / 0.46 | 0.457 |  |  | 10/16 | -0.019 | +0.126 |  | +0.8 / +0.7 |  |
| MES | 15 | h16 * | +0.155 | -0.048 .. +0.359 | +0.0030 | 0.13 / 0.13 / 0.11 | 0.113 | 1 | 1 | 9/16 | +0.091 | +0.219 | False | +1.6 / +1.5 |  |
| MES | 15 | eod | +0.071 | -0.548 .. +0.690 | +0.0005 | 0.82 / 0.83 / 0.8 | 0.793 |  |  | 9/16 | -0.132 | +0.273 |  | +0.3 / +0.2 |  |
| MES | 60 | h1 | +0.039 | -0.096 .. +0.174 | +0.0034 | 0.57 / 0.58 / 0.42 | 0.409 |  |  | 8/16 | +0.128 | -0.050 |  | +0.6 / +0.6 |  |
| MES | 60 | h2 | -0.024 | -0.207 .. +0.158 | -0.0015 | 0.79 / 0.79 / 0.72 | 0.727 |  |  | 9/16 | +0.135 | -0.184 |  | -0.3 / -0.3 |  |
| MES | 60 | h4 | -0.051 | -0.267 .. +0.164 | -0.0022 | 0.64 / 0.64 / 0.59 | 0.594 |  |  | 10/16 | +0.108 | -0.210 |  | -0.5 / -0.5 | 0.281 |
| MES | 60 | h8 | -0.074 | -0.371 .. +0.223 | -0.0023 | 0.63 / 0.61 / 0.58 | 0.581 |  |  | 10/16 | +0.227 | -0.375 |  | -0.5 / -0.5 |  |
| MES | 60 | h16 | -0.118 | -0.431 .. +0.196 | -0.0028 | 0.46 / 0.45 / 0.43 | 0.422 |  |  | 12/16 | +0.120 | -0.355 |  | -0.8 / -0.7 |  |
| MES | 60 | eod * | -0.119 | -0.433 .. +0.194 | -0.0027 | 0.46 / 0.45 / 0.42 | 0.414 | 1 | 1 | 12/16 | +0.111 | -0.350 | False | -0.8 / -0.7 |  |
| MNQ | 5 | h1 | +0.011 | -0.018 .. +0.041 | +0.0009 | 0.45 / 0.44 / 0.38 | 0.358 |  |  | 7/16 | +0.044 | -0.021 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h2 | +0.012 | -0.024 .. +0.049 | +0.0006 | 0.5 / 0.49 / 0.54 | 0.494 |  |  | 7/16 | +0.029 | -0.004 |  | +0.7 / +0.7 |  |
| MNQ | 5 | h4 | +0.006 | -0.046 .. +0.058 | +0.0002 | 0.82 / 0.82 / 0.84 | 0.836 |  |  | 10/16 | +0.021 | -0.009 |  | +0.2 / +0.2 | 0.067 |
| MNQ | 5 | h8 | +0.004 | -0.073 .. +0.080 | +0.0001 | 0.92 / 0.92 / 0.94 | 0.922 |  |  | 9/16 | +0.035 | -0.027 |  | +0.1 / +0.1 |  |
| MNQ | 5 | h16 * | +0.062 | -0.053 .. +0.177 | +0.0010 | 0.29 / 0.29 / 0.35 | 0.334 | 1 | 1 | 8/16 | +0.114 | +0.011 | False | +1.1 / +1.1 |  |
| MNQ | 5 | eod | +0.472 | -0.615 .. +1.558 | +0.0015 | 0.39 / 0.4 / 0.2 | 0.198 |  |  | 9/16 | +1.245 | -0.295 |  | +1.3 / +0.9 |  |
| MNQ | 15 | h1 | +0.006 | -0.052 .. +0.063 | +0.0004 | 0.85 / 0.85 / 0.86 | 0.829 |  |  | 8/16 | -0.006 | +0.017 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h2 | -0.049 | -0.132 .. +0.034 | -0.0019 | 0.25 / 0.23 / 0.38 | 0.216 |  |  | 13/16 | -0.091 | -0.007 |  | -1.2 / -1.1 |  |
| MNQ | 15 | h4 | -0.013 | -0.129 .. +0.102 | -0.0003 | 0.82 / 0.82 / 0.89 | 0.816 |  |  | 9/16 | -0.079 | +0.052 |  | -0.2 / -0.2 | 0.150 |
| MNQ | 15 | h8 | -0.015 | -0.175 .. +0.145 | -0.0003 | 0.86 / 0.85 / 0.89 | 0.86 |  |  | 7/16 | -0.131 | +0.100 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h16 * | +0.063 | -0.172 .. +0.299 | +0.0009 | 0.6 / 0.6 / 0.64 | 0.604 | 1 | 1 | 6/16 | -0.027 | +0.153 | False | +0.6 / +0.5 |  |
| MNQ | 15 | eod | -0.056 | -0.803 .. +0.690 | -0.0003 | 0.88 / 0.88 / 0.88 | 0.869 |  |  | 8/16 | -0.327 | +0.213 |  | -0.2 / -0.1 |  |
| MNQ | 60 | h1 | +0.037 | -0.058 .. +0.131 | +0.0028 | 0.45 / 0.46 / 0.52 | 0.495 |  |  | 8/16 | +0.053 | +0.020 |  | +0.7 / +0.8 |  |
| MNQ | 60 | h2 * | +0.180 | +0.055 .. +0.305 | +0.0096 | 0.0048 / 0.0089 / 0.023 | 0.025 | 1 | 0.673 | 13/16 | +0.228 | +0.132 | False | +2.5 / +2.8 |  |
| MNQ | 60 | h4 | +0.082 | -0.125 .. +0.288 | +0.0031 | 0.44 / 0.46 / 0.46 | 0.46 |  |  | 9/16 | +0.200 | -0.037 |  | +0.7 / +0.8 | 0.311 |
| MNQ | 60 | h8 | +0.073 | -0.236 .. +0.383 | +0.0020 | 0.64 / 0.65 / 0.63 | 0.623 |  |  | 10/16 | +0.224 | -0.077 |  | +0.5 / +0.5 |  |
| MNQ | 60 | h16 | +0.065 | -0.273 .. +0.403 | +0.0014 | 0.71 / 0.71 / 0.7 | 0.701 |  |  | 9/16 | +0.118 | +0.012 |  | +0.4 / +0.4 |  |
| MNQ | 60 | eod | +0.075 | -0.263 .. +0.414 | +0.0015 | 0.66 / 0.66 / 0.66 | 0.655 |  |  | 11/16 | +0.132 | +0.018 |  | +0.5 / +0.4 |  |
| MYM | 5 | h1 | +0.001 | -0.039 .. +0.041 | +0.0001 | 0.96 / 0.96 / 0.97 | 0.962 |  |  | 4/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 5 | h2 * | +0.058 | -0.001 .. +0.117 | +0.0025 | 0.054 / 0.048 / 0.11 | 0.0632 | 1 | 1 | 6/8 | n/a | +0.058 | False | +2.0 / +1.9 |  |
| MYM | 5 | h4 | +0.056 | -0.024 .. +0.137 | +0.0015 | 0.17 / 0.17 / 0.35 | 0.213 |  |  | 6/8 | n/a | +0.056 |  | +1.4 / +1.4 | 0.106 |
| MYM | 5 | h8 | +0.070 | -0.039 .. +0.179 | +0.0013 | 0.21 / 0.21 / 0.38 | 0.297 |  |  | 5/8 | n/a | +0.070 |  | +1.3 / +1.3 |  |
| MYM | 5 | h16 | +0.024 | -0.147 .. +0.195 | +0.0004 | 0.78 / 0.78 / 0.83 | 0.818 |  |  | 5/8 | n/a | +0.024 |  | +0.3 / +0.3 |  |
| MYM | 5 | eod | +0.048 | -1.289 .. +1.386 | +0.0002 | 0.94 / 0.94 / 0.92 | 0.932 |  |  | 4/8 | n/a | +0.048 |  | +0.1 / +0.1 |  |
| MYM | 15 | h1 | +0.037 | -0.039 .. +0.112 | +0.0024 | 0.34 / 0.34 / 0.44 | 0.334 |  |  | 3/8 | n/a | +0.037 |  | +0.9 / +0.9 |  |
| MYM | 15 | h2 | -0.025 | -0.127 .. +0.076 | -0.0010 | 0.62 / 0.64 / 0.74 | 0.648 |  |  | 5/8 | n/a | -0.025 |  | -0.4 / -0.5 |  |
| MYM | 15 | h4 | -0.015 | -0.161 .. +0.130 | -0.0003 | 0.84 / 0.85 / 0.9 | 0.85 |  |  | 6/8 | n/a | -0.015 |  | -0.2 / -0.2 | 0.215 |
| MYM | 15 | h8 | -0.017 | -0.226 .. +0.191 | -0.0003 | 0.87 / 0.87 / 0.9 | 0.878 |  |  | 3/8 | n/a | -0.017 |  | -0.2 / -0.2 |  |
| MYM | 15 | h16 | -0.002 | -0.293 .. +0.288 | -0.0000 | 0.99 / 0.99 / 0.99 | 0.992 |  |  | 2/8 | n/a | -0.002 |  | -0.0 / -0.0 |  |
| MYM | 15 | eod * | -0.225 | -1.079 .. +0.629 | -0.0012 | 0.61 / 0.62 / 0.67 | 0.612 | 1 | 1 | 4/8 | n/a | -0.225 | False | -0.6 / -0.5 |  |
| MYM | 60 | h1 | -0.005 | -0.127 .. +0.118 | -0.0004 | 0.94 / 0.94 / 0.95 | 0.954 |  |  | 3/8 | n/a | -0.005 |  | -0.1 / -0.1 |  |
| MYM | 60 | h2 * | -0.107 | -0.272 .. +0.059 | -0.0065 | 0.21 / 0.23 / 0.3 | 0.297 | 1 | 1 | 7/8 | n/a | -0.107 | False | -1.3 / -1.3 |  |
| MYM | 60 | h4 | -0.121 | -0.389 .. +0.147 | -0.0053 | 0.38 / 0.38 / 0.39 | 0.407 |  |  | 6/8 | n/a | -0.121 |  | -0.9 / -0.9 | 0.413 |
| MYM | 60 | h8 | -0.217 | -0.553 .. +0.119 | -0.0069 | 0.21 / 0.23 / 0.25 | 0.256 |  |  | 6/8 | n/a | -0.217 |  | -1.3 / -1.3 |  |
| MYM | 60 | h16 | -0.175 | -0.526 .. +0.176 | -0.0042 | 0.33 / 0.34 / 0.4 | 0.395 |  |  | 7/8 | n/a | -0.175 |  | -1.1 / -1.0 |  |
| MYM | 60 | eod | -0.167 | -0.518 .. +0.184 | -0.0039 | 0.35 / 0.37 / 0.42 | 0.414 |  |  | 7/8 | n/a | -0.167 |  | -1.0 / -0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.038 | +0.020 .. +0.055 | +7.5% | +0.069 | 2.9e-05 | 0.0063 | 14/16 |
| MES | 5 | h2 | +0.025 | +0.002 .. +0.047 | +3.5% | +0.070 | 0.032 |  | 9/16 |
| MES | 5 | h4 | +0.049 | +0.019 .. +0.080 | +4.9% | +0.091 | 0.0021 |  | 11/16 |
| MES | 5 | h8 | +0.055 | +0.012 .. +0.098 | +3.8% | +0.099 | 0.026 |  | 11/16 |
| MES | 5 | h16 | +0.029 | -0.032 .. +0.089 | +1.4% | +0.071 | 0.78 |  | 10/16 |
| MES | 5 | eod | +0.029 | -0.345 .. +0.402 | +0.3% | +0.452 | 0.88 |  | 6/16 |
| MES | 15 | h1 * | +0.060 | +0.028 .. +0.091 | +11.7% | +0.103 | 0.00026 | 0.0485 | 15/16 |
| MES | 15 | h2 | +0.079 | +0.033 .. +0.125 | +10.8% | +0.139 | 0.00071 |  | 13/16 |
| MES | 15 | h4 | +0.105 | +0.041 .. +0.168 | +9.9% | +0.172 | 0.0012 |  | 12/16 |
| MES | 15 | h8 | +0.065 | -0.026 .. +0.157 | +4.3% | +0.187 | 0.22 |  | 10/16 |
| MES | 15 | h16 | +0.079 | -0.055 .. +0.213 | +3.5% | +0.208 | 0.31 |  | 8/16 |
| MES | 15 | eod | +0.383 | -0.000 .. +0.766 | +7.0% | +0.568 | 0.05 |  | 11/16 |
| MES | 60 | h1 | +0.162 | +0.057 .. +0.267 | +31.6% | +0.178 | 0.0026 |  | 12/16 |
| MES | 60 | h2 * | +0.209 | +0.087 .. +0.331 | +28.3% | +0.276 | 0.00077 | 0.135 | 14/16 |
| MES | 60 | h4 | +0.117 | -0.026 .. +0.260 | +11.0% | +0.258 | 0.29 |  | 11/16 |
| MES | 60 | h8 | +0.101 | -0.080 .. +0.282 | +6.7% | +0.211 | 0.51 |  | 10/16 |
| MES | 60 | h16 | +0.017 | -0.165 .. +0.199 | +0.8% | +0.166 | 0.96 |  | 9/16 |
| MES | 60 | eod | +0.016 | -0.166 .. +0.199 | +0.8% | +0.170 | 0.96 |  | 10/16 |
| MNQ | 5 | h1 * | +0.066 | +0.045 .. +0.086 | +12.3% | +0.107 | 3.4e-10 | 1.09e-07 | 16/16 |
| MNQ | 5 | h2 | +0.048 | +0.021 .. +0.076 | +6.3% | +0.120 | 0.00058 |  | 14/16 |
| MNQ | 5 | h4 | +0.040 | +0.004 .. +0.076 | +3.6% | +0.136 | 0.13 |  | 11/16 |
| MNQ | 5 | h8 | +0.087 | +0.029 .. +0.145 | +5.4% | +0.206 | 0.027 |  | 10/16 |
| MNQ | 5 | h16 | +0.074 | -0.010 .. +0.159 | +3.1% | +0.230 | 0.32 |  | 10/16 |
| MNQ | 5 | eod | +0.605 | -0.019 .. +1.228 | +4.8% | +1.882 | 0.057 |  | 10/16 |
| MNQ | 15 | h1 * | +0.089 | +0.050 .. +0.128 | +16.7% | +0.138 | 6.4e-06 | 0.0015 | 15/16 |
| MNQ | 15 | h2 | +0.109 | +0.057 .. +0.161 | +14.1% | +0.162 | 0.087 |  | 12/16 |
| MNQ | 15 | h4 | +0.082 | +0.000 .. +0.164 | +7.2% | +0.183 | 0.15 |  | 11/16 |
| MNQ | 15 | h8 | +0.018 | -0.088 .. +0.125 | +1.1% | +0.138 | 0.95 |  | 7/16 |
| MNQ | 15 | h16 | -0.044 | -0.200 .. +0.112 | -1.7% | +0.121 | 0.73 |  | 9/16 |
| MNQ | 15 | eod | +0.146 | -0.336 .. +0.629 | +2.3% | +0.449 | 0.55 |  | 8/16 |
| MNQ | 60 | h1 | +0.003 | -0.062 .. +0.068 | +0.5% | +0.028 | 0.93 |  | 11/16 |
| MNQ | 60 | h2 | +0.001 | -0.084 .. +0.087 | +0.2% | +0.030 | 0.98 |  | 8/16 |
| MNQ | 60 | h4 * | +0.075 | -0.063 .. +0.213 | +6.8% | +0.068 | 0.49 | 1 | 8/16 |
| MNQ | 60 | h8 | +0.032 | -0.157 .. +0.221 | +2.0% | +0.138 | 0.83 |  | 9/16 |
| MNQ | 60 | h16 | -0.029 | -0.215 .. +0.157 | -1.3% | +0.117 | 0.76 |  | 10/16 |
| MNQ | 60 | eod | -0.029 | -0.215 .. +0.157 | -1.3% | +0.112 | 0.76 |  | 10/16 |
| MYM | 5 | h1 | +0.047 | +0.016 .. +0.078 | +8.8% | +0.099 | 0.15 |  | 8/8 |
| MYM | 5 | h2 | +0.072 | +0.033 .. +0.111 | +9.5% | +0.110 | 0.098 |  | 7/8 |
| MYM | 5 | h4 * | +0.078 | +0.019 .. +0.137 | +7.1% | +0.152 | 0.032 | 1 | 8/8 |
| MYM | 5 | h8 | +0.087 | +0.002 .. +0.173 | +5.5% | +0.153 | 0.053 |  | 7/8 |
| MYM | 5 | h16 | +0.072 | -0.049 .. +0.192 | +3.1% | +0.121 | 0.24 |  | 6/8 |
| MYM | 5 | eod | +0.552 | -0.160 .. +1.265 | +4.7% | +1.066 | 0.35 |  | 5/8 |
| MYM | 15 | h1 | +0.036 | -0.019 .. +0.092 | +6.9% | +0.115 | 0.95 |  | 5/8 |
| MYM | 15 | h2 | +0.093 | +0.011 .. +0.174 | +12.1% | +0.137 | 0.45 |  | 6/8 |
| MYM | 15 | h4 * | +0.160 | +0.057 .. +0.262 | +14.3% | +0.222 | 0.18 | 1 | 6/8 |
| MYM | 15 | h8 | +0.047 | -0.092 .. +0.186 | +2.9% | +0.130 | 0.83 |  | 3/8 |
| MYM | 15 | h16 | -0.226 | -0.439 .. -0.013 | -9.2% | -0.063 | 0.22 |  | 7/8 |
| MYM | 15 | eod | -0.270 | -0.867 .. +0.326 | -4.5% | +0.273 | 0.41 |  | 6/8 |
| MYM | 60 | h1 | +0.001 | -0.075 .. +0.077 | +0.2% | +0.024 | 0.98 |  | 4/8 |
| MYM | 60 | h2 | -0.070 | -0.180 .. +0.041 | -9.2% | -0.010 | 0.22 |  | 6/8 |
| MYM | 60 | h4 | -0.078 | -0.259 .. +0.103 | -7.2% | -0.034 | 0.4 |  | 6/8 |
| MYM | 60 | h8 | -0.210 | -0.444 .. +0.024 | -13.6% | -0.074 | 0.081 |  | 6/8 |
| MYM | 60 | h16 * | -0.284 | -0.488 .. -0.080 | -13.4% | -0.133 | 0.028 | 1 | 8/8 |
| MYM | 60 | eod | -0.287 | -0.495 .. -0.079 | -12.9% | -0.144 | 0.029 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +1.80 pts | +0.49 .. +3.12 | 0.01 |
| MES | 15 | +0.62 pts | -1.78 .. +3.03 | 0.61 |
| MES | 60 | +0.17 pts | -4.85 .. +5.19 | 0.97 |
| MNQ | 5 | +0.67 pts | -0.70 .. +2.04 | 0.57 |
| MNQ | 15 | -0.20 pts | -2.63 .. +2.23 | 0.87 |
| MNQ | 60 | +4.67 pts | +0.12 .. +9.22 | 0.11 |
| MYM | 5 | +1.74 pts | -0.20 .. +3.69 | 0.12 |
| MYM | 15 | +1.34 pts | -2.22 .. +4.90 | 0.47 |
| MYM | 60 | +0.67 pts | -6.09 .. +7.43 | 0.85 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 5864 | +0.006 | 0.435 | -0.09 | -3.59 | -3.37 | -3.93 | -3.59 |
| MES | 5 | h2 | event | with signal | 5864 | +0.020 | 0.435 | +0.13 | -3.37 | -3.36 | -3.40 | -3.38 |
| MES | 5 | h4 | event | with signal | 5864 | +0.046 | 0.435 | +0.13 | -3.37 | -3.20 | -3.63 | -3.41 |
| MES | 5 | h8 | event | with signal | 5864 | +0.054 | 0.435 | -0.21 | -3.71 | -3.19 | -4.52 | -3.83 |
| MES | 5 | h16 | event | with signal | 5864 | +0.079 | 0.435 | -0.22 | -3.72 | -2.97 | -4.89 | -3.98 |
| MES | 5 | eod | event | with signal | 5864 | +0.698 | 0.435 | +1.69 | -1.81 | +0.71 | -5.77 | -3.32 |
| MES | 15 | h1 | event | with signal | 1513 | +0.018 | 0.210 | +0.54 | -2.96 | -3.59 | -2.11 | -3.02 |
| MES | 15 | h2 | event | against signal | 1513 | +0.008 | 0.210 | +0.15 | -3.35 | -3.26 | -3.48 | -3.25 |
| MES | 15 | h4 | event | with signal | 1513 | +0.057 | 0.210 | +0.81 | -2.69 | -3.34 | -1.82 | -2.89 |
| MES | 15 | h8 | event | with signal | 1513 | +0.106 | 0.210 | +1.94 | -1.56 | -3.80 | +1.46 | -1.91 |
| MES | 15 | h16 | event | with signal | 1513 | +0.250 | 0.210 | +3.19 | -0.31 | -2.70 | +2.91 | -0.78 |
| MES | 15 | eod | event | with signal | 1513 | +0.397 | 0.210 | +5.53 | +2.03 | -1.18 | +6.36 | +1.78 |
| MES | 60 | h1 | event | with signal | 373 | +0.050 | 0.087 | -0.39 | -3.89 | -1.14 | -6.77 | -4.22 |
| MES | 60 | h2 | event | against signal | 373 | +0.003 | 0.087 | +3.64 | +0.14 | -6.18 | +6.78 | +0.73 |
| MES | 60 | h4 | event | against signal | 373 | +0.008 | 0.087 | +4.80 | +1.30 | -6.52 | +9.50 | +2.51 |
| MES | 60 | h8 | event | against signal | 373 | -0.001 | 0.087 | +6.91 | +3.41 | -10.46 | +17.96 | +5.43 |
| MES | 60 | h16 | event | against signal | 373 | +0.023 | 0.087 | +5.65 | +2.15 | -9.48 | +14.36 | +4.19 |
| MES | 60 | eod | event | against signal | 373 | +0.022 | 0.087 | +5.27 | +1.77 | -9.48 | +13.57 | +3.81 |
| MNQ | 5 | h1 | event | with signal | 5272 | +0.016 | 0.201 | -0.23 | -2.23 | -1.91 | -2.86 | -2.23 |
| MNQ | 5 | h2 | event | with signal | 5272 | +0.022 | 0.201 | +0.06 | -1.94 | -1.94 | -1.95 | -1.95 |
| MNQ | 5 | h4 | event | with signal | 5272 | +0.026 | 0.201 | +0.00 | -2.00 | -1.89 | -2.22 | -2.03 |
| MNQ | 5 | h8 | event | with signal | 5272 | +0.045 | 0.201 | -0.12 | -2.12 | -1.90 | -2.58 | -2.22 |
| MNQ | 5 | h16 | event | with signal | 5272 | +0.141 | 0.201 | +0.68 | -1.32 | -1.56 | -0.84 | -1.52 |
| MNQ | 5 | eod | event | with signal | 5272 | +1.445 | 0.201 | +4.23 | +2.23 | +1.71 | +3.28 | +2.29 |
| MNQ | 15 | h1 | event | with signal | 1454 | +0.016 | 0.091 | +0.57 | -1.43 | -2.18 | -0.20 | -1.56 |
| MNQ | 15 | h2 | event | against signal | 1454 | +0.033 | 0.091 | -0.17 | -2.17 | -1.47 | -3.32 | -2.04 |
| MNQ | 15 | h4 | event | against signal | 1454 | -0.017 | 0.091 | -1.18 | -3.18 | -1.50 | -5.94 | -2.86 |
| MNQ | 15 | h8 | event | against signal | 1454 | -0.051 | 0.091 | -1.75 | -3.75 | -1.53 | -7.41 | -3.14 |
| MNQ | 15 | h16 | event | with signal | 1454 | +0.157 | 0.091 | +1.80 | -0.20 | -1.74 | +2.34 | -0.36 |
| MNQ | 15 | eod | event | against signal | 1454 | -0.326 | 0.091 | -7.47 | -9.47 | -4.06 | -18.37 | -10.64 |
| MNQ | 60 | h1 | event | with signal | 328 | +0.048 | 0.037 | +0.08 | -1.92 | -0.63 | -3.61 | -2.31 |
| MNQ | 60 | h2 | event | with signal | 328 | +0.200 | 0.037 | +4.09 | +2.09 | +1.72 | +2.58 | +1.63 |
| MNQ | 60 | h4 | event | with signal | 328 | +0.124 | 0.037 | -7.15 | -9.15 | +1.50 | -23.10 | -10.30 |
| MNQ | 60 | h8 | event | with signal | 328 | +0.152 | 0.037 | -13.22 | -15.22 | +3.03 | -39.12 | -17.09 |
| MNQ | 60 | h16 | event | with signal | 328 | +0.173 | 0.037 | -14.00 | -16.00 | +2.33 | -40.00 | -17.09 |
| MNQ | 60 | eod | event | with signal | 328 | +0.182 | 0.037 | -13.91 | -15.91 | +2.48 | -40.00 | -16.51 |
| MYM | 5 | h1 | event | with signal | 2373 | -0.003 | 0.195 | -0.19 | -2.19 | +nan | -2.19 | -2.15 |
| MYM | 5 | h2 | event | with signal | 2373 | +0.049 | 0.195 | +0.26 | -1.74 | +nan | -1.74 | -1.66 |
| MYM | 5 | h4 | event | with signal | 2373 | +0.037 | 0.195 | +0.01 | -1.99 | +nan | -1.99 | -1.80 |
| MYM | 5 | h8 | event | with signal | 2373 | +0.040 | 0.195 | -0.08 | -2.08 | +nan | -2.08 | -1.81 |
| MYM | 5 | h16 | event | with signal | 2373 | -0.013 | 0.195 | -0.20 | -2.20 | +nan | -2.20 | -1.96 |
| MYM | 5 | eod | event | with signal | 2373 | +0.255 | 0.195 | +0.85 | -1.15 | +nan | -1.15 | -1.65 |
| MYM | 15 | h1 | event | with signal | 712 | +0.036 | 0.094 | +1.04 | -0.96 | +nan | -0.96 | -0.93 |
| MYM | 15 | h2 | event | against signal | 712 | +0.033 | 0.094 | -0.07 | -2.07 | +nan | -2.07 | -2.23 |
| MYM | 15 | h4 | event | against signal | 712 | +0.019 | 0.094 | -0.75 | -2.75 | +nan | -2.75 | -2.87 |
| MYM | 15 | h8 | event | against signal | 712 | +0.021 | 0.094 | -2.68 | -4.68 | +nan | -4.68 | -4.79 |
| MYM | 15 | h16 | event | against signal | 712 | +0.060 | 0.094 | -1.92 | -3.92 | +nan | -3.92 | -4.97 |
| MYM | 15 | eod | event | against signal | 712 | +0.189 | 0.094 | -3.79 | -5.79 | +nan | -5.79 | -7.57 |
| MYM | 60 | h1 | event | against signal | 208 | -0.005 | 0.047 | -0.79 | -2.79 | +nan | -2.79 | -2.32 |
| MYM | 60 | h2 | event | against signal | 208 | +0.093 | 0.047 | +2.22 | +0.22 | +nan | +0.22 | +0.96 |
| MYM | 60 | h4 | event | against signal | 208 | +0.097 | 0.047 | +7.74 | +5.74 | +nan | +5.74 | +6.98 |
| MYM | 60 | h8 | event | against signal | 208 | +0.178 | 0.047 | +10.76 | +8.76 | +nan | +8.76 | +11.00 |
| MYM | 60 | h16 | event | against signal | 208 | +0.117 | 0.047 | +8.30 | +6.30 | +nan | +6.30 | +10.01 |
| MYM | 60 | eod | event | against signal | 208 | +0.105 | 0.047 | +7.70 | +5.70 | +nan | +5.70 | +9.90 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.767 | +0.902 | +0.686 | +0.329 | -0.003 | +0.000 | +0.078 | +0.088 | +0.109 | +0.105 | +0.096 |
| MES | 15 | +0.878 | +0.922 | +0.710 | +0.344 | -0.033 | +0.000 | +0.054 | +0.026 | +0.083 | +0.128 | +0.243 |
| MES | 60 | +1.171 | +0.899 | +0.759 | +0.352 | -0.050 | +0.000 | +0.045 | -0.025 | -0.119 | -0.035 | -1.402 |
| MNQ | 5 | +0.843 | +1.013 | +0.745 | +0.298 | -0.060 | +0.000 | +0.062 | +0.063 | +0.058 | +0.058 | +0.120 |
| MNQ | 15 | +0.896 | +0.952 | +0.708 | +0.336 | -0.075 | +0.000 | +0.029 | -0.021 | +0.010 | +0.021 | +0.111 |
| MNQ | 60 | +0.923 | +0.917 | +0.709 | +0.297 | -0.058 | +0.000 | +0.045 | +0.203 | +0.086 | +0.190 | -2.186 |
| MYM | 5 | +0.775 | +0.898 | +0.676 | +0.293 | -0.070 | +0.000 | +0.020 | +0.076 | +0.073 | +0.079 | +0.030 |
| MYM | 15 | +0.858 | +0.968 | +0.718 | +0.331 | -0.097 | +0.000 | +0.052 | -0.005 | +0.009 | -0.005 | +0.020 |
| MYM | 60 | +1.122 | +0.882 | +0.706 | +0.329 | -0.056 | +0.000 | -0.007 | -0.124 | -0.165 | -0.588 | -0.573 |

## Calibration

- MES 5-min: 1036271 bars, 5864 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1513 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 373 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 5272 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1454 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 328 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 2373 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 712 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 208 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43296 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
