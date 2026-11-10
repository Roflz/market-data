# Impact card: pat_morning_evening_star

candle pattern morning_evening_star in its textbook direction: TA-Lib style 3 bars: long body 1, small body 2 gapping beyond body 1, long body 3 closing beyond 30% into body 1; morning (bullish) after close1 < EMA10, evening mirror [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.027 R20 over the next 1 bar (5 min), p=0.43; we would catch an effect of 0.080 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.53).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.47 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.198 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.080 R20 over the next 4 bars (1 h), p=0.74; we would catch an effect of 0.146 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.23 at recent bar sizes, 90% range up to $5.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.136 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.323 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $7.52 at recent bar sizes, 90% range up to $18.83); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.033 R20 over the next 2 bars (10 min), p=0.35; we would catch an effect of 0.068 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.88 at recent bar sizes, 90% range up to $1.63); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.070 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.127 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.97 at recent bar sizes, 90% range up to $7.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.135 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.286 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $12.83 at recent bar sizes, 90% range up to $29.86); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.017 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.087 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.63).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.87 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.158 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.104 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.172 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.23 at recent bar sizes, 90% range up to $6.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.181 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.384 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.58).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.78 at recent bar sizes, 90% range up to $18.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.027 | -0.001 .. +0.055 | +0.0019 | 0.059 / 0.072 / 0.062 | 0.056 | 1 | 1 | 12/16 | +0.013 | +0.041 | False | +1.8 / +1.9 |  |
| MES | 5 | h2 | +0.021 | -0.019 .. +0.062 | +0.0011 | 0.31 / 0.31 / 0.3 | 0.283 |  |  | 8/16 | +0.012 | +0.031 |  | +1.0 / +1.0 |  |
| MES | 5 | h4 | +0.003 | -0.054 .. +0.061 | +0.0001 | 0.91 / 0.91 / 0.9 | 0.903 |  |  | 8/16 | +0.005 | +0.001 |  | +0.1 / +0.1 | 0.080 |
| MES | 5 | h8 | -0.012 | -0.096 .. +0.072 | -0.0003 | 0.78 / 0.78 / 0.79 | 0.793 |  |  | 8/16 | +0.005 | -0.029 |  | -0.3 / -0.3 |  |
| MES | 5 | h16 | +0.008 | -0.112 .. +0.127 | +0.0001 | 0.9 / 0.9 / 0.9 | 0.888 |  |  | 8/16 | +0.029 | -0.014 |  | +0.1 / +0.1 |  |
| MES | 5 | eod | +0.174 | -0.330 .. +0.679 | +0.0006 | 0.5 / 0.49 / 0.53 | 0.528 |  |  | 9/16 | +0.241 | +0.108 |  | +0.6 / +0.7 |  |
| MES | 15 | h1 | -0.024 | -0.077 .. +0.029 | -0.0017 | 0.37 / 0.35 / 0.38 | 0.365 |  |  | 9/16 | -0.016 | -0.031 |  | -1.0 / -0.9 |  |
| MES | 15 | h2 | -0.014 | -0.090 .. +0.063 | -0.0007 | 0.73 / 0.71 / 0.74 | 0.71 |  |  | 7/16 | -0.074 | +0.047 |  | -0.4 / -0.4 |  |
| MES | 15 | h4 * | +0.080 | -0.021 .. +0.181 | +0.0026 | 0.12 / 0.11 / 0.18 | 0.157 | 1 | 1 | 11/16 | +0.035 | +0.124 | False | +1.5 / +1.5 | 0.146 |
| MES | 15 | h8 | +0.078 | -0.069 .. +0.226 | +0.0018 | 0.3 / 0.26 / 0.35 | 0.337 |  |  | 11/16 | +0.041 | +0.115 |  | +1.0 / +1.0 |  |
| MES | 15 | h16 | +0.010 | -0.206 .. +0.227 | +0.0002 | 0.92 / 0.92 / 0.93 | 0.928 |  |  | 7/16 | +0.101 | -0.080 |  | +0.1 / +0.1 |  |
| MES | 15 | eod | +0.081 | -0.448 .. +0.611 | +0.0005 | 0.76 / 0.76 / 0.78 | 0.78 |  |  | 11/16 | -0.129 | +0.291 |  | +0.3 / +0.3 |  |
| MES | 60 | h1 | +0.033 | -0.100 .. +0.167 | +0.0023 | 0.62 / 0.62 / 0.56 | 0.557 |  |  | 6/16 | +0.022 | +0.045 |  | +0.5 / +0.5 |  |
| MES | 60 | h2 | +0.079 | -0.111 .. +0.270 | +0.0039 | 0.42 / 0.4 / 0.35 | 0.349 |  |  | 9/16 | +0.101 | +0.058 |  | +0.8 / +0.8 |  |
| MES | 60 | h4 * | +0.136 | -0.096 .. +0.368 | +0.0048 | 0.25 / 0.25 / 0.24 | 0.249 | 1 | 1 | 8/16 | +0.130 | +0.142 | False | +1.1 / +1.2 | 0.323 |
| MES | 60 | h8 | +0.076 | -0.236 .. +0.389 | +0.0020 | 0.63 / 0.63 / 0.62 | 0.619 |  |  | 8/16 | -0.095 | +0.248 |  | +0.5 / +0.5 |  |
| MES | 60 | h16 | +0.056 | -0.282 .. +0.394 | +0.0011 | 0.74 / 0.74 / 0.74 | 0.729 |  |  | 8/16 | -0.192 | +0.305 |  | +0.3 / +0.3 |  |
| MES | 60 | eod | +0.086 | -0.254 .. +0.426 | +0.0016 | 0.62 / 0.62 / 0.61 | 0.608 |  |  | 8/16 | -0.171 | +0.344 |  | +0.5 / +0.5 |  |
| MNQ | 5 | h1 | +0.001 | -0.021 .. +0.024 | +0.0001 | 0.9 / 0.9 / 0.94 | 0.933 |  |  | 9/16 | +0.009 | -0.006 |  | +0.1 / +0.1 |  |
| MNQ | 5 | h2 * | -0.033 | -0.068 .. +0.001 | -0.0016 | 0.058 / 0.053 / 0.12 | 0.0745 | 1 | 1 | 11/16 | -0.024 | -0.043 | False | -1.9 / -1.9 |  |
| MNQ | 5 | h4 | -0.002 | -0.051 .. +0.047 | -0.0001 | 0.94 / 0.94 / 0.96 | 0.943 |  |  | 10/16 | +0.029 | -0.033 |  | -0.1 / -0.1 | 0.068 |
| MNQ | 5 | h8 | +0.005 | -0.062 .. +0.072 | +0.0001 | 0.88 / 0.88 / 0.91 | 0.884 |  |  | 11/16 | +0.038 | -0.027 |  | +0.1 / +0.1 |  |
| MNQ | 5 | h16 | +0.009 | -0.087 .. +0.105 | +0.0001 | 0.85 / 0.86 / 0.89 | 0.876 |  |  | 10/16 | +0.035 | -0.016 |  | +0.2 / +0.2 |  |
| MNQ | 5 | eod | +0.251 | -0.224 .. +0.727 | +0.0008 | 0.3 / 0.3 / 0.41 | 0.42 |  |  | 10/16 | -0.061 | +0.562 |  | +0.9 / +1.0 |  |
| MNQ | 15 | h1 | -0.006 | -0.051 .. +0.039 | -0.0004 | 0.79 / 0.79 / 0.83 | 0.788 |  |  | 8/16 | -0.028 | +0.016 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h2 | +0.006 | -0.057 .. +0.069 | +0.0003 | 0.85 / 0.86 / 0.9 | 0.852 |  |  | 8/16 | -0.050 | +0.062 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h4 | +0.000 | -0.091 .. +0.091 | -0.0000 | 1 / 1 / 1 | 1 |  |  | 6/16 | -0.088 | +0.088 |  | +0.0 / +0.0 | 0.127 |
| MNQ | 15 | h8 | +0.047 | -0.078 .. +0.172 | +0.0009 | 0.46 / 0.48 / 0.64 | 0.529 |  |  | 8/16 | -0.142 | +0.235 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h16 * | +0.070 | -0.102 .. +0.241 | +0.0011 | 0.43 / 0.45 / 0.56 | 0.517 | 1 | 1 | 6/16 | -0.071 | +0.210 | False | +0.7 / +0.8 |  |
| MNQ | 15 | eod | +0.010 | -0.434 .. +0.454 | +0.0001 | 0.97 / 0.97 / 0.98 | 0.974 |  |  | 7/16 | -0.193 | +0.211 |  | +0.0 / +0.0 |  |
| MNQ | 60 | h1 | -0.044 | -0.169 .. +0.081 | -0.0036 | 0.49 / 0.45 / 0.38 | 0.378 |  |  | 12/16 | -0.168 | +0.080 |  | -0.8 / -0.7 |  |
| MNQ | 60 | h2 | +0.007 | -0.146 .. +0.161 | +0.0004 | 0.92 / 0.92 / 0.92 | 0.922 |  |  | 7/16 | -0.069 | +0.084 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h4 | +0.002 | -0.183 .. +0.187 | +0.0001 | 0.98 / 0.98 / 0.99 | 0.985 |  |  | 9/16 | -0.025 | +0.029 |  | +0.0 / +0.0 | 0.286 |
| MNQ | 60 | h8 | +0.098 | -0.157 .. +0.353 | +0.0029 | 0.45 / 0.45 / 0.48 | 0.473 |  |  | 8/16 | +0.086 | +0.110 |  | +0.7 / +0.8 |  |
| MNQ | 60 | h16 | +0.131 | -0.155 .. +0.417 | +0.0030 | 0.37 / 0.36 / 0.39 | 0.403 |  |  | 10/16 | +0.178 | +0.085 |  | +0.9 / +0.9 |  |
| MNQ | 60 | eod * | +0.135 | -0.154 .. +0.423 | +0.0029 | 0.36 / 0.35 / 0.38 | 0.389 | 1 | 1 | 9/16 | +0.190 | +0.080 | False | +0.9 / +0.9 |  |
| MYM | 5 | h1 * | -0.017 | -0.050 .. +0.016 | -0.0013 | 0.31 / 0.3 / 0.36 | 0.266 | 1 | 1 | 5/8 | n/a | -0.017 | False | -1.1 / -1.0 |  |
| MYM | 5 | h2 | +0.004 | -0.043 .. +0.052 | +0.0002 | 0.86 / 0.86 / 0.91 | 0.872 |  |  | 4/8 | n/a | +0.004 |  | +0.2 / +0.2 |  |
| MYM | 5 | h4 | +0.031 | -0.028 .. +0.091 | +0.0009 | 0.3 / 0.29 / 0.53 | 0.387 |  |  | 6/8 | n/a | +0.031 |  | +1.0 / +1.0 | 0.087 |
| MYM | 5 | h8 | +0.038 | -0.048 .. +0.125 | +0.0008 | 0.39 / 0.38 / 0.6 | 0.489 |  |  | 6/8 | n/a | +0.038 |  | +0.9 / +0.9 |  |
| MYM | 5 | h16 | +0.054 | -0.065 .. +0.173 | +0.0008 | 0.37 / 0.4 / 0.57 | 0.518 |  |  | 4/8 | n/a | +0.054 |  | +0.8 / +0.9 |  |
| MYM | 5 | eod | -0.117 | -0.839 .. +0.604 | -0.0004 | 0.75 / 0.74 / 0.76 | 0.767 |  |  | 4/8 | n/a | -0.117 |  | -0.3 / -0.3 |  |
| MYM | 15 | h1 | -0.007 | -0.062 .. +0.048 | -0.0005 | 0.8 / 0.8 / 0.84 | 0.803 |  |  | 4/8 | n/a | -0.007 |  | -0.3 / -0.2 |  |
| MYM | 15 | h2 | +0.001 | -0.069 .. +0.070 | +0.0000 | 0.99 / 0.99 / 0.99 | 0.989 |  |  | 3/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 15 | h4 | +0.029 | -0.096 .. +0.153 | +0.0007 | 0.65 / 0.64 / 0.8 | 0.669 |  |  | 5/8 | n/a | +0.029 |  | +0.5 / +0.5 | 0.172 |
| MYM | 15 | h8 * | +0.104 | -0.071 .. +0.279 | +0.0020 | 0.24 / 0.25 / 0.39 | 0.278 | 1 | 1 | 3/8 | n/a | +0.104 | False | +1.1 / +1.2 |  |
| MYM | 15 | h16 | +0.157 | -0.096 .. +0.411 | +0.0022 | 0.22 / 0.25 / 0.42 | 0.303 |  |  | 3/8 | n/a | +0.157 |  | +1.2 / +1.2 |  |
| MYM | 15 | eod | +0.305 | -0.224 .. +0.835 | +0.0018 | 0.26 / 0.29 / 0.5 | 0.407 |  |  | 5/8 | n/a | +0.305 |  | +1.0 / +1.1 |  |
| MYM | 60 | h1 | -0.014 | -0.160 .. +0.132 | -0.0012 | 0.85 / 0.85 / 0.83 | 0.829 |  |  | 5/8 | n/a | -0.014 |  | -0.2 / -0.2 |  |
| MYM | 60 | h2 | -0.046 | -0.237 .. +0.144 | -0.0028 | 0.64 / 0.62 / 0.64 | 0.651 |  |  | 6/8 | n/a | -0.046 |  | -0.5 / -0.5 |  |
| MYM | 60 | h4 | -0.025 | -0.264 .. +0.214 | -0.0011 | 0.84 / 0.84 / 0.86 | 0.875 |  |  | 5/8 | n/a | -0.025 |  | -0.2 / -0.2 | 0.384 |
| MYM | 60 | h8 | -0.149 | -0.465 .. +0.166 | -0.0047 | 0.35 / 0.37 / 0.41 | 0.409 |  |  | 6/8 | n/a | -0.149 |  | -0.9 / -0.9 |  |
| MYM | 60 | h16 | -0.179 | -0.526 .. +0.169 | -0.0043 | 0.31 / 0.32 / 0.37 | 0.374 |  |  | 7/8 | n/a | -0.179 |  | -1.0 / -1.0 |  |
| MYM | 60 | eod * | -0.181 | -0.530 .. +0.167 | -0.0041 | 0.31 / 0.32 / 0.37 | 0.375 | 1 | 1 | 7/8 | n/a | -0.181 | False | -1.0 / -1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.011 | -0.010 .. +0.032 | +2.2% | +0.020 | 0.56 |  | 8/16 |
| MES | 5 | h2 * | +0.030 | -0.002 .. +0.063 | +4.3% | +0.030 | 0.089 | 1 | 9/16 |
| MES | 5 | h4 | +0.039 | -0.007 .. +0.086 | +3.9% | +0.066 | 0.13 |  | 10/16 |
| MES | 5 | h8 | +0.043 | -0.022 .. +0.109 | +3.0% | +0.055 | 0.29 |  | 12/16 |
| MES | 5 | h16 | +0.081 | -0.004 .. +0.166 | +3.9% | +0.086 | 0.19 |  | 11/16 |
| MES | 5 | eod | -0.036 | -0.449 .. +0.377 | -0.4% | -0.015 | 0.9 |  | 8/16 |
| MES | 15 | h1 | +0.002 | -0.030 .. +0.033 | +0.3% | -0.002 | 0.97 |  | 8/16 |
| MES | 15 | h2 | -0.008 | -0.056 .. +0.041 | -1.0% | -0.001 | 0.81 |  | 8/16 |
| MES | 15 | h4 * | -0.035 | -0.106 .. +0.037 | -3.3% | -0.015 | 0.38 | 1 | 8/16 |
| MES | 15 | h8 | -0.013 | -0.116 .. +0.090 | -0.8% | -0.048 | 0.89 |  | 10/16 |
| MES | 15 | h16 | -0.020 | -0.160 .. +0.121 | -0.9% | -0.069 | 0.78 |  | 9/16 |
| MES | 15 | eod | +0.032 | -0.355 .. +0.418 | +0.6% | -0.019 | 0.99 |  | 10/16 |
| MES | 60 | h1 * | +0.067 | -0.035 .. +0.169 | +13.1% | +0.062 | 0.2 | 1 | 13/16 |
| MES | 60 | h2 | +0.037 | -0.107 .. +0.181 | +5.0% | +0.074 | 0.61 |  | 7/16 |
| MES | 60 | h4 | +0.046 | -0.121 .. +0.213 | +4.4% | +0.071 | 0.59 |  | 8/16 |
| MES | 60 | h8 | +0.022 | -0.188 .. +0.233 | +1.5% | +0.041 | 0.83 |  | 8/16 |
| MES | 60 | h16 | +0.058 | -0.173 .. +0.289 | +2.8% | -0.035 | 0.62 |  | 11/16 |
| MES | 60 | eod | +0.066 | -0.163 .. +0.296 | +3.1% | -0.029 | 0.57 |  | 10/16 |
| MNQ | 5 | h1 | +0.005 | -0.008 .. +0.019 | +1.0% | +0.018 | 0.91 |  | 10/16 |
| MNQ | 5 | h2 | +0.011 | -0.014 .. +0.036 | +1.5% | +0.027 | 0.51 |  | 10/16 |
| MNQ | 5 | h4 * | +0.025 | -0.010 .. +0.060 | +2.2% | +0.022 | 0.2 | 1 | 9/16 |
| MNQ | 5 | h8 | +0.016 | -0.037 .. +0.068 | +1.0% | +0.030 | 0.56 |  | 10/16 |
| MNQ | 5 | h16 | +0.012 | -0.067 .. +0.091 | +0.5% | +0.023 | 0.98 |  | 9/16 |
| MNQ | 5 | eod | -0.264 | -0.756 .. +0.228 | -2.1% | -0.361 | 0.3 |  | 10/16 |
| MNQ | 15 | h1 | +0.020 | -0.012 .. +0.051 | +3.7% | +0.032 | 0.76 |  | 11/16 |
| MNQ | 15 | h2 | +0.041 | -0.005 .. +0.088 | +5.3% | +0.046 | 0.76 |  | 10/16 |
| MNQ | 15 | h4 * | +0.063 | -0.007 .. +0.133 | +5.6% | +0.090 | 0.64 | 1 | 10/16 |
| MNQ | 15 | h8 | +0.008 | -0.091 .. +0.108 | +0.5% | +0.032 | 0.89 |  | 9/16 |
| MNQ | 15 | h16 | -0.021 | -0.157 .. +0.115 | -0.8% | -0.034 | 0.99 |  | 10/16 |
| MNQ | 15 | eod | +0.023 | -0.312 .. +0.358 | +0.4% | -0.215 | 0.9 |  | 12/16 |
| MNQ | 60 | h1 * | +0.037 | -0.041 .. +0.115 | +7.0% | +0.065 | 0.35 | 1 | 10/16 |
| MNQ | 60 | h2 | -0.002 | -0.095 .. +0.091 | -0.3% | +0.059 | 0.96 |  | 8/16 |
| MNQ | 60 | h4 | -0.059 | -0.178 .. +0.060 | -5.3% | +0.007 | 0.6 |  | 11/16 |
| MNQ | 60 | h8 | +0.003 | -0.156 .. +0.162 | +0.2% | +0.013 | 0.97 |  | 8/16 |
| MNQ | 60 | h16 | -0.064 | -0.242 .. +0.114 | -2.9% | -0.016 | 0.62 |  | 9/16 |
| MNQ | 60 | eod | -0.054 | -0.234 .. +0.127 | -2.3% | -0.016 | 0.71 |  | 8/16 |
| MYM | 5 | h1 | +0.006 | -0.016 .. +0.027 | +1.1% | +0.008 | 0.88 |  | 4/8 |
| MYM | 5 | h2 | +0.006 | -0.023 .. +0.035 | +0.8% | +0.010 | 0.92 |  | 4/8 |
| MYM | 5 | h4 | -0.018 | -0.059 .. +0.024 | -1.6% | +0.024 | 0.44 |  | 5/8 |
| MYM | 5 | h8 * | -0.055 | -0.117 .. +0.007 | -3.5% | -0.004 | 0.1 | 1 | 5/8 |
| MYM | 5 | h16 | -0.018 | -0.114 .. +0.078 | -0.8% | -0.019 | 0.91 |  | 4/8 |
| MYM | 5 | eod | -0.158 | -0.640 .. +0.324 | -1.3% | +0.017 | 0.9 |  | 3/8 |
| MYM | 15 | h1 | -0.010 | -0.044 .. +0.024 | -1.9% | -0.015 | 0.61 |  | 5/8 |
| MYM | 15 | h2 * | -0.061 | -0.114 .. -0.007 | -7.9% | -0.063 | 0.39 | 1 | 6/8 |
| MYM | 15 | h4 | +0.004 | -0.082 .. +0.090 | +0.4% | -0.027 | 0.93 |  | 4/8 |
| MYM | 15 | h8 | +0.037 | -0.088 .. +0.162 | +2.3% | -0.008 | 0.95 |  | 3/8 |
| MYM | 15 | h16 | +0.094 | -0.104 .. +0.292 | +3.8% | +0.002 | 0.97 |  | 5/8 |
| MYM | 15 | eod | -0.187 | -0.652 .. +0.278 | -3.1% | -0.322 | 0.48 |  | 5/8 |
| MYM | 60 | h1 | +0.061 | -0.030 .. +0.153 | +11.7% | +0.087 | 0.26 |  | 7/8 |
| MYM | 60 | h2 | -0.048 | -0.159 .. +0.063 | -6.4% | -0.022 | 0.42 |  | 5/8 |
| MYM | 60 | h4 | -0.131 | -0.297 .. +0.035 | -12.1% | -0.104 | 0.12 |  | 6/8 |
| MYM | 60 | h8 | -0.077 | -0.277 .. +0.122 | -5.0% | -0.178 | 0.45 |  | 6/8 |
| MYM | 60 | h16 | -0.179 | -0.384 .. +0.026 | -8.5% | -0.241 | 0.11 |  | 6/8 |
| MYM | 60 | eod * | -0.188 | -0.395 .. +0.020 | -8.4% | -0.258 | 0.096 | 1 | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +1.06 pts | -0.80 .. +2.93 | 0.26 |
| MES | 15 | -0.02 pts | -2.89 .. +2.85 | 0.99 |
| MES | 60 | +2.64 pts | -2.87 .. +8.16 | 0.45 |
| MNQ | 5 | -0.13 pts | -1.49 .. +1.22 | 0.85 |
| MNQ | 15 | +0.91 pts | -1.43 .. +3.25 | 0.46 |
| MNQ | 60 | -0.26 pts | -4.97 .. +4.45 | 0.99 |
| MYM | 5 | +0.59 pts | -1.24 .. +2.43 | 0.53 |
| MYM | 15 | +0.81 pts | -2.32 .. +3.95 | 0.61 |
| MYM | 60 | -1.83 pts | -7.82 .. +4.17 | 0.55 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 2756 | +0.016 | 0.261 | +0.37 | -3.13 | -3.44 | -2.94 | -2.98 |
| MES | 5 | h2 | event | with signal | 2756 | +0.005 | 0.261 | +0.26 | -3.24 | -3.40 | -3.14 | -3.01 |
| MES | 5 | h4 | event | with signal | 2756 | -0.014 | 0.261 | +0.07 | -3.43 | -3.47 | -3.41 | -3.20 |
| MES | 5 | h8 | event | against signal | 2756 | +0.028 | 0.261 | +0.10 | -3.40 | -3.61 | -3.28 | -3.64 |
| MES | 5 | h16 | event | with signal | 2756 | -0.009 | 0.261 | -0.26 | -3.76 | -3.48 | -3.94 | -3.56 |
| MES | 5 | eod | event | with signal | 2756 | +0.122 | 0.261 | +2.52 | -0.98 | -2.16 | -0.27 | -0.50 |
| MES | 15 | h1 | event | against signal | 1080 | +0.032 | 0.179 | +0.99 | -2.51 | -3.25 | -1.87 | -2.66 |
| MES | 15 | h2 | event | against signal | 1080 | +0.025 | 0.179 | +0.93 | -2.57 | -2.81 | -2.37 | -2.80 |
| MES | 15 | h4 | event | with signal | 1080 | +0.068 | 0.179 | +0.55 | -2.95 | -3.18 | -2.75 | -2.72 |
| MES | 15 | h8 | event | with signal | 1080 | +0.063 | 0.179 | +0.59 | -2.91 | -3.18 | -2.68 | -2.59 |
| MES | 15 | h16 | event | with signal | 1080 | -0.017 | 0.179 | -0.94 | -4.44 | -2.81 | -5.84 | -3.92 |
| MES | 15 | eod | event | with signal | 1080 | +0.018 | 0.179 | +1.90 | -1.60 | -4.45 | +0.83 | +0.08 |
| MES | 60 | h1 | event | with signal | 255 | +0.032 | 0.094 | +0.50 | -3.00 | -2.16 | -3.89 | -2.97 |
| MES | 60 | h2 | event | with signal | 255 | +0.070 | 0.094 | +0.16 | -3.34 | -1.05 | -5.76 | -3.04 |
| MES | 60 | h4 | event | with signal | 255 | +0.122 | 0.094 | +1.22 | -2.28 | -1.10 | -3.53 | -1.80 |
| MES | 60 | h8 | event | with signal | 255 | +0.052 | 0.094 | +0.05 | -3.45 | -5.95 | -0.80 | -2.62 |
| MES | 60 | h16 | event | with signal | 255 | +0.034 | 0.094 | +2.38 | -1.12 | -7.84 | +5.98 | -0.37 |
| MES | 60 | eod | event | with signal | 255 | +0.059 | 0.094 | +3.67 | +0.17 | -7.76 | +8.55 | +1.06 |
| MNQ | 5 | h1 | event | with signal | 4973 | -0.004 | 0.112 | +0.23 | -1.77 | -1.92 | -1.67 | -1.68 |
| MNQ | 5 | h2 | event | against signal | 4973 | +0.042 | 0.112 | +0.41 | -1.59 | -1.92 | -1.37 | -1.75 |
| MNQ | 5 | h4 | event | against signal | 4973 | +0.009 | 0.112 | -0.28 | -2.28 | -2.15 | -2.37 | -2.41 |
| MNQ | 5 | h8 | event | with signal | 4973 | +0.003 | 0.112 | +0.39 | -1.61 | -1.71 | -1.55 | -1.58 |
| MNQ | 5 | h16 | event | with signal | 4973 | +0.007 | 0.112 | -0.61 | -2.61 | -1.66 | -3.25 | -2.59 |
| MNQ | 5 | eod | event | with signal | 4973 | +0.122 | 0.112 | +4.83 | +2.83 | -2.16 | +6.14 | +5.46 |
| MNQ | 15 | h1 | event | against signal | 1710 | +0.009 | 0.070 | -0.27 | -2.27 | -1.61 | -2.73 | -2.37 |
| MNQ | 15 | h2 | event | with signal | 1710 | +0.005 | 0.070 | +0.82 | -1.18 | -2.82 | -0.02 | -1.15 |
| MNQ | 15 | h4 | event | with signal | 1710 | -0.001 | 0.070 | +1.70 | -0.30 | -3.29 | +1.82 | -0.26 |
| MNQ | 15 | h8 | event | with signal | 1710 | +0.047 | 0.070 | +4.14 | +2.14 | -3.75 | +6.31 | +2.10 |
| MNQ | 15 | h16 | event | with signal | 1710 | +0.057 | 0.070 | +3.34 | +1.34 | -3.59 | +4.84 | +1.70 |
| MNQ | 15 | eod | event | with signal | 1710 | -0.023 | 0.070 | +5.76 | +3.76 | -4.41 | +9.56 | +4.93 |
| MNQ | 60 | h1 | event | against signal | 380 | +0.044 | 0.032 | +0.19 | -1.81 | +1.79 | -4.63 | -1.73 |
| MNQ | 60 | h2 | event | with signal | 380 | +0.001 | 0.032 | +0.34 | -1.66 | -5.20 | +1.12 | -1.48 |
| MNQ | 60 | h4 | event | with signal | 380 | -0.010 | 0.032 | -3.26 | -5.26 | -5.14 | -5.36 | -4.83 |
| MNQ | 60 | h8 | event | with signal | 380 | +0.082 | 0.032 | -0.73 | -2.73 | -2.54 | -2.88 | -2.27 |
| MNQ | 60 | h16 | event | with signal | 380 | +0.120 | 0.032 | -0.68 | -2.68 | -1.11 | -3.92 | -2.71 |
| MNQ | 60 | eod | event | with signal | 380 | +0.119 | 0.032 | -1.52 | -3.52 | -1.37 | -5.20 | -3.27 |
| MYM | 5 | h1 | event | against signal | 2739 | +0.025 | 0.158 | +0.18 | -1.82 | +nan | -1.82 | -1.92 |
| MYM | 5 | h2 | event | with signal | 2739 | -0.007 | 0.158 | -0.04 | -2.04 | +nan | -2.04 | -1.87 |
| MYM | 5 | h4 | event | with signal | 2739 | +0.016 | 0.158 | +0.52 | -1.48 | +nan | -1.48 | -1.26 |
| MYM | 5 | h8 | event | with signal | 2739 | +0.017 | 0.158 | +0.65 | -1.35 | +nan | -1.35 | -1.04 |
| MYM | 5 | h16 | event | with signal | 2739 | +0.023 | 0.158 | +0.79 | -1.21 | +nan | -1.21 | -0.78 |
| MYM | 5 | eod | event | against signal | 2739 | +0.223 | 0.158 | +1.06 | -0.94 | +nan | -0.94 | -2.46 |
| MYM | 15 | h1 | event | against signal | 904 | +0.013 | 0.093 | +0.09 | -1.91 | +nan | -1.91 | -2.05 |
| MYM | 15 | h2 | event | with signal | 904 | -0.007 | 0.093 | +0.22 | -1.78 | +nan | -1.78 | -1.62 |
| MYM | 15 | h4 | event | with signal | 904 | +0.021 | 0.093 | +0.31 | -1.69 | +nan | -1.69 | -1.55 |
| MYM | 15 | h8 | event | with signal | 904 | +0.094 | 0.093 | +3.38 | +1.38 | +nan | +1.38 | +1.61 |
| MYM | 15 | h16 | event | with signal | 904 | +0.145 | 0.093 | +3.88 | +1.88 | +nan | +1.88 | +2.11 |
| MYM | 15 | eod | event | with signal | 904 | +0.273 | 0.093 | +5.64 | +3.64 | +nan | +3.64 | +3.99 |
| MYM | 60 | h1 | event | against signal | 204 | +0.012 | 0.047 | +3.52 | +1.52 | +nan | +1.52 | +1.70 |
| MYM | 60 | h2 | event | against signal | 204 | +0.053 | 0.047 | +4.96 | +2.96 | +nan | +2.96 | +2.84 |
| MYM | 60 | h4 | event | against signal | 204 | +0.035 | 0.047 | +3.73 | +1.73 | +nan | +1.73 | +1.54 |
| MYM | 60 | h8 | event | against signal | 204 | +0.169 | 0.047 | +8.25 | +6.25 | +nan | +6.25 | +5.61 |
| MYM | 60 | h16 | event | against signal | 204 | +0.190 | 0.047 | +8.61 | +6.61 | +nan | +6.61 | +6.18 |
| MYM | 60 | eod | event | against signal | 204 | +0.194 | 0.047 | +8.59 | +6.59 | +nan | +6.59 | +6.16 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.095 | +0.222 | +0.128 | -0.707 | -0.987 | +0.000 | -0.009 | -0.020 | -0.036 | -0.050 | -0.044 |
| MES | 15 | +0.109 | +0.213 | +0.087 | -0.752 | -0.990 | +0.000 | -0.039 | -0.031 | +0.064 | +0.061 | -0.028 |
| MES | 60 | +0.193 | +0.080 | +0.035 | -0.850 | -1.042 | +0.000 | +0.035 | +0.085 | +0.081 | -0.193 | +0.027 |
| MNQ | 5 | +0.059 | +0.159 | +0.098 | -0.775 | -1.010 | +0.000 | -0.017 | -0.056 | -0.021 | -0.008 | -0.011 |
| MNQ | 15 | +0.060 | +0.130 | +0.059 | -0.782 | -0.975 | +0.000 | -0.015 | +0.005 | +0.004 | +0.049 | +0.075 |
| MNQ | 60 | -0.181 | +0.026 | -0.046 | -0.867 | -1.018 | +0.000 | -0.040 | +0.006 | +0.031 | +0.315 | -1.024 |
| MYM | 5 | +0.125 | +0.241 | +0.127 | -0.764 | -0.990 | +0.000 | -0.030 | -0.010 | +0.016 | +0.022 | +0.044 |
| MYM | 15 | +0.063 | +0.166 | +0.082 | -0.801 | -1.003 | +0.000 | -0.012 | -0.007 | +0.030 | +0.101 | +0.189 |
| MYM | 60 | +0.446 | +0.291 | +0.031 | -0.864 | -1.054 | +0.000 | -0.011 | -0.038 | -0.069 | +0.045 | +0.327 |

## Calibration

- MES 5-min: 1036271 bars, 2756 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1080 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 255 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 4973 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1710 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 380 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 2739 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 904 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 204 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32781 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
