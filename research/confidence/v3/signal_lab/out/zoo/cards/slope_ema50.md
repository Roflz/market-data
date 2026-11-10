# Impact card: slope_ema50

5-bar change of EMA50 in R20 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.014 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.015 R20, CONFIRMED, q=1.51e-09, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.32 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.217 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.013 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.020 R20, CONFIRMED, q=1.16e-05, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.17 at recent bar sizes, 90% range up to $0.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.029 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.094 R20 or more 80% of the time).
- MES 60-min size: the market moves 6% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.031 R20, CONFIRMED, q=0.000641, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.82 at recent bar sizes, 90% range up to $3.68); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (5 min), p=0.1; we would catch an effect of 0.033 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.013 R20, CONFIRMED, q=0.00444, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.09 at recent bar sizes, 90% range up to $0.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.010 R20 over the next 1 bar (15 min), p=0.12; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.014 R20, possible, q=0.201, 11 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.22 at recent bar sizes, 90% range up to $2.27); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.076 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.099 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.024 R20, possible, q=0.0754, 12 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.51 at recent bar sizes, 90% range up to $4.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.588 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.019).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.53 at recent bar sizes, 90% range up to $0.68); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.069 R20 over the next 4 bars (1 h), p=0.61; we would catch an effect of 0.077 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.013).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.71 at recent bar sizes, 90% range up to $2.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.077 R20 over the next 4 bars (4 h), p=0.56; we would catch an effect of 0.136 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.64 at recent bar sizes, 90% range up to $5.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.004 .. +0.005 | -0.0005 | 0.85 / 0.84 / 0.86 | 0.866 |  |  | 9/16 | -0.004 | +0.005 |  | +0.2 / +0.2 |  |
| MES | 5 | h2 | -0.001 | -0.009 .. +0.007 | -0.0025 | 0.88 / 0.87 / 0.88 | 0.883 |  |  | 7/16 | -0.010 | +0.009 |  | -0.2 / -0.2 |  |
| MES | 5 | h4 | -0.003 | -0.019 .. +0.012 | -0.0038 | 0.68 / 0.67 / 0.71 | 0.713 |  |  | 8/16 | -0.023 | +0.017 |  | -0.7 / -0.4 | 0.024 |
| MES | 5 | h8 * | -0.014 | -0.045 .. +0.017 | -0.0054 | 0.37 / 0.35 / 0.41 | 0.417 | 1 | 1 | 10/16 | -0.054 | +0.025 | False | -2.2 / -0.9 |  |
| MES | 5 | h16 | -0.006 | -0.066 .. +0.054 | -0.0024 | 0.84 / 0.83 / 0.85 | 0.854 |  |  | 7/16 | -0.059 | +0.047 |  | -0.6 / -0.2 |  |
| MES | 5 | eod | +0.007 | -0.657 .. +0.671 | +0.0025 | 0.98 / 0.98 / 0.98 | 0.983 |  |  | 5/16 | -0.081 | +0.095 |  | +0.1 / +0.0 |  |
| MES | 15 | h1 | -0.001 | -0.009 .. +0.007 | -0.0018 | 0.84 / 0.85 / 0.85 | 0.856 |  |  | 8/16 | -0.006 | +0.004 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.000 | -0.015 .. +0.014 | +0.0001 | 0.99 / 0.99 / 0.99 | 0.991 |  |  | 7/16 | -0.011 | +0.011 |  | -0.0 / -0.0 |  |
| MES | 15 | h4 | +0.005 | -0.023 .. +0.033 | +0.0006 | 0.74 / 0.75 / 0.77 | 0.77 |  |  | 9/16 | -0.019 | +0.028 |  | +0.5 / +0.3 | 0.044 |
| MES | 15 | h8 * | +0.013 | -0.040 .. +0.066 | +0.0023 | 0.64 / 0.65 / 0.69 | 0.695 | 1 | 1 | 9/16 | -0.038 | +0.063 | False | +1.0 / +0.5 |  |
| MES | 15 | h16 | +0.009 | -0.096 .. +0.115 | +0.0023 | 0.86 / 0.87 / 0.88 | 0.885 |  |  | 10/16 | -0.092 | +0.110 |  | +0.5 / +0.2 |  |
| MES | 15 | eod | -0.075 | -0.630 .. +0.480 | +0.0044 | 0.79 / 0.79 / 0.8 | 0.797 |  |  | 11/16 | -0.323 | +0.171 |  | -1.4 / -0.3 |  |
| MES | 60 | h1 | +0.008 | -0.009 .. +0.024 | +0.0042 | 0.36 / 0.35 / 0.41 | 0.396 |  |  | 8/16 | -0.002 | +0.017 |  | +0.9 / +0.9 |  |
| MES | 60 | h2 | +0.013 | -0.018 .. +0.045 | +0.0043 | 0.41 / 0.41 / 0.46 | 0.452 |  |  | 8/16 | -0.008 | +0.035 |  | +1.1 / +0.8 |  |
| MES | 60 | h4 * | +0.029 | -0.031 .. +0.090 | +0.0062 | 0.34 / 0.34 / 0.39 | 0.385 | 1 | 1 | 9/16 | -0.013 | +0.072 | False | +1.7 / +1.0 | 0.094 |
| MES | 60 | h8 | +0.039 | -0.073 .. +0.150 | +0.0011 | 0.5 / 0.5 / 0.54 | 0.537 |  |  | 9/16 | -0.040 | +0.117 |  | +1.7 / +0.7 |  |
| MES | 60 | h16 | +0.003 | -0.187 .. +0.193 | +0.0006 | 0.98 / 0.98 / 0.97 | 0.975 |  |  | 9/16 | -0.117 | +0.123 |  | +0.1 / +0.0 |  |
| MES | 60 | eod | -0.017 | -0.228 .. +0.194 | -0.0009 | 0.87 / 0.88 / 0.9 | 0.903 |  |  | 8/16 | -0.112 | +0.078 |  | -0.5 / -0.2 |  |
| MNQ | 5 | h1 * | +0.007 | +0.001 .. +0.012 | +0.0025 | 0.012 / 0.0083 / 0.014 | 0.0154 | 1 | 0.847 | 13/16 | +0.005 | +0.008 | False | +2.2 / +2.5 |  |
| MNQ | 5 | h2 | +0.013 | +0.003 .. +0.022 | +0.0023 | 0.0084 / 0.0059 / 0.031 | 0.032 |  |  | 11/16 | +0.004 | +0.022 |  | +2.6 / +2.6 |  |
| MNQ | 5 | h4 | +0.020 | +0.000 .. +0.040 | +0.0027 | 0.045 / 0.04 / 0.08 | 0.0768 |  |  | 9/16 | -0.002 | +0.042 |  | +2.6 / +2.0 | 0.033 |
| MNQ | 5 | h8 | +0.025 | -0.016 .. +0.065 | -0.0005 | 0.23 / 0.22 / 0.28 | 0.286 |  |  | 9/16 | -0.020 | +0.069 |  | +2.0 / +1.2 |  |
| MNQ | 5 | h16 | +0.035 | -0.049 .. +0.118 | -0.0024 | 0.42 / 0.42 / 0.42 | 0.415 |  |  | 7/16 | -0.020 | +0.089 |  | +1.9 / +0.8 |  |
| MNQ | 5 | eod | +0.188 | -0.933 .. +1.310 | +0.0128 | 0.74 / 0.74 / 0.66 | 0.661 |  |  | 7/16 | +0.120 | +0.256 |  | +2.4 / +0.3 |  |
| MNQ | 15 | h1 * | +0.010 | +0.002 .. +0.018 | +0.0043 | 0.015 / 0.019 / 0.021 | 0.0247 | 1 | 0.962 | 13/16 | +0.003 | +0.016 | False | +2.3 / +2.4 |  |
| MNQ | 15 | h2 | +0.011 | -0.015 .. +0.036 | -0.0011 | 0.42 / 0.43 / 0.28 | 0.281 |  |  | 12/16 | +0.008 | +0.013 |  | +1.2 / +0.8 |  |
| MNQ | 15 | h4 | +0.003 | -0.069 .. +0.074 | -0.0074 | 0.94 / 0.94 / 0.9 | 0.905 |  |  | 12/16 | +0.013 | -0.008 |  | +0.1 / +0.1 | 0.050 |
| MNQ | 15 | h8 | -0.010 | -0.118 .. +0.099 | -0.0095 | 0.86 / 0.87 / 0.81 | 0.801 |  |  | 6/16 | +0.001 | -0.020 |  | -0.4 / -0.2 |  |
| MNQ | 15 | h16 | -0.075 | -0.258 .. +0.108 | -0.0172 | 0.42 / 0.44 / 0.32 | 0.328 |  |  | 7/16 | -0.065 | -0.085 |  | -2.6 / -0.8 |  |
| MNQ | 15 | eod | -0.463 | -1.352 .. +0.427 | -0.0382 | 0.31 / 0.31 / 0.2 | 0.199 |  |  | 10/16 | +0.053 | -0.975 |  | -4.9 / -1.0 |  |
| MNQ | 60 | h1 | +0.002 | -0.016 .. +0.019 | +0.0029 | 0.86 / 0.86 / 0.86 | 0.859 |  |  | 8/16 | -0.004 | +0.007 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h2 | +0.004 | -0.030 .. +0.038 | +0.0035 | 0.81 / 0.82 / 0.82 | 0.821 |  |  | 8/16 | -0.008 | +0.016 |  | +0.3 / +0.2 |  |
| MNQ | 60 | h4 | +0.004 | -0.060 .. +0.067 | +0.0040 | 0.91 / 0.91 / 0.91 | 0.903 |  |  | 9/16 | -0.018 | +0.026 |  | +0.2 / +0.1 | 0.099 |
| MNQ | 60 | h8 | -0.008 | -0.125 .. +0.109 | +0.0007 | 0.89 / 0.89 / 0.91 | 0.908 |  |  | 8/16 | -0.017 | +0.000 |  | -0.3 / -0.1 |  |
| MNQ | 60 | h16 | -0.043 | -0.246 .. +0.159 | -0.0033 | 0.67 / 0.68 / 0.73 | 0.717 |  |  | 8/16 | -0.016 | -0.071 |  | -1.3 / -0.4 |  |
| MNQ | 60 | eod * | -0.076 | -0.300 .. +0.147 | -0.0080 | 0.5 / 0.52 / 0.57 | 0.567 | 1 | 1 | 7/16 | -0.007 | -0.145 | False | -2.2 / -0.7 |  |
| MYM | 5 | h1 | -0.003 | -0.011 .. +0.005 | +0.0004 | 0.5 / 0.5 / 0.49 | 0.494 |  |  | 6/8 | n/a | -0.003 |  | -0.5 / -0.7 |  |
| MYM | 5 | h2 | +0.003 | -0.024 .. +0.029 | +0.0044 | 0.85 / 0.85 / 0.79 | 0.777 |  |  | 2/8 | n/a | +0.003 |  | +0.3 / +0.2 |  |
| MYM | 5 | h4 | +0.012 | -0.053 .. +0.077 | +0.0092 | 0.72 / 0.71 / 0.53 | 0.523 |  |  | 2/8 | n/a | +0.012 |  | +0.8 / +0.4 | 0.046 |
| MYM | 5 | h8 | +0.025 | -0.080 .. +0.130 | +0.0098 | 0.64 / 0.64 / 0.46 | 0.454 |  |  | 2/8 | n/a | +0.025 |  | +1.1 / +0.5 |  |
| MYM | 5 | h16 | +0.047 | -0.120 .. +0.214 | +0.0135 | 0.58 / 0.59 / 0.43 | 0.415 |  |  | 4/8 | n/a | +0.047 |  | +1.8 / +0.6 |  |
| MYM | 5 | eod * | +0.588 | -0.939 .. +2.116 | +0.0327 | 0.45 / 0.44 / 0.28 | 0.286 | 1 | 1 | 3/8 | n/a | +0.588 | False | +5.8 / +0.8 |  |
| MYM | 15 | h1 | +0.011 | -0.003 .. +0.024 | +0.0110 | 0.12 / 0.13 / 0.1 | 0.0985 |  |  | 4/8 | n/a | +0.011 |  | +1.4 / +1.5 |  |
| MYM | 15 | h2 | +0.025 | -0.004 .. +0.054 | +0.0111 | 0.086 / 0.097 / 0.098 | 0.098 |  |  | 5/8 | n/a | +0.025 |  | +2.0 / +1.7 |  |
| MYM | 15 | h4 * | +0.069 | -0.012 .. +0.150 | +0.0091 | 0.093 / 0.1 / 0.028 | 0.0311 | 1 | 1 | 5/8 | n/a | +0.069 | False | +2.5 / +1.7 | 0.077 |
| MYM | 15 | h8 | +0.126 | -0.047 .. +0.299 | +0.0111 | 0.15 / 0.16 / 0.037 | 0.0374 |  |  | 6/8 | n/a | +0.126 |  | +3.3 / +1.4 |  |
| MYM | 15 | h16 | +0.243 | -0.097 .. +0.583 | +0.0195 | 0.16 / 0.17 / 0.036 | 0.0374 |  |  | 5/8 | n/a | +0.243 |  | +4.9 / +1.4 |  |
| MYM | 15 | eod | +0.751 | -0.499 .. +2.001 | +0.0347 | 0.24 / 0.24 / 0.11 | 0.104 |  |  | 5/8 | n/a | +0.751 |  | +5.9 / +1.2 |  |
| MYM | 60 | h1 | +0.016 | -0.007 .. +0.039 | +0.0109 | 0.18 / 0.19 / 0.21 | 0.215 |  |  | 6/8 | n/a | +0.016 |  | +1.3 / +1.4 |  |
| MYM | 60 | h2 | +0.034 | -0.010 .. +0.079 | +0.0138 | 0.13 / 0.15 / 0.17 | 0.178 |  |  | 6/8 | n/a | +0.034 |  | +1.9 / +1.5 |  |
| MYM | 60 | h4 * | +0.077 | -0.010 .. +0.164 | +0.0190 | 0.082 / 0.093 / 0.11 | 0.119 | 1 | 1 | 5/8 | n/a | +0.077 | False | +3.0 / +1.7 | 0.136 |
| MYM | 60 | h8 | +0.123 | -0.040 .. +0.287 | +0.0244 | 0.14 / 0.15 / 0.17 | 0.179 |  |  | 5/8 | n/a | +0.123 |  | +3.5 / +1.5 |  |
| MYM | 60 | h16 | +0.186 | -0.094 .. +0.467 | +0.0253 | 0.19 / 0.21 / 0.24 | 0.249 |  |  | 6/8 | n/a | +0.186 |  | +4.0 / +1.3 |  |
| MYM | 60 | eod | +0.196 | -0.117 .. +0.509 | +0.0250 | 0.22 / 0.24 / 0.26 | 0.264 |  |  | 5/8 | n/a | +0.196 |  | +4.0 / +1.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.015 | -0.019 .. -0.011 | -3.0% | -0.022 | 4.2e-12 | 1.51e-09 | 13/16 |
| MES | 5 | h2 | -0.020 | -0.027 .. -0.013 | -2.8% | -0.033 | 6.8e-08 |  | 12/16 |
| MES | 5 | h4 | -0.027 | -0.040 .. -0.014 | -2.7% | -0.047 | 3.2e-05 |  | 13/16 |
| MES | 5 | h8 | -0.034 | -0.057 .. -0.012 | -2.4% | -0.062 | 0.0028 |  | 13/16 |
| MES | 5 | h16 | -0.053 | -0.092 .. -0.015 | -2.5% | -0.086 | 0.0071 |  | 12/16 |
| MES | 5 | eod | +0.114 | -0.346 .. +0.574 | +1.1% | -0.017 | 0.94 |  | 7/16 |
| MES | 15 | h1 * | -0.020 | -0.028 .. -0.013 | -4.0% | -0.036 | 4.2e-08 | 1.16e-05 | 14/16 |
| MES | 15 | h2 | -0.032 | -0.047 .. -0.018 | -4.4% | -0.053 | 1.3e-05 |  | 12/16 |
| MES | 15 | h4 | -0.047 | -0.071 .. -0.022 | -4.5% | -0.079 | 0.00018 |  | 12/16 |
| MES | 15 | h8 | -0.061 | -0.102 .. -0.021 | -4.0% | -0.106 | 0.0031 |  | 11/16 |
| MES | 15 | h16 | -0.086 | -0.154 .. -0.018 | -3.8% | -0.159 | 0.013 |  | 10/16 |
| MES | 15 | eod | -0.194 | -0.600 .. +0.211 | -3.6% | -0.305 | 0.35 |  | 10/16 |
| MES | 60 | h1 * | -0.031 | -0.044 .. -0.018 | -6.1% | -0.054 | 2.6e-06 | 0.000641 | 13/16 |
| MES | 60 | h2 | -0.045 | -0.067 .. -0.023 | -6.0% | -0.078 | 7.8e-05 |  | 13/16 |
| MES | 60 | h4 | -0.074 | -0.116 .. -0.033 | -7.0% | -0.121 | 0.00039 |  | 14/16 |
| MES | 60 | h8 | -0.114 | -0.186 .. -0.042 | -7.5% | -0.182 | 0.0019 |  | 13/16 |
| MES | 60 | h16 | -0.141 | -0.273 .. -0.009 | -6.8% | -0.237 | 0.037 |  | 12/16 |
| MES | 60 | eod | -0.136 | -0.288 .. +0.016 | -6.3% | -0.244 | 0.08 |  | 11/16 |
| MNQ | 5 | h1 * | -0.013 | -0.019 .. -0.007 | -2.5% | -0.020 | 2e-05 | 0.00444 | 13/16 |
| MNQ | 5 | h2 | -0.018 | -0.031 .. -0.006 | -2.4% | -0.032 | 0.0043 |  | 12/16 |
| MNQ | 5 | h4 | -0.025 | -0.049 .. -0.000 | -2.2% | -0.049 | 0.046 |  | 10/16 |
| MNQ | 5 | h8 | -0.041 | -0.092 .. +0.011 | -2.5% | -0.077 | 0.12 |  | 10/16 |
| MNQ | 5 | h16 | -0.055 | -0.149 .. +0.038 | -2.3% | -0.133 | 0.25 |  | 10/16 |
| MNQ | 5 | eod | -0.193 | -1.085 .. +0.700 | -1.5% | -0.419 | 0.67 |  | 7/16 |
| MNQ | 15 | h1 * | -0.014 | -0.022 .. -0.005 | -2.6% | -0.028 | 0.0012 | 0.201 | 11/16 |
| MNQ | 15 | h2 | -0.013 | -0.031 .. +0.006 | -1.6% | -0.029 | 0.18 |  | 11/16 |
| MNQ | 15 | h4 | -0.012 | -0.057 .. +0.033 | -1.1% | -0.032 | 0.6 |  | 10/16 |
| MNQ | 15 | h8 | -0.007 | -0.094 .. +0.081 | -0.4% | -0.011 | 0.88 |  | 10/16 |
| MNQ | 15 | h16 | -0.004 | -0.154 .. +0.145 | -0.2% | +0.037 | 0.95 |  | 10/16 |
| MNQ | 15 | eod | +0.145 | -0.612 .. +0.901 | +2.3% | +0.025 | 0.72 |  | 6/16 |
| MNQ | 60 | h1 * | -0.024 | -0.038 .. -0.011 | -4.6% | -0.039 | 0.00041 | 0.0754 | 12/16 |
| MNQ | 60 | h2 | -0.042 | -0.066 .. -0.019 | -5.5% | -0.063 | 0.00043 |  | 12/16 |
| MNQ | 60 | h4 | -0.072 | -0.114 .. -0.031 | -6.5% | -0.103 | 0.00062 |  | 12/16 |
| MNQ | 60 | h8 | -0.116 | -0.187 .. -0.044 | -7.3% | -0.167 | 0.0018 |  | 12/16 |
| MNQ | 60 | h16 | -0.140 | -0.270 .. -0.010 | -6.4% | -0.238 | 0.037 |  | 10/16 |
| MNQ | 60 | eod | -0.131 | -0.278 .. +0.015 | -5.7% | -0.243 | 0.088 |  | 10/16 |
| MYM | 5 | h1 * | -0.018 | -0.030 .. -0.006 | -3.4% | -0.027 | 0.0032 | 0.493 | 5/8 |
| MYM | 5 | h2 | -0.032 | -0.061 .. -0.002 | -4.2% | -0.050 | 0.035 |  | 5/8 |
| MYM | 5 | h4 | -0.050 | -0.118 .. +0.019 | -4.5% | -0.083 | 0.15 |  | 4/8 |
| MYM | 5 | h8 | -0.073 | -0.191 .. +0.046 | -4.6% | -0.134 | 0.23 |  | 3/8 |
| MYM | 5 | h16 | -0.099 | -0.280 .. +0.082 | -4.3% | -0.226 | 0.29 |  | 5/8 |
| MYM | 5 | eod | -0.045 | -1.159 .. +1.069 | -0.4% | -0.154 | 0.94 |  | 3/8 |
| MYM | 15 | h1 * | -0.024 | -0.040 .. -0.009 | -4.6% | -0.044 | 0.0022 | 0.361 | 5/8 |
| MYM | 15 | h2 | -0.047 | -0.079 .. -0.014 | -6.1% | -0.075 | 0.0045 |  | 6/8 |
| MYM | 15 | h4 | -0.098 | -0.195 .. -0.000 | -8.8% | -0.174 | 0.052 |  | 5/8 |
| MYM | 15 | h8 | -0.176 | -0.356 .. +0.005 | -10.7% | -0.349 | 0.061 |  | 6/8 |
| MYM | 15 | h16 | -0.288 | -0.591 .. +0.016 | -11.7% | -0.629 | 0.069 |  | 6/8 |
| MYM | 15 | eod | -0.523 | -1.586 .. +0.539 | -8.7% | -0.844 | 0.34 |  | 5/8 |
| MYM | 60 | h1 * | -0.016 | -0.037 .. +0.006 | -3.0% | -0.037 | 0.17 | 1 | 5/8 |
| MYM | 60 | h2 | -0.017 | -0.053 .. +0.019 | -2.3% | -0.051 | 0.42 |  | 5/8 |
| MYM | 60 | h4 | -0.032 | -0.095 .. +0.031 | -2.9% | -0.079 | 0.35 |  | 5/8 |
| MYM | 60 | h8 | -0.073 | -0.187 .. +0.041 | -4.7% | -0.123 | 0.27 |  | 4/8 |
| MYM | 60 | h16 | -0.107 | -0.315 .. +0.102 | -5.0% | -0.171 | 0.32 |  | 4/8 |
| MYM | 60 | eod | -0.111 | -0.351 .. +0.129 | -5.0% | -0.197 | 0.38 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.32 pts | -0.88 .. +0.23 | 0.29 |
| MES | 15 | -0.00 pts | -1.01 .. +1.00 | 0.99 |
| MES | 60 | +0.71 pts | -1.37 .. +2.79 | 0.51 |
| MNQ | 5 | +0.22 pts | -0.38 .. +0.81 | 0.52 |
| MNQ | 15 | +0.47 pts | -0.57 .. +1.51 | 0.37 |
| MNQ | 60 | +1.28 pts | -0.84 .. +3.39 | 0.24 |
| MYM | 5 | +0.03 pts | -0.71 .. +0.78 | 0.95 |
| MYM | 15 | +0.23 pts | -1.18 .. +1.63 | 0.75 |
| MYM | 60 | +1.80 pts | -1.11 .. +4.70 | 0.29 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | long | 206808 | -0.000 | 0.342 | +0.01 | -3.49 | -3.51 | -3.48 | -3.49 |
| MES | 5 | h2 | bottom fifth | long | 206808 | +0.001 | 0.273 | +0.00 | -3.50 | -3.46 | -3.53 | -3.50 |
| MES | 5 | h4 | bottom fifth | long | 206808 | +0.004 | 0.273 | +0.00 | -3.50 | -3.41 | -3.58 | -3.50 |
| MES | 5 | h8 | bottom fifth | long | 206808 | +0.014 | 0.273 | +0.09 | -3.41 | -3.24 | -3.56 | -3.45 |
| MES | 5 | h16 | bottom fifth | long | 206808 | +0.033 | 0.273 | +0.39 | -3.11 | -3.01 | -3.20 | -3.32 |
| MES | 5 | eod | top fifth | long | 206808 | +0.406 | 0.342 | +3.10 | -0.40 | +0.39 | -1.06 | -3.36 |
| MES | 15 | h1 | bottom fifth | long | 67998 | +0.006 | 0.158 | +0.05 | -3.45 | -3.40 | -3.49 | -3.51 |
| MES | 15 | h2 | bottom fifth | long | 67998 | +0.010 | 0.158 | +0.11 | -3.39 | -3.29 | -3.48 | -3.48 |
| MES | 15 | h4 | top fifth | long | 67997 | +0.030 | 0.220 | +0.32 | -3.18 | -3.12 | -3.24 | -3.42 |
| MES | 15 | h8 | top fifth | long | 67997 | +0.054 | 0.220 | +0.42 | -3.08 | -2.81 | -3.32 | -3.49 |
| MES | 15 | h16 | top fifth | long | 67997 | +0.105 | 0.220 | +0.99 | -2.51 | -2.16 | -2.83 | -3.53 |
| MES | 15 | eod | bottom fifth | long | 67998 | +0.074 | 0.158 | +4.75 | +1.25 | +0.54 | +1.92 | +2.46 |
| MES | 60 | h1 | top fifth | long | 16261 | +0.015 | 0.115 | +0.42 | -3.08 | -3.31 | -2.88 | -3.35 |
| MES | 60 | h2 | top fifth | long | 16261 | +0.030 | 0.115 | +0.92 | -2.58 | -3.20 | -2.03 | -3.15 |
| MES | 60 | h4 | top fifth | long | 16261 | +0.058 | 0.115 | +2.07 | -1.43 | -2.93 | -0.07 | -2.44 |
| MES | 60 | h8 | top fifth | long | 16261 | +0.076 | 0.115 | +3.05 | -0.45 | -2.84 | +1.70 | -2.26 |
| MES | 60 | h16 | top fifth | long | 16261 | +0.097 | 0.115 | +3.49 | -0.01 | -3.10 | +2.77 | -2.95 |
| MES | 60 | eod | bottom fifth | long | 16261 | +0.073 | 0.074 | +4.62 | +1.12 | -0.92 | +2.99 | -2.20 |
| MNQ | 5 | h1 | top fifth | long | 206458 | +0.009 | 0.154 | +0.08 | -1.92 | -1.97 | -1.88 | -1.96 |
| MNQ | 5 | h2 | top fifth | long | 206458 | +0.017 | 0.154 | +0.17 | -1.83 | -1.93 | -1.73 | -1.90 |
| MNQ | 5 | h4 | top fifth | long | 206458 | +0.030 | 0.154 | +0.33 | -1.67 | -1.87 | -1.47 | -1.81 |
| MNQ | 5 | h8 | top fifth | long | 206458 | +0.051 | 0.154 | +0.58 | -1.42 | -1.74 | -1.08 | -1.71 |
| MNQ | 5 | h16 | top fifth | long | 206458 | +0.094 | 0.154 | +1.01 | -0.99 | -1.49 | -0.45 | -1.62 |
| MNQ | 5 | eod | top fifth | long | 206458 | +0.955 | 0.154 | +3.72 | +1.72 | +1.88 | +1.55 | -4.01 |
| MNQ | 15 | h1 | top fifth | long | 67966 | +0.015 | 0.095 | +0.25 | -1.75 | -1.86 | -1.64 | -1.86 |
| MNQ | 15 | h2 | top fifth | long | 67966 | +0.019 | 0.095 | +0.49 | -1.51 | -1.74 | -1.27 | -1.70 |
| MNQ | 15 | h4 | top fifth | long | 67966 | +0.023 | 0.095 | +0.82 | -1.18 | -1.53 | -0.83 | -1.55 |
| MNQ | 15 | h8 | bottom fifth | long | 67966 | +0.027 | 0.064 | -0.08 | -2.08 | -1.36 | -2.79 | -2.63 |
| MNQ | 15 | h16 | bottom fifth | long | 67966 | +0.054 | 0.064 | +0.02 | -1.98 | -0.82 | -3.13 | -2.04 |
| MNQ | 15 | eod | bottom fifth | long | 67966 | +0.283 | 0.064 | +8.61 | +6.61 | +2.25 | +10.93 | +7.99 |
| MNQ | 60 | h1 | top fifth | long | 16261 | +0.021 | 0.047 | +0.79 | -1.21 | -1.71 | -0.71 | -1.85 |
| MNQ | 60 | h2 | top fifth | long | 16261 | +0.040 | 0.047 | +1.38 | -0.62 | -1.49 | +0.25 | -1.87 |
| MNQ | 60 | h4 | top fifth | long | 16261 | +0.077 | 0.047 | +2.90 | +0.90 | -1.13 | +2.90 | -1.35 |
| MNQ | 60 | h8 | bottom fifth | long | 16261 | +0.064 | 0.029 | +3.98 | +1.98 | +0.09 | +3.70 | -0.00 |
| MNQ | 60 | h16 | bottom fifth | long | 16261 | +0.117 | 0.029 | +9.22 | +7.22 | +1.32 | +12.59 | +4.51 |
| MNQ | 60 | eod | bottom fifth | long | 16261 | +0.147 | 0.029 | +12.57 | +10.57 | +1.32 | +18.99 | +7.07 |
| MYM | 5 | h1 | top fifth | short | 103585 | +0.006 | 0.189 | +0.03 | -1.97 | +nan | -1.97 | -1.98 |
| MYM | 5 | h2 | bottom fifth | short | 103585 | +0.019 | 0.149 | -0.00 | -2.00 | +nan | -2.00 | -2.11 |
| MYM | 5 | h4 | bottom fifth | short | 103585 | +0.050 | 0.149 | +0.03 | -1.97 | +nan | -1.97 | -2.26 |
| MYM | 5 | h8 | bottom fifth | short | 103585 | +0.093 | 0.149 | +0.09 | -1.91 | +nan | -1.91 | -2.46 |
| MYM | 5 | h16 | top fifth | long | 103585 | -0.004 | 0.189 | -0.04 | -2.04 | +nan | -2.04 | -2.38 |
| MYM | 5 | eod | top fifth | long | 103585 | +0.376 | 0.189 | +3.64 | +1.64 | +nan | +1.64 | -0.36 |
| MYM | 15 | h1 | top fifth | long | 34062 | +0.006 | 0.115 | +0.04 | -1.96 | +nan | -1.96 | -2.02 |
| MYM | 15 | h2 | top fifth | long | 34062 | +0.011 | 0.115 | +0.06 | -1.94 | +nan | -1.94 | -2.07 |
| MYM | 15 | h4 | top fifth | long | 34062 | +0.025 | 0.115 | +0.21 | -1.79 | +nan | -1.79 | -2.02 |
| MYM | 15 | h8 | top fifth | long | 34062 | +0.039 | 0.115 | +0.26 | -1.74 | +nan | -1.74 | -2.02 |
| MYM | 15 | h16 | top fifth | long | 34062 | +0.071 | 0.115 | +0.85 | -1.15 | +nan | -1.15 | -1.73 |
| MYM | 15 | eod | top fifth | long | 34062 | +0.441 | 0.115 | +3.97 | +1.97 | +nan | +1.97 | -0.66 |
| MYM | 60 | h1 | top fifth | long | 8120 | +0.022 | 0.057 | +0.56 | -1.44 | +nan | -1.44 | -1.70 |
| MYM | 60 | h2 | top fifth | long | 8120 | +0.043 | 0.057 | +1.18 | -0.82 | +nan | -0.82 | -1.38 |
| MYM | 60 | h4 | top fifth | long | 8120 | +0.079 | 0.057 | +2.40 | +0.40 | +nan | +0.40 | -0.71 |
| MYM | 60 | h8 | top fifth | long | 8120 | +0.097 | 0.057 | +3.10 | +1.10 | +nan | +1.10 | -0.56 |
| MYM | 60 | h16 | top fifth | long | 8120 | +0.136 | 0.057 | +3.81 | +1.81 | +nan | +1.81 | -1.02 |
| MYM | 60 | eod | top fifth | long | 8120 | +0.140 | 0.057 | +3.86 | +1.86 | +nan | +1.86 | -1.54 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.493 | -0.869 | -0.258 | -0.042 | -0.006 | +0.000 | +0.000 | -0.001 | -0.003 | -0.014 | -0.006 |
| MES | 15 | -1.443 | -0.821 | -0.248 | -0.043 | -0.009 | +0.000 | +0.003 | +0.005 | +0.012 | +0.026 | +0.027 |
| MES | 60 | -1.718 | -0.907 | -0.304 | -0.060 | -0.013 | +0.000 | +0.011 | +0.019 | +0.041 | +0.058 | -0.059 |
| MNQ | 5 | -1.602 | -0.932 | -0.282 | -0.050 | -0.011 | +0.000 | +0.007 | +0.013 | +0.020 | +0.022 | +0.028 |
| MNQ | 15 | -1.486 | -0.833 | -0.261 | -0.051 | -0.013 | +0.000 | +0.008 | +0.009 | +0.001 | -0.008 | -0.072 |
| MNQ | 60 | -1.937 | -0.969 | -0.328 | -0.061 | -0.010 | +0.000 | +0.005 | +0.008 | +0.007 | +0.002 | +0.016 |
| MYM | 5 | -1.605 | -0.943 | -0.285 | -0.049 | -0.008 | +0.000 | +0.003 | +0.007 | +0.016 | +0.026 | +0.042 |
| MYM | 15 | -1.521 | -0.876 | -0.278 | -0.058 | -0.014 | +0.000 | +0.017 | +0.030 | +0.075 | +0.133 | +0.280 |
| MYM | 60 | -1.823 | -0.985 | -0.315 | -0.060 | -0.016 | +0.000 | +0.016 | +0.030 | +0.071 | +0.101 | +0.127 |

## Calibration

- MES 5-min: 1034039 bars, 206808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 339986 bars, 67997 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81304 bars, 16261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1032290 bars, 206458 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 339830 bars, 67966 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81302 bars, 16261 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 517923 bars, 103585 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170311 bars, 34062 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40600 bars, 8120 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
