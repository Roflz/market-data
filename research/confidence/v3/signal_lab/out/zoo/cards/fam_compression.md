# Impact card: fam_compression

any of doji / spinning top / inside bar / NR7 [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: moves price up 0.031 average bars (~$0.50 per micro at 2018-25 bar sizes) over the next 16 bars (80 min) (after the event vs matched non-events), same sign in 13 of 16 years, q=0.0391; best leg (event, long) grosses $+0.53 and nets $-2.97 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 4% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.369 R20, CONFIRMED, q=0.000531, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.60, pessimistic $+0.23) does not clearly beat the $3.50 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: moves price up 0.017 average bars (~$0.46 per micro at 2018-25 bar sizes) over the next 2 bars (30 min) (after the event vs matched non-events), same sign in 15 of 16 years, q=0.0214; best leg (event, long) grosses $+0.30 and nets $-3.20 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: the market moves 3% LESS after the event than after matched bars over the next 8 bars (2 h) (-0.043 R20, CONFIRMED, q=0.00287, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.34, pessimistic $+0.16) does not clearly beat the $3.50 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.049 R20 over the rest of the session (to 16:45), p=0.1; we would catch an effect of 0.031 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.063).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.77 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: POSSIBLE direction effect +0.021 average bars (~$0.54 per micro at 2018-25 bar sizes) over the next 4 bars (20 min) (after the event vs matched non-events), not confirmed (q=0.0581, replicated in the other half=True, 14 of 16 years); best leg (event, long) grosses $+0.22 and nets $-1.78 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 2% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.013 R20, CONFIRMED, q=3.3e-13, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.35 at recent bar sizes, 90% range up to $0.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.305 R20 over the rest of the session (to 16:45), p=0.064; we would catch an effect of 0.021 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 5% LESS after the event than after matched bars over the next 2 bars (30 min) (-0.035 R20, CONFIRMED, q=0.000629, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $8.47 at recent bar sizes, 90% range up to $1.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.023 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.032 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.017).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.30 at recent bar sizes, 90% range up to $4.18); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: moves price up 0.052 average bars (~$0.62 per micro at 2018-25 bar sizes) over the next 4 bars (20 min) (after the event vs matched non-events), same sign in 8 of 8 years, q=0.0236; best leg (event, long) grosses $+0.20 and nets $-1.80 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 5-min size: the market moves 5% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.024 R20, CONFIRMED, q=3.13e-18, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.32, pessimistic $+0.22) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: moves price up 0.033 average bars (~$0.70 per micro at 2018-25 bar sizes) over the next 2 bars (30 min) (after the event vs matched non-events), same sign in 8 of 8 years, q=0.00318; best leg (event, long) grosses $+0.35 and nets $-1.65 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 15-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.022 R20, CONFIRMED, q=0.000231, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.42, pessimistic $+0.29) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.021 R20 over the next 1 bar (1 h), p=0.04; we would catch an effect of 0.045 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.091).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.56 at recent bar sizes, 90% range up to $3.51); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.001 .. +0.005 | +0.0013 | 0.27 / 0.26 / 0.29 | 0.286 |  |  | 11/16 | -0.002 | +0.005 |  | +1.1 / +1.1 |  |
| MES | 5 | h2 | +0.007 | +0.003 .. +0.012 | +0.0041 | 0.00075 / 0.00062 / 0.00035 | 0.000521 |  |  | 14/16 | +0.002 | +0.013 |  | +3.5 / +3.4 |  |
| MES | 5 | h4 | +0.012 | +0.005 .. +0.019 | +0.0047 | 0.00036 / 0.00027 / 3.7e-05 | 0.00026 |  |  | 13/16 | +0.007 | +0.017 |  | +4.1 / +3.6 | 0.008 |
| MES | 5 | h8 | +0.019 | +0.008 .. +0.030 | +0.0052 | 0.00052 / 0.00045 / 7.2e-06 | 0.00026 |  |  | 13/16 | +0.011 | +0.028 |  | +4.5 / +3.5 |  |
| MES | 5 | h16 * | +0.031 | +0.015 .. +0.048 | +0.0058 | 0.0002 / 0.00013 / 3.3e-07 | 0.00026 | 0.0391 | 0.084 | 13/16 | +0.026 | +0.037 | True | +5.0 / +3.7 |  |
| MES | 5 | eod | +0.257 | +0.096 .. +0.417 | +0.0094 | 0.0017 / 0.0014 / 1.9e-13 | 0.00026 |  |  | 15/16 | +0.220 | +0.294 |  | +8.1 / +3.1 |  |
| MES | 15 | h1 | +0.006 | +0.001 .. +0.011 | +0.0045 | 0.011 / 0.012 / 0.018 | 0.0159 |  |  | 11/16 | +0.003 | +0.010 |  | +2.4 / +2.5 |  |
| MES | 15 | h2 * | +0.017 | +0.010 .. +0.023 | +0.0077 | 1.5e-06 / 1.5e-06 / 2.2e-05 | 0.00026 | 0.0214 | 0.004 | 15/16 | +0.012 | +0.022 | True | +4.3 / +4.8 |  |
| MES | 15 | h4 | +0.017 | +0.006 .. +0.028 | +0.0052 | 0.0024 / 0.0029 / 0.0035 | 0.00339 |  |  | 12/16 | +0.005 | +0.028 |  | +2.9 / +3.0 | 0.016 |
| MES | 15 | h8 | +0.032 | +0.015 .. +0.048 | +0.0070 | 0.00016 / 0.00025 / 8.9e-05 | 0.00026 |  |  | 10/16 | +0.019 | +0.045 |  | +3.8 / +3.8 |  |
| MES | 15 | h16 | +0.061 | +0.029 .. +0.093 | +0.0094 | 0.00018 / 0.00024 / 2.2e-07 | 0.00026 |  |  | 14/16 | +0.049 | +0.073 |  | +5.1 / +3.7 |  |
| MES | 15 | eod | +0.260 | +0.101 .. +0.419 | +0.0154 | 0.0013 / 0.0011 / 1.4e-17 | 0.00026 |  |  | 14/16 | +0.180 | +0.340 |  | +8.5 / +3.2 |  |
| MES | 60 | h1 | +0.006 | -0.004 .. +0.017 | +0.0041 | 0.24 / 0.24 / 0.25 | 0.25 |  |  | 10/16 | +0.004 | +0.009 |  | +1.2 / +1.2 |  |
| MES | 60 | h2 | +0.013 | -0.003 .. +0.028 | +0.0058 | 0.1 / 0.1 / 0.099 | 0.0987 |  |  | 8/16 | +0.010 | +0.016 |  | +1.6 / +1.6 |  |
| MES | 60 | h4 | +0.010 | -0.010 .. +0.031 | +0.0034 | 0.33 / 0.34 / 0.34 | 0.336 |  |  | 9/16 | +0.015 | +0.006 |  | +0.9 / +1.0 | 0.031 |
| MES | 60 | h8 | +0.021 | -0.008 .. +0.049 | +0.0048 | 0.16 / 0.17 / 0.16 | 0.154 |  |  | 12/16 | +0.040 | +0.001 |  | +1.3 / +1.4 |  |
| MES | 60 | h16 | +0.046 | +0.011 .. +0.081 | +0.0082 | 0.011 / 0.015 / 0.017 | 0.0185 |  |  | 12/16 | +0.058 | +0.034 |  | +2.3 / +2.5 |  |
| MES | 60 | eod * | +0.049 | +0.011 .. +0.087 | +0.0084 | 0.012 / 0.017 / 0.017 | 0.0151 | 1 | 0.889 | 12/16 | +0.050 | +0.048 | False | +2.3 / +2.5 |  |
| MNQ | 5 | h1 | +0.002 | -0.001 .. +0.005 | +0.0013 | 0.18 / 0.17 / 0.24 | 0.236 |  |  | 11/16 | -0.001 | +0.005 |  | +1.3 / +1.4 |  |
| MNQ | 5 | h2 | +0.010 | +0.004 .. +0.016 | +0.0034 | 0.0019 / 0.0014 / 0.001 | 0.00104 |  |  | 13/16 | +0.007 | +0.012 |  | +3.6 / +3.1 |  |
| MNQ | 5 | h4 * | +0.021 | +0.010 .. +0.032 | +0.0049 | 0.00031 / 0.00017 / 2.4e-06 | 0.00026 | 0.0581 | 0.11 | 14/16 | +0.015 | +0.027 | True | +5.3 / +3.6 | 0.011 |
| MNQ | 5 | h8 | +0.034 | +0.015 .. +0.054 | +0.0054 | 0.00067 / 0.00039 / 9.3e-08 | 0.00026 |  |  | 15/16 | +0.027 | +0.042 |  | +5.9 / +3.4 |  |
| MNQ | 5 | h16 | +0.050 | +0.019 .. +0.080 | +0.0055 | 0.0014 / 0.0012 / 4.7e-08 | 0.00026 |  |  | 14/16 | +0.044 | +0.055 |  | +5.9 / +3.2 |  |
| MNQ | 5 | eod | +0.293 | +0.050 .. +0.536 | +0.0068 | 0.018 / 0.015 / 3.6e-08 | 0.00026 |  |  | 13/16 | +0.192 | +0.393 |  | +6.9 / +2.4 |  |
| MNQ | 15 | h1 | +0.002 | -0.004 .. +0.008 | +0.0009 | 0.55 / 0.56 / 0.61 | 0.611 |  |  | 8/16 | -0.001 | +0.004 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h2 | +0.010 | +0.002 .. +0.019 | +0.0031 | 0.016 / 0.014 / 0.071 | 0.0711 |  |  | 13/16 | +0.010 | +0.010 |  | +2.0 / +2.4 |  |
| MNQ | 15 | h4 | +0.013 | -0.002 .. +0.028 | +0.0023 | 0.094 / 0.097 / 0.18 | 0.188 |  |  | 13/16 | +0.012 | +0.014 |  | +1.5 / +1.7 | 0.021 |
| MNQ | 15 | h8 | +0.013 | -0.008 .. +0.033 | +0.0018 | 0.22 / 0.23 / 0.3 | 0.294 |  |  | 13/16 | +0.009 | +0.016 |  | +1.1 / +1.2 |  |
| MNQ | 15 | h16 | +0.060 | +0.010 .. +0.109 | +0.0066 | 0.018 / 0.017 / 7.2e-05 | 0.00026 |  |  | 15/16 | +0.045 | +0.074 |  | +4.0 / +2.4 |  |
| MNQ | 15 | eod * | +0.305 | +0.071 .. +0.539 | +0.0118 | 0.011 / 0.0085 / 2.1e-12 | 0.00026 | 1 | 0.904 | 16/16 | +0.253 | +0.357 | False | +7.3 / +2.6 |  |
| MNQ | 60 | h1 | +0.002 | -0.010 .. +0.014 | +0.0013 | 0.72 / 0.73 / 0.71 | 0.708 |  |  | 8/16 | +0.005 | -0.000 |  | +0.4 / +0.4 |  |
| MNQ | 60 | h2 | +0.001 | -0.014 .. +0.017 | +0.0006 | 0.87 / 0.87 / 0.87 | 0.87 |  |  | 8/16 | +0.010 | -0.007 |  | +0.2 / +0.2 |  |
| MNQ | 60 | h4 | +0.010 | -0.014 .. +0.033 | +0.0028 | 0.42 / 0.42 / 0.39 | 0.381 |  |  | 8/16 | +0.012 | +0.007 |  | +0.8 / +0.8 | 0.032 |
| MNQ | 60 | h8 | +0.013 | -0.019 .. +0.046 | +0.0029 | 0.42 / 0.42 / 0.38 | 0.371 |  |  | 10/16 | +0.024 | +0.003 |  | +0.8 / +0.8 |  |
| MNQ | 60 | h16 | +0.023 | -0.017 .. +0.062 | +0.0037 | 0.27 / 0.27 / 0.27 | 0.257 |  |  | 10/16 | +0.022 | +0.023 |  | +1.0 / +1.1 |  |
| MNQ | 60 | eod * | +0.023 | -0.019 .. +0.064 | +0.0036 | 0.28 / 0.29 / 0.29 | 0.283 | 1 | 1 | 9/16 | +0.013 | +0.033 | False | +1.0 / +1.1 |  |
| MYM | 5 | h1 | +0.008 | +0.003 .. +0.014 | +0.0043 | 0.0033 / 0.0028 / 0.0034 | 0.00211 |  |  | 7/8 | n/a | +0.008 |  | +3.3 / +2.9 |  |
| MYM | 5 | h2 | +0.023 | +0.011 .. +0.036 | +0.0074 | 0.00017 / 0.00011 / 3e-07 | 0.000527 |  |  | 7/8 | n/a | +0.023 |  | +5.8 / +3.8 |  |
| MYM | 5 | h4 * | +0.052 | +0.026 .. +0.079 | +0.0103 | 0.00012 / 0.0001 / 8.1e-13 | 0.000527 | 0.0236 | 0.048 | 8/8 | n/a | +0.052 | True | +8.2 / +3.9 | 0.019 |
| MYM | 5 | h8 | +0.087 | +0.041 .. +0.132 | +0.0122 | 0.00021 / 0.00026 / 3.8e-18 | 0.000527 |  |  | 8/8 | n/a | +0.087 |  | +9.7 / +3.7 |  |
| MYM | 5 | h16 | +0.105 | +0.042 .. +0.167 | +0.0115 | 0.00099 / 0.0012 / 1.9e-16 | 0.000527 |  |  | 7/8 | n/a | +0.105 |  | +8.8 / +3.3 |  |
| MYM | 5 | eod | +0.444 | +0.121 .. +0.767 | +0.0109 | 0.0071 / 0.0068 / 4.6e-14 | 0.000527 |  |  | 7/8 | n/a | +0.444 |  | +7.9 / +2.7 |  |
| MYM | 15 | h1 | +0.010 | +0.003 .. +0.018 | +0.0054 | 0.0077 / 0.0096 / 0.025 | 0.0269 |  |  | 6/8 | n/a | +0.010 |  | +2.4 / +2.7 |  |
| MYM | 15 | h2 * | +0.033 | +0.020 .. +0.047 | +0.0098 | 1.5e-06 / 1e-05 / 3.6e-05 | 0.000527 | 0.00318 | 0.002 | 8/8 | n/a | +0.033 | True | +4.5 / +4.8 |  |
| MYM | 15 | h4 | +0.046 | +0.017 .. +0.075 | +0.0081 | 0.0016 / 0.0025 / 0.00082 | 0.000527 |  |  | 7/8 | n/a | +0.046 |  | +3.8 / +3.2 | 0.034 |
| MYM | 15 | h8 | +0.088 | +0.036 .. +0.140 | +0.0119 | 0.001 / 0.0011 / 7.5e-07 | 0.000527 |  |  | 8/8 | n/a | +0.088 |  | +5.4 / +3.3 |  |
| MYM | 15 | h16 | +0.190 | +0.065 .. +0.314 | +0.0183 | 0.0029 / 0.0034 / 2.8e-15 | 0.000527 |  |  | 8/8 | n/a | +0.190 |  | +8.2 / +3.0 |  |
| MYM | 15 | eod | +0.481 | +0.150 .. +0.812 | +0.0192 | 0.0044 / 0.0058 / 4.9e-16 | 0.000527 |  |  | 8/8 | n/a | +0.481 |  | +8.5 / +2.8 |  |
| MYM | 60 | h1 * | +0.021 | +0.006 .. +0.036 | +0.0125 | 0.006 / 0.0067 / 0.012 | 0.0126 | 0.936 | 0.704 | 6/8 | n/a | +0.021 | False | +2.6 / +2.7 |  |
| MYM | 60 | h2 | +0.018 | -0.003 .. +0.039 | +0.0075 | 0.099 / 0.11 / 0.12 | 0.125 |  |  | 6/8 | n/a | +0.018 |  | +1.5 / +1.7 |  |
| MYM | 60 | h4 | +0.001 | -0.030 .. +0.033 | +0.0004 | 0.93 / 0.93 / 0.93 | 0.933 |  |  | 5/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.045 |
| MYM | 60 | h8 | -0.003 | -0.045 .. +0.040 | -0.0006 | 0.89 / 0.89 / 0.89 | 0.88 |  |  | 5/8 | n/a | -0.003 |  | -0.1 / -0.1 |  |
| MYM | 60 | h16 | +0.006 | -0.049 .. +0.060 | +0.0010 | 0.84 / 0.83 / 0.83 | 0.824 |  |  | 4/8 | n/a | +0.006 |  | +0.2 / +0.2 |  |
| MYM | 60 | eod | +0.020 | -0.037 .. +0.076 | +0.0032 | 0.49 / 0.49 / 0.48 | 0.478 |  |  | 6/8 | n/a | +0.020 |  | +0.6 / +0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.003 .. +0.002 | -0.1% | -0.011 | 0.77 |  | 8/16 |
| MES | 5 | h2 | -0.002 | -0.005 .. +0.002 | -0.3% | -0.011 | 0.49 |  | 9/16 |
| MES | 5 | h4 | -0.008 | -0.013 .. -0.003 | -0.8% | -0.020 | 0.0049 |  | 14/16 |
| MES | 5 | h8 | -0.022 | -0.033 .. -0.012 | -1.6% | -0.043 | 1.9e-05 |  | 15/16 |
| MES | 5 | h16 | -0.037 | -0.052 .. -0.021 | -1.7% | -0.085 | 6e-06 |  | 16/16 |
| MES | 5 | eod * | -0.369 | -0.522 .. -0.216 | -3.7% | -0.721 | 2.2e-06 | 0.000531 | 15/16 |
| MES | 15 | h1 | -0.004 | -0.008 .. +0.000 | -0.7% | -0.017 | 0.16 |  | 11/16 |
| MES | 15 | h2 | -0.014 | -0.020 .. -0.007 | -1.9% | -0.032 | 9e-05 |  | 14/16 |
| MES | 15 | h4 | -0.026 | -0.039 .. -0.013 | -2.5% | -0.057 | 0.00012 |  | 15/16 |
| MES | 15 | h8 * | -0.043 | -0.062 .. -0.024 | -2.8% | -0.106 | 1.3e-05 | 0.00287 | 16/16 |
| MES | 15 | h16 | -0.066 | -0.096 .. -0.037 | -2.9% | -0.205 | 1.3e-05 |  | 15/16 |
| MES | 15 | eod | -0.304 | -0.453 .. -0.155 | -5.5% | -0.524 | 6.1e-05 |  | 16/16 |
| MES | 60 | h1 | -0.007 | -0.015 .. +0.001 | -1.4% | -0.025 | 0.22 |  | 11/16 |
| MES | 60 | h2 | -0.009 | -0.019 .. +0.002 | -1.2% | -0.032 | 0.4 |  | 11/16 |
| MES | 60 | h4 | -0.017 | -0.033 .. -0.001 | -1.6% | -0.040 | 0.13 |  | 12/16 |
| MES | 60 | h8 | -0.020 | -0.039 .. -0.002 | -1.4% | -0.050 | 0.24 |  | 9/16 |
| MES | 60 | h16 * | -0.032 | -0.056 .. -0.008 | -1.5% | -0.061 | 0.011 | 1 | 12/16 |
| MES | 60 | eod | -0.028 | -0.052 .. -0.003 | -1.3% | -0.062 | 0.032 |  | 13/16 |
| MNQ | 5 | h1 * | -0.013 | -0.016 .. -0.010 | -2.4% | -0.026 | 7.7e-16 | 3.3e-13 | 16/16 |
| MNQ | 5 | h2 | -0.025 | -0.031 .. -0.018 | -3.2% | -0.041 | 2.4e-13 |  | 16/16 |
| MNQ | 5 | h4 | -0.044 | -0.057 .. -0.030 | -3.9% | -0.076 | 2.2e-10 |  | 16/16 |
| MNQ | 5 | h8 | -0.082 | -0.112 .. -0.053 | -5.1% | -0.149 | 4.2e-08 |  | 16/16 |
| MNQ | 5 | h16 | -0.137 | -0.191 .. -0.082 | -5.7% | -0.285 | 9.3e-07 |  | 16/16 |
| MNQ | 5 | eod | -0.818 | -1.126 .. -0.510 | -6.5% | -1.756 | 1.9e-07 |  | 16/16 |
| MNQ | 15 | h1 | -0.014 | -0.019 .. -0.008 | -2.6% | -0.037 | 4.1e-05 |  | 14/16 |
| MNQ | 15 | h2 * | -0.035 | -0.050 .. -0.021 | -4.6% | -0.068 | 2.6e-06 | 0.000629 | 15/16 |
| MNQ | 15 | h4 | -0.068 | -0.104 .. -0.032 | -6.0% | -0.126 | 0.00023 |  | 16/16 |
| MNQ | 15 | h8 | -0.108 | -0.164 .. -0.052 | -6.4% | -0.241 | 0.00016 |  | 16/16 |
| MNQ | 15 | h16 | -0.137 | -0.197 .. -0.077 | -5.4% | -0.423 | 8.2e-06 |  | 16/16 |
| MNQ | 15 | eod | -0.473 | -0.744 .. -0.202 | -7.4% | -0.824 | 0.00061 |  | 15/16 |
| MNQ | 60 | h1 | -0.007 | -0.014 .. +0.000 | -1.3% | -0.027 | 0.21 |  | 11/16 |
| MNQ | 60 | h2 | -0.011 | -0.023 .. -0.000 | -1.5% | -0.033 | 0.14 |  | 10/16 |
| MNQ | 60 | h4 * | -0.025 | -0.041 .. -0.009 | -2.3% | -0.040 | 0.0028 | 0.444 | 13/16 |
| MNQ | 60 | h8 | -0.030 | -0.051 .. -0.009 | -1.9% | -0.050 | 0.039 |  | 12/16 |
| MNQ | 60 | h16 | -0.028 | -0.056 .. -0.001 | -1.3% | -0.056 | 0.07 |  | 10/16 |
| MNQ | 60 | eod | -0.029 | -0.057 .. -0.001 | -1.3% | -0.055 | 0.074 |  | 10/16 |
| MYM | 5 | h1 * | -0.024 | -0.029 .. -0.019 | -4.5% | -0.046 | 5.6e-21 | 3.13e-18 | 8/8 |
| MYM | 5 | h2 | -0.037 | -0.048 .. -0.025 | -4.8% | -0.066 | 3.8e-10 |  | 8/8 |
| MYM | 5 | h4 | -0.065 | -0.091 .. -0.040 | -6.0% | -0.116 | 8.7e-07 |  | 8/8 |
| MYM | 5 | h8 | -0.111 | -0.160 .. -0.062 | -7.0% | -0.202 | 1.2e-05 |  | 8/8 |
| MYM | 5 | h16 | -0.154 | -0.221 .. -0.087 | -6.6% | -0.337 | 1e-05 |  | 8/8 |
| MYM | 5 | eod | -0.806 | -1.128 .. -0.485 | -6.9% | -1.333 | 8.9e-07 |  | 8/8 |
| MYM | 15 | h1 * | -0.022 | -0.029 .. -0.015 | -4.1% | -0.047 | 9.4e-07 | 0.000231 | 8/8 |
| MYM | 15 | h2 | -0.043 | -0.061 .. -0.025 | -5.6% | -0.082 | 4.9e-06 |  | 8/8 |
| MYM | 15 | h4 | -0.080 | -0.121 .. -0.039 | -7.2% | -0.153 | 0.00017 |  | 8/8 |
| MYM | 15 | h8 | -0.120 | -0.185 .. -0.055 | -7.3% | -0.296 | 0.0004 |  | 8/8 |
| MYM | 15 | h16 | -0.195 | -0.313 .. -0.076 | -7.9% | -0.481 | 0.0017 |  | 8/8 |
| MYM | 15 | eod | -0.500 | -0.817 .. -0.182 | -8.3% | -0.798 | 0.0028 |  | 8/8 |
| MYM | 60 | h1 * | -0.017 | -0.029 .. -0.006 | -3.3% | -0.038 | 0.015 | 1 | 7/8 |
| MYM | 60 | h2 | -0.022 | -0.038 .. -0.007 | -3.0% | -0.052 | 0.047 |  | 6/8 |
| MYM | 60 | h4 | -0.007 | -0.028 .. +0.014 | -0.7% | -0.048 | 0.96 |  | 4/8 |
| MYM | 60 | h8 | -0.033 | -0.060 .. -0.006 | -2.1% | -0.067 | 0.1 |  | 7/8 |
| MYM | 60 | h16 | -0.017 | -0.051 .. +0.017 | -0.8% | -0.053 | 0.53 |  | 5/8 |
| MYM | 60 | eod | -0.015 | -0.050 .. +0.020 | -0.7% | -0.049 | 0.49 |  | 7/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.17 pts | -0.02 .. +0.35 | 0.075 |
| MES | 15 | +0.27 pts | -0.07 .. +0.61 | 0.12 |
| MES | 60 | +0.34 pts | -0.29 .. +0.97 | 0.42 |
| MNQ | 5 | +0.12 pts | -0.07 .. +0.31 | 0.21 |
| MNQ | 15 | +0.30 pts | -0.03 .. +0.62 | 0.095 |
| MNQ | 60 | +0.40 pts | -0.25 .. +1.05 | 0.22 |
| MYM | 5 | +0.39 pts | +0.12 .. +0.67 | 0.0056 |
| MYM | 15 | +0.25 pts | -0.19 .. +0.69 | 0.28 |
| MYM | 60 | +0.00 pts | -0.93 .. +0.94 | 1 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 376710 | +0.002 | 0.320 | +0.04 | -3.46 | -3.50 | -3.41 | -3.46 |
| MES | 5 | h2 | event | long | 376710 | +0.009 | 0.320 | +0.11 | -3.39 | -3.46 | -3.32 | -3.41 |
| MES | 5 | h4 | event | long | 376710 | +0.015 | 0.320 | +0.16 | -3.34 | -3.42 | -3.25 | -3.37 |
| MES | 5 | h8 | event | long | 376710 | +0.029 | 0.320 | +0.29 | -3.21 | -3.35 | -3.07 | -3.29 |
| MES | 5 | h16 | event | long | 376710 | +0.056 | 0.320 | +0.53 | -2.97 | -3.17 | -2.77 | -3.16 |
| MES | 5 | eod | event | long | 376710 | +0.599 | 0.320 | +4.58 | +1.08 | -0.18 | +2.32 | +0.35 |
| MES | 15 | h1 | event | long | 127720 | +0.009 | 0.186 | +0.17 | -3.33 | -3.43 | -3.25 | -3.38 |
| MES | 15 | h2 | event | long | 127720 | +0.020 | 0.186 | +0.30 | -3.20 | -3.32 | -3.08 | -3.28 |
| MES | 15 | h4 | event | long | 127720 | +0.030 | 0.186 | +0.45 | -3.05 | -3.25 | -2.86 | -3.21 |
| MES | 15 | h8 | event | long | 127720 | +0.054 | 0.186 | +0.89 | -2.61 | -2.98 | -2.26 | -2.88 |
| MES | 15 | h16 | event | long | 127720 | +0.097 | 0.186 | +1.57 | -1.93 | -2.46 | -1.43 | -2.30 |
| MES | 15 | eod | event | long | 127720 | +0.358 | 0.186 | +4.97 | +1.47 | -0.29 | +3.17 | +0.96 |
| MES | 60 | h1 | event | long | 29753 | +0.012 | 0.095 | +0.40 | -3.10 | -3.22 | -2.99 | -3.25 |
| MES | 60 | h2 | event | long | 29753 | +0.024 | 0.095 | +0.92 | -2.58 | -2.92 | -2.23 | -2.91 |
| MES | 60 | h4 | event | long | 29753 | +0.039 | 0.095 | +1.42 | -2.08 | -2.49 | -1.66 | -2.81 |
| MES | 60 | h8 | event | long | 29753 | +0.076 | 0.095 | +2.72 | -0.78 | -1.44 | -0.10 | -2.26 |
| MES | 60 | h16 | event | long | 29753 | +0.139 | 0.095 | +4.73 | +1.23 | -0.25 | +2.76 | -1.41 |
| MES | 60 | eod | event | long | 29753 | +0.156 | 0.095 | +5.23 | +1.73 | -0.08 | +3.60 | -1.42 |
| MNQ | 5 | h1 | event | long | 374167 | +0.005 | 0.123 | +0.06 | -1.94 | -1.99 | -1.89 | -1.95 |
| MNQ | 5 | h2 | event | long | 374167 | +0.011 | 0.123 | +0.12 | -1.88 | -1.96 | -1.82 | -1.89 |
| MNQ | 5 | h4 | event | long | 374167 | +0.022 | 0.123 | +0.22 | -1.78 | -1.89 | -1.69 | -1.78 |
| MNQ | 5 | h8 | event | long | 374167 | +0.041 | 0.123 | +0.42 | -1.58 | -1.80 | -1.39 | -1.61 |
| MNQ | 5 | h16 | event | long | 374167 | +0.076 | 0.123 | +0.82 | -1.18 | -1.59 | -0.84 | -1.38 |
| MNQ | 5 | eod | event | long | 374167 | +0.806 | 0.123 | +6.55 | +4.55 | +1.29 | +7.33 | +4.64 |
| MNQ | 15 | h1 | event | long | 130360 | +0.010 | 0.073 | +0.23 | -1.77 | -1.92 | -1.62 | -1.89 |
| MNQ | 15 | h2 | event | long | 130360 | +0.018 | 0.073 | +0.37 | -1.63 | -1.83 | -1.45 | -1.78 |
| MNQ | 15 | h4 | event | long | 130360 | +0.029 | 0.073 | +0.58 | -1.42 | -1.73 | -1.12 | -1.67 |
| MNQ | 15 | h8 | event | long | 130360 | +0.052 | 0.073 | +1.10 | -0.90 | -1.52 | -0.31 | -1.43 |
| MNQ | 15 | h16 | event | long | 130360 | +0.101 | 0.073 | +2.05 | +0.05 | -1.04 | +1.07 | -0.39 |
| MNQ | 15 | eod | event | long | 130360 | +0.412 | 0.073 | +6.70 | +4.70 | +1.25 | +7.93 | +4.95 |
| MNQ | 60 | h1 | event | long | 30560 | +0.014 | 0.037 | +0.60 | -1.40 | -1.65 | -1.16 | -1.72 |
| MNQ | 60 | h2 | event | long | 30560 | +0.024 | 0.037 | +1.18 | -0.82 | -1.31 | -0.32 | -1.45 |
| MNQ | 60 | h4 | event | long | 30560 | +0.049 | 0.037 | +2.41 | +0.41 | -0.88 | +1.71 | -0.75 |
| MNQ | 60 | h8 | event | long | 30560 | +0.084 | 0.037 | +3.73 | +1.73 | -0.07 | +3.55 | -0.35 |
| MNQ | 60 | h16 | event | long | 30560 | +0.141 | 0.037 | +5.95 | +3.95 | +0.89 | +7.02 | +0.55 |
| MNQ | 60 | eod | event | long | 30560 | +0.165 | 0.037 | +6.84 | +4.84 | +1.23 | +8.46 | +0.52 |
| MYM | 5 | h1 | event | long | 191988 | +0.003 | 0.167 | +0.06 | -1.94 | +nan | -1.94 | -1.93 |
| MYM | 5 | h2 | event | long | 191988 | +0.008 | 0.167 | +0.12 | -1.88 | +nan | -1.88 | -1.83 |
| MYM | 5 | h4 | event | long | 191988 | +0.013 | 0.167 | +0.20 | -1.80 | +nan | -1.80 | -1.68 |
| MYM | 5 | h8 | event | long | 191988 | +0.022 | 0.167 | +0.27 | -1.73 | +nan | -1.73 | -1.53 |
| MYM | 5 | h16 | event | long | 191988 | +0.029 | 0.167 | +0.47 | -1.53 | +nan | -1.53 | -1.35 |
| MYM | 5 | eod | event | long | 191988 | +0.325 | 0.167 | +4.00 | +2.00 | +nan | +2.00 | +2.34 |
| MYM | 15 | h1 | event | long | 65914 | +0.008 | 0.096 | +0.19 | -1.81 | +nan | -1.81 | -1.83 |
| MYM | 15 | h2 | event | long | 65914 | +0.017 | 0.096 | +0.35 | -1.65 | +nan | -1.65 | -1.58 |
| MYM | 15 | h4 | event | long | 65914 | +0.017 | 0.096 | +0.47 | -1.53 | +nan | -1.53 | -1.34 |
| MYM | 15 | h8 | event | long | 65914 | +0.024 | 0.096 | +0.73 | -1.27 | +nan | -1.27 | -0.76 |
| MYM | 15 | h16 | event | long | 65914 | +0.033 | 0.096 | +1.11 | -0.89 | +nan | -0.89 | +0.43 |
| MYM | 15 | eod | event | long | 65914 | +0.187 | 0.096 | +3.89 | +1.89 | +nan | +1.89 | +4.53 |
| MYM | 60 | h1 | event | long | 15132 | +0.017 | 0.047 | +0.69 | -1.31 | +nan | -1.31 | -1.41 |
| MYM | 60 | h2 | event | long | 15132 | +0.018 | 0.047 | +1.09 | -0.91 | +nan | -0.91 | -1.13 |
| MYM | 60 | h4 | event | long | 15132 | +0.013 | 0.047 | +1.29 | -0.71 | +nan | -0.71 | -1.11 |
| MYM | 60 | h8 | event | short | 15132 | -0.019 | 0.047 | -2.13 | -4.13 | +nan | -4.13 | -3.36 |
| MYM | 60 | h16 | event | long | 15132 | +0.042 | 0.047 | +3.77 | +1.77 | +nan | +1.77 | +0.26 |
| MYM | 60 | eod | event | long | 15132 | +0.063 | 0.047 | +4.55 | +2.55 | +nan | +2.55 | +0.43 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.018 | -0.020 | -0.017 | -0.007 | -0.001 | +0.000 | +0.002 | +0.004 | +0.003 | +0.006 | +0.009 |
| MES | 15 | -0.015 | -0.025 | -0.029 | -0.012 | -0.002 | +0.000 | +0.006 | +0.012 | +0.011 | +0.016 | +0.025 |
| MES | 60 | -0.036 | -0.029 | -0.019 | -0.006 | -0.001 | +0.000 | +0.003 | +0.007 | +0.004 | +0.011 | +0.022 |
| MNQ | 5 | -0.014 | -0.023 | -0.022 | -0.009 | -0.000 | +0.000 | +0.003 | +0.004 | +0.008 | +0.016 | +0.025 |
| MNQ | 15 | -0.018 | -0.025 | -0.029 | -0.013 | -0.001 | +0.000 | +0.005 | +0.007 | +0.007 | +0.004 | +0.017 |
| MNQ | 60 | -0.006 | -0.016 | -0.010 | +0.000 | +0.003 | +0.000 | +0.002 | +0.002 | +0.009 | +0.006 | +0.015 |
| MYM | 5 | -0.021 | -0.028 | -0.024 | -0.012 | -0.004 | +0.000 | +0.006 | +0.012 | +0.020 | +0.032 | +0.036 |
| MYM | 15 | -0.026 | -0.033 | -0.040 | -0.018 | -0.007 | +0.000 | +0.010 | +0.019 | +0.021 | +0.033 | +0.059 |
| MYM | 60 | -0.049 | -0.038 | -0.024 | -0.006 | -0.007 | +0.000 | +0.012 | +0.011 | +0.001 | -0.004 | -0.001 |

## Calibration

- MES 5-min: 1036271 bars, 376710 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 127720 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 29753 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 374167 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 130360 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 30560 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 191988 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 65914 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 15132 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 32002 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.

## Plain-$ cross-check (zoo.dollar_check)

Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 units can overweight quiet bars at long holds; a direction claim must survive this check.

FINAL WORD: DIRECTION: confirmed in R20 and $, far below costs ($0.36 vs $2.00)

| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | 5 | dir_h16 | all | 376710 | REAL BUT TOO SMALL | +0.60 | +0.15 | 0.17 | +0.9 | 3.50 |
| ES | 5 | dir_h16 | 2018-25H1 | 190653 | REAL BUT TOO SMALL | +0.60 | +0.27 | 0.33 | +0.8 | 3.50 |
| ES | 15 | dir_h2 | all | 127720 | REAL BUT TOO SMALL | +0.34 | +0.23 | 0.07 | +3.0 | 3.50 |
| ES | 15 | dir_h2 | 2018-25H1 | 64945 | REAL BUT TOO SMALL | +0.34 | +0.34 | 0.15 | +2.3 | 3.50 |
| ES | 60 | dir_eod | all | 29753 | CONFIDENTLY NOTHING | +3.27 | +0.90 | 2.04 | +0.4 | 3.50 |
| ES | 60 | dir_eod | 2018-25H1 | 14599 | CONFIDENTLY NOTHING | +3.27 | +1.57 | 4.06 | +0.4 | 3.50 |
| NQ | 5 | dir_h4 | all | 374163 | INCONCLUSIVE | +0.39 | +0.09 | 0.08 | +1.2 | 2.00 |
| NQ | 5 | dir_h4 | 2018-25H1 | 202333 | INCONCLUSIVE | +0.39 | +0.13 | 0.15 | +0.8 | 2.00 |
| NQ | 15 | dir_eod | all | 130356 | INCONCLUSIVE | +12.96 | +1.43 | 3.44 | +0.4 | 2.00 |
| NQ | 15 | dir_eod | 2018-25H1 | 67337 | INCONCLUSIVE | +12.96 | +2.66 | 6.42 | +0.4 | 2.00 |
| NQ | 60 | dir_eod | all | 30560 | INCONCLUSIVE | +4.71 | +2.04 | 3.26 | +0.6 | 2.00 |
| NQ | 60 | dir_eod | 2018-25H1 | 15246 | INCONCLUSIVE | +4.71 | +3.94 | 6.55 | +0.6 | 2.00 |
| YM | 5 | dir_h4 | all | 191988 | REAL BUT TOO SMALL | +0.32 | +0.17 | 0.07 | +2.4 | 2.00 |
| YM | 5 | dir_h4 | 2018-25H1 | 191988 | REAL BUT TOO SMALL | +0.32 | +0.17 | 0.07 | +2.4 | 2.00 |
| YM | 15 | dir_h2 | all | 65914 | REAL BUT TOO SMALL | +0.42 | +0.36 | 0.11 | +3.2 | 2.00 |
| YM | 15 | dir_h2 | 2018-25H1 | 65914 | REAL BUT TOO SMALL | +0.42 | +0.36 | 0.11 | +3.2 | 2.00 |
| YM | 60 | dir_h1 | all | 15132 | INCONCLUSIVE | +0.59 | +0.59 | 0.28 | +2.1 | 2.00 |
| YM | 60 | dir_h1 | 2018-25H1 | 15132 | INCONCLUSIVE | +0.59 | +0.59 | 0.28 | +2.1 | 2.00 |
