# Impact card: tod_close_15_1645

bar closes in the close_15_1645 block (ET) vs all other bars [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.373 R20 over the rest of the session (to 16:45), p=0.51; we would catch an effect of 0.027 R20 or more 80% of the time).
- MES 5-min size: the market moves 80% LESS after the event than after matched bars over the rest of the session (to 16:45) (-7.937 R20, CONFIRMED, q=2.17e-284, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $8.53 at recent bar sizes, 90% range up to $1.16); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (15 min), p=0.043; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 15-min size: the market moves 44% LESS after the event than after matched bars over the next 16 bars (4 h) (-1.010 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.53 at recent bar sizes, 90% range up to $2.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.024 R20 over the next 1 bar (1 h), p=0.05; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 60-min size: the market moves 46% LESS after the event than after matched bars over the next 2 bars (2 h) (-0.342 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $1.34 at recent bar sizes, 90% range up to $3.04); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.619 R20 over the rest of the session (to 16:45), p=0.15; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 81% LESS after the event than after matched bars over the rest of the session (to 16:45) (-10.136 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $22.31 at recent bar sizes, 90% range up to $2.29); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (15 min), p=0.039; we would catch an effect of 0.042 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 42% LESS after the event than after matched bars over the next 16 bars (4 h) (-1.052 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.88 at recent bar sizes, 90% range up to $3.89); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: POSSIBLE direction effect +0.035 average bars (~$3.34 per micro at 2018-25 bar sizes) over the next 1 bar (1 h) (after the event vs matched non-events), not confirmed (q=0.249, replicated in the other half=False, 11 of 16 years); best leg (event, long) grosses $+1.61 and nets $-0.39 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 60-min size: the market moves 58% LESS after the event than after matched bars over the next 4 bars (4 h) (-0.642 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.19 at recent bar sizes, 90% range up to $4.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 5-min size: the market moves 79% LESS after the event than after matched bars over the rest of the session (to 16:45) (-9.240 R20, CONFIRMED, q=6.97e-129, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.08 at recent bar sizes, 90% range up to $1.00); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.051 R20 over the next 4 bars (1 h), p=0.069; we would catch an effect of 0.055 R20 or more 80% of the time).
- MYM 15-min size: the market moves 45% LESS after the event than after matched bars over the next 16 bars (4 h) (-1.120 R20, CONFIRMED, q=3.17e-118, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.49 at recent bar sizes, 90% range up to $2.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: POSSIBLE direction effect +0.044 average bars (~$1.96 per micro at 2018-25 bar sizes) over the next 1 bar (1 h) (after the event vs matched non-events), not confirmed (q=0.151, replicated in the other half=False, 6 of 8 years); best leg (event, long) grosses $+1.63 and nets $-0.37 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 60-min size: the market moves 52% LESS after the event than after matched bars over the next 2 bars (2 h) (-0.393 R20, CONFIRMED, q=0, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.87 at recent bar sizes, 90% range up to $2.79); about 54.0x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.004 | -0.001 .. +0.009 | +0.0016 | 0.078 / 0.092 / 0.54 | nan |  |  | 10/16 | +0.004 | +0.005 |  | +1.7 / +1.8 |  |
| MES | 5 | h2 | +0.008 | -0.002 .. +0.017 | +0.0019 | 0.12 / 0.14 / 0.72 | nan |  |  | 10/16 | +0.007 | +0.008 |  | +2.1 / +1.5 |  |
| MES | 5 | h4 | +0.013 | -0.006 .. +0.032 | +0.0021 | 0.19 / 0.21 / 0.84 | nan |  |  | 11/16 | +0.012 | +0.014 |  | +2.5 / +1.3 | 0.027 |
| MES | 5 | h8 | +0.018 | -0.017 .. +0.054 | +0.0021 | 0.31 / 0.34 / 0.98 | nan |  |  | 11/16 | +0.009 | +0.027 |  | +2.6 / +1.0 |  |
| MES | 5 | h16 | +0.025 | -0.025 .. +0.074 | +0.0020 | 0.33 / 0.36 / 0.87 | nan |  |  | 9/16 | -0.013 | +0.062 |  | +2.9 / +1.0 |  |
| MES | 5 | eod * | -0.373 | -0.793 .. +0.047 | -0.0059 | 0.082 / 0.085 / 0.47 | nan | 1 | 1 | 10/16 | -0.604 | -0.143 | False | -19.8 / -1.7 |  |
| MES | 15 | h1 * | +0.014 | +0.004 .. +0.023 | +0.0042 | 0.0054 / 0.0071 / 0.71 | nan | 0.992 | 0.743 | 10/16 | +0.015 | +0.012 | False | +2.7 / +2.8 |  |
| MES | 15 | h2 | +0.019 | +0.002 .. +0.037 | +0.0040 | 0.03 / 0.04 / 0.86 | nan |  |  | 11/16 | +0.018 | +0.021 |  | +2.8 / +2.2 |  |
| MES | 15 | h4 | +0.029 | +0.002 .. +0.056 | +0.0041 | 0.034 / 0.047 / 0.95 | nan |  |  | 11/16 | +0.012 | +0.046 |  | +3.3 / +2.1 | 0.038 |
| MES | 15 | h8 | +0.019 | -0.013 .. +0.051 | +0.0019 | 0.25 / 0.28 / 0.93 | nan |  |  | 9/16 | -0.011 | +0.049 |  | +2.0 / +1.2 |  |
| MES | 15 | h16 | -0.009 | -0.061 .. +0.043 | -0.0006 | 0.73 / 0.73 / 0.86 | nan |  |  | 9/16 | -0.058 | +0.040 |  | -0.9 / -0.3 |  |
| MES | 15 | eod | -0.144 | -0.388 .. +0.099 | -0.0038 | 0.24 / 0.25 / 0.87 | nan |  |  | 10/16 | -0.304 | +0.014 |  | -7.7 / -1.2 |  |
| MES | 60 | h1 * | +0.024 | +0.007 .. +0.042 | +0.0064 | 0.0071 / 0.0083 / 0.96 | nan | 1 | 0.796 | 9/16 | +0.014 | +0.034 | False | +2.7 / +2.7 |  |
| MES | 60 | h2 | +0.015 | -0.005 .. +0.034 | +0.0027 | 0.14 / 0.14 / 0.99 | nan |  |  | 9/16 | +0.003 | +0.026 |  | +1.5 / +1.5 |  |
| MES | 60 | h4 | -0.005 | -0.031 .. +0.022 | -0.0006 | 0.73 / 0.74 / 0.98 | nan |  |  | 9/16 | -0.020 | +0.011 |  | -0.4 / -0.3 | 0.038 |
| MES | 60 | h8 | -0.038 | -0.081 .. +0.006 | -0.0036 | 0.089 / 0.093 / 0.97 | nan |  |  | 11/16 | -0.063 | -0.012 |  | -3.2 / -1.7 |  |
| MES | 60 | h16 | -0.080 | -0.155 .. -0.005 | -0.0059 | 0.036 / 0.041 / 0.97 | nan |  |  | 12/16 | -0.117 | -0.043 |  | -5.9 / -2.1 |  |
| MES | 60 | eod | -0.099 | -0.181 .. -0.016 | -0.0069 | 0.019 / 0.023 / 0.96 | nan |  |  | 12/16 | -0.140 | -0.057 |  | -7.0 / -2.3 |  |
| MNQ | 5 | h1 | +0.004 | -0.001 .. +0.009 | +0.0011 | 0.14 / 0.16 / 0.62 | nan |  |  | 11/16 | +0.002 | +0.006 |  | +1.3 / +1.5 |  |
| MNQ | 5 | h2 | +0.008 | -0.003 .. +0.018 | +0.0014 | 0.14 / 0.15 / 0.75 | nan |  |  | 10/16 | +0.002 | +0.014 |  | +2.0 / +1.5 |  |
| MNQ | 5 | h4 | +0.016 | -0.005 .. +0.037 | +0.0019 | 0.13 / 0.14 / 0.86 | nan |  |  | 10/16 | +0.005 | +0.027 |  | +2.8 / +1.5 | 0.030 |
| MNQ | 5 | h8 | +0.030 | -0.009 .. +0.069 | +0.0023 | 0.14 / 0.15 / 0.95 | nan |  |  | 10/16 | +0.006 | +0.053 |  | +3.7 / +1.5 |  |
| MNQ | 5 | h16 | +0.044 | -0.016 .. +0.103 | +0.0024 | 0.15 / 0.16 / 0.85 | nan |  |  | 9/16 | -0.005 | +0.092 |  | +4.4 / +1.4 |  |
| MNQ | 5 | eod * | -0.619 | -1.144 .. -0.093 | -0.0072 | 0.021 / 0.024 / 0.5 | nan | 1 | 0.986 | 11/16 | -0.996 | -0.244 | False | -24.6 / -2.3 |  |
| MNQ | 15 | h1 * | +0.014 | +0.004 .. +0.023 | +0.0033 | 0.0042 / 0.0066 / 0.48 | nan | 0.927 | 0.656 | 11/16 | +0.016 | +0.011 | False | +2.6 / +2.9 |  |
| MNQ | 15 | h2 | +0.023 | +0.005 .. +0.040 | +0.0033 | 0.011 / 0.016 / 0.73 | nan |  |  | 12/16 | +0.021 | +0.024 |  | +3.1 / +2.5 |  |
| MNQ | 15 | h4 | +0.035 | +0.006 .. +0.064 | +0.0029 | 0.02 / 0.027 / 0.89 | nan |  |  | 10/16 | +0.023 | +0.046 |  | +3.5 / +2.3 | 0.042 |
| MNQ | 15 | h8 | +0.018 | -0.018 .. +0.053 | +0.0012 | 0.33 / 0.36 / 0.94 | nan |  |  | 8/16 | -0.002 | +0.037 |  | +1.6 / +1.0 |  |
| MNQ | 15 | h16 | -0.023 | -0.085 .. +0.038 | -0.0012 | 0.45 / 0.46 / 0.95 | nan |  |  | 10/16 | -0.077 | +0.029 |  | -1.9 / -0.8 |  |
| MNQ | 15 | eod | -0.180 | -0.471 .. +0.112 | -0.0033 | 0.23 / 0.23 / 0.98 | nan |  |  | 8/16 | -0.401 | +0.040 |  | -7.0 / -1.2 |  |
| MNQ | 60 | h1 * | +0.035 | +0.013 .. +0.056 | +0.0087 | 0.0015 / 0.0014 / 0.95 | nan | 0.249 | 0.326 | 11/16 | +0.031 | +0.038 | False | +3.0 / +3.2 |  |
| MNQ | 60 | h2 | +0.026 | +0.003 .. +0.048 | +0.0045 | 0.028 / 0.028 / 0.98 | nan |  |  | 9/16 | +0.019 | +0.032 |  | +2.2 / +2.2 |  |
| MNQ | 60 | h4 | +0.009 | -0.020 .. +0.038 | +0.0011 | 0.56 / 0.56 / 0.99 | nan |  |  | 7/16 | -0.003 | +0.020 |  | +0.7 / +0.6 | 0.042 |
| MNQ | 60 | h8 | -0.022 | -0.068 .. +0.023 | -0.0020 | 0.34 / 0.35 / 0.99 | nan |  |  | 12/16 | -0.045 | +0.000 |  | -1.6 / -1.0 |  |
| MNQ | 60 | h16 | -0.059 | -0.137 .. +0.019 | -0.0041 | 0.14 / 0.15 / 0.98 | nan |  |  | 10/16 | -0.095 | -0.024 |  | -3.8 / -1.5 |  |
| MNQ | 60 | eod | -0.078 | -0.163 .. +0.007 | -0.0052 | 0.071 / 0.082 / 0.98 | nan |  |  | 11/16 | -0.119 | -0.038 |  | -4.8 / -1.8 |  |
| MYM | 5 | h1 * | +0.004 | -0.003 .. +0.012 | +0.0012 | 0.23 / 0.23 / 0.82 | nan | 1 | 1 | 6/8 | n/a | +0.004 | False | +1.2 / +1.2 |  |
| MYM | 5 | h2 | +0.007 | -0.008 .. +0.023 | +0.0011 | 0.37 / 0.37 / 0.9 | nan |  |  | 4/8 | n/a | +0.007 |  | +1.3 / +0.9 |  |
| MYM | 5 | h4 | +0.011 | -0.022 .. +0.043 | +0.0011 | 0.51 / 0.51 / 0.99 | nan |  |  | 4/8 | n/a | +0.011 |  | +1.3 / +0.7 | 0.046 |
| MYM | 5 | h8 | +0.015 | -0.044 .. +0.074 | +0.0011 | 0.61 / 0.62 / 0.85 | nan |  |  | 4/8 | n/a | +0.015 |  | +1.4 / +0.5 |  |
| MYM | 5 | h16 | +0.045 | -0.037 .. +0.127 | +0.0025 | 0.28 / 0.29 / 0.75 | nan |  |  | 5/8 | n/a | +0.045 |  | +3.4 / +1.1 |  |
| MYM | 5 | eod | -0.209 | -0.982 .. +0.564 | -0.0026 | 0.6 / 0.59 / 0.45 | nan |  |  | 5/8 | n/a | -0.209 |  | -6.3 / -0.5 |  |
| MYM | 15 | h1 | +0.014 | +0.002 .. +0.027 | +0.0037 | 0.028 / 0.03 / 0.59 | nan |  |  | 6/8 | n/a | +0.014 |  | +2.1 / +2.2 |  |
| MYM | 15 | h2 | +0.024 | -0.001 .. +0.049 | +0.0035 | 0.055 / 0.061 / 0.77 | nan |  |  | 7/8 | n/a | +0.024 |  | +2.4 / +1.9 |  |
| MYM | 15 | h4 * | +0.051 | +0.013 .. +0.090 | +0.0044 | 0.0095 / 0.011 / 0.85 | nan | 1 | 0.826 | 5/8 | n/a | +0.051 | False | +4.0 / +2.6 | 0.055 |
| MYM | 15 | h8 | +0.057 | +0.001 .. +0.113 | +0.0038 | 0.046 / 0.044 / 0.84 | nan |  |  | 6/8 | n/a | +0.057 |  | +3.9 / +2.0 |  |
| MYM | 15 | h16 | +0.048 | -0.068 .. +0.163 | +0.0023 | 0.42 / 0.41 / 0.86 | nan |  |  | 3/8 | n/a | +0.048 |  | +2.7 / +0.8 |  |
| MYM | 15 | eod | -0.003 | -0.434 .. +0.427 | -0.0001 | 0.99 / 0.99 / 0.88 | nan |  |  | 5/8 | n/a | -0.003 |  | -0.1 / -0.0 |  |
| MYM | 60 | h1 * | +0.044 | +0.018 .. +0.070 | +0.0112 | 0.00087 / 0.00033 / 0.91 | nan | 0.151 | 0.216 | 6/8 | n/a | +0.044 | False | +3.7 / +3.3 |  |
| MYM | 60 | h2 | +0.039 | +0.010 .. +0.068 | +0.0069 | 0.0082 / 0.0041 / 0.94 | nan |  |  | 6/8 | n/a | +0.039 |  | +3.1 / +2.6 |  |
| MYM | 60 | h4 | +0.029 | -0.010 .. +0.069 | +0.0037 | 0.15 / 0.12 / 0.98 | nan |  |  | 5/8 | n/a | +0.029 |  | +2.1 / +1.4 | 0.057 |
| MYM | 60 | h8 | +0.015 | -0.052 .. +0.081 | +0.0014 | 0.66 / 0.65 / 0.99 | nan |  |  | 4/8 | n/a | +0.015 |  | +0.9 / +0.4 |  |
| MYM | 60 | h16 | -0.005 | -0.119 .. +0.110 | -0.0003 | 0.94 / 0.94 / 1 | nan |  |  | 5/8 | n/a | -0.005 |  | -0.2 / -0.1 |  |
| MYM | 60 | eod | -0.020 | -0.145 .. +0.105 | -0.0014 | 0.75 / 0.75 / 0.99 | nan |  |  | 5/8 | n/a | -0.020 |  | -1.0 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.036 | -0.044 .. -0.028 | -7.2% | -0.068 | 8.2e-20 |  | 11/16 |
| MES | 5 | h2 | -0.069 | -0.081 .. -0.057 | -9.8% | -0.141 | 2.2e-29 |  | 14/16 |
| MES | 5 | h4 | -0.144 | -0.163 .. -0.124 | -14.4% | -0.312 | 5.4e-47 |  | 16/16 |
| MES | 5 | h8 | -0.330 | -0.363 .. -0.296 | -22.9% | -0.732 | 1.7e-83 |  | 16/16 |
| MES | 5 | h16 | -0.910 | -0.962 .. -0.858 | -43.4% | -1.980 | 3.9e-261 |  | 16/16 |
| MES | 5 | eod * | -7.937 | -8.366 .. -7.508 | -79.6% | -15.724 | 5.2e-288 | 2.17e-284 | 16/16 |
| MES | 15 | h1 | +0.026 | +0.016 .. +0.035 | +5.0% | +0.035 | 1.6e-07 |  | 12/16 |
| MES | 15 | h2 | +0.001 | -0.014 .. +0.017 | +0.2% | -0.031 | 0.86 |  | 9/16 |
| MES | 15 | h4 | -0.138 | -0.161 .. -0.114 | -13.1% | -0.341 | 2.3e-30 |  | 16/16 |
| MES | 15 | h8 | -0.512 | -0.541 .. -0.483 | -33.3% | -1.100 | 5.1e-264 |  | 16/16 |
| MES | 15 | h16 * | -1.010 | -1.050 .. -0.969 | -44.2% | -2.078 | 0 | 0 | 16/16 |
| MES | 15 | eod | -2.266 | -2.448 .. -2.085 | -41.3% | -4.546 | 2.3e-132 |  | 16/16 |
| MES | 60 | h1 | -0.119 | -0.132 .. -0.106 | -23.2% | -0.230 | 3.4e-63 |  | 16/16 |
| MES | 60 | h2 * | -0.342 | -0.356 .. -0.328 | -46.3% | -0.679 | 0 | 0 | 16/16 |
| MES | 60 | h4 | -0.659 | -0.676 .. -0.642 | -62.2% | -1.315 | 0 |  | 16/16 |
| MES | 60 | h8 | -1.114 | -1.140 .. -1.087 | -73.9% | -2.224 | 0 |  | 16/16 |
| MES | 60 | h16 | -1.705 | -1.752 .. -1.657 | -82.8% | -3.373 | 0 |  | 16/16 |
| MES | 60 | eod | -1.824 | -1.879 .. -1.769 | -84.2% | -3.588 | 0 |  | 16/16 |
| MNQ | 5 | h1 | -0.062 | -0.069 .. -0.055 | -11.6% | -0.109 | 1.3e-61 |  | 15/16 |
| MNQ | 5 | h2 | -0.117 | -0.129 .. -0.105 | -15.2% | -0.228 | 7e-80 |  | 15/16 |
| MNQ | 5 | h4 | -0.230 | -0.251 .. -0.209 | -20.8% | -0.472 | 5.3e-103 |  | 16/16 |
| MNQ | 5 | h8 | -0.479 | -0.517 .. -0.441 | -29.6% | -1.017 | 6.3e-134 |  | 16/16 |
| MNQ | 5 | h16 | -1.168 | -1.230 .. -1.107 | -48.7% | -2.495 | 1.3e-298 |  | 16/16 |
| MNQ | 5 | eod * | -10.136 | -10.600 .. -9.671 | -80.7% | -20.024 | 0 | 0 | 16/16 |
| MNQ | 15 | h1 | -0.005 | -0.016 .. +0.005 | -1.0% | -0.028 | 0.32 |  | 8/16 |
| MNQ | 15 | h2 | -0.042 | -0.060 .. -0.024 | -5.4% | -0.112 | 4.7e-06 |  | 11/16 |
| MNQ | 15 | h4 | -0.174 | -0.207 .. -0.140 | -15.3% | -0.410 | 1.1e-23 |  | 16/16 |
| MNQ | 15 | h8 | -0.545 | -0.591 .. -0.500 | -32.5% | -1.171 | 4.7e-119 |  | 16/16 |
| MNQ | 15 | h16 * | -1.052 | -1.105 .. -0.998 | -41.6% | -2.155 | 0 | 0 | 16/16 |
| MNQ | 15 | eod | -2.359 | -2.602 .. -2.116 | -37.1% | -4.671 | 6.6e-81 |  | 16/16 |
| MNQ | 60 | h1 | -0.083 | -0.104 .. -0.063 | -15.8% | -0.178 | 7.4e-14 |  | 16/16 |
| MNQ | 60 | h2 | -0.311 | -0.331 .. -0.291 | -40.6% | -0.636 | 1.1e-168 |  | 16/16 |
| MNQ | 60 | h4 * | -0.642 | -0.664 .. -0.620 | -58.1% | -1.297 | 0 | 0 | 16/16 |
| MNQ | 60 | h8 | -1.132 | -1.161 .. -1.103 | -71.4% | -2.264 | 0 |  | 16/16 |
| MNQ | 60 | h16 | -1.803 | -1.851 .. -1.754 | -82.2% | -3.550 | 0 |  | 16/16 |
| MNQ | 60 | eod | -1.925 | -1.979 .. -1.871 | -83.7% | -3.768 | 0 |  | 16/16 |
| MYM | 5 | h1 | -0.069 | -0.083 .. -0.055 | -12.9% | -0.113 | 2.3e-21 |  | 7/8 |
| MYM | 5 | h2 | -0.124 | -0.147 .. -0.101 | -16.3% | -0.225 | 4.5e-27 |  | 8/8 |
| MYM | 5 | h4 | -0.238 | -0.277 .. -0.200 | -21.7% | -0.460 | 3.8e-34 |  | 8/8 |
| MYM | 5 | h8 | -0.486 | -0.553 .. -0.420 | -30.6% | -0.977 | 2.2e-46 |  | 8/8 |
| MYM | 5 | h16 | -1.194 | -1.296 .. -1.093 | -51.1% | -2.434 | 2.8e-118 |  | 8/8 |
| MYM | 5 | eod * | -9.240 | -9.980 .. -8.499 | -78.8% | -18.349 | 3.9e-132 | 6.97e-129 | 8/8 |
| MYM | 15 | h1 | -0.008 | -0.024 .. +0.009 | -1.4% | -0.023 | 0.37 |  | 4/8 |
| MYM | 15 | h2 | -0.054 | -0.080 .. -0.027 | -7.0% | -0.116 | 9.4e-05 |  | 4/8 |
| MYM | 15 | h4 | -0.232 | -0.276 .. -0.188 | -20.8% | -0.471 | 6.3e-25 |  | 8/8 |
| MYM | 15 | h8 | -0.619 | -0.678 .. -0.561 | -37.8% | -1.256 | 4.8e-96 |  | 8/8 |
| MYM | 15 | h16 * | -1.120 | -1.213 .. -1.026 | -45.5% | -2.266 | 1.9e-121 | 3.17e-118 | 8/8 |
| MYM | 15 | eod | -2.458 | -2.747 .. -2.169 | -40.8% | -4.875 | 2.1e-60 |  | 8/8 |
| MYM | 60 | h1 | -0.166 | -0.183 .. -0.149 | -31.6% | -0.294 | 1.5e-79 |  | 8/8 |
| MYM | 60 | h2 * | -0.393 | -0.411 .. -0.374 | -52.0% | -0.751 | 0 | 0 | 8/8 |
| MYM | 60 | h4 | -0.714 | -0.737 .. -0.691 | -66.1% | -1.401 | 0 |  | 8/8 |
| MYM | 60 | h8 | -1.190 | -1.224 .. -1.156 | -76.9% | -2.345 | 0 |  | 8/8 |
| MYM | 60 | h16 | -1.809 | -1.872 .. -1.746 | -85.3% | -3.557 | 0 |  | 8/8 |
| MYM | 60 | eod | -1.927 | -2.000 .. -1.854 | -86.5% | -3.764 | 0 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.05 pts | -0.58 .. +0.48 | 0.87 |
| MES | 15 | -0.54 pts | -1.25 .. +0.17 | 0.15 |
| MES | 60 | -2.30 pts | -3.18 .. -1.42 | 5.3e-07 |
| MNQ | 5 | -0.24 pts | -0.76 .. +0.29 | 0.4 |
| MNQ | 15 | -0.84 pts | -1.51 .. -0.16 | 0.017 |
| MNQ | 60 | -2.06 pts | -2.94 .. -1.17 | 9.2e-06 |
| MYM | 5 | +0.30 pts | -0.42 .. +1.02 | 0.42 |
| MYM | 15 | -0.20 pts | -1.12 .. +0.73 | 0.68 |
| MYM | 60 | -0.58 pts | -1.75 .. +0.60 | 0.35 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 66619 | +0.006 | 0.208 | +0.04 | -3.46 | -3.45 | -3.46 | -3.48 |
| MES | 5 | h2 | event | long | 66619 | +0.013 | 0.208 | +0.10 | -3.40 | -3.40 | -3.40 | -3.46 |
| MES | 5 | h4 | event | long | 66619 | +0.026 | 0.208 | +0.16 | -3.34 | -3.31 | -3.36 | -3.47 |
| MES | 5 | h8 | event | long | 66619 | +0.046 | 0.208 | +0.26 | -3.24 | -3.28 | -3.21 | -3.53 |
| MES | 5 | h16 | event | long | 66619 | +0.080 | 0.208 | +0.49 | -3.01 | -3.31 | -2.73 | -3.58 |
| MES | 5 | eod | event | short | 66619 | -0.081 | 0.208 | -0.50 | -4.00 | -3.69 | -4.29 | -2.30 |
| MES | 15 | h1 | event | long | 19835 | +0.014 | 0.124 | +0.16 | -3.34 | -3.34 | -3.34 | -3.34 |
| MES | 15 | h2 | event | long | 19835 | +0.022 | 0.124 | +0.23 | -3.27 | -3.28 | -3.26 | -3.29 |
| MES | 15 | h4 | event | long | 19835 | +0.038 | 0.124 | +0.47 | -3.03 | -3.35 | -2.75 | -3.08 |
| MES | 15 | h8 | event | long | 19835 | +0.042 | 0.124 | +0.57 | -2.93 | -3.36 | -2.54 | -3.04 |
| MES | 15 | h16 | event | short | 19835 | -0.042 | 0.124 | -0.57 | -4.07 | -3.64 | -4.46 | -3.84 |
| MES | 15 | eod | event | short | 19835 | -0.042 | 0.124 | -0.57 | -4.07 | -3.64 | -4.46 | -4.31 |
| MES | 60 | h1 | event | long | 3753 | +0.031 | 0.089 | +0.80 | -2.70 | -3.14 | -2.25 | -2.85 |
| MES | 60 | h2 | event | long | 3753 | +0.031 | 0.089 | +0.80 | -2.70 | -3.14 | -2.25 | -3.08 |
| MES | 60 | h4 | event | short | 3753 | -0.031 | 0.089 | -0.80 | -4.30 | -3.86 | -4.75 | -3.44 |
| MES | 60 | h8 | event | short | 3753 | -0.031 | 0.089 | -0.80 | -4.30 | -3.86 | -4.75 | -2.62 |
| MES | 60 | h16 | event | short | 3753 | -0.031 | 0.089 | -0.80 | -4.30 | -3.86 | -4.75 | -1.62 |
| MES | 60 | eod | event | short | 3753 | -0.031 | 0.089 | -0.80 | -4.30 | -3.86 | -4.75 | -1.04 |
| MNQ | 5 | h1 | event | long | 66502 | +0.007 | 0.084 | +0.07 | -1.93 | -1.94 | -1.93 | -1.97 |
| MNQ | 5 | h2 | event | long | 66502 | +0.015 | 0.084 | +0.15 | -1.85 | -1.87 | -1.83 | -1.90 |
| MNQ | 5 | h4 | event | long | 66502 | +0.031 | 0.084 | +0.28 | -1.72 | -1.73 | -1.72 | -1.81 |
| MNQ | 5 | h8 | event | long | 66502 | +0.061 | 0.084 | +0.58 | -1.42 | -1.57 | -1.29 | -1.65 |
| MNQ | 5 | h16 | event | long | 66502 | +0.105 | 0.084 | +1.08 | -0.92 | -1.38 | -0.49 | -1.41 |
| MNQ | 5 | eod | event | short | 66502 | -0.106 | 0.084 | -1.09 | -3.09 | -2.62 | -3.52 | -0.01 |
| MNQ | 15 | h1 | event | long | 19718 | +0.016 | 0.047 | +0.25 | -1.75 | -1.74 | -1.76 | -1.83 |
| MNQ | 15 | h2 | event | long | 19718 | +0.030 | 0.047 | +0.51 | -1.49 | -1.57 | -1.41 | -1.62 |
| MNQ | 15 | h4 | event | long | 19718 | +0.052 | 0.047 | +1.12 | -0.88 | -1.36 | -0.44 | -1.20 |
| MNQ | 15 | h8 | event | long | 19718 | +0.058 | 0.047 | +1.26 | -0.74 | -1.30 | -0.24 | -1.48 |
| MNQ | 15 | h16 | event | short | 19718 | -0.058 | 0.047 | -1.26 | -3.26 | -2.70 | -3.76 | -2.42 |
| MNQ | 15 | eod | event | short | 19718 | -0.058 | 0.047 | -1.26 | -3.26 | -2.70 | -3.76 | -5.11 |
| MNQ | 60 | h1 | event | long | 3753 | +0.042 | 0.035 | +1.61 | -0.39 | -1.12 | +0.34 | -0.59 |
| MNQ | 60 | h2 | event | long | 3753 | +0.042 | 0.035 | +1.61 | -0.39 | -1.12 | +0.34 | -0.82 |
| MNQ | 60 | h4 | event | long | 3753 | +0.042 | 0.035 | +1.61 | -0.39 | -1.12 | +0.34 | -1.24 |
| MNQ | 60 | h8 | event | short | 3753 | -0.042 | 0.035 | -1.61 | -3.61 | -2.88 | -4.34 | -2.02 |
| MNQ | 60 | h16 | event | short | 3753 | -0.042 | 0.035 | -1.61 | -3.61 | -2.88 | -4.34 | -1.52 |
| MNQ | 60 | eod | event | short | 3753 | -0.042 | 0.035 | -1.61 | -3.61 | -2.88 | -4.34 | -0.80 |
| MYM | 5 | h1 | event | long | 34789 | +0.007 | 0.111 | +0.08 | -1.92 | +nan | -1.92 | -1.95 |
| MYM | 5 | h2 | event | long | 34789 | +0.014 | 0.111 | +0.18 | -1.82 | +nan | -1.82 | -1.90 |
| MYM | 5 | h4 | event | long | 34789 | +0.027 | 0.111 | +0.32 | -1.68 | +nan | -1.68 | -1.89 |
| MYM | 5 | h8 | event | long | 34789 | +0.052 | 0.111 | +0.56 | -1.44 | +nan | -1.44 | -1.89 |
| MYM | 5 | h16 | event | long | 34789 | +0.105 | 0.111 | +1.05 | -0.95 | +nan | -0.95 | -1.74 |
| MYM | 5 | eod | event | short | 34789 | -0.107 | 0.111 | -1.07 | -3.07 | +nan | -3.07 | -0.93 |
| MYM | 15 | h1 | event | long | 10397 | +0.013 | 0.065 | +0.27 | -1.73 | +nan | -1.73 | -1.69 |
| MYM | 15 | h2 | event | long | 10397 | +0.023 | 0.065 | +0.44 | -1.56 | +nan | -1.56 | -1.48 |
| MYM | 15 | h4 | event | long | 10397 | +0.049 | 0.065 | +0.98 | -1.02 | +nan | -1.02 | -0.89 |
| MYM | 15 | h8 | event | long | 10397 | +0.058 | 0.065 | +1.19 | -0.81 | +nan | -0.81 | -0.65 |
| MYM | 15 | h16 | event | long | 10397 | +0.058 | 0.065 | +1.19 | -0.81 | +nan | -0.81 | -0.58 |
| MYM | 15 | eod | event | short | 10397 | -0.058 | 0.065 | -1.19 | -3.19 | +nan | -3.19 | -4.03 |
| MYM | 60 | h1 | event | long | 1866 | +0.046 | 0.045 | +1.63 | -0.37 | +nan | -0.37 | -0.51 |
| MYM | 60 | h2 | event | long | 1866 | +0.046 | 0.045 | +1.63 | -0.37 | +nan | -0.37 | -0.69 |
| MYM | 60 | h4 | event | long | 1866 | +0.046 | 0.045 | +1.63 | -0.37 | +nan | -0.37 | -1.06 |
| MYM | 60 | h8 | event | long | 1866 | +0.046 | 0.045 | +1.63 | -0.37 | +nan | -0.37 | -1.63 |
| MYM | 60 | h16 | event | short | 1866 | -0.046 | 0.045 | -1.63 | -3.63 | +nan | -3.63 | -1.49 |
| MYM | 60 | eod | event | short | 1866 | -0.046 | 0.045 | -1.63 | -3.63 | +nan | -3.63 | -0.75 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.001 | +0.001 | +0.002 | +0.001 | +0.002 | +0.000 | +0.000 | +0.001 | +0.002 | +0.001 | +0.008 |
| MES | 15 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +nan | +nan |
| MES | 60 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +nan | +nan | +nan | +nan |
| MNQ | 5 | +0.001 | +0.002 | +0.002 | +0.002 | +0.002 | +0.000 | +0.001 | +0.001 | +0.002 | +0.001 | +0.013 |
| MNQ | 15 | -0.000 | -0.000 | -0.000 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +nan | +nan |
| MNQ | 60 | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 | -0.000 | +nan | +nan | +nan | +nan |
| MYM | 5 | +0.002 | +0.001 | +0.002 | +0.002 | +0.003 | +0.000 | +0.001 | +0.001 | +0.002 | +0.000 | +0.006 |
| MYM | 15 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +nan | +nan |
| MYM | 60 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +nan | +nan | +nan | +nan |

## Calibration

- MES 5-min: 1036271 bars, 66619 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 19835 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3753 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 66502 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 19718 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 3753 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 34789 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 10397 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.047); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 1866 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
