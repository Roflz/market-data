# Impact card: x_close_ema20

close crosses EMA20: above long, below short [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.023 R20 over the rest of the session (to 16:45), p=0.043; we would catch an effect of 0.008 R20 or more 80% of the time).
- MES 5-min size: the market moves 1% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.006 R20, CONFIRMED, q=0.0399, 11 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.10 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.236 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.010 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.017 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.39 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.134 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.009 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.032 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.62).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.42 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: POSSIBLE direction effect +0.059 average bars (~$1.45 per micro at 2018-25 bar sizes) over the rest of the session (to 16:45) (in the signal's direction), not confirmed (q=0.0754, replicated in the other half=True, 16 of 16 years); best leg (event, with signal) grosses $+0.20 and nets $-1.80 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.20 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.081 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.60 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.046 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.020 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.036 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.85 at recent bar sizes, 90% range up to $3.12); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.055 R20 over the rest of the session (to 16:45), p=0.15; we would catch an effect of 0.016 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.15 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.179 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.021 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.43 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.100 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.024 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.049 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.99 at recent bar sizes, 90% range up to $2.46); about 2.4x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.008 .. +0.001 | -0.0019 | 0.14 / 0.12 / 0.11 | 0.109 |  |  | 9/16 | -0.006 | -0.001 |  | -1.7 / -1.5 |  |
| MES | 5 | h2 | -0.002 | -0.007 .. +0.003 | -0.0007 | 0.49 / 0.47 / 0.53 | 0.525 |  |  | 7/16 | -0.004 | +0.001 |  | -0.6 / -0.7 |  |
| MES | 5 | h4 | -0.002 | -0.008 .. +0.004 | -0.0005 | 0.54 / 0.53 / 0.55 | 0.557 |  |  | 9/16 | -0.004 | +0.000 |  | -0.5 / -0.6 | 0.008 |
| MES | 5 | h8 | -0.002 | -0.008 .. +0.004 | -0.0003 | 0.6 / 0.61 / 0.66 | 0.66 |  |  | 11/16 | -0.006 | +0.003 |  | -0.3 / -0.5 |  |
| MES | 5 | h16 | -0.001 | -0.008 .. +0.006 | -0.0001 | 0.8 / 0.79 / 0.85 | 0.846 |  |  | 10/16 | -0.004 | +0.002 |  | -0.1 / -0.3 |  |
| MES | 5 | eod * | +0.023 | +0.011 .. +0.035 | +0.0006 | 0.00014 / 0.00016 / 0.0023 | 0.00391 | 0.99 | 0.056 | 15/16 | +0.014 | +0.031 | False | +0.6 / +3.8 |  |
| MES | 15 | h1 | -0.001 | -0.008 .. +0.006 | -0.0006 | 0.74 / 0.74 / 0.76 | 0.771 |  |  | 10/16 | -0.005 | +0.003 |  | -0.3 / -0.3 |  |
| MES | 15 | h2 | +0.003 | -0.006 .. +0.011 | +0.0009 | 0.55 / 0.56 / 0.6 | 0.59 |  |  | 9/16 | -0.001 | +0.006 |  | +0.5 / +0.6 |  |
| MES | 15 | h4 | +0.002 | -0.008 .. +0.011 | +0.0003 | 0.76 / 0.76 / 0.81 | 0.811 |  |  | 8/16 | -0.005 | +0.008 |  | +0.2 / +0.3 | 0.017 |
| MES | 15 | h8 | +0.002 | -0.009 .. +0.014 | +0.0004 | 0.7 / 0.7 / 0.76 | 0.766 |  |  | 7/16 | -0.006 | +0.011 |  | +0.2 / +0.4 |  |
| MES | 15 | h16 | +0.004 | -0.009 .. +0.017 | +0.0004 | 0.54 / 0.56 / 0.6 | 0.604 |  |  | 9/16 | -0.008 | +0.016 |  | +0.3 / +0.6 |  |
| MES | 15 | eod * | +0.010 | -0.007 .. +0.026 | +0.0004 | 0.25 / 0.27 / 0.35 | 0.347 | 1 | 1 | 9/16 | -0.008 | +0.027 | False | +0.2 / +1.2 |  |
| MES | 60 | h1 | -0.002 | -0.018 .. +0.015 | -0.0007 | 0.84 / 0.84 / 0.84 | 0.833 |  |  | 8/16 | -0.013 | +0.010 |  | -0.2 / -0.2 |  |
| MES | 60 | h2 * | -0.009 | -0.028 .. +0.009 | -0.0032 | 0.32 / 0.33 / 0.35 | 0.35 | 1 | 1 | 9/16 | -0.019 | +0.000 | False | -0.8 / -1.0 |  |
| MES | 60 | h4 | -0.001 | -0.023 .. +0.020 | -0.0003 | 0.89 / 0.9 / 0.9 | 0.903 |  |  | 7/16 | -0.026 | +0.023 |  | -0.1 / -0.1 | 0.032 |
| MES | 60 | h8 | -0.001 | -0.024 .. +0.023 | -0.0001 | 0.95 / 0.95 / 0.95 | 0.95 |  |  | 9/16 | -0.023 | +0.021 |  | -0.0 / -0.1 |  |
| MES | 60 | h16 | -0.007 | -0.032 .. +0.017 | -0.0010 | 0.56 / 0.56 / 0.58 | 0.588 |  |  | 9/16 | -0.020 | +0.006 |  | -0.3 / -0.6 |  |
| MES | 60 | eod | -0.007 | -0.032 .. +0.017 | -0.0009 | 0.57 / 0.56 / 0.59 | 0.59 |  |  | 10/16 | -0.019 | +0.005 |  | -0.3 / -0.6 |  |
| MNQ | 5 | h1 | -0.001 | -0.005 .. +0.003 | -0.0006 | 0.53 / 0.55 / 0.64 | 0.655 |  |  | 7/16 | -0.007 | +0.004 |  | -0.6 / -0.6 |  |
| MNQ | 5 | h2 | -0.001 | -0.006 .. +0.005 | -0.0003 | 0.73 / 0.72 / 0.82 | 0.819 |  |  | 6/16 | -0.008 | +0.006 |  | -0.3 / -0.4 |  |
| MNQ | 5 | h4 | +0.001 | -0.005 .. +0.008 | +0.0003 | 0.66 / 0.66 / 0.72 | 0.699 |  |  | 8/16 | -0.005 | +0.008 |  | +0.3 / +0.4 | 0.013 |
| MNQ | 5 | h8 | -0.000 | -0.008 .. +0.007 | -0.0000 | 0.94 / 0.94 / 0.99 | 0.984 |  |  | 8/16 | -0.014 | +0.013 |  | -0.0 / -0.1 |  |
| MNQ | 5 | h16 | -0.008 | -0.015 .. +0.000 | -0.0007 | 0.063 / 0.063 / 0.33 | 0.327 |  |  | 10/16 | -0.014 | -0.001 |  | -0.8 / -1.9 |  |
| MNQ | 5 | eod * | +0.059 | +0.043 .. +0.075 | +0.0011 | 7.7e-13 / 1.4e-13 / 0.0015 | 0.00208 | 0.0754 | 0 | 16/16 | +0.035 | +0.083 | True | +1.1 / +7.2 |  |
| MNQ | 15 | h1 * | -0.002 | -0.011 .. +0.006 | -0.0010 | 0.57 / 0.57 / 0.62 | 0.6 | 1 | 1 | 8/16 | -0.013 | +0.008 | False | -0.6 / -0.6 |  |
| MNQ | 15 | h2 | +0.006 | -0.004 .. +0.015 | +0.0013 | 0.23 / 0.25 / 0.44 | 0.416 |  |  | 10/16 | -0.007 | +0.018 |  | +0.9 / +1.2 |  |
| MNQ | 15 | h4 | -0.002 | -0.012 .. +0.009 | -0.0002 | 0.76 / 0.77 / 0.89 | 0.89 |  |  | 7/16 | -0.012 | +0.009 |  | -0.2 / -0.3 | 0.025 |
| MNQ | 15 | h8 | +0.001 | -0.013 .. +0.015 | +0.0001 | 0.88 / 0.87 / 0.93 | 0.924 |  |  | 9/16 | -0.011 | +0.013 |  | +0.1 / +0.2 |  |
| MNQ | 15 | h16 | +0.005 | -0.012 .. +0.021 | +0.0004 | 0.58 / 0.59 / 0.72 | 0.721 |  |  | 10/16 | -0.005 | +0.014 |  | +0.2 / +0.6 |  |
| MNQ | 15 | eod | +0.018 | -0.003 .. +0.039 | +0.0005 | 0.091 / 0.091 / 0.54 | 0.532 |  |  | 12/16 | -0.014 | +0.049 |  | +0.4 / +1.7 |  |
| MNQ | 60 | h1 | -0.009 | -0.028 .. +0.011 | -0.0038 | 0.39 / 0.4 / 0.38 | 0.372 |  |  | 8/16 | -0.020 | +0.003 |  | -0.9 / -0.9 |  |
| MNQ | 60 | h2 | -0.002 | -0.023 .. +0.020 | -0.0005 | 0.88 / 0.88 / 0.88 | 0.882 |  |  | 10/16 | +0.004 | -0.007 |  | -0.1 / -0.2 |  |
| MNQ | 60 | h4 | -0.012 | -0.038 .. +0.013 | -0.0028 | 0.33 / 0.35 / 0.34 | 0.343 |  |  | 9/16 | -0.028 | +0.003 |  | -0.7 / -1.0 | 0.036 |
| MNQ | 60 | h8 | +0.004 | -0.022 .. +0.031 | +0.0007 | 0.76 / 0.77 / 0.78 | 0.766 |  |  | 8/16 | -0.028 | +0.036 |  | +0.2 / +0.3 |  |
| MNQ | 60 | h16 | +0.008 | -0.019 .. +0.035 | +0.0010 | 0.55 / 0.56 / 0.58 | 0.587 |  |  | 8/16 | -0.010 | +0.026 |  | +0.3 / +0.6 |  |
| MNQ | 60 | eod * | +0.020 | -0.007 .. +0.047 | +0.0024 | 0.14 / 0.15 / 0.17 | 0.166 | 1 | 1 | 11/16 | +0.000 | +0.040 | False | +0.7 / +1.5 |  |
| MYM | 5 | h1 | -0.001 | -0.007 .. +0.006 | -0.0003 | 0.84 / 0.84 / 0.92 | 0.921 |  |  | 3/8 | n/a | -0.001 |  | -0.2 / -0.2 |  |
| MYM | 5 | h2 | -0.001 | -0.008 .. +0.006 | -0.0002 | 0.87 / 0.87 / 0.97 | 0.966 |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.2 |  |
| MYM | 5 | h4 | +0.000 | -0.008 .. +0.009 | +0.0000 | 0.96 / 0.96 / 0.93 | 0.942 |  |  | 5/8 | n/a | +0.000 |  | +0.0 / +0.0 | 0.016 |
| MYM | 5 | h8 | +0.004 | -0.005 .. +0.013 | +0.0005 | 0.38 / 0.37 / 0.68 | 0.666 |  |  | 6/8 | n/a | +0.004 |  | +0.5 / +0.9 |  |
| MYM | 5 | h16 | +0.008 | -0.004 .. +0.019 | +0.0007 | 0.18 / 0.16 / 0.48 | 0.477 |  |  | 5/8 | n/a | +0.008 |  | +0.6 / +1.3 |  |
| MYM | 5 | eod * | +0.055 | +0.035 .. +0.075 | +0.0011 | 3.9e-08 / 1.1e-07 / 0.033 | 0.0332 | 1 | 0.001 | 8/8 | n/a | +0.055 | True | +0.8 / +5.5 |  |
| MYM | 15 | h1 | +0.001 | -0.010 .. +0.013 | +0.0004 | 0.85 / 0.85 / 0.88 | 0.864 |  |  | 4/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 15 | h2 | -0.007 | -0.020 .. +0.006 | -0.0015 | 0.32 / 0.34 / 0.57 | 0.557 |  |  | 4/8 | n/a | -0.007 |  | -0.8 / -1.0 |  |
| MYM | 15 | h4 | +0.005 | -0.009 .. +0.020 | +0.0007 | 0.47 / 0.5 / 0.79 | 0.756 |  |  | 4/8 | n/a | +0.005 |  | +0.4 / +0.7 | 0.035 |
| MYM | 15 | h8 | -0.006 | -0.025 .. +0.014 | -0.0006 | 0.57 / 0.54 / 0.76 | 0.733 |  |  | 5/8 | n/a | -0.006 |  | -0.3 / -0.6 |  |
| MYM | 15 | h16 | +0.002 | -0.019 .. +0.024 | +0.0002 | 0.84 / 0.84 / 0.92 | 0.916 |  |  | 4/8 | n/a | +0.002 |  | +0.1 / +0.2 |  |
| MYM | 15 | eod * | +0.021 | -0.006 .. +0.048 | +0.0007 | 0.13 / 0.12 / 0.64 | 0.631 | 1 | 1 | 6/8 | n/a | +0.021 | False | +0.3 / +1.5 |  |
| MYM | 60 | h1 | +0.009 | -0.018 .. +0.036 | +0.0046 | 0.49 / 0.5 / 0.46 | 0.462 |  |  | 5/8 | n/a | +0.009 |  | +0.7 / +0.7 |  |
| MYM | 60 | h2 | -0.001 | -0.030 .. +0.029 | -0.0001 | 0.97 / 0.97 / 0.97 | 0.972 |  |  | 6/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MYM | 60 | h4 * | +0.024 | -0.009 .. +0.056 | +0.0056 | 0.15 / 0.19 / 0.19 | 0.189 | 1 | 1 | 7/8 | n/a | +0.024 | False | +0.9 / +1.4 | 0.049 |
| MYM | 60 | h8 | +0.020 | -0.016 .. +0.057 | +0.0035 | 0.27 / 0.27 / 0.3 | 0.289 |  |  | 6/8 | n/a | +0.020 |  | +0.6 / +1.1 |  |
| MYM | 60 | h16 | +0.000 | -0.035 .. +0.036 | +0.0001 | 0.99 / 0.99 / 1 | 0.999 |  |  | 4/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 60 | eod | +0.006 | -0.030 .. +0.041 | +0.0007 | 0.75 / 0.76 / 0.79 | 0.798 |  |  | 4/8 | n/a | +0.006 |  | +0.1 / +0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.006 | -0.009 .. -0.003 | -1.2% | -0.008 | 0.00021 | 0.0399 | 11/16 |
| MES | 5 | h2 | -0.006 | -0.010 .. -0.001 | -0.8% | -0.013 | 0.011 |  | 10/16 |
| MES | 5 | h4 | -0.000 | -0.007 .. +0.007 | -0.0% | -0.014 | 0.98 |  | 6/16 |
| MES | 5 | h8 | +0.009 | -0.002 .. +0.020 | +0.6% | -0.011 | 0.21 |  | 10/16 |
| MES | 5 | h16 | +0.010 | -0.007 .. +0.027 | +0.5% | -0.009 | 0.26 |  | 12/16 |
| MES | 5 | eod | -0.041 | -0.181 .. +0.099 | -0.4% | +0.051 | 0.57 |  | 9/16 |
| MES | 15 | h1 | +0.004 | -0.002 .. +0.009 | +0.7% | +0.013 | 0.59 |  | 9/16 |
| MES | 15 | h2 | +0.006 | -0.003 .. +0.015 | +0.8% | +0.018 | 0.61 |  | 8/16 |
| MES | 15 | h4 * | +0.010 | -0.004 .. +0.025 | +1.0% | +0.017 | 0.36 | 1 | 10/16 |
| MES | 15 | h8 | +0.010 | -0.013 .. +0.033 | +0.7% | +0.014 | 0.48 |  | 11/16 |
| MES | 15 | h16 | +0.010 | -0.024 .. +0.045 | +0.5% | +0.024 | 0.8 |  | 8/16 |
| MES | 15 | eod | -0.043 | -0.173 .. +0.086 | -0.8% | -0.006 | 0.51 |  | 9/16 |
| MES | 60 | h1 * | +0.012 | +0.000 .. +0.023 | +2.3% | +0.044 | 0.1 | 1 | 12/16 |
| MES | 60 | h2 | +0.015 | -0.002 .. +0.032 | +2.1% | +0.055 | 0.35 |  | 12/16 |
| MES | 60 | h4 | +0.015 | -0.008 .. +0.039 | +1.4% | +0.061 | 0.58 |  | 11/16 |
| MES | 60 | h8 | +0.036 | -0.001 .. +0.074 | +2.4% | +0.086 | 0.14 |  | 10/16 |
| MES | 60 | h16 | +0.027 | -0.022 .. +0.077 | +1.3% | +0.075 | 0.36 |  | 11/16 |
| MES | 60 | eod | +0.025 | -0.029 .. +0.079 | +1.1% | +0.076 | 0.38 |  | 9/16 |
| MNQ | 5 | h1 | -0.002 | -0.005 .. +0.002 | -0.3% | -0.001 | 0.38 |  | 9/16 |
| MNQ | 5 | h2 | -0.002 | -0.009 .. +0.005 | -0.2% | -0.001 | 0.6 |  | 8/16 |
| MNQ | 5 | h4 | +0.004 | -0.008 .. +0.017 | +0.4% | +0.003 | 0.81 |  | 12/16 |
| MNQ | 5 | h8 * | +0.012 | -0.012 .. +0.036 | +0.8% | +0.009 | 0.32 | 1 | 12/16 |
| MNQ | 5 | h16 | +0.016 | -0.028 .. +0.059 | +0.6% | +0.019 | 0.48 |  | 12/16 |
| MNQ | 5 | eod | +0.096 | -0.147 .. +0.340 | +0.8% | +0.335 | 0.51 |  | 12/16 |
| MNQ | 15 | h1 | +0.004 | -0.002 .. +0.011 | +0.8% | +0.017 | 0.88 |  | 11/16 |
| MNQ | 15 | h2 * | +0.008 | -0.005 .. +0.020 | +1.0% | +0.019 | 0.79 | 1 | 11/16 |
| MNQ | 15 | h4 | +0.007 | -0.021 .. +0.035 | +0.6% | +0.017 | 0.96 |  | 13/16 |
| MNQ | 15 | h8 | +0.005 | -0.043 .. +0.053 | +0.3% | +0.005 | 0.9 |  | 10/16 |
| MNQ | 15 | h16 | +0.010 | -0.043 .. +0.063 | +0.4% | -0.009 | 0.9 |  | 9/16 |
| MNQ | 15 | eod | -0.007 | -0.216 .. +0.202 | -0.1% | +0.016 | 0.95 |  | 7/16 |
| MNQ | 60 | h1 * | +0.008 | -0.005 .. +0.020 | +1.5% | +0.046 | 0.31 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.004 | -0.016 .. +0.023 | +0.5% | +0.051 | 1 |  | 9/16 |
| MNQ | 60 | h4 | +0.007 | -0.022 .. +0.037 | +0.7% | +0.052 | 0.75 |  | 9/16 |
| MNQ | 60 | h8 | +0.006 | -0.039 .. +0.051 | +0.4% | +0.051 | 0.81 |  | 9/16 |
| MNQ | 60 | h16 | -0.005 | -0.057 .. +0.047 | -0.2% | +0.046 | 0.92 |  | 7/16 |
| MNQ | 60 | eod | -0.007 | -0.059 .. +0.046 | -0.3% | +0.045 | 0.93 |  | 7/16 |
| MYM | 5 | h1 | -0.000 | -0.007 .. +0.006 | -0.1% | +0.001 | 0.91 |  | 3/8 |
| MYM | 5 | h2 | -0.001 | -0.012 .. +0.010 | -0.2% | -0.004 | 0.82 |  | 3/8 |
| MYM | 5 | h4 | -0.005 | -0.026 .. +0.017 | -0.4% | -0.006 | 0.68 |  | 4/8 |
| MYM | 5 | h8 | +0.009 | -0.028 .. +0.047 | +0.6% | +0.001 | 0.76 |  | 6/8 |
| MYM | 5 | h16 | +0.013 | -0.041 .. +0.067 | +0.5% | -0.003 | 0.64 |  | 7/8 |
| MYM | 5 | eod * | +0.102 | -0.187 .. +0.391 | +0.9% | +0.232 | 0.49 | 1 | 7/8 |
| MYM | 15 | h1 | +0.002 | -0.009 .. +0.012 | +0.4% | +0.008 | 0.72 |  | 4/8 |
| MYM | 15 | h2 | +0.002 | -0.017 .. +0.021 | +0.3% | +0.004 | 0.81 |  | 3/8 |
| MYM | 15 | h4 | -0.001 | -0.036 .. +0.035 | -0.0% | -0.003 | 0.98 |  | 4/8 |
| MYM | 15 | h8 | +0.001 | -0.053 .. +0.056 | +0.1% | -0.014 | 0.96 |  | 5/8 |
| MYM | 15 | h16 | +0.001 | -0.093 .. +0.095 | +0.0% | -0.032 | 0.98 |  | 6/8 |
| MYM | 15 | eod * | -0.119 | -0.381 .. +0.143 | -2.0% | -0.096 | 0.38 | 1 | 4/8 |
| MYM | 60 | h1 | +0.004 | -0.014 .. +0.023 | +0.9% | +0.031 | 0.91 |  | 4/8 |
| MYM | 60 | h2 | -0.001 | -0.029 .. +0.028 | -0.1% | +0.032 | 0.96 |  | 5/8 |
| MYM | 60 | h4 | -0.005 | -0.044 .. +0.035 | -0.4% | +0.029 | 0.82 |  | 5/8 |
| MYM | 60 | h8 * | +0.028 | -0.030 .. +0.086 | +1.8% | +0.055 | 0.47 | 1 | 5/8 |
| MYM | 60 | h16 | -0.000 | -0.077 .. +0.076 | -0.0% | +0.058 | 1 |  | 4/8 |
| MYM | 60 | eod | -0.003 | -0.078 .. +0.072 | -0.1% | +0.062 | 0.95 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.16 pts | -0.39 .. +0.08 | 0.28 |
| MES | 15 | +0.06 pts | -0.32 .. +0.45 | 0.74 |
| MES | 60 | +0.35 pts | -0.42 .. +1.12 | 0.44 |
| MNQ | 5 | -0.07 pts | -0.29 .. +0.15 | 0.57 |
| MNQ | 15 | +0.15 pts | -0.23 .. +0.53 | 0.45 |
| MNQ | 60 | +0.29 pts | -0.53 .. +1.12 | 0.66 |
| MYM | 5 | +0.06 pts | -0.24 .. +0.36 | 0.69 |
| MYM | 15 | -0.11 pts | -0.68 .. +0.46 | 0.7 |
| MYM | 60 | +0.82 pts | -0.24 .. +1.88 | 0.18 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 147680 | +0.014 | 0.350 | +0.10 | -3.40 | -3.43 | -3.36 | -3.51 |
| MES | 5 | h2 | event | against signal | 147680 | +0.017 | 0.350 | +0.15 | -3.35 | -3.40 | -3.30 | -3.51 |
| MES | 5 | h4 | event | against signal | 147680 | +0.018 | 0.350 | +0.13 | -3.37 | -3.41 | -3.33 | -3.53 |
| MES | 5 | h8 | event | against signal | 147680 | +0.016 | 0.350 | +0.10 | -3.40 | -3.40 | -3.39 | -3.54 |
| MES | 5 | h16 | event | against signal | 147680 | +0.016 | 0.350 | +0.11 | -3.39 | -3.42 | -3.36 | -3.54 |
| MES | 5 | eod | event | with signal | 147680 | -0.017 | 0.350 | -0.06 | -3.56 | -3.57 | -3.54 | -3.13 |
| MES | 15 | h1 | event | against signal | 46344 | +0.009 | 0.200 | +0.03 | -3.47 | -3.40 | -3.54 | -3.61 |
| MES | 15 | h2 | event | with signal | 46344 | -0.007 | 0.200 | -0.10 | -3.60 | -3.55 | -3.67 | -3.44 |
| MES | 15 | h4 | event | with signal | 46344 | -0.008 | 0.200 | -0.06 | -3.56 | -3.54 | -3.58 | -3.39 |
| MES | 15 | h8 | event | with signal | 46344 | -0.010 | 0.200 | -0.02 | -3.52 | -3.57 | -3.46 | -3.31 |
| MES | 15 | h16 | event | with signal | 46344 | -0.014 | 0.200 | -0.14 | -3.64 | -3.65 | -3.62 | -3.32 |
| MES | 15 | eod | event | with signal | 46344 | -0.009 | 0.200 | +0.15 | -3.35 | -3.53 | -3.16 | -3.04 |
| MES | 60 | h1 | event | against signal | 10648 | +0.002 | 0.095 | +0.02 | -3.48 | -3.43 | -3.54 | -3.47 |
| MES | 60 | h2 | event | against signal | 10648 | +0.012 | 0.095 | +0.11 | -3.39 | -3.32 | -3.48 | -3.47 |
| MES | 60 | h4 | event | against signal | 10648 | +0.007 | 0.095 | -0.20 | -3.70 | -3.11 | -4.34 | -3.84 |
| MES | 60 | h8 | event | against signal | 10648 | +0.009 | 0.095 | +0.18 | -3.32 | -3.06 | -3.60 | -3.55 |
| MES | 60 | h16 | event | against signal | 10648 | +0.006 | 0.095 | -0.17 | -3.67 | -3.44 | -3.91 | -3.53 |
| MES | 60 | eod | event | against signal | 10648 | +0.009 | 0.095 | -0.21 | -3.71 | -3.41 | -4.04 | -3.69 |
| MNQ | 5 | h1 | event | against signal | 142956 | +0.006 | 0.139 | +0.02 | -1.98 | -1.96 | -2.00 | -2.05 |
| MNQ | 5 | h2 | event | against signal | 142956 | +0.009 | 0.139 | +0.07 | -1.93 | -1.95 | -1.91 | -2.06 |
| MNQ | 5 | h4 | event | with signal | 142956 | -0.005 | 0.139 | -0.01 | -2.01 | -2.03 | -1.98 | -1.91 |
| MNQ | 5 | h8 | event | against signal | 142956 | +0.001 | 0.139 | -0.07 | -2.07 | -1.96 | -2.18 | -2.08 |
| MNQ | 5 | h16 | event | against signal | 142956 | +0.008 | 0.139 | +0.07 | -1.93 | -1.97 | -1.89 | -1.93 |
| MNQ | 5 | eod | event | with signal | 142956 | -0.005 | 0.139 | +0.20 | -1.80 | -2.00 | -1.59 | -0.84 |
| MNQ | 15 | h1 | event | against signal | 44956 | +0.006 | 0.078 | +0.03 | -1.97 | -1.89 | -2.06 | -2.06 |
| MNQ | 15 | h2 | event | with signal | 44956 | +0.004 | 0.078 | +0.12 | -1.88 | -2.02 | -1.74 | -1.85 |
| MNQ | 15 | h4 | event | against signal | 44956 | +0.002 | 0.078 | +0.13 | -1.87 | -1.99 | -1.74 | -1.85 |
| MNQ | 15 | h8 | event | with signal | 44956 | +0.004 | 0.078 | +0.04 | -1.96 | -2.03 | -1.90 | -2.07 |
| MNQ | 15 | h16 | event | with signal | 44956 | -0.002 | 0.078 | -0.17 | -2.17 | -2.02 | -2.32 | -2.01 |
| MNQ | 15 | eod | event | with signal | 44956 | +0.003 | 0.078 | +0.72 | -1.28 | -1.93 | -0.62 | -0.94 |
| MNQ | 60 | h1 | event | against signal | 10180 | +0.008 | 0.037 | +0.05 | -1.95 | -1.90 | -1.99 | -1.93 |
| MNQ | 60 | h2 | event | against signal | 10180 | +0.005 | 0.037 | -0.08 | -2.08 | -2.27 | -1.87 | -2.22 |
| MNQ | 60 | h4 | event | against signal | 10180 | +0.018 | 0.037 | -0.01 | -2.01 | -1.68 | -2.35 | -2.25 |
| MNQ | 60 | h8 | event | with signal | 10180 | -0.003 | 0.037 | +1.27 | -0.73 | -2.27 | +0.86 | -0.45 |
| MNQ | 60 | h16 | event | with signal | 10180 | +0.009 | 0.037 | +2.12 | +0.12 | -1.71 | +2.02 | -0.08 |
| MNQ | 60 | eod | event | with signal | 10180 | +0.017 | 0.037 | +2.54 | +0.54 | -1.70 | +2.85 | +0.54 |
| MYM | 5 | h1 | event | against signal | 72449 | +0.008 | 0.179 | +0.09 | -1.91 | +nan | -1.91 | -2.00 |
| MYM | 5 | h2 | event | against signal | 72449 | +0.011 | 0.179 | +0.13 | -1.87 | +nan | -1.87 | -1.99 |
| MYM | 5 | h4 | event | with signal | 72449 | -0.013 | 0.179 | -0.11 | -2.11 | +nan | -2.11 | -1.96 |
| MYM | 5 | h8 | event | with signal | 72449 | -0.013 | 0.179 | -0.14 | -2.14 | +nan | -2.14 | -1.94 |
| MYM | 5 | h16 | event | with signal | 72449 | -0.017 | 0.179 | -0.13 | -2.13 | +nan | -2.13 | -1.85 |
| MYM | 5 | eod | event | with signal | 72449 | -0.010 | 0.179 | -0.06 | -2.06 | +nan | -2.06 | -1.31 |
| MYM | 15 | h1 | event | with signal | 22616 | -0.005 | 0.100 | -0.02 | -2.02 | +nan | -2.02 | -1.90 |
| MYM | 15 | h2 | event | against signal | 22616 | +0.013 | 0.100 | +0.24 | -1.76 | +nan | -1.76 | -1.88 |
| MYM | 15 | h4 | event | with signal | 22616 | +0.001 | 0.100 | +0.05 | -1.95 | +nan | -1.95 | -1.86 |
| MYM | 15 | h8 | event | against signal | 22616 | +0.014 | 0.100 | +0.24 | -1.76 | +nan | -1.76 | -1.92 |
| MYM | 15 | h16 | event | with signal | 22616 | -0.006 | 0.100 | -0.22 | -2.22 | +nan | -2.22 | -2.07 |
| MYM | 15 | eod | event | with signal | 22616 | -0.005 | 0.100 | -0.04 | -2.04 | +nan | -2.04 | -1.60 |
| MYM | 60 | h1 | event | with signal | 5137 | +0.010 | 0.048 | +0.83 | -1.17 | +nan | -1.17 | -1.20 |
| MYM | 60 | h2 | event | against signal | 5137 | +0.007 | 0.048 | +0.16 | -1.84 | +nan | -1.84 | -2.08 |
| MYM | 60 | h4 | event | with signal | 5137 | +0.015 | 0.048 | +0.82 | -1.18 | +nan | -1.18 | -0.85 |
| MYM | 60 | h8 | event | with signal | 5137 | +0.007 | 0.048 | +0.44 | -1.56 | +nan | -1.56 | -1.06 |
| MYM | 60 | h16 | event | with signal | 5137 | -0.003 | 0.048 | +0.02 | -1.98 | +nan | -1.98 | -1.92 |
| MYM | 60 | eod | event | with signal | 5137 | +0.002 | 0.048 | +0.56 | -1.44 | +nan | -1.44 | -1.36 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.507 | -0.556 | -0.633 | -0.711 | -0.818 | +0.000 | -0.044 | -0.047 | -0.048 | -0.047 | -0.049 |
| MES | 15 | -0.560 | -0.592 | -0.675 | -0.756 | -0.853 | +0.000 | -0.018 | -0.015 | -0.018 | -0.020 | -0.022 |
| MES | 60 | -0.736 | -0.697 | -0.750 | -0.842 | -0.934 | +0.000 | -0.002 | -0.014 | -0.014 | -0.031 | -0.001 |
| MNQ | 5 | -0.559 | -0.611 | -0.693 | -0.783 | -0.877 | +0.000 | -0.020 | -0.023 | -0.018 | -0.015 | -0.020 |
| MNQ | 15 | -0.609 | -0.640 | -0.724 | -0.816 | -0.906 | +0.000 | -0.008 | +0.002 | -0.005 | +0.003 | -0.001 |
| MNQ | 60 | -0.752 | -0.742 | -0.796 | -0.897 | -1.003 | +0.000 | -0.008 | -0.003 | -0.017 | -0.040 | +0.105 |
| MYM | 5 | -0.538 | -0.587 | -0.680 | -0.763 | -0.847 | +0.000 | -0.014 | -0.016 | -0.017 | -0.015 | -0.017 |
| MYM | 15 | -0.593 | -0.631 | -0.713 | -0.807 | -0.886 | +0.000 | -0.002 | -0.010 | +0.003 | -0.009 | +0.002 |
| MYM | 60 | -0.732 | -0.718 | -0.797 | -0.874 | -0.962 | +0.000 | +0.010 | -0.005 | +0.009 | -0.025 | -0.070 |

## Calibration

- MES 5-min: 1036147 bars, 147680 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342094 bars, 46344 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83335 bars, 10648 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034398 bars, 142956 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341938 bars, 44956 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83333 bars, 10180 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518977 bars, 72449 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171365 bars, 22616 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41615 bars, 5137 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
