# Impact card: new_sess_extreme

bar makes a new session high (long) / low (short), at least 1 hour into the session [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.011 R20 over the next 4 bars (20 min), p=0.68; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.051 R20, CONFIRMED, q=9.71e-64, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.60 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.205 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.005 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.035 R20, CONFIRMED, q=6.47e-21, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.04 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.125 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.021).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.10 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: POSSIBLE direction effect +0.031 average bars (~$0.88 per micro at 2018-25 bar sizes) over the next 4 bars (20 min) (in the signal's direction), not confirmed (q=0.0529, replicated in the other half=False, 15 of 16 years); best leg (event, with signal) grosses $+0.25 and nets $-1.75 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 10% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.054 R20, CONFIRMED, q=1.21e-52, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.88 at recent bar sizes, 90% range up to $1.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.012 R20 over the next 1 bar (15 min), p=0.022; we would catch an effect of 0.033 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.037 R20, CONFIRMED, q=1.15e-16, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.54 at recent bar sizes, 90% range up to $1.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.031 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.024 R20, CONFIRMED, q=0.000749, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.85 at recent bar sizes, 90% range up to $3.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.055 R20 over the next 16 bars (80 min), p=0.68; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 5-min size: the market moves 8% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.062 R20, CONFIRMED, q=3.48e-25, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.69 at recent bar sizes, 90% range up to $0.73); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.069 R20 over the next 16 bars (4 h), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MYM 15-min size: the market moves 9% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.050 R20, CONFIRMED, q=2.43e-17, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.45 at recent bar sizes, 90% range up to $1.42); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.034 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.051 R20 or more 80% of the time).
- MYM 60-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.026 R20, CONFIRMED, q=0.0156, 5 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.45 at recent bar sizes, 90% range up to $3.49); about 13.6x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.007 .. +0.003 | -0.0008 | 0.48 / 0.49 / 0.48 | 0.476 |  |  | 9/16 | +0.000 | -0.004 |  | -0.7 / -0.7 |  |
| MES | 5 | h2 | +0.003 | -0.006 .. +0.011 | +0.0008 | 0.56 / 0.55 / 0.53 | 0.533 |  |  | 7/16 | +0.001 | +0.004 |  | +0.6 / +0.6 |  |
| MES | 5 | h4 * | +0.011 | -0.003 .. +0.026 | +0.0025 | 0.11 / 0.11 / 0.11 | 0.113 | 1 | 1 | 10/16 | +0.008 | +0.015 | False | +2.2 / +1.6 | 0.020 |
| MES | 5 | h8 | +0.016 | -0.008 .. +0.039 | +0.0023 | 0.19 / 0.18 / 0.2 | 0.204 |  |  | 11/16 | +0.004 | +0.028 |  | +2.1 / +1.3 |  |
| MES | 5 | h16 | +0.004 | -0.037 .. +0.045 | +0.0004 | 0.86 / 0.85 / 0.86 | 0.859 |  |  | 6/16 | -0.039 | +0.047 |  | +0.4 / +0.2 |  |
| MES | 5 | eod | -0.106 | -0.389 .. +0.176 | -0.0022 | 0.46 / 0.47 / 0.5 | 0.498 |  |  | 9/16 | -0.136 | -0.076 |  | -2.2 / -0.7 |  |
| MES | 15 | h1 * | +0.005 | -0.003 .. +0.013 | +0.0031 | 0.22 / 0.21 / 0.14 | 0.142 | 1 | 1 | 11/16 | +0.004 | +0.006 | False | +1.3 / +1.2 |  |
| MES | 15 | h2 | +0.005 | -0.007 .. +0.017 | +0.0019 | 0.43 / 0.42 / 0.4 | 0.403 |  |  | 11/16 | -0.002 | +0.011 |  | +0.9 / +0.8 |  |
| MES | 15 | h4 | -0.004 | -0.025 .. +0.017 | -0.0011 | 0.72 / 0.71 / 0.7 | 0.692 |  |  | 11/16 | -0.025 | +0.017 |  | -0.5 / -0.4 | 0.028 |
| MES | 15 | h8 | -0.009 | -0.043 .. +0.024 | -0.0019 | 0.58 / 0.57 / 0.57 | 0.567 |  |  | 10/16 | -0.040 | +0.021 |  | -0.9 / -0.6 |  |
| MES | 15 | h16 | -0.021 | -0.069 .. +0.026 | -0.0029 | 0.38 / 0.39 / 0.45 | 0.44 |  |  | 9/16 | -0.059 | +0.016 |  | -1.6 / -0.9 |  |
| MES | 15 | eod | -0.039 | -0.198 .. +0.120 | -0.0021 | 0.63 / 0.63 / 0.67 | 0.667 |  |  | 9/16 | -0.068 | -0.010 |  | -1.2 / -0.5 |  |
| MES | 60 | h1 * | -0.003 | -0.012 .. +0.005 | -0.0034 | 0.46 / 0.46 / 0.46 | 0.468 | 1 | 1 | 9/16 | -0.015 | +0.008 | False | -0.7 / -0.7 |  |
| MES | 60 | h2 | -0.004 | -0.018 .. +0.010 | -0.0028 | 0.58 / 0.58 / 0.61 | 0.612 |  |  | 8/16 | -0.017 | +0.009 |  | -0.6 / -0.6 |  |
| MES | 60 | h4 | -0.005 | -0.027 .. +0.017 | -0.0024 | 0.68 / 0.68 / 0.71 | 0.716 |  |  | 9/16 | -0.018 | +0.009 |  | -0.5 / -0.4 | 0.035 |
| MES | 60 | h8 | -0.006 | -0.044 .. +0.031 | -0.0025 | 0.74 / 0.75 / 0.76 | 0.754 |  |  | 11/16 | -0.014 | +0.001 |  | -0.5 / -0.3 |  |
| MES | 60 | h16 | -0.006 | -0.059 .. +0.048 | -0.0013 | 0.84 / 0.84 / 0.85 | 0.84 |  |  | 9/16 | -0.008 | -0.003 |  | -0.4 / -0.2 |  |
| MES | 60 | eod | -0.006 | -0.062 .. +0.051 | -0.0015 | 0.84 / 0.84 / 0.84 | 0.838 |  |  | 9/16 | -0.004 | -0.008 |  | -0.4 / -0.2 |  |
| MNQ | 5 | h1 | +0.011 | +0.004 .. +0.017 | +0.0040 | 0.0016 / 0.0019 / 0.00048 | 0.000781 |  |  | 13/16 | +0.010 | +0.011 |  | +3.0 / +3.2 |  |
| MNQ | 5 | h2 | +0.016 | +0.006 .. +0.026 | +0.0037 | 0.0013 / 0.00095 / 0.0023 | 0.00365 |  |  | 13/16 | +0.016 | +0.016 |  | +4.0 / +3.2 |  |
| MNQ | 5 | h4 * | +0.031 | +0.017 .. +0.046 | +0.0048 | 1.5e-05 / 2.1e-05 / 0.00073 | 0.00182 | 0.0529 | 0.009 | 15/16 | +0.033 | +0.030 | False | +5.6 / +4.3 | 0.023 |
| MNQ | 5 | h8 | +0.041 | +0.017 .. +0.066 | +0.0043 | 0.00098 / 0.0012 / 0.0099 | 0.0148 |  |  | 12/16 | +0.033 | +0.050 |  | +5.2 / +3.3 |  |
| MNQ | 5 | h16 | +0.029 | -0.016 .. +0.074 | +0.0021 | 0.21 / 0.2 / 0.3 | 0.302 |  |  | 10/16 | +0.007 | +0.050 |  | +2.4 / +1.3 |  |
| MNQ | 5 | eod | -0.169 | -0.508 .. +0.170 | -0.0027 | 0.33 / 0.33 / 0.42 | 0.43 |  |  | 10/16 | -0.299 | -0.039 |  | -2.9 / -1.0 |  |
| MNQ | 15 | h1 * | +0.012 | +0.005 .. +0.019 | +0.0057 | 0.0011 / 0.00094 / 0.0039 | 0.00495 | 0.55 | 0.279 | 12/16 | +0.012 | +0.012 | False | +3.3 / +3.3 |  |
| MNQ | 15 | h2 | +0.016 | +0.004 .. +0.028 | +0.0045 | 0.011 / 0.0088 / 0.039 | 0.0404 |  |  | 11/16 | +0.012 | +0.020 |  | +3.1 / +2.6 |  |
| MNQ | 15 | h4 | +0.011 | -0.013 .. +0.035 | +0.0018 | 0.37 / 0.35 / 0.44 | 0.439 |  |  | 11/16 | +0.002 | +0.020 |  | +1.3 / +0.9 | 0.033 |
| MNQ | 15 | h8 | +0.005 | -0.035 .. +0.044 | +0.0006 | 0.82 / 0.81 / 0.84 | 0.837 |  |  | 8/16 | +0.000 | +0.009 |  | +0.4 / +0.2 |  |
| MNQ | 15 | h16 | -0.011 | -0.068 .. +0.045 | -0.0012 | 0.69 / 0.69 / 0.74 | 0.749 |  |  | 10/16 | -0.048 | +0.025 |  | -0.8 / -0.4 |  |
| MNQ | 15 | eod | +0.050 | -0.131 .. +0.231 | +0.0018 | 0.59 / 0.58 / 0.67 | 0.674 |  |  | 9/16 | -0.039 | +0.139 |  | +1.4 / +0.5 |  |
| MNQ | 60 | h1 | +0.002 | -0.008 .. +0.012 | +0.0016 | 0.72 / 0.7 / 0.7 | 0.696 |  |  | 8/16 | -0.007 | +0.010 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h2 | -0.002 | -0.018 .. +0.014 | -0.0013 | 0.81 / 0.81 / 0.81 | 0.813 |  |  | 8/16 | -0.016 | +0.012 |  | -0.3 / -0.2 |  |
| MNQ | 60 | h4 | +0.001 | -0.024 .. +0.026 | +0.0002 | 0.95 / 0.95 / 0.95 | 0.954 |  |  | 8/16 | -0.022 | +0.023 |  | +0.1 / +0.1 | 0.037 |
| MNQ | 60 | h8 | +0.007 | -0.032 .. +0.046 | +0.0019 | 0.72 / 0.72 / 0.74 | 0.747 |  |  | 8/16 | -0.023 | +0.037 |  | +0.6 / +0.4 |  |
| MNQ | 60 | h16 * | +0.031 | -0.024 .. +0.086 | +0.0075 | 0.27 / 0.27 / 0.31 | 0.308 | 1 | 1 | 8/16 | -0.005 | +0.068 | False | +1.9 / +1.1 |  |
| MNQ | 60 | eod | +0.028 | -0.031 .. +0.086 | +0.0067 | 0.35 / 0.35 / 0.39 | 0.391 |  |  | 9/16 | -0.001 | +0.057 |  | +1.6 / +0.9 |  |
| MYM | 5 | h1 | +0.002 | -0.012 .. +0.016 | +0.0008 | 0.77 / 0.77 / 0.64 | 0.632 |  |  | 4/8 | n/a | +0.002 |  | +0.3 / +0.3 |  |
| MYM | 5 | h2 | -0.008 | -0.021 .. +0.005 | -0.0017 | 0.24 / 0.23 / 0.35 | 0.332 |  |  | 4/8 | n/a | -0.008 |  | -1.4 / -1.2 |  |
| MYM | 5 | h4 | -0.010 | -0.034 .. +0.014 | -0.0012 | 0.43 / 0.4 / 0.58 | 0.547 |  |  | 5/8 | n/a | -0.010 |  | -1.1 / -0.8 | 0.035 |
| MYM | 5 | h8 | -0.028 | -0.064 .. +0.008 | -0.0026 | 0.13 / 0.12 / 0.27 | 0.261 |  |  | 6/8 | n/a | -0.028 |  | -2.6 / -1.5 |  |
| MYM | 5 | h16 * | -0.055 | -0.113 .. +0.004 | -0.0040 | 0.067 / 0.076 / 0.17 | 0.167 | 1 | 1 | 6/8 | n/a | -0.055 | False | -3.5 / -1.8 |  |
| MYM | 5 | eod | -0.356 | -0.881 .. +0.169 | -0.0059 | 0.18 / 0.15 / 0.19 | 0.201 |  |  | 5/8 | n/a | -0.356 |  | -4.5 / -1.3 |  |
| MYM | 15 | h1 | +0.004 | -0.008 .. +0.017 | +0.0021 | 0.52 / 0.5 / 0.5 | 0.489 |  |  | 3/8 | n/a | +0.004 |  | +0.7 / +0.6 |  |
| MYM | 15 | h2 | -0.000 | -0.018 .. +0.018 | -0.0000 | 0.99 / 0.99 / 1 | 0.995 |  |  | 5/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 15 | h4 | -0.016 | -0.044 .. +0.012 | -0.0027 | 0.27 / 0.28 / 0.44 | 0.416 |  |  | 6/8 | n/a | -0.016 |  | -1.5 / -1.1 | 0.045 |
| MYM | 15 | h8 | -0.028 | -0.075 .. +0.018 | -0.0037 | 0.23 / 0.24 / 0.35 | 0.341 |  |  | 6/8 | n/a | -0.028 |  | -1.9 / -1.2 |  |
| MYM | 15 | h16 * | -0.069 | -0.142 .. +0.004 | -0.0064 | 0.064 / 0.07 / 0.22 | 0.225 | 1 | 1 | 6/8 | n/a | -0.069 | False | -3.5 / -1.9 |  |
| MYM | 15 | eod | -0.125 | -0.396 .. +0.147 | -0.0049 | 0.37 / 0.34 / 0.45 | 0.464 |  |  | 5/8 | n/a | -0.125 |  | -2.5 / -0.9 |  |
| MYM | 60 | h1 | +0.002 | -0.011 .. +0.014 | +0.0014 | 0.81 / 0.81 / 0.82 | 0.84 |  |  | 4/8 | n/a | +0.002 |  | +0.2 / +0.2 |  |
| MYM | 60 | h2 | -0.006 | -0.025 .. +0.013 | -0.0034 | 0.55 / 0.57 / 0.59 | 0.592 |  |  | 5/8 | n/a | -0.006 |  | -0.6 / -0.6 |  |
| MYM | 60 | h4 | -0.017 | -0.049 .. +0.016 | -0.0072 | 0.32 / 0.33 / 0.36 | 0.377 |  |  | 5/8 | n/a | -0.017 |  | -1.3 / -1.0 | 0.051 |
| MYM | 60 | h8 * | -0.034 | -0.092 .. +0.023 | -0.0108 | 0.24 / 0.25 / 0.24 | 0.255 | 1 | 1 | 6/8 | n/a | -0.034 | False | -1.9 / -1.2 |  |
| MYM | 60 | h16 | -0.036 | -0.117 .. +0.044 | -0.0086 | 0.37 / 0.36 / 0.37 | 0.371 |  |  | 5/8 | n/a | -0.036 |  | -1.6 / -0.9 |  |
| MYM | 60 | eod | -0.046 | -0.130 .. +0.038 | -0.0106 | 0.28 / 0.27 / 0.29 | 0.291 |  |  | 5/8 | n/a | -0.046 |  | -2.0 / -1.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.051 | +0.046 .. +0.057 | +10.3% | +0.125 | 8e-67 | 9.71e-64 | 16/16 |
| MES | 5 | h2 | +0.053 | +0.045 .. +0.061 | +7.5% | +0.137 | 2.8e-38 |  | 16/16 |
| MES | 5 | h4 | +0.053 | +0.042 .. +0.065 | +5.3% | +0.147 | 3.7e-19 |  | 15/16 |
| MES | 5 | h8 | +0.054 | +0.038 .. +0.071 | +3.8% | +0.146 | 1.3e-10 |  | 14/16 |
| MES | 5 | h16 | +0.061 | +0.035 .. +0.087 | +2.9% | +0.148 | 7.1e-05 |  | 13/16 |
| MES | 5 | eod | +0.030 | -0.132 .. +0.193 | +0.3% | +0.112 | 0.71 |  | 10/16 |
| MES | 15 | h1 * | +0.035 | +0.029 .. +0.042 | +6.9% | +0.093 | 1.1e-23 | 6.47e-21 | 15/16 |
| MES | 15 | h2 | +0.038 | +0.029 .. +0.048 | +5.2% | +0.104 | 8.2e-14 |  | 14/16 |
| MES | 15 | h4 | +0.048 | +0.034 .. +0.061 | +4.5% | +0.113 | 8.6e-09 |  | 14/16 |
| MES | 15 | h8 | +0.065 | +0.043 .. +0.086 | +4.2% | +0.130 | 1.9e-05 |  | 13/16 |
| MES | 15 | h16 | +0.067 | +0.028 .. +0.105 | +2.9% | +0.134 | 0.0009 |  | 14/16 |
| MES | 15 | eod | +0.045 | -0.088 .. +0.179 | +0.8% | +0.146 | 0.51 |  | 12/16 |
| MES | 60 | h1 * | +0.015 | +0.007 .. +0.024 | +2.9% | +0.042 | 0.0035 | 0.533 | 9/16 |
| MES | 60 | h2 | +0.018 | +0.006 .. +0.031 | +2.4% | +0.049 | 0.021 |  | 9/16 |
| MES | 60 | h4 | +0.024 | +0.006 .. +0.043 | +2.2% | +0.054 | 0.048 |  | 10/16 |
| MES | 60 | h8 | +0.029 | +0.006 .. +0.052 | +1.9% | +0.062 | 0.086 |  | 13/16 |
| MES | 60 | h16 | +0.018 | -0.012 .. +0.048 | +0.9% | +0.057 | 0.35 |  | 10/16 |
| MES | 60 | eod | +0.017 | -0.013 .. +0.046 | +0.8% | +0.057 | 0.36 |  | 9/16 |
| MNQ | 5 | h1 * | +0.054 | +0.047 .. +0.060 | +10.0% | +0.126 | 1.1e-55 | 1.21e-52 | 16/16 |
| MNQ | 5 | h2 | +0.056 | +0.047 .. +0.064 | +7.3% | +0.138 | 1.8e-37 |  | 15/16 |
| MNQ | 5 | h4 | +0.060 | +0.046 .. +0.074 | +5.4% | +0.149 | 3.2e-14 |  | 15/16 |
| MNQ | 5 | h8 | +0.058 | +0.032 .. +0.084 | +3.6% | +0.139 | 1.3e-05 |  | 13/16 |
| MNQ | 5 | h16 | +0.073 | +0.032 .. +0.114 | +3.0% | +0.137 | 0.0005 |  | 12/16 |
| MNQ | 5 | eod | -0.117 | -0.382 .. +0.148 | -0.9% | -0.134 | 0.39 |  | 9/16 |
| MNQ | 15 | h1 * | +0.037 | +0.030 .. +0.044 | +6.9% | +0.094 | 2.2e-19 | 1.15e-16 | 15/16 |
| MNQ | 15 | h2 | +0.040 | +0.027 .. +0.052 | +5.1% | +0.101 | 3.5e-07 |  | 14/16 |
| MNQ | 15 | h4 | +0.049 | +0.028 .. +0.070 | +4.3% | +0.111 | 0.0037 |  | 13/16 |
| MNQ | 15 | h8 | +0.083 | +0.048 .. +0.117 | +4.9% | +0.141 | 2.6e-06 |  | 13/16 |
| MNQ | 15 | h16 | +0.085 | +0.029 .. +0.142 | +3.4% | +0.140 | 0.0029 |  | 13/16 |
| MNQ | 15 | eod | +0.045 | -0.173 .. +0.262 | +0.7% | +0.159 | 0.69 |  | 12/16 |
| MNQ | 60 | h1 * | +0.024 | +0.015 .. +0.032 | +4.4% | +0.046 | 3.1e-06 | 0.000749 | 13/16 |
| MNQ | 60 | h2 | +0.025 | +0.012 .. +0.038 | +3.2% | +0.053 | 0.00032 |  | 10/16 |
| MNQ | 60 | h4 | +0.025 | +0.007 .. +0.043 | +2.2% | +0.054 | 0.035 |  | 11/16 |
| MNQ | 60 | h8 | +0.031 | +0.008 .. +0.055 | +1.9% | +0.061 | 0.059 |  | 11/16 |
| MNQ | 60 | h16 | -0.001 | -0.033 .. +0.031 | -0.0% | +0.040 | 0.96 |  | 6/16 |
| MNQ | 60 | eod | -0.001 | -0.032 .. +0.030 | -0.0% | +0.038 | 0.95 |  | 5/16 |
| MYM | 5 | h1 | +0.063 | +0.051 .. +0.075 | +11.8% | +0.132 | 9.8e-22 |  | 8/8 |
| MYM | 5 | h2 * | +0.062 | +0.051 .. +0.073 | +8.1% | +0.145 | 5.2e-28 | 3.48e-25 | 8/8 |
| MYM | 5 | h4 | +0.067 | +0.049 .. +0.086 | +6.1% | +0.153 | 3.5e-13 |  | 8/8 |
| MYM | 5 | h8 | +0.059 | +0.019 .. +0.099 | +3.7% | +0.145 | 0.0042 |  | 6/8 |
| MYM | 5 | h16 | +0.055 | +0.000 .. +0.110 | +2.4% | +0.145 | 0.21 |  | 6/8 |
| MYM | 5 | eod | -0.018 | -0.307 .. +0.270 | -0.2% | +0.009 | 0.9 |  | 4/8 |
| MYM | 15 | h1 * | +0.050 | +0.040 .. +0.060 | +9.4% | +0.109 | 4.6e-20 | 2.43e-17 | 8/8 |
| MYM | 15 | h2 | +0.053 | +0.038 .. +0.068 | +6.9% | +0.121 | 9.8e-10 |  | 8/8 |
| MYM | 15 | h4 | +0.053 | +0.024 .. +0.082 | +4.7% | +0.129 | 0.0031 |  | 8/8 |
| MYM | 15 | h8 | +0.067 | +0.020 .. +0.114 | +4.1% | +0.150 | 0.022 |  | 7/8 |
| MYM | 15 | h16 | +0.035 | -0.072 .. +0.141 | +1.4% | +0.129 | 0.69 |  | 7/8 |
| MYM | 15 | eod | +0.085 | -0.169 .. +0.339 | +1.4% | +0.191 | 0.51 |  | 7/8 |
| MYM | 60 | h1 * | +0.026 | +0.013 .. +0.039 | +4.9% | +0.055 | 7.5e-05 | 0.0156 | 5/8 |
| MYM | 60 | h2 | +0.029 | +0.011 .. +0.048 | +3.8% | +0.065 | 0.0036 |  | 5/8 |
| MYM | 60 | h4 | +0.024 | -0.001 .. +0.049 | +2.2% | +0.075 | 0.28 |  | 7/8 |
| MYM | 60 | h8 | +0.053 | +0.020 .. +0.087 | +3.4% | +0.104 | 0.023 |  | 8/8 |
| MYM | 60 | h16 | +0.030 | -0.011 .. +0.071 | +1.4% | +0.075 | 0.39 |  | 7/8 |
| MYM | 60 | eod | +0.030 | -0.013 .. +0.074 | +1.4% | +0.066 | 0.34 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.02 pts | -0.40 .. +0.35 | 0.92 |
| MES | 15 | -0.05 pts | -0.51 .. +0.42 | 0.84 |
| MES | 60 | -0.52 pts | -1.20 .. +0.15 | 0.13 |
| MNQ | 5 | +0.32 pts | -0.06 .. +0.70 | 0.14 |
| MNQ | 15 | -0.08 pts | -0.55 .. +0.38 | 0.79 |
| MNQ | 60 | -0.40 pts | -1.05 .. +0.25 | 0.23 |
| MYM | 5 | -0.55 pts | -1.09 .. -0.00 | 0.05 |
| MYM | 15 | -0.40 pts | -1.03 .. +0.23 | 0.21 |
| MYM | 60 | -0.46 pts | -1.42 .. +0.50 | 0.35 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 91699 | +0.009 | 0.287 | +0.14 | -3.36 | -3.41 | -3.31 | -3.43 |
| MES | 5 | h2 | event | with signal | 91699 | -0.006 | 0.287 | -0.16 | -3.66 | -3.63 | -3.69 | -3.56 |
| MES | 5 | h4 | event | with signal | 91699 | +0.004 | 0.287 | +0.01 | -3.49 | -3.58 | -3.41 | -3.40 |
| MES | 5 | h8 | event | with signal | 91699 | +0.011 | 0.287 | +0.08 | -3.42 | -3.62 | -3.25 | -3.35 |
| MES | 5 | h16 | event | with signal | 91699 | -0.001 | 0.287 | +0.01 | -3.49 | -3.78 | -3.25 | -3.40 |
| MES | 5 | eod | event | against signal | 91699 | -0.088 | 0.287 | -0.67 | -4.17 | -3.97 | -4.33 | -1.93 |
| MES | 15 | h1 | event | with signal | 61408 | +0.001 | 0.178 | +0.03 | -3.47 | -3.52 | -3.42 | -3.38 |
| MES | 15 | h2 | event | with signal | 61408 | +0.001 | 0.178 | +0.04 | -3.46 | -3.58 | -3.35 | -3.37 |
| MES | 15 | h4 | event | against signal | 61408 | +0.005 | 0.178 | -0.02 | -3.52 | -3.25 | -3.76 | -3.57 |
| MES | 15 | h8 | event | against signal | 61408 | +0.007 | 0.178 | +0.06 | -3.44 | -3.27 | -3.59 | -3.41 |
| MES | 15 | h16 | event | against signal | 61408 | +0.001 | 0.178 | +0.13 | -3.37 | -3.42 | -3.33 | -3.02 |
| MES | 15 | eod | event | against signal | 61408 | -0.060 | 0.178 | -0.54 | -4.04 | -3.85 | -4.20 | -2.22 |
| MES | 60 | h1 | event | against signal | 33696 | +0.003 | 0.093 | +0.01 | -3.49 | -3.33 | -3.65 | -3.48 |
| MES | 60 | h2 | event | against signal | 33696 | +0.003 | 0.093 | +0.11 | -3.39 | -3.29 | -3.48 | -3.39 |
| MES | 60 | h4 | event | against signal | 33696 | +0.003 | 0.093 | +0.24 | -3.26 | -3.35 | -3.18 | -3.25 |
| MES | 60 | h8 | event | against signal | 33696 | +0.002 | 0.093 | -0.07 | -3.57 | -3.75 | -3.39 | -3.50 |
| MES | 60 | h16 | event | against signal | 33696 | -0.009 | 0.093 | -0.89 | -4.39 | -4.26 | -4.52 | -3.95 |
| MES | 60 | eod | event | against signal | 33696 | -0.006 | 0.093 | -0.72 | -4.22 | -4.12 | -4.32 | -3.90 |
| MNQ | 5 | h1 | event | with signal | 102753 | +0.010 | 0.116 | +0.01 | -1.99 | -1.99 | -1.98 | -1.97 |
| MNQ | 5 | h2 | event | with signal | 102753 | +0.016 | 0.116 | +0.06 | -1.94 | -1.99 | -1.90 | -1.92 |
| MNQ | 5 | h4 | event | with signal | 102753 | +0.037 | 0.116 | +0.25 | -1.75 | -1.90 | -1.61 | -1.82 |
| MNQ | 5 | h8 | event | with signal | 102753 | +0.056 | 0.116 | +0.56 | -1.44 | -1.84 | -1.08 | -1.64 |
| MNQ | 5 | h16 | event | with signal | 102753 | +0.055 | 0.116 | +0.66 | -1.34 | -1.80 | -0.92 | -1.68 |
| MNQ | 5 | eod | event | against signal | 102753 | -0.216 | 0.116 | -3.11 | -5.11 | -2.28 | -7.65 | +0.93 |
| MNQ | 15 | h1 | event | with signal | 65989 | +0.010 | 0.072 | +0.15 | -1.85 | -1.90 | -1.80 | -1.78 |
| MNQ | 15 | h2 | event | with signal | 65989 | +0.016 | 0.072 | +0.20 | -1.80 | -1.90 | -1.71 | -1.76 |
| MNQ | 15 | h4 | event | with signal | 65989 | +0.014 | 0.072 | +0.37 | -1.63 | -1.92 | -1.36 | -1.64 |
| MNQ | 15 | h8 | event | with signal | 65989 | +0.017 | 0.072 | +0.40 | -1.60 | -1.82 | -1.39 | -1.81 |
| MNQ | 15 | h16 | event | against signal | 65989 | -0.021 | 0.072 | -0.61 | -2.61 | -2.16 | -3.05 | -1.93 |
| MNQ | 15 | eod | event | with signal | 65989 | +0.176 | 0.072 | +3.19 | +1.19 | -1.65 | +3.89 | -1.67 |
| MNQ | 60 | h1 | event | with signal | 34772 | +0.005 | 0.037 | +0.47 | -1.53 | -1.95 | -1.11 | -1.62 |
| MNQ | 60 | h2 | event | against signal | 34772 | -0.001 | 0.037 | -0.19 | -2.19 | -1.93 | -2.46 | -2.13 |
| MNQ | 60 | h4 | event | with signal | 34772 | +0.007 | 0.037 | +0.50 | -1.50 | -2.12 | -0.88 | -1.63 |
| MNQ | 60 | h8 | event | with signal | 34772 | +0.017 | 0.037 | +1.51 | -0.49 | -1.84 | +0.85 | -0.71 |
| MNQ | 60 | h16 | event | with signal | 34772 | +0.050 | 0.037 | +3.47 | +1.47 | -1.46 | +4.40 | +0.93 |
| MNQ | 60 | eod | event | with signal | 34772 | +0.047 | 0.037 | +2.96 | +0.96 | -1.53 | +3.44 | +0.48 |
| MYM | 5 | h1 | event | with signal | 52212 | -0.002 | 0.159 | -0.06 | -2.06 | +nan | -2.06 | -2.02 |
| MYM | 5 | h2 | event | against signal | 52212 | +0.009 | 0.159 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 5 | h4 | event | against signal | 52212 | +0.003 | 0.159 | -0.13 | -2.13 | +nan | -2.13 | -2.02 |
| MYM | 5 | h8 | event | against signal | 52212 | +0.008 | 0.159 | -0.17 | -2.17 | +nan | -2.17 | -1.88 |
| MYM | 5 | h16 | event | against signal | 52212 | +0.025 | 0.159 | -0.04 | -2.04 | +nan | -2.04 | -1.62 |
| MYM | 5 | eod | event | against signal | 52212 | +0.190 | 0.159 | +1.11 | -0.89 | +nan | -0.89 | +0.94 |
| MYM | 15 | h1 | event | with signal | 33283 | +0.003 | 0.095 | +0.08 | -1.92 | +nan | -1.92 | -1.90 |
| MYM | 15 | h2 | event | against signal | 33283 | -0.001 | 0.095 | -0.11 | -2.11 | +nan | -2.11 | -2.09 |
| MYM | 15 | h4 | event | against signal | 33283 | +0.011 | 0.095 | -0.08 | -2.08 | +nan | -2.08 | -1.97 |
| MYM | 15 | h8 | event | against signal | 33283 | +0.017 | 0.095 | +0.15 | -1.85 | +nan | -1.85 | -1.60 |
| MYM | 15 | h16 | event | against signal | 33283 | +0.049 | 0.095 | +0.93 | -1.07 | +nan | -1.07 | -0.63 |
| MYM | 15 | eod | event | against signal | 33283 | +0.062 | 0.095 | +0.83 | -1.17 | +nan | -1.17 | -0.31 |
| MYM | 60 | h1 | event | with signal | 17283 | +0.003 | 0.047 | +0.06 | -1.94 | +nan | -1.94 | -1.98 |
| MYM | 60 | h2 | event | against signal | 17283 | +0.005 | 0.047 | +0.31 | -1.69 | +nan | -1.69 | -1.73 |
| MYM | 60 | h4 | event | against signal | 17283 | +0.014 | 0.047 | +0.94 | -1.06 | +nan | -1.06 | -1.07 |
| MYM | 60 | h8 | event | against signal | 17283 | +0.027 | 0.047 | +1.00 | -1.00 | +nan | -1.00 | -0.92 |
| MYM | 60 | h16 | event | against signal | 17283 | +0.011 | 0.047 | +0.05 | -1.95 | +nan | -1.95 | -1.22 |
| MYM | 60 | eod | event | against signal | 17283 | +0.021 | 0.047 | +0.26 | -1.74 | +nan | -1.74 | -1.06 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -1.790 | -1.722 | -1.457 | -1.061 | -0.583 | +0.000 | -0.007 | -0.006 | +0.001 | +0.001 | -0.014 |
| MES | 15 | -1.700 | -1.615 | -1.339 | -0.971 | -0.522 | +0.000 | +0.002 | -0.001 | -0.011 | -0.020 | -0.043 |
| MES | 60 | -1.988 | -1.601 | -1.281 | -0.878 | -0.451 | +0.000 | -0.004 | -0.007 | -0.013 | -0.030 | +0.007 |
| MNQ | 5 | -1.913 | -1.837 | -1.554 | -1.125 | -0.610 | +0.000 | +0.008 | +0.012 | +0.027 | +0.038 | +0.031 |
| MNQ | 15 | -1.789 | -1.678 | -1.388 | -1.006 | -0.536 | +0.000 | +0.011 | +0.015 | +0.014 | +0.009 | -0.020 |
| MNQ | 60 | -2.063 | -1.628 | -1.302 | -0.897 | -0.456 | +0.000 | +0.002 | -0.006 | -0.007 | -0.018 | +0.047 |
| MYM | 5 | -1.861 | -1.780 | -1.499 | -1.079 | -0.576 | +0.000 | -0.001 | -0.011 | -0.014 | -0.030 | -0.067 |
| MYM | 15 | -1.769 | -1.665 | -1.357 | -0.974 | -0.514 | +0.000 | +0.004 | +0.001 | -0.009 | -0.025 | -0.067 |
| MYM | 60 | -2.040 | -1.624 | -1.306 | -0.888 | -0.450 | +0.000 | +0.003 | -0.005 | -0.017 | -0.047 | -0.006 |

## Calibration

- MES 5-min: 1032456 bars, 91699 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 338403 bars, 61408 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 79599 bars, 33696 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1030707 bars, 102753 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 338247 bars, 65989 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 79597 bars, 34772 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 517134 bars, 52212 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 169522 bars, 33283 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 39751 bars, 17283 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
