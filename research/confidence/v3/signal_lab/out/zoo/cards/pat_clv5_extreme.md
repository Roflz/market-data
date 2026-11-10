# Impact card: pat_clv5_extreme

candle pattern clv5_extreme in its textbook direction: close within the bottom 10% of the last 5 bars' range -> bullish; top 10% -> bearish [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: POSSIBLE direction effect +0.007 average bars (~$0.11 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.0102, replicated in the other half=False, 15 of 16 years); best leg (event, with signal) grosses $+0.21 and nets $-3.29 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: the market moves 1% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.005 R20, possible, q=0.171, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.29 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.216 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=0.28; we would catch an effect of 0.022 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.46).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.86 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.124 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.017 R20 over the next 2 bars (2 h), p=0.68; we would catch an effect of 0.051 R20 or more 80% of the time).
- MES 60-min size: the market moves 4% LESS after the event than after matched bars over the next 2 bars (2 h) (-0.030 R20, CONFIRMED, q=0.0236, 13 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.98 at recent bar sizes, 90% range up to $3.73); about 1.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.012 R20 over the next 4 bars (20 min), p=0.044; we would catch an effect of 0.014 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.022 R20, CONFIRMED, q=2.17e-24, 13 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $0.84); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.015 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.014 R20, CONFIRMED, q=0.00166, 13 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.87 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.042 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.065 R20 over the next 16 bars (16 h), p=0.25; we would catch an effect of 0.055 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 4% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.023 R20, CONFIRMED, q=0.0215, 13 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.06 at recent bar sizes, 90% range up to $8.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: POSSIBLE direction effect +0.008 average bars (~$0.10 per micro at 2018-25 bar sizes) over the next 1 bar (5 min) (in the signal's direction), not confirmed (q=0.275, replicated in the other half=False, 6 of 8 years); best leg (event, with signal) grosses $+0.18 and nets $-1.82 per micro per trade after $2.00 costs -> not tradable on its own.
- MYM 5-min size: the market moves 4% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.019 R20, CONFIRMED, q=8.24e-08, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.23 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.168 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.007 R20 over the next 1 bar (15 min), p=0.97; we would catch an effect of 0.039 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.082).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.98 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.094 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.005 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.074 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.23 at recent bar sizes, 90% range up to $3.60); about 6.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.007 | +0.004 .. +0.010 | +0.0051 | 4.8e-05 / 2.4e-05 / 8.1e-06 | 0.00026 | 0.0102 | 0.018 | 15/16 | +0.006 | +0.007 | False | +4.5 / +4.1 |  |
| MES | 5 | h2 | +0.005 | -0.000 .. +0.009 | +0.0023 | 0.055 / 0.053 / 0.066 | 0.0656 |  |  | 10/16 | +0.005 | +0.004 |  | +2.1 / +1.9 |  |
| MES | 5 | h4 | -0.002 | -0.009 .. +0.005 | -0.0008 | 0.54 / 0.53 / 0.56 | 0.562 |  |  | 9/16 | -0.003 | -0.001 |  | -0.7 / -0.6 | 0.011 |
| MES | 5 | h8 | -0.009 | -0.020 .. +0.002 | -0.0021 | 0.12 / 0.13 / 0.16 | 0.158 |  |  | 11/16 | -0.001 | -0.017 |  | -2.0 / -1.6 |  |
| MES | 5 | h16 | -0.006 | -0.021 .. +0.010 | -0.0010 | 0.45 / 0.46 / 0.51 | 0.506 |  |  | 8/16 | +0.004 | -0.016 |  | -0.9 / -0.8 |  |
| MES | 5 | eod | +0.075 | -0.012 .. +0.162 | +0.0025 | 0.091 / 0.1 / 0.12 | 0.123 |  |  | 11/16 | +0.072 | +0.079 |  | +2.3 / +1.7 |  |
| MES | 15 | h1 * | +0.007 | +0.002 .. +0.013 | +0.0047 | 0.012 / 0.011 / 0.017 | 0.0175 | 1 | 0.908 | 12/16 | +0.009 | +0.006 | False | +2.5 / +2.5 |  |
| MES | 15 | h2 | +0.001 | -0.008 .. +0.011 | +0.0006 | 0.79 / 0.79 / 0.8 | 0.798 |  |  | 8/16 | +0.010 | -0.007 |  | +0.3 / +0.3 |  |
| MES | 15 | h4 | -0.000 | -0.015 .. +0.014 | -0.0000 | 0.99 / 0.99 / 0.99 | 0.993 |  |  | 8/16 | +0.009 | -0.009 |  | -0.0 / -0.0 | 0.022 |
| MES | 15 | h8 | +0.011 | -0.013 .. +0.034 | +0.0022 | 0.37 / 0.36 / 0.38 | 0.384 |  |  | 10/16 | +0.030 | -0.008 |  | +1.2 / +0.9 |  |
| MES | 15 | h16 | +0.019 | -0.014 .. +0.052 | +0.0026 | 0.26 / 0.26 / 0.3 | 0.294 |  |  | 11/16 | +0.064 | -0.026 |  | +1.4 / +1.1 |  |
| MES | 15 | eod | +0.045 | -0.042 .. +0.131 | +0.0023 | 0.31 / 0.3 / 0.35 | 0.343 |  |  | 10/16 | +0.080 | +0.010 |  | +1.4 / +1.0 |  |
| MES | 60 | h1 | -0.008 | -0.020 .. +0.005 | -0.0044 | 0.23 / 0.24 / 0.28 | 0.286 |  |  | 9/16 | -0.002 | -0.013 |  | -1.1 / -1.2 |  |
| MES | 60 | h2 * | -0.017 | -0.037 .. +0.002 | -0.0071 | 0.076 / 0.087 / 0.13 | 0.12 | 1 | 1 | 11/16 | -0.008 | -0.026 | False | -1.8 / -1.8 |  |
| MES | 60 | h4 | -0.022 | -0.052 .. +0.008 | -0.0063 | 0.16 / 0.17 / 0.23 | 0.233 |  |  | 9/16 | +0.006 | -0.049 |  | -1.6 / -1.4 | 0.051 |
| MES | 60 | h8 | -0.029 | -0.071 .. +0.013 | -0.0059 | 0.18 / 0.22 / 0.28 | 0.276 |  |  | 11/16 | +0.008 | -0.065 |  | -1.5 / -1.3 |  |
| MES | 60 | h16 | -0.044 | -0.097 .. +0.010 | -0.0072 | 0.11 / 0.13 / 0.18 | 0.185 |  |  | 9/16 | -0.006 | -0.082 |  | -1.9 / -1.6 |  |
| MES | 60 | eod | -0.045 | -0.100 .. +0.009 | -0.0072 | 0.1 / 0.12 / 0.17 | 0.175 |  |  | 9/16 | -0.011 | -0.080 |  | -1.9 / -1.6 |  |
| MNQ | 5 | h1 | +0.001 | -0.003 .. +0.005 | +0.0006 | 0.63 / 0.63 / 0.66 | 0.67 |  |  | 8/16 | +0.000 | +0.002 |  | +0.5 / +0.5 |  |
| MNQ | 5 | h2 | -0.001 | -0.006 .. +0.005 | -0.0003 | 0.74 / 0.75 / 0.76 | 0.749 |  |  | 7/16 | -0.000 | -0.001 |  | -0.4 / -0.3 |  |
| MNQ | 5 | h4 * | -0.012 | -0.020 .. -0.004 | -0.0028 | 0.0049 / 0.006 / 0.033 | 0.032 | 1 | 0.529 | 12/16 | -0.011 | -0.013 | False | -3.4 / -2.8 | 0.014 |
| MNQ | 5 | h8 | -0.019 | -0.032 .. -0.007 | -0.0031 | 0.003 / 0.0047 / 0.029 | 0.0281 |  |  | 11/16 | -0.008 | -0.030 |  | -3.7 / -3.0 |  |
| MNQ | 5 | h16 | -0.015 | -0.036 .. +0.005 | -0.0017 | 0.13 / 0.13 / 0.22 | 0.217 |  |  | 10/16 | -0.001 | -0.030 |  | -2.0 / -1.5 |  |
| MNQ | 5 | eod | +0.108 | +0.000 .. +0.216 | +0.0026 | 0.049 / 0.054 / 0.075 | 0.0787 |  |  | 11/16 | +0.176 | +0.040 |  | +2.5 / +2.0 |  |
| MNQ | 15 | h1 | -0.002 | -0.008 .. +0.004 | -0.0009 | 0.49 / 0.5 / 0.61 | 0.596 |  |  | 9/16 | -0.002 | -0.002 |  | -0.6 / -0.7 |  |
| MNQ | 15 | h2 | -0.008 | -0.017 .. +0.001 | -0.0024 | 0.078 / 0.087 / 0.26 | 0.247 |  |  | 11/16 | -0.006 | -0.010 |  | -1.8 / -1.8 |  |
| MNQ | 15 | h4 * | -0.015 | -0.031 .. +0.000 | -0.0027 | 0.05 / 0.061 / 0.24 | 0.244 | 1 | 0.999 | 12/16 | -0.014 | -0.016 | False | -2.3 / -2.0 | 0.037 |
| MNQ | 15 | h8 | -0.018 | -0.043 .. +0.007 | -0.0024 | 0.15 / 0.16 / 0.34 | 0.333 |  |  | 10/16 | -0.013 | -0.023 |  | -1.8 / -1.4 |  |
| MNQ | 15 | h16 | -0.010 | -0.047 .. +0.026 | -0.0011 | 0.59 / 0.59 / 0.68 | 0.669 |  |  | 10/16 | +0.028 | -0.048 |  | -0.7 / -0.5 |  |
| MNQ | 15 | eod | -0.011 | -0.108 .. +0.086 | -0.0005 | 0.82 / 0.82 / 0.87 | 0.868 |  |  | 8/16 | +0.050 | -0.072 |  | -0.3 / -0.2 |  |
| MNQ | 60 | h1 | -0.012 | -0.026 .. +0.001 | -0.0064 | 0.076 / 0.083 / 0.11 | 0.114 |  |  | 8/16 | -0.006 | -0.018 |  | -1.7 / -1.8 |  |
| MNQ | 60 | h2 | -0.020 | -0.041 .. +0.001 | -0.0075 | 0.061 / 0.065 / 0.1 | 0.0979 |  |  | 11/16 | -0.010 | -0.030 |  | -1.9 / -1.9 |  |
| MNQ | 60 | h4 | -0.034 | -0.066 .. -0.001 | -0.0090 | 0.043 / 0.044 / 0.08 | 0.0821 |  |  | 9/16 | +0.005 | -0.073 |  | -2.3 / -2.0 | 0.055 |
| MNQ | 60 | h8 | -0.047 | -0.095 .. +0.002 | -0.0091 | 0.06 / 0.066 / 0.089 | 0.0935 |  |  | 9/16 | -0.007 | -0.086 |  | -2.3 / -1.9 |  |
| MNQ | 60 | h16 * | -0.065 | -0.126 .. -0.005 | -0.0099 | 0.033 / 0.036 / 0.056 | 0.0581 | 1 | 0.993 | 10/16 | -0.017 | -0.114 | False | -2.7 / -2.1 |  |
| MNQ | 60 | eod | -0.065 | -0.126 .. -0.003 | -0.0094 | 0.039 / 0.041 / 0.061 | 0.0612 |  |  | 10/16 | -0.020 | -0.110 |  | -2.6 / -2.1 |  |
| MYM | 5 | h1 * | +0.008 | +0.003 .. +0.013 | +0.0045 | 0.0015 / 0.001 / 0.0053 | 0.00685 | 0.275 | 0.347 | 6/8 | n/a | +0.008 | False | +3.5 / +3.2 |  |
| MYM | 5 | h2 | +0.009 | +0.001 .. +0.018 | +0.0031 | 0.026 / 0.019 / 0.075 | 0.0817 |  |  | 5/8 | n/a | +0.009 |  | +2.8 / +2.2 |  |
| MYM | 5 | h4 | +0.009 | -0.004 .. +0.022 | +0.0018 | 0.19 / 0.17 / 0.35 | 0.351 |  |  | 4/8 | n/a | +0.009 |  | +1.8 / +1.3 | 0.020 |
| MYM | 5 | h8 | +0.001 | -0.021 .. +0.022 | +0.0001 | 0.96 / 0.96 / 1 | 1 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.0 |  |
| MYM | 5 | h16 | +0.004 | -0.024 .. +0.033 | +0.0005 | 0.77 / 0.76 / 0.83 | 0.836 |  |  | 5/8 | n/a | +0.004 |  | +0.4 / +0.3 |  |
| MYM | 5 | eod | +0.097 | -0.043 .. +0.237 | +0.0025 | 0.17 / 0.19 / 0.22 | 0.22 |  |  | 6/8 | n/a | +0.097 |  | +1.7 / +1.4 |  |
| MYM | 15 | h1 * | +0.007 | -0.002 .. +0.016 | +0.0034 | 0.15 / 0.13 / 0.21 | 0.22 | 1 | 1 | 7/8 | n/a | +0.007 | False | +1.5 / +1.5 |  |
| MYM | 15 | h2 | +0.003 | -0.012 .. +0.018 | +0.0009 | 0.66 / 0.64 / 0.75 | 0.752 |  |  | 4/8 | n/a | +0.003 |  | +0.5 / +0.4 |  |
| MYM | 15 | h4 | +0.007 | -0.015 .. +0.029 | +0.0011 | 0.54 / 0.54 / 0.7 | 0.68 |  |  | 5/8 | n/a | +0.007 |  | +0.7 / +0.6 | 0.039 |
| MYM | 15 | h8 | +0.016 | -0.016 .. +0.049 | +0.0021 | 0.32 / 0.34 / 0.52 | 0.506 |  |  | 6/8 | n/a | +0.016 |  | +1.2 / +1.0 |  |
| MYM | 15 | h16 | +0.002 | -0.048 .. +0.052 | +0.0002 | 0.93 / 0.94 / 0.96 | 0.96 |  |  | 3/8 | n/a | +0.002 |  | +0.1 / +0.1 |  |
| MYM | 15 | eod | +0.040 | -0.099 .. +0.178 | +0.0016 | 0.57 / 0.57 / 0.66 | 0.641 |  |  | 5/8 | n/a | +0.040 |  | +0.8 / +0.6 |  |
| MYM | 60 | h1 * | -0.005 | -0.024 .. +0.014 | -0.0032 | 0.59 / 0.59 / 0.63 | 0.64 | 1 | 1 | 4/8 | n/a | -0.005 | False | -0.5 / -0.5 |  |
| MYM | 60 | h2 | -0.004 | -0.034 .. +0.026 | -0.0017 | 0.8 / 0.8 / 0.82 | 0.826 |  |  | 4/8 | n/a | -0.004 |  | -0.3 / -0.3 |  |
| MYM | 60 | h4 | -0.013 | -0.062 .. +0.035 | -0.0038 | 0.6 / 0.59 / 0.62 | 0.617 |  |  | 6/8 | n/a | -0.013 |  | -0.6 / -0.5 | 0.074 |
| MYM | 60 | h8 | -0.006 | -0.074 .. +0.062 | -0.0012 | 0.86 / 0.86 / 0.88 | 0.868 |  |  | 5/8 | n/a | -0.006 |  | -0.2 / -0.2 |  |
| MYM | 60 | h16 | -0.015 | -0.102 .. +0.073 | -0.0024 | 0.74 / 0.74 / 0.76 | 0.753 |  |  | 6/8 | n/a | -0.015 |  | -0.4 / -0.3 |  |
| MYM | 60 | eod | -0.012 | -0.101 .. +0.077 | -0.0019 | 0.79 / 0.79 / 0.81 | 0.809 |  |  | 6/8 | n/a | -0.012 |  | -0.4 / -0.3 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.005 | +0.002 .. +0.008 | +1.0% | +0.022 | 0.001 | 0.171 | 12/16 |
| MES | 5 | h2 | -0.001 | -0.005 .. +0.003 | -0.2% | +0.009 | 0.56 |  | 9/16 |
| MES | 5 | h4 | -0.006 | -0.013 .. +0.000 | -0.6% | -0.003 | 0.2 |  | 10/16 |
| MES | 5 | h8 | -0.006 | -0.016 .. +0.005 | -0.4% | -0.014 | 0.8 |  | 10/16 |
| MES | 5 | h16 | -0.007 | -0.022 .. +0.009 | -0.3% | -0.021 | 0.74 |  | 10/16 |
| MES | 5 | eod | -0.009 | -0.156 .. +0.138 | -0.1% | +0.021 | 0.91 |  | 7/16 |
| MES | 15 | h1 * | +0.006 | +0.001 .. +0.011 | +1.2% | +0.018 | 0.076 | 1 | 13/16 |
| MES | 15 | h2 | +0.004 | -0.004 .. +0.012 | +0.6% | +0.017 | 0.51 |  | 11/16 |
| MES | 15 | h4 | +0.006 | -0.007 .. +0.020 | +0.6% | +0.013 | 0.52 |  | 11/16 |
| MES | 15 | h8 | +0.010 | -0.010 .. +0.029 | +0.6% | +0.010 | 0.61 |  | 12/16 |
| MES | 15 | h16 | +0.025 | -0.005 .. +0.056 | +1.1% | +0.021 | 0.1 |  | 12/16 |
| MES | 15 | eod | +0.055 | -0.074 .. +0.185 | +1.0% | +0.084 | 0.4 |  | 13/16 |
| MES | 60 | h1 | -0.020 | -0.031 .. -0.009 | -3.9% | -0.018 | 0.00025 |  | 12/16 |
| MES | 60 | h2 * | -0.030 | -0.046 .. -0.015 | -4.1% | -0.035 | 0.00012 | 0.0236 | 13/16 |
| MES | 60 | h4 | -0.026 | -0.048 .. -0.004 | -2.5% | -0.038 | 0.02 |  | 7/16 |
| MES | 60 | h8 | -0.006 | -0.037 .. +0.025 | -0.4% | -0.029 | 0.69 |  | 6/16 |
| MES | 60 | h16 | -0.014 | -0.051 .. +0.023 | -0.7% | -0.036 | 0.46 |  | 9/16 |
| MES | 60 | eod | -0.010 | -0.049 .. +0.028 | -0.5% | -0.034 | 0.7 |  | 11/16 |
| MNQ | 5 | h1 * | +0.022 | +0.018 .. +0.026 | +4.1% | +0.046 | 3.3e-27 | 2.17e-24 | 13/16 |
| MNQ | 5 | h2 | +0.021 | +0.014 .. +0.028 | +2.7% | +0.043 | 3.7e-09 |  | 13/16 |
| MNQ | 5 | h4 | +0.023 | +0.010 .. +0.036 | +2.0% | +0.046 | 0.00061 |  | 14/16 |
| MNQ | 5 | h8 | +0.027 | +0.001 .. +0.052 | +1.7% | +0.050 | 0.039 |  | 14/16 |
| MNQ | 5 | h16 | +0.044 | -0.002 .. +0.090 | +1.8% | +0.068 | 0.058 |  | 13/16 |
| MNQ | 5 | eod | +0.258 | +0.010 .. +0.506 | +2.1% | +0.496 | 0.041 |  | 13/16 |
| MNQ | 15 | h1 * | +0.014 | +0.008 .. +0.021 | +2.7% | +0.028 | 7.1e-06 | 0.00166 | 13/16 |
| MNQ | 15 | h2 | +0.007 | -0.007 .. +0.021 | +0.9% | +0.021 | 0.43 |  | 11/16 |
| MNQ | 15 | h4 | +0.004 | -0.028 .. +0.035 | +0.3% | +0.010 | 0.83 |  | 12/16 |
| MNQ | 15 | h8 | +0.014 | -0.035 .. +0.062 | +0.8% | +0.012 | 0.57 |  | 11/16 |
| MNQ | 15 | h16 | +0.032 | -0.021 .. +0.085 | +1.3% | +0.020 | 0.24 |  | 12/16 |
| MNQ | 15 | eod | +0.017 | -0.204 .. +0.238 | +0.3% | +0.059 | 0.88 |  | 11/16 |
| MNQ | 60 | h1 * | -0.023 | -0.034 .. -0.012 | -4.4% | -0.032 | 0.00011 | 0.0215 | 13/16 |
| MNQ | 60 | h2 | -0.020 | -0.037 .. -0.004 | -2.7% | -0.040 | 0.038 |  | 11/16 |
| MNQ | 60 | h4 | -0.027 | -0.051 .. -0.004 | -2.5% | -0.046 | 0.039 |  | 11/16 |
| MNQ | 60 | h8 | -0.012 | -0.043 .. +0.018 | -0.8% | -0.041 | 0.51 |  | 8/16 |
| MNQ | 60 | h16 | -0.013 | -0.051 .. +0.026 | -0.6% | -0.036 | 0.74 |  | 7/16 |
| MNQ | 60 | eod | -0.010 | -0.049 .. +0.030 | -0.4% | -0.035 | 0.87 |  | 8/16 |
| MYM | 5 | h1 * | +0.019 | +0.013 .. +0.025 | +3.7% | +0.049 | 2.6e-10 | 8.24e-08 | 7/8 |
| MYM | 5 | h2 | +0.021 | +0.010 .. +0.031 | +2.7% | +0.048 | 0.00018 |  | 7/8 |
| MYM | 5 | h4 | +0.015 | -0.008 .. +0.038 | +1.4% | +0.040 | 0.2 |  | 6/8 |
| MYM | 5 | h8 | +0.019 | -0.023 .. +0.061 | +1.2% | +0.034 | 0.38 |  | 6/8 |
| MYM | 5 | h16 | +0.030 | -0.028 .. +0.088 | +1.3% | +0.030 | 0.32 |  | 6/8 |
| MYM | 5 | eod | +0.135 | -0.135 .. +0.406 | +1.2% | +0.283 | 0.34 |  | 7/8 |
| MYM | 15 | h1 * | +0.013 | +0.005 .. +0.022 | +2.5% | +0.031 | 0.014 | 1 | 7/8 |
| MYM | 15 | h2 | +0.017 | -0.002 .. +0.036 | +2.2% | +0.028 | 0.18 |  | 5/8 |
| MYM | 15 | h4 | +0.018 | -0.020 .. +0.056 | +1.6% | +0.029 | 0.43 |  | 6/8 |
| MYM | 15 | h8 | +0.012 | -0.043 .. +0.068 | +0.7% | +0.013 | 0.86 |  | 6/8 |
| MYM | 15 | h16 | +0.012 | -0.088 .. +0.111 | +0.5% | +0.004 | 0.86 |  | 6/8 |
| MYM | 15 | eod | -0.022 | -0.280 .. +0.235 | -0.4% | -0.001 | 0.87 |  | 3/8 |
| MYM | 60 | h1 * | +0.011 | -0.005 .. +0.028 | +2.2% | +0.018 | 0.24 | 1 | 4/8 |
| MYM | 60 | h2 | +0.007 | -0.018 .. +0.032 | +0.9% | +0.016 | 0.85 |  | 4/8 |
| MYM | 60 | h4 | +0.005 | -0.029 .. +0.039 | +0.5% | +0.002 | 0.95 |  | 5/8 |
| MYM | 60 | h8 | +0.022 | -0.024 .. +0.069 | +1.4% | +0.008 | 0.44 |  | 5/8 |
| MYM | 60 | h16 | +0.014 | -0.037 .. +0.066 | +0.7% | +0.002 | 0.73 |  | 4/8 |
| MYM | 60 | eod | +0.016 | -0.036 .. +0.067 | +0.7% | +0.005 | 0.68 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.70 pts | +0.46 .. +0.95 | 1.9e-07 |
| MES | 15 | +0.67 pts | +0.27 .. +1.06 | 0.0022 |
| MES | 60 | -0.12 pts | -1.01 .. +0.76 | 0.86 |
| MNQ | 5 | +0.46 pts | +0.22 .. +0.70 | 0.001 |
| MNQ | 15 | +0.10 pts | -0.29 .. +0.48 | 0.63 |
| MNQ | 60 | -0.77 pts | -1.64 .. +0.11 | 0.087 |
| MYM | 5 | +0.50 pts | +0.14 .. +0.86 | 0.0067 |
| MYM | 15 | +0.57 pts | +0.04 .. +1.10 | 0.058 |
| MYM | 60 | -0.61 pts | -1.71 .. +0.49 | 0.43 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | with signal | 224342 | +0.017 | 0.323 | +0.21 | -3.29 | -3.39 | -3.20 | -3.41 |
| MES | 5 | h2 | event | with signal | 224342 | +0.019 | 0.323 | +0.24 | -3.26 | -3.37 | -3.15 | -3.42 |
| MES | 5 | h4 | event | against signal | 224342 | -0.012 | 0.323 | -0.13 | -3.63 | -3.58 | -3.69 | -3.47 |
| MES | 5 | h8 | event | against signal | 224342 | -0.003 | 0.323 | +0.01 | -3.49 | -3.57 | -3.41 | -3.35 |
| MES | 5 | h16 | event | against signal | 224342 | -0.006 | 0.323 | -0.01 | -3.51 | -3.57 | -3.45 | -3.37 |
| MES | 5 | eod | event | with signal | 224342 | +0.027 | 0.323 | +0.05 | -3.45 | -3.50 | -3.40 | -2.98 |
| MES | 15 | h1 | event | with signal | 66137 | +0.015 | 0.179 | +0.26 | -3.24 | -3.30 | -3.18 | -3.39 |
| MES | 15 | h2 | event | with signal | 66137 | +0.009 | 0.179 | +0.09 | -3.41 | -3.32 | -3.49 | -3.58 |
| MES | 15 | h4 | event | against signal | 66137 | -0.006 | 0.179 | -0.04 | -3.54 | -3.62 | -3.48 | -3.40 |
| MES | 15 | h8 | event | with signal | 66137 | +0.015 | 0.179 | +0.10 | -3.40 | -3.30 | -3.48 | -3.50 |
| MES | 15 | h16 | event | with signal | 66137 | +0.015 | 0.179 | +0.06 | -3.44 | -3.09 | -3.75 | -3.42 |
| MES | 15 | eod | event | with signal | 66137 | -0.015 | 0.179 | +0.11 | -3.39 | -3.62 | -3.18 | -2.45 |
| MES | 60 | h1 | event | against signal | 14088 | +0.010 | 0.089 | +0.33 | -3.17 | -3.49 | -2.89 | -3.23 |
| MES | 60 | h2 | event | against signal | 14088 | +0.021 | 0.089 | +0.57 | -2.93 | -3.40 | -2.52 | -2.98 |
| MES | 60 | h4 | event | against signal | 14088 | +0.028 | 0.089 | +0.86 | -2.64 | -3.64 | -1.78 | -2.74 |
| MES | 60 | h8 | event | against signal | 14088 | +0.040 | 0.089 | +1.58 | -1.92 | -3.30 | -0.73 | -2.14 |
| MES | 60 | h16 | event | against signal | 14088 | +0.072 | 0.089 | +2.68 | -0.82 | -2.68 | +0.80 | -1.62 |
| MES | 60 | eod | event | against signal | 14088 | +0.070 | 0.089 | +2.56 | -0.94 | -2.66 | +0.57 | -1.54 |
| MNQ | 5 | h1 | event | with signal | 221664 | +0.005 | 0.130 | +0.12 | -1.88 | -1.96 | -1.79 | -1.94 |
| MNQ | 5 | h2 | event | against signal | 221664 | -0.005 | 0.130 | -0.15 | -2.15 | -2.06 | -2.26 | -2.05 |
| MNQ | 5 | h4 | event | against signal | 221664 | +0.009 | 0.130 | +0.06 | -1.94 | -2.00 | -1.87 | -1.89 |
| MNQ | 5 | h8 | event | against signal | 221664 | +0.025 | 0.130 | +0.24 | -1.76 | -1.97 | -1.53 | -1.82 |
| MNQ | 5 | h16 | event | against signal | 221664 | +0.027 | 0.130 | +0.32 | -1.68 | -1.92 | -1.42 | -1.83 |
| MNQ | 5 | eod | event | with signal | 221664 | +0.002 | 0.130 | +0.22 | -1.78 | -1.96 | -1.57 | -0.50 |
| MNQ | 15 | h1 | event | against signal | 67100 | -0.001 | 0.073 | -0.08 | -2.08 | -2.00 | -2.17 | -2.00 |
| MNQ | 15 | h2 | event | against signal | 67100 | +0.008 | 0.073 | +0.09 | -1.91 | -1.91 | -1.91 | -1.88 |
| MNQ | 15 | h4 | event | against signal | 67100 | +0.019 | 0.073 | +0.17 | -1.83 | -1.79 | -1.87 | -1.87 |
| MNQ | 15 | h8 | event | against signal | 67100 | +0.030 | 0.073 | +0.46 | -1.54 | -1.70 | -1.37 | -1.79 |
| MNQ | 15 | h16 | event | against signal | 67100 | +0.029 | 0.073 | +0.59 | -1.41 | -1.88 | -0.92 | -1.76 |
| MNQ | 15 | eod | event | against signal | 67100 | +0.093 | 0.073 | +0.82 | -1.18 | -1.50 | -0.85 | -2.59 |
| MNQ | 60 | h1 | event | against signal | 14406 | +0.017 | 0.036 | +0.92 | -1.08 | -1.73 | -0.43 | -1.26 |
| MNQ | 60 | h2 | event | against signal | 14406 | +0.027 | 0.036 | +1.38 | -0.62 | -1.68 | +0.43 | -0.82 |
| MNQ | 60 | h4 | event | against signal | 14406 | +0.045 | 0.036 | +2.84 | +0.84 | -1.99 | +3.68 | +0.56 |
| MNQ | 60 | h8 | event | against signal | 14406 | +0.065 | 0.036 | +4.37 | +2.37 | -1.54 | +6.30 | +1.93 |
| MNQ | 60 | h16 | event | against signal | 14406 | +0.098 | 0.036 | +5.70 | +3.70 | -1.16 | +8.58 | +2.76 |
| MNQ | 60 | eod | event | against signal | 14406 | +0.095 | 0.036 | +5.40 | +3.40 | -1.16 | +7.98 | +2.70 |
| MYM | 5 | h1 | event | with signal | 112454 | +0.015 | 0.168 | +0.18 | -1.82 | +nan | -1.82 | -1.91 |
| MYM | 5 | h2 | event | with signal | 112454 | +0.017 | 0.168 | +0.20 | -1.80 | +nan | -1.80 | -1.89 |
| MYM | 5 | h4 | event | with signal | 112454 | +0.015 | 0.168 | +0.11 | -1.89 | +nan | -1.89 | -1.96 |
| MYM | 5 | h8 | event | with signal | 112454 | +0.005 | 0.168 | -0.00 | -2.00 | +nan | -2.00 | -2.04 |
| MYM | 5 | h16 | event | with signal | 112454 | +0.010 | 0.168 | +0.04 | -1.96 | +nan | -1.96 | -2.01 |
| MYM | 5 | eod | event | with signal | 112454 | +0.077 | 0.168 | +0.27 | -1.73 | +nan | -1.73 | -1.57 |
| MYM | 15 | h1 | event | with signal | 33708 | +0.012 | 0.094 | +0.22 | -1.78 | +nan | -1.78 | -1.88 |
| MYM | 15 | h2 | event | with signal | 33708 | +0.007 | 0.094 | +0.05 | -1.95 | +nan | -1.95 | -2.02 |
| MYM | 15 | h4 | event | with signal | 33708 | +0.006 | 0.094 | +0.06 | -1.94 | +nan | -1.94 | -1.94 |
| MYM | 15 | h8 | event | with signal | 33708 | +0.014 | 0.094 | +0.35 | -1.65 | +nan | -1.65 | -1.61 |
| MYM | 15 | h16 | event | with signal | 33708 | -0.009 | 0.094 | +0.10 | -1.90 | +nan | -1.90 | -1.68 |
| MYM | 15 | eod | event | with signal | 33708 | +0.009 | 0.094 | +0.30 | -1.70 | +nan | -1.70 | -1.34 |
| MYM | 60 | h1 | event | against signal | 7213 | +0.008 | 0.046 | +0.28 | -1.72 | +nan | -1.72 | -1.78 |
| MYM | 60 | h2 | event | against signal | 7213 | +0.003 | 0.046 | -0.02 | -2.02 | +nan | -2.02 | -1.92 |
| MYM | 60 | h4 | event | against signal | 7213 | +0.013 | 0.046 | +0.50 | -1.50 | +nan | -1.50 | -1.38 |
| MYM | 60 | h8 | event | against signal | 7213 | +0.011 | 0.046 | +0.96 | -1.04 | +nan | -1.04 | -1.03 |
| MYM | 60 | h16 | event | against signal | 7213 | +0.043 | 0.046 | +2.06 | +0.06 | +nan | +0.06 | -0.82 |
| MYM | 60 | eod | event | against signal | 7213 | +0.039 | 0.046 | +2.01 | +0.01 | +nan | +0.01 | -0.79 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | +1.083 | +1.325 | +1.409 | +1.061 | +0.745 | +0.000 | +0.073 | +0.076 | +0.068 | +0.064 | +0.073 |
| MES | 15 | +1.229 | +1.434 | +1.512 | +1.144 | +0.795 | +0.000 | +0.038 | +0.034 | +0.035 | +0.053 | +0.070 |
| MES | 60 | +2.024 | +1.690 | +1.574 | +1.198 | +0.841 | +0.000 | -0.002 | -0.008 | +0.001 | +0.039 | +0.038 |
| MNQ | 5 | +1.244 | +1.508 | +1.604 | +1.203 | +0.833 | +0.000 | +0.032 | +0.033 | +0.020 | +0.007 | +0.004 |
| MNQ | 15 | +1.321 | +1.511 | +1.589 | +1.204 | +0.837 | +0.000 | +0.011 | +0.004 | -0.005 | -0.011 | +0.008 |
| MNQ | 60 | +2.171 | +1.784 | +1.627 | +1.237 | +0.870 | +0.000 | -0.011 | -0.014 | -0.020 | +0.014 | -0.016 |
| MYM | 5 | +1.207 | +1.475 | +1.584 | +1.182 | +0.812 | +0.000 | +0.028 | +0.031 | +0.031 | +0.023 | +0.032 |
| MYM | 15 | +1.285 | +1.505 | +1.595 | +1.201 | +0.828 | +0.000 | +0.016 | +0.012 | +0.011 | +0.022 | -0.003 |
| MYM | 60 | +2.128 | +1.757 | +1.655 | +1.266 | +0.881 | +0.000 | -0.007 | -0.003 | -0.005 | +0.042 | -0.048 |

## Calibration

- MES 5-min: 1036271 bars, 224342 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 66137 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 14088 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 221664 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 67100 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 14406 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 112454 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 33708 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 7213 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 45% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 36593 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
