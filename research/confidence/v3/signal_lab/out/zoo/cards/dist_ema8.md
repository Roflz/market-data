# Impact card: dist_ema8

(close - EMA8) in R20 (average bars) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: moves price down 0.012 average bars (top-minus-bottom spread ~$0.18; ~$0.09 per trade when trading both ends, at 2018-25 bar sizes) over the next 1 bar (5 min) (top fifth vs bottom fifth of the metric), same sign in 15 of 16 years, q=0.00151; best leg (bottom fifth, long) grosses $+0.14 and nets $-3.36 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.037 R20, CONFIRMED, q=1.01e-32, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.03, pessimistic $-0.00) does not clearly beat the $3.50 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.019 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.044 R20 or more 80% of the time).
- MES 15-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.054 R20, CONFIRMED, q=2.04e-27, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.76 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.127 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.011 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.082 R20 or more 80% of the time).
- MES 60-min size: the market moves 15% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.076 R20, CONFIRMED, q=8.07e-18, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.06 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.018 R20 over the next 4 bars (20 min), p=0.25; we would catch an effect of 0.026 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.038 R20, CONFIRMED, q=1.36e-27, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.44 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.077 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.142 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.059 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 10% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.054 R20, CONFIRMED, q=2.7e-25, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.21 at recent bar sizes, 90% range up to $1.09); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.009 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.087 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 12% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.063 R20, CONFIRMED, q=1.08e-10, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.42 at recent bar sizes, 90% range up to $4.18); about 18.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.016 R20 over the next 2 bars (10 min), p=0.31; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 5-min size: the market moves 8% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.042 R20, CONFIRMED, q=5.77e-15, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.171 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.039 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MYM 15-min size: the market moves 11% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.059 R20, CONFIRMED, q=1.9e-12, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.11 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.096 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.016 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.120 R20 or more 80% of the time).
- MYM 60-min size: the market moves 13% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.067 R20, CONFIRMED, q=2.23e-06, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.35 at recent bar sizes, 90% range up to $2.61); about 1.9x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.012 | -0.016 .. -0.007 | -0.0052 | 2.5e-06 / 6.4e-06 / 1.6e-06 | 0.00026 | 0.00151 | 0.003 | 15/16 | -0.015 | -0.008 | True | -4.7 / -4.7 |  |
| MES | 5 | h2 | -0.009 | -0.017 .. -0.001 | -0.0030 | 0.024 / 0.029 / 0.038 | 0.0357 |  |  | 12/16 | -0.019 | +0.001 |  | -2.7 / -2.3 |  |
| MES | 5 | h4 | -0.005 | -0.018 .. +0.009 | +0.0001 | 0.48 / 0.49 / 0.54 | 0.552 |  |  | 11/16 | -0.020 | +0.011 |  | -1.0 / -0.7 | 0.021 |
| MES | 5 | h8 | -0.011 | -0.035 .. +0.013 | -0.0012 | 0.37 / 0.37 / 0.41 | 0.406 |  |  | 10/16 | -0.052 | +0.029 |  | -1.6 / -0.9 |  |
| MES | 5 | h16 | -0.020 | -0.060 .. +0.020 | -0.0021 | 0.33 / 0.32 / 0.37 | 0.363 |  |  | 11/16 | -0.081 | +0.041 |  | -2.0 / -1.0 |  |
| MES | 5 | eod | -0.055 | -0.262 .. +0.153 | -0.0020 | 0.61 / 0.61 / 0.63 | 0.636 |  |  | 9/16 | -0.092 | -0.018 |  | -1.1 / -0.5 |  |
| MES | 15 | h1 | -0.003 | -0.012 .. +0.007 | -0.0018 | 0.59 / 0.58 / 0.58 | 0.571 |  |  | 9/16 | -0.013 | +0.007 |  | -0.5 / -0.5 |  |
| MES | 15 | h2 | -0.001 | -0.017 .. +0.015 | -0.0006 | 0.94 / 0.94 / 0.94 | 0.931 |  |  | 9/16 | -0.021 | +0.019 |  | -0.1 / -0.1 |  |
| MES | 15 | h4 | -0.008 | -0.037 .. +0.021 | -0.0018 | 0.57 / 0.56 / 0.59 | 0.575 |  |  | 10/16 | -0.037 | +0.020 |  | -0.9 / -0.6 | 0.044 |
| MES | 15 | h8 | -0.015 | -0.063 .. +0.034 | -0.0032 | 0.55 / 0.54 / 0.56 | 0.561 |  |  | 11/16 | -0.060 | +0.030 |  | -1.1 / -0.6 |  |
| MES | 15 | h16 * | -0.019 | -0.091 .. +0.053 | -0.0019 | 0.61 / 0.61 / 0.65 | 0.651 | 1 | 1 | 9/16 | -0.101 | +0.063 | False | -1.0 / -0.5 |  |
| MES | 15 | eod | +0.013 | -0.192 .. +0.217 | +0.0013 | 0.9 / 0.9 / 0.92 | 0.919 |  |  | 7/16 | -0.058 | +0.083 |  | +0.3 / +0.1 |  |
| MES | 60 | h1 * | +0.011 | -0.007 .. +0.028 | +0.0077 | 0.22 / 0.23 / 0.27 | 0.276 | 1 | 1 | 9/16 | -0.004 | +0.025 | False | +1.1 / +1.2 |  |
| MES | 60 | h2 | +0.007 | -0.024 .. +0.038 | +0.0060 | 0.65 / 0.65 / 0.68 | 0.681 |  |  | 7/16 | -0.009 | +0.023 |  | +0.5 / +0.5 |  |
| MES | 60 | h4 | +0.018 | -0.033 .. +0.068 | +0.0071 | 0.49 / 0.49 / 0.55 | 0.54 |  |  | 8/16 | -0.018 | +0.053 |  | +1.0 / +0.7 | 0.082 |
| MES | 60 | h8 | +0.006 | -0.076 .. +0.087 | +0.0039 | 0.89 / 0.9 / 0.9 | 0.907 |  |  | 9/16 | -0.046 | +0.057 |  | +0.2 / +0.1 |  |
| MES | 60 | h16 | -0.000 | -0.116 .. +0.116 | -0.0008 | 1 / 1 / 1 | 0.998 |  |  | 7/16 | -0.090 | +0.090 |  | -0.0 / -0.0 |  |
| MES | 60 | eod | -0.009 | -0.131 .. +0.113 | -0.0011 | 0.89 / 0.89 / 0.9 | 0.899 |  |  | 9/16 | -0.067 | +0.049 |  | -0.3 / -0.1 |  |
| MNQ | 5 | h1 | +0.003 | -0.003 .. +0.008 | +0.0035 | 0.38 / 0.38 / 0.34 | 0.334 |  |  | 9/16 | -0.003 | +0.008 |  | +0.9 / +0.9 |  |
| MNQ | 5 | h2 | +0.006 | -0.003 .. +0.015 | +0.0032 | 0.21 / 0.22 / 0.28 | 0.288 |  |  | 12/16 | -0.005 | +0.017 |  | +1.5 / +1.3 |  |
| MNQ | 5 | h4 * | +0.018 | +0.002 .. +0.033 | +0.0058 | 0.024 / 0.031 / 0.083 | 0.0831 | 1 | 0.996 | 11/16 | -0.003 | +0.038 | False | +3.2 / +2.2 | 0.026 |
| MNQ | 5 | h8 | +0.011 | -0.017 .. +0.038 | +0.0033 | 0.45 / 0.46 / 0.55 | 0.55 |  |  | 8/16 | -0.029 | +0.050 |  | +1.3 / +0.8 |  |
| MNQ | 5 | h16 | +0.006 | -0.045 .. +0.056 | +0.0013 | 0.82 / 0.82 / 0.84 | 0.832 |  |  | 7/16 | -0.049 | +0.060 |  | +0.5 / +0.2 |  |
| MNQ | 5 | eod | -0.132 | -0.416 .. +0.153 | -0.0023 | 0.36 / 0.36 / 0.41 | 0.43 |  |  | 8/16 | -0.240 | -0.025 |  | -2.0 / -0.9 |  |
| MNQ | 15 | h1 | +0.004 | -0.005 .. +0.014 | +0.0043 | 0.37 / 0.36 / 0.47 | 0.485 |  |  | 8/16 | -0.009 | +0.018 |  | +0.9 / +0.9 |  |
| MNQ | 15 | h2 | +0.010 | -0.006 .. +0.027 | +0.0041 | 0.21 / 0.22 / 0.4 | 0.403 |  |  | 10/16 | -0.010 | +0.031 |  | +1.5 / +1.2 |  |
| MNQ | 15 | h4 | +0.007 | -0.025 .. +0.039 | +0.0014 | 0.66 / 0.67 / 0.76 | 0.764 |  |  | 8/16 | -0.018 | +0.033 |  | +0.6 / +0.4 | 0.059 |
| MNQ | 15 | h8 | +0.002 | -0.052 .. +0.057 | -0.0007 | 0.93 / 0.93 / 0.95 | 0.948 |  |  | 9/16 | -0.033 | +0.037 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h16 | -0.019 | -0.098 .. +0.059 | -0.0012 | 0.63 / 0.63 / 0.72 | 0.719 |  |  | 8/16 | -0.101 | +0.062 |  | -0.9 / -0.5 |  |
| MNQ | 15 | eod * | +0.142 | -0.127 .. +0.411 | +0.0051 | 0.3 / 0.29 / 0.37 | 0.382 | 1 | 1 | 9/16 | -0.025 | +0.308 | False | +2.3 / +1.0 |  |
| MNQ | 60 | h1 * | +0.009 | -0.011 .. +0.029 | +0.0092 | 0.36 / 0.36 / 0.37 | 0.375 | 1 | 1 | 9/16 | -0.007 | +0.026 | False | +0.9 / +0.9 |  |
| MNQ | 60 | h2 | +0.011 | -0.023 .. +0.045 | +0.0087 | 0.54 / 0.54 / 0.56 | 0.569 |  |  | 9/16 | -0.014 | +0.035 |  | +0.7 / +0.6 |  |
| MNQ | 60 | h4 | +0.015 | -0.038 .. +0.069 | +0.0086 | 0.58 / 0.59 / 0.62 | 0.62 |  |  | 9/16 | -0.035 | +0.065 |  | +0.8 / +0.6 | 0.087 |
| MNQ | 60 | h8 | +0.021 | -0.062 .. +0.104 | +0.0064 | 0.62 / 0.63 / 0.66 | 0.654 |  |  | 9/16 | -0.035 | +0.077 |  | +0.8 / +0.5 |  |
| MNQ | 60 | h16 | +0.009 | -0.106 .. +0.124 | +0.0037 | 0.88 / 0.88 / 0.89 | 0.888 |  |  | 7/16 | -0.048 | +0.066 |  | +0.3 / +0.2 |  |
| MNQ | 60 | eod | -0.021 | -0.145 .. +0.103 | +0.0010 | 0.74 / 0.75 / 0.76 | 0.775 |  |  | 9/16 | -0.042 | -0.000 |  | -0.6 / -0.3 |  |
| MYM | 5 | h1 | -0.007 | -0.017 .. +0.003 | +0.0001 | 0.19 / 0.18 / 0.16 | 0.168 |  |  | 5/8 | n/a | -0.007 |  | -1.5 / -1.3 |  |
| MYM | 5 | h2 * | -0.016 | -0.029 .. -0.002 | -0.0027 | 0.025 / 0.023 / 0.085 | 0.0875 | 1 | 0.989 | 5/8 | n/a | -0.016 | False | -3.0 / -2.2 |  |
| MYM | 5 | h4 | -0.018 | -0.042 .. +0.006 | -0.0020 | 0.15 / 0.13 / 0.32 | 0.321 |  |  | 5/8 | n/a | -0.018 |  | -2.3 / -1.4 | 0.048 |
| MYM | 5 | h8 | -0.029 | -0.070 .. +0.012 | -0.0029 | 0.17 / 0.14 / 0.28 | 0.285 |  |  | 5/8 | n/a | -0.029 |  | -2.7 / -1.4 |  |
| MYM | 5 | h16 | -0.054 | -0.112 .. +0.005 | -0.0042 | 0.071 / 0.085 / 0.18 | 0.179 |  |  | 7/8 | n/a | -0.054 |  | -3.4 / -1.8 |  |
| MYM | 5 | eod | -0.068 | -0.427 .. +0.292 | -0.0014 | 0.71 / 0.72 / 0.74 | 0.749 |  |  | 4/8 | n/a | -0.068 |  | -0.8 / -0.4 |  |
| MYM | 15 | h1 | +0.002 | -0.012 .. +0.017 | +0.0026 | 0.75 / 0.74 / 0.78 | 0.783 |  |  | 5/8 | n/a | +0.002 |  | +0.3 / +0.3 |  |
| MYM | 15 | h2 | +0.005 | -0.018 .. +0.028 | +0.0013 | 0.69 / 0.68 / 0.79 | 0.801 |  |  | 4/8 | n/a | +0.005 |  | +0.5 / +0.4 |  |
| MYM | 15 | h4 | -0.002 | -0.041 .. +0.038 | -0.0016 | 0.94 / 0.94 / 0.96 | 0.954 |  |  | 5/8 | n/a | -0.002 |  | -0.1 / -0.1 | 0.078 |
| MYM | 15 | h8 | -0.029 | -0.097 .. +0.039 | -0.0036 | 0.4 / 0.43 / 0.56 | 0.571 |  |  | 5/8 | n/a | -0.029 |  | -1.4 / -0.8 |  |
| MYM | 15 | h16 * | -0.039 | -0.142 .. +0.065 | -0.0003 | 0.46 / 0.49 / 0.64 | 0.64 | 1 | 1 | 6/8 | n/a | -0.039 | False | -1.3 / -0.7 |  |
| MYM | 15 | eod | +0.053 | -0.253 .. +0.359 | +0.0032 | 0.73 / 0.75 / 0.8 | 0.811 |  |  | 4/8 | n/a | +0.053 |  | +0.7 / +0.3 |  |
| MYM | 60 | h1 * | +0.016 | -0.008 .. +0.040 | +0.0048 | 0.18 / 0.22 / 0.27 | 0.271 | 1 | 1 | 6/8 | n/a | +0.016 | False | +1.1 / +1.3 |  |
| MYM | 60 | h2 | +0.017 | -0.026 .. +0.060 | +0.0023 | 0.45 / 0.48 / 0.52 | 0.54 |  |  | 6/8 | n/a | +0.017 |  | +0.8 / +0.8 |  |
| MYM | 60 | h4 | +0.021 | -0.053 .. +0.095 | +0.0049 | 0.58 / 0.6 / 0.63 | 0.638 |  |  | 4/8 | n/a | +0.021 |  | +0.8 / +0.6 | 0.120 |
| MYM | 60 | h8 | +0.020 | -0.101 .. +0.141 | +0.0062 | 0.75 / 0.76 / 0.76 | 0.768 |  |  | 5/8 | n/a | +0.020 |  | +0.6 / +0.3 |  |
| MYM | 60 | h16 | +0.054 | -0.116 .. +0.224 | +0.0051 | 0.53 / 0.53 / 0.54 | 0.534 |  |  | 5/8 | n/a | +0.054 |  | +1.3 / +0.6 |  |
| MYM | 60 | eod | +0.032 | -0.152 .. +0.215 | +0.0032 | 0.74 / 0.73 / 0.74 | 0.729 |  |  | 5/8 | n/a | +0.032 |  | +0.7 / +0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.037 | -0.043 .. -0.031 | -7.5% | -0.072 | 1.2e-35 | 1.01e-32 | 15/16 |
| MES | 5 | h2 | -0.050 | -0.059 .. -0.042 | -7.1% | -0.099 | 1.1e-30 |  | 13/16 |
| MES | 5 | h4 | -0.062 | -0.075 .. -0.049 | -6.2% | -0.131 | 7.4e-21 |  | 13/16 |
| MES | 5 | h8 | -0.081 | -0.102 .. -0.061 | -5.7% | -0.171 | 1.5e-14 |  | 15/16 |
| MES | 5 | h16 | -0.104 | -0.134 .. -0.075 | -5.0% | -0.200 | 5.2e-12 |  | 14/16 |
| MES | 5 | eod | -0.187 | -0.323 .. -0.052 | -1.9% | -0.368 | 0.0084 |  | 12/16 |
| MES | 15 | h1 * | -0.054 | -0.064 .. -0.045 | -10.6% | -0.112 | 2.8e-30 | 2.04e-27 | 14/16 |
| MES | 15 | h2 | -0.067 | -0.081 .. -0.053 | -9.2% | -0.140 | 4.2e-20 |  | 14/16 |
| MES | 15 | h4 | -0.075 | -0.096 .. -0.054 | -7.1% | -0.161 | 4.9e-12 |  | 14/16 |
| MES | 15 | h8 | -0.084 | -0.118 .. -0.051 | -5.5% | -0.172 | 6e-07 |  | 15/16 |
| MES | 15 | h16 | -0.080 | -0.133 .. -0.026 | -3.5% | -0.167 | 0.0035 |  | 12/16 |
| MES | 15 | eod | -0.107 | -0.233 .. +0.019 | -2.0% | -0.197 | 0.12 |  | 10/16 |
| MES | 60 | h1 * | -0.076 | -0.092 .. -0.060 | -14.8% | -0.160 | 1.5e-20 | 8.07e-18 | 16/16 |
| MES | 60 | h2 | -0.093 | -0.117 .. -0.070 | -12.7% | -0.204 | 1.8e-14 |  | 16/16 |
| MES | 60 | h4 | -0.114 | -0.151 .. -0.076 | -10.7% | -0.243 | 2.6e-09 |  | 15/16 |
| MES | 60 | h8 | -0.141 | -0.197 .. -0.086 | -9.4% | -0.285 | 5.3e-07 |  | 14/16 |
| MES | 60 | h16 | -0.146 | -0.218 .. -0.074 | -7.1% | -0.304 | 7.2e-05 |  | 12/16 |
| MES | 60 | eod | -0.147 | -0.228 .. -0.067 | -6.8% | -0.315 | 0.00033 |  | 12/16 |
| MNQ | 5 | h1 * | -0.038 | -0.045 .. -0.032 | -7.1% | -0.073 | 1.9e-30 | 1.36e-27 | 15/16 |
| MNQ | 5 | h2 | -0.047 | -0.056 .. -0.038 | -6.1% | -0.098 | 2.1e-25 |  | 14/16 |
| MNQ | 5 | h4 | -0.059 | -0.073 .. -0.045 | -5.3% | -0.128 | 2e-16 |  | 14/16 |
| MNQ | 5 | h8 | -0.078 | -0.102 .. -0.054 | -4.8% | -0.168 | 3.4e-09 |  | 15/16 |
| MNQ | 5 | h16 | -0.093 | -0.129 .. -0.058 | -3.9% | -0.183 | 1.1e-05 |  | 14/16 |
| MNQ | 5 | eod | -0.201 | -0.382 .. -0.020 | -1.6% | -0.352 | 0.033 |  | 11/16 |
| MNQ | 15 | h1 * | -0.054 | -0.064 .. -0.044 | -10.1% | -0.112 | 4e-28 | 2.7e-25 | 15/16 |
| MNQ | 15 | h2 | -0.070 | -0.085 .. -0.055 | -9.1% | -0.147 | 3.1e-15 |  | 15/16 |
| MNQ | 15 | h4 | -0.079 | -0.105 .. -0.053 | -7.0% | -0.171 | 3e-05 |  | 14/16 |
| MNQ | 15 | h8 | -0.081 | -0.120 .. -0.041 | -4.8% | -0.180 | 0.00066 |  | 15/16 |
| MNQ | 15 | h16 | -0.050 | -0.107 .. +0.008 | -2.0% | -0.155 | 0.15 |  | 10/16 |
| MNQ | 15 | eod | -0.146 | -0.341 .. +0.049 | -2.3% | -0.218 | 0.18 |  | 10/16 |
| MNQ | 60 | h1 * | -0.063 | -0.080 .. -0.046 | -12.0% | -0.144 | 2.8e-13 | 1.08e-10 | 14/16 |
| MNQ | 60 | h2 | -0.066 | -0.092 .. -0.041 | -8.7% | -0.174 | 2.9e-07 |  | 14/16 |
| MNQ | 60 | h4 | -0.078 | -0.115 .. -0.040 | -7.0% | -0.197 | 5.2e-05 |  | 14/16 |
| MNQ | 60 | h8 | -0.121 | -0.174 .. -0.068 | -7.6% | -0.252 | 8.7e-06 |  | 14/16 |
| MNQ | 60 | h16 | -0.134 | -0.206 .. -0.062 | -6.1% | -0.298 | 0.00028 |  | 14/16 |
| MNQ | 60 | eod | -0.128 | -0.208 .. -0.048 | -5.6% | -0.298 | 0.0018 |  | 13/16 |
| MYM | 5 | h1 * | -0.042 | -0.051 .. -0.032 | -7.9% | -0.077 | 1.2e-17 | 5.77e-15 | 8/8 |
| MYM | 5 | h2 | -0.050 | -0.061 .. -0.038 | -6.5% | -0.101 | 7.3e-16 |  | 7/8 |
| MYM | 5 | h4 | -0.066 | -0.086 .. -0.046 | -6.0% | -0.133 | 3.6e-07 |  | 7/8 |
| MYM | 5 | h8 | -0.073 | -0.104 .. -0.042 | -4.6% | -0.152 | 4.7e-05 |  | 7/8 |
| MYM | 5 | h16 | -0.096 | -0.145 .. -0.047 | -4.1% | -0.166 | 0.00078 |  | 6/8 |
| MYM | 5 | eod | -0.255 | -0.522 .. +0.012 | -2.2% | -0.405 | 0.061 |  | 7/8 |
| MYM | 15 | h1 * | -0.059 | -0.074 .. -0.044 | -11.1% | -0.118 | 4.6e-15 | 1.9e-12 | 8/8 |
| MYM | 15 | h2 | -0.073 | -0.093 .. -0.054 | -9.6% | -0.148 | 5e-10 |  | 7/8 |
| MYM | 15 | h4 | -0.087 | -0.118 .. -0.056 | -7.8% | -0.174 | 9.7e-05 |  | 7/8 |
| MYM | 15 | h8 | -0.097 | -0.148 .. -0.047 | -5.9% | -0.192 | 0.007 |  | 7/8 |
| MYM | 15 | h16 | -0.125 | -0.208 .. -0.042 | -5.1% | -0.217 | 0.047 |  | 7/8 |
| MYM | 15 | eod | -0.160 | -0.387 .. +0.068 | -2.6% | -0.301 | 0.39 |  | 6/8 |
| MYM | 60 | h1 * | -0.067 | -0.090 .. -0.044 | -12.8% | -0.137 | 7.8e-09 | 2.23e-06 | 8/8 |
| MYM | 60 | h2 | -0.088 | -0.124 .. -0.053 | -11.7% | -0.182 | 8.6e-07 |  | 7/8 |
| MYM | 60 | h4 | -0.114 | -0.169 .. -0.058 | -10.5% | -0.218 | 5.9e-05 |  | 7/8 |
| MYM | 60 | h8 | -0.120 | -0.204 .. -0.036 | -7.7% | -0.243 | 0.0052 |  | 7/8 |
| MYM | 60 | h16 | -0.116 | -0.228 .. -0.003 | -5.4% | -0.234 | 0.045 |  | 5/8 |
| MYM | 60 | eod | -0.119 | -0.244 .. +0.007 | -5.3% | -0.253 | 0.063 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.92 pts | -1.33 .. -0.51 | 0.00026 |
| MES | 15 | -0.64 pts | -1.35 .. +0.07 | 0.11 |
| MES | 60 | +0.35 pts | -1.04 .. +1.75 | 0.64 |
| MNQ | 5 | -0.59 pts | -1.06 .. -0.12 | 0.024 |
| MNQ | 15 | -0.19 pts | -0.96 .. +0.57 | 0.75 |
| MNQ | 60 | +0.67 pts | -0.73 .. +2.06 | 0.35 |
| MYM | 5 | -0.64 pts | -1.24 .. -0.04 | 0.04 |
| MYM | 15 | -0.02 pts | -0.90 .. +0.86 | 0.99 |
| MYM | 60 | +1.61 pts | -0.22 .. +3.43 | 0.2 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207255 | +0.014 | 0.307 | +0.14 | -3.36 | -3.40 | -3.32 | -3.44 |
| MES | 5 | h2 | bottom fifth | long | 207255 | +0.016 | 0.307 | +0.15 | -3.35 | -3.37 | -3.33 | -3.48 |
| MES | 5 | h4 | bottom fifth | long | 207255 | +0.018 | 0.307 | +0.14 | -3.36 | -3.36 | -3.37 | -3.52 |
| MES | 5 | h8 | bottom fifth | long | 207255 | +0.028 | 0.307 | +0.19 | -3.31 | -3.25 | -3.37 | -3.52 |
| MES | 5 | h16 | bottom fifth | long | 207255 | +0.055 | 0.307 | +0.34 | -3.16 | -3.02 | -3.29 | -3.54 |
| MES | 5 | eod | bottom fifth | long | 207255 | +0.395 | 0.307 | +3.18 | -0.32 | -0.79 | +0.11 | -0.58 |
| MES | 15 | h1 | bottom fifth | long | 68444 | +0.010 | 0.179 | +0.10 | -3.40 | -3.40 | -3.39 | -3.57 |
| MES | 15 | h2 | bottom fifth | long | 68444 | +0.010 | 0.179 | +0.13 | -3.37 | -3.39 | -3.34 | -3.59 |
| MES | 15 | h4 | bottom fifth | long | 68444 | +0.021 | 0.179 | +0.24 | -3.26 | -3.22 | -3.31 | -3.57 |
| MES | 15 | h8 | bottom fifth | long | 68444 | +0.040 | 0.179 | +0.46 | -3.04 | -2.90 | -3.17 | -3.50 |
| MES | 15 | h16 | bottom fifth | long | 68444 | +0.070 | 0.179 | +1.18 | -2.32 | -2.29 | -2.36 | -2.81 |
| MES | 15 | eod | top fifth | long | 68444 | +0.277 | 0.190 | +3.93 | +0.43 | -0.07 | +0.91 | -1.57 |
| MES | 60 | h1 | top fifth | long | 16683 | +0.017 | 0.097 | +0.43 | -3.07 | -3.20 | -2.95 | -3.28 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.021 | 0.097 | +0.52 | -2.98 | -2.98 | -2.98 | -3.40 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.044 | 0.097 | +1.45 | -2.05 | -2.58 | -1.54 | -2.88 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.063 | 0.097 | +2.16 | -1.34 | -1.57 | -1.12 | -2.80 |
| MES | 60 | h16 | bottom fifth | long | 16683 | +0.064 | 0.089 | +2.09 | -1.41 | -0.74 | -2.06 | -3.50 |
| MES | 60 | eod | bottom fifth | long | 16683 | +0.084 | 0.089 | +3.44 | -0.06 | -0.58 | +0.44 | -2.92 |
| MNQ | 5 | h1 | top fifth | long | 206905 | +0.004 | 0.139 | +0.03 | -1.97 | -2.01 | -1.92 | -1.94 |
| MNQ | 5 | h2 | top fifth | long | 206905 | +0.009 | 0.139 | +0.08 | -1.92 | -2.00 | -1.84 | -1.89 |
| MNQ | 5 | h4 | top fifth | long | 206905 | +0.026 | 0.139 | +0.28 | -1.72 | -1.94 | -1.48 | -1.74 |
| MNQ | 5 | h8 | top fifth | long | 206905 | +0.044 | 0.139 | +0.49 | -1.51 | -1.88 | -1.10 | -1.67 |
| MNQ | 5 | h16 | top fifth | long | 206905 | +0.077 | 0.139 | +0.78 | -1.22 | -1.69 | -0.72 | -1.65 |
| MNQ | 5 | eod | bottom fifth | long | 206905 | +0.613 | 0.130 | +3.19 | +1.19 | +0.69 | +1.74 | +3.64 |
| MNQ | 15 | h1 | top fifth | long | 68413 | +0.005 | 0.079 | +0.14 | -1.86 | -1.98 | -1.73 | -1.89 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.014 | 0.079 | +0.37 | -1.63 | -1.93 | -1.32 | -1.71 |
| MNQ | 15 | h4 | top fifth | long | 68413 | +0.027 | 0.079 | +0.61 | -1.39 | -1.76 | -1.01 | -1.66 |
| MNQ | 15 | h8 | top fifth | long | 68413 | +0.057 | 0.079 | +1.09 | -0.91 | -1.38 | -0.43 | -1.64 |
| MNQ | 15 | h16 | bottom fifth | long | 68413 | +0.086 | 0.072 | +0.90 | -1.10 | -0.89 | -1.31 | -1.33 |
| MNQ | 15 | eod | top fifth | long | 68413 | +0.443 | 0.079 | +5.91 | +3.91 | +1.17 | +6.73 | +1.96 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.025 | 0.039 | +0.91 | -1.09 | -1.61 | -0.57 | -1.54 |
| MNQ | 60 | h2 | top fifth | long | 16682 | +0.037 | 0.039 | +1.38 | -0.62 | -1.38 | +0.16 | -1.41 |
| MNQ | 60 | h4 | top fifth | long | 16682 | +0.066 | 0.039 | +3.16 | +1.16 | -1.02 | +3.38 | -0.31 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.092 | 0.039 | +3.89 | +1.89 | +0.01 | +3.79 | -0.36 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.114 | 0.039 | +4.59 | +2.59 | +0.45 | +4.77 | +0.20 |
| MNQ | 60 | eod | bottom fifth | long | 16683 | +0.126 | 0.035 | +4.93 | +2.93 | +1.69 | +4.14 | -0.26 |
| MYM | 5 | h1 | bottom fifth | long | 103808 | +0.005 | 0.168 | +0.08 | -1.92 | +nan | -1.92 | -1.96 |
| MYM | 5 | h2 | bottom fifth | long | 103808 | +0.009 | 0.168 | +0.10 | -1.90 | +nan | -1.90 | -1.92 |
| MYM | 5 | h4 | bottom fifth | long | 103808 | +0.006 | 0.168 | +0.11 | -1.89 | +nan | -1.89 | -1.83 |
| MYM | 5 | h8 | bottom fifth | long | 103808 | +0.001 | 0.168 | +0.11 | -1.89 | +nan | -1.89 | -1.78 |
| MYM | 5 | h16 | bottom fifth | long | 103808 | +0.015 | 0.168 | +0.27 | -1.73 | +nan | -1.73 | -1.68 |
| MYM | 5 | eod | bottom fifth | long | 103808 | +0.202 | 0.168 | +3.28 | +1.28 | +nan | +1.28 | +1.29 |
| MYM | 15 | h1 | bottom fifth | short | 34286 | +0.002 | 0.094 | -0.04 | -2.04 | +nan | -2.04 | -1.98 |
| MYM | 15 | h2 | bottom fifth | short | 34286 | +0.009 | 0.094 | +0.00 | -2.00 | +nan | -2.00 | -2.02 |
| MYM | 15 | h4 | top fifth | short | 34286 | +0.004 | 0.098 | +0.06 | -1.94 | +nan | -1.94 | -1.87 |
| MYM | 15 | h8 | bottom fifth | long | 34286 | +0.006 | 0.094 | +0.45 | -1.55 | +nan | -1.55 | -1.32 |
| MYM | 15 | h16 | bottom fifth | long | 34286 | +0.007 | 0.094 | +1.16 | -0.84 | +nan | -0.84 | +0.01 |
| MYM | 15 | eod | top fifth | long | 34286 | +0.148 | 0.098 | +3.45 | +1.45 | +nan | +1.45 | +1.34 |
| MYM | 60 | h1 | bottom fifth | short | 8331 | +0.014 | 0.046 | +0.29 | -1.71 | +nan | -1.71 | -1.59 |
| MYM | 60 | h2 | top fifth | long | 8331 | +0.010 | 0.049 | +0.15 | -1.85 | +nan | -1.85 | -2.14 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.022 | 0.049 | +0.63 | -1.37 | +nan | -1.37 | -2.01 |
| MYM | 60 | h8 | top fifth | long | 8331 | +0.038 | 0.049 | +1.35 | -0.65 | +nan | -0.65 | -1.89 |
| MYM | 60 | h16 | top fifth | long | 8331 | +0.080 | 0.049 | +3.59 | +1.59 | +nan | +1.59 | -0.68 |
| MYM | 60 | eod | top fifth | long | 8331 | +0.078 | 0.049 | +3.57 | +1.57 | +nan | +1.57 | -1.13 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -2.922 | -3.303 | -2.746 | -1.843 | -1.098 | +0.000 | -0.057 | -0.061 | -0.057 | -0.066 | -0.078 |
| MES | 15 | -3.026 | -3.357 | -2.839 | -1.912 | -1.126 | +0.000 | -0.024 | -0.026 | -0.037 | -0.051 | -0.072 |
| MES | 60 | -3.644 | -3.580 | -3.050 | -2.043 | -1.202 | +0.000 | +0.007 | -0.001 | -0.010 | -0.096 | -0.135 |
| MNQ | 5 | -3.236 | -3.644 | -3.016 | -2.014 | -1.186 | +0.000 | -0.023 | -0.025 | -0.009 | -0.012 | -0.012 |
| MNQ | 15 | -3.240 | -3.557 | -2.989 | -2.009 | -1.182 | +0.000 | -0.003 | +0.004 | +0.003 | +0.001 | -0.044 |
| MNQ | 60 | -3.833 | -3.741 | -3.172 | -2.121 | -1.250 | +0.000 | +0.008 | +0.002 | -0.011 | -0.083 | -0.069 |
| MYM | 5 | -3.145 | -3.556 | -2.958 | -1.971 | -1.158 | +0.000 | -0.024 | -0.035 | -0.039 | -0.050 | -0.083 |
| MYM | 15 | -3.165 | -3.521 | -2.962 | -1.997 | -1.172 | +0.000 | -0.000 | +0.004 | +0.004 | -0.023 | -0.038 |
| MYM | 60 | -3.765 | -3.689 | -3.161 | -2.116 | -1.246 | +0.000 | +0.018 | +0.015 | +0.006 | -0.024 | +0.112 |

## Calibration

- MES 5-min: 1036271 bars, 207254 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68444 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
