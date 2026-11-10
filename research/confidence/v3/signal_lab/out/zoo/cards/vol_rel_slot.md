# Impact card: vol_rel_slot

volume / average volume of the same time slot over the previous 20 sessions [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect -0.016 average bars (top-minus-bottom spread ~$0.26; ~$0.13 per trade when trading both ends, at 2018-25 bar sizes) over the next 2 bars (10 min) (top fifth vs bottom fifth of the metric), not confirmed (q=0.0122, replicated in the other half=False, 13 of 16 years); best leg (bottom fifth, long) grosses $+0.09 and nets $-3.41 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 13% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.063 R20, CONFIRMED, q=2.04e-172, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.13 at recent bar sizes, 90% range up to $0.51); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: POSSIBLE direction effect -0.014 average bars (top-minus-bottom spread ~$0.40; ~$0.20 per trade when trading both ends, at 2018-25 bar sizes) over the next 1 bar (15 min) (top fifth vs bottom fifth of the metric), not confirmed (q=0.212, replicated in the other half=False, 12 of 16 years); best leg (bottom fifth, long) grosses $+0.15 and nets $-3.35 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: the market moves 15% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.076 R20, CONFIRMED, q=1.91e-105, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.20 at recent bar sizes, 90% range up to $1.14); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.018 R20 over the next 1 bar (1 h), p=0.26; we would catch an effect of 0.072 R20 or more 80% of the time).
- MES 60-min size: the market moves 18% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.092 R20, CONFIRMED, q=3.51e-44, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.54 at recent bar sizes, 90% range up to $4.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.006 R20 over the next 1 bar (5 min), p=0.21; we would catch an effect of 0.029 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 10% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.056 R20, CONFIRMED, q=1.08e-38, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.08 at recent bar sizes, 90% range up to $0.96); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.019 R20 over the next 1 bar (15 min), p=0.017; we would catch an effect of 0.050 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 13% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.068 R20, CONFIRMED, q=9.57e-20, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.75 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.044 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.007 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 16% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.083 R20, CONFIRMED, q=5.78e-38, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $4.94); about 24.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.042 R20 or more 80% of the time).
- MYM 5-min size: the market moves 10% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (+0.052 R20, CONFIRMED, q=1.83e-12, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.79); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.010 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MYM 15-min size: the market moves 13% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.071 R20, CONFIRMED, q=4.2e-11, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.71 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.093 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.031 R20 over the next 2 bars (2 h), p=0.95; we would catch an effect of 0.109 R20 or more 80% of the time).
- MYM 60-min size: the market moves 20% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (+0.107 R20, CONFIRMED, q=3.21e-33, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.71 at recent bar sizes, 90% range up to $3.22); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.007 | -0.012 .. -0.003 | -0.0042 | 0.0008 / 0.00066 / 0.00062 | 0.00104 |  |  | 12/16 | -0.006 | -0.009 |  | -3.3 / -3.4 |  |
| MES | 5 | h2 * | -0.016 | -0.024 .. -0.009 | -0.0049 | 3.7e-05 / 5.8e-05 / 3e-05 | 0.00026 | 0.0122 | 0.015 | 13/16 | -0.017 | -0.016 | False | -4.8 / -4.1 |  |
| MES | 5 | h4 | -0.027 | -0.043 .. -0.011 | -0.0045 | 0.0013 / 0.0017 / 0.00018 | 0.00026 |  |  | 12/16 | -0.036 | -0.017 |  | -5.3 / -3.2 | 0.019 |
| MES | 5 | h8 | -0.037 | -0.069 .. -0.005 | -0.0038 | 0.026 / 0.025 / 0.0068 | 0.00729 |  |  | 12/16 | -0.050 | -0.024 |  | -5.0 / -2.2 |  |
| MES | 5 | h16 | -0.049 | -0.104 .. +0.006 | -0.0037 | 0.078 / 0.084 / 0.057 | 0.0565 |  |  | 9/16 | -0.055 | -0.044 |  | -4.8 / -1.8 |  |
| MES | 5 | eod | -0.488 | -1.233 .. +0.258 | -0.0043 | 0.2 / 0.2 / 0.16 | 0.155 |  |  | 11/16 | -0.486 | -0.489 |  | -9.1 / -1.3 |  |
| MES | 15 | h1 * | -0.014 | -0.023 .. -0.006 | -0.0087 | 0.0013 / 0.00068 / 0.00046 | 0.000781 | 0.212 | 0.313 | 12/16 | -0.015 | -0.013 | False | -3.3 / -3.2 |  |
| MES | 15 | h2 | -0.019 | -0.032 .. -0.005 | -0.0069 | 0.006 / 0.0064 / 0.013 | 0.0146 |  |  | 12/16 | -0.027 | -0.010 |  | -2.7 / -2.7 |  |
| MES | 15 | h4 | -0.026 | -0.053 .. -0.000 | -0.0058 | 0.049 / 0.054 / 0.068 | 0.0662 |  |  | 10/16 | -0.028 | -0.025 |  | -2.5 / -2.0 | 0.039 |
| MES | 15 | h8 | -0.038 | -0.089 .. +0.013 | -0.0044 | 0.14 / 0.15 / 0.15 | 0.155 |  |  | 9/16 | -0.042 | -0.034 |  | -2.6 / -1.5 |  |
| MES | 15 | h16 | -0.070 | -0.182 .. +0.043 | -0.0018 | 0.23 / 0.24 / 0.19 | 0.187 |  |  | 12/16 | -0.088 | -0.051 |  | -3.4 / -1.2 |  |
| MES | 15 | eod | -0.265 | -0.863 .. +0.333 | +0.0009 | 0.38 / 0.38 / 0.25 | 0.238 |  |  | 13/16 | -0.363 | -0.169 |  | -4.7 / -0.9 |  |
| MES | 60 | h1 * | -0.018 | -0.034 .. -0.003 | -0.0070 | 0.023 / 0.028 / 0.032 | 0.03 | 1 | 0.987 | 11/16 | -0.009 | -0.028 | False | -2.2 / -2.3 |  |
| MES | 60 | h2 | -0.029 | -0.056 .. -0.002 | -0.0078 | 0.035 / 0.042 / 0.058 | 0.0526 |  |  | 11/16 | -0.026 | -0.033 |  | -2.4 / -2.1 |  |
| MES | 60 | h4 | -0.045 | -0.091 .. +0.001 | -0.0097 | 0.058 / 0.079 / 0.11 | 0.105 |  |  | 9/16 | -0.042 | -0.048 |  | -2.6 / -1.9 | 0.072 |
| MES | 60 | h8 | -0.068 | -0.150 .. +0.014 | -0.0104 | 0.1 / 0.13 / 0.17 | 0.164 |  |  | 7/16 | -0.041 | -0.096 |  | -2.9 / -1.6 |  |
| MES | 60 | h16 | -0.135 | -0.278 .. +0.009 | -0.0155 | 0.067 / 0.08 / 0.11 | 0.11 |  |  | 9/16 | -0.074 | -0.195 |  | -4.3 / -1.8 |  |
| MES | 60 | eod | -0.160 | -0.319 .. -0.000 | -0.0188 | 0.05 / 0.063 / 0.091 | 0.0899 |  |  | 9/16 | -0.114 | -0.206 |  | -4.8 / -2.0 |  |
| MNQ | 5 | h1 * | -0.006 | -0.011 .. -0.001 | -0.0027 | 0.023 / 0.034 / 0.02 | 0.0208 | 1 | 0.99 | 10/16 | -0.007 | -0.005 | False | -1.9 / -2.3 |  |
| MNQ | 5 | h2 | -0.010 | -0.025 .. +0.005 | -0.0010 | 0.18 / 0.18 / 0.049 | 0.0479 |  |  | 11/16 | -0.021 | -0.000 |  | -1.8 / -1.4 |  |
| MNQ | 5 | h4 | -0.020 | -0.055 .. +0.015 | -0.0004 | 0.26 / 0.25 / 0.042 | 0.0393 |  |  | 12/16 | -0.053 | +0.012 |  | -2.2 / -1.1 | 0.029 |
| MNQ | 5 | h8 | -0.023 | -0.086 .. +0.040 | +0.0007 | 0.48 / 0.48 / 0.22 | 0.227 |  |  | 12/16 | -0.077 | +0.030 |  | -1.7 / -0.7 |  |
| MNQ | 5 | h16 | -0.037 | -0.138 .. +0.064 | +0.0002 | 0.48 / 0.48 / 0.29 | 0.287 |  |  | 11/16 | -0.109 | +0.034 |  | -2.0 / -0.7 |  |
| MNQ | 5 | eod | -0.143 | -1.155 .. +0.869 | +0.0039 | 0.78 / 0.78 / 0.72 | 0.717 |  |  | 8/16 | -0.717 | +0.424 |  | -1.8 / -0.3 |  |
| MNQ | 15 | h1 * | -0.019 | -0.031 .. -0.006 | -0.0080 | 0.0029 / 0.0026 / 0.0003 | 0.000521 | 0.451 | 0.518 | 14/16 | -0.018 | -0.019 | False | -2.8 / -3.0 |  |
| MNQ | 15 | h2 | -0.019 | -0.036 .. -0.001 | -0.0033 | 0.039 / 0.051 / 0.065 | 0.0659 |  |  | 12/16 | -0.032 | -0.005 |  | -1.5 / -2.1 |  |
| MNQ | 15 | h4 | -0.024 | -0.064 .. +0.015 | -0.0024 | 0.23 / 0.24 / 0.25 | 0.249 |  |  | 11/16 | -0.038 | -0.010 |  | -1.1 / -1.2 | 0.050 |
| MNQ | 15 | h8 | -0.023 | -0.087 .. +0.040 | -0.0023 | 0.47 / 0.48 / 0.49 | 0.495 |  |  | 6/16 | -0.035 | -0.012 |  | -0.9 / -0.7 |  |
| MNQ | 15 | h16 | -0.025 | -0.184 .. +0.134 | +0.0054 | 0.76 / 0.76 / 0.67 | 0.685 |  |  | 9/16 | -0.099 | +0.048 |  | -0.8 / -0.3 |  |
| MNQ | 15 | eod | +0.009 | -0.807 .. +0.824 | +0.0104 | 0.98 / 0.98 / 0.98 | 0.981 |  |  | 7/16 | -0.430 | +0.443 |  | +0.1 / +0.0 |  |
| MNQ | 60 | h1 | -0.000 | -0.017 .. +0.017 | -0.0026 | 0.97 / 0.97 / 0.96 | 0.96 |  |  | 7/16 | +0.007 | -0.007 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h2 * | +0.007 | -0.023 .. +0.037 | +0.0008 | 0.65 / 0.64 / 0.66 | 0.669 | 1 | 1 | 12/16 | +0.005 | +0.009 | False | +0.6 / +0.5 |  |
| MNQ | 60 | h4 | -0.009 | -0.062 .. +0.044 | -0.0004 | 0.74 / 0.75 / 0.75 | 0.742 |  |  | 10/16 | -0.007 | -0.010 |  | -0.5 / -0.3 | 0.075 |
| MNQ | 60 | h8 | -0.026 | -0.117 .. +0.065 | -0.0004 | 0.57 / 0.58 / 0.59 | 0.578 |  |  | 10/16 | -0.011 | -0.041 |  | -1.0 / -0.6 |  |
| MNQ | 60 | h16 | -0.018 | -0.178 .. +0.141 | +0.0006 | 0.82 / 0.82 / 0.82 | 0.813 |  |  | 10/16 | -0.018 | -0.019 |  | -0.5 / -0.2 |  |
| MNQ | 60 | eod | -0.030 | -0.204 .. +0.143 | -0.0007 | 0.73 / 0.74 / 0.74 | 0.731 |  |  | 9/16 | -0.043 | -0.017 |  | -0.8 / -0.3 |  |
| MYM | 5 | h1 * | -0.007 | -0.018 .. +0.003 | -0.0011 | 0.15 / 0.19 / 0.063 | 0.0659 | 1 | 1 | 7/8 | n/a | -0.007 | False | -1.4 / -1.4 |  |
| MYM | 5 | h2 | -0.006 | -0.038 .. +0.026 | +0.0024 | 0.71 / 0.72 / 0.5 | 0.515 |  |  | 7/8 | n/a | -0.006 |  | -0.6 / -0.4 |  |
| MYM | 5 | h4 | -0.003 | -0.080 .. +0.075 | +0.0064 | 0.95 / 0.95 / 0.86 | 0.859 |  |  | 7/8 | n/a | -0.003 |  | -0.2 / -0.1 | 0.042 |
| MYM | 5 | h8 | -0.010 | -0.151 .. +0.132 | +0.0075 | 0.89 / 0.9 / 0.78 | 0.786 |  |  | 7/8 | n/a | -0.010 |  | -0.4 / -0.1 |  |
| MYM | 5 | h16 | -0.042 | -0.236 .. +0.151 | +0.0062 | 0.67 / 0.68 / 0.46 | 0.452 |  |  | 6/8 | n/a | -0.042 |  | -1.6 / -0.4 |  |
| MYM | 5 | eod | -0.377 | -1.765 .. +1.012 | +0.0036 | 0.6 / 0.6 / 0.56 | 0.554 |  |  | 6/8 | n/a | -0.377 |  | -3.6 / -0.5 |  |
| MYM | 15 | h1 * | -0.010 | -0.023 .. +0.003 | -0.0051 | 0.12 / 0.17 / 0.15 | 0.154 | 1 | 1 | 7/8 | n/a | -0.010 | False | -1.1 / -1.5 |  |
| MYM | 15 | h2 | -0.015 | -0.051 .. +0.022 | -0.0005 | 0.43 / 0.45 / 0.32 | 0.327 |  |  | 6/8 | n/a | -0.015 |  | -0.8 / -0.8 |  |
| MYM | 15 | h4 | -0.031 | -0.110 .. +0.048 | +0.0002 | 0.44 / 0.47 / 0.31 | 0.331 |  |  | 6/8 | n/a | -0.031 |  | -1.0 / -0.8 | 0.075 |
| MYM | 15 | h8 | -0.024 | -0.178 .. +0.131 | +0.0053 | 0.76 / 0.77 / 0.66 | 0.663 |  |  | 6/8 | n/a | -0.024 |  | -0.6 / -0.3 |  |
| MYM | 15 | h16 | +0.035 | -0.361 .. +0.431 | +0.0184 | 0.86 / 0.87 / 0.76 | 0.755 |  |  | 1/8 | n/a | +0.035 |  | +0.7 / +0.2 |  |
| MYM | 15 | eod | -0.042 | -1.206 .. +1.122 | +0.0179 | 0.94 / 0.94 / 0.91 | 0.919 |  |  | 6/8 | n/a | -0.042 |  | -0.3 / -0.1 |  |
| MYM | 60 | h1 | -0.016 | -0.040 .. +0.008 | -0.0132 | 0.2 / 0.19 / 0.21 | 0.208 |  |  | 6/8 | n/a | -0.016 |  | -1.3 / -1.3 |  |
| MYM | 60 | h2 * | -0.031 | -0.075 .. +0.012 | -0.0126 | 0.16 / 0.14 / 0.17 | 0.161 | 1 | 1 | 6/8 | n/a | -0.031 | False | -1.8 / -1.4 |  |
| MYM | 60 | h4 | -0.028 | -0.103 .. +0.046 | -0.0077 | 0.46 / 0.45 / 0.49 | 0.498 |  |  | 5/8 | n/a | -0.028 |  | -1.2 / -0.7 | 0.109 |
| MYM | 60 | h8 | -0.032 | -0.164 .. +0.099 | -0.0071 | 0.63 / 0.62 / 0.66 | 0.65 |  |  | 4/8 | n/a | -0.032 |  | -0.9 / -0.5 |  |
| MYM | 60 | h16 | -0.081 | -0.308 .. +0.146 | -0.0127 | 0.49 / 0.48 / 0.52 | 0.532 |  |  | 4/8 | n/a | -0.081 |  | -1.8 / -0.7 |  |
| MYM | 60 | eod | -0.115 | -0.369 .. +0.138 | -0.0156 | 0.37 / 0.36 / 0.4 | 0.404 |  |  | 4/8 | n/a | -0.115 |  | -2.4 / -0.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.063 | +0.059 .. +0.067 | +12.6% | +0.138 | 8.8e-176 | 2.04e-172 | 16/16 |
| MES | 5 | h2 | +0.076 | +0.068 .. +0.085 | +10.9% | +0.160 | 2.8e-76 |  | 16/16 |
| MES | 5 | h4 | +0.076 | +0.060 .. +0.093 | +7.6% | +0.167 | 1.9e-19 |  | 15/16 |
| MES | 5 | h8 | +0.063 | +0.030 .. +0.097 | +4.4% | +0.144 | 0.00022 |  | 14/16 |
| MES | 5 | h16 | +0.029 | -0.025 .. +0.083 | +1.4% | +0.056 | 0.3 |  | 10/16 |
| MES | 5 | eod | -0.777 | -1.410 .. -0.144 | -7.8% | -1.419 | 0.016 |  | 11/16 |
| MES | 15 | h1 * | +0.076 | +0.069 .. +0.083 | +14.9% | +0.161 | 1.3e-108 | 1.91e-105 | 16/16 |
| MES | 15 | h2 | +0.086 | +0.069 .. +0.104 | +11.8% | +0.184 | 1.9e-21 |  | 15/16 |
| MES | 15 | h4 | +0.089 | +0.051 .. +0.128 | +8.5% | +0.186 | 6.2e-06 |  | 15/16 |
| MES | 15 | h8 | +0.098 | +0.034 .. +0.163 | +6.4% | +0.156 | 0.0026 |  | 15/16 |
| MES | 15 | h16 | +0.105 | +0.000 .. +0.209 | +4.6% | +0.098 | 0.05 |  | 13/16 |
| MES | 15 | eod | -0.118 | -0.635 .. +0.399 | -2.1% | -0.200 | 0.66 |  | 7/16 |
| MES | 60 | h1 * | +0.092 | +0.079 .. +0.104 | +17.9% | +0.196 | 3.5e-47 | 3.51e-44 | 16/16 |
| MES | 60 | h2 | +0.110 | +0.091 .. +0.130 | +15.0% | +0.227 | 3.9e-28 |  | 16/16 |
| MES | 60 | h4 | +0.137 | +0.103 .. +0.171 | +13.0% | +0.264 | 3.3e-15 |  | 15/16 |
| MES | 60 | h8 | +0.149 | +0.095 .. +0.203 | +9.9% | +0.294 | 2.9e-07 |  | 15/16 |
| MES | 60 | h16 | +0.155 | +0.057 .. +0.253 | +7.5% | +0.307 | 0.0019 |  | 12/16 |
| MES | 60 | eod | +0.126 | +0.015 .. +0.236 | +5.8% | +0.295 | 0.025 |  | 12/16 |
| MNQ | 5 | h1 * | +0.056 | +0.048 .. +0.064 | +10.4% | +0.144 | 1.2e-41 | 1.08e-38 | 15/16 |
| MNQ | 5 | h2 | +0.052 | +0.030 .. +0.073 | +6.8% | +0.134 | 2.3e-06 |  | 15/16 |
| MNQ | 5 | h4 | +0.032 | -0.014 .. +0.079 | +2.9% | +0.095 | 0.17 |  | 14/16 |
| MNQ | 5 | h8 | -0.018 | -0.117 .. +0.081 | -1.1% | -0.005 | 0.73 |  | 5/16 |
| MNQ | 5 | h16 | -0.126 | -0.308 .. +0.057 | -5.2% | -0.238 | 0.18 |  | 11/16 |
| MNQ | 5 | eod | -2.046 | -3.138 .. -0.953 | -16.3% | -3.843 | 0.00024 |  | 15/16 |
| MNQ | 15 | h1 * | +0.068 | +0.054 .. +0.082 | +12.7% | +0.154 | 1.7e-22 | 9.57e-20 | 15/16 |
| MNQ | 15 | h2 | +0.067 | +0.023 .. +0.111 | +8.7% | +0.159 | 0.0028 |  | 15/16 |
| MNQ | 15 | h4 | +0.049 | -0.065 .. +0.162 | +4.3% | +0.125 | 0.4 |  | 15/16 |
| MNQ | 15 | h8 | +0.026 | -0.152 .. +0.205 | +1.6% | +0.027 | 0.77 |  | 15/16 |
| MNQ | 15 | h16 | -0.020 | -0.217 .. +0.178 | -0.8% | -0.157 | 0.85 |  | 5/16 |
| MNQ | 15 | eod | -0.589 | -1.462 .. +0.283 | -9.3% | -0.979 | 0.19 |  | 10/16 |
| MNQ | 60 | h1 * | +0.083 | +0.071 .. +0.096 | +15.8% | +0.194 | 6.5e-41 | 5.78e-38 | 16/16 |
| MNQ | 60 | h2 | +0.094 | +0.074 .. +0.115 | +12.3% | +0.223 | 5.3e-20 |  | 16/16 |
| MNQ | 60 | h4 | +0.117 | +0.082 .. +0.151 | +10.6% | +0.253 | 3.3e-11 |  | 14/16 |
| MNQ | 60 | h8 | +0.138 | +0.081 .. +0.196 | +8.7% | +0.271 | 1e-05 |  | 15/16 |
| MNQ | 60 | h16 | +0.110 | +0.005 .. +0.215 | +5.0% | +0.268 | 0.04 |  | 11/16 |
| MNQ | 60 | eod | +0.088 | -0.030 .. +0.207 | +3.8% | +0.261 | 0.14 |  | 10/16 |
| MYM | 5 | h1 * | +0.052 | +0.039 .. +0.065 | +9.8% | +0.127 | 4.4e-15 | 1.83e-12 | 8/8 |
| MYM | 5 | h2 | +0.044 | +0.010 .. +0.078 | +5.8% | +0.108 | 0.011 |  | 7/8 |
| MYM | 5 | h4 | +0.015 | -0.066 .. +0.096 | +1.4% | +0.050 | 0.72 |  | 7/8 |
| MYM | 5 | h8 | -0.033 | -0.190 .. +0.124 | -2.1% | -0.071 | 0.68 |  | 2/8 |
| MYM | 5 | h16 | -0.120 | -0.337 .. +0.097 | -5.1% | -0.307 | 0.28 |  | 3/8 |
| MYM | 5 | eod | -1.534 | -2.703 .. -0.365 | -13.1% | -3.175 | 0.01 |  | 7/8 |
| MYM | 15 | h1 * | +0.071 | +0.052 .. +0.090 | +13.4% | +0.153 | 1.1e-13 | 4.2e-11 | 7/8 |
| MYM | 15 | h2 | +0.076 | +0.020 .. +0.131 | +9.9% | +0.156 | 0.0075 |  | 7/8 |
| MYM | 15 | h4 | +0.066 | -0.062 .. +0.194 | +5.9% | +0.115 | 0.31 |  | 7/8 |
| MYM | 15 | h8 | +0.026 | -0.180 .. +0.232 | +1.6% | -0.005 | 0.8 |  | 7/8 |
| MYM | 15 | h16 | -0.031 | -0.408 .. +0.347 | -1.2% | -0.231 | 0.87 |  | 1/8 |
| MYM | 15 | eod | -0.225 | -1.261 .. +0.810 | -3.7% | -0.520 | 0.68 |  | 2/8 |
| MYM | 60 | h1 * | +0.107 | +0.091 .. +0.123 | +20.4% | +0.207 | 3.8e-36 | 3.21e-33 | 8/8 |
| MYM | 60 | h2 | +0.138 | +0.113 .. +0.164 | +18.3% | +0.255 | 2.7e-20 |  | 8/8 |
| MYM | 60 | h4 | +0.181 | +0.135 .. +0.228 | +16.8% | +0.304 | 5.9e-10 |  | 8/8 |
| MYM | 60 | h8 | +0.217 | +0.143 .. +0.292 | +14.1% | +0.350 | 2.1e-05 |  | 8/8 |
| MYM | 60 | h16 | +0.257 | +0.126 .. +0.389 | +12.2% | +0.405 | 0.0046 |  | 6/8 |
| MYM | 60 | eod | +0.242 | +0.093 .. +0.391 | +10.9% | +0.419 | 0.012 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.86 pts | -1.31 .. -0.41 | 0.00029 |
| MES | 15 | -1.19 pts | -1.96 .. -0.43 | 0.0032 |
| MES | 60 | -1.91 pts | -3.58 .. -0.24 | 0.028 |
| MNQ | 5 | -0.88 pts | -1.32 .. -0.45 | 0.00046 |
| MNQ | 15 | -1.67 pts | -2.45 .. -0.89 | 0.00013 |
| MNQ | 60 | -0.66 pts | -2.36 .. +1.03 | 0.44 |
| MYM | 5 | -0.55 pts | -1.24 .. +0.13 | 0.11 |
| MYM | 15 | -0.60 pts | -1.76 .. +0.57 | 0.42 |
| MYM | 60 | -0.32 pts | -2.92 .. +2.29 | 0.81 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 206719 | +0.004 | 0.526 | +0.03 | -3.47 | -3.49 | -3.44 | -3.47 |
| MES | 5 | h2 | bottom fifth | long | 206719 | +0.011 | 0.526 | +0.09 | -3.41 | -3.46 | -3.35 | -3.43 |
| MES | 5 | h4 | bottom fifth | long | 206719 | +0.018 | 0.526 | +0.15 | -3.35 | -3.40 | -3.28 | -3.38 |
| MES | 5 | h8 | bottom fifth | long | 206719 | +0.032 | 0.526 | +0.27 | -3.23 | -3.31 | -3.12 | -3.31 |
| MES | 5 | h16 | bottom fifth | long | 206719 | +0.060 | 0.526 | +0.47 | -3.03 | -3.18 | -2.82 | -3.23 |
| MES | 5 | eod | bottom fifth | long | 206719 | +0.863 | 0.526 | +6.25 | +2.75 | +0.27 | +6.23 | +0.39 |
| MES | 15 | h1 | bottom fifth | long | 68272 | +0.014 | 0.266 | +0.15 | -3.35 | -3.42 | -3.27 | -3.39 |
| MES | 15 | h2 | bottom fifth | long | 68272 | +0.019 | 0.266 | +0.20 | -3.30 | -3.34 | -3.24 | -3.37 |
| MES | 15 | h4 | bottom fifth | long | 68272 | +0.032 | 0.266 | +0.45 | -3.05 | -3.27 | -2.78 | -3.20 |
| MES | 15 | h8 | bottom fifth | long | 68272 | +0.055 | 0.266 | +0.76 | -2.74 | -3.05 | -2.37 | -3.04 |
| MES | 15 | h16 | bottom fifth | long | 68272 | +0.103 | 0.266 | +1.64 | -1.86 | -2.49 | -1.07 | -2.39 |
| MES | 15 | eod | bottom fifth | long | 68272 | +0.359 | 0.266 | +6.73 | +3.23 | +0.31 | +6.90 | +1.73 |
| MES | 60 | h1 | bottom fifth | long | 16647 | +0.016 | 0.114 | +0.49 | -3.01 | -3.24 | -2.75 | -3.19 |
| MES | 60 | h2 | bottom fifth | long | 16647 | +0.030 | 0.114 | +0.79 | -2.71 | -2.94 | -2.44 | -3.03 |
| MES | 60 | h4 | bottom fifth | long | 16647 | +0.058 | 0.114 | +1.49 | -2.01 | -2.47 | -1.46 | -2.75 |
| MES | 60 | h8 | bottom fifth | long | 16647 | +0.114 | 0.114 | +3.18 | -0.32 | -1.75 | +1.36 | -1.86 |
| MES | 60 | h16 | bottom fifth | long | 16647 | +0.199 | 0.114 | +6.35 | +2.85 | -0.40 | +6.63 | +0.13 |
| MES | 60 | eod | bottom fifth | long | 16647 | +0.236 | 0.114 | +7.61 | +4.11 | +0.43 | +8.40 | +0.73 |
| MNQ | 5 | h1 | bottom fifth | long | 206370 | +0.006 | 0.247 | +0.05 | -1.95 | -1.99 | -1.89 | -1.97 |
| MNQ | 5 | h2 | bottom fifth | long | 206370 | +0.011 | 0.247 | +0.10 | -1.90 | -1.97 | -1.79 | -1.93 |
| MNQ | 5 | h4 | bottom fifth | long | 206370 | +0.019 | 0.247 | +0.20 | -1.80 | -1.90 | -1.62 | -1.83 |
| MNQ | 5 | h8 | bottom fifth | long | 206370 | +0.037 | 0.247 | +0.40 | -1.60 | -1.81 | -1.24 | -1.68 |
| MNQ | 5 | h16 | bottom fifth | long | 206370 | +0.076 | 0.247 | +0.68 | -1.32 | -1.65 | -0.76 | -1.53 |
| MNQ | 5 | eod | bottom fifth | long | 206370 | +0.937 | 0.247 | +5.85 | +3.85 | +1.31 | +8.25 | +0.38 |
| MNQ | 15 | h1 | bottom fifth | long | 68241 | +0.017 | 0.119 | +0.18 | -1.82 | -1.93 | -1.65 | -1.93 |
| MNQ | 15 | h2 | bottom fifth | long | 68241 | +0.023 | 0.119 | +0.31 | -1.69 | -1.83 | -1.47 | -1.82 |
| MNQ | 15 | h4 | bottom fifth | long | 68241 | +0.039 | 0.119 | +0.70 | -1.30 | -1.74 | -0.60 | -1.54 |
| MNQ | 15 | h8 | bottom fifth | long | 68241 | +0.063 | 0.119 | +0.90 | -1.10 | -1.60 | -0.32 | -1.65 |
| MNQ | 15 | h16 | bottom fifth | long | 68241 | +0.087 | 0.119 | +1.92 | -0.08 | -1.16 | +1.62 | -0.72 |
| MNQ | 15 | eod | top fifth | long | 68241 | +0.232 | 0.063 | +8.12 | +6.12 | +0.82 | +11.90 | +5.02 |
| MNQ | 60 | h1 | bottom fifth | long | 16646 | +0.011 | 0.048 | +0.32 | -1.68 | -1.82 | -1.47 | -2.07 |
| MNQ | 60 | h2 | top fifth | long | 16646 | +0.018 | 0.032 | +1.52 | -0.48 | -1.60 | +0.72 | -0.86 |
| MNQ | 60 | h4 | bottom fifth | long | 16646 | +0.056 | 0.048 | +2.44 | +0.44 | -1.18 | +2.79 | -0.93 |
| MNQ | 60 | h8 | bottom fifth | long | 16646 | +0.112 | 0.048 | +4.22 | +2.22 | -0.39 | +6.00 | -0.42 |
| MNQ | 60 | h16 | bottom fifth | long | 16646 | +0.168 | 0.048 | +4.87 | +2.87 | +0.41 | +6.44 | -2.03 |
| MNQ | 60 | eod | bottom fifth | long | 16646 | +0.210 | 0.048 | +6.47 | +4.47 | +1.15 | +9.29 | -1.78 |
| MYM | 5 | h1 | top fifth | short | 103268 | +0.007 | 0.131 | +0.05 | -1.95 | +nan | -1.95 | -1.95 |
| MYM | 5 | h2 | top fifth | short | 103268 | +0.010 | 0.131 | +0.07 | -1.93 | +nan | -1.93 | -1.92 |
| MYM | 5 | h4 | bottom fifth | long | 103268 | -0.034 | 0.236 | +0.15 | -1.85 | +nan | -1.85 | -1.71 |
| MYM | 5 | h8 | bottom fifth | long | 103268 | -0.052 | 0.236 | +0.30 | -1.70 | +nan | -1.70 | -1.48 |
| MYM | 5 | h16 | bottom fifth | long | 103268 | -0.047 | 0.236 | +0.54 | -1.46 | +nan | -1.46 | -1.22 |
| MYM | 5 | eod | bottom fifth | long | 103268 | +0.175 | 0.236 | +4.20 | +2.20 | +nan | +2.20 | +2.47 |
| MYM | 15 | h1 | top fifth | short | 34110 | +0.008 | 0.076 | +0.08 | -1.92 | +nan | -1.92 | -1.95 |
| MYM | 15 | h2 | top fifth | short | 34110 | +0.015 | 0.076 | +0.17 | -1.83 | +nan | -1.83 | -1.87 |
| MYM | 15 | h4 | bottom fifth | long | 34110 | -0.004 | 0.119 | +0.50 | -1.50 | +nan | -1.50 | -1.29 |
| MYM | 15 | h8 | bottom fifth | long | 34110 | -0.026 | 0.119 | +0.66 | -1.34 | +nan | -1.34 | -0.96 |
| MYM | 15 | h16 | top fifth | long | 34110 | -0.021 | 0.076 | +0.94 | -1.06 | +nan | -1.06 | -0.78 |
| MYM | 15 | eod | bottom fifth | long | 34110 | -0.155 | 0.119 | +4.35 | +2.35 | +nan | +2.35 | +4.57 |
| MYM | 60 | h1 | bottom fifth | long | 8291 | +0.014 | 0.052 | +0.41 | -1.59 | +nan | -1.59 | -1.67 |
| MYM | 60 | h2 | bottom fifth | long | 8291 | +0.021 | 0.052 | +0.67 | -1.33 | +nan | -1.33 | -1.46 |
| MYM | 60 | h4 | bottom fifth | long | 8291 | +0.027 | 0.052 | +0.87 | -1.13 | +nan | -1.13 | -1.33 |
| MYM | 60 | h8 | bottom fifth | long | 8291 | +0.045 | 0.052 | +1.39 | -0.61 | +nan | -0.61 | -1.05 |
| MYM | 60 | h16 | bottom fifth | long | 8291 | +0.068 | 0.052 | +1.68 | -0.32 | +nan | -0.32 | -1.07 |
| MYM | 60 | eod | bottom fifth | long | 8291 | +0.107 | 0.052 | +2.83 | +0.83 | +nan | +0.83 | -0.46 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.024 | +0.043 | +0.044 | +0.026 | +0.010 | +0.000 | -0.007 | -0.016 | -0.027 | -0.037 | -0.045 |
| MES | 15 | +0.056 | +0.128 | +0.121 | +0.072 | +0.025 | +0.000 | -0.012 | -0.018 | -0.028 | -0.039 | -0.071 |
| MES | 60 | +0.399 | +0.322 | +0.305 | +0.224 | +0.096 | +0.000 | -0.023 | -0.035 | -0.049 | -0.068 | -0.108 |
| MNQ | 5 | +0.001 | +0.027 | +0.038 | +0.020 | +0.005 | +0.000 | -0.005 | -0.008 | -0.013 | -0.012 | -0.019 |
| MNQ | 15 | +0.031 | +0.108 | +0.115 | +0.069 | +0.024 | +0.000 | -0.011 | -0.010 | -0.017 | -0.026 | -0.027 |
| MNQ | 60 | +0.701 | +0.405 | +0.330 | +0.235 | +0.102 | +0.000 | -0.006 | -0.003 | -0.022 | -0.043 | -0.054 |
| MYM | 5 | +0.011 | +0.036 | +0.037 | +0.024 | +0.011 | +0.000 | +0.004 | +0.013 | +0.031 | +0.046 | +0.038 |
| MYM | 15 | +0.145 | +0.173 | +0.135 | +0.071 | +0.025 | +0.000 | +0.012 | +0.014 | +0.004 | +0.037 | +0.206 |
| MYM | 60 | +0.556 | +0.435 | +0.361 | +0.232 | +0.095 | +0.000 | -0.016 | -0.030 | -0.001 | +0.040 | +0.058 |

## Calibration

- MES 5-min: 1033593 bars, 206719 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341360 bars, 68272 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83231 bars, 16646 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1031845 bars, 206366 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341205 bars, 68241 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83229 bars, 16646 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 516339 bars, 103268 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170547 bars, 34110 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41455 bars, 8291 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
