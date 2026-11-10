# Impact card: tod_asia_18_02

bar closes in the asia_18_02 block (ET) vs all other bars [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (5 min), p=0.86; we would catch an effect of 0.016 R20 or more 80% of the time).
- MES 5-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.051 R20, CONFIRMED, q=8.92e-125, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.17 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.330 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.248 R20 over the rest of the session (to 16:45), p=0.015; we would catch an effect of 0.027 R20 or more 80% of the time).
- MES 15-min size: the market moves 48% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.243 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.80 at recent bar sizes, 90% range up to $0.60); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: POSSIBLE direction effect +0.092 average bars (~$5.31 per micro at 2018-25 bar sizes) over the rest of the session (to 16:45) (after the event vs matched non-events), not confirmed (q=0.0416, replicated in the other half=False, 14 of 16 years); best leg (event, long) grosses $+7.10 and nets $+3.60 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 60-min size: the market moves 63% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.323 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.37 at recent bar sizes, 90% range up to $2.82); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.035 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.022 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 9% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.047 R20, CONFIRMED, q=4.44e-91, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.41 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.120 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.286 R20 over the rest of the session (to 16:45), p=0.012; we would catch an effect of 0.030 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 53% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.283 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.92 at recent bar sizes, 90% range up to $1.04); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: moves price up 0.129 average bars (~$12.42 per micro at 2018-25 bar sizes) over the rest of the session (to 16:45) (after the event vs matched non-events), same sign in 15 of 16 years, q=3.06e-05; best leg (event, long) grosses $+8.59 and nets $+6.59 per micro per trade after $2.00 costs -> tradable on its own.
- MNQ 60-min size: the market moves 68% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.359 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+8.89, pessimistic $-0.68) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.042 R20 over the next 4 bars (20 min), p=0.032; we would catch an effect of 0.043 R20 or more 80% of the time).
- MYM 5-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.051 R20, CONFIRMED, q=6.32e-51, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.21 at recent bar sizes, 90% range up to $0.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.244 R20 over the rest of the session (to 16:45), p=0.54; we would catch an effect of 0.053 R20 or more 80% of the time).
- MYM 15-min size: the market moves 52% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.274 R20, CONFIRMED, q=1.35e-280, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.80 at recent bar sizes, 90% range up to $1.34); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.037 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.069 R20 or more 80% of the time).
- MYM 60-min size: the market moves 66% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.344 R20, CONFIRMED, q=1.3e-234, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.05 at recent bar sizes, 90% range up to $2.88); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.002 | -0.005 .. +0.001 | -0.0022 | 0.14 / 0.13 / 0.75 | nan | 1 | 1 | 9/16 | -0.002 | -0.002 | False | -1.4 / -1.5 |  |
| MES | 5 | h2 | -0.002 | -0.008 .. +0.003 | -0.0017 | 0.42 / 0.4 / 0.79 | nan |  |  | 8/16 | -0.002 | -0.002 |  | -1.1 / -0.8 |  |
| MES | 5 | h4 | -0.001 | -0.013 .. +0.010 | -0.0007 | 0.81 / 0.8 / 0.8 | nan |  |  | 8/16 | -0.001 | -0.002 |  | -0.5 / -0.2 | 0.016 |
| MES | 5 | h8 | +0.002 | -0.020 .. +0.024 | +0.0008 | 0.85 / 0.84 / 0.83 | nan |  |  | 8/16 | +0.005 | -0.001 |  | +0.5 / +0.2 |  |
| MES | 5 | h16 | +0.005 | -0.040 .. +0.049 | +0.0012 | 0.83 / 0.83 / 0.84 | nan |  |  | 9/16 | +0.014 | -0.005 |  | +0.8 / +0.2 |  |
| MES | 5 | eod | +0.065 | -0.339 .. +0.469 | +0.0032 | 0.75 / 0.76 / 0.87 | nan |  |  | 9/16 | +0.306 | -0.175 |  | +1.7 / +0.3 |  |
| MES | 15 | h1 | -0.007 | -0.012 .. -0.002 | -0.0046 | 0.0038 / 0.0028 / 0.72 | nan |  |  | 13/16 | -0.006 | -0.008 |  | -2.9 / -2.9 |  |
| MES | 15 | h2 | -0.006 | -0.015 .. +0.003 | -0.0027 | 0.18 / 0.17 / 0.74 | nan |  |  | 9/16 | -0.005 | -0.007 |  | -1.8 / -1.3 |  |
| MES | 15 | h4 | -0.006 | -0.024 .. +0.013 | -0.0016 | 0.55 / 0.55 / 0.76 | nan |  |  | 8/16 | -0.003 | -0.008 |  | -1.1 / -0.6 | 0.027 |
| MES | 15 | h8 | -0.007 | -0.045 .. +0.030 | -0.0015 | 0.7 / 0.7 / 0.87 | nan |  |  | 9/16 | -0.003 | -0.011 |  | -1.0 / -0.4 |  |
| MES | 15 | h16 | +0.002 | -0.072 .. +0.075 | +0.0003 | 0.96 / 0.96 / 0.95 | nan |  |  | 8/16 | -0.002 | +0.006 |  | +0.2 / +0.1 |  |
| MES | 15 | eod * | +0.248 | +0.092 .. +0.405 | +0.0138 | 0.0019 / 0.0026 / 0.95 | nan | 0.41 | 0.421 | 13/16 | +0.285 | +0.212 | False | +7.2 / +3.1 |  |
| MES | 60 | h1 | -0.003 | -0.012 .. +0.006 | -0.0019 | 0.52 / 0.52 / 0.98 | nan |  |  | 9/16 | -0.001 | -0.005 |  | -0.7 / -0.6 |  |
| MES | 60 | h2 | -0.008 | -0.026 .. +0.010 | -0.0034 | 0.4 / 0.4 / 0.98 | nan |  |  | 8/16 | -0.007 | -0.008 |  | -1.2 / -0.8 |  |
| MES | 60 | h4 | -0.009 | -0.042 .. +0.024 | -0.0028 | 0.6 / 0.61 / 1 | nan |  |  | 9/16 | -0.007 | -0.011 |  | -0.9 / -0.5 | 0.048 |
| MES | 60 | h8 | +0.001 | -0.057 .. +0.058 | +0.0001 | 0.99 / 0.99 / 0.96 | nan |  |  | 8/16 | +0.006 | -0.005 |  | +0.0 / +0.0 |  |
| MES | 60 | h16 | +0.045 | -0.008 .. +0.098 | +0.0079 | 0.095 / 0.098 / 0.92 | nan |  |  | 11/16 | +0.064 | +0.026 |  | +2.2 / +1.7 |  |
| MES | 60 | eod * | +0.092 | +0.044 .. +0.140 | +0.0153 | 0.00017 / 0.00022 / 0.91 | nan | 0.0416 | 0.053 | 14/16 | +0.121 | +0.062 | False | +4.1 / +3.8 |  |
| MNQ | 5 | h1 | -0.001 | -0.004 .. +0.002 | -0.0011 | 0.42 / 0.42 / 0.81 | nan |  |  | 8/16 | +0.000 | -0.003 |  | -0.7 / -0.8 |  |
| MNQ | 5 | h2 | +0.001 | -0.006 .. +0.008 | +0.0004 | 0.85 / 0.85 / 0.81 | nan |  |  | 8/16 | +0.004 | -0.003 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h4 | +0.006 | -0.009 .. +0.021 | +0.0023 | 0.43 / 0.42 / 0.81 | nan |  |  | 9/16 | +0.014 | -0.001 |  | +1.5 / +0.8 | 0.022 |
| MNQ | 5 | h8 | +0.016 | -0.013 .. +0.046 | +0.0043 | 0.27 / 0.26 / 0.85 | nan |  |  | 11/16 | +0.035 | -0.002 |  | +2.8 / +1.1 |  |
| MNQ | 5 | h16 * | +0.035 | -0.019 .. +0.090 | +0.0064 | 0.21 / 0.2 / 0.89 | nan | 1 | 1 | 11/16 | +0.074 | -0.003 | False | +4.2 / +1.3 |  |
| MNQ | 5 | eod | +0.173 | -0.399 .. +0.745 | +0.0066 | 0.55 / 0.56 / 0.88 | nan |  |  | 7/16 | +0.828 | -0.477 |  | +3.3 / +0.6 |  |
| MNQ | 15 | h1 | -0.004 | -0.010 .. +0.001 | -0.0022 | 0.1 / 0.11 / 0.65 | nan |  |  | 9/16 | -0.001 | -0.008 |  | -1.5 / -1.6 |  |
| MNQ | 15 | h2 | +0.002 | -0.008 .. +0.012 | +0.0006 | 0.68 / 0.69 / 0.75 | nan |  |  | 9/16 | +0.008 | -0.003 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h4 | +0.012 | -0.009 .. +0.033 | +0.0021 | 0.27 / 0.27 / 0.82 | nan |  |  | 10/16 | +0.022 | +0.002 |  | +1.5 / +1.1 | 0.030 |
| MNQ | 15 | h8 | +0.012 | -0.028 .. +0.052 | +0.0016 | 0.56 / 0.56 / 0.96 | nan |  |  | 10/16 | +0.023 | +0.001 |  | +1.1 / +0.6 |  |
| MNQ | 15 | h16 | +0.044 | -0.041 .. +0.130 | +0.0049 | 0.31 / 0.32 / 0.96 | nan |  |  | 11/16 | +0.043 | +0.046 |  | +3.2 / +1.0 |  |
| MNQ | 15 | eod * | +0.286 | +0.110 .. +0.462 | +0.0110 | 0.0014 / 0.0021 / 0.95 | nan | 0.332 | 0.334 | 12/16 | +0.443 | +0.129 | False | +5.9 / +3.2 |  |
| MNQ | 60 | h1 | +0.002 | -0.007 .. +0.011 | +0.0012 | 0.66 / 0.67 / 0.94 | nan |  |  | 8/16 | +0.004 | -0.000 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h2 | -0.000 | -0.018 .. +0.018 | -0.0000 | 1 / 1 / 0.94 | nan |  |  | 8/16 | +0.001 | -0.001 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h4 | -0.000 | -0.035 .. +0.034 | -0.0001 | 0.99 / 0.99 / 0.96 | nan |  |  | 8/16 | +0.001 | -0.002 |  | -0.0 / -0.0 | 0.050 |
| MNQ | 60 | h8 | +0.010 | -0.050 .. +0.071 | +0.0022 | 0.73 / 0.74 / 0.98 | nan |  |  | 7/16 | +0.022 | -0.001 |  | +0.7 / +0.3 |  |
| MNQ | 60 | h16 | +0.070 | +0.018 .. +0.121 | +0.0114 | 0.0086 / 0.01 / 0.94 | nan |  |  | 12/16 | +0.096 | +0.044 |  | +3.2 / +2.6 |  |
| MNQ | 60 | eod * | +0.129 | +0.083 .. +0.175 | +0.0202 | 3.5e-08 / 1.1e-07 / 0.92 | nan | 3.06e-05 | 0 | 15/16 | +0.168 | +0.090 | True | +5.5 / +5.5 |  |
| MYM | 5 | h1 | +0.003 | -0.001 .. +0.008 | +0.0029 | 0.17 / 0.17 / 0.79 | nan |  |  | 5/8 | n/a | +0.003 |  | +1.4 / +1.4 |  |
| MYM | 5 | h2 | +0.016 | +0.003 .. +0.029 | +0.0083 | 0.014 / 0.013 / 0.84 | nan |  |  | 7/8 | n/a | +0.016 |  | +4.1 / +2.4 |  |
| MYM | 5 | h4 * | +0.042 | +0.013 .. +0.072 | +0.0135 | 0.0053 / 0.0048 / 0.89 | nan | 0.764 | 0.684 | 7/8 | n/a | +0.042 | False | +6.8 / +2.8 | 0.043 |
| MYM | 5 | h8 | +0.078 | +0.023 .. +0.134 | +0.0179 | 0.0053 / 0.0053 / 0.95 | nan |  |  | 7/8 | n/a | +0.078 |  | +8.9 / +2.8 |  |
| MYM | 5 | h16 | +0.104 | +0.015 .. +0.193 | +0.0186 | 0.023 / 0.022 / 0.95 | nan |  |  | 7/8 | n/a | +0.104 |  | +9.0 / +2.3 |  |
| MYM | 5 | eod | +0.225 | -0.600 .. +1.050 | +0.0090 | 0.59 / 0.59 / 0.91 | nan |  |  | 5/8 | n/a | +0.225 |  | +3.2 / +0.5 |  |
| MYM | 15 | h1 | -0.004 | -0.011 .. +0.003 | -0.0022 | 0.25 / 0.25 / 0.74 | nan |  |  | 5/8 | n/a | -0.004 |  | -1.0 / -1.2 |  |
| MYM | 15 | h2 | +0.005 | -0.012 .. +0.023 | +0.0016 | 0.54 / 0.54 / 0.75 | nan |  |  | 4/8 | n/a | +0.005 |  | +0.8 / +0.6 |  |
| MYM | 15 | h4 | +0.016 | -0.021 .. +0.052 | +0.0027 | 0.41 / 0.4 / 0.77 | nan |  |  | 4/8 | n/a | +0.016 |  | +1.4 / +0.8 | 0.053 |
| MYM | 15 | h8 | +0.034 | -0.038 .. +0.106 | +0.0046 | 0.35 / 0.35 / 0.82 | nan |  |  | 5/8 | n/a | +0.034 |  | +2.2 / +0.9 |  |
| MYM | 15 | h16 | +0.111 | -0.049 .. +0.270 | +0.0106 | 0.17 / 0.19 / 0.84 | nan |  |  | 5/8 | n/a | +0.111 |  | +5.1 / +1.4 |  |
| MYM | 15 | eod * | +0.244 | -0.032 .. +0.519 | +0.0096 | 0.083 / 0.09 / 0.99 | nan | 1 | 1 | 7/8 | n/a | +0.244 | False | +3.8 / +1.7 |  |
| MYM | 60 | h1 | -0.004 | -0.017 .. +0.009 | -0.0026 | 0.52 / 0.51 / 0.99 | nan |  |  | 5/8 | n/a | -0.004 |  | -0.6 / -0.7 |  |
| MYM | 60 | h2 | -0.009 | -0.034 .. +0.016 | -0.0038 | 0.48 / 0.48 / 0.98 | nan |  |  | 4/8 | n/a | -0.009 |  | -0.9 / -0.7 |  |
| MYM | 60 | h4 | -0.014 | -0.062 .. +0.034 | -0.0043 | 0.56 / 0.57 / 0.97 | nan |  |  | 4/8 | n/a | -0.014 |  | -1.0 / -0.6 | 0.069 |
| MYM | 60 | h8 | -0.018 | -0.101 .. +0.065 | -0.0039 | 0.67 / 0.68 / 0.99 | nan |  |  | 4/8 | n/a | -0.018 |  | -0.9 / -0.4 |  |
| MYM | 60 | h16 * | -0.037 | -0.115 .. +0.041 | -0.0062 | 0.35 / 0.36 / 0.99 | nan | 1 | 1 | 6/8 | n/a | -0.037 | False | -1.2 / -0.9 |  |
| MYM | 60 | eod | -0.007 | -0.082 .. +0.067 | -0.0012 | 0.84 / 0.85 / 0.98 | nan |  |  | 3/8 | n/a | -0.007 |  | -0.2 / -0.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.051 | -0.055 .. -0.047 | -10.2% | -0.105 | 5.1e-128 | 8.92e-125 | 16/16 |
| MES | 5 | h2 | -0.080 | -0.086 .. -0.073 | -11.3% | -0.158 | 1.5e-114 |  | 16/16 |
| MES | 5 | h4 | -0.126 | -0.138 .. -0.114 | -12.6% | -0.247 | 1.2e-92 |  | 16/16 |
| MES | 5 | h8 | -0.208 | -0.230 .. -0.186 | -14.5% | -0.404 | 1.6e-79 |  | 16/16 |
| MES | 5 | h16 | -0.336 | -0.374 .. -0.298 | -16.0% | -0.656 | 2.9e-66 |  | 16/16 |
| MES | 5 | eod | +1.557 | +1.200 .. +1.914 | +15.6% | +3.194 | 1.3e-17 |  | 14/16 |
| MES | 15 | h1 * | -0.243 | -0.250 .. -0.236 | -47.6% | -0.500 | 0 | 0 | 16/16 |
| MES | 15 | h2 | -0.363 | -0.375 .. -0.352 | -49.8% | -0.739 | 0 |  | 16/16 |
| MES | 15 | h4 | -0.550 | -0.570 .. -0.529 | -52.2% | -1.115 | 0 |  | 16/16 |
| MES | 15 | h8 | -0.772 | -0.808 .. -0.736 | -50.2% | -1.571 | 0 |  | 16/16 |
| MES | 15 | h16 | -1.094 | -1.156 .. -1.032 | -47.9% | -2.224 | 2.8e-259 |  | 16/16 |
| MES | 15 | eod | +0.839 | +0.714 .. +0.965 | +15.3% | +1.780 | 2.8e-39 |  | 16/16 |
| MES | 60 | h1 * | -0.323 | -0.334 .. -0.312 | -63.0% | -0.661 | 0 | 0 | 16/16 |
| MES | 60 | h2 | -0.429 | -0.447 .. -0.411 | -58.1% | -0.870 | 0 |  | 16/16 |
| MES | 60 | h4 | -0.567 | -0.596 .. -0.538 | -53.6% | -1.133 | 0 |  | 16/16 |
| MES | 60 | h8 | -0.613 | -0.656 .. -0.570 | -40.7% | -1.175 | 1.9e-173 |  | 16/16 |
| MES | 60 | h16 | +0.336 | +0.298 .. +0.373 | +16.3% | +0.750 | 1.3e-66 |  | 16/16 |
| MES | 60 | eod | +0.621 | +0.584 .. +0.657 | +28.7% | +1.265 | 1.3e-246 |  | 16/16 |
| MNQ | 5 | h1 * | -0.047 | -0.052 .. -0.043 | -8.8% | -0.097 | 3.3e-94 | 4.44e-91 | 16/16 |
| MNQ | 5 | h2 | -0.074 | -0.083 .. -0.064 | -9.6% | -0.144 | 1.9e-53 |  | 16/16 |
| MNQ | 5 | h4 | -0.119 | -0.137 .. -0.101 | -10.7% | -0.231 | 4.6e-37 |  | 16/16 |
| MNQ | 5 | h8 | -0.209 | -0.246 .. -0.172 | -12.9% | -0.400 | 2.3e-28 |  | 16/16 |
| MNQ | 5 | h16 | -0.370 | -0.438 .. -0.303 | -15.4% | -0.704 | 5.3e-27 |  | 16/16 |
| MNQ | 5 | eod | +1.655 | +1.203 .. +2.107 | +13.2% | +3.263 | 7.2e-13 |  | 12/16 |
| MNQ | 15 | h1 * | -0.283 | -0.290 .. -0.275 | -52.9% | -0.577 | 0 | 0 | 16/16 |
| MNQ | 15 | h2 | -0.431 | -0.447 .. -0.414 | -55.6% | -0.865 | 0 |  | 16/16 |
| MNQ | 15 | h4 | -0.673 | -0.712 .. -0.635 | -59.4% | -1.340 | 1.9e-255 |  | 16/16 |
| MNQ | 15 | h8 | -0.979 | -1.041 .. -0.916 | -58.3% | -1.972 | 8.5e-208 |  | 16/16 |
| MNQ | 15 | h16 | -1.407 | -1.492 .. -1.323 | -55.7% | -2.917 | 3e-235 |  | 16/16 |
| MNQ | 15 | eod | +0.769 | +0.623 .. +0.915 | +12.1% | +1.583 | 6.5e-25 |  | 16/16 |
| MNQ | 60 | h1 * | -0.359 | -0.371 .. -0.348 | -68.0% | -0.726 | 0 | 0 | 16/16 |
| MNQ | 60 | h2 | -0.483 | -0.501 .. -0.464 | -63.0% | -0.970 | 0 |  | 16/16 |
| MNQ | 60 | h4 | -0.649 | -0.679 .. -0.619 | -58.7% | -1.295 | 0 |  | 16/16 |
| MNQ | 60 | h8 | -0.745 | -0.789 .. -0.701 | -47.0% | -1.425 | 1.1e-237 |  | 16/16 |
| MNQ | 60 | h16 | +0.360 | +0.321 .. +0.399 | +16.4% | +0.788 | 2.4e-69 |  | 16/16 |
| MNQ | 60 | eod | +0.641 | +0.604 .. +0.678 | +27.9% | +1.297 | 3.6e-249 |  | 16/16 |
| MYM | 5 | h1 * | -0.051 | -0.057 .. -0.044 | -9.6% | -0.099 | 5.8e-54 | 6.32e-51 | 8/8 |
| MYM | 5 | h2 | -0.088 | -0.102 .. -0.074 | -11.6% | -0.163 | 1.8e-36 |  | 8/8 |
| MYM | 5 | h4 | -0.155 | -0.184 .. -0.125 | -14.1% | -0.282 | 8.3e-25 |  | 8/8 |
| MYM | 5 | h8 | -0.273 | -0.328 .. -0.217 | -17.1% | -0.507 | 6.7e-22 |  | 8/8 |
| MYM | 5 | h16 | -0.430 | -0.514 .. -0.346 | -18.4% | -0.870 | 7e-24 |  | 8/8 |
| MYM | 5 | eod | +1.380 | +0.747 .. +2.014 | +11.8% | +2.829 | 2e-05 |  | 6/8 |
| MYM | 15 | h1 * | -0.274 | -0.289 .. -0.259 | -51.7% | -0.546 | 3.4e-284 | 1.35e-280 | 8/8 |
| MYM | 15 | h2 | -0.418 | -0.444 .. -0.391 | -54.5% | -0.823 | 1.2e-202 |  | 8/8 |
| MYM | 15 | h4 | -0.646 | -0.698 .. -0.595 | -58.0% | -1.274 | 1.9e-134 |  | 8/8 |
| MYM | 15 | h8 | -0.932 | -1.015 .. -0.850 | -56.8% | -1.870 | 4.5e-109 |  | 8/8 |
| MYM | 15 | h16 | -1.387 | -1.534 .. -1.240 | -56.3% | -2.763 | 3.2e-76 |  | 8/8 |
| MYM | 15 | eod | +0.817 | +0.606 .. +1.028 | +13.6% | +1.789 | 3.3e-14 |  | 8/8 |
| MYM | 60 | h1 * | -0.344 | -0.365 .. -0.324 | -65.7% | -0.681 | 4.5e-238 | 1.3e-234 | 8/8 |
| MYM | 60 | h2 | -0.470 | -0.501 .. -0.440 | -62.2% | -0.918 | 9.9e-201 |  | 8/8 |
| MYM | 60 | h4 | -0.624 | -0.670 .. -0.577 | -57.8% | -1.224 | 7.2e-153 |  | 8/8 |
| MYM | 60 | h8 | -0.650 | -0.716 .. -0.585 | -42.0% | -1.258 | 1.7e-84 |  | 8/8 |
| MYM | 60 | h16 | +0.379 | +0.321 .. +0.438 | +17.9% | +0.845 | 8.2e-37 |  | 8/8 |
| MYM | 60 | eod | +0.661 | +0.605 .. +0.716 | +29.7% | +1.341 | 1.3e-119 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.11 pts | -0.51 .. +0.30 | 0.61 |
| MES | 15 | +0.37 pts | -0.38 .. +1.11 | 0.34 |
| MES | 60 | +1.70 pts | +0.64 .. +2.76 | 0.003 |
| MNQ | 5 | +0.12 pts | -0.24 .. +0.47 | 0.54 |
| MNQ | 15 | +0.94 pts | +0.28 .. +1.59 | 0.0067 |
| MNQ | 60 | +1.81 pts | +0.71 .. +2.91 | 0.0016 |
| MYM | 5 | +0.12 pts | -0.47 .. +0.70 | 0.7 |
| MYM | 15 | -0.33 pts | -1.46 .. +0.81 | 0.57 |
| MYM | 60 | +0.78 pts | -0.92 .. +2.48 | 0.37 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 368852 | -0.000 | 0.481 | -0.00 | -3.50 | -3.50 | -3.51 | -3.49 |
| MES | 5 | h2 | event | short | 368852 | -0.003 | 0.481 | -0.03 | -3.53 | -3.51 | -3.55 | -3.51 |
| MES | 5 | h4 | event | short | 368852 | -0.010 | 0.481 | -0.08 | -3.58 | -3.54 | -3.62 | -3.53 |
| MES | 5 | h8 | event | long | 368852 | +0.024 | 0.481 | +0.18 | -3.32 | -3.40 | -3.24 | -3.43 |
| MES | 5 | h16 | event | long | 368852 | +0.055 | 0.481 | +0.42 | -3.08 | -3.23 | -2.92 | -3.35 |
| MES | 5 | eod | event | long | 368852 | +0.971 | 0.481 | +7.15 | +3.65 | +1.71 | +5.58 | -0.80 |
| MES | 15 | h1 | event | short | 122176 | -0.002 | 0.218 | -0.04 | -3.54 | -3.52 | -3.56 | -3.47 |
| MES | 15 | h2 | event | short | 122176 | -0.009 | 0.218 | -0.12 | -3.62 | -3.57 | -3.68 | -3.51 |
| MES | 15 | h4 | event | short | 122176 | -0.021 | 0.218 | -0.30 | -3.80 | -3.69 | -3.91 | -3.59 |
| MES | 15 | h8 | event | short | 122176 | -0.041 | 0.218 | -0.65 | -4.15 | -3.94 | -4.37 | -3.79 |
| MES | 15 | h16 | event | long | 122176 | +0.085 | 0.218 | +1.48 | -2.02 | -2.55 | -1.49 | -2.60 |
| MES | 15 | eod | event | long | 122176 | +0.452 | 0.218 | +7.17 | +3.67 | +1.61 | +5.74 | +2.34 |
| MES | 60 | h1 | event | short | 30452 | -0.006 | 0.089 | -0.29 | -3.79 | -3.72 | -3.86 | -3.63 |
| MES | 60 | h2 | event | short | 30452 | -0.011 | 0.089 | -0.64 | -4.14 | -3.92 | -4.36 | -3.77 |
| MES | 60 | h4 | event | short | 30452 | -0.027 | 0.089 | -1.46 | -4.96 | -4.44 | -5.47 | -4.15 |
| MES | 60 | h8 | event | long | 30452 | +0.063 | 0.089 | +3.09 | -0.41 | -1.32 | +0.50 | -1.96 |
| MES | 60 | h16 | event | long | 30452 | +0.133 | 0.089 | +5.87 | +2.37 | +0.64 | +4.10 | -0.21 |
| MES | 60 | eod | event | long | 30452 | +0.178 | 0.089 | +7.10 | +3.60 | +1.51 | +5.68 | +0.49 |
| MNQ | 5 | h1 | event | short | 367371 | -0.005 | 0.204 | -0.02 | -2.02 | -2.01 | -2.03 | -1.99 |
| MNQ | 5 | h2 | event | long | 367371 | +0.012 | 0.204 | +0.06 | -1.94 | -1.97 | -1.90 | -2.00 |
| MNQ | 5 | h4 | event | long | 367371 | +0.026 | 0.204 | +0.15 | -1.85 | -1.93 | -1.77 | -1.96 |
| MNQ | 5 | h8 | event | long | 367371 | +0.056 | 0.204 | +0.33 | -1.67 | -1.84 | -1.50 | -1.92 |
| MNQ | 5 | h16 | event | long | 367371 | +0.114 | 0.204 | +0.71 | -1.29 | -1.66 | -0.91 | -1.81 |
| MNQ | 5 | eod | event | long | 367371 | +1.405 | 0.204 | +9.14 | +7.14 | +2.96 | +11.29 | -0.17 |
| MNQ | 15 | h1 | event | short | 122158 | -0.008 | 0.089 | -0.09 | -2.09 | -2.05 | -2.13 | -1.96 |
| MNQ | 15 | h2 | event | long | 122158 | +0.017 | 0.089 | +0.22 | -1.78 | -1.88 | -1.67 | -1.94 |
| MNQ | 15 | h4 | event | long | 122158 | +0.037 | 0.089 | +0.52 | -1.48 | -1.74 | -1.23 | -1.78 |
| MNQ | 15 | h8 | event | long | 122158 | +0.067 | 0.089 | +1.10 | -0.90 | -1.48 | -0.32 | -1.53 |
| MNQ | 15 | h16 | event | long | 122158 | +0.121 | 0.089 | +2.23 | +0.23 | -1.04 | +1.51 | -0.39 |
| MNQ | 15 | eod | event | long | 122158 | +0.550 | 0.089 | +8.86 | +6.86 | +2.83 | +10.88 | +5.17 |
| MNQ | 60 | h1 | event | long | 30452 | +0.011 | 0.035 | +0.54 | -1.46 | -1.71 | -1.22 | -1.70 |
| MNQ | 60 | h2 | event | short | 30452 | -0.019 | 0.035 | -1.12 | -3.12 | -2.50 | -3.75 | -2.63 |
| MNQ | 60 | h4 | event | short | 30452 | -0.037 | 0.035 | -2.22 | -4.22 | -2.95 | -5.49 | -3.25 |
| MNQ | 60 | h8 | event | long | 30452 | +0.072 | 0.035 | +4.15 | +2.15 | +0.08 | +4.21 | +0.47 |
| MNQ | 60 | h16 | event | long | 30452 | +0.147 | 0.035 | +6.76 | +4.76 | +1.73 | +7.79 | +2.45 |
| MNQ | 60 | eod | event | long | 30452 | +0.204 | 0.035 | +8.59 | +6.59 | +2.71 | +10.45 | +3.54 |
| MYM | 5 | h1 | event | long | 184384 | -0.002 | 0.258 | -0.00 | -2.00 | +nan | -2.00 | -1.97 |
| MYM | 5 | h2 | event | long | 184384 | -0.001 | 0.258 | +0.03 | -1.97 | +nan | -1.97 | -1.89 |
| MYM | 5 | h4 | event | long | 184384 | -0.001 | 0.258 | +0.07 | -1.93 | +nan | -1.93 | -1.72 |
| MYM | 5 | h8 | event | long | 184384 | +0.002 | 0.258 | +0.16 | -1.84 | +nan | -1.84 | -1.49 |
| MYM | 5 | h16 | event | long | 184384 | +0.009 | 0.258 | +0.34 | -1.66 | +nan | -1.66 | -1.26 |
| MYM | 5 | eod | event | long | 184384 | +0.380 | 0.258 | +5.46 | +3.46 | +nan | +3.46 | +2.83 |
| MYM | 15 | h1 | event | short | 61086 | +0.001 | 0.112 | -0.04 | -2.04 | +nan | -2.04 | -2.02 |
| MYM | 15 | h2 | event | long | 61086 | +0.002 | 0.112 | +0.11 | -1.89 | +nan | -1.89 | -1.85 |
| MYM | 15 | h4 | event | long | 61086 | +0.005 | 0.112 | +0.25 | -1.75 | +nan | -1.75 | -1.64 |
| MYM | 15 | h8 | event | long | 61086 | +0.007 | 0.112 | +0.47 | -1.53 | +nan | -1.53 | -1.23 |
| MYM | 15 | h16 | event | long | 61086 | +0.014 | 0.112 | +1.00 | -1.00 | +nan | -1.00 | -0.03 |
| MYM | 15 | eod | event | long | 61086 | +0.165 | 0.112 | +5.50 | +3.50 | +nan | +3.50 | +5.04 |
| MYM | 60 | h1 | event | short | 15225 | -0.001 | 0.045 | -0.19 | -2.19 | +nan | -2.19 | -2.07 |
| MYM | 60 | h2 | event | short | 15225 | -0.002 | 0.045 | -0.42 | -2.42 | +nan | -2.42 | -2.11 |
| MYM | 60 | h4 | event | short | 15225 | -0.007 | 0.045 | -0.98 | -2.98 | +nan | -2.98 | -2.34 |
| MYM | 60 | h8 | event | short | 15225 | -0.017 | 0.045 | -2.04 | -4.04 | +nan | -4.04 | -2.93 |
| MYM | 60 | h16 | event | short | 15225 | -0.025 | 0.045 | -3.90 | -5.90 | +nan | -5.90 | -3.82 |
| MYM | 60 | eod | event | short | 15225 | -0.058 | 0.045 | -5.33 | -7.33 | +nan | -7.33 | -4.52 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.006 | +0.004 | +0.003 | +0.001 | +0.001 | +0.000 | +0.002 | +0.002 | +0.002 | +0.004 | +0.004 |
| MES | 15 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 |
| MES | 60 | +nan | +nan | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +0.000 |
| MNQ | 5 | -0.002 | -0.001 | -0.001 | -0.001 | -0.000 | +0.000 | +0.002 | +0.001 | +0.001 | -0.002 | -0.004 |
| MNQ | 15 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | -0.000 | -0.000 | -0.000 |
| MNQ | 60 | +nan | +nan | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.000 |
| MYM | 5 | -0.001 | -0.001 | -0.001 | -0.001 | -0.001 | +0.000 | -0.001 | -0.001 | -0.001 | -0.001 | -0.001 |
| MYM | 15 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +0.000 | -0.000 |
| MYM | 60 | +nan | +nan | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 |

## Calibration

- MES 5-min: 1036271 bars, 368852 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 122176 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 30452 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 367371 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 122158 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 30452 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 184384 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 61086 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 15225 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.

## Plain-$ cross-check (zoo.dollar_check)

Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 units can overweight quiet bars at long holds; a direction claim must survive this check.

FINAL WORD: DIRECTION: R20 units only - NOT confirmed in plain $ (treat as none)

| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | 5 | dir_h1 | all | 368852 | CONFIDENTLY NOTHING | -0.00 | +0.02 | 0.01 | +2.4 | 3.50 |
| ES | 5 | dir_h1 | 2018-25H1 | 184568 | CONFIDENTLY NOTHING | -0.00 | +0.03 | 0.02 | +1.5 | 3.50 |
| ES | 15 | dir_eod | all | 122176 | INCONCLUSIVE | +9.29 | +4.27 | 2.75 | +1.5 | 3.50 |
| ES | 15 | dir_eod | 2018-25H1 | 61148 | INCONCLUSIVE | +9.29 | +5.66 | 5.01 | +1.1 | 3.50 |
| ES | 60 | dir_eod | all | 30452 | INCONCLUSIVE | +5.54 | +4.10 | 2.72 | +1.5 | 3.50 |
| ES | 60 | dir_eod | 2018-25H1 | 15242 | INCONCLUSIVE | +5.54 | +5.32 | 4.83 | +1.1 | 3.50 |
| NQ | 5 | dir_h16 | all | 367371 | CONFIDENTLY NOTHING | +0.38 | +0.14 | 0.22 | +0.6 | 2.00 |
| NQ | 5 | dir_h16 | 2018-25H1 | 184521 | CONFIDENTLY NOTHING | +0.38 | +0.27 | 0.46 | +0.6 | 2.00 |
| NQ | 15 | dir_eod | all | 122158 | INCONCLUSIVE | +12.77 | +4.80 | 4.47 | +1.1 | 2.00 |
| NQ | 15 | dir_eod | 2018-25H1 | 61141 | INCONCLUSIVE | +12.77 | +7.00 | 8.53 | +0.8 | 2.00 |
| NQ | 60 | dir_eod | all | 30452 | REAL BUT TOO SMALL | +8.89 | +4.99 | 4.35 | +1.1 | 2.00 |
| NQ | 60 | dir_eod | 2018-25H1 | 15242 | REAL BUT TOO SMALL | +8.89 | +7.37 | 8.40 | +0.9 | 2.00 |
| YM | 5 | dir_h4 | all | 184384 | INCONCLUSIVE | +0.28 | -0.02 | 0.05 | -0.4 | 2.00 |
| YM | 5 | dir_h4 | 2018-25H1 | 184384 | INCONCLUSIVE | +0.28 | -0.02 | 0.05 | -0.4 | 2.00 |
| YM | 15 | dir_eod | all | 61086 | INCONCLUSIVE | +7.04 | +2.71 | 3.73 | +0.7 | 2.00 |
| YM | 15 | dir_eod | 2018-25H1 | 61086 | INCONCLUSIVE | +7.04 | +2.71 | 3.73 | +0.7 | 2.00 |
| YM | 60 | dir_h16 | all | 15225 | INCONCLUSIVE | -1.82 | -1.14 | 3.03 | -0.4 | 2.00 |
| YM | 60 | dir_h16 | 2018-25H1 | 15225 | INCONCLUSIVE | -1.82 | -1.14 | 3.03 | -0.4 | 2.00 |
