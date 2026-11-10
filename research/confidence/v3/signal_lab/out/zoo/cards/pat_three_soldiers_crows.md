# Impact card: pat_three_soldiers_crows

candle pattern three_soldiers_crows in its textbook direction: 3 bars same colour, each closing beyond the previous close, each opening inside the previous body, bodies > 0.5 x avgB10, shadow on the close side <= 0.3 x body [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.090 R20 over the next 8 bars (40 min), p=0.07; we would catch an effect of 0.064 R20 or more 80% of the time).
- MES 5-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.059 R20, CONFIRMED, q=1.45e-10, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.33 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.222 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.409 R20 over the rest of the session (to 16:45), p=0.96; we would catch an effect of 0.140 R20 or more 80% of the time).
- MES 15-min size: the market moves 11% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.054 R20, possible, q=0.212, 13 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $12.25 at recent bar sizes, 90% range up to $6.30); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.239 R20 over the next 4 bars (4 h), p=0.42; we would catch an effect of 0.333 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.87).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $12.48 at recent bar sizes, 90% range up to $27.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.089 R20 over the next 4 bars (20 min), p=0.053; we would catch an effect of 0.077 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.065 R20, CONFIRMED, q=7.73e-05, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.38 at recent bar sizes, 90% range up to $5.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.173 R20 over the next 4 bars (1 h), p=0.05; we would catch an effect of 0.170 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.017).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.99 at recent bar sizes, 90% range up to $12.38); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.065 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.399 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.78 at recent bar sizes, 90% range up to $28.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.103 R20 over the next 4 bars (20 min), p=0.18; we would catch an effect of 0.110 R20 or more 80% of the time).
- MYM 5-min size: the market moves 13% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.069 R20, CONFIRMED, q=0.000173, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.13 at recent bar sizes, 90% range up to $2.01); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.098 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.232 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.048).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.93 at recent bar sizes, 90% range up to $5.29); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.245 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.524 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.60 at recent bar sizes, 90% range up to $32.13); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.008 | -0.015 .. +0.032 | +0.0008 | 0.5 / 0.49 / 0.43 | 0.434 |  |  | 9/16 | +0.015 | +0.002 |  | +0.7 / +0.7 |  |
| MES | 5 | h2 | +0.028 | -0.006 .. +0.061 | +0.0019 | 0.1 / 0.11 / 0.093 | 0.0875 |  |  | 13/16 | +0.040 | +0.015 |  | +1.7 / +1.6 |  |
| MES | 5 | h4 | +0.042 | -0.005 .. +0.089 | +0.0020 | 0.078 / 0.085 / 0.08 | 0.081 |  |  | 12/16 | +0.064 | +0.020 |  | +1.9 / +1.8 | 0.064 |
| MES | 5 | h8 * | +0.090 | +0.021 .. +0.158 | +0.0029 | 0.01 / 0.012 / 0.011 | 0.0141 | 1 | 0.904 | 14/16 | +0.119 | +0.060 | False | +2.9 / +2.6 |  |
| MES | 5 | h16 | +0.059 | -0.035 .. +0.153 | +0.0013 | 0.22 / 0.24 / 0.25 | 0.248 |  |  | 11/16 | +0.043 | +0.075 |  | +1.3 / +1.2 |  |
| MES | 5 | eod | +0.172 | -0.368 .. +0.713 | +0.0008 | 0.53 / 0.55 / 0.52 | 0.519 |  |  | 11/16 | +0.282 | +0.063 |  | +0.7 / +0.6 |  |
| MES | 15 | h1 | +0.008 | -0.035 .. +0.051 | +0.0006 | 0.73 / 0.73 / 0.73 | 0.739 |  |  | 9/16 | -0.003 | +0.018 |  | +0.3 / +0.3 |  |
| MES | 15 | h2 | +0.048 | -0.017 .. +0.114 | +0.0026 | 0.15 / 0.16 / 0.16 | 0.15 |  |  | 7/16 | +0.050 | +0.047 |  | +1.5 / +1.5 |  |
| MES | 15 | h4 | +0.079 | -0.013 .. +0.170 | +0.0029 | 0.092 / 0.096 / 0.14 | 0.119 |  |  | 12/16 | +0.052 | +0.106 |  | +1.8 / +1.7 | 0.140 |
| MES | 15 | h8 | +0.095 | -0.035 .. +0.226 | +0.0024 | 0.15 / 0.18 / 0.2 | 0.194 |  |  | 12/16 | +0.074 | +0.117 |  | +1.5 / +1.4 |  |
| MES | 15 | h16 | +0.115 | -0.070 .. +0.301 | +0.0021 | 0.22 / 0.23 / 0.26 | 0.262 |  |  | 9/16 | +0.127 | +0.104 |  | +1.3 / +1.2 |  |
| MES | 15 | eod * | +0.409 | -0.092 .. +0.911 | +0.0028 | 0.11 / 0.11 / 0.14 | 0.143 | 1 | 1 | 13/16 | +0.413 | +0.406 | False | +1.8 / +1.6 |  |
| MES | 60 | h1 | +0.056 | -0.069 .. +0.182 | +0.0040 | 0.38 / 0.38 / 0.31 | 0.31 |  |  | 7/16 | -0.093 | +0.205 |  | +0.9 / +0.9 |  |
| MES | 60 | h2 | +0.088 | -0.077 .. +0.253 | +0.0043 | 0.3 / 0.31 / 0.29 | 0.29 |  |  | 5/16 | -0.078 | +0.254 |  | +1.1 / +1.0 |  |
| MES | 60 | h4 * | +0.239 | +0.021 .. +0.458 | +0.0084 | 0.032 / 0.037 / 0.046 | 0.0495 | 1 | 0.997 | 9/16 | +0.023 | +0.455 | False | +2.3 / +2.1 | 0.333 |
| MES | 60 | h8 | +0.241 | -0.075 .. +0.556 | +0.0061 | 0.14 / 0.14 / 0.14 | 0.14 |  |  | 9/16 | -0.083 | +0.564 |  | +1.6 / +1.5 |  |
| MES | 60 | h16 | +0.176 | -0.186 .. +0.539 | +0.0035 | 0.34 / 0.35 / 0.35 | 0.351 |  |  | 7/16 | -0.260 | +0.613 |  | +1.0 / +1.0 |  |
| MES | 60 | eod | +0.184 | -0.182 .. +0.550 | +0.0035 | 0.32 / 0.34 / 0.33 | 0.329 |  |  | 7/16 | -0.264 | +0.632 |  | +1.1 / +1.0 |  |
| MNQ | 5 | h1 | +0.034 | +0.006 .. +0.061 | +0.0025 | 0.015 / 0.016 / 0.01 | 0.0154 |  |  | 11/16 | +0.040 | +0.028 |  | +2.5 / +2.4 |  |
| MNQ | 5 | h2 | +0.035 | -0.009 .. +0.079 | +0.0016 | 0.12 / 0.12 / 0.11 | 0.0703 |  |  | 11/16 | +0.032 | +0.039 |  | +1.8 / +1.6 |  |
| MNQ | 5 | h4 * | +0.089 | +0.023 .. +0.154 | +0.0026 | 0.0078 / 0.0088 / 0.012 | 0.0232 | 1 | 0.83 | 11/16 | +0.109 | +0.069 | False | +3.2 / +2.7 | 0.077 |
| MNQ | 5 | h8 | +0.117 | +0.023 .. +0.211 | +0.0024 | 0.015 / 0.014 / 0.03 | 0.0438 |  |  | 9/16 | +0.148 | +0.087 |  | +2.9 / +2.4 |  |
| MNQ | 5 | h16 | +0.111 | -0.017 .. +0.240 | +0.0016 | 0.09 / 0.099 / 0.16 | 0.143 |  |  | 11/16 | +0.145 | +0.078 |  | +1.9 / +1.7 |  |
| MNQ | 5 | eod | +0.240 | -0.470 .. +0.951 | +0.0007 | 0.51 / 0.53 / 0.54 | 0.55 |  |  | 9/16 | +0.196 | +0.284 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h1 | +0.000 | -0.057 .. +0.057 | +0.0000 | 1 / 1 / 1 | 0.999 |  |  | 9/16 | -0.000 | +0.000 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h2 | +0.074 | -0.006 .. +0.154 | +0.0025 | 0.068 / 0.078 / 0.2 | 0.0742 |  |  | 10/16 | +0.114 | +0.034 |  | +1.9 / +1.8 |  |
| MNQ | 15 | h4 * | +0.173 | +0.058 .. +0.287 | +0.0034 | 0.0031 / 0.0031 / 0.092 | 0.0344 | 1 | 0.539 | 13/16 | +0.209 | +0.136 | False | +3.0 / +3.0 | 0.170 |
| MNQ | 15 | h8 | +0.085 | -0.102 .. +0.272 | +0.0013 | 0.37 / 0.36 / 0.52 | 0.392 |  |  | 9/16 | -0.032 | +0.201 |  | +1.0 / +0.9 |  |
| MNQ | 15 | h16 | +0.157 | -0.103 .. +0.417 | +0.0019 | 0.24 / 0.24 / 0.33 | 0.277 |  |  | 11/16 | -0.039 | +0.352 |  | +1.2 / +1.2 |  |
| MNQ | 15 | eod | +0.176 | -0.486 .. +0.838 | +0.0008 | 0.6 / 0.61 / 0.69 | 0.628 |  |  | 11/16 | +0.008 | +0.343 |  | +0.6 / +0.5 |  |
| MNQ | 60 | h1 | -0.007 | -0.126 .. +0.112 | -0.0004 | 0.91 / 0.91 / 0.92 | 0.918 |  |  | 9/16 | -0.099 | +0.085 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h2 * | +0.065 | -0.102 .. +0.233 | +0.0028 | 0.44 / 0.46 / 0.52 | 0.526 | 1 | 1 | 10/16 | -0.002 | +0.133 | False | +0.8 / +0.8 |  |
| MNQ | 60 | h4 | +0.062 | -0.195 .. +0.319 | +0.0018 | 0.64 / 0.63 / 0.66 | 0.661 |  |  | 11/16 | -0.086 | +0.210 |  | +0.5 / +0.5 | 0.399 |
| MNQ | 60 | h8 | -0.006 | -0.384 .. +0.372 | -0.0002 | 0.98 / 0.98 / 0.97 | 0.972 |  |  | 6/16 | -0.300 | +0.289 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h16 | -0.040 | -0.463 .. +0.384 | -0.0008 | 0.85 / 0.85 / 0.84 | 0.833 |  |  | 8/16 | -0.411 | +0.332 |  | -0.2 / -0.2 |  |
| MNQ | 60 | eod | -0.048 | -0.471 .. +0.375 | -0.0009 | 0.82 / 0.82 / 0.81 | 0.807 |  |  | 8/16 | -0.415 | +0.319 |  | -0.2 / -0.2 |  |
| MYM | 5 | h1 | +0.034 | -0.006 .. +0.074 | +0.0022 | 0.097 / 0.09 / 0.14 | 0.0711 |  |  | 5/8 | n/a | +0.034 |  | +1.8 / +1.7 |  |
| MYM | 5 | h2 | +0.065 | +0.002 .. +0.128 | +0.0026 | 0.042 / 0.031 / 0.08 | 0.0411 |  |  | 6/8 | n/a | +0.065 |  | +2.5 / +2.0 |  |
| MYM | 5 | h4 * | +0.103 | +0.010 .. +0.196 | +0.0025 | 0.03 / 0.023 / 0.079 | 0.0453 | 1 | 0.996 | 7/8 | n/a | +0.103 | False | +2.5 / +2.2 | 0.110 |
| MYM | 5 | h8 | +0.078 | -0.047 .. +0.203 | +0.0014 | 0.22 / 0.21 / 0.35 | 0.239 |  |  | 4/8 | n/a | +0.078 |  | +1.4 / +1.2 |  |
| MYM | 5 | h16 | +0.062 | -0.121 .. +0.244 | +0.0008 | 0.51 / 0.5 / 0.57 | 0.522 |  |  | 5/8 | n/a | +0.062 |  | +0.8 / +0.7 |  |
| MYM | 5 | eod | -0.674 | -1.759 .. +0.411 | -0.0021 | 0.22 / 0.19 / 0.17 | 0.178 |  |  | 6/8 | n/a | -0.674 |  | -1.5 / -1.2 |  |
| MYM | 15 | h1 | -0.037 | -0.121 .. +0.047 | -0.0021 | 0.39 / 0.4 / 0.4 | 0.338 |  |  | 4/8 | n/a | -0.037 |  | -0.8 / -0.9 |  |
| MYM | 15 | h2 | -0.063 | -0.188 .. +0.062 | -0.0020 | 0.32 / 0.32 / 0.43 | 0.291 |  |  | 4/8 | n/a | -0.063 |  | -1.0 / -1.0 |  |
| MYM | 15 | h4 * | -0.098 | -0.276 .. +0.081 | -0.0019 | 0.28 / 0.26 / 0.49 | 0.29 | 1 | 1 | 5/8 | n/a | -0.098 | False | -1.2 / -1.1 | 0.232 |
| MYM | 15 | h8 | -0.079 | -0.303 .. +0.144 | -0.0012 | 0.49 / 0.48 / 0.64 | 0.544 |  |  | 4/8 | n/a | -0.079 |  | -0.7 / -0.7 |  |
| MYM | 15 | h16 | -0.104 | -0.400 .. +0.192 | -0.0011 | 0.49 / 0.53 / 0.7 | 0.619 |  |  | 4/8 | n/a | -0.104 |  | -0.6 / -0.7 |  |
| MYM | 15 | eod | +0.066 | -1.077 .. +1.208 | +0.0003 | 0.91 / 0.91 / 0.92 | 0.891 |  |  | 5/8 | n/a | +0.066 |  | +0.1 / +0.1 |  |
| MYM | 60 | h1 | +0.063 | -0.108 .. +0.233 | +0.0038 | 0.47 / 0.46 / 0.49 | 0.502 |  |  | 4/8 | n/a | +0.063 |  | +0.8 / +0.7 |  |
| MYM | 60 | h2 | +0.047 | -0.222 .. +0.316 | +0.0020 | 0.73 / 0.72 / 0.73 | 0.728 |  |  | 4/8 | n/a | +0.047 |  | +0.4 / +0.3 |  |
| MYM | 60 | h4 * | +0.245 | -0.178 .. +0.667 | +0.0073 | 0.26 / 0.23 / 0.21 | 0.208 | 1 | 1 | 5/8 | n/a | +0.245 | False | +1.4 / +1.1 | 0.524 |
| MYM | 60 | h8 | +0.217 | -0.407 .. +0.842 | +0.0047 | 0.49 / 0.47 / 0.42 | 0.417 |  |  | 5/8 | n/a | +0.217 |  | +0.9 / +0.7 |  |
| MYM | 60 | h16 | +0.238 | -0.468 .. +0.944 | +0.0040 | 0.51 / 0.49 / 0.45 | 0.444 |  |  | 5/8 | n/a | +0.238 |  | +0.8 / +0.7 |  |
| MYM | 60 | eod | +0.148 | -0.569 .. +0.865 | +0.0023 | 0.69 / 0.66 / 0.64 | 0.643 |  |  | 4/8 | n/a | +0.148 |  | +0.5 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.059 | +0.043 .. +0.075 | +11.9% | +0.129 | 3.8e-13 | 1.45e-10 | 15/16 |
| MES | 5 | h2 | +0.064 | +0.040 .. +0.088 | +9.1% | +0.136 | 1.5e-07 |  | 16/16 |
| MES | 5 | h4 | +0.065 | +0.028 .. +0.102 | +6.5% | +0.152 | 0.00055 |  | 14/16 |
| MES | 5 | h8 | +0.065 | +0.013 .. +0.117 | +4.5% | +0.146 | 0.015 |  | 12/16 |
| MES | 5 | h16 | +0.051 | -0.016 .. +0.119 | +2.5% | +0.156 | 0.14 |  | 10/16 |
| MES | 5 | eod | +0.242 | -0.134 .. +0.618 | +2.4% | +0.382 | 0.22 |  | 10/16 |
| MES | 15 | h1 * | +0.054 | +0.022 .. +0.086 | +10.6% | +0.102 | 0.0013 | 0.212 | 13/16 |
| MES | 15 | h2 | +0.041 | +0.001 .. +0.081 | +5.6% | +0.104 | 0.11 |  | 10/16 |
| MES | 15 | h4 | +0.022 | -0.034 .. +0.079 | +2.1% | +0.086 | 0.75 |  | 9/16 |
| MES | 15 | h8 | +0.023 | -0.065 .. +0.112 | +1.5% | +0.063 | 0.91 |  | 8/16 |
| MES | 15 | h16 | +0.022 | -0.113 .. +0.157 | +1.0% | +0.086 | 0.97 |  | 7/16 |
| MES | 15 | eod | -0.138 | -0.497 .. +0.222 | -2.5% | -0.010 | 0.58 |  | 10/16 |
| MES | 60 | h1 * | +0.065 | -0.023 .. +0.154 | +12.8% | +0.099 | 0.15 | 1 | 10/16 |
| MES | 60 | h2 | +0.061 | -0.041 .. +0.162 | +8.2% | +0.089 | 0.3 |  | 10/16 |
| MES | 60 | h4 | +0.017 | -0.116 .. +0.151 | +1.6% | +0.065 | 0.89 |  | 7/16 |
| MES | 60 | h8 | +0.138 | -0.064 .. +0.341 | +9.2% | +0.022 | 0.19 |  | 8/16 |
| MES | 60 | h16 | +0.101 | -0.142 .. +0.344 | +4.9% | -0.005 | 0.41 |  | 7/16 |
| MES | 60 | eod | +0.101 | -0.153 .. +0.354 | +4.6% | -0.015 | 0.44 |  | 7/16 |
| MNQ | 5 | h1 * | +0.065 | +0.044 .. +0.085 | +12.1% | +0.137 | 3e-07 | 7.73e-05 | 15/16 |
| MNQ | 5 | h2 | +0.081 | +0.050 .. +0.112 | +10.5% | +0.171 | 0.0007 |  | 15/16 |
| MNQ | 5 | h4 | +0.089 | +0.042 .. +0.136 | +8.0% | +0.196 | 0.007 |  | 15/16 |
| MNQ | 5 | h8 | +0.131 | +0.066 .. +0.195 | +8.1% | +0.236 | 0.0015 |  | 13/16 |
| MNQ | 5 | h16 | +0.142 | +0.047 .. +0.236 | +5.9% | +0.299 | 0.0096 |  | 13/16 |
| MNQ | 5 | eod | +0.574 | +0.030 .. +1.117 | +4.6% | +1.457 | 0.053 |  | 10/16 |
| MNQ | 15 | h1 | +0.046 | +0.005 .. +0.088 | +8.7% | +0.093 | 0.028 |  | 11/16 |
| MNQ | 15 | h2 | +0.069 | +0.014 .. +0.124 | +8.9% | +0.118 | 0.018 |  | 13/16 |
| MNQ | 15 | h4 * | +0.122 | +0.043 .. +0.201 | +10.8% | +0.165 | 0.0029 | 0.451 | 11/16 |
| MNQ | 15 | h8 | +0.133 | +0.009 .. +0.256 | +7.9% | +0.210 | 0.1 |  | 11/16 |
| MNQ | 15 | h16 | +0.237 | +0.056 .. +0.418 | +9.4% | +0.272 | 0.037 |  | 13/16 |
| MNQ | 15 | eod | +0.335 | -0.178 .. +0.848 | +5.3% | +0.400 | 0.29 |  | 11/16 |
| MNQ | 60 | h1 | -0.048 | -0.126 .. +0.030 | -9.0% | -0.001 | 0.25 |  | 11/16 |
| MNQ | 60 | h2 | -0.035 | -0.136 .. +0.065 | -4.6% | +0.007 | 0.5 |  | 8/16 |
| MNQ | 60 | h4 | -0.029 | -0.178 .. +0.121 | -2.6% | +0.007 | 0.71 |  | 10/16 |
| MNQ | 60 | h8 | +0.129 | -0.115 .. +0.373 | +8.1% | +0.070 | 0.3 |  | 8/16 |
| MNQ | 60 | h16 * | +0.177 | -0.076 .. +0.431 | +8.1% | +0.108 | 0.17 | 1 | 10/16 |
| MNQ | 60 | eod | +0.154 | -0.102 .. +0.409 | +6.7% | +0.106 | 0.24 |  | 10/16 |
| MYM | 5 | h1 * | +0.069 | +0.042 .. +0.097 | +13.0% | +0.120 | 6.9e-07 | 0.000173 | 7/8 |
| MYM | 5 | h2 | +0.075 | +0.037 .. +0.114 | +9.9% | +0.148 | 0.00013 |  | 7/8 |
| MYM | 5 | h4 | +0.089 | +0.025 .. +0.154 | +8.2% | +0.149 | 0.0067 |  | 7/8 |
| MYM | 5 | h8 | +0.075 | -0.008 .. +0.158 | +4.7% | +0.140 | 0.085 |  | 6/8 |
| MYM | 5 | h16 | +0.072 | -0.054 .. +0.199 | +3.1% | +0.150 | 0.31 |  | 6/8 |
| MYM | 5 | eod | +0.273 | -0.453 .. +1.000 | +2.3% | +0.788 | 0.73 |  | 4/8 |
| MYM | 15 | h1 * | +0.085 | +0.022 .. +0.148 | +16.1% | +0.145 | 0.0079 | 1 | 7/8 |
| MYM | 15 | h2 | +0.067 | -0.024 .. +0.158 | +8.7% | +0.110 | 0.15 |  | 5/8 |
| MYM | 15 | h4 | +0.050 | -0.067 .. +0.166 | +4.5% | +0.130 | 0.4 |  | 5/8 |
| MYM | 15 | h8 | -0.014 | -0.167 .. +0.140 | -0.8% | +0.050 | 0.98 |  | 5/8 |
| MYM | 15 | h16 | -0.028 | -0.263 .. +0.206 | -1.1% | +0.071 | 0.81 |  | 5/8 |
| MYM | 15 | eod | +0.328 | -0.387 .. +1.042 | +5.4% | +0.721 | 0.74 |  | 5/8 |
| MYM | 60 | h1 * | -0.044 | -0.132 .. +0.043 | -8.5% | -0.055 | 0.34 | 1 | 7/8 |
| MYM | 60 | h2 | +0.027 | -0.129 .. +0.182 | +3.5% | +0.002 | 0.96 |  | 2/8 |
| MYM | 60 | h4 | +0.032 | -0.206 .. +0.269 | +2.9% | +0.005 | 0.9 |  | 5/8 |
| MYM | 60 | h8 | -0.012 | -0.371 .. +0.347 | -0.8% | -0.007 | 0.95 |  | 5/8 |
| MYM | 60 | h16 | +0.076 | -0.314 .. +0.465 | +3.6% | +0.037 | 0.74 |  | 5/8 |
| MYM | 60 | eod | +0.037 | -0.348 .. +0.422 | +1.7% | +0.003 | 0.85 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.17 pts | -1.52 .. +1.17 | 0.8 |
| MES | 15 | +1.43 pts | -1.21 .. +4.06 | 0.48 |
| MES | 60 | +1.12 pts | -5.06 .. +7.30 | 0.72 |
| MNQ | 5 | +0.85 pts | -0.56 .. +2.26 | 0.29 |
| MNQ | 15 | -0.39 pts | -3.37 .. +2.59 | 0.83 |
| MNQ | 60 | +0.81 pts | -5.32 .. +6.94 | 0.8 |
| MYM | 5 | +0.80 pts | -1.42 .. +3.03 | 0.48 |
| MYM | 15 | -3.51 pts | -7.64 .. +0.62 | 0.12 |
| MYM | 60 | +3.97 pts | -5.27 .. +13.21 | 0.4 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 5009 | -0.003 | 0.337 | -0.32 | -3.82 | -3.59 | -4.05 | -3.70 |
| MES | 5 | h2 | event | with signal | 5009 | +0.012 | 0.337 | -0.18 | -3.68 | -3.45 | -3.93 | -3.52 |
| MES | 5 | h4 | event | with signal | 5009 | +0.026 | 0.337 | -0.02 | -3.52 | -3.21 | -3.85 | -3.35 |
| MES | 5 | h8 | event | with signal | 5009 | +0.076 | 0.337 | +0.31 | -3.19 | -3.00 | -3.39 | -3.03 |
| MES | 5 | h16 | event | with signal | 5009 | +0.043 | 0.337 | +0.27 | -3.23 | -3.33 | -3.13 | -3.06 |
| MES | 5 | eod | event | with signal | 5009 | +0.221 | 0.337 | +1.70 | -1.80 | -2.92 | -0.63 | -2.15 |
| MES | 15 | h1 | event | with signal | 1347 | +0.001 | 0.165 | +0.12 | -3.38 | -3.58 | -3.22 | -3.19 |
| MES | 15 | h2 | event | with signal | 1347 | +0.041 | 0.165 | +1.06 | -2.44 | -3.05 | -1.96 | -2.24 |
| MES | 15 | h4 | event | with signal | 1347 | +0.075 | 0.165 | +1.34 | -2.16 | -2.42 | -1.95 | -2.02 |
| MES | 15 | h8 | event | with signal | 1347 | +0.096 | 0.165 | +3.22 | -0.28 | -1.81 | +0.90 | -0.26 |
| MES | 15 | h16 | event | with signal | 1347 | +0.129 | 0.165 | +1.70 | -1.80 | -1.59 | -1.96 | -2.05 |
| MES | 15 | eod | event | with signal | 1347 | +0.501 | 0.165 | +7.15 | +3.65 | +0.81 | +5.85 | +1.68 |
| MES | 60 | h1 | event | with signal | 251 | +0.061 | 0.091 | +4.63 | +1.13 | -5.10 | +5.60 | +1.03 |
| MES | 60 | h2 | event | with signal | 251 | +0.094 | 0.091 | +3.51 | +0.01 | -4.73 | +3.41 | -0.08 |
| MES | 60 | h4 | event | with signal | 251 | +0.246 | 0.091 | +9.84 | +6.34 | -2.51 | +12.70 | +6.31 |
| MES | 60 | h8 | event | with signal | 251 | +0.250 | 0.091 | +14.05 | +10.55 | -0.33 | +18.38 | +10.51 |
| MES | 60 | h16 | event | with signal | 251 | +0.207 | 0.091 | +13.51 | +10.01 | -4.86 | +20.70 | +9.11 |
| MES | 60 | eod | event | with signal | 251 | +0.212 | 0.091 | +13.69 | +10.19 | -5.17 | +21.23 | +9.42 |
| MNQ | 5 | h1 | event | with signal | 4351 | +0.030 | 0.164 | +0.17 | -1.83 | -2.03 | -1.47 | -1.78 |
| MNQ | 5 | h2 | event | with signal | 4351 | +0.029 | 0.164 | +0.64 | -1.36 | -1.95 | -0.29 | -1.29 |
| MNQ | 5 | h4 | event | with signal | 4351 | +0.086 | 0.164 | +1.36 | -0.64 | -1.65 | +1.20 | -0.62 |
| MNQ | 5 | h8 | event | with signal | 4351 | +0.123 | 0.164 | +0.62 | -1.38 | -1.62 | -0.95 | -1.47 |
| MNQ | 5 | h16 | event | with signal | 4351 | +0.123 | 0.164 | +0.71 | -1.29 | -1.52 | -0.89 | -1.47 |
| MNQ | 5 | eod | event | with signal | 4351 | +0.357 | 0.164 | +0.40 | -1.60 | -0.89 | -2.89 | -2.63 |
| MNQ | 15 | h1 | event | with signal | 1074 | -0.002 | 0.086 | -0.35 | -2.35 | -2.13 | -2.69 | -2.30 |
| MNQ | 15 | h2 | event | with signal | 1074 | +0.074 | 0.086 | +0.39 | -1.61 | -1.42 | -1.91 | -1.57 |
| MNQ | 15 | h4 | event | with signal | 1074 | +0.173 | 0.086 | +1.86 | -0.14 | -1.11 | +1.37 | -0.16 |
| MNQ | 15 | h8 | event | with signal | 1074 | +0.092 | 0.086 | +1.49 | -0.51 | -1.58 | +1.17 | -0.74 |
| MNQ | 15 | h16 | event | with signal | 1074 | +0.171 | 0.086 | +4.16 | +2.16 | -1.31 | +7.58 | +1.71 |
| MNQ | 15 | eod | event | with signal | 1074 | +0.246 | 0.086 | +6.11 | +4.11 | +0.35 | +9.99 | +1.62 |
| MNQ | 60 | h1 | event | against signal | 219 | -0.001 | 0.039 | -3.92 | -5.92 | -1.00 | -11.26 | -5.60 |
| MNQ | 60 | h2 | event | with signal | 219 | +0.079 | 0.039 | +7.77 | +5.77 | -2.34 | +14.59 | +5.13 |
| MNQ | 60 | h4 | event | with signal | 219 | +0.084 | 0.039 | +7.70 | +5.70 | -3.82 | +16.04 | +4.56 |
| MNQ | 60 | h8 | event | against signal | 219 | -0.027 | 0.039 | -12.67 | -14.67 | +3.06 | -33.91 | -12.74 |
| MNQ | 60 | h16 | event | against signal | 219 | -0.025 | 0.039 | -13.48 | -15.48 | +3.38 | -35.95 | -11.80 |
| MNQ | 60 | eod | event | against signal | 219 | -0.019 | 0.039 | -14.26 | -16.26 | +3.39 | -37.60 | -12.45 |
| MYM | 5 | h1 | event | with signal | 2080 | +0.027 | 0.182 | +0.17 | -1.83 | +nan | -1.83 | -1.75 |
| MYM | 5 | h2 | event | with signal | 2080 | +0.057 | 0.182 | +0.28 | -1.72 | +nan | -1.72 | -1.64 |
| MYM | 5 | h4 | event | with signal | 2080 | +0.095 | 0.182 | +0.67 | -1.33 | +nan | -1.33 | -1.26 |
| MYM | 5 | h8 | event | with signal | 2080 | +0.070 | 0.182 | +0.30 | -1.70 | +nan | -1.70 | -1.66 |
| MYM | 5 | h16 | event | with signal | 2080 | +0.049 | 0.182 | +0.24 | -1.76 | +nan | -1.76 | -1.69 |
| MYM | 5 | eod | event | against signal | 2080 | +0.682 | 0.182 | +2.43 | +0.43 | +nan | +0.43 | +0.93 |
| MYM | 15 | h1 | event | against signal | 524 | +0.040 | 0.101 | +0.46 | -1.54 | +nan | -1.54 | -1.61 |
| MYM | 15 | h2 | event | against signal | 524 | +0.065 | 0.101 | +1.19 | -0.81 | +nan | -0.81 | -0.87 |
| MYM | 15 | h4 | event | against signal | 524 | +0.098 | 0.101 | +0.75 | -1.25 | +nan | -1.25 | -1.26 |
| MYM | 15 | h8 | event | against signal | 524 | +0.072 | 0.101 | +0.31 | -1.69 | +nan | -1.69 | -1.51 |
| MYM | 15 | h16 | event | against signal | 524 | +0.084 | 0.101 | +1.08 | -0.92 | +nan | -0.92 | -0.54 |
| MYM | 15 | eod | event | with signal | 524 | +0.099 | 0.101 | +6.23 | +4.23 | +nan | +4.23 | +3.67 |
| MYM | 60 | h1 | event | with signal | 98 | +0.061 | 0.051 | +1.82 | -0.18 | +nan | -0.18 | -0.09 |
| MYM | 60 | h2 | event | with signal | 98 | +0.044 | 0.051 | +1.82 | -0.18 | +nan | -0.18 | -0.08 |
| MYM | 60 | h4 | event | with signal | 98 | +0.240 | 0.051 | +8.94 | +6.94 | +nan | +6.94 | +7.10 |
| MYM | 60 | h8 | event | with signal | 98 | +0.210 | 0.051 | +10.07 | +8.07 | +nan | +8.07 | +8.28 |
| MYM | 60 | h16 | event | with signal | 98 | +0.246 | 0.051 | +6.35 | +4.35 | +nan | +4.35 | +3.75 |
| MYM | 60 | eod | event | with signal | 98 | +0.156 | 0.051 | +3.60 | +1.60 | +nan | +1.60 | +0.94 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.637 | -1.922 | -2.175 | -1.595 | -0.863 | +0.000 | -0.068 | -0.053 | -0.039 | +0.006 | -0.036 |
| MES | 15 | -1.817 | -2.071 | -2.330 | -1.747 | -0.950 | +0.000 | -0.027 | +0.009 | +0.038 | +0.058 | +0.057 |
| MES | 60 | -2.868 | -2.352 | -2.550 | -1.878 | -0.982 | +0.000 | +0.055 | +0.091 | +0.181 | -0.055 | -0.660 |
| MNQ | 5 | -1.919 | -2.177 | -2.454 | -1.789 | -0.957 | +0.000 | -0.006 | -0.008 | +0.048 | +0.085 | +0.087 |
| MNQ | 15 | -2.013 | -2.278 | -2.503 | -1.874 | -1.017 | +0.000 | -0.014 | +0.061 | +0.168 | +0.085 | +0.142 |
| MNQ | 60 | -3.220 | -2.627 | -2.887 | -2.088 | -1.102 | +0.000 | -0.007 | +0.078 | +0.078 | -0.494 | -0.251 |
| MYM | 5 | -1.768 | -2.115 | -2.413 | -1.733 | -0.917 | +0.000 | +0.008 | +0.038 | +0.075 | +0.055 | +0.037 |
| MYM | 15 | -1.980 | -2.283 | -2.550 | -1.882 | -1.015 | +0.000 | -0.046 | -0.074 | -0.116 | -0.095 | -0.101 |
| MYM | 60 | -2.984 | -2.319 | -2.605 | -1.945 | -1.077 | +0.000 | +0.063 | +0.056 | +0.217 | -0.165 | +0.377 |

## Calibration

- MES 5-min: 1036271 bars, 5009 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1347 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 251 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 4351 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1074 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 219 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 2080 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 524 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 98 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35312 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
