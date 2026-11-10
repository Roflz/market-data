# Impact card: dist_vwap

(close - VWAP) in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.020 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.017 R20, CONFIRMED, q=8.16e-11, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.222 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.013 R20 over the next 2 bars (30 min), p=0.82; we would catch an effect of 0.048 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.046 R20, CONFIRMED, q=7.5e-21, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.18 at recent bar sizes, 90% range up to $1.27); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.016 R20 over the next 1 bar (1 h), p=0.84; we would catch an effect of 0.086 R20 or more 80% of the time).
- MES 60-min size: the market moves 17% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.088 R20, CONFIRMED, q=3.74e-20, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.44 at recent bar sizes, 90% range up to $3.63); about 1.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.011 R20 over the next 2 bars (10 min), p=0.72; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.016 R20, CONFIRMED, q=0.00234, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.14 at recent bar sizes, 90% range up to $0.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.613 R20 over the rest of the session (to 16:45), p=0.96; we would catch an effect of 0.068 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.047 R20, CONFIRMED, q=1.57e-08, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $13.80 at recent bar sizes, 90% range up to $2.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.052 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.094 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 15% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.080 R20, CONFIRMED, q=5.21e-16, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.32 at recent bar sizes, 90% range up to $5.79); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.089 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.019 R20, possible, q=0.156, 6 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.86 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.168 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.051 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.107 R20 or more 80% of the time).
- MYM 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.053 R20, CONFIRMED, q=7.23e-05, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.54 at recent bar sizes, 90% range up to $2.36); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.018 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.131 R20 or more 80% of the time).
- MYM 60-min size: the market moves 15% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.077 R20, CONFIRMED, q=1.21e-07, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.38 at recent bar sizes, 90% range up to $3.22); about 3.8x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.006 .. +0.002 | -0.0038 | 0.31 / 0.32 / 0.34 | 0.342 |  |  | 9/16 | -0.006 | +0.002 |  | -0.9 / -1.0 |  |
| MES | 5 | h2 | +0.002 | -0.006 .. +0.009 | -0.0011 | 0.7 / 0.7 / 0.73 | 0.73 |  |  | 8/16 | -0.011 | +0.014 |  | +0.4 / +0.4 |  |
| MES | 5 | h4 | +0.009 | -0.007 .. +0.025 | +0.0022 | 0.25 / 0.26 / 0.29 | 0.288 |  |  | 9/16 | -0.014 | +0.033 |  | +1.8 / +1.2 | 0.025 |
| MES | 5 | h8 * | +0.020 | -0.011 .. +0.052 | +0.0032 | 0.21 / 0.22 / 0.25 | 0.246 | 1 | 1 | 11/16 | -0.024 | +0.064 | False | +2.7 / +1.3 |  |
| MES | 5 | h16 | +0.042 | -0.019 .. +0.102 | +0.0063 | 0.18 / 0.19 / 0.23 | 0.222 |  |  | 11/16 | -0.032 | +0.115 |  | +3.9 / +1.4 |  |
| MES | 5 | eod | +0.271 | -0.599 .. +1.141 | +0.0194 | 0.54 / 0.53 / 0.44 | 0.44 |  |  | 7/16 | +0.298 | +0.245 |  | +5.3 / +0.6 |  |
| MES | 15 | h1 | +0.003 | -0.007 .. +0.012 | -0.0026 | 0.57 / 0.56 / 0.54 | 0.548 |  |  | 8/16 | -0.006 | +0.011 |  | +0.6 / +0.6 |  |
| MES | 15 | h2 * | +0.013 | -0.002 .. +0.028 | +0.0027 | 0.089 / 0.1 / 0.14 | 0.134 | 1 | 1 | 11/16 | -0.007 | +0.033 | False | +1.7 / +1.7 |  |
| MES | 15 | h4 | +0.021 | -0.008 .. +0.051 | +0.0057 | 0.15 / 0.17 / 0.21 | 0.209 |  |  | 10/16 | -0.021 | +0.063 |  | +1.9 / +1.4 | 0.048 |
| MES | 15 | h8 | +0.043 | -0.014 .. +0.101 | +0.0080 | 0.14 / 0.16 / 0.18 | 0.173 |  |  | 9/16 | -0.031 | +0.117 |  | +2.8 / +1.5 |  |
| MES | 15 | h16 | +0.075 | -0.050 .. +0.200 | +0.0151 | 0.24 / 0.25 / 0.22 | 0.223 |  |  | 8/16 | -0.073 | +0.223 |  | +3.5 / +1.2 |  |
| MES | 15 | eod | +0.315 | -0.316 .. +0.945 | +0.0319 | 0.33 / 0.31 / 0.14 | 0.142 |  |  | 10/16 | +0.121 | +0.507 |  | +5.7 / +1.0 |  |
| MES | 60 | h1 * | +0.016 | -0.001 .. +0.034 | +0.0084 | 0.072 / 0.08 / 0.11 | 0.116 | 1 | 1 | 9/16 | +0.001 | +0.032 | False | +1.6 / +1.8 |  |
| MES | 60 | h2 | +0.020 | -0.012 .. +0.052 | +0.0084 | 0.21 / 0.22 / 0.26 | 0.265 |  |  | 9/16 | +0.001 | +0.039 |  | +1.4 / +1.2 |  |
| MES | 60 | h4 | +0.047 | -0.005 .. +0.099 | +0.0109 | 0.077 / 0.086 / 0.13 | 0.131 |  |  | 9/16 | +0.005 | +0.089 |  | +2.4 / +1.8 | 0.086 |
| MES | 60 | h8 | +0.060 | -0.024 .. +0.144 | +0.0097 | 0.16 / 0.17 / 0.21 | 0.214 |  |  | 9/16 | +0.023 | +0.097 |  | +2.3 / +1.4 |  |
| MES | 60 | h16 | +0.048 | -0.065 .. +0.161 | +0.0059 | 0.41 / 0.41 / 0.44 | 0.439 |  |  | 9/16 | +0.015 | +0.080 |  | +1.6 / +0.8 |  |
| MES | 60 | eod | +0.067 | -0.049 .. +0.183 | +0.0067 | 0.26 / 0.26 / 0.29 | 0.289 |  |  | 9/16 | +0.035 | +0.099 |  | +2.2 / +1.1 |  |
| MNQ | 5 | h1 | +0.003 | -0.002 .. +0.009 | +0.0012 | 0.19 / 0.21 / 0.22 | 0.222 |  |  | 10/16 | -0.004 | +0.011 |  | +1.0 / +1.3 |  |
| MNQ | 5 | h2 * | +0.011 | -0.001 .. +0.023 | +0.0039 | 0.072 / 0.076 / 0.068 | 0.0703 | 1 | 1 | 9/16 | -0.008 | +0.030 | False | +1.9 / +1.8 |  |
| MNQ | 5 | h4 | +0.021 | -0.005 .. +0.047 | +0.0061 | 0.12 / 0.11 / 0.093 | 0.0985 |  |  | 8/16 | -0.016 | +0.058 |  | +2.3 / +1.6 | 0.030 |
| MNQ | 5 | h8 | +0.016 | -0.027 .. +0.058 | +0.0026 | 0.47 / 0.48 / 0.54 | 0.54 |  |  | 8/16 | -0.037 | +0.068 |  | +1.2 / +0.7 |  |
| MNQ | 5 | h16 | +0.009 | -0.076 .. +0.094 | -0.0016 | 0.83 / 0.84 / 0.85 | 0.858 |  |  | 8/16 | -0.053 | +0.071 |  | +0.5 / +0.2 |  |
| MNQ | 5 | eod | +0.430 | -0.774 .. +1.634 | +0.0221 | 0.48 / 0.47 / 0.36 | 0.36 |  |  | 7/16 | +0.070 | +0.787 |  | +5.7 / +0.7 |  |
| MNQ | 15 | h1 | +0.004 | -0.011 .. +0.020 | -0.0016 | 0.56 / 0.56 / 0.47 | 0.485 |  |  | 8/16 | -0.000 | +0.009 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h2 | +0.013 | -0.009 .. +0.035 | +0.0017 | 0.23 / 0.24 / 0.31 | 0.324 |  |  | 10/16 | +0.001 | +0.026 |  | +1.1 / +1.2 |  |
| MNQ | 15 | h4 | +0.023 | -0.021 .. +0.067 | +0.0007 | 0.31 / 0.32 / 0.41 | 0.408 |  |  | 10/16 | +0.001 | +0.044 |  | +1.0 / +1.0 | 0.068 |
| MNQ | 15 | h8 | +0.029 | -0.047 .. +0.106 | -0.0008 | 0.45 / 0.46 / 0.54 | 0.541 |  |  | 8/16 | -0.016 | +0.074 |  | +1.1 / +0.7 |  |
| MNQ | 15 | h16 | +0.094 | -0.055 .. +0.243 | +0.0110 | 0.22 / 0.23 / 0.23 | 0.234 |  |  | 10/16 | -0.081 | +0.268 |  | +3.0 / +1.2 |  |
| MNQ | 15 | eod * | +0.613 | -0.241 .. +1.468 | +0.0359 | 0.16 / 0.15 / 0.035 | 0.0294 | 1 | 1 | 11/16 | +0.261 | +0.964 | False | +6.7 / +1.4 |  |
| MNQ | 60 | h1 | +0.011 | -0.009 .. +0.031 | +0.0086 | 0.29 / 0.3 / 0.32 | 0.326 |  |  | 10/16 | -0.005 | +0.027 |  | +1.0 / +1.1 |  |
| MNQ | 60 | h2 | +0.013 | -0.023 .. +0.048 | +0.0086 | 0.49 / 0.49 / 0.52 | 0.529 |  |  | 9/16 | -0.019 | +0.044 |  | +0.8 / +0.7 |  |
| MNQ | 60 | h4 | +0.031 | -0.027 .. +0.089 | +0.0092 | 0.29 / 0.31 / 0.36 | 0.366 |  |  | 9/16 | -0.023 | +0.085 |  | +1.5 / +1.1 | 0.094 |
| MNQ | 60 | h8 * | +0.052 | -0.038 .. +0.141 | +0.0095 | 0.26 / 0.27 / 0.31 | 0.317 | 1 | 1 | 10/16 | -0.010 | +0.114 | False | +1.9 / +1.1 |  |
| MNQ | 60 | h16 | +0.056 | -0.061 .. +0.174 | +0.0100 | 0.35 / 0.36 / 0.39 | 0.389 |  |  | 9/16 | +0.010 | +0.103 |  | +1.8 / +0.9 |  |
| MNQ | 60 | eod | +0.062 | -0.059 .. +0.183 | +0.0093 | 0.32 / 0.33 / 0.35 | 0.354 |  |  | 9/16 | +0.017 | +0.107 |  | +2.0 / +1.0 |  |
| MYM | 5 | h1 | -0.001 | -0.010 .. +0.007 | +0.0014 | 0.78 / 0.79 / 0.82 | 0.832 |  |  | 5/8 | n/a | -0.001 |  | -0.2 / -0.3 |  |
| MYM | 5 | h2 | +0.006 | -0.021 .. +0.032 | +0.0074 | 0.69 / 0.69 / 0.55 | 0.548 |  |  | 2/8 | n/a | +0.006 |  | +0.6 / +0.4 |  |
| MYM | 5 | h4 | +0.023 | -0.043 .. +0.089 | +0.0135 | 0.49 / 0.48 / 0.26 | 0.261 |  |  | 2/8 | n/a | +0.023 |  | +1.5 / +0.7 | 0.048 |
| MYM | 5 | h8 | +0.053 | -0.056 .. +0.163 | +0.0145 | 0.34 / 0.34 / 0.16 | 0.161 |  |  | 3/8 | n/a | +0.053 |  | +2.4 / +0.9 |  |
| MYM | 5 | h16 * | +0.089 | -0.087 .. +0.265 | +0.0170 | 0.32 / 0.32 / 0.17 | 0.174 | 1 | 1 | 4/8 | n/a | +0.089 | False | +3.3 / +1.0 |  |
| MYM | 5 | eod | +0.157 | -1.444 .. +1.757 | +0.0201 | 0.85 / 0.85 / 0.79 | 0.811 |  |  | 3/8 | n/a | +0.157 |  | +1.6 / +0.2 |  |
| MYM | 15 | h1 | -0.004 | -0.018 .. +0.010 | +0.0004 | 0.59 / 0.62 / 0.64 | 0.639 |  |  | 5/8 | n/a | -0.004 |  | -0.4 / -0.5 |  |
| MYM | 15 | h2 | +0.020 | -0.018 .. +0.058 | +0.0100 | 0.31 / 0.32 / 0.29 | 0.3 |  |  | 3/8 | n/a | +0.020 |  | +1.1 / +1.0 |  |
| MYM | 15 | h4 * | +0.051 | -0.031 .. +0.133 | +0.0129 | 0.22 / 0.24 / 0.18 | 0.201 | 1 | 1 | 5/8 | n/a | +0.051 | False | +1.6 / +1.2 | 0.107 |
| MYM | 15 | h8 | +0.085 | -0.079 .. +0.249 | +0.0193 | 0.31 / 0.32 / 0.19 | 0.193 |  |  | 4/8 | n/a | +0.085 |  | +2.2 / +1.0 |  |
| MYM | 15 | h16 | +0.200 | -0.211 .. +0.611 | +0.0395 | 0.34 / 0.35 / 0.1 | 0.106 |  |  | 3/8 | n/a | +0.200 |  | +3.7 / +1.0 |  |
| MYM | 15 | eod | +0.478 | -0.733 .. +1.690 | +0.0409 | 0.44 / 0.44 / 0.2 | 0.198 |  |  | 3/8 | n/a | +0.478 |  | +3.8 / +0.8 |  |
| MYM | 60 | h1 * | +0.018 | -0.006 .. +0.043 | +0.0068 | 0.15 / 0.19 / 0.24 | 0.236 | 1 | 1 | 6/8 | n/a | +0.018 | False | +1.2 / +1.5 |  |
| MYM | 60 | h2 | +0.027 | -0.018 .. +0.072 | +0.0060 | 0.24 / 0.28 / 0.33 | 0.323 |  |  | 6/8 | n/a | +0.027 |  | +1.2 / +1.2 |  |
| MYM | 60 | h4 | +0.050 | -0.032 .. +0.133 | +0.0075 | 0.23 / 0.24 / 0.29 | 0.275 |  |  | 7/8 | n/a | +0.050 |  | +1.7 / +1.2 | 0.131 |
| MYM | 60 | h8 | +0.035 | -0.099 .. +0.170 | +0.0045 | 0.61 / 0.61 / 0.63 | 0.616 |  |  | 5/8 | n/a | +0.035 |  | +0.9 / +0.5 |  |
| MYM | 60 | h16 | +0.030 | -0.139 .. +0.200 | -0.0003 | 0.73 / 0.72 / 0.74 | 0.742 |  |  | 4/8 | n/a | +0.030 |  | +0.7 / +0.4 |  |
| MYM | 60 | eod | +0.039 | -0.134 .. +0.211 | +0.0001 | 0.66 / 0.66 / 0.67 | 0.682 |  |  | 4/8 | n/a | +0.039 |  | +0.9 / +0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.017 | -0.021 .. -0.012 | -3.3% | -0.023 | 2.1e-13 | 8.16e-11 | 12/16 |
| MES | 5 | h2 | -0.023 | -0.031 .. -0.016 | -3.3% | -0.035 | 2e-09 |  | 12/16 |
| MES | 5 | h4 | -0.032 | -0.047 .. -0.017 | -3.2% | -0.052 | 4.7e-05 |  | 12/16 |
| MES | 5 | h8 | -0.038 | -0.066 .. -0.010 | -2.7% | -0.071 | 0.0076 |  | 10/16 |
| MES | 5 | h16 | -0.056 | -0.105 .. -0.008 | -2.7% | -0.095 | 0.023 |  | 12/16 |
| MES | 5 | eod | +0.086 | -0.515 .. +0.687 | +0.9% | +0.015 | 0.78 |  | 11/16 |
| MES | 15 | h1 * | -0.046 | -0.056 .. -0.037 | -9.1% | -0.096 | 1.2e-23 | 7.5e-21 | 15/16 |
| MES | 15 | h2 | -0.061 | -0.081 .. -0.041 | -8.4% | -0.130 | 1.9e-09 |  | 14/16 |
| MES | 15 | h4 | -0.078 | -0.117 .. -0.038 | -7.4% | -0.167 | 0.00014 |  | 13/16 |
| MES | 15 | h8 | -0.098 | -0.163 .. -0.032 | -6.4% | -0.216 | 0.0033 |  | 11/16 |
| MES | 15 | h16 | -0.115 | -0.220 .. -0.010 | -5.0% | -0.289 | 0.032 |  | 10/16 |
| MES | 15 | eod | -0.182 | -0.685 .. +0.322 | -3.3% | -0.438 | 0.48 |  | 6/16 |
| MES | 60 | h1 * | -0.088 | -0.106 .. -0.071 | -17.2% | -0.183 | 6.4e-23 | 3.74e-20 | 16/16 |
| MES | 60 | h2 | -0.101 | -0.126 .. -0.076 | -13.7% | -0.229 | 1.4e-15 |  | 16/16 |
| MES | 60 | h4 | -0.125 | -0.164 .. -0.086 | -11.9% | -0.279 | 2.8e-10 |  | 15/16 |
| MES | 60 | h8 | -0.143 | -0.201 .. -0.086 | -9.5% | -0.312 | 2e-06 |  | 15/16 |
| MES | 60 | h16 | -0.101 | -0.177 .. -0.024 | -4.9% | -0.285 | 0.0096 |  | 13/16 |
| MES | 60 | eod | -0.105 | -0.183 .. -0.027 | -4.8% | -0.288 | 0.0085 |  | 12/16 |
| MNQ | 5 | h1 * | -0.016 | -0.023 .. -0.009 | -2.9% | -0.022 | 1e-05 | 0.00234 | 13/16 |
| MNQ | 5 | h2 | -0.023 | -0.040 .. -0.006 | -3.0% | -0.035 | 0.0084 |  | 13/16 |
| MNQ | 5 | h4 | -0.032 | -0.066 .. +0.002 | -2.9% | -0.054 | 0.069 |  | 11/16 |
| MNQ | 5 | h8 | -0.044 | -0.105 .. +0.017 | -2.7% | -0.084 | 0.16 |  | 9/16 |
| MNQ | 5 | h16 | -0.053 | -0.149 .. +0.042 | -2.2% | -0.126 | 0.27 |  | 9/16 |
| MNQ | 5 | eod | +0.211 | -0.729 .. +1.150 | +1.7% | +0.134 | 0.83 |  | 10/16 |
| MNQ | 15 | h1 * | -0.047 | -0.060 .. -0.033 | -8.7% | -0.096 | 4.7e-11 | 1.57e-08 | 14/16 |
| MNQ | 15 | h2 | -0.067 | -0.103 .. -0.031 | -8.6% | -0.143 | 0.00027 |  | 14/16 |
| MNQ | 15 | h4 | -0.094 | -0.185 .. -0.004 | -8.3% | -0.212 | 0.041 |  | 13/16 |
| MNQ | 15 | h8 | -0.119 | -0.275 .. +0.038 | -7.1% | -0.311 | 0.14 |  | 12/16 |
| MNQ | 15 | h16 | -0.110 | -0.288 .. +0.069 | -4.3% | -0.448 | 0.23 |  | 7/16 |
| MNQ | 15 | eod | -0.337 | -1.187 .. +0.514 | -5.3% | -0.574 | 0.44 |  | 8/16 |
| MNQ | 60 | h1 * | -0.080 | -0.098 .. -0.062 | -15.2% | -0.170 | 1e-18 | 5.21e-16 | 14/16 |
| MNQ | 60 | h2 | -0.094 | -0.120 .. -0.067 | -12.2% | -0.205 | 3.1e-12 |  | 15/16 |
| MNQ | 60 | h4 | -0.108 | -0.148 .. -0.068 | -9.8% | -0.234 | 1.1e-07 |  | 15/16 |
| MNQ | 60 | h8 | -0.118 | -0.174 .. -0.062 | -7.5% | -0.248 | 0.00014 |  | 13/16 |
| MNQ | 60 | h16 | -0.087 | -0.161 .. -0.013 | -4.0% | -0.221 | 0.025 |  | 12/16 |
| MNQ | 60 | eod | -0.092 | -0.169 .. -0.015 | -4.0% | -0.223 | 0.022 |  | 12/16 |
| MYM | 5 | h1 * | -0.019 | -0.030 .. -0.008 | -3.6% | -0.026 | 0.0009 | 0.156 | 6/8 |
| MYM | 5 | h2 | -0.029 | -0.058 .. -0.000 | -3.8% | -0.044 | 0.048 |  | 4/8 |
| MYM | 5 | h4 | -0.051 | -0.119 .. +0.017 | -4.7% | -0.076 | 0.14 |  | 4/8 |
| MYM | 5 | h8 | -0.083 | -0.202 .. +0.035 | -5.2% | -0.127 | 0.17 |  | 4/8 |
| MYM | 5 | h16 | -0.099 | -0.281 .. +0.082 | -4.3% | -0.206 | 0.29 |  | 3/8 |
| MYM | 5 | eod | -0.029 | -1.161 .. +1.104 | -0.2% | -0.099 | 0.96 |  | 2/8 |
| MYM | 15 | h1 * | -0.053 | -0.073 .. -0.033 | -9.9% | -0.101 | 2.8e-07 | 7.23e-05 | 8/8 |
| MYM | 15 | h2 | -0.087 | -0.143 .. -0.031 | -11.3% | -0.163 | 0.0025 |  | 7/8 |
| MYM | 15 | h4 | -0.137 | -0.263 .. -0.010 | -12.3% | -0.261 | 0.036 |  | 5/8 |
| MYM | 15 | h8 | -0.189 | -0.395 .. +0.017 | -11.5% | -0.436 | 0.076 |  | 5/8 |
| MYM | 15 | h16 | -0.308 | -0.690 .. +0.074 | -12.5% | -0.690 | 0.12 |  | 5/8 |
| MYM | 15 | eod | -0.575 | -1.626 .. +0.475 | -9.6% | -1.023 | 0.3 |  | 5/8 |
| MYM | 60 | h1 * | -0.077 | -0.102 .. -0.053 | -14.8% | -0.154 | 3.8e-10 | 1.21e-07 | 8/8 |
| MYM | 60 | h2 | -0.093 | -0.130 .. -0.056 | -12.3% | -0.201 | 7.8e-07 |  | 7/8 |
| MYM | 60 | h4 | -0.113 | -0.172 .. -0.054 | -10.5% | -0.239 | 0.00031 |  | 7/8 |
| MYM | 60 | h8 | -0.108 | -0.198 .. -0.019 | -7.0% | -0.264 | 0.019 |  | 6/8 |
| MYM | 60 | h16 | -0.106 | -0.214 .. +0.002 | -5.0% | -0.263 | 0.055 |  | 6/8 |
| MYM | 60 | eod | -0.101 | -0.212 .. +0.009 | -4.5% | -0.267 | 0.072 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.35 pts | -0.88 .. +0.17 | 0.21 |
| MES | 15 | -0.46 pts | -1.30 .. +0.38 | 0.29 |
| MES | 60 | +1.02 pts | -0.32 .. +2.37 | 0.28 |
| MNQ | 5 | -0.25 pts | -0.82 .. +0.32 | 0.42 |
| MNQ | 15 | -0.62 pts | -1.51 .. +0.28 | 0.18 |
| MNQ | 60 | +0.66 pts | -0.72 .. +2.04 | 0.4 |
| MYM | 5 | -0.55 pts | -1.32 .. +0.22 | 0.16 |
| MYM | 15 | -0.30 pts | -1.49 .. +0.89 | 0.62 |
| MYM | 60 | +1.44 pts | -0.44 .. +3.31 | 0.25 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207255 | +0.006 | 0.278 | +0.07 | -3.43 | -3.45 | -3.42 | -3.47 |
| MES | 5 | h2 | top fifth | long | 207254 | +0.004 | 0.342 | +0.09 | -3.41 | -3.49 | -3.35 | -3.41 |
| MES | 5 | h4 | top fifth | long | 207254 | +0.013 | 0.342 | +0.23 | -3.27 | -3.42 | -3.16 | -3.32 |
| MES | 5 | h8 | top fifth | long | 207254 | +0.029 | 0.342 | +0.45 | -3.05 | -3.30 | -2.87 | -3.18 |
| MES | 5 | h16 | top fifth | long | 207254 | +0.067 | 0.342 | +0.85 | -2.65 | -3.06 | -2.33 | -2.95 |
| MES | 5 | eod | top fifth | long | 207254 | +0.481 | 0.342 | +4.06 | +0.56 | +1.20 | +0.08 | -1.75 |
| MES | 15 | h1 | top fifth | long | 68444 | +0.006 | 0.195 | +0.16 | -3.34 | -3.48 | -3.22 | -3.37 |
| MES | 15 | h2 | top fifth | long | 68444 | +0.014 | 0.195 | +0.32 | -3.18 | -3.39 | -3.00 | -3.27 |
| MES | 15 | h4 | top fifth | long | 68444 | +0.030 | 0.195 | +0.58 | -2.92 | -3.23 | -2.67 | -3.16 |
| MES | 15 | h8 | top fifth | long | 68444 | +0.062 | 0.195 | +1.09 | -2.41 | -2.80 | -2.09 | -2.88 |
| MES | 15 | h16 | top fifth | long | 68444 | +0.121 | 0.195 | +1.87 | -1.63 | -1.97 | -1.34 | -2.64 |
| MES | 15 | eod | top fifth | long | 68444 | +0.271 | 0.195 | +3.93 | +0.43 | +0.81 | +0.11 | -1.49 |
| MES | 60 | h1 | top fifth | long | 16683 | +0.020 | 0.094 | +0.68 | -2.82 | -3.15 | -2.52 | -3.07 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.032 | 0.094 | +1.12 | -2.38 | -2.75 | -2.04 | -2.87 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.069 | 0.094 | +2.36 | -1.14 | -1.77 | -0.56 | -2.08 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.101 | 0.094 | +3.62 | +0.12 | -0.51 | +0.69 | -1.41 |
| MES | 60 | h16 | top fifth | long | 16683 | +0.106 | 0.094 | +4.71 | +1.21 | +0.19 | +2.13 | -0.80 |
| MES | 60 | eod | top fifth | long | 16683 | +0.111 | 0.094 | +4.89 | +1.39 | +0.32 | +2.36 | -0.44 |
| MNQ | 5 | h1 | top fifth | long | 206905 | +0.007 | 0.147 | +0.12 | -1.88 | -1.98 | -1.80 | -1.92 |
| MNQ | 5 | h2 | top fifth | long | 206905 | +0.015 | 0.147 | +0.23 | -1.77 | -1.94 | -1.62 | -1.83 |
| MNQ | 5 | h4 | top fifth | long | 206905 | +0.028 | 0.147 | +0.47 | -1.53 | -1.85 | -1.22 | -1.65 |
| MNQ | 5 | h8 | top fifth | long | 206905 | +0.045 | 0.147 | +0.79 | -1.21 | -1.70 | -0.75 | -1.48 |
| MNQ | 5 | h16 | top fifth | long | 206905 | +0.079 | 0.147 | +1.43 | -0.57 | -1.41 | +0.23 | -1.14 |
| MNQ | 5 | eod | top fifth | long | 206905 | +0.950 | 0.147 | +5.74 | +3.74 | +1.93 | +5.45 | -0.29 |
| MNQ | 15 | h1 | top fifth | long | 68413 | +0.011 | 0.079 | +0.31 | -1.69 | -1.91 | -1.50 | -1.79 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.019 | 0.079 | +0.51 | -1.49 | -1.80 | -1.21 | -1.65 |
| MNQ | 15 | h4 | top fifth | long | 68413 | +0.038 | 0.079 | +1.04 | -0.96 | -1.55 | -0.43 | -1.29 |
| MNQ | 15 | h8 | top fifth | long | 68413 | +0.071 | 0.079 | +1.76 | -0.24 | -1.20 | +0.62 | -1.01 |
| MNQ | 15 | h16 | top fifth | long | 68413 | +0.138 | 0.079 | +3.38 | +1.38 | -0.67 | +3.24 | +0.10 |
| MNQ | 15 | eod | top fifth | long | 68413 | +0.503 | 0.079 | +5.95 | +3.95 | +2.13 | +5.61 | +1.77 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.024 | 0.037 | +0.93 | -1.07 | -1.51 | -0.67 | -1.53 |
| MNQ | 60 | h2 | top fifth | long | 16682 | +0.038 | 0.037 | +1.73 | -0.27 | -1.25 | +0.64 | -1.07 |
| MNQ | 60 | h4 | top fifth | long | 16682 | +0.074 | 0.037 | +3.72 | +1.72 | -0.64 | +3.90 | +0.24 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.106 | 0.037 | +4.98 | +2.98 | +0.24 | +5.51 | +0.75 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.131 | 0.037 | +6.02 | +4.02 | +0.96 | +6.85 | +1.78 |
| MNQ | 60 | eod | top fifth | long | 16682 | +0.133 | 0.037 | +5.90 | +3.90 | +1.03 | +6.55 | +1.98 |
| MYM | 5 | h1 | bottom fifth | long | 103808 | +0.000 | 0.152 | +0.05 | -1.95 | +nan | -1.95 | -1.95 |
| MYM | 5 | h2 | top fifth | long | 103808 | -0.003 | 0.188 | +0.02 | -1.98 | +nan | -1.98 | -1.96 |
| MYM | 5 | h4 | top fifth | long | 103808 | +0.000 | 0.188 | +0.10 | -1.90 | +nan | -1.90 | -1.90 |
| MYM | 5 | h8 | top fifth | long | 103808 | +0.009 | 0.188 | +0.27 | -1.73 | +nan | -1.73 | -1.81 |
| MYM | 5 | h16 | top fifth | long | 103808 | +0.028 | 0.188 | +0.45 | -1.55 | +nan | -1.55 | -1.84 |
| MYM | 5 | eod | top fifth | long | 103808 | +0.101 | 0.188 | +2.97 | +0.97 | +nan | +0.97 | -0.40 |
| MYM | 15 | h1 | bottom fifth | long | 34286 | +0.002 | 0.090 | +0.13 | -1.87 | +nan | -1.87 | -1.89 |
| MYM | 15 | h2 | top fifth | long | 34286 | +0.009 | 0.102 | +0.19 | -1.81 | +nan | -1.81 | -1.92 |
| MYM | 15 | h4 | top fifth | long | 34286 | +0.019 | 0.102 | +0.31 | -1.69 | +nan | -1.69 | -1.89 |
| MYM | 15 | h8 | top fifth | long | 34286 | +0.023 | 0.102 | +0.41 | -1.59 | +nan | -1.59 | -1.91 |
| MYM | 15 | h16 | top fifth | long | 34286 | +0.023 | 0.102 | +0.53 | -1.47 | +nan | -1.47 | -1.84 |
| MYM | 15 | eod | top fifth | long | 34286 | +0.112 | 0.102 | +3.08 | +1.08 | +nan | +1.08 | +0.14 |
| MYM | 60 | h1 | top fifth | long | 8331 | +0.014 | 0.048 | +0.44 | -1.56 | +nan | -1.56 | -1.77 |
| MYM | 60 | h2 | top fifth | long | 8331 | +0.016 | 0.048 | +0.65 | -1.35 | +nan | -1.35 | -1.64 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.030 | 0.048 | +1.10 | -0.90 | +nan | -0.90 | -1.48 |
| MYM | 60 | h8 | top fifth | long | 8331 | +0.049 | 0.048 | +2.05 | +0.05 | +nan | +0.05 | -1.11 |
| MYM | 60 | h16 | top fifth | long | 8331 | +0.068 | 0.048 | +3.83 | +1.83 | +nan | +1.83 | -0.32 |
| MYM | 60 | eod | top fifth | long | 8331 | +0.071 | 0.048 | +4.31 | +2.31 | +nan | +2.31 | +0.12 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.169 | -0.979 | -0.776 | -0.527 | -0.319 | +0.000 | -0.011 | -0.010 | -0.003 | +0.004 | +0.019 |
| MES | 15 | -2.789 | -2.275 | -1.649 | -1.052 | -0.612 | +0.000 | -0.005 | +0.001 | +0.005 | +0.020 | +0.028 |
| MES | 60 | -3.351 | -3.287 | -2.811 | -1.951 | -1.200 | +0.000 | +0.011 | +0.008 | +0.015 | -0.040 | -0.145 |
| MNQ | 5 | -1.295 | -1.078 | -0.847 | -0.573 | -0.344 | +0.000 | +0.000 | +0.006 | +0.016 | +0.011 | +0.006 |
| MNQ | 15 | -2.982 | -2.414 | -1.741 | -1.110 | -0.646 | +0.000 | +0.010 | +0.021 | +0.033 | +0.043 | +0.103 |
| MNQ | 60 | -3.514 | -3.396 | -2.891 | -2.006 | -1.237 | +0.000 | +0.009 | +0.002 | -0.003 | -0.060 | -0.018 |
| MYM | 5 | -1.082 | -0.930 | -0.759 | -0.518 | -0.312 | +0.000 | +0.000 | +0.003 | +0.014 | +0.035 | +0.068 |
| MYM | 15 | -2.766 | -2.237 | -1.611 | -1.027 | -0.596 | +0.000 | +0.009 | +0.034 | +0.070 | +0.108 | +0.250 |
| MYM | 60 | -3.511 | -3.403 | -2.866 | -1.948 | -1.179 | +0.000 | +0.020 | +0.022 | +0.034 | -0.019 | -0.184 |

## Calibration

- MES 5-min: 1036271 bars, 207254 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68444 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
