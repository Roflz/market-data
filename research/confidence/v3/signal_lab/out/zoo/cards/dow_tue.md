# Impact card: dow_tue

session weekday = tue vs other days [controls: volatility decile, EMA trend state, last-bar sign, year (slot / weekday NOT controlled)]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best -0.031 R20 over the next 16 bars (80 min), p=1; we would catch an effect of 0.020 R20 or more 80% of the time).
- MES 5-min size: no measurable effect on how much price moves (best p=0.048).
- MES 5-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.48 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.232 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: no measurable direction effect (best -0.003 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.037 R20 or more 80% of the time).
- MES 15-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.014 R20, CONFIRMED, q=1.23e-07, 15 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.43 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.134 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.119 R20 over the next 16 bars (16 h), p=1; we would catch an effect of 0.074 R20 or more 80% of the time).
- MES 60-min size: no measurable effect on how much price moves (best p=1).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $4.92 at recent bar sizes, 90% range up to $6.67); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.562 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.025 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 4% MORE after the event than after matched bars over the next 16 bars (80 min) (+0.088 R20, CONFIRMED, q=0.00415, 14 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $11.08 at recent bar sizes, 90% range up to $0.80); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.328 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.045 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 3% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.017 R20, CONFIRMED, q=4.65e-10, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $11.25 at recent bar sizes, 90% range up to $2.18); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best +0.002 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.080 R20 or more 80% of the time).
- MNQ 60-min size: no measurable effect on how much price moves (best p=1).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.16 at recent bar sizes, 90% range up to $7.70); about 25.7x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best -1.891 R20 over the rest of the session (to 16:45), p=0.16; we would catch an effect of 0.041 R20 or more 80% of the time).
- MYM 5-min size: no measurable effect on how much price moves (best p=0.01).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $17.21 at recent bar sizes, 90% range up to $0.74); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best -0.012 R20 over the next 1 bar (15 min), p=0.097; we would catch an effect of 0.070 R20 or more 80% of the time).
- MYM 15-min size: the market moves 2% MORE after the event than after matched bars over the next 1 bar (15 min) (+0.013 R20, possible, q=0.201, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.19 at recent bar sizes, 90% range up to $2.54); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.417 R20 over the next 16 bars (16 h), p=0.023; we would catch an effect of 0.110 R20 or more 80% of the time).
- MYM 60-min size: no measurable effect on how much price moves (best p=1).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $13.36 at recent bar sizes, 90% range up to $11.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.002 | -0.006 .. +0.002 | -0.0010 | 0.32 / 0.31 / 0.32 | nan |  |  | 10/16 | +0.001 | -0.005 |  | -1.1 / -1.0 |  |
| MES | 5 | h2 | -0.003 | -0.011 .. +0.004 | -0.0013 | 0.35 / 0.33 / 0.35 | nan |  |  | 9/16 | +0.003 | -0.010 |  | -1.4 / -0.9 |  |
| MES | 5 | h4 | -0.007 | -0.021 .. +0.008 | -0.0018 | 0.36 / 0.35 / 0.36 | nan |  |  | 8/16 | +0.006 | -0.020 |  | -1.9 / -0.9 | 0.020 |
| MES | 5 | h8 | -0.014 | -0.044 .. +0.016 | -0.0026 | 0.35 / 0.34 / 0.35 | nan |  |  | 8/16 | +0.012 | -0.040 |  | -2.7 / -0.9 |  |
| MES | 5 | h16 * | -0.031 | -0.092 .. +0.030 | -0.0040 | 0.31 / 0.3 / 0.3 | nan | 1 | 1 | 8/16 | +0.020 | -0.083 | False | -4.1 / -1.0 |  |
| MES | 5 | eod | -0.289 | -1.263 .. +0.685 | -0.0073 | 0.56 / 0.56 / 0.56 | nan |  |  | 12/16 | +0.498 | -1.071 |  | -7.7 / -0.6 |  |
| MES | 15 | h1 * | -0.003 | -0.010 .. +0.003 | -0.0017 | 0.32 / 0.31 / 0.35 | nan | 1 | 1 | 9/16 | +0.003 | -0.009 | False | -1.0 / -1.0 |  |
| MES | 15 | h2 | -0.006 | -0.019 .. +0.008 | -0.0019 | 0.4 / 0.39 / 0.4 | nan |  |  | 8/16 | +0.005 | -0.016 |  | -1.2 / -0.8 |  |
| MES | 15 | h4 | -0.011 | -0.037 .. +0.016 | -0.0025 | 0.44 / 0.43 / 0.44 | nan |  |  | 7/16 | +0.010 | -0.031 |  | -1.5 / -0.8 | 0.037 |
| MES | 15 | h8 | -0.020 | -0.074 .. +0.035 | -0.0032 | 0.49 / 0.47 / 0.48 | nan |  |  | 7/16 | +0.021 | -0.060 |  | -2.0 / -0.7 |  |
| MES | 15 | h16 | -0.033 | -0.148 .. +0.081 | -0.0038 | 0.57 / 0.55 / 0.56 | nan |  |  | 7/16 | +0.050 | -0.117 |  | -2.3 / -0.6 |  |
| MES | 15 | eod | -0.138 | -0.685 .. +0.408 | -0.0061 | 0.62 / 0.62 / 0.63 | nan |  |  | 12/16 | +0.289 | -0.563 |  | -3.9 / -0.5 |  |
| MES | 60 | h1 | -0.006 | -0.020 .. +0.008 | -0.0033 | 0.38 / 0.38 / 0.36 | nan |  |  | 9/16 | +0.009 | -0.021 |  | -0.9 / -0.9 |  |
| MES | 60 | h2 | -0.013 | -0.041 .. +0.015 | -0.0048 | 0.37 / 0.36 / 0.34 | nan |  |  | 10/16 | +0.018 | -0.043 |  | -1.3 / -0.9 |  |
| MES | 60 | h4 | -0.029 | -0.083 .. +0.025 | -0.0076 | 0.3 / 0.29 / 0.28 | nan |  |  | 12/16 | +0.029 | -0.086 |  | -2.1 / -1.0 | 0.074 |
| MES | 60 | h8 | -0.063 | -0.167 .. +0.042 | -0.0120 | 0.24 / 0.24 / 0.23 | nan |  |  | 12/16 | +0.046 | -0.172 |  | -3.3 / -1.2 |  |
| MES | 60 | h16 * | -0.119 | -0.308 .. +0.070 | -0.0174 | 0.22 / 0.22 / 0.21 | nan | 1 | 1 | 12/16 | +0.088 | -0.326 | False | -4.8 / -1.2 |  |
| MES | 60 | eod | -0.124 | -0.333 .. +0.085 | -0.0173 | 0.24 / 0.25 / 0.25 | nan |  |  | 12/16 | +0.099 | -0.347 |  | -4.8 / -1.2 |  |
| MNQ | 5 | h1 | +0.001 | -0.004 .. +0.005 | +0.0003 | 0.77 / 0.75 / 0.78 | nan |  |  | 9/16 | +0.004 | -0.002 |  | +0.3 / +0.3 |  |
| MNQ | 5 | h2 | +0.003 | -0.006 .. +0.012 | +0.0007 | 0.57 / 0.53 / 0.6 | nan |  |  | 9/16 | +0.008 | -0.003 |  | +0.9 / +0.6 |  |
| MNQ | 5 | h4 | +0.006 | -0.013 .. +0.024 | +0.0010 | 0.54 / 0.51 / 0.6 | nan |  |  | 9/16 | +0.017 | -0.006 |  | +1.3 / +0.6 | 0.025 |
| MNQ | 5 | h8 | +0.008 | -0.029 .. +0.045 | +0.0010 | 0.68 / 0.65 / 0.71 | nan |  |  | 8/16 | +0.036 | -0.020 |  | +1.2 / +0.4 |  |
| MNQ | 5 | h16 | -0.001 | -0.083 .. +0.081 | -0.0001 | 0.99 / 0.99 / 0.99 | nan |  |  | 8/16 | +0.071 | -0.072 |  | -0.1 / -0.0 |  |
| MNQ | 5 | eod * | +0.562 | -0.798 .. +1.922 | +0.0103 | 0.42 / 0.4 / 0.36 | nan | 1 | 1 | 10/16 | +1.353 | -0.222 | False | +11.1 / +0.8 |  |
| MNQ | 15 | h1 | -0.001 | -0.009 .. +0.008 | -0.0003 | 0.87 / 0.86 / 0.87 | nan |  |  | 8/16 | +0.006 | -0.008 |  | -0.2 / -0.2 |  |
| MNQ | 15 | h2 | -0.001 | -0.017 .. +0.016 | -0.0002 | 0.93 / 0.92 / 0.94 | nan |  |  | 8/16 | +0.013 | -0.015 |  | -0.1 / -0.1 |  |
| MNQ | 15 | h4 | -0.001 | -0.036 .. +0.033 | -0.0002 | 0.94 / 0.94 / 0.95 | nan |  |  | 8/16 | +0.028 | -0.030 |  | -0.1 / -0.1 | 0.045 |
| MNQ | 15 | h8 | +0.005 | -0.063 .. +0.072 | +0.0005 | 0.9 / 0.89 / 0.91 | nan |  |  | 8/16 | +0.057 | -0.048 |  | +0.3 / +0.1 |  |
| MNQ | 15 | h16 | +0.034 | -0.106 .. +0.173 | +0.0030 | 0.64 / 0.61 / 0.63 | nan |  |  | 9/16 | +0.123 | -0.055 |  | +1.9 / +0.5 |  |
| MNQ | 15 | eod * | +0.328 | -0.369 .. +1.025 | +0.0101 | 0.36 / 0.34 / 0.35 | nan | 1 | 1 | 10/16 | +0.730 | -0.071 | False | +7.2 / +0.9 |  |
| MNQ | 60 | h1 * | +0.002 | -0.013 .. +0.018 | +0.0012 | 0.77 / 0.76 / 0.74 | nan | 1 | 1 | 7/16 | +0.016 | -0.011 | False | +0.3 / +0.3 |  |
| MNQ | 60 | h2 | +0.005 | -0.027 .. +0.036 | +0.0016 | 0.77 / 0.76 / 0.74 | nan |  |  | 7/16 | +0.032 | -0.023 |  | +0.4 / +0.3 |  |
| MNQ | 60 | h4 | +0.007 | -0.054 .. +0.068 | +0.0018 | 0.81 / 0.81 / 0.79 | nan |  |  | 7/16 | +0.056 | -0.042 |  | +0.5 / +0.2 | 0.080 |
| MNQ | 60 | h8 | +0.009 | -0.109 .. +0.126 | +0.0016 | 0.88 / 0.88 / 0.87 | nan |  |  | 7/16 | +0.095 | -0.078 |  | +0.4 / +0.1 |  |
| MNQ | 60 | h16 | +0.009 | -0.203 .. +0.222 | +0.0013 | 0.93 / 0.93 / 0.92 | nan |  |  | 7/16 | +0.175 | -0.157 |  | +0.4 / +0.1 |  |
| MNQ | 60 | eod | +0.024 | -0.210 .. +0.258 | +0.0031 | 0.84 / 0.84 / 0.82 | nan |  |  | 9/16 | +0.201 | -0.154 |  | +0.9 / +0.2 |  |
| MYM | 5 | h1 | -0.006 | -0.012 .. -0.001 | -0.0026 | 0.027 / 0.034 / 0.073 | nan |  |  | 6/8 | n/a | -0.006 |  | -2.2 / -2.2 |  |
| MYM | 5 | h2 | -0.010 | -0.023 .. +0.003 | -0.0025 | 0.12 / 0.14 / 0.19 | nan |  |  | 6/8 | n/a | -0.010 |  | -2.3 / -1.5 |  |
| MYM | 5 | h4 | -0.018 | -0.046 .. +0.010 | -0.0028 | 0.21 / 0.23 / 0.28 | nan |  |  | 6/8 | n/a | -0.018 |  | -2.8 / -1.3 | 0.041 |
| MYM | 5 | h8 | -0.040 | -0.095 .. +0.015 | -0.0044 | 0.16 / 0.17 / 0.21 | nan |  |  | 6/8 | n/a | -0.040 |  | -4.2 / -1.4 |  |
| MYM | 5 | h16 | -0.094 | -0.195 .. +0.007 | -0.0082 | 0.067 / 0.078 / 0.11 | nan |  |  | 6/8 | n/a | -0.094 |  | -7.2 / -1.8 |  |
| MYM | 5 | eod * | -1.891 | -3.476 .. -0.307 | -0.0368 | 0.019 / 0.027 / 0.053 | nan | 1 | 0.968 | 7/8 | n/a | -1.891 | False | -28.1 / -2.3 |  |
| MYM | 15 | h1 * | -0.012 | -0.021 .. -0.002 | -0.0049 | 0.013 / 0.016 / 0.043 | nan | 1 | 0.914 | 6/8 | n/a | -0.012 | False | -2.3 / -2.5 |  |
| MYM | 15 | h2 | -0.020 | -0.041 .. +0.000 | -0.0048 | 0.054 / 0.06 / 0.15 | nan |  |  | 5/8 | n/a | -0.020 |  | -2.6 / -1.9 |  |
| MYM | 15 | h4 | -0.040 | -0.084 .. +0.003 | -0.0057 | 0.068 / 0.074 / 0.17 | nan |  |  | 5/8 | n/a | -0.040 |  | -3.3 / -1.8 | 0.070 |
| MYM | 15 | h8 | -0.081 | -0.171 .. +0.008 | -0.0088 | 0.074 / 0.079 / 0.13 | nan |  |  | 5/8 | n/a | -0.081 |  | -4.8 / -1.8 |  |
| MYM | 15 | h16 | -0.168 | -0.364 .. +0.028 | -0.0130 | 0.093 / 0.099 / 0.14 | nan |  |  | 5/8 | n/a | -0.168 |  | -6.8 / -1.7 |  |
| MYM | 15 | eod | -0.935 | -1.767 .. -0.103 | -0.0298 | 0.028 / 0.039 / 0.078 | nan |  |  | 7/8 | n/a | -0.935 |  | -15.2 / -2.2 |  |
| MYM | 60 | h1 | -0.027 | -0.046 .. -0.008 | -0.0136 | 0.0056 / 0.0086 / 0.027 | nan |  |  | 6/8 | n/a | -0.027 |  | -2.6 / -2.8 |  |
| MYM | 60 | h2 | -0.054 | -0.092 .. -0.015 | -0.0189 | 0.0065 / 0.0097 / 0.029 | nan |  |  | 6/8 | n/a | -0.054 |  | -3.7 / -2.7 |  |
| MYM | 60 | h4 | -0.105 | -0.181 .. -0.029 | -0.0265 | 0.0067 / 0.01 / 0.029 | nan |  |  | 6/8 | n/a | -0.105 |  | -5.1 / -2.7 | 0.110 |
| MYM | 60 | h8 | -0.219 | -0.367 .. -0.070 | -0.0400 | 0.0039 / 0.0061 / 0.022 | nan |  |  | 7/8 | n/a | -0.219 |  | -7.7 / -2.9 |  |
| MYM | 60 | h16 * | -0.417 | -0.688 .. -0.146 | -0.0581 | 0.0026 / 0.0039 / 0.019 | nan | 0.591 | 0.473 | 7/8 | n/a | -0.417 | False | -11.1 / -3.0 |  |
| MYM | 60 | eod | -0.439 | -0.735 .. -0.144 | -0.0585 | 0.0035 / 0.0054 / 0.025 | nan |  |  | 7/8 | n/a | -0.439 |  | -11.3 / -2.9 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.002 | -0.000 .. +0.004 | +0.4% | +0.001 | 0.053 |  | 12/16 |
| MES | 5 | h2 * | +0.005 | +0.001 .. +0.009 | +0.7% | +0.003 | 0.008 | 1 | 11/16 |
| MES | 5 | h4 | +0.009 | +0.002 .. +0.017 | +0.9% | +0.006 | 0.012 |  | 10/16 |
| MES | 5 | h8 | +0.019 | +0.004 .. +0.033 | +1.3% | +0.012 | 0.013 |  | 10/16 |
| MES | 5 | h16 | +0.034 | +0.004 .. +0.064 | +1.6% | +0.023 | 0.028 |  | 10/16 |
| MES | 5 | eod | +0.112 | -0.475 .. +0.698 | +1.1% | +0.738 | 0.71 |  | 9/16 |
| MES | 15 | h1 * | +0.014 | +0.009 .. +0.018 | +2.7% | +0.018 | 3.9e-10 | 1.23e-07 | 15/16 |
| MES | 15 | h2 | +0.020 | +0.013 .. +0.028 | +2.8% | +0.027 | 4.4e-07 |  | 13/16 |
| MES | 15 | h4 | +0.029 | +0.012 .. +0.046 | +2.8% | +0.042 | 0.00057 |  | 11/16 |
| MES | 15 | h8 | +0.056 | +0.024 .. +0.088 | +3.6% | +0.069 | 0.00056 |  | 13/16 |
| MES | 15 | h16 | +0.105 | +0.039 .. +0.171 | +4.6% | +0.117 | 0.0019 |  | 13/16 |
| MES | 15 | eod | +0.103 | -0.233 .. +0.440 | +1.9% | +0.504 | 0.55 |  | 10/16 |
| MES | 60 | h1 | -0.006 | -0.016 .. +0.004 | -1.2% | -0.016 | 0.25 |  | 7/16 |
| MES | 60 | h2 | -0.007 | -0.024 .. +0.010 | -0.9% | -0.024 | 0.45 |  | 9/16 |
| MES | 60 | h4 | +0.000 | -0.031 .. +0.032 | +0.0% | -0.018 | 0.99 |  | 10/16 |
| MES | 60 | h8 | +0.020 | -0.036 .. +0.076 | +1.3% | +0.045 | 0.49 |  | 10/16 |
| MES | 60 | h16 * | +0.075 | -0.033 .. +0.183 | +3.6% | +0.213 | 0.17 | 1 | 10/16 |
| MES | 60 | eod | +0.062 | -0.059 .. +0.183 | +2.9% | +0.231 | 0.32 |  | 10/16 |
| MNQ | 5 | h1 | +0.004 | +0.001 .. +0.007 | +0.7% | +0.004 | 0.0036 |  | 12/16 |
| MNQ | 5 | h2 | +0.008 | +0.002 .. +0.014 | +1.1% | +0.009 | 0.0062 |  | 14/16 |
| MNQ | 5 | h4 | +0.019 | +0.008 .. +0.031 | +1.7% | +0.017 | 0.0011 |  | 13/16 |
| MNQ | 5 | h8 | +0.038 | +0.017 .. +0.059 | +2.3% | +0.034 | 0.00041 |  | 13/16 |
| MNQ | 5 | h16 * | +0.088 | +0.048 .. +0.128 | +3.7% | +0.076 | 1.9e-05 | 0.00415 | 14/16 |
| MNQ | 5 | eod | +0.318 | -0.445 .. +1.081 | +2.5% | +1.536 | 0.42 |  | 8/16 |
| MNQ | 15 | h1 * | +0.017 | +0.012 .. +0.022 | +3.2% | +0.020 | 1.3e-12 | 4.65e-10 | 16/16 |
| MNQ | 15 | h2 | +0.028 | +0.019 .. +0.037 | +3.6% | +0.033 | 1.4e-09 |  | 15/16 |
| MNQ | 15 | h4 | +0.043 | +0.022 .. +0.064 | +3.8% | +0.052 | 8.1e-05 |  | 13/16 |
| MNQ | 15 | h8 | +0.080 | +0.034 .. +0.125 | +4.8% | +0.088 | 0.00059 |  | 14/16 |
| MNQ | 15 | h16 | +0.148 | +0.066 .. +0.231 | +5.9% | +0.158 | 0.00041 |  | 13/16 |
| MNQ | 15 | eod | +0.147 | -0.272 .. +0.566 | +2.3% | +0.755 | 0.5 |  | 9/16 |
| MNQ | 60 | h1 | -0.006 | -0.017 .. +0.006 | -1.0% | -0.016 | 0.33 |  | 10/16 |
| MNQ | 60 | h2 | -0.008 | -0.028 .. +0.012 | -1.0% | -0.022 | 0.44 |  | 8/16 |
| MNQ | 60 | h4 | -0.004 | -0.041 .. +0.033 | -0.4% | -0.009 | 0.82 |  | 5/16 |
| MNQ | 60 | h8 | +0.016 | -0.048 .. +0.080 | +1.0% | +0.066 | 0.62 |  | 10/16 |
| MNQ | 60 | h16 * | +0.063 | -0.056 .. +0.181 | +2.9% | +0.243 | 0.3 | 1 | 9/16 |
| MNQ | 60 | eod | +0.058 | -0.074 .. +0.190 | +2.5% | +0.262 | 0.39 |  | 8/16 |
| MYM | 5 | h1 * | +0.007 | +0.003 .. +0.011 | +1.3% | +0.004 | 0.0017 | 0.285 | 7/8 |
| MYM | 5 | h2 | +0.012 | +0.002 .. +0.023 | +1.6% | +0.010 | 0.018 |  | 7/8 |
| MYM | 5 | h4 | +0.014 | -0.009 .. +0.037 | +1.3% | +0.017 | 0.24 |  | 6/8 |
| MYM | 5 | h8 | +0.021 | -0.023 .. +0.065 | +1.3% | +0.026 | 0.36 |  | 5/8 |
| MYM | 5 | h16 | +0.028 | -0.041 .. +0.097 | +1.2% | +0.037 | 0.42 |  | 4/8 |
| MYM | 5 | eod | +0.231 | -0.788 .. +1.250 | +2.0% | +0.901 | 0.67 |  | 4/8 |
| MYM | 15 | h1 * | +0.013 | +0.005 .. +0.021 | +2.4% | +0.014 | 0.0012 | 0.201 | 8/8 |
| MYM | 15 | h2 | +0.015 | -0.003 .. +0.033 | +2.0% | +0.020 | 0.094 |  | 5/8 |
| MYM | 15 | h4 | +0.014 | -0.025 .. +0.053 | +1.3% | +0.025 | 0.48 |  | 4/8 |
| MYM | 15 | h8 | +0.018 | -0.050 .. +0.086 | +1.1% | +0.027 | 0.6 |  | 6/8 |
| MYM | 15 | h16 | +0.046 | -0.089 .. +0.181 | +1.9% | +0.036 | 0.51 |  | 5/8 |
| MYM | 15 | eod | +0.136 | -0.433 .. +0.705 | +2.3% | +0.469 | 0.65 |  | 4/8 |
| MYM | 60 | h1 | +0.000 | -0.014 .. +0.015 | +0.1% | -0.005 | 0.95 |  | 5/8 |
| MYM | 60 | h2 | -0.010 | -0.035 .. +0.014 | -1.4% | -0.013 | 0.43 |  | 5/8 |
| MYM | 60 | h4 | -0.004 | -0.047 .. +0.039 | -0.4% | -0.004 | 0.87 |  | 2/8 |
| MYM | 60 | h8 | +0.017 | -0.064 .. +0.098 | +1.1% | +0.061 | 0.69 |  | 5/8 |
| MYM | 60 | h16 * | +0.099 | -0.056 .. +0.254 | +4.7% | +0.225 | 0.23 | 1 | 5/8 |
| MYM | 60 | eod | +0.077 | -0.095 .. +0.249 | +3.5% | +0.225 | 0.41 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | -0.06 pts | -0.56 .. +0.43 | 0.8 |
| MES | 15 | -0.14 pts | -0.99 .. +0.71 | 0.75 |
| MES | 60 | -1.18 pts | -2.93 .. +0.57 | 0.18 |
| MNQ | 5 | +0.19 pts | -0.28 .. +0.66 | 0.43 |
| MNQ | 15 | +0.14 pts | -0.66 .. +0.94 | 0.73 |
| MNQ | 60 | -0.70 pts | -2.44 .. +1.04 | 0.43 |
| MYM | 5 | -0.48 pts | -1.11 .. +0.14 | 0.13 |
| MYM | 15 | -1.35 pts | -2.42 .. -0.29 | 0.017 |
| MYM | 60 | -3.00 pts | -5.30 .. -0.70 | 0.011 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | short | 209979 | -0.000 | 0.338 | -0.01 | -3.51 | -3.52 | -3.50 | -3.50 |
| MES | 5 | h2 | event | short | 209979 | -0.002 | 0.338 | -0.04 | -3.54 | -3.56 | -3.51 | -3.52 |
| MES | 5 | h4 | event | short | 209979 | -0.005 | 0.338 | -0.08 | -3.58 | -3.63 | -3.54 | -3.54 |
| MES | 5 | h8 | event | short | 209979 | -0.011 | 0.338 | -0.17 | -3.67 | -3.76 | -3.57 | -3.56 |
| MES | 5 | h16 | event | short | 209979 | -0.022 | 0.338 | -0.33 | -3.83 | -4.03 | -3.63 | -3.58 |
| MES | 5 | eod | event | short | 209979 | -0.302 | 0.338 | -1.68 | -5.18 | -9.07 | -1.31 | -3.58 |
| MES | 15 | h1 | event | short | 69468 | -0.002 | 0.197 | -0.06 | -3.56 | -3.59 | -3.52 | -3.52 |
| MES | 15 | h2 | event | short | 69468 | -0.005 | 0.197 | -0.12 | -3.62 | -3.69 | -3.55 | -3.54 |
| MES | 15 | h4 | event | short | 69468 | -0.011 | 0.197 | -0.25 | -3.75 | -3.90 | -3.60 | -3.59 |
| MES | 15 | h8 | event | short | 69468 | -0.023 | 0.197 | -0.46 | -3.96 | -4.29 | -3.63 | -3.67 |
| MES | 15 | h16 | event | short | 69468 | -0.049 | 0.197 | -0.90 | -4.40 | -5.05 | -3.75 | -3.89 |
| MES | 15 | eod | event | short | 69468 | -0.163 | 0.197 | -1.61 | -5.11 | -9.01 | -1.23 | -3.96 |
| MES | 60 | h1 | event | short | 17067 | -0.005 | 0.100 | -0.22 | -3.72 | -3.89 | -3.55 | -3.54 |
| MES | 60 | h2 | event | short | 17067 | -0.010 | 0.100 | -0.42 | -3.92 | -4.27 | -3.58 | -3.52 |
| MES | 60 | h4 | event | short | 17067 | -0.019 | 0.100 | -0.84 | -4.34 | -4.99 | -3.69 | -3.43 |
| MES | 60 | h8 | event | short | 17067 | -0.027 | 0.100 | -1.43 | -4.93 | -6.35 | -3.52 | -3.19 |
| MES | 60 | h16 | event | short | 17067 | -0.026 | 0.100 | -1.31 | -4.81 | -8.37 | -1.27 | -2.13 |
| MES | 60 | eod | event | short | 17067 | -0.037 | 0.100 | -1.37 | -4.87 | -8.84 | -0.92 | -1.71 |
| MNQ | 5 | h1 | event | long | 209599 | +0.004 | 0.136 | +0.04 | -1.96 | -1.97 | -1.96 | -1.98 |
| MNQ | 5 | h2 | event | long | 209599 | +0.009 | 0.136 | +0.08 | -1.92 | -1.93 | -1.91 | -1.93 |
| MNQ | 5 | h4 | event | long | 209599 | +0.019 | 0.136 | +0.17 | -1.83 | -1.86 | -1.80 | -1.84 |
| MNQ | 5 | h8 | event | long | 209599 | +0.036 | 0.136 | +0.34 | -1.66 | -1.71 | -1.61 | -1.72 |
| MNQ | 5 | h16 | event | short | 209599 | -0.061 | 0.136 | -0.67 | -2.67 | -2.58 | -2.76 | -2.47 |
| MNQ | 5 | eod | event | long | 209599 | +1.201 | 0.136 | +5.92 | +3.92 | +3.92 | +3.93 | +2.48 |
| MNQ | 15 | h1 | event | short | 69434 | -0.007 | 0.078 | -0.13 | -2.13 | -2.11 | -2.15 | -2.03 |
| MNQ | 15 | h2 | event | short | 69434 | -0.012 | 0.078 | -0.25 | -2.25 | -2.22 | -2.29 | -2.12 |
| MNQ | 15 | h4 | event | short | 69434 | -0.024 | 0.078 | -0.50 | -2.50 | -2.44 | -2.57 | -2.24 |
| MNQ | 15 | h8 | event | long | 69434 | +0.053 | 0.078 | +0.97 | -1.03 | -1.14 | -0.92 | -1.59 |
| MNQ | 15 | h16 | event | long | 69434 | +0.114 | 0.078 | +1.88 | -0.12 | -0.35 | +0.10 | -0.74 |
| MNQ | 15 | eod | event | long | 69434 | +0.596 | 0.078 | +5.89 | +3.89 | +3.86 | +3.91 | +3.12 |
| MNQ | 60 | h1 | event | long | 17067 | +0.014 | 0.039 | +0.48 | -1.52 | -1.58 | -1.47 | -1.83 |
| MNQ | 60 | h2 | event | long | 17067 | +0.028 | 0.039 | +0.92 | -1.08 | -1.17 | -0.98 | -1.70 |
| MNQ | 60 | h4 | event | long | 17067 | +0.054 | 0.039 | +1.82 | -0.18 | -0.42 | +0.06 | -1.48 |
| MNQ | 60 | h8 | event | long | 17067 | +0.097 | 0.039 | +3.32 | +1.32 | +0.93 | +1.71 | -1.17 |
| MNQ | 60 | h16 | event | long | 17067 | +0.156 | 0.039 | +4.56 | +2.56 | +3.08 | +2.03 | -1.40 |
| MNQ | 60 | eod | event | long | 17067 | +0.191 | 0.039 | +5.56 | +3.56 | +3.66 | +3.46 | -1.28 |
| MYM | 5 | h1 | event | short | 104998 | +0.005 | 0.175 | +0.02 | -1.98 | +nan | -1.98 | -1.98 |
| MYM | 5 | h2 | event | short | 104998 | +0.010 | 0.175 | +0.03 | -1.97 | +nan | -1.97 | -1.99 |
| MYM | 5 | h4 | event | short | 104998 | +0.019 | 0.175 | +0.05 | -1.95 | +nan | -1.95 | -2.01 |
| MYM | 5 | h8 | event | short | 104998 | +0.038 | 0.175 | +0.11 | -1.89 | +nan | -1.89 | -1.98 |
| MYM | 5 | h16 | event | short | 104998 | +0.077 | 0.175 | +0.25 | -1.75 | +nan | -1.75 | -1.83 |
| MYM | 5 | eod | event | short | 104998 | +1.302 | 0.175 | +6.20 | +4.20 | +nan | +4.20 | +4.58 |
| MYM | 15 | h1 | event | short | 34745 | +0.008 | 0.100 | +0.05 | -1.95 | +nan | -1.95 | -1.94 |
| MYM | 15 | h2 | event | short | 34745 | +0.016 | 0.100 | +0.09 | -1.91 | +nan | -1.91 | -1.94 |
| MYM | 15 | h4 | event | short | 34745 | +0.032 | 0.100 | +0.18 | -1.82 | +nan | -1.82 | -1.88 |
| MYM | 15 | h8 | event | short | 34745 | +0.067 | 0.100 | +0.44 | -1.56 | +nan | -1.56 | -1.72 |
| MYM | 15 | h16 | event | short | 34745 | +0.150 | 0.100 | +0.96 | -1.04 | +nan | -1.04 | -1.56 |
| MYM | 15 | eod | event | short | 34745 | +0.690 | 0.100 | +6.28 | +4.28 | +nan | +4.28 | +3.45 |
| MYM | 60 | h1 | event | short | 8520 | +0.019 | 0.050 | +0.24 | -1.76 | +nan | -1.76 | -1.68 |
| MYM | 60 | h2 | event | short | 8520 | +0.038 | 0.050 | +0.51 | -1.49 | +nan | -1.49 | -1.35 |
| MYM | 60 | h4 | event | short | 8520 | +0.076 | 0.050 | +1.04 | -0.96 | +nan | -0.96 | -0.70 |
| MYM | 60 | h8 | event | short | 8520 | +0.156 | 0.050 | +2.39 | +0.39 | +nan | +0.39 | +1.04 |
| MYM | 60 | h16 | event | short | 8520 | +0.305 | 0.050 | +6.04 | +4.04 | +nan | +4.04 | +5.21 |
| MYM | 60 | eod | event | short | 8520 | +0.315 | 0.050 | +6.47 | +4.47 | +nan | +4.47 | +6.07 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.004 | -0.000 | +0.001 | +0.001 | +0.001 | +0.000 | -0.001 | -0.003 | -0.006 | -0.013 | -0.027 |
| MES | 15 | +0.012 | +0.007 | +0.004 | +0.002 | +0.001 | +0.000 | -0.001 | -0.003 | -0.008 | -0.015 | -0.026 |
| MES | 60 | +0.023 | +0.021 | +0.010 | +0.005 | +0.003 | +0.000 | -0.004 | -0.009 | -0.021 | -0.056 | -0.127 |
| MNQ | 5 | -0.011 | -0.003 | -0.002 | -0.002 | -0.001 | +0.000 | +0.002 | +0.003 | +0.006 | +0.005 | -0.007 |
| MNQ | 15 | +0.002 | +0.002 | +0.000 | -0.001 | -0.001 | +0.000 | +0.002 | +0.002 | -0.001 | -0.001 | +0.018 |
| MNQ | 60 | +0.005 | +0.005 | -0.001 | -0.001 | -0.001 | +0.000 | +0.004 | +0.005 | +0.008 | +0.002 | -0.017 |
| MYM | 5 | +0.006 | +0.005 | +0.005 | +0.004 | +0.002 | +0.000 | -0.002 | -0.005 | -0.011 | -0.027 | -0.069 |
| MYM | 15 | +0.045 | +0.026 | +0.016 | +0.009 | +0.004 | +0.000 | -0.005 | -0.011 | -0.027 | -0.057 | -0.131 |
| MYM | 60 | +0.261 | +0.161 | +0.080 | +0.040 | +0.020 | +0.000 | -0.022 | -0.046 | -0.095 | -0.223 | -0.440 |

## Calibration

- MES 5-min: 1036271 bars, 209979 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 69468 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 95% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 17067 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 209599 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 69434 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 17067 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 55% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 104998 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 75% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 34745 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 35% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 8520 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 30% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
