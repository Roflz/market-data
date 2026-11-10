# Impact card: pat_nr7

candle pattern nr7 (no direction): range smaller than each of the previous 6 ranges [controls: 15-min slot, weekday, volatility decile, EMA trend state, last-bar sign, year]

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 5-min: no measurable direction effect (best +0.016 R20 over the next 16 bars (80 min), p=0.58; we would catch an effect of 0.014 R20 or more 80% of the time).
- MES 5-min size: the market moves 4% LESS after the event than after matched bars over the next 8 bars (40 min) (-0.050 R20, CONFIRMED, q=2.01e-10, 12 of 16 years same sign).
- MES 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.28 at recent bar sizes, 90% range up to $0.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MES 15-min: POSSIBLE direction effect +0.022 average bars (~$0.66 per micro at 2018-25 bar sizes) over the next 2 bars (30 min) (after the event vs matched non-events), not confirmed (q=0.0139, replicated in the other half=False, 12 of 16 years); best leg (event, long) grosses $+0.61 and nets $-2.89 per micro per trade after $3.50 costs -> not tradable on its own.
- MES 15-min size: the market moves 6% LESS after the event than after matched bars over the next 2 bars (30 min) (-0.046 R20, CONFIRMED, q=6.71e-17, 14 of 16 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.60 at recent bar sizes, 90% range up to $1.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MES 60-min: no measurable direction effect (best -0.010 R20 over the next 1 bar (1 h), p=1; we would catch an effect of 0.077 R20 or more 80% of the time).
- MES 60-min size: the market moves 13% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.067 R20, CONFIRMED, q=4.03e-07, 16 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.56 at recent bar sizes, 90% range up to $3.93); about 1.3x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).
- MNQ 5-min: no measurable direction effect (best +0.013 R20 over the next 4 bars (20 min), p=0.15; we would catch an effect of 0.017 R20 or more 80% of the time).
- MNQ 5-min size: the market moves 5% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.029 R20, CONFIRMED, q=5.01e-46, 16 of 16 years same sign).
- MNQ 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.32 at recent bar sizes, 90% range up to $0.81); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MNQ 15-min: no measurable direction effect (best +0.129 R20 over the rest of the session (to 16:45), p=0.93; we would catch an effect of 0.027 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 7% LESS after the event than after matched bars over the next 2 bars (30 min) (-0.055 R20, CONFIRMED, q=4.61e-13, 16 of 16 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $5.54 at recent bar sizes, 90% range up to $1.77); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MNQ 60-min: no measurable direction effect (best -0.023 R20 over the next 2 bars (2 h), p=1; we would catch an effect of 0.075 R20 or more 80% of the time).
- MNQ 60-min size: the market moves 9% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.048 R20, CONFIRMED, q=0.00139, 15 of 16 years same sign).
- MNQ 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.01 at recent bar sizes, 90% range up to $6.06); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:25; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.047 R20 for ~1 event/session).
- MYM 5-min: no measurable direction effect (best +0.019 R20 over the next 2 bars (10 min), p=0.018; we would catch an effect of 0.023 R20 or more 80% of the time).
- MYM 5-min size: the market moves 6% LESS after the event than after matched bars over the next 1 bar (5 min) (-0.033 R20, CONFIRMED, q=9.25e-28, 8 of 8 years same sign).
- MYM 5-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.22 at recent bar sizes, 90% range up to $0.78); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: UNCALIBRATED (run v3/signal_lab/calibrate_lab.py).
- MYM 15-min: no measurable direction effect (best +0.014 R20 over the next 1 bar (15 min), p=0.045; we would catch an effect of 0.040 R20 or more 80% of the time).
- MYM 15-min size: the market moves 7% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.037 R20, CONFIRMED, q=4.15e-08, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.27 at recent bar sizes, 90% range up to $2.10); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).
- MYM 60-min: no measurable direction effect (best -0.038 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.100 R20 or more 80% of the time).
- MYM 60-min size: the market moves 10% LESS after the event than after matched bars over the next 1 bar (1 h) (-0.051 R20, CONFIRMED, q=0.0152, 8 of 8 years same sign).
- MYM 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $1.52 at recent bar sizes, 90% range up to $3.89); about 5.5x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:19; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.066 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | +0.001 | -0.003 .. +0.006 | +0.0005 | 0.55 / 0.57 / 0.66 | 0.657 |  |  | 10/16 | -0.001 | +0.004 |  | +0.6 / +0.6 |  |
| MES | 5 | h2 | +0.004 | -0.003 .. +0.010 | +0.0011 | 0.25 / 0.23 / 0.28 | 0.275 |  |  | 8/16 | -0.000 | +0.008 |  | +1.2 / +1.1 |  |
| MES | 5 | h4 | +0.003 | -0.006 .. +0.012 | +0.0006 | 0.47 / 0.47 / 0.47 | 0.46 |  |  | 10/16 | -0.004 | +0.011 |  | +0.7 / +0.7 | 0.014 |
| MES | 5 | h8 | +0.011 | -0.003 .. +0.025 | +0.0014 | 0.13 / 0.11 / 0.079 | 0.0771 |  |  | 8/16 | +0.002 | +0.020 |  | +1.7 / +1.5 |  |
| MES | 5 | h16 * | +0.016 | -0.003 .. +0.035 | +0.0015 | 0.097 / 0.096 / 0.067 | 0.0677 | 1 | 1 | 10/16 | +0.003 | +0.030 | False | +1.7 / +1.7 |  |
| MES | 5 | eod | +0.121 | -0.057 .. +0.298 | +0.0022 | 0.18 / 0.18 / 0.037 | 0.0339 |  |  | 8/16 | +0.008 | +0.233 |  | +2.5 / +1.3 |  |
| MES | 15 | h1 | +0.015 | +0.007 .. +0.022 | +0.0060 | 9.1e-05 / 5.1e-05 / 9.6e-05 | 0.00026 |  |  | 13/16 | +0.012 | +0.018 |  | +4.1 / +3.9 |  |
| MES | 15 | h2 * | +0.022 | +0.011 .. +0.032 | +0.0058 | 4.8e-05 / 3.5e-05 / 0.00011 | 0.00026 | 0.0139 | 0.021 | 12/16 | +0.021 | +0.022 | False | +4.2 / +4.1 |  |
| MES | 15 | h4 | +0.024 | +0.009 .. +0.040 | +0.0044 | 0.0018 / 0.0023 / 0.0028 | 0.00339 |  |  | 11/16 | +0.016 | +0.032 |  | +3.2 / +3.1 | 0.024 |
| MES | 15 | h8 | +0.036 | +0.014 .. +0.058 | +0.0046 | 0.0015 / 0.0022 / 0.0012 | 0.0013 |  |  | 12/16 | +0.027 | +0.045 |  | +3.2 / +3.2 |  |
| MES | 15 | h16 | +0.060 | +0.023 .. +0.097 | +0.0054 | 0.0014 / 0.0013 / 0.00018 | 0.00026 |  |  | 14/16 | +0.041 | +0.079 |  | +3.4 / +3.2 |  |
| MES | 15 | eod | +0.133 | +0.001 .. +0.265 | +0.0046 | 0.048 / 0.047 / 0.00079 | 0.0013 |  |  | 9/16 | +0.039 | +0.227 |  | +3.0 / +2.0 |  |
| MES | 60 | h1 * | -0.010 | -0.033 .. +0.013 | -0.0028 | 0.38 / 0.4 / 0.45 | 0.456 | 1 | 1 | 8/16 | -0.020 | -0.001 | False | -0.9 / -0.9 |  |
| MES | 60 | h2 | +0.011 | -0.022 .. +0.044 | +0.0021 | 0.52 / 0.54 / 0.59 | 0.592 |  |  | 10/16 | +0.016 | +0.005 |  | +0.6 / +0.6 |  |
| MES | 60 | h4 | +0.004 | -0.043 .. +0.051 | +0.0005 | 0.88 / 0.87 / 0.89 | 0.889 |  |  | 7/16 | +0.012 | -0.004 |  | +0.2 / +0.2 | 0.077 |
| MES | 60 | h8 | +0.013 | -0.047 .. +0.074 | +0.0013 | 0.67 / 0.66 / 0.69 | 0.695 |  |  | 9/16 | +0.023 | +0.004 |  | +0.4 / +0.4 |  |
| MES | 60 | h16 | +0.025 | -0.050 .. +0.099 | +0.0019 | 0.52 / 0.53 / 0.56 | 0.556 |  |  | 7/16 | +0.067 | -0.018 |  | +0.6 / +0.6 |  |
| MES | 60 | eod | +0.027 | -0.048 .. +0.103 | +0.0020 | 0.48 / 0.5 / 0.52 | 0.521 |  |  | 7/16 | +0.067 | -0.013 |  | +0.6 / +0.7 |  |
| MNQ | 5 | h1 | +0.004 | -0.000 .. +0.008 | +0.0014 | 0.066 / 0.065 / 0.13 | 0.139 |  |  | 10/16 | +0.001 | +0.007 |  | +1.8 / +1.8 |  |
| MNQ | 5 | h2 | +0.006 | -0.000 .. +0.013 | +0.0014 | 0.069 / 0.059 / 0.15 | 0.148 |  |  | 10/16 | +0.005 | +0.007 |  | +2.0 / +1.8 |  |
| MNQ | 5 | h4 * | +0.013 | +0.002 .. +0.024 | +0.0019 | 0.024 / 0.022 / 0.047 | 0.0466 | 1 | 0.996 | 10/16 | +0.011 | +0.015 | False | +2.8 / +2.3 | 0.017 |
| MNQ | 5 | h8 | +0.018 | -0.000 .. +0.037 | +0.0019 | 0.052 / 0.046 / 0.034 | 0.0352 |  |  | 10/16 | +0.019 | +0.017 |  | +2.7 / +1.9 |  |
| MNQ | 5 | h16 | +0.027 | -0.001 .. +0.055 | +0.0019 | 0.061 / 0.058 / 0.021 | 0.0216 |  |  | 10/16 | +0.021 | +0.033 |  | +2.6 / +1.9 |  |
| MNQ | 5 | eod | +0.068 | -0.196 .. +0.332 | +0.0010 | 0.61 / 0.61 / 0.3 | 0.306 |  |  | 10/16 | -0.121 | +0.256 |  | +1.3 / +0.5 |  |
| MNQ | 15 | h1 | +0.006 | -0.000 .. +0.013 | +0.0021 | 0.057 / 0.074 / 0.16 | 0.142 |  |  | 11/16 | +0.005 | +0.008 |  | +1.7 / +1.9 |  |
| MNQ | 15 | h2 | +0.010 | +0.001 .. +0.020 | +0.0021 | 0.037 / 0.042 / 0.15 | 0.133 |  |  | 14/16 | +0.009 | +0.012 |  | +1.9 / +2.1 |  |
| MNQ | 15 | h4 | +0.014 | -0.002 .. +0.030 | +0.0017 | 0.085 / 0.095 / 0.24 | 0.223 |  |  | 12/16 | +0.012 | +0.017 |  | +1.7 / +1.7 | 0.027 |
| MNQ | 15 | h8 | +0.018 | -0.006 .. +0.043 | +0.0017 | 0.15 / 0.17 / 0.28 | 0.272 |  |  | 13/16 | +0.021 | +0.016 |  | +1.5 / +1.4 |  |
| MNQ | 15 | h16 | +0.027 | -0.018 .. +0.071 | +0.0020 | 0.24 / 0.26 / 0.16 | 0.157 |  |  | 9/16 | +0.008 | +0.045 |  | +1.4 / +1.2 |  |
| MNQ | 15 | eod * | +0.129 | -0.049 .. +0.308 | +0.0034 | 0.16 / 0.15 / 0.018 | 0.0195 | 1 | 0.999 | 12/16 | +0.022 | +0.236 | False | +2.6 / +1.4 |  |
| MNQ | 60 | h1 | -0.010 | -0.032 .. +0.013 | -0.0027 | 0.4 / 0.41 / 0.45 | 0.459 |  |  | 9/16 | -0.026 | +0.007 |  | -0.8 / -0.8 |  |
| MNQ | 60 | h2 * | -0.023 | -0.059 .. +0.012 | -0.0045 | 0.2 / 0.2 / 0.21 | 0.216 | 1 | 1 | 9/16 | -0.034 | -0.013 | False | -1.3 / -1.3 |  |
| MNQ | 60 | h4 | -0.018 | -0.069 .. +0.033 | -0.0025 | 0.49 / 0.47 / 0.47 | 0.478 |  |  | 10/16 | -0.050 | +0.013 |  | -0.7 / -0.7 | 0.075 |
| MNQ | 60 | h8 | -0.007 | -0.074 .. +0.061 | -0.0006 | 0.85 / 0.84 / 0.84 | 0.823 |  |  | 9/16 | -0.026 | +0.013 |  | -0.2 / -0.2 |  |
| MNQ | 60 | h16 | +0.014 | -0.065 .. +0.092 | +0.0010 | 0.73 / 0.74 / 0.74 | 0.734 |  |  | 7/16 | -0.023 | +0.050 |  | +0.3 / +0.3 |  |
| MNQ | 60 | eod | +0.013 | -0.067 .. +0.093 | +0.0009 | 0.75 / 0.76 / 0.76 | 0.747 |  |  | 7/16 | -0.030 | +0.056 |  | +0.3 / +0.3 |  |
| MYM | 5 | h1 | +0.008 | +0.002 .. +0.015 | +0.0030 | 0.0074 / 0.0061 / 0.019 | 0.0242 |  |  | 6/8 | n/a | +0.008 |  | +2.9 / +2.7 |  |
| MYM | 5 | h2 * | +0.019 | +0.007 .. +0.031 | +0.0041 | 0.0013 / 0.00061 / 0.0036 | 0.00527 | 0.457 | 0.31 | 7/8 | n/a | +0.019 | False | +4.3 / +3.2 |  |
| MYM | 5 | h4 | +0.028 | +0.008 .. +0.048 | +0.0037 | 0.0073 / 0.0084 / 0.0028 | 0.00474 |  |  | 8/8 | n/a | +0.028 |  | +4.2 / +2.7 | 0.023 |
| MYM | 5 | h8 | +0.048 | +0.014 .. +0.083 | +0.0046 | 0.0065 / 0.0076 / 0.00036 | 0.000527 |  |  | 8/8 | n/a | +0.048 |  | +5.0 / +2.7 |  |
| MYM | 5 | h16 | +0.052 | +0.002 .. +0.101 | +0.0039 | 0.04 / 0.04 / 0.0014 | 0.00105 |  |  | 6/8 | n/a | +0.052 |  | +3.8 / +2.1 |  |
| MYM | 5 | eod | +0.200 | -0.092 .. +0.493 | +0.0033 | 0.18 / 0.17 / 0.0033 | 0.0058 |  |  | 6/8 | n/a | +0.200 |  | +2.8 / +1.3 |  |
| MYM | 15 | h1 * | +0.014 | +0.005 .. +0.023 | +0.0050 | 0.0034 / 0.0043 / 0.013 | 0.0126 | 1 | 0.55 | 7/8 | n/a | +0.014 | False | +2.8 / +2.9 |  |
| MYM | 15 | h2 | +0.018 | +0.004 .. +0.033 | +0.0038 | 0.014 / 0.017 / 0.049 | 0.059 |  |  | 5/8 | n/a | +0.018 |  | +2.4 / +2.4 |  |
| MYM | 15 | h4 | +0.018 | -0.011 .. +0.047 | +0.0022 | 0.22 / 0.22 / 0.29 | 0.274 |  |  | 3/8 | n/a | +0.018 |  | +1.5 / +1.2 | 0.040 |
| MYM | 15 | h8 | +0.063 | +0.015 .. +0.111 | +0.0060 | 0.01 / 0.01 / 0.018 | 0.0163 |  |  | 6/8 | n/a | +0.063 |  | +3.7 / +2.6 |  |
| MYM | 15 | h16 | +0.095 | -0.007 .. +0.198 | +0.0065 | 0.067 / 0.063 / 0.00097 | 0.00158 |  |  | 6/8 | n/a | +0.095 |  | +3.6 / +1.8 |  |
| MYM | 15 | eod | +0.185 | -0.073 .. +0.442 | +0.0052 | 0.16 / 0.16 / 0.0059 | 0.00896 |  |  | 6/8 | n/a | +0.185 |  | +2.8 / +1.4 |  |
| MYM | 60 | h1 | +0.003 | -0.031 .. +0.037 | +0.0008 | 0.87 / 0.88 / 0.88 | 0.895 |  |  | 4/8 | n/a | +0.003 |  | +0.2 / +0.2 |  |
| MYM | 60 | h2 | -0.013 | -0.060 .. +0.033 | -0.0028 | 0.57 / 0.56 / 0.6 | 0.608 |  |  | 5/8 | n/a | -0.013 |  | -0.6 / -0.6 |  |
| MYM | 60 | h4 | -0.002 | -0.064 .. +0.061 | -0.0002 | 0.96 / 0.96 / 0.96 | 0.959 |  |  | 5/8 | n/a | -0.002 |  | -0.0 / -0.1 | 0.100 |
| MYM | 60 | h8 | -0.014 | -0.101 .. +0.072 | -0.0016 | 0.74 / 0.74 / 0.73 | 0.733 |  |  | 5/8 | n/a | -0.014 |  | -0.3 / -0.3 |  |
| MYM | 60 | h16 | -0.036 | -0.142 .. +0.069 | -0.0030 | 0.5 / 0.49 / 0.48 | 0.483 |  |  | 4/8 | n/a | -0.036 |  | -0.6 / -0.7 |  |
| MYM | 60 | eod * | -0.038 | -0.145 .. +0.070 | -0.0030 | 0.49 / 0.48 / 0.47 | 0.465 | 1 | 1 | 4/8 | n/a | -0.038 | False | -0.6 / -0.7 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | -0.014 | -0.018 .. -0.010 | -2.8% | -0.049 | 9.4e-11 |  | 10/16 |
| MES | 5 | h2 | -0.021 | -0.027 .. -0.015 | -3.0% | -0.060 | 7.9e-12 |  | 10/16 |
| MES | 5 | h4 | -0.032 | -0.041 .. -0.024 | -3.2% | -0.078 | 7.7e-12 |  | 12/16 |
| MES | 5 | h8 * | -0.050 | -0.064 .. -0.037 | -3.5% | -0.108 | 5.4e-13 | 2.01e-10 | 12/16 |
| MES | 5 | h16 | -0.063 | -0.083 .. -0.044 | -3.0% | -0.146 | 2.6e-10 |  | 12/16 |
| MES | 5 | eod | -0.337 | -0.504 .. -0.169 | -3.4% | -0.746 | 8e-05 |  | 10/16 |
| MES | 15 | h1 | -0.027 | -0.032 .. -0.021 | -5.2% | -0.070 | 4.2e-14 |  | 14/16 |
| MES | 15 | h2 * | -0.046 | -0.055 .. -0.038 | -6.4% | -0.096 | 1.3e-19 | 6.71e-17 | 14/16 |
| MES | 15 | h4 | -0.061 | -0.075 .. -0.048 | -5.8% | -0.127 | 1.2e-15 |  | 16/16 |
| MES | 15 | h8 | -0.078 | -0.097 .. -0.060 | -5.1% | -0.169 | 5.9e-17 |  | 16/16 |
| MES | 15 | h16 | -0.100 | -0.129 .. -0.071 | -4.4% | -0.239 | 8.3e-12 |  | 15/16 |
| MES | 15 | eod | -0.223 | -0.340 .. -0.105 | -4.1% | -0.476 | 0.0002 |  | 16/16 |
| MES | 60 | h1 * | -0.067 | -0.083 .. -0.051 | -13.0% | -0.127 | 1.3e-09 | 4.03e-07 | 16/16 |
| MES | 60 | h2 | -0.083 | -0.106 .. -0.059 | -11.2% | -0.170 | 3.5e-09 |  | 15/16 |
| MES | 60 | h4 | -0.090 | -0.123 .. -0.056 | -8.5% | -0.198 | 3.1e-05 |  | 15/16 |
| MES | 60 | h8 | -0.094 | -0.136 .. -0.052 | -6.2% | -0.229 | 0.00038 |  | 13/16 |
| MES | 60 | h16 | -0.086 | -0.138 .. -0.033 | -4.2% | -0.208 | 0.0035 |  | 13/16 |
| MES | 60 | eod | -0.085 | -0.139 .. -0.031 | -3.9% | -0.205 | 0.0033 |  | 12/16 |
| MNQ | 5 | h1 * | -0.029 | -0.032 .. -0.026 | -5.4% | -0.064 | 4.8e-49 | 5.01e-46 | 16/16 |
| MNQ | 5 | h2 | -0.044 | -0.051 .. -0.038 | -5.8% | -0.090 | 8.4e-35 |  | 16/16 |
| MNQ | 5 | h4 | -0.066 | -0.078 .. -0.054 | -6.0% | -0.129 | 1.8e-27 |  | 16/16 |
| MNQ | 5 | h8 | -0.092 | -0.115 .. -0.068 | -5.7% | -0.183 | 3.5e-14 |  | 16/16 |
| MNQ | 5 | h16 | -0.129 | -0.171 .. -0.086 | -5.4% | -0.272 | 2.8e-09 |  | 16/16 |
| MNQ | 5 | eod | -0.676 | -0.950 .. -0.402 | -5.4% | -1.486 | 1.3e-06 |  | 15/16 |
| MNQ | 15 | h1 | -0.032 | -0.037 .. -0.027 | -6.0% | -0.078 | 3.5e-13 |  | 16/16 |
| MNQ | 15 | h2 * | -0.055 | -0.067 .. -0.044 | -7.1% | -0.109 | 1.1e-15 | 4.61e-13 | 16/16 |
| MNQ | 15 | h4 | -0.080 | -0.107 .. -0.052 | -7.0% | -0.152 | 1.1e-08 |  | 16/16 |
| MNQ | 15 | h8 | -0.100 | -0.141 .. -0.059 | -6.0% | -0.219 | 2e-06 |  | 16/16 |
| MNQ | 15 | h16 | -0.122 | -0.169 .. -0.074 | -4.8% | -0.331 | 4.7e-07 |  | 14/16 |
| MNQ | 15 | eod | -0.300 | -0.499 .. -0.101 | -4.7% | -0.604 | 0.0031 |  | 14/16 |
| MNQ | 60 | h1 * | -0.048 | -0.064 .. -0.031 | -9.0% | -0.101 | 5.9e-06 | 0.00139 | 15/16 |
| MNQ | 60 | h2 | -0.057 | -0.083 .. -0.031 | -7.4% | -0.132 | 1.8e-05 |  | 14/16 |
| MNQ | 60 | h4 | -0.077 | -0.111 .. -0.042 | -6.9% | -0.159 | 6e-05 |  | 14/16 |
| MNQ | 60 | h8 | -0.083 | -0.128 .. -0.038 | -5.2% | -0.180 | 0.002 |  | 13/16 |
| MNQ | 60 | h16 | -0.093 | -0.151 .. -0.035 | -4.2% | -0.171 | 0.0026 |  | 13/16 |
| MNQ | 60 | eod | -0.093 | -0.151 .. -0.035 | -4.0% | -0.167 | 0.0025 |  | 11/16 |
| MYM | 5 | h1 * | -0.033 | -0.038 .. -0.028 | -6.2% | -0.068 | 1.3e-30 | 9.25e-28 | 8/8 |
| MYM | 5 | h2 | -0.049 | -0.058 .. -0.039 | -6.4% | -0.093 | 2.4e-13 |  | 8/8 |
| MYM | 5 | h4 | -0.074 | -0.094 .. -0.055 | -6.8% | -0.140 | 7.6e-13 |  | 8/8 |
| MYM | 5 | h8 | -0.112 | -0.149 .. -0.074 | -7.0% | -0.209 | 6.8e-09 |  | 8/8 |
| MYM | 5 | h16 | -0.145 | -0.197 .. -0.092 | -6.2% | -0.308 | 6.5e-08 |  | 8/8 |
| MYM | 5 | eod | -0.682 | -0.939 .. -0.425 | -5.8% | -1.252 | 2.2e-07 |  | 8/8 |
| MYM | 15 | h1 * | -0.037 | -0.044 .. -0.030 | -6.9% | -0.081 | 1.3e-10 | 4.15e-08 | 8/8 |
| MYM | 15 | h2 | -0.058 | -0.073 .. -0.043 | -7.6% | -0.113 | 1.5e-08 |  | 8/8 |
| MYM | 15 | h4 | -0.073 | -0.105 .. -0.040 | -6.5% | -0.149 | 3.9e-05 |  | 8/8 |
| MYM | 15 | h8 | -0.117 | -0.165 .. -0.069 | -7.1% | -0.255 | 4.7e-06 |  | 8/8 |
| MYM | 15 | h16 | -0.146 | -0.235 .. -0.057 | -5.9% | -0.349 | 0.0017 |  | 8/8 |
| MYM | 15 | eod | -0.367 | -0.599 .. -0.135 | -6.1% | -0.612 | 0.0026 |  | 8/8 |
| MYM | 60 | h1 * | -0.051 | -0.075 .. -0.027 | -9.7% | -0.099 | 7.3e-05 | 0.0152 | 8/8 |
| MYM | 60 | h2 | -0.071 | -0.103 .. -0.039 | -9.3% | -0.140 | 0.00011 |  | 7/8 |
| MYM | 60 | h4 | -0.083 | -0.123 .. -0.044 | -7.7% | -0.175 | 0.00076 |  | 8/8 |
| MYM | 60 | h8 | -0.103 | -0.158 .. -0.048 | -6.7% | -0.209 | 0.0041 |  | 7/8 |
| MYM | 60 | h16 | -0.122 | -0.188 .. -0.055 | -5.7% | -0.199 | 0.00043 |  | 8/8 |
| MYM | 60 | eod | -0.119 | -0.185 .. -0.053 | -5.4% | -0.194 | 0.00058 |  | 8/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 5 | +0.05 pts | -0.25 .. +0.36 | 0.94 |
| MES | 15 | +0.64 pts | +0.02 .. +1.26 | 0.042 |
| MES | 60 | +0.28 pts | -1.22 .. +1.78 | 0.72 |
| MNQ | 5 | +0.23 pts | -0.05 .. +0.50 | 0.11 |
| MNQ | 15 | +0.68 pts | +0.19 .. +1.17 | 0.011 |
| MNQ | 60 | -0.40 pts | -1.81 .. +1.02 | 0.63 |
| MYM | 5 | +0.63 pts | +0.25 .. +1.01 | 0.0045 |
| MYM | 15 | +0.70 pts | +0.03 .. +1.38 | 0.043 |
| MYM | 60 | -0.53 pts | -2.32 .. +1.25 | 0.56 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | h1 | event | long | 92386 | +0.003 | 0.243 | +0.06 | -3.44 | -3.46 | -3.42 | -3.45 |
| MES | 5 | h2 | event | long | 92386 | +0.008 | 0.243 | +0.08 | -3.42 | -3.42 | -3.42 | -3.45 |
| MES | 5 | h4 | event | long | 92386 | +0.011 | 0.243 | +0.09 | -3.41 | -3.41 | -3.41 | -3.45 |
| MES | 5 | h8 | event | long | 92386 | +0.026 | 0.243 | +0.22 | -3.28 | -3.27 | -3.29 | -3.37 |
| MES | 5 | h16 | event | long | 92386 | +0.047 | 0.243 | +0.57 | -2.93 | -3.05 | -2.86 | -3.13 |
| MES | 5 | eod | event | long | 92386 | +0.421 | 0.243 | +4.77 | +1.27 | -0.43 | +2.35 | +1.97 |
| MES | 15 | h1 | event | long | 34070 | +0.017 | 0.155 | +0.39 | -3.11 | -3.30 | -2.97 | -3.17 |
| MES | 15 | h2 | event | long | 34070 | +0.028 | 0.155 | +0.61 | -2.89 | -3.12 | -2.72 | -2.99 |
| MES | 15 | h4 | event | long | 34070 | +0.040 | 0.155 | +0.84 | -2.66 | -3.09 | -2.35 | -2.85 |
| MES | 15 | h8 | event | long | 34070 | +0.067 | 0.155 | +1.42 | -2.08 | -2.81 | -1.56 | -2.41 |
| MES | 15 | h16 | event | long | 34070 | +0.112 | 0.155 | +2.52 | -0.98 | -2.11 | -0.18 | -1.41 |
| MES | 15 | eod | event | long | 34070 | +0.293 | 0.155 | +5.69 | +2.19 | -0.26 | +3.93 | +2.38 |
| MES | 60 | h1 | event | short | 3621 | +0.001 | 0.085 | +0.05 | -3.45 | -3.36 | -3.51 | -3.22 |
| MES | 60 | h2 | event | long | 3621 | +0.028 | 0.085 | +0.75 | -2.75 | -2.61 | -2.86 | -3.20 |
| MES | 60 | h4 | event | long | 3621 | +0.035 | 0.085 | +0.59 | -2.91 | -2.40 | -3.30 | -3.70 |
| MES | 60 | h8 | event | long | 3621 | +0.064 | 0.085 | +1.64 | -1.86 | -1.58 | -2.08 | -3.22 |
| MES | 60 | h16 | event | long | 3621 | +0.124 | 0.085 | +3.40 | -0.10 | +0.54 | -0.61 | -2.96 |
| MES | 60 | eod | event | long | 3621 | +0.124 | 0.085 | +3.40 | -0.10 | +0.54 | -0.61 | -2.78 |
| MNQ | 5 | h1 | event | long | 123889 | +0.007 | 0.103 | +0.05 | -1.95 | -1.96 | -1.94 | -1.98 |
| MNQ | 5 | h2 | event | long | 123889 | +0.011 | 0.103 | +0.00 | -2.00 | -1.92 | -2.05 | -2.00 |
| MNQ | 5 | h4 | event | long | 123889 | +0.021 | 0.103 | +0.08 | -1.92 | -1.84 | -1.98 | -1.93 |
| MNQ | 5 | h8 | event | long | 123889 | +0.036 | 0.103 | +0.24 | -1.76 | -1.74 | -1.77 | -1.81 |
| MNQ | 5 | h16 | event | long | 123889 | +0.068 | 0.103 | +0.85 | -1.15 | -1.55 | -0.88 | -1.35 |
| MNQ | 5 | eod | event | long | 123889 | +0.588 | 0.103 | +6.33 | +4.33 | +1.02 | +6.60 | +6.01 |
| MNQ | 15 | h1 | event | long | 41752 | +0.013 | 0.063 | +0.41 | -1.59 | -1.89 | -1.36 | -1.74 |
| MNQ | 15 | h2 | event | long | 41752 | +0.021 | 0.063 | +0.58 | -1.42 | -1.81 | -1.12 | -1.60 |
| MNQ | 15 | h4 | event | long | 41752 | +0.033 | 0.063 | +0.99 | -1.01 | -1.71 | -0.47 | -1.28 |
| MNQ | 15 | h8 | event | long | 41752 | +0.058 | 0.063 | +1.33 | -0.67 | -1.50 | -0.02 | -1.21 |
| MNQ | 15 | h16 | event | long | 41752 | +0.094 | 0.063 | +2.50 | +0.50 | -0.91 | +1.60 | -0.05 |
| MNQ | 15 | eod | event | long | 41752 | +0.329 | 0.063 | +6.38 | +4.38 | +0.84 | +7.14 | +5.78 |
| MNQ | 60 | h1 | event | short | 4044 | -0.005 | 0.034 | -0.15 | -2.15 | -1.97 | -2.28 | -1.65 |
| MNQ | 60 | h2 | event | short | 4044 | -0.003 | 0.034 | +0.16 | -1.84 | -2.35 | -1.46 | -0.96 |
| MNQ | 60 | h4 | event | short | 4044 | -0.020 | 0.034 | -0.34 | -2.34 | -2.29 | -2.39 | -1.32 |
| MNQ | 60 | h8 | event | short | 4044 | -0.054 | 0.034 | -0.80 | -2.80 | -3.46 | -2.30 | -1.26 |
| MNQ | 60 | h16 | event | long | 4044 | +0.127 | 0.034 | +4.37 | +2.37 | +0.54 | +3.76 | -0.83 |
| MNQ | 60 | eod | event | long | 4044 | +0.127 | 0.034 | +4.37 | +2.37 | +0.54 | +3.76 | -0.45 |
| MYM | 5 | h1 | event | long | 66578 | +0.007 | 0.151 | +0.08 | -1.92 | +nan | -1.92 | -1.93 |
| MYM | 5 | h2 | event | long | 66578 | +0.014 | 0.151 | +0.16 | -1.84 | +nan | -1.84 | -1.83 |
| MYM | 5 | h4 | event | long | 66578 | +0.015 | 0.151 | +0.21 | -1.79 | +nan | -1.79 | -1.75 |
| MYM | 5 | h8 | event | long | 66578 | +0.024 | 0.151 | +0.31 | -1.69 | +nan | -1.69 | -1.60 |
| MYM | 5 | h16 | event | long | 66578 | +0.024 | 0.151 | +0.45 | -1.55 | +nan | -1.55 | -1.47 |
| MYM | 5 | eod | event | long | 66578 | +0.259 | 0.151 | +4.12 | +2.12 | +nan | +2.12 | +2.37 |
| MYM | 15 | h1 | event | long | 22279 | +0.014 | 0.089 | +0.43 | -1.57 | +nan | -1.57 | -1.61 |
| MYM | 15 | h2 | event | long | 22279 | +0.017 | 0.089 | +0.54 | -1.46 | +nan | -1.46 | -1.47 |
| MYM | 15 | h4 | event | long | 22279 | +0.011 | 0.089 | +0.54 | -1.46 | +nan | -1.46 | -1.35 |
| MYM | 15 | h8 | event | long | 22279 | +0.029 | 0.089 | +0.91 | -1.09 | +nan | -1.09 | -0.61 |
| MYM | 15 | h16 | event | long | 22279 | +0.036 | 0.089 | +1.45 | -0.55 | +nan | -0.55 | +0.26 |
| MYM | 15 | eod | event | long | 22279 | +0.115 | 0.089 | +3.66 | +1.66 | +nan | +1.66 | +3.58 |
| MYM | 60 | h1 | event | long | 2255 | +0.008 | 0.047 | -0.07 | -2.07 | +nan | -2.07 | -2.23 |
| MYM | 60 | h2 | event | short | 2255 | +0.008 | 0.047 | +0.55 | -1.45 | +nan | -1.45 | -1.35 |
| MYM | 60 | h4 | event | short | 2255 | -0.010 | 0.047 | -0.20 | -2.20 | +nan | -2.20 | -1.82 |
| MYM | 60 | h8 | event | short | 2255 | -0.006 | 0.047 | -0.53 | -2.53 | +nan | -2.53 | -1.82 |
| MYM | 60 | h16 | event | short | 2255 | -0.013 | 0.047 | -1.89 | -3.89 | +nan | -3.89 | -1.99 |
| MYM | 60 | eod | event | short | 2255 | -0.013 | 0.047 | -1.89 | -3.89 | +nan | -3.89 | -1.88 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 5 | -0.087 | -0.128 | -0.132 | -0.065 | -0.005 | +0.000 | +0.001 | +0.003 | +0.000 | +0.006 | +0.005 |
| MES | 15 | -0.104 | -0.156 | -0.183 | -0.091 | -0.006 | +0.000 | +0.014 | +0.019 | +0.020 | +0.024 | +0.038 |
| MES | 60 | -0.460 | -0.473 | -0.306 | -0.147 | -0.008 | +0.000 | -0.012 | +0.011 | -0.009 | +0.005 | -0.119 |
| MNQ | 5 | -0.075 | -0.114 | -0.125 | -0.065 | -0.004 | +0.000 | +0.004 | +0.005 | +0.009 | +0.010 | +0.011 |
| MNQ | 15 | -0.084 | -0.132 | -0.163 | -0.086 | -0.008 | +0.000 | +0.007 | +0.009 | +0.011 | +0.009 | +0.003 |
| MNQ | 60 | -0.415 | -0.423 | -0.265 | -0.140 | -0.005 | +0.000 | -0.010 | -0.027 | -0.023 | -0.001 | +0.115 |
| MYM | 5 | -0.069 | -0.108 | -0.111 | -0.052 | -0.003 | +0.000 | +0.009 | +0.016 | +0.019 | +0.035 | +0.035 |
| MYM | 15 | -0.100 | -0.138 | -0.161 | -0.084 | -0.007 | +0.000 | +0.013 | +0.015 | +0.010 | +0.043 | +0.052 |
| MYM | 60 | -0.282 | -0.364 | -0.240 | -0.127 | -0.010 | +0.000 | +0.002 | -0.014 | -0.007 | -0.020 | -0.128 |

## Calibration

- MES 5-min: 1036271 bars, 92386 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 15-min: 342218 bars, 34070 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MES 60-min: 83413 bars, 3621 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 25% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 5-min: 1034522 bars, 123889 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 342062 bars, 41752 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 80% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 60-min: 83411 bars, 4044 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 5-min: 519039 bars, 66578 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 22279 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 90% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 60-min: 41655 bars, 2255 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 31825 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
