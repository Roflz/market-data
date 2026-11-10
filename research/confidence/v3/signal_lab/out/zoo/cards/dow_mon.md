# Impact card: dow_mon

session weekday = mon vs other days [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: the market moves 2% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.008 R20, CONFIRMED, q=1.8e-08, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.01 at recent bar sizes, 90% range up to $0.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 15-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.017 R20, CONFIRMED, q=1.5e-08, 16 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.09 at recent bar sizes, 90% range up to $1.75); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.054 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.076 R20 or more 80% of the time).
- MES 60-min size: the market moves 9% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.047 R20, CONFIRMED, q=9.16e-15, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.50 at recent bar sizes, 90% range up to $6.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.365 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.036).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.31 at recent bar sizes, 90% range up to $1.33); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.016 R20, CONFIRMED, q=1.41e-05, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.15 at recent bar sizes, 90% range up to $3.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.139 R20 over the next 16 bars (16 h), p=0.88; we would catch an effect of 0.082 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 7% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.040 R20, CONFIRMED, q=9.54e-09, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.61 at recent bar sizes, 90% range up to $12.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.015 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.036 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.037).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.13 at recent bar sizes, 90% range up to $1.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.025 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.064 R20 or more 80% of the time).
- MYM 15-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.019 R20, possible, q=0.111, 7 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.41 at recent bar sizes, 90% range up to $3.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.012 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.113 R20 or more 80% of the time).
- MYM 60-min size: the market moves 8% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.043 R20, CONFIRMED, q=2.75e-05, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.41 at recent bar sizes, 90% range up to $10.02); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.001 | -0.002 .. +0.004 | +0.0006 | 0.52 / 0.53 / 0.58 | nan | 1 | 1 | 8/16 | -0.001 | +0.003 | False | +0.6 / +0.6 |  |
| MES | 5 | h2 | +0.001 | -0.006 .. +0.008 | +0.0004 | 0.76 / 0.77 / 0.78 | nan |  |  | 8/16 | -0.002 | +0.004 |  | +0.4 / +0.3 |  |
| MES | 5 | h4 | +0.001 | -0.014 .. +0.016 | +0.0003 | 0.9 / 0.9 / 0.9 | nan |  |  | 8/16 | -0.005 | +0.007 |  | +0.2 / +0.1 | 0.020 |
| MES | 5 | h8 | +0.003 | -0.028 .. +0.035 | +0.0006 | 0.84 / 0.84 / 0.84 | nan |  |  | 9/16 | -0.009 | +0.015 |  | +0.5 / +0.2 |  |
| MES | 5 | h16 | +0.014 | -0.048 .. +0.077 | +0.0018 | 0.66 / 0.66 / 0.65 | nan |  |  | 9/16 | -0.010 | +0.039 |  | +1.7 / +0.4 |  |
| MES | 5 | eod | +0.109 | -0.918 .. +1.136 | +0.0027 | 0.84 / 0.83 / 0.83 | nan |  |  | 9/16 | -0.352 | +0.567 |  | +2.8 / +0.2 |  |
| MES | 15 | h1 * | +0.004 | -0.003 .. +0.011 | +0.0021 | 0.25 / 0.25 / 0.26 | nan | 1 | 1 | 9/16 | -0.001 | +0.009 | False | +1.2 / +1.1 |  |
| MES | 15 | h2 | +0.003 | -0.010 .. +0.017 | +0.0011 | 0.64 / 0.65 / 0.64 | nan |  |  | 9/16 | -0.003 | +0.009 |  | +0.6 / +0.5 |  |
| MES | 15 | h4 | +0.003 | -0.027 .. +0.034 | +0.0007 | 0.84 / 0.84 / 0.81 | nan |  |  | 8/16 | -0.004 | +0.010 |  | +0.4 / +0.2 | 0.039 |
| MES | 15 | h8 | +0.008 | -0.052 .. +0.067 | +0.0013 | 0.8 / 0.8 / 0.78 | nan |  |  | 9/16 | -0.005 | +0.020 |  | +0.6 / +0.3 |  |
| MES | 15 | h16 | +0.016 | -0.110 .. +0.142 | +0.0018 | 0.8 / 0.8 / 0.79 | nan |  |  | 9/16 | -0.003 | +0.035 |  | +1.0 / +0.2 |  |
| MES | 15 | eod | -0.078 | -0.779 .. +0.622 | -0.0034 | 0.83 / 0.82 / 0.79 | nan |  |  | 7/16 | -0.219 | +0.062 |  | -1.7 / -0.2 |  |
| MES | 60 | h1 | +0.004 | -0.009 .. +0.016 | +0.0018 | 0.58 / 0.58 / 0.61 | nan |  |  | 9/16 | -0.007 | +0.014 |  | +0.6 / +0.5 |  |
| MES | 60 | h2 | +0.007 | -0.018 .. +0.032 | +0.0026 | 0.56 / 0.55 / 0.58 | nan |  |  | 9/16 | -0.013 | +0.028 |  | +0.8 / +0.6 |  |
| MES | 60 | h4 | +0.015 | -0.034 .. +0.064 | +0.0038 | 0.54 / 0.53 / 0.57 | nan |  |  | 9/16 | -0.026 | +0.057 |  | +1.2 / +0.6 | 0.076 |
| MES | 60 | h8 | +0.027 | -0.067 .. +0.122 | +0.0050 | 0.57 / 0.56 / 0.62 | nan |  |  | 9/16 | -0.055 | +0.110 |  | +1.6 / +0.6 |  |
| MES | 60 | h16 * | +0.054 | -0.116 .. +0.224 | +0.0075 | 0.54 / 0.53 / 0.59 | nan | 1 | 1 | 8/16 | -0.102 | +0.210 | False | +2.4 / +0.6 |  |
| MES | 60 | eod | +0.055 | -0.136 .. +0.247 | +0.0074 | 0.57 / 0.56 / 0.62 | nan |  |  | 8/16 | -0.137 | +0.248 |  | +2.4 / +0.6 |  |
| MNQ | 5 | h1 | -0.000 | -0.005 .. +0.005 | -0.0001 | 0.91 / 0.91 / 0.9 | nan |  |  | 9/16 | -0.001 | +0.000 |  | -0.1 / -0.1 |  |
| MNQ | 5 | h2 | -0.003 | -0.018 .. +0.012 | -0.0008 | 0.69 / 0.68 / 0.56 | nan |  |  | 9/16 | -0.001 | -0.005 |  | -0.6 / -0.4 |  |
| MNQ | 5 | h4 | -0.007 | -0.039 .. +0.026 | -0.0012 | 0.69 / 0.68 / 0.55 | nan |  |  | 8/16 | -0.001 | -0.012 |  | -0.8 / -0.4 | 0.025 |
| MNQ | 5 | h8 | -0.005 | -0.064 .. +0.054 | -0.0006 | 0.87 / 0.87 / 0.83 | nan |  |  | 8/16 | +0.002 | -0.012 |  | -0.4 / -0.2 |  |
| MNQ | 5 | h16 | +0.013 | -0.086 .. +0.112 | +0.0011 | 0.8 / 0.8 / 0.76 | nan |  |  | 8/16 | +0.015 | +0.011 |  | +0.9 / +0.3 |  |
| MNQ | 5 | eod * | +0.365 | -1.090 .. +1.820 | +0.0066 | 0.62 / 0.61 / 0.57 | nan | 1 | 1 | 9/16 | +0.107 | +0.620 | False | +5.9 / +0.5 |  |
| MNQ | 15 | h1 * | +0.004 | -0.003 .. +0.011 | +0.0016 | 0.24 / 0.25 / 0.36 | nan | 1 | 1 | 9/16 | +0.002 | +0.007 | False | +1.1 / +1.2 |  |
| MNQ | 15 | h2 | +0.001 | -0.024 .. +0.025 | +0.0002 | 0.96 / 0.96 / 0.95 | nan |  |  | 8/16 | +0.004 | -0.003 |  | +0.1 / +0.1 |  |
| MNQ | 15 | h4 | -0.002 | -0.058 .. +0.055 | -0.0003 | 0.95 / 0.95 / 0.93 | nan |  |  | 8/16 | +0.010 | -0.014 |  | -0.1 / -0.1 | 0.048 |
| MNQ | 15 | h8 | +0.007 | -0.087 .. +0.102 | +0.0008 | 0.88 / 0.88 / 0.85 | nan |  |  | 8/16 | +0.024 | -0.009 |  | +0.3 / +0.2 |  |
| MNQ | 15 | h16 | +0.030 | -0.152 .. +0.211 | +0.0026 | 0.75 / 0.75 / 0.68 | nan |  |  | 9/16 | +0.053 | +0.006 |  | +1.1 / +0.3 |  |
| MNQ | 15 | eod | +0.001 | -1.012 .. +1.013 | +0.0000 | 1 / 1 / 1 | nan |  |  | 9/16 | +0.003 | -0.002 |  | +0.0 / +0.0 |  |
| MNQ | 60 | h1 | +0.010 | -0.004 .. +0.024 | +0.0049 | 0.15 / 0.14 / 0.15 | nan |  |  | 10/16 | -0.000 | +0.020 |  | +1.5 / +1.4 |  |
| MNQ | 60 | h2 | +0.020 | -0.007 .. +0.048 | +0.0067 | 0.15 / 0.15 / 0.15 | nan |  |  | 10/16 | -0.000 | +0.040 |  | +2.0 / +1.4 |  |
| MNQ | 60 | h4 | +0.039 | -0.014 .. +0.093 | +0.0093 | 0.15 / 0.15 / 0.16 | nan |  |  | 10/16 | -0.001 | +0.080 |  | +2.9 / +1.4 | 0.082 |
| MNQ | 60 | h8 | +0.075 | -0.029 .. +0.179 | +0.0128 | 0.16 / 0.15 / 0.17 | nan |  |  | 10/16 | -0.007 | +0.156 |  | +4.0 / +1.4 |  |
| MNQ | 60 | h16 * | +0.139 | -0.049 .. +0.328 | +0.0182 | 0.15 / 0.14 / 0.16 | nan | 1 | 1 | 10/16 | -0.019 | +0.298 | False | +5.7 / +1.5 |  |
| MNQ | 60 | eod | +0.154 | -0.055 .. +0.363 | +0.0193 | 0.15 / 0.14 / 0.16 | nan |  |  | 10/16 | -0.043 | +0.352 |  | +6.1 / +1.4 |  |
| MYM | 5 | h1 | -0.001 | -0.009 .. +0.007 | -0.0005 | 0.77 / 0.78 / 0.73 | nan |  |  | 4/8 | n/a | -0.001 |  | -0.3 / -0.3 |  |
| MYM | 5 | h2 | -0.006 | -0.027 .. +0.016 | -0.0014 | 0.61 / 0.61 / 0.48 | nan |  |  | 5/8 | n/a | -0.006 |  | -0.7 / -0.5 |  |
| MYM | 5 | h4 * | -0.015 | -0.065 .. +0.035 | -0.0023 | 0.56 / 0.57 / 0.39 | nan | 1 | 1 | 5/8 | n/a | -0.015 | False | -1.1 / -0.6 | 0.036 |
| MYM | 5 | h8 | -0.021 | -0.113 .. +0.072 | -0.0023 | 0.67 / 0.67 / 0.52 | nan |  |  | 5/8 | n/a | -0.021 |  | -1.1 / -0.4 |  |
| MYM | 5 | h16 | -0.023 | -0.190 .. +0.144 | -0.0020 | 0.79 / 0.79 / 0.7 | nan |  |  | 5/8 | n/a | -0.023 |  | -1.0 / -0.3 |  |
| MYM | 5 | eod | +0.477 | -1.192 .. +2.147 | +0.0092 | 0.58 / 0.58 / 0.63 | nan |  |  | 4/8 | n/a | +0.477 |  | +5.9 / +0.6 |  |
| MYM | 15 | h1 | -0.001 | -0.015 .. +0.013 | -0.0004 | 0.9 / 0.9 / 0.89 | nan |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 15 | h2 | -0.011 | -0.056 .. +0.034 | -0.0026 | 0.63 / 0.64 / 0.45 | nan |  |  | 4/8 | n/a | -0.011 |  | -0.7 / -0.5 |  |
| MYM | 15 | h4 * | -0.025 | -0.123 .. +0.073 | -0.0035 | 0.62 / 0.63 / 0.41 | nan | 1 | 1 | 4/8 | n/a | -0.025 | False | -0.9 / -0.5 | 0.064 |
| MYM | 15 | h8 | -0.033 | -0.198 .. +0.133 | -0.0035 | 0.7 / 0.71 / 0.56 | nan |  |  | 4/8 | n/a | -0.033 |  | -0.9 / -0.4 |  |
| MYM | 15 | h16 | -0.043 | -0.365 .. +0.280 | -0.0033 | 0.8 / 0.8 / 0.72 | nan |  |  | 4/8 | n/a | -0.043 |  | -0.9 / -0.3 |  |
| MYM | 15 | eod | -0.053 | -1.261 .. +1.155 | -0.0017 | 0.93 / 0.93 / 0.92 | nan |  |  | 4/8 | n/a | -0.053 |  | -0.5 / -0.1 |  |
| MYM | 60 | h1 * | +0.012 | -0.006 .. +0.029 | +0.0056 | 0.2 / 0.21 / 0.35 | nan | 1 | 1 | 5/8 | n/a | +0.012 | False | +1.2 / +1.3 |  |
| MYM | 60 | h2 | +0.021 | -0.014 .. +0.057 | +0.0073 | 0.23 / 0.25 / 0.38 | nan |  |  | 4/8 | n/a | +0.021 |  | +1.6 / +1.2 |  |
| MYM | 60 | h4 | +0.041 | -0.028 .. +0.110 | +0.0100 | 0.24 / 0.26 / 0.4 | nan |  |  | 5/8 | n/a | +0.041 |  | +2.2 / +1.2 | 0.113 |
| MYM | 60 | h8 | +0.082 | -0.052 .. +0.216 | +0.0145 | 0.23 / 0.24 / 0.39 | nan |  |  | 5/8 | n/a | +0.082 |  | +3.2 / +1.2 |  |
| MYM | 60 | h16 | +0.142 | -0.104 .. +0.389 | +0.0193 | 0.26 / 0.26 / 0.43 | nan |  |  | 5/8 | n/a | +0.142 |  | +4.3 / +1.1 |  |
| MYM | 60 | eod | +0.167 | -0.109 .. +0.443 | +0.0216 | 0.24 / 0.24 / 0.4 | nan |  |  | 5/8 | n/a | +0.167 |  | +4.9 / +1.2 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.008 | -0.010 .. -0.005 | -1.6% | -0.012 | 5.4e-11 | 1.8e-08 | 14/16 |
| MES | 5 | h2 | -0.010 | -0.016 .. -0.005 | -1.4% | -0.020 | 0.00044 |  | 12/16 |
| MES | 5 | h4 | -0.014 | -0.027 .. -0.001 | -1.4% | -0.035 | 0.033 |  | 12/16 |
| MES | 5 | h8 | -0.024 | -0.049 .. +0.001 | -1.7% | -0.064 | 0.065 |  | 12/16 |
| MES | 5 | h16 | -0.054 | -0.098 .. -0.010 | -2.6% | -0.124 | 0.017 |  | 12/16 |
| MES | 5 | eod | -1.720 | -2.497 .. -0.944 | -17.3% | -3.126 | 1.4e-05 |  | 14/16 |
| MES | 15 | h1 * | -0.017 | -0.023 .. -0.012 | -3.4% | -0.036 | 4.5e-11 | 1.5e-08 | 16/16 |
| MES | 15 | h2 | -0.023 | -0.038 .. -0.008 | -3.1% | -0.052 | 0.0033 |  | 13/16 |
| MES | 15 | h4 | -0.034 | -0.068 .. -0.000 | -3.2% | -0.080 | 0.05 |  | 14/16 |
| MES | 15 | h8 | -0.072 | -0.132 .. -0.012 | -4.7% | -0.140 | 0.018 |  | 13/16 |
| MES | 15 | h16 | -0.170 | -0.266 .. -0.073 | -7.4% | -0.300 | 0.00056 |  | 12/16 |
| MES | 15 | eod | -1.053 | -1.641 .. -0.465 | -19.2% | -1.969 | 0.00045 |  | 15/16 |
| MES | 60 | h1 * | -0.047 | -0.057 .. -0.036 | -9.1% | -0.095 | 2e-17 | 9.16e-15 | 16/16 |
| MES | 60 | h2 | -0.075 | -0.094 .. -0.056 | -10.2% | -0.149 | 1.8e-14 |  | 16/16 |
| MES | 60 | h4 | -0.117 | -0.152 .. -0.082 | -11.1% | -0.241 | 5.1e-11 |  | 16/16 |
| MES | 60 | h8 | -0.207 | -0.267 .. -0.147 | -13.7% | -0.399 | 1.4e-11 |  | 14/16 |
| MES | 60 | h16 | -0.362 | -0.468 .. -0.257 | -17.6% | -0.660 | 2e-11 |  | 14/16 |
| MES | 60 | eod | -0.414 | -0.534 .. -0.295 | -19.1% | -0.719 | 1.1e-11 |  | 15/16 |
| MNQ | 5 | h1 | -0.005 | -0.009 .. -0.001 | -0.9% | -0.006 | 0.018 |  | 12/16 |
| MNQ | 5 | h2 | -0.003 | -0.017 .. +0.011 | -0.4% | -0.008 | 0.69 |  | 12/16 |
| MNQ | 5 | h4 | +0.001 | -0.030 .. +0.032 | +0.1% | -0.010 | 0.93 |  | 6/16 |
| MNQ | 5 | h8 | +0.007 | -0.047 .. +0.061 | +0.4% | -0.013 | 0.8 |  | 8/16 |
| MNQ | 5 | h16 | -0.005 | -0.087 .. +0.076 | -0.2% | -0.013 | 0.9 |  | 9/16 |
| MNQ | 5 | eod * | -1.556 | -2.665 .. -0.446 | -12.4% | -2.978 | 0.006 | 0.857 | 12/16 |
| MNQ | 15 | h1 * | -0.016 | -0.021 .. -0.010 | -2.9% | -0.024 | 5.1e-08 | 1.41e-05 | 13/16 |
| MNQ | 15 | h2 | -0.013 | -0.033 .. +0.007 | -1.6% | -0.028 | 0.21 |  | 11/16 |
| MNQ | 15 | h4 | -0.008 | -0.067 .. +0.050 | -0.7% | -0.029 | 0.78 |  | 11/16 |
| MNQ | 15 | h8 | -0.029 | -0.132 .. +0.073 | -1.7% | -0.041 | 0.58 |  | 13/16 |
| MNQ | 15 | h16 | -0.104 | -0.263 .. +0.056 | -4.1% | -0.107 | 0.2 |  | 12/16 |
| MNQ | 15 | eod | -0.729 | -1.606 .. +0.147 | -11.5% | -1.538 | 0.1 |  | 14/16 |
| MNQ | 60 | h1 * | -0.040 | -0.051 .. -0.028 | -7.5% | -0.089 | 2.8e-11 | 9.54e-09 | 15/16 |
| MNQ | 60 | h2 | -0.065 | -0.086 .. -0.044 | -8.5% | -0.138 | 1.4e-09 |  | 15/16 |
| MNQ | 60 | h4 | -0.103 | -0.141 .. -0.065 | -9.3% | -0.214 | 1e-07 |  | 14/16 |
| MNQ | 60 | h8 | -0.164 | -0.230 .. -0.097 | -10.3% | -0.330 | 1.3e-06 |  | 12/16 |
| MNQ | 60 | h16 | -0.261 | -0.379 .. -0.143 | -11.9% | -0.496 | 1.6e-05 |  | 11/16 |
| MNQ | 60 | eod | -0.304 | -0.436 .. -0.171 | -13.2% | -0.540 | 6.8e-06 |  | 12/16 |
| MYM | 5 | h1 * | -0.009 | -0.016 .. -0.003 | -1.7% | -0.012 | 0.0061 | 0.869 | 7/8 |
| MYM | 5 | h2 | -0.007 | -0.028 .. +0.013 | -0.9% | -0.016 | 0.5 |  | 7/8 |
| MYM | 5 | h4 | -0.001 | -0.051 .. +0.048 | -0.1% | -0.022 | 0.96 |  | 7/8 |
| MYM | 5 | h8 | -0.001 | -0.093 .. +0.091 | -0.1% | -0.028 | 0.98 |  | 7/8 |
| MYM | 5 | h16 | -0.009 | -0.163 .. +0.144 | -0.4% | -0.026 | 0.91 |  | 7/8 |
| MYM | 5 | eod | -1.774 | -3.108 .. -0.440 | -15.1% | -3.347 | 0.0092 |  | 6/8 |
| MYM | 15 | h1 * | -0.019 | -0.031 .. -0.008 | -3.7% | -0.032 | 0.00062 | 0.111 | 7/8 |
| MYM | 15 | h2 | -0.016 | -0.060 .. +0.027 | -2.1% | -0.033 | 0.46 |  | 7/8 |
| MYM | 15 | h4 | -0.003 | -0.110 .. +0.104 | -0.3% | -0.028 | 0.95 |  | 7/8 |
| MYM | 15 | h8 | -0.011 | -0.190 .. +0.168 | -0.7% | -0.013 | 0.91 |  | 6/8 |
| MYM | 15 | h16 | -0.052 | -0.346 .. +0.241 | -2.1% | -0.033 | 0.73 |  | 7/8 |
| MYM | 15 | eod | -0.779 | -1.882 .. +0.325 | -12.9% | -1.705 | 0.17 |  | 7/8 |
| MYM | 60 | h1 * | -0.043 | -0.059 .. -0.027 | -8.3% | -0.087 | 1e-07 | 2.75e-05 | 8/8 |
| MYM | 60 | h2 | -0.069 | -0.096 .. -0.042 | -9.1% | -0.138 | 7.9e-07 |  | 7/8 |
| MYM | 60 | h4 | -0.102 | -0.150 .. -0.055 | -9.5% | -0.220 | 2.4e-05 |  | 7/8 |
| MYM | 60 | h8 | -0.172 | -0.257 .. -0.087 | -11.1% | -0.361 | 7.4e-05 |  | 6/8 |
| MYM | 60 | h16 | -0.314 | -0.470 .. -0.158 | -14.8% | -0.595 | 8.1e-05 |  | 6/8 |
| MYM | 60 | eod | -0.366 | -0.540 .. -0.192 | -16.4% | -0.649 | 3.8e-05 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.26 pts | -0.76 .. +0.24 | 0.32 |
| MES | 15 | -0.34 pts | -1.13 .. +0.45 | 0.42 |
| MES | 60 | +0.90 pts | -0.79 .. +2.58 | 0.3 |
| MNQ | 5 | -0.12 pts | -0.58 .. +0.34 | 0.62 |
| MNQ | 15 | -0.01 pts | -0.83 .. +0.80 | 0.97 |
| MNQ | 60 | +1.48 pts | -0.26 .. +3.22 | 0.1 |
| MYM | 5 | -0.12 pts | -0.83 .. +0.60 | 0.75 |
| MYM | 15 | -0.06 pts | -1.25 .. +1.13 | 0.92 |
| MYM | 60 | +3.32 pts | +0.88 .. +5.77 | 0.0076 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 203208 | +0.003 | 0.338 | +0.04 | -3.46 | -3.50 | -3.41 | -3.46 |
| MES | 5 | h2 | event | long | 203208 | +0.006 | 0.338 | +0.10 | -3.40 | -3.49 | -3.31 | -3.42 |
| MES | 5 | h4 | event | long | 203208 | +0.011 | 0.338 | +0.21 | -3.29 | -3.48 | -3.11 | -3.34 |
| MES | 5 | h8 | event | long | 203208 | +0.025 | 0.338 | +0.43 | -3.07 | -3.44 | -2.71 | -3.19 |
| MES | 5 | h16 | event | long | 203208 | +0.059 | 0.338 | +0.86 | -2.64 | -3.34 | -1.95 | -2.90 |
| MES | 5 | eod | event | long | 203208 | +0.661 | 0.338 | +9.75 | +6.25 | -2.71 | +15.04 | +4.20 |
| MES | 15 | h1 | event | long | 66733 | +0.008 | 0.193 | +0.16 | -3.34 | -3.49 | -3.20 | -3.39 |
| MES | 15 | h2 | event | long | 66733 | +0.013 | 0.193 | +0.33 | -3.17 | -3.46 | -2.90 | -3.26 |
| MES | 15 | h4 | event | long | 66733 | +0.024 | 0.193 | +0.66 | -2.84 | -3.38 | -2.31 | -3.02 |
| MES | 15 | h8 | event | long | 66733 | +0.049 | 0.193 | +1.29 | -2.21 | -3.24 | -1.21 | -2.57 |
| MES | 15 | h16 | event | long | 66733 | +0.092 | 0.193 | +2.50 | -1.00 | -3.00 | +0.95 | -1.58 |
| MES | 15 | eod | event | short | 66733 | -0.219 | 0.193 | -9.65 | -13.15 | -4.13 | -21.94 | -11.80 |
| MES | 60 | h1 | event | long | 15814 | +0.011 | 0.090 | +0.67 | -2.83 | -3.41 | -2.29 | -3.00 |
| MES | 60 | h2 | event | long | 15814 | +0.024 | 0.090 | +1.32 | -2.18 | -3.33 | -1.08 | -2.56 |
| MES | 60 | h4 | event | long | 15814 | +0.048 | 0.090 | +2.63 | -0.87 | -3.16 | +1.30 | -1.71 |
| MES | 60 | h8 | event | long | 15814 | +0.089 | 0.090 | +5.01 | +1.51 | -2.89 | +5.70 | -0.12 |
| MES | 60 | h16 | event | long | 15814 | +0.151 | 0.090 | +8.81 | +5.31 | -3.04 | +13.27 | +2.70 |
| MES | 60 | eod | event | long | 15814 | +0.169 | 0.090 | +10.01 | +6.51 | -3.22 | +15.79 | +3.35 |
| MNQ | 5 | h1 | event | short | 203039 | -0.004 | 0.134 | -0.10 | -2.10 | -2.01 | -2.17 | -2.08 |
| MNQ | 5 | h2 | event | short | 203039 | -0.006 | 0.134 | -0.20 | -2.20 | -2.03 | -2.36 | -2.18 |
| MNQ | 5 | h4 | event | short | 203039 | -0.010 | 0.134 | -0.40 | -2.40 | -2.07 | -2.73 | -2.37 |
| MNQ | 5 | h8 | event | short | 203039 | -0.028 | 0.134 | -0.82 | -2.82 | -2.15 | -3.47 | -2.72 |
| MNQ | 5 | h16 | event | long | 203039 | +0.076 | 0.134 | +1.62 | -0.38 | -1.68 | +0.89 | -0.64 |
| MNQ | 5 | eod | event | long | 203039 | +1.093 | 0.134 | +19.67 | +17.67 | +0.67 | +34.27 | +15.30 |
| MNQ | 15 | h1 | event | long | 66823 | +0.011 | 0.076 | +0.30 | -1.70 | -1.94 | -1.46 | -1.80 |
| MNQ | 15 | h2 | event | long | 66823 | +0.013 | 0.076 | +0.61 | -1.39 | -1.88 | -0.91 | -1.53 |
| MNQ | 15 | h4 | event | short | 66823 | -0.023 | 0.076 | -1.22 | -3.22 | -2.25 | -4.18 | -2.94 |
| MNQ | 15 | h8 | event | long | 66823 | +0.057 | 0.076 | +2.40 | +0.40 | -1.51 | +2.24 | -0.22 |
| MNQ | 15 | h16 | event | long | 66823 | +0.112 | 0.076 | +4.64 | +2.64 | -1.05 | +6.23 | +1.97 |
| MNQ | 15 | eod | event | long | 66823 | +0.340 | 0.076 | +19.59 | +17.59 | +0.56 | +34.13 | +16.38 |
| MNQ | 60 | h1 | event | long | 15916 | +0.020 | 0.035 | +1.25 | -0.75 | -1.77 | +0.21 | -1.04 |
| MNQ | 60 | h2 | event | long | 15916 | +0.039 | 0.035 | +2.47 | +0.47 | -1.57 | +2.39 | -0.13 |
| MNQ | 60 | h4 | event | long | 15916 | +0.075 | 0.035 | +4.83 | +2.83 | -1.19 | +6.61 | +1.61 |
| MNQ | 60 | h8 | event | long | 15916 | +0.139 | 0.035 | +9.27 | +7.27 | -0.52 | +14.60 | +5.06 |
| MNQ | 60 | h16 | event | long | 15916 | +0.241 | 0.035 | +17.06 | +15.06 | +0.08 | +29.15 | +11.74 |
| MNQ | 60 | eod | event | long | 15916 | +0.273 | 0.035 | +19.91 | +17.91 | +0.15 | +34.61 | +13.77 |
| MYM | 5 | h1 | event | short | 102461 | +0.002 | 0.176 | -0.06 | -2.06 | +nan | -2.06 | -2.07 |
| MYM | 5 | h2 | event | short | 102461 | +0.007 | 0.176 | -0.13 | -2.13 | +nan | -2.13 | -2.16 |
| MYM | 5 | h4 | event | short | 102461 | +0.017 | 0.176 | -0.27 | -2.27 | +nan | -2.27 | -2.34 |
| MYM | 5 | h8 | event | short | 102461 | +0.025 | 0.176 | -0.54 | -2.54 | +nan | -2.54 | -2.64 |
| MYM | 5 | h16 | event | short | 102461 | +0.022 | 0.176 | -1.06 | -3.06 | +nan | -3.06 | -3.14 |
| MYM | 5 | eod | event | long | 102461 | +0.594 | 0.176 | +13.16 | +11.16 | +nan | +11.16 | +10.58 |
| MYM | 15 | h1 | event | short | 33765 | -0.001 | 0.098 | -0.21 | -2.21 | +nan | -2.21 | -2.20 |
| MYM | 15 | h2 | event | short | 33765 | +0.008 | 0.098 | -0.41 | -2.41 | +nan | -2.41 | -2.44 |
| MYM | 15 | h4 | event | short | 33765 | +0.020 | 0.098 | -0.82 | -2.82 | +nan | -2.82 | -2.88 |
| MYM | 15 | h8 | event | short | 33765 | +0.029 | 0.098 | -1.56 | -3.56 | +nan | -3.56 | -3.72 |
| MYM | 15 | h16 | event | short | 33765 | +0.057 | 0.098 | -3.00 | -5.00 | +nan | -5.00 | -5.57 |
| MYM | 15 | eod | event | short | 33765 | -0.010 | 0.098 | -12.97 | -14.97 | +nan | -14.97 | -15.72 |
| MYM | 60 | h1 | event | long | 8098 | +0.013 | 0.045 | +0.86 | -1.14 | +nan | -1.14 | -1.25 |
| MYM | 60 | h2 | event | long | 8098 | +0.025 | 0.045 | +1.68 | -0.32 | +nan | -0.32 | -0.58 |
| MYM | 60 | h4 | event | long | 8098 | +0.048 | 0.045 | +3.30 | +1.30 | +nan | +1.30 | +0.73 |
| MYM | 60 | h8 | event | long | 8098 | +0.093 | 0.045 | +6.35 | +4.35 | +nan | +4.35 | +3.32 |
| MYM | 60 | h16 | event | long | 8098 | +0.162 | 0.045 | +11.42 | +9.42 | +nan | +9.42 | +7.36 |
| MYM | 60 | eod | event | long | 8098 | +0.195 | 0.045 | +13.09 | +11.09 | +nan | +11.09 | +8.34 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.003 | -0.000 | -0.000 | +0.000 | +0.000 | +0.000 | -0.001 | -0.001 | +0.000 | +0.002 | +0.010 |
| MES | 15 | +0.019 | +0.013 | +0.007 | +0.003 | +0.002 | +0.000 | -0.001 | -0.001 | -0.001 | +0.002 | +0.008 |
| MES | 60 | +0.045 | +0.015 | +0.007 | +0.002 | +0.000 | +0.000 | +0.003 | +0.007 | +0.018 | +0.039 | +0.071 |
| MNQ | 5 | +0.002 | -0.000 | -0.001 | -0.001 | +0.000 | +0.000 | -0.003 | -0.003 | -0.005 | -0.002 | +0.010 |
| MNQ | 15 | -0.011 | -0.004 | -0.001 | -0.000 | +0.002 | +0.000 | -0.004 | -0.007 | -0.009 | -0.005 | +0.012 |
| MNQ | 60 | -0.098 | -0.047 | -0.026 | -0.014 | -0.007 | +0.000 | +0.008 | +0.018 | +0.038 | +0.079 | +0.135 |
| MYM | 5 | +0.018 | +0.005 | +0.002 | +0.001 | +0.001 | +0.000 | -0.006 | -0.009 | -0.017 | -0.024 | -0.031 |
| MYM | 15 | +0.055 | +0.029 | +0.012 | +0.006 | +0.005 | +0.000 | -0.012 | -0.021 | -0.033 | -0.048 | -0.077 |
| MYM | 60 | +0.045 | -0.006 | +0.002 | -0.000 | -0.003 | +0.000 | +0.009 | +0.017 | +0.031 | +0.069 | +0.116 |

## Calibration

- MES 5-min: 1036271 bars, 203208 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 66733 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 15814 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 203039 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 66823 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 15916 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 102461 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 33765 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8098 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
