# Impact card: pat_harami

candle pattern harami in its textbook direction: body1 > avgB10, body2 <= avgB10, body2 strictly inside body1; bullish if bar1 down and close1 < EMA10, bearish mirror [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.038 R20 over the next 16 bars (80 min), p=0.66; we would catch an effect of 0.025 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.1).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.67 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.226 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.044 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.32).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.34 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.132 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.075 R20 over the next 4 bars (4 h), p=0.44; we would catch an effect of 0.119 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.59).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.12 at recent bar sizes, 90% range up to $7.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.006 R20 over the next 1 bar (5 min), p=0.89; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.669 R20, CONFIRMED, q=1.29e-05, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.17 at recent bar sizes, 90% range up to $0.89); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.018 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.049 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.017).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.82 at recent bar sizes, 90% range up to $2.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.082 R20 over the next 4 bars (4 h), p=0.41; we would catch an effect of 0.113 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.7).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.96 at recent bar sizes, 90% range up to $15.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.238 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.033 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% LESS after the event than after matched bars over the next 16 bars (80 min) (-0.105 R20, CONFIRMED, q=0.0379, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.81 at recent bar sizes, 90% range up to $0.61); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.060 R20 over the next 4 bars (1 h), p=0.19; we would catch an effect of 0.067 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.067).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.24 at recent bar sizes, 90% range up to $2.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.019 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.159 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.87).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.83 at recent bar sizes, 90% range up to $9.02); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.005 | -0.013 .. +0.003 | -0.0010 | 0.25 / 0.27 / 0.3 | 0.307 |  |  | 9/16 | -0.012 | +0.002 |  | -1.1 / -1.2 |  |
| MES | 5 | h2 | -0.003 | -0.014 .. +0.007 | -0.0005 | 0.54 / 0.57 / 0.63 | 0.618 |  |  | 8/16 | -0.001 | -0.005 |  | -0.6 / -0.6 |  |
| MES | 5 | h4 | -0.001 | -0.018 .. +0.015 | -0.0001 | 0.87 / 0.88 / 0.89 | 0.896 |  |  | 7/16 | +0.011 | -0.014 |  | -0.2 / -0.2 | 0.025 |
| MES | 5 | h8 | +0.021 | -0.006 .. +0.047 | +0.0015 | 0.13 / 0.13 / 0.14 | 0.141 |  |  | 10/16 | +0.048 | -0.006 |  | +1.6 / +1.5 |  |
| MES | 5 | h16 * | +0.038 | -0.001 .. +0.077 | +0.0019 | 0.055 / 0.06 / 0.059 | 0.0581 | 1 | 1 | 13/16 | +0.081 | -0.005 | False | +2.0 / +1.9 |  |
| MES | 5 | eod | +0.160 | -0.031 .. +0.351 | +0.0016 | 0.1 / 0.098 / 0.12 | 0.12 |  |  | 11/16 | +0.059 | +0.260 |  | +1.7 / +1.6 |  |
| MES | 15 | h1 | +0.001 | -0.016 .. +0.017 | +0.0001 | 0.94 / 0.94 / 0.95 | 0.946 |  |  | 7/16 | -0.011 | +0.012 |  | +0.1 / +0.1 |  |
| MES | 15 | h2 | +0.011 | -0.012 .. +0.034 | +0.0014 | 0.36 / 0.35 / 0.4 | 0.397 |  |  | 9/16 | -0.003 | +0.025 |  | +0.9 / +0.9 |  |
| MES | 15 | h4 | +0.021 | -0.016 .. +0.058 | +0.0019 | 0.26 / 0.24 / 0.28 | 0.275 |  |  | 8/16 | +0.025 | +0.017 |  | +1.2 / +1.1 | 0.050 |
| MES | 15 | h8 * | +0.044 | -0.010 .. +0.097 | +0.0027 | 0.11 / 0.1 / 0.12 | 0.121 | 1 | 1 | 9/16 | +0.071 | +0.017 | False | +1.7 / +1.6 |  |
| MES | 15 | h16 | +0.024 | -0.053 .. +0.101 | +0.0011 | 0.54 / 0.54 / 0.56 | 0.558 |  |  | 10/16 | +0.098 | -0.050 |  | +0.6 / +0.6 |  |
| MES | 15 | eod | -0.105 | -0.284 .. +0.074 | -0.0017 | 0.25 / 0.27 / 0.34 | 0.336 |  |  | 11/16 | -0.002 | -0.206 |  | -1.1 / -1.1 |  |
| MES | 60 | h1 | +0.027 | -0.010 .. +0.064 | +0.0049 | 0.15 / 0.15 / 0.18 | 0.182 |  |  | 11/16 | +0.042 | +0.013 |  | +1.5 / +1.5 |  |
| MES | 60 | h2 | +0.016 | -0.039 .. +0.071 | +0.0020 | 0.57 / 0.57 / 0.59 | 0.602 |  |  | 9/16 | +0.028 | +0.003 |  | +0.6 / +0.6 |  |
| MES | 60 | h4 * | +0.075 | -0.003 .. +0.152 | +0.0067 | 0.059 / 0.073 / 0.079 | 0.0823 | 1 | 1 | 11/16 | +0.071 | +0.079 | False | +1.8 / +1.9 | 0.119 |
| MES | 60 | h8 | +0.049 | -0.058 .. +0.156 | +0.0032 | 0.37 / 0.4 / 0.4 | 0.386 |  |  | 10/16 | +0.041 | +0.057 |  | +0.8 / +0.9 |  |
| MES | 60 | h16 | +0.063 | -0.072 .. +0.198 | +0.0032 | 0.36 / 0.37 / 0.37 | 0.377 |  |  | 9/16 | +0.003 | +0.123 |  | +0.9 / +0.9 |  |
| MES | 60 | eod | +0.040 | -0.104 .. +0.185 | +0.0019 | 0.58 / 0.59 / 0.57 | 0.579 |  |  | 9/16 | -0.027 | +0.108 |  | +0.6 / +0.5 |  |
| MNQ | 5 | h1 * | +0.006 | -0.001 .. +0.013 | +0.0014 | 0.079 / 0.092 / 0.18 | 0.162 | 1 | 1 | 12/16 | +0.010 | +0.003 | False | +1.6 / +1.8 |  |
| MNQ | 5 | h2 | -0.005 | -0.016 .. +0.006 | -0.0007 | 0.35 / 0.35 / 0.48 | 0.433 |  |  | 8/16 | +0.006 | -0.016 |  | -0.9 / -0.9 |  |
| MNQ | 5 | h4 | -0.008 | -0.025 .. +0.009 | -0.0007 | 0.37 / 0.35 / 0.51 | 0.479 |  |  | 9/16 | +0.006 | -0.022 |  | -0.9 / -0.9 | 0.025 |
| MNQ | 5 | h8 | -0.010 | -0.036 .. +0.015 | -0.0006 | 0.43 / 0.42 / 0.55 | 0.528 |  |  | 9/16 | +0.011 | -0.031 |  | -0.8 / -0.8 |  |
| MNQ | 5 | h16 | +0.000 | -0.038 .. +0.038 | +0.0000 | 0.99 / 0.99 / 1 | 0.997 |  |  | 8/16 | +0.051 | -0.050 |  | +0.0 / +0.0 |  |
| MNQ | 5 | eod | +0.103 | -0.104 .. +0.311 | +0.0009 | 0.33 / 0.34 / 0.39 | 0.397 |  |  | 10/16 | +0.008 | +0.198 |  | +1.0 / +1.0 |  |
| MNQ | 15 | h1 | -0.002 | -0.017 .. +0.012 | -0.0004 | 0.73 / 0.75 / 0.8 | 0.755 |  |  | 8/16 | -0.008 | +0.003 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h2 * | +0.018 | -0.003 .. +0.039 | +0.0019 | 0.096 / 0.1 / 0.27 | 0.209 | 1 | 1 | 11/16 | +0.006 | +0.030 | False | +1.6 / +1.7 |  |
| MNQ | 15 | h4 | +0.004 | -0.031 .. +0.039 | +0.0002 | 0.83 / 0.83 / 0.89 | 0.855 |  |  | 7/16 | -0.016 | +0.023 |  | +0.2 / +0.2 | 0.049 |
| MNQ | 15 | h8 | -0.014 | -0.067 .. +0.038 | -0.0007 | 0.59 / 0.58 / 0.69 | 0.656 |  |  | 9/16 | -0.030 | +0.001 |  | -0.6 / -0.5 |  |
| MNQ | 15 | h16 | -0.010 | -0.084 .. +0.064 | -0.0004 | 0.79 / 0.8 / 0.83 | 0.83 |  |  | 9/16 | -0.022 | +0.002 |  | -0.3 / -0.3 |  |
| MNQ | 15 | eod | -0.137 | -0.328 .. +0.055 | -0.0019 | 0.16 / 0.17 / 0.31 | 0.305 |  |  | 11/16 | -0.120 | -0.154 |  | -1.4 / -1.4 |  |
| MNQ | 60 | h1 | +0.021 | -0.016 .. +0.059 | +0.0041 | 0.26 / 0.24 / 0.26 | 0.261 |  |  | 10/16 | +0.038 | +0.005 |  | +1.1 / +1.1 |  |
| MNQ | 60 | h2 | +0.041 | -0.008 .. +0.090 | +0.0055 | 0.1 / 0.1 / 0.14 | 0.138 |  |  | 10/16 | +0.078 | +0.004 |  | +1.6 / +1.6 |  |
| MNQ | 60 | h4 * | +0.082 | +0.010 .. +0.154 | +0.0078 | 0.025 / 0.027 / 0.042 | 0.0422 | 1 | 0.99 | 12/16 | +0.098 | +0.066 | False | +2.1 / +2.2 | 0.113 |
| MNQ | 60 | h8 | +0.076 | -0.025 .. +0.178 | +0.0053 | 0.14 / 0.15 / 0.17 | 0.167 |  |  | 9/16 | +0.101 | +0.052 |  | +1.4 / +1.5 |  |
| MNQ | 60 | h16 | +0.059 | -0.064 .. +0.183 | +0.0031 | 0.35 / 0.36 / 0.39 | 0.382 |  |  | 11/16 | +0.040 | +0.079 |  | +0.9 / +0.9 |  |
| MNQ | 60 | eod | +0.040 | -0.093 .. +0.173 | +0.0020 | 0.56 / 0.56 / 0.57 | 0.565 |  |  | 8/16 | +0.028 | +0.052 |  | +0.6 / +0.6 |  |
| MYM | 5 | h1 | +0.007 | -0.004 .. +0.017 | +0.0014 | 0.19 / 0.19 / 0.26 | 0.236 |  |  | 5/8 | n/a | +0.007 |  | +1.3 / +1.3 |  |
| MYM | 5 | h2 | +0.016 | +0.001 .. +0.030 | +0.0019 | 0.039 / 0.036 / 0.15 | 0.132 |  |  | 6/8 | n/a | +0.016 |  | +2.0 / +2.1 |  |
| MYM | 5 | h4 | +0.020 | -0.002 .. +0.041 | +0.0015 | 0.074 / 0.068 / 0.28 | 0.238 |  |  | 6/8 | n/a | +0.020 |  | +1.8 / +1.8 | 0.033 |
| MYM | 5 | h8 | -0.000 | -0.033 .. +0.032 | -0.0000 | 0.98 / 0.98 / 0.99 | 0.982 |  |  | 3/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h16 | +0.011 | -0.039 .. +0.061 | +0.0005 | 0.67 / 0.67 / 0.75 | 0.737 |  |  | 4/8 | n/a | +0.011 |  | +0.4 / +0.4 |  |
| MYM | 5 | eod * | +0.238 | -0.024 .. +0.500 | +0.0023 | 0.075 / 0.1 / 0.13 | 0.132 | 1 | 0.999 | 6/8 | n/a | +0.238 | False | +1.7 / +1.8 |  |
| MYM | 15 | h1 | +0.014 | -0.008 .. +0.035 | +0.0026 | 0.21 / 0.19 / 0.29 | 0.254 |  |  | 4/8 | n/a | +0.014 |  | +1.3 / +1.3 |  |
| MYM | 15 | h2 | +0.024 | -0.003 .. +0.052 | +0.0026 | 0.08 / 0.079 / 0.3 | 0.209 |  |  | 6/8 | n/a | +0.024 |  | +1.6 / +1.8 |  |
| MYM | 15 | h4 * | +0.060 | +0.016 .. +0.104 | +0.0038 | 0.0079 / 0.0061 / 0.14 | 0.112 | 1 | 0.787 | 6/8 | n/a | +0.060 | False | +2.7 / +2.7 | 0.067 |
| MYM | 15 | h8 | +0.052 | -0.014 .. +0.117 | +0.0025 | 0.12 / 0.13 / 0.31 | 0.249 |  |  | 7/8 | n/a | +0.052 |  | +1.6 / +1.5 |  |
| MYM | 15 | h16 | +0.072 | -0.009 .. +0.154 | +0.0025 | 0.081 / 0.11 / 0.32 | 0.309 |  |  | 5/8 | n/a | +0.072 |  | +1.5 / +1.7 |  |
| MYM | 15 | eod | +0.100 | -0.141 .. +0.341 | +0.0015 | 0.41 / 0.45 / 0.58 | 0.541 |  |  | 4/8 | n/a | +0.100 |  | +0.8 / +0.8 |  |
| MYM | 60 | h1 | +0.001 | -0.048 .. +0.049 | +0.0001 | 0.98 / 0.98 / 0.98 | 0.984 |  |  | 4/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 60 | h2 * | -0.019 | -0.093 .. +0.055 | -0.0026 | 0.62 / 0.61 / 0.64 | 0.645 | 1 | 1 | 5/8 | n/a | -0.019 | False | -0.5 / -0.5 |  |
| MYM | 60 | h4 | -0.034 | -0.138 .. +0.071 | -0.0033 | 0.53 / 0.52 / 0.55 | 0.561 |  |  | 5/8 | n/a | -0.034 |  | -0.6 / -0.6 | 0.159 |
| MYM | 60 | h8 | -0.011 | -0.160 .. +0.139 | -0.0007 | 0.89 / 0.89 / 0.89 | 0.899 |  |  | 5/8 | n/a | -0.011 |  | -0.1 / -0.1 |  |
| MYM | 60 | h16 | -0.008 | -0.190 .. +0.174 | -0.0004 | 0.93 / 0.93 / 0.93 | 0.92 |  |  | 6/8 | n/a | -0.008 |  | -0.1 / -0.1 |  |
| MYM | 60 | eod | +0.001 | -0.185 .. +0.186 | +0.0001 | 0.99 / 0.99 / 1 | 0.993 |  |  | 2/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.006 .. +0.007 | +0.1% | -0.001 | 0.91 |  | 8/16 |
| MES | 5 | h2 | +0.001 | -0.007 .. +0.009 | +0.1% | +0.002 | 0.83 |  | 9/16 |
| MES | 5 | h4 | +0.007 | -0.006 .. +0.020 | +0.7% | +0.008 | 0.66 |  | 8/16 |
| MES | 5 | h8 | +0.011 | -0.007 .. +0.029 | +0.8% | +0.008 | 0.71 |  | 9/16 |
| MES | 5 | h16 | -0.005 | -0.032 .. +0.022 | -0.2% | -0.004 | 0.72 |  | 9/16 |
| MES | 5 | eod * | -0.193 | -0.351 .. -0.035 | -1.9% | -0.455 | 0.017 | 1 | 10/16 |
| MES | 15 | h1 | +0.005 | -0.007 .. +0.016 | +0.9% | +0.001 | 0.46 |  | 9/16 |
| MES | 15 | h2 | -0.008 | -0.024 .. +0.009 | -1.1% | -0.008 | 0.55 |  | 9/16 |
| MES | 15 | h4 | +0.001 | -0.023 .. +0.025 | +0.1% | -0.010 | 0.96 |  | 7/16 |
| MES | 15 | h8 | -0.015 | -0.048 .. +0.018 | -1.0% | -0.061 | 0.44 |  | 10/16 |
| MES | 15 | h16 | -0.017 | -0.068 .. +0.033 | -0.8% | -0.118 | 0.54 |  | 9/16 |
| MES | 15 | eod * | -0.152 | -0.307 .. +0.003 | -2.8% | -0.303 | 0.054 | 1 | 11/16 |
| MES | 60 | h1 * | -0.023 | -0.049 .. +0.002 | -4.5% | -0.018 | 0.099 | 1 | 12/16 |
| MES | 60 | h2 | -0.005 | -0.044 .. +0.034 | -0.7% | -0.014 | 0.95 |  | 8/16 |
| MES | 60 | h4 | -0.014 | -0.067 .. +0.040 | -1.3% | +0.003 | 0.61 |  | 8/16 |
| MES | 60 | h8 | +0.017 | -0.055 .. +0.090 | +1.2% | +0.026 | 0.64 |  | 6/16 |
| MES | 60 | h16 | -0.035 | -0.121 .. +0.051 | -1.7% | -0.023 | 0.46 |  | 9/16 |
| MES | 60 | eod | -0.032 | -0.121 .. +0.058 | -1.5% | -0.007 | 0.54 |  | 9/16 |
| MNQ | 5 | h1 | -0.008 | -0.013 .. -0.003 | -1.6% | -0.013 | 0.023 |  | 13/16 |
| MNQ | 5 | h2 | -0.012 | -0.021 .. -0.003 | -1.6% | -0.017 | 0.041 |  | 14/16 |
| MNQ | 5 | h4 | -0.016 | -0.031 .. -0.002 | -1.5% | -0.033 | 0.068 |  | 12/16 |
| MNQ | 5 | h8 | -0.039 | -0.064 .. -0.013 | -2.4% | -0.077 | 0.0057 |  | 13/16 |
| MNQ | 5 | h16 | -0.061 | -0.105 .. -0.018 | -2.5% | -0.159 | 0.011 |  | 12/16 |
| MNQ | 5 | eod * | -0.669 | -0.909 .. -0.429 | -5.3% | -1.304 | 4.7e-08 | 1.29e-05 | 15/16 |
| MNQ | 15 | h1 | -0.006 | -0.016 .. +0.005 | -1.0% | -0.018 | 0.48 |  | 8/16 |
| MNQ | 15 | h2 | -0.026 | -0.043 .. -0.009 | -3.3% | -0.041 | 0.16 |  | 12/16 |
| MNQ | 15 | h4 | -0.039 | -0.072 .. -0.005 | -3.4% | -0.063 | 0.17 |  | 12/16 |
| MNQ | 15 | h8 | -0.059 | -0.111 .. -0.007 | -3.5% | -0.143 | 0.09 |  | 14/16 |
| MNQ | 15 | h16 | -0.069 | -0.130 .. -0.009 | -2.7% | -0.278 | 0.1 |  | 11/16 |
| MNQ | 15 | eod * | -0.355 | -0.579 .. -0.132 | -5.6% | -0.649 | 0.0028 | 0.439 | 11/16 |
| MNQ | 60 | h1 | -0.002 | -0.027 .. +0.023 | -0.3% | +0.017 | 0.9 |  | 7/16 |
| MNQ | 60 | h2 * | -0.029 | -0.065 .. +0.007 | -3.8% | -0.012 | 0.12 | 1 | 11/16 |
| MNQ | 60 | h4 | -0.019 | -0.075 .. +0.037 | -1.7% | +0.015 | 0.5 |  | 9/16 |
| MNQ | 60 | h8 | +0.005 | -0.069 .. +0.079 | +0.3% | +0.053 | 0.89 |  | 6/16 |
| MNQ | 60 | h16 | +0.007 | -0.071 .. +0.086 | +0.3% | +0.027 | 0.86 |  | 7/16 |
| MNQ | 60 | eod | +0.019 | -0.063 .. +0.101 | +0.8% | +0.041 | 0.66 |  | 8/16 |
| MYM | 5 | h1 | -0.015 | -0.022 .. -0.007 | -2.8% | -0.028 | 0.017 |  | 8/8 |
| MYM | 5 | h2 | -0.024 | -0.036 .. -0.011 | -3.1% | -0.043 | 0.043 |  | 8/8 |
| MYM | 5 | h4 | -0.041 | -0.062 .. -0.020 | -3.7% | -0.068 | 0.033 |  | 7/8 |
| MYM | 5 | h8 | -0.075 | -0.113 .. -0.038 | -4.7% | -0.131 | 0.0015 |  | 8/8 |
| MYM | 5 | h16 * | -0.105 | -0.160 .. -0.051 | -4.5% | -0.227 | 0.00019 | 0.0379 | 7/8 |
| MYM | 5 | eod | -0.410 | -0.686 .. -0.134 | -3.5% | -0.784 | 0.0037 |  | 8/8 |
| MYM | 15 | h1 | -0.015 | -0.030 .. -0.001 | -2.9% | -0.024 | 0.29 |  | 5/8 |
| MYM | 15 | h2 | -0.039 | -0.060 .. -0.018 | -5.1% | -0.048 | 0.11 |  | 7/8 |
| MYM | 15 | h4 | -0.064 | -0.101 .. -0.026 | -5.7% | -0.099 | 0.059 |  | 8/8 |
| MYM | 15 | h8 * | -0.125 | -0.185 .. -0.065 | -7.6% | -0.221 | 0.011 | 1 | 8/8 |
| MYM | 15 | h16 | -0.168 | -0.261 .. -0.075 | -6.8% | -0.359 | 0.012 |  | 7/8 |
| MYM | 15 | eod | -0.359 | -0.624 .. -0.093 | -6.0% | -0.502 | 0.016 |  | 8/8 |
| MYM | 60 | h1 * | -0.028 | -0.065 .. +0.010 | -5.3% | -0.016 | 0.15 | 1 | 6/8 |
| MYM | 60 | h2 | -0.019 | -0.067 .. +0.030 | -2.5% | -0.020 | 0.59 |  | 6/8 |
| MYM | 60 | h4 | -0.005 | -0.081 .. +0.071 | -0.5% | +0.037 | 0.91 |  | 4/8 |
| MYM | 60 | h8 | +0.026 | -0.078 .. +0.130 | +1.7% | +0.086 | 0.63 |  | 4/8 |
| MYM | 60 | h16 | -0.036 | -0.166 .. +0.094 | -1.7% | +0.061 | 0.59 |  | 5/8 |
| MYM | 60 | eod | -0.042 | -0.171 .. +0.086 | -1.9% | +0.050 | 0.52 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.18 pts | -0.76 .. +0.40 | 0.59 |
| MES | 15 | +1.16 pts | +0.08 .. +2.23 | 0.036 |
| MES | 60 | +2.13 pts | -0.25 .. +4.51 | 0.12 |
| MNQ | 5 | +0.61 pts | +0.12 .. +1.09 | 0.019 |
| MNQ | 15 | +0.65 pts | -0.24 .. +1.54 | 0.15 |
| MNQ | 60 | +2.57 pts | +0.53 .. +4.61 | 0.02 |
| MYM | 5 | +0.69 pts | +0.02 .. +1.37 | 0.062 |
| MYM | 15 | +0.15 pts | -1.19 .. +1.49 | 0.87 |
| MYM | 60 | -0.51 pts | -3.21 .. +2.19 | 0.72 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 25604 | +0.011 | 0.325 | +0.10 | -3.40 | -3.43 | -3.38 | -3.49 |
| MES | 5 | h2 | event | against signal | 25604 | +0.013 | 0.325 | +0.22 | -3.28 | -3.45 | -3.11 | -3.41 |
| MES | 5 | h4 | event | against signal | 25604 | +0.011 | 0.325 | +0.31 | -3.19 | -3.49 | -2.91 | -3.33 |
| MES | 5 | h8 | event | with signal | 25604 | +0.012 | 0.325 | -0.29 | -3.79 | -3.25 | -4.31 | -3.67 |
| MES | 5 | h16 | event | with signal | 25604 | +0.029 | 0.325 | -0.24 | -3.74 | -3.15 | -4.32 | -3.61 |
| MES | 5 | eod | event | with signal | 25604 | +0.112 | 0.325 | +0.81 | -2.69 | -3.48 | -1.93 | -2.21 |
| MES | 15 | h1 | event | with signal | 7831 | -0.006 | 0.199 | -0.10 | -3.60 | -3.75 | -3.43 | -3.47 |
| MES | 15 | h2 | event | with signal | 7831 | +0.004 | 0.199 | -0.08 | -3.58 | -3.77 | -3.38 | -3.43 |
| MES | 15 | h4 | event | with signal | 7831 | +0.014 | 0.199 | -0.38 | -3.88 | -3.67 | -4.09 | -3.72 |
| MES | 15 | h8 | event | with signal | 7831 | +0.033 | 0.199 | -0.54 | -4.04 | -3.37 | -4.75 | -3.81 |
| MES | 15 | h16 | event | with signal | 7831 | +0.005 | 0.199 | -0.74 | -4.24 | -3.21 | -5.34 | -3.85 |
| MES | 15 | eod | event | against signal | 7831 | +0.137 | 0.199 | +2.39 | -1.11 | -3.34 | +1.26 | -1.80 |
| MES | 60 | h1 | event | with signal | 1608 | +0.027 | 0.095 | +0.93 | -2.57 | -2.66 | -2.48 | -2.57 |
| MES | 60 | h2 | event | with signal | 1608 | +0.013 | 0.095 | +0.81 | -2.69 | -2.81 | -2.56 | -2.58 |
| MES | 60 | h4 | event | with signal | 1608 | +0.071 | 0.095 | +2.49 | -1.01 | -1.98 | +0.00 | -0.85 |
| MES | 60 | h8 | event | with signal | 1608 | +0.042 | 0.095 | +2.06 | -1.44 | -2.52 | -0.31 | -1.13 |
| MES | 60 | h16 | event | with signal | 1608 | +0.063 | 0.095 | +3.93 | +0.43 | -3.41 | +4.46 | +0.50 |
| MES | 60 | eod | event | with signal | 1608 | +0.040 | 0.095 | +3.50 | -0.00 | -3.60 | +3.78 | +0.06 |
| MNQ | 5 | h1 | event | with signal | 36547 | +0.002 | 0.118 | -0.05 | -2.05 | -2.00 | -2.08 | -1.97 |
| MNQ | 5 | h2 | event | against signal | 36547 | +0.012 | 0.118 | +0.41 | -1.59 | -1.97 | -1.31 | -1.73 |
| MNQ | 5 | h4 | event | against signal | 36547 | +0.014 | 0.118 | +0.40 | -1.60 | -1.99 | -1.31 | -1.72 |
| MNQ | 5 | h8 | event | against signal | 36547 | +0.012 | 0.118 | +0.44 | -1.56 | -2.05 | -1.20 | -1.60 |
| MNQ | 5 | h16 | event | with signal | 36547 | -0.002 | 0.118 | -0.26 | -2.26 | -1.84 | -2.57 | -2.23 |
| MNQ | 5 | eod | event | with signal | 36547 | +0.012 | 0.118 | +1.00 | -1.00 | -2.06 | -0.22 | +0.59 |
| MNQ | 15 | h1 | event | against signal | 10871 | +0.005 | 0.068 | +0.05 | -1.95 | -1.80 | -2.07 | -2.04 |
| MNQ | 15 | h2 | event | with signal | 10871 | +0.016 | 0.068 | +0.74 | -1.26 | -2.15 | -0.58 | -1.23 |
| MNQ | 15 | h4 | event | with signal | 10871 | +0.003 | 0.068 | +0.31 | -1.69 | -2.42 | -1.12 | -1.69 |
| MNQ | 15 | h8 | event | against signal | 10871 | +0.013 | 0.068 | +0.64 | -1.36 | -1.71 | -1.10 | -1.28 |
| MNQ | 15 | h16 | event | against signal | 10871 | +0.022 | 0.068 | +0.82 | -1.18 | -1.61 | -0.85 | -1.46 |
| MNQ | 15 | eod | event | against signal | 10871 | +0.174 | 0.068 | +3.09 | +1.09 | -2.24 | +3.65 | +0.34 |
| MNQ | 60 | h1 | event | with signal | 2066 | +0.020 | 0.033 | +0.84 | -1.16 | -1.61 | -0.79 | -1.20 |
| MNQ | 60 | h2 | event | with signal | 2066 | +0.036 | 0.033 | +1.21 | -0.79 | -0.86 | -0.74 | -0.65 |
| MNQ | 60 | h4 | event | with signal | 2066 | +0.074 | 0.033 | +3.49 | +1.49 | -0.43 | +3.07 | +1.75 |
| MNQ | 60 | h8 | event | with signal | 2066 | +0.066 | 0.033 | +2.61 | +0.61 | +0.16 | +0.98 | +1.03 |
| MNQ | 60 | h16 | event | with signal | 2066 | +0.051 | 0.033 | +2.17 | +0.17 | -0.21 | +0.49 | +0.45 |
| MNQ | 60 | eod | event | with signal | 2066 | +0.028 | 0.033 | +1.10 | -0.90 | -0.35 | -1.35 | -0.51 |
| MYM | 5 | h1 | event | with signal | 19473 | +0.001 | 0.169 | +0.11 | -1.89 | +nan | -1.89 | -1.82 |
| MYM | 5 | h2 | event | with signal | 19473 | +0.007 | 0.169 | +0.07 | -1.93 | +nan | -1.93 | -1.83 |
| MYM | 5 | h4 | event | with signal | 19473 | +0.008 | 0.169 | +0.21 | -1.79 | +nan | -1.79 | -1.65 |
| MYM | 5 | h8 | event | against signal | 19473 | +0.014 | 0.169 | -0.03 | -2.03 | +nan | -2.03 | -2.21 |
| MYM | 5 | h16 | event | with signal | 19473 | -0.009 | 0.169 | +0.23 | -1.77 | +nan | -1.77 | -1.51 |
| MYM | 5 | eod | event | with signal | 19473 | +0.190 | 0.169 | -0.16 | -2.16 | +nan | -2.16 | -1.63 |
| MYM | 15 | h1 | event | with signal | 5562 | +0.008 | 0.096 | -0.06 | -2.06 | +nan | -2.06 | -1.92 |
| MYM | 15 | h2 | event | with signal | 5562 | +0.017 | 0.096 | +0.29 | -1.71 | +nan | -1.71 | -1.56 |
| MYM | 15 | h4 | event | with signal | 5562 | +0.052 | 0.096 | +0.98 | -1.02 | +nan | -1.02 | -0.85 |
| MYM | 15 | h8 | event | with signal | 5562 | +0.039 | 0.096 | +0.60 | -1.40 | +nan | -1.40 | -1.12 |
| MYM | 15 | h16 | event | with signal | 5562 | +0.054 | 0.096 | +1.02 | -0.98 | +nan | -0.98 | -0.62 |
| MYM | 15 | eod | event | with signal | 5562 | +0.044 | 0.096 | -0.77 | -2.77 | +nan | -2.77 | -1.79 |
| MYM | 60 | h1 | event | with signal | 1048 | +0.000 | 0.045 | +0.56 | -1.44 | +nan | -1.44 | -1.47 |
| MYM | 60 | h2 | event | against signal | 1048 | +0.026 | 0.045 | -0.15 | -2.15 | +nan | -2.15 | -2.41 |
| MYM | 60 | h4 | event | against signal | 1048 | +0.047 | 0.045 | +0.16 | -1.84 | +nan | -1.84 | -2.33 |
| MYM | 60 | h8 | event | against signal | 1048 | +0.033 | 0.045 | -1.92 | -3.92 | +nan | -3.92 | -4.70 |
| MYM | 60 | h16 | event | against signal | 1048 | +0.028 | 0.045 | -0.89 | -2.89 | +nan | -2.89 | -3.29 |
| MYM | 60 | eod | event | with signal | 1048 | -0.020 | 0.045 | +1.36 | -0.64 | +nan | -0.64 | -0.25 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.607 | +0.734 | +0.676 | +0.579 | -0.383 | +0.000 | -0.016 | -0.018 | -0.016 | +0.009 | +0.031 |
| MES | 15 | +0.697 | +0.789 | +0.718 | +0.598 | -0.330 | +0.000 | -0.005 | +0.005 | +0.018 | +0.050 | +0.043 |
| MES | 60 | +0.963 | +0.805 | +0.755 | +0.645 | -0.277 | +0.000 | +0.027 | +0.011 | +0.091 | +0.023 | +0.179 |
| MNQ | 5 | +0.674 | +0.828 | +0.758 | +0.637 | -0.344 | +0.000 | +0.002 | -0.012 | -0.013 | -0.010 | +0.002 |
| MNQ | 15 | +0.767 | +0.845 | +0.785 | +0.644 | -0.300 | +0.000 | -0.006 | +0.017 | +0.011 | +0.009 | +0.016 |
| MNQ | 60 | +0.983 | +0.899 | +0.820 | +0.668 | -0.264 | +0.000 | +0.022 | +0.036 | +0.093 | +0.071 | -0.048 |
| MYM | 5 | +0.676 | +0.798 | +0.736 | +0.627 | -0.329 | +0.000 | -0.000 | +0.007 | +0.011 | -0.009 | +0.002 |
| MYM | 15 | +0.771 | +0.856 | +0.779 | +0.647 | -0.290 | +0.000 | +0.011 | +0.022 | +0.062 | +0.049 | +0.081 |
| MYM | 60 | +1.064 | +0.969 | +0.865 | +0.707 | -0.258 | +0.000 | +0.002 | -0.029 | -0.034 | -0.046 | +0.120 |

## Calibration

- MES 5-min: 1036271 bars, 25604 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 7831 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 1608 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 36547 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 10871 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 2066 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 19473 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 5562 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1048 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 38962 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
