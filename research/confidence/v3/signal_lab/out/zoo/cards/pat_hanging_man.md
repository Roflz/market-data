# Impact card: pat_hanging_man

candle pattern hanging_man in its textbook direction: hammer shape after prior close > EMA10 -> bearish (textbook) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.070 R20 over the next 16 bars (80 min), p=0.78; we would catch an effect of 0.053 R20 or more 80% of the time).
- MES 5-min size: the market moves 5% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.035 R20, possible, q=0.111, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.95 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.279 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.318 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.122 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.55).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $7.81 at recent bar sizes, 90% range up to $4.05); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.181 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.220 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $9.03 at recent bar sizes, 90% range up to $19.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.045 R20 over the next 2 bars (10 min), p=0.11; we would catch an effect of 0.067 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 8% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.042 R20, CONFIRMED, q=0.000189, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.98 at recent bar sizes, 90% range up to $2.71); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.442 R20 over the rest of the session (to 16:45), p=0.97; we would catch an effect of 0.136 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $18.34 at recent bar sizes, 90% range up to $5.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.038 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.249 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.21 at recent bar sizes, 90% range up to $18.98); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.025 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.098 R20 or more 80% of the time).
- MYM 5-min size: the market moves 12% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.062 R20, CONFIRMED, q=0.00898, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.66 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.205 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.063 R20 over the next 1 bar (15 min), p=0.59; we would catch an effect of 0.189 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.21 at recent bar sizes, 90% range up to $5.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.176 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.328 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.87 at recent bar sizes, 90% range up to $18.50); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.022 .. +0.017 | -0.0003 | 0.82 / 0.83 / 0.8 | 0.799 |  |  | 8/16 | +0.012 | -0.017 |  | -0.2 / -0.2 |  |
| MES | 5 | h2 | +0.001 | -0.027 .. +0.029 | +0.0001 | 0.94 / 0.94 / 0.93 | 0.923 |  |  | 9/16 | +0.020 | -0.017 |  | +0.1 / +0.1 |  |
| MES | 5 | h4 | -0.009 | -0.048 .. +0.030 | -0.0005 | 0.64 / 0.64 / 0.63 | 0.633 |  |  | 8/16 | +0.018 | -0.037 |  | -0.5 / -0.5 | 0.053 |
| MES | 5 | h8 | -0.021 | -0.082 .. +0.040 | -0.0008 | 0.5 / 0.5 / 0.47 | 0.466 |  |  | 7/16 | +0.025 | -0.067 |  | -0.8 / -0.7 |  |
| MES | 5 | h16 * | -0.070 | -0.160 .. +0.020 | -0.0018 | 0.13 / 0.13 / 0.11 | 0.104 | 1 | 1 | 10/16 | -0.040 | -0.100 | False | -1.8 / -1.5 |  |
| MES | 5 | eod | -0.102 | -0.729 .. +0.525 | -0.0005 | 0.75 / 0.76 / 0.67 | 0.662 |  |  | 8/16 | +0.276 | -0.478 |  | -0.5 / -0.3 |  |
| MES | 15 | h1 | +0.016 | -0.025 .. +0.058 | +0.0015 | 0.44 / 0.42 / 0.43 | 0.409 |  |  | 10/16 | -0.009 | +0.042 |  | +0.8 / +0.8 |  |
| MES | 15 | h2 | -0.030 | -0.093 .. +0.034 | -0.0019 | 0.36 / 0.35 / 0.34 | 0.324 |  |  | 9/16 | -0.060 | +0.001 |  | -1.0 / -0.9 |  |
| MES | 15 | h4 | -0.039 | -0.132 .. +0.055 | -0.0016 | 0.42 / 0.4 / 0.4 | 0.374 |  |  | 11/16 | -0.031 | -0.046 |  | -0.9 / -0.8 | 0.122 |
| MES | 15 | h8 | +0.036 | -0.118 .. +0.190 | +0.0011 | 0.65 / 0.63 / 0.58 | 0.563 |  |  | 8/16 | +0.064 | +0.008 |  | +0.5 / +0.5 |  |
| MES | 15 | h16 | +0.102 | -0.125 .. +0.328 | +0.0021 | 0.38 / 0.37 / 0.25 | 0.245 |  |  | 8/16 | +0.211 | -0.007 |  | +1.1 / +0.9 |  |
| MES | 15 | eod * | -0.318 | -0.781 .. +0.146 | -0.0026 | 0.18 / 0.19 / 0.17 | 0.17 | 1 | 1 | 8/16 | -0.123 | -0.511 | False | -1.5 / -1.3 |  |
| MES | 60 | h1 | +0.033 | -0.050 .. +0.116 | +0.0035 | 0.44 / 0.44 / 0.41 | 0.404 |  |  | 8/16 | +0.065 | +0.001 |  | +0.8 / +0.8 |  |
| MES | 60 | h2 | -0.003 | -0.117 .. +0.110 | -0.0002 | 0.96 / 0.96 / 0.95 | 0.956 |  |  | 10/16 | +0.055 | -0.061 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | -0.007 | -0.153 .. +0.140 | -0.0003 | 0.93 / 0.93 / 0.93 | 0.923 |  |  | 8/16 | +0.059 | -0.072 |  | -0.1 / -0.1 | 0.220 |
| MES | 60 | h8 * | -0.181 | -0.397 .. +0.034 | -0.0069 | 0.098 / 0.1 / 0.082 | 0.0857 | 1 | 1 | 9/16 | +0.099 | -0.462 | False | -1.7 / -1.7 |  |
| MES | 60 | h16 | -0.180 | -0.429 .. +0.068 | -0.0053 | 0.16 / 0.16 / 0.12 | 0.115 |  |  | 9/16 | +0.167 | -0.527 |  | -1.5 / -1.4 |  |
| MES | 60 | eod | -0.173 | -0.425 .. +0.079 | -0.0048 | 0.18 / 0.18 / 0.13 | 0.132 |  |  | 9/16 | +0.167 | -0.514 |  | -1.5 / -1.3 |  |
| MNQ | 5 | h1 | +0.015 | -0.010 .. +0.039 | +0.0013 | 0.23 / 0.23 / 0.23 | 0.187 |  |  | 9/16 | +0.029 | +0.000 |  | +1.2 / +1.2 |  |
| MNQ | 5 | h2 * | +0.045 | +0.008 .. +0.082 | +0.0024 | 0.017 / 0.018 / 0.01 | 0.0151 | 1 | 0.972 | 10/16 | +0.073 | +0.018 | False | +2.4 / +2.4 |  |
| MNQ | 5 | h4 | +0.045 | -0.017 .. +0.107 | +0.0016 | 0.16 / 0.16 / 0.11 | 0.0729 |  |  | 11/16 | +0.066 | +0.024 |  | +1.6 / +1.4 | 0.067 |
| MNQ | 5 | h8 | +0.042 | -0.055 .. +0.140 | +0.0010 | 0.39 / 0.38 / 0.31 | 0.261 |  |  | 10/16 | +0.040 | +0.045 |  | +1.0 / +0.9 |  |
| MNQ | 5 | h16 | -0.019 | -0.153 .. +0.116 | -0.0003 | 0.79 / 0.78 / 0.77 | 0.751 |  |  | 11/16 | -0.029 | -0.008 |  | -0.3 / -0.3 |  |
| MNQ | 5 | eod | -0.717 | -1.668 .. +0.234 | -0.0025 | 0.14 / 0.15 / 0.04 | 0.0422 |  |  | 12/16 | -0.886 | -0.549 |  | -2.3 / -1.5 |  |
| MNQ | 15 | h1 | +0.024 | -0.016 .. +0.063 | +0.0017 | 0.24 / 0.24 / 0.4 | 0.31 |  |  | 10/16 | +0.036 | +0.011 |  | +1.1 / +1.2 |  |
| MNQ | 15 | h2 | +0.026 | -0.034 .. +0.087 | +0.0012 | 0.39 / 0.39 / 0.58 | 0.446 |  |  | 9/16 | +0.046 | +0.007 |  | +0.9 / +0.9 |  |
| MNQ | 15 | h4 | +0.055 | -0.041 .. +0.150 | +0.0014 | 0.26 / 0.25 / 0.49 | 0.306 |  |  | 9/16 | +0.094 | +0.015 |  | +1.2 / +1.1 | 0.136 |
| MNQ | 15 | h8 | +0.013 | -0.121 .. +0.146 | +0.0003 | 0.85 / 0.85 / 0.89 | 0.872 |  |  | 7/16 | +0.078 | -0.052 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h16 | +0.009 | -0.203 .. +0.221 | +0.0001 | 0.94 / 0.94 / 0.95 | 0.946 |  |  | 8/16 | +0.222 | -0.204 |  | +0.1 / +0.1 |  |
| MNQ | 15 | eod * | -0.442 | -0.998 .. +0.115 | -0.0025 | 0.12 / 0.12 / 0.18 | 0.163 | 1 | 1 | 11/16 | -0.093 | -0.788 | False | -1.8 / -1.6 |  |
| MNQ | 60 | h1 * | +0.038 | -0.048 .. +0.125 | +0.0037 | 0.39 / 0.39 / 0.38 | 0.378 | 1 | 1 | 8/16 | +0.043 | +0.033 | False | +0.9 / +0.9 |  |
| MNQ | 60 | h2 | +0.017 | -0.093 .. +0.128 | +0.0012 | 0.76 / 0.76 / 0.78 | 0.775 |  |  | 7/16 | +0.071 | -0.036 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h4 | +0.042 | -0.138 .. +0.222 | +0.0020 | 0.65 / 0.64 / 0.63 | 0.633 |  |  | 9/16 | +0.057 | +0.027 |  | +0.5 / +0.5 | 0.249 |
| MNQ | 60 | h8 | -0.023 | -0.265 .. +0.220 | -0.0008 | 0.85 / 0.85 / 0.85 | 0.853 |  |  | 9/16 | +0.060 | -0.105 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h16 | +0.054 | -0.207 .. +0.315 | +0.0015 | 0.68 / 0.69 / 0.69 | 0.686 |  |  | 7/16 | +0.166 | -0.058 |  | +0.4 / +0.4 |  |
| MNQ | 60 | eod | +0.061 | -0.199 .. +0.322 | +0.0016 | 0.64 / 0.65 / 0.65 | 0.652 |  |  | 9/16 | +0.179 | -0.056 |  | +0.5 / +0.5 |  |
| MYM | 5 | h1 * | -0.025 | -0.061 .. +0.012 | -0.0018 | 0.18 / 0.18 / 0.26 | 0.162 | 1 | 1 | 7/8 | n/a | -0.025 | False | -1.3 / -1.3 |  |
| MYM | 5 | h2 | -0.023 | -0.072 .. +0.025 | -0.0010 | 0.34 / 0.35 / 0.46 | 0.369 |  |  | 6/8 | n/a | -0.023 |  | -0.9 / -0.9 |  |
| MYM | 5 | h4 | -0.016 | -0.090 .. +0.057 | -0.0005 | 0.66 / 0.66 / 0.78 | 0.685 |  |  | 3/8 | n/a | -0.016 |  | -0.4 / -0.4 | 0.098 |
| MYM | 5 | h8 | +0.016 | -0.096 .. +0.129 | +0.0003 | 0.78 / 0.77 / 0.82 | 0.774 |  |  | 6/8 | n/a | +0.016 |  | +0.3 / +0.3 |  |
| MYM | 5 | h16 | -0.082 | -0.248 .. +0.083 | -0.0013 | 0.33 / 0.34 / 0.39 | 0.346 |  |  | 6/8 | n/a | -0.082 |  | -1.1 / -1.0 |  |
| MYM | 5 | eod | -0.160 | -1.300 .. +0.980 | -0.0005 | 0.78 / 0.78 / 0.73 | 0.726 |  |  | 5/8 | n/a | -0.160 |  | -0.4 / -0.3 |  |
| MYM | 15 | h1 * | +0.063 | +0.003 .. +0.123 | +0.0045 | 0.04 / 0.039 / 0.09 | 0.0638 | 1 | 0.998 | 6/8 | n/a | +0.063 | False | +2.0 / +2.1 |  |
| MYM | 15 | h2 | +0.082 | -0.009 .. +0.174 | +0.0034 | 0.078 / 0.078 / 0.18 | 0.101 |  |  | 6/8 | n/a | +0.082 |  | +1.7 / +1.8 |  |
| MYM | 15 | h4 | -0.005 | -0.144 .. +0.133 | -0.0001 | 0.94 / 0.94 / 0.96 | 0.932 |  |  | 5/8 | n/a | -0.005 |  | -0.1 / -0.1 | 0.189 |
| MYM | 15 | h8 | +0.096 | -0.109 .. +0.301 | +0.0018 | 0.36 / 0.36 / 0.46 | 0.364 |  |  | 3/8 | n/a | +0.096 |  | +1.0 / +0.9 |  |
| MYM | 15 | h16 | +0.074 | -0.204 .. +0.351 | +0.0010 | 0.6 / 0.6 / 0.73 | 0.657 |  |  | 5/8 | n/a | +0.074 |  | +0.5 / +0.5 |  |
| MYM | 15 | eod | +0.002 | -0.773 .. +0.777 | +0.0000 | 1 / 1 / 1 | 0.992 |  |  | 3/8 | n/a | +0.002 |  | +0.0 / +0.0 |  |
| MYM | 60 | h1 | -0.003 | -0.115 .. +0.108 | -0.0003 | 0.95 / 0.95 / 0.95 | 0.957 |  |  | 5/8 | n/a | -0.003 |  | -0.1 / -0.1 |  |
| MYM | 60 | h2 | +0.032 | -0.135 .. +0.198 | +0.0022 | 0.71 / 0.71 / 0.71 | 0.702 |  |  | 3/8 | n/a | +0.032 |  | +0.4 / +0.4 |  |
| MYM | 60 | h4 | +0.038 | -0.202 .. +0.279 | +0.0019 | 0.76 / 0.75 / 0.74 | 0.736 |  |  | 3/8 | n/a | +0.038 |  | +0.3 / +0.3 | 0.328 |
| MYM | 60 | h8 | -0.056 | -0.409 .. +0.298 | -0.0020 | 0.76 / 0.75 / 0.72 | 0.733 |  |  | 4/8 | n/a | -0.056 |  | -0.3 / -0.3 |  |
| MYM | 60 | h16 | -0.158 | -0.557 .. +0.240 | -0.0043 | 0.44 / 0.42 / 0.36 | 0.37 |  |  | 5/8 | n/a | -0.158 |  | -0.9 / -0.8 |  |
| MYM | 60 | eod * | -0.176 | -0.570 .. +0.219 | -0.0046 | 0.38 / 0.36 / 0.31 | 0.319 | 1 | 1 | 5/8 | n/a | -0.176 | False | -1.0 / -0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.022 | +0.007 .. +0.037 | +4.4% | +0.044 | 0.0048 |  | 10/16 |
| MES | 5 | h2 * | +0.035 | +0.015 .. +0.054 | +4.9% | +0.055 | 0.00063 | 0.111 | 13/16 |
| MES | 5 | h4 | +0.023 | -0.005 .. +0.050 | +2.3% | +0.067 | 0.11 |  | 8/16 |
| MES | 5 | h8 | +0.013 | -0.028 .. +0.053 | +0.9% | +0.064 | 0.54 |  | 9/16 |
| MES | 5 | h16 | +0.015 | -0.044 .. +0.074 | +0.7% | +0.057 | 0.62 |  | 11/16 |
| MES | 5 | eod | +0.010 | -0.343 .. +0.363 | +0.1% | +0.208 | 0.96 |  | 8/16 |
| MES | 15 | h1 | +0.010 | -0.020 .. +0.040 | +1.9% | +0.040 | 0.75 |  | 8/16 |
| MES | 15 | h2 | +0.038 | -0.005 .. +0.081 | +5.2% | +0.066 | 0.1 |  | 11/16 |
| MES | 15 | h4 | +0.050 | -0.011 .. +0.111 | +4.7% | +0.102 | 0.23 |  | 10/16 |
| MES | 15 | h8 * | +0.094 | -0.015 .. +0.203 | +6.1% | +0.147 | 0.091 | 1 | 11/16 |
| MES | 15 | h16 | +0.121 | -0.032 .. +0.274 | +5.3% | +0.160 | 0.12 |  | 9/16 |
| MES | 15 | eod | -0.083 | -0.379 .. +0.213 | -1.5% | +0.059 | 0.77 |  | 9/16 |
| MES | 60 | h1 | +0.012 | -0.051 .. +0.075 | +2.4% | +0.039 | 0.71 |  | 8/16 |
| MES | 60 | h2 | +0.021 | -0.066 .. +0.108 | +2.9% | +0.055 | 0.63 |  | 7/16 |
| MES | 60 | h4 * | +0.029 | -0.084 .. +0.142 | +2.7% | +0.062 | 0.63 | 1 | 7/16 |
| MES | 60 | h8 | +0.011 | -0.123 .. +0.145 | +0.7% | +0.035 | 0.97 |  | 7/16 |
| MES | 60 | h16 | +0.026 | -0.123 .. +0.175 | +1.3% | +0.027 | 0.78 |  | 8/16 |
| MES | 60 | eod | +0.023 | -0.128 .. +0.173 | +1.0% | +0.023 | 0.78 |  | 8/16 |
| MNQ | 5 | h1 * | +0.042 | +0.026 .. +0.059 | +7.9% | +0.066 | 7.5e-07 | 0.000189 | 15/16 |
| MNQ | 5 | h2 | +0.053 | +0.027 .. +0.078 | +6.9% | +0.094 | 0.00011 |  | 14/16 |
| MNQ | 5 | h4 | +0.081 | +0.035 .. +0.126 | +7.3% | +0.134 | 0.00063 |  | 12/16 |
| MNQ | 5 | h8 | +0.080 | +0.015 .. +0.144 | +4.9% | +0.136 | 0.019 |  | 11/16 |
| MNQ | 5 | h16 | +0.046 | -0.036 .. +0.128 | +1.9% | +0.137 | 0.36 |  | 11/16 |
| MNQ | 5 | eod | +0.346 | -0.162 .. +0.854 | +2.8% | +0.992 | 0.4 |  | 10/16 |
| MNQ | 15 | h1 | +0.002 | -0.025 .. +0.029 | +0.4% | +0.046 | 0.99 |  | 6/16 |
| MNQ | 15 | h2 | -0.026 | -0.069 .. +0.016 | -3.4% | +0.033 | 0.34 |  | 11/16 |
| MNQ | 15 | h4 * | -0.054 | -0.115 .. +0.008 | -4.7% | -0.002 | 0.3 | 1 | 12/16 |
| MNQ | 15 | h8 | -0.068 | -0.161 .. +0.024 | -4.1% | -0.063 | 0.37 |  | 10/16 |
| MNQ | 15 | h16 | -0.002 | -0.136 .. +0.132 | -0.1% | -0.053 | 0.98 |  | 7/16 |
| MNQ | 15 | eod | -0.146 | -0.519 .. +0.227 | -2.3% | -0.092 | 0.48 |  | 8/16 |
| MNQ | 60 | h1 | -0.005 | -0.065 .. +0.055 | -0.9% | +0.000 | 0.88 |  | 5/16 |
| MNQ | 60 | h2 | -0.031 | -0.108 .. +0.046 | -4.1% | -0.004 | 0.48 |  | 9/16 |
| MNQ | 60 | h4 * | +0.071 | -0.049 .. +0.191 | +6.4% | +0.030 | 0.25 | 1 | 10/16 |
| MNQ | 60 | h8 | +0.059 | -0.100 .. +0.218 | +3.7% | +0.033 | 0.55 |  | 11/16 |
| MNQ | 60 | h16 | +0.036 | -0.123 .. +0.196 | +1.6% | +0.005 | 0.86 |  | 12/16 |
| MNQ | 60 | eod | +0.030 | -0.128 .. +0.189 | +1.3% | -0.003 | 0.9 |  | 12/16 |
| MYM | 5 | h1 * | +0.062 | +0.032 .. +0.091 | +11.6% | +0.074 | 4.1e-05 | 0.00898 | 8/8 |
| MYM | 5 | h2 | +0.056 | +0.019 .. +0.094 | +7.4% | +0.088 | 0.0034 |  | 7/8 |
| MYM | 5 | h4 | +0.060 | +0.005 .. +0.115 | +5.5% | +0.139 | 0.032 |  | 6/8 |
| MYM | 5 | h8 | +0.098 | +0.009 .. +0.186 | +6.1% | +0.207 | 0.03 |  | 6/8 |
| MYM | 5 | h16 | +0.067 | -0.045 .. +0.180 | +2.9% | +0.150 | 0.25 |  | 6/8 |
| MYM | 5 | eod | -0.104 | -0.684 .. +0.476 | -0.9% | +0.058 | 0.73 |  | 3/8 |
| MYM | 15 | h1 | +0.008 | -0.032 .. +0.048 | +1.5% | +0.053 | 0.92 |  | 5/8 |
| MYM | 15 | h2 | +0.037 | -0.026 .. +0.101 | +4.9% | +0.077 | 0.65 |  | 5/8 |
| MYM | 15 | h4 | +0.039 | -0.055 .. +0.132 | +3.5% | +0.059 | 0.55 |  | 3/8 |
| MYM | 15 | h8 | +0.052 | -0.097 .. +0.201 | +3.1% | +0.038 | 0.51 |  | 5/8 |
| MYM | 15 | h16 | -0.092 | -0.276 .. +0.092 | -3.7% | -0.072 | 0.33 |  | 6/8 |
| MYM | 15 | eod * | -0.414 | -0.906 .. +0.078 | -6.9% | -0.018 | 0.25 | 1 | 7/8 |
| MYM | 60 | h1 * | -0.025 | -0.102 .. +0.052 | -4.7% | -0.004 | 0.53 | 1 | 4/8 |
| MYM | 60 | h2 | +0.020 | -0.093 .. +0.132 | +2.6% | -0.009 | 0.91 |  | 3/8 |
| MYM | 60 | h4 | -0.017 | -0.183 .. +0.148 | -1.6% | -0.000 | 0.84 |  | 5/8 |
| MYM | 60 | h8 | +0.055 | -0.153 .. +0.262 | +3.6% | +0.081 | 0.87 |  | 4/8 |
| MYM | 60 | h16 | +0.048 | -0.164 .. +0.260 | +2.3% | +0.006 | 0.82 |  | 5/8 |
| MYM | 60 | eod | +0.018 | -0.192 .. +0.228 | +0.8% | -0.005 | 0.97 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.71 pts | -0.51 .. +1.93 | 0.32 |
| MES | 15 | -0.31 pts | -2.52 .. +1.89 | 0.78 |
| MES | 60 | +0.42 pts | -3.53 .. +4.36 | 0.84 |
| MNQ | 5 | +0.09 pts | -1.17 .. +1.36 | 0.98 |
| MNQ | 15 | +2.91 pts | +0.93 .. +4.89 | 0.0075 |
| MNQ | 60 | -2.90 pts | -6.76 .. +0.96 | 0.27 |
| MYM | 5 | -0.51 pts | -2.49 .. +1.47 | 0.62 |
| MYM | 15 | +3.19 pts | +0.08 .. +6.31 | 0.068 |
| MYM | 60 | -2.89 pts | -8.11 .. +2.33 | 0.54 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 6523 | +0.005 | 0.457 | +0.08 | -3.42 | -3.52 | -3.27 | -3.43 |
| MES | 5 | h2 | event | with signal | 6523 | -0.007 | 0.457 | -0.24 | -3.74 | -3.51 | -4.06 | -3.70 |
| MES | 5 | h4 | event | against signal | 6523 | +0.026 | 0.457 | +0.37 | -3.13 | -3.48 | -2.64 | -3.20 |
| MES | 5 | h8 | event | against signal | 6523 | +0.052 | 0.457 | +0.54 | -2.96 | -3.38 | -2.36 | -3.11 |
| MES | 5 | h16 | event | against signal | 6523 | +0.130 | 0.457 | +1.31 | -2.19 | -3.01 | -1.04 | -2.47 |
| MES | 5 | eod | event | against signal | 6523 | +0.916 | 0.457 | +4.82 | +1.32 | -0.42 | +3.78 | -1.60 |
| MES | 15 | h1 | event | with signal | 1823 | +0.008 | 0.223 | +0.01 | -3.49 | -3.65 | -3.30 | -3.42 |
| MES | 15 | h2 | event | against signal | 1823 | +0.045 | 0.223 | +0.83 | -2.67 | -2.92 | -2.39 | -2.81 |
| MES | 15 | h4 | event | against signal | 1823 | +0.066 | 0.223 | +0.61 | -2.89 | -2.83 | -2.96 | -3.12 |
| MES | 15 | h8 | event | with signal | 1823 | -0.019 | 0.223 | -0.60 | -4.10 | -3.94 | -4.27 | -3.60 |
| MES | 15 | h16 | event | with signal | 1823 | -0.008 | 0.223 | -1.64 | -5.14 | -3.86 | -6.55 | -4.22 |
| MES | 15 | eod | event | against signal | 1823 | +0.683 | 0.223 | +8.21 | +4.71 | -0.60 | +10.57 | +2.32 |
| MES | 60 | h1 | event | with signal | 559 | +0.021 | 0.098 | -1.66 | -5.16 | -2.57 | -7.21 | -4.93 |
| MES | 60 | h2 | event | against signal | 559 | +0.030 | 0.098 | +2.60 | -0.90 | -3.45 | +1.10 | -1.55 |
| MES | 60 | h4 | event | against signal | 559 | +0.054 | 0.098 | +4.30 | +0.80 | -2.67 | +3.52 | -0.30 |
| MES | 60 | h8 | event | against signal | 559 | +0.261 | 0.098 | +13.61 | +10.11 | -2.73 | +20.20 | +8.35 |
| MES | 60 | h16 | event | against signal | 559 | +0.279 | 0.098 | +16.29 | +12.79 | -4.00 | +25.98 | +11.06 |
| MES | 60 | eod | event | against signal | 559 | +0.271 | 0.098 | +16.08 | +12.58 | -3.93 | +25.57 | +11.01 |
| MNQ | 5 | h1 | event | with signal | 5929 | +0.009 | 0.200 | +0.08 | -1.92 | -1.99 | -1.79 | -1.90 |
| MNQ | 5 | h2 | event | with signal | 5929 | +0.032 | 0.200 | -0.06 | -2.06 | -1.95 | -2.24 | -2.00 |
| MNQ | 5 | h4 | event | with signal | 5929 | +0.021 | 0.200 | -0.29 | -2.29 | -1.90 | -2.95 | -2.21 |
| MNQ | 5 | h8 | event | with signal | 5929 | -0.002 | 0.200 | -0.47 | -2.47 | -2.11 | -3.07 | -2.32 |
| MNQ | 5 | h16 | event | against signal | 5929 | +0.104 | 0.200 | +1.43 | -0.57 | -1.36 | +0.78 | -0.89 |
| MNQ | 5 | eod | event | against signal | 5929 | +1.867 | 0.200 | +6.77 | +4.77 | +2.79 | +8.19 | +1.68 |
| MNQ | 15 | h1 | event | with signal | 1861 | +0.013 | 0.096 | -0.32 | -2.32 | -1.89 | -2.93 | -2.21 |
| MNQ | 15 | h2 | event | with signal | 1861 | +0.010 | 0.096 | -0.20 | -2.20 | -1.86 | -2.69 | -2.07 |
| MNQ | 15 | h4 | event | with signal | 1861 | +0.022 | 0.096 | +1.69 | -0.31 | -1.74 | +1.73 | +0.04 |
| MNQ | 15 | h8 | event | with signal | 1861 | -0.054 | 0.096 | -0.37 | -2.37 | -2.41 | -2.32 | -1.60 |
| MNQ | 15 | h16 | event | with signal | 1861 | -0.109 | 0.096 | -3.85 | -5.85 | -2.39 | -10.81 | -4.89 |
| MNQ | 15 | eod | event | against signal | 1861 | +0.898 | 0.096 | +12.76 | +10.76 | +0.00 | +26.15 | +8.65 |
| MNQ | 60 | h1 | event | with signal | 537 | +0.027 | 0.039 | +0.63 | -1.37 | -1.56 | -1.20 | -1.16 |
| MNQ | 60 | h2 | event | with signal | 537 | -0.010 | 0.039 | -1.20 | -3.20 | -1.53 | -4.76 | -2.38 |
| MNQ | 60 | h4 | event | with signal | 537 | -0.011 | 0.039 | -1.58 | -3.58 | -3.07 | -4.06 | -2.08 |
| MNQ | 60 | h8 | event | against signal | 537 | +0.117 | 0.039 | +5.58 | +3.58 | +0.24 | +6.70 | +0.94 |
| MNQ | 60 | h16 | event | with signal | 537 | -0.076 | 0.039 | -0.26 | -2.26 | -2.96 | -1.60 | +0.42 |
| MNQ | 60 | eod | event | with signal | 537 | -0.072 | 0.039 | +0.12 | -1.88 | -2.78 | -1.04 | +0.54 |
| MYM | 5 | h1 | event | against signal | 2500 | +0.023 | 0.205 | +0.22 | -1.78 | +nan | -1.78 | -1.77 |
| MYM | 5 | h2 | event | against signal | 2500 | +0.023 | 0.205 | +0.10 | -1.90 | +nan | -1.90 | -1.92 |
| MYM | 5 | h4 | event | against signal | 2500 | +0.016 | 0.205 | -0.28 | -2.28 | +nan | -2.28 | -2.32 |
| MYM | 5 | h8 | event | with signal | 2500 | +0.014 | 0.205 | +0.57 | -1.43 | +nan | -1.43 | -1.31 |
| MYM | 5 | h16 | event | against signal | 2500 | +0.094 | 0.205 | +0.94 | -1.06 | +nan | -1.06 | -1.31 |
| MYM | 5 | eod | event | against signal | 2500 | +0.526 | 0.205 | +3.55 | +1.55 | +nan | +1.55 | -0.52 |
| MYM | 15 | h1 | event | with signal | 825 | +0.062 | 0.104 | +0.39 | -1.61 | +nan | -1.61 | -1.59 |
| MYM | 15 | h2 | event | with signal | 825 | +0.082 | 0.104 | +0.47 | -1.53 | +nan | -1.53 | -1.48 |
| MYM | 15 | h4 | event | against signal | 825 | +0.004 | 0.104 | +0.66 | -1.34 | +nan | -1.34 | -1.41 |
| MYM | 15 | h8 | event | with signal | 825 | +0.086 | 0.104 | -0.23 | -2.23 | +nan | -2.23 | -1.98 |
| MYM | 15 | h16 | event | with signal | 825 | +0.091 | 0.104 | -1.30 | -3.30 | +nan | -3.30 | -3.50 |
| MYM | 15 | eod | event | with signal | 825 | -0.102 | 0.104 | -4.62 | -6.62 | +nan | -6.62 | -6.96 |
| MYM | 60 | h1 | event | against signal | 261 | +0.010 | 0.051 | +2.64 | +0.64 | +nan | +0.64 | +0.53 |
| MYM | 60 | h2 | event | with signal | 261 | +0.016 | 0.051 | -0.37 | -2.37 | +nan | -2.37 | -1.93 |
| MYM | 60 | h4 | event | with signal | 261 | +0.012 | 0.051 | -0.57 | -2.57 | +nan | -2.57 | -1.73 |
| MYM | 60 | h8 | event | against signal | 261 | +0.103 | 0.051 | +8.25 | +6.25 | +nan | +6.25 | +4.66 |
| MYM | 60 | h16 | event | against signal | 261 | +0.223 | 0.051 | +12.44 | +10.44 | +nan | +10.44 | +8.29 |
| MYM | 60 | eod | event | against signal | 261 | +0.240 | 0.051 | +12.73 | +10.73 | +nan | +10.73 | +8.48 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.581 | +0.663 | +0.520 | +0.249 | -0.024 | +0.000 | +0.066 | +0.068 | +0.056 | +0.042 | -0.012 |
| MES | 15 | +0.614 | +0.628 | +0.472 | +0.213 | -0.048 | +0.000 | +0.048 | +0.001 | -0.009 | +0.042 | +0.063 |
| MES | 60 | +0.553 | +0.625 | +0.483 | +0.115 | -0.089 | +0.000 | +0.045 | +0.016 | +0.023 | -0.105 | -0.246 |
| MNQ | 5 | +0.653 | +0.749 | +0.537 | +0.209 | -0.085 | +0.000 | +0.053 | +0.082 | +0.083 | +0.081 | +0.019 |
| MNQ | 15 | +0.581 | +0.631 | +0.430 | +0.174 | -0.089 | +0.000 | +0.037 | +0.039 | +0.074 | +0.019 | -0.005 |
| MNQ | 60 | +0.396 | +0.508 | +0.369 | +0.106 | -0.091 | +0.000 | +0.043 | +0.030 | +0.073 | +0.033 | -1.777 |
| MYM | 5 | +0.626 | +0.679 | +0.516 | +0.206 | -0.083 | +0.000 | -0.007 | -0.006 | +0.000 | +0.027 | -0.069 |
| MYM | 15 | +0.589 | +0.610 | +0.473 | +0.202 | -0.068 | +0.000 | +0.066 | +0.084 | -0.002 | +0.096 | +0.048 |
| MYM | 60 | +0.793 | +0.702 | +0.598 | +0.231 | -0.085 | +0.000 | -0.003 | +0.035 | -0.009 | -0.072 | +1.121 |

## Calibration

- MES 5-min: 1036271 bars, 6523 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1823 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 559 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 5929 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1861 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 537 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 2500 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 825 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 40426 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
