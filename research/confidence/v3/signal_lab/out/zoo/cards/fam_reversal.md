# Impact card: fam_reversal

any reversal pattern, textbook direction (both sides) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.015 R20 over the next 16 bars (80 min), p=0.091; we would catch an effect of 0.008 R20 or more 80% of the time).
- MES 5-min size: the market moves 1% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.005 R20, possible, q=0.0612, 10 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.21 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.234 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.008 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.61 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.132 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.029 R20 over the next 16 bars (16 h), p=0.89; we would catch an effect of 0.032 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.25).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.58 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.064 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.011 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 1% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.006 R20, CONFIRMED, q=0.0141, 12 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.32 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.080 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.014 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.022 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.87).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.06 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.046 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.016 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.036 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.47 at recent bar sizes, 90% range up to $2.91); about 2.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.024 R20 over the next 16 bars (80 min), p=0.18; we would catch an effect of 0.019 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.15).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.34 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.173 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.030 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.68).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.60 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.099 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.035 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.46 at recent bar sizes, 90% range up to $3.88); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | +0.000 .. +0.006 | +0.0023 | 0.034 / 0.027 / 0.032 | 0.0339 |  |  | 12/16 | -0.002 | +0.008 |  | +2.2 / +2.1 |  |
| MES | 5 | h2 | +0.004 | +0.000 .. +0.007 | +0.0020 | 0.033 / 0.029 / 0.044 | 0.0485 |  |  | 10/16 | +0.000 | +0.007 |  | +2.0 / +2.1 |  |
| MES | 5 | h4 | +0.003 | -0.002 .. +0.008 | +0.0011 | 0.2 / 0.21 / 0.28 | 0.276 |  |  | 10/16 | +0.001 | +0.006 |  | +1.1 / +1.3 | 0.008 |
| MES | 5 | h8 | +0.008 | +0.001 .. +0.015 | +0.0021 | 0.018 / 0.019 / 0.043 | 0.0458 |  |  | 13/16 | +0.010 | +0.007 |  | +2.1 / +2.4 |  |
| MES | 5 | h16 * | +0.015 | +0.004 .. +0.027 | +0.0026 | 0.0084 / 0.0061 / 0.011 | 0.0125 | 1 | 0.866 | 11/16 | +0.017 | +0.014 | False | +2.6 / +2.6 |  |
| MES | 5 | eod | -0.015 | -0.081 .. +0.052 | -0.0005 | 0.67 / 0.67 / 0.69 | 0.677 |  |  | 9/16 | -0.074 | +0.044 |  | -0.5 / -0.4 |  |
| MES | 15 | h1 | -0.002 | -0.008 .. +0.003 | -0.0016 | 0.39 / 0.38 / 0.4 | 0.396 |  |  | 9/16 | -0.001 | -0.004 |  | -0.9 / -0.9 |  |
| MES | 15 | h2 | +0.005 | -0.002 .. +0.012 | +0.0020 | 0.2 / 0.2 / 0.27 | 0.277 |  |  | 11/16 | +0.003 | +0.006 |  | +1.1 / +1.3 |  |
| MES | 15 | h4 * | +0.008 | -0.003 .. +0.018 | +0.0022 | 0.16 / 0.15 / 0.22 | 0.22 | 1 | 1 | 11/16 | +0.008 | +0.007 | False | +1.3 / +1.4 | 0.017 |
| MES | 15 | h8 | +0.010 | -0.006 .. +0.026 | +0.0021 | 0.22 / 0.21 / 0.26 | 0.259 |  |  | 9/16 | +0.017 | +0.003 |  | +1.2 / +1.2 |  |
| MES | 15 | h16 | -0.003 | -0.026 .. +0.019 | -0.0005 | 0.77 / 0.78 / 0.79 | 0.783 |  |  | 7/16 | +0.024 | -0.031 |  | -0.3 / -0.3 |  |
| MES | 15 | eod | -0.033 | -0.090 .. +0.024 | -0.0018 | 0.26 / 0.27 / 0.33 | 0.336 |  |  | 13/16 | -0.021 | -0.044 |  | -1.1 / -1.1 |  |
| MES | 60 | h1 | +0.001 | -0.011 .. +0.013 | +0.0006 | 0.88 / 0.88 / 0.89 | 0.891 |  |  | 9/16 | -0.001 | +0.002 |  | +0.1 / +0.1 |  |
| MES | 60 | h2 | -0.007 | -0.024 .. +0.010 | -0.0030 | 0.44 / 0.45 / 0.43 | 0.425 |  |  | 11/16 | -0.008 | -0.006 |  | -0.7 / -0.8 |  |
| MES | 60 | h4 | -0.017 | -0.040 .. +0.005 | -0.0056 | 0.12 / 0.12 / 0.13 | 0.13 |  |  | 11/16 | -0.028 | -0.007 |  | -1.4 / -1.6 | 0.032 |
| MES | 60 | h8 | -0.021 | -0.052 .. +0.010 | -0.0048 | 0.19 / 0.19 / 0.18 | 0.184 |  |  | 10/16 | -0.027 | -0.015 |  | -1.2 / -1.3 |  |
| MES | 60 | h16 * | -0.029 | -0.069 .. +0.010 | -0.0052 | 0.15 / 0.14 / 0.14 | 0.147 | 1 | 1 | 9/16 | -0.035 | -0.023 | False | -1.4 / -1.4 |  |
| MES | 60 | eod | -0.023 | -0.064 .. +0.018 | -0.0040 | 0.26 / 0.26 / 0.26 | 0.253 |  |  | 9/16 | -0.036 | -0.011 |  | -1.1 / -1.1 |  |
| MNQ | 5 | h1 * | +0.001 | -0.002 .. +0.004 | +0.0007 | 0.47 / 0.46 / 0.56 | 0.559 | 1 | 1 | 9/16 | +0.002 | +0.001 | False | +0.7 / +0.7 |  |
| MNQ | 5 | h2 | -0.002 | -0.006 .. +0.003 | -0.0006 | 0.49 / 0.48 / 0.59 | 0.582 |  |  | 8/16 | -0.001 | -0.002 |  | -0.7 / -0.7 |  |
| MNQ | 5 | h4 | -0.003 | -0.010 .. +0.003 | -0.0008 | 0.28 / 0.26 / 0.44 | 0.443 |  |  | 10/16 | +0.002 | -0.009 |  | -1.0 / -1.1 | 0.011 |
| MNQ | 5 | h8 | -0.004 | -0.013 .. +0.005 | -0.0006 | 0.38 / 0.36 / 0.54 | 0.55 |  |  | 11/16 | +0.004 | -0.012 |  | -0.8 / -0.9 |  |
| MNQ | 5 | h16 | +0.003 | -0.011 .. +0.017 | +0.0003 | 0.67 / 0.65 / 0.75 | 0.756 |  |  | 10/16 | +0.014 | -0.008 |  | +0.4 / +0.4 |  |
| MNQ | 5 | eod | +0.034 | -0.057 .. +0.125 | +0.0008 | 0.46 / 0.46 / 0.48 | 0.479 |  |  | 7/16 | -0.023 | +0.091 |  | +0.8 / +0.7 |  |
| MNQ | 15 | h1 | +0.001 | -0.006 .. +0.007 | +0.0002 | 0.88 / 0.88 / 0.9 | 0.899 |  |  | 8/16 | -0.005 | +0.006 |  | +0.2 / +0.2 |  |
| MNQ | 15 | h2 | +0.008 | -0.001 .. +0.017 | +0.0024 | 0.089 / 0.087 / 0.2 | 0.188 |  |  | 10/16 | +0.006 | +0.011 |  | +1.8 / +1.7 |  |
| MNQ | 15 | h4 | +0.010 | -0.003 .. +0.022 | +0.0017 | 0.14 / 0.13 / 0.36 | 0.351 |  |  | 9/16 | +0.007 | +0.013 |  | +1.4 / +1.5 | 0.022 |
| MNQ | 15 | h8 | +0.009 | -0.009 .. +0.027 | +0.0013 | 0.31 / 0.29 / 0.49 | 0.49 |  |  | 12/16 | +0.010 | +0.009 |  | +1.0 / +1.0 |  |
| MNQ | 15 | h16 * | +0.014 | -0.012 .. +0.041 | +0.0016 | 0.29 / 0.3 / 0.39 | 0.391 | 1 | 1 | 10/16 | +0.037 | -0.009 | False | +1.0 / +1.1 |  |
| MNQ | 15 | eod | -0.028 | -0.101 .. +0.045 | -0.0011 | 0.45 / 0.44 / 0.55 | 0.543 |  |  | 9/16 | +0.022 | -0.079 |  | -0.8 / -0.8 |  |
| MNQ | 60 | h1 | +0.002 | -0.010 .. +0.015 | +0.0013 | 0.73 / 0.73 / 0.75 | 0.75 |  |  | 10/16 | +0.005 | -0.001 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h2 | +0.003 | -0.015 .. +0.020 | +0.0011 | 0.78 / 0.77 / 0.78 | 0.779 |  |  | 10/16 | +0.008 | -0.003 |  | +0.3 / +0.3 |  |
| MNQ | 60 | h4 | +0.000 | -0.024 .. +0.024 | +0.0001 | 0.99 / 0.99 / 0.99 | 0.99 |  |  | 7/16 | -0.000 | +0.001 |  | +0.0 / +0.0 | 0.036 |
| MNQ | 60 | h8 | -0.004 | -0.038 .. +0.029 | -0.0009 | 0.81 / 0.81 / 0.81 | 0.803 |  |  | 6/16 | -0.023 | +0.015 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h16 * | -0.016 | -0.059 .. +0.027 | -0.0027 | 0.46 / 0.46 / 0.46 | 0.45 | 1 | 1 | 9/16 | -0.032 | -0.000 | False | -0.7 / -0.7 |  |
| MNQ | 60 | eod | -0.016 | -0.061 .. +0.029 | -0.0025 | 0.48 / 0.49 / 0.49 | 0.479 |  |  | 9/16 | -0.033 | +0.001 |  | -0.7 / -0.7 |  |
| MYM | 5 | h1 | +0.006 | +0.001 .. +0.010 | +0.0030 | 0.013 / 0.012 / 0.05 | 0.0501 |  |  | 5/8 | n/a | +0.006 |  | +2.5 / +2.5 |  |
| MYM | 5 | h2 | +0.007 | +0.001 .. +0.014 | +0.0023 | 0.028 / 0.02 / 0.12 | 0.12 |  |  | 6/8 | n/a | +0.007 |  | +2.2 / +2.2 |  |
| MYM | 5 | h4 | +0.012 | +0.003 .. +0.022 | +0.0024 | 0.0091 / 0.006 / 0.11 | 0.111 |  |  | 6/8 | n/a | +0.012 |  | +2.6 / +2.6 | 0.019 |
| MYM | 5 | h8 | +0.018 | +0.004 .. +0.032 | +0.0025 | 0.012 / 0.0068 / 0.094 | 0.0933 |  |  | 5/8 | n/a | +0.018 |  | +2.5 / +2.5 |  |
| MYM | 5 | h16 * | +0.024 | +0.004 .. +0.045 | +0.0027 | 0.022 / 0.018 / 0.078 | 0.0796 | 1 | 0.836 | 6/8 | n/a | +0.024 | False | +2.3 / +2.3 |  |
| MYM | 5 | eod | +0.064 | -0.045 .. +0.173 | +0.0016 | 0.25 / 0.26 / 0.32 | 0.319 |  |  | 5/8 | n/a | +0.064 |  | +1.1 / +1.2 |  |
| MYM | 15 | h1 * | -0.007 | -0.016 .. +0.001 | -0.0038 | 0.096 / 0.093 / 0.16 | 0.166 | 1 | 1 | 6/8 | n/a | -0.007 | False | -1.7 / -1.7 |  |
| MYM | 15 | h2 | -0.008 | -0.019 .. +0.004 | -0.0023 | 0.18 / 0.18 / 0.38 | 0.384 |  |  | 6/8 | n/a | -0.008 |  | -1.3 / -1.3 |  |
| MYM | 15 | h4 | -0.003 | -0.019 .. +0.013 | -0.0005 | 0.72 / 0.72 / 0.85 | 0.834 |  |  | 4/8 | n/a | -0.003 |  | -0.3 / -0.4 | 0.030 |
| MYM | 15 | h8 | +0.007 | -0.016 .. +0.031 | +0.0010 | 0.54 / 0.54 / 0.71 | 0.694 |  |  | 7/8 | n/a | +0.007 |  | +0.6 / +0.6 |  |
| MYM | 15 | h16 | +0.000 | -0.033 .. +0.033 | +0.0000 | 1 / 1 / 1 | 0.999 |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 15 | eod | +0.011 | -0.083 .. +0.105 | +0.0005 | 0.82 / 0.82 / 0.87 | 0.855 |  |  | 4/8 | n/a | +0.011 |  | +0.2 / +0.2 |  |
| MYM | 60 | h1 | +0.009 | -0.009 .. +0.027 | +0.0053 | 0.34 / 0.35 / 0.33 | 0.324 |  |  | 4/8 | n/a | +0.009 |  | +0.9 / +1.0 |  |
| MYM | 60 | h2 | +0.005 | -0.021 .. +0.030 | +0.0019 | 0.73 / 0.73 / 0.72 | 0.727 |  |  | 3/8 | n/a | +0.005 |  | +0.3 / +0.3 |  |
| MYM | 60 | h4 | +0.015 | -0.021 .. +0.050 | +0.0044 | 0.42 / 0.41 / 0.39 | 0.386 |  |  | 5/8 | n/a | +0.015 |  | +0.8 / +0.8 | 0.048 |
| MYM | 60 | h8 * | +0.035 | -0.016 .. +0.086 | +0.0078 | 0.18 / 0.15 / 0.13 | 0.124 | 1 | 1 | 4/8 | n/a | +0.035 | False | +1.4 / +1.4 |  |
| MYM | 60 | h16 | +0.035 | -0.024 .. +0.093 | +0.0059 | 0.25 / 0.24 / 0.24 | 0.249 |  |  | 6/8 | n/a | +0.035 |  | +1.1 / +1.2 |  |
| MYM | 60 | eod | +0.036 | -0.025 .. +0.097 | +0.0059 | 0.25 / 0.23 / 0.24 | 0.246 |  |  | 6/8 | n/a | +0.036 |  | +1.1 / +1.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.005 | -0.008 .. -0.003 | -1.1% | -0.012 | 0.00033 | 0.0612 | 10/16 |
| MES | 5 | h2 | -0.005 | -0.008 .. -0.001 | -0.7% | -0.014 | 0.032 |  | 11/16 |
| MES | 5 | h4 | -0.007 | -0.012 .. -0.001 | -0.7% | -0.016 | 0.087 |  | 10/16 |
| MES | 5 | h8 | -0.008 | -0.018 .. +0.002 | -0.5% | -0.024 | 0.19 |  | 8/16 |
| MES | 5 | h16 | -0.013 | -0.028 .. +0.003 | -0.6% | -0.041 | 0.12 |  | 8/16 |
| MES | 5 | eod | -0.154 | -0.308 .. -0.000 | -1.5% | -0.219 | 0.05 |  | 10/16 |
| MES | 15 | h1 | +0.000 | -0.004 .. +0.004 | +0.0% | -0.000 | 0.98 |  | 7/16 |
| MES | 15 | h2 | +0.001 | -0.006 .. +0.009 | +0.2% | +0.000 | 0.77 |  | 10/16 |
| MES | 15 | h4 | +0.000 | -0.012 .. +0.012 | +0.0% | -0.007 | 0.96 |  | 7/16 |
| MES | 15 | h8 | +0.001 | -0.018 .. +0.020 | +0.1% | -0.026 | 0.92 |  | 9/16 |
| MES | 15 | h16 | -0.008 | -0.037 .. +0.022 | -0.3% | -0.054 | 0.61 |  | 7/16 |
| MES | 15 | eod * | -0.082 | -0.214 .. +0.051 | -1.5% | -0.118 | 0.23 | 1 | 8/16 |
| MES | 60 | h1 | +0.009 | -0.000 .. +0.018 | +1.7% | +0.020 | 0.13 |  | 11/16 |
| MES | 60 | h2 * | +0.015 | +0.001 .. +0.029 | +2.0% | +0.026 | 0.042 | 1 | 11/16 |
| MES | 60 | h4 | +0.007 | -0.013 .. +0.026 | +0.6% | +0.027 | 0.7 |  | 11/16 |
| MES | 60 | h8 | +0.002 | -0.023 .. +0.028 | +0.1% | +0.024 | 0.98 |  | 9/16 |
| MES | 60 | h16 | -0.012 | -0.043 .. +0.019 | -0.6% | +0.014 | 0.46 |  | 7/16 |
| MES | 60 | eod | -0.013 | -0.045 .. +0.019 | -0.6% | +0.017 | 0.45 |  | 8/16 |
| MNQ | 5 | h1 * | -0.006 | -0.009 .. -0.003 | -1.2% | -0.010 | 6.7e-05 | 0.0141 | 12/16 |
| MNQ | 5 | h2 | -0.006 | -0.012 .. -0.000 | -0.8% | -0.010 | 0.047 |  | 12/16 |
| MNQ | 5 | h4 | -0.010 | -0.022 .. +0.002 | -0.9% | -0.018 | 0.095 |  | 9/16 |
| MNQ | 5 | h8 | -0.022 | -0.047 .. +0.002 | -1.4% | -0.043 | 0.078 |  | 11/16 |
| MNQ | 5 | h16 | -0.036 | -0.081 .. +0.009 | -1.5% | -0.093 | 0.12 |  | 11/16 |
| MNQ | 5 | eod | -0.247 | -0.490 .. -0.005 | -2.0% | -0.436 | 0.046 |  | 12/16 |
| MNQ | 15 | h1 | -0.002 | -0.007 .. +0.004 | -0.3% | -0.003 | 0.6 |  | 9/16 |
| MNQ | 15 | h2 | -0.004 | -0.017 .. +0.010 | -0.5% | -0.009 | 0.59 |  | 10/16 |
| MNQ | 15 | h4 | -0.017 | -0.047 .. +0.014 | -1.5% | -0.027 | 0.28 |  | 10/16 |
| MNQ | 15 | h8 | -0.035 | -0.082 .. +0.013 | -2.1% | -0.085 | 0.15 |  | 10/16 |
| MNQ | 15 | h16 * | -0.040 | -0.093 .. +0.014 | -1.6% | -0.162 | 0.14 | 1 | 10/16 |
| MNQ | 15 | eod | -0.131 | -0.351 .. +0.089 | -2.1% | -0.251 | 0.24 |  | 11/16 |
| MNQ | 60 | h1 * | +0.006 | -0.004 .. +0.015 | +1.1% | +0.020 | 0.28 | 1 | 9/16 |
| MNQ | 60 | h2 | +0.003 | -0.010 .. +0.017 | +0.4% | +0.012 | 0.66 |  | 9/16 |
| MNQ | 60 | h4 | -0.001 | -0.021 .. +0.019 | -0.1% | +0.022 | 0.92 |  | 8/16 |
| MNQ | 60 | h8 | -0.008 | -0.034 .. +0.019 | -0.5% | +0.017 | 0.59 |  | 7/16 |
| MNQ | 60 | h16 | -0.010 | -0.042 .. +0.022 | -0.5% | +0.017 | 0.55 |  | 9/16 |
| MNQ | 60 | eod | -0.013 | -0.045 .. +0.019 | -0.5% | +0.014 | 0.46 |  | 8/16 |
| MYM | 5 | h1 | -0.005 | -0.010 .. -0.001 | -1.0% | -0.011 | 0.14 |  | 6/8 |
| MYM | 5 | h2 * | -0.011 | -0.020 .. -0.001 | -1.4% | -0.019 | 0.025 | 1 | 5/8 |
| MYM | 5 | h4 | -0.019 | -0.040 .. +0.002 | -1.7% | -0.032 | 0.08 |  | 5/8 |
| MYM | 5 | h8 | -0.025 | -0.064 .. +0.015 | -1.6% | -0.053 | 0.22 |  | 5/8 |
| MYM | 5 | h16 | -0.045 | -0.100 .. +0.010 | -1.9% | -0.105 | 0.11 |  | 7/8 |
| MYM | 5 | eod | -0.139 | -0.409 .. +0.131 | -1.2% | -0.257 | 0.31 |  | 3/8 |
| MYM | 15 | h1 | -0.003 | -0.010 .. +0.005 | -0.5% | -0.006 | 0.5 |  | 4/8 |
| MYM | 15 | h2 * | -0.014 | -0.030 .. +0.002 | -1.8% | -0.018 | 0.11 | 1 | 5/8 |
| MYM | 15 | h4 | -0.018 | -0.054 .. +0.017 | -1.6% | -0.037 | 0.31 |  | 4/8 |
| MYM | 15 | h8 | -0.032 | -0.086 .. +0.023 | -1.9% | -0.092 | 0.25 |  | 5/8 |
| MYM | 15 | h16 | -0.073 | -0.169 .. +0.024 | -2.9% | -0.181 | 0.14 |  | 6/8 |
| MYM | 15 | eod | -0.180 | -0.442 .. +0.083 | -3.0% | -0.245 | 0.18 |  | 6/8 |
| MYM | 60 | h1 | +0.006 | -0.008 .. +0.020 | +1.1% | +0.008 | 0.47 |  | 3/8 |
| MYM | 60 | h2 | +0.008 | -0.013 .. +0.028 | +1.0% | +0.014 | 0.47 |  | 4/8 |
| MYM | 60 | h4 | +0.008 | -0.021 .. +0.037 | +0.7% | +0.025 | 0.67 |  | 4/8 |
| MYM | 60 | h8 | +0.018 | -0.025 .. +0.062 | +1.2% | +0.043 | 0.55 |  | 3/8 |
| MYM | 60 | h16 | -0.015 | -0.062 .. +0.032 | -0.7% | +0.032 | 0.54 |  | 6/8 |
| MYM | 60 | eod * | -0.020 | -0.067 .. +0.027 | -0.9% | +0.027 | 0.4 | 1 | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.24 pts | +0.05 .. +0.42 | 0.014 |
| MES | 15 | +0.27 pts | -0.06 .. +0.60 | 0.11 |
| MES | 60 | +0.30 pts | -0.34 .. +0.94 | 0.43 |
| MNQ | 5 | +0.24 pts | +0.04 .. +0.43 | 0.019 |
| MNQ | 15 | +0.41 pts | +0.08 .. +0.74 | 0.016 |
| MNQ | 60 | +0.49 pts | -0.15 .. +1.13 | 0.26 |
| MYM | 5 | +0.68 pts | +0.40 .. +0.96 | 1.5e-06 |
| MYM | 15 | -0.08 pts | -0.57 .. +0.41 | 0.94 |
| MYM | 60 | +0.24 pts | -0.77 .. +1.24 | 0.64 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 263276 | -0.004 | 0.368 | +0.01 | -3.49 | -3.54 | -3.44 | -3.41 |
| MES | 5 | h2 | event | with signal | 263276 | -0.006 | 0.368 | -0.05 | -3.55 | -3.55 | -3.55 | -3.43 |
| MES | 5 | h4 | event | with signal | 263276 | -0.008 | 0.368 | -0.06 | -3.56 | -3.55 | -3.58 | -3.44 |
| MES | 5 | h8 | event | with signal | 263276 | -0.001 | 0.368 | -0.04 | -3.54 | -3.52 | -3.58 | -3.43 |
| MES | 5 | h16 | event | with signal | 263276 | +0.005 | 0.368 | +0.05 | -3.45 | -3.50 | -3.38 | -3.33 |
| MES | 5 | eod | event | against signal | 263276 | +0.063 | 0.368 | +0.20 | -3.30 | -3.08 | -3.56 | -3.80 |
| MES | 15 | h1 | event | against signal | 77382 | +0.008 | 0.199 | +0.12 | -3.38 | -3.42 | -3.35 | -3.49 |
| MES | 15 | h2 | event | with signal | 77382 | -0.003 | 0.199 | -0.05 | -3.55 | -3.56 | -3.54 | -3.42 |
| MES | 15 | h4 | event | with signal | 77382 | -0.000 | 0.199 | -0.04 | -3.54 | -3.56 | -3.51 | -3.40 |
| MES | 15 | h8 | event | with signal | 77382 | -0.000 | 0.199 | -0.14 | -3.64 | -3.52 | -3.77 | -3.46 |
| MES | 15 | h16 | event | against signal | 77382 | +0.020 | 0.199 | +0.40 | -3.10 | -3.45 | -2.73 | -3.41 |
| MES | 15 | eod | event | against signal | 77382 | +0.060 | 0.199 | +0.85 | -2.65 | -3.06 | -2.21 | -3.18 |
| MES | 60 | h1 | event | with signal | 17879 | +0.001 | 0.094 | +0.14 | -3.36 | -3.32 | -3.40 | -3.36 |
| MES | 60 | h2 | event | against signal | 17879 | +0.009 | 0.094 | -0.03 | -3.53 | -3.67 | -3.38 | -3.60 |
| MES | 60 | h4 | event | against signal | 17879 | +0.021 | 0.094 | +0.31 | -3.19 | -3.07 | -3.32 | -3.32 |
| MES | 60 | h8 | event | against signal | 17879 | +0.027 | 0.094 | +0.46 | -3.04 | -3.02 | -3.06 | -3.26 |
| MES | 60 | h16 | event | against signal | 17879 | +0.030 | 0.094 | +0.22 | -3.28 | -3.08 | -3.49 | -3.31 |
| MES | 60 | eod | event | against signal | 17879 | +0.027 | 0.094 | -0.03 | -3.53 | -3.05 | -4.00 | -3.62 |
| MNQ | 5 | h1 | event | with signal | 232163 | -0.003 | 0.139 | -0.04 | -2.04 | -2.01 | -2.07 | -1.98 |
| MNQ | 5 | h2 | event | against signal | 232163 | +0.008 | 0.139 | +0.14 | -1.86 | -1.97 | -1.75 | -1.97 |
| MNQ | 5 | h4 | event | against signal | 232163 | +0.009 | 0.139 | +0.19 | -1.81 | -1.98 | -1.62 | -1.89 |
| MNQ | 5 | h8 | event | against signal | 232163 | +0.006 | 0.139 | +0.19 | -1.81 | -2.00 | -1.60 | -1.83 |
| MNQ | 5 | h16 | event | with signal | 232163 | +0.000 | 0.139 | -0.09 | -2.09 | -1.99 | -2.20 | -2.07 |
| MNQ | 5 | eod | event | with signal | 232163 | -0.051 | 0.139 | -0.25 | -2.25 | -2.18 | -2.33 | -1.02 |
| MNQ | 15 | h1 | event | with signal | 74577 | -0.002 | 0.078 | +0.15 | -1.85 | -2.05 | -1.65 | -1.80 |
| MNQ | 15 | h2 | event | with signal | 74577 | +0.007 | 0.078 | +0.25 | -1.75 | -2.00 | -1.50 | -1.73 |
| MNQ | 15 | h4 | event | with signal | 74577 | +0.010 | 0.078 | +0.30 | -1.70 | -2.03 | -1.36 | -1.72 |
| MNQ | 15 | h8 | event | with signal | 74577 | +0.011 | 0.078 | +0.18 | -1.82 | -2.04 | -1.60 | -1.90 |
| MNQ | 15 | h16 | event | with signal | 74577 | +0.005 | 0.078 | -0.26 | -2.26 | -1.96 | -2.58 | -2.07 |
| MNQ | 15 | eod | event | against signal | 74577 | +0.057 | 0.078 | +1.26 | -0.74 | -1.98 | +0.53 | -1.35 |
| MNQ | 60 | h1 | event | with signal | 17972 | +0.002 | 0.038 | -0.24 | -2.24 | -1.93 | -2.58 | -2.25 |
| MNQ | 60 | h2 | event | with signal | 17972 | +0.000 | 0.038 | -0.28 | -2.28 | -1.76 | -2.83 | -2.18 |
| MNQ | 60 | h4 | event | with signal | 17972 | -0.005 | 0.038 | -0.29 | -2.29 | -1.99 | -2.60 | -2.08 |
| MNQ | 60 | h8 | event | against signal | 17972 | +0.011 | 0.038 | -0.04 | -2.04 | -1.77 | -2.33 | -2.26 |
| MNQ | 60 | h16 | event | against signal | 17972 | +0.019 | 0.038 | -0.19 | -2.19 | -1.93 | -2.47 | -2.17 |
| MNQ | 60 | eod | event | against signal | 17972 | +0.022 | 0.038 | -0.27 | -2.27 | -1.83 | -2.74 | -2.40 |
| MYM | 5 | h1 | event | with signal | 112062 | -0.000 | 0.173 | +0.03 | -1.97 | +nan | -1.97 | -1.90 |
| MYM | 5 | h2 | event | with signal | 112062 | -0.001 | 0.173 | -0.03 | -2.03 | +nan | -2.03 | -1.92 |
| MYM | 5 | h4 | event | with signal | 112062 | +0.001 | 0.173 | +0.00 | -2.00 | +nan | -2.00 | -1.85 |
| MYM | 5 | h8 | event | with signal | 112062 | +0.003 | 0.173 | -0.02 | -2.02 | +nan | -2.02 | -1.83 |
| MYM | 5 | h16 | event | with signal | 112062 | +0.002 | 0.173 | +0.05 | -1.95 | +nan | -1.95 | -1.67 |
| MYM | 5 | eod | event | with signal | 112062 | -0.005 | 0.173 | -0.29 | -2.29 | +nan | -2.29 | -1.48 |
| MYM | 15 | h1 | event | against signal | 37007 | +0.012 | 0.099 | +0.16 | -1.84 | +nan | -1.84 | -1.94 |
| MYM | 15 | h2 | event | against signal | 37007 | +0.014 | 0.099 | +0.21 | -1.79 | +nan | -1.79 | -1.91 |
| MYM | 15 | h4 | event | against signal | 37007 | +0.008 | 0.099 | +0.08 | -1.92 | +nan | -1.92 | -2.03 |
| MYM | 15 | h8 | event | with signal | 37007 | -0.001 | 0.099 | +0.06 | -1.94 | +nan | -1.94 | -1.75 |
| MYM | 15 | h16 | event | with signal | 37007 | -0.012 | 0.099 | -0.18 | -2.18 | +nan | -2.18 | -1.94 |
| MYM | 15 | eod | event | with signal | 37007 | -0.023 | 0.099 | -0.82 | -2.82 | +nan | -2.82 | -2.24 |
| MYM | 60 | h1 | event | with signal | 8851 | +0.008 | 0.048 | +0.28 | -1.72 | +nan | -1.72 | -1.69 |
| MYM | 60 | h2 | event | with signal | 8851 | -0.002 | 0.048 | +0.06 | -1.94 | +nan | -1.94 | -1.68 |
| MYM | 60 | h4 | event | with signal | 8851 | +0.003 | 0.048 | +0.79 | -1.21 | +nan | -1.21 | -0.81 |
| MYM | 60 | h8 | event | with signal | 8851 | +0.017 | 0.048 | +1.39 | -0.61 | +nan | -0.61 | +0.01 |
| MYM | 60 | h16 | event | with signal | 8851 | +0.018 | 0.048 | +1.03 | -0.97 | +nan | -0.97 | -0.48 |
| MYM | 60 | eod | event | with signal | 8851 | +0.017 | 0.048 | +1.17 | -0.83 | +nan | -0.83 | -0.27 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.160 | +0.192 | +0.082 | -0.063 | -0.474 | +0.000 | -0.045 | -0.047 | -0.047 | -0.040 | -0.033 |
| MES | 15 | +0.187 | +0.222 | +0.099 | -0.070 | -0.530 | +0.000 | -0.021 | -0.015 | -0.013 | -0.011 | -0.027 |
| MES | 60 | +0.201 | +0.159 | +0.063 | -0.098 | -0.554 | +0.000 | -0.001 | -0.012 | -0.032 | -0.043 | +0.047 |
| MNQ | 5 | +0.257 | +0.309 | +0.175 | -0.017 | -0.504 | +0.000 | -0.017 | -0.022 | -0.023 | -0.017 | -0.003 |
| MNQ | 15 | +0.234 | +0.271 | +0.147 | -0.044 | -0.534 | +0.000 | -0.007 | +0.003 | +0.006 | +0.010 | +0.010 |
| MNQ | 60 | +0.247 | +0.202 | +0.091 | -0.084 | -0.543 | +0.000 | +0.003 | +0.000 | -0.004 | -0.024 | -0.017 |
| MYM | 5 | +0.255 | +0.298 | +0.167 | -0.028 | -0.527 | +0.000 | -0.006 | -0.006 | -0.002 | +0.002 | +0.007 |
| MYM | 15 | +0.234 | +0.267 | +0.142 | -0.045 | -0.536 | +0.000 | -0.013 | -0.014 | -0.008 | +0.003 | -0.003 |
| MYM | 60 | +0.204 | +0.209 | +0.098 | -0.075 | -0.541 | +0.000 | +0.008 | -0.002 | +0.001 | +0.030 | +0.001 |

## Calibration

- MES 5-min: 1036271 bars, 263276 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 77382 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 17879 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 232163 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 74577 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 17972 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 112062 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 37007 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8851 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 50019 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
