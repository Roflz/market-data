# Impact card: dist_sess_hi

(session high so far - close) in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.011 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.019 R20, CONFIRMED, q=2.34e-16, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.35 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.214 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.011 R20 over the next 2 bars (30 min), p=0.82; we would catch an effect of 0.042 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.036 R20, CONFIRMED, q=9.34e-16, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.17 at recent bar sizes, 90% range up to $1.11); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.080 R20 or more 80% of the time).
- MES 60-min size: the market moves 16% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.084 R20, CONFIRMED, q=1.15e-21, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.08 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.062 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (5 min), p=0.024; we would catch an effect of 0.029 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.020 R20, CONFIRMED, q=3.24e-05, 12 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.10 at recent bar sizes, 90% range up to $0.87); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (15 min), p=0.49; we would catch an effect of 0.056 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 8% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.041 R20, CONFIRMED, q=3.22e-07, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.30 at recent bar sizes, 90% range up to $2.44); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.017 R20 over the next 1 bar (1 h), p=0.5; we would catch an effect of 0.084 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 14% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.077 R20, CONFIRMED, q=1.54e-17, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.80 at recent bar sizes, 90% range up to $6.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.015 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.047 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.021 R20, possible, q=0.0823, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.64 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.165 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.022 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.088 R20 or more 80% of the time).
- MYM 15-min size: the market moves 8% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.043 R20, CONFIRMED, q=0.00987, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.24 at recent bar sizes, 90% range up to $2.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.022 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.115 R20 or more 80% of the time).
- MYM 60-min size: the market moves 15% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.079 R20, CONFIRMED, q=1.16e-08, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.46 at recent bar sizes, 90% range up to $3.55); about 5.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.003 .. +0.005 | +0.0014 | 0.57 / 0.59 / 0.64 | 0.643 |  |  | 9/16 | +0.003 | -0.001 |  | +0.5 / +0.6 |  |
| MES | 5 | h2 | -0.003 | -0.011 .. +0.004 | -0.0011 | 0.39 / 0.41 / 0.38 | 0.391 |  |  | 9/16 | +0.005 | -0.012 |  | -1.0 / -0.9 |  |
| MES | 5 | h4 * | -0.011 | -0.027 .. +0.005 | -0.0040 | 0.2 / 0.2 / 0.18 | 0.175 | 1 | 1 | 10/16 | +0.007 | -0.028 | False | -2.1 / -1.3 | 0.023 |
| MES | 5 | h8 | -0.008 | -0.040 .. +0.023 | -0.0037 | 0.6 / 0.61 / 0.59 | 0.599 |  |  | 7/16 | +0.029 | -0.045 |  | -1.1 / -0.5 |  |
| MES | 5 | h16 | +0.004 | -0.058 .. +0.065 | -0.0045 | 0.91 / 0.91 / 0.92 | 0.911 |  |  | 8/16 | +0.076 | -0.068 |  | +0.4 / +0.1 |  |
| MES | 5 | eod | -0.351 | -1.164 .. +0.461 | -0.0221 | 0.4 / 0.38 / 0.28 | 0.278 |  |  | 9/16 | -0.045 | -0.656 |  | -7.1 / -0.8 |  |
| MES | 15 | h1 | -0.005 | -0.014 .. +0.004 | -0.0007 | 0.26 / 0.26 / 0.23 | 0.237 |  |  | 7/16 | +0.001 | -0.011 |  | -1.1 / -1.1 |  |
| MES | 15 | h2 * | -0.011 | -0.025 .. +0.003 | -0.0054 | 0.11 / 0.12 / 0.14 | 0.134 | 1 | 1 | 9/16 | +0.005 | -0.028 | False | -1.6 / -1.6 |  |
| MES | 15 | h4 | -0.017 | -0.046 .. +0.012 | -0.0074 | 0.25 / 0.26 / 0.26 | 0.257 |  |  | 9/16 | +0.018 | -0.052 |  | -1.6 / -1.1 | 0.042 |
| MES | 15 | h8 | -0.028 | -0.085 .. +0.030 | -0.0092 | 0.34 / 0.35 / 0.31 | 0.313 |  |  | 8/16 | +0.042 | -0.098 |  | -1.9 / -0.9 |  |
| MES | 15 | h16 | -0.064 | -0.188 .. +0.059 | -0.0165 | 0.31 / 0.31 / 0.22 | 0.222 |  |  | 7/16 | +0.075 | -0.204 |  | -3.3 / -1.0 |  |
| MES | 15 | eod | -0.310 | -0.899 .. +0.280 | -0.0332 | 0.3 / 0.28 / 0.11 | 0.111 |  |  | 8/16 | -0.036 | -0.582 |  | -5.8 / -1.0 |  |
| MES | 60 | h1 * | -0.008 | -0.026 .. +0.010 | -0.0096 | 0.4 / 0.4 / 0.35 | 0.363 | 1 | 1 | 8/16 | +0.008 | -0.024 | False | -0.8 / -0.8 |  |
| MES | 60 | h2 | -0.009 | -0.040 .. +0.022 | -0.0097 | 0.56 / 0.57 / 0.53 | 0.538 |  |  | 7/16 | +0.018 | -0.036 |  | -0.7 / -0.6 |  |
| MES | 60 | h4 | -0.019 | -0.071 .. +0.034 | -0.0130 | 0.48 / 0.5 / 0.47 | 0.472 |  |  | 9/16 | +0.017 | -0.055 |  | -1.1 / -0.7 | 0.080 |
| MES | 60 | h8 | -0.036 | -0.121 .. +0.049 | -0.0135 | 0.41 / 0.42 / 0.4 | 0.399 |  |  | 9/16 | -0.010 | -0.062 |  | -1.5 / -0.8 |  |
| MES | 60 | h16 | -0.033 | -0.148 .. +0.082 | -0.0108 | 0.57 / 0.57 / 0.58 | 0.582 |  |  | 10/16 | -0.010 | -0.057 |  | -1.1 / -0.6 |  |
| MES | 60 | eod | -0.034 | -0.152 .. +0.083 | -0.0108 | 0.57 / 0.56 / 0.59 | 0.582 |  |  | 11/16 | -0.038 | -0.031 |  | -1.1 / -0.6 |  |
| MNQ | 5 | h1 * | -0.008 | -0.013 .. -0.003 | -0.0040 | 0.0024 / 0.004 / 0.0036 | 0.00234 | 0.602 | 0.46 | 13/16 | -0.004 | -0.012 | False | -2.4 / -3.0 |  |
| MNQ | 5 | h2 | -0.015 | -0.028 .. -0.003 | -0.0066 | 0.018 / 0.017 / 0.006 | 0.00651 |  |  | 11/16 | -0.001 | -0.029 |  | -2.7 / -2.4 |  |
| MNQ | 5 | h4 | -0.029 | -0.055 .. -0.002 | -0.0086 | 0.034 / 0.031 / 0.01 | 0.0112 |  |  | 11/16 | +0.003 | -0.059 |  | -3.2 / -2.1 | 0.029 |
| MNQ | 5 | h8 | -0.031 | -0.072 .. +0.011 | -0.0059 | 0.15 / 0.15 / 0.17 | 0.176 |  |  | 9/16 | +0.021 | -0.082 |  | -2.3 / -1.4 |  |
| MNQ | 5 | h16 | -0.025 | -0.107 .. +0.056 | -0.0027 | 0.54 / 0.55 / 0.55 | 0.559 |  |  | 8/16 | +0.044 | -0.094 |  | -1.4 / -0.6 |  |
| MNQ | 5 | eod | -0.589 | -1.745 .. +0.566 | -0.0260 | 0.32 / 0.3 / 0.17 | 0.169 |  |  | 8/16 | +0.252 | -1.423 |  | -7.9 / -1.0 |  |
| MNQ | 15 | h1 * | -0.012 | -0.026 .. +0.002 | -0.0023 | 0.082 / 0.079 / 0.022 | 0.0245 | 1 | 0.997 | 11/16 | -0.013 | -0.012 | False | -1.8 / -1.7 |  |
| MNQ | 15 | h2 | -0.022 | -0.042 .. -0.001 | -0.0053 | 0.036 / 0.037 / 0.05 | 0.0492 |  |  | 11/16 | -0.008 | -0.036 |  | -1.8 / -2.1 |  |
| MNQ | 15 | h4 | -0.033 | -0.075 .. +0.008 | -0.0050 | 0.12 / 0.12 / 0.15 | 0.146 |  |  | 11/16 | -0.012 | -0.054 |  | -1.5 / -1.6 | 0.056 |
| MNQ | 15 | h8 | -0.041 | -0.113 .. +0.031 | -0.0038 | 0.26 / 0.26 / 0.3 | 0.304 |  |  | 10/16 | +0.001 | -0.083 |  | -1.5 / -1.1 |  |
| MNQ | 15 | h16 | -0.094 | -0.241 .. +0.053 | -0.0153 | 0.21 / 0.21 / 0.15 | 0.156 |  |  | 8/16 | +0.083 | -0.270 |  | -3.2 / -1.3 |  |
| MNQ | 15 | eod | -0.570 | -1.396 .. +0.255 | -0.0387 | 0.18 / 0.16 / 0.023 | 0.0208 |  |  | 8/16 | -0.103 | -1.035 |  | -6.3 / -1.4 |  |
| MNQ | 60 | h1 * | -0.017 | -0.036 .. +0.001 | -0.0110 | 0.071 / 0.083 / 0.055 | 0.0578 | 1 | 1 | 10/16 | +0.000 | -0.035 | False | -1.8 / -1.8 |  |
| MNQ | 60 | h2 | -0.030 | -0.064 .. +0.003 | -0.0120 | 0.078 / 0.084 / 0.055 | 0.0516 |  |  | 9/16 | +0.002 | -0.063 |  | -2.2 / -1.8 |  |
| MNQ | 60 | h4 | -0.046 | -0.103 .. +0.010 | -0.0134 | 0.11 / 0.12 / 0.093 | 0.0943 |  |  | 9/16 | +0.012 | -0.105 |  | -2.5 / -1.6 | 0.084 |
| MNQ | 60 | h8 | -0.069 | -0.158 .. +0.019 | -0.0144 | 0.12 / 0.13 / 0.11 | 0.114 |  |  | 8/16 | -0.013 | -0.126 |  | -2.8 / -1.5 |  |
| MNQ | 60 | h16 | -0.094 | -0.215 .. +0.027 | -0.0163 | 0.13 / 0.13 / 0.14 | 0.135 |  |  | 10/16 | -0.055 | -0.133 |  | -3.0 / -1.5 |  |
| MNQ | 60 | eod | -0.086 | -0.210 .. +0.038 | -0.0140 | 0.17 / 0.17 / 0.19 | 0.19 |  |  | 9/16 | -0.064 | -0.109 |  | -2.6 / -1.4 |  |
| MYM | 5 | h1 | +0.001 | -0.008 .. +0.010 | -0.0018 | 0.86 / 0.86 / 0.9 | 0.913 |  |  | 5/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 5 | h2 | -0.004 | -0.032 .. +0.023 | -0.0072 | 0.75 / 0.75 / 0.61 | 0.613 |  |  | 3/8 | n/a | -0.004 |  | -0.5 / -0.3 |  |
| MYM | 5 | h4 * | -0.015 | -0.082 .. +0.052 | -0.0122 | 0.66 / 0.66 / 0.43 | 0.433 | 1 | 1 | 2/8 | n/a | -0.015 | False | -1.0 / -0.4 | 0.047 |
| MYM | 5 | h8 | -0.015 | -0.124 .. +0.095 | -0.0128 | 0.79 / 0.79 / 0.68 | 0.681 |  |  | 2/8 | n/a | -0.015 |  | -0.7 / -0.3 |  |
| MYM | 5 | h16 | -0.020 | -0.194 .. +0.154 | -0.0140 | 0.82 / 0.82 / 0.75 | 0.728 |  |  | 3/8 | n/a | -0.020 |  | -0.8 / -0.2 |  |
| MYM | 5 | eod | -0.148 | -1.803 .. +1.507 | -0.0206 | 0.86 / 0.85 / 0.8 | 0.801 |  |  | 3/8 | n/a | -0.148 |  | -1.5 / -0.2 |  |
| MYM | 15 | h1 | -0.005 | -0.019 .. +0.009 | -0.0012 | 0.49 / 0.51 / 0.51 | 0.52 |  |  | 4/8 | n/a | -0.005 |  | -0.5 / -0.7 |  |
| MYM | 15 | h2 * | -0.022 | -0.062 .. +0.018 | -0.0107 | 0.28 / 0.27 / 0.17 | 0.177 | 1 | 1 | 4/8 | n/a | -0.022 | False | -1.2 / -1.1 |  |
| MYM | 15 | h4 | -0.038 | -0.123 .. +0.046 | -0.0133 | 0.37 / 0.38 / 0.22 | 0.237 |  |  | 3/8 | n/a | -0.038 |  | -1.2 / -0.9 | 0.088 |
| MYM | 15 | h8 | -0.058 | -0.225 .. +0.109 | -0.0189 | 0.5 / 0.5 / 0.27 | 0.291 |  |  | 3/8 | n/a | -0.058 |  | -1.5 / -0.7 |  |
| MYM | 15 | h16 | -0.153 | -0.568 .. +0.261 | -0.0351 | 0.47 / 0.47 / 0.12 | 0.128 |  |  | 3/8 | n/a | -0.153 |  | -2.9 / -0.7 |  |
| MYM | 15 | eod | -0.364 | -1.574 .. +0.846 | -0.0394 | 0.56 / 0.55 / 0.27 | 0.274 |  |  | 3/8 | n/a | -0.364 |  | -3.0 / -0.6 |  |
| MYM | 60 | h1 | -0.011 | -0.037 .. +0.015 | -0.0081 | 0.41 / 0.42 / 0.4 | 0.414 |  |  | 5/8 | n/a | -0.011 |  | -0.8 / -0.8 |  |
| MYM | 60 | h2 * | -0.022 | -0.067 .. +0.023 | -0.0058 | 0.35 / 0.34 / 0.33 | 0.343 | 1 | 1 | 5/8 | n/a | -0.022 | False | -1.1 / -0.9 |  |
| MYM | 60 | h4 | -0.029 | -0.104 .. +0.047 | -0.0036 | 0.46 / 0.45 / 0.46 | 0.473 |  |  | 4/8 | n/a | -0.029 |  | -1.1 / -0.7 | 0.115 |
| MYM | 60 | h8 | -0.015 | -0.141 .. +0.111 | -0.0024 | 0.81 / 0.81 / 0.81 | 0.813 |  |  | 2/8 | n/a | -0.015 |  | -0.4 / -0.2 |  |
| MYM | 60 | h16 | -0.015 | -0.200 .. +0.171 | -0.0027 | 0.88 / 0.87 / 0.87 | 0.865 |  |  | 4/8 | n/a | -0.015 |  | -0.3 / -0.2 |  |
| MYM | 60 | eod | -0.008 | -0.203 .. +0.188 | -0.0015 | 0.94 / 0.93 / 0.94 | 0.945 |  |  | 4/8 | n/a | -0.008 |  | -0.2 / -0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.019 | +0.015 .. +0.024 | +3.9% | +0.024 | 4.5e-19 | 2.34e-16 | 14/16 |
| MES | 5 | h2 | +0.029 | +0.022 .. +0.037 | +4.2% | +0.043 | 1.1e-13 |  | 13/16 |
| MES | 5 | h4 | +0.040 | +0.025 .. +0.055 | +4.0% | +0.071 | 3.2e-07 |  | 12/16 |
| MES | 5 | h8 | +0.056 | +0.029 .. +0.083 | +3.9% | +0.111 | 6.4e-05 |  | 11/16 |
| MES | 5 | h16 | +0.075 | +0.028 .. +0.121 | +3.6% | +0.151 | 0.0016 |  | 11/16 |
| MES | 5 | eod | +0.126 | -0.472 .. +0.725 | +1.3% | +0.199 | 0.68 |  | 9/16 |
| MES | 15 | h1 * | +0.036 | +0.028 .. +0.044 | +7.1% | +0.077 | 1.9e-18 | 9.34e-16 | 15/16 |
| MES | 15 | h2 | +0.052 | +0.033 .. +0.070 | +7.1% | +0.111 | 3.8e-08 |  | 14/16 |
| MES | 15 | h4 | +0.065 | +0.027 .. +0.102 | +6.1% | +0.145 | 0.00079 |  | 12/16 |
| MES | 15 | h8 | +0.083 | +0.021 .. +0.144 | +5.4% | +0.182 | 0.0082 |  | 9/16 |
| MES | 15 | h16 | +0.106 | +0.008 .. +0.205 | +4.7% | +0.222 | 0.035 |  | 9/16 |
| MES | 15 | eod | +0.103 | -0.397 .. +0.603 | +1.9% | +0.282 | 0.69 |  | 8/16 |
| MES | 60 | h1 * | +0.084 | +0.068 .. +0.100 | +16.4% | +0.181 | 1.8e-24 | 1.15e-21 | 14/16 |
| MES | 60 | h2 | +0.100 | +0.076 .. +0.125 | +13.6% | +0.225 | 1e-15 |  | 13/16 |
| MES | 60 | h4 | +0.135 | +0.097 .. +0.173 | +12.7% | +0.269 | 2.8e-12 |  | 13/16 |
| MES | 60 | h8 | +0.132 | +0.080 .. +0.183 | +8.7% | +0.294 | 1.7e-06 |  | 14/16 |
| MES | 60 | h16 | +0.112 | +0.039 .. +0.184 | +5.4% | +0.289 | 0.0025 |  | 12/16 |
| MES | 60 | eod | +0.093 | +0.015 .. +0.170 | +4.3% | +0.283 | 0.019 |  | 13/16 |
| MNQ | 5 | h1 * | +0.020 | +0.013 .. +0.027 | +3.7% | +0.025 | 1.2e-07 | 3.24e-05 | 12/16 |
| MNQ | 5 | h2 | +0.033 | +0.016 .. +0.050 | +4.3% | +0.048 | 0.00015 |  | 12/16 |
| MNQ | 5 | h4 | +0.048 | +0.014 .. +0.082 | +4.3% | +0.082 | 0.0062 |  | 10/16 |
| MNQ | 5 | h8 | +0.073 | +0.013 .. +0.134 | +4.5% | +0.133 | 0.018 |  | 10/16 |
| MNQ | 5 | h16 | +0.097 | +0.004 .. +0.190 | +4.1% | +0.200 | 0.04 |  | 11/16 |
| MNQ | 5 | eod | +0.554 | -0.378 .. +1.486 | +4.4% | +0.719 | 0.24 |  | 9/16 |
| MNQ | 15 | h1 * | +0.041 | +0.028 .. +0.054 | +7.7% | +0.082 | 1.1e-09 | 3.22e-07 | 14/16 |
| MNQ | 15 | h2 | +0.060 | +0.025 .. +0.095 | +7.7% | +0.125 | 0.00087 |  | 12/16 |
| MNQ | 15 | h4 | +0.086 | -0.004 .. +0.176 | +7.6% | +0.191 | 0.06 |  | 11/16 |
| MNQ | 15 | h8 | +0.114 | -0.039 .. +0.266 | +6.8% | +0.279 | 0.14 |  | 11/16 |
| MNQ | 15 | h16 | +0.136 | -0.035 .. +0.307 | +5.4% | +0.395 | 0.12 |  | 10/16 |
| MNQ | 15 | eod | +0.433 | -0.416 .. +1.283 | +6.8% | +0.564 | 0.32 |  | 9/16 |
| MNQ | 60 | h1 * | +0.077 | +0.060 .. +0.093 | +14.5% | +0.172 | 2.8e-20 | 1.54e-17 | 16/16 |
| MNQ | 60 | h2 | +0.093 | +0.068 .. +0.119 | +12.2% | +0.213 | 6.5e-13 |  | 16/16 |
| MNQ | 60 | h4 | +0.124 | +0.086 .. +0.163 | +11.3% | +0.250 | 1.8e-10 |  | 15/16 |
| MNQ | 60 | h8 | +0.142 | +0.086 .. +0.198 | +9.0% | +0.289 | 6.8e-07 |  | 15/16 |
| MNQ | 60 | h16 | +0.152 | +0.072 .. +0.232 | +6.9% | +0.322 | 0.0002 |  | 13/16 |
| MNQ | 60 | eod | +0.164 | +0.079 .. +0.249 | +7.1% | +0.328 | 0.00015 |  | 14/16 |
| MYM | 5 | h1 * | +0.021 | +0.009 .. +0.033 | +3.9% | +0.025 | 0.00045 | 0.0823 | 7/8 |
| MYM | 5 | h2 | +0.035 | +0.006 .. +0.064 | +4.6% | +0.048 | 0.019 |  | 7/8 |
| MYM | 5 | h4 | +0.050 | -0.018 .. +0.118 | +4.6% | +0.079 | 0.15 |  | 6/8 |
| MYM | 5 | h8 | +0.071 | -0.045 .. +0.188 | +4.5% | +0.116 | 0.23 |  | 6/8 |
| MYM | 5 | h16 | +0.089 | -0.086 .. +0.264 | +3.8% | +0.175 | 0.33 |  | 5/8 |
| MYM | 5 | eod | +0.381 | -0.777 .. +1.539 | +3.3% | +0.745 | 0.52 |  | 4/8 |
| MYM | 15 | h1 * | +0.043 | +0.022 .. +0.064 | +8.1% | +0.088 | 4.6e-05 | 0.00987 | 7/8 |
| MYM | 15 | h2 | +0.073 | +0.017 .. +0.129 | +9.5% | +0.141 | 0.011 |  | 7/8 |
| MYM | 15 | h4 | +0.112 | -0.012 .. +0.237 | +10.1% | +0.222 | 0.082 |  | 7/8 |
| MYM | 15 | h8 | +0.161 | -0.039 .. +0.361 | +9.8% | +0.360 | 0.12 |  | 6/8 |
| MYM | 15 | h16 | +0.273 | -0.101 .. +0.647 | +11.1% | +0.556 | 0.16 |  | 7/8 |
| MYM | 15 | eod | +0.461 | -0.602 .. +1.523 | +7.7% | +0.928 | 0.4 |  | 5/8 |
| MYM | 60 | h1 * | +0.079 | +0.056 .. +0.102 | +15.1% | +0.169 | 3.4e-11 | 1.16e-08 | 7/8 |
| MYM | 60 | h2 | +0.100 | +0.064 .. +0.135 | +13.2% | +0.218 | 5.2e-08 |  | 7/8 |
| MYM | 60 | h4 | +0.132 | +0.076 .. +0.188 | +12.2% | +0.267 | 4.3e-06 |  | 7/8 |
| MYM | 60 | h8 | +0.131 | +0.049 .. +0.213 | +8.5% | +0.291 | 0.0017 |  | 7/8 |
| MYM | 60 | h16 | +0.128 | +0.016 .. +0.239 | +6.0% | +0.297 | 0.025 |  | 7/8 |
| MYM | 60 | eod | +0.117 | +0.003 .. +0.230 | +5.2% | +0.300 | 0.044 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.08 pts | -0.47 .. +0.63 | 0.78 |
| MES | 15 | +0.43 pts | -0.45 .. +1.32 | 0.34 |
| MES | 60 | +0.28 pts | -1.18 .. +1.74 | 0.71 |
| MNQ | 5 | -0.21 pts | -0.79 .. +0.37 | 0.48 |
| MNQ | 15 | +0.01 pts | -0.91 .. +0.94 | 0.98 |
| MNQ | 60 | -0.46 pts | -1.96 .. +1.04 | 0.56 |
| MYM | 5 | +0.18 pts | -0.57 .. +0.94 | 0.64 |
| MYM | 15 | +0.20 pts | -1.08 .. +1.49 | 0.76 |
| MYM | 60 | -0.41 pts | -2.50 .. +1.68 | 0.7 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | long | 207239 | +0.006 | 0.279 | +0.05 | -3.45 | -3.46 | -3.45 | -3.49 |
| MES | 5 | h2 | bottom fifth | long | 207648 | +0.001 | 0.340 | +0.06 | -3.44 | -3.48 | -3.40 | -3.39 |
| MES | 5 | h4 | bottom fifth | long | 207648 | +0.009 | 0.340 | +0.18 | -3.32 | -3.43 | -3.21 | -3.28 |
| MES | 5 | h8 | bottom fifth | long | 207648 | +0.012 | 0.340 | +0.26 | -3.24 | -3.39 | -3.08 | -3.24 |
| MES | 5 | h16 | top fifth | long | 207239 | +0.049 | 0.279 | +0.23 | -3.27 | -3.05 | -3.45 | -3.67 |
| MES | 5 | eod | bottom fifth | long | 207648 | +0.604 | 0.340 | +4.91 | +1.41 | +0.38 | +2.51 | -1.57 |
| MES | 15 | h1 | bottom fifth | long | 68483 | +0.001 | 0.180 | +0.03 | -3.47 | -3.49 | -3.46 | -3.38 |
| MES | 15 | h2 | bottom fifth | long | 68483 | +0.006 | 0.180 | +0.15 | -3.35 | -3.48 | -3.22 | -3.27 |
| MES | 15 | h4 | bottom fifth | long | 68483 | +0.014 | 0.180 | +0.30 | -3.20 | -3.42 | -2.99 | -3.17 |
| MES | 15 | h8 | bottom fifth | long | 68483 | +0.020 | 0.180 | +0.34 | -3.16 | -3.29 | -3.03 | -3.19 |
| MES | 15 | h16 | bottom fifth | long | 68483 | +0.063 | 0.180 | +1.06 | -2.44 | -2.69 | -2.19 | -2.80 |
| MES | 15 | eod | bottom fifth | long | 68483 | +0.308 | 0.180 | +5.00 | +1.50 | +0.55 | +2.43 | -1.91 |
| MES | 60 | h1 | bottom fifth | long | 16684 | +0.007 | 0.088 | +0.14 | -3.36 | -3.56 | -3.17 | -3.45 |
| MES | 60 | h2 | bottom fifth | long | 16684 | +0.008 | 0.088 | +0.23 | -3.27 | -3.52 | -3.04 | -3.43 |
| MES | 60 | h4 | bottom fifth | long | 16684 | +0.021 | 0.088 | +0.64 | -2.86 | -3.01 | -2.71 | -3.35 |
| MES | 60 | h8 | bottom fifth | long | 16684 | +0.056 | 0.088 | +2.13 | -1.37 | -1.68 | -1.09 | -2.73 |
| MES | 60 | h16 | bottom fifth | long | 16684 | +0.117 | 0.088 | +4.21 | +0.71 | +0.36 | +1.02 | -2.36 |
| MES | 60 | eod | bottom fifth | long | 16684 | +0.144 | 0.088 | +4.82 | +1.32 | +1.28 | +1.35 | -2.81 |
| MNQ | 5 | h1 | bottom fifth | long | 206905 | +0.009 | 0.132 | +0.10 | -1.90 | -1.97 | -1.82 | -1.90 |
| MNQ | 5 | h2 | bottom fifth | long | 206905 | +0.017 | 0.132 | +0.22 | -1.78 | -1.93 | -1.64 | -1.80 |
| MNQ | 5 | h4 | bottom fifth | long | 206905 | +0.035 | 0.132 | +0.46 | -1.54 | -1.85 | -1.24 | -1.62 |
| MNQ | 5 | h8 | bottom fifth | long | 206905 | +0.051 | 0.132 | +0.74 | -1.26 | -1.74 | -0.77 | -1.48 |
| MNQ | 5 | h16 | bottom fifth | long | 206905 | +0.075 | 0.132 | +1.16 | -0.84 | -1.56 | -0.12 | -1.36 |
| MNQ | 5 | eod | bottom fifth | long | 206905 | +1.032 | 0.132 | +9.49 | +7.49 | +1.72 | +13.26 | +2.78 |
| MNQ | 15 | h1 | bottom fifth | long | 68575 | +0.015 | 0.073 | +0.32 | -1.68 | -1.86 | -1.48 | -1.67 |
| MNQ | 15 | h2 | bottom fifth | long | 68575 | +0.024 | 0.073 | +0.62 | -1.38 | -1.81 | -0.91 | -1.44 |
| MNQ | 15 | h4 | bottom fifth | long | 68575 | +0.038 | 0.073 | +0.96 | -1.04 | -1.67 | -0.37 | -1.28 |
| MNQ | 15 | h8 | bottom fifth | long | 68575 | +0.059 | 0.073 | +1.32 | -0.68 | -1.45 | +0.14 | -1.29 |
| MNQ | 15 | h16 | bottom fifth | long | 68575 | +0.102 | 0.073 | +2.55 | +0.55 | -1.01 | +2.21 | -0.44 |
| MNQ | 15 | eod | bottom fifth | long | 68575 | +0.488 | 0.073 | +8.48 | +6.48 | +1.88 | +11.37 | +2.14 |
| MNQ | 60 | h1 | bottom fifth | long | 16683 | +0.022 | 0.036 | +0.91 | -1.09 | -1.68 | -0.46 | -1.36 |
| MNQ | 60 | h2 | bottom fifth | long | 16683 | +0.033 | 0.036 | +1.44 | -0.56 | -1.58 | +0.54 | -0.92 |
| MNQ | 60 | h4 | bottom fifth | long | 16683 | +0.053 | 0.036 | +2.53 | +0.53 | -1.12 | +2.29 | -0.20 |
| MNQ | 60 | h8 | bottom fifth | long | 16683 | +0.092 | 0.036 | +4.73 | +2.73 | -0.01 | +5.66 | +1.09 |
| MNQ | 60 | h16 | bottom fifth | long | 16683 | +0.184 | 0.036 | +8.14 | +6.14 | +1.97 | +10.57 | +2.75 |
| MNQ | 60 | eod | bottom fifth | long | 16683 | +0.218 | 0.036 | +9.11 | +7.11 | +2.53 | +11.97 | +1.98 |
| MYM | 5 | h1 | top fifth | long | 103800 | -0.000 | 0.162 | +0.05 | -1.95 | +nan | -1.95 | -1.95 |
| MYM | 5 | h2 | bottom fifth | long | 103817 | -0.002 | 0.169 | +0.01 | -1.99 | +nan | -1.99 | -1.98 |
| MYM | 5 | h4 | bottom fifth | long | 103817 | +0.000 | 0.169 | +0.08 | -1.92 | +nan | -1.92 | -1.98 |
| MYM | 5 | h8 | bottom fifth | long | 103817 | -0.007 | 0.169 | +0.15 | -1.85 | +nan | -1.85 | -2.02 |
| MYM | 5 | h16 | bottom fifth | long | 103817 | -0.017 | 0.169 | +0.14 | -1.86 | +nan | -1.86 | -2.20 |
| MYM | 5 | eod | bottom fifth | long | 103817 | +0.105 | 0.169 | +3.06 | +1.06 | +nan | +1.06 | -1.13 |
| MYM | 15 | h1 | top fifth | short | 34285 | +0.002 | 0.089 | +0.01 | -1.99 | +nan | -1.99 | -1.97 |
| MYM | 15 | h2 | bottom fifth | long | 34288 | +0.006 | 0.091 | +0.14 | -1.86 | +nan | -1.86 | -1.85 |
| MYM | 15 | h4 | bottom fifth | long | 34288 | +0.007 | 0.091 | +0.27 | -1.73 | +nan | -1.73 | -1.77 |
| MYM | 15 | h8 | top fifth | short | 34285 | +0.096 | 0.089 | +0.37 | -1.63 | +nan | -1.63 | -2.17 |
| MYM | 15 | h16 | top fifth | short | 34285 | +0.244 | 0.089 | +0.61 | -1.39 | +nan | -1.39 | -2.72 |
| MYM | 15 | eod | bottom fifth | long | 34288 | +0.079 | 0.091 | +3.30 | +1.30 | +nan | +1.30 | -0.47 |
| MYM | 60 | h1 | top fifth | short | 8331 | +0.010 | 0.048 | +0.24 | -1.76 | +nan | -1.76 | -1.61 |
| MYM | 60 | h2 | top fifth | short | 8331 | +0.018 | 0.048 | +0.26 | -1.74 | +nan | -1.74 | -1.34 |
| MYM | 60 | h4 | top fifth | short | 8331 | +0.029 | 0.048 | +0.57 | -1.43 | +nan | -1.43 | -0.74 |
| MYM | 60 | h8 | top fifth | short | 8331 | +0.025 | 0.048 | +0.80 | -1.20 | +nan | -1.20 | -0.08 |
| MYM | 60 | h16 | bottom fifth | long | 8331 | +0.021 | 0.045 | +1.67 | -0.33 | +nan | -0.33 | -2.08 |
| MYM | 60 | eod | bottom fifth | long | 8331 | +0.039 | 0.045 | +2.42 | +0.42 | +nan | +0.42 | -2.31 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.223 | +1.126 | +0.887 | +0.597 | +0.361 | +0.000 | +0.016 | +0.015 | +0.011 | +0.017 | +0.034 |
| MES | 15 | +2.476 | +2.031 | +1.482 | +0.970 | +0.588 | +0.000 | +0.008 | +0.005 | +0.002 | -0.004 | -0.029 |
| MES | 60 | +3.580 | +2.990 | +2.232 | +1.491 | +0.917 | +0.000 | -0.001 | +0.005 | +0.009 | +0.003 | +0.185 |
| MNQ | 5 | +1.402 | +1.273 | +0.989 | +0.661 | +0.394 | +0.000 | -0.002 | -0.008 | -0.023 | -0.027 | -0.022 |
| MNQ | 15 | +2.711 | +2.183 | +1.576 | +1.033 | +0.625 | +0.000 | -0.013 | -0.025 | -0.041 | -0.049 | -0.095 |
| MNQ | 60 | +3.690 | +3.067 | +2.284 | +1.531 | +0.952 | +0.000 | -0.014 | -0.020 | -0.013 | -0.014 | +0.204 |
| MYM | 5 | +1.300 | +1.199 | +0.936 | +0.621 | +0.368 | +0.000 | -0.000 | -0.007 | -0.019 | -0.023 | -0.028 |
| MYM | 15 | +2.619 | +2.129 | +1.539 | +0.999 | +0.596 | +0.000 | -0.015 | -0.034 | -0.058 | -0.086 | -0.226 |
| MYM | 60 | +3.702 | +3.084 | +2.278 | +1.520 | +0.941 | +0.000 | -0.012 | -0.019 | -0.022 | -0.043 | -0.037 |

## Calibration

- MES 5-min: 1036271 bars, 207239 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68422 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68399 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103800 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34285 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
