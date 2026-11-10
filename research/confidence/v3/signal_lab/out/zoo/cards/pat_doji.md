# Impact card: pat_doji

candle pattern doji (no direction): body <= 0.1 x avgR10 (TA-Lib BodyDoji) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect +0.037 average bars (~$0.56 per micro at 2018-25 bar sizes) over the next 16 bars (80 min) (after the event vs matched non-events), not confirmed (q=0.0913, replicated in the other half=False, 12 of 16 years); best leg (event, long) grosses $+0.52 and nets $-2.98 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 5% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.545 R20, CONFIRMED, q=1.4e-06, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.46 at recent bar sizes, 90% range up to $0.45); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: moves price up 0.418 average bars (~$11.76 per micro at 2018-25 bar sizes) over the rest of the session (to 16:45) (after the event vs matched non-events), same sign in 16 of 16 years, q=1.67e-06; best leg (event, long) grosses $+5.20 and nets $+1.70 per micro per trade after $3.50 costs -> tradable on its own.
- MES 15-min size: the market moves 9% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.489 R20, CONFIRMED, q=4.27e-12, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): REAL & TRADABLE - the effect is confirmed and, in 2018-25H1, its per-trade edge is $+9.69 per micro with a pessimistic (lower 80%) value of $+4.89, above the $3.50 round trip. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.006 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 60-min size: the market moves 4% LESS after the event than after matched bars over the next 2 bars (2 h) (-0.028 R20, possible, q=0.0956, 12 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.28 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.063 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: moves price up 0.055 average bars (~$1.43 per micro at 2018-25 bar sizes) over the next 8 bars (40 min) (after the event vs matched non-events), same sign in 16 of 16 years, q=6.5e-07; best leg (event, long) grosses $+0.50 and nets $-1.50 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 9% LESS after the event than after matched bars over the rest of the session (to 16:45) (-1.177 R20, CONFIRMED, q=1.51e-20, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+1.03, pessimistic $+0.65) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: moves price up 0.572 average bars (~$26.06 per micro at 2018-25 bar sizes) over the rest of the session (to 16:45) (after the event vs matched non-events), same sign in 13 of 16 years, q=8.35e-07; best leg (event, long) grosses $+6.94 and nets $+4.94 per micro per trade after $2.00 costs -> tradable on its own.
- MNQ 15-min size: the market moves 8% LESS after the event than after matched bars over the next 16 bars (4 h) (-0.209 R20, CONFIRMED, q=1.64e-13, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): REAL & TRADABLE - the effect is confirmed and, in 2018-25H1, its per-trade edge is $+15.10 per micro with a pessimistic (lower 80%) value of $+7.20, above the $2.00 round trip. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.021 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.012).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.61 at recent bar sizes, 90% range up to $3.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: moves price up 0.089 average bars (~$1.08 per micro at 2018-25 bar sizes) over the next 4 bars (20 min) (after the event vs matched non-events), same sign in 8 of 8 years, q=1.36e-12; best leg (event, long) grosses $+0.23 and nets $-1.77 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 5-min size: the market moves 12% LESS after the event than after matched bars over the rest of the session (to 16:45) (-1.407 R20, CONFIRMED, q=3.95e-25, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.66, pessimistic $+0.54) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: moves price up 0.320 average bars (~$6.80 per micro at 2018-25 bar sizes) over the next 16 bars (4 h) (after the event vs matched non-events), same sign in 8 of 8 years, q=1.7e-07; best leg (event, long) grosses $+1.16 and nets $-0.84 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 15-min size: the market moves 12% LESS after the event than after matched bars over the next 8 bars (2 h) (-0.204 R20, CONFIRMED, q=1.9e-12, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): REAL & TRADABLE - the effect is confirmed and, in 2018-25H1, its per-trade edge is $+5.06 per micro with a pessimistic (lower 80%) value of $+4.11, above the $2.00 round trip. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.038 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.055 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.14).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.35 at recent bar sizes, 90% range up to $3.71); about 13.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.003 .. +0.004 | +0.0009 | 0.65 / 0.65 / 0.67 | 0.678 |  |  | 8/16 | +0.000 | +0.001 |  | +0.5 / +0.4 |  |
| MES | 5 | h2 | +0.003 | -0.002 .. +0.009 | +0.0026 | 0.24 / 0.23 / 0.21 | 0.216 |  |  | 9/16 | +0.003 | +0.003 |  | +1.3 / +1.2 |  |
| MES | 5 | h4 | +0.011 | +0.003 .. +0.020 | +0.0064 | 0.0066 / 0.0051 / 0.0025 | 0.00208 |  |  | 13/16 | +0.013 | +0.010 |  | +3.2 / +2.7 | 0.012 |
| MES | 5 | h8 | +0.022 | +0.009 .. +0.035 | +0.0085 | 0.0013 / 0.00086 / 0.00018 | 0.00104 |  |  | 11/16 | +0.026 | +0.017 |  | +4.3 / +3.2 |  |
| MES | 5 | h16 * | +0.037 | +0.016 .. +0.058 | +0.0100 | 0.00051 / 0.00034 / 3.2e-05 | 0.00026 | 0.0913 | 0.161 | 12/16 | +0.047 | +0.026 | False | +4.9 / +3.5 |  |
| MES | 5 | eod | +0.405 | +0.174 .. +0.636 | +0.0218 | 0.00058 / 0.00053 / 3.9e-07 | 0.00026 |  |  | 14/16 | +0.397 | +0.413 |  | +9.8 / +3.4 |  |
| MES | 15 | h1 | +0.003 | -0.003 .. +0.009 | +0.0020 | 0.37 / 0.39 / 0.41 | 0.414 |  |  | 9/16 | -0.002 | +0.007 |  | +0.9 / +0.9 |  |
| MES | 15 | h2 | +0.013 | +0.004 .. +0.022 | +0.0061 | 0.0066 / 0.0069 / 0.012 | 0.0107 |  |  | 14/16 | +0.010 | +0.015 |  | +2.7 / +2.7 |  |
| MES | 15 | h4 | +0.025 | +0.011 .. +0.039 | +0.0080 | 0.00043 / 0.00061 / 0.0013 | 0.0013 |  |  | 15/16 | +0.016 | +0.034 |  | +3.6 / +3.5 | 0.021 |
| MES | 15 | h8 | +0.045 | +0.024 .. +0.065 | +0.0101 | 2.4e-05 / 5.6e-05 / 5.7e-05 | 0.00026 |  |  | 14/16 | +0.051 | +0.039 |  | +4.4 / +4.2 |  |
| MES | 15 | h16 | +0.082 | +0.047 .. +0.117 | +0.0129 | 4.8e-06 / 9.5e-06 / 9.9e-07 | 0.00026 |  |  | 15/16 | +0.102 | +0.063 |  | +5.4 / +4.6 |  |
| MES | 15 | eod * | +0.418 | +0.277 .. +0.558 | +0.0254 | 5.3e-09 / 5.8e-09 / 1.1e-17 | 0.00026 | 1.67e-06 | 0 | 16/16 | +0.469 | +0.366 | True | +10.4 / +5.8 |  |
| MES | 60 | h1 | +0.002 | -0.010 .. +0.015 | +0.0013 | 0.71 / 0.7 / 0.69 | 0.699 |  |  | 10/16 | -0.000 | +0.005 |  | +0.4 / +0.4 |  |
| MES | 60 | h2 * | +0.006 | -0.013 .. +0.025 | +0.0023 | 0.54 / 0.53 / 0.51 | 0.501 | 1 | 1 | 11/16 | +0.009 | +0.003 | False | +0.7 / +0.6 |  |
| MES | 60 | h4 | +0.001 | -0.027 .. +0.029 | +0.0003 | 0.93 / 0.93 / 0.92 | 0.92 |  |  | 8/16 | +0.010 | -0.007 |  | +0.1 / +0.1 | 0.039 |
| MES | 60 | h8 | -0.005 | -0.046 .. +0.037 | -0.0009 | 0.83 / 0.82 / 0.8 | 0.801 |  |  | 6/16 | +0.012 | -0.022 |  | -0.3 / -0.2 |  |
| MES | 60 | h16 | +0.010 | -0.042 .. +0.063 | +0.0016 | 0.7 / 0.7 / 0.69 | 0.685 |  |  | 10/16 | +0.025 | -0.004 |  | +0.4 / +0.4 |  |
| MES | 60 | eod | +0.017 | -0.040 .. +0.073 | +0.0025 | 0.57 / 0.58 / 0.55 | 0.554 |  |  | 9/16 | +0.015 | +0.018 |  | +0.6 / +0.6 |  |
| MNQ | 5 | h1 | +0.004 | +0.000 .. +0.008 | +0.0020 | 0.049 / 0.048 / 0.088 | 0.088 |  |  | 11/16 | +0.002 | +0.006 |  | +1.9 / +2.0 |  |
| MNQ | 5 | h2 | +0.015 | +0.008 .. +0.022 | +0.0046 | 8.8e-06 / 4e-06 / 0.00018 | 0.000521 |  |  | 14/16 | +0.015 | +0.015 |  | +4.7 / +4.4 |  |
| MNQ | 5 | h4 | +0.034 | +0.023 .. +0.045 | +0.0068 | 1.5e-09 / 4.4e-10 / 3.4e-08 | 0.00026 |  |  | 16/16 | +0.038 | +0.031 |  | +7.3 / +6.0 | 0.017 |
| MNQ | 5 | h8 * | +0.055 | +0.037 .. +0.073 | +0.0074 | 2.2e-09 / 4.1e-10 / 6.2e-10 | 0.00026 | 6.5e-07 | 0 | 16/16 | +0.064 | +0.047 | True | +7.9 / +6.0 |  |
| MNQ | 5 | h16 | +0.074 | +0.048 .. +0.101 | +0.0071 | 5.4e-08 / 4.6e-08 / 7.1e-09 | 0.00026 |  |  | 15/16 | +0.087 | +0.062 |  | +7.2 / +5.4 |  |
| MNQ | 5 | eod | +0.453 | +0.254 .. +0.652 | +0.0090 | 8.4e-06 / 6.9e-06 / 1.5e-10 | 0.00026 |  |  | 16/16 | +0.543 | +0.364 |  | +7.7 / +4.5 |  |
| MNQ | 15 | h1 | -0.003 | -0.010 .. +0.004 | -0.0012 | 0.42 / 0.41 / 0.5 | 0.477 |  |  | 12/16 | -0.005 | -0.001 |  | -0.8 / -0.8 |  |
| MNQ | 15 | h2 | +0.011 | +0.000 .. +0.021 | +0.0026 | 0.044 / 0.04 / 0.15 | 0.152 |  |  | 12/16 | +0.014 | +0.007 |  | +1.9 / +2.0 |  |
| MNQ | 15 | h4 | +0.020 | +0.004 .. +0.037 | +0.0029 | 0.016 / 0.017 / 0.1 | 0.101 |  |  | 11/16 | +0.034 | +0.007 |  | +2.3 / +2.4 | 0.029 |
| MNQ | 15 | h8 | +0.026 | +0.002 .. +0.050 | +0.0028 | 0.036 / 0.04 / 0.13 | 0.138 |  |  | 12/16 | +0.036 | +0.015 |  | +2.1 / +2.1 |  |
| MNQ | 15 | h16 | +0.120 | +0.072 .. +0.168 | +0.0109 | 1e-06 / 8.9e-07 / 4.5e-09 | 0.00026 |  |  | 15/16 | +0.153 | +0.087 |  | +6.8 / +4.9 |  |
| MNQ | 15 | eod * | +0.572 | +0.383 .. +0.761 | +0.0180 | 2.8e-09 / 8.9e-10 / 4e-20 | 0.00026 | 8.35e-07 | 0 | 13/16 | +0.774 | +0.371 | True | +11.7 / +5.9 |  |
| MNQ | 60 | h1 | +0.005 | -0.008 .. +0.017 | +0.0023 | 0.45 / 0.46 / 0.43 | 0.432 |  |  | 9/16 | +0.006 | +0.003 |  | +0.8 / +0.8 |  |
| MNQ | 60 | h2 | +0.001 | -0.018 .. +0.019 | +0.0002 | 0.96 / 0.96 / 0.95 | 0.961 |  |  | 7/16 | +0.004 | -0.003 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h4 | +0.005 | -0.021 .. +0.031 | +0.0012 | 0.71 / 0.71 / 0.69 | 0.694 |  |  | 8/16 | +0.001 | +0.009 |  | +0.4 / +0.4 | 0.040 |
| MNQ | 60 | h8 | +0.005 | -0.033 .. +0.043 | +0.0009 | 0.8 / 0.81 / 0.79 | 0.789 |  |  | 8/16 | +0.035 | -0.025 |  | +0.3 / +0.2 |  |
| MNQ | 60 | h16 | +0.015 | -0.040 .. +0.070 | +0.0021 | 0.59 / 0.59 / 0.57 | 0.57 |  |  | 9/16 | +0.019 | +0.012 |  | +0.6 / +0.5 |  |
| MNQ | 60 | eod * | +0.021 | -0.037 .. +0.079 | +0.0028 | 0.47 / 0.48 / 0.46 | 0.455 | 1 | 1 | 10/16 | +0.010 | +0.032 | False | +0.7 / +0.7 |  |
| MYM | 5 | h1 | +0.008 | +0.002 .. +0.014 | +0.0036 | 0.0066 / 0.007 / 0.027 | 0.0258 |  |  | 5/8 | n/a | +0.008 |  | +2.8 / +2.7 |  |
| MYM | 5 | h2 | +0.036 | +0.024 .. +0.048 | +0.0093 | 2.6e-09 / 4.1e-10 / 5.1e-08 | 0.000527 |  |  | 7/8 | n/a | +0.036 |  | +7.8 / +6.0 |  |
| MYM | 5 | h4 * | +0.089 | +0.067 .. +0.112 | +0.0144 | 3.2e-15 / 7.6e-16 / 3.7e-18 | 0.000527 | 1.36e-12 | 0 | 8/8 | n/a | +0.089 | True | +13.0 / +7.9 | 0.025 |
| MYM | 5 | h8 | +0.145 | +0.108 .. +0.182 | +0.0167 | 2.4e-14 / 3.4e-14 / 1.1e-23 | 0.000527 |  |  | 8/8 | n/a | +0.145 |  | +14.5 / +7.6 |  |
| MYM | 5 | h16 | +0.188 | +0.135 .. +0.240 | +0.0169 | 2.2e-12 / 1.1e-12 / 7.7e-25 | 0.000527 |  |  | 8/8 | n/a | +0.188 |  | +13.2 / +7.0 |  |
| MYM | 5 | eod | +0.882 | +0.623 .. +1.140 | +0.0177 | 2.2e-11 / 6.1e-11 / 5e-25 | 0.000527 |  |  | 8/8 | n/a | +0.882 |  | +11.7 / +6.7 |  |
| MYM | 15 | h1 | -0.002 | -0.012 .. +0.009 | -0.0007 | 0.74 / 0.74 / 0.77 | 0.763 |  |  | 4/8 | n/a | -0.002 |  | -0.3 / -0.3 |  |
| MYM | 15 | h2 | +0.034 | +0.019 .. +0.049 | +0.0077 | 1.4e-05 / 2.5e-05 / 0.0018 | 0.00369 |  |  | 8/8 | n/a | +0.034 |  | +4.3 / +4.3 |  |
| MYM | 15 | h4 | +0.062 | +0.035 .. +0.089 | +0.0084 | 5.4e-06 / 1e-05 / 0.00077 | 0.00316 |  |  | 8/8 | n/a | +0.062 |  | +5.1 / +4.6 | 0.042 |
| MYM | 15 | h8 | +0.137 | +0.091 .. +0.183 | +0.0144 | 5.2e-09 / 6e-09 / 7e-08 | 0.000527 |  |  | 8/8 | n/a | +0.137 |  | +7.9 / +5.8 |  |
| MYM | 15 | h16 * | +0.320 | +0.221 .. +0.419 | +0.0239 | 2.4e-10 / 5.5e-10 / 1e-21 | 0.000527 | 1.7e-07 | 0 | 8/8 | n/a | +0.320 | True | +12.4 / +6.3 |  |
| MYM | 15 | eod | +0.825 | +0.569 .. +1.081 | +0.0255 | 2.8e-10 / 1.2e-09 / 4.6e-25 | 0.000527 |  |  | 8/8 | n/a | +0.825 |  | +12.5 / +6.3 |  |
| MYM | 60 | h1 | +0.009 | -0.008 .. +0.026 | +0.0044 | 0.31 / 0.29 / 0.33 | 0.323 |  |  | 5/8 | n/a | +0.009 |  | +1.0 / +1.0 |  |
| MYM | 60 | h2 | +0.001 | -0.023 .. +0.025 | +0.0003 | 0.95 / 0.95 / 0.95 | 0.947 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 60 | h4 | -0.023 | -0.062 .. +0.017 | -0.0056 | 0.26 / 0.24 / 0.21 | 0.211 |  |  | 5/8 | n/a | -0.023 |  | -1.2 / -1.1 | 0.055 |
| MYM | 60 | h8 * | -0.038 | -0.092 .. +0.017 | -0.0067 | 0.17 / 0.17 / 0.14 | 0.139 | 1 | 1 | 5/8 | n/a | -0.038 | False | -1.5 / -1.4 |  |
| MYM | 60 | h16 | -0.031 | -0.108 .. +0.047 | -0.0042 | 0.43 / 0.43 / 0.41 | 0.408 |  |  | 5/8 | n/a | -0.031 |  | -0.8 / -0.8 |  |
| MYM | 60 | eod | -0.016 | -0.098 .. +0.066 | -0.0021 | 0.7 / 0.69 / 0.68 | 0.672 |  |  | 5/8 | n/a | -0.016 |  | -0.4 / -0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.001 | -0.004 .. +0.001 | -0.3% | -0.006 | 0.74 |  | 10/16 |
| MES | 5 | h2 | -0.005 | -0.010 .. -0.001 | -0.7% | -0.013 | 0.18 |  | 10/16 |
| MES | 5 | h4 | -0.012 | -0.019 .. -0.005 | -1.2% | -0.028 | 0.0099 |  | 14/16 |
| MES | 5 | h8 | -0.028 | -0.039 .. -0.017 | -2.0% | -0.060 | 5.4e-07 |  | 15/16 |
| MES | 5 | h16 | -0.048 | -0.065 .. -0.031 | -2.3% | -0.122 | 1.1e-07 |  | 15/16 |
| MES | 5 | eod * | -0.545 | -0.728 .. -0.363 | -5.5% | -0.985 | 4.8e-09 | 1.4e-06 | 15/16 |
| MES | 15 | h1 | -0.007 | -0.012 .. -0.002 | -1.4% | -0.023 | 0.029 |  | 12/16 |
| MES | 15 | h2 | -0.019 | -0.026 .. -0.012 | -2.6% | -0.046 | 6.7e-07 |  | 15/16 |
| MES | 15 | h4 | -0.038 | -0.051 .. -0.026 | -3.6% | -0.089 | 1.4e-08 |  | 16/16 |
| MES | 15 | h8 | -0.065 | -0.084 .. -0.046 | -4.2% | -0.173 | 3e-11 |  | 15/16 |
| MES | 15 | h16 | -0.096 | -0.126 .. -0.067 | -4.2% | -0.334 | 2e-10 |  | 14/16 |
| MES | 15 | eod * | -0.489 | -0.612 .. -0.365 | -8.9% | -0.831 | 1e-14 | 4.27e-12 | 15/16 |
| MES | 60 | h1 | -0.016 | -0.025 .. -0.007 | -3.2% | -0.045 | 0.034 |  | 12/16 |
| MES | 60 | h2 * | -0.028 | -0.041 .. -0.014 | -3.7% | -0.060 | 0.00053 | 0.0956 | 12/16 |
| MES | 60 | h4 | -0.029 | -0.048 .. -0.011 | -2.8% | -0.072 | 0.018 |  | 10/16 |
| MES | 60 | h8 | -0.039 | -0.064 .. -0.015 | -2.6% | -0.096 | 0.039 |  | 12/16 |
| MES | 60 | h16 | -0.034 | -0.066 .. -0.001 | -1.6% | -0.096 | 0.051 |  | 9/16 |
| MES | 60 | eod | -0.026 | -0.059 .. +0.007 | -1.2% | -0.100 | 0.14 |  | 11/16 |
| MNQ | 5 | h1 | -0.011 | -0.015 .. -0.008 | -2.1% | -0.019 | 3.4e-11 |  | 15/16 |
| MNQ | 5 | h2 | -0.029 | -0.034 .. -0.023 | -3.7% | -0.044 | 5.6e-17 |  | 16/16 |
| MNQ | 5 | h4 | -0.055 | -0.066 .. -0.045 | -5.0% | -0.099 | 2.9e-19 |  | 15/16 |
| MNQ | 5 | h8 | -0.111 | -0.133 .. -0.088 | -6.8% | -0.212 | 2.7e-22 |  | 16/16 |
| MNQ | 5 | h16 | -0.200 | -0.241 .. -0.158 | -8.3% | -0.434 | 5e-21 |  | 16/16 |
| MNQ | 5 | eod * | -1.177 | -1.408 .. -0.945 | -9.4% | -2.444 | 2.5e-23 | 1.51e-20 | 16/16 |
| MNQ | 15 | h1 | -0.024 | -0.029 .. -0.018 | -4.4% | -0.057 | 5.1e-07 |  | 15/16 |
| MNQ | 15 | h2 | -0.054 | -0.066 .. -0.041 | -6.9% | -0.108 | 3.8e-12 |  | 16/16 |
| MNQ | 15 | h4 | -0.112 | -0.141 .. -0.083 | -9.9% | -0.216 | 2e-14 |  | 15/16 |
| MNQ | 15 | h8 | -0.179 | -0.223 .. -0.136 | -10.7% | -0.432 | 7.4e-16 |  | 15/16 |
| MNQ | 15 | h16 * | -0.209 | -0.260 .. -0.159 | -8.3% | -0.743 | 3.8e-16 | 1.64e-13 | 16/16 |
| MNQ | 15 | eod | -0.807 | -1.013 .. -0.601 | -12.7% | -1.437 | 1.7e-14 |  | 15/16 |
| MNQ | 60 | h1 | -0.018 | -0.027 .. -0.008 | -3.3% | -0.047 | 0.0065 |  | 12/16 |
| MNQ | 60 | h2 | -0.025 | -0.039 .. -0.011 | -3.3% | -0.057 | 0.0051 |  | 12/16 |
| MNQ | 60 | h4 * | -0.034 | -0.053 .. -0.015 | -3.1% | -0.065 | 0.002 | 0.324 | 12/16 |
| MNQ | 60 | h8 | -0.036 | -0.063 .. -0.010 | -2.3% | -0.079 | 0.076 |  | 13/16 |
| MNQ | 60 | h16 | -0.026 | -0.064 .. +0.013 | -1.2% | -0.069 | 0.21 |  | 11/16 |
| MNQ | 60 | eod | -0.025 | -0.066 .. +0.015 | -1.1% | -0.071 | 0.22 |  | 10/16 |
| MYM | 5 | h1 | -0.027 | -0.032 .. -0.022 | -5.1% | -0.046 | 1.6e-22 |  | 8/8 |
| MYM | 5 | h2 | -0.053 | -0.063 .. -0.043 | -7.0% | -0.087 | 4.4e-22 |  | 8/8 |
| MYM | 5 | h4 | -0.110 | -0.130 .. -0.089 | -10.0% | -0.182 | 5e-24 |  | 8/8 |
| MYM | 5 | h8 | -0.194 | -0.231 .. -0.158 | -12.2% | -0.350 | 5.9e-24 |  | 8/8 |
| MYM | 5 | h16 | -0.274 | -0.324 .. -0.224 | -11.7% | -0.605 | 5e-25 |  | 8/8 |
| MYM | 5 | eod * | -1.407 | -1.658 .. -1.155 | -12.0% | -2.397 | 6e-28 | 3.95e-25 | 8/8 |
| MYM | 15 | h1 | -0.031 | -0.039 .. -0.024 | -5.9% | -0.066 | 8.3e-11 |  | 8/8 |
| MYM | 15 | h2 | -0.068 | -0.083 .. -0.054 | -8.9% | -0.133 | 8.2e-14 |  | 8/8 |
| MYM | 15 | h4 | -0.134 | -0.166 .. -0.102 | -12.0% | -0.258 | 1.7e-12 |  | 8/8 |
| MYM | 15 | h8 * | -0.204 | -0.253 .. -0.154 | -12.4% | -0.509 | 4.6e-15 | 1.9e-12 | 8/8 |
| MYM | 15 | h16 | -0.351 | -0.439 .. -0.263 | -14.3% | -0.877 | 2.6e-14 |  | 8/8 |
| MYM | 15 | eod | -0.910 | -1.145 .. -0.675 | -15.1% | -1.428 | 2.5e-13 |  | 8/8 |
| MYM | 60 | h1 | -0.021 | -0.036 .. -0.006 | -4.0% | -0.056 | 0.18 |  | 4/8 |
| MYM | 60 | h2 * | -0.034 | -0.054 .. -0.015 | -4.6% | -0.076 | 0.024 | 1 | 6/8 |
| MYM | 60 | h4 | -0.026 | -0.055 .. +0.004 | -2.4% | -0.082 | 0.45 |  | 4/8 |
| MYM | 60 | h8 | -0.059 | -0.094 .. -0.023 | -3.8% | -0.118 | 0.059 |  | 6/8 |
| MYM | 60 | h16 | -0.027 | -0.074 .. +0.021 | -1.3% | -0.069 | 0.53 |  | 4/8 |
| MYM | 60 | eod | -0.024 | -0.075 .. +0.027 | -1.1% | -0.061 | 0.39 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.06 pts | -0.23 .. +0.35 | 0.68 |
| MES | 15 | +0.47 pts | +0.03 .. +0.91 | 0.051 |
| MES | 60 | -0.01 pts | -0.97 .. +0.94 | 0.98 |
| MNQ | 5 | +0.30 pts | +0.03 .. +0.58 | 0.029 |
| MNQ | 15 | +0.29 pts | -0.20 .. +0.79 | 0.35 |
| MNQ | 60 | +0.76 pts | -0.21 .. +1.73 | 0.12 |
| MYM | 5 | +0.22 pts | -0.16 .. +0.61 | 0.28 |
| MYM | 15 | +0.21 pts | -0.43 .. +0.85 | 0.54 |
| MYM | 60 | -0.45 pts | -1.82 .. +0.91 | 0.51 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 185187 | +0.001 | 0.392 | +0.03 | -3.47 | -3.50 | -3.42 | -3.47 |
| MES | 5 | h2 | event | long | 185187 | +0.007 | 0.392 | +0.08 | -3.42 | -3.47 | -3.36 | -3.44 |
| MES | 5 | h4 | event | long | 185187 | +0.014 | 0.392 | +0.14 | -3.36 | -3.43 | -3.27 | -3.37 |
| MES | 5 | h8 | event | long | 185187 | +0.032 | 0.392 | +0.30 | -3.20 | -3.35 | -2.98 | -3.23 |
| MES | 5 | h16 | event | long | 185187 | +0.060 | 0.392 | +0.52 | -2.98 | -3.21 | -2.64 | -3.07 |
| MES | 5 | eod | event | long | 185187 | +0.774 | 0.392 | +4.26 | +0.76 | -0.10 | +2.06 | +0.46 |
| MES | 15 | h1 | event | long | 52292 | +0.008 | 0.192 | +0.13 | -3.37 | -3.43 | -3.30 | -3.41 |
| MES | 15 | h2 | event | long | 52292 | +0.020 | 0.192 | +0.27 | -3.23 | -3.32 | -3.14 | -3.30 |
| MES | 15 | h4 | event | long | 52292 | +0.039 | 0.192 | +0.58 | -2.92 | -3.20 | -2.60 | -3.03 |
| MES | 15 | h8 | event | long | 52292 | +0.061 | 0.192 | +0.92 | -2.58 | -2.86 | -2.25 | -2.65 |
| MES | 15 | h16 | event | long | 52292 | +0.091 | 0.192 | +1.38 | -2.12 | -2.42 | -1.78 | -1.98 |
| MES | 15 | eod | event | long | 52292 | +0.406 | 0.192 | +5.20 | +1.70 | +0.10 | +3.49 | +2.69 |
| MES | 60 | h1 | event | long | 13886 | +0.006 | 0.093 | +0.26 | -3.24 | -3.28 | -3.19 | -3.29 |
| MES | 60 | h2 | event | long | 13886 | +0.014 | 0.093 | +0.63 | -2.87 | -2.91 | -2.83 | -3.03 |
| MES | 60 | h4 | event | long | 13886 | +0.022 | 0.093 | +0.90 | -2.60 | -2.56 | -2.64 | -3.06 |
| MES | 60 | h8 | event | short | 13886 | -0.043 | 0.093 | -1.59 | -5.09 | -5.30 | -4.86 | -3.95 |
| MES | 60 | h16 | event | long | 13886 | +0.115 | 0.093 | +3.85 | +0.35 | -0.14 | +0.86 | -2.40 |
| MES | 60 | eod | event | long | 13886 | +0.141 | 0.093 | +4.80 | +1.30 | +0.02 | +2.61 | -2.26 |
| MNQ | 5 | h1 | event | long | 145574 | +0.007 | 0.130 | +0.10 | -1.90 | -1.97 | -1.82 | -1.92 |
| MNQ | 5 | h2 | event | long | 145574 | +0.014 | 0.130 | +0.13 | -1.87 | -1.95 | -1.78 | -1.85 |
| MNQ | 5 | h4 | event | long | 145574 | +0.027 | 0.130 | +0.30 | -1.70 | -1.90 | -1.51 | -1.63 |
| MNQ | 5 | h8 | event | long | 145574 | +0.046 | 0.130 | +0.50 | -1.50 | -1.81 | -1.20 | -1.40 |
| MNQ | 5 | h16 | event | long | 145574 | +0.078 | 0.130 | +0.79 | -1.21 | -1.70 | -0.73 | -1.19 |
| MNQ | 5 | eod | event | long | 145574 | +0.851 | 0.130 | +5.49 | +3.49 | +0.89 | +6.05 | +4.73 |
| MNQ | 15 | h1 | event | short | 50582 | -0.011 | 0.073 | -0.11 | -2.11 | -2.06 | -2.17 | -1.95 |
| MNQ | 15 | h2 | event | long | 50582 | +0.018 | 0.073 | +0.25 | -1.75 | -1.88 | -1.62 | -1.86 |
| MNQ | 15 | h4 | event | long | 50582 | +0.031 | 0.073 | +0.36 | -1.64 | -1.73 | -1.55 | -1.81 |
| MNQ | 15 | h8 | event | long | 50582 | +0.052 | 0.073 | +1.07 | -0.93 | -1.48 | -0.39 | -1.31 |
| MNQ | 15 | h16 | event | long | 50582 | +0.108 | 0.073 | +2.00 | -0.00 | -1.00 | +0.98 | +0.12 |
| MNQ | 15 | eod | event | long | 50582 | +0.453 | 0.073 | +6.94 | +4.94 | +1.61 | +8.23 | +7.24 |
| MNQ | 60 | h1 | event | long | 14765 | +0.017 | 0.037 | +0.61 | -1.39 | -1.49 | -1.27 | -1.71 |
| MNQ | 60 | h2 | event | long | 14765 | +0.023 | 0.037 | +1.07 | -0.93 | -1.22 | -0.62 | -1.51 |
| MNQ | 60 | h4 | event | long | 14765 | +0.045 | 0.037 | +2.51 | +0.51 | -0.92 | +2.06 | -0.55 |
| MNQ | 60 | h8 | event | long | 14765 | +0.072 | 0.037 | +2.57 | +0.57 | +0.20 | +0.97 | -1.24 |
| MNQ | 60 | h16 | event | long | 14765 | +0.138 | 0.037 | +5.97 | +3.97 | +1.07 | +7.13 | +0.47 |
| MNQ | 60 | eod | event | long | 14765 | +0.181 | 0.037 | +7.99 | +5.99 | +1.59 | +10.77 | +0.85 |
| MYM | 5 | h1 | event | long | 69680 | +0.002 | 0.165 | +0.06 | -1.94 | +nan | -1.94 | -1.90 |
| MYM | 5 | h2 | event | long | 69680 | +0.009 | 0.165 | +0.14 | -1.86 | +nan | -1.86 | -1.71 |
| MYM | 5 | h4 | event | long | 69680 | +0.016 | 0.165 | +0.23 | -1.77 | +nan | -1.77 | -1.34 |
| MYM | 5 | h8 | event | long | 69680 | +0.019 | 0.165 | +0.30 | -1.70 | +nan | -1.70 | -0.96 |
| MYM | 5 | h16 | event | long | 69680 | +0.027 | 0.165 | +0.54 | -1.46 | +nan | -1.46 | -0.58 |
| MYM | 5 | eod | event | long | 69680 | +0.364 | 0.165 | +3.65 | +1.65 | +nan | +1.65 | +5.17 |
| MYM | 15 | h1 | event | short | 25341 | -0.001 | 0.094 | -0.01 | -2.01 | +nan | -2.01 | -1.97 |
| MYM | 15 | h2 | event | long | 25341 | +0.013 | 0.094 | +0.20 | -1.80 | +nan | -1.80 | -1.55 |
| MYM | 15 | h4 | event | long | 25341 | +0.009 | 0.094 | +0.36 | -1.64 | +nan | -1.64 | -0.97 |
| MYM | 15 | h8 | event | long | 25341 | +0.014 | 0.094 | +0.61 | -1.39 | +nan | -1.39 | +0.17 |
| MYM | 15 | h16 | event | long | 25341 | +0.009 | 0.094 | +1.16 | -0.84 | +nan | -0.84 | +3.06 |
| MYM | 15 | eod | event | long | 25341 | +0.153 | 0.094 | +3.44 | +1.44 | +nan | +1.44 | +10.17 |
| MYM | 60 | h1 | event | long | 7037 | +0.008 | 0.047 | +0.20 | -1.80 | +nan | -1.80 | -1.80 |
| MYM | 60 | h2 | event | long | 7037 | +0.005 | 0.047 | +0.22 | -1.78 | +nan | -1.78 | -1.91 |
| MYM | 60 | h4 | event | short | 7037 | +0.012 | 0.047 | +0.21 | -1.79 | +nan | -1.79 | -1.54 |
| MYM | 60 | h8 | event | short | 7037 | +0.019 | 0.047 | +0.20 | -1.80 | +nan | -1.80 | -1.37 |
| MYM | 60 | h16 | event | short | 7037 | -0.008 | 0.047 | -1.44 | -3.44 | +nan | -3.44 | -2.12 |
| MYM | 60 | eod | event | short | 7037 | -0.038 | 0.047 | -2.50 | -4.50 | +nan | -4.50 | -2.33 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.017 | -0.027 | -0.016 | -0.003 | +0.003 | +0.000 | +0.000 | +0.003 | +0.005 | +0.011 | +0.013 |
| MES | 15 | -0.011 | -0.040 | -0.040 | -0.012 | +0.006 | +0.000 | +0.006 | +0.013 | +0.023 | +0.026 | +0.020 |
| MES | 60 | -0.108 | -0.106 | -0.061 | -0.033 | +0.009 | +0.000 | -0.001 | -0.001 | -0.012 | -0.020 | -0.007 |
| MNQ | 5 | -0.036 | -0.045 | -0.027 | -0.009 | +0.005 | +0.000 | +0.004 | +0.008 | +0.013 | +0.018 | +0.016 |
| MNQ | 15 | -0.039 | -0.060 | -0.044 | -0.014 | +0.007 | +0.000 | +0.006 | +0.008 | +0.008 | +0.009 | +0.031 |
| MNQ | 60 | -0.105 | -0.088 | -0.048 | -0.018 | +0.014 | +0.000 | +0.006 | +0.002 | +0.005 | -0.001 | +0.012 |
| MYM | 5 | -0.050 | -0.065 | -0.038 | -0.015 | +0.001 | +0.000 | +0.003 | +0.013 | +0.022 | +0.029 | +0.033 |
| MYM | 15 | -0.040 | -0.061 | -0.057 | -0.017 | +0.003 | +0.000 | +0.003 | +0.014 | +0.011 | +0.023 | +0.022 |
| MYM | 60 | -0.178 | -0.166 | -0.064 | -0.021 | +0.006 | +0.000 | +0.004 | -0.002 | -0.028 | -0.050 | -0.025 |

## Calibration

- MES 5-min: 1036271 bars, 185187 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 52292 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 13886 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 145574 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 50582 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 14765 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 69680 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 25341 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 7037 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 35276 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.

## Plain-$ cross-check (zoo.dollar_check)

Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 units can overweight quiet bars at long holds; a direction claim must survive this check.

FINAL WORD: DIRECTION: R20 units only - NOT confirmed in plain $ (treat as none)

| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | 5 | dir_h16 | all | 185187 | INCONCLUSIVE | +0.87 | +0.11 | 0.14 | +0.7 | 3.50 |
| ES | 5 | dir_h16 | 2018-25H1 | 74434 | INCONCLUSIVE | +0.87 | +0.33 | 0.34 | +1.0 | 3.50 |
| ES | 15 | dir_eod | all | 52292 | REAL & TRADABLE | +9.69 | +0.41 | 2.06 | +0.2 | 3.50 |
| ES | 15 | dir_eod | 2018-25H1 | 24637 | REAL & TRADABLE | +9.69 | +1.12 | 4.02 | +0.3 | 3.50 |
| ES | 60 | dir_h2 | all | 13886 | CONFIDENTLY NOTHING | +0.49 | +0.02 | 0.36 | +0.0 | 3.50 |
| ES | 60 | dir_h2 | 2018-25H1 | 6846 | CONFIDENTLY NOTHING | +0.49 | -0.20 | 0.70 | -0.3 | 3.50 |
| NQ | 5 | dir_h8 | all | 145574 | REAL BUT TOO SMALL | +1.03 | +0.24 | 0.16 | +1.5 | 2.00 |
| NQ | 5 | dir_h8 | 2018-25H1 | 73321 | REAL BUT TOO SMALL | +1.03 | +0.45 | 0.31 | +1.4 | 2.00 |
| NQ | 15 | dir_eod | all | 50582 | REAL & TRADABLE | +15.10 | +1.09 | 3.49 | +0.3 | 2.00 |
| NQ | 15 | dir_eod | 2018-25H1 | 25412 | REAL & TRADABLE | +15.10 | +1.90 | 6.57 | +0.3 | 2.00 |
| NQ | 60 | dir_eod | all | 14765 | INCONCLUSIVE | +5.53 | +1.97 | 3.72 | +0.5 | 2.00 |
| NQ | 60 | dir_eod | 2018-25H1 | 7071 | INCONCLUSIVE | +5.53 | +4.56 | 7.68 | +0.6 | 2.00 |
| YM | 5 | dir_h4 | all | 69680 | REAL BUT TOO SMALL | +0.66 | +0.16 | 0.09 | +1.7 | 2.00 |
| YM | 5 | dir_h4 | 2018-25H1 | 69680 | REAL BUT TOO SMALL | +0.66 | +0.16 | 0.09 | +1.7 | 2.00 |
| YM | 15 | dir_h16 | all | 25341 | REAL & TRADABLE | +5.06 | +0.28 | 0.77 | +0.4 | 2.00 |
| YM | 15 | dir_h16 | 2018-25H1 | 25341 | REAL & TRADABLE | +5.06 | +0.28 | 0.77 | +0.4 | 2.00 |
| YM | 60 | dir_h8 | all | 7037 | INCONCLUSIVE | +0.63 | +2.36 | 1.42 | +1.7 | 2.00 |
| YM | 60 | dir_h8 | 2018-25H1 | 7037 | INCONCLUSIVE | +0.63 | +2.36 | 1.42 | +1.7 | 2.00 |
