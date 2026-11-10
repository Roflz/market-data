# Impact card: x_vwap

close crosses VWAP: above long, below short [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: sided. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.020 R20 over the rest of the session (to 16:45), p=0.22; we would catch an effect of 0.010 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.022).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.16 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.225 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.010 R20 over the next 4 bars (1 h), p=0.34; we would catch an effect of 0.015 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.027).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.57 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.129 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.008 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.021 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=0.4).
- MES 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.13 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.064 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.040 R20 over the rest of the session (to 16:45), p=0.24; we would catch an effect of 0.012 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.013 R20, CONFIRMED, q=3.47e-05, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.26 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.078 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.005 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 0.019 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.097).
- MNQ 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.70 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.045 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.006 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.023 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.59 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.022 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.063 R20 over the rest of the session (to 16:45), p=0.35; we would catch an effect of 0.021 R20 or more 80% of the time).
- MYM 5-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (5 min) (+0.014 R20, possible, q=0.155, 7 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.28 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.174 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.012 R20 over the next 1 bar (15 min), p=0.85; we would catch an effect of 0.025 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.4).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.78 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.098 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.012 R20 over the next 4 bars (4 h), p=1; we would catch an effect of 0.032 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=0.6).
- MYM 60-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.42 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.048 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.003 | -0.008 .. +0.003 | -0.0010 | 0.36 / 0.35 / 0.35 | 0.349 |  |  | 8/16 | -0.003 | -0.002 |  | -1.0 / -0.9 |  |
| MES | 5 | h2 | -0.002 | -0.008 .. +0.004 | -0.0006 | 0.46 / 0.48 / 0.51 | 0.506 |  |  | 9/16 | -0.001 | -0.003 |  | -0.6 / -0.7 |  |
| MES | 5 | h4 | +0.002 | -0.006 .. +0.009 | +0.0003 | 0.66 / 0.67 / 0.64 | 0.636 |  |  | 9/16 | +0.005 | -0.002 |  | +0.3 / +0.4 | 0.010 |
| MES | 5 | h8 | +0.003 | -0.005 .. +0.012 | +0.0004 | 0.44 / 0.45 / 0.47 | 0.451 |  |  | 9/16 | -0.003 | +0.009 |  | +0.4 / +0.8 |  |
| MES | 5 | h16 | -0.004 | -0.015 .. +0.006 | -0.0004 | 0.4 / 0.39 / 0.43 | 0.419 |  |  | 10/16 | -0.013 | +0.004 |  | -0.4 / -0.8 |  |
| MES | 5 | eod * | +0.020 | +0.001 .. +0.040 | +0.0004 | 0.036 / 0.036 / 0.072 | 0.0706 | 1 | 0.998 | 11/16 | +0.001 | +0.039 | False | +0.4 / +2.1 |  |
| MES | 15 | h1 | +0.004 | -0.003 .. +0.011 | +0.0019 | 0.27 / 0.28 / 0.32 | 0.315 |  |  | 11/16 | +0.002 | +0.006 |  | +1.0 / +1.1 |  |
| MES | 15 | h2 | +0.005 | -0.004 .. +0.013 | +0.0015 | 0.28 / 0.29 / 0.36 | 0.36 |  |  | 9/16 | -0.006 | +0.015 |  | +0.9 / +1.1 |  |
| MES | 15 | h4 * | +0.010 | +0.001 .. +0.020 | +0.0023 | 0.033 / 0.037 / 0.096 | 0.0956 | 1 | 0.997 | 11/16 | -0.002 | +0.023 | False | +1.4 / +2.1 | 0.015 |
| MES | 15 | h8 | -0.001 | -0.012 .. +0.010 | -0.0001 | 0.89 / 0.89 / 0.91 | 0.913 |  |  | 9/16 | -0.013 | +0.012 |  | -0.1 / -0.1 |  |
| MES | 15 | h16 | +0.006 | -0.008 .. +0.020 | +0.0006 | 0.44 / 0.44 / 0.48 | 0.482 |  |  | 9/16 | -0.009 | +0.021 |  | +0.4 / +0.8 |  |
| MES | 15 | eod | +0.016 | -0.001 .. +0.033 | +0.0006 | 0.061 / 0.065 / 0.11 | 0.106 |  |  | 13/16 | +0.001 | +0.032 |  | +0.4 / +1.9 |  |
| MES | 60 | h1 | +0.003 | -0.008 .. +0.014 | +0.0017 | 0.58 / 0.59 / 0.6 | 0.604 |  |  | 9/16 | -0.000 | +0.007 |  | +0.5 / +0.6 |  |
| MES | 60 | h2 * | -0.008 | -0.021 .. +0.005 | -0.0041 | 0.22 / 0.23 / 0.23 | 0.232 | 1 | 1 | 10/16 | -0.011 | -0.005 | False | -1.0 / -1.2 |  |
| MES | 60 | h4 | -0.008 | -0.023 .. +0.006 | -0.0031 | 0.27 / 0.29 / 0.28 | 0.284 |  |  | 11/16 | -0.025 | +0.009 |  | -0.7 / -1.1 | 0.021 |
| MES | 60 | h8 | -0.006 | -0.021 .. +0.009 | -0.0020 | 0.45 / 0.45 / 0.46 | 0.466 |  |  | 8/16 | -0.015 | +0.003 |  | -0.4 / -0.8 |  |
| MES | 60 | h16 | -0.008 | -0.023 .. +0.007 | -0.0015 | 0.28 / 0.3 / 0.31 | 0.314 |  |  | 9/16 | -0.025 | +0.009 |  | -0.4 / -1.1 |  |
| MES | 60 | eod | -0.005 | -0.020 .. +0.010 | -0.0010 | 0.49 / 0.5 / 0.51 | 0.514 |  |  | 10/16 | -0.008 | -0.003 |  | -0.2 / -0.7 |  |
| MNQ | 5 | h1 | +0.002 | -0.004 .. +0.008 | +0.0007 | 0.52 / 0.51 / 0.54 | 0.529 |  |  | 10/16 | -0.000 | +0.005 |  | +0.7 / +0.6 |  |
| MNQ | 5 | h2 | +0.001 | -0.007 .. +0.009 | +0.0002 | 0.86 / 0.85 / 0.84 | 0.827 |  |  | 7/16 | -0.006 | +0.007 |  | +0.2 / +0.2 |  |
| MNQ | 5 | h4 | -0.000 | -0.009 .. +0.008 | -0.0001 | 0.92 / 0.92 / 0.96 | 0.964 |  |  | 9/16 | -0.002 | +0.001 |  | -0.1 / -0.1 | 0.012 |
| MNQ | 5 | h8 | -0.002 | -0.012 .. +0.009 | -0.0001 | 0.77 / 0.77 / 0.86 | 0.844 |  |  | 7/16 | -0.013 | +0.010 |  | -0.2 / -0.3 |  |
| MNQ | 5 | h16 | -0.006 | -0.018 .. +0.006 | -0.0004 | 0.34 / 0.35 / 0.57 | 0.545 |  |  | 8/16 | -0.011 | -0.001 |  | -0.4 / -1.0 |  |
| MNQ | 5 | eod * | +0.040 | +0.013 .. +0.068 | +0.0005 | 0.0039 / 0.0027 / 0.1 | 0.105 | 1 | 0.607 | 13/16 | +0.019 | +0.061 | False | +0.5 / +2.9 |  |
| MNQ | 15 | h1 | -0.001 | -0.008 .. +0.007 | -0.0003 | 0.82 / 0.83 / 0.86 | 0.851 |  |  | 9/16 | -0.012 | +0.010 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h2 * | +0.005 | -0.005 .. +0.014 | +0.0011 | 0.32 / 0.31 / 0.49 | 0.449 | 1 | 1 | 9/16 | -0.008 | +0.017 | False | +0.8 / +1.0 |  |
| MNQ | 15 | h4 | -0.003 | -0.014 .. +0.008 | -0.0005 | 0.58 / 0.59 / 0.79 | 0.768 |  |  | 7/16 | -0.016 | +0.010 |  | -0.4 / -0.6 | 0.019 |
| MNQ | 15 | h8 | -0.004 | -0.017 .. +0.009 | -0.0005 | 0.5 / 0.52 / 0.7 | 0.697 |  |  | 8/16 | -0.018 | +0.009 |  | -0.4 / -0.7 |  |
| MNQ | 15 | h16 | -0.001 | -0.016 .. +0.015 | -0.0001 | 0.95 / 0.95 / 0.96 | 0.962 |  |  | 8/16 | -0.018 | +0.017 |  | -0.0 / -0.1 |  |
| MNQ | 15 | eod | +0.007 | -0.012 .. +0.027 | +0.0002 | 0.45 / 0.45 / 0.79 | 0.761 |  |  | 10/16 | -0.016 | +0.031 |  | +0.2 / +0.7 |  |
| MNQ | 60 | h1 | +0.001 | -0.011 .. +0.013 | +0.0005 | 0.87 / 0.88 / 0.88 | 0.877 |  |  | 10/16 | +0.000 | +0.002 |  | +0.1 / +0.2 |  |
| MNQ | 60 | h2 | +0.003 | -0.011 .. +0.017 | +0.0011 | 0.7 / 0.72 / 0.71 | 0.705 |  |  | 10/16 | +0.004 | +0.001 |  | +0.3 / +0.4 |  |
| MNQ | 60 | h4 | -0.004 | -0.019 .. +0.011 | -0.0016 | 0.6 / 0.62 / 0.62 | 0.622 |  |  | 7/16 | -0.016 | +0.007 |  | -0.3 / -0.5 | 0.023 |
| MNQ | 60 | h8 | -0.001 | -0.017 .. +0.014 | -0.0007 | 0.89 / 0.9 / 0.9 | 0.89 |  |  | 7/16 | -0.012 | +0.009 |  | -0.1 / -0.1 |  |
| MNQ | 60 | h16 * | -0.006 | -0.023 .. +0.011 | -0.0011 | 0.47 / 0.48 / 0.47 | 0.465 | 1 | 1 | 6/16 | -0.026 | +0.014 | False | -0.3 / -0.7 |  |
| MNQ | 60 | eod | +0.002 | -0.015 .. +0.019 | +0.0005 | 0.84 / 0.85 / 0.84 | 0.829 |  |  | 8/16 | -0.011 | +0.014 |  | +0.1 / +0.2 |  |
| MYM | 5 | h1 | -0.006 | -0.014 .. +0.001 | -0.0018 | 0.11 / 0.12 / 0.29 | 0.266 |  |  | 6/8 | n/a | -0.006 |  | -1.5 / -1.6 |  |
| MYM | 5 | h2 | -0.003 | -0.013 .. +0.007 | -0.0005 | 0.54 / 0.54 / 0.72 | 0.688 |  |  | 4/8 | n/a | -0.003 |  | -0.5 / -0.6 |  |
| MYM | 5 | h4 | +0.003 | -0.010 .. +0.015 | +0.0003 | 0.67 / 0.66 / 0.78 | 0.728 |  |  | 5/8 | n/a | +0.003 |  | +0.3 / +0.4 | 0.021 |
| MYM | 5 | h8 | +0.013 | -0.002 .. +0.027 | +0.0010 | 0.087 / 0.084 / 0.31 | 0.266 |  |  | 5/8 | n/a | +0.013 |  | +1.0 / +1.7 |  |
| MYM | 5 | h16 | +0.004 | -0.012 .. +0.020 | +0.0002 | 0.62 / 0.62 / 0.76 | 0.719 |  |  | 4/8 | n/a | +0.004 |  | +0.2 / +0.5 |  |
| MYM | 5 | eod * | +0.063 | +0.030 .. +0.096 | +0.0008 | 0.00019 / 0.00039 / 0.085 | 0.0817 | 1 | 0.069 | 8/8 | n/a | +0.063 | False | +0.6 / +3.7 |  |
| MYM | 15 | h1 * | +0.012 | +0.001 .. +0.023 | +0.0045 | 0.04 / 0.049 / 0.11 | 0.117 | 1 | 0.931 | 6/8 | n/a | +0.012 | False | +2.0 / +2.0 |  |
| MYM | 15 | h2 | +0.011 | -0.003 .. +0.025 | +0.0025 | 0.11 / 0.12 / 0.3 | 0.272 |  |  | 6/8 | n/a | +0.011 |  | +1.4 / +1.6 |  |
| MYM | 15 | h4 | +0.021 | +0.004 .. +0.037 | +0.0027 | 0.015 / 0.016 / 0.25 | 0.223 |  |  | 6/8 | n/a | +0.021 |  | +1.7 / +2.4 | 0.025 |
| MYM | 15 | h8 | +0.005 | -0.012 .. +0.023 | +0.0005 | 0.55 / 0.57 / 0.77 | 0.733 |  |  | 3/8 | n/a | +0.005 |  | +0.3 / +0.6 |  |
| MYM | 15 | h16 | +0.010 | -0.011 .. +0.032 | +0.0007 | 0.35 / 0.36 / 0.64 | 0.611 |  |  | 6/8 | n/a | +0.010 |  | +0.4 / +0.9 |  |
| MYM | 15 | eod | +0.030 | +0.003 .. +0.056 | +0.0008 | 0.028 / 0.042 / 0.49 | 0.459 |  |  | 6/8 | n/a | +0.030 |  | +0.5 / +2.2 |  |
| MYM | 60 | h1 | +0.001 | -0.016 .. +0.018 | +0.0005 | 0.93 / 0.93 / 0.93 | 0.929 |  |  | 4/8 | n/a | +0.001 |  | +0.1 / +0.1 |  |
| MYM | 60 | h2 | -0.006 | -0.027 .. +0.016 | -0.0023 | 0.61 / 0.6 / 0.57 | 0.566 |  |  | 5/8 | n/a | -0.006 |  | -0.5 / -0.5 |  |
| MYM | 60 | h4 * | +0.012 | -0.010 .. +0.035 | +0.0040 | 0.28 / 0.29 / 0.28 | 0.295 | 1 | 1 | 2/8 | n/a | +0.012 | False | +0.7 / +1.1 | 0.032 |
| MYM | 60 | h8 | +0.005 | -0.019 .. +0.029 | +0.0009 | 0.7 / 0.71 / 0.7 | 0.737 |  |  | 3/8 | n/a | +0.005 |  | +0.2 / +0.4 |  |
| MYM | 60 | h16 | +0.006 | -0.017 .. +0.029 | +0.0011 | 0.6 / 0.61 / 0.63 | 0.634 |  |  | 5/8 | n/a | +0.006 |  | +0.2 / +0.5 |  |
| MYM | 60 | eod | -0.000 | -0.022 .. +0.021 | +0.0001 | 1 / 1 / 1 | 0.995 |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.006 | +0.001 .. +0.011 | +1.2% | +0.018 | 0.011 |  | 8/16 |
| MES | 5 | h2 | +0.008 | +0.001 .. +0.014 | +1.1% | +0.021 | 0.017 |  | 10/16 |
| MES | 5 | h4 | +0.011 | +0.002 .. +0.020 | +1.1% | +0.023 | 0.023 |  | 12/16 |
| MES | 5 | h8 * | +0.024 | +0.008 .. +0.040 | +1.6% | +0.032 | 0.0036 | 0.551 | 13/16 |
| MES | 5 | h16 | +0.023 | -0.003 .. +0.049 | +1.1% | +0.040 | 0.088 |  | 12/16 |
| MES | 5 | eod | +0.026 | -0.156 .. +0.208 | +0.3% | +0.156 | 0.78 |  | 10/16 |
| MES | 15 | h1 | +0.005 | +0.000 .. +0.010 | +1.0% | +0.020 | 0.21 |  | 10/16 |
| MES | 15 | h2 | +0.010 | +0.002 .. +0.018 | +1.4% | +0.026 | 0.086 |  | 12/16 |
| MES | 15 | h4 * | +0.023 | +0.009 .. +0.037 | +2.2% | +0.039 | 0.0045 | 0.672 | 12/16 |
| MES | 15 | h8 | +0.030 | +0.007 .. +0.053 | +1.9% | +0.040 | 0.011 |  | 10/16 |
| MES | 15 | h16 | +0.046 | +0.010 .. +0.082 | +2.0% | +0.065 | 0.022 |  | 11/16 |
| MES | 15 | eod | +0.027 | -0.107 .. +0.162 | +0.5% | +0.110 | 0.69 |  | 12/16 |
| MES | 60 | h1 | +0.008 | -0.001 .. +0.017 | +1.6% | +0.027 | 0.1 |  | 10/16 |
| MES | 60 | h2 | +0.009 | -0.004 .. +0.022 | +1.2% | +0.029 | 0.24 |  | 13/16 |
| MES | 60 | h4 * | +0.019 | -0.001 .. +0.039 | +1.7% | +0.038 | 0.066 | 1 | 12/16 |
| MES | 60 | h8 | +0.006 | -0.022 .. +0.034 | +0.4% | +0.047 | 0.67 |  | 7/16 |
| MES | 60 | h16 | +0.021 | -0.014 .. +0.056 | +1.0% | +0.055 | 0.25 |  | 9/16 |
| MES | 60 | eod | +0.008 | -0.029 .. +0.044 | +0.4% | +0.056 | 0.67 |  | 9/16 |
| MNQ | 5 | h1 * | +0.013 | +0.008 .. +0.018 | +2.4% | +0.029 | 1.3e-07 | 3.47e-05 | 14/16 |
| MNQ | 5 | h2 | +0.017 | +0.008 .. +0.025 | +2.2% | +0.036 | 6.6e-05 |  | 14/16 |
| MNQ | 5 | h4 | +0.024 | +0.009 .. +0.038 | +2.1% | +0.042 | 0.0011 |  | 12/16 |
| MNQ | 5 | h8 | +0.030 | +0.005 .. +0.056 | +1.9% | +0.052 | 0.02 |  | 10/16 |
| MNQ | 5 | h16 | +0.024 | -0.021 .. +0.069 | +1.0% | +0.067 | 0.3 |  | 11/16 |
| MNQ | 5 | eod | -0.005 | -0.275 .. +0.265 | -0.0% | +0.334 | 0.99 |  | 7/16 |
| MNQ | 15 | h1 | +0.010 | +0.003 .. +0.017 | +1.9% | +0.026 | 0.021 |  | 11/16 |
| MNQ | 15 | h2 * | +0.016 | +0.004 .. +0.028 | +2.0% | +0.033 | 0.016 | 1 | 11/16 |
| MNQ | 15 | h4 | +0.016 | -0.012 .. +0.045 | +1.4% | +0.040 | 0.26 |  | 10/16 |
| MNQ | 15 | h8 | +0.009 | -0.036 .. +0.054 | +0.5% | +0.030 | 0.7 |  | 10/16 |
| MNQ | 15 | h16 | +0.002 | -0.052 .. +0.056 | +0.1% | +0.027 | 0.94 |  | 8/16 |
| MNQ | 15 | eod | -0.028 | -0.239 .. +0.184 | -0.4% | +0.051 | 0.8 |  | 6/16 |
| MNQ | 60 | h1 * | +0.006 | -0.003 .. +0.015 | +1.1% | +0.032 | 0.19 | 1 | 10/16 |
| MNQ | 60 | h2 | +0.009 | -0.005 .. +0.023 | +1.1% | +0.040 | 0.21 |  | 9/16 |
| MNQ | 60 | h4 | +0.011 | -0.010 .. +0.033 | +1.0% | +0.043 | 0.31 |  | 10/16 |
| MNQ | 60 | h8 | -0.010 | -0.040 .. +0.020 | -0.6% | +0.039 | 0.54 |  | 10/16 |
| MNQ | 60 | h16 | -0.008 | -0.045 .. +0.030 | -0.3% | +0.024 | 0.88 |  | 9/16 |
| MNQ | 60 | eod | -0.027 | -0.066 .. +0.011 | -1.2% | +0.016 | 0.32 |  | 11/16 |
| MYM | 5 | h1 * | +0.014 | +0.008 .. +0.020 | +2.6% | +0.030 | 0.0009 | 0.155 | 7/8 |
| MYM | 5 | h2 | +0.016 | +0.004 .. +0.028 | +2.1% | +0.035 | 0.012 |  | 6/8 |
| MYM | 5 | h4 | +0.020 | -0.004 .. +0.045 | +1.9% | +0.045 | 0.13 |  | 6/8 |
| MYM | 5 | h8 | +0.041 | -0.003 .. +0.084 | +2.5% | +0.078 | 0.067 |  | 6/8 |
| MYM | 5 | h16 | +0.032 | -0.030 .. +0.093 | +1.4% | +0.082 | 0.31 |  | 4/8 |
| MYM | 5 | eod | -0.029 | -0.364 .. +0.307 | -0.2% | +0.034 | 0.87 |  | 5/8 |
| MYM | 15 | h1 * | +0.016 | +0.006 .. +0.025 | +2.9% | +0.034 | 0.067 | 1 | 7/8 |
| MYM | 15 | h2 | +0.023 | +0.004 .. +0.042 | +3.0% | +0.044 | 0.14 |  | 7/8 |
| MYM | 15 | h4 | +0.023 | -0.014 .. +0.060 | +2.0% | +0.046 | 0.59 |  | 6/8 |
| MYM | 15 | h8 | +0.011 | -0.047 .. +0.069 | +0.7% | +0.028 | 0.93 |  | 5/8 |
| MYM | 15 | h16 | +0.012 | -0.086 .. +0.109 | +0.5% | +0.002 | 0.94 |  | 5/8 |
| MYM | 15 | eod | -0.082 | -0.342 .. +0.177 | -1.4% | -0.085 | 0.54 |  | 5/8 |
| MYM | 60 | h1 * | +0.014 | -0.000 .. +0.028 | +2.5% | +0.032 | 0.1 | 1 | 6/8 |
| MYM | 60 | h2 | +0.018 | -0.004 .. +0.039 | +2.3% | +0.038 | 0.1 |  | 5/8 |
| MYM | 60 | h4 | +0.025 | -0.004 .. +0.055 | +2.3% | +0.037 | 0.12 |  | 6/8 |
| MYM | 60 | h8 | +0.027 | -0.012 .. +0.065 | +1.7% | +0.046 | 0.37 |  | 5/8 |
| MYM | 60 | h16 | -0.004 | -0.057 .. +0.049 | -0.2% | +0.011 | 0.88 |  | 5/8 |
| MYM | 60 | eod | -0.021 | -0.076 .. +0.033 | -1.0% | +0.003 | 0.44 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.19 pts | -0.47 .. +0.09 | 0.2 |
| MES | 15 | +0.08 pts | -0.30 .. +0.46 | 0.69 |
| MES | 60 | +0.32 pts | -0.22 .. +0.86 | 0.34 |
| MNQ | 5 | -0.11 pts | -0.42 .. +0.20 | 0.7 |
| MNQ | 15 | +0.26 pts | -0.13 .. +0.66 | 0.19 |
| MNQ | 60 | +0.27 pts | -0.29 .. +0.83 | 0.35 |
| MYM | 5 | -0.04 pts | -0.47 .. +0.39 | 0.86 |
| MYM | 15 | +0.12 pts | -0.43 .. +0.66 | 0.68 |
| MYM | 60 | +0.87 pts | +0.11 .. +1.64 | 0.026 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | against signal | 80492 | +0.013 | 0.342 | +0.10 | -3.40 | -3.45 | -3.34 | -3.51 |
| MES | 5 | h2 | event | against signal | 80492 | +0.018 | 0.342 | +0.15 | -3.35 | -3.41 | -3.29 | -3.52 |
| MES | 5 | h4 | event | with signal | 80492 | -0.014 | 0.342 | -0.10 | -3.60 | -3.54 | -3.67 | -3.43 |
| MES | 5 | h8 | event | with signal | 80492 | -0.011 | 0.342 | -0.07 | -3.57 | -3.58 | -3.57 | -3.42 |
| MES | 5 | h16 | event | against signal | 80492 | +0.020 | 0.342 | +0.09 | -3.41 | -3.39 | -3.43 | -3.57 |
| MES | 5 | eod | event | with signal | 80492 | -0.002 | 0.342 | +0.07 | -3.43 | -3.55 | -3.30 | -3.17 |
| MES | 15 | h1 | event | with signal | 43639 | -0.004 | 0.196 | +0.05 | -3.45 | -3.51 | -3.38 | -3.30 |
| MES | 15 | h2 | event | with signal | 43639 | -0.005 | 0.196 | +0.03 | -3.47 | -3.56 | -3.36 | -3.29 |
| MES | 15 | h4 | event | with signal | 43639 | +0.001 | 0.196 | +0.22 | -3.28 | -3.53 | -3.00 | -3.11 |
| MES | 15 | h8 | event | against signal | 43639 | +0.012 | 0.196 | -0.07 | -3.57 | -3.42 | -3.73 | -3.77 |
| MES | 15 | h16 | event | with signal | 43639 | -0.010 | 0.196 | +0.01 | -3.49 | -3.60 | -3.36 | -3.20 |
| MES | 15 | eod | event | with signal | 43639 | +0.009 | 0.196 | +0.39 | -3.11 | -3.38 | -2.80 | -2.95 |
| MES | 60 | h1 | event | with signal | 18938 | +0.003 | 0.097 | +0.40 | -3.10 | -3.39 | -2.78 | -3.09 |
| MES | 60 | h2 | event | against signal | 18938 | +0.010 | 0.097 | -0.01 | -3.51 | -3.42 | -3.61 | -3.59 |
| MES | 60 | h4 | event | against signal | 18938 | +0.012 | 0.097 | -0.09 | -3.59 | -3.12 | -4.10 | -3.74 |
| MES | 60 | h8 | event | against signal | 18938 | +0.012 | 0.097 | +0.11 | -3.39 | -3.28 | -3.50 | -3.60 |
| MES | 60 | h16 | event | against signal | 18938 | +0.004 | 0.097 | -0.34 | -3.84 | -3.35 | -4.37 | -3.69 |
| MES | 60 | eod | event | against signal | 18938 | +0.005 | 0.097 | -0.12 | -3.62 | -3.65 | -3.60 | -3.58 |
| MNQ | 5 | h1 | event | with signal | 77761 | -0.003 | 0.138 | -0.03 | -2.03 | -1.98 | -2.07 | -1.96 |
| MNQ | 5 | h2 | event | with signal | 77761 | -0.007 | 0.138 | -0.08 | -2.08 | -2.04 | -2.13 | -1.96 |
| MNQ | 5 | h4 | event | against signal | 77761 | +0.006 | 0.138 | +0.08 | -1.92 | -2.00 | -1.82 | -2.00 |
| MNQ | 5 | h8 | event | against signal | 77761 | +0.001 | 0.138 | +0.01 | -1.99 | -1.96 | -2.03 | -1.99 |
| MNQ | 5 | h16 | event | against signal | 77761 | +0.003 | 0.138 | +0.09 | -1.91 | -2.01 | -1.80 | -1.88 |
| MNQ | 5 | eod | event | with signal | 77761 | +0.013 | 0.138 | +0.32 | -1.68 | -2.00 | -1.32 | -1.22 |
| MNQ | 15 | h1 | event | against signal | 42957 | +0.004 | 0.078 | -0.05 | -2.05 | -1.91 | -2.20 | -2.13 |
| MNQ | 15 | h2 | event | with signal | 42957 | +0.003 | 0.078 | +0.14 | -1.86 | -2.03 | -1.66 | -1.82 |
| MNQ | 15 | h4 | event | against signal | 42957 | +0.003 | 0.078 | -0.05 | -2.05 | -1.88 | -2.23 | -2.03 |
| MNQ | 15 | h8 | event | against signal | 42957 | +0.000 | 0.078 | -0.10 | -2.10 | -1.94 | -2.28 | -1.98 |
| MNQ | 15 | h16 | event | against signal | 42957 | +0.004 | 0.078 | +0.07 | -1.93 | -1.90 | -1.95 | -2.01 |
| MNQ | 15 | eod | event | with signal | 42957 | +0.007 | 0.078 | +0.45 | -1.55 | -2.03 | -1.00 | -1.50 |
| MNQ | 60 | h1 | event | with signal | 18738 | +0.002 | 0.038 | -0.13 | -2.13 | -1.94 | -2.34 | -2.18 |
| MNQ | 60 | h2 | event | with signal | 18738 | +0.001 | 0.038 | +0.04 | -1.96 | -1.87 | -2.05 | -1.88 |
| MNQ | 60 | h4 | event | against signal | 18738 | +0.008 | 0.038 | +0.26 | -1.74 | -1.75 | -1.74 | -1.92 |
| MNQ | 60 | h8 | event | against signal | 18738 | +0.005 | 0.038 | -0.19 | -2.19 | -1.89 | -2.53 | -2.37 |
| MNQ | 60 | h16 | event | against signal | 18738 | +0.003 | 0.038 | -0.55 | -2.55 | -1.82 | -3.35 | -2.34 |
| MNQ | 60 | eod | event | with signal | 18738 | +0.002 | 0.038 | +0.74 | -1.26 | -1.94 | -0.52 | -1.32 |
| MYM | 5 | h1 | event | against signal | 37509 | +0.014 | 0.174 | +0.11 | -1.89 | +nan | -1.89 | -1.98 |
| MYM | 5 | h2 | event | against signal | 37509 | +0.013 | 0.174 | +0.14 | -1.86 | +nan | -1.86 | -1.98 |
| MYM | 5 | h4 | event | with signal | 37509 | -0.009 | 0.174 | -0.05 | -2.05 | +nan | -2.05 | -1.91 |
| MYM | 5 | h8 | event | with signal | 37509 | -0.001 | 0.174 | -0.01 | -2.01 | +nan | -2.01 | -1.86 |
| MYM | 5 | h16 | event | with signal | 37509 | -0.016 | 0.174 | -0.09 | -2.09 | +nan | -2.09 | -1.85 |
| MYM | 5 | eod | event | with signal | 37509 | +0.017 | 0.174 | +0.12 | -1.88 | +nan | -1.88 | -1.35 |
| MYM | 15 | h1 | event | with signal | 20659 | +0.006 | 0.098 | +0.17 | -1.83 | +nan | -1.83 | -1.72 |
| MYM | 15 | h2 | event | with signal | 20659 | +0.006 | 0.098 | +0.09 | -1.91 | +nan | -1.91 | -1.79 |
| MYM | 15 | h4 | event | with signal | 20659 | +0.017 | 0.098 | +0.41 | -1.59 | +nan | -1.59 | -1.52 |
| MYM | 15 | h8 | event | with signal | 20659 | -0.001 | 0.098 | -0.01 | -2.01 | +nan | -2.01 | -1.86 |
| MYM | 15 | h16 | event | with signal | 20659 | +0.006 | 0.098 | +0.13 | -1.87 | +nan | -1.87 | -1.75 |
| MYM | 15 | eod | event | with signal | 20659 | +0.014 | 0.098 | +0.27 | -1.73 | +nan | -1.73 | -1.37 |
| MYM | 60 | h1 | event | with signal | 8985 | +0.001 | 0.048 | +0.15 | -1.85 | +nan | -1.85 | -1.86 |
| MYM | 60 | h2 | event | against signal | 8985 | +0.011 | 0.048 | +0.34 | -1.66 | +nan | -1.66 | -1.89 |
| MYM | 60 | h4 | event | with signal | 8985 | +0.004 | 0.048 | +0.24 | -1.76 | +nan | -1.76 | -1.42 |
| MYM | 60 | h8 | event | with signal | 8985 | -0.007 | 0.048 | -0.18 | -2.18 | +nan | -2.18 | -1.72 |
| MYM | 60 | h16 | event | with signal | 8985 | +0.006 | 0.048 | +0.29 | -1.71 | +nan | -1.71 | -1.72 |
| MYM | 60 | eod | event | against signal | 8985 | +0.002 | 0.048 | +0.02 | -1.98 | +nan | -1.98 | -2.01 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.682 | -0.714 | -0.744 | -0.776 | -0.847 | +0.000 | -0.042 | -0.047 | -0.043 | -0.040 | -0.051 |
| MES | 15 | -0.618 | -0.623 | -0.667 | -0.737 | -0.814 | +0.000 | -0.012 | -0.013 | -0.008 | -0.023 | -0.022 |
| MES | 60 | -0.429 | -0.345 | -0.425 | -0.564 | -0.740 | +0.000 | +0.001 | -0.013 | -0.022 | -0.046 | +0.007 |
| MNQ | 5 | -0.761 | -0.797 | -0.832 | -0.867 | -0.926 | +0.000 | -0.018 | -0.023 | -0.022 | -0.017 | -0.020 |
| MNQ | 15 | -0.667 | -0.666 | -0.715 | -0.786 | -0.860 | +0.000 | -0.006 | +0.002 | -0.005 | -0.004 | -0.007 |
| MNQ | 60 | -0.480 | -0.371 | -0.453 | -0.584 | -0.758 | +0.000 | +0.002 | +0.001 | -0.014 | -0.028 | +0.017 |
| MYM | 5 | -0.743 | -0.769 | -0.811 | -0.844 | -0.888 | +0.000 | -0.020 | -0.019 | -0.015 | -0.007 | -0.020 |
| MYM | 15 | -0.673 | -0.672 | -0.718 | -0.776 | -0.835 | +0.000 | +0.007 | +0.007 | +0.017 | -0.000 | +0.003 |
| MYM | 60 | -0.490 | -0.382 | -0.474 | -0.599 | -0.763 | +0.000 | +0.001 | -0.011 | -0.000 | -0.037 | +0.013 |

## Calibration

- MES 5-min: 1032456 bars, 80492 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 338403 bars, 43639 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 79599 bars, 18938 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1030707 bars, 77761 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 338247 bars, 42957 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 79597 bars, 18738 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 517134 bars, 37509 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 169522 bars, 20659 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 39751 bars, 8985 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
