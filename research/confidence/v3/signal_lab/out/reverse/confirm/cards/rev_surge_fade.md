# Impact card: rev_surge_fade

distance from EMA8, only on bars with volume >= 1.65x usual for the time of day

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.021 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.122 R20 or more 80% of the time).
- MES 15-min size: the market moves 23% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.125 R20, CONFIRMED, q=6.78e-16, 8 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.33 at recent bar sizes, 90% range up to $2.32); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best -0.088 R20 over the next 8 bars (2 h), p=1; we would catch an effect of 0.180 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 19% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.102 R20, CONFIRMED, q=4.54e-10, 7 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $2.13 at recent bar sizes, 90% range up to $5.43); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.053 R20 over the next 2 bars (30 min), p=0.25; we would catch an effect of 0.144 R20 or more 80% of the time).
- MYM 15-min size: the market moves 22% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (-0.119 R20, CONFIRMED, q=1.46e-14, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.81 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.084 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.021 | -0.011 .. +0.053 | +0.0156 | 0.2 / 0.18 / 0.19 | 0.184 | 1 | 0.99 | 5/8 | n/a | +0.021 | False | +1.3 / +1.3 |  |
| MES | 15 | h2 | +0.032 | -0.019 .. +0.083 | +0.0185 | 0.22 / 0.22 / 0.21 | 0.205 |  |  | 5/8 | n/a | +0.032 |  | +1.4 / +1.2 |  |
| MES | 15 | h4 | +0.044 | -0.044 .. +0.132 | +0.0220 | 0.33 / 0.33 / 0.32 | 0.336 |  |  | 5/8 | n/a | +0.044 |  | +1.4 / +1.0 | 0.122 |
| MES | 15 | h8 | -0.001 | -0.145 .. +0.143 | +0.0135 | 0.99 / 0.99 / 0.99 | 0.991 |  |  | 5/8 | n/a | -0.001 |  | -0.0 / -0.0 |  |
| MES | 15 | h16 | -0.050 | -0.238 .. +0.137 | +0.0109 | 0.6 / 0.6 / 0.63 | 0.633 |  |  | 4/8 | n/a | -0.050 |  | -0.8 / -0.5 |  |
| MES | 15 | eod | -0.157 | -0.711 .. +0.396 | +0.0118 | 0.58 / 0.58 / 0.59 | 0.595 |  |  | 6/8 | n/a | -0.157 |  | -1.0 / -0.6 |  |
| MNQ | 15 | h1 | +0.019 | -0.010 .. +0.048 | +0.0077 | 0.19 / 0.2 / 0.25 | 0.28 |  |  | 6/8 | n/a | +0.019 |  | +1.1 / +1.3 |  |
| MNQ | 15 | h2 | +0.007 | -0.043 .. +0.056 | +0.0014 | 0.8 / 0.8 / 0.82 | 0.802 |  |  | 5/8 | n/a | +0.007 |  | +0.3 / +0.3 |  |
| MNQ | 15 | h4 | -0.013 | -0.101 .. +0.075 | -0.0030 | 0.77 / 0.77 / 0.76 | 0.782 |  |  | 5/8 | n/a | -0.013 |  | -0.4 / -0.3 | 0.180 |
| MNQ | 15 | h8 * | -0.088 | -0.225 .. +0.049 | -0.0171 | 0.21 / 0.2 / 0.2 | 0.205 | 1 | 0.978 | 6/8 | n/a | -0.088 | False | -1.8 / -1.3 |  |
| MNQ | 15 | h16 | -0.102 | -0.312 .. +0.109 | -0.0070 | 0.34 / 0.34 / 0.37 | 0.379 |  |  | 6/8 | n/a | -0.102 |  | -1.5 / -0.9 |  |
| MNQ | 15 | eod | -0.054 | -0.630 .. +0.522 | +0.0108 | 0.85 / 0.86 / 0.85 | 0.868 |  |  | 5/8 | n/a | -0.054 |  | -0.3 / -0.2 |  |
| MYM | 15 | h1 | +0.024 | -0.007 .. +0.055 | +0.0147 | 0.12 / 0.12 / 0.13 | 0.135 |  |  | 4/8 | n/a | +0.024 |  | +1.5 / +1.5 |  |
| MYM | 15 | h2 * | +0.053 | +0.003 .. +0.102 | +0.0169 | 0.037 / 0.042 / 0.038 | 0.0353 | 1 | 0.557 | 7/8 | n/a | +0.053 | False | +2.3 / +2.1 |  |
| MYM | 15 | h4 | +0.034 | -0.049 .. +0.118 | +0.0163 | 0.42 / 0.43 / 0.4 | 0.405 |  |  | 6/8 | n/a | +0.034 |  | +1.1 / +0.8 | 0.144 |
| MYM | 15 | h8 | -0.035 | -0.173 .. +0.103 | +0.0093 | 0.62 / 0.62 / 0.61 | 0.617 |  |  | 4/8 | n/a | -0.035 |  | -0.8 / -0.5 |  |
| MYM | 15 | h16 | -0.105 | -0.292 .. +0.083 | +0.0030 | 0.27 / 0.29 / 0.32 | 0.319 |  |  | 5/8 | n/a | -0.105 |  | -1.6 / -1.1 |  |
| MYM | 15 | eod | +0.013 | -0.529 .. +0.555 | +0.0091 | 0.96 / 0.96 / 0.97 | 0.965 |  |  | 3/8 | n/a | +0.013 |  | +0.1 / +0.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.125 | -0.154 .. -0.097 | -23.0% | -0.257 | 3.2e-18 | 6.78e-16 | 8/8 |
| MES | 15 | h2 | -0.159 | -0.199 .. -0.119 | -20.7% | -0.339 | 9.4e-15 |  | 8/8 |
| MES | 15 | h4 | -0.221 | -0.281 .. -0.160 | -20.3% | -0.428 | 9.2e-13 |  | 8/8 |
| MES | 15 | h8 | -0.212 | -0.299 .. -0.125 | -13.5% | -0.478 | 3.7e-06 |  | 8/8 |
| MES | 15 | h16 | -0.191 | -0.334 .. -0.048 | -8.3% | -0.446 | 0.0094 |  | 7/8 |
| MES | 15 | eod | -0.272 | -0.634 .. +0.091 | -4.9% | -0.646 | 0.14 |  | 7/8 |
| MNQ | 15 | h1 * | -0.102 | -0.131 .. -0.073 | -19.3% | -0.224 | 4e-12 | 4.54e-10 | 7/8 |
| MNQ | 15 | h2 | -0.122 | -0.161 .. -0.083 | -16.3% | -0.281 | 9.7e-10 |  | 8/8 |
| MNQ | 15 | h4 | -0.157 | -0.220 .. -0.093 | -14.5% | -0.341 | 1.3e-06 |  | 8/8 |
| MNQ | 15 | h8 | -0.145 | -0.243 .. -0.047 | -9.2% | -0.387 | 0.0038 |  | 7/8 |
| MNQ | 15 | h16 | -0.159 | -0.312 .. -0.006 | -6.8% | -0.382 | 0.042 |  | 7/8 |
| MNQ | 15 | eod | -0.549 | -0.904 .. -0.194 | -9.4% | -0.853 | 0.0038 |  | 8/8 |
| MYM | 15 | h1 * | -0.119 | -0.147 .. -0.091 | -21.7% | -0.237 | 1e-16 | 1.46e-14 | 8/8 |
| MYM | 15 | h2 | -0.169 | -0.210 .. -0.129 | -22.0% | -0.327 | 2.9e-16 |  | 8/8 |
| MYM | 15 | h4 | -0.197 | -0.259 .. -0.135 | -17.9% | -0.406 | 6e-10 |  | 8/8 |
| MYM | 15 | h8 | -0.235 | -0.320 .. -0.150 | -14.7% | -0.479 | 3e-07 |  | 8/8 |
| MYM | 15 | h16 | -0.251 | -0.394 .. -0.107 | -10.6% | -0.526 | 0.00061 |  | 8/8 |
| MYM | 15 | eod | -0.378 | -0.770 .. +0.014 | -6.7% | -0.860 | 0.069 |  | 6/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.00 pts | -1.86 .. +1.86 | 1 |
| MNQ | 15 | +1.55 pts | -0.46 .. +3.57 | 0.16 |
| MYM | 15 | +0.47 pts | -1.35 .. +2.30 | 0.64 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | long | 6137 | -0.003 | 0.112 | +0.09 | -3.41 | +nan | -3.41 | -3.27 |
| MES | 15 | h2 | top fifth | long | 6137 | -0.002 | 0.112 | +0.45 | -3.05 | +nan | -3.05 | -3.05 |
| MES | 15 | h4 | bottom fifth | short | 6137 | +0.051 | 0.110 | +0.79 | -2.71 | +nan | -2.71 | -2.79 |
| MES | 15 | h8 | bottom fifth | long | 6137 | -0.046 | 0.110 | +0.16 | -3.34 | +nan | -3.34 | -2.98 |
| MES | 15 | h16 | bottom fifth | long | 6137 | -0.026 | 0.110 | +2.29 | -1.21 | +nan | -1.21 | -0.02 |
| MES | 15 | eod | bottom fifth | long | 6137 | -0.212 | 0.110 | +2.94 | -0.56 | +nan | -0.56 | +2.51 |
| MNQ | 15 | h1 | bottom fifth | short | 5723 | +0.024 | 0.040 | +0.49 | -1.51 | +nan | -1.51 | -1.35 |
| MNQ | 15 | h2 | bottom fifth | short | 5723 | +0.017 | 0.040 | -0.06 | -2.06 | +nan | -2.06 | -1.93 |
| MNQ | 15 | h4 | bottom fifth | long | 5723 | -0.005 | 0.040 | +0.38 | -1.62 | +nan | -1.62 | -1.84 |
| MNQ | 15 | h8 | bottom fifth | long | 5723 | +0.011 | 0.040 | +2.06 | +0.06 | +nan | +0.06 | +0.26 |
| MNQ | 15 | h16 | bottom fifth | long | 5723 | +0.005 | 0.040 | +4.31 | +2.31 | +nan | +2.31 | +3.89 |
| MNQ | 15 | eod | bottom fifth | long | 5723 | -0.205 | 0.040 | +2.33 | +0.33 | +nan | +0.33 | -0.62 |
| MYM | 15 | h1 | bottom fifth | short | 6264 | +0.028 | 0.083 | +0.44 | -1.56 | +nan | -1.56 | -1.51 |
| MYM | 15 | h2 | bottom fifth | short | 6264 | +0.061 | 0.083 | +1.10 | -0.90 | +nan | -0.90 | -0.89 |
| MYM | 15 | h4 | bottom fifth | short | 6264 | +0.068 | 0.083 | +1.03 | -0.97 | +nan | -0.97 | -1.07 |
| MYM | 15 | h8 | top fifth | short | 6264 | +0.070 | 0.084 | +0.87 | -1.13 | +nan | -1.13 | -0.96 |
| MYM | 15 | h16 | bottom fifth | long | 6264 | -0.018 | 0.083 | +1.50 | -0.50 | +nan | -0.50 | +0.07 |
| MYM | 15 | eod | top fifth | long | 6264 | +0.013 | 0.084 | +3.91 | +1.91 | +nan | +1.91 | +1.34 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -4.679 | -5.065 | -4.445 | -3.117 | -1.840 | +0.000 | +0.008 | +0.019 | +0.025 | -0.054 | -0.148 |
| MNQ | 15 | -4.752 | -5.210 | -4.571 | -3.226 | -1.917 | +0.000 | +0.019 | +0.012 | -0.007 | -0.113 | -0.137 |
| MYM | 15 | -4.658 | -5.079 | -4.454 | -3.152 | -1.865 | +0.000 | +0.020 | +0.049 | +0.034 | -0.046 | -0.147 |

## Calibration

- MES 15-min: 30682 bars, 6137 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 20% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 28612 bars, 5723 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 31317 bars, 6264 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 15% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
