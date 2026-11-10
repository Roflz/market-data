# Impact card: swing_struct

swing structure (5-bar fractals): higher high AND higher low (+1) vs lower high AND lower low (-1) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: state. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.014 R20 over the next 4 bars (20 min), p=0.4; we would catch an effect of 0.021 R20 or more 80% of the time).
- MES 5-min size: the market moves 2% MORE at the top level than at the bottom level over the next 1 bar (5 min) (+0.009 R20, CONFIRMED, q=3.71e-05, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.39 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.219 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.047 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.017).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.69 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.128 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.090 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.24).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.38 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.064 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.236 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.026 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% MORE at the top level than at the bottom level over the next 1 bar (5 min) (+0.012 R20, CONFIRMED, q=4.05e-05, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.04 at recent bar sizes, 90% range up to $0.46); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.320 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.063 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% MORE at the top level than at the bottom level over the next 1 bar (15 min) (+0.017 R20, CONFIRMED, q=7.04e-06, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.21 at recent bar sizes, 90% range up to $1.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.014 R20 over the next 1 bar (1 h), p=0.53; we would catch an effect of 0.084 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.14).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.63 at recent bar sizes, 90% range up to $6.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.773 R20 over the rest of the session (to 16:45), p=0.71; we would catch an effect of 0.038 R20 or more 80% of the time).
- MYM 5-min size: the market moves 3% MORE at the top level than at the bottom level over the next 1 bar (5 min) (+0.013 R20, CONFIRMED, q=0.0163, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.60 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.014 R20 over the next 1 bar (15 min), p=0.03; we would catch an effect of 0.092 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.17).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $2.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.039 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.113 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.82 at recent bar sizes, 90% range up to $2.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.006 .. +0.001 | -0.0013 | 0.22 / 0.2 / 0.23 | 0.225 |  |  | 8/16 | +0.000 | -0.005 |  | -1.2 / -1.2 |  |
| MES | 5 | h2 | -0.006 | -0.014 .. +0.001 | -0.0024 | 0.091 / 0.082 / 0.1 | 0.103 |  |  | 10/16 | -0.003 | -0.009 |  | -2.3 / -1.7 |  |
| MES | 5 | h4 * | -0.014 | -0.028 .. +0.001 | -0.0036 | 0.063 / 0.056 / 0.077 | 0.0732 | 1 | 1 | 10/16 | -0.011 | -0.017 | False | -3.5 / -1.9 | 0.021 |
| MES | 5 | h8 | -0.025 | -0.054 .. +0.004 | -0.0044 | 0.09 / 0.082 / 0.11 | 0.109 |  |  | 12/16 | -0.021 | -0.029 |  | -4.4 / -1.7 |  |
| MES | 5 | h16 | -0.030 | -0.085 .. +0.026 | -0.0035 | 0.29 / 0.28 / 0.32 | 0.32 |  |  | 11/16 | -0.021 | -0.039 |  | -3.7 / -1.1 |  |
| MES | 5 | eod | -0.033 | -0.524 .. +0.458 | -0.0007 | 0.89 / 0.9 / 0.9 | 0.906 |  |  | 10/16 | +0.109 | -0.175 |  | -0.8 / -0.1 |  |
| MES | 15 | h1 | -0.001 | -0.008 .. +0.005 | -0.0008 | 0.71 / 0.72 / 0.73 | 0.735 |  |  | 10/16 | -0.004 | +0.002 |  | -0.3 / -0.4 |  |
| MES | 15 | h2 | -0.002 | -0.015 .. +0.012 | -0.0007 | 0.82 / 0.82 / 0.83 | 0.84 |  |  | 10/16 | -0.008 | +0.005 |  | -0.3 / -0.2 |  |
| MES | 15 | h4 | -0.001 | -0.028 .. +0.025 | -0.0005 | 0.92 / 0.92 / 0.92 | 0.921 |  |  | 9/16 | -0.016 | +0.013 |  | -0.2 / -0.1 | 0.041 |
| MES | 15 | h8 | -0.003 | -0.054 .. +0.048 | -0.0008 | 0.9 / 0.91 / 0.91 | 0.913 |  |  | 8/16 | -0.039 | +0.033 |  | -0.3 / -0.1 |  |
| MES | 15 | h16 * | -0.047 | -0.147 .. +0.053 | -0.0058 | 0.36 / 0.37 / 0.4 | 0.393 | 1 | 1 | 8/16 | -0.144 | +0.050 | False | -2.9 / -0.9 |  |
| MES | 15 | eod | -0.107 | -0.527 .. +0.313 | -0.0046 | 0.62 / 0.63 / 0.62 | 0.62 |  |  | 10/16 | -0.077 | -0.137 |  | -2.5 / -0.5 |  |
| MES | 60 | h1 | -0.003 | -0.016 .. +0.011 | -0.0018 | 0.69 / 0.69 / 0.71 | 0.701 |  |  | 8/16 | -0.008 | +0.002 |  | -0.4 / -0.4 |  |
| MES | 60 | h2 | -0.007 | -0.034 .. +0.020 | -0.0029 | 0.63 / 0.63 / 0.65 | 0.65 |  |  | 8/16 | -0.014 | +0.001 |  | -0.7 / -0.5 |  |
| MES | 60 | h4 | -0.010 | -0.064 .. +0.043 | -0.0033 | 0.7 / 0.7 / 0.71 | 0.711 |  |  | 8/16 | -0.018 | -0.003 |  | -0.7 / -0.4 | 0.077 |
| MES | 60 | h8 | -0.039 | -0.140 .. +0.061 | -0.0081 | 0.44 / 0.44 / 0.46 | 0.446 |  |  | 11/16 | -0.044 | -0.035 |  | -2.0 / -0.8 |  |
| MES | 60 | h16 * | -0.090 | -0.263 .. +0.084 | -0.0129 | 0.31 / 0.3 / 0.32 | 0.317 | 1 | 1 | 10/16 | -0.063 | -0.116 | False | -3.5 / -1.0 |  |
| MES | 60 | eod | -0.081 | -0.275 .. +0.113 | -0.0109 | 0.41 / 0.4 / 0.41 | 0.414 |  |  | 10/16 | -0.031 | -0.131 |  | -3.0 / -0.8 |  |
| MNQ | 5 | h1 | -0.001 | -0.005 .. +0.004 | -0.0002 | 0.78 / 0.79 / 0.81 | 0.816 |  |  | 9/16 | -0.001 | +0.000 |  | -0.3 / -0.3 |  |
| MNQ | 5 | h2 | -0.004 | -0.012 .. +0.004 | -0.0010 | 0.35 / 0.36 / 0.45 | 0.453 |  |  | 10/16 | -0.006 | -0.001 |  | -1.2 / -0.9 |  |
| MNQ | 5 | h4 | -0.008 | -0.024 .. +0.007 | -0.0015 | 0.3 / 0.3 / 0.4 | 0.399 |  |  | 10/16 | -0.016 | -0.002 |  | -1.9 / -1.0 | 0.026 |
| MNQ | 5 | h8 | -0.008 | -0.041 .. +0.026 | -0.0008 | 0.66 / 0.66 / 0.71 | 0.718 |  |  | 10/16 | -0.029 | +0.014 |  | -1.1 / -0.4 |  |
| MNQ | 5 | h16 | -0.005 | -0.074 .. +0.063 | -0.0001 | 0.88 / 0.88 / 0.89 | 0.886 |  |  | 9/16 | -0.070 | +0.058 |  | -0.5 / -0.2 |  |
| MNQ | 5 | eod * | +0.236 | -0.311 .. +0.783 | +0.0048 | 0.4 / 0.39 / 0.4 | 0.403 | 1 | 1 | 11/16 | +0.051 | +0.418 | False | +4.6 / +0.8 |  |
| MNQ | 15 | h1 | +0.001 | -0.005 .. +0.008 | +0.0004 | 0.69 / 0.7 / 0.72 | 0.717 |  |  | 8/16 | +0.004 | -0.001 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h2 | -0.003 | -0.020 .. +0.013 | -0.0011 | 0.7 / 0.71 / 0.71 | 0.726 |  |  | 9/16 | +0.008 | -0.014 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h4 | -0.011 | -0.048 .. +0.026 | -0.0018 | 0.55 / 0.57 / 0.57 | 0.579 |  |  | 10/16 | +0.014 | -0.036 |  | -0.9 / -0.6 | 0.063 |
| MNQ | 15 | h8 | -0.021 | -0.086 .. +0.043 | -0.0024 | 0.52 / 0.54 / 0.56 | 0.567 |  |  | 10/16 | +0.020 | -0.063 |  | -1.3 / -0.6 |  |
| MNQ | 15 | h16 | -0.052 | -0.184 .. +0.080 | -0.0050 | 0.44 / 0.46 / 0.43 | 0.425 |  |  | 9/16 | +0.034 | -0.137 |  | -2.4 / -0.8 |  |
| MNQ | 15 | eod * | -0.320 | -0.898 .. +0.259 | -0.0102 | 0.28 / 0.29 / 0.2 | 0.212 | 1 | 1 | 10/16 | -0.114 | -0.524 | False | -5.0 / -1.1 |  |
| MNQ | 60 | h1 * | -0.014 | -0.029 .. +0.001 | -0.0074 | 0.073 / 0.066 / 0.082 | 0.0826 | 1 | 1 | 12/16 | -0.009 | -0.019 | False | -1.8 / -1.8 |  |
| MNQ | 60 | h2 | -0.020 | -0.050 .. +0.009 | -0.0079 | 0.18 / 0.17 / 0.19 | 0.198 |  |  | 11/16 | -0.005 | -0.036 |  | -1.9 / -1.4 |  |
| MNQ | 60 | h4 | -0.036 | -0.094 .. +0.021 | -0.0098 | 0.22 / 0.21 / 0.23 | 0.235 |  |  | 11/16 | -0.001 | -0.072 |  | -2.4 / -1.2 | 0.084 |
| MNQ | 60 | h8 | -0.049 | -0.156 .. +0.059 | -0.0093 | 0.37 / 0.37 / 0.39 | 0.401 |  |  | 11/16 | +0.040 | -0.137 |  | -2.3 / -0.9 |  |
| MNQ | 60 | h16 | -0.097 | -0.280 .. +0.086 | -0.0144 | 0.3 / 0.29 / 0.32 | 0.321 |  |  | 11/16 | +0.055 | -0.249 |  | -3.5 / -1.0 |  |
| MNQ | 60 | eod | -0.123 | -0.324 .. +0.079 | -0.0173 | 0.23 / 0.22 / 0.25 | 0.256 |  |  | 11/16 | +0.038 | -0.282 |  | -4.3 / -1.2 |  |
| MYM | 5 | h1 | -0.004 | -0.012 .. +0.004 | -0.0016 | 0.31 / 0.32 / 0.26 | 0.269 |  |  | 6/8 | n/a | -0.004 |  | -1.0 / -1.0 |  |
| MYM | 5 | h2 | -0.009 | -0.026 .. +0.008 | -0.0022 | 0.31 / 0.32 / 0.25 | 0.246 |  |  | 7/8 | n/a | -0.009 |  | -1.4 / -1.0 |  |
| MYM | 5 | h4 | -0.017 | -0.056 .. +0.023 | -0.0026 | 0.41 / 0.43 / 0.33 | 0.345 |  |  | 7/8 | n/a | -0.017 |  | -1.6 / -0.8 | 0.038 |
| MYM | 5 | h8 | -0.037 | -0.112 .. +0.039 | -0.0042 | 0.34 / 0.35 / 0.22 | 0.217 |  |  | 6/8 | n/a | -0.037 |  | -2.4 / -1.0 |  |
| MYM | 5 | h16 | -0.065 | -0.195 .. +0.064 | -0.0060 | 0.32 / 0.34 / 0.21 | 0.198 |  |  | 6/8 | n/a | -0.065 |  | -3.4 / -1.0 |  |
| MYM | 5 | eod * | -0.773 | -1.744 .. +0.198 | -0.0163 | 0.12 / 0.11 / 0.025 | 0.0221 | 1 | 1 | 7/8 | n/a | -0.773 | False | -9.8 / -1.6 |  |
| MYM | 15 | h1 * | -0.014 | -0.023 .. -0.005 | -0.0066 | 0.002 / 0.0039 / 0.01 | 0.01 | 0.73 | 0.401 | 8/8 | n/a | -0.014 | False | -2.4 / -3.1 |  |
| MYM | 15 | h2 | -0.034 | -0.061 .. -0.007 | -0.0087 | 0.014 / 0.02 / 0.016 | 0.0116 |  |  | 8/8 | n/a | -0.034 |  | -2.9 / -2.4 |  |
| MYM | 15 | h4 | -0.065 | -0.124 .. -0.005 | -0.0097 | 0.034 / 0.045 / 0.029 | 0.0216 |  |  | 8/8 | n/a | -0.065 |  | -3.1 / -2.1 | 0.092 |
| MYM | 15 | h8 | -0.105 | -0.212 .. +0.002 | -0.0122 | 0.054 / 0.071 / 0.053 | 0.0558 |  |  | 7/8 | n/a | -0.105 |  | -3.9 / -1.9 |  |
| MYM | 15 | h16 | -0.185 | -0.404 .. +0.034 | -0.0163 | 0.098 / 0.12 / 0.061 | 0.0606 |  |  | 6/8 | n/a | -0.185 |  | -5.2 / -1.7 |  |
| MYM | 15 | eod | -0.542 | -1.291 .. +0.207 | -0.0182 | 0.16 / 0.18 / 0.094 | 0.0959 |  |  | 6/8 | n/a | -0.542 |  | -6.2 / -1.4 |  |
| MYM | 60 | h1 | -0.001 | -0.022 .. +0.019 | -0.0010 | 0.89 / 0.89 / 0.9 | 0.907 |  |  | 5/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 60 | h2 | -0.005 | -0.048 .. +0.037 | -0.0022 | 0.8 / 0.8 / 0.8 | 0.802 |  |  | 4/8 | n/a | -0.005 |  | -0.4 / -0.2 |  |
| MYM | 60 | h4 | -0.010 | -0.091 .. +0.072 | -0.0023 | 0.82 / 0.81 / 0.82 | 0.812 |  |  | 3/8 | n/a | -0.010 |  | -0.5 / -0.2 | 0.113 |
| MYM | 60 | h8 | -0.006 | -0.156 .. +0.145 | +0.0002 | 0.94 / 0.94 / 0.95 | 0.942 |  |  | 3/8 | n/a | -0.006 |  | -0.2 / -0.1 |  |
| MYM | 60 | h16 * | -0.039 | -0.286 .. +0.208 | -0.0041 | 0.76 / 0.75 / 0.77 | 0.76 | 1 | 1 | 4/8 | n/a | -0.039 | False | -1.1 / -0.3 |  |
| MYM | 60 | eod | -0.041 | -0.314 .. +0.232 | -0.0039 | 0.77 / 0.77 / 0.78 | 0.776 |  |  | 5/8 | n/a | -0.041 |  | -1.1 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.009 | +0.006 .. +0.012 | +1.8% | +0.022 | 1.4e-07 | 3.71e-05 | 14/16 |
| MES | 5 | h2 | +0.009 | +0.003 .. +0.015 | +1.3% | +0.028 | 0.0039 |  | 12/16 |
| MES | 5 | h4 | +0.011 | -0.000 .. +0.022 | +1.1% | +0.034 | 0.14 |  | 12/16 |
| MES | 5 | h8 | +0.016 | -0.002 .. +0.035 | +1.1% | +0.044 | 0.27 |  | 11/16 |
| MES | 5 | h16 | +0.029 | -0.005 .. +0.064 | +1.4% | +0.061 | 0.2 |  | 11/16 |
| MES | 5 | eod | +0.063 | -0.260 .. +0.385 | +0.6% | +0.330 | 0.98 |  | 9/16 |
| MES | 15 | h1 * | +0.009 | +0.003 .. +0.014 | +1.7% | +0.023 | 0.0028 | 0.439 | 11/16 |
| MES | 15 | h2 | +0.009 | -0.001 .. +0.020 | +1.3% | +0.027 | 0.13 |  | 11/16 |
| MES | 15 | h4 | +0.008 | -0.011 .. +0.028 | +0.8% | +0.029 | 0.6 |  | 9/16 |
| MES | 15 | h8 | -0.005 | -0.042 .. +0.032 | -0.3% | +0.031 | 0.81 |  | 10/16 |
| MES | 15 | h16 | -0.004 | -0.076 .. +0.067 | -0.2% | +0.029 | 0.9 |  | 8/16 |
| MES | 15 | eod | +0.043 | -0.271 .. +0.357 | +0.8% | +0.057 | 0.97 |  | 9/16 |
| MES | 60 | h1 * | +0.011 | +0.001 .. +0.020 | +2.1% | +0.020 | 0.041 | 1 | 12/16 |
| MES | 60 | h2 | +0.010 | -0.007 .. +0.026 | +1.3% | +0.020 | 0.28 |  | 8/16 |
| MES | 60 | h4 | +0.002 | -0.029 .. +0.034 | +0.2% | +0.015 | 0.89 |  | 9/16 |
| MES | 60 | h8 | -0.010 | -0.069 .. +0.049 | -0.7% | +0.008 | 0.88 |  | 7/16 |
| MES | 60 | h16 | +0.004 | -0.103 .. +0.110 | +0.2% | +0.042 | 0.95 |  | 10/16 |
| MES | 60 | eod | -0.001 | -0.120 .. +0.118 | -0.0% | +0.049 | 0.99 |  | 6/16 |
| MNQ | 5 | h1 * | +0.012 | +0.008 .. +0.015 | +2.2% | +0.026 | 1.6e-07 | 4.05e-05 | 15/16 |
| MNQ | 5 | h2 | +0.014 | +0.008 .. +0.019 | +1.8% | +0.035 | 0.0078 |  | 14/16 |
| MNQ | 5 | h4 | +0.017 | +0.007 .. +0.028 | +1.6% | +0.049 | 0.079 |  | 12/16 |
| MNQ | 5 | h8 | +0.029 | +0.006 .. +0.053 | +1.8% | +0.070 | 0.087 |  | 12/16 |
| MNQ | 5 | h16 | +0.049 | -0.002 .. +0.100 | +2.0% | +0.112 | 0.11 |  | 9/16 |
| MNQ | 5 | eod | +0.118 | -0.231 .. +0.466 | +0.9% | +0.120 | 0.75 |  | 8/16 |
| MNQ | 15 | h1 * | +0.017 | +0.011 .. +0.023 | +3.1% | +0.037 | 2.5e-08 | 7.04e-06 | 15/16 |
| MNQ | 15 | h2 | +0.025 | +0.009 .. +0.040 | +3.2% | +0.055 | 0.0017 |  | 14/16 |
| MNQ | 15 | h4 | +0.036 | -0.007 .. +0.079 | +3.2% | +0.081 | 0.1 |  | 10/16 |
| MNQ | 15 | h8 | +0.053 | -0.023 .. +0.129 | +3.2% | +0.133 | 0.17 |  | 9/16 |
| MNQ | 15 | h16 | +0.081 | -0.028 .. +0.189 | +3.2% | +0.223 | 0.17 |  | 12/16 |
| MNQ | 15 | eod | +0.402 | -0.085 .. +0.889 | +6.3% | +0.435 | 0.11 |  | 11/16 |
| MNQ | 60 | h1 * | +0.013 | +0.002 .. +0.024 | +2.4% | +0.023 | 0.023 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.014 | -0.006 .. +0.033 | +1.8% | +0.024 | 0.17 |  | 10/16 |
| MNQ | 60 | h4 | +0.015 | -0.022 .. +0.052 | +1.4% | +0.025 | 0.42 |  | 8/16 |
| MNQ | 60 | h8 | +0.021 | -0.046 .. +0.087 | +1.3% | +0.022 | 0.54 |  | 9/16 |
| MNQ | 60 | h16 | +0.041 | -0.074 .. +0.157 | +1.9% | +0.030 | 0.48 |  | 11/16 |
| MNQ | 60 | eod | +0.036 | -0.091 .. +0.163 | +1.6% | +0.030 | 0.58 |  | 10/16 |
| MYM | 5 | h1 * | +0.013 | +0.008 .. +0.019 | +2.5% | +0.028 | 7.8e-05 | 0.0163 | 8/8 |
| MYM | 5 | h2 | +0.017 | +0.003 .. +0.031 | +2.3% | +0.038 | 0.019 |  | 7/8 |
| MYM | 5 | h4 | +0.023 | -0.011 .. +0.057 | +2.1% | +0.052 | 0.2 |  | 6/8 |
| MYM | 5 | h8 | +0.030 | -0.030 .. +0.090 | +1.9% | +0.074 | 0.35 |  | 6/8 |
| MYM | 5 | h16 | +0.072 | -0.031 .. +0.175 | +3.1% | +0.118 | 0.19 |  | 7/8 |
| MYM | 5 | eod | +0.173 | -0.580 .. +0.926 | +1.5% | +0.293 | 0.69 |  | 5/8 |
| MYM | 15 | h1 * | +0.010 | +0.001 .. +0.018 | +1.8% | +0.027 | 0.029 | 1 | 7/8 |
| MYM | 15 | h2 | +0.018 | -0.005 .. +0.041 | +2.4% | +0.042 | 0.16 |  | 6/8 |
| MYM | 15 | h4 | +0.041 | -0.019 .. +0.101 | +3.7% | +0.068 | 0.22 |  | 6/8 |
| MYM | 15 | h8 | +0.057 | -0.047 .. +0.162 | +3.5% | +0.122 | 0.33 |  | 6/8 |
| MYM | 15 | h16 | +0.109 | -0.077 .. +0.296 | +4.5% | +0.236 | 0.29 |  | 5/8 |
| MYM | 15 | eod | +0.406 | -0.228 .. +1.040 | +6.8% | +0.378 | 0.23 |  | 5/8 |
| MYM | 60 | h1 * | +0.010 | -0.005 .. +0.025 | +1.9% | +0.019 | 0.21 | 1 | 7/8 |
| MYM | 60 | h2 | +0.003 | -0.023 .. +0.028 | +0.4% | +0.015 | 0.83 |  | 4/8 |
| MYM | 60 | h4 | -0.003 | -0.047 .. +0.042 | -0.2% | +0.008 | 0.97 |  | 4/8 |
| MYM | 60 | h8 | -0.027 | -0.107 .. +0.053 | -1.7% | -0.003 | 0.63 |  | 4/8 |
| MYM | 60 | h16 | -0.022 | -0.174 .. +0.129 | -1.1% | +0.012 | 0.81 |  | 5/8 |
| MYM | 60 | eod | -0.031 | -0.198 .. +0.136 | -1.4% | +0.015 | 0.75 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.19 pts | -0.68 .. +0.30 | 0.45 |
| MES | 15 | -0.52 pts | -1.34 .. +0.30 | 0.42 |
| MES | 60 | +0.22 pts | -1.48 .. +1.93 | 0.89 |
| MNQ | 5 | -0.07 pts | -0.52 .. +0.37 | 0.75 |
| MNQ | 15 | -0.11 pts | -0.93 .. +0.71 | 0.98 |
| MNQ | 60 | +0.51 pts | -1.21 .. +2.22 | 0.6 |
| MYM | 5 | -0.32 pts | -0.90 .. +0.26 | 0.29 |
| MYM | 15 | -1.84 pts | -2.92 .. -0.75 | 0.0047 |
| MYM | 60 | -0.39 pts | -3.02 .. +2.23 | 0.77 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom level | long | 254332 | +0.003 | 0.285 | +0.05 | -3.45 | -3.49 | -3.42 | -3.45 |
| MES | 5 | h2 | bottom level | long | 254332 | +0.008 | 0.285 | +0.11 | -3.39 | -3.45 | -3.33 | -3.40 |
| MES | 5 | h4 | bottom level | long | 254332 | +0.018 | 0.285 | +0.24 | -3.26 | -3.35 | -3.16 | -3.29 |
| MES | 5 | h8 | bottom level | long | 254332 | +0.039 | 0.285 | +0.48 | -3.02 | -3.18 | -2.86 | -3.12 |
| MES | 5 | h16 | bottom level | long | 254332 | +0.070 | 0.285 | +0.93 | -2.57 | -2.99 | -2.18 | -2.83 |
| MES | 5 | eod | bottom level | long | 254332 | +0.501 | 0.285 | +5.02 | +1.52 | -0.97 | +3.82 | +1.48 |
| MES | 15 | h1 | bottom level | long | 81715 | +0.004 | 0.163 | +0.04 | -3.46 | -3.48 | -3.44 | -3.50 |
| MES | 15 | h2 | bottom level | long | 81715 | +0.006 | 0.163 | +0.04 | -3.46 | -3.43 | -3.48 | -3.53 |
| MES | 15 | h4 | bottom level | long | 81715 | +0.012 | 0.163 | +0.10 | -3.40 | -3.31 | -3.48 | -3.54 |
| MES | 15 | h8 | bottom level | long | 81715 | +0.024 | 0.163 | +0.09 | -3.41 | -3.09 | -3.71 | -3.65 |
| MES | 15 | h16 | bottom level | long | 81715 | +0.066 | 0.163 | +0.49 | -3.01 | -2.27 | -3.68 | -3.21 |
| MES | 15 | eod | bottom level | long | 81715 | +0.278 | 0.163 | +4.86 | +1.36 | +0.73 | +1.93 | +1.37 |
| MES | 60 | h1 | bottom level | long | 20307 | +0.008 | 0.082 | +0.27 | -3.23 | -3.24 | -3.22 | -3.40 |
| MES | 60 | h2 | bottom level | long | 20307 | +0.016 | 0.082 | +0.54 | -2.96 | -3.02 | -2.89 | -3.35 |
| MES | 60 | h4 | bottom level | long | 20307 | +0.032 | 0.082 | +1.09 | -2.41 | -2.69 | -2.15 | -3.28 |
| MES | 60 | h8 | bottom level | long | 20307 | +0.069 | 0.082 | +2.27 | -1.23 | -2.26 | -0.26 | -2.87 |
| MES | 60 | h16 | bottom level | long | 20307 | +0.134 | 0.082 | +5.63 | +2.13 | -1.95 | +5.98 | -0.42 |
| MES | 60 | eod | bottom level | long | 20307 | +0.148 | 0.082 | +6.42 | +2.92 | -2.06 | +7.63 | -0.28 |
| MNQ | 5 | h1 | bottom level | long | 272273 | +0.004 | 0.115 | +0.02 | -1.98 | -1.98 | -1.97 | -1.98 |
| MNQ | 5 | h2 | bottom level | long | 272273 | +0.009 | 0.115 | +0.05 | -1.95 | -1.95 | -1.94 | -1.93 |
| MNQ | 5 | h4 | bottom level | long | 272273 | +0.019 | 0.115 | +0.11 | -1.89 | -1.88 | -1.90 | -1.85 |
| MNQ | 5 | h8 | bottom level | long | 272273 | +0.037 | 0.115 | +0.18 | -1.82 | -1.73 | -1.90 | -1.82 |
| MNQ | 5 | h16 | bottom level | long | 272273 | +0.077 | 0.115 | +0.69 | -1.31 | -1.41 | -1.21 | -1.46 |
| MNQ | 5 | eod | top level | long | 317016 | +1.152 | 0.137 | +8.38 | +6.38 | +1.81 | +10.61 | +3.22 |
| MNQ | 15 | h1 | top level | long | 106587 | +0.009 | 0.080 | +0.14 | -1.86 | -1.89 | -1.83 | -1.97 |
| MNQ | 15 | h2 | bottom level | long | 84525 | +0.014 | 0.066 | +0.22 | -1.78 | -1.87 | -1.69 | -1.94 |
| MNQ | 15 | h4 | bottom level | long | 84525 | +0.029 | 0.066 | +0.47 | -1.53 | -1.75 | -1.32 | -1.84 |
| MNQ | 15 | h8 | bottom level | long | 84525 | +0.055 | 0.066 | +0.87 | -1.13 | -1.52 | -0.76 | -1.70 |
| MNQ | 15 | h16 | bottom level | long | 84525 | +0.079 | 0.066 | +1.32 | -0.68 | -1.15 | -0.24 | -0.91 |
| MNQ | 15 | eod | bottom level | long | 84525 | +0.410 | 0.066 | +7.76 | +5.76 | +2.38 | +8.85 | +6.79 |
| MNQ | 60 | h1 | bottom level | long | 20177 | +0.013 | 0.032 | +0.89 | -1.11 | -1.85 | -0.44 | -1.31 |
| MNQ | 60 | h2 | bottom level | long | 20177 | +0.023 | 0.032 | +1.64 | -0.36 | -1.83 | +0.98 | -0.83 |
| MNQ | 60 | h4 | bottom level | long | 20177 | +0.045 | 0.032 | +3.50 | +1.50 | -1.75 | +4.48 | +0.53 |
| MNQ | 60 | h8 | bottom level | long | 20177 | +0.081 | 0.032 | +7.13 | +5.13 | -1.66 | +11.35 | +3.18 |
| MNQ | 60 | h16 | bottom level | long | 20177 | +0.131 | 0.032 | +11.66 | +9.66 | -1.39 | +19.77 | +6.72 |
| MNQ | 60 | eod | bottom level | long | 20177 | +0.157 | 0.032 | +13.19 | +11.19 | -1.27 | +22.59 | +7.43 |
| MYM | 5 | h1 | bottom level | long | 141053 | +0.003 | 0.157 | +0.06 | -1.94 | +nan | -1.94 | -1.93 |
| MYM | 5 | h2 | bottom level | long | 141053 | +0.003 | 0.157 | +0.12 | -1.88 | +nan | -1.88 | -1.83 |
| MYM | 5 | h4 | bottom level | long | 141053 | -0.002 | 0.157 | +0.24 | -1.76 | +nan | -1.76 | -1.65 |
| MYM | 5 | h8 | bottom level | long | 141053 | -0.007 | 0.157 | +0.38 | -1.62 | +nan | -1.62 | -1.44 |
| MYM | 5 | h16 | bottom level | long | 141053 | -0.006 | 0.157 | +0.66 | -1.34 | +nan | -1.34 | -1.21 |
| MYM | 5 | eod | bottom level | long | 141053 | +0.417 | 0.157 | +4.98 | +2.98 | +nan | +2.98 | +3.11 |
| MYM | 15 | h1 | bottom level | long | 45408 | +0.006 | 0.089 | +0.25 | -1.75 | +nan | -1.75 | -1.73 |
| MYM | 15 | h2 | bottom level | long | 45408 | +0.012 | 0.089 | +0.41 | -1.59 | +nan | -1.59 | -1.52 |
| MYM | 15 | h4 | bottom level | long | 45408 | +0.021 | 0.089 | +0.63 | -1.37 | +nan | -1.37 | -1.23 |
| MYM | 15 | h8 | bottom level | long | 45408 | +0.025 | 0.089 | +0.70 | -1.30 | +nan | -1.30 | -0.98 |
| MYM | 15 | h16 | bottom level | long | 45408 | +0.020 | 0.089 | +0.61 | -1.39 | +nan | -1.39 | -0.64 |
| MYM | 15 | eod | bottom level | long | 45408 | +0.236 | 0.089 | +5.53 | +3.53 | +nan | +3.53 | +4.73 |
| MYM | 60 | h1 | bottom level | long | 10962 | +0.001 | 0.043 | +0.31 | -1.69 | +nan | -1.69 | -1.77 |
| MYM | 60 | h2 | bottom level | long | 10962 | +0.004 | 0.043 | +0.52 | -1.48 | +nan | -1.48 | -1.63 |
| MYM | 60 | h4 | bottom level | long | 10962 | +0.015 | 0.043 | +1.01 | -0.99 | +nan | -0.99 | -1.34 |
| MYM | 60 | h8 | bottom level | long | 10962 | +0.040 | 0.043 | +2.34 | +0.34 | +nan | +0.34 | -0.33 |
| MYM | 60 | h16 | bottom level | long | 10962 | +0.081 | 0.043 | +6.49 | +4.49 | +nan | +4.49 | +3.21 |
| MYM | 60 | eod | bottom level | long | 10962 | +0.103 | 0.043 | +8.15 | +6.15 | +nan | +6.15 | +4.04 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.813 | +0.656 | +0.292 | +0.112 | +0.043 | +0.000 | -0.002 | -0.006 | -0.013 | -0.023 | -0.020 |
| MES | 15 | +0.779 | +0.698 | +0.316 | +0.122 | +0.046 | +0.000 | -0.001 | -0.001 | +0.001 | +0.005 | -0.042 |
| MES | 60 | +0.896 | +0.572 | +0.316 | +0.131 | +0.053 | +0.000 | -0.000 | +0.001 | +0.008 | -0.010 | -0.034 |
| MNQ | 5 | +0.794 | +0.761 | +0.349 | +0.135 | +0.054 | +0.000 | +0.001 | -0.003 | -0.008 | -0.008 | -0.006 |
| MNQ | 15 | +0.664 | +0.735 | +0.346 | +0.136 | +0.055 | +0.000 | -0.005 | -0.011 | -0.018 | -0.026 | -0.049 |
| MNQ | 60 | +1.006 | +0.610 | +0.378 | +0.164 | +0.068 | +0.000 | -0.011 | -0.015 | -0.028 | -0.019 | -0.030 |
| MYM | 5 | +0.850 | +0.815 | +0.374 | +0.146 | +0.056 | +0.000 | -0.003 | -0.009 | -0.018 | -0.041 | -0.079 |
| MYM | 15 | +0.775 | +0.823 | +0.387 | +0.159 | +0.068 | +0.000 | -0.024 | -0.044 | -0.079 | -0.126 | -0.235 |
| MYM | 60 | +0.821 | +0.574 | +0.331 | +0.141 | +0.057 | +0.000 | -0.001 | -0.003 | +0.004 | +0.000 | -0.108 |

## Calibration

- MES 5-min: 1031774 bars, 309581 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 339588 bars, 105415 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 81702 bars, 28549 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1032244 bars, 317016 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 340290 bars, 106587 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 81866 bars, 28220 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518032 bars, 158516 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170449 bars, 52156 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 40979 bars, 13606 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
