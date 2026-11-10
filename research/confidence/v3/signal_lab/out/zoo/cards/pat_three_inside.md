# Impact card: pat_three_inside

candle pattern three_inside in its textbook direction: harami (body2 inside body1) then bar3 closes beyond open1 in the reversal direction [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.074 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.070 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.66 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.222 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.393 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.130 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $10.54 at recent bar sizes, 90% range up to $3.50); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.084 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.304 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.84 at recent bar sizes, 90% range up to $19.31); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.033 R20 over the next 1 bar (5 min), p=0.13; we would catch an effect of 0.059 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.84 at recent bar sizes, 90% range up to $2.30); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.029 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.122 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.33 at recent bar sizes, 90% range up to $4.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.142 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.297 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $14.35 at recent bar sizes, 90% range up to $31.71); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.231 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.75 at recent bar sizes, 90% range up to $1.11); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.131 R20 over the next 4 bars (1 h), p=0.83; we would catch an effect of 0.162 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.58 at recent bar sizes, 90% range up to $6.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.090 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.416 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.90 at recent bar sizes, 90% range up to $33.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.012 | -0.035 .. +0.011 | -0.0010 | 0.32 / 0.33 / 0.37 | 0.362 |  |  | 8/16 | +0.007 | -0.030 |  | -1.0 / -1.0 |  |
| MES | 5 | h2 | -0.005 | -0.037 .. +0.027 | -0.0003 | 0.77 / 0.77 / 0.79 | 0.786 |  |  | 6/16 | +0.024 | -0.033 |  | -0.3 / -0.3 |  |
| MES | 5 | h4 | +0.020 | -0.026 .. +0.066 | +0.0008 | 0.4 / 0.41 / 0.44 | 0.416 |  |  | 9/16 | +0.044 | -0.005 |  | +0.8 / +0.8 | 0.070 |
| MES | 5 | h8 | +0.046 | -0.026 .. +0.117 | +0.0013 | 0.21 / 0.2 / 0.22 | 0.199 |  |  | 10/16 | +0.080 | +0.012 |  | +1.3 / +1.3 |  |
| MES | 5 | h16 * | +0.074 | -0.030 .. +0.178 | +0.0014 | 0.17 / 0.17 / 0.16 | 0.168 | 1 | 1 | 12/16 | +0.128 | +0.020 | False | +1.4 / +1.4 |  |
| MES | 5 | eod | -0.056 | -0.547 .. +0.435 | -0.0002 | 0.82 / 0.81 / 0.82 | 0.823 |  |  | 7/16 | -0.094 | -0.019 |  | -0.2 / -0.2 |  |
| MES | 15 | h1 | -0.005 | -0.047 .. +0.037 | -0.0004 | 0.81 / 0.81 / 0.83 | 0.823 |  |  | 9/16 | -0.020 | +0.009 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.010 | -0.072 .. +0.053 | -0.0005 | 0.76 / 0.76 / 0.79 | 0.777 |  |  | 10/16 | -0.026 | +0.007 |  | -0.3 / -0.3 |  |
| MES | 15 | h4 | -0.016 | -0.111 .. +0.079 | -0.0005 | 0.74 / 0.74 / 0.77 | 0.742 |  |  | 9/16 | -0.058 | +0.025 |  | -0.3 / -0.3 | 0.130 |
| MES | 15 | h8 | -0.012 | -0.146 .. +0.121 | -0.0003 | 0.86 / 0.86 / 0.88 | 0.864 |  |  | 9/16 | -0.052 | +0.027 |  | -0.2 / -0.2 |  |
| MES | 15 | h16 | -0.038 | -0.242 .. +0.167 | -0.0006 | 0.72 / 0.71 / 0.72 | 0.713 |  |  | 10/16 | -0.051 | -0.025 |  | -0.4 / -0.4 |  |
| MES | 15 | eod * | -0.393 | -0.819 .. +0.034 | -0.0026 | 0.071 / 0.072 / 0.14 | 0.147 | 1 | 1 | 11/16 | -0.302 | -0.483 | False | -1.6 / -1.8 |  |
| MES | 60 | h1 | +0.016 | -0.091 .. +0.123 | +0.0012 | 0.76 / 0.75 / 0.77 | 0.765 |  |  | 7/16 | +0.006 | +0.027 |  | +0.3 / +0.3 |  |
| MES | 60 | h2 * | +0.084 | -0.068 .. +0.235 | +0.0043 | 0.28 / 0.29 / 0.3 | 0.304 | 1 | 1 | 8/16 | +0.015 | +0.152 | False | +1.1 / +1.1 |  |
| MES | 60 | h4 | +0.115 | -0.090 .. +0.319 | +0.0041 | 0.27 / 0.28 / 0.31 | 0.306 |  |  | 11/16 | +0.124 | +0.105 |  | +1.1 / +1.1 | 0.304 |
| MES | 60 | h8 | +0.085 | -0.212 .. +0.382 | +0.0022 | 0.57 / 0.57 / 0.58 | 0.577 |  |  | 8/16 | +0.189 | -0.019 |  | +0.5 / +0.6 |  |
| MES | 60 | h16 | +0.113 | -0.231 .. +0.457 | +0.0023 | 0.52 / 0.51 / 0.52 | 0.527 |  |  | 9/16 | +0.236 | -0.009 |  | +0.6 / +0.6 |  |
| MES | 60 | eod | +0.147 | -0.197 .. +0.491 | +0.0028 | 0.4 / 0.4 / 0.42 | 0.413 |  |  | 9/16 | +0.274 | +0.020 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h1 * | -0.033 | -0.053 .. -0.012 | -0.0028 | 0.0016 / 0.0012 / 0.0062 | 0.0167 | 1 | 0.349 | 11/16 | -0.019 | -0.046 | False | -3.3 / -3.2 |  |
| MNQ | 5 | h2 | -0.028 | -0.060 .. +0.004 | -0.0015 | 0.083 / 0.078 / 0.16 | 0.0914 |  |  | 10/16 | -0.024 | -0.032 |  | -1.8 / -1.7 |  |
| MNQ | 5 | h4 | -0.038 | -0.082 .. +0.006 | -0.0013 | 0.089 / 0.087 / 0.2 | 0.127 |  |  | 12/16 | -0.032 | -0.044 |  | -1.7 / -1.7 | 0.059 |
| MNQ | 5 | h8 | -0.038 | -0.097 .. +0.021 | -0.0009 | 0.2 / 0.22 / 0.38 | 0.305 |  |  | 10/16 | -0.005 | -0.071 |  | -1.2 / -1.3 |  |
| MNQ | 5 | h16 | -0.054 | -0.145 .. +0.037 | -0.0009 | 0.24 / 0.25 / 0.37 | 0.338 |  |  | 9/16 | -0.010 | -0.097 |  | -1.1 / -1.2 |  |
| MNQ | 5 | eod | +0.084 | -0.426 .. +0.595 | +0.0003 | 0.75 / 0.74 / 0.77 | 0.762 |  |  | 7/16 | -0.010 | +0.177 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h1 * | +0.029 | -0.013 .. +0.071 | +0.0021 | 0.17 / 0.18 / 0.27 | 0.176 | 1 | 1 | 9/16 | -0.021 | +0.078 | False | +1.3 / +1.4 |  |
| MNQ | 15 | h2 | +0.019 | -0.041 .. +0.079 | +0.0008 | 0.53 / 0.53 / 0.65 | 0.548 |  |  | 9/16 | +0.000 | +0.038 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h4 | +0.021 | -0.070 .. +0.112 | +0.0005 | 0.64 / 0.63 / 0.77 | 0.647 |  |  | 5/16 | -0.014 | +0.057 |  | +0.5 / +0.5 | 0.122 |
| MNQ | 15 | h8 | +0.004 | -0.119 .. +0.127 | +0.0001 | 0.95 / 0.95 / 0.96 | 0.951 |  |  | 8/16 | -0.023 | +0.032 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h16 | +0.105 | -0.059 .. +0.270 | +0.0017 | 0.21 / 0.22 / 0.37 | 0.319 |  |  | 10/16 | +0.065 | +0.146 |  | +1.1 / +1.3 |  |
| MNQ | 15 | eod | -0.159 | -0.628 .. +0.310 | -0.0009 | 0.51 / 0.5 / 0.62 | 0.568 |  |  | 9/16 | -0.124 | -0.194 |  | -0.7 / -0.7 |  |
| MNQ | 60 | h1 | -0.009 | -0.101 .. +0.082 | -0.0007 | 0.84 / 0.85 / 0.87 | 0.858 |  |  | 10/16 | -0.054 | +0.036 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h2 | -0.017 | -0.152 .. +0.118 | -0.0009 | 0.81 / 0.82 / 0.83 | 0.831 |  |  | 8/16 | -0.182 | +0.148 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | -0.063 | -0.282 .. +0.157 | -0.0024 | 0.58 / 0.58 / 0.57 | 0.567 |  |  | 10/16 | -0.257 | +0.131 |  | -0.6 / -0.6 | 0.297 |
| MNQ | 60 | h8 | -0.076 | -0.359 .. +0.206 | -0.0022 | 0.6 / 0.59 / 0.6 | 0.591 |  |  | 8/16 | -0.388 | +0.235 |  | -0.5 / -0.5 |  |
| MNQ | 60 | h16 | -0.100 | -0.403 .. +0.202 | -0.0022 | 0.52 / 0.52 / 0.53 | 0.535 |  |  | 8/16 | -0.411 | +0.210 |  | -0.6 / -0.7 |  |
| MNQ | 60 | eod * | -0.142 | -0.455 .. +0.171 | -0.0029 | 0.37 / 0.38 / 0.38 | 0.383 | 1 | 1 | 9/16 | -0.382 | +0.098 | False | -0.9 / -0.9 |  |
| MYM | 5 | h1 | +0.013 | -0.012 .. +0.039 | +0.0011 | 0.31 / 0.32 / 0.44 | 0.334 |  |  | 5/8 | n/a | +0.013 |  | +1.0 / +1.0 |  |
| MYM | 5 | h2 | +0.005 | -0.032 .. +0.043 | +0.0003 | 0.78 / 0.78 / 0.84 | 0.756 |  |  | 6/8 | n/a | +0.005 |  | +0.3 / +0.3 |  |
| MYM | 5 | h4 | -0.044 | -0.102 .. +0.014 | -0.0014 | 0.14 / 0.13 / 0.37 | 0.209 |  |  | 5/8 | n/a | -0.044 |  | -1.5 / -1.5 | 0.078 |
| MYM | 5 | h8 | -0.012 | -0.092 .. +0.067 | -0.0003 | 0.76 / 0.76 / 0.87 | 0.827 |  |  | 3/8 | n/a | -0.012 |  | -0.3 / -0.3 |  |
| MYM | 5 | h16 | -0.014 | -0.136 .. +0.108 | -0.0002 | 0.82 / 0.82 / 0.87 | 0.852 |  |  | 5/8 | n/a | -0.014 |  | -0.2 / -0.2 |  |
| MYM | 5 | eod * | +0.231 | -0.357 .. +0.818 | +0.0009 | 0.44 / 0.46 / 0.52 | 0.517 | 1 | 1 | 6/8 | n/a | +0.231 | False | +0.7 / +0.8 |  |
| MYM | 15 | h1 | -0.042 | -0.101 .. +0.017 | -0.0032 | 0.16 / 0.18 / 0.24 | 0.158 |  |  | 5/8 | n/a | -0.042 |  | -1.3 / -1.4 |  |
| MYM | 15 | h2 | -0.061 | -0.148 .. +0.025 | -0.0026 | 0.17 / 0.18 / 0.32 | 0.163 |  |  | 5/8 | n/a | -0.061 |  | -1.4 / -1.4 |  |
| MYM | 15 | h4 * | -0.131 | -0.256 .. -0.006 | -0.0034 | 0.04 / 0.034 / 0.23 | 0.0759 | 1 | 0.998 | 6/8 | n/a | -0.131 | False | -2.0 / -2.1 | 0.162 |
| MYM | 15 | h8 | -0.162 | -0.318 .. -0.006 | -0.0032 | 0.042 / 0.044 / 0.22 | 0.107 |  |  | 6/8 | n/a | -0.162 |  | -1.9 / -2.0 |  |
| MYM | 15 | h16 | -0.121 | -0.353 .. +0.112 | -0.0017 | 0.31 / 0.31 / 0.52 | 0.396 |  |  | 6/8 | n/a | -0.121 |  | -1.0 / -1.0 |  |
| MYM | 15 | eod | +0.026 | -0.551 .. +0.602 | +0.0001 | 0.93 / 0.93 / 0.96 | 0.95 |  |  | 3/8 | n/a | +0.026 |  | +0.1 / +0.1 |  |
| MYM | 60 | h1 * | -0.090 | -0.234 .. +0.055 | -0.0072 | 0.22 / 0.21 / 0.25 | 0.249 | 1 | 1 | 5/8 | n/a | -0.090 | False | -1.3 / -1.2 |  |
| MYM | 60 | h2 | -0.116 | -0.323 .. +0.091 | -0.0065 | 0.27 / 0.24 / 0.29 | 0.302 |  |  | 7/8 | n/a | -0.116 |  | -1.2 / -1.1 |  |
| MYM | 60 | h4 | -0.068 | -0.355 .. +0.220 | -0.0027 | 0.64 / 0.65 / 0.66 | 0.648 |  |  | 5/8 | n/a | -0.068 |  | -0.5 / -0.5 | 0.416 |
| MYM | 60 | h8 | -0.005 | -0.362 .. +0.351 | -0.0001 | 0.98 / 0.98 / 0.98 | 0.979 |  |  | 4/8 | n/a | -0.005 |  | -0.0 / -0.0 |  |
| MYM | 60 | h16 | -0.094 | -0.492 .. +0.304 | -0.0021 | 0.64 / 0.63 / 0.69 | 0.683 |  |  | 4/8 | n/a | -0.094 |  | -0.5 / -0.5 |  |
| MYM | 60 | eod | -0.096 | -0.491 .. +0.299 | -0.0020 | 0.63 / 0.62 / 0.69 | 0.682 |  |  | 4/8 | n/a | -0.096 |  | -0.5 / -0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.004 | -0.012 .. +0.020 | +0.8% | +0.011 | 0.87 |  | 8/16 |
| MES | 5 | h2 * | -0.003 | -0.024 .. +0.017 | -0.5% | +0.007 | 0.75 | 1 | 8/16 |
| MES | 5 | h4 | +0.015 | -0.014 .. +0.044 | +1.5% | +0.029 | 0.77 |  | 8/16 |
| MES | 5 | h8 | +0.013 | -0.033 .. +0.059 | +0.9% | +0.028 | 1 |  | 9/16 |
| MES | 5 | h16 | +0.003 | -0.067 .. +0.072 | +0.1% | +0.031 | 0.94 |  | 6/16 |
| MES | 5 | eod | -0.032 | -0.381 .. +0.317 | -0.3% | -0.275 | 0.86 |  | 8/16 |
| MES | 15 | h1 | +0.007 | -0.022 .. +0.036 | +1.4% | +0.008 | 0.84 |  | 7/16 |
| MES | 15 | h2 | +0.005 | -0.039 .. +0.049 | +0.7% | +0.021 | 0.89 |  | 9/16 |
| MES | 15 | h4 | +0.031 | -0.024 .. +0.086 | +2.9% | +0.007 | 0.78 |  | 11/16 |
| MES | 15 | h8 | +0.005 | -0.079 .. +0.088 | +0.3% | +0.023 | 0.91 |  | 7/16 |
| MES | 15 | h16 * | +0.043 | -0.083 .. +0.168 | +1.9% | +0.026 | 0.64 | 1 | 9/16 |
| MES | 15 | eod | -0.018 | -0.341 .. +0.305 | -0.3% | -0.072 | 0.91 |  | 8/16 |
| MES | 60 | h1 | -0.007 | -0.067 .. +0.052 | -1.5% | +0.010 | 0.81 |  | 7/16 |
| MES | 60 | h2 * | -0.013 | -0.112 .. +0.086 | -1.8% | +0.010 | 0.8 | 1 | 7/16 |
| MES | 60 | h4 | -0.019 | -0.155 .. +0.117 | -1.8% | +0.018 | 0.98 |  | 8/16 |
| MES | 60 | h8 | -0.013 | -0.231 .. +0.204 | -0.9% | +0.004 | 0.9 |  | 8/16 |
| MES | 60 | h16 | -0.009 | -0.254 .. +0.235 | -0.4% | -0.030 | 0.94 |  | 8/16 |
| MES | 60 | eod | -0.015 | -0.261 .. +0.230 | -0.7% | -0.029 | 0.92 |  | 8/16 |
| MNQ | 5 | h1 | -0.005 | -0.019 .. +0.009 | -0.9% | +0.003 | 0.52 |  | 8/16 |
| MNQ | 5 | h2 * | +0.021 | -0.000 .. +0.043 | +2.8% | +0.024 | 0.37 | 1 | 11/16 |
| MNQ | 5 | h4 | +0.019 | -0.012 .. +0.050 | +1.7% | +0.015 | 0.53 |  | 10/16 |
| MNQ | 5 | h8 | +0.014 | -0.033 .. +0.061 | +0.9% | +0.013 | 0.61 |  | 7/16 |
| MNQ | 5 | h16 | +0.026 | -0.047 .. +0.099 | +1.1% | +0.017 | 0.55 |  | 12/16 |
| MNQ | 5 | eod | -0.264 | -0.677 .. +0.148 | -2.1% | -0.314 | 0.41 |  | 9/16 |
| MNQ | 15 | h1 | +0.004 | -0.027 .. +0.035 | +0.8% | +0.005 | 0.79 |  | 8/16 |
| MNQ | 15 | h2 | +0.011 | -0.032 .. +0.054 | +1.4% | +0.014 | 0.62 |  | 8/16 |
| MNQ | 15 | h4 * | +0.020 | -0.041 .. +0.082 | +1.8% | +0.033 | 0.51 | 1 | 11/16 |
| MNQ | 15 | h8 | +0.008 | -0.085 .. +0.101 | +0.5% | +0.033 | 0.86 |  | 8/16 |
| MNQ | 15 | h16 | -0.036 | -0.158 .. +0.086 | -1.4% | -0.008 | 0.75 |  | 7/16 |
| MNQ | 15 | eod | -0.149 | -0.557 .. +0.259 | -2.3% | -0.252 | 0.67 |  | 8/16 |
| MNQ | 60 | h1 | -0.022 | -0.089 .. +0.044 | -4.2% | +0.011 | 0.59 |  | 10/16 |
| MNQ | 60 | h2 * | -0.054 | -0.152 .. +0.044 | -7.1% | +0.006 | 0.35 | 1 | 9/16 |
| MNQ | 60 | h4 | -0.006 | -0.173 .. +0.160 | -0.6% | +0.030 | 0.94 |  | 8/16 |
| MNQ | 60 | h8 | -0.068 | -0.272 .. +0.137 | -4.3% | +0.041 | 0.53 |  | 11/16 |
| MNQ | 60 | h16 | -0.088 | -0.306 .. +0.129 | -4.0% | +0.003 | 0.49 |  | 11/16 |
| MNQ | 60 | eod | -0.069 | -0.297 .. +0.159 | -3.0% | +0.039 | 0.67 |  | 10/16 |
| MYM | 5 | h1 * | -0.008 | -0.026 .. +0.009 | -1.5% | -0.001 | 0.49 | 1 | 6/8 |
| MYM | 5 | h2 | -0.005 | -0.031 .. +0.021 | -0.7% | -0.007 | 0.72 |  | 4/8 |
| MYM | 5 | h4 | +0.016 | -0.024 .. +0.057 | +1.5% | -0.011 | 0.84 |  | 5/8 |
| MYM | 5 | h8 | +0.012 | -0.051 .. +0.075 | +0.8% | -0.025 | 0.99 |  | 4/8 |
| MYM | 5 | h16 | -0.009 | -0.101 .. +0.082 | -0.4% | -0.024 | 0.84 |  | 5/8 |
| MYM | 5 | eod | +0.041 | -0.464 .. +0.545 | +0.3% | -0.399 | 0.92 |  | 5/8 |
| MYM | 15 | h1 | +0.024 | -0.019 .. +0.067 | +4.5% | +0.028 | 0.72 |  | 6/8 |
| MYM | 15 | h2 | +0.025 | -0.036 .. +0.085 | +3.2% | +0.047 | 0.83 |  | 5/8 |
| MYM | 15 | h4 | +0.015 | -0.078 .. +0.108 | +1.3% | +0.034 | 0.92 |  | 6/8 |
| MYM | 15 | h8 | -0.024 | -0.135 .. +0.088 | -1.5% | -0.018 | 0.84 |  | 5/8 |
| MYM | 15 | h16 | -0.125 | -0.302 .. +0.052 | -5.1% | -0.105 | 0.58 |  | 6/8 |
| MYM | 15 | eod * | -0.265 | -0.702 .. +0.172 | -4.4% | -0.171 | 0.41 | 1 | 5/8 |
| MYM | 60 | h1 | -0.011 | -0.085 .. +0.062 | -2.2% | -0.023 | 0.84 |  | 5/8 |
| MYM | 60 | h2 | -0.062 | -0.187 .. +0.064 | -8.2% | +0.002 | 0.66 |  | 4/8 |
| MYM | 60 | h4 | +0.013 | -0.170 .. +0.197 | +1.2% | +0.120 | 0.89 |  | 4/8 |
| MYM | 60 | h8 | -0.009 | -0.271 .. +0.253 | -0.6% | +0.081 | 0.95 |  | 5/8 |
| MYM | 60 | h16 | -0.101 | -0.362 .. +0.160 | -4.8% | -0.007 | 0.55 |  | 5/8 |
| MYM | 60 | eod * | -0.129 | -0.394 .. +0.135 | -5.8% | -0.022 | 0.45 | 1 | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.42 pts | -1.20 .. +2.05 | 0.66 |
| MES | 15 | -0.01 pts | -2.55 .. +2.53 | 1 |
| MES | 60 | +1.02 pts | -4.66 .. +6.71 | 0.9 |
| MNQ | 5 | -0.39 pts | -1.64 .. +0.87 | 0.62 |
| MNQ | 15 | -1.21 pts | -3.33 .. +0.92 | 0.29 |
| MNQ | 60 | +2.50 pts | -2.10 .. +7.10 | 0.37 |
| MYM | 5 | +0.53 pts | -1.05 .. +2.12 | 0.52 |
| MYM | 15 | +0.09 pts | -2.63 .. +2.81 | 0.95 |
| MYM | 60 | -4.03 pts | -11.48 .. +3.41 | 0.29 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 3706 | +0.023 | 0.294 | +0.36 | -3.14 | -3.45 | -2.92 | -3.28 |
| MES | 5 | h2 | event | against signal | 3706 | +0.021 | 0.294 | +0.64 | -2.86 | -3.51 | -2.40 | -3.06 |
| MES | 5 | h4 | event | with signal | 3706 | +0.004 | 0.294 | -0.35 | -3.85 | -3.29 | -4.24 | -3.65 |
| MES | 5 | h8 | event | with signal | 3706 | +0.031 | 0.294 | -0.34 | -3.84 | -3.20 | -4.31 | -3.66 |
| MES | 5 | h16 | event | with signal | 3706 | +0.059 | 0.294 | +0.08 | -3.42 | -3.10 | -3.64 | -3.24 |
| MES | 5 | eod | event | against signal | 3706 | +0.061 | 0.294 | +2.37 | -1.13 | -1.65 | -0.76 | -0.95 |
| MES | 15 | h1 | event | against signal | 1234 | +0.014 | 0.191 | +0.05 | -3.45 | -3.11 | -3.76 | -3.60 |
| MES | 15 | h2 | event | against signal | 1234 | +0.020 | 0.191 | +0.43 | -3.07 | -3.02 | -3.12 | -3.26 |
| MES | 15 | h4 | event | against signal | 1234 | +0.026 | 0.191 | +1.37 | -2.13 | -2.59 | -1.71 | -2.31 |
| MES | 15 | h8 | event | against signal | 1234 | +0.026 | 0.191 | +1.34 | -2.16 | -2.75 | -1.60 | -2.39 |
| MES | 15 | h16 | event | against signal | 1234 | +0.060 | 0.191 | +1.49 | -2.01 | -3.32 | -0.77 | -2.44 |
| MES | 15 | eod | event | against signal | 1234 | +0.407 | 0.191 | +9.55 | +6.05 | -2.46 | +14.03 | +5.52 |
| MES | 60 | h1 | event | with signal | 265 | +0.015 | 0.092 | -0.39 | -3.89 | -2.80 | -5.06 | -3.85 |
| MES | 60 | h2 | event | with signal | 265 | +0.081 | 0.092 | +2.45 | -1.05 | -3.01 | +1.04 | -0.95 |
| MES | 60 | h4 | event | with signal | 265 | +0.109 | 0.092 | +2.98 | -0.52 | -1.06 | +0.05 | -0.25 |
| MES | 60 | h8 | event | with signal | 265 | +0.076 | 0.092 | -0.75 | -4.25 | -0.95 | -7.79 | -3.81 |
| MES | 60 | h16 | event | with signal | 265 | +0.112 | 0.092 | -0.97 | -4.47 | +0.48 | -9.76 | -4.03 |
| MES | 60 | eod | event | with signal | 265 | +0.146 | 0.092 | +0.01 | -3.49 | +1.27 | -8.59 | -3.01 |
| MNQ | 5 | h1 | event | against signal | 6135 | +0.038 | 0.116 | +1.00 | -1.00 | -1.89 | -0.38 | -1.08 |
| MNQ | 5 | h2 | event | against signal | 6135 | +0.037 | 0.116 | +0.80 | -1.20 | -1.91 | -0.71 | -1.34 |
| MNQ | 5 | h4 | event | against signal | 6135 | +0.044 | 0.116 | +0.86 | -1.14 | -1.85 | -0.64 | -1.24 |
| MNQ | 5 | h8 | event | against signal | 6135 | +0.038 | 0.116 | +1.01 | -0.99 | -2.02 | -0.27 | -0.99 |
| MNQ | 5 | h16 | event | against signal | 6135 | +0.053 | 0.116 | +0.74 | -1.26 | -1.91 | -0.80 | -1.23 |
| MNQ | 5 | eod | event | with signal | 6135 | +0.046 | 0.116 | +2.53 | +0.53 | -1.39 | +1.86 | +0.77 |
| MNQ | 15 | h1 | event | with signal | 1806 | +0.025 | 0.069 | +1.11 | -0.89 | -2.31 | +0.24 | -0.77 |
| MNQ | 15 | h2 | event | with signal | 1806 | +0.018 | 0.069 | +0.62 | -1.38 | -2.21 | -0.73 | -1.34 |
| MNQ | 15 | h4 | event | with signal | 1806 | +0.023 | 0.069 | -0.98 | -2.98 | -2.36 | -3.46 | -3.01 |
| MNQ | 15 | h8 | event | with signal | 1806 | +0.010 | 0.069 | -0.06 | -2.06 | -2.58 | -1.66 | -2.15 |
| MNQ | 15 | h16 | event | with signal | 1806 | +0.101 | 0.069 | +0.72 | -1.28 | -2.08 | -0.65 | -1.08 |
| MNQ | 15 | eod | event | against signal | 1806 | +0.168 | 0.069 | +2.26 | +0.26 | -1.21 | +1.41 | -0.40 |
| MNQ | 60 | h1 | event | against signal | 347 | +0.010 | 0.032 | -1.68 | -3.68 | -1.63 | -5.43 | -3.90 |
| MNQ | 60 | h2 | event | against signal | 347 | +0.023 | 0.032 | -3.42 | -5.42 | +0.55 | -10.53 | -5.89 |
| MNQ | 60 | h4 | event | against signal | 347 | +0.072 | 0.032 | -1.46 | -3.46 | +2.67 | -8.70 | -4.13 |
| MNQ | 60 | h8 | event | against signal | 347 | +0.087 | 0.032 | -10.33 | -12.33 | +3.01 | -25.46 | -13.25 |
| MNQ | 60 | h16 | event | against signal | 347 | +0.104 | 0.032 | -12.12 | -14.12 | +0.81 | -26.89 | -15.01 |
| MNQ | 60 | eod | event | against signal | 347 | +0.147 | 0.032 | -5.54 | -7.54 | +0.23 | -14.18 | -8.58 |
| MYM | 5 | h1 | event | with signal | 3443 | +0.005 | 0.168 | +0.08 | -1.92 | +nan | -1.92 | -1.82 |
| MYM | 5 | h2 | event | with signal | 3443 | -0.006 | 0.168 | -0.09 | -2.09 | +nan | -2.09 | -1.96 |
| MYM | 5 | h4 | event | against signal | 3443 | +0.059 | 0.168 | +0.58 | -1.42 | +nan | -1.42 | -1.59 |
| MYM | 5 | h8 | event | against signal | 3443 | +0.030 | 0.168 | +0.09 | -1.91 | +nan | -1.91 | -2.12 |
| MYM | 5 | h16 | event | against signal | 3443 | +0.040 | 0.168 | +0.17 | -1.83 | +nan | -1.83 | -2.13 |
| MYM | 5 | eod | event | with signal | 3443 | +0.157 | 0.168 | +1.16 | -0.84 | +nan | -0.84 | -0.05 |
| MYM | 15 | h1 | event | against signal | 924 | +0.048 | 0.101 | +0.75 | -1.25 | +nan | -1.25 | -1.37 |
| MYM | 15 | h2 | event | against signal | 924 | +0.070 | 0.101 | +0.69 | -1.31 | +nan | -1.31 | -1.49 |
| MYM | 15 | h4 | event | against signal | 924 | +0.133 | 0.101 | +1.94 | -0.06 | +nan | -0.06 | -0.10 |
| MYM | 15 | h8 | event | against signal | 924 | +0.170 | 0.101 | +3.83 | +1.83 | +nan | +1.83 | +1.68 |
| MYM | 15 | h16 | event | against signal | 924 | +0.135 | 0.101 | +2.64 | +0.64 | +nan | +0.64 | +0.38 |
| MYM | 15 | eod | event | with signal | 924 | -0.007 | 0.101 | -5.38 | -7.38 | +nan | -7.38 | -6.82 |
| MYM | 60 | h1 | event | against signal | 178 | +0.088 | 0.046 | +4.39 | +2.39 | +nan | +2.39 | +2.32 |
| MYM | 60 | h2 | event | against signal | 178 | +0.121 | 0.046 | +5.47 | +3.47 | +nan | +3.47 | +3.15 |
| MYM | 60 | h4 | event | against signal | 178 | +0.077 | 0.046 | -5.12 | -7.12 | +nan | -7.12 | -7.64 |
| MYM | 60 | h8 | event | against signal | 178 | +0.020 | 0.046 | -13.57 | -15.57 | +nan | -15.57 | -16.22 |
| MYM | 60 | h16 | event | against signal | 178 | +0.097 | 0.046 | -9.74 | -11.74 | +nan | -11.74 | -11.97 |
| MYM | 60 | eod | event | against signal | 178 | +0.095 | 0.046 | -9.07 | -11.07 | +nan | -11.07 | -11.18 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.246 | -0.251 | -0.441 | -1.293 | -0.900 | +0.000 | -0.041 | -0.040 | -0.015 | +0.012 | +0.049 |
| MES | 15 | -0.264 | -0.234 | -0.452 | -1.264 | -0.918 | +0.000 | -0.022 | -0.029 | -0.033 | -0.009 | -0.014 |
| MES | 60 | -0.552 | -0.387 | -0.509 | -1.232 | -0.936 | +0.000 | +0.012 | +0.070 | +0.116 | +0.033 | -0.314 |
| MNQ | 5 | -0.237 | -0.239 | -0.429 | -1.278 | -0.906 | +0.000 | -0.049 | -0.048 | -0.054 | -0.046 | -0.063 |
| MNQ | 15 | -0.292 | -0.291 | -0.449 | -1.263 | -0.925 | +0.000 | +0.024 | +0.018 | +0.019 | +0.013 | +0.107 |
| MNQ | 60 | -0.212 | -0.314 | -0.562 | -1.303 | -1.035 | +0.000 | -0.012 | -0.013 | -0.090 | -0.298 | -0.912 |
| MYM | 5 | -0.198 | -0.221 | -0.399 | -1.242 | -0.878 | +0.000 | +0.003 | -0.007 | -0.057 | -0.026 | -0.018 |
| MYM | 15 | -0.245 | -0.259 | -0.423 | -1.266 | -0.937 | +0.000 | -0.045 | -0.065 | -0.142 | -0.171 | -0.108 |
| MYM | 60 | -0.633 | -0.312 | -0.500 | -1.189 | -0.931 | +0.000 | -0.089 | -0.128 | -0.094 | +0.081 | -0.630 |

## Calibration

- MES 5-min: 1036271 bars, 3706 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1234 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 265 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 6135 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1806 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 347 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 3443 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 924 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 178 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 39444 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
