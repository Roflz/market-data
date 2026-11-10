# Impact card: fam_breakout

any breakout pattern, textbook direction (both sides) [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: moves price AGAINST the signal 0.011 average bars (~$0.21 per micro at 2018-25 bar sizes) over the next 2 bars (10 min) (in the signal's direction), same sign in 14 of 16 years, q=0.012; best leg (event, against signal) grosses $+0.34 and nets $-3.16 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 5-min size: no measurable effect on how much price moves (best p=0.52).
- MES 5-min BOTTOM LINE (direction): REAL BUT TOO SMALL - the effect is confirmed but its 2018-25H1 per-trade edge ($+0.09, pessimistic $-0.01) does not clearly beat the $3.50 round trip: use it as a filter or for sizing only. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.031 R20 over the next 8 bars (2 h), p=0.1; we would catch an effect of 0.021 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.40 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.121 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.045 R20 over the next 8 bars (8 h), p=0.14; we would catch an effect of 0.039 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.092).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.51 at recent bar sizes, 90% range up to $4.16); about 2.8x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best -0.006 R20 over the next 2 bars (10 min), p=0.58; we would catch an effect of 0.013 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.40 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.075 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.009 R20 over the next 1 bar (15 min), p=0.17; we would catch an effect of 0.024 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.39 at recent bar sizes, 90% range up to $2.07); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.040 R20 over the next 8 bars (8 h), p=0.2; we would catch an effect of 0.039 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=0.46).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.58 at recent bar sizes, 90% range up to $6.33); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.104 R20 over the rest of the session (to 16:45), p=0.34; we would catch an effect of 0.018 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.22 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.160 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.008 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.035 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.64 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.095 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.013 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.052 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.37).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.54 at recent bar sizes, 90% range up to $2.16); about 1.2x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.007 | -0.011 .. -0.004 | -0.0042 | 0.0002 / 9.2e-05 / 0.00016 | 0.00104 |  |  | 15/16 | -0.007 | -0.008 |  | -3.8 / -3.7 |  |
| MES | 5 | h2 * | -0.011 | -0.017 .. -0.006 | -0.0045 | 2.6e-05 / 1.4e-05 / 0.0001 | 0.00026 | 0.012 | 0.01 | 14/16 | -0.015 | -0.008 | True | -4.2 / -4.2 |  |
| MES | 5 | h4 | -0.012 | -0.019 .. -0.004 | -0.0032 | 0.002 / 0.0015 / 0.0052 | 0.00495 |  |  | 13/16 | -0.017 | -0.006 |  | -3.1 / -3.1 | 0.011 |
| MES | 5 | h8 | -0.009 | -0.019 .. +0.002 | -0.0016 | 0.11 / 0.12 / 0.15 | 0.15 |  |  | 10/16 | -0.019 | +0.001 |  | -1.6 / -1.6 |  |
| MES | 5 | h16 | -0.003 | -0.018 .. +0.012 | -0.0004 | 0.72 / 0.73 / 0.76 | 0.771 |  |  | 10/16 | -0.014 | +0.009 |  | -0.3 / -0.4 |  |
| MES | 5 | eod | +0.012 | -0.058 .. +0.082 | +0.0003 | 0.74 / 0.74 / 0.75 | 0.755 |  |  | 7/16 | -0.044 | +0.068 |  | +0.3 / +0.3 |  |
| MES | 15 | h1 | -0.005 | -0.012 .. +0.001 | -0.0031 | 0.12 / 0.12 / 0.13 | 0.134 |  |  | 12/16 | -0.006 | -0.005 |  | -1.6 / -1.5 |  |
| MES | 15 | h2 | -0.011 | -0.020 .. -0.001 | -0.0042 | 0.023 / 0.019 / 0.037 | 0.0378 |  |  | 10/16 | -0.020 | -0.002 |  | -2.3 / -2.3 |  |
| MES | 15 | h4 | -0.019 | -0.033 .. -0.005 | -0.0050 | 0.0059 / 0.0048 / 0.012 | 0.0117 |  |  | 11/16 | -0.034 | -0.004 |  | -2.9 / -2.8 | 0.021 |
| MES | 15 | h8 * | -0.031 | -0.052 .. -0.010 | -0.0057 | 0.0035 / 0.0021 / 0.0036 | 0.00365 | 1 | 0.615 | 11/16 | -0.054 | -0.008 | False | -3.2 / -2.9 |  |
| MES | 15 | h16 | -0.033 | -0.062 .. -0.003 | -0.0042 | 0.032 / 0.028 / 0.03 | 0.0287 |  |  | 8/16 | -0.070 | +0.004 |  | -2.3 / -2.1 |  |
| MES | 15 | eod | -0.016 | -0.082 .. +0.050 | -0.0008 | 0.63 / 0.62 / 0.65 | 0.657 |  |  | 11/16 | -0.005 | -0.028 |  | -0.5 / -0.5 |  |
| MES | 60 | h1 | -0.007 | -0.021 .. +0.007 | -0.0041 | 0.33 / 0.31 / 0.36 | 0.362 |  |  | 10/16 | -0.000 | -0.014 |  | -0.9 / -1.0 |  |
| MES | 60 | h2 | -0.006 | -0.026 .. +0.013 | -0.0025 | 0.53 / 0.53 / 0.54 | 0.536 |  |  | 11/16 | +0.003 | -0.016 |  | -0.6 / -0.6 |  |
| MES | 60 | h4 | -0.017 | -0.044 .. +0.009 | -0.0049 | 0.21 / 0.2 / 0.21 | 0.204 |  |  | 10/16 | -0.003 | -0.032 |  | -1.2 / -1.3 | 0.039 |
| MES | 60 | h8 * | -0.045 | -0.079 .. -0.011 | -0.0094 | 0.0096 / 0.012 / 0.02 | 0.0193 | 1 | 0.866 | 11/16 | -0.008 | -0.082 | False | -2.3 / -2.6 |  |
| MES | 60 | h16 | -0.033 | -0.074 .. +0.008 | -0.0052 | 0.12 / 0.12 / 0.17 | 0.177 |  |  | 9/16 | -0.000 | -0.065 |  | -1.4 / -1.6 |  |
| MES | 60 | eod | -0.028 | -0.071 .. +0.015 | -0.0043 | 0.2 / 0.19 / 0.25 | 0.25 |  |  | 9/16 | +0.009 | -0.066 |  | -1.2 / -1.3 |  |
| MNQ | 5 | h1 | -0.003 | -0.007 .. +0.000 | -0.0019 | 0.064 / 0.063 / 0.1 | 0.104 |  |  | 9/16 | +0.002 | -0.009 |  | -2.0 / -1.9 |  |
| MNQ | 5 | h2 * | -0.006 | -0.012 .. -0.001 | -0.0023 | 0.013 / 0.015 / 0.052 | 0.0563 | 1 | 0.945 | 12/16 | -0.003 | -0.010 | False | -2.6 / -2.5 |  |
| MNQ | 5 | h4 | -0.007 | -0.014 .. -0.000 | -0.0017 | 0.042 / 0.048 / 0.16 | 0.161 |  |  | 11/16 | -0.004 | -0.010 |  | -2.0 / -2.0 | 0.013 |
| MNQ | 5 | h8 | -0.006 | -0.016 .. +0.003 | -0.0010 | 0.19 / 0.21 / 0.4 | 0.399 |  |  | 11/16 | -0.010 | -0.002 |  | -1.2 / -1.3 |  |
| MNQ | 5 | h16 | +0.000 | -0.014 .. +0.015 | +0.0000 | 0.98 / 0.98 / 0.97 | 0.97 |  |  | 8/16 | +0.006 | -0.005 |  | +0.0 / +0.0 |  |
| MNQ | 5 | eod | +0.024 | -0.059 .. +0.107 | +0.0006 | 0.56 / 0.56 / 0.59 | 0.601 |  |  | 8/16 | +0.013 | +0.035 |  | +0.6 / +0.6 |  |
| MNQ | 15 | h1 * | -0.009 | -0.015 .. -0.003 | -0.0044 | 0.0049 / 0.0029 / 0.023 | 0.0266 | 1 | 0.204 | 13/16 | -0.011 | -0.006 | False | -2.7 / -2.8 |  |
| MNQ | 15 | h2 | -0.012 | -0.021 .. -0.003 | -0.0037 | 0.0057 / 0.004 / 0.057 | 0.0625 |  |  | 12/16 | -0.023 | -0.001 |  | -2.7 / -2.8 |  |
| MNQ | 15 | h4 | -0.022 | -0.034 .. -0.009 | -0.0040 | 0.00066 / 0.00051 / 0.051 | 0.0555 |  |  | 14/16 | -0.027 | -0.017 |  | -3.4 / -3.4 | 0.024 |
| MNQ | 15 | h8 | -0.030 | -0.049 .. -0.011 | -0.0042 | 0.0016 / 0.00096 / 0.04 | 0.0432 |  |  | 13/16 | -0.036 | -0.024 |  | -3.2 / -3.2 |  |
| MNQ | 15 | h16 | -0.033 | -0.060 .. -0.006 | -0.0038 | 0.016 / 0.015 / 0.056 | 0.0542 |  |  | 12/16 | -0.046 | -0.020 |  | -2.3 / -2.4 |  |
| MNQ | 15 | eod | +0.019 | -0.047 .. +0.086 | +0.0008 | 0.56 / 0.56 / 0.68 | 0.681 |  |  | 9/16 | +0.007 | +0.032 |  | +0.6 / +0.6 |  |
| MNQ | 60 | h1 | -0.002 | -0.017 .. +0.012 | -0.0014 | 0.75 / 0.75 / 0.75 | 0.76 |  |  | 8/16 | -0.006 | +0.001 |  | -0.3 / -0.3 |  |
| MNQ | 60 | h2 | -0.009 | -0.029 .. +0.011 | -0.0037 | 0.38 / 0.39 / 0.39 | 0.383 |  |  | 10/16 | -0.010 | -0.008 |  | -0.8 / -0.9 |  |
| MNQ | 60 | h4 | -0.019 | -0.045 .. +0.007 | -0.0054 | 0.16 / 0.17 / 0.18 | 0.178 |  |  | 9/16 | -0.013 | -0.025 |  | -1.3 / -1.4 | 0.039 |
| MNQ | 60 | h8 * | -0.040 | -0.075 .. -0.004 | -0.0083 | 0.029 / 0.033 / 0.044 | 0.0471 | 1 | 0.99 | 11/16 | -0.036 | -0.044 | False | -2.0 / -2.2 |  |
| MNQ | 60 | h16 | -0.040 | -0.087 .. +0.008 | -0.0064 | 0.1 / 0.093 / 0.11 | 0.115 |  |  | 10/16 | -0.024 | -0.055 |  | -1.6 / -1.6 |  |
| MNQ | 60 | eod | -0.042 | -0.089 .. +0.006 | -0.0064 | 0.086 / 0.08 / 0.1 | 0.101 |  |  | 11/16 | -0.025 | -0.058 |  | -1.7 / -1.7 |  |
| MYM | 5 | h1 | -0.003 | -0.007 .. +0.002 | -0.0014 | 0.3 / 0.3 / 0.5 | 0.502 |  |  | 4/8 | n/a | -0.003 |  | -1.1 / -1.0 |  |
| MYM | 5 | h2 | -0.005 | -0.012 .. +0.001 | -0.0018 | 0.11 / 0.1 / 0.31 | 0.311 |  |  | 5/8 | n/a | -0.005 |  | -1.6 / -1.6 |  |
| MYM | 5 | h4 | -0.008 | -0.017 .. +0.002 | -0.0016 | 0.11 / 0.11 / 0.37 | 0.382 |  |  | 6/8 | n/a | -0.008 |  | -1.6 / -1.6 | 0.018 |
| MYM | 5 | h8 | -0.006 | -0.021 .. +0.008 | -0.0009 | 0.39 / 0.38 / 0.59 | 0.596 |  |  | 7/8 | n/a | -0.006 |  | -0.9 / -0.9 |  |
| MYM | 5 | h16 | +0.001 | -0.017 .. +0.020 | +0.0002 | 0.88 / 0.88 / 0.91 | 0.917 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.2 |  |
| MYM | 5 | eod * | +0.104 | -0.001 .. +0.209 | +0.0026 | 0.053 / 0.057 / 0.079 | 0.0838 | 1 | 1 | 6/8 | n/a | +0.104 | False | +1.9 / +1.9 |  |
| MYM | 15 | h1 | -0.004 | -0.012 .. +0.004 | -0.0022 | 0.35 / 0.37 / 0.47 | 0.468 |  |  | 4/8 | n/a | -0.004 |  | -0.9 / -0.9 |  |
| MYM | 15 | h2 | -0.001 | -0.013 .. +0.011 | -0.0003 | 0.88 / 0.88 / 0.92 | 0.912 |  |  | 4/8 | n/a | -0.001 |  | -0.2 / -0.1 |  |
| MYM | 15 | h4 * | -0.008 | -0.026 .. +0.010 | -0.0015 | 0.37 / 0.38 / 0.61 | 0.595 | 1 | 1 | 4/8 | n/a | -0.008 | False | -0.9 / -0.9 | 0.035 |
| MYM | 15 | h8 | -0.009 | -0.034 .. +0.016 | -0.0013 | 0.46 / 0.47 / 0.64 | 0.645 |  |  | 6/8 | n/a | -0.009 |  | -0.7 / -0.7 |  |
| MYM | 15 | h16 | +0.003 | -0.033 .. +0.038 | +0.0003 | 0.88 / 0.88 / 0.92 | 0.92 |  |  | 4/8 | n/a | +0.003 |  | +0.1 / +0.1 |  |
| MYM | 15 | eod | -0.004 | -0.093 .. +0.084 | -0.0002 | 0.92 / 0.92 / 0.94 | 0.935 |  |  | 5/8 | n/a | -0.004 |  | -0.1 / -0.1 |  |
| MYM | 60 | h1 * | +0.013 | -0.005 .. +0.031 | +0.0079 | 0.16 / 0.18 / 0.21 | 0.204 | 1 | 1 | 6/8 | n/a | +0.013 | False | +1.3 / +1.4 |  |
| MYM | 60 | h2 | +0.011 | -0.013 .. +0.036 | +0.0049 | 0.36 / 0.37 / 0.41 | 0.409 |  |  | 6/8 | n/a | +0.011 |  | +0.8 / +0.9 |  |
| MYM | 60 | h4 | +0.018 | -0.017 .. +0.053 | +0.0056 | 0.3 / 0.31 / 0.32 | 0.325 |  |  | 5/8 | n/a | +0.018 |  | +1.0 / +1.0 | 0.052 |
| MYM | 60 | h8 | +0.009 | -0.041 .. +0.059 | +0.0020 | 0.73 / 0.73 / 0.73 | 0.721 |  |  | 4/8 | n/a | +0.009 |  | +0.3 / +0.3 |  |
| MYM | 60 | h16 | -0.010 | -0.070 .. +0.051 | -0.0016 | 0.76 / 0.77 / 0.76 | 0.752 |  |  | 4/8 | n/a | -0.010 |  | -0.3 / -0.3 |  |
| MYM | 60 | eod | -0.014 | -0.076 .. +0.049 | -0.0022 | 0.67 / 0.68 / 0.67 | 0.668 |  |  | 4/8 | n/a | -0.014 |  | -0.4 / -0.4 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | -0.000 .. +0.007 | +0.7% | +0.007 | 0.43 |  | 12/16 |
| MES | 5 | h2 | +0.002 | -0.003 .. +0.006 | +0.2% | +0.001 | 0.95 |  | 9/16 |
| MES | 5 | h4 | +0.001 | -0.005 .. +0.008 | +0.1% | -0.005 | 0.7 |  | 10/16 |
| MES | 5 | h8 | -0.004 | -0.015 .. +0.007 | -0.3% | -0.012 | 0.5 |  | 8/16 |
| MES | 5 | h16 | -0.005 | -0.022 .. +0.011 | -0.3% | -0.026 | 0.53 |  | 8/16 |
| MES | 5 | eod * | -0.147 | -0.316 .. +0.021 | -1.5% | -0.331 | 0.087 | 1 | 9/16 |
| MES | 15 | h1 | -0.001 | -0.007 .. +0.004 | -0.3% | -0.001 | 0.61 |  | 8/16 |
| MES | 15 | h2 | -0.001 | -0.009 .. +0.007 | -0.1% | -0.006 | 0.8 |  | 8/16 |
| MES | 15 | h4 | -0.005 | -0.018 .. +0.007 | -0.5% | -0.011 | 0.42 |  | 6/16 |
| MES | 15 | h8 * | -0.008 | -0.027 .. +0.010 | -0.6% | -0.023 | 0.37 | 1 | 7/16 |
| MES | 15 | h16 | -0.007 | -0.038 .. +0.024 | -0.3% | -0.039 | 0.67 |  | 7/16 |
| MES | 15 | eod | -0.042 | -0.168 .. +0.084 | -0.8% | -0.130 | 0.52 |  | 7/16 |
| MES | 60 | h1 | +0.006 | -0.005 .. +0.018 | +1.2% | +0.008 | 0.28 |  | 10/16 |
| MES | 60 | h2 | +0.001 | -0.014 .. +0.016 | +0.1% | +0.003 | 0.91 |  | 7/16 |
| MES | 60 | h4 | +0.001 | -0.019 .. +0.021 | +0.1% | -0.005 | 0.91 |  | 5/16 |
| MES | 60 | h8 | -0.004 | -0.029 .. +0.020 | -0.3% | +0.005 | 0.78 |  | 10/16 |
| MES | 60 | h16 | -0.035 | -0.063 .. -0.006 | -1.7% | -0.025 | 0.024 |  | 10/16 |
| MES | 60 | eod * | -0.038 | -0.068 .. -0.008 | -1.7% | -0.032 | 0.015 | 1 | 11/16 |
| MNQ | 5 | h1 | +0.002 | -0.002 .. +0.005 | +0.3% | +0.006 | 0.55 |  | 10/16 |
| MNQ | 5 | h2 | -0.001 | -0.007 .. +0.005 | -0.1% | -0.003 | 0.72 |  | 7/16 |
| MNQ | 5 | h4 | -0.003 | -0.016 .. +0.009 | -0.3% | -0.013 | 0.61 |  | 5/16 |
| MNQ | 5 | h8 * | -0.014 | -0.040 .. +0.011 | -0.9% | -0.026 | 0.27 | 1 | 8/16 |
| MNQ | 5 | h16 | -0.020 | -0.066 .. +0.027 | -0.8% | -0.048 | 0.4 |  | 5/16 |
| MNQ | 5 | eod | -0.135 | -0.400 .. +0.129 | -1.1% | -0.382 | 0.32 |  | 9/16 |
| MNQ | 15 | h1 | +0.001 | -0.005 .. +0.006 | +0.1% | -0.001 | 0.92 |  | 10/16 |
| MNQ | 15 | h2 | +0.003 | -0.009 .. +0.016 | +0.4% | -0.003 | 0.94 |  | 13/16 |
| MNQ | 15 | h4 | -0.002 | -0.032 .. +0.028 | -0.2% | -0.012 | 0.91 |  | 4/16 |
| MNQ | 15 | h8 | -0.004 | -0.050 .. +0.041 | -0.2% | -0.028 | 0.86 |  | 4/16 |
| MNQ | 15 | h16 | -0.007 | -0.057 .. +0.043 | -0.3% | -0.057 | 0.78 |  | 5/16 |
| MNQ | 15 | eod * | -0.057 | -0.272 .. +0.159 | -0.9% | -0.131 | 0.61 | 1 | 5/16 |
| MNQ | 60 | h1 | +0.008 | -0.004 .. +0.019 | +1.4% | +0.016 | 0.19 |  | 10/16 |
| MNQ | 60 | h2 * | +0.015 | -0.002 .. +0.031 | +1.9% | +0.025 | 0.077 | 1 | 12/16 |
| MNQ | 60 | h4 | +0.016 | -0.005 .. +0.037 | +1.4% | +0.023 | 0.14 |  | 11/16 |
| MNQ | 60 | h8 | +0.020 | -0.004 .. +0.045 | +1.3% | +0.026 | 0.12 |  | 11/16 |
| MNQ | 60 | h16 | +0.007 | -0.023 .. +0.036 | +0.3% | +0.009 | 0.78 |  | 9/16 |
| MNQ | 60 | eod | +0.003 | -0.028 .. +0.034 | +0.1% | +0.008 | 0.9 |  | 6/16 |
| MYM | 5 | h1 | +0.005 | +0.000 .. +0.010 | +0.9% | +0.012 | 0.86 |  | 6/8 |
| MYM | 5 | h2 | -0.001 | -0.010 .. +0.009 | -0.1% | +0.001 | 0.9 |  | 3/8 |
| MYM | 5 | h4 | -0.004 | -0.026 .. +0.019 | -0.3% | -0.007 | 0.76 |  | 2/8 |
| MYM | 5 | h8 | -0.011 | -0.052 .. +0.031 | -0.7% | -0.020 | 0.61 |  | 2/8 |
| MYM | 5 | h16 | -0.014 | -0.072 .. +0.044 | -0.6% | -0.035 | 0.64 |  | 1/8 |
| MYM | 5 | eod * | -0.148 | -0.424 .. +0.129 | -1.3% | -0.341 | 0.29 | 1 | 5/8 |
| MYM | 15 | h1 | +0.002 | -0.006 .. +0.011 | +0.5% | -0.002 | 0.77 |  | 6/8 |
| MYM | 15 | h2 | -0.001 | -0.018 .. +0.016 | -0.1% | -0.005 | 0.92 |  | 4/8 |
| MYM | 15 | h4 | -0.005 | -0.040 .. +0.030 | -0.4% | -0.013 | 0.79 |  | 1/8 |
| MYM | 15 | h8 * | -0.011 | -0.066 .. +0.044 | -0.7% | -0.030 | 0.69 | 1 | 2/8 |
| MYM | 15 | h16 | -0.003 | -0.103 .. +0.096 | -0.1% | -0.033 | 0.95 |  | 2/8 |
| MYM | 15 | eod | +0.019 | -0.243 .. +0.280 | +0.3% | -0.045 | 0.89 |  | 7/8 |
| MYM | 60 | h1 * | +0.016 | +0.002 .. +0.030 | +3.0% | +0.020 | 0.061 | 1 | 5/8 |
| MYM | 60 | h2 | -0.003 | -0.023 .. +0.018 | -0.4% | +0.009 | 0.79 |  | 3/8 |
| MYM | 60 | h4 | +0.013 | -0.016 .. +0.041 | +1.2% | +0.013 | 0.38 |  | 5/8 |
| MYM | 60 | h8 | +0.013 | -0.023 .. +0.049 | +0.8% | +0.022 | 0.49 |  | 5/8 |
| MYM | 60 | h16 | -0.009 | -0.053 .. +0.035 | -0.4% | -0.002 | 0.71 |  | 4/8 |
| MYM | 60 | eod | -0.012 | -0.057 .. +0.033 | -0.5% | -0.006 | 0.6 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.38 pts | -0.63 .. -0.14 | 0.0051 |
| MES | 15 | -0.45 pts | -0.85 .. -0.06 | 0.027 |
| MES | 60 | -0.57 pts | -1.31 .. +0.18 | 0.15 |
| MNQ | 5 | -0.35 pts | -0.57 .. -0.12 | 0.0042 |
| MNQ | 15 | -0.41 pts | -0.76 .. -0.07 | 0.031 |
| MNQ | 60 | +0.03 pts | -0.71 .. +0.78 | 1 |
| MYM | 5 | -0.29 pts | -0.59 .. +0.00 | 0.056 |
| MYM | 15 | -0.41 pts | -0.90 .. +0.07 | 0.18 |
| MYM | 60 | +0.17 pts | -0.76 .. +1.10 | 0.83 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 144293 | +0.019 | 0.251 | +0.23 | -3.27 | -3.35 | -3.23 | -3.43 |
| MES | 5 | h2 | event | against signal | 144293 | +0.027 | 0.251 | +0.34 | -3.16 | -3.23 | -3.12 | -3.39 |
| MES | 5 | h4 | event | against signal | 144293 | +0.028 | 0.251 | +0.35 | -3.15 | -3.20 | -3.12 | -3.38 |
| MES | 5 | h8 | event | against signal | 144293 | +0.023 | 0.251 | +0.30 | -3.20 | -3.20 | -3.20 | -3.40 |
| MES | 5 | h16 | event | against signal | 144293 | +0.018 | 0.251 | +0.15 | -3.35 | -3.26 | -3.40 | -3.56 |
| MES | 5 | eod | event | with signal | 144293 | +0.015 | 0.251 | +0.14 | -3.36 | -3.91 | -3.02 | -3.33 |
| MES | 15 | h1 | event | against signal | 57379 | +0.013 | 0.163 | +0.24 | -3.26 | -3.34 | -3.21 | -3.44 |
| MES | 15 | h2 | event | against signal | 57379 | +0.020 | 0.163 | +0.35 | -3.15 | -3.17 | -3.14 | -3.36 |
| MES | 15 | h4 | event | against signal | 57379 | +0.028 | 0.163 | +0.25 | -3.25 | -3.06 | -3.38 | -3.45 |
| MES | 15 | h8 | event | against signal | 57379 | +0.040 | 0.163 | +0.35 | -3.15 | -2.89 | -3.33 | -3.36 |
| MES | 15 | h16 | event | against signal | 57379 | +0.042 | 0.163 | +0.26 | -3.24 | -2.85 | -3.51 | -3.46 |
| MES | 15 | eod | event | against signal | 57379 | -0.002 | 0.163 | -0.05 | -3.55 | -3.64 | -3.49 | -3.25 |
| MES | 60 | h1 | event | against signal | 13823 | +0.007 | 0.088 | +0.48 | -3.02 | -3.57 | -2.58 | -3.02 |
| MES | 60 | h2 | event | against signal | 13823 | +0.008 | 0.088 | +0.56 | -2.94 | -3.71 | -2.30 | -3.02 |
| MES | 60 | h4 | event | against signal | 13823 | +0.020 | 0.088 | +1.38 | -2.12 | -3.55 | -0.94 | -2.25 |
| MES | 60 | h8 | event | against signal | 13823 | +0.048 | 0.088 | +1.95 | -1.55 | -3.54 | +0.09 | -1.75 |
| MES | 60 | h16 | event | against signal | 13823 | +0.023 | 0.088 | +0.76 | -2.74 | -3.95 | -1.74 | -2.46 |
| MES | 60 | eod | event | against signal | 13823 | +0.023 | 0.088 | +0.80 | -2.70 | -4.06 | -1.57 | -2.58 |
| MNQ | 5 | h1 | event | against signal | 207676 | +0.008 | 0.113 | +0.19 | -1.81 | -1.96 | -1.70 | -1.90 |
| MNQ | 5 | h2 | event | against signal | 207676 | +0.014 | 0.113 | +0.31 | -1.69 | -1.92 | -1.52 | -1.83 |
| MNQ | 5 | h4 | event | against signal | 207676 | +0.012 | 0.113 | +0.32 | -1.68 | -1.90 | -1.52 | -1.77 |
| MNQ | 5 | h8 | event | against signal | 207676 | +0.004 | 0.113 | +0.20 | -1.80 | -1.89 | -1.73 | -1.77 |
| MNQ | 5 | h16 | event | with signal | 207676 | +0.005 | 0.113 | -0.03 | -2.03 | -1.99 | -2.05 | -2.11 |
| MNQ | 5 | eod | event | with signal | 207676 | +0.043 | 0.113 | +0.38 | -1.62 | -1.84 | -1.45 | -1.77 |
| MNQ | 15 | h1 | event | against signal | 72642 | +0.012 | 0.069 | +0.24 | -1.76 | -1.90 | -1.64 | -1.86 |
| MNQ | 15 | h2 | event | against signal | 72642 | +0.013 | 0.069 | +0.18 | -1.82 | -1.80 | -1.84 | -1.87 |
| MNQ | 15 | h4 | event | against signal | 72642 | +0.020 | 0.069 | +0.18 | -1.82 | -1.84 | -1.81 | -1.80 |
| MNQ | 15 | h8 | event | against signal | 72642 | +0.024 | 0.069 | +0.28 | -1.72 | -1.79 | -1.66 | -1.57 |
| MNQ | 15 | h16 | event | against signal | 72642 | +0.029 | 0.069 | +0.61 | -1.39 | -1.69 | -1.15 | -1.35 |
| MNQ | 15 | eod | event | with signal | 72642 | +0.046 | 0.069 | +0.13 | -1.87 | -1.84 | -1.88 | -2.35 |
| MNQ | 60 | h1 | event | against signal | 15833 | +0.001 | 0.036 | -0.09 | -2.09 | -2.21 | -1.97 | -2.03 |
| MNQ | 60 | h2 | event | against signal | 15833 | +0.010 | 0.036 | +0.58 | -1.42 | -2.17 | -0.73 | -1.50 |
| MNQ | 60 | h4 | event | against signal | 15833 | +0.020 | 0.036 | +1.65 | -0.35 | -2.15 | +1.32 | -0.52 |
| MNQ | 60 | h8 | event | against signal | 15833 | +0.041 | 0.036 | +1.82 | -0.18 | -1.77 | +1.29 | -0.38 |
| MNQ | 60 | h16 | event | against signal | 15833 | +0.033 | 0.036 | +1.99 | -0.01 | -2.31 | +2.13 | +0.17 |
| MNQ | 60 | eod | event | against signal | 15833 | +0.038 | 0.036 | +2.41 | +0.41 | -2.22 | +2.87 | +0.39 |
| MYM | 5 | h1 | event | against signal | 110112 | +0.010 | 0.160 | +0.09 | -1.91 | +nan | -1.91 | -2.01 |
| MYM | 5 | h2 | event | against signal | 110112 | +0.015 | 0.160 | +0.11 | -1.89 | +nan | -1.89 | -2.00 |
| MYM | 5 | h4 | event | against signal | 110112 | +0.017 | 0.160 | +0.12 | -1.88 | +nan | -1.88 | -2.00 |
| MYM | 5 | h8 | event | against signal | 110112 | +0.015 | 0.160 | +0.10 | -1.90 | +nan | -1.90 | -2.01 |
| MYM | 5 | h16 | event | with signal | 110112 | -0.013 | 0.160 | -0.07 | -2.07 | +nan | -2.07 | -1.90 |
| MYM | 5 | eod | event | with signal | 110112 | +0.082 | 0.160 | +0.58 | -1.42 | +nan | -1.42 | -1.13 |
| MYM | 15 | h1 | event | against signal | 38053 | +0.009 | 0.095 | +0.13 | -1.87 | +nan | -1.87 | -1.97 |
| MYM | 15 | h2 | event | against signal | 38053 | +0.006 | 0.095 | +0.13 | -1.87 | +nan | -1.87 | -1.97 |
| MYM | 15 | h4 | event | against signal | 38053 | +0.010 | 0.095 | +0.06 | -1.94 | +nan | -1.94 | -1.98 |
| MYM | 15 | h8 | event | against signal | 38053 | +0.011 | 0.095 | +0.12 | -1.88 | +nan | -1.88 | -1.92 |
| MYM | 15 | h16 | event | with signal | 38053 | +0.006 | 0.095 | +0.20 | -1.80 | +nan | -1.80 | -1.88 |
| MYM | 15 | eod | event | against signal | 38053 | -0.004 | 0.095 | -0.08 | -2.08 | +nan | -2.08 | -1.98 |
| MYM | 60 | h1 | event | with signal | 8213 | +0.014 | 0.047 | +0.48 | -1.52 | +nan | -1.52 | -1.57 |
| MYM | 60 | h2 | event | with signal | 8213 | +0.008 | 0.047 | +0.15 | -1.85 | +nan | -1.85 | -1.65 |
| MYM | 60 | h4 | event | with signal | 8213 | +0.013 | 0.047 | -0.15 | -2.15 | +nan | -2.15 | -1.88 |
| MYM | 60 | h8 | event | with signal | 8213 | +0.003 | 0.047 | +0.09 | -1.91 | +nan | -1.91 | -1.57 |
| MYM | 60 | h16 | event | against signal | 8213 | -0.002 | 0.047 | -0.25 | -2.25 | +nan | -2.25 | -1.91 |
| MYM | 60 | eod | event | against signal | 8213 | +0.003 | 0.047 | -0.06 | -2.06 | +nan | -2.06 | -1.77 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.612 | -0.684 | -0.743 | -0.749 | -0.731 | +0.000 | -0.033 | -0.042 | -0.043 | -0.039 | -0.034 |
| MES | 15 | -0.629 | -0.681 | -0.734 | -0.737 | -0.724 | +0.000 | -0.018 | -0.025 | -0.035 | -0.050 | -0.063 |
| MES | 60 | -0.898 | -0.745 | -0.724 | -0.694 | -0.723 | +0.000 | -0.008 | -0.011 | -0.036 | -0.098 | +0.013 |
| MNQ | 5 | -0.591 | -0.664 | -0.722 | -0.735 | -0.722 | +0.000 | -0.018 | -0.024 | -0.023 | -0.016 | -0.005 |
| MNQ | 15 | -0.617 | -0.671 | -0.719 | -0.721 | -0.714 | +0.000 | -0.015 | -0.017 | -0.025 | -0.032 | -0.046 |
| MNQ | 60 | -0.951 | -0.761 | -0.712 | -0.677 | -0.708 | +0.000 | -0.002 | -0.013 | -0.036 | -0.092 | +0.059 |
| MYM | 5 | -0.591 | -0.657 | -0.711 | -0.717 | -0.708 | +0.000 | -0.015 | -0.020 | -0.024 | -0.022 | -0.018 |
| MYM | 15 | -0.614 | -0.649 | -0.686 | -0.702 | -0.697 | +0.000 | -0.010 | -0.007 | -0.010 | -0.012 | +0.005 |
| MYM | 60 | -0.904 | -0.753 | -0.700 | -0.679 | -0.706 | +0.000 | +0.014 | +0.011 | +0.006 | -0.040 | +0.041 |

## Calibration

- MES 5-min: 1036271 bars, 144293 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 57379 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 13823 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 207676 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 72642 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 15833 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 110112 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 38053 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8213 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 41621 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.

## Plain-$ cross-check (zoo.dollar_check)

Each signal bar traded in its side at the lab's best hold, in $ per micro, minus the average $ move of non-signal bars in the same year x 15-min slot (session bootstrap se). The lab's R20 units can overweight quiet bars at long holds; a direction claim must survive this check.

FINAL WORD: DIRECTION: confirmed in R20 and $, far below costs ($0.40 vs $3.50)

| market | tf | hold | era | trades | lab verdict | lab $ edge 2018-25 | $ excess | se | z | cost |
|---|---|---|---|---|---|---|---|---|---|---|
| ES | 5 | dir_h2 | all | 144293 | REAL BUT TOO SMALL | +0.09 | -0.35 | 0.04 | -8.0 | 3.50 |
| ES | 5 | dir_h2 | 2018-25H1 | 90285 | REAL BUT TOO SMALL | +0.09 | -0.40 | 0.07 | -5.6 | 3.50 |
| ES | 15 | dir_h8 | all | 57379 | CONFIDENTLY NOTHING | -0.12 | -0.39 | 0.23 | -1.7 | 3.50 |
| ES | 15 | dir_h8 | 2018-25H1 | 33627 | CONFIDENTLY NOTHING | -0.12 | -0.21 | 0.39 | -0.5 | 3.50 |
| ES | 60 | dir_h8 | all | 13823 | INCONCLUSIVE | +3.28 | -2.09 | 0.88 | -2.4 | 3.50 |
| ES | 60 | dir_h8 | 2018-25H1 | 7569 | INCONCLUSIVE | +3.28 | -3.78 | 1.49 | -2.5 | 3.50 |
| NQ | 5 | dir_h2 | all | 207676 | CONFIDENTLY NOTHING | +0.27 | -0.33 | 0.06 | -5.8 | 2.00 |
| NQ | 5 | dir_h2 | 2018-25H1 | 119944 | CONFIDENTLY NOTHING | +0.27 | -0.51 | 0.10 | -5.0 | 2.00 |
| NQ | 15 | dir_h1 | all | 72642 | INCONCLUSIVE | +0.20 | -0.24 | 0.11 | -2.1 | 2.00 |
| NQ | 15 | dir_h1 | 2018-25H1 | 40038 | INCONCLUSIVE | +0.20 | -0.34 | 0.19 | -1.8 | 2.00 |
| NQ | 60 | dir_h8 | all | 15833 | INCONCLUSIVE | +2.93 | -2.11 | 1.26 | -1.7 | 2.00 |
| NQ | 60 | dir_h8 | 2018-25H1 | 8202 | INCONCLUSIVE | +2.93 | -3.78 | 2.43 | -1.6 | 2.00 |
| YM | 5 | dir_eod | all | 110112 | CONFIDENTLY NOTHING | +0.87 | +0.51 | 0.41 | +1.2 | 2.00 |
| YM | 5 | dir_eod | 2018-25H1 | 110112 | CONFIDENTLY NOTHING | +0.87 | +0.51 | 0.41 | +1.2 | 2.00 |
| YM | 15 | dir_h4 | all | 38053 | CONFIDENTLY NOTHING | +0.02 | -0.05 | 0.20 | -0.2 | 2.00 |
| YM | 15 | dir_h4 | 2018-25H1 | 38053 | CONFIDENTLY NOTHING | +0.02 | -0.05 | 0.20 | -0.2 | 2.00 |
| YM | 60 | dir_h1 | all | 8213 | INCONCLUSIVE | +0.43 | +0.49 | 0.44 | +1.1 | 2.00 |
| YM | 60 | dir_h1 | 2018-25H1 | 8213 | INCONCLUSIVE | +0.43 | +0.49 | 0.44 | +1.1 | 2.00 |
