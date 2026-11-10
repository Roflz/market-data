# Impact card: pat_dragonfly_doji

candle pattern dragonfly_doji in its textbook direction: doji AND upper shadow <= 0.1 x range AND lower shadow >= 0.6 x range -> bullish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.023 R20 over the next 8 bars (40 min), p=0.46; we would catch an effect of 0.026 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.016 R20, CONFIRMED, q=0.0262, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.51 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.302 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.026 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.057 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.014).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.74 at recent bar sizes, 90% range up to $2.23); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.035 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.118 R20 or more 80% of the time).
- MES 60-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.053 R20, possible, q=0.212, 15 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.06 at recent bar sizes, 90% range up to $6.82); about 7.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.056 R20 over the next 8 bars (40 min), p=0.09; we would catch an effect of 0.036 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 7% LESS after the event than after matched bars over the next 16 bars (80 min) (-0.175 R20, CONFIRMED, q=5.28e-07, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.35 at recent bar sizes, 90% range up to $2.24); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.637 R20 over the rest of the session (to 16:45), p=0.061; we would catch an effect of 0.068 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 14% LESS after the event than after matched bars over the rest of the session (to 16:45) (-0.899 R20, CONFIRMED, q=1.9e-05, 15 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $29.45 at recent bar sizes, 90% range up to $3.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.024 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.113 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.46).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.29 at recent bar sizes, 90% range up to $17.52); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: POSSIBLE direction effect +0.145 average bars (~$1.59 per micro at 2018-25 bar sizes) over the next 8 bars (40 min) (in the signal's direction), not confirmed (q=0.0278, replicated in the other half=False, 8 of 8 years); best leg (event, with signal) grosses $-0.02 and nets $-2.02 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 5-min size: the market moves 8% LESS after the event than after matched bars over the next 16 bars (80 min) (-0.178 R20, possible, q=0.0749, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.59 at recent bar sizes, 90% range up to $2.20); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.047 R20 over the next 1 bar (15 min), p=0.071; we would catch an effect of 0.104 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.098).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.95 at recent bar sizes, 90% range up to $3.59); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.098 R20 over the next 4 bars (4 h), p=0.57; we would catch an effect of 0.174 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.35 at recent bar sizes, 90% range up to $13.53); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.000 | -0.008 .. +0.007 | -0.0001 | 0.94 / 0.94 / 0.97 | 0.973 |  |  | 8/16 | +0.002 | -0.002 |  | -0.1 / -0.1 |  |
| MES | 5 | h2 | -0.000 | -0.011 .. +0.010 | -0.0001 | 0.95 / 0.95 / 0.98 | 0.986 |  |  | 9/16 | +0.001 | -0.002 |  | -0.1 / -0.1 |  |
| MES | 5 | h4 | +0.002 | -0.013 .. +0.018 | +0.0003 | 0.76 / 0.75 / 0.74 | 0.731 |  |  | 8/16 | +0.015 | -0.010 |  | +0.3 / +0.3 | 0.026 |
| MES | 5 | h8 * | +0.023 | -0.002 .. +0.049 | +0.0019 | 0.073 / 0.077 / 0.066 | 0.069 | 1 | 1 | 13/16 | +0.043 | +0.003 | False | +2.1 / +1.8 |  |
| MES | 5 | h16 | +0.038 | -0.007 .. +0.083 | +0.0022 | 0.094 / 0.089 / 0.058 | 0.0604 |  |  | 12/16 | +0.071 | +0.005 |  | +2.4 / +1.7 |  |
| MES | 5 | eod | +0.254 | -0.403 .. +0.911 | +0.0030 | 0.45 / 0.48 / 0.21 | 0.212 |  |  | 10/16 | +0.209 | +0.299 |  | +2.4 / +0.8 |  |
| MES | 15 | h1 | -0.007 | -0.024 .. +0.009 | -0.0011 | 0.39 / 0.41 / 0.46 | 0.462 |  |  | 8/16 | -0.017 | +0.002 |  | -0.8 / -0.9 |  |
| MES | 15 | h2 | +0.005 | -0.021 .. +0.031 | +0.0005 | 0.71 / 0.72 / 0.73 | 0.719 |  |  | 9/16 | -0.019 | +0.028 |  | +0.4 / +0.4 |  |
| MES | 15 | h4 | +0.016 | -0.025 .. +0.056 | +0.0010 | 0.44 / 0.45 / 0.46 | 0.437 |  |  | 10/16 | -0.016 | +0.047 |  | +0.8 / +0.8 | 0.057 |
| MES | 15 | h8 * | +0.026 | -0.033 .. +0.086 | +0.0012 | 0.39 / 0.41 / 0.41 | 0.414 | 1 | 1 | 10/16 | +0.008 | +0.044 | False | +0.9 / +0.9 |  |
| MES | 15 | h16 | -0.037 | -0.145 .. +0.070 | -0.0012 | 0.5 / 0.5 / 0.45 | 0.442 |  |  | 9/16 | -0.076 | +0.002 |  | -0.8 / -0.7 |  |
| MES | 15 | eod | +0.190 | -0.236 .. +0.615 | +0.0024 | 0.38 / 0.4 / 0.26 | 0.256 |  |  | 11/16 | +0.222 | +0.158 |  | +1.3 / +0.9 |  |
| MES | 60 | h1 | +0.020 | -0.014 .. +0.053 | +0.0026 | 0.25 / 0.24 / 0.33 | 0.327 |  |  | 10/16 | +0.032 | +0.007 |  | +1.2 / +1.2 |  |
| MES | 60 | h2 * | +0.035 | -0.016 .. +0.086 | +0.0033 | 0.18 / 0.17 / 0.24 | 0.236 | 1 | 1 | 10/16 | +0.068 | +0.003 | False | +1.4 / +1.4 |  |
| MES | 60 | h4 | -0.016 | -0.093 .. +0.060 | -0.0011 | 0.67 / 0.67 / 0.71 | 0.704 |  |  | 8/16 | +0.032 | -0.065 |  | -0.4 / -0.4 | 0.118 |
| MES | 60 | h8 | +0.009 | -0.119 .. +0.136 | +0.0004 | 0.89 / 0.89 / 0.89 | 0.893 |  |  | 9/16 | +0.032 | -0.015 |  | +0.1 / +0.1 |  |
| MES | 60 | h16 | +0.014 | -0.197 .. +0.225 | +0.0005 | 0.9 / 0.9 / 0.88 | 0.879 |  |  | 8/16 | +0.166 | -0.138 |  | +0.1 / +0.1 |  |
| MES | 60 | eod | -0.029 | -0.267 .. +0.209 | -0.0010 | 0.81 / 0.81 / 0.78 | 0.789 |  |  | 8/16 | +0.027 | -0.085 |  | -0.3 / -0.2 |  |
| MNQ | 5 | h1 | -0.005 | -0.015 .. +0.005 | -0.0008 | 0.31 / 0.32 / 0.4 | 0.383 |  |  | 10/16 | -0.007 | -0.003 |  | -0.9 / -1.0 |  |
| MNQ | 5 | h2 | +0.002 | -0.017 .. +0.021 | +0.0002 | 0.82 / 0.82 / 0.82 | 0.798 |  |  | 9/16 | +0.013 | -0.008 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h4 | +0.017 | -0.013 .. +0.047 | +0.0010 | 0.26 / 0.25 / 0.25 | 0.201 |  |  | 10/16 | +0.049 | -0.014 |  | +1.3 / +1.1 | 0.036 |
| MNQ | 5 | h8 * | +0.056 | +0.011 .. +0.101 | +0.0023 | 0.015 / 0.013 / 0.014 | 0.0237 | 1 | 0.959 | 11/16 | +0.134 | -0.021 | False | +2.8 / +2.4 |  |
| MNQ | 5 | h16 | +0.085 | +0.014 .. +0.157 | +0.0025 | 0.019 / 0.02 / 0.013 | 0.0141 |  |  | 11/16 | +0.175 | -0.003 |  | +2.8 / +2.4 |  |
| MNQ | 5 | eod | +0.418 | -0.576 .. +1.413 | +0.0025 | 0.41 / 0.43 / 0.11 | 0.102 |  |  | 11/16 | +0.675 | +0.165 |  | +2.0 / +0.8 |  |
| MNQ | 15 | h1 | -0.008 | -0.029 .. +0.012 | -0.0009 | 0.42 / 0.42 / 0.55 | 0.463 |  |  | 11/16 | -0.013 | -0.004 |  | -0.8 / -0.8 |  |
| MNQ | 15 | h2 | +0.005 | -0.026 .. +0.035 | +0.0003 | 0.76 / 0.76 / 0.84 | 0.773 |  |  | 9/16 | +0.012 | -0.002 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h4 | +0.005 | -0.046 .. +0.055 | +0.0002 | 0.86 / 0.85 / 0.9 | 0.85 |  |  | 8/16 | +0.003 | +0.006 |  | +0.2 / +0.2 | 0.068 |
| MNQ | 15 | h8 | -0.014 | -0.088 .. +0.060 | -0.0004 | 0.71 / 0.71 / 0.78 | 0.729 |  |  | 8/16 | -0.008 | -0.020 |  | -0.4 / -0.4 |  |
| MNQ | 15 | h16 | +0.045 | -0.076 .. +0.166 | +0.0010 | 0.47 / 0.46 / 0.49 | 0.479 |  |  | 9/16 | +0.082 | +0.007 |  | +0.8 / +0.7 |  |
| MNQ | 15 | eod * | +0.637 | +0.161 .. +1.114 | +0.0052 | 0.0087 / 0.01 / 0.0037 | 0.00677 | 1 | 0.854 | 13/16 | +1.270 | +0.009 | False | +3.9 / +2.6 |  |
| MNQ | 60 | h1 * | -0.024 | -0.058 .. +0.010 | -0.0032 | 0.16 / 0.16 / 0.21 | 0.211 | 1 | 1 | 11/16 | -0.008 | -0.041 | False | -1.4 / -1.4 |  |
| MNQ | 60 | h2 | -0.006 | -0.063 .. +0.052 | -0.0005 | 0.85 / 0.85 / 0.84 | 0.841 |  |  | 10/16 | +0.012 | -0.023 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h4 | +0.018 | -0.068 .. +0.104 | +0.0012 | 0.68 / 0.68 / 0.66 | 0.654 |  |  | 8/16 | -0.018 | +0.055 |  | +0.4 / +0.4 | 0.113 |
| MNQ | 60 | h8 | +0.080 | -0.046 .. +0.205 | +0.0038 | 0.21 / 0.21 / 0.17 | 0.171 |  |  | 9/16 | +0.051 | +0.108 |  | +1.3 / +1.2 |  |
| MNQ | 60 | h16 | +0.104 | -0.113 .. +0.321 | +0.0038 | 0.35 / 0.34 / 0.28 | 0.289 |  |  | 9/16 | +0.159 | +0.049 |  | +1.1 / +0.9 |  |
| MNQ | 60 | eod | +0.015 | -0.225 .. +0.255 | +0.0005 | 0.9 / 0.9 / 0.89 | 0.885 |  |  | 8/16 | +0.044 | -0.014 |  | +0.1 / +0.1 |  |
| MYM | 5 | h1 | +0.012 | -0.006 .. +0.029 | +0.0013 | 0.19 / 0.18 / 0.31 | 0.269 |  |  | 6/8 | n/a | +0.012 |  | +1.3 / +1.3 |  |
| MYM | 5 | h2 | +0.022 | -0.004 .. +0.048 | +0.0014 | 0.094 / 0.096 / 0.3 | 0.184 |  |  | 7/8 | n/a | +0.022 |  | +1.7 / +1.7 |  |
| MYM | 5 | h4 | +0.064 | +0.026 .. +0.102 | +0.0026 | 0.00087 / 0.0011 / 0.044 | 0.0506 |  |  | 8/8 | n/a | +0.064 |  | +3.4 / +3.3 | 0.059 |
| MYM | 5 | h8 * | +0.145 | +0.078 .. +0.212 | +0.0042 | 2.1e-05 / 1.9e-05 / 0.0018 | 0.0142 | 0.0278 | 0.014 | 8/8 | n/a | +0.145 | False | +4.6 / +4.3 |  |
| MYM | 5 | h16 | +0.139 | +0.030 .. +0.248 | +0.0031 | 0.012 / 0.01 / 0.023 | 0.029 |  |  | 6/8 | n/a | +0.139 |  | +2.9 / +2.5 |  |
| MYM | 5 | eod | +1.023 | +0.000 .. +2.045 | +0.0051 | 0.05 / 0.05 / 0.0013 | 0.00105 |  |  | 6/8 | n/a | +1.023 |  | +3.6 / +2.0 |  |
| MYM | 15 | h1 * | -0.047 | -0.074 .. -0.019 | -0.0048 | 0.001 / 0.0016 / 0.01 | 0.0153 | 1 | 0.253 | 7/8 | n/a | -0.047 | False | -3.2 / -3.3 |  |
| MYM | 15 | h2 | -0.012 | -0.056 .. +0.031 | -0.0007 | 0.58 / 0.58 / 0.7 | 0.614 |  |  | 5/8 | n/a | -0.012 |  | -0.5 / -0.6 |  |
| MYM | 15 | h4 | +0.007 | -0.061 .. +0.076 | +0.0003 | 0.84 / 0.83 / 0.91 | 0.861 |  |  | 5/8 | n/a | +0.007 |  | +0.2 / +0.2 | 0.104 |
| MYM | 15 | h8 | +0.085 | -0.023 .. +0.193 | +0.0023 | 0.12 / 0.11 / 0.34 | 0.207 |  |  | 7/8 | n/a | +0.085 |  | +1.6 / +1.5 |  |
| MYM | 15 | h16 | +0.151 | -0.038 .. +0.339 | +0.0029 | 0.12 / 0.1 / 0.18 | 0.152 |  |  | 7/8 | n/a | +0.151 |  | +1.8 / +1.6 |  |
| MYM | 15 | eod | +0.321 | -0.209 .. +0.851 | +0.0026 | 0.24 / 0.23 / 0.26 | 0.238 |  |  | 5/8 | n/a | +0.321 |  | +1.5 / +1.2 |  |
| MYM | 60 | h1 | -0.001 | -0.053 .. +0.051 | -0.0001 | 0.97 / 0.97 / 0.98 | 0.982 |  |  | 4/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MYM | 60 | h2 | -0.040 | -0.109 .. +0.030 | -0.0036 | 0.26 / 0.29 / 0.35 | 0.346 |  |  | 5/8 | n/a | -0.040 |  | -1.1 / -1.1 |  |
| MYM | 60 | h4 * | -0.098 | -0.211 .. +0.014 | -0.0064 | 0.087 / 0.095 / 0.11 | 0.11 | 1 | 1 | 6/8 | n/a | -0.098 | False | -1.7 / -1.7 | 0.174 |
| MYM | 60 | h8 | -0.141 | -0.326 .. +0.044 | -0.0067 | 0.13 / 0.16 / 0.11 | 0.119 |  |  | 5/8 | n/a | -0.141 |  | -1.5 / -1.5 |  |
| MYM | 60 | h16 | -0.122 | -0.415 .. +0.171 | -0.0044 | 0.42 / 0.44 / 0.38 | 0.398 |  |  | 5/8 | n/a | -0.122 |  | -0.8 / -0.8 |  |
| MYM | 60 | eod | -0.085 | -0.390 .. +0.221 | -0.0029 | 0.59 / 0.61 / 0.57 | 0.58 |  |  | 5/8 | n/a | -0.085 |  | -0.6 / -0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | -0.016 | -0.022 .. -0.009 | -3.1% | -0.039 | 0.00013 | 0.0262 | 12/16 |
| MES | 5 | h2 | -0.022 | -0.033 .. -0.012 | -3.2% | -0.059 | 0.00063 |  | 13/16 |
| MES | 5 | h4 | -0.034 | -0.049 .. -0.019 | -3.4% | -0.084 | 0.00035 |  | 13/16 |
| MES | 5 | h8 | -0.048 | -0.071 .. -0.024 | -3.3% | -0.124 | 0.00059 |  | 10/16 |
| MES | 5 | h16 | -0.071 | -0.107 .. -0.035 | -3.4% | -0.198 | 0.00026 |  | 13/16 |
| MES | 5 | eod | -0.541 | -0.947 .. -0.134 | -5.4% | -0.734 | 0.17 |  | 10/16 |
| MES | 15 | h1 | -0.008 | -0.019 .. +0.003 | -1.6% | -0.037 | 0.39 |  | 9/16 |
| MES | 15 | h2 | -0.022 | -0.041 .. -0.003 | -3.1% | -0.062 | 0.077 |  | 11/16 |
| MES | 15 | h4 | -0.042 | -0.072 .. -0.013 | -4.0% | -0.098 | 0.018 |  | 13/16 |
| MES | 15 | h8 | -0.071 | -0.113 .. -0.029 | -4.6% | -0.176 | 0.0093 |  | 11/16 |
| MES | 15 | h16 | -0.044 | -0.118 .. +0.030 | -1.9% | -0.248 | 0.27 |  | 9/16 |
| MES | 15 | eod * | -0.404 | -0.655 .. -0.152 | -7.4% | -0.503 | 0.0023 | 0.368 | 10/16 |
| MES | 60 | h1 * | -0.053 | -0.072 .. -0.034 | -10.4% | -0.084 | 0.0013 | 0.212 | 15/16 |
| MES | 60 | h2 | -0.048 | -0.084 .. -0.012 | -6.5% | -0.076 | 0.052 |  | 13/16 |
| MES | 60 | h4 | -0.047 | -0.106 .. +0.011 | -4.5% | -0.098 | 0.17 |  | 11/16 |
| MES | 60 | h8 | -0.035 | -0.108 .. +0.038 | -2.3% | -0.085 | 0.59 |  | 9/16 |
| MES | 60 | h16 | -0.062 | -0.194 .. +0.069 | -3.0% | -0.069 | 0.36 |  | 10/16 |
| MES | 60 | eod | -0.034 | -0.170 .. +0.102 | -1.6% | -0.069 | 0.64 |  | 10/16 |
| MNQ | 5 | h1 | -0.010 | -0.018 .. -0.002 | -1.9% | -0.036 | 0.018 |  | 9/16 |
| MNQ | 5 | h2 | -0.023 | -0.036 .. -0.010 | -3.0% | -0.054 | 0.00057 |  | 11/16 |
| MNQ | 5 | h4 | -0.053 | -0.074 .. -0.032 | -4.8% | -0.107 | 1.1e-05 |  | 13/16 |
| MNQ | 5 | h8 | -0.101 | -0.133 .. -0.069 | -6.2% | -0.223 | 8.8e-09 |  | 14/16 |
| MNQ | 5 | h16 * | -0.175 | -0.226 .. -0.124 | -7.3% | -0.436 | 1.8e-09 | 5.28e-07 | 16/16 |
| MNQ | 5 | eod | -0.586 | -1.170 .. -0.002 | -4.7% | -1.122 | 0.049 |  | 11/16 |
| MNQ | 15 | h1 | -0.041 | -0.056 .. -0.026 | -7.6% | -0.084 | 1.4e-05 |  | 13/16 |
| MNQ | 15 | h2 | -0.069 | -0.096 .. -0.042 | -8.9% | -0.136 | 8.7e-07 |  | 13/16 |
| MNQ | 15 | h4 | -0.117 | -0.163 .. -0.071 | -10.3% | -0.254 | 2.3e-06 |  | 11/16 |
| MNQ | 15 | h8 | -0.202 | -0.268 .. -0.137 | -12.1% | -0.466 | 1.4e-07 |  | 15/16 |
| MNQ | 15 | h16 | -0.226 | -0.314 .. -0.138 | -8.9% | -0.732 | 1.2e-05 |  | 15/16 |
| MNQ | 15 | eod * | -0.899 | -1.215 .. -0.583 | -14.1% | -1.267 | 7e-08 | 1.9e-05 | 15/16 |
| MNQ | 60 | h1 * | -0.031 | -0.055 .. -0.007 | -6.0% | -0.060 | 0.076 | 1 | 11/16 |
| MNQ | 60 | h2 | -0.018 | -0.057 .. +0.021 | -2.4% | -0.044 | 0.65 |  | 9/16 |
| MNQ | 60 | h4 | -0.027 | -0.086 .. +0.033 | -2.4% | -0.056 | 0.55 |  | 8/16 |
| MNQ | 60 | h8 | -0.005 | -0.086 .. +0.076 | -0.3% | -0.088 | 0.91 |  | 7/16 |
| MNQ | 60 | h16 | -0.033 | -0.168 .. +0.102 | -1.5% | -0.117 | 0.76 |  | 9/16 |
| MNQ | 60 | eod | -0.061 | -0.205 .. +0.084 | -2.6% | -0.159 | 0.47 |  | 9/16 |
| MYM | 5 | h1 | -0.026 | -0.038 .. -0.013 | -4.8% | -0.047 | 0.0028 |  | 8/8 |
| MYM | 5 | h2 | -0.055 | -0.076 .. -0.033 | -7.2% | -0.080 | 0.0028 |  | 8/8 |
| MYM | 5 | h4 | -0.108 | -0.141 .. -0.074 | -9.8% | -0.170 | 0.00056 |  | 8/8 |
| MYM | 5 | h8 | -0.124 | -0.184 .. -0.065 | -7.8% | -0.246 | 0.0028 |  | 8/8 |
| MYM | 5 | h16 * | -0.178 | -0.264 .. -0.092 | -7.6% | -0.439 | 0.00041 | 0.0749 | 8/8 |
| MYM | 5 | eod | -0.809 | -1.260 .. -0.357 | -6.9% | -1.398 | 0.0011 |  | 7/8 |
| MYM | 15 | h1 | -0.033 | -0.051 .. -0.014 | -6.2% | -0.070 | 0.025 |  | 8/8 |
| MYM | 15 | h2 | -0.044 | -0.074 .. -0.013 | -5.7% | -0.107 | 0.12 |  | 8/8 |
| MYM | 15 | h4 | -0.089 | -0.140 .. -0.039 | -8.0% | -0.162 | 0.26 |  | 7/8 |
| MYM | 15 | h8 | -0.102 | -0.178 .. -0.025 | -6.2% | -0.278 | 0.27 |  | 6/8 |
| MYM | 15 | h16 | -0.176 | -0.295 .. -0.058 | -7.2% | -0.508 | 0.1 |  | 7/8 |
| MYM | 15 | eod * | -0.561 | -0.890 .. -0.232 | -9.3% | -0.835 | 0.016 | 1 | 8/8 |
| MYM | 60 | h1 | -0.013 | -0.047 .. +0.022 | -2.4% | -0.074 | 0.88 |  | 4/8 |
| MYM | 60 | h2 * | -0.051 | -0.102 .. -0.000 | -6.8% | -0.123 | 0.22 | 1 | 4/8 |
| MYM | 60 | h4 | -0.063 | -0.144 .. +0.018 | -5.8% | -0.145 | 0.33 |  | 5/8 |
| MYM | 60 | h8 | +0.033 | -0.077 .. +0.142 | +2.1% | -0.105 | 0.57 |  | 5/8 |
| MYM | 60 | h16 | +0.058 | -0.134 .. +0.249 | +2.7% | -0.046 | 0.56 |  | 3/8 |
| MYM | 60 | eod | +0.012 | -0.185 .. +0.209 | +0.5% | -0.050 | 0.92 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -1.30 pts | -2.00 .. -0.61 | 0.00023 |
| MES | 15 | -0.01 pts | -1.47 .. +1.46 | 0.99 |
| MES | 60 | +1.43 pts | -1.96 .. +4.82 | 0.41 |
| MNQ | 5 | -0.41 pts | -1.14 .. +0.32 | 0.28 |
| MNQ | 15 | -0.21 pts | -1.76 .. +1.34 | 0.79 |
| MNQ | 60 | +1.22 pts | -1.83 .. +4.28 | 0.44 |
| MYM | 5 | -0.30 pts | -1.59 .. +1.00 | 0.73 |
| MYM | 15 | -1.09 pts | -3.33 .. +1.15 | 0.34 |
| MYM | 60 | -3.96 pts | -8.65 .. +0.74 | 0.1 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 28607 | -0.001 | 0.647 | -0.01 | -3.51 | -3.51 | -3.54 | -3.51 |
| MES | 5 | h2 | event | against signal | 28607 | -0.005 | 0.647 | +0.00 | -3.50 | -3.51 | -3.46 | -3.48 |
| MES | 5 | h4 | event | with signal | 28607 | +0.010 | 0.647 | -0.03 | -3.53 | -3.46 | -3.76 | -3.55 |
| MES | 5 | h8 | event | with signal | 28607 | +0.044 | 0.647 | +0.11 | -3.39 | -3.35 | -3.52 | -3.44 |
| MES | 5 | h16 | event | with signal | 28607 | +0.081 | 0.647 | +0.30 | -3.20 | -3.23 | -3.12 | -3.33 |
| MES | 5 | eod | event | with signal | 28607 | +0.975 | 0.647 | +3.29 | -0.21 | -0.49 | +0.71 | -2.08 |
| MES | 15 | h1 | event | against signal | 4135 | +0.001 | 0.231 | -0.04 | -3.54 | -3.47 | -3.66 | -3.51 |
| MES | 15 | h2 | event | with signal | 4135 | +0.016 | 0.231 | +0.45 | -3.05 | -3.55 | -2.16 | -3.09 |
| MES | 15 | h4 | event | with signal | 4135 | +0.039 | 0.231 | +0.53 | -2.97 | -3.44 | -2.16 | -3.06 |
| MES | 15 | h8 | event | with signal | 4135 | +0.058 | 0.231 | +0.54 | -2.96 | -3.12 | -2.68 | -3.03 |
| MES | 15 | h16 | event | against signal | 4135 | +0.001 | 0.231 | -0.25 | -3.75 | -3.78 | -3.68 | -3.79 |
| MES | 15 | eod | event | with signal | 4135 | +0.327 | 0.231 | +2.40 | -1.10 | -1.62 | -0.20 | -1.11 |
| MES | 60 | h1 | event | with signal | 858 | +0.025 | 0.086 | +1.30 | -2.20 | -2.38 | -2.04 | -2.25 |
| MES | 60 | h2 | event | with signal | 858 | +0.046 | 0.086 | +1.51 | -1.99 | -1.43 | -2.49 | -2.20 |
| MES | 60 | h4 | event | against signal | 858 | -0.007 | 0.086 | -0.76 | -4.26 | -5.18 | -3.44 | -3.69 |
| MES | 60 | h8 | event | with signal | 858 | +0.062 | 0.086 | +2.89 | -0.61 | -0.46 | -0.75 | -2.00 |
| MES | 60 | h16 | event | with signal | 858 | +0.125 | 0.086 | +2.23 | -1.27 | +4.31 | -6.25 | -4.24 |
| MES | 60 | eod | event | against signal | 858 | -0.110 | 0.086 | -3.09 | -6.59 | -8.77 | -4.65 | -2.51 |
| MNQ | 5 | h1 | event | against signal | 16339 | +0.000 | 0.231 | +0.05 | -1.95 | -1.99 | -1.83 | -1.93 |
| MNQ | 5 | h2 | event | with signal | 16339 | +0.005 | 0.231 | -0.05 | -2.05 | -1.99 | -2.23 | -2.06 |
| MNQ | 5 | h4 | event | with signal | 16339 | +0.015 | 0.231 | -0.18 | -2.18 | -1.94 | -2.86 | -2.16 |
| MNQ | 5 | h8 | event | with signal | 16339 | +0.056 | 0.231 | -0.09 | -2.09 | -1.74 | -3.05 | -2.06 |
| MNQ | 5 | h16 | event | with signal | 16339 | +0.107 | 0.231 | +0.26 | -1.74 | -1.60 | -2.12 | -1.78 |
| MNQ | 5 | eod | event | with signal | 16339 | +1.169 | 0.231 | +2.19 | +0.19 | +0.62 | -1.01 | -0.59 |
| MNQ | 15 | h1 | event | against signal | 3714 | -0.007 | 0.087 | +0.33 | -1.67 | -1.99 | -1.17 | -1.54 |
| MNQ | 15 | h2 | event | with signal | 3714 | +0.016 | 0.087 | -0.57 | -2.57 | -1.91 | -3.60 | -2.66 |
| MNQ | 15 | h4 | event | with signal | 3714 | +0.022 | 0.087 | -0.43 | -2.43 | -2.07 | -2.98 | -2.58 |
| MNQ | 15 | h8 | event | against signal | 3714 | -0.023 | 0.087 | +0.11 | -1.89 | -2.33 | -1.20 | -1.53 |
| MNQ | 15 | h16 | event | with signal | 3714 | +0.057 | 0.087 | +0.51 | -1.49 | -1.69 | -1.18 | -1.55 |
| MNQ | 15 | eod | event | with signal | 3714 | +0.646 | 0.087 | -0.16 | -2.16 | +1.61 | -8.05 | -1.44 |
| MNQ | 60 | h1 | event | against signal | 994 | +0.012 | 0.038 | +1.54 | -0.46 | -1.98 | +1.47 | -0.21 |
| MNQ | 60 | h2 | event | against signal | 994 | -0.015 | 0.038 | +1.00 | -1.00 | -2.52 | +0.92 | -0.57 |
| MNQ | 60 | h4 | event | with signal | 994 | +0.057 | 0.038 | +3.44 | +1.44 | -1.22 | +4.80 | +0.61 |
| MNQ | 60 | h8 | event | with signal | 994 | +0.150 | 0.038 | +8.73 | +6.73 | +1.53 | +13.31 | +5.22 |
| MNQ | 60 | h16 | event | with signal | 994 | +0.235 | 0.038 | +7.02 | +5.02 | +4.22 | +6.04 | +1.98 |
| MNQ | 60 | eod | event | with signal | 994 | +0.191 | 0.038 | +4.16 | +2.16 | +2.86 | +1.26 | -2.77 |
| MYM | 5 | h1 | event | with signal | 5458 | +0.006 | 0.182 | +0.11 | -1.89 | +nan | -1.89 | -1.86 |
| MYM | 5 | h2 | event | with signal | 5458 | +0.001 | 0.182 | -0.08 | -2.08 | +nan | -2.08 | -1.95 |
| MYM | 5 | h4 | event | with signal | 5458 | +0.003 | 0.182 | -0.11 | -2.11 | +nan | -2.11 | -1.77 |
| MYM | 5 | h8 | event | with signal | 5458 | +0.037 | 0.182 | -0.02 | -2.02 | +nan | -2.02 | -1.44 |
| MYM | 5 | h16 | event | with signal | 5458 | -0.000 | 0.182 | -0.02 | -2.02 | +nan | -2.02 | -1.32 |
| MYM | 5 | eod | event | with signal | 5458 | +0.658 | 0.182 | +2.03 | +0.03 | +nan | +0.03 | +2.37 |
| MYM | 15 | h1 | event | against signal | 1699 | +0.046 | 0.098 | +0.87 | -1.13 | +nan | -1.13 | -1.14 |
| MYM | 15 | h2 | event | against signal | 1699 | +0.022 | 0.098 | +0.34 | -1.66 | +nan | -1.66 | -1.81 |
| MYM | 15 | h4 | event | with signal | 1699 | -0.022 | 0.098 | -0.24 | -2.24 | +nan | -2.24 | -1.78 |
| MYM | 15 | h8 | event | with signal | 1699 | +0.019 | 0.098 | +0.09 | -1.91 | +nan | -1.91 | -0.92 |
| MYM | 15 | h16 | event | with signal | 1699 | -0.002 | 0.098 | +0.87 | -1.13 | +nan | -1.13 | +0.89 |
| MYM | 15 | eod | event | with signal | 1699 | +0.068 | 0.098 | +3.73 | +1.73 | +nan | +1.73 | +5.33 |
| MYM | 60 | h1 | event | against signal | 463 | +0.001 | 0.045 | -0.18 | -2.18 | +nan | -2.18 | -2.23 |
| MYM | 60 | h2 | event | against signal | 463 | +0.037 | 0.045 | +0.56 | -1.44 | +nan | -1.44 | -1.35 |
| MYM | 60 | h4 | event | against signal | 463 | +0.094 | 0.045 | +2.07 | +0.07 | +nan | +0.07 | +0.24 |
| MYM | 60 | h8 | event | against signal | 463 | +0.134 | 0.045 | +3.82 | +1.82 | +nan | +1.82 | +2.07 |
| MYM | 60 | h16 | event | against signal | 463 | +0.111 | 0.045 | +4.09 | +2.09 | +nan | +2.09 | +2.33 |
| MYM | 60 | eod | event | against signal | 463 | +0.058 | 0.045 | +1.88 | -0.12 | +nan | -0.12 | +0.95 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.079 | -0.117 | -0.129 | -0.118 | -0.087 | +0.000 | -0.101 | -0.100 | -0.102 | -0.081 | -0.070 |
| MES | 15 | -0.019 | -0.026 | -0.053 | -0.068 | -0.042 | +0.000 | -0.053 | -0.042 | -0.027 | -0.028 | -0.116 |
| MES | 60 | -0.072 | -0.077 | -0.053 | +0.009 | +0.007 | +0.000 | +0.007 | +0.020 | -0.052 | -0.021 | +0.023 |
| MNQ | 5 | +0.024 | +0.010 | -0.023 | -0.025 | -0.007 | +0.000 | -0.047 | -0.046 | -0.046 | -0.022 | -0.013 |
| MNQ | 15 | +0.005 | +0.038 | +0.029 | +0.012 | +0.004 | +0.000 | -0.016 | -0.013 | -0.023 | -0.044 | -0.053 |
| MNQ | 60 | -0.073 | -0.043 | -0.001 | +0.023 | +0.020 | +0.000 | -0.027 | -0.012 | +0.008 | +0.110 | +0.077 |
| MYM | 5 | +0.001 | -0.051 | -0.065 | -0.039 | -0.000 | +0.000 | -0.011 | -0.015 | -0.013 | +0.026 | -0.005 |
| MYM | 15 | +0.065 | +0.033 | +0.029 | +0.005 | +0.003 | +0.000 | -0.052 | -0.031 | -0.028 | +0.025 | +0.001 |
| MYM | 60 | -0.331 | -0.132 | -0.053 | +0.005 | +0.016 | +0.000 | -0.007 | -0.050 | -0.126 | -0.193 | -0.168 |

## Calibration

- MES 5-min: 1036271 bars, 28607 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 4135 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 858 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 16339 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 3714 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 994 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 5458 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 1699 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 463 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 10% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 48346 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
