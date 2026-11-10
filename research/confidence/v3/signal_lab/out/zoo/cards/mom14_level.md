# Impact card: mom14_level

Momentum(14) - 100 (% change over 14 bars) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (5 min), p=0.61; we would catch an effect of 0.023 R20 or more 80% of the time).
- MES 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.038 R20, CONFIRMED, q=2.25e-42, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.32 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.159 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.043 R20 or more 80% of the time).
- MES 15-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.045 R20, CONFIRMED, q=1.36e-21, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.94 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.094 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.017 R20 over the next 1 bar (1 h), p=0.14; we would catch an effect of 0.079 R20 or more 80% of the time).
- MES 60-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.048 R20, CONFIRMED, q=1.8e-08, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.59 at recent bar sizes, 90% range up to $4.58); about 3.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.311 R20 over the rest of the session (to 16:45), p=0.79; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.041 R20, CONFIRMED, q=1.49e-39, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.46 at recent bar sizes, 90% range up to $0.47); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.043 R20, CONFIRMED, q=1.57e-17, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.22 at recent bar sizes, 90% range up to $1.49); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.024 R20 over the next 1 bar (1 h), p=0.029; we would catch an effect of 0.082 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.044 R20, CONFIRMED, q=2.48e-08, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.30 at recent bar sizes, 90% range up to $7.40); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.074 R20 over the next 16 bars (80 min), p=0.52; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.039 R20, CONFIRMED, q=4.49e-14, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.58 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.118 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.043 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MYM 15-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.041 R20, CONFIRMED, q=5.08e-06, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.68 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.069 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.044 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.116 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.053 R20, CONFIRMED, q=2.28e-05, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.17 at recent bar sizes, 90% range up to $4.78); about 8739.8x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.003 | -0.007 .. +0.001 | -0.0021 | 0.098 / 0.1 / 0.14 | 0.144 | 1 | 1 | 11/16 | -0.007 | +0.000 | False | -1.5 / -1.7 |  |
| MES | 5 | h2 | -0.004 | -0.012 .. +0.003 | -0.0016 | 0.26 / 0.26 / 0.34 | 0.339 |  |  | 10/16 | -0.012 | +0.003 |  | -1.4 / -1.1 |  |
| MES | 5 | h4 | -0.003 | -0.017 .. +0.011 | -0.0011 | 0.71 / 0.71 / 0.75 | 0.746 |  |  | 10/16 | -0.014 | +0.008 |  | -0.6 / -0.4 | 0.023 |
| MES | 5 | h8 | -0.007 | -0.034 .. +0.020 | -0.0017 | 0.62 / 0.62 / 0.66 | 0.664 |  |  | 9/16 | -0.029 | +0.015 |  | -1.1 / -0.5 |  |
| MES | 5 | h16 | -0.014 | -0.062 .. +0.035 | -0.0024 | 0.57 / 0.56 / 0.6 | 0.599 |  |  | 11/16 | -0.047 | +0.019 |  | -1.5 / -0.6 |  |
| MES | 5 | eod | -0.059 | -0.266 .. +0.147 | -0.0031 | 0.57 / 0.58 / 0.65 | 0.66 |  |  | 12/16 | -0.013 | -0.105 |  | -1.7 / -0.6 |  |
| MES | 15 | h1 * | +0.004 | -0.004 .. +0.013 | -0.0004 | 0.35 / 0.33 / 0.35 | 0.337 | 1 | 1 | 11/16 | -0.001 | +0.009 | False | +1.0 / +0.9 |  |
| MES | 15 | h2 | +0.003 | -0.012 .. +0.018 | -0.0011 | 0.74 / 0.73 / 0.75 | 0.745 |  |  | 9/16 | -0.006 | +0.011 |  | +0.4 / +0.3 |  |
| MES | 15 | h4 | -0.002 | -0.030 .. +0.026 | -0.0022 | 0.9 / 0.89 / 0.9 | 0.892 |  |  | 8/16 | -0.017 | +0.013 |  | -0.2 / -0.1 | 0.043 |
| MES | 15 | h8 | -0.011 | -0.058 .. +0.037 | -0.0037 | 0.66 / 0.65 / 0.7 | 0.692 |  |  | 10/16 | -0.030 | +0.008 |  | -0.9 / -0.4 |  |
| MES | 15 | h16 | -0.007 | -0.078 .. +0.064 | -0.0022 | 0.85 / 0.85 / 0.89 | 0.887 |  |  | 8/16 | -0.049 | +0.035 |  | -0.4 / -0.2 |  |
| MES | 15 | eod | -0.006 | -0.202 .. +0.189 | -0.0016 | 0.95 / 0.95 / 0.96 | 0.96 |  |  | 9/16 | -0.041 | +0.028 |  | -0.2 / -0.1 |  |
| MES | 60 | h1 * | +0.017 | +0.003 .. +0.031 | +0.0051 | 0.017 / 0.019 / 0.042 | 0.0396 | 1 | 0.958 | 14/16 | +0.014 | +0.020 | False | +2.2 / +2.4 |  |
| MES | 60 | h2 | +0.026 | -0.000 .. +0.053 | +0.0063 | 0.053 / 0.055 / 0.096 | 0.0946 |  |  | 12/16 | +0.022 | +0.031 |  | +2.4 / +1.9 |  |
| MES | 60 | h4 | +0.041 | -0.007 .. +0.089 | +0.0090 | 0.093 / 0.093 / 0.15 | 0.156 |  |  | 11/16 | +0.033 | +0.050 |  | +2.6 / +1.7 | 0.079 |
| MES | 60 | h8 | +0.060 | -0.027 .. +0.148 | +0.0105 | 0.18 / 0.16 / 0.23 | 0.227 |  |  | 11/16 | +0.038 | +0.083 |  | +2.9 / +1.4 |  |
| MES | 60 | h16 | +0.024 | -0.125 .. +0.173 | +0.0044 | 0.75 / 0.74 / 0.77 | 0.767 |  |  | 8/16 | -0.041 | +0.089 |  | +0.8 / +0.3 |  |
| MES | 60 | eod | +0.006 | -0.157 .. +0.169 | +0.0012 | 0.94 / 0.94 / 0.94 | 0.944 |  |  | 6/16 | -0.046 | +0.058 |  | +0.2 / +0.1 |  |
| MNQ | 5 | h1 | +0.003 | -0.002 .. +0.007 | +0.0017 | 0.23 / 0.25 / 0.31 | 0.312 |  |  | 9/16 | -0.000 | +0.006 |  | +1.1 / +1.2 |  |
| MNQ | 5 | h2 | +0.002 | -0.006 .. +0.010 | +0.0008 | 0.63 / 0.63 / 0.73 | 0.733 |  |  | 9/16 | -0.002 | +0.006 |  | +0.6 / +0.5 |  |
| MNQ | 5 | h4 | +0.007 | -0.008 .. +0.021 | +0.0015 | 0.38 / 0.39 / 0.55 | 0.552 |  |  | 10/16 | -0.000 | +0.013 |  | +1.4 / +0.9 | 0.032 |
| MNQ | 5 | h8 | -0.003 | -0.032 .. +0.026 | +0.0003 | 0.85 / 0.85 / 0.89 | 0.888 |  |  | 7/16 | -0.023 | +0.017 |  | -0.4 / -0.2 |  |
| MNQ | 5 | h16 | -0.014 | -0.068 .. +0.040 | -0.0004 | 0.61 / 0.6 / 0.69 | 0.69 |  |  | 9/16 | -0.050 | +0.022 |  | -1.4 / -0.5 |  |
| MNQ | 5 | eod * | -0.311 | -0.535 .. -0.088 | -0.0059 | 0.0063 / 0.007 / 0.072 | 0.0672 | 1 | 0.76 | 13/16 | -0.322 | -0.300 | False | -7.7 / -2.7 |  |
| MNQ | 15 | h1 * | +0.007 | -0.001 .. +0.015 | +0.0030 | 0.068 / 0.069 / 0.18 | 0.179 | 1 | 1 | 12/16 | +0.003 | +0.012 | False | +1.7 / +1.8 |  |
| MNQ | 15 | h2 | +0.008 | -0.007 .. +0.023 | +0.0020 | 0.28 / 0.28 / 0.47 | 0.47 |  |  | 12/16 | +0.002 | +0.015 |  | +1.4 / +1.1 |  |
| MNQ | 15 | h4 | +0.009 | -0.022 .. +0.039 | +0.0001 | 0.57 / 0.56 / 0.7 | 0.69 |  |  | 11/16 | -0.001 | +0.019 |  | +0.9 / +0.6 | 0.050 |
| MNQ | 15 | h8 | +0.007 | -0.045 .. +0.059 | -0.0012 | 0.8 / 0.8 / 0.87 | 0.858 |  |  | 8/16 | -0.015 | +0.028 |  | +0.5 / +0.3 |  |
| MNQ | 15 | h16 | +0.018 | -0.057 .. +0.094 | -0.0011 | 0.64 / 0.66 / 0.76 | 0.752 |  |  | 9/16 | -0.039 | +0.075 |  | +1.1 / +0.5 |  |
| MNQ | 15 | eod | -0.087 | -0.292 .. +0.119 | -0.0006 | 0.41 / 0.4 / 0.61 | 0.614 |  |  | 10/16 | -0.168 | -0.006 |  | -2.3 / -0.8 |  |
| MNQ | 60 | h1 * | +0.024 | +0.010 .. +0.038 | +0.0065 | 0.00063 / 0.001 / 0.0068 | 0.00599 | 0.721 | 0.161 | 12/16 | +0.019 | +0.029 | False | +3.0 / +3.4 |  |
| MNQ | 60 | h2 | +0.038 | +0.012 .. +0.063 | +0.0093 | 0.0039 / 0.0049 / 0.023 | 0.0245 |  |  | 13/16 | +0.030 | +0.045 |  | +3.3 / +2.9 |  |
| MNQ | 60 | h4 | +0.056 | +0.010 .. +0.101 | +0.0107 | 0.017 / 0.02 / 0.062 | 0.061 |  |  | 12/16 | +0.043 | +0.068 |  | +3.5 / +2.4 | 0.082 |
| MNQ | 60 | h8 | +0.069 | -0.010 .. +0.149 | +0.0111 | 0.088 / 0.092 / 0.18 | 0.181 |  |  | 10/16 | +0.062 | +0.077 |  | +3.2 / +1.7 |  |
| MNQ | 60 | h16 | +0.039 | -0.105 .. +0.184 | +0.0009 | 0.59 / 0.59 / 0.65 | 0.651 |  |  | 8/16 | +0.036 | +0.042 |  | +1.3 / +0.5 |  |
| MNQ | 60 | eod | -0.010 | -0.166 .. +0.146 | -0.0045 | 0.9 / 0.9 / 0.92 | 0.924 |  |  | 9/16 | +0.012 | -0.032 |  | -0.3 / -0.1 |  |
| MYM | 5 | h1 | -0.001 | -0.009 .. +0.008 | +0.0011 | 0.89 / 0.89 / 0.93 | 0.932 |  |  | 5/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 5 | h2 | -0.009 | -0.020 .. +0.002 | -0.0023 | 0.12 / 0.12 / 0.35 | 0.361 |  |  | 6/8 | n/a | -0.009 |  | -1.9 / -1.5 |  |
| MYM | 5 | h4 | -0.022 | -0.043 .. -0.002 | -0.0034 | 0.033 / 0.034 / 0.24 | 0.23 |  |  | 5/8 | n/a | -0.022 |  | -3.2 / -2.1 | 0.048 |
| MYM | 5 | h8 | -0.038 | -0.074 .. -0.002 | -0.0049 | 0.039 / 0.047 / 0.2 | 0.197 |  |  | 7/8 | n/a | -0.038 |  | -4.0 / -2.1 |  |
| MYM | 5 | h16 * | -0.074 | -0.139 .. -0.009 | -0.0075 | 0.026 / 0.038 / 0.12 | 0.116 | 1 | 0.992 | 7/8 | n/a | -0.074 | False | -5.4 / -2.2 |  |
| MYM | 5 | eod | -0.157 | -0.459 .. +0.146 | -0.0039 | 0.31 / 0.33 / 0.5 | 0.497 |  |  | 6/8 | n/a | -0.157 |  | -3.0 / -1.0 |  |
| MYM | 15 | h1 | -0.002 | -0.013 .. +0.009 | +0.0005 | 0.72 / 0.74 / 0.79 | 0.793 |  |  | 4/8 | n/a | -0.002 |  | -0.3 / -0.4 |  |
| MYM | 15 | h2 | -0.005 | -0.023 .. +0.013 | -0.0016 | 0.59 / 0.62 / 0.76 | 0.76 |  |  | 4/8 | n/a | -0.005 |  | -0.6 / -0.5 |  |
| MYM | 15 | h4 | -0.013 | -0.050 .. +0.024 | -0.0026 | 0.49 / 0.52 / 0.67 | 0.676 |  |  | 5/8 | n/a | -0.013 |  | -1.0 / -0.7 | 0.076 |
| MYM | 15 | h8 * | -0.043 | -0.111 .. +0.024 | -0.0048 | 0.21 / 0.23 / 0.42 | 0.403 | 1 | 1 | 7/8 | n/a | -0.043 | False | -2.5 / -1.3 |  |
| MYM | 15 | h16 | -0.019 | -0.126 .. +0.088 | -0.0037 | 0.73 / 0.74 / 0.83 | 0.808 |  |  | 5/8 | n/a | -0.019 |  | -0.8 / -0.3 |  |
| MYM | 15 | eod | +0.023 | -0.261 .. +0.308 | +0.0000 | 0.87 / 0.87 / 0.92 | 0.923 |  |  | 4/8 | n/a | +0.023 |  | +0.5 / +0.2 |  |
| MYM | 60 | h1 | +0.011 | -0.010 .. +0.031 | +0.0052 | 0.31 / 0.34 / 0.4 | 0.391 |  |  | 5/8 | n/a | +0.011 |  | +0.9 / +1.0 |  |
| MYM | 60 | h2 | +0.017 | -0.021 .. +0.055 | +0.0061 | 0.37 / 0.39 / 0.47 | 0.469 |  |  | 6/8 | n/a | +0.017 |  | +1.1 / +0.9 |  |
| MYM | 60 | h4 * | +0.044 | -0.026 .. +0.114 | +0.0101 | 0.22 / 0.23 / 0.31 | 0.314 | 1 | 1 | 6/8 | n/a | +0.044 | False | +2.0 / +1.2 | 0.116 |
| MYM | 60 | h8 | +0.074 | -0.053 .. +0.201 | +0.0109 | 0.25 / 0.24 / 0.32 | 0.326 |  |  | 6/8 | n/a | +0.074 |  | +2.4 / +1.1 |  |
| MYM | 60 | h16 | +0.055 | -0.161 .. +0.270 | +0.0044 | 0.62 / 0.61 / 0.64 | 0.63 |  |  | 5/8 | n/a | +0.055 |  | +1.3 / +0.5 |  |
| MYM | 60 | eod | +0.073 | -0.165 .. +0.310 | +0.0038 | 0.55 / 0.54 / 0.57 | 0.568 |  |  | 4/8 | n/a | +0.073 |  | +1.6 / +0.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.038 | -0.044 .. -0.033 | -7.7% | -0.076 | 2.3e-45 | 2.25e-42 | 16/16 |
| MES | 5 | h2 | -0.048 | -0.056 .. -0.040 | -6.9% | -0.102 | 1.5e-32 |  | 15/16 |
| MES | 5 | h4 | -0.060 | -0.073 .. -0.047 | -6.0% | -0.132 | 1.3e-19 |  | 13/16 |
| MES | 5 | h8 | -0.079 | -0.100 .. -0.058 | -5.5% | -0.169 | 1.3e-13 |  | 15/16 |
| MES | 5 | h16 | -0.114 | -0.146 .. -0.083 | -5.4% | -0.217 | 1.7e-11 |  | 15/16 |
| MES | 5 | eod | -0.263 | -0.411 .. -0.115 | -2.6% | -0.496 | 0.0033 |  | 11/16 |
| MES | 15 | h1 * | -0.045 | -0.054 .. -0.036 | -8.8% | -0.098 | 2.1e-24 | 1.36e-21 | 15/16 |
| MES | 15 | h2 | -0.055 | -0.068 .. -0.042 | -7.5% | -0.122 | 4.6e-16 |  | 14/16 |
| MES | 15 | h4 | -0.068 | -0.088 .. -0.048 | -6.4% | -0.143 | 2.7e-08 |  | 15/16 |
| MES | 15 | h8 | -0.077 | -0.110 .. -0.045 | -5.0% | -0.151 | 0.00016 |  | 13/16 |
| MES | 15 | h16 | -0.061 | -0.118 .. -0.003 | -2.6% | -0.110 | 0.05 |  | 9/16 |
| MES | 15 | eod | -0.084 | -0.212 .. +0.043 | -1.5% | -0.190 | 0.3 |  | 9/16 |
| MES | 60 | h1 * | -0.048 | -0.062 .. -0.034 | -9.4% | -0.120 | 5.4e-11 | 1.8e-08 | 14/16 |
| MES | 60 | h2 | -0.063 | -0.084 .. -0.042 | -8.6% | -0.154 | 3e-09 |  | 15/16 |
| MES | 60 | h4 | -0.088 | -0.122 .. -0.055 | -8.3% | -0.191 | 2.9e-07 |  | 14/16 |
| MES | 60 | h8 | -0.117 | -0.166 .. -0.068 | -7.8% | -0.244 | 1.3e-05 |  | 14/16 |
| MES | 60 | h16 | -0.133 | -0.224 .. -0.042 | -6.5% | -0.305 | 0.0043 |  | 14/16 |
| MES | 60 | eod | -0.140 | -0.248 .. -0.033 | -6.5% | -0.322 | 0.014 |  | 13/16 |
| MNQ | 5 | h1 * | -0.041 | -0.047 .. -0.035 | -7.7% | -0.079 | 1.6e-42 | 1.49e-39 | 15/16 |
| MNQ | 5 | h2 | -0.050 | -0.058 .. -0.041 | -6.5% | -0.105 | 9.4e-26 |  | 15/16 |
| MNQ | 5 | h4 | -0.061 | -0.075 .. -0.048 | -5.5% | -0.134 | 8e-13 |  | 15/16 |
| MNQ | 5 | h8 | -0.079 | -0.102 .. -0.057 | -4.9% | -0.166 | 1.4e-06 |  | 14/16 |
| MNQ | 5 | h16 | -0.104 | -0.139 .. -0.068 | -4.3% | -0.189 | 0.00014 |  | 14/16 |
| MNQ | 5 | eod | -0.201 | -0.356 .. -0.046 | -1.6% | -0.426 | 0.037 |  | 12/16 |
| MNQ | 15 | h1 * | -0.043 | -0.051 .. -0.035 | -8.1% | -0.092 | 2.9e-20 | 1.57e-17 | 15/16 |
| MNQ | 15 | h2 | -0.052 | -0.065 .. -0.039 | -6.7% | -0.115 | 1.4e-06 |  | 14/16 |
| MNQ | 15 | h4 | -0.054 | -0.077 .. -0.032 | -4.8% | -0.131 | 0.024 |  | 14/16 |
| MNQ | 15 | h8 | -0.050 | -0.085 .. -0.015 | -3.0% | -0.137 | 0.14 |  | 12/16 |
| MNQ | 15 | h16 | -0.020 | -0.079 .. +0.039 | -0.8% | -0.082 | 0.6 |  | 10/16 |
| MNQ | 15 | eod | -0.065 | -0.204 .. +0.074 | -1.0% | -0.146 | 0.56 |  | 12/16 |
| MNQ | 60 | h1 * | -0.044 | -0.057 .. -0.031 | -8.3% | -0.112 | 7.6e-11 | 2.48e-08 | 13/16 |
| MNQ | 60 | h2 | -0.057 | -0.078 .. -0.037 | -7.5% | -0.146 | 6.1e-08 |  | 14/16 |
| MNQ | 60 | h4 | -0.078 | -0.112 .. -0.045 | -7.1% | -0.180 | 5.6e-06 |  | 13/16 |
| MNQ | 60 | h8 | -0.117 | -0.169 .. -0.066 | -7.4% | -0.244 | 7.9e-06 |  | 13/16 |
| MNQ | 60 | h16 | -0.158 | -0.248 .. -0.068 | -7.2% | -0.356 | 0.0012 |  | 13/16 |
| MNQ | 60 | eod | -0.147 | -0.252 .. -0.041 | -6.4% | -0.367 | 0.009 |  | 11/16 |
| MYM | 5 | h1 * | -0.039 | -0.048 .. -0.030 | -7.3% | -0.076 | 1e-16 | 4.49e-14 | 8/8 |
| MYM | 5 | h2 | -0.041 | -0.052 .. -0.031 | -5.4% | -0.095 | 1.4e-06 |  | 7/8 |
| MYM | 5 | h4 | -0.049 | -0.067 .. -0.030 | -4.5% | -0.109 | 0.0063 |  | 7/8 |
| MYM | 5 | h8 | -0.056 | -0.087 .. -0.026 | -3.5% | -0.123 | 0.032 |  | 6/8 |
| MYM | 5 | h16 | -0.084 | -0.132 .. -0.036 | -3.6% | -0.131 | 0.042 |  | 6/8 |
| MYM | 5 | eod | -0.327 | -0.550 .. -0.104 | -2.8% | -0.583 | 0.013 |  | 7/8 |
| MYM | 15 | h1 * | -0.041 | -0.055 .. -0.027 | -7.7% | -0.097 | 1.8e-08 | 5.08e-06 | 8/8 |
| MYM | 15 | h2 | -0.054 | -0.073 .. -0.035 | -7.0% | -0.120 | 0.0005 |  | 7/8 |
| MYM | 15 | h4 | -0.071 | -0.101 .. -0.041 | -6.4% | -0.147 | 0.027 |  | 7/8 |
| MYM | 15 | h8 | -0.097 | -0.149 .. -0.044 | -5.9% | -0.179 | 0.11 |  | 7/8 |
| MYM | 15 | h16 | -0.109 | -0.198 .. -0.019 | -4.4% | -0.220 | 0.2 |  | 6/8 |
| MYM | 15 | eod | -0.136 | -0.339 .. +0.068 | -2.3% | -0.429 | 0.55 |  | 5/8 |
| MYM | 60 | h1 * | -0.053 | -0.072 .. -0.033 | -10.1% | -0.115 | 8.5e-08 | 2.28e-05 | 8/8 |
| MYM | 60 | h2 | -0.063 | -0.092 .. -0.033 | -8.3% | -0.147 | 2.9e-05 |  | 8/8 |
| MYM | 60 | h4 | -0.083 | -0.130 .. -0.036 | -7.7% | -0.183 | 0.00059 |  | 8/8 |
| MYM | 60 | h8 | -0.111 | -0.189 .. -0.032 | -7.2% | -0.215 | 0.0056 |  | 6/8 |
| MYM | 60 | h16 | -0.142 | -0.282 .. -0.002 | -6.7% | -0.260 | 0.053 |  | 5/8 |
| MYM | 60 | eod | -0.177 | -0.338 .. -0.016 | -8.0% | -0.299 | 0.046 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.41 pts | -0.90 .. +0.08 | 0.1 |
| MES | 15 | +0.63 pts | -0.22 .. +1.47 | 0.15 |
| MES | 60 | +1.71 pts | -0.11 .. +3.53 | 0.088 |
| MNQ | 5 | -0.07 pts | -0.57 .. +0.42 | 0.78 |
| MNQ | 15 | +0.59 pts | -0.27 .. +1.46 | 0.18 |
| MNQ | 60 | +2.04 pts | +0.28 .. +3.80 | 0.026 |
| MYM | 5 | -0.14 pts | -0.76 .. +0.48 | 0.68 |
| MYM | 15 | -0.09 pts | -1.16 .. +0.98 | 0.92 |
| MYM | 60 | +1.36 pts | -1.01 .. +3.73 | 0.33 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207256 | +0.005 | 0.222 | +0.05 | -3.45 | -3.46 | -3.43 | -3.48 |
| MES | 5 | h2 | bottom fifth | long | 207256 | +0.007 | 0.222 | +0.06 | -3.44 | -3.44 | -3.43 | -3.48 |
| MES | 5 | h4 | bottom fifth | long | 207256 | +0.007 | 0.222 | +0.06 | -3.44 | -3.47 | -3.42 | -3.49 |
| MES | 5 | h8 | bottom fifth | long | 207256 | +0.014 | 0.222 | +0.16 | -3.34 | -3.40 | -3.28 | -3.44 |
| MES | 5 | h16 | bottom fifth | long | 207256 | +0.034 | 0.222 | +0.41 | -3.09 | -3.19 | -2.99 | -3.34 |
| MES | 5 | eod | bottom fifth | long | 207256 | +0.210 | 0.222 | +4.21 | +0.71 | -1.36 | +2.53 | +3.93 |
| MES | 15 | h1 | top fifth | long | 68444 | +0.003 | 0.137 | +0.08 | -3.42 | -3.45 | -3.40 | -3.39 |
| MES | 15 | h2 | top fifth | long | 68444 | +0.005 | 0.137 | +0.11 | -3.39 | -3.38 | -3.40 | -3.40 |
| MES | 15 | h4 | bottom fifth | long | 68444 | +0.019 | 0.131 | +0.47 | -3.03 | -3.20 | -2.88 | -3.18 |
| MES | 15 | h8 | bottom fifth | long | 68444 | +0.040 | 0.131 | +1.08 | -2.42 | -2.80 | -2.09 | -2.54 |
| MES | 15 | h16 | bottom fifth | long | 68444 | +0.062 | 0.131 | +2.04 | -1.46 | -2.40 | -0.65 | -1.15 |
| MES | 15 | eod | bottom fifth | long | 68444 | +0.113 | 0.131 | +5.07 | +1.57 | -1.03 | +3.81 | +5.03 |
| MES | 60 | h1 | top fifth | long | 16683 | +0.020 | 0.074 | +0.69 | -2.81 | -3.02 | -2.64 | -2.87 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.033 | 0.074 | +1.18 | -2.32 | -2.52 | -2.17 | -2.54 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.055 | 0.074 | +2.25 | -1.25 | -1.75 | -0.84 | -1.80 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.097 | 0.074 | +4.63 | +1.13 | +0.04 | +2.01 | -0.03 |
| MES | 60 | h16 | top fifth | long | 16683 | +0.125 | 0.074 | +5.82 | +2.32 | +0.72 | +3.61 | +0.23 |
| MES | 60 | eod | top fifth | long | 16683 | +0.126 | 0.074 | +5.34 | +1.84 | +0.91 | +2.59 | -0.75 |
| MNQ | 5 | h1 | top fifth | long | 206905 | +0.003 | 0.089 | +0.08 | -1.92 | -1.96 | -1.90 | -1.92 |
| MNQ | 5 | h2 | top fifth | long | 206905 | +0.005 | 0.089 | +0.14 | -1.86 | -1.93 | -1.81 | -1.84 |
| MNQ | 5 | h4 | top fifth | long | 206905 | +0.013 | 0.089 | +0.36 | -1.64 | -1.85 | -1.47 | -1.64 |
| MNQ | 5 | h8 | bottom fifth | long | 206905 | +0.014 | 0.085 | +0.25 | -1.75 | -2.01 | -1.55 | -1.55 |
| MNQ | 5 | h16 | bottom fifth | long | 206905 | +0.038 | 0.085 | +0.44 | -1.56 | -1.81 | -1.36 | -1.41 |
| MNQ | 5 | eod | bottom fifth | long | 206905 | +0.268 | 0.085 | +5.40 | +3.40 | +0.40 | +5.71 | +14.07 |
| MNQ | 15 | h1 | top fifth | long | 68413 | +0.006 | 0.052 | +0.09 | -1.91 | -1.90 | -1.91 | -1.94 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.013 | 0.052 | +0.21 | -1.79 | -1.78 | -1.79 | -1.83 |
| MNQ | 15 | h4 | top fifth | long | 68413 | +0.026 | 0.052 | +0.66 | -1.34 | -1.57 | -1.18 | -1.52 |
| MNQ | 15 | h8 | top fifth | long | 68413 | +0.048 | 0.052 | +1.28 | -0.72 | -1.28 | -0.30 | -1.34 |
| MNQ | 15 | h16 | top fifth | long | 68413 | +0.105 | 0.052 | +3.45 | +1.45 | -0.72 | +3.04 | +0.63 |
| MNQ | 15 | eod | bottom fifth | long | 68413 | +0.148 | 0.050 | +5.61 | +3.61 | +1.49 | +5.21 | +10.57 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.028 | 0.029 | +1.16 | -0.84 | -1.46 | -0.42 | -1.11 |
| MNQ | 60 | h2 | top fifth | long | 16682 | +0.046 | 0.029 | +2.23 | +0.23 | -1.07 | +1.13 | -0.25 |
| MNQ | 60 | h4 | top fifth | long | 16682 | +0.076 | 0.029 | +4.18 | +2.18 | -0.40 | +3.97 | +1.24 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.111 | 0.029 | +5.54 | +3.54 | +0.90 | +5.38 | +2.17 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.141 | 0.029 | +4.74 | +2.74 | +1.25 | +3.77 | +1.02 |
| MNQ | 60 | eod | bottom fifth | long | 16683 | +0.143 | 0.027 | +12.85 | +10.85 | +2.47 | +16.95 | +7.28 |
| MYM | 5 | h1 | bottom fifth | long | 103808 | -0.002 | 0.116 | +0.03 | -1.97 | +nan | -1.97 | -1.97 |
| MYM | 5 | h2 | bottom fifth | long | 103808 | +0.000 | 0.116 | +0.04 | -1.96 | +nan | -1.96 | -1.90 |
| MYM | 5 | h4 | bottom fifth | long | 103808 | -0.000 | 0.116 | +0.06 | -1.94 | +nan | -1.94 | -1.71 |
| MYM | 5 | h8 | bottom fifth | long | 103808 | -0.003 | 0.116 | +0.04 | -1.96 | +nan | -1.96 | -1.57 |
| MYM | 5 | h16 | bottom fifth | long | 103808 | +0.009 | 0.116 | +0.37 | -1.63 | +nan | -1.63 | -1.24 |
| MYM | 5 | eod | bottom fifth | long | 103808 | +0.173 | 0.116 | +5.43 | +3.43 | +nan | +3.43 | +6.03 |
| MYM | 15 | h1 | bottom fifth | long | 34286 | -0.002 | 0.068 | +0.17 | -1.83 | +nan | -1.83 | -1.80 |
| MYM | 15 | h2 | bottom fifth | long | 34286 | -0.001 | 0.068 | +0.37 | -1.63 | +nan | -1.63 | -1.48 |
| MYM | 15 | h4 | bottom fifth | long | 34286 | +0.009 | 0.068 | +0.69 | -1.31 | +nan | -1.31 | -1.01 |
| MYM | 15 | h8 | bottom fifth | long | 34286 | +0.021 | 0.068 | +1.43 | -0.57 | +nan | -0.57 | +0.19 |
| MYM | 15 | h16 | bottom fifth | long | 34286 | +0.029 | 0.068 | +2.59 | +0.59 | +nan | +0.59 | +2.25 |
| MYM | 15 | eod | top fifth | long | 34286 | +0.238 | 0.071 | +8.45 | +6.45 | +nan | +6.45 | +7.87 |
| MYM | 60 | h1 | top fifth | long | 8331 | +0.008 | 0.039 | +0.29 | -1.71 | +nan | -1.71 | -1.82 |
| MYM | 60 | h2 | top fifth | long | 8331 | +0.018 | 0.039 | +0.77 | -1.23 | +nan | -1.23 | -1.51 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.048 | 0.039 | +2.47 | +0.47 | +nan | +0.47 | -0.18 |
| MYM | 60 | h8 | top fifth | long | 8331 | +0.091 | 0.039 | +4.95 | +2.95 | +nan | +2.95 | +1.75 |
| MYM | 60 | h16 | top fifth | long | 8331 | +0.152 | 0.039 | +6.15 | +4.15 | +nan | +4.15 | +1.72 |
| MYM | 60 | eod | top fifth | long | 8331 | +0.179 | 0.039 | +6.69 | +4.69 | +nan | +4.69 | +1.52 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -3.096 | -2.072 | -1.189 | -0.678 | -0.373 | +0.000 | -0.013 | -0.017 | -0.020 | -0.027 | -0.042 |
| MES | 15 | -3.145 | -2.142 | -1.260 | -0.722 | -0.396 | +0.000 | -0.003 | -0.007 | -0.012 | -0.028 | -0.054 |
| MES | 60 | -4.419 | -2.967 | -1.583 | -0.863 | -0.464 | +0.000 | +0.014 | +0.019 | +0.021 | +0.010 | -0.065 |
| MNQ | 5 | -3.238 | -2.166 | -1.247 | -0.713 | -0.391 | +0.000 | -0.001 | -0.005 | -0.001 | -0.009 | -0.016 |
| MNQ | 15 | -3.239 | -2.202 | -1.306 | -0.757 | -0.417 | +0.000 | +0.005 | +0.005 | +0.007 | +0.003 | -0.012 |
| MNQ | 60 | -4.712 | -3.231 | -1.708 | -0.921 | -0.488 | +0.000 | +0.021 | +0.032 | +0.044 | +0.019 | +0.016 |
| MYM | 5 | -3.203 | -2.140 | -1.236 | -0.705 | -0.386 | +0.000 | -0.006 | -0.016 | -0.030 | -0.041 | -0.079 |
| MYM | 15 | -3.217 | -2.212 | -1.314 | -0.758 | -0.417 | +0.000 | -0.001 | -0.002 | -0.002 | -0.034 | -0.006 |
| MYM | 60 | -4.538 | -3.109 | -1.663 | -0.914 | -0.485 | +0.000 | +0.008 | +0.009 | +0.036 | +0.052 | -0.010 |

## Calibration

- MES 5-min: 1036271 bars, 207252 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68444 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
