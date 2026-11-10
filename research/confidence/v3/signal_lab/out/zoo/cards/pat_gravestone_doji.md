# Impact card: pat_gravestone_doji

candle pattern gravestone_doji in its textbook direction: doji AND lower shadow <= 0.1 x range AND upper shadow >= 0.6 x range -> bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.013 R20 over the next 4 bars (20 min), p=0.76; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 5-min size: the market moves 5% LESS after the event than after matched bars over the next 2 bars (10 min) (-0.038 R20, CONFIRMED, q=4.56e-10, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $0.46); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.069 R20 over the next 8 bars (2 h), p=0.3; we would catch an effect of 0.060 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.35).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.95 at recent bar sizes, 90% range up to $3.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.017 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.136 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.97 at recent bar sizes, 90% range up to $6.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.030 R20 over the next 4 bars (20 min), p=0.29; we would catch an effect of 0.035 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% LESS after the event than after matched bars over the next 16 bars (80 min) (-0.159 R20, CONFIRMED, q=0.000108, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.72 at recent bar sizes, 90% range up to $1.93); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.815 R20 over the rest of the session (to 16:45), p=0.016; we would catch an effect of 0.069 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 13% LESS after the event than after matched bars over the next 8 bars (2 h) (-0.220 R20, CONFIRMED, q=9.93e-07, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $36.33 at recent bar sizes, 90% range up to $3.79); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.041 R20 over the next 2 bars (2 h), p=0.76; we would catch an effect of 0.120 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.17).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.00 at recent bar sizes, 90% range up to $9.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -1.296 R20 over the rest of the session (to 16:45), p=0.075; we would catch an effect of 0.059 R20 or more 80% of the time).
- MYM 5-min size: the market moves 11% LESS after the event than after matched bars over the next 16 bars (80 min) (-0.260 R20, CONFIRMED, q=0.000193, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $13.92 at recent bar sizes, 90% range up to $1.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.292 R20 over the next 16 bars (4 h), p=0.027; we would catch an effect of 0.103 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.053).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.23 at recent bar sizes, 90% range up to $4.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.192 R20 over the next 4 bars (4 h), p=0.057; we would catch an effect of 0.189 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.037).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.50 at recent bar sizes, 90% range up to $13.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.005 .. +0.009 | +0.0006 | 0.53 / 0.54 / 0.59 | 0.595 |  |  | 10/16 | +0.002 | +0.003 |  | +0.6 / +0.6 |  |
| MES | 5 | h2 | +0.000 | -0.010 .. +0.011 | +0.0001 | 0.93 / 0.93 / 0.98 | 0.976 |  |  | 9/16 | -0.000 | +0.001 |  | +0.1 / +0.1 |  |
| MES | 5 | h4 * | -0.013 | -0.029 .. +0.002 | -0.0016 | 0.095 / 0.1 / 0.11 | 0.119 | 1 | 1 | 12/16 | -0.023 | -0.003 | False | -1.8 / -1.7 | 0.026 |
| MES | 5 | h8 | -0.018 | -0.043 .. +0.006 | -0.0015 | 0.14 / 0.15 / 0.14 | 0.141 |  |  | 11/16 | -0.030 | -0.006 |  | -1.7 / -1.5 |  |
| MES | 5 | h16 | -0.003 | -0.041 .. +0.036 | -0.0002 | 0.89 / 0.9 / 0.86 | 0.862 |  |  | 8/16 | -0.014 | +0.009 |  | -0.2 / -0.1 |  |
| MES | 5 | eod | -0.487 | -1.157 .. +0.182 | -0.0056 | 0.15 / 0.16 / 0.02 | 0.0172 |  |  | 10/16 | -0.613 | -0.362 |  | -4.6 / -1.4 |  |
| MES | 15 | h1 | +0.000 | -0.021 .. +0.021 | +0.0000 | 0.99 / 0.99 / 1 | 0.997 |  |  | 8/16 | +0.005 | -0.005 |  | +0.0 / +0.0 |  |
| MES | 15 | h2 | +0.003 | -0.026 .. +0.033 | +0.0003 | 0.82 / 0.82 / 0.82 | 0.816 |  |  | 9/16 | +0.006 | +0.001 |  | +0.2 / +0.2 |  |
| MES | 15 | h4 | -0.025 | -0.067 .. +0.017 | -0.0016 | 0.24 / 0.25 / 0.25 | 0.238 |  |  | 10/16 | -0.032 | -0.018 |  | -1.2 / -1.2 | 0.060 |
| MES | 15 | h8 * | -0.069 | -0.139 .. -0.000 | -0.0031 | 0.05 / 0.045 / 0.034 | 0.0404 | 1 | 1 | 12/16 | -0.063 | -0.075 | False | -2.2 / -2.0 |  |
| MES | 15 | h16 | -0.059 | -0.180 .. +0.063 | -0.0018 | 0.35 / 0.32 / 0.27 | 0.268 |  |  | 9/16 | -0.012 | -0.105 |  | -1.1 / -0.9 |  |
| MES | 15 | eod | -0.219 | -0.661 .. +0.222 | -0.0027 | 0.33 / 0.33 / 0.23 | 0.239 |  |  | 11/16 | -0.180 | -0.258 |  | -1.4 / -1.0 |  |
| MES | 60 | h1 | -0.001 | -0.046 .. +0.043 | -0.0002 | 0.95 / 0.95 / 0.95 | 0.949 |  |  | 10/16 | -0.024 | +0.021 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 * | -0.017 | -0.081 .. +0.047 | -0.0014 | 0.6 / 0.61 / 0.62 | 0.616 | 1 | 1 | 8/16 | -0.070 | +0.037 | False | -0.5 / -0.5 |  |
| MES | 60 | h4 | +0.024 | -0.068 .. +0.116 | +0.0014 | 0.61 / 0.61 / 0.62 | 0.619 |  |  | 10/16 | -0.035 | +0.083 |  | +0.5 / +0.5 | 0.136 |
| MES | 60 | h8 | +0.007 | -0.122 .. +0.137 | +0.0003 | 0.91 / 0.91 / 0.92 | 0.913 |  |  | 10/16 | -0.077 | +0.092 |  | +0.1 / +0.1 |  |
| MES | 60 | h16 | -0.030 | -0.247 .. +0.188 | -0.0010 | 0.79 / 0.79 / 0.79 | 0.796 |  |  | 11/16 | -0.187 | +0.128 |  | -0.3 / -0.3 |  |
| MES | 60 | eod | +0.050 | -0.195 .. +0.296 | +0.0015 | 0.69 / 0.68 / 0.68 | 0.682 |  |  | 8/16 | -0.075 | +0.176 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h1 | +0.001 | -0.011 .. +0.014 | +0.0002 | 0.84 / 0.84 / 0.89 | 0.877 |  |  | 9/16 | -0.002 | +0.004 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h2 | -0.015 | -0.033 .. +0.003 | -0.0014 | 0.098 / 0.11 / 0.14 | 0.108 |  |  | 12/16 | -0.022 | -0.008 |  | -1.7 / -1.7 |  |
| MNQ | 5 | h4 * | -0.030 | -0.057 .. -0.003 | -0.0018 | 0.027 / 0.037 / 0.046 | 0.0422 | 1 | 0.997 | 11/16 | -0.048 | -0.012 | False | -2.3 / -2.2 | 0.035 |
| MNQ | 5 | h8 | -0.045 | -0.087 .. -0.003 | -0.0018 | 0.036 / 0.038 / 0.049 | 0.0524 |  |  | 11/16 | -0.063 | -0.027 |  | -2.4 / -2.1 |  |
| MNQ | 5 | h16 | -0.066 | -0.138 .. +0.005 | -0.0019 | 0.068 / 0.066 / 0.055 | 0.0576 |  |  | 12/16 | -0.092 | -0.041 |  | -2.3 / -1.8 |  |
| MNQ | 5 | eod | -0.736 | -1.686 .. +0.215 | -0.0045 | 0.13 / 0.15 / 0.0056 | 0.00339 |  |  | 10/16 | -1.356 | -0.121 |  | -3.4 / -1.5 |  |
| MNQ | 15 | h1 | +0.002 | -0.019 .. +0.022 | +0.0002 | 0.88 / 0.88 / 0.92 | 0.901 |  |  | 11/16 | -0.004 | +0.007 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h2 | -0.002 | -0.034 .. +0.030 | -0.0001 | 0.9 / 0.9 / 0.93 | 0.909 |  |  | 10/16 | -0.009 | +0.005 |  | -0.1 / -0.1 |  |
| MNQ | 15 | h4 | -0.004 | -0.051 .. +0.043 | -0.0001 | 0.87 / 0.86 / 0.92 | 0.877 |  |  | 8/16 | -0.009 | +0.001 |  | -0.2 / -0.2 | 0.069 |
| MNQ | 15 | h8 | -0.022 | -0.097 .. +0.052 | -0.0006 | 0.56 / 0.55 / 0.66 | 0.575 |  |  | 8/16 | -0.002 | -0.042 |  | -0.6 / -0.6 |  |
| MNQ | 15 | h16 | -0.036 | -0.186 .. +0.115 | -0.0008 | 0.64 / 0.64 / 0.59 | 0.563 |  |  | 8/16 | +0.004 | -0.074 |  | -0.6 / -0.5 |  |
| MNQ | 15 | eod * | -0.815 | -1.348 .. -0.282 | -0.0064 | 0.0027 / 0.0019 / 0.00029 | 0.00234 | 0.433 | 0.495 | 11/16 | -1.547 | -0.088 | False | -4.5 / -3.0 |  |
| MNQ | 60 | h1 | -0.009 | -0.042 .. +0.024 | -0.0011 | 0.6 / 0.61 / 0.65 | 0.659 |  |  | 8/16 | +0.015 | -0.033 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h2 * | -0.041 | -0.094 .. +0.012 | -0.0036 | 0.13 / 0.12 / 0.16 | 0.164 | 1 | 1 | 10/16 | -0.060 | -0.022 | False | -1.6 / -1.5 |  |
| MNQ | 60 | h4 | -0.030 | -0.110 .. +0.050 | -0.0019 | 0.46 / 0.46 / 0.48 | 0.487 |  |  | 10/16 | -0.070 | +0.010 |  | -0.8 / -0.7 | 0.120 |
| MNQ | 60 | h8 | -0.003 | -0.116 .. +0.109 | -0.0002 | 0.95 / 0.95 / 0.95 | 0.953 |  |  | 8/16 | -0.063 | +0.056 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h16 | +0.052 | -0.156 .. +0.259 | +0.0018 | 0.62 / 0.62 / 0.62 | 0.611 |  |  | 8/16 | -0.048 | +0.152 |  | +0.5 / +0.5 |  |
| MNQ | 60 | eod | +0.097 | -0.131 .. +0.325 | +0.0032 | 0.4 / 0.41 / 0.39 | 0.397 |  |  | 8/16 | -0.034 | +0.228 |  | +0.9 / +0.8 |  |
| MYM | 5 | h1 | +0.004 | -0.014 .. +0.022 | +0.0004 | 0.66 / 0.66 / 0.69 | 0.682 |  |  | 6/8 | n/a | +0.004 |  | +0.4 / +0.4 |  |
| MYM | 5 | h2 | -0.018 | -0.042 .. +0.006 | -0.0012 | 0.15 / 0.15 / 0.39 | 0.285 |  |  | 7/8 | n/a | -0.018 |  | -1.4 / -1.4 |  |
| MYM | 5 | h4 | -0.063 | -0.099 .. -0.027 | -0.0026 | 0.00066 / 0.00047 / 0.047 | 0.0548 |  |  | 7/8 | n/a | -0.063 |  | -3.5 / -3.4 | 0.059 |
| MYM | 5 | h8 | -0.091 | -0.148 .. -0.034 | -0.0026 | 0.0019 / 0.0018 / 0.052 | 0.0638 |  |  | 7/8 | n/a | -0.091 |  | -3.2 / -3.1 |  |
| MYM | 5 | h16 | -0.140 | -0.241 .. -0.039 | -0.0032 | 0.0067 / 0.0049 / 0.022 | 0.0306 |  |  | 7/8 | n/a | -0.140 |  | -3.2 / -2.7 |  |
| MYM | 5 | eod * | -1.296 | -2.313 .. -0.278 | -0.0066 | 0.013 / 0.011 / 6.7e-05 | 0.000527 | 1 | 0.179 | 8/8 | n/a | -1.296 | False | -4.4 / -2.5 |  |
| MYM | 15 | h1 | -0.044 | -0.091 .. +0.004 | -0.0043 | 0.075 / 0.068 / 0.036 | 0.0316 |  |  | 6/8 | n/a | -0.044 |  | -1.8 / -1.8 |  |
| MYM | 15 | h2 | -0.073 | -0.138 .. -0.008 | -0.0041 | 0.029 / 0.021 / 0.043 | 0.0279 |  |  | 7/8 | n/a | -0.073 |  | -2.3 / -2.2 |  |
| MYM | 15 | h4 | -0.076 | -0.149 .. -0.003 | -0.0026 | 0.041 / 0.038 / 0.21 | 0.0785 |  |  | 6/8 | n/a | -0.076 |  | -2.1 / -2.0 | 0.103 |
| MYM | 15 | h8 | -0.110 | -0.217 .. -0.003 | -0.0029 | 0.043 / 0.052 / 0.23 | 0.111 |  |  | 7/8 | n/a | -0.110 |  | -2.0 / -2.0 |  |
| MYM | 15 | h16 * | -0.292 | -0.453 .. -0.130 | -0.0054 | 0.00041 / 0.00037 / 0.0091 | 0.019 | 0.672 | 0.134 | 7/8 | n/a | -0.292 | False | -3.6 / -3.5 |  |
| MYM | 15 | eod | -0.617 | -1.181 .. -0.053 | -0.0047 | 0.032 / 0.026 / 0.038 | 0.0395 |  |  | 6/8 | n/a | -0.617 |  | -2.8 / -2.1 |  |
| MYM | 60 | h1 | +0.029 | -0.028 .. +0.086 | +0.0033 | 0.32 / 0.33 / 0.4 | 0.402 |  |  | 5/8 | n/a | +0.029 |  | +1.0 / +1.0 |  |
| MYM | 60 | h2 | +0.082 | +0.007 .. +0.157 | +0.0066 | 0.032 / 0.036 / 0.094 | 0.0948 |  |  | 6/8 | n/a | +0.082 |  | +2.1 / +2.1 |  |
| MYM | 60 | h4 * | +0.192 | +0.049 .. +0.335 | +0.0110 | 0.0084 / 0.0091 / 0.0061 | 0.00738 | 1 | 0.807 | 7/8 | n/a | +0.192 | False | +2.7 / +2.6 | 0.189 |
| MYM | 60 | h8 | +0.113 | -0.097 .. +0.322 | +0.0047 | 0.29 / 0.31 / 0.26 | 0.26 |  |  | 6/8 | n/a | +0.113 |  | +1.1 / +1.1 |  |
| MYM | 60 | h16 | +0.101 | -0.211 .. +0.412 | +0.0032 | 0.53 / 0.53 / 0.52 | 0.518 |  |  | 4/8 | n/a | +0.101 |  | +0.7 / +0.6 |  |
| MYM | 60 | eod | +0.078 | -0.271 .. +0.427 | +0.0024 | 0.66 / 0.65 / 0.64 | 0.661 |  |  | 5/8 | n/a | +0.078 |  | +0.5 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.021 | -0.028 .. -0.014 | -4.2% | -0.042 | 9e-10 |  | 12/16 |
| MES | 5 | h2 * | -0.038 | -0.048 .. -0.027 | -5.4% | -0.072 | 1.2e-12 | 4.56e-10 | 15/16 |
| MES | 5 | h4 | -0.052 | -0.068 .. -0.036 | -5.2% | -0.103 | 2.4e-10 |  | 13/16 |
| MES | 5 | h8 | -0.066 | -0.090 .. -0.041 | -4.6% | -0.153 | 1.4e-07 |  | 12/16 |
| MES | 5 | h16 | -0.094 | -0.133 .. -0.055 | -4.5% | -0.227 | 2.8e-06 |  | 13/16 |
| MES | 5 | eod | -0.613 | -1.019 .. -0.207 | -6.1% | -0.977 | 0.072 |  | 10/16 |
| MES | 15 | h1 | -0.010 | -0.026 .. +0.006 | -1.9% | -0.031 | 0.24 |  | 10/16 |
| MES | 15 | h2 | -0.006 | -0.026 .. +0.015 | -0.8% | -0.047 | 0.6 |  | 9/16 |
| MES | 15 | h4 | -0.025 | -0.056 .. +0.005 | -2.4% | -0.089 | 0.22 |  | 10/16 |
| MES | 15 | h8 | -0.034 | -0.084 .. +0.016 | -2.2% | -0.142 | 0.18 |  | 12/16 |
| MES | 15 | h16 | -0.078 | -0.161 .. +0.005 | -3.4% | -0.301 | 0.069 |  | 11/16 |
| MES | 15 | eod * | -0.306 | -0.571 .. -0.041 | -5.6% | -0.540 | 0.058 | 1 | 10/16 |
| MES | 60 | h1 | +0.008 | -0.025 .. +0.042 | +1.6% | -0.021 | 0.62 |  | 7/16 |
| MES | 60 | h2 | +0.000 | -0.042 .. +0.043 | +0.0% | -0.026 | 0.99 |  | 6/16 |
| MES | 60 | h4 | -0.004 | -0.066 .. +0.057 | -0.4% | -0.023 | 0.97 |  | 10/16 |
| MES | 60 | h8 | -0.027 | -0.113 .. +0.058 | -1.8% | -0.034 | 0.63 |  | 9/16 |
| MES | 60 | h16 | -0.008 | -0.136 .. +0.120 | -0.4% | -0.008 | 0.92 |  | 10/16 |
| MES | 60 | eod * | -0.058 | -0.203 .. +0.087 | -2.7% | -0.031 | 0.43 | 1 | 11/16 |
| MNQ | 5 | h1 | -0.012 | -0.021 .. -0.003 | -2.2% | -0.035 | 0.058 |  | 12/16 |
| MNQ | 5 | h2 | -0.020 | -0.035 .. -0.005 | -2.6% | -0.048 | 0.0094 |  | 11/16 |
| MNQ | 5 | h4 | -0.037 | -0.059 .. -0.014 | -3.3% | -0.090 | 0.0014 |  | 14/16 |
| MNQ | 5 | h8 | -0.083 | -0.119 .. -0.047 | -5.1% | -0.185 | 6.3e-06 |  | 14/16 |
| MNQ | 5 | h16 * | -0.159 | -0.220 .. -0.097 | -6.6% | -0.403 | 4.3e-07 | 0.000108 | 14/16 |
| MNQ | 5 | eod | -0.587 | -1.104 .. -0.071 | -4.7% | -0.986 | 0.027 |  | 9/16 |
| MNQ | 15 | h1 | -0.028 | -0.043 .. -0.012 | -5.2% | -0.071 | 0.022 |  | 12/16 |
| MNQ | 15 | h2 | -0.055 | -0.079 .. -0.030 | -7.1% | -0.123 | 0.00077 |  | 14/16 |
| MNQ | 15 | h4 | -0.119 | -0.166 .. -0.073 | -10.5% | -0.229 | 5.2e-07 |  | 12/16 |
| MNQ | 15 | h8 * | -0.220 | -0.293 .. -0.147 | -13.1% | -0.470 | 3.4e-09 | 9.93e-07 | 14/16 |
| MNQ | 15 | h16 | -0.149 | -0.264 .. -0.035 | -5.9% | -0.717 | 0.013 |  | 12/16 |
| MNQ | 15 | eod | -0.593 | -0.925 .. -0.261 | -9.3% | -1.156 | 0.0023 |  | 13/16 |
| MNQ | 60 | h1 * | -0.029 | -0.052 .. -0.005 | -5.4% | -0.050 | 0.028 | 1 | 12/16 |
| MNQ | 60 | h2 | -0.036 | -0.070 .. -0.002 | -4.7% | -0.066 | 0.15 |  | 12/16 |
| MNQ | 60 | h4 | -0.058 | -0.111 .. -0.005 | -5.2% | -0.068 | 0.16 |  | 13/16 |
| MNQ | 60 | h8 | -0.035 | -0.105 .. +0.035 | -2.2% | -0.050 | 0.7 |  | 10/16 |
| MNQ | 60 | h16 | -0.125 | -0.242 .. -0.008 | -5.7% | -0.124 | 0.082 |  | 11/16 |
| MNQ | 60 | eod | -0.133 | -0.269 .. +0.002 | -5.8% | -0.151 | 0.06 |  | 12/16 |
| MYM | 5 | h1 | -0.023 | -0.036 .. -0.010 | -4.3% | -0.042 | 0.0071 |  | 6/8 |
| MYM | 5 | h2 | -0.052 | -0.073 .. -0.032 | -6.9% | -0.090 | 0.031 |  | 8/8 |
| MYM | 5 | h4 | -0.114 | -0.146 .. -0.082 | -10.4% | -0.193 | 0.0035 |  | 8/8 |
| MYM | 5 | h8 | -0.197 | -0.249 .. -0.145 | -12.4% | -0.349 | 1e-05 |  | 8/8 |
| MYM | 5 | h16 * | -0.260 | -0.334 .. -0.186 | -11.1% | -0.565 | 7.7e-07 | 0.000193 | 8/8 |
| MYM | 5 | eod | -0.803 | -1.290 .. -0.316 | -6.9% | -1.364 | 0.0012 |  | 7/8 |
| MYM | 15 | h1 | +0.011 | -0.024 .. +0.046 | +2.1% | -0.012 | 0.55 |  | 4/8 |
| MYM | 15 | h2 | -0.011 | -0.058 .. +0.035 | -1.5% | -0.062 | 0.65 |  | 5/8 |
| MYM | 15 | h4 | -0.072 | -0.131 .. -0.013 | -6.5% | -0.161 | 0.27 |  | 7/8 |
| MYM | 15 | h8 | -0.107 | -0.194 .. -0.021 | -6.5% | -0.289 | 0.31 |  | 7/8 |
| MYM | 15 | h16 | -0.238 | -0.379 .. -0.096 | -9.6% | -0.594 | 0.012 |  | 8/8 |
| MYM | 15 | eod * | -0.611 | -0.977 .. -0.245 | -10.1% | -0.953 | 0.0089 | 1 | 8/8 |
| MYM | 60 | h1 | -0.030 | -0.077 .. +0.017 | -5.7% | -0.067 | 0.33 |  | 6/8 |
| MYM | 60 | h2 * | -0.082 | -0.137 .. -0.027 | -10.8% | -0.110 | 0.0061 | 0.87 | 8/8 |
| MYM | 60 | h4 | -0.025 | -0.124 .. +0.074 | -2.3% | -0.066 | 0.63 |  | 4/8 |
| MYM | 60 | h8 | -0.082 | -0.232 .. +0.068 | -5.3% | -0.077 | 0.29 |  | 6/8 |
| MYM | 60 | h16 | -0.134 | -0.324 .. +0.057 | -6.3% | -0.069 | 0.19 |  | 4/8 |
| MYM | 60 | eod | -0.085 | -0.292 .. +0.123 | -3.8% | -0.099 | 0.44 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.31 pts | -1.00 .. +0.38 | 0.37 |
| MES | 15 | -0.72 pts | -2.21 .. +0.78 | 0.47 |
| MES | 60 | -1.00 pts | -4.60 .. +2.61 | 0.6 |
| MNQ | 5 | +0.04 pts | -0.72 .. +0.80 | 0.92 |
| MNQ | 15 | +0.09 pts | -1.43 .. +1.60 | 0.93 |
| MNQ | 60 | -0.69 pts | -4.02 .. +2.63 | 0.69 |
| MYM | 5 | +0.62 pts | -0.55 .. +1.79 | 0.32 |
| MYM | 15 | -1.00 pts | -3.38 .. +1.38 | 0.54 |
| MYM | 60 | +2.69 pts | -2.26 .. +7.63 | 0.3 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 28428 | +0.001 | 0.656 | -0.00 | -3.50 | -3.51 | -3.47 | -3.50 |
| MES | 5 | h2 | event | with signal | 28428 | -0.005 | 0.656 | -0.03 | -3.53 | -3.53 | -3.54 | -3.51 |
| MES | 5 | h4 | event | against signal | 28428 | +0.021 | 0.656 | +0.10 | -3.40 | -3.41 | -3.38 | -3.42 |
| MES | 5 | h8 | event | against signal | 28428 | +0.039 | 0.656 | +0.27 | -3.23 | -3.32 | -2.91 | -3.29 |
| MES | 5 | h16 | event | against signal | 28428 | +0.046 | 0.656 | +0.20 | -3.30 | -3.28 | -3.38 | -3.42 |
| MES | 5 | eod | event | against signal | 28428 | +1.226 | 0.656 | +4.38 | +0.88 | +0.63 | +1.79 | -1.06 |
| MES | 15 | h1 | event | with signal | 3880 | -0.006 | 0.241 | -0.03 | -3.53 | -3.55 | -3.47 | -3.49 |
| MES | 15 | h2 | event | with signal | 3880 | -0.008 | 0.241 | +0.35 | -3.15 | -3.51 | -2.45 | -3.10 |
| MES | 15 | h4 | event | against signal | 3880 | +0.047 | 0.241 | -0.01 | -3.51 | -3.11 | -4.29 | -3.60 |
| MES | 15 | h8 | event | against signal | 3880 | +0.102 | 0.241 | +0.77 | -2.73 | -2.95 | -2.29 | -2.81 |
| MES | 15 | h16 | event | against signal | 3880 | +0.095 | 0.241 | +0.40 | -3.10 | -2.87 | -3.54 | -3.06 |
| MES | 15 | eod | event | against signal | 3880 | +0.362 | 0.241 | +2.42 | -1.08 | -0.75 | -1.73 | -1.26 |
| MES | 60 | h1 | event | against signal | 675 | +0.007 | 0.094 | +0.04 | -3.46 | -3.06 | -3.92 | -3.55 |
| MES | 60 | h2 | event | against signal | 675 | +0.028 | 0.094 | +0.09 | -3.41 | -2.00 | -5.04 | -3.63 |
| MES | 60 | h4 | event | with signal | 675 | -0.002 | 0.094 | +0.17 | -3.33 | -5.43 | -0.92 | -2.70 |
| MES | 60 | h8 | event | with signal | 675 | -0.049 | 0.094 | -0.66 | -4.16 | -7.01 | -0.87 | -2.67 |
| MES | 60 | h16 | event | against signal | 675 | +0.152 | 0.094 | +1.43 | -2.07 | +3.28 | -8.23 | -5.45 |
| MES | 60 | eod | event | with signal | 675 | -0.102 | 0.094 | +1.56 | -1.94 | -8.95 | +6.13 | +2.42 |
| MNQ | 5 | h1 | event | with signal | 16269 | -0.004 | 0.236 | -0.07 | -2.07 | -2.01 | -2.25 | -2.05 |
| MNQ | 5 | h2 | event | against signal | 16269 | +0.018 | 0.236 | +0.21 | -1.79 | -1.99 | -1.19 | -1.79 |
| MNQ | 5 | h4 | event | against signal | 16269 | +0.028 | 0.236 | +0.26 | -1.74 | -1.96 | -1.10 | -1.72 |
| MNQ | 5 | h8 | event | against signal | 16269 | +0.046 | 0.236 | +0.45 | -1.55 | -1.93 | -0.45 | -1.53 |
| MNQ | 5 | h16 | event | against signal | 16269 | +0.089 | 0.236 | +0.62 | -1.38 | -1.80 | -0.18 | -1.44 |
| MNQ | 5 | eod | event | against signal | 16269 | +1.507 | 0.236 | +5.34 | +3.34 | +1.17 | +9.63 | +2.14 |
| MNQ | 15 | h1 | event | with signal | 3513 | -0.014 | 0.096 | +0.06 | -1.94 | -2.08 | -1.67 | -1.81 |
| MNQ | 15 | h2 | event | against signal | 3513 | +0.013 | 0.096 | +0.15 | -1.85 | -1.91 | -1.72 | -1.93 |
| MNQ | 15 | h4 | event | against signal | 3513 | +0.020 | 0.096 | -0.02 | -2.02 | -1.90 | -2.25 | -2.17 |
| MNQ | 15 | h8 | event | against signal | 3513 | +0.060 | 0.096 | +1.45 | -0.55 | -1.53 | +1.28 | -0.87 |
| MNQ | 15 | h16 | event | against signal | 3513 | +0.041 | 0.096 | +2.37 | +0.37 | -0.98 | +2.89 | +0.38 |
| MNQ | 15 | eod | event | against signal | 3513 | +0.786 | 0.096 | +9.18 | +7.18 | +3.01 | +14.99 | +7.73 |
| MNQ | 60 | h1 | event | against signal | 884 | +0.021 | 0.042 | +1.57 | -0.43 | -1.57 | +1.54 | -0.74 |
| MNQ | 60 | h2 | event | against signal | 884 | +0.063 | 0.042 | +2.01 | +0.01 | -0.09 | +0.20 | -0.55 |
| MNQ | 60 | h4 | event | against signal | 884 | +0.070 | 0.042 | +1.81 | -0.19 | +0.67 | -1.66 | -1.24 |
| MNQ | 60 | h8 | event | against signal | 884 | +0.072 | 0.042 | +1.49 | -0.51 | +1.00 | -3.12 | -2.24 |
| MNQ | 60 | h16 | event | with signal | 884 | -0.077 | 0.042 | +3.18 | +1.18 | -5.36 | +12.43 | +4.61 |
| MNQ | 60 | eod | event | with signal | 884 | -0.074 | 0.042 | +7.37 | +5.37 | -5.94 | +24.82 | +10.41 |
| MYM | 5 | h1 | event | with signal | 5500 | +0.010 | 0.186 | +0.01 | -1.99 | +nan | -1.99 | -2.01 |
| MYM | 5 | h2 | event | against signal | 5500 | -0.004 | 0.186 | +0.07 | -1.93 | +nan | -1.93 | -1.83 |
| MYM | 5 | h4 | event | against signal | 5500 | +0.001 | 0.186 | +0.08 | -1.92 | +nan | -1.92 | -1.63 |
| MYM | 5 | h8 | event | against signal | 5500 | -0.020 | 0.186 | +0.05 | -1.95 | +nan | -1.95 | -1.42 |
| MYM | 5 | h16 | event | against signal | 5500 | -0.004 | 0.186 | +0.05 | -1.95 | +nan | -1.95 | -1.30 |
| MYM | 5 | eod | event | against signal | 5500 | +0.908 | 0.186 | +3.28 | +1.28 | +nan | +1.28 | +3.13 |
| MYM | 15 | h1 | event | against signal | 1573 | +0.046 | 0.094 | +0.76 | -1.24 | +nan | -1.24 | -1.25 |
| MYM | 15 | h2 | event | against signal | 1573 | +0.062 | 0.094 | +0.75 | -1.25 | +nan | -1.25 | -1.08 |
| MYM | 15 | h4 | event | against signal | 1573 | +0.046 | 0.094 | +0.25 | -1.75 | +nan | -1.75 | -1.25 |
| MYM | 15 | h8 | event | against signal | 1573 | +0.035 | 0.094 | +0.07 | -1.93 | +nan | -1.93 | -0.76 |
| MYM | 15 | h16 | event | against signal | 1573 | +0.105 | 0.094 | +1.76 | -0.24 | +nan | -0.24 | +2.56 |
| MYM | 15 | eod | event | against signal | 1573 | +0.259 | 0.094 | +1.73 | -0.27 | +nan | -0.27 | +5.61 |
| MYM | 60 | h1 | event | with signal | 358 | +0.024 | 0.045 | +0.09 | -1.91 | +nan | -1.91 | -1.78 |
| MYM | 60 | h2 | event | with signal | 358 | +0.074 | 0.045 | +0.94 | -1.06 | +nan | -1.06 | -0.77 |
| MYM | 60 | h4 | event | with signal | 358 | +0.177 | 0.045 | +4.41 | +2.41 | +nan | +2.41 | +2.92 |
| MYM | 60 | h8 | event | with signal | 358 | +0.083 | 0.045 | +1.48 | -0.52 | +nan | -0.52 | +0.45 |
| MYM | 60 | h16 | event | with signal | 358 | +0.045 | 0.045 | -0.52 | -2.52 | +nan | -2.52 | -0.42 |
| MYM | 60 | eod | event | with signal | 358 | -0.002 | 0.045 | +0.88 | -1.12 | +nan | -1.12 | +2.08 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.104 | -0.107 | -0.121 | -0.128 | -0.097 | +0.000 | -0.099 | -0.102 | -0.113 | -0.118 | -0.096 |
| MES | 15 | +0.005 | +0.016 | -0.018 | -0.044 | -0.051 | +0.000 | -0.061 | -0.058 | -0.091 | -0.122 | -0.103 |
| MES | 60 | +0.251 | +0.246 | +0.085 | +0.057 | -0.008 | +0.000 | -0.011 | -0.025 | +0.027 | -0.009 | +0.053 |
| MNQ | 5 | +0.062 | +0.064 | +0.005 | -0.022 | -0.015 | +0.000 | -0.044 | -0.054 | -0.055 | -0.053 | -0.055 |
| MNQ | 15 | +0.092 | +0.117 | +0.068 | +0.013 | -0.009 | +0.000 | -0.028 | -0.021 | -0.016 | -0.039 | -0.018 |
| MNQ | 60 | +0.428 | +0.255 | +0.063 | +0.059 | -0.003 | +0.000 | -0.017 | -0.054 | -0.035 | -0.008 | -0.011 |
| MYM | 5 | +0.059 | +0.059 | +0.036 | +0.008 | -0.003 | +0.000 | -0.009 | -0.017 | -0.023 | -0.006 | -0.018 |
| MYM | 15 | +0.069 | +0.099 | +0.116 | +0.038 | +0.002 | +0.000 | -0.057 | -0.075 | -0.064 | -0.062 | -0.128 |
| MYM | 60 | -0.176 | +0.177 | +0.123 | +0.087 | +0.003 | +0.000 | +0.026 | +0.084 | +0.191 | +0.130 | +0.202 |

## Calibration

- MES 5-min: 1036271 bars, 28428 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 3880 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 675 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 16269 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 3513 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 884 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 5500 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1573 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 358 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 45482 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
