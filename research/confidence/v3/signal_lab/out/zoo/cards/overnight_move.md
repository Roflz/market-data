# Impact card: overnight_move

move from prior session close to the US cash open (09:30; 10:00 on 60-min bars), in ADR20; known from that bar on [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.008 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.75 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.131 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.123 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.086 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.27 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.083 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.030 R20 over the next 1 bar (1 h), p=0.93; we would catch an effect of 0.191 R20 or more 80% of the time).
- MES 60-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.061 R20, CONFIRMED, q=0.00788, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.89 at recent bar sizes, 90% range up to $4.93); about 2.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.272 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.047 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.74).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.10 at recent bar sizes, 90% range up to $1.40); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.022 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.090 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.12).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.79 at recent bar sizes, 90% range up to $4.98); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.026 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.193 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.01).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.28 at recent bar sizes, 90% range up to $8.91); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.008 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.064 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.22 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.099 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.016 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.131 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.26 at recent bar sizes, 90% range up to $4.07); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.022 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.278 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.078 R20, possible, q=0.0598, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.49 at recent bar sizes, 90% range up to $7.72); about 69.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.009 .. +0.007 | -0.0012 | 0.79 / 0.78 / 0.8 | 0.799 |  |  | 9/16 | +0.001 | -0.003 |  | -0.3 / -0.3 |  |
| MES | 5 | h2 | +0.001 | -0.015 .. +0.016 | -0.0010 | 0.95 / 0.94 / 0.95 | 0.951 |  |  | 7/16 | +0.002 | -0.001 |  | +0.1 / +0.1 |  |
| MES | 5 | h4 * | +0.008 | -0.023 .. +0.039 | +0.0005 | 0.61 / 0.6 / 0.63 | 0.625 | 1 | 1 | 10/16 | +0.011 | +0.005 | False | +1.0 / +0.5 | 0.045 |
| MES | 5 | h8 | +0.006 | -0.054 .. +0.066 | -0.0000 | 0.84 / 0.83 / 0.85 | 0.847 |  |  | 7/16 | +0.014 | -0.001 |  | +0.6 / +0.2 |  |
| MES | 5 | h16 | -0.014 | -0.128 .. +0.100 | -0.0007 | 0.81 / 0.8 / 0.81 | 0.817 |  |  | 8/16 | +0.003 | -0.031 |  | -0.9 / -0.2 |  |
| MES | 5 | eod | -0.126 | -0.515 .. +0.264 | +0.0031 | 0.53 / 0.51 / 0.52 | 0.525 |  |  | 10/16 | +0.020 | -0.268 |  | -4.9 / -0.6 |  |
| MES | 15 | h1 | +0.001 | -0.018 .. +0.021 | -0.0050 | 0.88 / 0.88 / 0.88 | 0.877 |  |  | 8/16 | +0.009 | -0.006 |  | +0.2 / +0.1 |  |
| MES | 15 | h2 | +0.011 | -0.022 .. +0.045 | -0.0029 | 0.51 / 0.51 / 0.52 | 0.519 |  |  | 8/16 | +0.017 | +0.005 |  | +0.8 / +0.7 |  |
| MES | 15 | h4 | +0.006 | -0.054 .. +0.066 | -0.0042 | 0.85 / 0.85 / 0.85 | 0.854 |  |  | 8/16 | +0.015 | -0.003 |  | +0.3 / +0.2 | 0.086 |
| MES | 15 | h8 | -0.017 | -0.125 .. +0.091 | -0.0064 | 0.76 / 0.75 / 0.76 | 0.769 |  |  | 9/16 | +0.014 | -0.047 |  | -0.7 / -0.3 |  |
| MES | 15 | h16 | -0.024 | -0.209 .. +0.160 | -0.0016 | 0.8 / 0.79 / 0.8 | 0.809 |  |  | 8/16 | +0.034 | -0.082 |  | -0.9 / -0.3 |  |
| MES | 15 | eod * | -0.123 | -0.391 .. +0.145 | +0.0011 | 0.37 / 0.35 / 0.36 | 0.369 | 1 | 1 | 10/16 | -0.052 | -0.191 | False | -3.7 / -0.9 |  |
| MES | 60 | h1 * | +0.030 | -0.011 .. +0.070 | +0.0077 | 0.15 / 0.14 / 0.16 | 0.171 | 1 | 1 | 9/16 | +0.046 | +0.013 | False | +1.5 / +1.4 |  |
| MES | 60 | h2 | +0.033 | -0.043 .. +0.110 | +0.0083 | 0.39 / 0.39 / 0.4 | 0.401 |  |  | 6/16 | +0.074 | -0.008 |  | +1.3 / +0.9 |  |
| MES | 60 | h4 | +0.033 | -0.106 .. +0.172 | +0.0108 | 0.65 / 0.64 / 0.64 | 0.634 |  |  | 6/16 | +0.124 | -0.059 |  | +0.9 / +0.5 | 0.191 |
| MES | 60 | h8 | +0.009 | -0.177 .. +0.196 | +0.0103 | 0.92 / 0.92 / 0.92 | 0.923 |  |  | 6/16 | +0.110 | -0.091 |  | +0.2 / +0.1 |  |
| MES | 60 | h16 | -0.005 | -0.192 .. +0.182 | +0.0103 | 0.96 / 0.96 / 0.95 | 0.952 |  |  | 10/16 | +0.096 | -0.106 |  | -0.1 / -0.1 |  |
| MES | 60 | eod | +0.001 | -0.185 .. +0.188 | +0.0103 | 0.99 / 0.99 / 0.99 | 0.991 |  |  | 6/16 | +0.102 | -0.099 |  | +0.0 / +0.0 |  |
| MNQ | 5 | h1 | +0.002 | -0.009 .. +0.012 | +0.0011 | 0.76 / 0.75 / 0.74 | 0.752 |  |  | 8/16 | +0.002 | +0.001 |  | +0.3 / +0.3 |  |
| MNQ | 5 | h2 | -0.002 | -0.019 .. +0.016 | -0.0004 | 0.86 / 0.86 / 0.86 | 0.866 |  |  | 9/16 | +0.005 | -0.008 |  | -0.3 / -0.2 |  |
| MNQ | 5 | h4 | +0.007 | -0.026 .. +0.040 | +0.0030 | 0.68 / 0.67 / 0.69 | 0.701 |  |  | 9/16 | +0.021 | -0.006 |  | +0.8 / +0.4 | 0.047 |
| MNQ | 5 | h8 | -0.002 | -0.065 .. +0.062 | +0.0024 | 0.96 / 0.96 / 0.96 | 0.967 |  |  | 9/16 | +0.028 | -0.030 |  | -0.1 / -0.0 |  |
| MNQ | 5 | h16 | -0.035 | -0.152 .. +0.083 | +0.0011 | 0.56 / 0.56 / 0.58 | 0.579 |  |  | 10/16 | +0.000 | -0.069 |  | -2.1 / -0.6 |  |
| MNQ | 5 | eod * | -0.272 | -0.656 .. +0.111 | +0.0042 | 0.16 / 0.15 / 0.17 | 0.172 | 1 | 1 | 11/16 | -0.212 | -0.331 | False | -10.0 / -1.4 |  |
| MNQ | 15 | h1 | +0.005 | -0.014 .. +0.024 | +0.0010 | 0.62 / 0.63 / 0.64 | 0.637 |  |  | 8/16 | +0.013 | -0.003 |  | +0.5 / +0.5 |  |
| MNQ | 15 | h2 * | +0.022 | -0.019 .. +0.063 | +0.0049 | 0.3 / 0.29 / 0.28 | 0.279 | 1 | 1 | 9/16 | +0.033 | +0.012 | False | +1.1 / +1.0 |  |
| MNQ | 15 | h4 | +0.007 | -0.057 .. +0.070 | +0.0021 | 0.84 / 0.84 / 0.84 | 0.844 |  |  | 7/16 | +0.040 | -0.026 |  | +0.3 / +0.2 | 0.090 |
| MNQ | 15 | h8 | -0.032 | -0.159 .. +0.095 | -0.0024 | 0.62 / 0.63 / 0.61 | 0.61 |  |  | 10/16 | +0.034 | -0.096 |  | -0.9 / -0.5 |  |
| MNQ | 15 | h16 | -0.033 | -0.216 .. +0.149 | +0.0027 | 0.72 / 0.72 / 0.74 | 0.738 |  |  | 9/16 | +0.026 | -0.090 |  | -1.2 / -0.4 |  |
| MNQ | 15 | eod | -0.128 | -0.427 .. +0.171 | +0.0087 | 0.4 / 0.38 / 0.37 | 0.37 |  |  | 11/16 | -0.124 | -0.131 |  | -2.5 / -0.8 |  |
| MNQ | 60 | h1 * | +0.026 | -0.018 .. +0.070 | +0.0109 | 0.24 / 0.22 / 0.25 | 0.247 | 1 | 1 | 8/16 | +0.036 | +0.016 | False | +1.3 / +1.2 |  |
| MNQ | 60 | h2 | +0.029 | -0.051 .. +0.109 | +0.0127 | 0.47 / 0.45 / 0.48 | 0.465 |  |  | 8/16 | +0.044 | +0.015 |  | +1.0 / +0.7 |  |
| MNQ | 60 | h4 | +0.012 | -0.126 .. +0.151 | +0.0148 | 0.86 / 0.86 / 0.86 | 0.857 |  |  | 7/16 | +0.062 | -0.038 |  | +0.3 / +0.2 | 0.193 |
| MNQ | 60 | h8 | -0.027 | -0.211 .. +0.157 | +0.0144 | 0.77 / 0.76 / 0.77 | 0.773 |  |  | 10/16 | +0.032 | -0.085 |  | -0.7 / -0.3 |  |
| MNQ | 60 | h16 | -0.042 | -0.226 .. +0.142 | +0.0144 | 0.65 / 0.64 / 0.65 | 0.651 |  |  | 10/16 | +0.018 | -0.102 |  | -1.0 / -0.4 |  |
| MNQ | 60 | eod | -0.047 | -0.231 .. +0.136 | +0.0144 | 0.61 / 0.59 / 0.61 | 0.611 |  |  | 10/16 | +0.012 | -0.107 |  | -1.2 / -0.5 |  |
| MYM | 5 | h1 * | +0.008 | -0.012 .. +0.027 | +0.0025 | 0.46 / 0.48 / 0.37 | 0.376 | 1 | 1 | 6/8 | n/a | +0.008 | False | +0.7 / +0.7 |  |
| MYM | 5 | h2 | +0.003 | -0.017 .. +0.023 | -0.0008 | 0.78 / 0.8 / 0.82 | 0.819 |  |  | 6/8 | n/a | +0.003 |  | +0.3 / +0.3 |  |
| MYM | 5 | h4 | +0.008 | -0.032 .. +0.047 | +0.0001 | 0.7 / 0.72 / 0.74 | 0.74 |  |  | 6/8 | n/a | +0.008 |  | +0.6 / +0.4 | 0.064 |
| MYM | 5 | h8 | -0.010 | -0.084 .. +0.063 | -0.0041 | 0.78 / 0.79 / 0.82 | 0.806 |  |  | 5/8 | n/a | -0.010 |  | -0.7 / -0.3 |  |
| MYM | 5 | h16 | -0.039 | -0.183 .. +0.105 | -0.0059 | 0.6 / 0.61 / 0.64 | 0.632 |  |  | 5/8 | n/a | -0.039 |  | -1.8 / -0.5 |  |
| MYM | 5 | eod | -0.162 | -0.688 .. +0.365 | -0.0072 | 0.55 / 0.54 / 0.56 | 0.544 |  |  | 6/8 | n/a | -0.162 |  | -4.2 / -0.6 |  |
| MYM | 15 | h1 * | +0.016 | -0.019 .. +0.052 | +0.0036 | 0.37 / 0.39 / 0.28 | 0.292 | 1 | 1 | 6/8 | n/a | +0.016 | False | +0.9 / +0.9 |  |
| MYM | 15 | h2 | +0.025 | -0.056 .. +0.105 | +0.0036 | 0.55 / 0.58 / 0.46 | 0.472 |  |  | 3/8 | n/a | +0.025 |  | +0.7 / +0.6 |  |
| MYM | 15 | h4 | -0.019 | -0.097 .. +0.059 | -0.0049 | 0.64 / 0.65 / 0.64 | 0.648 |  |  | 5/8 | n/a | -0.019 |  | -0.5 / -0.5 | 0.131 |
| MYM | 15 | h8 | -0.099 | -0.242 .. +0.044 | -0.0181 | 0.17 / 0.18 / 0.21 | 0.212 |  |  | 7/8 | n/a | -0.099 |  | -2.9 / -1.4 |  |
| MYM | 15 | h16 | -0.110 | -0.359 .. +0.140 | -0.0138 | 0.39 / 0.39 / 0.39 | 0.388 |  |  | 6/8 | n/a | -0.110 |  | -2.8 / -0.9 |  |
| MYM | 15 | eod | -0.115 | -0.546 .. +0.316 | -0.0011 | 0.6 / 0.59 / 0.57 | 0.552 |  |  | 6/8 | n/a | -0.115 |  | -1.5 / -0.5 |  |
| MYM | 60 | h1 | -0.002 | -0.056 .. +0.052 | -0.0028 | 0.94 / 0.94 / 0.94 | 0.953 |  |  | 5/8 | n/a | -0.002 |  | -0.1 / -0.1 |  |
| MYM | 60 | h2 | -0.015 | -0.117 .. +0.088 | -0.0041 | 0.78 / 0.78 / 0.8 | 0.799 |  |  | 6/8 | n/a | -0.015 |  | -0.4 / -0.3 |  |
| MYM | 60 | h4 | -0.018 | -0.200 .. +0.165 | -0.0035 | 0.85 / 0.85 / 0.86 | 0.861 |  |  | 5/8 | n/a | -0.018 |  | -0.4 / -0.2 | 0.278 |
| MYM | 60 | h8 * | +0.022 | -0.222 .. +0.265 | +0.0005 | 0.86 / 0.86 / 0.87 | 0.871 | 1 | 1 | 4/8 | n/a | +0.022 | False | +0.4 / +0.2 |  |
| MYM | 60 | h16 | -0.008 | -0.254 .. +0.238 | +0.0005 | 0.95 / 0.94 / 0.95 | 0.945 |  |  | 5/8 | n/a | -0.008 |  | -0.2 / -0.1 |  |
| MYM | 60 | eod | -0.003 | -0.249 .. +0.244 | +0.0005 | 0.98 / 0.98 / 0.98 | 0.981 |  |  | 4/8 | n/a | -0.003 |  | -0.1 / -0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.008 .. +0.007 | -0.1% | +0.014 | 0.94 |  | 8/16 |
| MES | 5 | h2 | -0.003 | -0.014 .. +0.008 | -0.4% | +0.011 | 0.65 |  | 9/16 |
| MES | 5 | h4 | +0.001 | -0.016 .. +0.018 | +0.1% | +0.012 | 0.93 |  | 7/16 |
| MES | 5 | h8 | +0.015 | -0.016 .. +0.046 | +1.1% | +0.030 | 0.72 |  | 8/16 |
| MES | 5 | h16 * | +0.040 | -0.021 .. +0.101 | +2.1% | +0.063 | 0.42 | 1 | 9/16 |
| MES | 5 | eod | +0.115 | -0.160 .. +0.391 | +3.7% | +0.272 | 0.95 |  | 6/16 |
| MES | 15 | h1 * | +0.008 | -0.007 .. +0.023 | +1.4% | +0.009 | 0.46 | 1 | 11/16 |
| MES | 15 | h2 | +0.009 | -0.023 .. +0.041 | +1.1% | -0.002 | 0.8 |  | 11/16 |
| MES | 15 | h4 | +0.020 | -0.029 .. +0.069 | +1.8% | +0.018 | 0.57 |  | 11/16 |
| MES | 15 | h8 | +0.030 | -0.037 .. +0.097 | +2.0% | +0.043 | 0.55 |  | 11/16 |
| MES | 15 | h16 | +0.041 | -0.062 .. +0.143 | +2.2% | +0.088 | 0.65 |  | 7/16 |
| MES | 15 | eod | +0.020 | -0.148 .. +0.188 | +1.0% | +0.010 | 0.85 |  | 6/16 |
| MES | 60 | h1 * | -0.061 | -0.090 .. -0.033 | -8.3% | -0.132 | 3.6e-05 | 0.00788 | 13/16 |
| MES | 60 | h2 | -0.082 | -0.128 .. -0.036 | -8.2% | -0.157 | 0.00094 |  | 11/16 |
| MES | 60 | h4 | -0.118 | -0.193 .. -0.043 | -9.3% | -0.199 | 0.0035 |  | 13/16 |
| MES | 60 | h8 | -0.126 | -0.226 .. -0.027 | -9.0% | -0.227 | 0.018 |  | 13/16 |
| MES | 60 | h16 | -0.107 | -0.208 .. -0.005 | -7.6% | -0.222 | 0.048 |  | 13/16 |
| MES | 60 | eod | -0.099 | -0.201 .. +0.004 | -7.0% | -0.217 | 0.069 |  | 11/16 |
| MNQ | 5 | h1 | -0.003 | -0.013 .. +0.007 | -0.6% | +0.015 | 0.51 |  | 8/16 |
| MNQ | 5 | h2 | +0.002 | -0.009 .. +0.012 | +0.2% | +0.018 | 0.84 |  | 7/16 |
| MNQ | 5 | h4 | +0.007 | -0.011 .. +0.026 | +0.7% | +0.028 | 0.42 |  | 7/16 |
| MNQ | 5 | h8 | +0.017 | -0.017 .. +0.051 | +1.2% | +0.052 | 0.34 |  | 6/16 |
| MNQ | 5 | h16 * | +0.054 | -0.013 .. +0.121 | +2.8% | +0.094 | 0.12 | 1 | 8/16 |
| MNQ | 5 | eod | +0.216 | -0.031 .. +0.463 | +6.9% | +0.234 | 0.13 |  | 9/16 |
| MNQ | 15 | h1 | +0.011 | -0.004 .. +0.026 | +1.9% | +0.013 | 0.13 |  | 9/16 |
| MNQ | 15 | h2 | +0.012 | -0.029 .. +0.053 | +1.4% | -0.002 | 0.57 |  | 11/16 |
| MNQ | 15 | h4 | +0.023 | -0.047 .. +0.092 | +2.0% | +0.018 | 0.52 |  | 12/16 |
| MNQ | 15 | h8 | +0.057 | -0.039 .. +0.153 | +3.8% | +0.055 | 0.25 |  | 11/16 |
| MNQ | 15 | h16 * | +0.129 | +0.026 .. +0.233 | +6.8% | +0.137 | 0.02 | 1 | 10/16 |
| MNQ | 15 | eod | +0.112 | -0.068 .. +0.292 | +5.2% | +0.090 | 0.26 |  | 9/16 |
| MNQ | 60 | h1 * | -0.048 | -0.076 .. -0.019 | -6.1% | -0.108 | 0.0017 | 0.278 | 13/16 |
| MNQ | 60 | h2 | -0.058 | -0.103 .. -0.013 | -5.6% | -0.125 | 0.021 |  | 12/16 |
| MNQ | 60 | h4 | -0.076 | -0.145 .. -0.007 | -5.8% | -0.149 | 0.088 |  | 12/16 |
| MNQ | 60 | h8 | -0.086 | -0.179 .. +0.008 | -5.9% | -0.186 | 0.17 |  | 12/16 |
| MNQ | 60 | h16 | -0.097 | -0.191 .. -0.003 | -6.7% | -0.210 | 0.087 |  | 12/16 |
| MNQ | 60 | eod | -0.101 | -0.195 .. -0.007 | -6.9% | -0.209 | 0.066 |  | 12/16 |
| MYM | 5 | h1 | -0.002 | -0.023 .. +0.020 | -0.3% | +0.004 | 0.89 |  | 2/8 |
| MYM | 5 | h2 | +0.008 | -0.006 .. +0.022 | +1.1% | +0.010 | 0.57 |  | 5/8 |
| MYM | 5 | h4 | +0.001 | -0.029 .. +0.031 | +0.1% | +0.018 | 0.96 |  | 4/8 |
| MYM | 5 | h8 | +0.008 | -0.039 .. +0.056 | +0.6% | +0.034 | 0.92 |  | 4/8 |
| MYM | 5 | h16 * | +0.057 | -0.034 .. +0.148 | +3.0% | +0.068 | 0.36 | 1 | 6/8 |
| MYM | 5 | eod | +0.273 | -0.108 .. +0.654 | +8.7% | +0.544 | 0.85 |  | 5/8 |
| MYM | 15 | h1 | -0.006 | -0.047 .. +0.035 | -1.0% | -0.018 | 0.77 |  | 2/8 |
| MYM | 15 | h2 * | -0.027 | -0.117 .. +0.062 | -3.3% | -0.070 | 0.55 | 1 | 3/8 |
| MYM | 15 | h4 | -0.020 | -0.123 .. +0.084 | -1.8% | -0.068 | 0.71 |  | 2/8 |
| MYM | 15 | h8 | +0.023 | -0.077 .. +0.122 | +1.5% | -0.068 | 0.66 |  | 6/8 |
| MYM | 15 | h16 | +0.000 | -0.141 .. +0.142 | +0.0% | -0.073 | 1 |  | 5/8 |
| MYM | 15 | eod | -0.060 | -0.324 .. +0.203 | -2.9% | -0.159 | 0.67 |  | 4/8 |
| MYM | 60 | h1 * | -0.078 | -0.120 .. -0.036 | -10.3% | -0.118 | 0.00032 | 0.0598 | 7/8 |
| MYM | 60 | h2 | -0.090 | -0.154 .. -0.027 | -8.9% | -0.161 | 0.018 |  | 7/8 |
| MYM | 60 | h4 | -0.148 | -0.247 .. -0.050 | -11.6% | -0.222 | 0.018 |  | 7/8 |
| MYM | 60 | h8 | -0.139 | -0.269 .. -0.008 | -9.8% | -0.242 | 0.071 |  | 5/8 |
| MYM | 60 | h16 | -0.135 | -0.267 .. -0.002 | -9.5% | -0.237 | 0.058 |  | 5/8 |
| MYM | 60 | eod | -0.131 | -0.264 .. +0.002 | -9.3% | -0.232 | 0.064 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.72 pts | -0.40 .. +1.84 | 0.22 |
| MES | 15 | -0.10 pts | -1.82 .. +1.62 | 0.95 |
| MES | 60 | +1.07 pts | -1.25 .. +3.39 | 0.4 |
| MNQ | 5 | +1.21 pts | +0.08 .. +2.34 | 0.037 |
| MNQ | 15 | -0.16 pts | -1.94 .. +1.62 | 0.9 |
| MNQ | 60 | +1.09 pts | -1.21 .. +3.40 | 0.35 |
| MYM | 5 | -0.51 pts | -1.86 .. +0.85 | 0.87 |
| MYM | 15 | -2.33 pts | -4.36 .. -0.30 | 0.13 |
| MYM | 60 | -2.21 pts | -4.95 .. +0.54 | 0.16 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 63356 | +0.002 | 0.171 | +0.08 | -3.42 | -3.50 | -3.35 | -3.42 |
| MES | 5 | h2 | top fifth | long | 63278 | +0.007 | 0.216 | +0.03 | -3.47 | -3.44 | -3.49 | -3.50 |
| MES | 5 | h4 | top fifth | long | 63278 | +0.018 | 0.216 | +0.15 | -3.35 | -3.33 | -3.37 | -3.45 |
| MES | 5 | h8 | top fifth | long | 63278 | +0.035 | 0.216 | +0.26 | -3.24 | -3.14 | -3.34 | -3.49 |
| MES | 5 | h16 | bottom fifth | long | 63356 | +0.060 | 0.171 | +0.77 | -2.73 | -3.69 | -1.86 | -3.37 |
| MES | 5 | eod | bottom fifth | long | 63356 | +0.169 | 0.171 | +2.64 | -0.86 | -4.53 | +2.51 | +3.39 |
| MES | 15 | h1 | top fifth | long | 21122 | +0.011 | 0.137 | +0.08 | -3.42 | -3.37 | -3.48 | -3.56 |
| MES | 15 | h2 | top fifth | long | 21122 | +0.022 | 0.137 | +0.23 | -3.27 | -3.18 | -3.34 | -3.53 |
| MES | 15 | h4 | top fifth | long | 21122 | +0.037 | 0.137 | +0.33 | -3.17 | -2.94 | -3.37 | -3.68 |
| MES | 15 | h8 | bottom fifth | long | 21143 | +0.059 | 0.107 | +1.12 | -2.38 | -3.77 | -1.11 | -3.10 |
| MES | 15 | h16 | bottom fifth | long | 21143 | +0.071 | 0.107 | +1.92 | -1.58 | -4.14 | +0.77 | -2.01 |
| MES | 15 | eod | bottom fifth | long | 21143 | +0.088 | 0.107 | +2.67 | -0.83 | -4.51 | +2.55 | +3.77 |
| MES | 60 | h1 | top fifth | long | 5223 | +0.035 | 0.095 | +0.95 | -2.55 | -2.39 | -2.70 | -2.90 |
| MES | 60 | h2 | top fifth | long | 5223 | +0.059 | 0.095 | +1.60 | -1.90 | -1.42 | -2.36 | -2.82 |
| MES | 60 | h4 | top fifth | long | 5223 | +0.087 | 0.095 | +2.07 | -1.43 | +0.03 | -2.84 | -2.88 |
| MES | 60 | h8 | top fifth | long | 5223 | +0.104 | 0.095 | +2.95 | -0.55 | +0.88 | -1.94 | -2.25 |
| MES | 60 | h16 | bottom fifth | long | 5225 | +0.085 | 0.081 | +3.13 | -0.37 | -3.50 | +2.82 | -0.92 |
| MES | 60 | eod | top fifth | long | 5223 | +0.104 | 0.095 | +2.95 | -0.55 | +0.88 | -1.94 | -1.54 |
| MNQ | 5 | h1 | top fifth | long | 63230 | +0.005 | 0.080 | -0.05 | -2.05 | -1.96 | -2.14 | -2.07 |
| MNQ | 5 | h2 | bottom fifth | long | 63310 | +0.012 | 0.065 | +0.23 | -1.77 | -1.96 | -1.60 | -1.79 |
| MNQ | 5 | h4 | top fifth | long | 63230 | +0.024 | 0.080 | -0.07 | -2.07 | -1.80 | -2.31 | -2.14 |
| MNQ | 5 | h8 | bottom fifth | long | 63310 | +0.039 | 0.065 | +0.79 | -1.21 | -2.03 | -0.51 | -1.31 |
| MNQ | 5 | h16 | bottom fifth | long | 63310 | +0.089 | 0.065 | +1.48 | -0.52 | -1.95 | +0.71 | -0.85 |
| MNQ | 5 | eod | bottom fifth | long | 63310 | +0.289 | 0.065 | +5.71 | +3.71 | -1.31 | +8.04 | +18.59 |
| MNQ | 15 | h1 | top fifth | long | 21087 | +0.013 | 0.051 | -0.12 | -2.12 | -1.85 | -2.38 | -2.32 |
| MNQ | 15 | h2 | top fifth | long | 21087 | +0.025 | 0.051 | -0.16 | -2.16 | -1.67 | -2.60 | -2.40 |
| MNQ | 15 | h4 | top fifth | long | 21087 | +0.042 | 0.051 | -0.38 | -2.38 | -1.50 | -3.18 | -2.97 |
| MNQ | 15 | h8 | bottom fifth | long | 21117 | +0.095 | 0.040 | +2.24 | +0.24 | -1.84 | +2.04 | -0.91 |
| MNQ | 15 | h16 | bottom fifth | long | 21117 | +0.108 | 0.040 | +3.97 | +1.97 | -1.71 | +5.12 | +1.92 |
| MNQ | 15 | eod | bottom fifth | long | 21117 | +0.128 | 0.040 | +5.95 | +3.95 | -1.23 | +8.40 | +16.14 |
| MNQ | 60 | h1 | top fifth | long | 5223 | +0.037 | 0.037 | +1.78 | -0.22 | -1.01 | +0.54 | -0.79 |
| MNQ | 60 | h2 | top fifth | long | 5223 | +0.067 | 0.037 | +3.77 | +1.77 | -0.34 | +3.77 | +0.33 |
| MNQ | 60 | h4 | top fifth | long | 5223 | +0.088 | 0.037 | +4.95 | +2.95 | +0.52 | +5.24 | +0.66 |
| MNQ | 60 | h8 | bottom fifth | long | 5229 | +0.108 | 0.030 | +3.32 | +1.32 | -1.00 | +3.39 | -0.68 |
| MNQ | 60 | h16 | bottom fifth | long | 5229 | +0.108 | 0.030 | +3.32 | +1.32 | -1.00 | +3.39 | +1.96 |
| MNQ | 60 | eod | bottom fifth | long | 5229 | +0.108 | 0.030 | +3.32 | +1.32 | -1.00 | +3.39 | +2.63 |
| MYM | 5 | h1 | top fifth | long | 31695 | +0.006 | 0.111 | +0.02 | -1.98 | +nan | -1.98 | -1.98 |
| MYM | 5 | h2 | top fifth | long | 31695 | +0.013 | 0.111 | +0.07 | -1.93 | +nan | -1.93 | -1.99 |
| MYM | 5 | h4 | top fifth | long | 31695 | +0.024 | 0.111 | +0.16 | -1.84 | +nan | -1.84 | -1.96 |
| MYM | 5 | h8 | bottom fifth | long | 31778 | +0.051 | 0.089 | +1.29 | -0.71 | +nan | -0.71 | -1.11 |
| MYM | 5 | h16 | bottom fifth | long | 31778 | +0.112 | 0.089 | +2.60 | +0.60 | +nan | +0.60 | -0.28 |
| MYM | 5 | eod | bottom fifth | long | 31778 | +0.325 | 0.089 | +7.77 | +5.77 | +nan | +5.77 | +5.20 |
| MYM | 15 | h1 | top fifth | long | 10575 | +0.013 | 0.069 | +0.09 | -1.91 | +nan | -1.91 | -2.02 |
| MYM | 15 | h2 | top fifth | long | 10575 | +0.021 | 0.069 | +0.22 | -1.78 | +nan | -1.78 | -1.96 |
| MYM | 15 | h4 | bottom fifth | long | 10607 | +0.038 | 0.055 | +1.92 | -0.08 | +nan | -0.08 | -0.28 |
| MYM | 15 | h8 | bottom fifth | long | 10607 | +0.127 | 0.055 | +3.80 | +1.80 | +nan | +1.80 | +1.45 |
| MYM | 15 | h16 | bottom fifth | long | 10607 | +0.151 | 0.055 | +6.44 | +4.44 | +nan | +4.44 | +4.57 |
| MYM | 15 | eod | bottom fifth | long | 10607 | +0.136 | 0.055 | +7.93 | +5.93 | +nan | +5.93 | +8.26 |
| MYM | 60 | h1 | bottom fifth | long | 2596 | +0.001 | 0.041 | +0.52 | -1.48 | +nan | -1.48 | -1.64 |
| MYM | 60 | h2 | bottom fifth | long | 2596 | +0.020 | 0.041 | +1.23 | -0.77 | +nan | -0.77 | -1.37 |
| MYM | 60 | h4 | bottom fifth | long | 2596 | +0.039 | 0.041 | +1.84 | -0.16 | +nan | -0.16 | -1.30 |
| MYM | 60 | h8 | top fifth | long | 2591 | +0.087 | 0.046 | +4.37 | +2.37 | +nan | +2.37 | +0.47 |
| MYM | 60 | h16 | bottom fifth | long | 2596 | +0.036 | 0.041 | +1.82 | -0.18 | +nan | -0.18 | -1.98 |
| MYM | 60 | eod | bottom fifth | long | 2596 | +0.036 | 0.041 | +1.82 | -0.18 | +nan | -0.18 | -2.49 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.330 | +0.251 | +0.118 | +0.046 | +0.017 | +0.000 | +0.003 | +0.004 | +0.007 | -0.008 | -0.033 |
| MES | 15 | +0.646 | +0.609 | +0.350 | +0.157 | +0.058 | +0.000 | +0.009 | +0.014 | +0.004 | -0.002 | +0.006 |
| MES | 60 | -2.707 | -1.720 | -0.574 | -0.256 | -0.104 | +0.000 | +0.025 | +0.026 | +0.070 | +nan | +nan |
| MNQ | 5 | +0.299 | +0.251 | +0.129 | +0.054 | +0.020 | +0.000 | +0.005 | +0.003 | +0.009 | -0.004 | -0.033 |
| MNQ | 15 | +0.565 | +0.611 | +0.382 | +0.178 | +0.069 | +0.000 | +0.027 | +0.046 | +0.039 | +0.009 | +0.033 |
| MNQ | 60 | -2.951 | -2.028 | -0.765 | -0.372 | -0.182 | +0.000 | +0.019 | +0.024 | +0.070 | +nan | +nan |
| MYM | 5 | +0.368 | +0.274 | +0.129 | +0.050 | +0.016 | +0.000 | +0.010 | +0.008 | +0.009 | -0.020 | -0.067 |
| MYM | 15 | +0.744 | +0.679 | +0.386 | +0.170 | +0.059 | +0.000 | +0.045 | +0.069 | +0.029 | -0.043 | -0.034 |
| MYM | 60 | -2.871 | -1.999 | -0.674 | -0.291 | -0.119 | +0.000 | +0.010 | -0.010 | -0.003 | +nan | +nan |

## Calibration

- MES 5-min: 316481 bars, 63278 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 105630 bars, 21122 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 26118 bars, 5223 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 316364 bars, 63230 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 105512 bars, 21087 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 26117 bars, 5223 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 158784 bars, 31695 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 52977 bars, 10575 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 12963 bars, 2591 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
