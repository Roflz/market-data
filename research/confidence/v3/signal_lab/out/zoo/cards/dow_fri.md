# Impact card: dow_fri

session weekday = fri vs other days [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.315 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.72).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.08 at recent bar sizes, 90% range up to $0.35); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.175 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% LESS after the event than after matched bars over the next 2 bars (30 min) (-0.015 R20, possible, q=0.0535, 12 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.97 at recent bar sizes, 90% range up to $1.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.057 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.65).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.58 at recent bar sizes, 90% range up to $5.21); about 2.7x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.025 R20 over the next 8 bars (40 min), p=0.8; we would catch an effect of 0.024 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% LESS after the event than after matched bars over the next 8 bars (40 min) (-0.033 R20, possible, q=0.187, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.52 at recent bar sizes, 90% range up to $1.20); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.007 R20 over the next 1 bar (15 min), p=0.38; we would catch an effect of 0.045 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.014 R20, CONFIRMED, q=2.86e-05, 14 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.25 at recent bar sizes, 90% range up to $3.99); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.010 R20 over the next 1 bar (1 h), p=0.82; we would catch an effect of 0.080 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.79 at recent bar sizes, 90% range up to $12.25); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +1.396 R20 over the rest of the session (to 16:45), p=0.7; we would catch an effect of 0.042 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.21).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $13.43 at recent bar sizes, 90% range up to $0.78); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.172 R20 over the next 16 bars (4 h), p=0.54; we would catch an effect of 0.072 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.33).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.93 at recent bar sizes, 90% range up to $2.50); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.114 R20 over the next 8 bars (8 h), p=0.84; we would catch an effect of 0.110 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.29).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.98 at recent bar sizes, 90% range up to $9.03); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.003 .. +0.004 | +0.0002 | 0.86 / 0.86 / 0.86 | nan |  |  | 8/16 | -0.001 | +0.001 |  | +0.2 / +0.2 |  |
| MES | 5 | h2 | +0.001 | -0.006 .. +0.007 | +0.0003 | 0.8 / 0.8 / 0.81 | nan |  |  | 9/16 | -0.002 | +0.003 |  | +0.3 / +0.3 |  |
| MES | 5 | h4 | +0.001 | -0.012 .. +0.015 | +0.0004 | 0.84 / 0.84 / 0.85 | nan |  |  | 9/16 | -0.004 | +0.006 |  | +0.4 / +0.2 | 0.020 |
| MES | 5 | h8 | +0.000 | -0.027 .. +0.028 | +0.0001 | 0.98 / 0.98 / 0.97 | nan |  |  | 9/16 | -0.009 | +0.009 |  | +0.1 / +0.0 |  |
| MES | 5 | h16 | -0.000 | -0.057 .. +0.057 | -0.0000 | 1 / 1 / 1 | nan |  |  | 8/16 | -0.022 | +0.021 |  | -0.0 / -0.0 |  |
| MES | 5 | eod * | +0.315 | -0.619 .. +1.249 | +0.0079 | 0.51 / 0.52 / 0.53 | nan | 1 | 1 | 9/16 | -0.308 | +0.934 | False | +8.2 / +0.7 |  |
| MES | 15 | h1 | -0.001 | -0.007 .. +0.006 | -0.0003 | 0.83 / 0.83 / 0.87 | nan |  |  | 8/16 | -0.003 | +0.002 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.001 | -0.013 .. +0.012 | -0.0002 | 0.92 / 0.92 / 0.93 | nan |  |  | 8/16 | -0.007 | +0.005 |  | -0.1 / -0.1 |  |
| MES | 15 | h4 | -0.002 | -0.028 .. +0.023 | -0.0005 | 0.86 / 0.86 / 0.87 | nan |  |  | 8/16 | -0.016 | +0.012 |  | -0.3 / -0.2 | 0.037 |
| MES | 15 | h8 | -0.004 | -0.056 .. +0.049 | -0.0006 | 0.89 / 0.89 / 0.9 | nan |  |  | 8/16 | -0.037 | +0.030 |  | -0.4 / -0.1 |  |
| MES | 15 | h16 | -0.004 | -0.113 .. +0.106 | -0.0004 | 0.95 / 0.95 / 0.95 | nan |  |  | 8/16 | -0.089 | +0.082 |  | -0.2 / -0.1 |  |
| MES | 15 | eod * | +0.175 | -0.351 .. +0.701 | +0.0077 | 0.51 / 0.53 / 0.55 | nan | 1 | 1 | 9/16 | -0.217 | +0.565 | False | +4.7 / +0.7 |  |
| MES | 60 | h1 | +0.000 | -0.013 .. +0.013 | +0.0001 | 0.99 / 0.99 / 0.98 | nan |  |  | 8/16 | -0.007 | +0.007 |  | +0.0 / +0.0 |  |
| MES | 60 | h2 | +0.002 | -0.024 .. +0.027 | +0.0007 | 0.89 / 0.89 / 0.89 | nan |  |  | 8/16 | -0.014 | +0.017 |  | +0.2 / +0.1 |  |
| MES | 60 | h4 | +0.006 | -0.044 .. +0.056 | +0.0016 | 0.81 / 0.81 / 0.82 | nan |  |  | 8/16 | -0.025 | +0.037 |  | +0.5 / +0.2 | 0.075 |
| MES | 60 | h8 | +0.019 | -0.076 .. +0.114 | +0.0036 | 0.69 / 0.7 / 0.72 | nan |  |  | 8/16 | -0.037 | +0.075 |  | +1.0 / +0.4 |  |
| MES | 60 | h16 | +0.043 | -0.125 .. +0.211 | +0.0062 | 0.62 / 0.63 / 0.65 | nan |  |  | 9/16 | -0.051 | +0.137 |  | +1.8 / +0.5 |  |
| MES | 60 | eod * | +0.057 | -0.132 .. +0.245 | +0.0077 | 0.56 / 0.57 / 0.6 | nan | 1 | 1 | 9/16 | -0.047 | +0.160 | False | +2.2 / +0.6 |  |
| MNQ | 5 | h1 | -0.002 | -0.006 .. +0.001 | -0.0010 | 0.22 / 0.22 / 0.31 | nan |  |  | 11/16 | -0.001 | -0.004 |  | -1.1 / -1.2 |  |
| MNQ | 5 | h2 | -0.004 | -0.011 .. +0.004 | -0.0011 | 0.31 / 0.3 / 0.45 | nan |  |  | 12/16 | -0.003 | -0.005 |  | -1.2 / -1.0 |  |
| MNQ | 5 | h4 | -0.009 | -0.024 .. +0.007 | -0.0016 | 0.28 / 0.27 / 0.43 | nan |  |  | 12/16 | -0.007 | -0.010 |  | -1.9 / -1.1 | 0.024 |
| MNQ | 5 | h8 * | -0.025 | -0.057 .. +0.007 | -0.0030 | 0.13 / 0.13 / 0.25 | nan | 1 | 1 | 12/16 | -0.018 | -0.031 | False | -3.5 / -1.5 |  |
| MNQ | 5 | h16 | -0.051 | -0.119 .. +0.018 | -0.0044 | 0.15 / 0.14 / 0.24 | nan |  |  | 12/16 | -0.046 | -0.055 |  | -5.2 / -1.5 |  |
| MNQ | 5 | eod | -0.675 | -1.917 .. +0.568 | -0.0123 | 0.29 / 0.29 / 0.29 | nan |  |  | 9/16 | -1.181 | -0.172 |  | -13.0 / -1.1 |  |
| MNQ | 15 | h1 * | -0.007 | -0.014 .. +0.000 | -0.0027 | 0.063 / 0.061 / 0.14 | nan | 1 | 1 | 10/16 | -0.007 | -0.007 | False | -1.8 / -1.9 |  |
| MNQ | 15 | h2 | -0.011 | -0.025 .. +0.003 | -0.0027 | 0.12 / 0.11 / 0.27 | nan |  |  | 10/16 | -0.013 | -0.009 |  | -2.0 / -1.6 |  |
| MNQ | 15 | h4 | -0.024 | -0.053 .. +0.006 | -0.0033 | 0.12 / 0.11 / 0.29 | nan |  |  | 11/16 | -0.030 | -0.018 |  | -2.7 / -1.6 | 0.045 |
| MNQ | 15 | h8 | -0.051 | -0.111 .. +0.009 | -0.0055 | 0.093 / 0.088 / 0.19 | nan |  |  | 10/16 | -0.066 | -0.037 |  | -4.2 / -1.7 |  |
| MNQ | 15 | h16 | -0.096 | -0.225 .. +0.033 | -0.0084 | 0.15 / 0.14 / 0.18 | nan |  |  | 10/16 | -0.150 | -0.041 |  | -5.5 / -1.5 |  |
| MNQ | 15 | eod | -0.309 | -0.942 .. +0.323 | -0.0094 | 0.34 / 0.34 / 0.38 | nan |  |  | 9/16 | -0.598 | -0.022 |  | -6.7 / -1.0 |  |
| MNQ | 60 | h1 * | -0.010 | -0.024 .. +0.003 | -0.0051 | 0.13 / 0.14 / 0.14 | nan | 1 | 1 | 10/16 | -0.013 | -0.008 | False | -1.5 / -1.5 |  |
| MNQ | 60 | h2 | -0.019 | -0.046 .. +0.008 | -0.0065 | 0.16 / 0.17 / 0.17 | nan |  |  | 10/16 | -0.025 | -0.013 |  | -1.9 / -1.4 |  |
| MNQ | 60 | h4 | -0.036 | -0.089 .. +0.017 | -0.0086 | 0.19 / 0.19 / 0.19 | nan |  |  | 9/16 | -0.049 | -0.023 |  | -2.6 / -1.3 | 0.080 |
| MNQ | 60 | h8 | -0.062 | -0.163 .. +0.039 | -0.0109 | 0.23 / 0.24 / 0.25 | nan |  |  | 9/16 | -0.083 | -0.041 |  | -3.2 / -1.2 |  |
| MNQ | 60 | h16 | -0.100 | -0.280 .. +0.080 | -0.0134 | 0.28 / 0.29 / 0.3 | nan |  |  | 9/16 | -0.135 | -0.065 |  | -3.9 / -1.1 |  |
| MNQ | 60 | eod | -0.109 | -0.307 .. +0.090 | -0.0139 | 0.28 / 0.3 / 0.31 | nan |  |  | 9/16 | -0.153 | -0.064 |  | -4.1 / -1.1 |  |
| MYM | 5 | h1 | +0.003 | -0.002 .. +0.008 | +0.0012 | 0.25 / 0.28 / 0.4 | nan |  |  | 5/8 | n/a | +0.003 |  | +1.0 / +1.1 |  |
| MYM | 5 | h2 | +0.008 | -0.002 .. +0.019 | +0.0020 | 0.13 / 0.15 / 0.29 | nan |  |  | 5/8 | n/a | +0.008 |  | +1.7 / +1.5 |  |
| MYM | 5 | h4 | +0.018 | -0.005 .. +0.041 | +0.0027 | 0.13 / 0.14 / 0.3 | nan |  |  | 5/8 | n/a | +0.018 |  | +2.5 / +1.5 | 0.042 |
| MYM | 5 | h8 | +0.028 | -0.016 .. +0.072 | +0.0031 | 0.21 / 0.23 / 0.38 | nan |  |  | 5/8 | n/a | +0.028 |  | +2.7 / +1.3 |  |
| MYM | 5 | h16 | +0.063 | -0.029 .. +0.155 | +0.0055 | 0.18 / 0.19 / 0.29 | nan |  |  | 5/8 | n/a | +0.063 |  | +4.6 / +1.3 |  |
| MYM | 5 | eod * | +1.396 | -0.345 .. +3.137 | +0.0269 | 0.12 / 0.12 / 0.15 | nan | 1 | 1 | 6/8 | n/a | +1.396 | False | +20.1 / +1.6 |  |
| MYM | 15 | h1 | +0.006 | -0.003 .. +0.015 | +0.0025 | 0.2 / 0.22 / 0.3 | nan |  |  | 5/8 | n/a | +0.006 |  | +1.2 / +1.3 |  |
| MYM | 15 | h2 | +0.015 | -0.005 .. +0.035 | +0.0035 | 0.14 / 0.16 / 0.28 | nan |  |  | 5/8 | n/a | +0.015 |  | +1.9 / +1.5 |  |
| MYM | 15 | h4 | +0.031 | -0.010 .. +0.073 | +0.0044 | 0.14 / 0.16 / 0.29 | nan |  |  | 5/8 | n/a | +0.031 |  | +2.6 / +1.5 | 0.072 |
| MYM | 15 | h8 | +0.070 | -0.015 .. +0.156 | +0.0075 | 0.11 / 0.12 / 0.19 | nan |  |  | 5/8 | n/a | +0.070 |  | +4.1 / +1.6 |  |
| MYM | 15 | h16 * | +0.172 | -0.020 .. +0.364 | +0.0131 | 0.079 / 0.089 / 0.14 | nan | 1 | 1 | 6/8 | n/a | +0.172 | False | +6.9 / +1.8 |  |
| MYM | 15 | eod | +0.773 | -0.133 .. +1.680 | +0.0244 | 0.095 / 0.093 / 0.14 | nan |  |  | 6/8 | n/a | +0.773 |  | +12.3 / +1.7 |  |
| MYM | 60 | h1 | +0.012 | -0.008 .. +0.032 | +0.0059 | 0.23 / 0.24 / 0.33 | nan |  |  | 5/8 | n/a | +0.012 |  | +1.2 / +1.2 |  |
| MYM | 60 | h2 | +0.028 | -0.011 .. +0.067 | +0.0096 | 0.17 / 0.17 / 0.26 | nan |  |  | 5/8 | n/a | +0.028 |  | +2.0 / +1.4 |  |
| MYM | 60 | h4 | +0.058 | -0.020 .. +0.135 | +0.0143 | 0.15 / 0.15 / 0.23 | nan |  |  | 5/8 | n/a | +0.058 |  | +2.9 / +1.5 | 0.110 |
| MYM | 60 | h8 * | +0.114 | -0.037 .. +0.266 | +0.0206 | 0.14 / 0.14 / 0.23 | nan | 1 | 1 | 5/8 | n/a | +0.114 | False | +4.2 / +1.5 |  |
| MYM | 60 | h16 | +0.199 | -0.074 .. +0.471 | +0.0273 | 0.15 / 0.15 / 0.26 | nan |  |  | 5/8 | n/a | +0.199 |  | +5.6 / +1.4 |  |
| MYM | 60 | eod | +0.221 | -0.083 .. +0.525 | +0.0290 | 0.15 / 0.15 / 0.26 | nan |  |  | 5/8 | n/a | +0.221 |  | +5.9 / +1.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.000 | -0.002 .. +0.002 | +0.0% | +0.003 | 0.88 |  | 10/16 |
| MES | 5 | h2 | -0.002 | -0.006 .. +0.002 | -0.3% | +0.004 | 0.28 |  | 10/16 |
| MES | 5 | h4 | -0.005 | -0.012 .. +0.002 | -0.5% | +0.006 | 0.16 |  | 10/16 |
| MES | 5 | h8 * | -0.012 | -0.026 .. +0.003 | -0.8% | +0.010 | 0.12 | 1 | 12/16 |
| MES | 5 | h16 | -0.015 | -0.043 .. +0.014 | -0.7% | +0.012 | 0.33 |  | 11/16 |
| MES | 5 | eod | +0.124 | -0.456 .. +0.704 | +1.2% | -0.247 | 0.68 |  | 8/16 |
| MES | 15 | h1 | -0.007 | -0.011 .. -0.003 | -1.4% | -0.006 | 0.00053 |  | 12/16 |
| MES | 15 | h2 * | -0.015 | -0.023 .. -0.007 | -2.0% | -0.014 | 0.00028 | 0.0535 | 12/16 |
| MES | 15 | h4 | -0.022 | -0.038 .. -0.006 | -2.1% | -0.027 | 0.0062 |  | 12/16 |
| MES | 15 | h8 | -0.032 | -0.063 .. -0.002 | -2.1% | -0.048 | 0.035 |  | 12/16 |
| MES | 15 | h16 | -0.044 | -0.104 .. +0.016 | -1.9% | -0.074 | 0.15 |  | 11/16 |
| MES | 15 | eod | +0.031 | -0.305 .. +0.368 | +0.6% | -0.242 | 0.86 |  | 8/16 |
| MES | 60 | h1 | +0.007 | -0.003 .. +0.017 | +1.4% | +0.028 | 0.18 |  | 10/16 |
| MES | 60 | h2 * | +0.014 | -0.003 .. +0.031 | +1.9% | +0.042 | 0.11 | 1 | 11/16 |
| MES | 60 | h4 | +0.022 | -0.008 .. +0.052 | +2.1% | +0.051 | 0.17 |  | 9/16 |
| MES | 60 | h8 | +0.028 | -0.026 .. +0.082 | +1.8% | +0.031 | 0.34 |  | 9/16 |
| MES | 60 | h16 | +0.025 | -0.076 .. +0.126 | +1.2% | -0.043 | 0.64 |  | 8/16 |
| MES | 60 | eod | +0.018 | -0.097 .. +0.133 | +0.8% | -0.092 | 0.76 |  | 8/16 |
| MNQ | 5 | h1 | -0.001 | -0.004 .. +0.001 | -0.3% | -0.001 | 0.21 |  | 12/16 |
| MNQ | 5 | h2 | -0.005 | -0.010 .. -0.000 | -0.6% | -0.003 | 0.04 |  | 13/16 |
| MNQ | 5 | h4 | -0.015 | -0.024 .. -0.005 | -1.3% | -0.007 | 0.0023 |  | 13/16 |
| MNQ | 5 | h8 * | -0.033 | -0.053 .. -0.013 | -2.0% | -0.017 | 0.0011 | 0.187 | 14/16 |
| MNQ | 5 | h16 | -0.068 | -0.115 .. -0.022 | -2.8% | -0.059 | 0.0039 |  | 13/16 |
| MNQ | 5 | eod | -0.035 | -0.829 .. +0.758 | -0.3% | -0.865 | 0.93 |  | 8/16 |
| MNQ | 15 | h1 * | -0.014 | -0.019 .. -0.009 | -2.6% | -0.021 | 1.1e-07 | 2.86e-05 | 14/16 |
| MNQ | 15 | h2 | -0.032 | -0.045 .. -0.018 | -4.1% | -0.040 | 4.2e-06 |  | 15/16 |
| MNQ | 15 | h4 | -0.056 | -0.088 .. -0.024 | -5.0% | -0.079 | 0.00055 |  | 14/16 |
| MNQ | 15 | h8 | -0.095 | -0.148 .. -0.042 | -5.7% | -0.149 | 0.00048 |  | 15/16 |
| MNQ | 15 | h16 | -0.131 | -0.214 .. -0.049 | -5.2% | -0.248 | 0.0018 |  | 13/16 |
| MNQ | 15 | eod | -0.215 | -0.648 .. +0.218 | -3.4% | -0.771 | 0.33 |  | 8/16 |
| MNQ | 60 | h1 * | -0.005 | -0.016 .. +0.006 | -1.0% | +0.005 | 0.35 | 1 | 10/16 |
| MNQ | 60 | h2 | -0.007 | -0.026 .. +0.012 | -0.9% | +0.003 | 0.46 |  | 8/16 |
| MNQ | 60 | h4 | -0.012 | -0.046 .. +0.022 | -1.1% | -0.012 | 0.48 |  | 8/16 |
| MNQ | 60 | h8 | -0.026 | -0.086 .. +0.033 | -1.6% | -0.065 | 0.4 |  | 9/16 |
| MNQ | 60 | h16 | -0.036 | -0.146 .. +0.075 | -1.6% | -0.170 | 0.54 |  | 8/16 |
| MNQ | 60 | eod | -0.048 | -0.172 .. +0.076 | -2.1% | -0.225 | 0.46 |  | 8/16 |
| MYM | 5 | h1 | -0.002 | -0.005 .. +0.002 | -0.3% | +0.002 | 0.33 |  | 6/8 |
| MYM | 5 | h2 * | -0.008 | -0.015 .. -0.001 | -1.0% | -0.004 | 0.036 | 1 | 5/8 |
| MYM | 5 | h4 | -0.017 | -0.032 .. -0.001 | -1.5% | -0.012 | 0.043 |  | 6/8 |
| MYM | 5 | h8 | -0.017 | -0.045 .. +0.011 | -1.1% | -0.023 | 0.23 |  | 5/8 |
| MYM | 5 | h16 | -0.015 | -0.068 .. +0.038 | -0.6% | -0.051 | 0.59 |  | 5/8 |
| MYM | 5 | eod | +0.420 | -0.660 .. +1.500 | +3.6% | -0.103 | 0.45 |  | 5/8 |
| MYM | 15 | h1 * | -0.007 | -0.015 .. +0.000 | -1.4% | -0.007 | 0.055 | 1 | 6/8 |
| MYM | 15 | h2 | -0.011 | -0.029 .. +0.006 | -1.5% | -0.019 | 0.2 |  | 5/8 |
| MYM | 15 | h4 | -0.017 | -0.055 .. +0.020 | -1.5% | -0.041 | 0.37 |  | 3/8 |
| MYM | 15 | h8 | -0.017 | -0.080 .. +0.047 | -1.0% | -0.076 | 0.61 |  | 3/8 |
| MYM | 15 | h16 | -0.012 | -0.136 .. +0.111 | -0.5% | -0.102 | 0.85 |  | 3/8 |
| MYM | 15 | eod | +0.164 | -0.408 .. +0.735 | +2.7% | -0.112 | 0.58 |  | 5/8 |
| MYM | 60 | h1 | +0.014 | -0.000 .. +0.029 | +2.7% | +0.038 | 0.06 |  | 5/8 |
| MYM | 60 | h2 * | +0.026 | +0.002 .. +0.050 | +3.4% | +0.059 | 0.048 | 1 | 5/8 |
| MYM | 60 | h4 | +0.045 | +0.003 .. +0.087 | +4.2% | +0.079 | 0.048 |  | 6/8 |
| MYM | 60 | h8 | +0.065 | -0.014 .. +0.145 | +4.2% | +0.074 | 0.12 |  | 6/8 |
| MYM | 60 | h16 | +0.072 | -0.080 .. +0.224 | +3.4% | +0.020 | 0.36 |  | 5/8 |
| MYM | 60 | eod | +0.069 | -0.104 .. +0.243 | +3.1% | -0.014 | 0.44 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.01 pts | -0.45 .. +0.46 | 0.98 |
| MES | 15 | +0.19 pts | -0.62 .. +1.01 | 0.65 |
| MES | 60 | +0.24 pts | -1.53 .. +2.01 | 0.79 |
| MNQ | 5 | -0.18 pts | -0.62 .. +0.26 | 0.44 |
| MNQ | 15 | +0.04 pts | -0.77 .. +0.85 | 0.93 |
| MNQ | 60 | -0.32 pts | -2.06 .. +1.41 | 0.71 |
| MYM | 5 | +0.48 pts | -0.13 .. +1.09 | 0.15 |
| MYM | 15 | +0.85 pts | -0.27 .. +1.97 | 0.14 |
| MYM | 60 | +0.91 pts | -1.60 .. +3.41 | 0.48 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 205642 | +0.002 | 0.319 | +0.01 | -3.49 | -3.50 | -3.48 | -3.50 |
| MES | 5 | h2 | event | long | 205642 | +0.005 | 0.319 | +0.03 | -3.47 | -3.49 | -3.45 | -3.49 |
| MES | 5 | h4 | event | long | 205642 | +0.011 | 0.319 | +0.06 | -3.44 | -3.48 | -3.40 | -3.48 |
| MES | 5 | h8 | event | long | 205642 | +0.022 | 0.319 | +0.14 | -3.36 | -3.45 | -3.28 | -3.47 |
| MES | 5 | h16 | event | short | 205642 | -0.046 | 0.319 | -0.29 | -3.79 | -3.61 | -3.97 | -3.53 |
| MES | 5 | eod | event | long | 205642 | +0.811 | 0.319 | +5.08 | +1.58 | -1.73 | +4.89 | -0.40 |
| MES | 15 | h1 | event | short | 68064 | -0.004 | 0.183 | -0.04 | -3.54 | -3.51 | -3.56 | -3.49 |
| MES | 15 | h2 | event | short | 68064 | -0.010 | 0.183 | -0.09 | -3.59 | -3.53 | -3.65 | -3.51 |
| MES | 15 | h4 | event | short | 68064 | -0.019 | 0.183 | -0.21 | -3.71 | -3.57 | -3.84 | -3.53 |
| MES | 15 | h8 | event | short | 68064 | -0.038 | 0.183 | -0.47 | -3.97 | -3.68 | -4.26 | -3.64 |
| MES | 15 | h16 | event | short | 68064 | -0.076 | 0.183 | -1.09 | -4.59 | -3.87 | -5.32 | -4.03 |
| MES | 15 | eod | event | long | 68064 | +0.421 | 0.183 | +5.10 | +1.60 | -1.75 | +4.94 | +0.28 |
| MES | 60 | h1 | event | long | 16799 | +0.008 | 0.091 | +0.21 | -3.29 | -3.44 | -3.14 | -3.46 |
| MES | 60 | h2 | event | long | 16799 | +0.019 | 0.091 | +0.51 | -2.99 | -3.34 | -2.64 | -3.38 |
| MES | 60 | h4 | event | long | 16799 | +0.040 | 0.091 | +1.11 | -2.39 | -3.13 | -1.64 | -3.23 |
| MES | 60 | h8 | event | long | 16799 | +0.081 | 0.091 | +2.16 | -1.34 | -2.61 | -0.06 | -2.97 |
| MES | 60 | h16 | event | long | 16799 | +0.141 | 0.091 | +3.69 | +0.19 | -1.99 | +2.39 | -2.46 |
| MES | 60 | eod | event | long | 16799 | +0.168 | 0.091 | +4.95 | +1.45 | -1.71 | +4.64 | -1.75 |
| MNQ | 5 | h1 | event | short | 205222 | -0.002 | 0.128 | +0.01 | -1.99 | -2.00 | -1.97 | -1.97 |
| MNQ | 5 | h2 | event | short | 205222 | -0.004 | 0.128 | +0.01 | -1.99 | -2.01 | -1.96 | -1.97 |
| MNQ | 5 | h4 | event | short | 205222 | -0.008 | 0.128 | +0.03 | -1.97 | -2.02 | -1.92 | -1.96 |
| MNQ | 5 | h8 | event | short | 205222 | -0.011 | 0.128 | +0.05 | -1.95 | -2.05 | -1.86 | -1.89 |
| MNQ | 5 | h16 | event | short | 205222 | -0.023 | 0.128 | +0.08 | -1.92 | -2.09 | -1.75 | -1.70 |
| MNQ | 5 | eod | event | short | 205222 | -0.238 | 0.128 | -0.55 | -2.55 | -2.61 | -2.48 | -0.51 |
| MNQ | 15 | h1 | event | short | 68036 | -0.003 | 0.073 | +0.03 | -1.97 | -2.02 | -1.91 | -1.86 |
| MNQ | 15 | h2 | event | short | 68036 | -0.005 | 0.073 | +0.05 | -1.95 | -2.04 | -1.86 | -1.80 |
| MNQ | 15 | h4 | event | short | 68036 | -0.007 | 0.073 | +0.07 | -1.93 | -2.07 | -1.78 | -1.62 |
| MNQ | 15 | h8 | event | short | 68036 | -0.012 | 0.073 | +0.09 | -1.91 | -2.14 | -1.68 | -1.27 |
| MNQ | 15 | h16 | event | short | 68036 | -0.015 | 0.073 | -0.03 | -2.03 | -2.27 | -1.80 | -1.34 |
| MNQ | 15 | eod | event | short | 68036 | -0.102 | 0.073 | -0.54 | -2.54 | -2.58 | -2.49 | -1.42 |
| MNQ | 60 | h1 | event | short | 16798 | -0.002 | 0.036 | +0.07 | -1.93 | -2.07 | -1.80 | -1.70 |
| MNQ | 60 | h2 | event | short | 16798 | -0.005 | 0.036 | +0.03 | -1.97 | -2.14 | -1.80 | -1.48 |
| MNQ | 60 | h4 | event | short | 16798 | -0.011 | 0.036 | -0.04 | -2.04 | -2.27 | -1.82 | -1.04 |
| MNQ | 60 | h8 | event | short | 16798 | -0.022 | 0.036 | +0.04 | -1.96 | -2.55 | -1.38 | -0.15 |
| MNQ | 60 | h16 | event | short | 16798 | -0.035 | 0.036 | +0.59 | -1.41 | -2.64 | -0.18 | +1.23 |
| MNQ | 60 | eod | event | short | 16798 | -0.048 | 0.036 | -0.37 | -2.37 | -2.61 | -2.12 | +1.04 |
| MYM | 5 | h1 | event | long | 102700 | +0.002 | 0.167 | +0.02 | -1.98 | +nan | -1.98 | -1.97 |
| MYM | 5 | h2 | event | long | 102700 | +0.004 | 0.167 | +0.05 | -1.95 | +nan | -1.95 | -1.92 |
| MYM | 5 | h4 | event | long | 102700 | +0.009 | 0.167 | +0.11 | -1.89 | +nan | -1.89 | -1.82 |
| MYM | 5 | h8 | event | long | 102700 | +0.015 | 0.167 | +0.23 | -1.77 | +nan | -1.77 | -1.66 |
| MYM | 5 | h16 | event | long | 102700 | +0.047 | 0.167 | +0.49 | -1.51 | +nan | -1.51 | -1.42 |
| MYM | 5 | eod | event | long | 102700 | +1.334 | 0.167 | +7.71 | +5.71 | +nan | +5.71 | +5.09 |
| MYM | 15 | h1 | event | long | 33988 | +0.006 | 0.094 | +0.07 | -1.93 | +nan | -1.93 | -1.93 |
| MYM | 15 | h2 | event | long | 33988 | +0.013 | 0.094 | +0.16 | -1.84 | +nan | -1.84 | -1.81 |
| MYM | 15 | h4 | event | long | 33988 | +0.026 | 0.094 | +0.36 | -1.64 | +nan | -1.64 | -1.59 |
| MYM | 15 | h8 | event | long | 33988 | +0.055 | 0.094 | +0.79 | -1.21 | +nan | -1.21 | -1.07 |
| MYM | 15 | h16 | event | long | 33988 | +0.120 | 0.094 | +1.79 | -0.21 | +nan | -0.21 | +0.26 |
| MYM | 15 | eod | event | long | 33988 | +0.684 | 0.094 | +7.76 | +5.76 | +nan | +5.76 | +6.28 |
| MYM | 60 | h1 | event | long | 8350 | +0.014 | 0.046 | +0.38 | -1.62 | +nan | -1.62 | -1.75 |
| MYM | 60 | h2 | event | long | 8350 | +0.031 | 0.046 | +0.86 | -1.14 | +nan | -1.14 | -1.43 |
| MYM | 60 | h4 | event | long | 8350 | +0.064 | 0.046 | +1.82 | -0.18 | +nan | -0.18 | -0.82 |
| MYM | 60 | h8 | event | long | 8350 | +0.121 | 0.046 | +3.34 | +1.34 | +nan | +1.34 | +0.19 |
| MYM | 60 | h16 | event | long | 8350 | +0.207 | 0.046 | +5.73 | +3.73 | +nan | +3.73 | +1.73 |
| MYM | 60 | eod | event | long | 8350 | +0.240 | 0.046 | +7.50 | +5.50 | +nan | +5.50 | +2.74 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.014 | +0.006 | +0.003 | +0.001 | -0.000 | +0.000 | +0.001 | +0.001 | +0.001 | -0.000 | -0.003 |
| MES | 15 | +0.023 | +0.011 | +0.004 | +0.001 | +0.000 | +0.000 | +0.001 | +0.001 | -0.000 | -0.005 | -0.015 |
| MES | 60 | +0.004 | +0.005 | +0.004 | +0.002 | -0.001 | +0.000 | -0.001 | +0.001 | -0.007 | -0.011 | -0.019 |
| MNQ | 5 | +0.009 | +0.002 | +0.002 | +0.001 | +0.000 | +0.000 | -0.001 | -0.002 | -0.007 | -0.019 | -0.041 |
| MNQ | 15 | +0.019 | +0.009 | +0.005 | +0.003 | +0.001 | +0.000 | -0.002 | -0.006 | -0.014 | -0.034 | -0.073 |
| MNQ | 60 | +0.067 | +0.045 | +0.024 | +0.014 | +0.006 | +0.000 | -0.009 | -0.016 | -0.037 | -0.071 | -0.125 |
| MYM | 5 | +0.000 | +0.002 | -0.000 | -0.002 | -0.002 | +0.000 | +0.005 | +0.009 | +0.017 | +0.026 | +0.053 |
| MYM | 15 | -0.008 | -0.006 | -0.006 | -0.005 | -0.003 | +0.000 | +0.009 | +0.016 | +0.029 | +0.059 | +0.133 |
| MYM | 60 | -0.112 | -0.056 | -0.031 | -0.018 | -0.011 | +0.000 | +0.010 | +0.026 | +0.042 | +0.077 | +0.134 |

## Calibration

- MES 5-min: 1036271 bars, 205642 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68064 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16799 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 205222 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68036 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16798 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 102700 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 33988 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8350 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
