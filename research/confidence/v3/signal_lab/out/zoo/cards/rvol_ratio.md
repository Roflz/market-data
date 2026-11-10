# Impact card: rvol_ratio

realized volatility of the last 20 bars / last 200 bars [controls: 15-min slot, weekday, year (trend state / volatility NOT controlled: they are the metric)]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=0.75; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 5-min size: the market moves 15% LESS in the metric's top fifth than in its bottom fifth over the next 16 bars (80 min) (-0.320 R20, CONFIRMED, q=1.79e-21, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.33 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.204 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.008 R20 over the next 1 bar (15 min), p=0.31; we would catch an effect of 0.045 R20 or more 80% of the time).
- MES 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.050 R20, CONFIRMED, q=3.71e-34, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.75 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.122 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.023 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.096 R20 or more 80% of the time).
- MES 60-min size: the market moves 12% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.062 R20, CONFIRMED, q=3.76e-16, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.38 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.061 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.026 R20 over the next 8 bars (40 min), p=1; we would catch an effect of 0.027 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.050 R20, CONFIRMED, q=2.86e-31, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.38 at recent bar sizes, 90% range up to $1.49); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.011 R20 over the next 1 bar (15 min), p=0.081; we would catch an effect of 0.049 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.054 R20, CONFIRMED, q=1.42e-23, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $3.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.197 R20 over the rest of the session (to 16:45), p=0.69; we would catch an effect of 0.103 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 14% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.075 R20, CONFIRMED, q=1.83e-18, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $9.36 at recent bar sizes, 90% range up to $7.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.052 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MYM 5-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.054 R20, CONFIRMED, q=1.35e-41, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.34 at recent bar sizes, 90% range up to $1.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.009 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.069 R20 or more 80% of the time).
- MYM 15-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.059 R20, CONFIRMED, q=6.07e-15, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.87 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.092 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.034 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.139 R20 or more 80% of the time).
- MYM 60-min size: the market moves 16% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.084 R20, CONFIRMED, q=1.4e-11, 7 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.76 at recent bar sizes, 90% range up to $3.88); about 5.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.008 .. +0.001 | -0.0019 | 0.13 / 0.13 / 0.042 | 0.0427 | 1 | 1 | 11/16 | -0.007 | -0.000 | False | -1.5 / -1.5 |  |
| MES | 5 | h2 | -0.004 | -0.014 .. +0.006 | +0.0002 | 0.48 / 0.46 / 0.25 | 0.255 |  |  | 9/16 | -0.012 | +0.005 |  | -1.1 / -0.7 |  |
| MES | 5 | h4 | -0.002 | -0.025 .. +0.020 | +0.0023 | 0.84 / 0.83 / 0.7 | 0.719 |  |  | 8/16 | -0.021 | +0.017 |  | -0.5 / -0.2 | 0.024 |
| MES | 5 | h8 | +0.002 | -0.043 .. +0.047 | +0.0045 | 0.93 / 0.93 / 0.87 | 0.873 |  |  | 9/16 | -0.040 | +0.043 |  | +0.3 / +0.1 |  |
| MES | 5 | h16 | -0.004 | -0.082 .. +0.074 | +0.0030 | 0.93 / 0.92 / 0.88 | 0.89 |  |  | 10/16 | -0.077 | +0.070 |  | -0.4 / -0.1 |  |
| MES | 5 | eod | -0.147 | -1.153 .. +0.860 | +0.0039 | 0.78 / 0.77 / 0.5 | 0.496 |  |  | 10/16 | -0.630 | +0.334 |  | -2.4 / -0.3 |  |
| MES | 15 | h1 * | -0.008 | -0.015 .. -0.000 | -0.0054 | 0.049 / 0.052 / 0.025 | 0.0227 | 1 | 1 | 9/16 | -0.008 | -0.007 | False | -1.8 / -2.0 |  |
| MES | 15 | h2 | -0.012 | -0.030 .. +0.005 | -0.0038 | 0.17 / 0.17 / 0.065 | 0.063 |  |  | 11/16 | -0.020 | -0.005 |  | -1.8 / -1.4 |  |
| MES | 15 | h4 | -0.025 | -0.063 .. +0.014 | -0.0027 | 0.21 / 0.21 / 0.061 | 0.0617 |  |  | 12/16 | -0.044 | -0.005 |  | -2.4 / -1.3 | 0.045 |
| MES | 15 | h8 | -0.062 | -0.134 .. +0.011 | -0.0041 | 0.095 / 0.093 / 0.014 | 0.0159 |  |  | 12/16 | -0.083 | -0.041 |  | -4.2 / -1.7 |  |
| MES | 15 | h16 | -0.117 | -0.259 .. +0.024 | -0.0031 | 0.1 / 0.11 / 0.017 | 0.0193 |  |  | 12/16 | -0.151 | -0.084 |  | -5.6 / -1.6 |  |
| MES | 15 | eod | -0.073 | -0.767 .. +0.620 | +0.0120 | 0.84 / 0.83 / 0.69 | 0.692 |  |  | 9/16 | -0.397 | +0.248 |  | -1.2 / -0.2 |  |
| MES | 60 | h1 | -0.010 | -0.028 .. +0.009 | -0.0014 | 0.32 / 0.3 / 0.32 | 0.308 |  |  | 11/16 | -0.001 | -0.018 |  | -1.0 / -1.0 |  |
| MES | 60 | h2 * | -0.023 | -0.058 .. +0.012 | -0.0025 | 0.2 / 0.19 / 0.22 | 0.223 | 1 | 1 | 12/16 | -0.008 | -0.037 | False | -1.7 / -1.3 |  |
| MES | 60 | h4 | -0.026 | -0.091 .. +0.039 | -0.0028 | 0.44 / 0.43 / 0.47 | 0.469 |  |  | 11/16 | -0.009 | -0.042 |  | -1.4 / -0.8 | 0.096 |
| MES | 60 | h8 | -0.019 | -0.133 .. +0.095 | -0.0017 | 0.74 / 0.75 / 0.77 | 0.775 |  |  | 7/16 | +0.031 | -0.069 |  | -0.8 / -0.3 |  |
| MES | 60 | h16 | -0.039 | -0.234 .. +0.157 | -0.0041 | 0.7 / 0.71 / 0.73 | 0.738 |  |  | 8/16 | +0.039 | -0.116 |  | -1.2 / -0.4 |  |
| MES | 60 | eod | -0.059 | -0.275 .. +0.157 | -0.0071 | 0.59 / 0.62 / 0.64 | 0.65 |  |  | 8/16 | +0.024 | -0.142 |  | -1.7 / -0.5 |  |
| MNQ | 5 | h1 | -0.001 | -0.007 .. +0.005 | +0.0008 | 0.67 / 0.66 / 0.53 | 0.539 |  |  | 8/16 | -0.007 | +0.004 |  | -0.5 / -0.4 |  |
| MNQ | 5 | h2 | +0.003 | -0.017 .. +0.024 | +0.0069 | 0.75 / 0.73 / 0.4 | 0.403 |  |  | 8/16 | -0.015 | +0.021 |  | +0.6 / +0.3 |  |
| MNQ | 5 | h4 | +0.010 | -0.035 .. +0.055 | +0.0103 | 0.66 / 0.64 / 0.2 | 0.204 |  |  | 7/16 | -0.028 | +0.047 |  | +1.1 / +0.4 | 0.027 |
| MNQ | 5 | h8 * | +0.026 | -0.064 .. +0.116 | +0.0142 | 0.57 / 0.55 / 0.068 | 0.068 | 1 | 1 | 7/16 | -0.046 | +0.098 | False | +2.1 / +0.6 |  |
| MNQ | 5 | h16 | +0.033 | -0.125 .. +0.191 | +0.0160 | 0.68 / 0.67 / 0.2 | 0.202 |  |  | 6/16 | -0.103 | +0.168 |  | +2.0 / +0.4 |  |
| MNQ | 5 | eod | -0.002 | -1.400 .. +1.397 | +0.0048 | 1 / 1 / 1 | 0.999 |  |  | 7/16 | -1.343 | +1.327 |  | -0.0 / -0.0 |  |
| MNQ | 15 | h1 * | -0.011 | -0.020 .. -0.002 | -0.0037 | 0.013 / 0.014 / 0.00089 | 0.0013 | 1 | 0.931 | 11/16 | -0.020 | -0.003 | False | -2.5 / -2.5 |  |
| MNQ | 15 | h2 | -0.011 | -0.043 .. +0.020 | +0.0037 | 0.48 / 0.48 / 0.14 | 0.141 |  |  | 11/16 | -0.041 | +0.018 |  | -1.2 / -0.7 |  |
| MNQ | 15 | h4 | -0.014 | -0.092 .. +0.063 | +0.0076 | 0.72 / 0.71 / 0.39 | 0.386 |  |  | 12/16 | -0.076 | +0.047 |  | -0.8 / -0.4 | 0.049 |
| MNQ | 15 | h8 | -0.044 | -0.162 .. +0.074 | +0.0041 | 0.46 / 0.45 / 0.15 | 0.152 |  |  | 11/16 | -0.134 | +0.045 |  | -1.9 / -0.7 |  |
| MNQ | 15 | h16 | -0.107 | -0.315 .. +0.101 | +0.0030 | 0.31 / 0.31 / 0.064 | 0.0633 |  |  | 10/16 | -0.258 | +0.043 |  | -3.5 / -1.0 |  |
| MNQ | 15 | eod | -0.270 | -1.244 .. +0.704 | +0.0105 | 0.59 / 0.59 / 0.25 | 0.253 |  |  | 11/16 | -1.005 | +0.459 |  | -2.7 / -0.5 |  |
| MNQ | 60 | h1 | -0.015 | -0.035 .. +0.006 | -0.0034 | 0.16 / 0.15 / 0.16 | 0.159 |  |  | 11/16 | -0.006 | -0.024 |  | -1.5 / -1.4 |  |
| MNQ | 60 | h2 | -0.018 | -0.056 .. +0.020 | -0.0045 | 0.35 / 0.35 / 0.36 | 0.357 |  |  | 11/16 | -0.002 | -0.034 |  | -1.3 / -0.9 |  |
| MNQ | 60 | h4 | -0.032 | -0.101 .. +0.037 | -0.0052 | 0.37 / 0.38 / 0.4 | 0.397 |  |  | 10/16 | -0.001 | -0.062 |  | -1.6 / -0.9 | 0.103 |
| MNQ | 60 | h8 | -0.044 | -0.168 .. +0.080 | -0.0052 | 0.48 / 0.5 / 0.52 | 0.52 |  |  | 9/16 | +0.004 | -0.093 |  | -1.6 / -0.7 |  |
| MNQ | 60 | h16 | -0.160 | -0.383 .. +0.062 | -0.0107 | 0.16 / 0.16 / 0.19 | 0.192 |  |  | 10/16 | -0.139 | -0.182 |  | -4.6 / -1.4 |  |
| MNQ | 60 | eod * | -0.197 | -0.441 .. +0.047 | -0.0132 | 0.11 / 0.11 / 0.15 | 0.148 | 1 | 1 | 12/16 | -0.196 | -0.198 | False | -5.4 / -1.6 |  |
| MYM | 5 | h1 | +0.003 | -0.005 .. +0.012 | +0.0059 | 0.47 / 0.49 / 0.28 | 0.28 |  |  | 5/8 | n/a | +0.003 |  | +0.8 / +0.7 |  |
| MYM | 5 | h2 | +0.022 | -0.014 .. +0.057 | +0.0175 | 0.23 / 0.23 / 0.0054 | 0.00421 |  |  | 5/8 | n/a | +0.022 |  | +2.3 / +1.2 |  |
| MYM | 5 | h4 * | +0.052 | -0.030 .. +0.134 | +0.0254 | 0.21 / 0.21 / 0.0014 | 0.00211 | 1 | 1 | 5/8 | n/a | +0.052 | False | +3.4 / +1.3 | 0.044 |
| MYM | 5 | h8 | +0.094 | -0.064 .. +0.252 | +0.0322 | 0.24 / 0.25 / 0.00026 | 0.000527 |  |  | 6/8 | n/a | +0.094 |  | +4.4 / +1.2 |  |
| MYM | 5 | h16 | +0.118 | -0.115 .. +0.351 | +0.0319 | 0.32 / 0.32 / 0.0035 | 0.00316 |  |  | 4/8 | n/a | +0.118 |  | +4.5 / +1.0 |  |
| MYM | 5 | eod | +0.379 | -1.648 .. +2.406 | +0.0211 | 0.71 / 0.71 / 0.29 | 0.289 |  |  | 4/8 | n/a | +0.379 |  | +3.2 / +0.4 |  |
| MYM | 15 | h1 | -0.002 | -0.016 .. +0.012 | +0.0008 | 0.77 / 0.77 / 0.71 | 0.694 |  |  | 5/8 | n/a | -0.002 |  | -0.3 / -0.3 |  |
| MYM | 15 | h2 * | +0.009 | -0.037 .. +0.056 | +0.0103 | 0.7 / 0.69 / 0.44 | 0.428 | 1 | 1 | 3/8 | n/a | +0.009 | False | +0.6 / +0.4 |  |
| MYM | 15 | h4 | +0.022 | -0.092 .. +0.136 | +0.0156 | 0.7 / 0.71 / 0.38 | 0.36 |  |  | 3/8 | n/a | +0.022 |  | +0.7 / +0.4 | 0.069 |
| MYM | 15 | h8 | +0.009 | -0.184 .. +0.203 | +0.0194 | 0.92 / 0.92 / 0.83 | 0.827 |  |  | 3/8 | n/a | +0.009 |  | +0.2 / +0.1 |  |
| MYM | 15 | h16 | +0.025 | -0.351 .. +0.401 | +0.0295 | 0.9 / 0.9 / 0.76 | 0.759 |  |  | 2/8 | n/a | +0.025 |  | +0.5 / +0.1 |  |
| MYM | 15 | eod | +0.134 | -1.204 .. +1.473 | +0.0310 | 0.84 / 0.84 / 0.67 | 0.654 |  |  | 3/8 | n/a | +0.134 |  | +1.0 / +0.2 |  |
| MYM | 60 | h1 | +0.002 | -0.024 .. +0.027 | -0.0009 | 0.9 / 0.9 / 0.91 | 0.904 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 60 | h2 | +0.013 | -0.036 .. +0.063 | +0.0012 | 0.59 / 0.6 / 0.62 | 0.624 |  |  | 5/8 | n/a | +0.013 |  | +0.7 / +0.5 |  |
| MYM | 60 | h4 * | +0.034 | -0.061 .. +0.130 | +0.0042 | 0.48 / 0.49 / 0.5 | 0.522 | 1 | 1 | 5/8 | n/a | +0.034 | False | +1.3 / +0.7 | 0.139 |
| MYM | 60 | h8 | +0.022 | -0.157 .. +0.201 | +0.0059 | 0.81 / 0.81 / 0.82 | 0.831 |  |  | 3/8 | n/a | +0.022 |  | +0.6 / +0.2 |  |
| MYM | 60 | h16 | +0.039 | -0.268 .. +0.346 | +0.0081 | 0.8 / 0.81 / 0.82 | 0.807 |  |  | 4/8 | n/a | +0.039 |  | +0.8 / +0.2 |  |
| MYM | 60 | eod | +0.035 | -0.306 .. +0.375 | +0.0076 | 0.84 / 0.85 / 0.85 | 0.848 |  |  | 4/8 | n/a | +0.035 |  | +0.7 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.028 | -0.035 .. -0.022 | -5.7% | -0.055 | 2.2e-17 |  | 13/16 |
| MES | 5 | h2 | -0.051 | -0.061 .. -0.041 | -7.3% | -0.092 | 5e-23 |  | 13/16 |
| MES | 5 | h4 | -0.096 | -0.115 .. -0.077 | -9.6% | -0.169 | 5.5e-23 |  | 13/16 |
| MES | 5 | h8 | -0.180 | -0.216 .. -0.144 | -12.5% | -0.322 | 1.7e-22 |  | 14/16 |
| MES | 5 | h16 * | -0.320 | -0.382 .. -0.258 | -15.3% | -0.608 | 2.9e-24 | 1.79e-21 | 14/16 |
| MES | 5 | eod | -3.738 | -4.629 .. -2.846 | -37.7% | -6.561 | 2e-16 |  | 14/16 |
| MES | 15 | h1 * | -0.050 | -0.058 .. -0.043 | -9.9% | -0.106 | 4.4e-37 | 3.71e-34 | 15/16 |
| MES | 15 | h2 | -0.093 | -0.108 .. -0.077 | -12.7% | -0.182 | 1.1e-32 |  | 16/16 |
| MES | 15 | h4 | -0.167 | -0.199 .. -0.134 | -15.8% | -0.323 | 3.5e-24 |  | 16/16 |
| MES | 15 | h8 | -0.302 | -0.362 .. -0.242 | -19.7% | -0.587 | 9.6e-23 |  | 16/16 |
| MES | 15 | h16 | -0.565 | -0.673 .. -0.457 | -24.7% | -1.104 | 1.3e-24 |  | 16/16 |
| MES | 15 | eod | -1.975 | -2.566 .. -1.385 | -36.1% | -3.629 | 5.6e-11 |  | 15/16 |
| MES | 60 | h1 * | -0.062 | -0.074 .. -0.050 | -12.1% | -0.134 | 7.3e-19 | 3.76e-16 | 15/16 |
| MES | 60 | h2 | -0.090 | -0.111 .. -0.070 | -12.2% | -0.204 | 1.5e-14 |  | 15/16 |
| MES | 60 | h4 | -0.138 | -0.176 .. -0.099 | -13.0% | -0.317 | 3.1e-09 |  | 15/16 |
| MES | 60 | h8 | -0.204 | -0.276 .. -0.132 | -13.6% | -0.475 | 4.4e-06 |  | 14/16 |
| MES | 60 | h16 | -0.245 | -0.370 .. -0.120 | -12.0% | -0.672 | 0.0013 |  | 13/16 |
| MES | 60 | eod | -0.241 | -0.383 .. -0.100 | -11.2% | -0.694 | 0.0045 |  | 12/16 |
| MNQ | 5 | h1 * | -0.050 | -0.058 .. -0.042 | -9.4% | -0.080 | 3.5e-34 | 2.86e-31 | 14/16 |
| MNQ | 5 | h2 | -0.094 | -0.116 .. -0.073 | -12.3% | -0.156 | 1.4e-18 |  | 14/16 |
| MNQ | 5 | h4 | -0.170 | -0.215 .. -0.125 | -15.3% | -0.294 | 9.7e-14 |  | 16/16 |
| MNQ | 5 | h8 | -0.304 | -0.393 .. -0.216 | -18.8% | -0.552 | 1.3e-11 |  | 16/16 |
| MNQ | 5 | h16 | -0.510 | -0.659 .. -0.362 | -21.3% | -1.016 | 1.5e-11 |  | 16/16 |
| MNQ | 5 | eod | -5.481 | -6.760 .. -4.201 | -43.8% | -10.160 | 4.6e-17 |  | 16/16 |
| MNQ | 15 | h1 * | -0.054 | -0.064 .. -0.044 | -10.2% | -0.110 | 2.2e-26 | 1.42e-23 | 14/16 |
| MNQ | 15 | h2 | -0.107 | -0.137 .. -0.078 | -13.9% | -0.206 | 1.2e-12 |  | 16/16 |
| MNQ | 15 | h4 | -0.199 | -0.271 .. -0.128 | -17.6% | -0.382 | 5.4e-08 |  | 16/16 |
| MNQ | 15 | h8 | -0.357 | -0.474 .. -0.239 | -21.3% | -0.711 | 4.4e-09 |  | 16/16 |
| MNQ | 15 | h16 | -0.649 | -0.831 .. -0.466 | -25.7% | -1.331 | 5.1e-12 |  | 16/16 |
| MNQ | 15 | eod | -2.443 | -3.333 .. -1.553 | -38.5% | -4.449 | 7.4e-08 |  | 15/16 |
| MNQ | 60 | h1 * | -0.075 | -0.089 .. -0.062 | -14.2% | -0.157 | 3.2e-21 | 1.83e-18 | 16/16 |
| MNQ | 60 | h2 | -0.121 | -0.145 .. -0.097 | -15.8% | -0.249 | 5e-20 |  | 16/16 |
| MNQ | 60 | h4 | -0.196 | -0.236 .. -0.155 | -17.7% | -0.394 | 1e-16 |  | 16/16 |
| MNQ | 60 | h8 | -0.305 | -0.381 .. -0.229 | -19.3% | -0.616 | 3.8e-12 |  | 15/16 |
| MNQ | 60 | h16 | -0.383 | -0.522 .. -0.245 | -17.5% | -0.867 | 1.6e-06 |  | 14/16 |
| MNQ | 60 | eod | -0.400 | -0.560 .. -0.240 | -17.4% | -0.895 | 3.8e-06 |  | 14/16 |
| MYM | 5 | h1 * | -0.054 | -0.062 .. -0.047 | -10.2% | -0.080 | 1.4e-44 | 1.35e-41 | 8/8 |
| MYM | 5 | h2 | -0.105 | -0.136 .. -0.073 | -13.8% | -0.161 | 6e-11 |  | 8/8 |
| MYM | 5 | h4 | -0.195 | -0.270 .. -0.119 | -17.8% | -0.316 | 4.3e-07 |  | 8/8 |
| MYM | 5 | h8 | -0.340 | -0.492 .. -0.188 | -21.4% | -0.590 | 1.3e-05 |  | 8/8 |
| MYM | 5 | h16 | -0.541 | -0.753 .. -0.329 | -23.2% | -1.031 | 6.5e-07 |  | 8/8 |
| MYM | 5 | eod | -4.939 | -6.602 .. -3.276 | -42.4% | -9.501 | 5.9e-09 |  | 8/8 |
| MYM | 15 | h1 * | -0.059 | -0.072 .. -0.045 | -11.1% | -0.112 | 1.3e-17 | 6.07e-15 | 7/8 |
| MYM | 15 | h2 | -0.121 | -0.163 .. -0.078 | -15.8% | -0.223 | 2.4e-08 |  | 8/8 |
| MYM | 15 | h4 | -0.221 | -0.328 .. -0.113 | -19.9% | -0.425 | 7.7e-05 |  | 8/8 |
| MYM | 15 | h8 | -0.377 | -0.563 .. -0.190 | -23.0% | -0.780 | 9.5e-05 |  | 8/8 |
| MYM | 15 | h16 | -0.671 | -0.997 .. -0.345 | -27.4% | -1.404 | 7.8e-05 |  | 8/8 |
| MYM | 15 | eod | -2.484 | -3.600 .. -1.368 | -41.5% | -4.657 | 1.7e-05 |  | 8/8 |
| MYM | 60 | h1 * | -0.084 | -0.104 .. -0.065 | -16.1% | -0.175 | 3.5e-14 | 1.4e-11 | 7/8 |
| MYM | 60 | h2 | -0.127 | -0.158 .. -0.096 | -16.9% | -0.268 | 3.7e-12 |  | 7/8 |
| MYM | 60 | h4 | -0.177 | -0.231 .. -0.123 | -16.5% | -0.396 | 1.3e-08 |  | 7/8 |
| MYM | 60 | h8 | -0.260 | -0.362 .. -0.158 | -16.9% | -0.593 | 6.5e-07 |  | 8/8 |
| MYM | 60 | h16 | -0.266 | -0.474 .. -0.059 | -12.7% | -0.803 | 0.012 |  | 6/8 |
| MYM | 60 | eod | -0.259 | -0.497 .. -0.022 | -11.7% | -0.814 | 0.032 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.42 pts | -1.01 .. +0.17 | 0.16 |
| MES | 15 | -0.36 pts | -1.29 .. +0.57 | 0.45 |
| MES | 60 | +0.91 pts | -1.18 .. +3.00 | 0.4 |
| MNQ | 5 | -0.20 pts | -0.76 .. +0.37 | 0.49 |
| MNQ | 15 | -0.86 pts | -1.77 .. +0.04 | 0.066 |
| MNQ | 60 | +1.29 pts | -0.97 .. +3.55 | 0.33 |
| MYM | 5 | -0.30 pts | -1.10 .. +0.50 | 0.47 |
| MYM | 15 | +0.36 pts | -1.04 .. +1.76 | 0.99 |
| MYM | 60 | +0.41 pts | -2.75 .. +3.56 | 0.94 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | top fifth | short | 205010 | +0.002 | 0.189 | +0.03 | -3.47 | -3.48 | -3.47 | -3.48 |
| MES | 5 | h2 | bottom fifth | long | 205010 | +0.006 | 0.615 | +0.04 | -3.46 | -3.45 | -3.47 | -3.49 |
| MES | 5 | h4 | bottom fifth | long | 205010 | +0.012 | 0.615 | +0.08 | -3.42 | -3.40 | -3.43 | -3.47 |
| MES | 5 | h8 | top fifth | long | 205010 | +0.013 | 0.189 | +0.20 | -3.30 | -3.44 | -3.16 | -3.52 |
| MES | 5 | h16 | bottom fifth | long | 205010 | +0.052 | 0.615 | +0.33 | -3.17 | -3.07 | -3.26 | -3.44 |
| MES | 5 | eod | bottom fifth | long | 205010 | +1.018 | 0.615 | +4.78 | +1.28 | +1.13 | +1.41 | -2.75 |
| MES | 15 | h1 | bottom fifth | long | 66224 | +0.013 | 0.331 | +0.12 | -3.38 | -3.42 | -3.35 | -3.43 |
| MES | 15 | h2 | bottom fifth | long | 66224 | +0.023 | 0.331 | +0.24 | -3.26 | -3.32 | -3.21 | -3.36 |
| MES | 15 | h4 | bottom fifth | long | 66224 | +0.047 | 0.331 | +0.56 | -2.94 | -3.10 | -2.81 | -3.14 |
| MES | 15 | h8 | bottom fifth | long | 66224 | +0.104 | 0.331 | +1.21 | -2.29 | -2.75 | -1.90 | -2.68 |
| MES | 15 | h16 | bottom fifth | long | 66224 | +0.210 | 0.331 | +2.53 | -0.97 | -1.87 | -0.21 | -1.70 |
| MES | 15 | eod | bottom fifth | long | 66224 | +0.438 | 0.331 | +4.00 | +0.50 | +0.99 | +0.09 | -2.24 |
| MES | 60 | h1 | bottom fifth | long | 14555 | +0.020 | 0.119 | +0.71 | -2.79 | -3.31 | -2.38 | -2.94 |
| MES | 60 | h2 | bottom fifth | long | 14555 | +0.045 | 0.119 | +1.33 | -2.17 | -3.02 | -1.50 | -2.51 |
| MES | 60 | h4 | bottom fifth | long | 14555 | +0.081 | 0.119 | +2.35 | -1.15 | -2.37 | -0.20 | -1.92 |
| MES | 60 | h8 | bottom fifth | long | 14555 | +0.133 | 0.119 | +3.96 | +0.46 | -1.64 | +2.11 | -0.95 |
| MES | 60 | h16 | bottom fifth | long | 14555 | +0.195 | 0.119 | +5.70 | +2.20 | -0.37 | +4.21 | +0.16 |
| MES | 60 | eod | bottom fifth | long | 14555 | +0.217 | 0.119 | +5.83 | +2.33 | +0.20 | +4.00 | -0.04 |
| MNQ | 5 | h1 | bottom fifth | long | 204660 | +0.005 | 0.294 | +0.02 | -1.98 | -1.98 | -1.98 | -2.00 |
| MNQ | 5 | h2 | top fifth | long | 204660 | -0.001 | 0.072 | -0.04 | -2.04 | -2.00 | -2.08 | -2.03 |
| MNQ | 5 | h4 | top fifth | long | 204660 | +0.002 | 0.072 | -0.01 | -2.01 | -1.96 | -2.05 | -2.00 |
| MNQ | 5 | h8 | top fifth | long | 204660 | +0.015 | 0.072 | +0.24 | -1.76 | -1.84 | -1.67 | -1.87 |
| MNQ | 5 | h16 | top fifth | long | 204660 | +0.035 | 0.072 | +0.76 | -1.24 | -1.70 | -0.78 | -1.60 |
| MNQ | 5 | eod | bottom fifth | long | 204660 | +1.425 | 0.294 | +4.40 | +2.40 | +2.28 | +2.54 | -4.01 |
| MNQ | 15 | h1 | bottom fifth | long | 66193 | +0.016 | 0.148 | +0.17 | -1.83 | -1.90 | -1.77 | -1.93 |
| MNQ | 15 | h2 | bottom fifth | long | 66193 | +0.020 | 0.148 | +0.32 | -1.68 | -1.81 | -1.55 | -1.82 |
| MNQ | 15 | h4 | bottom fifth | long | 66193 | +0.030 | 0.148 | +0.66 | -1.34 | -1.62 | -1.07 | -1.60 |
| MNQ | 15 | h8 | bottom fifth | long | 66193 | +0.082 | 0.148 | +1.19 | -0.81 | -1.28 | -0.34 | -1.33 |
| MNQ | 15 | h16 | bottom fifth | long | 66193 | +0.191 | 0.148 | +2.76 | +0.76 | -0.58 | +2.10 | +0.00 |
| MNQ | 15 | eod | bottom fifth | long | 66193 | +0.732 | 0.148 | +7.75 | +5.75 | +3.34 | +8.17 | +1.85 |
| MNQ | 60 | h1 | bottom fifth | long | 14555 | +0.025 | 0.048 | +1.16 | -0.84 | -1.81 | +0.05 | -1.13 |
| MNQ | 60 | h2 | bottom fifth | long | 14555 | +0.042 | 0.048 | +1.79 | -0.21 | -1.75 | +1.21 | -0.81 |
| MNQ | 60 | h4 | bottom fifth | long | 14555 | +0.088 | 0.048 | +3.54 | +1.54 | -1.22 | +4.09 | +0.26 |
| MNQ | 60 | h8 | bottom fifth | long | 14555 | +0.151 | 0.048 | +5.64 | +3.64 | -0.28 | +7.25 | +1.22 |
| MNQ | 60 | h16 | bottom fifth | long | 14555 | +0.264 | 0.048 | +7.91 | +5.91 | +1.60 | +9.88 | +2.39 |
| MNQ | 60 | eod | bottom fifth | long | 14555 | +0.294 | 0.048 | +7.88 | +5.88 | +2.31 | +9.17 | +1.75 |
| MYM | 5 | h1 | bottom fifth | short | 102686 | +0.005 | 0.386 | -0.01 | -2.01 | +nan | -2.01 | -2.01 |
| MYM | 5 | h2 | bottom fifth | short | 102686 | +0.021 | 0.386 | -0.01 | -2.01 | +nan | -2.01 | -2.01 |
| MYM | 5 | h4 | bottom fifth | short | 102686 | +0.048 | 0.386 | -0.00 | -2.00 | +nan | -2.00 | -2.00 |
| MYM | 5 | h8 | bottom fifth | short | 102686 | +0.090 | 0.386 | +0.01 | -1.99 | +nan | -1.99 | -1.99 |
| MYM | 5 | h16 | bottom fifth | short | 102686 | +0.125 | 0.386 | +0.08 | -1.92 | +nan | -1.92 | -1.93 |
| MYM | 5 | eod | top fifth | long | 102686 | +0.052 | 0.098 | +2.44 | +0.44 | +nan | +0.44 | +0.15 |
| MYM | 15 | h1 | bottom fifth | long | 33176 | +0.003 | 0.190 | +0.05 | -1.95 | +nan | -1.95 | -1.96 |
| MYM | 15 | h2 | top fifth | long | 33176 | +0.003 | 0.060 | +0.34 | -1.66 | +nan | -1.66 | -1.77 |
| MYM | 15 | h4 | top fifth | long | 33176 | +0.007 | 0.060 | +0.66 | -1.34 | +nan | -1.34 | -1.57 |
| MYM | 15 | h8 | top fifth | long | 33176 | +0.013 | 0.060 | +1.23 | -0.77 | +nan | -0.77 | -1.18 |
| MYM | 15 | h16 | top fifth | long | 33176 | +0.032 | 0.060 | +2.23 | +0.23 | +nan | +0.23 | -0.37 |
| MYM | 15 | eod | top fifth | long | 33176 | +0.039 | 0.060 | +4.47 | +2.47 | +nan | +2.47 | +1.04 |
| MYM | 60 | h1 | top fifth | long | 7258 | +0.006 | 0.035 | +0.71 | -1.29 | +nan | -1.29 | -1.55 |
| MYM | 60 | h2 | top fifth | long | 7258 | +0.016 | 0.035 | +1.44 | -0.56 | +nan | -0.56 | -1.08 |
| MYM | 60 | h4 | top fifth | long | 7258 | +0.025 | 0.035 | +2.37 | +0.37 | +nan | +0.37 | -0.61 |
| MYM | 60 | h8 | top fifth | long | 7258 | +0.024 | 0.035 | +2.64 | +0.64 | +nan | +0.64 | -1.09 |
| MYM | 60 | h16 | top fifth | long | 7258 | +0.027 | 0.035 | +2.86 | +0.86 | +nan | +0.86 | -2.14 |
| MYM | 60 | eod | top fifth | long | 7258 | +0.040 | 0.035 | +2.93 | +0.93 | +nan | +0.93 | -3.05 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.122 | -0.114 | -0.051 | -0.018 | -0.006 | +0.000 | -0.002 | -0.002 | +0.000 | +0.007 | +0.006 |
| MES | 15 | -0.159 | -0.150 | -0.069 | -0.022 | -0.005 | +0.000 | -0.004 | -0.008 | -0.018 | -0.055 | -0.109 |
| MES | 60 | -0.296 | -0.294 | -0.120 | -0.039 | -0.007 | +0.000 | -0.011 | -0.021 | -0.013 | +0.048 | +0.135 |
| MNQ | 5 | -0.144 | -0.125 | -0.058 | -0.022 | -0.008 | +0.000 | +0.002 | +0.007 | +0.014 | +0.031 | +0.040 |
| MNQ | 15 | -0.143 | -0.132 | -0.055 | -0.014 | -0.001 | +0.000 | -0.005 | -0.006 | -0.008 | -0.044 | -0.115 |
| MNQ | 60 | -0.258 | -0.277 | -0.095 | -0.022 | +0.002 | +0.000 | -0.012 | -0.014 | -0.018 | -0.016 | -0.138 |
| MYM | 5 | -0.119 | -0.108 | -0.048 | -0.019 | -0.007 | +0.000 | +0.010 | +0.029 | +0.060 | +0.107 | +0.134 |
| MYM | 15 | -0.094 | -0.111 | -0.053 | -0.017 | -0.005 | +0.000 | +0.010 | +0.022 | +0.038 | +0.032 | +0.059 |
| MYM | 60 | -0.200 | -0.253 | -0.126 | -0.051 | -0.019 | +0.000 | +0.007 | +0.028 | +0.071 | +0.122 | +0.473 |

## Calibration

- MES 5-min: 1025049 bars, 205010 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 331120 bars, 66224 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 72773 bars, 14555 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1023300 bars, 204660 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 330964 bars, 66193 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 72771 bars, 14554 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 513429 bars, 102686 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 165878 bars, 33176 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 36291 bars, 7258 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
