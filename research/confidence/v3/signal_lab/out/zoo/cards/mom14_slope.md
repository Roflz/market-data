# Impact card: mom14_slope

1-bar change of Momentum(14) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.004 R20 over the next 1 bar (5 min), p=0.93; we would catch an effect of 0.013 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.015 R20, CONFIRMED, q=7.31e-14, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.14 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.161 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.008 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 15-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.022 R20, CONFIRMED, q=6.9e-08, 12 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.43 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.096 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.058 R20 over the rest of the session (to 16:45), p=0.57; we would catch an effect of 0.050 R20 or more 80% of the time).
- MES 60-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.022 R20, possible, q=0.085, 12 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.80 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.051 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.046 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.019 R20, CONFIRMED, q=3.32e-14, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.24 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.057 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.033 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.027 R20, CONFIRMED, q=1.82e-09, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.26 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.034 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.078 R20 over the rest of the session (to 16:45), p=0.19; we would catch an effect of 0.054 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.026 R20, CONFIRMED, q=0.0196, 12 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.18 at recent bar sizes, 90% range up to $4.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (5 min), p=0.88; we would catch an effect of 0.025 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (5 min) (-0.019 R20, CONFIRMED, q=0.000873, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.25 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.120 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.013 R20 over the next 1 bar (15 min), p=0.6; we would catch an effect of 0.044 R20 or more 80% of the time).
- MYM 15-min size: the market moves 5% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.027 R20, CONFIRMED, q=0.00909, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.59 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.071 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.009 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.074 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.035).
- MYM 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.69 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.038 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.004 | -0.009 .. +0.001 | -0.0018 | 0.095 / 0.086 / 0.08 | 0.0841 | 1 | 1 | 10/16 | -0.009 | +0.001 | False | -1.8 / -1.7 |  |
| MES | 5 | h2 | -0.003 | -0.009 .. +0.004 | -0.0011 | 0.38 / 0.37 / 0.4 | 0.399 |  |  | 10/16 | -0.012 | +0.006 |  | -0.9 / -0.9 |  |
| MES | 5 | h4 | -0.000 | -0.008 .. +0.008 | +0.0001 | 0.94 / 0.94 / 0.97 | 0.971 |  |  | 8/16 | -0.008 | +0.008 |  | -0.1 / -0.1 | 0.013 |
| MES | 5 | h8 | +0.001 | -0.010 .. +0.012 | +0.0003 | 0.83 / 0.84 / 0.85 | 0.843 |  |  | 8/16 | -0.005 | +0.007 |  | +0.2 / +0.2 |  |
| MES | 5 | h16 | -0.002 | -0.019 .. +0.014 | -0.0000 | 0.77 / 0.77 / 0.79 | 0.782 |  |  | 9/16 | -0.015 | +0.010 |  | -0.3 / -0.3 |  |
| MES | 5 | eod | +0.016 | -0.031 .. +0.062 | +0.0007 | 0.51 / 0.51 / 0.55 | 0.549 |  |  | 9/16 | +0.003 | +0.028 |  | +0.4 / +0.7 |  |
| MES | 15 | h1 | -0.002 | -0.010 .. +0.007 | -0.0002 | 0.71 / 0.71 / 0.71 | 0.707 |  |  | 11/16 | -0.008 | +0.005 |  | -0.4 / -0.4 |  |
| MES | 15 | h2 | +0.003 | -0.009 .. +0.015 | +0.0003 | 0.64 / 0.63 / 0.65 | 0.656 |  |  | 9/16 | -0.006 | +0.012 |  | +0.5 / +0.5 |  |
| MES | 15 | h4 * | +0.008 | -0.010 .. +0.025 | -0.0001 | 0.39 / 0.37 / 0.41 | 0.412 | 1 | 1 | 10/16 | -0.009 | +0.024 | False | +0.9 / +0.9 | 0.026 |
| MES | 15 | h8 | -0.003 | -0.028 .. +0.021 | -0.0017 | 0.79 / 0.78 / 0.8 | 0.796 |  |  | 9/16 | -0.010 | +0.004 |  | -0.3 / -0.3 |  |
| MES | 15 | h16 | +0.003 | -0.029 .. +0.034 | -0.0001 | 0.88 / 0.87 / 0.88 | 0.876 |  |  | 8/16 | -0.020 | +0.025 |  | +0.2 / +0.2 |  |
| MES | 15 | eod | +0.003 | -0.043 .. +0.049 | +0.0005 | 0.9 / 0.91 / 0.93 | 0.926 |  |  | 9/16 | -0.013 | +0.019 |  | +0.1 / +0.1 |  |
| MES | 60 | h1 | +0.008 | -0.008 .. +0.024 | +0.0021 | 0.32 / 0.35 / 0.34 | 0.341 |  |  | 11/16 | +0.005 | +0.012 |  | +1.0 / +1.0 |  |
| MES | 60 | h2 | +0.013 | -0.008 .. +0.035 | +0.0041 | 0.23 / 0.25 / 0.28 | 0.282 |  |  | 12/16 | +0.022 | +0.005 |  | +1.1 / +1.2 |  |
| MES | 60 | h4 | +0.014 | -0.015 .. +0.043 | +0.0009 | 0.35 / 0.37 / 0.44 | 0.446 |  |  | 11/16 | +0.009 | +0.019 |  | +0.8 / +0.9 | 0.050 |
| MES | 60 | h8 | +0.014 | -0.029 .. +0.058 | +0.0002 | 0.52 / 0.54 / 0.56 | 0.566 |  |  | 10/16 | +0.032 | -0.003 |  | +0.6 / +0.6 |  |
| MES | 60 | h16 | +0.044 | -0.013 .. +0.102 | +0.0018 | 0.13 / 0.13 / 0.17 | 0.166 |  |  | 10/16 | +0.074 | +0.015 |  | +1.5 / +1.5 |  |
| MES | 60 | eod * | +0.058 | +0.001 .. +0.115 | +0.0029 | 0.047 / 0.046 / 0.082 | 0.0839 | 1 | 0.999 | 11/16 | +0.085 | +0.031 | False | +1.8 / +2.0 |  |
| MNQ | 5 | h1 | +0.002 | -0.003 .. +0.007 | +0.0010 | 0.43 / 0.43 / 0.45 | 0.453 |  |  | 9/16 | -0.004 | +0.008 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h2 | +0.000 | -0.007 .. +0.007 | -0.0004 | 0.98 / 0.98 / 0.95 | 0.942 |  |  | 9/16 | -0.011 | +0.011 |  | +0.0 / +0.0 |  |
| MNQ | 5 | h4 | +0.005 | -0.004 .. +0.014 | +0.0009 | 0.27 / 0.28 / 0.44 | 0.426 |  |  | 12/16 | -0.002 | +0.012 |  | +1.0 / +1.1 | 0.019 |
| MNQ | 5 | h8 | +0.004 | -0.009 .. +0.016 | +0.0006 | 0.56 / 0.57 / 0.7 | 0.693 |  |  | 12/16 | -0.003 | +0.010 |  | +0.5 / +0.6 |  |
| MNQ | 5 | h16 | -0.013 | -0.031 .. +0.005 | -0.0003 | 0.14 / 0.15 / 0.3 | 0.292 |  |  | 9/16 | -0.024 | -0.003 |  | -1.3 / -1.5 |  |
| MNQ | 5 | eod * | +0.046 | -0.007 .. +0.098 | +0.0014 | 0.087 / 0.084 / 0.22 | 0.214 | 1 | 1 | 9/16 | +0.030 | +0.061 | False | +1.1 / +1.7 |  |
| MNQ | 15 | h1 * | +0.007 | -0.001 .. +0.015 | +0.0026 | 0.084 / 0.08 / 0.2 | 0.201 | 1 | 1 | 13/16 | +0.000 | +0.014 | False | +1.6 / +1.7 |  |
| MNQ | 15 | h2 | +0.006 | -0.007 .. +0.018 | +0.0016 | 0.38 / 0.36 / 0.52 | 0.516 |  |  | 8/16 | -0.003 | +0.015 |  | +0.9 / +0.9 |  |
| MNQ | 15 | h4 | -0.003 | -0.022 .. +0.016 | -0.0008 | 0.74 / 0.72 / 0.82 | 0.816 |  |  | 7/16 | -0.005 | -0.001 |  | -0.3 / -0.3 | 0.033 |
| MNQ | 15 | h8 | -0.019 | -0.048 .. +0.011 | -0.0019 | 0.22 / 0.19 / 0.34 | 0.334 |  |  | 13/16 | -0.015 | -0.022 |  | -1.3 / -1.2 |  |
| MNQ | 15 | h16 | -0.011 | -0.046 .. +0.023 | -0.0004 | 0.51 / 0.49 / 0.6 | 0.61 |  |  | 9/16 | -0.022 | -0.001 |  | -0.6 / -0.7 |  |
| MNQ | 15 | eod | +0.036 | -0.013 .. +0.084 | +0.0012 | 0.15 / 0.14 / 0.44 | 0.428 |  |  | 13/16 | -0.021 | +0.091 |  | +0.9 / +1.4 |  |
| MNQ | 60 | h1 | +0.009 | -0.007 .. +0.026 | +0.0028 | 0.26 / 0.29 / 0.32 | 0.322 |  |  | 11/16 | +0.018 | +0.001 |  | +1.0 / +1.1 |  |
| MNQ | 60 | h2 | +0.027 | +0.002 .. +0.052 | +0.0073 | 0.035 / 0.037 / 0.051 | 0.0505 |  |  | 12/16 | +0.034 | +0.020 |  | +2.1 / +2.1 |  |
| MNQ | 60 | h4 | +0.024 | -0.012 .. +0.059 | +0.0035 | 0.19 / 0.18 / 0.21 | 0.212 |  |  | 11/16 | +0.010 | +0.038 |  | +1.3 / +1.3 | 0.054 |
| MNQ | 60 | h8 | +0.045 | -0.004 .. +0.094 | +0.0047 | 0.073 / 0.079 / 0.087 | 0.086 |  |  | 9/16 | +0.034 | +0.056 |  | +1.8 / +1.8 |  |
| MNQ | 60 | h16 | +0.063 | +0.002 .. +0.125 | +0.0060 | 0.043 / 0.04 / 0.061 | 0.0646 |  |  | 10/16 | +0.067 | +0.060 |  | +2.0 / +2.0 |  |
| MNQ | 60 | eod * | +0.078 | +0.017 .. +0.138 | +0.0072 | 0.012 / 0.011 / 0.024 | 0.0247 | 1 | 0.892 | 11/16 | +0.080 | +0.076 | False | +2.4 / +2.5 |  |
| MYM | 5 | h1 * | +0.007 | -0.002 .. +0.016 | +0.0038 | 0.13 / 0.15 / 0.098 | 0.0985 | 1 | 1 | 4/8 | n/a | +0.007 | False | +1.6 / +1.5 |  |
| MYM | 5 | h2 | +0.008 | -0.002 .. +0.018 | +0.0014 | 0.1 / 0.12 / 0.24 | 0.247 |  |  | 6/8 | n/a | +0.008 |  | +1.7 / +1.6 |  |
| MYM | 5 | h4 | +0.009 | -0.005 .. +0.023 | +0.0022 | 0.19 / 0.21 / 0.42 | 0.408 |  |  | 4/8 | n/a | +0.009 |  | +1.3 / +1.3 | 0.025 |
| MYM | 5 | h8 | +0.004 | -0.015 .. +0.023 | +0.0016 | 0.69 / 0.69 / 0.78 | 0.769 |  |  | 6/8 | n/a | +0.004 |  | +0.4 / +0.4 |  |
| MYM | 5 | h16 | +0.012 | -0.013 .. +0.037 | +0.0017 | 0.35 / 0.35 / 0.5 | 0.488 |  |  | 5/8 | n/a | +0.012 |  | +0.9 / +0.9 |  |
| MYM | 5 | eod | +0.009 | -0.055 .. +0.074 | +0.0012 | 0.78 / 0.77 / 0.85 | 0.852 |  |  | 5/8 | n/a | +0.009 |  | +0.2 / +0.3 |  |
| MYM | 15 | h1 * | +0.013 | -0.001 .. +0.026 | +0.0055 | 0.061 / 0.058 / 0.096 | 0.0985 | 1 | 1 | 6/8 | n/a | +0.013 | False | +1.8 / +1.9 |  |
| MYM | 15 | h2 | +0.009 | -0.012 .. +0.030 | +0.0013 | 0.4 / 0.42 / 0.51 | 0.504 |  |  | 6/8 | n/a | +0.009 |  | +0.8 / +0.8 |  |
| MYM | 15 | h4 | +0.019 | -0.004 .. +0.043 | +0.0010 | 0.1 / 0.12 / 0.38 | 0.379 |  |  | 6/8 | n/a | +0.019 |  | +1.5 / +1.6 | 0.044 |
| MYM | 15 | h8 | -0.001 | -0.036 .. +0.033 | -0.0007 | 0.93 / 0.93 / 0.95 | 0.947 |  |  | 6/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 15 | h16 | -0.010 | -0.055 .. +0.036 | +0.0002 | 0.67 / 0.67 / 0.77 | 0.771 |  |  | 5/8 | n/a | -0.010 |  | -0.4 / -0.4 |  |
| MYM | 15 | eod | +0.011 | -0.057 .. +0.080 | +0.0011 | 0.75 / 0.76 / 0.86 | 0.854 |  |  | 4/8 | n/a | +0.011 |  | +0.2 / +0.3 |  |
| MYM | 60 | h1 | +0.003 | -0.020 .. +0.026 | -0.0009 | 0.8 / 0.81 / 0.83 | 0.829 |  |  | 3/8 | n/a | +0.003 |  | +0.2 / +0.3 |  |
| MYM | 60 | h2 | -0.004 | -0.035 .. +0.028 | -0.0045 | 0.82 / 0.83 / 0.85 | 0.845 |  |  | 5/8 | n/a | -0.004 |  | -0.2 / -0.2 |  |
| MYM | 60 | h4 * | +0.009 | -0.036 .. +0.053 | +0.0004 | 0.7 / 0.71 / 0.74 | 0.734 | 1 | 1 | 6/8 | n/a | +0.009 | False | +0.4 / +0.4 | 0.074 |
| MYM | 60 | h8 | -0.004 | -0.068 .. +0.061 | -0.0021 | 0.91 / 0.91 / 0.92 | 0.922 |  |  | 4/8 | n/a | -0.004 |  | -0.1 / -0.1 |  |
| MYM | 60 | h16 | -0.001 | -0.081 .. +0.080 | -0.0017 | 0.99 / 0.99 / 0.98 | 0.984 |  |  | 4/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MYM | 60 | eod | -0.000 | -0.078 .. +0.077 | -0.0018 | 1 / 1 / 0.99 | 0.988 |  |  | 3/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.015 | -0.019 .. -0.012 | -3.1% | -0.027 | 1.7e-16 | 7.31e-14 | 13/16 |
| MES | 5 | h2 | -0.016 | -0.021 .. -0.011 | -2.3% | -0.033 | 1.7e-10 |  | 12/16 |
| MES | 5 | h4 | -0.014 | -0.021 .. -0.008 | -1.4% | -0.037 | 2.6e-05 |  | 10/16 |
| MES | 5 | h8 | -0.019 | -0.027 .. -0.010 | -1.3% | -0.044 | 0.00022 |  | 12/16 |
| MES | 5 | h16 | -0.026 | -0.038 .. -0.013 | -1.2% | -0.054 | 4.4e-05 |  | 12/16 |
| MES | 5 | eod | -0.029 | -0.060 .. +0.003 | -0.3% | -0.073 | 0.12 |  | 12/16 |
| MES | 15 | h1 * | -0.022 | -0.029 .. -0.015 | -4.3% | -0.048 | 2.1e-10 | 6.9e-08 | 12/16 |
| MES | 15 | h2 | -0.031 | -0.040 .. -0.022 | -4.3% | -0.062 | 2.1e-09 |  | 13/16 |
| MES | 15 | h4 | -0.031 | -0.044 .. -0.019 | -3.0% | -0.071 | 7.2e-06 |  | 13/16 |
| MES | 15 | h8 | -0.041 | -0.058 .. -0.024 | -2.6% | -0.089 | 2.7e-05 |  | 15/16 |
| MES | 15 | h16 | -0.039 | -0.060 .. -0.017 | -1.7% | -0.107 | 0.0067 |  | 14/16 |
| MES | 15 | eod | -0.071 | -0.103 .. -0.038 | -1.3% | -0.139 | 0.0072 |  | 13/16 |
| MES | 60 | h1 * | -0.022 | -0.034 .. -0.010 | -4.2% | -0.049 | 0.00047 | 0.085 | 12/16 |
| MES | 60 | h2 | -0.022 | -0.039 .. -0.004 | -2.9% | -0.060 | 0.015 |  | 12/16 |
| MES | 60 | h4 | -0.032 | -0.056 .. -0.009 | -3.1% | -0.071 | 0.0078 |  | 11/16 |
| MES | 60 | h8 | -0.049 | -0.081 .. -0.017 | -3.2% | -0.088 | 0.0026 |  | 11/16 |
| MES | 60 | h16 | -0.019 | -0.055 .. +0.018 | -0.9% | -0.064 | 0.32 |  | 9/16 |
| MES | 60 | eod | -0.026 | -0.066 .. +0.015 | -1.2% | -0.070 | 0.21 |  | 12/16 |
| MNQ | 5 | h1 * | -0.019 | -0.024 .. -0.015 | -3.6% | -0.035 | 7.3e-17 | 3.32e-14 | 16/16 |
| MNQ | 5 | h2 | -0.020 | -0.025 .. -0.014 | -2.6% | -0.042 | 2.7e-06 |  | 12/16 |
| MNQ | 5 | h4 | -0.020 | -0.028 .. -0.013 | -1.8% | -0.050 | 0.0015 |  | 11/16 |
| MNQ | 5 | h8 | -0.034 | -0.043 .. -0.024 | -2.1% | -0.066 | 0.00029 |  | 15/16 |
| MNQ | 5 | h16 | -0.030 | -0.044 .. -0.016 | -1.2% | -0.072 | 0.0073 |  | 13/16 |
| MNQ | 5 | eod | -0.050 | -0.085 .. -0.016 | -0.4% | -0.092 | 0.085 |  | 11/16 |
| MNQ | 15 | h1 * | -0.027 | -0.033 .. -0.020 | -5.0% | -0.061 | 5.1e-12 | 1.82e-09 | 13/16 |
| MNQ | 15 | h2 | -0.034 | -0.043 .. -0.025 | -4.5% | -0.072 | 1e-06 |  | 16/16 |
| MNQ | 15 | h4 | -0.039 | -0.054 .. -0.024 | -3.4% | -0.085 | 0.0053 |  | 11/16 |
| MNQ | 15 | h8 | -0.052 | -0.073 .. -0.031 | -3.1% | -0.111 | 0.0011 |  | 15/16 |
| MNQ | 15 | h16 | -0.044 | -0.067 .. -0.021 | -1.7% | -0.118 | 0.003 |  | 14/16 |
| MNQ | 15 | eod | -0.059 | -0.096 .. -0.022 | -0.9% | -0.131 | 0.12 |  | 13/16 |
| MNQ | 60 | h1 * | -0.026 | -0.040 .. -0.013 | -5.0% | -0.055 | 9.5e-05 | 0.0196 | 12/16 |
| MNQ | 60 | h2 | -0.026 | -0.045 .. -0.008 | -3.4% | -0.066 | 0.0052 |  | 13/16 |
| MNQ | 60 | h4 | -0.032 | -0.055 .. -0.009 | -2.9% | -0.071 | 0.017 |  | 14/16 |
| MNQ | 60 | h8 | -0.034 | -0.066 .. -0.003 | -2.2% | -0.069 | 0.035 |  | 10/16 |
| MNQ | 60 | h16 | -0.032 | -0.071 .. +0.007 | -1.5% | -0.068 | 0.15 |  | 10/16 |
| MNQ | 60 | eod | -0.028 | -0.069 .. +0.012 | -1.2% | -0.070 | 0.21 |  | 11/16 |
| MYM | 5 | h1 * | -0.019 | -0.027 .. -0.012 | -3.6% | -0.034 | 3.6e-06 | 0.000873 | 8/8 |
| MYM | 5 | h2 | -0.019 | -0.026 .. -0.012 | -2.5% | -0.043 | 0.0075 |  | 8/8 |
| MYM | 5 | h4 | -0.019 | -0.030 .. -0.007 | -1.7% | -0.046 | 0.11 |  | 6/8 |
| MYM | 5 | h8 | -0.019 | -0.032 .. -0.007 | -1.2% | -0.046 | 0.09 |  | 6/8 |
| MYM | 5 | h16 | -0.028 | -0.047 .. -0.008 | -1.2% | -0.062 | 0.073 |  | 6/8 |
| MYM | 5 | eod | -0.034 | -0.076 .. +0.008 | -0.3% | -0.069 | 0.4 |  | 6/8 |
| MYM | 15 | h1 * | -0.027 | -0.038 .. -0.016 | -5.1% | -0.060 | 4.2e-05 | 0.00909 | 7/8 |
| MYM | 15 | h2 | -0.031 | -0.044 .. -0.017 | -4.0% | -0.070 | 0.051 |  | 7/8 |
| MYM | 15 | h4 | -0.039 | -0.058 .. -0.020 | -3.5% | -0.086 | 0.081 |  | 7/8 |
| MYM | 15 | h8 | -0.050 | -0.075 .. -0.025 | -3.1% | -0.104 | 0.025 |  | 7/8 |
| MYM | 15 | h16 | -0.041 | -0.074 .. -0.008 | -1.7% | -0.122 | 0.28 |  | 6/8 |
| MYM | 15 | eod | -0.066 | -0.111 .. -0.022 | -1.1% | -0.150 | 0.32 |  | 7/8 |
| MYM | 60 | h1 | -0.024 | -0.042 .. -0.005 | -4.5% | -0.041 | 0.015 |  | 5/8 |
| MYM | 60 | h2 * | -0.032 | -0.056 .. -0.009 | -4.3% | -0.060 | 0.0059 | 0.841 | 6/8 |
| MYM | 60 | h4 | -0.046 | -0.081 .. -0.011 | -4.3% | -0.086 | 0.01 |  | 7/8 |
| MYM | 60 | h8 | -0.051 | -0.094 .. -0.008 | -3.3% | -0.099 | 0.021 |  | 6/8 |
| MYM | 60 | h16 | +0.006 | -0.051 .. +0.063 | +0.3% | -0.058 | 0.84 |  | 4/8 |
| MYM | 60 | eod | -0.015 | -0.075 .. +0.045 | -0.7% | -0.067 | 0.63 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.19 pts | -0.12 .. +0.50 | 0.23 |
| MES | 15 | +0.04 pts | -0.44 .. +0.53 | 0.86 |
| MES | 60 | +0.77 pts | -0.20 .. +1.74 | 0.15 |
| MNQ | 5 | +0.01 pts | -0.29 .. +0.32 | 0.93 |
| MNQ | 15 | +0.34 pts | -0.10 .. +0.79 | 0.16 |
| MNQ | 60 | +0.92 pts | -0.01 .. +1.85 | 0.061 |
| MYM | 5 | +0.17 pts | -0.24 .. +0.59 | 0.42 |
| MYM | 15 | +0.31 pts | -0.31 .. +0.93 | 0.32 |
| MYM | 60 | -0.11 pts | -1.48 .. +1.25 | 0.95 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | bottom fifth | long | 207255 | +0.011 | 0.233 | +0.12 | -3.38 | -3.41 | -3.36 | -3.48 |
| MES | 5 | h2 | bottom fifth | long | 207255 | +0.014 | 0.233 | +0.18 | -3.32 | -3.35 | -3.30 | -3.49 |
| MES | 5 | h4 | bottom fifth | long | 207255 | +0.020 | 0.233 | +0.26 | -3.24 | -3.32 | -3.17 | -3.43 |
| MES | 5 | h8 | top fifth | long | 207254 | +0.010 | 0.229 | +0.23 | -3.27 | -3.46 | -3.10 | -3.20 |
| MES | 5 | h16 | bottom fifth | long | 207255 | +0.052 | 0.233 | +0.71 | -2.79 | -3.02 | -2.58 | -3.16 |
| MES | 5 | eod | top fifth | long | 207254 | +0.428 | 0.229 | +6.22 | +2.72 | -0.11 | +5.23 | +4.26 |
| MES | 15 | h1 | bottom fifth | long | 68444 | +0.008 | 0.139 | +0.16 | -3.34 | -3.34 | -3.34 | -3.52 |
| MES | 15 | h2 | top fifth | long | 68444 | -0.001 | 0.136 | +0.08 | -3.42 | -3.47 | -3.38 | -3.33 |
| MES | 15 | h4 | top fifth | long | 68444 | +0.013 | 0.136 | +0.44 | -3.06 | -3.22 | -2.92 | -3.02 |
| MES | 15 | h8 | bottom fifth | long | 68444 | +0.038 | 0.139 | +0.88 | -2.62 | -2.83 | -2.44 | -3.03 |
| MES | 15 | h16 | top fifth | long | 68444 | +0.062 | 0.136 | +1.61 | -1.89 | -2.51 | -1.35 | -1.82 |
| MES | 15 | eod | top fifth | long | 68444 | +0.218 | 0.136 | +5.91 | +2.41 | +0.01 | +4.51 | +3.83 |
| MES | 60 | h1 | top fifth | long | 16683 | +0.009 | 0.072 | +0.08 | -3.42 | -2.99 | -3.78 | -3.58 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.016 | 0.072 | +0.43 | -3.07 | -2.67 | -3.42 | -3.35 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.032 | 0.072 | +1.23 | -2.27 | -2.52 | -2.06 | -2.92 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.066 | 0.072 | +2.84 | -0.66 | -0.81 | -0.53 | -1.93 |
| MES | 60 | h16 | top fifth | long | 16683 | +0.132 | 0.072 | +6.01 | +2.51 | +1.29 | +3.55 | +0.25 |
| MES | 60 | eod | top fifth | long | 16683 | +0.140 | 0.072 | +6.41 | +2.91 | +1.48 | +4.13 | +0.30 |
| MNQ | 5 | h1 | top fifth | long | 206905 | -0.002 | 0.088 | -0.04 | -2.04 | -2.03 | -2.04 | -1.97 |
| MNQ | 5 | h2 | top fifth | long | 206905 | -0.003 | 0.088 | -0.03 | -2.03 | -2.06 | -2.01 | -1.89 |
| MNQ | 5 | h4 | top fifth | long | 206905 | +0.006 | 0.088 | +0.13 | -1.87 | -1.99 | -1.78 | -1.73 |
| MNQ | 5 | h8 | top fifth | long | 206905 | +0.020 | 0.088 | +0.37 | -1.63 | -1.90 | -1.41 | -1.58 |
| MNQ | 5 | h16 | bottom fifth | long | 206905 | +0.045 | 0.089 | +0.77 | -1.23 | -1.62 | -0.92 | -1.33 |
| MNQ | 5 | eod | top fifth | long | 206905 | +0.426 | 0.088 | +7.85 | +5.85 | +0.84 | +9.78 | +11.96 |
| MNQ | 15 | h1 | top fifth | long | 68413 | +0.006 | 0.052 | +0.13 | -1.87 | -1.90 | -1.86 | -1.92 |
| MNQ | 15 | h2 | top fifth | long | 68413 | +0.011 | 0.052 | +0.35 | -1.65 | -1.84 | -1.51 | -1.75 |
| MNQ | 15 | h4 | bottom fifth | long | 68413 | +0.028 | 0.053 | +0.58 | -1.42 | -1.65 | -1.23 | -1.69 |
| MNQ | 15 | h8 | bottom fifth | long | 68413 | +0.050 | 0.053 | +1.39 | -0.61 | -1.35 | -0.03 | -1.08 |
| MNQ | 15 | h16 | bottom fifth | long | 68413 | +0.086 | 0.053 | +2.87 | +0.87 | -0.79 | +2.14 | +0.64 |
| MNQ | 15 | eod | top fifth | long | 68413 | +0.222 | 0.052 | +7.54 | +5.54 | +0.96 | +9.09 | +9.57 |
| MNQ | 60 | h1 | top fifth | long | 16682 | +0.014 | 0.028 | +0.39 | -1.61 | -1.38 | -1.78 | -1.81 |
| MNQ | 60 | h2 | top fifth | long | 16682 | +0.026 | 0.028 | +1.00 | -1.00 | -0.90 | -1.07 | -1.27 |
| MNQ | 60 | h4 | top fifth | long | 16682 | +0.042 | 0.028 | +2.26 | +0.26 | -0.65 | +0.94 | -0.30 |
| MNQ | 60 | h8 | top fifth | long | 16682 | +0.088 | 0.028 | +4.98 | +2.98 | +1.01 | +4.45 | +1.71 |
| MNQ | 60 | h16 | top fifth | long | 16682 | +0.141 | 0.028 | +8.53 | +6.53 | +2.47 | +9.56 | +4.64 |
| MNQ | 60 | eod | top fifth | long | 16682 | +0.148 | 0.028 | +8.85 | +6.85 | +2.55 | +10.06 | +4.64 |
| MYM | 5 | h1 | top fifth | long | 103808 | -0.004 | 0.119 | -0.03 | -2.03 | +nan | -2.03 | -1.94 |
| MYM | 5 | h2 | top fifth | long | 103808 | -0.004 | 0.119 | +0.02 | -1.98 | +nan | -1.98 | -1.86 |
| MYM | 5 | h4 | top fifth | long | 103808 | -0.001 | 0.119 | +0.13 | -1.87 | +nan | -1.87 | -1.69 |
| MYM | 5 | h8 | top fifth | long | 103808 | +0.003 | 0.119 | +0.29 | -1.71 | +nan | -1.71 | -1.54 |
| MYM | 5 | h16 | top fifth | long | 103808 | +0.013 | 0.119 | +0.59 | -1.41 | +nan | -1.41 | -1.32 |
| MYM | 5 | eod | top fifth | long | 103808 | +0.274 | 0.119 | +6.97 | +4.97 | +nan | +4.97 | +5.98 |
| MYM | 15 | h1 | top fifth | long | 34286 | -0.002 | 0.070 | +0.08 | -1.92 | +nan | -1.92 | -1.81 |
| MYM | 15 | h2 | top fifth | long | 34286 | -0.009 | 0.070 | +0.18 | -1.82 | +nan | -1.82 | -1.63 |
| MYM | 15 | h4 | top fifth | long | 34286 | +0.007 | 0.070 | +0.66 | -1.34 | +nan | -1.34 | -1.12 |
| MYM | 15 | h8 | bottom fifth | long | 34286 | +0.009 | 0.072 | +0.75 | -1.25 | +nan | -1.25 | -1.16 |
| MYM | 15 | h16 | bottom fifth | long | 34286 | +0.038 | 0.072 | +2.16 | +0.16 | +nan | +0.16 | +0.84 |
| MYM | 15 | eod | top fifth | long | 34286 | +0.142 | 0.070 | +7.00 | +5.00 | +nan | +5.00 | +8.02 |
| MYM | 60 | h1 | bottom fifth | short | 8331 | +0.009 | 0.039 | +0.01 | -1.99 | +nan | -1.99 | -1.92 |
| MYM | 60 | h2 | bottom fifth | long | 8331 | +0.002 | 0.039 | +0.63 | -1.37 | +nan | -1.37 | -1.77 |
| MYM | 60 | h4 | top fifth | long | 8331 | +0.004 | 0.037 | +0.74 | -1.26 | +nan | -1.26 | -1.52 |
| MYM | 60 | h8 | bottom fifth | long | 8331 | +0.038 | 0.039 | +3.37 | +1.37 | +nan | +1.37 | +0.02 |
| MYM | 60 | h16 | bottom fifth | long | 8331 | +0.062 | 0.039 | +5.01 | +3.01 | +nan | +3.01 | +1.28 |
| MYM | 60 | eod | bottom fifth | long | 8331 | +0.068 | 0.039 | +5.36 | +3.36 | +nan | +3.36 | +0.89 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.411 | -1.250 | -1.174 | -1.159 | -1.189 | +0.000 | -0.040 | -0.045 | -0.043 | -0.042 | -0.052 |
| MES | 15 | -0.575 | -1.331 | -1.254 | -1.231 | -1.237 | +0.000 | -0.015 | -0.013 | -0.011 | -0.026 | -0.021 |
| MES | 60 | -1.818 | -1.685 | -1.406 | -1.353 | -1.331 | +0.000 | +0.006 | +0.005 | +0.001 | -0.069 | +0.030 |
| MNQ | 5 | -0.429 | -1.336 | -1.252 | -1.231 | -1.239 | +0.000 | -0.012 | -0.018 | -0.010 | -0.003 | -0.017 |
| MNQ | 15 | -0.615 | -1.398 | -1.316 | -1.295 | -1.287 | +0.000 | +0.005 | +0.006 | -0.001 | -0.009 | -0.012 |
| MNQ | 60 | -1.985 | -1.758 | -1.454 | -1.419 | -1.392 | +0.000 | +0.009 | +0.020 | +0.007 | -0.032 | -0.005 |
| MYM | 5 | -0.419 | -1.316 | -1.236 | -1.219 | -1.223 | +0.000 | -0.005 | -0.007 | -0.009 | -0.015 | -0.016 |
| MYM | 15 | -0.596 | -1.392 | -1.310 | -1.274 | -1.276 | +0.000 | +0.011 | +0.007 | +0.024 | -0.000 | -0.007 |
| MYM | 60 | -1.879 | -1.715 | -1.454 | -1.420 | -1.397 | +0.000 | +0.006 | -0.005 | +0.007 | -0.048 | +0.019 |

## Calibration

- MES 5-min: 1036271 bars, 207254 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68444 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 206905 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68413 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16682 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103808 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34286 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8331 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
