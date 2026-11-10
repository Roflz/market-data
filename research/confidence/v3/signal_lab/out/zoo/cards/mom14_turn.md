# Impact card: mom14_turn

Momentum(14) turns up (long) / down (short) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.003 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=1).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.05 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.224 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.003 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.006 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.16).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.15 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.129 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.004 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.011 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.016).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.57 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.014 R20 over the rest of the session (to 16:45), p=0.35; we would catch an effect of 0.005 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 1% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.006 R20, CONFIRMED, q=0.0275, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.17 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.079 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.004 R20 over the next 2 bars (30 min), p=0.71; we would catch an effect of 0.010 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.44).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.32 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.045 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.005 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.011 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.07 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.022 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.009 R20 over the next 16 bars (80 min), p=0.43; we would catch an effect of 0.009 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.081).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.07 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.172 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.004 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.20 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.097 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.008 R20 over the rest of the session (to 16:45), p=0.79; we would catch an effect of 0.016 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.079).
- MYM 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.75 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.047 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.001 | -0.001 .. +0.003 | +0.0014 | 0.19 / 0.18 / 0.16 | 0.158 | 1 | 1 | 10/16 | +0.002 | +0.001 | False | +1.4 / +1.3 |  |
| MES | 5 | h2 | +0.001 | -0.001 .. +0.003 | +0.0006 | 0.46 / 0.46 / 0.46 | 0.456 |  |  | 11/16 | -0.001 | +0.002 |  | +0.5 / +0.7 |  |
| MES | 5 | h4 | +0.002 | -0.000 .. +0.004 | +0.0009 | 0.098 / 0.089 / 0.13 | 0.136 |  |  | 11/16 | +0.000 | +0.003 |  | +0.9 / +1.7 | 0.003 |
| MES | 5 | h8 | -0.000 | -0.002 .. +0.002 | -0.0001 | 0.9 / 0.9 / 0.93 | 0.924 |  |  | 8/16 | +0.000 | -0.000 |  | -0.1 / -0.1 |  |
| MES | 5 | h16 | +0.002 | -0.001 .. +0.004 | +0.0004 | 0.14 / 0.14 / 0.24 | 0.241 |  |  | 11/16 | -0.001 | +0.005 |  | +0.4 / +1.5 |  |
| MES | 5 | eod | +0.004 | -0.004 .. +0.013 | +0.0002 | 0.32 / 0.35 / 0.42 | 0.421 |  |  | 12/16 | +0.006 | +0.003 |  | +0.2 / +1.0 |  |
| MES | 15 | h1 | +0.001 | -0.002 .. +0.005 | +0.0014 | 0.4 / 0.41 / 0.45 | 0.454 |  |  | 9/16 | +0.001 | +0.002 |  | +0.8 / +0.8 |  |
| MES | 15 | h2 | -0.000 | -0.004 .. +0.004 | -0.0001 | 0.96 / 0.95 / 0.96 | 0.961 |  |  | 7/16 | -0.001 | +0.001 |  | -0.0 / -0.1 |  |
| MES | 15 | h4 | +0.001 | -0.003 .. +0.005 | +0.0004 | 0.61 / 0.6 / 0.69 | 0.688 |  |  | 9/16 | -0.001 | +0.003 |  | +0.3 / +0.5 | 0.006 |
| MES | 15 | h8 | +0.003 | -0.001 .. +0.006 | +0.0008 | 0.2 / 0.18 / 0.28 | 0.284 |  |  | 10/16 | +0.000 | +0.005 |  | +0.5 / +1.3 |  |
| MES | 15 | h16 * | +0.003 | -0.002 .. +0.007 | +0.0005 | 0.25 / 0.23 / 0.31 | 0.307 | 1 | 1 | 11/16 | +0.001 | +0.004 | False | +0.3 / +1.1 |  |
| MES | 15 | eod | -0.001 | -0.007 .. +0.006 | -0.0000 | 0.87 / 0.87 / 0.88 | 0.885 |  |  | 8/16 | +0.003 | -0.004 |  | -0.0 / -0.2 |  |
| MES | 60 | h1 | -0.000 | -0.007 .. +0.007 | -0.0003 | 0.94 / 0.94 / 0.94 | 0.941 |  |  | 7/16 | -0.001 | +0.001 |  | -0.1 / -0.1 |  |
| MES | 60 | h2 * | +0.004 | -0.003 .. +0.011 | +0.0029 | 0.24 / 0.26 / 0.27 | 0.266 | 1 | 1 | 9/16 | +0.006 | +0.002 | False | +0.8 / +1.2 |  |
| MES | 60 | h4 | -0.002 | -0.010 .. +0.005 | -0.0011 | 0.54 / 0.53 / 0.55 | 0.545 |  |  | 8/16 | -0.001 | -0.004 |  | -0.3 / -0.6 | 0.011 |
| MES | 60 | h8 | +0.001 | -0.006 .. +0.008 | +0.0005 | 0.71 / 0.72 / 0.71 | 0.718 |  |  | 11/16 | +0.001 | +0.002 |  | +0.1 / +0.4 |  |
| MES | 60 | h16 | +0.002 | -0.005 .. +0.009 | +0.0005 | 0.59 / 0.6 / 0.62 | 0.617 |  |  | 8/16 | +0.000 | +0.003 |  | +0.1 / +0.5 |  |
| MES | 60 | eod | +0.004 | -0.003 .. +0.010 | +0.0009 | 0.31 / 0.32 / 0.35 | 0.344 |  |  | 10/16 | -0.001 | +0.008 |  | +0.2 / +1.0 |  |
| MNQ | 5 | h1 | +0.001 | -0.001 .. +0.003 | +0.0008 | 0.42 / 0.41 / 0.43 | 0.434 |  |  | 8/16 | +0.001 | +0.001 |  | +0.9 / +0.8 |  |
| MNQ | 5 | h2 | -0.001 | -0.003 .. +0.001 | -0.0005 | 0.4 / 0.4 / 0.56 | 0.564 |  |  | 9/16 | -0.003 | +0.001 |  | -0.6 / -0.8 |  |
| MNQ | 5 | h4 | -0.002 | -0.004 .. +0.000 | -0.0007 | 0.1 / 0.093 / 0.38 | 0.395 |  |  | 9/16 | -0.004 | -0.000 |  | -0.9 / -1.6 | 0.005 |
| MNQ | 5 | h8 | -0.005 | -0.007 .. -0.002 | -0.0011 | 4.4e-05 / 8.8e-05 / 0.088 | 0.0878 |  |  | 11/16 | -0.005 | -0.004 |  | -1.5 / -4.1 |  |
| MNQ | 5 | h16 | -0.005 | -0.007 .. -0.002 | -0.0008 | 0.00032 / 0.00031 / 0.14 | 0.144 |  |  | 13/16 | -0.008 | -0.002 |  | -1.0 / -3.6 |  |
| MNQ | 5 | eod * | +0.014 | +0.006 .. +0.021 | +0.0005 | 0.00038 / 0.00051 / 0.12 | 0.121 | 1 | 0.027 | 15/16 | +0.017 | +0.011 | False | +0.5 / +3.6 |  |
| MNQ | 15 | h1 | -0.001 | -0.005 .. +0.003 | -0.0009 | 0.54 / 0.55 / 0.62 | 0.619 |  |  | 9/16 | -0.004 | +0.001 |  | -0.6 / -0.6 |  |
| MNQ | 15 | h2 * | -0.004 | -0.008 .. +0.001 | -0.0017 | 0.11 / 0.11 / 0.24 | 0.252 | 1 | 1 | 10/16 | -0.007 | -0.001 | False | -1.3 / -1.6 |  |
| MNQ | 15 | h4 | -0.001 | -0.005 .. +0.003 | -0.0003 | 0.56 / 0.58 / 0.83 | 0.836 |  |  | 10/16 | -0.004 | +0.002 |  | -0.3 / -0.6 | 0.010 |
| MNQ | 15 | h8 | -0.003 | -0.007 .. +0.001 | -0.0006 | 0.2 / 0.19 / 0.49 | 0.494 |  |  | 11/16 | -0.006 | +0.000 |  | -0.5 / -1.3 |  |
| MNQ | 15 | h16 | +0.000 | -0.004 .. +0.005 | +0.0000 | 0.9 / 0.9 / 0.95 | 0.955 |  |  | 7/16 | -0.003 | +0.004 |  | +0.0 / +0.1 |  |
| MNQ | 15 | eod | -0.001 | -0.007 .. +0.004 | -0.0001 | 0.67 / 0.67 / 0.92 | 0.919 |  |  | 9/16 | +0.002 | -0.004 |  | -0.1 / -0.4 |  |
| MNQ | 60 | h1 | -0.000 | -0.008 .. +0.008 | -0.0001 | 0.97 / 0.97 / 0.97 | 0.975 |  |  | 8/16 | +0.000 | -0.001 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h2 * | +0.005 | -0.002 .. +0.013 | +0.0032 | 0.19 / 0.22 / 0.22 | 0.213 | 1 | 1 | 10/16 | +0.004 | +0.006 | False | +0.9 / +1.3 |  |
| MNQ | 60 | h4 | -0.001 | -0.009 .. +0.007 | -0.0004 | 0.82 / 0.82 / 0.82 | 0.822 |  |  | 8/16 | +0.003 | -0.005 |  | -0.1 / -0.2 | 0.011 |
| MNQ | 60 | h8 | +0.002 | -0.006 .. +0.010 | +0.0006 | 0.62 / 0.63 / 0.6 | 0.593 |  |  | 10/16 | +0.004 | +0.000 |  | +0.2 / +0.5 |  |
| MNQ | 60 | h16 | +0.001 | -0.006 .. +0.009 | +0.0004 | 0.7 / 0.7 / 0.71 | 0.695 |  |  | 6/16 | -0.000 | +0.003 |  | +0.1 / +0.4 |  |
| MNQ | 60 | eod | +0.003 | -0.005 .. +0.010 | +0.0006 | 0.51 / 0.51 / 0.51 | 0.513 |  |  | 10/16 | -0.001 | +0.006 |  | +0.2 / +0.7 |  |
| MYM | 5 | h1 | +0.001 | -0.002 .. +0.003 | +0.0006 | 0.6 / 0.62 / 0.63 | 0.651 |  |  | 5/8 | n/a | +0.001 |  | +0.5 / +0.5 |  |
| MYM | 5 | h2 | +0.000 | -0.003 .. +0.003 | +0.0002 | 0.79 / 0.8 / 0.84 | 0.855 |  |  | 4/8 | n/a | +0.000 |  | +0.2 / +0.3 |  |
| MYM | 5 | h4 | +0.003 | -0.000 .. +0.006 | +0.0008 | 0.086 / 0.081 / 0.42 | 0.417 |  |  | 5/8 | n/a | +0.003 |  | +0.9 / +1.7 | 0.009 |
| MYM | 5 | h8 | +0.002 | -0.001 .. +0.005 | +0.0004 | 0.23 / 0.24 / 0.67 | 0.645 |  |  | 7/8 | n/a | +0.002 |  | +0.4 / +1.2 |  |
| MYM | 5 | h16 * | +0.009 | +0.006 .. +0.012 | +0.0015 | 9.8e-08 / 8.5e-08 / 0.098 | 0.0917 | 1 | 0.001 | 8/8 | n/a | +0.009 | False | +1.4 / +5.3 |  |
| MYM | 5 | eod | +0.010 | +0.002 .. +0.018 | +0.0004 | 0.014 / 0.016 / 0.45 | 0.468 |  |  | 5/8 | n/a | +0.010 |  | +0.3 / +2.5 |  |
| MYM | 15 | h1 | +0.002 | -0.004 .. +0.007 | +0.0015 | 0.51 / 0.49 / 0.58 | 0.572 |  |  | 3/8 | n/a | +0.002 |  | +0.7 / +0.7 |  |
| MYM | 15 | h2 * | -0.004 | -0.011 .. +0.003 | -0.0019 | 0.24 / 0.24 / 0.4 | 0.403 | 1 | 1 | 5/8 | n/a | -0.004 | False | -1.0 / -1.2 |  |
| MYM | 15 | h4 | +0.000 | -0.005 .. +0.005 | +0.0001 | 0.94 / 0.94 / 0.99 | 0.987 |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.1 | 0.017 |
| MYM | 15 | h8 | -0.000 | -0.006 .. +0.006 | -0.0000 | 0.98 / 0.98 / 0.99 | 0.986 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 15 | h16 | -0.005 | -0.011 .. +0.000 | -0.0008 | 0.067 / 0.072 / 0.57 | 0.585 |  |  | 6/8 | n/a | -0.005 |  | -0.4 / -1.8 |  |
| MYM | 15 | eod | -0.009 | -0.021 .. +0.004 | -0.0005 | 0.19 / 0.18 / 0.66 | 0.65 |  |  | 6/8 | n/a | -0.009 |  | -0.3 / -1.3 |  |
| MYM | 60 | h1 | +0.004 | -0.007 .. +0.014 | +0.0034 | 0.49 / 0.51 / 0.51 | 0.499 |  |  | 4/8 | n/a | +0.004 |  | +0.7 / +0.7 |  |
| MYM | 60 | h2 | -0.005 | -0.015 .. +0.005 | -0.0031 | 0.36 / 0.37 / 0.41 | 0.409 |  |  | 6/8 | n/a | -0.005 |  | -0.6 / -0.9 |  |
| MYM | 60 | h4 | -0.007 | -0.018 .. +0.003 | -0.0034 | 0.18 / 0.18 / 0.2 | 0.202 |  |  | 6/8 | n/a | -0.007 |  | -0.6 / -1.3 | 0.016 |
| MYM | 60 | h8 | -0.002 | -0.012 .. +0.009 | -0.0005 | 0.78 / 0.77 / 0.81 | 0.808 |  |  | 2/8 | n/a | -0.002 |  | -0.1 / -0.3 |  |
| MYM | 60 | h16 | -0.008 | -0.018 .. +0.002 | -0.0020 | 0.13 / 0.13 / 0.15 | 0.156 |  |  | 6/8 | n/a | -0.008 |  | -0.4 / -1.5 |  |
| MYM | 60 | eod * | -0.008 | -0.018 .. +0.002 | -0.0020 | 0.13 / 0.13 / 0.15 | 0.148 | 1 | 1 | 6/8 | n/a | -0.008 | False | -0.4 / -1.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.003 .. +0.001 | -0.2% | -0.007 | 0.23 |  | 9/16 |
| MES | 5 | h2 | -0.001 | -0.005 .. +0.003 | -0.1% | -0.008 | 0.6 |  | 10/16 |
| MES | 5 | h4 | -0.003 | -0.010 .. +0.003 | -0.3% | -0.012 | 0.32 |  | 9/16 |
| MES | 5 | h8 | -0.008 | -0.021 .. +0.005 | -0.5% | -0.019 | 0.25 |  | 9/16 |
| MES | 5 | h16 * | -0.012 | -0.031 .. +0.007 | -0.6% | -0.036 | 0.21 | 1 | 11/16 |
| MES | 5 | eod | -0.087 | -0.283 .. +0.108 | -0.9% | -0.200 | 0.38 |  | 6/16 |
| MES | 15 | h1 * | -0.005 | -0.009 .. -0.002 | -1.1% | -0.014 | 0.027 | 1 | 12/16 |
| MES | 15 | h2 | -0.004 | -0.013 .. +0.004 | -0.6% | -0.019 | 0.39 |  | 7/16 |
| MES | 15 | h4 | -0.008 | -0.025 .. +0.008 | -0.8% | -0.027 | 0.31 |  | 8/16 |
| MES | 15 | h8 | -0.010 | -0.035 .. +0.014 | -0.7% | -0.049 | 0.39 |  | 9/16 |
| MES | 15 | h16 | -0.027 | -0.065 .. +0.010 | -1.2% | -0.093 | 0.15 |  | 10/16 |
| MES | 15 | eod | -0.099 | -0.289 .. +0.091 | -1.8% | -0.207 | 0.31 |  | 9/16 |
| MES | 60 | h1 | -0.001 | -0.008 .. +0.006 | -0.1% | -0.002 | 0.93 |  | 8/16 |
| MES | 60 | h2 | -0.000 | -0.010 .. +0.010 | -0.0% | -0.004 | 0.98 |  | 9/16 |
| MES | 60 | h4 | -0.002 | -0.016 .. +0.012 | -0.2% | -0.007 | 0.8 |  | 8/16 |
| MES | 60 | h8 | -0.013 | -0.032 .. +0.006 | -0.9% | -0.006 | 0.18 |  | 12/16 |
| MES | 60 | h16 | -0.026 | -0.050 .. -0.002 | -1.3% | -0.021 | 0.048 |  | 11/16 |
| MES | 60 | eod * | -0.039 | -0.063 .. -0.014 | -1.8% | -0.031 | 0.0027 | 0.427 | 13/16 |
| MNQ | 5 | h1 * | -0.006 | -0.010 .. -0.003 | -1.2% | -0.014 | 0.00014 | 0.0275 | 13/16 |
| MNQ | 5 | h2 | -0.009 | -0.018 .. -0.001 | -1.2% | -0.020 | 0.036 |  | 11/16 |
| MNQ | 5 | h4 | -0.017 | -0.035 .. +0.002 | -1.5% | -0.035 | 0.076 |  | 12/16 |
| MNQ | 5 | h8 | -0.033 | -0.073 .. +0.007 | -2.0% | -0.063 | 0.11 |  | 12/16 |
| MNQ | 5 | h16 | -0.056 | -0.129 .. +0.016 | -2.4% | -0.122 | 0.13 |  | 13/16 |
| MNQ | 5 | eod | -0.233 | -0.612 .. +0.145 | -1.9% | -0.525 | 0.23 |  | 10/16 |
| MNQ | 15 | h1 * | -0.006 | -0.012 .. +0.001 | -1.1% | -0.015 | 0.074 | 1 | 11/16 |
| MNQ | 15 | h2 | -0.012 | -0.029 .. +0.005 | -1.5% | -0.028 | 0.17 |  | 11/16 |
| MNQ | 15 | h4 | -0.026 | -0.072 .. +0.020 | -2.3% | -0.052 | 0.26 |  | 10/16 |
| MNQ | 15 | h8 | -0.040 | -0.112 .. +0.032 | -2.4% | -0.108 | 0.28 |  | 9/16 |
| MNQ | 15 | h16 | -0.050 | -0.126 .. +0.026 | -2.0% | -0.187 | 0.2 |  | 10/16 |
| MNQ | 15 | eod | -0.227 | -0.568 .. +0.113 | -3.6% | -0.348 | 0.19 |  | 13/16 |
| MNQ | 60 | h1 | +0.003 | -0.005 .. +0.010 | +0.5% | +0.002 | 0.48 |  | 9/16 |
| MNQ | 60 | h2 | -0.001 | -0.012 .. +0.010 | -0.1% | -0.003 | 0.86 |  | 9/16 |
| MNQ | 60 | h4 | -0.002 | -0.017 .. +0.012 | -0.2% | -0.004 | 0.75 |  | 9/16 |
| MNQ | 60 | h8 | -0.005 | -0.026 .. +0.015 | -0.3% | -0.003 | 0.61 |  | 9/16 |
| MNQ | 60 | h16 | -0.008 | -0.034 .. +0.018 | -0.4% | -0.007 | 0.54 |  | 10/16 |
| MNQ | 60 | eod * | -0.011 | -0.038 .. +0.016 | -0.5% | -0.013 | 0.47 | 1 | 9/16 |
| MYM | 5 | h1 * | -0.008 | -0.014 .. -0.002 | -1.5% | -0.017 | 0.014 | 1 | 8/8 |
| MYM | 5 | h2 | -0.015 | -0.030 .. -0.000 | -2.0% | -0.027 | 0.046 |  | 6/8 |
| MYM | 5 | h4 | -0.024 | -0.058 .. +0.010 | -2.2% | -0.044 | 0.17 |  | 5/8 |
| MYM | 5 | h8 | -0.040 | -0.104 .. +0.025 | -2.5% | -0.079 | 0.23 |  | 5/8 |
| MYM | 5 | h16 | -0.060 | -0.146 .. +0.025 | -2.6% | -0.138 | 0.17 |  | 6/8 |
| MYM | 5 | eod | -0.219 | -0.610 .. +0.173 | -1.9% | -0.328 | 0.28 |  | 4/8 |
| MYM | 15 | h1 * | -0.006 | -0.015 .. +0.003 | -1.1% | -0.017 | 0.22 | 1 | 3/8 |
| MYM | 15 | h2 | -0.010 | -0.029 .. +0.009 | -1.3% | -0.028 | 0.33 |  | 5/8 |
| MYM | 15 | h4 | -0.030 | -0.082 .. +0.021 | -2.7% | -0.061 | 0.26 |  | 5/8 |
| MYM | 15 | h8 | -0.044 | -0.127 .. +0.039 | -2.7% | -0.127 | 0.3 |  | 4/8 |
| MYM | 15 | h16 | -0.095 | -0.246 .. +0.055 | -3.9% | -0.240 | 0.22 |  | 5/8 |
| MYM | 15 | eod | -0.207 | -0.591 .. +0.178 | -3.4% | -0.340 | 0.31 |  | 5/8 |
| MYM | 60 | h1 | +0.003 | -0.008 .. +0.013 | +0.5% | +0.003 | 0.73 |  | 5/8 |
| MYM | 60 | h2 | +0.011 | -0.005 .. +0.026 | +1.4% | +0.006 | 0.23 |  | 6/8 |
| MYM | 60 | h4 * | +0.026 | +0.006 .. +0.046 | +2.4% | +0.016 | 0.013 | 1 | 7/8 |
| MYM | 60 | h8 | +0.006 | -0.025 .. +0.037 | +0.4% | +0.013 | 0.76 |  | 5/8 |
| MYM | 60 | h16 | -0.001 | -0.039 .. +0.037 | -0.1% | +0.012 | 0.95 |  | 4/8 |
| MYM | 60 | eod | -0.009 | -0.050 .. +0.031 | -0.4% | +0.004 | 0.66 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.07 pts | -0.03 .. +0.17 | 0.15 |
| MES | 15 | +0.22 pts | +0.05 .. +0.39 | 0.011 |
| MES | 60 | +0.12 pts | -0.20 .. +0.44 | 0.47 |
| MNQ | 5 | +0.07 pts | -0.04 .. +0.18 | 0.21 |
| MNQ | 15 | +0.12 pts | -0.05 .. +0.28 | 0.2 |
| MNQ | 60 | +0.19 pts | -0.11 .. +0.49 | 0.34 |
| MYM | 5 | +0.03 pts | -0.11 .. +0.16 | 0.72 |
| MYM | 15 | +0.03 pts | -0.20 .. +0.27 | 0.91 |
| MYM | 60 | -0.12 pts | -0.53 .. +0.28 | 0.65 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 504079 | -0.004 | 0.320 | -0.03 | -3.53 | -3.51 | -3.55 | -3.47 |
| MES | 5 | h2 | event | with signal | 504079 | -0.007 | 0.320 | -0.06 | -3.56 | -3.55 | -3.57 | -3.47 |
| MES | 5 | h4 | event | with signal | 504079 | -0.006 | 0.320 | -0.06 | -3.56 | -3.54 | -3.57 | -3.47 |
| MES | 5 | h8 | event | against signal | 504079 | +0.007 | 0.320 | +0.07 | -3.43 | -3.47 | -3.40 | -3.51 |
| MES | 5 | h16 | event | with signal | 504079 | -0.006 | 0.320 | -0.04 | -3.54 | -3.55 | -3.54 | -3.46 |
| MES | 5 | eod | event | with signal | 504079 | -0.006 | 0.320 | -0.05 | -3.55 | -3.54 | -3.57 | -3.43 |
| MES | 15 | h1 | event | with signal | 171256 | -0.003 | 0.189 | -0.05 | -3.55 | -3.54 | -3.55 | -3.47 |
| MES | 15 | h2 | event | against signal | 171256 | +0.005 | 0.189 | +0.09 | -3.41 | -3.44 | -3.39 | -3.50 |
| MES | 15 | h4 | event | with signal | 171256 | -0.004 | 0.189 | -0.02 | -3.52 | -3.55 | -3.50 | -3.43 |
| MES | 15 | h8 | event | with signal | 171256 | -0.003 | 0.189 | -0.04 | -3.54 | -3.55 | -3.53 | -3.44 |
| MES | 15 | h16 | event | with signal | 171256 | -0.005 | 0.189 | -0.08 | -3.58 | -3.56 | -3.59 | -3.44 |
| MES | 15 | eod | event | against signal | 171256 | +0.003 | 0.189 | +0.07 | -3.43 | -3.49 | -3.38 | -3.49 |
| MES | 60 | h1 | event | against signal | 41856 | +0.000 | 0.094 | +0.03 | -3.47 | -3.51 | -3.44 | -3.47 |
| MES | 60 | h2 | event | with signal | 41856 | +0.003 | 0.094 | -0.09 | -3.59 | -3.36 | -3.82 | -3.54 |
| MES | 60 | h4 | event | against signal | 41856 | +0.004 | 0.094 | +0.30 | -3.20 | -3.44 | -2.96 | -3.28 |
| MES | 60 | h8 | event | with signal | 41856 | -0.002 | 0.094 | -0.24 | -3.74 | -3.53 | -3.94 | -3.62 |
| MES | 60 | h16 | event | with signal | 41856 | +0.003 | 0.094 | +0.04 | -3.46 | -3.46 | -3.46 | -3.50 |
| MES | 60 | eod | event | with signal | 41856 | +0.003 | 0.094 | +0.14 | -3.36 | -3.49 | -3.23 | -3.33 |
| MNQ | 5 | h1 | event | with signal | 521486 | -0.001 | 0.131 | -0.01 | -2.01 | -1.99 | -2.03 | -1.98 |
| MNQ | 5 | h2 | event | against signal | 521486 | +0.005 | 0.131 | +0.04 | -1.96 | -1.97 | -1.94 | -2.02 |
| MNQ | 5 | h4 | event | against signal | 521486 | +0.005 | 0.131 | +0.06 | -1.94 | -1.97 | -1.91 | -1.99 |
| MNQ | 5 | h8 | event | against signal | 521486 | +0.005 | 0.131 | +0.08 | -1.92 | -1.98 | -1.87 | -1.92 |
| MNQ | 5 | h16 | event | against signal | 521486 | +0.004 | 0.131 | +0.03 | -1.97 | -1.98 | -1.97 | -1.96 |
| MNQ | 5 | eod | event | with signal | 521486 | +0.000 | 0.131 | -0.04 | -2.04 | -2.02 | -2.05 | -1.82 |
| MNQ | 15 | h1 | event | against signal | 172965 | +0.003 | 0.075 | +0.02 | -1.98 | -1.96 | -1.99 | -2.02 |
| MNQ | 15 | h2 | event | against signal | 172965 | +0.004 | 0.075 | +0.06 | -1.94 | -1.93 | -1.95 | -1.96 |
| MNQ | 15 | h4 | event | against signal | 172965 | +0.001 | 0.075 | -0.03 | -2.03 | -1.98 | -2.08 | -2.02 |
| MNQ | 15 | h8 | event | against signal | 172965 | +0.000 | 0.075 | -0.01 | -2.01 | -1.98 | -2.04 | -1.95 |
| MNQ | 15 | h16 | event | with signal | 172965 | -0.001 | 0.075 | -0.03 | -2.03 | -2.02 | -2.03 | -2.00 |
| MNQ | 15 | eod | event | against signal | 172965 | -0.000 | 0.075 | +0.10 | -1.90 | -2.02 | -1.78 | -1.90 |
| MNQ | 60 | h1 | event | against signal | 42020 | -0.000 | 0.037 | -0.01 | -2.01 | -2.03 | -1.99 | -2.00 |
| MNQ | 60 | h2 | event | with signal | 42020 | +0.004 | 0.037 | +0.10 | -1.90 | -1.87 | -1.93 | -1.85 |
| MNQ | 60 | h4 | event | against signal | 42020 | +0.003 | 0.037 | +0.36 | -1.64 | -2.04 | -1.23 | -1.75 |
| MNQ | 60 | h8 | event | with signal | 42020 | -0.000 | 0.037 | -0.07 | -2.07 | -1.95 | -2.19 | -1.95 |
| MNQ | 60 | h16 | event | with signal | 42020 | +0.002 | 0.037 | +0.07 | -1.93 | -1.92 | -1.94 | -1.96 |
| MNQ | 60 | eod | event | with signal | 42020 | +0.001 | 0.037 | +0.18 | -1.82 | -1.97 | -1.67 | -1.75 |
| MYM | 5 | h1 | event | with signal | 264119 | -0.003 | 0.172 | -0.02 | -2.02 | +nan | -2.02 | -1.97 |
| MYM | 5 | h2 | event | with signal | 264119 | -0.005 | 0.172 | -0.03 | -2.03 | +nan | -2.03 | -1.97 |
| MYM | 5 | h4 | event | with signal | 264119 | -0.003 | 0.172 | -0.03 | -2.03 | +nan | -2.03 | -1.96 |
| MYM | 5 | h8 | event | with signal | 264119 | -0.005 | 0.172 | -0.05 | -2.05 | +nan | -2.05 | -1.97 |
| MYM | 5 | h16 | event | with signal | 264119 | -0.001 | 0.172 | -0.01 | -2.01 | +nan | -2.01 | -1.89 |
| MYM | 5 | eod | event | with signal | 264119 | -0.012 | 0.172 | -0.03 | -2.03 | +nan | -2.03 | -1.76 |
| MYM | 15 | h1 | event | with signal | 87430 | -0.001 | 0.097 | -0.01 | -2.01 | +nan | -2.01 | -1.96 |
| MYM | 15 | h2 | event | against signal | 87430 | +0.007 | 0.097 | +0.09 | -1.91 | +nan | -1.91 | -1.97 |
| MYM | 15 | h4 | event | with signal | 87430 | -0.001 | 0.097 | +0.02 | -1.98 | +nan | -1.98 | -1.95 |
| MYM | 15 | h8 | event | against signal | 87430 | +0.002 | 0.097 | +0.01 | -1.99 | +nan | -1.99 | -2.04 |
| MYM | 15 | h16 | event | against signal | 87430 | +0.007 | 0.097 | +0.08 | -1.92 | +nan | -1.92 | -1.96 |
| MYM | 15 | eod | event | against signal | 87430 | +0.014 | 0.097 | +0.10 | -1.90 | +nan | -1.90 | -2.01 |
| MYM | 60 | h1 | event | with signal | 21064 | +0.004 | 0.047 | -0.00 | -2.00 | +nan | -2.00 | -2.02 |
| MYM | 60 | h2 | event | against signal | 21064 | +0.008 | 0.047 | +0.51 | -1.49 | +nan | -1.49 | -1.61 |
| MYM | 60 | h4 | event | against signal | 21064 | +0.012 | 0.047 | +0.39 | -1.61 | +nan | -1.61 | -1.79 |
| MYM | 60 | h8 | event | against signal | 21064 | +0.007 | 0.047 | +0.38 | -1.62 | +nan | -1.62 | -1.85 |
| MYM | 60 | h16 | event | against signal | 21064 | +0.008 | 0.047 | +0.25 | -1.75 | +nan | -1.75 | -1.74 |
| MYM | 60 | eod | event | against signal | 21064 | +0.010 | 0.047 | +0.27 | -1.73 | +nan | -1.73 | -1.77 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.089 | -0.041 | -0.026 | -0.001 | -0.380 | +0.000 | -0.016 | -0.016 | -0.015 | -0.015 | -0.008 |
| MES | 15 | -0.086 | -0.046 | -0.027 | -0.008 | -0.381 | +0.000 | -0.006 | -0.009 | -0.008 | -0.007 | -0.007 |
| MES | 60 | -0.063 | -0.079 | -0.053 | -0.036 | -0.392 | +0.000 | -0.001 | +0.001 | -0.008 | -0.014 | +0.013 |
| MNQ | 5 | -0.087 | -0.042 | -0.027 | -0.004 | -0.399 | +0.000 | -0.009 | -0.014 | -0.016 | -0.015 | -0.014 |
| MNQ | 15 | -0.085 | -0.048 | -0.026 | -0.012 | -0.394 | +0.000 | -0.005 | -0.006 | -0.002 | -0.003 | -0.002 |
| MNQ | 60 | -0.034 | -0.086 | -0.052 | -0.039 | -0.402 | +0.000 | +0.001 | +0.003 | -0.007 | -0.011 | +0.006 |
| MYM | 5 | -0.080 | -0.038 | -0.020 | -0.004 | -0.390 | +0.000 | -0.005 | -0.005 | -0.003 | -0.005 | +0.004 |
| MYM | 15 | -0.080 | -0.042 | -0.022 | -0.006 | -0.387 | +0.000 | -0.002 | -0.008 | -0.003 | -0.001 | -0.007 |
| MYM | 60 | -0.049 | -0.080 | -0.056 | -0.037 | -0.404 | +0.000 | +0.004 | -0.006 | -0.012 | -0.012 | -0.006 |

## Calibration

- MES 5-min: 1036271 bars, 504079 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 171256 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 41856 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 521486 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 172965 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 42020 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 264119 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 87430 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 21064 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
