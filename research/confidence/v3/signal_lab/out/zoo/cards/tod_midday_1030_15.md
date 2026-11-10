# Impact card: tod_midday_1030_15

bar closes in the midday_1030_15 block (ET) vs all other bars [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.002 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.016 R20 or more 80% of the time).
- MES 5-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.051 R20, CONFIRMED, q=1.81e-216, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (30 min), p=0.78; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 15-min size: the market moves 16% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.878 R20, CONFIRMED, q=1.32e-17, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.02 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.088 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.084 R20 over the rest of the session (to 16:45), p=0.11; we would catch an effect of 0.066 R20 or more 80% of the time).
- MES 60-min size: the market moves 44% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.952 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.10 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.066 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.323 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 16% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.084 R20, CONFIRMED, q=1.11e-264, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.99 at recent bar sizes, 90% range up to $1.13); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.121 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 14% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.877 R20, CONFIRMED, q=1.2e-07, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.73 at recent bar sizes, 90% range up to $2.08); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.098 R20 over the rest of the session (to 16:45), p=0.059; we would catch an effect of 0.066 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 54% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.285 R20, CONFIRMED, q=0, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.67 at recent bar sizes, 90% range up to $5.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.015 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.036 R20 or more 80% of the time).
- MYM 5-min size: the market moves 13% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.070 R20, CONFIRMED, q=1.24e-112, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.72 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.107 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.008 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MYM 15-min size: the market moves 15% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.926 R20, CONFIRMED, q=7.76e-06, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.20 at recent bar sizes, 90% range up to $2.25); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.029 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.096 R20 or more 80% of the time).
- MYM 60-min size: the market moves 46% LESS after the event than after matched bars over the rest of the session (to 16:45) (-1.029 R20, CONFIRMED, q=1.07e-168, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.91 at recent bar sizes, 90% range up to $3.79); about 11.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.002 | -0.005 .. +0.001 | -0.0012 | 0.16 / 0.17 / 0.78 | nan | 1 | 1 | 9/16 | -0.003 | -0.001 | False | -1.3 / -1.4 |  |
| MES | 5 | h2 | -0.001 | -0.006 .. +0.005 | -0.0003 | 0.8 / 0.8 / 0.84 | nan |  |  | 8/16 | -0.003 | +0.002 |  | -0.3 / -0.2 |  |
| MES | 5 | h4 | +0.001 | -0.010 .. +0.012 | +0.0002 | 0.91 / 0.91 / 0.89 | nan |  |  | 10/16 | -0.005 | +0.006 |  | +0.2 / +0.1 | 0.016 |
| MES | 5 | h8 | +0.008 | -0.013 .. +0.030 | +0.0017 | 0.44 / 0.45 / 0.96 | nan |  |  | 9/16 | +0.001 | +0.016 |  | +1.8 / +0.8 |  |
| MES | 5 | h16 | +0.019 | -0.023 .. +0.061 | +0.0026 | 0.37 / 0.38 / 0.99 | nan |  |  | 10/16 | +0.016 | +0.022 |  | +2.9 / +0.9 |  |
| MES | 5 | eod | -0.212 | -0.637 .. +0.212 | -0.0057 | 0.33 / 0.33 / 0.98 | nan |  |  | 10/16 | -0.456 | +0.030 |  | -9.7 / -1.0 |  |
| MES | 15 | h1 | +0.001 | -0.004 .. +0.007 | +0.0009 | 0.62 / 0.61 / 0.9 | nan |  |  | 9/16 | +0.001 | +0.002 |  | +0.5 / +0.5 |  |
| MES | 15 | h2 * | +0.008 | -0.002 .. +0.018 | +0.0033 | 0.13 / 0.13 / 0.93 | nan | 1 | 1 | 9/16 | +0.007 | +0.009 | False | +1.9 / +1.5 |  |
| MES | 15 | h4 | +0.014 | -0.005 .. +0.034 | +0.0041 | 0.14 / 0.14 / 0.99 | nan |  |  | 10/16 | +0.018 | +0.010 |  | +2.4 / +1.5 | 0.028 |
| MES | 15 | h8 | +0.027 | -0.010 .. +0.065 | +0.0056 | 0.15 / 0.16 / 0.98 | nan |  |  | 12/16 | +0.037 | +0.018 |  | +3.2 / +1.4 |  |
| MES | 15 | h16 | +0.032 | -0.041 .. +0.105 | +0.0045 | 0.39 / 0.4 / 0.99 | nan |  |  | 8/16 | +0.032 | +0.032 |  | +2.6 / +0.9 |  |
| MES | 15 | eod | -0.091 | -0.338 .. +0.156 | -0.0050 | 0.47 / 0.47 / 0.91 | nan |  |  | 9/16 | -0.223 | +0.039 |  | -4.1 / -0.7 |  |
| MES | 60 | h1 | +0.011 | -0.003 .. +0.025 | +0.0059 | 0.13 / 0.15 / 0.94 | nan |  |  | 10/16 | +0.015 | +0.007 |  | +1.4 / +1.5 |  |
| MES | 60 | h2 | +0.021 | -0.005 .. +0.047 | +0.0078 | 0.12 / 0.14 / 0.97 | nan |  |  | 11/16 | +0.030 | +0.012 |  | +1.8 / +1.5 |  |
| MES | 60 | h4 | +0.025 | -0.021 .. +0.070 | +0.0066 | 0.29 / 0.31 / 0.98 | nan |  |  | 9/16 | +0.036 | +0.013 |  | +1.6 / +1.0 | 0.066 |
| MES | 60 | h8 | -0.007 | -0.059 .. +0.045 | -0.0014 | 0.79 / 0.79 / 0.94 | nan |  |  | 10/16 | -0.006 | -0.009 |  | -0.4 / -0.3 |  |
| MES | 60 | h16 | -0.062 | -0.130 .. +0.007 | -0.0092 | 0.078 / 0.078 / 0.91 | nan |  |  | 13/16 | -0.074 | -0.049 |  | -3.2 / -1.8 |  |
| MES | 60 | eod * | -0.084 | -0.153 .. -0.015 | -0.0119 | 0.017 / 0.018 / 0.89 | nan | 1 | 0.96 | 13/16 | -0.102 | -0.066 | False | -4.3 / -2.4 |  |
| MNQ | 5 | h1 | -0.000 | -0.003 .. +0.003 | -0.0002 | 0.8 / 0.8 / 0.84 | nan |  |  | 11/16 | -0.003 | +0.002 |  | -0.2 / -0.3 |  |
| MNQ | 5 | h2 | +0.001 | -0.005 .. +0.007 | +0.0003 | 0.72 / 0.72 / 0.86 | nan |  |  | 9/16 | -0.006 | +0.008 |  | +0.4 / +0.4 |  |
| MNQ | 5 | h4 | +0.002 | -0.011 .. +0.016 | +0.0005 | 0.72 / 0.72 / 0.89 | nan |  |  | 8/16 | -0.015 | +0.019 |  | +0.7 / +0.4 | 0.019 |
| MNQ | 5 | h8 | +0.008 | -0.017 .. +0.034 | +0.0011 | 0.53 / 0.53 / 0.92 | nan |  |  | 9/16 | -0.023 | +0.039 |  | +1.5 / +0.6 |  |
| MNQ | 5 | h16 | +0.012 | -0.036 .. +0.059 | +0.0011 | 0.64 / 0.64 / 0.97 | nan |  |  | 7/16 | -0.040 | +0.063 |  | +1.5 / +0.5 |  |
| MNQ | 5 | eod * | -0.323 | -0.876 .. +0.229 | -0.0065 | 0.25 / 0.26 / 1 | nan | 1 | 1 | 8/16 | -0.845 | +0.194 | False | -11.3 / -1.1 |  |
| MNQ | 15 | h1 | -0.001 | -0.007 .. +0.005 | -0.0004 | 0.8 / 0.79 / 0.81 | nan |  |  | 9/16 | -0.002 | +0.001 |  | -0.2 / -0.3 |  |
| MNQ | 15 | h2 | +0.002 | -0.008 .. +0.013 | +0.0006 | 0.7 / 0.7 / 0.82 | nan |  |  | 9/16 | -0.004 | +0.008 |  | +0.4 / +0.4 |  |
| MNQ | 15 | h4 | +0.000 | -0.020 .. +0.021 | +0.0001 | 0.97 / 0.97 / 0.88 | nan |  |  | 8/16 | -0.009 | +0.009 |  | +0.0 / +0.0 | 0.029 |
| MNQ | 15 | h8 | +0.003 | -0.035 .. +0.042 | +0.0005 | 0.86 / 0.86 / 0.97 | nan |  |  | 9/16 | -0.009 | +0.015 |  | +0.3 / +0.2 |  |
| MNQ | 15 | h16 | +0.001 | -0.076 .. +0.078 | +0.0001 | 0.98 / 0.98 / 0.95 | nan |  |  | 7/16 | -0.048 | +0.050 |  | +0.1 / +0.0 |  |
| MNQ | 15 | eod * | -0.121 | -0.427 .. +0.185 | -0.0048 | 0.44 / 0.45 / 0.92 | nan | 1 | 1 | 8/16 | -0.374 | +0.131 | False | -4.1 / -0.8 |  |
| MNQ | 60 | h1 | +0.012 | -0.003 .. +0.026 | +0.0060 | 0.11 / 0.12 / 0.94 | nan |  |  | 11/16 | +0.011 | +0.013 |  | +1.4 / +1.6 |  |
| MNQ | 60 | h2 | +0.021 | -0.005 .. +0.048 | +0.0076 | 0.11 / 0.11 / 0.99 | nan |  |  | 12/16 | +0.022 | +0.021 |  | +1.9 / +1.6 |  |
| MNQ | 60 | h4 | +0.033 | -0.013 .. +0.079 | +0.0083 | 0.16 / 0.17 / 1 | nan |  |  | 9/16 | +0.034 | +0.032 |  | +2.1 / +1.4 | 0.066 |
| MNQ | 60 | h8 | -0.000 | -0.053 .. +0.052 | -0.0000 | 1 / 1 / 0.95 | nan |  |  | 12/16 | -0.008 | +0.008 |  | -0.0 / -0.0 |  |
| MNQ | 60 | h16 | -0.070 | -0.140 .. +0.001 | -0.0097 | 0.052 / 0.061 / 0.91 | nan |  |  | 13/16 | -0.095 | -0.044 |  | -3.5 / -1.9 |  |
| MNQ | 60 | eod * | -0.098 | -0.169 .. -0.027 | -0.0131 | 0.0071 / 0.0099 / 0.89 | nan | 1 | 0.766 | 13/16 | -0.129 | -0.067 | False | -4.9 / -2.7 |  |
| MYM | 5 | h1 | -0.000 | -0.005 .. +0.004 | -0.0001 | 0.94 / 0.95 / 0.85 | nan |  |  | 4/8 | n/a | -0.000 |  | -0.1 / -0.1 |  |
| MYM | 5 | h2 | -0.000 | -0.011 .. +0.011 | -0.0000 | 1 / 1 / 0.85 | nan |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 5 | h4 | +0.001 | -0.024 .. +0.026 | +0.0001 | 0.95 / 0.95 / 0.86 | nan |  |  | 3/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.036 |
| MYM | 5 | h8 | +0.007 | -0.040 .. +0.054 | +0.0009 | 0.77 / 0.77 / 0.92 | nan |  |  | 3/8 | n/a | +0.007 |  | +0.9 / +0.3 |  |
| MYM | 5 | h16 * | +0.015 | -0.066 .. +0.095 | +0.0014 | 0.72 / 0.73 / 0.96 | nan | 1 | 1 | 6/8 | n/a | +0.015 | False | +1.3 / +0.4 |  |
| MYM | 5 | eod | -0.052 | -0.859 .. +0.755 | -0.0011 | 0.9 / 0.9 / 0.99 | nan |  |  | 5/8 | n/a | -0.052 |  | -1.3 / -0.1 |  |
| MYM | 15 | h1 | +0.003 | -0.005 .. +0.010 | +0.0014 | 0.49 / 0.51 / 0.84 | nan |  |  | 6/8 | n/a | +0.003 |  | +0.6 / +0.7 |  |
| MYM | 15 | h2 * | +0.008 | -0.008 .. +0.024 | +0.0023 | 0.34 / 0.35 / 0.9 | nan | 1 | 1 | 6/8 | n/a | +0.008 | False | +1.1 / +1.0 |  |
| MYM | 15 | h4 | +0.009 | -0.024 .. +0.043 | +0.0016 | 0.58 / 0.59 / 0.93 | nan |  |  | 5/8 | n/a | +0.009 |  | +0.9 / +0.6 | 0.048 |
| MYM | 15 | h8 | +0.020 | -0.046 .. +0.085 | +0.0026 | 0.56 / 0.57 / 0.99 | nan |  |  | 6/8 | n/a | +0.020 |  | +1.3 / +0.6 |  |
| MYM | 15 | h16 | +0.044 | -0.101 .. +0.190 | +0.0042 | 0.55 / 0.55 / 0.99 | nan |  |  | 4/8 | n/a | +0.044 |  | +2.1 / +0.6 |  |
| MYM | 15 | eod | +0.022 | -0.431 .. +0.475 | +0.0009 | 0.92 / 0.92 / 0.96 | nan |  |  | 3/8 | n/a | +0.022 |  | +0.5 / +0.1 |  |
| MYM | 60 | h1 | +0.004 | -0.018 .. +0.025 | +0.0019 | 0.74 / 0.74 / 0.95 | nan |  |  | 5/8 | n/a | +0.004 |  | +0.3 / +0.3 |  |
| MYM | 60 | h2 | +0.014 | -0.024 .. +0.053 | +0.0051 | 0.46 / 0.48 / 0.99 | nan |  |  | 5/8 | n/a | +0.014 |  | +0.9 / +0.7 |  |
| MYM | 60 | h4 * | +0.029 | -0.038 .. +0.096 | +0.0074 | 0.4 / 0.41 / 0.99 | nan | 1 | 1 | 5/8 | n/a | +0.029 | False | +1.3 / +0.8 | 0.096 |
| MYM | 60 | h8 | +0.029 | -0.047 .. +0.105 | +0.0055 | 0.45 / 0.46 / 0.99 | nan |  |  | 6/8 | n/a | +0.029 |  | +1.2 / +0.8 |  |
| MYM | 60 | h16 | +0.016 | -0.091 .. +0.123 | +0.0023 | 0.76 / 0.76 / 0.99 | nan |  |  | 5/8 | n/a | +0.016 |  | +0.6 / +0.3 |  |
| MYM | 60 | eod | +0.003 | -0.105 .. +0.112 | +0.0005 | 0.95 / 0.95 / 0.98 | nan |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.051 | -0.054 .. -0.048 | -10.2% | -0.092 | 7e-220 | 1.81e-216 | 16/16 |
| MES | 5 | h2 | -0.074 | -0.080 .. -0.069 | -10.6% | -0.142 | 5.2e-166 |  | 16/16 |
| MES | 5 | h4 | -0.109 | -0.118 .. -0.099 | -10.9% | -0.214 | 9.5e-110 |  | 16/16 |
| MES | 5 | h8 | -0.161 | -0.179 .. -0.143 | -11.2% | -0.326 | 7.4e-70 |  | 16/16 |
| MES | 5 | h16 | -0.210 | -0.242 .. -0.178 | -10.0% | -0.442 | 2.7e-37 |  | 16/16 |
| MES | 5 | eod | -4.851 | -5.185 .. -4.516 | -48.6% | -9.602 | 1e-177 |  | 16/16 |
| MES | 15 | h1 | +0.018 | +0.012 .. +0.025 | +3.6% | +0.043 | 6e-09 |  | 13/16 |
| MES | 15 | h2 | +0.033 | +0.023 .. +0.043 | +4.5% | +0.069 | 2.3e-10 |  | 12/16 |
| MES | 15 | h4 | +0.070 | +0.052 .. +0.088 | +6.7% | +0.144 | 3e-14 |  | 14/16 |
| MES | 15 | h8 | +0.144 | +0.113 .. +0.176 | +9.4% | +0.284 | 3.2e-19 |  | 16/16 |
| MES | 15 | h16 | +0.191 | +0.133 .. +0.249 | +8.4% | +0.343 | 9.5e-11 |  | 15/16 |
| MES | 15 | eod * | -0.878 | -1.064 .. -0.692 | -16.0% | -1.789 | 2.4e-20 | 1.32e-17 | 14/16 |
| MES | 60 | h1 | +0.281 | +0.265 .. +0.297 | +54.8% | +0.574 | 4e-274 |  | 16/16 |
| MES | 60 | h2 | +0.357 | +0.333 .. +0.380 | +48.3% | +0.710 | 5e-192 |  | 16/16 |
| MES | 60 | h4 | +0.344 | +0.306 .. +0.383 | +32.5% | +0.653 | 2.1e-69 |  | 16/16 |
| MES | 60 | h8 | -0.130 | -0.170 .. -0.090 | -8.6% | -0.311 | 2.7e-10 |  | 15/16 |
| MES | 60 | h16 | -0.817 | -0.864 .. -0.771 | -39.7% | -1.660 | 2.5e-260 |  | 16/16 |
| MES | 60 | eod * | -0.952 | -1.001 .. -0.902 | -43.9% | -1.902 | 0 | 0 | 16/16 |
| MNQ | 5 | h1 * | -0.084 | -0.088 .. -0.079 | -15.6% | -0.146 | 3.6e-268 | 1.11e-264 | 16/16 |
| MNQ | 5 | h2 | -0.126 | -0.135 .. -0.118 | -16.4% | -0.236 | 8.6e-175 |  | 16/16 |
| MNQ | 5 | h4 | -0.193 | -0.209 .. -0.177 | -17.4% | -0.373 | 3.5e-121 |  | 16/16 |
| MNQ | 5 | h8 | -0.308 | -0.339 .. -0.277 | -19.0% | -0.600 | 6.3e-84 |  | 16/16 |
| MNQ | 5 | h16 | -0.472 | -0.530 .. -0.415 | -19.7% | -0.937 | 1.7e-58 |  | 16/16 |
| MNQ | 5 | eod | -6.108 | -6.563 .. -5.654 | -48.6% | -12.027 | 5.4e-153 |  | 16/16 |
| MNQ | 15 | h1 | +0.015 | +0.008 .. +0.022 | +2.8% | +0.034 | 1.7e-05 |  | 12/16 |
| MNQ | 15 | h2 | +0.025 | +0.011 .. +0.039 | +3.2% | +0.055 | 0.00069 |  | 13/16 |
| MNQ | 15 | h4 | +0.047 | +0.015 .. +0.079 | +4.1% | +0.108 | 0.0043 |  | 13/16 |
| MNQ | 15 | h8 | +0.111 | +0.057 .. +0.164 | +6.6% | +0.227 | 4.9e-05 |  | 14/16 |
| MNQ | 15 | h16 | +0.149 | +0.078 .. +0.221 | +5.9% | +0.276 | 4.6e-05 |  | 15/16 |
| MNQ | 15 | eod * | -0.877 | -1.151 .. -0.602 | -13.8% | -1.717 | 3.8e-10 | 1.2e-07 | 15/16 |
| MNQ | 60 | h1 * | +0.285 | +0.271 .. +0.299 | +53.9% | +0.590 | 0 | 0 | 16/16 |
| MNQ | 60 | h2 | +0.341 | +0.319 .. +0.363 | +44.5% | +0.701 | 3.2e-201 |  | 16/16 |
| MNQ | 60 | h4 | +0.296 | +0.260 .. +0.333 | +26.8% | +0.582 | 3.8e-57 |  | 16/16 |
| MNQ | 60 | h8 | -0.209 | -0.250 .. -0.167 | -13.2% | -0.443 | 1.1e-22 |  | 16/16 |
| MNQ | 60 | h16 | -0.965 | -1.019 .. -0.912 | -44.0% | -1.920 | 8.9e-272 |  | 16/16 |
| MNQ | 60 | eod | -1.097 | -1.153 .. -1.041 | -47.7% | -2.160 | 0 |  | 16/16 |
| MYM | 5 | h1 * | -0.070 | -0.076 .. -0.064 | -13.1% | -0.123 | 8e-116 | 1.24e-112 | 8/8 |
| MYM | 5 | h2 | -0.101 | -0.113 .. -0.090 | -13.3% | -0.192 | 1.4e-67 |  | 8/8 |
| MYM | 5 | h4 | -0.145 | -0.169 .. -0.121 | -13.2% | -0.294 | 3.9e-32 |  | 8/8 |
| MYM | 5 | h8 | -0.216 | -0.262 .. -0.170 | -13.6% | -0.454 | 3.6e-20 |  | 8/8 |
| MYM | 5 | h16 | -0.304 | -0.379 .. -0.230 | -13.0% | -0.640 | 1.1e-15 |  | 8/8 |
| MYM | 5 | eod | -5.465 | -6.054 .. -4.876 | -46.6% | -10.850 | 8.1e-74 |  | 8/8 |
| MYM | 15 | h1 | +0.018 | +0.008 .. +0.029 | +3.4% | +0.036 | 0.00085 |  | 6/8 |
| MYM | 15 | h2 | +0.034 | +0.013 .. +0.055 | +4.5% | +0.061 | 0.0014 |  | 5/8 |
| MYM | 15 | h4 | +0.075 | +0.033 .. +0.117 | +6.7% | +0.137 | 0.00048 |  | 5/8 |
| MYM | 15 | h8 | +0.138 | +0.069 .. +0.206 | +8.4% | +0.265 | 7.7e-05 |  | 6/8 |
| MYM | 15 | h16 | +0.177 | +0.056 .. +0.298 | +7.2% | +0.306 | 0.0045 |  | 7/8 |
| MYM | 15 | eod * | -0.926 | -1.242 .. -0.611 | -15.4% | -1.842 | 2.8e-08 | 7.76e-06 | 8/8 |
| MYM | 60 | h1 | +0.309 | +0.283 .. +0.335 | +59.0% | +0.596 | 5.7e-120 |  | 8/8 |
| MYM | 60 | h2 | +0.372 | +0.335 .. +0.410 | +49.3% | +0.721 | 5.6e-84 |  | 8/8 |
| MYM | 60 | h4 | +0.329 | +0.270 .. +0.388 | +30.4% | +0.622 | 1e-27 |  | 8/8 |
| MYM | 60 | h8 | -0.177 | -0.239 .. -0.116 | -11.5% | -0.399 | 1.9e-08 |  | 8/8 |
| MYM | 60 | h16 | -0.897 | -0.966 .. -0.828 | -42.3% | -1.816 | 3.6e-143 |  | 8/8 |
| MYM | 60 | eod * | -1.029 | -1.099 .. -0.958 | -46.2% | -2.048 | 4.7e-172 | 1.07e-168 | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.63 pts | +0.11 .. +1.14 | 0.017 |
| MES | 15 | +0.81 pts | +0.01 .. +1.61 | 0.048 |
| MES | 60 | -0.65 pts | -1.74 .. +0.43 | 0.26 |
| MNQ | 5 | +0.46 pts | -0.04 .. +0.95 | 0.072 |
| MNQ | 15 | +0.60 pts | -0.12 .. +1.33 | 0.11 |
| MNQ | 60 | -0.89 pts | -1.95 .. +0.16 | 0.12 |
| MYM | 5 | +0.07 pts | -0.57 .. +0.71 | 0.85 |
| MYM | 15 | +0.26 pts | -0.83 .. +1.34 | 0.64 |
| MYM | 60 | -0.46 pts | -2.02 .. +1.10 | 0.57 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 205871 | +0.001 | 0.211 | -0.00 | -3.50 | -3.50 | -3.51 | -3.51 |
| MES | 5 | h2 | event | short | 205871 | -0.003 | 0.211 | -0.04 | -3.54 | -3.53 | -3.55 | -3.54 |
| MES | 5 | h4 | event | long | 205871 | +0.009 | 0.211 | +0.11 | -3.39 | -3.43 | -3.34 | -3.41 |
| MES | 5 | h8 | event | long | 205871 | +0.025 | 0.211 | +0.32 | -3.18 | -3.25 | -3.11 | -3.27 |
| MES | 5 | h16 | event | long | 205871 | +0.053 | 0.211 | +0.60 | -2.90 | -2.93 | -2.86 | -3.12 |
| MES | 5 | eod | event | short | 205871 | -0.163 | 0.211 | -1.89 | -5.39 | -5.00 | -5.77 | -5.17 |
| MES | 15 | h1 | event | long | 68551 | +0.002 | 0.129 | +0.07 | -3.43 | -3.47 | -3.40 | -3.43 |
| MES | 15 | h2 | event | long | 68551 | +0.010 | 0.129 | +0.24 | -3.26 | -3.34 | -3.18 | -3.28 |
| MES | 15 | h4 | event | long | 68551 | +0.022 | 0.129 | +0.46 | -3.04 | -3.08 | -3.01 | -3.11 |
| MES | 15 | h8 | event | long | 68551 | +0.047 | 0.129 | +0.91 | -2.59 | -2.66 | -2.53 | -2.77 |
| MES | 15 | h16 | event | long | 68551 | +0.077 | 0.129 | +1.61 | -1.89 | -2.16 | -1.61 | -2.23 |
| MES | 15 | eod | event | short | 68551 | -0.088 | 0.129 | -1.82 | -5.32 | -4.93 | -5.70 | -5.49 |
| MES | 60 | h1 | event | long | 18725 | +0.017 | 0.098 | +0.53 | -2.97 | -3.11 | -2.83 | -3.15 |
| MES | 60 | h2 | event | long | 18725 | +0.035 | 0.098 | +0.99 | -2.51 | -2.78 | -2.24 | -2.91 |
| MES | 60 | h4 | event | long | 18725 | +0.058 | 0.098 | +1.58 | -1.92 | -2.36 | -1.48 | -2.80 |
| MES | 60 | h8 | event | short | 18725 | -0.068 | 0.098 | -1.78 | -5.28 | -4.83 | -5.74 | -3.56 |
| MES | 60 | h16 | event | short | 18725 | -0.068 | 0.098 | -1.78 | -5.28 | -4.83 | -5.74 | -2.62 |
| MES | 60 | eod | event | short | 18725 | -0.068 | 0.098 | -1.78 | -5.28 | -4.83 | -5.74 | -2.09 |
| MNQ | 5 | h1 | event | short | 205868 | -0.002 | 0.079 | -0.04 | -2.04 | -2.01 | -2.06 | -2.04 |
| MNQ | 5 | h2 | event | long | 205868 | +0.005 | 0.079 | +0.09 | -1.91 | -1.97 | -1.85 | -1.86 |
| MNQ | 5 | h4 | event | long | 205868 | +0.010 | 0.079 | +0.20 | -1.80 | -1.94 | -1.66 | -1.69 |
| MNQ | 5 | h8 | event | long | 205868 | +0.025 | 0.079 | +0.49 | -1.51 | -1.82 | -1.20 | -1.35 |
| MNQ | 5 | h16 | event | long | 205868 | +0.051 | 0.079 | +0.89 | -1.11 | -1.60 | -0.62 | -1.00 |
| MNQ | 5 | eod | event | short | 205868 | -0.186 | 0.079 | -3.14 | -5.14 | -3.55 | -6.73 | -7.67 |
| MNQ | 15 | h1 | event | short | 68548 | -0.003 | 0.048 | -0.13 | -2.13 | -2.02 | -2.24 | -2.04 |
| MNQ | 15 | h2 | event | long | 68548 | +0.010 | 0.048 | +0.37 | -1.63 | -1.89 | -1.36 | -1.77 |
| MNQ | 15 | h4 | event | long | 68548 | +0.021 | 0.048 | +0.65 | -1.35 | -1.72 | -0.98 | -1.71 |
| MNQ | 15 | h8 | event | long | 68548 | +0.045 | 0.048 | +1.36 | -0.64 | -1.37 | +0.10 | -1.45 |
| MNQ | 15 | h16 | event | long | 68548 | +0.084 | 0.048 | +2.61 | +0.61 | -0.79 | +2.02 | -0.38 |
| MNQ | 15 | eod | event | short | 68548 | -0.101 | 0.048 | -3.05 | -5.05 | -3.49 | -6.61 | -7.40 |
| MNQ | 60 | h1 | event | long | 18724 | +0.020 | 0.038 | +0.78 | -1.22 | -1.71 | -0.73 | -1.49 |
| MNQ | 60 | h2 | event | long | 18724 | +0.038 | 0.038 | +1.35 | -0.65 | -1.41 | +0.11 | -1.19 |
| MNQ | 60 | h4 | event | long | 18724 | +0.069 | 0.038 | +2.28 | +0.28 | -0.89 | +1.45 | -0.89 |
| MNQ | 60 | h8 | event | short | 18724 | -0.083 | 0.038 | -2.58 | -4.58 | -3.46 | -5.71 | -2.25 |
| MNQ | 60 | h16 | event | short | 18724 | -0.083 | 0.038 | -2.58 | -4.58 | -3.46 | -5.71 | -0.89 |
| MNQ | 60 | eod | event | short | 18724 | -0.083 | 0.038 | -2.58 | -4.58 | -3.46 | -5.71 | -0.03 |
| MYM | 5 | h1 | event | short | 102646 | -0.001 | 0.107 | -0.02 | -2.02 | +nan | -2.02 | -2.02 |
| MYM | 5 | h2 | event | short | 102646 | -0.002 | 0.107 | -0.04 | -2.04 | +nan | -2.04 | -2.04 |
| MYM | 5 | h4 | event | long | 102646 | +0.006 | 0.107 | +0.10 | -1.90 | +nan | -1.90 | -1.89 |
| MYM | 5 | h8 | event | long | 102646 | +0.016 | 0.107 | +0.26 | -1.74 | +nan | -1.74 | -1.72 |
| MYM | 5 | h16 | event | long | 102646 | +0.029 | 0.107 | +0.48 | -1.52 | +nan | -1.52 | -1.49 |
| MYM | 5 | eod | event | short | 102646 | -0.136 | 0.107 | -2.22 | -4.22 | +nan | -4.22 | -3.72 |
| MYM | 15 | h1 | event | long | 34175 | +0.001 | 0.064 | +0.08 | -1.92 | +nan | -1.92 | -1.88 |
| MYM | 15 | h2 | event | long | 34175 | +0.005 | 0.064 | +0.22 | -1.78 | +nan | -1.78 | -1.69 |
| MYM | 15 | h4 | event | long | 34175 | +0.007 | 0.064 | +0.37 | -1.63 | +nan | -1.63 | -1.49 |
| MYM | 15 | h8 | event | long | 34175 | +0.019 | 0.064 | +0.79 | -1.21 | +nan | -1.21 | -1.06 |
| MYM | 15 | h16 | event | long | 34175 | +0.046 | 0.064 | +1.72 | -0.28 | +nan | -0.28 | -0.05 |
| MYM | 15 | eod | event | long | 34175 | +0.066 | 0.064 | +2.16 | +0.16 | +nan | +0.16 | +1.00 |
| MYM | 60 | h1 | event | long | 9330 | +0.006 | 0.049 | +0.44 | -1.56 | +nan | -1.56 | -1.66 |
| MYM | 60 | h2 | event | long | 9330 | +0.017 | 0.049 | +0.94 | -1.06 | +nan | -1.06 | -1.23 |
| MYM | 60 | h4 | event | long | 9330 | +0.034 | 0.049 | +1.61 | -0.39 | +nan | -0.39 | -0.75 |
| MYM | 60 | h8 | event | long | 9330 | +0.046 | 0.049 | +2.02 | +0.02 | +nan | +0.02 | -0.75 |
| MYM | 60 | h16 | event | long | 9330 | +0.046 | 0.049 | +2.02 | +0.02 | +nan | +0.02 | -1.16 |
| MYM | 60 | eod | event | long | 9330 | +0.046 | 0.049 | +2.02 | +0.02 | +nan | +0.02 | -1.64 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.000 | -0.000 | -0.000 | -0.000 | -0.001 | +0.000 | +0.000 | -0.000 | -0.001 | -0.000 | -0.000 |
| MES | 15 | +0.000 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +0.000 | -0.000 |
| MES | 60 | +0.000 | -0.000 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +nan | +nan |
| MNQ | 5 | -0.000 | -0.001 | -0.001 | -0.001 | -0.000 | +0.000 | -0.000 | -0.000 | -0.001 | -0.000 | -0.000 |
| MNQ | 15 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | +0.000 |
| MNQ | 60 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | +0.000 | -0.000 | -0.000 | -0.000 | +nan | +nan |
| MYM | 5 | -0.000 | +0.000 | -0.000 | -0.000 | -0.001 | +0.000 | -0.000 | -0.000 | -0.001 | +0.000 | -0.000 |
| MYM | 15 | -0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 | -0.000 | +0.000 | -0.000 | -0.000 | +0.000 |
| MYM | 60 | -0.000 | -0.000 | -0.000 | -0.000 | +0.000 | +0.000 | -0.000 | +0.000 | -0.000 | +nan | +nan |

## Calibration

- MES 5-min: 1036271 bars, 205871 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68551 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 18725 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 205868 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68548 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 18724 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 102646 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34175 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 9330 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
