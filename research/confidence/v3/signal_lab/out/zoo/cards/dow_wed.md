# Impact card: dow_wed

session weekday = wed vs other days [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: the market moves 13% MORE after the event than after matched bars over the rest of the session (to 16:45) (+1.314 R20, possible, q=0.0675, 13 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.01 at recent bar sizes, 90% range up to $0.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.141 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 15-min size: the market moves 12% MORE after the event than after matched bars over the rest of the session (to 16:45) (+0.678 R20, possible, q=0.151, 13 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.44 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.132 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.050 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.078 R20 or more 80% of the time).
- MES 60-min size: the market moves 12% MORE after the event than after matched bars over the rest of the session (to 16:45) (+0.269 R20, CONFIRMED, q=0.0317, 12 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.14 at recent bar sizes, 90% range up to $5.65); about 5.7x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.002 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.044).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.05 at recent bar sizes, 90% range up to $1.00); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.028 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.049).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.96 at recent bar sizes, 90% range up to $4.56); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.068 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.085 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.023).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.84 at recent bar sizes, 90% range up to $9.07); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.004 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.67).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.04 at recent bar sizes, 90% range up to $0.83); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.013 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.062 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.81).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.21 at recent bar sizes, 90% range up to $2.31); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.059 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.110 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.63).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.94 at recent bar sizes, 90% range up to $7.88); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.001 | -0.005 .. +0.002 | -0.0007 | 0.48 / 0.5 / 0.52 | nan | 1 | 1 | 10/16 | -0.003 | +0.001 | False | -0.7 / -0.7 |  |
| MES | 5 | h2 | -0.001 | -0.008 .. +0.005 | -0.0006 | 0.65 / 0.66 / 0.68 | nan |  |  | 9/16 | -0.004 | +0.001 |  | -0.6 / -0.4 |  |
| MES | 5 | h4 | -0.001 | -0.015 .. +0.012 | -0.0004 | 0.83 / 0.83 / 0.84 | nan |  |  | 9/16 | -0.004 | +0.002 |  | -0.4 / -0.2 | 0.020 |
| MES | 5 | h8 | -0.000 | -0.028 .. +0.027 | -0.0001 | 0.97 / 0.97 / 0.97 | nan |  |  | 9/16 | -0.006 | +0.005 |  | -0.1 / -0.0 |  |
| MES | 5 | h16 | +0.000 | -0.057 .. +0.057 | +0.0000 | 1 / 1 / 1 | nan |  |  | 7/16 | -0.008 | +0.008 |  | +0.0 / +0.0 |  |
| MES | 5 | eod | -0.340 | -1.364 .. +0.683 | -0.0086 | 0.51 / 0.53 / 0.5 | nan |  |  | 7/16 | -0.277 | -0.403 |  | -8.2 / -0.7 |  |
| MES | 15 | h1 | -0.000 | -0.007 .. +0.006 | -0.0002 | 0.91 / 0.91 / 0.91 | nan |  |  | 7/16 | -0.001 | +0.000 |  | -0.1 / -0.1 |  |
| MES | 15 | h2 | +0.001 | -0.011 .. +0.014 | +0.0005 | 0.83 / 0.83 / 0.84 | nan |  |  | 9/16 | +0.001 | +0.002 |  | +0.3 / +0.2 |  |
| MES | 15 | h4 | +0.005 | -0.021 .. +0.032 | +0.0012 | 0.69 / 0.7 / 0.7 | nan |  |  | 8/16 | +0.004 | +0.006 |  | +0.8 / +0.4 | 0.038 |
| MES | 15 | h8 | +0.007 | -0.045 .. +0.060 | +0.0012 | 0.78 / 0.79 / 0.79 | nan |  |  | 8/16 | +0.009 | +0.006 |  | +0.7 / +0.3 |  |
| MES | 15 | h16 | +0.005 | -0.103 .. +0.113 | +0.0006 | 0.93 / 0.93 / 0.93 | nan |  |  | 9/16 | +0.018 | -0.008 |  | +0.3 / +0.1 |  |
| MES | 15 | eod * | -0.141 | -0.711 .. +0.430 | -0.0062 | 0.63 / 0.64 / 0.63 | nan | 1 | 1 | 6/16 | -0.142 | -0.139 | False | -3.6 / -0.5 |  |
| MES | 60 | h1 | -0.001 | -0.015 .. +0.012 | -0.0006 | 0.87 / 0.87 / 0.86 | nan |  |  | 8/16 | -0.003 | +0.001 |  | -0.2 / -0.2 |  |
| MES | 60 | h2 | -0.003 | -0.031 .. +0.025 | -0.0011 | 0.83 / 0.83 / 0.82 | nan |  |  | 8/16 | -0.008 | +0.002 |  | -0.3 / -0.2 |  |
| MES | 60 | h4 | -0.005 | -0.060 .. +0.049 | -0.0014 | 0.85 / 0.85 / 0.84 | nan |  |  | 7/16 | -0.012 | +0.001 |  | -0.4 / -0.2 | 0.078 |
| MES | 60 | h8 | -0.007 | -0.112 .. +0.098 | -0.0013 | 0.9 / 0.9 / 0.9 | nan |  |  | 7/16 | -0.010 | -0.004 |  | -0.4 / -0.1 |  |
| MES | 60 | h16 | -0.026 | -0.216 .. +0.164 | -0.0037 | 0.79 / 0.8 / 0.79 | nan |  |  | 7/16 | -0.049 | -0.003 |  | -1.0 / -0.3 |  |
| MES | 60 | eod * | -0.050 | -0.267 .. +0.167 | -0.0068 | 0.65 / 0.66 / 0.64 | nan | 1 | 1 | 7/16 | -0.055 | -0.046 | False | -1.8 / -0.5 |  |
| MNQ | 5 | h1 * | +0.002 | -0.003 .. +0.008 | +0.0010 | 0.41 / 0.4 / 0.33 | nan | 1 | 1 | 8/16 | +0.000 | +0.004 | False | +0.9 / +0.8 |  |
| MNQ | 5 | h2 | +0.003 | -0.007 .. +0.013 | +0.0009 | 0.54 / 0.53 / 0.53 | nan |  |  | 7/16 | -0.001 | +0.008 |  | +1.0 / +0.6 |  |
| MNQ | 5 | h4 | +0.006 | -0.015 .. +0.027 | +0.0010 | 0.6 / 0.59 / 0.61 | nan |  |  | 7/16 | -0.004 | +0.015 |  | +1.2 / +0.5 | 0.025 |
| MNQ | 5 | h8 | +0.014 | -0.034 .. +0.061 | +0.0017 | 0.58 / 0.57 / 0.53 | nan |  |  | 7/16 | -0.010 | +0.036 |  | +1.8 / +0.6 |  |
| MNQ | 5 | h16 | +0.028 | -0.071 .. +0.127 | +0.0024 | 0.58 / 0.58 / 0.52 | nan |  |  | 6/16 | -0.017 | +0.072 |  | +2.5 / +0.5 |  |
| MNQ | 5 | eod | -0.230 | -1.511 .. +1.051 | -0.0042 | 0.72 / 0.73 / 0.72 | nan |  |  | 6/16 | -0.461 | -0.002 |  | -4.3 / -0.4 |  |
| MNQ | 15 | h1 | +0.005 | -0.008 .. +0.017 | +0.0019 | 0.44 / 0.44 / 0.29 | nan |  |  | 9/16 | +0.001 | +0.009 |  | +0.8 / +0.8 |  |
| MNQ | 15 | h2 | +0.012 | -0.016 .. +0.040 | +0.0029 | 0.39 / 0.39 / 0.24 | nan |  |  | 9/16 | +0.001 | +0.023 |  | +1.3 / +0.9 |  |
| MNQ | 15 | h4 * | +0.028 | -0.033 .. +0.088 | +0.0039 | 0.37 / 0.36 / 0.21 | nan | 1 | 1 | 8/16 | +0.003 | +0.052 | False | +2.0 / +0.9 | 0.048 |
| MNQ | 15 | h8 | +0.044 | -0.056 .. +0.145 | +0.0048 | 0.38 / 0.38 / 0.26 | nan |  |  | 9/16 | +0.007 | +0.082 |  | +2.6 / +0.9 |  |
| MNQ | 15 | h16 | +0.035 | -0.097 .. +0.167 | +0.0031 | 0.61 / 0.61 / 0.62 | nan |  |  | 10/16 | +0.015 | +0.054 |  | +1.9 / +0.5 |  |
| MNQ | 15 | eod | -0.046 | -0.734 .. +0.643 | -0.0014 | 0.9 / 0.9 / 0.9 | nan |  |  | 5/16 | -0.234 | +0.142 |  | -0.9 / -0.1 |  |
| MNQ | 60 | h1 | -0.002 | -0.017 .. +0.012 | -0.0012 | 0.74 / 0.75 / 0.73 | nan |  |  | 6/16 | -0.005 | +0.000 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h2 | -0.006 | -0.035 .. +0.023 | -0.0019 | 0.69 / 0.7 / 0.68 | nan |  |  | 6/16 | -0.011 | -0.000 |  | -0.5 / -0.4 |  |
| MNQ | 60 | h4 | -0.011 | -0.068 .. +0.046 | -0.0026 | 0.71 / 0.72 / 0.7 | nan |  |  | 5/16 | -0.016 | -0.005 |  | -0.7 / -0.4 | 0.085 |
| MNQ | 60 | h8 | -0.020 | -0.131 .. +0.090 | -0.0035 | 0.72 / 0.73 / 0.71 | nan |  |  | 5/16 | -0.021 | -0.019 |  | -1.0 / -0.4 |  |
| MNQ | 60 | h16 | -0.047 | -0.247 .. +0.154 | -0.0062 | 0.65 / 0.66 / 0.63 | nan |  |  | 6/16 | -0.064 | -0.029 |  | -1.7 / -0.5 |  |
| MNQ | 60 | eod * | -0.068 | -0.296 .. +0.159 | -0.0087 | 0.56 / 0.57 / 0.53 | nan | 1 | 1 | 6/16 | -0.068 | -0.069 | False | -2.3 / -0.6 |  |
| MYM | 5 | h1 * | +0.004 | -0.003 .. +0.012 | +0.0019 | 0.23 / 0.23 / 0.19 | nan | 1 | 1 | 4/8 | n/a | +0.004 | False | +1.3 / +1.2 |  |
| MYM | 5 | h2 | +0.008 | -0.006 .. +0.021 | +0.0019 | 0.28 / 0.28 / 0.33 | nan |  |  | 4/8 | n/a | +0.008 |  | +1.7 / +1.1 |  |
| MYM | 5 | h4 | +0.014 | -0.014 .. +0.042 | +0.0022 | 0.31 / 0.32 / 0.39 | nan |  |  | 5/8 | n/a | +0.014 |  | +2.1 / +1.0 | 0.040 |
| MYM | 5 | h8 | +0.027 | -0.029 .. +0.084 | +0.0030 | 0.34 / 0.35 / 0.38 | nan |  |  | 5/8 | n/a | +0.027 |  | +2.8 / +0.9 |  |
| MYM | 5 | h16 | +0.041 | -0.062 .. +0.144 | +0.0036 | 0.44 / 0.44 / 0.49 | nan |  |  | 5/8 | n/a | +0.041 |  | +3.1 / +0.8 |  |
| MYM | 5 | eod | -0.515 | -2.190 .. +1.159 | -0.0100 | 0.55 / 0.57 / 0.6 | nan |  |  | 5/8 | n/a | -0.515 |  | -7.1 / -0.6 |  |
| MYM | 15 | h1 | +0.007 | -0.007 .. +0.021 | +0.0028 | 0.35 / 0.35 / 0.24 | nan |  |  | 4/8 | n/a | +0.007 |  | +1.0 / +0.9 |  |
| MYM | 15 | h2 * | +0.013 | -0.014 .. +0.040 | +0.0031 | 0.34 / 0.34 / 0.35 | nan | 1 | 1 | 4/8 | n/a | +0.013 | False | +1.3 / +1.0 |  |
| MYM | 15 | h4 | +0.027 | -0.028 .. +0.081 | +0.0038 | 0.33 / 0.34 / 0.37 | nan |  |  | 4/8 | n/a | +0.027 |  | +1.8 / +1.0 | 0.062 |
| MYM | 15 | h8 | +0.030 | -0.055 .. +0.116 | +0.0033 | 0.49 / 0.5 / 0.57 | nan |  |  | 5/8 | n/a | +0.030 |  | +1.7 / +0.7 |  |
| MYM | 15 | h16 | +0.001 | -0.169 .. +0.171 | +0.0001 | 0.99 / 0.99 / 0.99 | nan |  |  | 5/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 15 | eod | -0.172 | -1.026 .. +0.683 | -0.0054 | 0.69 / 0.71 / 0.75 | nan |  |  | 4/8 | n/a | -0.172 |  | -2.6 / -0.4 |  |
| MYM | 60 | h1 | +0.001 | -0.018 .. +0.020 | +0.0004 | 0.93 / 0.93 / 0.95 | nan |  |  | 5/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 60 | h2 | +0.001 | -0.038 .. +0.039 | +0.0002 | 0.97 / 0.97 / 0.98 | nan |  |  | 5/8 | n/a | +0.001 |  | +0.0 / +0.0 |  |
| MYM | 60 | h4 | -0.003 | -0.080 .. +0.074 | -0.0008 | 0.93 / 0.94 / 0.94 | nan |  |  | 3/8 | n/a | -0.003 |  | -0.2 / -0.1 | 0.110 |
| MYM | 60 | h8 | -0.011 | -0.162 .. +0.140 | -0.0020 | 0.88 / 0.89 / 0.91 | nan |  |  | 3/8 | n/a | -0.011 |  | -0.4 / -0.1 |  |
| MYM | 60 | h16 | -0.012 | -0.281 .. +0.258 | -0.0016 | 0.93 / 0.94 / 0.95 | nan |  |  | 3/8 | n/a | -0.012 |  | -0.3 / -0.1 |  |
| MYM | 60 | eod * | -0.059 | -0.369 .. +0.252 | -0.0076 | 0.71 / 0.73 / 0.77 | nan | 1 | 1 | 4/8 | n/a | -0.059 | False | -1.5 / -0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.000 .. +0.004 | +0.4% | +0.005 | 0.1 |  | 11/16 |
| MES | 5 | h2 | -0.000 | -0.005 .. +0.004 | -0.1% | +0.006 | 0.86 |  | 7/16 |
| MES | 5 | h4 | -0.001 | -0.010 .. +0.007 | -0.1% | +0.010 | 0.78 |  | 7/16 |
| MES | 5 | h8 | -0.002 | -0.019 .. +0.015 | -0.1% | +0.017 | 0.83 |  | 7/16 |
| MES | 5 | h16 | -0.001 | -0.035 .. +0.032 | -0.1% | +0.040 | 0.94 |  | 7/16 |
| MES | 5 | eod * | +1.314 | +0.615 .. +2.013 | +13.2% | +1.854 | 0.00037 | 0.0675 | 13/16 |
| MES | 15 | h1 | +0.007 | +0.002 .. +0.011 | +1.4% | +0.018 | 0.0028 |  | 12/16 |
| MES | 15 | h2 | +0.007 | -0.001 .. +0.016 | +1.0% | +0.025 | 0.072 |  | 11/16 |
| MES | 15 | h4 | +0.008 | -0.008 .. +0.024 | +0.8% | +0.036 | 0.32 |  | 11/16 |
| MES | 15 | h8 | +0.013 | -0.019 .. +0.045 | +0.8% | +0.056 | 0.43 |  | 9/16 |
| MES | 15 | h16 | +0.032 | -0.033 .. +0.097 | +1.4% | +0.109 | 0.35 |  | 9/16 |
| MES | 15 | eod * | +0.678 | +0.287 .. +1.070 | +12.4% | +0.962 | 0.00087 | 0.151 | 13/16 |
| MES | 60 | h1 | +0.010 | -0.001 .. +0.020 | +1.9% | +0.020 | 0.078 |  | 9/16 |
| MES | 60 | h2 | +0.015 | -0.004 .. +0.033 | +2.0% | +0.034 | 0.12 |  | 8/16 |
| MES | 60 | h4 | +0.026 | -0.009 .. +0.060 | +2.4% | +0.064 | 0.15 |  | 11/16 |
| MES | 60 | h8 | +0.079 | +0.015 .. +0.143 | +5.2% | +0.126 | 0.017 |  | 11/16 |
| MES | 60 | h16 | +0.195 | +0.080 .. +0.310 | +9.5% | +0.256 | 0.0013 |  | 11/16 |
| MES | 60 | eod * | +0.269 | +0.134 .. +0.404 | +12.4% | +0.343 | 0.00016 | 0.0317 | 12/16 |
| MNQ | 5 | h1 | +0.003 | +0.000 .. +0.006 | +0.6% | +0.005 | 0.031 |  | 12/16 |
| MNQ | 5 | h2 | +0.001 | -0.004 .. +0.007 | +0.2% | +0.007 | 0.63 |  | 10/16 |
| MNQ | 5 | h4 | -0.000 | -0.011 .. +0.011 | -0.0% | +0.010 | 0.99 |  | 7/16 |
| MNQ | 5 | h8 | +0.002 | -0.021 .. +0.025 | +0.1% | +0.020 | 0.86 |  | 10/16 |
| MNQ | 5 | h16 | +0.011 | -0.036 .. +0.057 | +0.4% | +0.047 | 0.65 |  | 8/16 |
| MNQ | 5 | eod * | +1.215 | +0.344 .. +2.087 | +9.7% | +2.011 | 0.0074 | 1 | 12/16 |
| MNQ | 15 | h1 | +0.013 | +0.003 .. +0.023 | +2.5% | +0.025 | 0.011 |  | 13/16 |
| MNQ | 15 | h2 | +0.018 | +0.002 .. +0.034 | +2.3% | +0.037 | 0.024 |  | 14/16 |
| MNQ | 15 | h4 | +0.025 | -0.006 .. +0.057 | +2.2% | +0.060 | 0.12 |  | 12/16 |
| MNQ | 15 | h8 | +0.044 | -0.011 .. +0.098 | +2.6% | +0.103 | 0.12 |  | 11/16 |
| MNQ | 15 | h16 | +0.045 | -0.033 .. +0.123 | +1.8% | +0.158 | 0.26 |  | 9/16 |
| MNQ | 15 | eod * | +0.620 | +0.164 .. +1.077 | +9.8% | +1.074 | 0.0082 | 1 | 11/16 |
| MNQ | 60 | h1 | +0.015 | +0.003 .. +0.027 | +2.8% | +0.033 | 0.017 |  | 12/16 |
| MNQ | 60 | h2 | +0.026 | +0.004 .. +0.047 | +3.4% | +0.052 | 0.019 |  | 10/16 |
| MNQ | 60 | h4 | +0.044 | +0.004 .. +0.083 | +3.9% | +0.087 | 0.03 |  | 14/16 |
| MNQ | 60 | h8 | +0.084 | +0.012 .. +0.157 | +5.3% | +0.148 | 0.023 |  | 11/16 |
| MNQ | 60 | h16 | +0.163 | +0.032 .. +0.294 | +7.4% | +0.258 | 0.015 |  | 10/16 |
| MNQ | 60 | eod * | +0.224 | +0.074 .. +0.374 | +9.8% | +0.335 | 0.0039 | 0.585 | 12/16 |
| MYM | 5 | h1 | +0.003 | -0.001 .. +0.006 | +0.5% | +0.009 | 0.21 |  | 5/8 |
| MYM | 5 | h2 | -0.001 | -0.010 .. +0.008 | -0.1% | +0.012 | 0.83 |  | 3/8 |
| MYM | 5 | h4 | -0.005 | -0.026 .. +0.015 | -0.5% | +0.015 | 0.62 |  | 5/8 |
| MYM | 5 | h8 | -0.020 | -0.058 .. +0.018 | -1.2% | +0.020 | 0.35 |  | 6/8 |
| MYM | 5 | h16 | -0.041 | -0.102 .. +0.020 | -1.7% | +0.038 | 0.22 |  | 6/8 |
| MYM | 5 | eod * | +0.987 | -0.169 .. +2.143 | +8.4% | +1.858 | 0.11 | 1 | 6/8 |
| MYM | 15 | h1 * | +0.008 | -0.002 .. +0.018 | +1.5% | +0.022 | 0.13 | 1 | 7/8 |
| MYM | 15 | h2 | +0.002 | -0.012 .. +0.016 | +0.3% | +0.027 | 0.78 |  | 5/8 |
| MYM | 15 | h4 | -0.009 | -0.036 .. +0.018 | -0.8% | +0.032 | 0.58 |  | 4/8 |
| MYM | 15 | h8 | -0.028 | -0.079 .. +0.024 | -1.7% | +0.037 | 0.33 |  | 6/8 |
| MYM | 15 | h16 | -0.027 | -0.138 .. +0.084 | -1.1% | +0.014 | 0.66 |  | 4/8 |
| MYM | 15 | eod | +0.266 | -0.328 .. +0.860 | +4.4% | +0.656 | 0.41 |  | 5/8 |
| MYM | 60 | h1 | -0.006 | -0.021 .. +0.009 | -1.2% | +0.007 | 0.46 |  | 5/8 |
| MYM | 60 | h2 | -0.006 | -0.032 .. +0.021 | -0.7% | +0.009 | 0.69 |  | 6/8 |
| MYM | 60 | h4 | -0.002 | -0.049 .. +0.046 | -0.2% | +0.020 | 0.94 |  | 6/8 |
| MYM | 60 | h8 | +0.025 | -0.060 .. +0.110 | +1.6% | +0.056 | 0.59 |  | 3/8 |
| MYM | 60 | h16 | +0.083 | -0.073 .. +0.238 | +3.9% | +0.127 | 0.33 |  | 5/8 |
| MYM | 60 | eod * | +0.165 | -0.020 .. +0.350 | +7.4% | +0.216 | 0.11 | 1 | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.09 pts | -0.37 .. +0.55 | 0.71 |
| MES | 15 | -0.18 pts | -1.03 .. +0.66 | 0.67 |
| MES | 60 | -1.21 pts | -3.00 .. +0.58 | 0.18 |
| MNQ | 5 | +0.13 pts | -0.32 .. +0.58 | 0.58 |
| MNQ | 15 | -0.20 pts | -0.95 .. +0.55 | 0.61 |
| MNQ | 60 | -0.69 pts | -2.32 .. +0.93 | 0.44 |
| MYM | 5 | +0.10 pts | -0.52 .. +0.72 | 0.76 |
| MYM | 15 | -0.04 pts | -1.19 .. +1.11 | 0.95 |
| MYM | 60 | -1.33 pts | -3.88 .. +1.23 | 0.31 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 208458 | -0.001 | 0.330 | -0.02 | -3.52 | -3.50 | -3.54 | -3.52 |
| MES | 5 | h2 | event | short | 208458 | -0.003 | 0.330 | -0.06 | -3.56 | -3.52 | -3.60 | -3.54 |
| MES | 5 | h4 | event | short | 208458 | -0.009 | 0.330 | -0.13 | -3.63 | -3.56 | -3.71 | -3.59 |
| MES | 5 | h8 | event | short | 208458 | -0.021 | 0.330 | -0.28 | -3.78 | -3.63 | -3.93 | -3.68 |
| MES | 5 | h16 | event | long | 208458 | +0.046 | 0.330 | +0.56 | -2.94 | -3.21 | -2.66 | -3.18 |
| MES | 5 | eod | event | short | 208458 | -0.270 | 0.330 | -4.24 | -7.74 | -6.53 | -8.96 | -5.89 |
| MES | 15 | h1 | event | short | 68787 | -0.004 | 0.194 | -0.09 | -3.59 | -3.53 | -3.65 | -3.55 |
| MES | 15 | h2 | event | long | 68787 | +0.011 | 0.194 | +0.21 | -3.29 | -3.41 | -3.18 | -3.37 |
| MES | 15 | h4 | event | long | 68787 | +0.024 | 0.194 | +0.42 | -3.08 | -3.29 | -2.86 | -3.24 |
| MES | 15 | h8 | event | long | 68787 | +0.046 | 0.194 | +0.85 | -2.65 | -3.07 | -2.22 | -2.97 |
| MES | 15 | h16 | event | long | 68787 | +0.080 | 0.194 | +1.68 | -1.82 | -2.56 | -1.06 | -2.37 |
| MES | 15 | eod | event | short | 68787 | -0.163 | 0.194 | -4.37 | -7.87 | -6.50 | -9.25 | -6.52 |
| MES | 60 | h1 | event | short | 16703 | -0.008 | 0.098 | -0.43 | -3.93 | -3.71 | -4.15 | -3.75 |
| MES | 60 | h2 | event | short | 16703 | -0.015 | 0.098 | -0.90 | -4.40 | -3.91 | -4.92 | -4.01 |
| MES | 60 | h4 | event | short | 16703 | -0.033 | 0.098 | -1.86 | -5.36 | -4.45 | -6.32 | -4.50 |
| MES | 60 | h8 | event | short | 16703 | -0.065 | 0.098 | -3.61 | -7.11 | -5.60 | -8.71 | -5.45 |
| MES | 60 | h16 | event | short | 16703 | -0.093 | 0.098 | -5.14 | -8.64 | -6.16 | -11.26 | -6.03 |
| MES | 60 | eod | event | short | 16703 | -0.090 | 0.098 | -4.94 | -8.44 | -6.44 | -10.55 | -5.32 |
| MNQ | 5 | h1 | event | long | 208007 | +0.006 | 0.132 | +0.06 | -1.94 | -1.98 | -1.91 | -1.96 |
| MNQ | 5 | h2 | event | long | 208007 | +0.010 | 0.132 | +0.12 | -1.88 | -1.95 | -1.80 | -1.89 |
| MNQ | 5 | h4 | event | long | 208007 | +0.019 | 0.132 | +0.25 | -1.75 | -1.91 | -1.59 | -1.77 |
| MNQ | 5 | h8 | event | long | 208007 | +0.041 | 0.132 | +0.50 | -1.50 | -1.81 | -1.19 | -1.56 |
| MNQ | 5 | h16 | event | long | 208007 | +0.084 | 0.132 | +0.98 | -1.02 | -1.61 | -0.43 | -1.23 |
| MNQ | 5 | eod | event | short | 208007 | -0.576 | 0.132 | -7.44 | -9.44 | -6.22 | -12.68 | -7.64 |
| MNQ | 15 | h1 | event | long | 68671 | +0.011 | 0.077 | +0.17 | -1.83 | -1.93 | -1.72 | -1.93 |
| MNQ | 15 | h2 | event | long | 68671 | +0.023 | 0.077 | +0.37 | -1.63 | -1.85 | -1.42 | -1.77 |
| MNQ | 15 | h4 | event | long | 68671 | +0.047 | 0.077 | +0.73 | -1.27 | -1.70 | -0.84 | -1.54 |
| MNQ | 15 | h8 | event | long | 68671 | +0.087 | 0.077 | +1.44 | -0.56 | -1.42 | +0.30 | -1.17 |
| MNQ | 15 | h16 | event | long | 68671 | +0.117 | 0.077 | +2.66 | +0.66 | -0.81 | +2.15 | -0.03 |
| MNQ | 15 | eod | event | short | 68671 | -0.300 | 0.077 | -7.08 | -9.08 | -6.21 | -12.01 | -8.03 |
| MNQ | 60 | h1 | event | short | 16641 | -0.009 | 0.038 | -0.61 | -2.61 | -2.29 | -2.95 | -2.33 |
| MNQ | 60 | h2 | event | short | 16641 | -0.017 | 0.038 | -1.20 | -3.20 | -2.56 | -3.87 | -2.62 |
| MNQ | 60 | h4 | event | short | 16641 | -0.033 | 0.038 | -2.25 | -4.25 | -3.20 | -5.37 | -3.09 |
| MNQ | 60 | h8 | event | short | 16641 | -0.061 | 0.038 | -4.12 | -6.12 | -4.51 | -7.83 | -3.93 |
| MNQ | 60 | h16 | event | short | 16641 | -0.089 | 0.038 | -5.75 | -7.75 | -5.57 | -10.07 | -4.40 |
| MNQ | 60 | eod | event | short | 16641 | -0.093 | 0.038 | -5.58 | -7.58 | -6.15 | -9.09 | -3.42 |
| MYM | 5 | h1 | event | long | 103684 | +0.003 | 0.172 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 5 | h2 | event | long | 103684 | +0.004 | 0.172 | +0.08 | -1.92 | +nan | -1.92 | -1.90 |
| MYM | 5 | h4 | event | long | 103684 | +0.006 | 0.172 | +0.16 | -1.84 | +nan | -1.84 | -1.78 |
| MYM | 5 | h8 | event | long | 103684 | +0.013 | 0.172 | +0.31 | -1.69 | +nan | -1.69 | -1.59 |
| MYM | 5 | h16 | event | long | 103684 | +0.027 | 0.172 | +0.58 | -1.42 | +nan | -1.42 | -1.32 |
| MYM | 5 | eod | event | short | 103684 | +0.211 | 0.172 | -3.62 | -5.62 | +nan | -5.62 | -5.04 |
| MYM | 15 | h1 | event | long | 34113 | +0.007 | 0.099 | +0.12 | -1.88 | +nan | -1.88 | -1.89 |
| MYM | 15 | h2 | event | long | 34113 | +0.010 | 0.099 | +0.23 | -1.77 | +nan | -1.77 | -1.73 |
| MYM | 15 | h4 | event | long | 34113 | +0.020 | 0.099 | +0.45 | -1.55 | +nan | -1.55 | -1.48 |
| MYM | 15 | h8 | event | long | 34113 | +0.019 | 0.099 | +0.88 | -1.12 | +nan | -1.12 | -0.97 |
| MYM | 15 | h16 | event | long | 34113 | -0.028 | 0.099 | +1.61 | -0.39 | +nan | -0.39 | +0.16 |
| MYM | 15 | eod | event | short | 34113 | +0.100 | 0.099 | -3.70 | -5.70 | +nan | -5.70 | -6.55 |
| MYM | 60 | h1 | event | long | 8140 | +0.004 | 0.049 | +0.46 | -1.54 | +nan | -1.54 | -1.64 |
| MYM | 60 | h2 | event | long | 8140 | +0.007 | 0.049 | +0.97 | -1.03 | +nan | -1.03 | -1.24 |
| MYM | 60 | h4 | event | short | 8140 | -0.010 | 0.049 | -1.84 | -3.84 | +nan | -3.84 | -3.44 |
| MYM | 60 | h8 | event | short | 8140 | -0.014 | 0.049 | -3.44 | -5.44 | +nan | -5.44 | -4.72 |
| MYM | 60 | h16 | event | short | 8140 | -0.022 | 0.049 | -4.96 | -6.96 | +nan | -6.96 | -5.95 |
| MYM | 60 | eod | event | short | 8140 | +0.005 | 0.049 | -4.13 | -6.13 | +nan | -6.13 | -4.62 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.004 | +0.004 | +0.001 | +0.000 | +0.000 | +0.000 | +0.000 | -0.000 | -0.000 | +0.002 | +0.008 |
| MES | 15 | -0.006 | -0.005 | -0.003 | -0.001 | -0.001 | +0.000 | +0.001 | +0.002 | +0.007 | +0.017 | +0.031 |
| MES | 60 | -0.007 | -0.007 | -0.003 | -0.002 | +0.001 | +0.000 | -0.001 | -0.001 | +0.009 | +0.028 | +0.073 |
| MNQ | 5 | +0.015 | +0.009 | +0.003 | +0.001 | +0.000 | +0.000 | +0.001 | +0.002 | +0.003 | +0.012 | +0.031 |
| MNQ | 15 | +0.020 | +0.009 | +0.003 | +0.001 | +0.000 | +0.000 | +0.004 | +0.009 | +0.024 | +0.045 | +0.046 |
| MNQ | 60 | +0.066 | +0.022 | +0.011 | +0.003 | +0.003 | +0.000 | -0.002 | -0.005 | -0.000 | +0.004 | +0.033 |
| MYM | 5 | +0.008 | +0.004 | +0.000 | -0.001 | -0.001 | +0.000 | +0.003 | +0.005 | +0.011 | +0.021 | +0.040 |
| MYM | 15 | -0.026 | -0.017 | -0.008 | -0.004 | -0.003 | +0.000 | +0.004 | +0.009 | +0.021 | +0.033 | +0.036 |
| MYM | 60 | -0.105 | -0.061 | -0.030 | -0.012 | -0.002 | +0.000 | +0.001 | -0.000 | +0.019 | +0.066 | +0.161 |

## Calibration

- MES 5-min: 1036271 bars, 208458 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 68787 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 16703 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 208007 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 68671 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16641 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 103684 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34113 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8140 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
