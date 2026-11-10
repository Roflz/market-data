# Impact card: dow_thu

session weekday = thu vs other days [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.002 R20 over the next 1 bar (5 min), p=1; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: the market moves 1% MORE after the event than after matched bars over the next 2 bars (10 min) (+0.007 R20, possible, q=0.0536, 14 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.49 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.218 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best +0.182 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.038 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.21).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.12 at recent bar sizes, 90% range up to $1.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best +0.066 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MES 60-min size: the market moves 7% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.033 R20, CONFIRMED, q=2.29e-08, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $2.93 at recent bar sizes, 90% range up to $5.58); about 3.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.004 R20 over the next 4 bars (20 min), p=1; we would catch an effect of 0.026 R20 or more 80% of the time).
- MNQ 5-min size: no measurable effect on how much price moves (best p=1).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.08 at recent bar sizes, 90% range up to $0.83); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best -0.001 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.048 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=1).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.06 at recent bar sizes, 90% range up to $2.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.001 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.080 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.034 R20, CONFIRMED, q=3.23e-06, 16 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.05 at recent bar sizes, 90% range up to $8.63); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.559 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.041 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=1).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.37 at recent bar sizes, 90% range up to $0.61); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.395 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.065 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=1).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $6.77 at recent bar sizes, 90% range up to $1.57); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best +0.117 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.110 R20 or more 80% of the time).
- MYM 60-min size: the market moves 6% MORE after the event than after matched bars over the next 1 bar (1 h) (+0.033 R20, CONFIRMED, q=0.0214, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $4.01 at recent bar sizes, 90% range up to $6.76); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 * | +0.002 | -0.002 .. +0.005 | +0.0009 | 0.36 / 0.33 / 0.37 | nan | 1 | 1 | 9/16 | +0.003 | +0.000 | False | +1.0 / +0.9 |  |
| MES | 5 | h2 | +0.003 | -0.004 .. +0.010 | +0.0012 | 0.39 / 0.37 / 0.41 | nan |  |  | 9/16 | +0.004 | +0.002 |  | +1.2 / +0.9 |  |
| MES | 5 | h4 | +0.006 | -0.008 .. +0.020 | +0.0016 | 0.41 / 0.39 / 0.43 | nan |  |  | 9/16 | +0.006 | +0.005 |  | +1.7 / +0.8 | 0.020 |
| MES | 5 | h8 | +0.011 | -0.017 .. +0.040 | +0.0020 | 0.45 / 0.43 / 0.46 | nan |  |  | 9/16 | +0.011 | +0.012 |  | +2.2 / +0.8 |  |
| MES | 5 | h16 | +0.018 | -0.041 .. +0.076 | +0.0022 | 0.56 / 0.54 / 0.56 | nan |  |  | 9/16 | +0.019 | +0.016 |  | +2.3 / +0.6 |  |
| MES | 5 | eod | +0.212 | -0.800 .. +1.224 | +0.0054 | 0.68 / 0.67 / 0.67 | nan |  |  | 10/16 | +0.426 | -0.000 |  | +5.5 / +0.4 |  |
| MES | 15 | h1 | +0.000 | -0.006 .. +0.007 | +0.0002 | 0.91 / 0.9 / 0.91 | nan |  |  | 10/16 | +0.003 | -0.002 |  | +0.1 / +0.1 |  |
| MES | 15 | h2 | +0.002 | -0.011 .. +0.015 | +0.0006 | 0.79 / 0.79 / 0.79 | nan |  |  | 10/16 | +0.003 | +0.000 |  | +0.4 / +0.3 |  |
| MES | 15 | h4 | +0.004 | -0.022 .. +0.030 | +0.0010 | 0.75 / 0.74 / 0.75 | nan |  |  | 10/16 | +0.006 | +0.003 |  | +0.6 / +0.3 | 0.038 |
| MES | 15 | h8 | +0.008 | -0.044 .. +0.061 | +0.0013 | 0.76 / 0.75 / 0.77 | nan |  |  | 10/16 | +0.011 | +0.005 |  | +0.8 / +0.3 |  |
| MES | 15 | h16 | +0.017 | -0.091 .. +0.125 | +0.0019 | 0.76 / 0.76 / 0.77 | nan |  |  | 9/16 | +0.023 | +0.010 |  | +1.2 / +0.3 |  |
| MES | 15 | eod * | +0.182 | -0.371 .. +0.735 | +0.0081 | 0.52 / 0.51 / 0.53 | nan | 1 | 1 | 10/16 | +0.280 | +0.085 | False | +5.0 / +0.6 |  |
| MES | 60 | h1 | +0.004 | -0.010 .. +0.017 | +0.0020 | 0.57 / 0.56 / 0.56 | nan |  |  | 9/16 | +0.008 | -0.001 |  | +0.6 / +0.6 |  |
| MES | 60 | h2 | +0.007 | -0.020 .. +0.034 | +0.0026 | 0.62 / 0.6 / 0.6 | nan |  |  | 9/16 | +0.017 | -0.003 |  | +0.7 / +0.5 |  |
| MES | 60 | h4 | +0.013 | -0.040 .. +0.067 | +0.0035 | 0.62 / 0.61 / 0.61 | nan |  |  | 9/16 | +0.032 | -0.005 |  | +1.0 / +0.5 | 0.075 |
| MES | 60 | h8 | +0.025 | -0.079 .. +0.129 | +0.0047 | 0.64 / 0.63 / 0.63 | nan |  |  | 9/16 | +0.052 | -0.002 |  | +1.4 / +0.5 |  |
| MES | 60 | h16 | +0.051 | -0.138 .. +0.241 | +0.0074 | 0.6 / 0.59 / 0.59 | nan |  |  | 9/16 | +0.108 | -0.005 |  | +2.1 / +0.5 |  |
| MES | 60 | eod * | +0.066 | -0.148 .. +0.280 | +0.0090 | 0.55 / 0.54 / 0.54 | nan | 1 | 1 | 10/16 | +0.132 | -0.001 | False | +2.6 / +0.6 |  |
| MNQ | 5 | h1 | -0.000 | -0.004 .. +0.004 | -0.0001 | 0.88 / 0.88 / 0.9 | nan |  |  | 6/16 | -0.002 | +0.001 |  | -0.2 / -0.1 |  |
| MNQ | 5 | h2 | +0.001 | -0.007 .. +0.009 | +0.0003 | 0.81 / 0.81 / 0.85 | nan |  |  | 11/16 | -0.003 | +0.005 |  | +0.3 / +0.2 |  |
| MNQ | 5 | h4 * | +0.004 | -0.013 .. +0.020 | +0.0007 | 0.66 / 0.65 / 0.73 | nan | 1 | 1 | 11/16 | -0.005 | +0.013 | False | +0.9 / +0.4 | 0.026 |
| MNQ | 5 | h8 | +0.007 | -0.026 .. +0.041 | +0.0009 | 0.67 / 0.66 / 0.73 | nan |  |  | 11/16 | -0.011 | +0.026 |  | +1.2 / +0.4 |  |
| MNQ | 5 | h16 | +0.010 | -0.060 .. +0.081 | +0.0009 | 0.77 / 0.77 / 0.81 | nan |  |  | 11/16 | -0.023 | +0.043 |  | +1.1 / +0.3 |  |
| MNQ | 5 | eod | -0.026 | -1.331 .. +1.280 | -0.0005 | 0.97 / 0.97 / 0.97 | nan |  |  | 7/16 | +0.163 | -0.212 |  | -0.5 / -0.0 |  |
| MNQ | 15 | h1 * | -0.001 | -0.009 .. +0.006 | -0.0006 | 0.71 / 0.69 / 0.74 | nan | 1 | 1 | 6/16 | -0.002 | -0.001 | False | -0.4 / -0.4 |  |
| MNQ | 15 | h2 | -0.001 | -0.015 .. +0.014 | -0.0002 | 0.92 / 0.92 / 0.94 | nan |  |  | 6/16 | -0.005 | +0.004 |  | -0.1 / -0.1 |  |
| MNQ | 15 | h4 | -0.001 | -0.031 .. +0.029 | -0.0001 | 0.95 / 0.95 / 0.97 | nan |  |  | 5/16 | -0.011 | +0.009 |  | -0.1 / -0.1 | 0.048 |
| MNQ | 15 | h8 | -0.005 | -0.067 .. +0.056 | -0.0006 | 0.87 / 0.86 / 0.89 | nan |  |  | 6/16 | -0.022 | +0.012 |  | -0.4 / -0.2 |  |
| MNQ | 15 | h16 | -0.003 | -0.130 .. +0.124 | -0.0002 | 0.97 / 0.97 / 0.97 | nan |  |  | 5/16 | -0.042 | +0.036 |  | -0.2 / -0.0 |  |
| MNQ | 15 | eod | +0.021 | -0.634 .. +0.677 | +0.0007 | 0.95 / 0.95 / 0.95 | nan |  |  | 9/16 | +0.089 | -0.046 |  | +0.5 / +0.1 |  |
| MNQ | 60 | h1 * | +0.001 | -0.014 .. +0.015 | +0.0003 | 0.94 / 0.93 / 0.93 | nan | 1 | 1 | 8/16 | +0.002 | -0.001 | False | +0.1 / +0.1 |  |
| MNQ | 60 | h2 | +0.001 | -0.028 .. +0.030 | +0.0003 | 0.95 / 0.95 / 0.94 | nan |  |  | 8/16 | +0.004 | -0.002 |  | +0.1 / +0.1 |  |
| MNQ | 60 | h4 | +0.001 | -0.057 .. +0.059 | +0.0003 | 0.97 / 0.97 / 0.97 | nan |  |  | 8/16 | +0.009 | -0.006 |  | +0.1 / +0.0 | 0.080 |
| MNQ | 60 | h8 | +0.002 | -0.111 .. +0.115 | +0.0003 | 0.98 / 0.98 / 0.97 | nan |  |  | 8/16 | +0.014 | -0.011 |  | +0.1 / +0.0 |  |
| MNQ | 60 | h16 | +0.003 | -0.204 .. +0.210 | +0.0004 | 0.98 / 0.98 / 0.97 | nan |  |  | 9/16 | +0.039 | -0.032 |  | +0.1 / +0.0 |  |
| MNQ | 60 | eod | +0.004 | -0.227 .. +0.236 | +0.0005 | 0.97 / 0.97 / 0.97 | nan |  |  | 9/16 | +0.058 | -0.050 |  | +0.2 / +0.0 |  |
| MYM | 5 | h1 | +0.000 | -0.005 .. +0.006 | +0.0000 | 0.99 / 0.99 / 0.99 | nan |  |  | 5/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 5 | h2 | +0.000 | -0.012 .. +0.012 | +0.0000 | 0.99 / 0.99 / 1 | nan |  |  | 5/8 | n/a | +0.000 |  | +0.0 / +0.0 |  |
| MYM | 5 | h4 | +0.001 | -0.024 .. +0.025 | +0.0001 | 0.95 / 0.94 / 0.96 | nan |  |  | 5/8 | n/a | +0.001 |  | +0.1 / +0.1 | 0.041 |
| MYM | 5 | h8 | +0.005 | -0.043 .. +0.053 | +0.0006 | 0.84 / 0.83 / 0.88 | nan |  |  | 5/8 | n/a | +0.005 |  | +0.4 / +0.2 |  |
| MYM | 5 | h16 | +0.014 | -0.078 .. +0.107 | +0.0012 | 0.76 / 0.76 / 0.81 | nan |  |  | 5/8 | n/a | +0.014 |  | +1.0 / +0.3 |  |
| MYM | 5 | eod * | +0.559 | -1.034 .. +2.153 | +0.0109 | 0.49 / 0.48 / 0.57 | nan | 1 | 1 | 5/8 | n/a | +0.559 | False | +8.2 / +0.7 |  |
| MYM | 15 | h1 | -0.000 | -0.009 .. +0.009 | -0.0001 | 0.98 / 0.98 / 0.98 | nan |  |  | 4/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MYM | 15 | h2 | +0.003 | -0.016 .. +0.022 | +0.0008 | 0.74 / 0.74 / 0.82 | nan |  |  | 4/8 | n/a | +0.003 |  | +0.4 / +0.3 |  |
| MYM | 15 | h4 | +0.007 | -0.032 .. +0.046 | +0.0010 | 0.71 / 0.71 / 0.8 | nan |  |  | 5/8 | n/a | +0.007 |  | +0.6 / +0.4 | 0.065 |
| MYM | 15 | h8 | +0.014 | -0.065 .. +0.094 | +0.0015 | 0.73 / 0.73 / 0.79 | nan |  |  | 5/8 | n/a | +0.014 |  | +0.8 / +0.3 |  |
| MYM | 15 | h16 | +0.040 | -0.136 .. +0.216 | +0.0031 | 0.66 / 0.66 / 0.73 | nan |  |  | 5/8 | n/a | +0.040 |  | +1.6 / +0.4 |  |
| MYM | 15 | eod * | +0.395 | -0.438 .. +1.228 | +0.0126 | 0.35 / 0.34 / 0.46 | nan | 1 | 1 | 5/8 | n/a | +0.395 | False | +6.5 / +0.9 |  |
| MYM | 60 | h1 | +0.003 | -0.015 .. +0.022 | +0.0017 | 0.73 / 0.72 / 0.78 | nan |  |  | 4/8 | n/a | +0.003 |  | +0.3 / +0.3 |  |
| MYM | 60 | h2 | +0.005 | -0.032 .. +0.042 | +0.0018 | 0.79 / 0.79 / 0.84 | nan |  |  | 4/8 | n/a | +0.005 |  | +0.4 / +0.3 |  |
| MYM | 60 | h4 | +0.012 | -0.061 .. +0.086 | +0.0030 | 0.75 / 0.74 / 0.8 | nan |  |  | 4/8 | n/a | +0.012 |  | +0.6 / +0.3 | 0.110 |
| MYM | 60 | h8 | +0.038 | -0.105 .. +0.181 | +0.0069 | 0.6 / 0.6 / 0.69 | nan |  |  | 4/8 | n/a | +0.038 |  | +1.4 / +0.5 |  |
| MYM | 60 | h16 | +0.095 | -0.164 .. +0.354 | +0.0131 | 0.47 / 0.47 / 0.59 | nan |  |  | 4/8 | n/a | +0.095 |  | +2.7 / +0.7 |  |
| MYM | 60 | eod * | +0.117 | -0.177 .. +0.411 | +0.0155 | 0.44 / 0.42 / 0.55 | nan | 1 | 1 | 4/8 | n/a | +0.117 | False | +3.2 / +0.8 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.003 | +0.001 .. +0.005 | +0.7% | +0.003 | 0.0012 |  | 13/16 |
| MES | 5 | h2 * | +0.007 | +0.003 .. +0.011 | +1.0% | +0.007 | 0.00028 | 0.0536 | 14/16 |
| MES | 5 | h4 | +0.010 | +0.003 .. +0.018 | +1.0% | +0.013 | 0.0095 |  | 10/16 |
| MES | 5 | h8 | +0.018 | +0.002 .. +0.034 | +1.3% | +0.024 | 0.031 |  | 10/16 |
| MES | 5 | h16 | +0.034 | +0.001 .. +0.068 | +1.6% | +0.046 | 0.041 |  | 11/16 |
| MES | 5 | eod | +0.138 | -0.478 .. +0.754 | +1.4% | +0.714 | 0.66 |  | 8/16 |
| MES | 15 | h1 | +0.004 | -0.000 .. +0.008 | +0.7% | +0.006 | 0.093 |  | 11/16 |
| MES | 15 | h2 | +0.009 | +0.001 .. +0.017 | +1.2% | +0.013 | 0.036 |  | 12/16 |
| MES | 15 | h4 * | +0.018 | +0.001 .. +0.035 | +1.7% | +0.027 | 0.035 | 1 | 12/16 |
| MES | 15 | h8 | +0.033 | +0.000 .. +0.066 | +2.2% | +0.058 | 0.049 |  | 12/16 |
| MES | 15 | h16 | +0.072 | +0.003 .. +0.140 | +3.1% | +0.140 | 0.04 |  | 11/16 |
| MES | 15 | eod | +0.215 | -0.139 .. +0.569 | +3.9% | +0.693 | 0.23 |  | 9/16 |
| MES | 60 | h1 * | +0.033 | +0.023 .. +0.044 | +6.5% | +0.058 | 7e-11 | 2.29e-08 | 16/16 |
| MES | 60 | h2 | +0.049 | +0.032 .. +0.067 | +6.7% | +0.090 | 6e-08 |  | 14/16 |
| MES | 60 | h4 | +0.063 | +0.031 .. +0.096 | +6.0% | +0.132 | 0.00016 |  | 12/16 |
| MES | 60 | h8 | +0.071 | +0.010 .. +0.131 | +4.7% | +0.176 | 0.022 |  | 9/16 |
| MES | 60 | h16 | +0.051 | -0.058 .. +0.161 | +2.5% | +0.200 | 0.36 |  | 9/16 |
| MES | 60 | eod | +0.047 | -0.079 .. +0.173 | +2.2% | +0.201 | 0.47 |  | 9/16 |
| MNQ | 5 | h1 | -0.001 | -0.004 .. +0.001 | -0.2% | -0.002 | 0.39 |  | 8/16 |
| MNQ | 5 | h2 | -0.002 | -0.008 .. +0.004 | -0.3% | -0.005 | 0.45 |  | 7/16 |
| MNQ | 5 | h4 | -0.006 | -0.018 .. +0.007 | -0.5% | -0.011 | 0.36 |  | 8/16 |
| MNQ | 5 | h8 * | -0.014 | -0.043 .. +0.014 | -0.9% | -0.025 | 0.33 | 1 | 8/16 |
| MNQ | 5 | h16 | -0.026 | -0.084 .. +0.031 | -1.1% | -0.052 | 0.37 |  | 8/16 |
| MNQ | 5 | eod | +0.028 | -0.846 .. +0.902 | +0.2% | +0.225 | 0.95 |  | 7/16 |
| MNQ | 15 | h1 | -0.001 | -0.007 .. +0.004 | -0.2% | -0.001 | 0.64 |  | 8/16 |
| MNQ | 15 | h2 | -0.002 | -0.016 .. +0.011 | -0.3% | -0.003 | 0.72 |  | 6/16 |
| MNQ | 15 | h4 | -0.004 | -0.037 .. +0.028 | -0.4% | -0.005 | 0.79 |  | 6/16 |
| MNQ | 15 | h8 | -0.001 | -0.057 .. +0.055 | -0.1% | -0.005 | 0.96 |  | 7/16 |
| MNQ | 15 | h16 * | +0.037 | -0.052 .. +0.126 | +1.5% | +0.033 | 0.41 | 1 | 10/16 |
| MNQ | 15 | eod | +0.159 | -0.318 .. +0.636 | +2.5% | +0.434 | 0.51 |  | 8/16 |
| MNQ | 60 | h1 * | +0.034 | +0.022 .. +0.045 | +6.4% | +0.063 | 1.1e-08 | 3.23e-06 | 16/16 |
| MNQ | 60 | h2 | +0.051 | +0.031 .. +0.072 | +6.7% | +0.099 | 8.4e-07 |  | 15/16 |
| MNQ | 60 | h4 | +0.072 | +0.034 .. +0.110 | +6.5% | +0.139 | 0.00019 |  | 12/16 |
| MNQ | 60 | h8 | +0.083 | +0.013 .. +0.152 | +5.2% | +0.167 | 0.019 |  | 11/16 |
| MNQ | 60 | h16 | +0.061 | -0.067 .. +0.188 | +2.8% | +0.144 | 0.35 |  | 8/16 |
| MNQ | 60 | eod | +0.057 | -0.088 .. +0.203 | +2.5% | +0.144 | 0.44 |  | 8/16 |
| MYM | 5 | h1 | +0.001 | -0.002 .. +0.004 | +0.2% | -0.002 | 0.54 |  | 5/8 |
| MYM | 5 | h2 | +0.004 | -0.003 .. +0.011 | +0.5% | -0.002 | 0.35 |  | 6/8 |
| MYM | 5 | h4 | +0.009 | -0.007 .. +0.024 | +0.8% | +0.003 | 0.28 |  | 6/8 |
| MYM | 5 | h8 | +0.017 | -0.012 .. +0.046 | +1.1% | +0.005 | 0.27 |  | 4/8 |
| MYM | 5 | h16 * | +0.035 | -0.024 .. +0.094 | +1.5% | +0.001 | 0.24 | 1 | 6/8 |
| MYM | 5 | eod | +0.119 | -0.874 .. +1.112 | +1.0% | +0.645 | 0.82 |  | 3/8 |
| MYM | 15 | h1 * | +0.005 | -0.002 .. +0.013 | +1.0% | +0.003 | 0.18 | 1 | 7/8 |
| MYM | 15 | h2 | +0.010 | -0.008 .. +0.028 | +1.3% | +0.005 | 0.29 |  | 6/8 |
| MYM | 15 | h4 | +0.015 | -0.025 .. +0.054 | +1.3% | +0.010 | 0.47 |  | 7/8 |
| MYM | 15 | h8 | +0.036 | -0.033 .. +0.105 | +2.2% | +0.025 | 0.3 |  | 6/8 |
| MYM | 15 | h16 | +0.044 | -0.094 .. +0.182 | +1.8% | +0.083 | 0.53 |  | 6/8 |
| MYM | 15 | eod | +0.202 | -0.363 .. +0.768 | +3.4% | +0.662 | 0.48 |  | 5/8 |
| MYM | 60 | h1 * | +0.033 | +0.016 .. +0.050 | +6.3% | +0.046 | 0.0001 | 0.0214 | 8/8 |
| MYM | 60 | h2 | +0.057 | +0.028 .. +0.086 | +7.5% | +0.078 | 0.00011 |  | 8/8 |
| MYM | 60 | h4 | +0.059 | +0.010 .. +0.108 | +5.5% | +0.119 | 0.017 |  | 6/8 |
| MYM | 60 | h8 | +0.059 | -0.026 .. +0.145 | +3.8% | +0.159 | 0.17 |  | 6/8 |
| MYM | 60 | h16 | +0.052 | -0.102 .. +0.206 | +2.4% | +0.205 | 0.51 |  | 5/8 |
| MYM | 60 | eod | +0.047 | -0.128 .. +0.222 | +2.1% | +0.204 | 0.6 |  | 4/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.22 pts | -0.26 .. +0.71 | 0.37 |
| MES | 15 | +0.46 pts | -0.35 .. +1.28 | 0.26 |
| MES | 60 | +1.29 pts | -0.41 .. +2.99 | 0.14 |
| MNQ | 5 | -0.02 pts | -0.49 .. +0.45 | 0.94 |
| MNQ | 15 | +0.04 pts | -0.78 .. +0.86 | 0.93 |
| MNQ | 60 | +0.30 pts | -1.48 .. +2.08 | 0.74 |
| MYM | 5 | +0.03 pts | -0.62 .. +0.68 | 0.92 |
| MYM | 15 | +0.61 pts | -0.54 .. +1.77 | 0.3 |
| MYM | 60 | +0.19 pts | -2.21 .. +2.58 | 0.88 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 208984 | +0.003 | 0.317 | -0.00 | -3.50 | -3.47 | -3.53 | -3.51 |
| MES | 5 | h2 | event | long | 208984 | +0.007 | 0.317 | +0.01 | -3.49 | -3.44 | -3.54 | -3.51 |
| MES | 5 | h4 | event | long | 208984 | +0.015 | 0.317 | +0.03 | -3.47 | -3.38 | -3.56 | -3.52 |
| MES | 5 | h8 | event | long | 208984 | +0.030 | 0.317 | +0.07 | -3.43 | -3.25 | -3.60 | -3.54 |
| MES | 5 | h16 | event | long | 208984 | +0.060 | 0.317 | +0.16 | -3.34 | -3.01 | -3.66 | -3.60 |
| MES | 5 | eod | event | long | 208984 | +0.717 | 0.317 | +1.68 | -1.82 | +1.82 | -5.41 | -3.68 |
| MES | 15 | h1 | event | long | 69166 | +0.005 | 0.181 | +0.01 | -3.49 | -3.42 | -3.56 | -3.53 |
| MES | 15 | h2 | event | long | 69166 | +0.011 | 0.181 | +0.04 | -3.46 | -3.32 | -3.59 | -3.54 |
| MES | 15 | h4 | event | long | 69166 | +0.023 | 0.181 | +0.11 | -3.39 | -3.13 | -3.64 | -3.54 |
| MES | 15 | h8 | event | long | 69166 | +0.045 | 0.181 | +0.25 | -3.25 | -2.77 | -3.72 | -3.55 |
| MES | 15 | h16 | event | long | 69166 | +0.087 | 0.181 | +0.46 | -3.04 | -2.13 | -3.95 | -3.54 |
| MES | 15 | eod | event | long | 69166 | +0.410 | 0.181 | +1.65 | -1.85 | +1.80 | -5.45 | -2.89 |
| MES | 60 | h1 | event | long | 17030 | +0.011 | 0.092 | +0.10 | -3.40 | -3.14 | -3.66 | -3.57 |
| MES | 60 | h2 | event | long | 17030 | +0.022 | 0.092 | +0.22 | -3.28 | -2.79 | -3.76 | -3.66 |
| MES | 60 | h4 | event | long | 17030 | +0.044 | 0.092 | +0.43 | -3.07 | -2.14 | -3.98 | -3.89 |
| MES | 60 | h8 | event | long | 17030 | +0.085 | 0.092 | +0.88 | -2.62 | -0.92 | -4.30 | -4.24 |
| MES | 60 | h16 | event | long | 17030 | +0.147 | 0.092 | +1.63 | -1.87 | +1.07 | -4.79 | -4.47 |
| MES | 60 | eod | event | long | 17030 | +0.175 | 0.092 | +1.60 | -1.90 | +1.75 | -5.53 | -5.07 |
| MNQ | 5 | h1 | event | short | 208655 | -0.004 | 0.127 | +0.01 | -1.99 | -2.01 | -1.97 | -1.97 |
| MNQ | 5 | h2 | event | long | 208655 | +0.008 | 0.127 | -0.01 | -2.01 | -1.97 | -2.05 | -2.03 |
| MNQ | 5 | h4 | event | long | 208655 | +0.018 | 0.127 | -0.02 | -2.02 | -1.93 | -2.10 | -2.04 |
| MNQ | 5 | h8 | event | long | 208655 | +0.036 | 0.127 | -0.03 | -2.03 | -1.86 | -2.20 | -2.10 |
| MNQ | 5 | h16 | event | long | 208655 | +0.071 | 0.127 | -0.05 | -2.05 | -1.73 | -2.36 | -2.27 |
| MNQ | 5 | eod | event | short | 208655 | -0.740 | 0.127 | +3.87 | +1.87 | -4.55 | +8.18 | +3.70 |
| MNQ | 15 | h1 | event | short | 69098 | -0.006 | 0.072 | +0.02 | -1.98 | -2.05 | -1.90 | -1.87 |
| MNQ | 15 | h2 | event | short | 69098 | -0.012 | 0.072 | +0.03 | -1.97 | -2.11 | -1.83 | -1.81 |
| MNQ | 15 | h4 | event | short | 69098 | -0.024 | 0.072 | +0.04 | -1.96 | -2.21 | -1.70 | -1.65 |
| MNQ | 15 | h8 | event | short | 69098 | -0.046 | 0.072 | +0.07 | -1.93 | -2.40 | -1.45 | -1.29 |
| MNQ | 15 | h16 | event | short | 69098 | -0.086 | 0.072 | +0.32 | -1.68 | -2.70 | -0.67 | -0.98 |
| MNQ | 15 | eod | event | long | 69098 | +0.350 | 0.072 | -3.83 | -5.83 | +0.56 | -12.13 | -6.74 |
| MNQ | 60 | h1 | event | long | 16989 | +0.010 | 0.036 | -0.03 | -2.03 | -1.79 | -2.27 | -2.28 |
| MNQ | 60 | h2 | event | long | 16989 | +0.020 | 0.036 | -0.06 | -2.06 | -1.60 | -2.51 | -2.56 |
| MNQ | 60 | h4 | event | long | 16989 | +0.038 | 0.036 | -0.26 | -2.26 | -1.31 | -3.20 | -3.28 |
| MNQ | 60 | h8 | event | long | 16989 | +0.070 | 0.036 | -0.67 | -2.67 | -0.83 | -4.51 | -4.52 |
| MNQ | 60 | h16 | event | long | 16989 | +0.112 | 0.036 | -2.32 | -4.32 | +0.02 | -8.64 | -6.99 |
| MNQ | 60 | eod | event | long | 16989 | +0.133 | 0.036 | -3.49 | -5.49 | +0.58 | -11.54 | -8.91 |
| MYM | 5 | h1 | event | long | 105196 | -0.001 | 0.166 | -0.02 | -2.02 | +nan | -2.02 | -2.01 |
| MYM | 5 | h2 | event | long | 105196 | -0.002 | 0.166 | -0.03 | -2.03 | +nan | -2.03 | -2.00 |
| MYM | 5 | h4 | event | long | 105196 | -0.005 | 0.166 | -0.05 | -2.05 | +nan | -2.05 | -1.98 |
| MYM | 5 | h8 | event | long | 105196 | -0.004 | 0.166 | -0.10 | -2.10 | +nan | -2.10 | -1.99 |
| MYM | 5 | h16 | event | long | 105196 | +0.008 | 0.166 | -0.17 | -2.17 | +nan | -2.17 | -2.08 |
| MYM | 5 | eod | event | long | 105196 | +0.655 | 0.166 | +1.03 | -0.97 | +nan | -0.97 | -1.51 |
| MYM | 15 | h1 | event | short | 34816 | -0.001 | 0.093 | +0.04 | -1.96 | +nan | -1.96 | -1.96 |
| MYM | 15 | h2 | event | long | 34816 | +0.003 | 0.093 | -0.07 | -2.07 | +nan | -2.07 | -2.04 |
| MYM | 15 | h4 | event | long | 34816 | +0.007 | 0.093 | -0.13 | -2.13 | +nan | -2.13 | -2.07 |
| MYM | 15 | h8 | event | long | 34816 | +0.010 | 0.093 | -0.24 | -2.24 | +nan | -2.24 | -2.08 |
| MYM | 15 | h16 | event | long | 34816 | +0.018 | 0.093 | -0.43 | -2.43 | +nan | -2.43 | -1.91 |
| MYM | 15 | eod | event | long | 34816 | +0.370 | 0.093 | +1.00 | -1.00 | +nan | -1.00 | -0.09 |
| MYM | 60 | h1 | event | long | 8547 | +0.007 | 0.046 | -0.09 | -2.09 | +nan | -2.09 | -2.22 |
| MYM | 60 | h2 | event | long | 8547 | +0.012 | 0.046 | -0.22 | -2.22 | +nan | -2.22 | -2.48 |
| MYM | 60 | h4 | event | long | 8547 | +0.026 | 0.046 | -0.39 | -2.39 | +nan | -2.39 | -2.97 |
| MYM | 60 | h8 | event | long | 8547 | +0.059 | 0.046 | -0.51 | -2.51 | +nan | -2.51 | -3.54 |
| MYM | 60 | h16 | event | long | 8547 | +0.122 | 0.046 | +0.38 | -1.62 | +nan | -1.62 | -3.34 |
| MYM | 60 | eod | event | long | 8547 | +0.153 | 0.046 | +0.83 | -1.17 | +nan | -1.17 | -3.53 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.016 | -0.009 | -0.005 | -0.002 | -0.000 | +0.000 | +0.001 | +0.002 | +0.004 | +0.008 | +0.009 |
| MES | 15 | -0.048 | -0.025 | -0.011 | -0.005 | -0.002 | +0.000 | +0.001 | +0.002 | +0.002 | +0.001 | +0.002 |
| MES | 60 | -0.061 | -0.032 | -0.017 | -0.007 | -0.003 | +0.000 | +0.002 | +0.003 | +0.003 | +0.004 | +0.011 |
| MNQ | 5 | -0.015 | -0.007 | -0.004 | -0.002 | -0.001 | +0.000 | +0.001 | +0.003 | +0.004 | +0.008 | +0.009 |
| MNQ | 15 | -0.030 | -0.015 | -0.007 | -0.003 | -0.002 | +0.000 | +0.001 | +0.002 | +0.001 | -0.005 | -0.004 |
| MNQ | 60 | -0.048 | -0.028 | -0.009 | -0.003 | -0.001 | +0.000 | -0.001 | -0.002 | -0.007 | -0.009 | -0.015 |
| MYM | 5 | -0.031 | -0.015 | -0.007 | -0.003 | -0.001 | +0.000 | +0.001 | +0.000 | +0.001 | +0.004 | +0.008 |
| MYM | 15 | -0.064 | -0.032 | -0.013 | -0.006 | -0.003 | +0.000 | +0.004 | +0.007 | +0.011 | +0.014 | +0.040 |
| MYM | 60 | -0.093 | -0.042 | -0.023 | -0.010 | -0.005 | +0.000 | +0.002 | +0.004 | +0.007 | +0.019 | +0.050 |

## Calibration

- MES 5-min: 1036271 bars, 208984 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 69166 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 17030 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 208655 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 69098 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 70% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 16989 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 105196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34816 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8547 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
