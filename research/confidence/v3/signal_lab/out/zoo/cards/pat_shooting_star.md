# Impact card: pat_shooting_star

candle pattern shooting_star in its textbook direction: inverted-hammer shape after prior close > EMA10 -> bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.014 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.052 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.02).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.80 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.288 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.393 R20 over the rest of the session (to 16:45), p=0.69; we would catch an effect of 0.118 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.02).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $9.12 at recent bar sizes, 90% range up to $5.34); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.114 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.268 R20 or more 80% of the time).
- MES 60-min size: the market moves 25% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.183 R20, possible, q=0.184, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $5.48 at recent bar sizes, 90% range up to $11.92); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.022 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=0.094).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.62 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.103 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.083 R20 over the next 2 bars (30 min), p=0.18; we would catch an effect of 0.133 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 12% MORE after the event than after matched bars over the next 2 bars (30 min) (+0.094 R20, possible, q=0.128, 10 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.99 at recent bar sizes, 90% range up to $8.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: POSSIBLE direction effect -0.468 average bars (~$39.59 per micro at 2018-25 bar sizes) over the next 8 bars (8 h) (in the signal's direction), not confirmed (q=0.224, replicated in the other half=False, 12 of 16 years); best leg (event, against signal) grosses $+12.23 and nets $+10.23 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.055).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $39.59 at recent bar sizes, 90% range up to $59.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.019 R20 over the next 2 bars (10 min), p=1; we would catch an effect of 0.093 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.46).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.18 at recent bar sizes, 90% range up to $1.36); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.027 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.184 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.44 at recent bar sizes, 90% range up to $4.39); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.321 R20 over the next 8 bars (8 h), p=0.82; we would catch an effect of 0.383 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $12.43 at recent bar sizes, 90% range up to $24.94); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.016 .. +0.020 | +0.0002 | 0.83 / 0.83 / 0.82 | 0.824 |  |  | 10/16 | -0.002 | +0.006 |  | +0.2 / +0.2 |  |
| MES | 5 | h2 * | +0.014 | -0.011 .. +0.040 | +0.0011 | 0.26 / 0.26 / 0.27 | 0.262 | 1 | 1 | 11/16 | +0.012 | +0.017 | False | +1.1 / +1.1 |  |
| MES | 5 | h4 | +0.004 | -0.032 .. +0.040 | +0.0002 | 0.82 / 0.82 / 0.81 | 0.808 |  |  | 10/16 | -0.001 | +0.009 |  | +0.2 / +0.2 | 0.052 |
| MES | 5 | h8 | -0.021 | -0.075 .. +0.032 | -0.0008 | 0.43 / 0.42 / 0.46 | 0.436 |  |  | 8/16 | -0.000 | -0.042 |  | -0.8 / -0.8 |  |
| MES | 5 | h16 | -0.009 | -0.084 .. +0.067 | -0.0002 | 0.82 / 0.82 / 0.83 | 0.819 |  |  | 9/16 | +0.054 | -0.071 |  | -0.2 / -0.2 |  |
| MES | 5 | eod | -0.070 | -0.668 .. +0.528 | -0.0004 | 0.82 / 0.82 / 0.75 | 0.741 |  |  | 8/16 | +0.225 | -0.364 |  | -0.3 / -0.2 |  |
| MES | 15 | h1 | -0.037 | -0.084 .. +0.011 | -0.0035 | 0.13 / 0.12 / 0.082 | 0.0787 |  |  | 10/16 | -0.018 | -0.055 |  | -1.6 / -1.5 |  |
| MES | 15 | h2 | +0.005 | -0.066 .. +0.076 | +0.0003 | 0.88 / 0.88 / 0.87 | 0.865 |  |  | 7/16 | -0.002 | +0.012 |  | +0.2 / +0.1 |  |
| MES | 15 | h4 | -0.014 | -0.111 .. +0.084 | -0.0006 | 0.78 / 0.78 / 0.77 | 0.744 |  |  | 9/16 | -0.025 | -0.002 |  | -0.3 / -0.3 | 0.118 |
| MES | 15 | h8 | -0.060 | -0.186 .. +0.065 | -0.0018 | 0.35 / 0.33 / 0.36 | 0.339 |  |  | 11/16 | -0.058 | -0.062 |  | -1.0 / -0.9 |  |
| MES | 15 | h16 | -0.120 | -0.293 .. +0.052 | -0.0025 | 0.17 / 0.18 / 0.18 | 0.185 |  |  | 12/16 | -0.132 | -0.109 |  | -1.4 / -1.4 |  |
| MES | 15 | eod * | -0.393 | -0.883 .. +0.096 | -0.0032 | 0.12 / 0.11 / 0.098 | 0.0987 | 1 | 1 | 11/16 | -0.592 | -0.196 | False | -1.8 / -1.6 |  |
| MES | 60 | h1 | +0.035 | -0.081 .. +0.151 | +0.0030 | 0.56 / 0.55 / 0.47 | 0.464 |  |  | 9/16 | +0.141 | -0.071 |  | +0.6 / +0.6 |  |
| MES | 60 | h2 | +0.015 | -0.161 .. +0.191 | +0.0009 | 0.87 / 0.86 / 0.83 | 0.825 |  |  | 7/16 | -0.007 | +0.037 |  | +0.2 / +0.2 |  |
| MES | 60 | h4 | -0.034 | -0.268 .. +0.200 | -0.0015 | 0.78 / 0.77 / 0.73 | 0.734 |  |  | 8/16 | -0.088 | +0.021 |  | -0.3 / -0.3 | 0.268 |
| MES | 60 | h8 | +0.006 | -0.280 .. +0.292 | +0.0002 | 0.97 / 0.97 / 0.97 | 0.962 |  |  | 9/16 | -0.016 | +0.029 |  | +0.0 / +0.0 |  |
| MES | 60 | h16 * | +0.114 | -0.201 .. +0.428 | +0.0027 | 0.48 / 0.48 / 0.46 | 0.451 | 1 | 1 | 10/16 | +0.097 | +0.131 | False | +0.7 / +0.7 |  |
| MES | 60 | eod | +0.106 | -0.207 .. +0.420 | +0.0024 | 0.51 / 0.51 / 0.49 | 0.487 |  |  | 10/16 | +0.081 | +0.132 |  | +0.6 / +0.7 |  |
| MNQ | 5 | h1 | -0.012 | -0.032 .. +0.008 | -0.0011 | 0.25 / 0.25 / 0.29 | 0.251 |  |  | 8/16 | -0.022 | -0.002 |  | -1.1 / -1.1 |  |
| MNQ | 5 | h2 * | -0.022 | -0.054 .. +0.010 | -0.0013 | 0.17 / 0.15 / 0.19 | 0.148 | 1 | 1 | 9/16 | -0.023 | -0.021 | False | -1.4 / -1.4 |  |
| MNQ | 5 | h4 | -0.004 | -0.046 .. +0.039 | -0.0001 | 0.86 / 0.86 / 0.89 | 0.874 |  |  | 9/16 | +0.021 | -0.028 |  | -0.2 / -0.2 | 0.060 |
| MNQ | 5 | h8 | -0.032 | -0.094 .. +0.030 | -0.0008 | 0.31 / 0.31 / 0.43 | 0.371 |  |  | 8/16 | -0.012 | -0.053 |  | -1.0 / -1.0 |  |
| MNQ | 5 | h16 | -0.056 | -0.157 .. +0.046 | -0.0010 | 0.28 / 0.28 / 0.34 | 0.324 |  |  | 6/16 | -0.053 | -0.058 |  | -1.1 / -1.1 |  |
| MNQ | 5 | eod | -0.048 | -0.960 .. +0.864 | -0.0002 | 0.92 / 0.92 / 0.87 | 0.861 |  |  | 9/16 | -0.225 | +0.127 |  | -0.2 / -0.1 |  |
| MNQ | 15 | h1 | +0.019 | -0.026 .. +0.065 | +0.0014 | 0.4 / 0.41 / 0.5 | 0.411 |  |  | 7/16 | +0.006 | +0.033 |  | +0.8 / +0.8 |  |
| MNQ | 15 | h2 * | +0.083 | +0.011 .. +0.155 | +0.0036 | 0.025 / 0.028 / 0.081 | 0.0406 | 1 | 0.995 | 10/16 | +0.087 | +0.079 | False | +2.2 / +2.2 |  |
| MNQ | 15 | h4 | +0.080 | -0.029 .. +0.189 | +0.0021 | 0.15 / 0.15 / 0.31 | 0.152 |  |  | 8/16 | +0.062 | +0.098 |  | +1.5 / +1.4 | 0.133 |
| MNQ | 15 | h8 | +0.115 | -0.028 .. +0.257 | +0.0023 | 0.11 / 0.13 / 0.23 | 0.168 |  |  | 10/16 | +0.120 | +0.110 |  | +1.5 / +1.6 |  |
| MNQ | 15 | h16 | +0.077 | -0.133 .. +0.288 | +0.0012 | 0.47 / 0.48 / 0.54 | 0.483 |  |  | 9/16 | +0.028 | +0.126 |  | +0.7 / +0.7 |  |
| MNQ | 15 | eod | -0.385 | -1.018 .. +0.248 | -0.0021 | 0.23 / 0.23 / 0.29 | 0.258 |  |  | 8/16 | -0.675 | -0.096 |  | -1.4 / -1.2 |  |
| MNQ | 60 | h1 | -0.098 | -0.212 .. +0.017 | -0.0078 | 0.094 / 0.081 / 0.066 | 0.0659 |  |  | 9/16 | -0.127 | -0.068 |  | -1.7 / -1.7 |  |
| MNQ | 60 | h2 | -0.146 | -0.313 .. +0.020 | -0.0082 | 0.085 / 0.067 / 0.055 | 0.0547 |  |  | 11/16 | -0.288 | -0.005 |  | -1.8 / -1.7 |  |
| MNQ | 60 | h4 | -0.226 | -0.453 .. +0.002 | -0.0090 | 0.052 / 0.053 / 0.037 | 0.0362 |  |  | 10/16 | -0.315 | -0.137 |  | -2.0 / -1.9 | 0.302 |
| MNQ | 60 | h8 * | -0.468 | -0.753 .. -0.183 | -0.0135 | 0.0013 / 0.0013 / 0.0018 | 0.00287 | 0.224 | 0.297 | 12/16 | -0.624 | -0.311 | False | -3.3 / -3.2 |  |
| MNQ | 60 | h16 | -0.454 | -0.764 .. -0.144 | -0.0100 | 0.0041 / 0.0043 / 0.0066 | 0.00677 |  |  | 11/16 | -0.520 | -0.389 |  | -2.9 / -2.9 |  |
| MNQ | 60 | eod | -0.460 | -0.770 .. -0.151 | -0.0097 | 0.0036 / 0.0037 / 0.0059 | 0.00677 |  |  | 11/16 | -0.531 | -0.390 |  | -3.0 / -2.9 |  |
| MYM | 5 | h1 | +0.011 | -0.020 .. +0.042 | +0.0009 | 0.49 / 0.49 / 0.58 | 0.511 |  |  | 7/8 | n/a | +0.011 |  | +0.6 / +0.7 |  |
| MYM | 5 | h2 * | +0.019 | -0.030 .. +0.069 | +0.0010 | 0.44 / 0.41 / 0.49 | 0.388 | 1 | 1 | 5/8 | n/a | +0.019 | False | +0.9 / +0.8 |  |
| MYM | 5 | h4 | +0.012 | -0.056 .. +0.081 | +0.0004 | 0.72 / 0.7 / 0.79 | 0.693 |  |  | 5/8 | n/a | +0.012 |  | +0.4 / +0.4 | 0.093 |
| MYM | 5 | h8 | -0.008 | -0.098 .. +0.082 | -0.0002 | 0.86 / 0.86 / 0.93 | 0.896 |  |  | 3/8 | n/a | -0.008 |  | -0.2 / -0.2 |  |
| MYM | 5 | h16 | -0.036 | -0.189 .. +0.118 | -0.0006 | 0.65 / 0.65 / 0.71 | 0.667 |  |  | 4/8 | n/a | -0.036 |  | -0.5 / -0.5 |  |
| MYM | 5 | eod | -0.388 | -1.566 .. +0.790 | -0.0015 | 0.52 / 0.51 / 0.37 | 0.353 |  |  | 6/8 | n/a | -0.388 |  | -1.0 / -0.6 |  |
| MYM | 15 | h1 * | -0.027 | -0.103 .. +0.049 | -0.0020 | 0.49 / 0.49 / 0.52 | 0.421 | 1 | 1 | 6/8 | n/a | -0.027 | False | -0.7 / -0.7 |  |
| MYM | 15 | h2 | -0.011 | -0.112 .. +0.091 | -0.0005 | 0.84 / 0.84 / 0.88 | 0.823 |  |  | 4/8 | n/a | -0.011 |  | -0.2 / -0.2 |  |
| MYM | 15 | h4 | +0.020 | -0.134 .. +0.174 | +0.0005 | 0.8 / 0.8 / 0.86 | 0.783 |  |  | 3/8 | n/a | +0.020 |  | +0.3 / +0.3 | 0.184 |
| MYM | 15 | h8 | +0.025 | -0.190 .. +0.240 | +0.0005 | 0.82 / 0.82 / 0.84 | 0.795 |  |  | 4/8 | n/a | +0.025 |  | +0.3 / +0.2 |  |
| MYM | 15 | h16 | -0.047 | -0.328 .. +0.233 | -0.0007 | 0.74 / 0.75 / 0.82 | 0.796 |  |  | 4/8 | n/a | -0.047 |  | -0.4 / -0.3 |  |
| MYM | 15 | eod | +0.058 | -0.838 .. +0.954 | +0.0003 | 0.9 / 0.9 / 0.91 | 0.895 |  |  | 5/8 | n/a | +0.058 |  | +0.2 / +0.1 |  |
| MYM | 60 | h1 | +0.019 | -0.106 .. +0.145 | +0.0016 | 0.76 / 0.77 / 0.78 | 0.787 |  |  | 3/8 | n/a | +0.019 |  | +0.3 / +0.3 |  |
| MYM | 60 | h2 | +0.064 | -0.116 .. +0.245 | +0.0038 | 0.48 / 0.49 / 0.53 | 0.507 |  |  | 5/8 | n/a | +0.064 |  | +0.7 / +0.7 |  |
| MYM | 60 | h4 | +0.140 | -0.115 .. +0.395 | +0.0060 | 0.28 / 0.27 / 0.32 | 0.31 |  |  | 5/8 | n/a | +0.140 |  | +1.0 / +1.1 | 0.383 |
| MYM | 60 | h8 * | +0.321 | -0.061 .. +0.703 | +0.0099 | 0.099 / 0.1 / 0.098 | 0.101 | 1 | 1 | 7/8 | n/a | +0.321 | False | +1.7 / +1.6 |  |
| MYM | 60 | h16 | +0.300 | -0.145 .. +0.744 | +0.0071 | 0.19 / 0.19 / 0.17 | 0.169 |  |  | 6/8 | n/a | +0.300 |  | +1.3 / +1.3 |  |
| MYM | 60 | eod | +0.296 | -0.149 .. +0.742 | +0.0067 | 0.19 / 0.2 / 0.18 | 0.175 |  |  | 6/8 | n/a | +0.296 |  | +1.3 / +1.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.005 | -0.007 .. +0.017 | +1.0% | +0.030 | 0.41 |  | 11/16 |
| MES | 5 | h2 | +0.016 | -0.001 .. +0.034 | +2.3% | +0.032 | 0.072 |  | 8/16 |
| MES | 5 | h4 | +0.030 | +0.005 .. +0.056 | +3.0% | +0.053 | 0.049 |  | 10/16 |
| MES | 5 | h8 * | +0.057 | +0.021 .. +0.093 | +4.0% | +0.087 | 0.0033 | 0.515 | 12/16 |
| MES | 5 | h16 | +0.048 | -0.009 .. +0.106 | +2.3% | +0.085 | 0.1 |  | 9/16 |
| MES | 5 | eod | +0.026 | -0.294 .. +0.347 | +0.3% | +0.220 | 0.87 |  | 8/16 |
| MES | 15 | h1 * | +0.050 | +0.017 .. +0.084 | +9.8% | +0.080 | 0.0033 | 0.504 | 11/16 |
| MES | 15 | h2 | +0.069 | +0.016 .. +0.122 | +9.5% | +0.106 | 0.011 |  | 13/16 |
| MES | 15 | h4 | +0.096 | +0.032 .. +0.160 | +9.1% | +0.124 | 0.0064 |  | 11/16 |
| MES | 15 | h8 | +0.076 | -0.003 .. +0.154 | +4.9% | +0.127 | 0.24 |  | 9/16 |
| MES | 15 | h16 | +0.020 | -0.093 .. +0.132 | +0.9% | +0.153 | 0.88 |  | 11/16 |
| MES | 15 | eod | -0.010 | -0.305 .. +0.284 | -0.2% | +0.146 | 0.97 |  | 7/16 |
| MES | 60 | h1 | +0.088 | +0.011 .. +0.165 | +17.1% | +0.117 | 0.027 |  | 10/16 |
| MES | 60 | h2 * | +0.183 | +0.073 .. +0.293 | +24.8% | +0.211 | 0.0011 | 0.184 | 13/16 |
| MES | 60 | h4 | +0.194 | +0.037 .. +0.351 | +18.4% | +0.291 | 0.016 |  | 12/16 |
| MES | 60 | h8 | +0.220 | +0.035 .. +0.405 | +14.6% | +0.353 | 0.021 |  | 11/16 |
| MES | 60 | h16 | +0.211 | +0.006 .. +0.417 | +10.3% | +0.408 | 0.047 |  | 11/16 |
| MES | 60 | eod | +0.200 | -0.007 .. +0.406 | +9.2% | +0.403 | 0.061 |  | 10/16 |
| MNQ | 5 | h1 | +0.020 | +0.005 .. +0.035 | +3.7% | +0.046 | 0.091 |  | 12/16 |
| MNQ | 5 | h2 * | +0.036 | +0.014 .. +0.059 | +4.7% | +0.082 | 0.016 | 1 | 12/16 |
| MNQ | 5 | h4 | +0.020 | -0.011 .. +0.052 | +1.8% | +0.081 | 0.62 |  | 9/16 |
| MNQ | 5 | h8 | +0.051 | +0.003 .. +0.100 | +3.2% | +0.113 | 0.095 |  | 11/16 |
| MNQ | 5 | h16 | +0.070 | -0.011 .. +0.151 | +2.9% | +0.138 | 0.092 |  | 11/16 |
| MNQ | 5 | eod | +0.562 | +0.011 .. +1.113 | +4.5% | +1.269 | 0.064 |  | 12/16 |
| MNQ | 15 | h1 | +0.037 | +0.007 .. +0.067 | +6.9% | +0.088 | 0.026 |  | 12/16 |
| MNQ | 15 | h2 * | +0.094 | +0.040 .. +0.147 | +12.1% | +0.151 | 0.00073 | 0.128 | 10/16 |
| MNQ | 15 | h4 | +0.100 | +0.023 .. +0.177 | +8.8% | +0.202 | 0.014 |  | 12/16 |
| MNQ | 15 | h8 | +0.093 | -0.008 .. +0.194 | +5.5% | +0.219 | 0.51 |  | 12/16 |
| MNQ | 15 | h16 | +0.117 | -0.031 .. +0.264 | +4.6% | +0.221 | 0.32 |  | 9/16 |
| MNQ | 15 | eod | +0.348 | -0.060 .. +0.756 | +5.5% | +0.437 | 0.34 |  | 11/16 |
| MNQ | 60 | h1 * | +0.096 | +0.026 .. +0.166 | +18.1% | +0.120 | 0.0091 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.095 | -0.010 .. +0.200 | +12.4% | +0.097 | 0.077 |  | 10/16 |
| MNQ | 60 | h4 | +0.109 | -0.036 .. +0.254 | +9.9% | +0.154 | 0.22 |  | 10/16 |
| MNQ | 60 | h8 | +0.005 | -0.170 .. +0.180 | +0.3% | +0.011 | 0.96 |  | 7/16 |
| MNQ | 60 | h16 | -0.042 | -0.229 .. +0.144 | -1.9% | -0.019 | 0.85 |  | 9/16 |
| MNQ | 60 | eod | -0.043 | -0.229 .. +0.143 | -1.9% | -0.020 | 0.84 |  | 9/16 |
| MYM | 5 | h1 * | +0.036 | +0.014 .. +0.058 | +6.7% | +0.055 | 0.076 | 1 | 6/8 |
| MYM | 5 | h2 | +0.028 | -0.004 .. +0.060 | +3.7% | +0.062 | 0.32 |  | 5/8 |
| MYM | 5 | h4 | +0.064 | +0.017 .. +0.111 | +5.8% | +0.089 | 0.33 |  | 5/8 |
| MYM | 5 | h8 | +0.077 | -0.001 .. +0.156 | +4.8% | +0.108 | 0.15 |  | 6/8 |
| MYM | 5 | h16 | +0.097 | -0.022 .. +0.217 | +4.2% | +0.157 | 0.38 |  | 6/8 |
| MYM | 5 | eod | +0.275 | -0.328 .. +0.879 | +2.3% | +0.505 | 0.5 |  | 5/8 |
| MYM | 15 | h1 * | +0.056 | +0.002 .. +0.111 | +10.6% | +0.076 | 0.41 | 1 | 5/8 |
| MYM | 15 | h2 | +0.078 | +0.004 .. +0.152 | +10.2% | +0.118 | 0.5 |  | 5/8 |
| MYM | 15 | h4 | +0.135 | +0.023 .. +0.247 | +12.1% | +0.146 | 0.7 |  | 6/8 |
| MYM | 15 | h8 | +0.077 | -0.070 .. +0.224 | +4.7% | +0.077 | 0.72 |  | 5/8 |
| MYM | 15 | h16 | -0.029 | -0.219 .. +0.160 | -1.2% | -0.034 | 0.81 |  | 3/8 |
| MYM | 15 | eod | -0.099 | -0.596 .. +0.398 | -1.6% | -0.054 | 0.7 |  | 5/8 |
| MYM | 60 | h1 | -0.014 | -0.099 .. +0.072 | -2.6% | +0.055 | 0.75 |  | 5/8 |
| MYM | 60 | h2 | +0.030 | -0.086 .. +0.146 | +3.9% | +0.068 | 0.68 |  | 5/8 |
| MYM | 60 | h4 | +0.011 | -0.156 .. +0.178 | +1.0% | +0.089 | 0.96 |  | 3/8 |
| MYM | 60 | h8 | +0.080 | -0.160 .. +0.320 | +5.2% | +0.093 | 0.65 |  | 5/8 |
| MYM | 60 | h16 * | +0.164 | -0.113 .. +0.441 | +7.7% | +0.130 | 0.33 | 1 | 6/8 |
| MYM | 60 | eod | +0.157 | -0.119 .. +0.432 | +7.0% | +0.125 | 0.34 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.56 pts | -0.62 .. +1.74 | 0.41 |
| MES | 15 | -1.12 pts | -3.41 .. +1.18 | 0.35 |
| MES | 60 | -1.26 pts | -6.09 .. +3.57 | 0.61 |
| MNQ | 5 | -0.45 pts | -1.52 .. +0.61 | 0.41 |
| MNQ | 15 | +1.80 pts | -0.55 .. +4.15 | 0.13 |
| MNQ | 60 | -5.08 pts | -10.24 .. +0.09 | 0.054 |
| MYM | 5 | +0.57 pts | -1.09 .. +2.24 | 0.55 |
| MYM | 15 | -2.03 pts | -5.20 .. +1.14 | 0.25 |
| MYM | 60 | +4.83 pts | -2.03 .. +11.69 | 0.17 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 7018 | +0.001 | 0.465 | +0.28 | -3.22 | -3.52 | -2.79 | -3.24 |
| MES | 5 | h2 | event | with signal | 7018 | +0.010 | 0.465 | +0.37 | -3.13 | -3.48 | -2.60 | -3.13 |
| MES | 5 | h4 | event | with signal | 7018 | -0.008 | 0.465 | +0.24 | -3.26 | -3.56 | -2.82 | -3.22 |
| MES | 5 | h8 | event | against signal | 7018 | +0.047 | 0.465 | +0.27 | -3.23 | -3.38 | -3.00 | -3.35 |
| MES | 5 | h16 | event | against signal | 7018 | +0.063 | 0.465 | +0.38 | -3.12 | -3.45 | -2.63 | -3.37 |
| MES | 5 | eod | event | against signal | 7018 | +0.857 | 0.465 | +4.98 | +1.48 | -0.78 | +4.88 | -1.65 |
| MES | 15 | h1 | event | against signal | 1827 | +0.043 | 0.234 | +1.35 | -2.15 | -3.13 | -1.00 | -2.19 |
| MES | 15 | h2 | event | with signal | 1827 | -0.008 | 0.234 | -0.58 | -4.08 | -3.75 | -4.48 | -4.00 |
| MES | 15 | h4 | event | against signal | 1827 | +0.040 | 0.234 | +1.14 | -2.36 | -2.79 | -1.84 | -2.54 |
| MES | 15 | h8 | event | against signal | 1827 | +0.113 | 0.234 | +2.66 | -0.84 | -2.60 | +1.25 | -1.26 |
| MES | 15 | h16 | event | against signal | 1827 | +0.232 | 0.234 | +4.86 | +1.36 | -1.40 | +4.63 | +0.46 |
| MES | 15 | eod | event | against signal | 1827 | +0.778 | 0.234 | +9.62 | +6.12 | +2.72 | +10.16 | +3.90 |
| MES | 60 | h1 | event | with signal | 377 | +0.022 | 0.111 | -0.27 | -3.77 | -2.33 | -5.51 | -3.51 |
| MES | 60 | h2 | event | with signal | 377 | -0.011 | 0.111 | +0.03 | -3.47 | -4.75 | -1.94 | -2.81 |
| MES | 60 | h4 | event | against signal | 377 | +0.086 | 0.111 | +1.53 | -1.97 | -0.32 | -3.96 | -3.26 |
| MES | 60 | h8 | event | with signal | 377 | -0.091 | 0.111 | -4.83 | -8.33 | -6.04 | -11.08 | -6.05 |
| MES | 60 | h16 | event | with signal | 377 | -0.022 | 0.111 | -5.94 | -9.44 | -6.33 | -13.19 | -6.44 |
| MES | 60 | eod | event | with signal | 377 | -0.030 | 0.111 | -5.98 | -9.48 | -6.63 | -12.92 | -6.56 |
| MNQ | 5 | h1 | event | against signal | 6965 | +0.017 | 0.218 | -0.06 | -2.06 | -1.91 | -2.33 | -2.07 |
| MNQ | 5 | h2 | event | against signal | 6965 | +0.033 | 0.218 | -0.12 | -2.12 | -1.96 | -2.38 | -2.16 |
| MNQ | 5 | h4 | event | against signal | 6965 | +0.027 | 0.218 | -0.02 | -2.02 | -2.03 | -2.00 | -2.10 |
| MNQ | 5 | h8 | event | against signal | 6965 | +0.078 | 0.218 | +0.72 | -1.28 | -1.90 | -0.20 | -1.46 |
| MNQ | 5 | h16 | event | against signal | 6965 | +0.146 | 0.218 | +0.58 | -1.42 | -1.68 | -0.97 | -1.78 |
| MNQ | 5 | eod | event | against signal | 6965 | +1.234 | 0.218 | +4.13 | +2.13 | +1.59 | +3.07 | -1.78 |
| MNQ | 15 | h1 | event | with signal | 1811 | +0.010 | 0.105 | +0.29 | -1.71 | -2.22 | -1.04 | -1.62 |
| MNQ | 15 | h2 | event | with signal | 1811 | +0.067 | 0.105 | +1.96 | -0.04 | -1.67 | +2.15 | +0.08 |
| MNQ | 15 | h4 | event | with signal | 1811 | +0.051 | 0.105 | +2.75 | +0.75 | -2.07 | +4.54 | +1.02 |
| MNQ | 15 | h8 | event | with signal | 1811 | +0.053 | 0.105 | +2.07 | +0.07 | -1.72 | +2.48 | +0.70 |
| MNQ | 15 | h16 | event | with signal | 1811 | -0.036 | 0.105 | -0.77 | -2.77 | -3.31 | -2.05 | -1.94 |
| MNQ | 15 | eod | event | against signal | 1811 | +0.853 | 0.105 | +7.83 | +5.83 | +3.19 | +9.39 | +3.44 |
| MNQ | 60 | h1 | event | against signal | 365 | +0.112 | 0.047 | +2.94 | +0.94 | +0.13 | +2.20 | +0.68 |
| MNQ | 60 | h2 | event | against signal | 365 | +0.172 | 0.047 | -0.48 | -2.48 | +2.05 | -9.58 | -2.98 |
| MNQ | 60 | h4 | event | against signal | 365 | +0.278 | 0.047 | +4.20 | +2.20 | +2.78 | +1.27 | +1.02 |
| MNQ | 60 | h8 | event | against signal | 365 | +0.564 | 0.047 | +12.23 | +10.23 | +7.67 | +14.26 | +8.13 |
| MNQ | 60 | h16 | event | against signal | 365 | +0.596 | 0.047 | +14.91 | +12.91 | +8.20 | +20.32 | +10.11 |
| MNQ | 60 | eod | event | against signal | 365 | +0.605 | 0.047 | +15.04 | +13.04 | +8.40 | +20.32 | +10.35 |
| MYM | 5 | h1 | event | with signal | 3108 | +0.013 | 0.217 | +0.34 | -1.66 | +nan | -1.66 | -1.68 |
| MYM | 5 | h2 | event | with signal | 3108 | +0.022 | 0.217 | +0.48 | -1.52 | +nan | -1.52 | -1.53 |
| MYM | 5 | h4 | event | with signal | 3108 | +0.017 | 0.217 | +0.55 | -1.45 | +nan | -1.45 | -1.46 |
| MYM | 5 | h8 | event | against signal | 3108 | +0.006 | 0.217 | -0.02 | -2.02 | +nan | -2.02 | -2.09 |
| MYM | 5 | h16 | event | against signal | 3108 | +0.042 | 0.217 | +0.55 | -1.45 | +nan | -1.45 | -1.67 |
| MYM | 5 | eod | event | against signal | 3108 | +0.713 | 0.217 | +7.93 | +5.93 | +nan | +5.93 | +3.60 |
| MYM | 15 | h1 | event | against signal | 910 | +0.029 | 0.122 | -0.08 | -2.08 | +nan | -2.08 | -2.10 |
| MYM | 15 | h2 | event | against signal | 910 | +0.011 | 0.122 | -0.46 | -2.46 | +nan | -2.46 | -2.45 |
| MYM | 15 | h4 | event | with signal | 910 | +0.013 | 0.122 | +1.18 | -0.82 | +nan | -0.82 | -0.73 |
| MYM | 15 | h8 | event | with signal | 910 | +0.003 | 0.122 | +1.12 | -0.88 | +nan | -0.88 | -0.50 |
| MYM | 15 | h16 | event | against signal | 910 | +0.043 | 0.122 | +1.11 | -0.89 | +nan | -0.89 | -0.90 |
| MYM | 15 | eod | event | with signal | 910 | -0.112 | 0.122 | -5.00 | -7.00 | +nan | -7.00 | -5.53 |
| MYM | 60 | h1 | event | with signal | 196 | +0.010 | 0.052 | -0.94 | -2.94 | +nan | -2.94 | -2.69 |
| MYM | 60 | h2 | event | with signal | 196 | +0.053 | 0.052 | +1.46 | -0.54 | +nan | -0.54 | -0.21 |
| MYM | 60 | h4 | event | with signal | 196 | +0.118 | 0.052 | +3.38 | +1.38 | +nan | +1.38 | +2.12 |
| MYM | 60 | h8 | event | with signal | 196 | +0.273 | 0.052 | +10.91 | +8.91 | +nan | +8.91 | +10.62 |
| MYM | 60 | h16 | event | with signal | 196 | +0.213 | 0.052 | +3.94 | +1.94 | +nan | +1.94 | +5.32 |
| MYM | 60 | eod | event | with signal | 196 | +0.212 | 0.052 | +3.90 | +1.90 | +nan | +1.90 | +5.24 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +0.694 | +0.768 | +0.564 | +0.265 | -0.064 | +0.000 | -0.076 | -0.064 | -0.075 | -0.101 | -0.097 |
| MES | 15 | +0.772 | +0.802 | +0.665 | +0.326 | -0.020 | +0.000 | -0.077 | -0.035 | -0.058 | -0.107 | -0.216 |
| MES | 60 | +0.899 | +0.697 | +0.577 | +0.296 | +0.012 | +0.000 | +0.024 | +0.003 | -0.079 | -0.243 | -0.278 |
| MNQ | 5 | +0.895 | +0.969 | +0.759 | +0.385 | +0.007 | +0.000 | -0.053 | -0.064 | -0.046 | -0.080 | -0.111 |
| MNQ | 15 | +0.810 | +0.849 | +0.711 | +0.357 | +0.021 | +0.000 | +0.007 | +0.070 | +0.060 | +0.100 | +0.060 |
| MNQ | 60 | +1.071 | +0.790 | +0.621 | +0.347 | -0.025 | +0.000 | -0.100 | -0.157 | -0.253 | -0.543 | +1.258 |
| MYM | 5 | +0.881 | +0.940 | +0.734 | +0.375 | +0.019 | +0.000 | -0.006 | +0.002 | -0.003 | -0.023 | -0.053 |
| MYM | 15 | +0.910 | +0.881 | +0.770 | +0.433 | +0.030 | +0.000 | -0.043 | -0.027 | -0.012 | -0.002 | -0.117 |
| MYM | 60 | +0.740 | +0.728 | +0.591 | +0.426 | -0.003 | +0.000 | +0.016 | +0.075 | +0.174 | +0.596 | -1.374 |

## Calibration

- MES 5-min: 1036271 bars, 7018 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 1827 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 377 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 6965 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 1811 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 365 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 3108 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 910 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 34751 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
