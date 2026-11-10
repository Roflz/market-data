# Impact card: mom14_div

divergence: close at a 20-bar high while Momentum(14) below its prior 19-bar high -> short; mirror -> long [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.043 R20 over the next 16 bars (80 min), p=0.017; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.014 R20, CONFIRMED, q=7.15e-16, 16 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.53 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.237 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.005 R20 over the next 1 bar (15 min), p=0.67; we would catch an effect of 0.028 R20 or more 80% of the time).
- MES 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.011 R20, CONFIRMED, q=0.0319, 12 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.98 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.136 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.026 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.060 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.075).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $3.10 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.066 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: moves price AGAINST the signal 0.010 average bars (~$0.26 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), same sign in 14 of 16 years, q=0.00425; best leg (event, against signal) grosses $+0.06 and nets $-1.94 per micro per trade after $2.00 costs -> not tradable on its own.
- MNQ 5-min size: the market moves 5% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.026 R20, CONFIRMED, q=7.42e-30, 15 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.15, pessimistic $+0.05) does not clearly beat the $2.00 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.233 R20 over the rest of the session (to 16:45), p=0.86; we would catch an effect of 0.035 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.032 R20, CONFIRMED, q=0.0219, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $10.13 at recent bar sizes, 90% range up to $6.66); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.055 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.066 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 7% MORE after the event than after matched bars over the next 2 bars (2 h) (+0.050 R20, CONFIRMED, q=0.000189, 14 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.79 at recent bar sizes, 90% range up to $5.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -0.509 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.029 R20 or more 80% of the time).
- MYM 5-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.023 R20, CONFIRMED, q=1.49e-14, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.82 at recent bar sizes, 90% range up to $0.79); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.743 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.054 R20 or more 80% of the time).
- MYM 15-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.031 R20, CONFIRMED, q=0.0267, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $14.82 at recent bar sizes, 90% range up to $5.20); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.018 R20 over the next 1 bar (1 h), p=0.79; we would catch an effect of 0.087 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.74 at recent bar sizes, 90% range up to $4.59); about 15.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.003 .. +0.005 | +0.0007 | 0.59 / 0.59 / 0.59 | 0.586 |  |  | 7/16 | -0.004 | +0.006 |  | +0.6 / +0.5 |  |
| MES | 5 | h2 | +0.001 | -0.005 .. +0.007 | +0.0004 | 0.79 / 0.78 / 0.8 | 0.802 |  |  | 7/16 | -0.001 | +0.003 |  | +0.3 / +0.3 |  |
| MES | 5 | h4 | +0.006 | -0.004 .. +0.016 | +0.0018 | 0.24 / 0.21 / 0.24 | 0.233 |  |  | 9/16 | +0.008 | +0.004 |  | +1.7 / +1.2 | 0.014 |
| MES | 5 | h8 | +0.022 | +0.006 .. +0.039 | +0.0046 | 0.0089 / 0.0062 / 0.0084 | 0.0086 |  |  | 12/16 | +0.033 | +0.011 |  | +4.3 / +2.6 |  |
| MES | 5 | h16 * | +0.043 | +0.015 .. +0.071 | +0.0062 | 0.0028 / 0.0017 / 0.0029 | 0.00391 | 0.447 | 0.545 | 12/16 | +0.067 | +0.019 | False | +5.7 / +3.0 |  |
| MES | 5 | eod | -0.026 | -0.239 .. +0.187 | -0.0008 | 0.81 / 0.81 / 0.79 | 0.791 |  |  | 6/16 | +0.103 | -0.155 |  | -0.7 / -0.2 |  |
| MES | 15 | h1 * | -0.005 | -0.012 .. +0.001 | -0.0030 | 0.11 / 0.11 / 0.14 | 0.137 | 1 | 1 | 11/16 | -0.000 | -0.011 | False | -1.6 / -1.6 |  |
| MES | 15 | h2 | -0.003 | -0.014 .. +0.007 | -0.0012 | 0.53 / 0.54 / 0.59 | 0.589 |  |  | 10/16 | +0.007 | -0.013 |  | -0.7 / -0.6 |  |
| MES | 15 | h4 | +0.008 | -0.010 .. +0.026 | +0.0020 | 0.4 / 0.4 / 0.44 | 0.442 |  |  | 10/16 | +0.023 | -0.008 |  | +1.1 / +0.8 | 0.028 |
| MES | 15 | h8 | +0.011 | -0.021 .. +0.043 | +0.0020 | 0.49 / 0.48 / 0.5 | 0.5 |  |  | 8/16 | +0.038 | -0.015 |  | +1.1 / +0.7 |  |
| MES | 15 | h16 | +0.038 | -0.016 .. +0.091 | +0.0046 | 0.17 / 0.17 / 0.19 | 0.192 |  |  | 11/16 | +0.098 | -0.023 |  | +2.3 / +1.4 |  |
| MES | 15 | eod | -0.058 | -0.302 .. +0.185 | -0.0029 | 0.64 / 0.62 / 0.55 | 0.549 |  |  | 8/16 | +0.078 | -0.194 |  | -1.3 / -0.5 |  |
| MES | 60 | h1 | -0.002 | -0.017 .. +0.013 | -0.0011 | 0.79 / 0.79 / 0.79 | 0.793 |  |  | 7/16 | +0.009 | -0.014 |  | -0.3 / -0.3 |  |
| MES | 60 | h2 | -0.003 | -0.027 .. +0.022 | -0.0011 | 0.84 / 0.84 / 0.85 | 0.838 |  |  | 6/16 | +0.011 | -0.016 |  | -0.2 / -0.2 |  |
| MES | 60 | h4 | +0.001 | -0.041 .. +0.043 | +0.0005 | 0.95 / 0.95 / 0.96 | 0.958 |  |  | 10/16 | +0.009 | -0.006 |  | +0.1 / +0.1 | 0.060 |
| MES | 60 | h8 | +0.003 | -0.064 .. +0.069 | +0.0006 | 0.94 / 0.94 / 0.94 | 0.94 |  |  | 9/16 | +0.004 | +0.002 |  | +0.1 / +0.1 |  |
| MES | 60 | h16 | +0.011 | -0.085 .. +0.107 | +0.0018 | 0.82 / 0.82 / 0.82 | 0.819 |  |  | 11/16 | +0.020 | +0.002 |  | +0.4 / +0.2 |  |
| MES | 60 | eod * | +0.026 | -0.075 .. +0.127 | +0.0037 | 0.62 / 0.62 / 0.62 | 0.62 | 1 | 1 | 10/16 | +0.018 | +0.034 | False | +1.0 / +0.5 |  |
| MNQ | 5 | h1 * | -0.010 | -0.015 .. -0.006 | -0.0050 | 4.6e-06 / 2.8e-06 / 7.4e-06 | 0.00026 | 0.00425 | 0.003 | 14/16 | -0.015 | -0.006 | True | -4.7 / -4.6 |  |
| MNQ | 5 | h2 | -0.014 | -0.021 .. -0.007 | -0.0041 | 0.00018 / 0.00017 / 0.00099 | 0.0013 |  |  | 12/16 | -0.015 | -0.013 |  | -4.0 / -3.8 |  |
| MNQ | 5 | h4 | -0.014 | -0.027 .. -0.001 | -0.0026 | 0.033 / 0.031 / 0.055 | 0.0529 |  |  | 12/16 | -0.014 | -0.013 |  | -2.8 / -2.1 | 0.019 |
| MNQ | 5 | h8 | +0.002 | -0.023 .. +0.027 | +0.0003 | 0.88 / 0.88 / 0.88 | 0.881 |  |  | 10/16 | +0.004 | +0.000 |  | +0.3 / +0.1 |  |
| MNQ | 5 | h16 | +0.007 | -0.030 .. +0.045 | +0.0007 | 0.7 / 0.7 / 0.72 | 0.714 |  |  | 8/16 | +0.020 | -0.005 |  | +0.6 / +0.4 |  |
| MNQ | 5 | eod | -0.050 | -0.554 .. +0.453 | -0.0011 | 0.84 / 0.84 / 0.7 | 0.71 |  |  | 4/16 | +0.233 | -0.332 |  | -0.8 / -0.2 |  |
| MNQ | 15 | h1 | -0.003 | -0.021 .. +0.015 | -0.0012 | 0.73 / 0.74 / 0.53 | 0.497 |  |  | 13/16 | -0.007 | +0.001 |  | -0.3 / -0.3 |  |
| MNQ | 15 | h2 | +0.004 | -0.034 .. +0.042 | +0.0010 | 0.85 / 0.85 / 0.67 | 0.659 |  |  | 4/16 | -0.004 | +0.012 |  | +0.3 / +0.2 |  |
| MNQ | 15 | h4 | +0.028 | -0.057 .. +0.114 | +0.0043 | 0.52 / 0.51 / 0.08 | 0.0823 |  |  | 6/16 | +0.007 | +0.049 |  | +1.4 / +0.6 | 0.035 |
| MNQ | 15 | h8 | +0.047 | -0.081 .. +0.174 | +0.0054 | 0.47 / 0.46 / 0.056 | 0.0578 |  |  | 7/16 | +0.025 | +0.068 |  | +2.0 / +0.7 |  |
| MNQ | 15 | h16 | +0.006 | -0.078 .. +0.089 | +0.0003 | 0.9 / 0.9 / 0.88 | 0.868 |  |  | 7/16 | +0.105 | -0.093 |  | +0.2 / +0.1 |  |
| MNQ | 15 | eod * | -0.233 | -0.545 .. +0.079 | -0.0074 | 0.14 / 0.13 / 0.076 | 0.0789 | 1 | 1 | 12/16 | -0.111 | -0.354 | False | -3.2 / -1.5 |  |
| MNQ | 60 | h1 | +0.005 | -0.013 .. +0.022 | +0.0023 | 0.61 / 0.61 / 0.6 | 0.602 |  |  | 10/16 | +0.018 | -0.009 |  | +0.5 / +0.5 |  |
| MNQ | 60 | h2 | +0.014 | -0.016 .. +0.043 | +0.0049 | 0.36 / 0.35 / 0.33 | 0.324 |  |  | 11/16 | +0.029 | -0.001 |  | +1.1 / +0.9 |  |
| MNQ | 60 | h4 | +0.007 | -0.039 .. +0.053 | +0.0017 | 0.76 / 0.76 / 0.76 | 0.768 |  |  | 8/16 | +0.027 | -0.013 |  | +0.4 / +0.3 | 0.066 |
| MNQ | 60 | h8 | -0.004 | -0.076 .. +0.068 | -0.0008 | 0.92 / 0.92 / 0.92 | 0.913 |  |  | 6/16 | +0.008 | -0.016 |  | -0.2 / -0.1 |  |
| MNQ | 60 | h16 * | -0.055 | -0.156 .. +0.046 | -0.0077 | 0.29 / 0.3 / 0.29 | 0.292 | 1 | 1 | 7/16 | -0.050 | -0.059 | False | -1.9 / -1.1 |  |
| MNQ | 60 | eod | -0.036 | -0.143 .. +0.072 | -0.0049 | 0.51 / 0.53 / 0.52 | 0.523 |  |  | 5/16 | -0.048 | -0.023 |  | -1.2 / -0.7 |  |
| MYM | 5 | h1 | -0.000 | -0.007 .. +0.006 | -0.0002 | 0.89 / 0.89 / 0.84 | 0.847 |  |  | 4/8 | n/a | -0.000 |  | -0.1 / -0.1 |  |
| MYM | 5 | h2 | -0.005 | -0.024 .. +0.014 | -0.0013 | 0.62 / 0.62 / 0.43 | 0.424 |  |  | 3/8 | n/a | -0.005 |  | -0.5 / -0.5 |  |
| MYM | 5 | h4 | -0.013 | -0.065 .. +0.040 | -0.0022 | 0.64 / 0.64 / 0.27 | 0.258 |  |  | 2/8 | n/a | -0.013 |  | -0.8 / -0.5 | 0.029 |
| MYM | 5 | h8 | -0.005 | -0.080 .. +0.069 | -0.0008 | 0.89 / 0.89 / 0.76 | 0.769 |  |  | 4/8 | n/a | -0.005 |  | -0.3 / -0.1 |  |
| MYM | 5 | h16 | +0.026 | -0.066 .. +0.118 | +0.0022 | 0.58 / 0.58 / 0.35 | 0.349 |  |  | 5/8 | n/a | +0.026 |  | +1.3 / +0.6 |  |
| MYM | 5 | eod * | -0.509 | -1.540 .. +0.521 | -0.0105 | 0.33 / 0.33 / 0.0033 | 0.00316 | 1 | 1 | 4/8 | n/a | -0.509 | False | -5.3 / -1.0 |  |
| MYM | 15 | h1 | -0.001 | -0.018 .. +0.016 | -0.0002 | 0.93 / 0.94 / 0.91 | 0.895 |  |  | 4/8 | n/a | -0.001 |  | -0.1 / -0.1 |  |
| MYM | 15 | h2 | -0.003 | -0.027 .. +0.021 | -0.0007 | 0.8 / 0.82 / 0.81 | 0.801 |  |  | 3/8 | n/a | -0.003 |  | -0.2 / -0.3 |  |
| MYM | 15 | h4 | +0.004 | -0.034 .. +0.041 | +0.0006 | 0.85 / 0.87 / 0.88 | 0.862 |  |  | 5/8 | n/a | +0.004 |  | +0.2 / +0.2 | 0.054 |
| MYM | 15 | h8 | -0.094 | -0.292 .. +0.103 | -0.0107 | 0.35 / 0.35 / 0.0035 | 0.00738 |  |  | 4/8 | n/a | -0.094 |  | -1.9 / -0.9 |  |
| MYM | 15 | h16 | -0.239 | -0.750 .. +0.272 | -0.0194 | 0.36 / 0.36 / 2.7e-05 | 0.00105 |  |  | 3/8 | n/a | -0.239 |  | -3.5 / -0.9 |  |
| MYM | 15 | eod * | -0.743 | -2.142 .. +0.656 | -0.0249 | 0.3 / 0.3 / 1.5e-05 | 0.000527 | 1 | 1 | 4/8 | n/a | -0.743 | False | -4.6 / -1.0 |  |
| MYM | 60 | h1 * | -0.018 | -0.042 .. +0.005 | -0.0098 | 0.13 / 0.13 / 0.12 | 0.118 | 1 | 1 | 4/8 | n/a | -0.018 | False | -1.5 / -1.5 |  |
| MYM | 60 | h2 | -0.021 | -0.060 .. +0.018 | -0.0080 | 0.3 / 0.31 / 0.28 | 0.282 |  |  | 5/8 | n/a | -0.021 |  | -1.2 / -1.0 |  |
| MYM | 60 | h4 | +0.011 | -0.050 .. +0.073 | +0.0029 | 0.72 / 0.73 / 0.72 | 0.715 |  |  | 5/8 | n/a | +0.011 |  | +0.5 / +0.4 | 0.087 |
| MYM | 60 | h8 | +0.017 | -0.083 .. +0.117 | +0.0034 | 0.74 / 0.74 / 0.73 | 0.732 |  |  | 3/8 | n/a | +0.017 |  | +0.5 / +0.3 |  |
| MYM | 60 | h16 | +0.020 | -0.128 .. +0.167 | +0.0029 | 0.79 / 0.79 / 0.78 | 0.781 |  |  | 4/8 | n/a | +0.020 |  | +0.5 / +0.3 |  |
| MYM | 60 | eod | +0.025 | -0.135 .. +0.186 | +0.0032 | 0.76 / 0.75 / 0.74 | 0.734 |  |  | 4/8 | n/a | +0.025 |  | +0.6 / +0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.014 | +0.011 .. +0.017 | +2.7% | +0.036 | 1.4e-18 | 7.15e-16 | 16/16 |
| MES | 5 | h2 | +0.012 | +0.007 .. +0.016 | +1.6% | +0.033 | 2.6e-06 |  | 13/16 |
| MES | 5 | h4 | +0.010 | +0.003 .. +0.017 | +1.0% | +0.030 | 0.0042 |  | 13/16 |
| MES | 5 | h8 | +0.006 | -0.004 .. +0.016 | +0.4% | +0.025 | 0.26 |  | 9/16 |
| MES | 5 | h16 | +0.011 | -0.005 .. +0.026 | +0.5% | +0.032 | 0.18 |  | 11/16 |
| MES | 5 | eod | +0.023 | -0.067 .. +0.113 | +0.2% | +0.189 | 0.62 |  | 9/16 |
| MES | 15 | h1 * | +0.011 | +0.005 .. +0.017 | +2.2% | +0.025 | 0.00016 | 0.0319 | 12/16 |
| MES | 15 | h2 | +0.008 | -0.002 .. +0.018 | +1.1% | +0.025 | 0.12 |  | 11/16 |
| MES | 15 | h4 | +0.008 | -0.008 .. +0.024 | +0.8% | +0.024 | 0.51 |  | 11/16 |
| MES | 15 | h8 | +0.015 | -0.008 .. +0.038 | +1.0% | +0.037 | 0.4 |  | 10/16 |
| MES | 15 | h16 | +0.029 | -0.005 .. +0.062 | +1.3% | +0.058 | 0.13 |  | 11/16 |
| MES | 15 | eod | +0.087 | -0.007 .. +0.180 | +1.6% | +0.270 | 0.12 |  | 9/16 |
| MES | 60 | h1 | +0.016 | +0.004 .. +0.027 | +3.1% | +0.025 | 0.037 |  | 11/16 |
| MES | 60 | h2 * | +0.027 | +0.009 .. +0.045 | +3.7% | +0.034 | 0.013 | 1 | 11/16 |
| MES | 60 | h4 | +0.020 | -0.007 .. +0.046 | +1.8% | +0.030 | 0.5 |  | 11/16 |
| MES | 60 | h8 | +0.042 | +0.003 .. +0.080 | +2.8% | +0.025 | 0.14 |  | 10/16 |
| MES | 60 | h16 | +0.072 | +0.021 .. +0.123 | +3.5% | +0.048 | 0.036 |  | 12/16 |
| MES | 60 | eod | +0.074 | +0.021 .. +0.127 | +3.4% | +0.053 | 0.034 |  | 12/16 |
| MNQ | 5 | h1 * | +0.026 | +0.022 .. +0.030 | +4.9% | +0.055 | 9.4e-33 | 7.42e-30 | 15/16 |
| MNQ | 5 | h2 | +0.031 | +0.024 .. +0.037 | +4.0% | +0.058 | 1.6e-16 |  | 15/16 |
| MNQ | 5 | h4 | +0.036 | +0.025 .. +0.046 | +3.2% | +0.068 | 2.3e-08 |  | 15/16 |
| MNQ | 5 | h8 | +0.029 | +0.011 .. +0.047 | +1.8% | +0.065 | 0.0079 |  | 13/16 |
| MNQ | 5 | h16 | +0.034 | +0.004 .. +0.063 | +1.4% | +0.089 | 0.042 |  | 14/16 |
| MNQ | 5 | eod | +0.445 | +0.130 .. +0.760 | +3.5% | +1.065 | 0.0056 |  | 15/16 |
| MNQ | 15 | h1 * | +0.032 | +0.016 .. +0.049 | +6.1% | +0.052 | 0.00011 | 0.0219 | 16/16 |
| MNQ | 15 | h2 | +0.045 | +0.013 .. +0.078 | +5.9% | +0.071 | 0.0063 |  | 14/16 |
| MNQ | 15 | h4 | +0.059 | -0.004 .. +0.121 | +5.2% | +0.098 | 0.069 |  | 13/16 |
| MNQ | 15 | h8 | +0.090 | -0.002 .. +0.181 | +5.3% | +0.169 | 0.059 |  | 13/16 |
| MNQ | 15 | h16 | +0.132 | -0.023 .. +0.286 | +5.2% | +0.316 | 0.097 |  | 10/16 |
| MNQ | 15 | eod | +0.203 | -0.050 .. +0.456 | +3.2% | +0.570 | 0.12 |  | 11/16 |
| MNQ | 60 | h1 | +0.026 | +0.013 .. +0.040 | +5.0% | +0.026 | 0.00017 |  | 14/16 |
| MNQ | 60 | h2 * | +0.050 | +0.030 .. +0.070 | +6.5% | +0.054 | 7.5e-07 | 0.000189 | 14/16 |
| MNQ | 60 | h4 | +0.050 | +0.023 .. +0.077 | +4.5% | +0.062 | 0.00052 |  | 14/16 |
| MNQ | 60 | h8 | +0.076 | +0.035 .. +0.116 | +4.8% | +0.082 | 0.00051 |  | 12/16 |
| MNQ | 60 | h16 | +0.094 | +0.040 .. +0.148 | +4.3% | +0.099 | 0.0013 |  | 11/16 |
| MNQ | 60 | eod | +0.103 | +0.046 .. +0.159 | +4.5% | +0.104 | 0.0012 |  | 12/16 |
| MYM | 5 | h1 * | +0.023 | +0.018 .. +0.028 | +4.3% | +0.052 | 3.2e-17 | 1.49e-14 | 8/8 |
| MYM | 5 | h2 | +0.037 | +0.018 .. +0.056 | +4.8% | +0.068 | 0.00036 |  | 8/8 |
| MYM | 5 | h4 | +0.065 | +0.007 .. +0.122 | +5.9% | +0.104 | 0.035 |  | 8/8 |
| MYM | 5 | h8 | +0.082 | -0.012 .. +0.176 | +5.2% | +0.155 | 0.1 |  | 4/8 |
| MYM | 5 | h16 | +0.089 | -0.005 .. +0.183 | +3.8% | +0.250 | 0.073 |  | 7/8 |
| MYM | 5 | eod | +0.732 | -0.051 .. +1.515 | +6.2% | +1.277 | 0.067 |  | 7/8 |
| MYM | 15 | h1 * | +0.031 | +0.015 .. +0.046 | +5.8% | +0.054 | 0.00013 | 0.0267 | 8/8 |
| MYM | 15 | h2 | +0.036 | +0.009 .. +0.063 | +4.7% | +0.068 | 0.0085 |  | 6/8 |
| MYM | 15 | h4 | +0.045 | -0.003 .. +0.093 | +4.1% | +0.110 | 0.064 |  | 5/8 |
| MYM | 15 | h8 | +0.153 | -0.077 .. +0.382 | +9.3% | +0.350 | 0.19 |  | 6/8 |
| MYM | 15 | h16 | +0.272 | -0.205 .. +0.750 | +11.1% | +0.709 | 0.27 |  | 3/8 |
| MYM | 15 | eod | +0.848 | -0.407 .. +2.103 | +14.1% | +1.254 | 0.19 |  | 6/8 |
| MYM | 60 | h1 | +0.018 | -0.000 .. +0.037 | +3.5% | +0.043 | 0.26 |  | 7/8 |
| MYM | 60 | h2 | +0.031 | +0.004 .. +0.057 | +4.0% | +0.065 | 0.2 |  | 6/8 |
| MYM | 60 | h4 | +0.034 | -0.002 .. +0.071 | +3.2% | +0.064 | 0.34 |  | 5/8 |
| MYM | 60 | h8 | +0.048 | -0.009 .. +0.105 | +3.1% | +0.063 | 0.36 |  | 5/8 |
| MYM | 60 | h16 | +0.051 | -0.027 .. +0.128 | +2.4% | +0.052 | 0.47 |  | 5/8 |
| MYM | 60 | eod * | +0.079 | -0.004 .. +0.161 | +3.5% | +0.067 | 0.18 | 1 | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.68 pts | +0.36 .. +1.01 | 4.2e-05 |
| MES | 15 | +0.32 pts | -0.22 .. +0.87 | 0.33 |
| MES | 60 | -0.04 pts | -1.16 .. +1.07 | 0.95 |
| MNQ | 5 | -0.18 pts | -0.54 .. +0.17 | 0.31 |
| MNQ | 15 | -0.21 pts | -0.80 .. +0.38 | 0.64 |
| MNQ | 60 | +1.17 pts | +0.02 .. +2.31 | 0.049 |
| MYM | 5 | +0.26 pts | -0.23 .. +0.76 | 0.29 |
| MYM | 15 | -0.00 pts | -0.71 .. +0.70 | 0.99 |
| MYM | 60 | -0.39 pts | -1.91 .. +1.12 | 0.82 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 170974 | +0.010 | 0.362 | +0.09 | -3.41 | -3.48 | -3.32 | -3.50 |
| MES | 5 | h2 | event | with signal | 170974 | +0.012 | 0.362 | +0.13 | -3.37 | -3.47 | -3.27 | -3.50 |
| MES | 5 | h4 | event | with signal | 170974 | +0.015 | 0.362 | +0.14 | -3.36 | -3.46 | -3.25 | -3.48 |
| MES | 5 | h8 | event | with signal | 170974 | +0.028 | 0.362 | +0.17 | -3.33 | -3.40 | -3.26 | -3.42 |
| MES | 5 | h16 | event | with signal | 170974 | +0.046 | 0.362 | +0.28 | -3.22 | -3.32 | -3.10 | -3.29 |
| MES | 5 | eod | event | against signal | 170974 | +0.246 | 0.362 | +1.55 | -1.95 | -2.89 | -0.88 | -3.62 |
| MES | 15 | h1 | event | against signal | 50270 | -0.001 | 0.204 | +0.06 | -3.44 | -3.53 | -3.34 | -3.31 |
| MES | 15 | h2 | event | against signal | 50270 | -0.002 | 0.204 | +0.06 | -3.44 | -3.55 | -3.32 | -3.32 |
| MES | 15 | h4 | event | with signal | 50270 | +0.009 | 0.204 | +0.02 | -3.48 | -3.37 | -3.59 | -3.55 |
| MES | 15 | h8 | event | with signal | 50270 | +0.006 | 0.204 | +0.11 | -3.39 | -3.43 | -3.36 | -3.37 |
| MES | 15 | h16 | event | with signal | 50270 | +0.008 | 0.204 | +0.18 | -3.32 | -3.27 | -3.38 | -2.96 |
| MES | 15 | eod | event | against signal | 50270 | +0.203 | 0.204 | +1.30 | -2.20 | -2.76 | -1.59 | -4.17 |
| MES | 60 | h1 | event | against signal | 12105 | +0.006 | 0.097 | +0.13 | -3.37 | -3.63 | -3.11 | -3.42 |
| MES | 60 | h2 | event | against signal | 12105 | +0.008 | 0.097 | +0.01 | -3.49 | -3.54 | -3.44 | -3.55 |
| MES | 60 | h4 | event | with signal | 12105 | -0.010 | 0.097 | +0.06 | -3.44 | -3.72 | -3.16 | -3.30 |
| MES | 60 | h8 | event | with signal | 12105 | -0.019 | 0.097 | -0.52 | -4.02 | -4.37 | -3.66 | -3.68 |
| MES | 60 | h16 | event | with signal | 12105 | -0.036 | 0.097 | -1.53 | -5.03 | -4.69 | -5.37 | -4.03 |
| MES | 60 | eod | event | with signal | 12105 | -0.019 | 0.097 | -0.21 | -3.71 | -4.49 | -2.92 | -2.85 |
| MNQ | 5 | h1 | event | against signal | 146890 | +0.008 | 0.140 | +0.06 | -1.94 | -1.95 | -1.94 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 146890 | +0.011 | 0.140 | +0.05 | -1.95 | -1.95 | -1.96 | -1.89 |
| MNQ | 5 | h4 | event | against signal | 146890 | +0.017 | 0.140 | +0.13 | -1.87 | -1.91 | -1.82 | -1.88 |
| MNQ | 5 | h8 | event | with signal | 146890 | -0.013 | 0.140 | -0.13 | -2.13 | -2.10 | -2.16 | -1.98 |
| MNQ | 5 | h16 | event | with signal | 146890 | -0.022 | 0.140 | -0.13 | -2.13 | -2.17 | -2.09 | -1.85 |
| MNQ | 5 | eod | event | against signal | 146890 | +0.427 | 0.140 | +1.05 | -0.95 | -1.52 | -0.31 | -5.14 |
| MNQ | 15 | h1 | event | against signal | 46087 | +0.001 | 0.079 | +0.28 | -1.72 | -1.97 | -1.46 | -1.65 |
| MNQ | 15 | h2 | event | with signal | 46087 | +0.002 | 0.079 | -0.36 | -2.36 | -2.07 | -2.67 | -2.39 |
| MNQ | 15 | h4 | event | with signal | 46087 | +0.022 | 0.079 | -0.51 | -2.51 | -2.07 | -2.98 | -2.45 |
| MNQ | 15 | h8 | event | with signal | 46087 | +0.026 | 0.079 | -0.83 | -2.83 | -2.08 | -3.61 | -2.49 |
| MNQ | 15 | h16 | event | with signal | 46087 | -0.038 | 0.079 | -0.66 | -2.66 | -1.86 | -3.50 | -1.93 |
| MNQ | 15 | eod | event | against signal | 46087 | +0.408 | 0.079 | +2.87 | +0.87 | -1.14 | +2.97 | -2.05 |
| MNQ | 60 | h1 | event | with signal | 11784 | -0.004 | 0.039 | -0.45 | -2.45 | -1.95 | -2.97 | -2.17 |
| MNQ | 60 | h2 | event | with signal | 11784 | +0.002 | 0.039 | +0.30 | -1.70 | -1.84 | -1.56 | -1.37 |
| MNQ | 60 | h4 | event | with signal | 11784 | -0.015 | 0.039 | -0.22 | -2.22 | -1.95 | -2.51 | -1.65 |
| MNQ | 60 | h8 | event | against signal | 11784 | +0.038 | 0.039 | +0.67 | -1.33 | -1.44 | -1.22 | -2.23 |
| MNQ | 60 | h16 | event | against signal | 11784 | +0.112 | 0.039 | +2.82 | +0.82 | -0.54 | +2.23 | -0.68 |
| MNQ | 60 | eod | event | against signal | 11784 | +0.098 | 0.039 | +0.95 | -1.05 | -0.58 | -1.55 | -2.63 |
| MYM | 5 | h1 | event | against signal | 71869 | -0.006 | 0.175 | -0.03 | -2.03 | +nan | -2.03 | -1.96 |
| MYM | 5 | h2 | event | against signal | 71869 | -0.000 | 0.175 | -0.08 | -2.08 | +nan | -2.08 | -2.03 |
| MYM | 5 | h4 | event | against signal | 71869 | +0.013 | 0.175 | -0.09 | -2.09 | +nan | -2.09 | -2.12 |
| MYM | 5 | h8 | event | against signal | 71869 | +0.015 | 0.175 | -0.13 | -2.13 | +nan | -2.13 | -2.30 |
| MYM | 5 | h16 | event | with signal | 71869 | +0.011 | 0.175 | +0.50 | -1.50 | +nan | -1.50 | -1.27 |
| MYM | 5 | eod | event | against signal | 71869 | +0.642 | 0.175 | +1.45 | -0.55 | +nan | -0.55 | -2.00 |
| MYM | 15 | h1 | event | against signal | 22597 | -0.002 | 0.100 | +0.09 | -1.91 | +nan | -1.91 | -1.86 |
| MYM | 15 | h2 | event | against signal | 22597 | +0.003 | 0.100 | +0.10 | -1.90 | +nan | -1.90 | -1.90 |
| MYM | 15 | h4 | event | with signal | 22597 | -0.002 | 0.100 | +0.04 | -1.96 | +nan | -1.96 | -1.86 |
| MYM | 15 | h8 | event | against signal | 22597 | +0.108 | 0.100 | -0.08 | -2.08 | +nan | -2.08 | -2.34 |
| MYM | 15 | h16 | event | against signal | 22597 | +0.266 | 0.100 | +0.12 | -1.88 | +nan | -1.88 | -2.37 |
| MYM | 15 | eod | event | against signal | 22597 | +0.821 | 0.100 | +1.85 | -0.15 | +nan | -0.15 | -0.99 |
| MYM | 60 | h1 | event | against signal | 5835 | +0.022 | 0.049 | +0.54 | -1.46 | +nan | -1.46 | -1.53 |
| MYM | 60 | h2 | event | against signal | 5835 | +0.023 | 0.049 | +0.36 | -1.64 | +nan | -1.64 | -1.59 |
| MYM | 60 | h4 | event | with signal | 5835 | +0.004 | 0.049 | +1.02 | -0.98 | +nan | -0.98 | -0.97 |
| MYM | 60 | h8 | event | with signal | 5835 | +0.000 | 0.049 | +0.91 | -1.09 | +nan | -1.09 | -0.88 |
| MYM | 60 | h16 | event | with signal | 5835 | -0.031 | 0.049 | -0.73 | -2.73 | +nan | -2.73 | -1.43 |
| MYM | 60 | eod | event | with signal | 5835 | -0.027 | 0.049 | -0.70 | -2.70 | +nan | -2.70 | -1.49 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.249 | +1.147 | +0.993 | +0.738 | +0.496 | +0.000 | +0.033 | +0.036 | +0.042 | +0.058 | +0.082 |
| MES | 15 | +1.324 | +1.176 | +1.033 | +0.779 | +0.526 | +0.000 | +0.012 | +0.016 | +0.027 | +0.034 | +0.071 |
| MES | 60 | +1.323 | +1.242 | +1.127 | +0.872 | +0.597 | +0.000 | +0.000 | +0.003 | +0.013 | +0.031 | +0.060 |
| MNQ | 5 | +1.471 | +1.336 | +1.159 | +0.863 | +0.576 | +0.000 | +0.006 | +0.005 | +0.003 | +0.013 | +0.016 |
| MNQ | 15 | +1.443 | +1.266 | +1.112 | +0.839 | +0.563 | +0.000 | +0.000 | +0.006 | +0.031 | +0.053 | +0.013 |
| MNQ | 60 | +1.265 | +1.252 | +1.153 | +0.912 | +0.632 | +0.000 | +0.004 | +0.018 | +0.012 | +0.009 | -0.105 |
| MYM | 5 | +1.443 | +1.318 | +1.145 | +0.853 | +0.574 | +0.000 | +0.009 | +0.006 | -0.001 | +0.006 | +0.042 |
| MYM | 15 | +1.420 | +1.257 | +1.088 | +0.822 | +0.557 | +0.000 | -0.008 | -0.010 | -0.007 | -0.114 | -0.316 |
| MYM | 60 | +1.332 | +1.248 | +1.175 | +0.923 | +0.630 | +0.000 | -0.021 | -0.024 | +0.016 | +0.040 | -0.010 |

## Calibration

- MES 5-min: 1035403 bars, 170974 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 341350 bars, 50270 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 82606 bars, 12105 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1033654 bars, 146890 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 341194 bars, 46087 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 82604 bars, 11784 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 518605 bars, 71869 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170993 bars, 22597 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41251 bars, 5835 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.

## Plain-$ cross-check (zoo.dollar_check)

Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 units can overweight quiet bars at long holds; a direction claim must survive this check.

FINAL WORD: DIRECTION: R20 units only - NOT confirmed in plain $ (treat as none)

| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | 5 | dir_h16 | all | 170974 | CONFIDENTLY NOTHING | +0.25 | +0.39 | 0.17 | +2.4 | 3.50 |
| ES | 5 | dir_h16 | 2018-25H1 | 79938 | CONFIDENTLY NOTHING | +0.25 | +0.55 | 0.35 | +1.6 | 3.50 |
| ES | 15 | dir_h1 | all | 50270 | CONFIDENTLY NOTHING | +0.36 | -0.06 | 0.07 | -0.7 | 3.50 |
| ES | 15 | dir_h1 | 2018-25H1 | 24250 | CONFIDENTLY NOTHING | +0.36 | -0.16 | 0.15 | -1.0 | 3.50 |
| ES | 60 | dir_eod | all | 12105 | CONFIDENTLY NOTHING | +1.57 | +1.47 | 2.37 | +0.6 | 3.50 |
| ES | 60 | dir_eod | 2018-25H1 | 6038 | CONFIDENTLY NOTHING | +1.57 | +3.09 | 4.62 | +0.7 | 3.50 |
| NQ | 5 | dir_h1 | all | 146890 | REAL BUT TOO SMALL | +0.15 | -0.04 | 0.04 | -1.1 | 2.00 |
| NQ | 5 | dir_h1 | 2018-25H1 | 69580 | REAL BUT TOO SMALL | +0.15 | -0.03 | 0.08 | -0.4 | 2.00 |
| NQ | 15 | dir_eod | all | 46087 | INCONCLUSIVE | +0.60 | -1.24 | 2.08 | -0.6 | 2.00 |
| NQ | 15 | dir_eod | 2018-25H1 | 22498 | INCONCLUSIVE | +0.60 | -2.43 | 4.51 | -0.5 | 2.00 |
| NQ | 60 | dir_h16 | all | 11784 | INCONCLUSIVE | +1.97 | -0.64 | 3.30 | -0.2 | 2.00 |
| NQ | 60 | dir_h16 | 2018-25H1 | 5786 | INCONCLUSIVE | +1.97 | -0.70 | 6.65 | -0.1 | 2.00 |
| YM | 5 | dir_eod | all | 71869 | INCONCLUSIVE | +0.00 | -0.87 | 1.56 | -0.6 | 2.00 |
| YM | 5 | dir_eod | 2018-25H1 | 71869 | INCONCLUSIVE | +0.00 | -0.87 | 1.56 | -0.6 | 2.00 |
| YM | 15 | dir_eod | all | 22597 | INCONCLUSIVE | +1.01 | -1.07 | 2.73 | -0.4 | 2.00 |
| YM | 15 | dir_eod | 2018-25H1 | 22597 | INCONCLUSIVE | +1.01 | -1.07 | 2.73 | -0.4 | 2.00 |
| YM | 60 | dir_h1 | all | 5835 | INCONCLUSIVE | +0.47 | -0.49 | 0.49 | -1.0 | 2.00 |
| YM | 60 | dir_h1 | 2018-25H1 | 5835 | INCONCLUSIVE | +0.47 | -0.49 | 0.49 | -1.0 | 2.00 |
