# Impact card: pat_five_lower_lows_higher_highs

candle pattern five_lower_lows_higher_highs in its textbook direction: 5 consecutive lower lows -> bullish (reversal); 5 higher highs -> bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.057 R20 over the next 8 bars (40 min), p=0.018; we would catch an effect of 0.035 R20 or more 80% of the time).
- MES 5-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.027 R20, CONFIRMED, q=9.58e-11, 15 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.82 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.169 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.020 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.057 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.015).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $2.26 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.109 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.011 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.120 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.084).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.58 at recent bar sizes, 90% range up to $7.16); about 19.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: POSSIBLE direction effect -0.055 average bars (~$1.68 per micro at 2018-25 bar sizes) over the next 4 bars (20 min) (in the signal's direction), not confirmed (q=0.00782, replicated in the other half=False, 14 of 16 years); best leg (event, against signal) grosses $+1.18 and nets $-0.82 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.017 R20, CONFIRMED, q=5.26e-05, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.68 at recent bar sizes, 90% range up to $3.58); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.045 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.74).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.22 at recent bar sizes, 90% range up to $4.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.028 R20 over the next 1 bar (1 h), p=0.37; we would catch an effect of 0.125 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.55 at recent bar sizes, 90% range up to $13.48); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.273 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.046 R20 or more 80% of the time).
- MYM 5-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.026 R20, CONFIRMED, q=5.78e-05, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.85 at recent bar sizes, 90% range up to $0.70); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.118 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.011).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.70 at recent bar sizes, 90% range up to $1.85); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.075 R20 over the next 8 bars (8 h), p=1; we would catch an effect of 0.166 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.92).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.13 at recent bar sizes, 90% range up to $9.19); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.005 | -0.004 .. +0.014 | +0.0011 | 0.29 / 0.28 / 0.29 | 0.282 |  |  | 12/16 | +0.006 | +0.004 |  | +1.1 / +1.1 |  |
| MES | 5 | h2 | -0.007 | -0.022 .. +0.008 | -0.0011 | 0.37 / 0.36 / 0.36 | 0.367 |  |  | 8/16 | -0.004 | -0.010 |  | -1.1 / -0.9 |  |
| MES | 5 | h4 | -0.035 | -0.061 .. -0.009 | -0.0039 | 0.0074 / 0.005 / 0.006 | 0.00625 |  |  | 11/16 | -0.014 | -0.056 |  | -3.9 / -2.7 | 0.035 |
| MES | 5 | h8 * | -0.057 | -0.094 .. -0.019 | -0.0043 | 0.0029 / 0.003 / 0.0039 | 0.00417 | 0.471 | 0.55 | 12/16 | -0.039 | -0.075 | False | -4.4 / -3.0 |  |
| MES | 5 | h16 | -0.074 | -0.127 .. -0.021 | -0.0039 | 0.0062 / 0.0069 / 0.011 | 0.013 |  |  | 11/16 | -0.007 | -0.141 |  | -4.0 / -2.7 |  |
| MES | 5 | eod | +0.069 | -0.180 .. +0.319 | +0.0007 | 0.59 / 0.58 / 0.56 | 0.553 |  |  | 9/16 | -0.024 | +0.162 |  | +0.9 / +0.5 |  |
| MES | 15 | h1 | +0.003 | -0.011 .. +0.017 | +0.0007 | 0.68 / 0.68 / 0.68 | 0.671 |  |  | 8/16 | +0.012 | -0.006 |  | +0.4 / +0.4 |  |
| MES | 15 | h2 | -0.008 | -0.031 .. +0.015 | -0.0014 | 0.51 / 0.51 / 0.55 | 0.545 |  |  | 8/16 | +0.004 | -0.019 |  | -0.8 / -0.7 |  |
| MES | 15 | h4 | -0.010 | -0.047 .. +0.027 | -0.0012 | 0.6 / 0.61 / 0.65 | 0.637 |  |  | 8/16 | +0.020 | -0.039 |  | -0.7 / -0.5 | 0.057 |
| MES | 15 | h8 * | -0.020 | -0.075 .. +0.036 | -0.0016 | 0.49 / 0.5 / 0.55 | 0.545 | 1 | 1 | 8/16 | +0.036 | -0.074 | False | -1.0 / -0.7 |  |
| MES | 15 | h16 | -0.019 | -0.102 .. +0.064 | -0.0011 | 0.65 / 0.66 / 0.68 | 0.677 |  |  | 7/16 | +0.041 | -0.079 |  | -0.7 / -0.5 |  |
| MES | 15 | eod | +0.029 | -0.151 .. +0.208 | +0.0006 | 0.76 / 0.76 / 0.8 | 0.794 |  |  | 9/16 | +0.102 | -0.044 |  | +0.5 / +0.3 |  |
| MES | 60 | h1 * | -0.011 | -0.039 .. +0.018 | -0.0027 | 0.46 / 0.46 / 0.49 | 0.478 | 1 | 1 | 9/16 | +0.003 | -0.024 | False | -0.7 / -0.7 |  |
| MES | 60 | h2 | +0.005 | -0.045 .. +0.055 | +0.0010 | 0.85 / 0.85 / 0.85 | 0.861 |  |  | 8/16 | +0.027 | -0.017 |  | +0.2 / +0.2 |  |
| MES | 60 | h4 | +0.016 | -0.072 .. +0.104 | +0.0022 | 0.73 / 0.72 / 0.72 | 0.715 |  |  | 8/16 | +0.037 | -0.006 |  | +0.5 / +0.4 | 0.120 |
| MES | 60 | h8 | -0.016 | -0.139 .. +0.108 | -0.0015 | 0.8 / 0.8 / 0.81 | 0.81 |  |  | 8/16 | +0.038 | -0.069 |  | -0.4 / -0.2 |  |
| MES | 60 | h16 | +0.003 | -0.140 .. +0.145 | +0.0002 | 0.97 / 0.97 / 0.97 | 0.968 |  |  | 8/16 | +0.036 | -0.031 |  | +0.1 / +0.0 |  |
| MES | 60 | eod | -0.004 | -0.147 .. +0.139 | -0.0003 | 0.96 / 0.96 / 0.96 | 0.963 |  |  | 8/16 | +0.030 | -0.038 |  | -0.1 / -0.1 |  |
| MNQ | 5 | h1 | -0.001 | -0.009 .. +0.007 | -0.0003 | 0.74 / 0.74 / 0.75 | 0.736 |  |  | 9/16 | +0.006 | -0.008 |  | -0.3 / -0.3 |  |
| MNQ | 5 | h2 | -0.017 | -0.030 .. -0.004 | -0.0025 | 0.012 / 0.011 / 0.034 | 0.0401 |  |  | 12/16 | +0.001 | -0.035 |  | -3.1 / -2.5 |  |
| MNQ | 5 | h4 * | -0.055 | -0.077 .. -0.033 | -0.0052 | 7e-07 / 4.3e-07 / 6e-05 | 0.0013 | 0.00782 | 0.001 | 14/16 | -0.011 | -0.098 | False | -7.1 / -5.0 | 0.034 |
| MNQ | 5 | h8 | -0.090 | -0.123 .. -0.058 | -0.0059 | 4.3e-08 / 4.5e-08 / 2.8e-05 | 0.0013 |  |  | 15/16 | -0.034 | -0.146 |  | -8.2 / -5.5 |  |
| MNQ | 5 | h16 | -0.124 | -0.172 .. -0.076 | -0.0056 | 4.3e-07 / 8.9e-07 / 0.00014 | 0.000521 |  |  | 13/16 | -0.045 | -0.201 |  | -7.5 / -5.1 |  |
| MNQ | 5 | eod | +0.054 | -0.153 .. +0.262 | +0.0005 | 0.61 / 0.62 / 0.7 | 0.706 |  |  | 10/16 | -0.019 | +0.127 |  | +0.7 / +0.5 |  |
| MNQ | 15 | h1 | +0.000 | -0.012 .. +0.013 | +0.0000 | 0.97 / 0.97 / 0.98 | 0.97 |  |  | 9/16 | +0.001 | -0.000 |  | +0.0 / +0.0 |  |
| MNQ | 15 | h2 | -0.006 | -0.028 .. +0.016 | -0.0008 | 0.62 / 0.61 / 0.73 | 0.677 |  |  | 8/16 | -0.002 | -0.009 |  | -0.6 / -0.5 |  |
| MNQ | 15 | h4 | -0.025 | -0.062 .. +0.012 | -0.0020 | 0.18 / 0.18 / 0.39 | 0.332 |  |  | 9/16 | -0.019 | -0.031 |  | -1.9 / -1.3 | 0.060 |
| MNQ | 15 | h8 * | -0.045 | -0.104 .. +0.015 | -0.0027 | 0.14 / 0.14 / 0.3 | 0.249 | 1 | 1 | 12/16 | -0.015 | -0.074 | False | -2.2 / -1.5 |  |
| MNQ | 15 | h16 | -0.045 | -0.133 .. +0.043 | -0.0022 | 0.31 / 0.32 / 0.4 | 0.367 |  |  | 9/16 | +0.053 | -0.143 |  | -1.5 / -1.0 |  |
| MNQ | 15 | eod | +0.105 | -0.112 .. +0.322 | +0.0018 | 0.34 / 0.33 / 0.46 | 0.421 |  |  | 11/16 | +0.194 | +0.017 |  | +1.5 / +1.0 |  |
| MNQ | 60 | h1 * | -0.028 | -0.058 .. +0.001 | -0.0076 | 0.062 / 0.059 / 0.062 | 0.0599 | 1 | 1 | 11/16 | -0.003 | -0.054 | False | -2.0 / -1.9 |  |
| MNQ | 60 | h2 | -0.042 | -0.097 .. +0.012 | -0.0080 | 0.12 / 0.12 / 0.11 | 0.11 |  |  | 9/16 | -0.000 | -0.085 |  | -2.0 / -1.5 |  |
| MNQ | 60 | h4 | -0.047 | -0.140 .. +0.047 | -0.0062 | 0.33 / 0.3 / 0.29 | 0.295 |  |  | 9/16 | +0.031 | -0.124 |  | -1.6 / -1.0 | 0.125 |
| MNQ | 60 | h8 | -0.048 | -0.170 .. +0.074 | -0.0048 | 0.44 / 0.42 / 0.44 | 0.445 |  |  | 9/16 | +0.072 | -0.168 |  | -1.3 / -0.8 |  |
| MNQ | 60 | h16 | -0.040 | -0.171 .. +0.091 | -0.0030 | 0.55 / 0.54 / 0.58 | 0.58 |  |  | 9/16 | +0.081 | -0.161 |  | -0.9 / -0.6 |  |
| MNQ | 60 | eod | -0.039 | -0.170 .. +0.093 | -0.0028 | 0.57 / 0.55 / 0.59 | 0.59 |  |  | 9/16 | +0.084 | -0.161 |  | -0.9 / -0.6 |  |
| MYM | 5 | h1 | +0.002 | -0.008 .. +0.011 | +0.0004 | 0.76 / 0.77 / 0.85 | 0.813 |  |  | 4/8 | n/a | +0.002 |  | +0.3 / +0.3 |  |
| MYM | 5 | h2 | -0.002 | -0.019 .. +0.015 | -0.0002 | 0.85 / 0.86 / 0.88 | 0.871 |  |  | 5/8 | n/a | -0.002 |  | -0.2 / -0.2 |  |
| MYM | 5 | h4 | -0.012 | -0.041 .. +0.018 | -0.0010 | 0.44 / 0.43 / 0.59 | 0.535 |  |  | 5/8 | n/a | -0.012 |  | -1.2 / -0.8 | 0.046 |
| MYM | 5 | h8 | -0.012 | -0.057 .. +0.032 | -0.0007 | 0.59 / 0.6 / 0.7 | 0.673 |  |  | 5/8 | n/a | -0.012 |  | -0.8 / -0.5 |  |
| MYM | 5 | h16 | -0.015 | -0.079 .. +0.048 | -0.0007 | 0.64 / 0.65 / 0.71 | 0.701 |  |  | 5/8 | n/a | -0.015 |  | -0.7 / -0.5 |  |
| MYM | 5 | eod * | +0.273 | -0.007 .. +0.552 | +0.0030 | 0.056 / 0.058 / 0.13 | 0.131 | 1 | 1 | 5/8 | n/a | +0.273 | False | +2.7 / +1.9 |  |
| MYM | 15 | h1 | -0.004 | -0.021 .. +0.012 | -0.0011 | 0.62 / 0.62 / 0.69 | 0.672 |  |  | 6/8 | n/a | -0.004 |  | -0.5 / -0.5 |  |
| MYM | 15 | h2 | -0.012 | -0.041 .. +0.016 | -0.0017 | 0.4 / 0.41 / 0.57 | 0.498 |  |  | 5/8 | n/a | -0.012 |  | -1.0 / -0.8 |  |
| MYM | 15 | h4 | -0.019 | -0.065 .. +0.026 | -0.0016 | 0.41 / 0.44 / 0.59 | 0.529 |  |  | 4/8 | n/a | -0.019 |  | -1.1 / -0.8 | 0.075 |
| MYM | 15 | h8 | -0.019 | -0.089 .. +0.052 | -0.0012 | 0.6 / 0.62 / 0.72 | 0.688 |  |  | 5/8 | n/a | -0.019 |  | -0.7 / -0.5 |  |
| MYM | 15 | h16 | -0.010 | -0.122 .. +0.101 | -0.0005 | 0.86 / 0.86 / 0.9 | 0.889 |  |  | 4/8 | n/a | -0.010 |  | -0.3 / -0.2 |  |
| MYM | 15 | eod * | +0.118 | -0.170 .. +0.405 | +0.0022 | 0.42 / 0.41 / 0.54 | 0.517 | 1 | 1 | 5/8 | n/a | +0.118 | False | +1.3 / +0.8 |  |
| MYM | 60 | h1 | +0.011 | -0.027 .. +0.049 | +0.0032 | 0.57 / 0.57 / 0.58 | 0.57 |  |  | 5/8 | n/a | +0.011 |  | +0.6 / +0.6 |  |
| MYM | 60 | h2 | +0.012 | -0.055 .. +0.078 | +0.0023 | 0.73 / 0.73 / 0.74 | 0.739 |  |  | 5/8 | n/a | +0.012 |  | +0.4 / +0.3 |  |
| MYM | 60 | h4 | -0.024 | -0.137 .. +0.089 | -0.0034 | 0.68 / 0.69 / 0.69 | 0.69 |  |  | 4/8 | n/a | -0.024 |  | -0.6 / -0.4 | 0.166 |
| MYM | 60 | h8 * | -0.075 | -0.243 .. +0.094 | -0.0077 | 0.39 / 0.4 / 0.39 | 0.393 | 1 | 1 | 5/8 | n/a | -0.075 | False | -1.4 / -0.9 |  |
| MYM | 60 | h16 | -0.047 | -0.248 .. +0.155 | -0.0036 | 0.65 / 0.66 / 0.65 | 0.629 |  |  | 3/8 | n/a | -0.047 |  | -0.8 / -0.5 |  |
| MYM | 60 | eod | -0.052 | -0.254 .. +0.151 | -0.0039 | 0.62 / 0.63 / 0.61 | 0.594 |  |  | 3/8 | n/a | -0.052 |  | -0.8 / -0.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.027 | +0.020 .. +0.034 | +5.5% | +0.053 | 2.5e-13 | 9.58e-11 | 15/16 |
| MES | 5 | h2 | +0.028 | +0.017 .. +0.038 | +3.9% | +0.064 | 9.3e-06 |  | 14/16 |
| MES | 5 | h4 | +0.025 | +0.008 .. +0.043 | +2.5% | +0.073 | 0.0066 |  | 13/16 |
| MES | 5 | h8 | +0.031 | +0.006 .. +0.057 | +2.2% | +0.078 | 0.057 |  | 10/16 |
| MES | 5 | h16 | +0.050 | +0.011 .. +0.088 | +2.4% | +0.089 | 0.011 |  | 11/16 |
| MES | 5 | eod | -0.199 | -0.436 .. +0.038 | -2.0% | -0.313 | 0.1 |  | 6/16 |
| MES | 15 | h1 * | +0.020 | +0.009 .. +0.030 | +3.8% | +0.048 | 0.0025 | 0.4 | 13/16 |
| MES | 15 | h2 | +0.014 | -0.002 .. +0.031 | +2.0% | +0.050 | 0.52 |  | 10/16 |
| MES | 15 | h4 | +0.001 | -0.026 .. +0.028 | +0.1% | +0.046 | 0.94 |  | 7/16 |
| MES | 15 | h8 | +0.020 | -0.018 .. +0.058 | +1.3% | +0.055 | 0.88 |  | 9/16 |
| MES | 15 | h16 | +0.053 | -0.009 .. +0.115 | +2.3% | +0.062 | 0.24 |  | 12/16 |
| MES | 15 | eod | -0.079 | -0.235 .. +0.078 | -1.4% | -0.059 | 0.57 |  | 6/16 |
| MES | 60 | h1 * | -0.026 | -0.046 .. -0.005 | -5.0% | -0.008 | 0.014 | 1 | 10/16 |
| MES | 60 | h2 | -0.011 | -0.047 .. +0.025 | -1.4% | -0.001 | 0.56 |  | 9/16 |
| MES | 60 | h4 | +0.007 | -0.050 .. +0.065 | +0.7% | +0.017 | 0.95 |  | 8/16 |
| MES | 60 | h8 | +0.024 | -0.053 .. +0.100 | +1.6% | +0.010 | 0.63 |  | 10/16 |
| MES | 60 | h16 | +0.041 | -0.049 .. +0.131 | +2.0% | +0.020 | 0.37 |  | 8/16 |
| MES | 60 | eod | +0.038 | -0.054 .. +0.129 | +1.7% | +0.014 | 0.42 |  | 8/16 |
| MNQ | 5 | h1 * | +0.017 | +0.010 .. +0.023 | +3.1% | +0.043 | 2e-07 | 5.26e-05 | 15/16 |
| MNQ | 5 | h2 | +0.014 | +0.003 .. +0.024 | +1.8% | +0.050 | 0.01 |  | 12/16 |
| MNQ | 5 | h4 | +0.007 | -0.010 .. +0.025 | +0.7% | +0.045 | 0.51 |  | 7/16 |
| MNQ | 5 | h8 | +0.004 | -0.025 .. +0.034 | +0.3% | +0.035 | 0.89 |  | 9/16 |
| MNQ | 5 | h16 | +0.017 | -0.032 .. +0.065 | +0.7% | +0.025 | 0.92 |  | 10/16 |
| MNQ | 5 | eod | -0.224 | -0.533 .. +0.085 | -1.8% | -0.333 | 0.16 |  | 11/16 |
| MNQ | 15 | h1 * | +0.014 | +0.004 .. +0.024 | +2.6% | +0.035 | 0.12 | 1 | 11/16 |
| MNQ | 15 | h2 | -0.003 | -0.020 .. +0.014 | -0.4% | +0.026 | 0.74 |  | 9/16 |
| MNQ | 15 | h4 | -0.014 | -0.045 .. +0.017 | -1.3% | +0.017 | 0.49 |  | 10/16 |
| MNQ | 15 | h8 | +0.014 | -0.039 .. +0.067 | +0.8% | +0.015 | 0.75 |  | 10/16 |
| MNQ | 15 | h16 | +0.054 | -0.018 .. +0.126 | +2.1% | +0.004 | 0.14 |  | 12/16 |
| MNQ | 15 | eod | +0.086 | -0.138 .. +0.311 | +1.4% | -0.005 | 0.45 |  | 10/16 |
| MNQ | 60 | h1 * | -0.013 | -0.035 .. +0.008 | -2.5% | -0.009 | 0.22 | 1 | 10/16 |
| MNQ | 60 | h2 | -0.010 | -0.045 .. +0.026 | -1.3% | -0.003 | 0.6 |  | 9/16 |
| MNQ | 60 | h4 | -0.017 | -0.071 .. +0.037 | -1.5% | -0.023 | 0.54 |  | 9/16 |
| MNQ | 60 | h8 | -0.012 | -0.086 .. +0.061 | -0.8% | -0.033 | 0.75 |  | 9/16 |
| MNQ | 60 | h16 | -0.033 | -0.125 .. +0.058 | -1.5% | -0.042 | 0.47 |  | 10/16 |
| MNQ | 60 | eod | -0.034 | -0.126 .. +0.058 | -1.5% | -0.043 | 0.47 |  | 9/16 |
| MYM | 5 | h1 * | +0.026 | +0.018 .. +0.033 | +4.8% | +0.052 | 2.2e-07 | 5.78e-05 | 8/8 |
| MYM | 5 | h2 | +0.025 | +0.012 .. +0.039 | +3.3% | +0.061 | 0.01 |  | 8/8 |
| MYM | 5 | h4 | +0.016 | -0.007 .. +0.040 | +1.5% | +0.061 | 0.43 |  | 6/8 |
| MYM | 5 | h8 | +0.012 | -0.030 .. +0.053 | +0.7% | +0.050 | 0.98 |  | 5/8 |
| MYM | 5 | h16 | +0.027 | -0.035 .. +0.089 | +1.2% | +0.036 | 0.87 |  | 6/8 |
| MYM | 5 | eod | -0.296 | -0.607 .. +0.016 | -2.5% | -0.433 | 0.063 |  | 5/8 |
| MYM | 15 | h1 * | +0.025 | +0.012 .. +0.038 | +4.7% | +0.057 | 0.0018 | 0.3 | 7/8 |
| MYM | 15 | h2 | +0.036 | +0.013 .. +0.059 | +4.7% | +0.062 | 0.014 |  | 7/8 |
| MYM | 15 | h4 | +0.017 | -0.020 .. +0.054 | +1.5% | +0.048 | 0.69 |  | 6/8 |
| MYM | 15 | h8 | +0.034 | -0.030 .. +0.098 | +2.1% | +0.033 | 0.7 |  | 6/8 |
| MYM | 15 | h16 | +0.019 | -0.093 .. +0.131 | +0.8% | +0.002 | 0.74 |  | 6/8 |
| MYM | 15 | eod | +0.002 | -0.272 .. +0.276 | +0.0% | +0.048 | 0.99 |  | 5/8 |
| MYM | 60 | h1 | +0.002 | -0.023 .. +0.027 | +0.4% | +0.018 | 0.86 |  | 4/8 |
| MYM | 60 | h2 | +0.013 | -0.031 .. +0.057 | +1.7% | +0.014 | 0.69 |  | 5/8 |
| MYM | 60 | h4 | +0.036 | -0.026 .. +0.098 | +3.3% | +0.039 | 0.31 |  | 5/8 |
| MYM | 60 | h8 | +0.074 | -0.019 .. +0.167 | +4.8% | +0.082 | 0.21 |  | 5/8 |
| MYM | 60 | h16 | +0.091 | -0.024 .. +0.206 | +4.3% | +0.091 | 0.16 |  | 4/8 |
| MYM | 60 | eod * | +0.093 | -0.023 .. +0.209 | +4.2% | +0.092 | 0.15 | 1 | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.50 pts | -1.20 .. +0.20 | 0.16 |
| MES | 15 | -0.22 pts | -1.19 .. +0.75 | 0.72 |
| MES | 60 | +0.57 pts | -1.30 .. +2.45 | 0.55 |
| MNQ | 5 | -0.84 pts | -1.38 .. -0.29 | 0.0041 |
| MNQ | 15 | -0.14 pts | -1.00 .. +0.72 | 0.75 |
| MNQ | 60 | -1.74 pts | -3.64 .. +0.16 | 0.072 |
| MYM | 5 | +0.20 pts | -0.50 .. +0.90 | 0.58 |
| MYM | 15 | +0.27 pts | -0.80 .. +1.35 | 0.63 |
| MYM | 60 | +0.64 pts | -1.95 .. +3.22 | 0.63 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 28601 | +0.010 | 0.206 | +0.18 | -3.32 | -3.30 | -3.33 | -3.40 |
| MES | 5 | h2 | event | against signal | 28601 | +0.000 | 0.206 | -0.05 | -3.55 | -3.61 | -3.52 | -3.44 |
| MES | 5 | h4 | event | against signal | 28601 | +0.029 | 0.206 | +0.49 | -3.01 | -3.46 | -2.81 | -2.91 |
| MES | 5 | h8 | event | against signal | 28601 | +0.052 | 0.206 | +0.76 | -2.74 | -3.17 | -2.55 | -2.65 |
| MES | 5 | h16 | event | against signal | 28601 | +0.067 | 0.206 | +1.16 | -2.34 | -3.37 | -1.89 | -2.24 |
| MES | 5 | eod | event | with signal | 28601 | -0.017 | 0.206 | -1.43 | -4.93 | -4.30 | -5.21 | -3.40 |
| MES | 15 | h1 | event | with signal | 13312 | +0.006 | 0.139 | +0.01 | -3.49 | -3.15 | -3.67 | -3.57 |
| MES | 15 | h2 | event | against signal | 13312 | +0.005 | 0.139 | +0.40 | -3.10 | -3.64 | -2.82 | -3.02 |
| MES | 15 | h4 | event | against signal | 13312 | +0.009 | 0.139 | +0.51 | -2.99 | -3.75 | -2.60 | -2.95 |
| MES | 15 | h8 | event | against signal | 13312 | +0.022 | 0.139 | +0.97 | -2.53 | -3.75 | -1.90 | -2.57 |
| MES | 15 | h16 | event | against signal | 13312 | +0.035 | 0.139 | +0.57 | -2.93 | -3.59 | -2.59 | -3.30 |
| MES | 15 | eod | event | with signal | 13312 | -0.054 | 0.139 | +0.46 | -3.04 | -3.35 | -2.88 | -1.02 |
| MES | 60 | h1 | event | against signal | 3675 | +0.014 | 0.086 | +0.54 | -2.96 | -3.39 | -2.68 | -3.05 |
| MES | 60 | h2 | event | with signal | 3675 | -0.000 | 0.086 | -0.47 | -3.97 | -3.11 | -4.52 | -3.81 |
| MES | 60 | h4 | event | with signal | 3675 | +0.008 | 0.086 | -0.44 | -3.94 | -2.91 | -4.60 | -3.70 |
| MES | 60 | h8 | event | against signal | 3675 | +0.029 | 0.086 | +2.86 | -0.64 | -3.59 | +1.27 | -1.07 |
| MES | 60 | h16 | event | with signal | 3675 | -0.022 | 0.086 | -3.02 | -6.52 | -3.52 | -8.45 | -5.63 |
| MES | 60 | eod | event | against signal | 3675 | +0.024 | 0.086 | +3.09 | -0.41 | -3.41 | +1.53 | -1.11 |
| MNQ | 5 | h1 | event | against signal | 44559 | +0.000 | 0.091 | +0.01 | -1.99 | -2.11 | -1.92 | -1.97 |
| MNQ | 5 | h2 | event | against signal | 44559 | +0.016 | 0.091 | +0.26 | -1.74 | -2.06 | -1.56 | -1.71 |
| MNQ | 5 | h4 | event | against signal | 44559 | +0.056 | 0.091 | +1.18 | -0.82 | -1.89 | -0.23 | -0.84 |
| MNQ | 5 | h8 | event | against signal | 44559 | +0.096 | 0.091 | +1.69 | -0.31 | -1.53 | +0.38 | -0.41 |
| MNQ | 5 | h16 | event | against signal | 44559 | +0.135 | 0.091 | +2.55 | +0.55 | -1.27 | +1.57 | +0.31 |
| MNQ | 5 | eod | event | with signal | 44559 | -0.105 | 0.091 | -1.83 | -3.83 | -2.86 | -4.37 | -0.45 |
| MNQ | 15 | h1 | event | with signal | 16760 | +0.001 | 0.058 | +0.07 | -1.93 | -1.97 | -1.90 | -1.97 |
| MNQ | 15 | h2 | event | against signal | 16760 | +0.006 | 0.058 | +0.34 | -1.66 | -1.87 | -1.53 | -1.65 |
| MNQ | 15 | h4 | event | against signal | 16760 | +0.027 | 0.058 | +1.21 | -0.79 | -1.58 | -0.30 | -0.81 |
| MNQ | 15 | h8 | event | against signal | 16760 | +0.052 | 0.058 | +2.08 | +0.08 | -1.43 | +1.04 | -0.09 |
| MNQ | 15 | h16 | event | against signal | 16760 | +0.068 | 0.058 | +2.90 | +0.90 | -1.42 | +2.36 | +0.24 |
| MNQ | 15 | eod | event | with signal | 16760 | +0.011 | 0.058 | +0.24 | -1.76 | -2.10 | -1.54 | +1.25 |
| MNQ | 60 | h1 | event | against signal | 4178 | +0.035 | 0.035 | +1.94 | -0.06 | -1.45 | +1.10 | -0.31 |
| MNQ | 60 | h2 | event | against signal | 4178 | +0.053 | 0.035 | +3.28 | +1.28 | -1.07 | +3.23 | +0.87 |
| MNQ | 60 | h4 | event | against signal | 4178 | +0.064 | 0.035 | +4.05 | +2.05 | -1.03 | +4.61 | +1.38 |
| MNQ | 60 | h8 | event | against signal | 4178 | +0.073 | 0.035 | +5.65 | +3.65 | -1.32 | +7.78 | +2.69 |
| MNQ | 60 | h16 | event | against signal | 4178 | +0.076 | 0.035 | +4.88 | +2.88 | -1.50 | +6.53 | +1.38 |
| MNQ | 60 | eod | event | against signal | 4178 | +0.075 | 0.035 | +4.73 | +2.73 | -1.52 | +6.25 | +1.30 |
| MYM | 5 | h1 | event | with signal | 25260 | +0.004 | 0.142 | +0.03 | -1.97 | +nan | -1.97 | -2.00 |
| MYM | 5 | h2 | event | against signal | 25260 | +0.001 | 0.142 | +0.02 | -1.98 | +nan | -1.98 | -1.98 |
| MYM | 5 | h4 | event | against signal | 25260 | +0.016 | 0.142 | +0.27 | -1.73 | +nan | -1.73 | -1.81 |
| MYM | 5 | h8 | event | against signal | 25260 | +0.023 | 0.142 | +0.36 | -1.64 | +nan | -1.64 | -1.84 |
| MYM | 5 | h16 | event | against signal | 25260 | +0.032 | 0.142 | +0.37 | -1.63 | +nan | -1.63 | -1.92 |
| MYM | 5 | eod | event | with signal | 25260 | +0.178 | 0.142 | +0.86 | -1.14 | +nan | -1.14 | +0.27 |
| MYM | 15 | h1 | event | against signal | 9509 | +0.004 | 0.087 | +0.23 | -1.77 | +nan | -1.77 | -1.76 |
| MYM | 15 | h2 | event | against signal | 9509 | +0.014 | 0.087 | +0.50 | -1.50 | +nan | -1.50 | -1.54 |
| MYM | 15 | h4 | event | against signal | 9509 | +0.023 | 0.087 | +0.50 | -1.50 | +nan | -1.50 | -1.60 |
| MYM | 15 | h8 | event | against signal | 9509 | +0.027 | 0.087 | +0.78 | -1.22 | +nan | -1.22 | -1.48 |
| MYM | 15 | h16 | event | against signal | 9509 | +0.031 | 0.087 | +0.36 | -1.64 | +nan | -1.64 | -2.16 |
| MYM | 15 | eod | event | with signal | 9509 | +0.067 | 0.087 | +1.11 | -0.89 | +nan | -0.89 | +0.18 |
| MYM | 60 | h1 | event | with signal | 2232 | +0.009 | 0.048 | +0.64 | -1.36 | +nan | -1.36 | -1.29 |
| MYM | 60 | h2 | event | with signal | 2232 | +0.009 | 0.048 | +0.64 | -1.36 | +nan | -1.36 | -1.25 |
| MYM | 60 | h4 | event | against signal | 2232 | +0.030 | 0.048 | +0.79 | -1.21 | +nan | -1.21 | -1.46 |
| MYM | 60 | h8 | event | against signal | 2232 | +0.089 | 0.048 | +3.14 | +1.14 | +nan | +1.14 | +0.49 |
| MYM | 60 | h16 | event | against signal | 2232 | +0.084 | 0.048 | +3.86 | +1.86 | +nan | +1.86 | +0.13 |
| MYM | 60 | eod | event | against signal | 2232 | +0.087 | 0.048 | +3.98 | +1.98 | +nan | +1.98 | +0.35 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.624 | +2.169 | +1.772 | +0.867 | +0.333 | +0.000 | +0.007 | -0.001 | -0.028 | -0.046 | -0.062 |
| MES | 15 | +1.615 | +2.098 | +1.719 | +0.846 | +0.318 | +0.000 | +0.007 | -0.002 | -0.003 | -0.006 | +0.024 |
| MES | 60 | +2.503 | +2.216 | +1.732 | +0.840 | +0.303 | +0.000 | -0.010 | +0.008 | +0.026 | -0.010 | +0.573 |
| MNQ | 5 | +1.593 | +2.140 | +1.756 | +0.863 | +0.326 | +0.000 | +0.000 | -0.013 | -0.051 | -0.085 | -0.126 |
| MNQ | 15 | +1.610 | +2.072 | +1.713 | +0.845 | +0.312 | +0.000 | +0.003 | -0.002 | -0.023 | -0.045 | -0.035 |
| MNQ | 60 | +2.682 | +2.305 | +1.780 | +0.883 | +0.330 | +0.000 | -0.028 | -0.044 | -0.051 | -0.022 | +0.228 |
| MYM | 5 | +1.593 | +2.142 | +1.742 | +0.848 | +0.317 | +0.000 | +0.004 | +0.001 | -0.009 | -0.011 | -0.006 |
| MYM | 15 | +1.602 | +2.072 | +1.675 | +0.817 | +0.299 | +0.000 | -0.001 | -0.007 | -0.023 | -0.027 | -0.026 |
| MYM | 60 | +2.584 | +2.134 | +1.655 | +0.817 | +0.290 | +0.000 | +0.008 | +0.011 | -0.045 | -0.127 | +0.335 |

## Calibration

- MES 5-min: 1036271 bars, 28601 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 13312 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3675 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 44559 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 16760 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 4178 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 25260 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 9509 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2232 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 5% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 43599 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
