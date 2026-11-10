# Impact card: rev_volsurge_size

log volume vs usual for the time of day; surge -> bigger move next hour

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.030 R20 over the next 4 bars (1 h), p=1; we would catch an effect of 0.061 R20 or more 80% of the time).
- MES 15-min size: the market moves 14% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.074 R20, CONFIRMED, q=8.03e-48, 8 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.41 at recent bar sizes, 90% range up to $1.69); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best -0.013 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.094 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 13% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.066 R20, CONFIRMED, q=3.22e-06, 8 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.28 at recent bar sizes, 90% range up to $2.65); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best -0.011 R20 over the next 1 bar (15 min), p=0.75; we would catch an effect of 0.071 R20 or more 80% of the time).
- MYM 15-min size: the market moves 13% MORE in the metric's top fifth than in its bottom fifth over the next 1 bar (15 min) (+0.070 R20, CONFIRMED, q=2.94e-11, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $1.81 per micro (at recent bar sizes), inside the $2.00 round trip (break-even 0.092 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.009 | -0.023 .. +0.005 | -0.0085 | 0.21 / 0.18 / 0.14 | 0.158 |  |  | 5/8 | n/a | -0.009 |  | -1.3 / -1.3 |  |
| MES | 15 | h2 | -0.014 | -0.034 .. +0.007 | -0.0057 | 0.18 / 0.2 / 0.23 | 0.218 |  |  | 7/8 | n/a | -0.014 |  | -1.2 / -1.3 |  |
| MES | 15 | h4 * | -0.030 | -0.071 .. +0.011 | -0.0062 | 0.16 / 0.18 / 0.2 | 0.206 | 1 | 0.981 | 6/8 | n/a | -0.030 | False | -1.6 / -1.4 | 0.061 |
| MES | 15 | h8 | -0.051 | -0.128 .. +0.026 | -0.0045 | 0.19 / 0.23 / 0.23 | 0.221 |  |  | 4/8 | n/a | -0.051 |  | -2.1 / -1.3 |  |
| MES | 15 | h16 | -0.074 | -0.264 .. +0.116 | -0.0000 | 0.45 / 0.46 / 0.38 | 0.376 |  |  | 5/8 | n/a | -0.074 |  | -2.3 / -0.8 |  |
| MES | 15 | eod | -0.324 | -1.385 .. +0.736 | +0.0074 | 0.55 / 0.55 / 0.4 | 0.394 |  |  | 5/8 | n/a | -0.324 |  | -3.4 / -0.6 |  |
| MNQ | 15 | h1 * | -0.013 | -0.033 .. +0.007 | -0.0069 | 0.21 / 0.22 / 0.14 | 0.149 | 1 | 0.982 | 4/8 | n/a | -0.013 | False | -1.1 / -1.3 |  |
| MNQ | 15 | h2 | -0.011 | -0.041 .. +0.020 | -0.0007 | 0.49 / 0.52 / 0.55 | 0.563 |  |  | 6/8 | n/a | -0.011 |  | -0.5 / -0.7 |  |
| MNQ | 15 | h4 | -0.023 | -0.091 .. +0.045 | -0.0014 | 0.51 / 0.55 / 0.55 | 0.553 |  |  | 5/8 | n/a | -0.023 |  | -0.6 / -0.7 | 0.094 |
| MNQ | 15 | h8 | -0.024 | -0.129 .. +0.081 | -0.0022 | 0.66 / 0.69 / 0.69 | 0.688 |  |  | 4/8 | n/a | -0.024 |  | -0.5 / -0.4 |  |
| MNQ | 15 | h16 | -0.007 | -0.273 .. +0.260 | +0.0084 | 0.96 / 0.96 / 0.94 | 0.943 |  |  | 5/8 | n/a | -0.007 |  | -0.1 / -0.0 |  |
| MNQ | 15 | eod | -0.010 | -1.444 .. +1.423 | +0.0177 | 0.99 / 0.99 / 0.97 | 0.971 |  |  | 5/8 | n/a | -0.010 |  | -0.1 / -0.0 |  |
| MYM | 15 | h1 * | -0.011 | -0.024 .. +0.002 | -0.0050 | 0.095 / 0.13 / 0.1 | 0.0996 | 1 | 0.865 | 6/8 | n/a | -0.011 | False | -1.2 / -1.7 |  |
| MYM | 15 | h2 | -0.018 | -0.055 .. +0.019 | -0.0004 | 0.33 / 0.36 / 0.22 | 0.219 |  |  | 6/8 | n/a | -0.018 |  | -1.0 / -1.0 |  |
| MYM | 15 | h4 | -0.031 | -0.110 .. +0.048 | +0.0009 | 0.44 / 0.47 / 0.32 | 0.339 |  |  | 7/8 | n/a | -0.031 |  | -1.0 / -0.8 | 0.071 |
| MYM | 15 | h8 | -0.032 | -0.187 .. +0.123 | +0.0060 | 0.68 / 0.7 / 0.56 | 0.564 |  |  | 7/8 | n/a | -0.032 |  | -0.8 / -0.4 |  |
| MYM | 15 | h16 | +0.043 | -0.351 .. +0.438 | +0.0188 | 0.83 / 0.83 / 0.7 | 0.692 |  |  | 1/8 | n/a | +0.043 |  | +0.8 / +0.2 |  |
| MYM | 15 | eod | -0.040 | -1.211 .. +1.132 | +0.0176 | 0.95 / 0.95 / 0.92 | 0.914 |  |  | 6/8 | n/a | -0.040 |  | -0.3 / -0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.074 | +0.064 .. +0.083 | +14.2% | +0.150 | 1.4e-50 | 8.03e-48 | 8/8 |
| MES | 15 | h2 | +0.084 | +0.055 .. +0.113 | +11.3% | +0.162 | 1.5e-08 |  | 7/8 |
| MES | 15 | h4 | +0.083 | +0.015 .. +0.152 | +7.7% | +0.143 | 0.017 |  | 7/8 |
| MES | 15 | h8 | +0.080 | -0.031 .. +0.191 | +5.0% | +0.073 | 0.16 |  | 7/8 |
| MES | 15 | h16 | +0.036 | -0.143 .. +0.216 | +1.5% | -0.081 | 0.77 |  | 6/8 |
| MES | 15 | eod | -0.466 | -1.370 .. +0.439 | -7.9% | -0.660 | 0.32 |  | 4/8 |
| MNQ | 15 | h1 * | +0.066 | +0.043 .. +0.089 | +12.6% | +0.136 | 3.2e-08 | 3.22e-06 | 8/8 |
| MNQ | 15 | h2 | +0.062 | -0.017 .. +0.141 | +8.1% | +0.133 | 0.12 |  | 7/8 |
| MNQ | 15 | h4 | +0.030 | -0.173 .. +0.233 | +2.7% | +0.074 | 0.77 |  | 7/8 |
| MNQ | 15 | h8 | -0.020 | -0.341 .. +0.302 | -1.2% | -0.084 | 0.91 |  | 1/8 |
| MNQ | 15 | h16 | -0.089 | -0.442 .. +0.264 | -3.6% | -0.358 | 0.62 |  | 2/8 |
| MNQ | 15 | eod | -1.105 | -2.647 .. +0.436 | -17.4% | -1.557 | 0.16 |  | 5/8 |
| MYM | 15 | h1 * | +0.070 | +0.051 .. +0.088 | +13.1% | +0.150 | 2.4e-13 | 2.94e-11 | 8/8 |
| MYM | 15 | h2 | +0.070 | +0.015 .. +0.125 | +9.1% | +0.149 | 0.013 |  | 7/8 |
| MYM | 15 | h4 | +0.059 | -0.068 .. +0.187 | +5.3% | +0.106 | 0.36 |  | 7/8 |
| MYM | 15 | h8 | +0.029 | -0.177 .. +0.235 | +1.8% | -0.009 | 0.78 |  | 7/8 |
| MYM | 15 | h16 | -0.036 | -0.412 .. +0.340 | -1.5% | -0.237 | 0.85 |  | 1/8 |
| MYM | 15 | eod | -0.298 | -1.333 .. +0.737 | -5.0% | -0.641 | 0.58 |  | 3/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.60 pts | -1.75 .. +0.56 | 0.32 |
| MNQ | 15 | -0.68 pts | -1.83 .. +0.47 | 0.28 |
| MYM | 15 | -0.47 pts | -1.61 .. +0.67 | 0.43 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | long | 34136 | +0.013 | 0.167 | +0.16 | -3.34 | +nan | -3.34 | -3.42 |
| MES | 15 | h2 | bottom fifth | long | 34136 | +0.016 | 0.167 | +0.37 | -3.13 | +nan | -3.13 | -3.24 |
| MES | 15 | h4 | bottom fifth | long | 34136 | +0.034 | 0.167 | +1.04 | -2.46 | +nan | -2.46 | -2.64 |
| MES | 15 | h8 | bottom fifth | long | 34136 | +0.056 | 0.167 | +1.76 | -1.74 | +nan | -1.74 | -2.03 |
| MES | 15 | h16 | bottom fifth | long | 34136 | +0.076 | 0.167 | +2.93 | -0.57 | +nan | -0.57 | -0.98 |
| MES | 15 | eod | bottom fifth | long | 34136 | +0.173 | 0.167 | +10.61 | +7.11 | +nan | +7.11 | +7.82 |
| MNQ | 15 | h1 | bottom fifth | long | 34130 | +0.016 | 0.058 | +0.25 | -1.75 | +nan | -1.75 | -1.99 |
| MNQ | 15 | h2 | bottom fifth | long | 34130 | +0.011 | 0.058 | +0.45 | -1.55 | +nan | -1.55 | -1.71 |
| MNQ | 15 | h4 | bottom fifth | long | 34130 | +0.026 | 0.058 | +1.15 | -0.85 | +nan | -0.85 | -1.08 |
| MNQ | 15 | h8 | bottom fifth | long | 34130 | +0.050 | 0.058 | +1.59 | -0.41 | +nan | -0.41 | -1.12 |
| MNQ | 15 | h16 | bottom fifth | long | 34130 | +0.006 | 0.058 | +3.55 | +1.55 | +nan | +1.55 | +1.41 |
| MNQ | 15 | eod | bottom fifth | long | 34130 | -0.203 | 0.058 | +11.73 | +9.73 | +nan | +9.73 | +13.64 |
| MYM | 15 | h1 | top fifth | short | 34110 | +0.009 | 0.076 | +0.09 | -1.91 | +nan | -1.91 | -1.93 |
| MYM | 15 | h2 | bottom fifth | long | 34110 | -0.003 | 0.117 | +0.21 | -1.79 | +nan | -1.79 | -1.73 |
| MYM | 15 | h4 | bottom fifth | long | 34110 | -0.004 | 0.117 | +0.55 | -1.45 | +nan | -1.45 | -1.27 |
| MYM | 15 | h8 | bottom fifth | long | 34110 | -0.016 | 0.117 | +0.84 | -1.16 | +nan | -1.16 | -0.78 |
| MYM | 15 | h16 | top fifth | long | 34110 | -0.009 | 0.076 | +1.19 | -0.81 | +nan | -0.81 | -0.59 |
| MYM | 15 | eod | bottom fifth | long | 34110 | -0.148 | 0.117 | +4.23 | +2.23 | +nan | +2.23 | +4.75 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | +0.107 | +0.186 | +0.158 | +0.095 | +0.036 | +0.000 | +0.001 | -0.003 | -0.019 | -0.022 | +0.016 |
| MNQ | 15 | +0.101 | +0.169 | +0.142 | +0.087 | +0.031 | +0.000 | +0.005 | +0.012 | +0.004 | +0.006 | +0.089 |
| MYM | 15 | +0.148 | +0.175 | +0.129 | +0.072 | +0.028 | +0.000 | +0.009 | +0.009 | +0.004 | +0.033 | +0.222 |

## Calibration

- MES 15-min: 170680 bars, 34136 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 170650 bars, 34130 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 170547 bars, 34110 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 50% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
