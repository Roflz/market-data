# Impact card: dist_swing_hi

(last swing high - close) in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.019 R20, CONFIRMED, q=4.17e-13, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.23 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.224 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.053 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.047 R20 or more 80% of the time).
- MES 15-min size: the market moves 5% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.026 R20, CONFIRMED, q=2.31e-07, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.82 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.021 R20 over the next 1 bar (1 h), p=0.092; we would catch an effect of 0.089 R20 or more 80% of the time).
- MES 60-min size: the market moves 8% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.043 R20, CONFIRMED, q=9.66e-06, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.61 at recent bar sizes, 90% range up to $3.56); about 1.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.009 R20 over the next 2 bars (10 min), p=0.95; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.023 R20, CONFIRMED, q=7.12e-08, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.12 at recent bar sizes, 90% range up to $0.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.534 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.059 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.027 R20, possible, q=0.0635, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $12.28 at recent bar sizes, 90% range up to $2.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.014 R20 over the next 1 bar (1 h), p=0.89; we would catch an effect of 0.095 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 6% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.034 R20, CONFIRMED, q=0.00309, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.63 at recent bar sizes, 90% range up to $6.04); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.056 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.047 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.028 R20, CONFIRMED, q=0.000206, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $0.51); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.023 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.079 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.03).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.25 at recent bar sizes, 90% range up to $2.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.129 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.027).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.26 at recent bar sizes, 90% range up to $3.83); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.003 | -0.002 .. +0.007 | +0.0010 | 0.2 / 0.2 / 0.22 | 0.215 | 1 | 1 | 11/16 | +0.006 | +0.000 | False | +1.2 / +1.3 |  |
| MES | 5 | h2 | +0.002 | -0.006 .. +0.010 | -0.0008 | 0.6 / 0.61 / 0.63 | 0.632 |  |  | 8/16 | +0.011 | -0.007 |  | +0.6 / +0.5 |  |
| MES | 5 | h4 | -0.002 | -0.018 .. +0.014 | -0.0034 | 0.83 / 0.84 / 0.85 | 0.846 |  |  | 8/16 | +0.017 | -0.020 |  | -0.3 / -0.2 | 0.024 |
| MES | 5 | h8 | -0.003 | -0.035 .. +0.028 | -0.0034 | 0.83 / 0.83 / 0.84 | 0.835 |  |  | 8/16 | +0.041 | -0.048 |  | -0.5 / -0.2 |  |
| MES | 5 | h16 | +0.000 | -0.061 .. +0.061 | -0.0024 | 1 / 1 / 0.99 | 0.99 |  |  | 7/16 | +0.058 | -0.057 |  | +0.0 / +0.0 |  |
| MES | 5 | eod | -0.364 | -1.134 .. +0.405 | -0.0207 | 0.35 / 0.35 / 0.19 | 0.193 |  |  | 8/16 | -0.300 | -0.428 |  | -7.0 / -0.9 |  |
| MES | 15 | h1 | +0.002 | -0.008 .. +0.011 | +0.0022 | 0.72 / 0.7 / 0.65 | 0.646 |  |  | 8/16 | +0.007 | -0.004 |  | +0.4 / +0.4 |  |
| MES | 15 | h2 | -0.002 | -0.017 .. +0.013 | -0.0013 | 0.82 / 0.82 / 0.84 | 0.846 |  |  | 8/16 | +0.019 | -0.023 |  | -0.3 / -0.2 |  |
| MES | 15 | h4 | -0.003 | -0.033 .. +0.027 | -0.0034 | 0.84 / 0.84 / 0.86 | 0.869 |  |  | 7/16 | +0.035 | -0.040 |  | -0.3 / -0.2 | 0.047 |
| MES | 15 | h8 | -0.010 | -0.069 .. +0.048 | -0.0038 | 0.73 / 0.73 / 0.74 | 0.744 |  |  | 8/16 | +0.056 | -0.077 |  | -0.7 / -0.4 |  |
| MES | 15 | h16 * | -0.053 | -0.183 .. +0.077 | -0.0103 | 0.43 / 0.42 / 0.36 | 0.361 | 1 | 1 | 8/16 | +0.090 | -0.195 | False | -2.6 / -0.8 |  |
| MES | 15 | eod | -0.197 | -0.859 .. +0.465 | -0.0185 | 0.56 / 0.54 / 0.37 | 0.358 |  |  | 7/16 | +0.185 | -0.577 |  | -3.5 / -0.6 |  |
| MES | 60 | h1 * | -0.021 | -0.039 .. -0.004 | -0.0075 | 0.015 / 0.015 / 0.019 | 0.0198 | 1 | 0.949 | 9/16 | -0.008 | -0.035 | False | -2.4 / -2.4 |  |
| MES | 60 | h2 | -0.034 | -0.066 .. -0.002 | -0.0078 | 0.038 / 0.037 / 0.05 | 0.0495 |  |  | 8/16 | -0.017 | -0.051 |  | -2.7 / -2.1 |  |
| MES | 60 | h4 | -0.048 | -0.107 .. +0.012 | -0.0083 | 0.12 / 0.11 / 0.14 | 0.145 |  |  | 10/16 | -0.024 | -0.071 |  | -2.7 / -1.6 | 0.089 |
| MES | 60 | h8 | -0.038 | -0.143 .. +0.066 | -0.0048 | 0.47 / 0.47 / 0.5 | 0.49 |  |  | 9/16 | -0.001 | -0.076 |  | -1.6 / -0.7 |  |
| MES | 60 | h16 | -0.002 | -0.174 .. +0.170 | +0.0003 | 0.98 / 0.98 / 0.98 | 0.98 |  |  | 6/16 | +0.081 | -0.085 |  | -0.1 / -0.0 |  |
| MES | 60 | eod | +0.022 | -0.169 .. +0.214 | +0.0028 | 0.82 / 0.82 / 0.84 | 0.841 |  |  | 10/16 | +0.100 | -0.056 |  | +0.7 / +0.2 |  |
| MNQ | 5 | h1 | -0.004 | -0.009 .. +0.002 | -0.0032 | 0.19 / 0.2 / 0.18 | 0.179 |  |  | 11/16 | -0.000 | -0.007 |  | -1.1 / -1.3 |  |
| MNQ | 5 | h2 * | -0.009 | -0.021 .. +0.003 | -0.0058 | 0.15 / 0.15 / 0.12 | 0.116 | 1 | 1 | 8/16 | +0.006 | -0.023 | False | -1.6 / -1.5 |  |
| MNQ | 5 | h4 | -0.017 | -0.042 .. +0.008 | -0.0080 | 0.18 / 0.18 / 0.13 | 0.132 |  |  | 8/16 | +0.013 | -0.046 |  | -1.9 / -1.3 | 0.030 |
| MNQ | 5 | h8 | -0.010 | -0.050 .. +0.030 | -0.0050 | 0.62 / 0.63 / 0.64 | 0.627 |  |  | 9/16 | +0.035 | -0.055 |  | -0.8 / -0.5 |  |
| MNQ | 5 | h16 | +0.004 | -0.075 .. +0.083 | -0.0002 | 0.91 / 0.91 / 0.92 | 0.927 |  |  | 7/16 | +0.046 | -0.036 |  | +0.2 / +0.1 |  |
| MNQ | 5 | eod | -0.296 | -1.256 .. +0.665 | -0.0179 | 0.55 / 0.54 / 0.33 | 0.334 |  |  | 7/16 | +0.067 | -0.655 |  | -3.8 / -0.6 |  |
| MNQ | 15 | h1 | -0.001 | -0.015 .. +0.012 | -0.0002 | 0.84 / 0.84 / 0.83 | 0.83 |  |  | 11/16 | +0.004 | -0.007 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h2 | -0.013 | -0.033 .. +0.007 | -0.0063 | 0.2 / 0.22 / 0.29 | 0.297 |  |  | 10/16 | +0.007 | -0.033 |  | -1.1 / -1.3 |  |
| MNQ | 15 | h4 | -0.022 | -0.065 .. +0.020 | -0.0074 | 0.3 / 0.32 / 0.36 | 0.367 |  |  | 10/16 | +0.012 | -0.056 |  | -1.0 / -1.0 | 0.059 |
| MNQ | 15 | h8 | -0.029 | -0.102 .. +0.044 | -0.0074 | 0.43 / 0.44 / 0.49 | 0.489 |  |  | 8/16 | +0.025 | -0.083 |  | -1.1 / -0.8 |  |
| MNQ | 15 | h16 | -0.104 | -0.272 .. +0.064 | -0.0211 | 0.23 / 0.22 / 0.14 | 0.138 |  |  | 9/16 | +0.077 | -0.283 |  | -3.5 / -1.2 |  |
| MNQ | 15 | eod * | -0.534 | -1.318 .. +0.250 | -0.0320 | 0.18 / 0.17 / 0.034 | 0.0357 | 1 | 1 | 9/16 | -0.110 | -0.955 | False | -5.9 / -1.3 |  |
| MNQ | 60 | h1 * | -0.014 | -0.032 .. +0.004 | -0.0067 | 0.14 / 0.15 / 0.16 | 0.161 | 1 | 1 | 11/16 | -0.000 | -0.027 | False | -1.4 / -1.5 |  |
| MNQ | 60 | h2 | -0.010 | -0.044 .. +0.024 | -0.0067 | 0.55 / 0.56 / 0.57 | 0.571 |  |  | 8/16 | +0.004 | -0.025 |  | -0.8 / -0.6 |  |
| MNQ | 60 | h4 | +0.006 | -0.055 .. +0.067 | -0.0055 | 0.84 / 0.85 / 0.86 | 0.862 |  |  | 8/16 | +0.022 | -0.010 |  | +0.3 / +0.2 | 0.095 |
| MNQ | 60 | h8 | +0.038 | -0.067 .. +0.144 | -0.0005 | 0.48 / 0.49 / 0.52 | 0.528 |  |  | 11/16 | +0.045 | +0.031 |  | +1.6 / +0.7 |  |
| MNQ | 60 | h16 | +0.107 | -0.067 .. +0.280 | +0.0085 | 0.23 / 0.24 / 0.28 | 0.289 |  |  | 12/16 | +0.080 | +0.133 |  | +3.3 / +1.2 |  |
| MNQ | 60 | eod | +0.152 | -0.037 .. +0.342 | +0.0132 | 0.12 / 0.13 / 0.16 | 0.168 |  |  | 12/16 | +0.091 | +0.214 |  | +4.5 / +1.6 |  |
| MYM | 5 | h1 | +0.001 | -0.006 .. +0.009 | -0.0008 | 0.71 / 0.71 / 0.79 | 0.787 |  |  | 4/8 | n/a | +0.001 |  | +0.3 / +0.4 |  |
| MYM | 5 | h2 | -0.002 | -0.023 .. +0.019 | -0.0038 | 0.88 / 0.87 / 0.81 | 0.814 |  |  | 3/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 5 | h4 | -0.009 | -0.060 .. +0.042 | -0.0065 | 0.74 / 0.72 / 0.6 | 0.614 |  |  | 3/8 | n/a | -0.009 |  | -0.6 / -0.3 | 0.047 |
| MYM | 5 | h8 | -0.013 | -0.098 .. +0.072 | -0.0060 | 0.76 / 0.75 / 0.64 | 0.656 |  |  | 3/8 | n/a | -0.013 |  | -0.6 / -0.3 |  |
| MYM | 5 | h16 * | -0.056 | -0.207 .. +0.095 | -0.0098 | 0.46 / 0.46 / 0.27 | 0.273 | 1 | 1 | 3/8 | n/a | -0.056 | False | -2.2 / -0.7 |  |
| MYM | 5 | eod | -0.393 | -1.628 .. +0.842 | -0.0209 | 0.53 / 0.53 / 0.27 | 0.265 |  |  | 3/8 | n/a | -0.393 |  | -3.9 / -0.6 |  |
| MYM | 15 | h1 | -0.002 | -0.016 .. +0.012 | -0.0014 | 0.77 / 0.78 / 0.79 | 0.785 |  |  | 4/8 | n/a | -0.002 |  | -0.2 / -0.3 |  |
| MYM | 15 | h2 * | -0.023 | -0.060 .. +0.014 | -0.0106 | 0.22 / 0.23 / 0.18 | 0.18 | 1 | 1 | 4/8 | n/a | -0.023 | False | -1.3 / -1.2 |  |
| MYM | 15 | h4 | -0.044 | -0.124 .. +0.035 | -0.0132 | 0.28 / 0.3 / 0.18 | 0.187 |  |  | 5/8 | n/a | -0.044 |  | -1.4 / -1.1 | 0.079 |
| MYM | 15 | h8 | -0.074 | -0.232 .. +0.084 | -0.0183 | 0.36 / 0.37 / 0.21 | 0.214 |  |  | 4/8 | n/a | -0.074 |  | -1.9 / -0.9 |  |
| MYM | 15 | h16 | -0.210 | -0.616 .. +0.196 | -0.0372 | 0.31 / 0.32 / 0.053 | 0.0511 |  |  | 5/8 | n/a | -0.210 |  | -3.9 / -1.0 |  |
| MYM | 15 | eod | -0.647 | -1.830 .. +0.535 | -0.0449 | 0.28 / 0.28 / 0.047 | 0.0469 |  |  | 2/8 | n/a | -0.647 |  | -5.2 / -1.1 |  |
| MYM | 60 | h1 * | -0.012 | -0.036 .. +0.012 | -0.0103 | 0.34 / 0.37 / 0.38 | 0.39 | 1 | 1 | 5/8 | n/a | -0.012 | False | -0.9 / -1.0 |  |
| MYM | 60 | h2 | -0.015 | -0.061 .. +0.032 | -0.0106 | 0.54 / 0.56 / 0.57 | 0.563 |  |  | 5/8 | n/a | -0.015 |  | -0.8 / -0.6 |  |
| MYM | 60 | h4 | -0.027 | -0.114 .. +0.060 | -0.0132 | 0.55 / 0.56 / 0.56 | 0.556 |  |  | 5/8 | n/a | -0.027 |  | -1.0 / -0.6 | 0.129 |
| MYM | 60 | h8 | -0.045 | -0.202 .. +0.112 | -0.0157 | 0.57 / 0.57 / 0.58 | 0.572 |  |  | 5/8 | n/a | -0.045 |  | -1.3 / -0.6 |  |
| MYM | 60 | h16 | -0.093 | -0.348 .. +0.162 | -0.0206 | 0.47 / 0.47 / 0.49 | 0.484 |  |  | 5/8 | n/a | -0.093 |  | -2.1 / -0.7 |  |
| MYM | 60 | eod | -0.077 | -0.361 .. +0.206 | -0.0192 | 0.59 / 0.59 / 0.6 | 0.597 |  |  | 5/8 | n/a | -0.077 |  | -1.6 / -0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.019 | +0.014 .. +0.023 | +3.7% | +0.028 | 9.8e-16 | 4.17e-13 | 13/16 |
| MES | 5 | h2 | +0.026 | +0.017 .. +0.034 | +3.6% | +0.044 | 4.5e-10 |  | 12/16 |
| MES | 5 | h4 | +0.036 | +0.020 .. +0.052 | +3.6% | +0.066 | 8e-06 |  | 12/16 |
| MES | 5 | h8 | +0.041 | +0.011 .. +0.070 | +2.8% | +0.088 | 0.0065 |  | 13/16 |
| MES | 5 | h16 | +0.046 | -0.004 .. +0.095 | +2.2% | +0.119 | 0.076 |  | 10/16 |
| MES | 5 | eod | +0.397 | -0.168 .. +0.961 | +4.0% | +0.536 | 0.17 |  | 9/16 |
| MES | 15 | h1 * | +0.026 | +0.017 .. +0.034 | +5.0% | +0.049 | 7.5e-10 | 2.31e-07 | 14/16 |
| MES | 15 | h2 | +0.035 | +0.016 .. +0.055 | +4.8% | +0.072 | 0.00035 |  | 11/16 |
| MES | 15 | h4 | +0.043 | +0.004 .. +0.082 | +4.1% | +0.100 | 0.03 |  | 10/16 |
| MES | 15 | h8 | +0.050 | -0.012 .. +0.113 | +3.3% | +0.141 | 0.11 |  | 11/16 |
| MES | 15 | h16 | +0.072 | -0.035 .. +0.179 | +3.1% | +0.223 | 0.19 |  | 9/16 |
| MES | 15 | eod | +0.217 | -0.312 .. +0.745 | +4.0% | +0.404 | 0.42 |  | 6/16 |
| MES | 60 | h1 * | +0.043 | +0.028 .. +0.058 | +8.4% | +0.096 | 3.5e-08 | 9.66e-06 | 13/16 |
| MES | 60 | h2 | +0.051 | +0.028 .. +0.075 | +7.0% | +0.124 | 1.6e-05 |  | 11/16 |
| MES | 60 | h4 | +0.073 | +0.035 .. +0.112 | +6.9% | +0.163 | 0.00021 |  | 11/16 |
| MES | 60 | h8 | +0.095 | +0.028 .. +0.162 | +6.3% | +0.205 | 0.0053 |  | 12/16 |
| MES | 60 | h16 | +0.107 | -0.007 .. +0.222 | +5.2% | +0.266 | 0.066 |  | 12/16 |
| MES | 60 | eod | +0.107 | -0.024 .. +0.238 | +5.0% | +0.274 | 0.11 |  | 12/16 |
| MNQ | 5 | h1 * | +0.023 | +0.016 .. +0.030 | +4.4% | +0.033 | 2.2e-10 | 7.12e-08 | 13/16 |
| MNQ | 5 | h2 | +0.034 | +0.017 .. +0.050 | +4.4% | +0.055 | 4.8e-05 |  | 12/16 |
| MNQ | 5 | h4 | +0.045 | +0.013 .. +0.078 | +4.1% | +0.086 | 0.0066 |  | 11/16 |
| MNQ | 5 | h8 | +0.049 | -0.011 .. +0.109 | +3.0% | +0.120 | 0.11 |  | 10/16 |
| MNQ | 5 | h16 | +0.068 | -0.026 .. +0.162 | +2.9% | +0.176 | 0.15 |  | 10/16 |
| MNQ | 5 | eod | +0.685 | -0.115 .. +1.486 | +5.5% | +0.858 | 0.093 |  | 11/16 |
| MNQ | 15 | h1 * | +0.027 | +0.012 .. +0.043 | +5.1% | +0.056 | 0.00034 | 0.0635 | 13/16 |
| MNQ | 15 | h2 | +0.046 | +0.001 .. +0.092 | +6.0% | +0.097 | 0.047 |  | 12/16 |
| MNQ | 15 | h4 | +0.071 | -0.044 .. +0.185 | +6.2% | +0.159 | 0.23 |  | 8/16 |
| MNQ | 15 | h8 | +0.092 | -0.091 .. +0.274 | +5.5% | +0.278 | 0.32 |  | 7/16 |
| MNQ | 15 | h16 | +0.088 | -0.115 .. +0.291 | +3.5% | +0.411 | 0.39 |  | 7/16 |
| MNQ | 15 | eod | +0.408 | -0.419 .. +1.235 | +6.4% | +0.687 | 0.33 |  | 9/16 |
| MNQ | 60 | h1 * | +0.034 | +0.019 .. +0.049 | +6.4% | +0.085 | 1.4e-05 | 0.00309 | 13/16 |
| MNQ | 60 | h2 | +0.034 | +0.011 .. +0.058 | +4.5% | +0.105 | 0.004 |  | 11/16 |
| MNQ | 60 | h4 | +0.039 | +0.000 .. +0.077 | +3.5% | +0.121 | 0.05 |  | 12/16 |
| MNQ | 60 | h8 | +0.074 | +0.011 .. +0.137 | +4.7% | +0.171 | 0.025 |  | 11/16 |
| MNQ | 60 | h16 | +0.112 | +0.007 .. +0.218 | +5.1% | +0.258 | 0.041 |  | 12/16 |
| MNQ | 60 | eod | +0.098 | -0.023 .. +0.219 | +4.3% | +0.259 | 0.12 |  | 11/16 |
| MYM | 5 | h1 * | +0.028 | +0.017 .. +0.039 | +5.3% | +0.042 | 8.3e-07 | 0.000206 | 7/8 |
| MYM | 5 | h2 | +0.038 | +0.014 .. +0.062 | +4.9% | +0.064 | 0.0021 |  | 6/8 |
| MYM | 5 | h4 | +0.054 | +0.000 .. +0.108 | +5.0% | +0.095 | 0.048 |  | 4/8 |
| MYM | 5 | h8 | +0.072 | -0.024 .. +0.168 | +4.5% | +0.137 | 0.14 |  | 3/8 |
| MYM | 5 | h16 | +0.119 | -0.048 .. +0.285 | +5.1% | +0.233 | 0.16 |  | 4/8 |
| MYM | 5 | eod | +0.552 | -0.450 .. +1.554 | +4.7% | +0.600 | 0.28 |  | 4/8 |
| MYM | 15 | h1 * | +0.031 | +0.009 .. +0.052 | +5.8% | +0.059 | 0.005 | 0.73 | 5/8 |
| MYM | 15 | h2 | +0.058 | +0.001 .. +0.115 | +7.6% | +0.109 | 0.046 |  | 5/8 |
| MYM | 15 | h4 | +0.099 | -0.028 .. +0.226 | +8.9% | +0.198 | 0.13 |  | 6/8 |
| MYM | 15 | h8 | +0.144 | -0.059 .. +0.348 | +8.8% | +0.357 | 0.17 |  | 6/8 |
| MYM | 15 | h16 | +0.238 | -0.142 .. +0.619 | +9.7% | +0.595 | 0.23 |  | 5/8 |
| MYM | 15 | eod | +0.405 | -0.654 .. +1.465 | +6.7% | +0.944 | 0.45 |  | 3/8 |
| MYM | 60 | h1 * | +0.034 | +0.011 .. +0.057 | +6.5% | +0.078 | 0.0045 | 0.668 | 6/8 |
| MYM | 60 | h2 | +0.032 | -0.003 .. +0.067 | +4.2% | +0.094 | 0.073 |  | 6/8 |
| MYM | 60 | h4 | +0.037 | -0.020 .. +0.093 | +3.4% | +0.101 | 0.21 |  | 5/8 |
| MYM | 60 | h8 | +0.023 | -0.072 .. +0.119 | +1.5% | +0.094 | 0.63 |  | 5/8 |
| MYM | 60 | h16 | +0.048 | -0.112 .. +0.207 | +2.2% | +0.141 | 0.56 |  | 5/8 |
| MYM | 60 | eod | +0.065 | -0.117 .. +0.248 | +2.9% | +0.163 | 0.54 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.63 pts | +0.06 .. +1.20 | 0.031 |
| MES | 15 | +0.25 pts | -0.62 .. +1.12 | 0.58 |
| MES | 60 | -1.73 pts | -3.74 .. +0.28 | 0.092 |
| MNQ | 5 | +0.50 pts | -0.05 .. +1.05 | 0.076 |
| MNQ | 15 | +0.15 pts | -0.78 .. +1.07 | 0.76 |
| MNQ | 60 | -0.60 pts | -2.59 .. +1.38 | 0.55 |
| MYM | 5 | +0.22 pts | -0.53 .. +0.96 | 0.61 |
| MYM | 15 | -0.01 pts | -1.15 .. +1.13 | 0.98 |
| MYM | 60 | -1.50 pts | -4.10 .. +1.10 | 0.28 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | long | 204826 | +0.004 | 0.326 | +0.06 | -3.44 | -3.46 | -3.42 | -3.47 |
| MES | 5 | h2 | top fifth | long | 204826 | +0.004 | 0.326 | +0.07 | -3.43 | -3.44 | -3.41 | -3.47 |
| MES | 5 | h4 | bottom fifth | long | 207070 | +0.000 | 0.340 | +0.05 | -3.45 | -3.49 | -3.42 | -3.47 |
| MES | 5 | h8 | bottom fifth | long | 207070 | +0.002 | 0.340 | +0.10 | -3.40 | -3.48 | -3.32 | -3.48 |
| MES | 5 | h16 | top fifth | long | 204826 | +0.012 | 0.326 | +0.12 | -3.38 | -3.19 | -3.59 | -3.61 |
| MES | 5 | eod | bottom fifth | long | 207070 | +0.459 | 0.340 | +3.47 | -0.03 | +0.00 | -0.07 | -2.64 |
| MES | 15 | h1 | top fifth | long | 68313 | +0.006 | 0.182 | +0.10 | -3.40 | -3.38 | -3.41 | -3.48 |
| MES | 15 | h2 | bottom fifth | long | 68352 | +0.005 | 0.199 | +0.03 | -3.47 | -3.51 | -3.42 | -3.54 |
| MES | 15 | h4 | bottom fifth | long | 68352 | +0.012 | 0.199 | +0.12 | -3.38 | -3.44 | -3.33 | -3.58 |
| MES | 15 | h8 | bottom fifth | long | 68352 | +0.025 | 0.199 | +0.23 | -3.27 | -3.26 | -3.29 | -3.70 |
| MES | 15 | h16 | bottom fifth | long | 68352 | +0.067 | 0.199 | +0.93 | -2.57 | -2.72 | -2.43 | -3.55 |
| MES | 15 | eod | bottom fifth | long | 68352 | +0.162 | 0.199 | +2.33 | -1.17 | -1.66 | -0.69 | -3.64 |
| MES | 60 | h1 | bottom fifth | long | 16645 | +0.019 | 0.104 | +0.54 | -2.96 | -3.19 | -2.74 | -3.16 |
| MES | 60 | h2 | bottom fifth | long | 16645 | +0.035 | 0.104 | +0.97 | -2.53 | -2.89 | -2.18 | -2.96 |
| MES | 60 | h4 | bottom fifth | long | 16645 | +0.060 | 0.104 | +1.69 | -1.81 | -2.48 | -1.15 | -2.63 |
| MES | 60 | h8 | bottom fifth | long | 16645 | +0.082 | 0.104 | +2.72 | -0.78 | -1.60 | +0.02 | -2.32 |
| MES | 60 | h16 | bottom fifth | long | 16645 | +0.090 | 0.104 | +3.61 | +0.11 | -1.60 | +1.78 | -2.33 |
| MES | 60 | eod | top fifth | long | 16644 | +0.099 | 0.080 | +6.01 | +2.51 | +0.54 | +4.35 | -0.85 |
| MNQ | 5 | h1 | bottom fifth | long | 206826 | +0.006 | 0.135 | +0.04 | -1.96 | -1.98 | -1.94 | -1.97 |
| MNQ | 5 | h2 | bottom fifth | long | 206826 | +0.009 | 0.135 | +0.08 | -1.92 | -1.97 | -1.87 | -1.96 |
| MNQ | 5 | h4 | bottom fifth | long | 206826 | +0.016 | 0.135 | +0.21 | -1.79 | -1.93 | -1.64 | -1.88 |
| MNQ | 5 | h8 | bottom fifth | long | 206826 | +0.019 | 0.135 | +0.36 | -1.64 | -1.87 | -1.41 | -1.86 |
| MNQ | 5 | h16 | top fifth | long | 206793 | +0.016 | 0.137 | -0.01 | -2.01 | -1.74 | -2.37 | -2.12 |
| MNQ | 5 | eod | bottom fifth | long | 206826 | +0.884 | 0.135 | +4.92 | +2.92 | +1.00 | +4.89 | -1.10 |
| MNQ | 15 | h1 | bottom fifth | long | 68341 | +0.008 | 0.078 | +0.06 | -1.94 | -1.93 | -1.94 | -2.00 |
| MNQ | 15 | h2 | bottom fifth | long | 68341 | +0.017 | 0.078 | +0.18 | -1.82 | -1.87 | -1.78 | -1.93 |
| MNQ | 15 | h4 | bottom fifth | long | 68341 | +0.030 | 0.078 | +0.39 | -1.61 | -1.74 | -1.49 | -1.90 |
| MNQ | 15 | h8 | bottom fifth | long | 68341 | +0.055 | 0.078 | +0.74 | -1.26 | -1.54 | -0.98 | -1.99 |
| MNQ | 15 | h16 | bottom fifth | long | 68341 | +0.126 | 0.078 | +2.06 | +0.06 | -0.99 | +1.09 | -1.22 |
| MNQ | 15 | eod | bottom fifth | long | 68341 | +0.499 | 0.078 | +5.98 | +3.98 | +1.09 | +6.80 | +1.17 |
| MNQ | 60 | h1 | bottom fifth | long | 16654 | +0.020 | 0.040 | +0.75 | -1.25 | -1.58 | -0.94 | -1.74 |
| MNQ | 60 | h2 | bottom fifth | long | 16654 | +0.033 | 0.040 | +0.99 | -1.01 | -1.20 | -0.82 | -1.91 |
| MNQ | 60 | h4 | top fifth | long | 16654 | +0.036 | 0.032 | +1.00 | -1.00 | -1.07 | -0.93 | -1.97 |
| MNQ | 60 | h8 | top fifth | long | 16654 | +0.088 | 0.032 | +3.98 | +1.98 | +0.02 | +3.88 | +0.06 |
| MNQ | 60 | h16 | top fifth | long | 16654 | +0.171 | 0.032 | +10.47 | +8.47 | +1.93 | +14.81 | +5.67 |
| MNQ | 60 | eod | top fifth | long | 16654 | +0.205 | 0.032 | +13.24 | +11.24 | +2.46 | +19.75 | +7.62 |
| MYM | 5 | h1 | top fifth | long | 103776 | -0.002 | 0.164 | +0.03 | -1.97 | +nan | -1.97 | -1.97 |
| MYM | 5 | h2 | bottom fifth | long | 104744 | -0.008 | 0.175 | -0.03 | -2.03 | +nan | -2.03 | -2.04 |
| MYM | 5 | h4 | top fifth | short | 103776 | +0.042 | 0.164 | -0.00 | -2.00 | +nan | -2.00 | -2.18 |
| MYM | 5 | h8 | top fifth | short | 103776 | +0.084 | 0.164 | +0.08 | -1.92 | +nan | -1.92 | -2.25 |
| MYM | 5 | h16 | top fifth | short | 103776 | +0.142 | 0.164 | +0.15 | -1.85 | +nan | -1.85 | -2.19 |
| MYM | 5 | eod | bottom fifth | long | 104744 | +0.232 | 0.175 | +2.90 | +0.90 | +nan | +0.90 | -1.27 |
| MYM | 15 | h1 | top fifth | short | 34254 | +0.004 | 0.089 | -0.03 | -2.03 | +nan | -2.03 | -2.05 |
| MYM | 15 | h2 | bottom fifth | long | 34256 | +0.004 | 0.100 | +0.02 | -1.98 | +nan | -1.98 | -2.05 |
| MYM | 15 | h4 | top fifth | short | 34254 | +0.049 | 0.089 | +0.03 | -1.97 | +nan | -1.97 | -2.19 |
| MYM | 15 | h8 | bottom fifth | long | 34256 | +0.007 | 0.100 | -0.07 | -2.07 | +nan | -2.07 | -2.32 |
| MYM | 15 | h16 | top fifth | short | 34254 | +0.264 | 0.089 | +0.29 | -1.71 | +nan | -1.71 | -2.86 |
| MYM | 15 | eod | bottom fifth | long | 34256 | +0.153 | 0.100 | +2.17 | +0.17 | +nan | +0.17 | -0.77 |
| MYM | 60 | h1 | bottom fifth | long | 8320 | +0.010 | 0.051 | +0.22 | -1.78 | +nan | -1.78 | -1.98 |
| MYM | 60 | h2 | bottom fifth | long | 8320 | +0.021 | 0.051 | +0.44 | -1.56 | +nan | -1.56 | -1.96 |
| MYM | 60 | h4 | bottom fifth | long | 8320 | +0.046 | 0.051 | +1.30 | -0.70 | +nan | -0.70 | -1.56 |
| MYM | 60 | h8 | bottom fifth | long | 8320 | +0.094 | 0.051 | +2.73 | +0.73 | +nan | +0.73 | -0.73 |
| MYM | 60 | h16 | bottom fifth | long | 8320 | +0.149 | 0.051 | +5.23 | +3.23 | +nan | +3.23 | +0.68 |
| MYM | 60 | eod | bottom fifth | long | 8320 | +0.149 | 0.051 | +4.98 | +2.98 | +nan | +2.98 | -0.11 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.983 | +1.470 | +0.952 | +0.574 | +0.328 | +0.000 | +0.012 | +0.013 | +0.010 | +0.010 | +0.014 |
| MES | 15 | +2.352 | +1.751 | +1.141 | +0.680 | +0.382 | +0.000 | +0.005 | +0.003 | +0.005 | +0.000 | -0.027 |
| MES | 60 | +3.105 | +2.168 | +1.433 | +0.835 | +0.462 | +0.000 | -0.020 | -0.030 | -0.034 | +0.003 | +0.110 |
| MNQ | 5 | +2.709 | +2.036 | +1.283 | +0.752 | +0.421 | +0.000 | +0.001 | -0.003 | -0.012 | -0.006 | +0.007 |
| MNQ | 15 | +2.881 | +2.159 | +1.383 | +0.812 | +0.456 | +0.000 | -0.006 | -0.018 | -0.026 | -0.028 | -0.090 |
| MNQ | 60 | +3.413 | +2.434 | +1.599 | +0.928 | +0.510 | +0.000 | -0.012 | -0.006 | +0.022 | +0.088 | +0.103 |
| MYM | 5 | +2.761 | +2.089 | +1.317 | +0.767 | +0.428 | +0.000 | +0.001 | -0.002 | -0.009 | -0.016 | -0.063 |
| MYM | 15 | +2.870 | +2.179 | +1.396 | +0.823 | +0.458 | +0.000 | -0.019 | -0.042 | -0.070 | -0.105 | -0.277 |
| MYM | 60 | +3.288 | +2.366 | +1.575 | +0.909 | +0.502 | +0.000 | -0.012 | -0.009 | -0.017 | -0.037 | -0.131 |

## Calibration

- MES 5-min: 1035075 bars, 204826 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341645 bars, 68313 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83221 bars, 16644 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034123 bars, 206793 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341666 bars, 68333 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83269 bars, 16654 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518880 bars, 103776 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171276 bars, 34254 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41596 bars, 8319 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
