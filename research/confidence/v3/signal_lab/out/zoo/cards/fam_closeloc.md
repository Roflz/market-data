# Impact card: fam_closeloc

any closeloc pattern, textbook direction (both sides) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect +0.005 average bars (~$0.08 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.0291, replicated in the other half=False, 14 of 16 years); best leg (event, with signal) grosses $+0.16 and nets $-3.34 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 1% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.004 R20, CONFIRMED, q=0.0476, 11 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.17 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.210 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: POSSIBLE direction effect +0.008 average bars (~$0.22 per micro at 2018-25 bar sizes) over the next 1 bar (15 min) (in the signal's direction), not confirmed (q=0.0196, replicated in the other half=False, 14 of 16 years); best leg (event, with signal) grosses $+0.26 and nets $-3.24 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.31 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.125 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.015 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.024 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.15).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.14 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.005 R20 over the next 4 bars (20 min), p=0.32; we would catch an effect of 0.008 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.008 R20, CONFIRMED, q=0.00305, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.076 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.002 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.016 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.68 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.043 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.010 R20 over the next 2 bars (2 h), p=0.56; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.016 R20, possible, q=0.0624, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.92 at recent bar sizes, 90% range up to $3.40); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.003 R20 over the next 1 bar (5 min), p=0.51; we would catch an effect of 0.012 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.4).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.11 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.170 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.008 R20 over the next 1 bar (15 min), p=0.16; we would catch an effect of 0.022 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.37 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.095 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.007 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.47 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.047 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.005 | +0.002 .. +0.008 | +0.0056 | 0.00015 / 4.3e-05 / 1.8e-05 | 0.00026 | 0.0291 | 0.06 | 14/16 | +0.006 | +0.004 | False | +4.5 / +3.8 |  |
| MES | 5 | h2 | +0.005 | +0.001 .. +0.008 | +0.0038 | 0.0062 / 0.0043 / 0.0042 | 0.00573 |  |  | 12/16 | +0.007 | +0.003 |  | +3.1 / +2.7 |  |
| MES | 5 | h4 | -0.000 | -0.005 .. +0.004 | -0.0002 | 0.86 / 0.86 / 0.85 | 0.853 |  |  | 8/16 | -0.000 | -0.000 |  | -0.2 / -0.2 | 0.007 |
| MES | 5 | h8 | -0.005 | -0.011 .. +0.002 | -0.0017 | 0.15 / 0.17 / 0.2 | 0.213 |  |  | 10/16 | -0.000 | -0.009 |  | -1.5 / -1.4 |  |
| MES | 5 | h16 | -0.003 | -0.012 .. +0.006 | -0.0007 | 0.54 / 0.56 / 0.59 | 0.575 |  |  | 8/16 | +0.005 | -0.011 |  | -0.6 / -0.6 |  |
| MES | 5 | eod | +0.038 | -0.015 .. +0.091 | +0.0019 | 0.16 / 0.17 / 0.17 | 0.169 |  |  | 11/16 | +0.032 | +0.044 |  | +1.7 / +1.4 |  |
| MES | 15 | h1 * | +0.008 | +0.004 .. +0.011 | +0.0086 | 3.6e-05 / 4.3e-05 / 0.00011 | 0.00026 | 0.0196 | 0.016 | 14/16 | +0.008 | +0.008 | False | +4.0 / +4.1 |  |
| MES | 15 | h2 | +0.002 | -0.003 .. +0.008 | +0.0017 | 0.42 / 0.42 / 0.45 | 0.445 |  |  | 10/16 | +0.003 | +0.001 |  | +0.8 / +0.8 |  |
| MES | 15 | h4 | -0.000 | -0.008 .. +0.008 | -0.0001 | 0.96 / 0.96 / 0.97 | 0.976 |  |  | 9/16 | +0.001 | -0.002 |  | -0.1 / -0.1 | 0.013 |
| MES | 15 | h8 | +0.001 | -0.011 .. +0.013 | +0.0004 | 0.87 / 0.87 / 0.87 | 0.874 |  |  | 9/16 | +0.007 | -0.005 |  | +0.2 / +0.2 |  |
| MES | 15 | h16 | +0.002 | -0.016 .. +0.019 | +0.0004 | 0.86 / 0.86 / 0.86 | 0.868 |  |  | 7/16 | +0.020 | -0.017 |  | +0.2 / +0.2 |  |
| MES | 15 | eod | +0.033 | -0.011 .. +0.078 | +0.0031 | 0.15 / 0.14 / 0.18 | 0.178 |  |  | 10/16 | +0.062 | +0.005 |  | +1.6 / +1.5 |  |
| MES | 60 | h1 | +0.003 | -0.005 .. +0.010 | +0.0031 | 0.47 / 0.48 / 0.49 | 0.486 |  |  | 11/16 | +0.008 | -0.002 |  | +0.7 / +0.7 |  |
| MES | 60 | h2 | -0.001 | -0.011 .. +0.010 | -0.0006 | 0.9 / 0.9 / 0.91 | 0.907 |  |  | 8/16 | +0.003 | -0.004 |  | -0.1 / -0.1 |  |
| MES | 60 | h4 | +0.004 | -0.011 .. +0.019 | +0.0022 | 0.59 / 0.59 / 0.63 | 0.613 |  |  | 9/16 | +0.014 | -0.006 |  | +0.5 / +0.5 | 0.024 |
| MES | 60 | h8 | +0.003 | -0.016 .. +0.023 | +0.0014 | 0.73 / 0.74 / 0.77 | 0.749 |  |  | 10/16 | +0.017 | -0.010 |  | +0.3 / +0.3 |  |
| MES | 60 | h16 * | +0.015 | -0.011 .. +0.040 | +0.0045 | 0.27 / 0.27 / 0.33 | 0.336 | 1 | 1 | 11/16 | +0.024 | +0.005 | False | +1.0 / +1.1 |  |
| MES | 60 | eod | +0.012 | -0.016 .. +0.039 | +0.0034 | 0.4 / 0.41 / 0.46 | 0.462 |  |  | 11/16 | +0.017 | +0.006 |  | +0.8 / +0.8 |  |
| MNQ | 5 | h1 | +0.003 | -0.000 .. +0.005 | +0.0025 | 0.058 / 0.047 / 0.058 | 0.0583 |  |  | 10/16 | +0.005 | +0.000 |  | +2.2 / +1.9 |  |
| MNQ | 5 | h2 | -0.000 | -0.004 .. +0.004 | -0.0000 | 1 / 1 / 0.98 | 0.979 |  |  | 9/16 | +0.005 | -0.005 |  | -0.0 / -0.0 |  |
| MNQ | 5 | h4 * | -0.005 | -0.010 .. -0.001 | -0.0022 | 0.022 / 0.032 / 0.1 | 0.101 | 1 | 0.974 | 12/16 | -0.001 | -0.010 | False | -2.3 / -2.3 | 0.008 |
| MNQ | 5 | h8 | -0.008 | -0.015 .. -0.001 | -0.0023 | 0.017 / 0.024 / 0.089 | 0.0914 |  |  | 12/16 | -0.001 | -0.015 |  | -2.5 / -2.4 |  |
| MNQ | 5 | h16 | -0.005 | -0.016 .. +0.005 | -0.0010 | 0.3 / 0.31 / 0.43 | 0.424 |  |  | 9/16 | -0.000 | -0.010 |  | -1.1 / -1.0 |  |
| MNQ | 5 | eod | +0.009 | -0.050 .. +0.069 | +0.0004 | 0.75 / 0.76 / 0.77 | 0.769 |  |  | 7/16 | +0.058 | -0.038 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h1 * | +0.002 | -0.001 .. +0.006 | +0.0022 | 0.18 / 0.2 / 0.33 | 0.334 | 1 | 1 | 10/16 | +0.007 | -0.002 | False | +1.2 / +1.3 |  |
| MNQ | 15 | h2 | -0.003 | -0.008 .. +0.002 | -0.0016 | 0.26 / 0.28 / 0.49 | 0.5 |  |  | 11/16 | +0.002 | -0.008 |  | -1.0 / -1.1 |  |
| MNQ | 15 | h4 | -0.005 | -0.013 .. +0.003 | -0.0016 | 0.24 / 0.24 / 0.49 | 0.5 |  |  | 10/16 | -0.002 | -0.008 |  | -1.2 / -1.2 | 0.016 |
| MNQ | 15 | h8 | -0.004 | -0.017 .. +0.008 | -0.0010 | 0.5 / 0.5 / 0.65 | 0.652 |  |  | 10/16 | +0.003 | -0.012 |  | -0.7 / -0.7 |  |
| MNQ | 15 | h16 | -0.004 | -0.022 .. +0.014 | -0.0008 | 0.66 / 0.66 / 0.73 | 0.723 |  |  | 9/16 | +0.018 | -0.026 |  | -0.4 / -0.4 |  |
| MNQ | 15 | eod | -0.000 | -0.048 .. +0.048 | -0.0000 | 0.99 / 0.99 / 1 | 0.995 |  |  | 7/16 | +0.048 | -0.048 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h1 | -0.006 | -0.014 .. +0.001 | -0.0069 | 0.11 / 0.11 / 0.13 | 0.127 |  |  | 10/16 | -0.003 | -0.010 |  | -1.6 / -1.6 |  |
| MNQ | 60 | h2 * | -0.010 | -0.021 .. +0.001 | -0.0074 | 0.075 / 0.088 / 0.11 | 0.113 | 1 | 1 | 10/16 | -0.005 | -0.015 | False | -1.7 / -1.8 |  |
| MNQ | 60 | h4 | -0.010 | -0.026 .. +0.006 | -0.0051 | 0.24 / 0.23 / 0.28 | 0.279 |  |  | 10/16 | +0.003 | -0.022 |  | -1.2 / -1.2 | 0.025 |
| MNQ | 60 | h8 | -0.018 | -0.040 .. +0.005 | -0.0068 | 0.13 / 0.12 / 0.16 | 0.154 |  |  | 10/16 | -0.004 | -0.031 |  | -1.5 / -1.5 |  |
| MNQ | 60 | h16 | -0.020 | -0.048 .. +0.009 | -0.0057 | 0.18 / 0.18 / 0.23 | 0.233 |  |  | 9/16 | -0.009 | -0.030 |  | -1.3 / -1.3 |  |
| MNQ | 60 | eod | -0.021 | -0.051 .. +0.010 | -0.0058 | 0.18 / 0.18 / 0.23 | 0.238 |  |  | 9/16 | -0.006 | -0.035 |  | -1.3 / -1.3 |  |
| MYM | 5 | h1 * | +0.003 | -0.000 .. +0.007 | +0.0031 | 0.076 / 0.052 / 0.12 | 0.129 | 1 | 1 | 5/8 | n/a | +0.003 | False | +2.1 / +1.8 |  |
| MYM | 5 | h2 | +0.003 | -0.002 .. +0.008 | +0.0018 | 0.22 / 0.19 / 0.4 | 0.393 |  |  | 5/8 | n/a | +0.003 |  | +1.4 / +1.2 |  |
| MYM | 5 | h4 | +0.003 | -0.003 .. +0.010 | +0.0012 | 0.3 / 0.29 / 0.57 | 0.562 |  |  | 5/8 | n/a | +0.003 |  | +1.1 / +1.0 | 0.012 |
| MYM | 5 | h8 | -0.001 | -0.011 .. +0.009 | -0.0003 | 0.82 / 0.81 / 0.82 | 0.818 |  |  | 5/8 | n/a | -0.001 |  | -0.3 / -0.2 |  |
| MYM | 5 | h16 | +0.001 | -0.012 .. +0.015 | +0.0003 | 0.84 / 0.85 / 0.92 | 0.926 |  |  | 4/8 | n/a | +0.001 |  | +0.2 / +0.2 |  |
| MYM | 5 | eod | +0.025 | -0.047 .. +0.097 | +0.0011 | 0.5 / 0.51 / 0.56 | 0.541 |  |  | 5/8 | n/a | +0.025 |  | +0.7 / +0.7 |  |
| MYM | 15 | h1 * | +0.008 | +0.002 .. +0.013 | +0.0071 | 0.009 / 0.0087 / 0.027 | 0.0279 | 1 | 0.816 | 6/8 | n/a | +0.008 | False | +2.8 / +2.6 |  |
| MYM | 15 | h2 | +0.005 | -0.004 .. +0.013 | +0.0025 | 0.28 / 0.27 / 0.44 | 0.452 |  |  | 4/8 | n/a | +0.005 |  | +1.2 / +1.1 |  |
| MYM | 15 | h4 | +0.003 | -0.009 .. +0.016 | +0.0011 | 0.58 / 0.57 / 0.73 | 0.723 |  |  | 3/8 | n/a | +0.003 |  | +0.6 / +0.5 | 0.022 |
| MYM | 15 | h8 | +0.003 | -0.014 .. +0.019 | +0.0007 | 0.76 / 0.76 / 0.84 | 0.826 |  |  | 4/8 | n/a | +0.003 |  | +0.3 / +0.3 |  |
| MYM | 15 | h16 | -0.003 | -0.027 .. +0.022 | -0.0004 | 0.84 / 0.85 / 0.89 | 0.888 |  |  | 5/8 | n/a | -0.003 |  | -0.2 / -0.2 |  |
| MYM | 15 | eod | +0.019 | -0.046 .. +0.084 | +0.0014 | 0.57 / 0.57 / 0.67 | 0.68 |  |  | 5/8 | n/a | +0.019 |  | +0.6 / +0.6 |  |
| MYM | 60 | h1 | -0.003 | -0.016 .. +0.009 | -0.0036 | 0.6 / 0.59 / 0.58 | 0.585 |  |  | 6/8 | n/a | -0.003 |  | -0.6 / -0.5 |  |
| MYM | 60 | h2 * | -0.007 | -0.023 .. +0.009 | -0.0051 | 0.42 / 0.42 / 0.43 | 0.423 | 1 | 1 | 4/8 | n/a | -0.007 | False | -0.8 / -0.8 |  |
| MYM | 60 | h4 | -0.001 | -0.023 .. +0.020 | -0.0006 | 0.91 / 0.92 / 0.92 | 0.913 |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.1 | 0.035 |
| MYM | 60 | h8 | +0.003 | -0.027 .. +0.033 | +0.0011 | 0.85 / 0.85 / 0.87 | 0.865 |  |  | 5/8 | n/a | +0.003 |  | +0.2 / +0.2 |  |
| MYM | 60 | h16 | +0.005 | -0.035 .. +0.045 | +0.0015 | 0.81 / 0.81 / 0.82 | 0.811 |  |  | 4/8 | n/a | +0.005 |  | +0.2 / +0.2 |  |
| MYM | 60 | eod | +0.005 | -0.036 .. +0.045 | +0.0013 | 0.83 / 0.83 / 0.84 | 0.832 |  |  | 4/8 | n/a | +0.005 |  | +0.2 / +0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.004 | +0.002 .. +0.007 | +0.9% | +0.016 | 0.00025 | 0.0476 | 11/16 |
| MES | 5 | h2 | +0.002 | -0.002 .. +0.005 | +0.2% | +0.010 | 0.32 |  | 10/16 |
| MES | 5 | h4 | -0.000 | -0.006 .. +0.006 | -0.0% | +0.004 | 0.98 |  | 7/16 |
| MES | 5 | h8 | -0.004 | -0.016 .. +0.007 | -0.3% | -0.009 | 0.48 |  | 7/16 |
| MES | 5 | h16 | -0.012 | -0.030 .. +0.006 | -0.6% | -0.027 | 0.18 |  | 9/16 |
| MES | 5 | eod | -0.107 | -0.296 .. +0.081 | -1.1% | -0.256 | 0.26 |  | 8/16 |
| MES | 15 | h1 | +0.001 | -0.003 .. +0.005 | +0.1% | +0.004 | 0.83 |  | 8/16 |
| MES | 15 | h2 * | +0.003 | -0.004 .. +0.011 | +0.5% | +0.004 | 0.39 | 1 | 11/16 |
| MES | 15 | h4 | +0.002 | -0.013 .. +0.017 | +0.2% | +0.001 | 0.78 |  | 11/16 |
| MES | 15 | h8 | +0.002 | -0.021 .. +0.026 | +0.2% | -0.009 | 0.93 |  | 10/16 |
| MES | 15 | h16 | +0.004 | -0.033 .. +0.040 | +0.2% | -0.030 | 0.85 |  | 12/16 |
| MES | 15 | eod | -0.033 | -0.207 .. +0.142 | -0.6% | -0.092 | 0.71 |  | 6/16 |
| MES | 60 | h1 * | -0.009 | -0.016 .. -0.001 | -1.7% | -0.007 | 0.025 | 1 | 12/16 |
| MES | 60 | h2 | -0.010 | -0.020 .. +0.000 | -1.3% | -0.010 | 0.061 |  | 9/16 |
| MES | 60 | h4 | -0.009 | -0.023 .. +0.006 | -0.8% | -0.012 | 0.24 |  | 11/16 |
| MES | 60 | h8 | -0.012 | -0.031 .. +0.007 | -0.8% | -0.018 | 0.23 |  | 9/16 |
| MES | 60 | h16 | -0.009 | -0.034 .. +0.016 | -0.4% | -0.017 | 0.52 |  | 7/16 |
| MES | 60 | eod | -0.007 | -0.033 .. +0.018 | -0.3% | -0.017 | 0.77 |  | 7/16 |
| MNQ | 5 | h1 * | +0.008 | +0.005 .. +0.012 | +1.6% | +0.025 | 1.3e-05 | 0.00305 | 13/16 |
| MNQ | 5 | h2 | +0.005 | -0.002 .. +0.013 | +0.7% | +0.018 | 0.18 |  | 13/16 |
| MNQ | 5 | h4 | +0.001 | -0.016 .. +0.018 | +0.1% | +0.011 | 0.91 |  | 11/16 |
| MNQ | 5 | h8 | -0.003 | -0.039 .. +0.032 | -0.2% | -0.002 | 0.85 |  | 3/16 |
| MNQ | 5 | h16 | -0.007 | -0.071 .. +0.058 | -0.3% | -0.026 | 0.84 |  | 4/16 |
| MNQ | 5 | eod | -0.138 | -0.494 .. +0.218 | -1.1% | -0.449 | 0.45 |  | 6/16 |
| MNQ | 15 | h1 | +0.000 | -0.006 .. +0.006 | +0.0% | +0.002 | 1 |  | 8/16 |
| MNQ | 15 | h2 * | -0.006 | -0.024 .. +0.011 | -0.8% | -0.007 | 0.47 | 1 | 6/16 |
| MNQ | 15 | h4 | -0.007 | -0.050 .. +0.037 | -0.6% | -0.015 | 0.76 |  | 3/16 |
| MNQ | 15 | h8 | -0.007 | -0.075 .. +0.060 | -0.4% | -0.037 | 0.83 |  | 3/16 |
| MNQ | 15 | h16 | +0.004 | -0.068 .. +0.076 | +0.2% | -0.062 | 0.93 |  | 12/16 |
| MNQ | 15 | eod | -0.058 | -0.373 .. +0.257 | -0.9% | -0.134 | 0.72 |  | 6/16 |
| MNQ | 60 | h1 * | -0.016 | -0.023 .. -0.008 | -3.0% | -0.020 | 0.00034 | 0.0624 | 14/16 |
| MNQ | 60 | h2 | -0.012 | -0.023 .. -0.002 | -1.6% | -0.024 | 0.056 |  | 13/16 |
| MNQ | 60 | h4 | -0.014 | -0.030 .. +0.002 | -1.2% | -0.027 | 0.23 |  | 10/16 |
| MNQ | 60 | h8 | -0.017 | -0.038 .. +0.004 | -1.1% | -0.033 | 0.19 |  | 8/16 |
| MNQ | 60 | h16 | -0.020 | -0.048 .. +0.007 | -0.9% | -0.027 | 0.26 |  | 11/16 |
| MNQ | 60 | eod | -0.027 | -0.055 .. +0.002 | -1.2% | -0.033 | 0.18 |  | 12/16 |
| MYM | 5 | h1 * | +0.006 | -0.000 .. +0.012 | +1.1% | +0.018 | 0.067 | 1 | 5/8 |
| MYM | 5 | h2 | +0.002 | -0.012 .. +0.015 | +0.2% | +0.009 | 0.82 |  | 6/8 |
| MYM | 5 | h4 | -0.005 | -0.038 .. +0.028 | -0.4% | -0.004 | 0.77 |  | 2/8 |
| MYM | 5 | h8 | -0.011 | -0.074 .. +0.051 | -0.7% | -0.026 | 0.72 |  | 2/8 |
| MYM | 5 | h16 | -0.021 | -0.107 .. +0.065 | -0.9% | -0.060 | 0.63 |  | 2/8 |
| MYM | 5 | eod | -0.172 | -0.567 .. +0.222 | -1.5% | -0.261 | 0.4 |  | 4/8 |
| MYM | 15 | h1 | -0.001 | -0.010 .. +0.008 | -0.2% | +0.001 | 0.83 |  | 2/8 |
| MYM | 15 | h2 | -0.004 | -0.028 .. +0.019 | -0.6% | -0.011 | 0.72 |  | 3/8 |
| MYM | 15 | h4 | -0.006 | -0.057 .. +0.045 | -0.5% | -0.024 | 0.82 |  | 2/8 |
| MYM | 15 | h8 | -0.023 | -0.103 .. +0.056 | -1.4% | -0.068 | 0.57 |  | 3/8 |
| MYM | 15 | h16 | -0.039 | -0.183 .. +0.105 | -1.6% | -0.118 | 0.6 |  | 2/8 |
| MYM | 15 | eod * | -0.142 | -0.522 .. +0.238 | -2.4% | -0.183 | 0.47 | 1 | 3/8 |
| MYM | 60 | h1 | +0.002 | -0.008 .. +0.013 | +0.5% | +0.004 | 0.9 |  | 4/8 |
| MYM | 60 | h2 | -0.004 | -0.019 .. +0.011 | -0.5% | -0.000 | 0.62 |  | 5/8 |
| MYM | 60 | h4 * | -0.012 | -0.034 .. +0.010 | -1.1% | -0.011 | 0.28 | 1 | 6/8 |
| MYM | 60 | h8 | -0.001 | -0.030 .. +0.028 | -0.1% | -0.012 | 0.94 |  | 4/8 |
| MYM | 60 | h16 | +0.006 | -0.028 .. +0.041 | +0.3% | -0.007 | 0.98 |  | 4/8 |
| MYM | 60 | eod | +0.003 | -0.035 .. +0.041 | +0.1% | -0.010 | 0.97 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.31 pts | +0.14 .. +0.48 | 0.0032 |
| MES | 15 | +0.44 pts | +0.21 .. +0.67 | 0.00081 |
| MES | 60 | +0.08 pts | -0.38 .. +0.54 | 0.74 |
| MNQ | 5 | +0.19 pts | +0.03 .. +0.35 | 0.037 |
| MNQ | 15 | +0.07 pts | -0.16 .. +0.29 | 0.63 |
| MNQ | 60 | -0.25 pts | -0.73 .. +0.23 | 0.36 |
| MYM | 5 | +0.11 pts | -0.11 .. +0.34 | 0.38 |
| MYM | 15 | +0.46 pts | +0.17 .. +0.75 | 0.0047 |
| MYM | 60 | -0.29 pts | -0.85 .. +0.26 | 0.39 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 418769 | +0.015 | 0.286 | +0.16 | -3.34 | -3.39 | -3.30 | -3.46 |
| MES | 5 | h2 | event | with signal | 418769 | +0.019 | 0.286 | +0.22 | -3.28 | -3.34 | -3.23 | -3.46 |
| MES | 5 | h4 | event | against signal | 418769 | -0.014 | 0.286 | -0.15 | -3.65 | -3.60 | -3.69 | -3.47 |
| MES | 5 | h8 | event | against signal | 418769 | -0.008 | 0.286 | -0.07 | -3.57 | -3.57 | -3.58 | -3.41 |
| MES | 5 | h16 | event | against signal | 418769 | -0.010 | 0.286 | -0.06 | -3.56 | -3.60 | -3.53 | -3.39 |
| MES | 5 | eod | event | with signal | 418769 | +0.022 | 0.286 | +0.14 | -3.36 | -3.50 | -3.24 | -3.29 |
| MES | 15 | h1 | event | with signal | 149647 | +0.015 | 0.174 | +0.26 | -3.24 | -3.34 | -3.15 | -3.39 |
| MES | 15 | h2 | event | with signal | 149647 | +0.011 | 0.174 | +0.16 | -3.34 | -3.41 | -3.29 | -3.52 |
| MES | 15 | h4 | event | against signal | 149647 | -0.007 | 0.174 | -0.07 | -3.57 | -3.55 | -3.59 | -3.41 |
| MES | 15 | h8 | event | with signal | 149647 | +0.008 | 0.174 | +0.09 | -3.41 | -3.46 | -3.36 | -3.57 |
| MES | 15 | h16 | event | with signal | 149647 | +0.007 | 0.174 | +0.06 | -3.44 | -3.42 | -3.46 | -3.59 |
| MES | 15 | eod | event | with signal | 149647 | +0.007 | 0.174 | +0.08 | -3.42 | -3.45 | -3.39 | -3.06 |
| MES | 60 | h1 | event | with signal | 37869 | +0.002 | 0.091 | +0.06 | -3.44 | -3.41 | -3.47 | -3.42 |
| MES | 60 | h2 | event | against signal | 37869 | +0.001 | 0.091 | -0.02 | -3.52 | -3.50 | -3.54 | -3.50 |
| MES | 60 | h4 | event | with signal | 37869 | +0.003 | 0.091 | +0.06 | -3.44 | -3.31 | -3.57 | -3.47 |
| MES | 60 | h8 | event | with signal | 37869 | +0.001 | 0.091 | -0.33 | -3.83 | -3.50 | -4.15 | -3.83 |
| MES | 60 | h16 | event | with signal | 37869 | -0.000 | 0.091 | -0.43 | -3.93 | -3.65 | -4.19 | -3.48 |
| MES | 60 | eod | event | with signal | 37869 | -0.001 | 0.091 | -0.43 | -3.93 | -3.61 | -4.23 | -3.59 |
| MNQ | 5 | h1 | event | with signal | 475265 | +0.007 | 0.125 | +0.10 | -1.90 | -1.94 | -1.87 | -1.97 |
| MNQ | 5 | h2 | event | against signal | 475265 | -0.007 | 0.125 | -0.10 | -2.10 | -2.08 | -2.11 | -1.98 |
| MNQ | 5 | h4 | event | against signal | 475265 | +0.001 | 0.125 | +0.03 | -1.97 | -2.03 | -1.92 | -1.90 |
| MNQ | 5 | h8 | event | against signal | 475265 | +0.011 | 0.125 | +0.12 | -1.88 | -2.00 | -1.77 | -1.91 |
| MNQ | 5 | h16 | event | against signal | 475265 | +0.011 | 0.125 | +0.16 | -1.84 | -1.96 | -1.73 | -1.92 |
| MNQ | 5 | eod | event | with signal | 475265 | -0.020 | 0.125 | +0.00 | -2.00 | -1.97 | -2.03 | -1.78 |
| MNQ | 15 | h1 | event | with signal | 159728 | +0.005 | 0.073 | +0.09 | -1.91 | -1.93 | -1.90 | -1.99 |
| MNQ | 15 | h2 | event | against signal | 159728 | +0.002 | 0.073 | +0.08 | -1.92 | -2.01 | -1.83 | -1.89 |
| MNQ | 15 | h4 | event | against signal | 159728 | +0.007 | 0.073 | +0.11 | -1.89 | -1.93 | -1.85 | -1.92 |
| MNQ | 15 | h8 | event | against signal | 159728 | +0.013 | 0.073 | +0.30 | -1.70 | -1.88 | -1.51 | -1.88 |
| MNQ | 15 | h16 | event | against signal | 159728 | +0.012 | 0.073 | +0.39 | -1.61 | -1.92 | -1.28 | -1.73 |
| MNQ | 15 | eod | event | against signal | 159728 | +0.038 | 0.073 | +0.50 | -1.50 | -1.98 | -1.01 | -2.13 |
| MNQ | 60 | h1 | event | against signal | 38446 | +0.009 | 0.037 | +0.45 | -1.55 | -1.83 | -1.26 | -1.66 |
| MNQ | 60 | h2 | event | against signal | 38446 | +0.013 | 0.037 | +0.61 | -1.39 | -1.81 | -0.96 | -1.45 |
| MNQ | 60 | h4 | event | against signal | 38446 | +0.014 | 0.037 | +0.95 | -1.05 | -1.96 | -0.11 | -1.12 |
| MNQ | 60 | h8 | event | against signal | 38446 | +0.026 | 0.037 | +1.92 | -0.08 | -1.49 | +1.39 | -0.25 |
| MNQ | 60 | h16 | event | against signal | 38446 | +0.039 | 0.037 | +2.55 | +0.55 | -1.24 | +2.40 | -0.09 |
| MNQ | 60 | eod | event | against signal | 38446 | +0.039 | 0.037 | +2.81 | +0.81 | -1.36 | +3.05 | +0.26 |
| MYM | 5 | h1 | event | with signal | 258360 | +0.010 | 0.170 | +0.11 | -1.89 | +nan | -1.89 | -1.97 |
| MYM | 5 | h2 | event | with signal | 258360 | +0.011 | 0.170 | +0.15 | -1.85 | +nan | -1.85 | -1.95 |
| MYM | 5 | h4 | event | with signal | 258360 | +0.012 | 0.170 | +0.12 | -1.88 | +nan | -1.88 | -1.99 |
| MYM | 5 | h8 | event | against signal | 258360 | -0.008 | 0.170 | -0.10 | -2.10 | +nan | -2.10 | -1.99 |
| MYM | 5 | h16 | event | with signal | 258360 | +0.014 | 0.170 | +0.13 | -1.87 | +nan | -1.87 | -2.02 |
| MYM | 5 | eod | event | with signal | 258360 | +0.042 | 0.170 | +0.22 | -1.78 | +nan | -1.78 | -2.04 |
| MYM | 15 | h1 | event | with signal | 82220 | +0.013 | 0.095 | +0.22 | -1.78 | +nan | -1.78 | -1.88 |
| MYM | 15 | h2 | event | with signal | 82220 | +0.009 | 0.095 | +0.16 | -1.84 | +nan | -1.84 | -1.93 |
| MYM | 15 | h4 | event | with signal | 82220 | +0.005 | 0.095 | +0.07 | -1.93 | +nan | -1.93 | -1.98 |
| MYM | 15 | h8 | event | with signal | 82220 | +0.005 | 0.095 | +0.15 | -1.85 | +nan | -1.85 | -1.91 |
| MYM | 15 | h16 | event | against signal | 82220 | +0.004 | 0.095 | -0.12 | -2.12 | +nan | -2.12 | -2.15 |
| MYM | 15 | eod | event | with signal | 82220 | +0.015 | 0.095 | +0.20 | -1.80 | +nan | -1.80 | -1.86 |
| MYM | 60 | h1 | event | against signal | 19205 | +0.004 | 0.047 | +0.03 | -1.97 | +nan | -1.97 | -2.00 |
| MYM | 60 | h2 | event | against signal | 19205 | +0.003 | 0.047 | -0.02 | -2.02 | +nan | -2.02 | -1.84 |
| MYM | 60 | h4 | event | against signal | 19205 | -0.003 | 0.047 | -0.12 | -2.12 | +nan | -2.12 | -1.89 |
| MYM | 60 | h8 | event | with signal | 19205 | +0.007 | 0.047 | -0.14 | -2.14 | +nan | -2.14 | -2.40 |
| MYM | 60 | h16 | event | with signal | 19205 | -0.007 | 0.047 | -0.81 | -2.81 | +nan | -2.81 | -2.46 |
| MYM | 60 | eod | event | with signal | 19205 | -0.007 | 0.047 | -1.00 | -3.00 | +nan | -3.00 | -2.67 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.617 | +0.718 | +0.778 | +0.727 | +0.680 | +0.000 | +0.055 | +0.060 | +0.057 | +0.052 | +0.055 |
| MES | 15 | +0.596 | +0.649 | +0.699 | +0.682 | +0.671 | +0.000 | +0.033 | +0.029 | +0.027 | +0.032 | +0.035 |
| MES | 60 | +1.001 | +0.811 | +0.745 | +0.678 | +0.659 | +0.000 | +0.008 | +0.009 | +0.023 | +0.054 | +0.065 |
| MNQ | 5 | +0.599 | +0.692 | +0.752 | +0.719 | +0.693 | +0.000 | +0.025 | +0.026 | +0.019 | +0.015 | +0.013 |
| MNQ | 15 | +0.605 | +0.648 | +0.692 | +0.680 | +0.672 | +0.000 | +0.014 | +0.007 | +0.003 | +0.001 | +0.010 |
| MNQ | 60 | +1.070 | +0.853 | +0.769 | +0.695 | +0.674 | +0.000 | -0.005 | -0.005 | +0.001 | +0.012 | +0.009 |
| MYM | 5 | +0.549 | +0.630 | +0.684 | +0.667 | +0.658 | +0.000 | +0.024 | +0.026 | +0.028 | +0.022 | +0.029 |
| MYM | 15 | +0.583 | +0.628 | +0.677 | +0.661 | +0.658 | +0.000 | +0.017 | +0.014 | +0.010 | +0.008 | -0.005 |
| MYM | 60 | +1.033 | +0.844 | +0.773 | +0.704 | +0.677 | +0.000 | -0.004 | -0.003 | +0.007 | +0.028 | +0.033 |

## Calibration

- MES 5-min: 1036271 bars, 418769 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 149647 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 37869 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 475265 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 159728 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 38446 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 258360 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 82220 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 19205 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 33083 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
