# Impact card: rev_volratio_0930

at 09:30 ET: average bar of last 20 / last 100 bars; high -> down into 16:45

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.297 R20 over the next 2 bars (30 min), p=1; we would catch an effect of 1.026 R20 or more 80% of the time).
- MES 15-min size: the market moves 29% LESS in the metric's top fifth than in its bottom fifth over the next 16 bars (4 h) (-1.187 R20, CONFIRMED, q=0.000818, 7 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $3.76 at recent bar sizes, 90% range up to $12.17); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.181 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 1.879 R20 or more 80% of the time).
- MNQ 15-min size: the market moves 26% LESS in the metric's top fifth than in its bottom fifth over the next 16 bars (4 h) (-1.243 R20, CONFIRMED, q=0.0202, 8 of 8 years same sign).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $3.63 at recent bar sizes, 90% range up to $18.98); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best -0.790 R20 over the next 4 bars (1 h), p=0.081; we would catch an effect of 2.106 R20 or more 80% of the time).
- MYM 15-min size: the market moves 24% LESS in the metric's top fifth than in its bottom fifth over the next 16 bars (4 h) (-1.006 R20, CONFIRMED, q=0.0183, 8 of 8 years same sign).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $7.62 at recent bar sizes, 90% range up to $12.72); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.084 | -0.344 .. +0.177 | +0.0259 | 0.53 / 0.51 / 0.52 | 0.542 |  |  | 4/8 | n/a | -0.084 |  | -0.6 / -0.6 |  |
| MES | 15 | h2 * | -0.297 | -0.759 .. +0.166 | -0.0179 | 0.21 / 0.21 / 0.13 | 0.131 | 1 | 0.994 | 5/8 | n/a | -0.297 | False | -1.2 / -1.3 |  |
| MES | 15 | h4 | -0.330 | -0.942 .. +0.282 | -0.0451 | 0.29 / 0.29 / 0.21 | 0.226 |  |  | 5/8 | n/a | -0.330 |  | -1.0 / -1.1 | 1.026 |
| MES | 15 | h8 | -0.345 | -1.080 .. +0.391 | -0.0364 | 0.36 / 0.35 / 0.32 | 0.33 |  |  | 3/8 | n/a | -0.345 |  | -0.9 / -0.9 |  |
| MES | 15 | h16 | -0.140 | -0.968 .. +0.688 | -0.0184 | 0.74 / 0.74 / 0.72 | 0.712 |  |  | 2/8 | n/a | -0.140 |  | -0.3 / -0.3 |  |
| MES | 15 | eod | +0.367 | -0.601 .. +1.334 | +0.0063 | 0.46 / 0.49 / 0.47 | 0.472 |  |  | 6/8 | n/a | +0.367 |  | +0.7 / +0.7 |  |
| MNQ | 15 | h1 * | +0.181 | -0.298 .. +0.660 | +0.0298 | 0.46 / 0.45 / 0.35 | 0.352 | 1 | 1 | 3/8 | n/a | +0.181 | False | +0.8 / +0.7 |  |
| MNQ | 15 | h2 | -0.172 | -0.657 .. +0.312 | -0.0217 | 0.49 / 0.49 / 0.45 | 0.422 |  |  | 5/8 | n/a | -0.172 |  | -0.7 / -0.7 |  |
| MNQ | 15 | h4 | +0.044 | -0.587 .. +0.675 | -0.0352 | 0.89 / 0.89 / 0.88 | 0.859 |  |  | 4/8 | n/a | +0.044 |  | +0.1 / +0.1 | 1.879 |
| MNQ | 15 | h8 | -0.000 | -0.770 .. +0.769 | -0.0354 | 1 / 1 / 1 | 0.997 |  |  | 2/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MNQ | 15 | h16 | +0.143 | -0.788 .. +1.074 | -0.0417 | 0.76 / 0.77 / 0.74 | 0.752 |  |  | 5/8 | n/a | +0.143 |  | +0.3 / +0.3 |  |
| MNQ | 15 | eod | +0.302 | -0.765 .. +1.369 | -0.0180 | 0.58 / 0.6 / 0.6 | 0.524 |  |  | 5/8 | n/a | +0.302 |  | +0.5 / +0.6 |  |
| MYM | 15 | h1 | -0.077 | -0.638 .. +0.485 | +0.0511 | 0.79 / 0.79 / 0.72 | 0.691 |  |  | 7/8 | n/a | -0.077 |  | -0.3 / -0.3 |  |
| MYM | 15 | h2 | -0.528 | -0.946 .. -0.109 | +0.0027 | 0.013 / 0.018 / 0.013 | 0.0105 |  |  | 8/8 | n/a | -0.528 |  | -2.2 / -2.5 |  |
| MYM | 15 | h4 * | -0.790 | -1.370 .. -0.210 | -0.0384 | 0.0076 / 0.011 / 0.0049 | 0.00316 | 0.905 | 0.193 | 7/8 | n/a | -0.790 | False | -2.4 / -2.7 | 2.106 |
| MYM | 15 | h8 | -0.764 | -1.426 .. -0.102 | -0.0162 | 0.024 / 0.024 / 0.038 | 0.0374 |  |  | 6/8 | n/a | -0.764 |  | -2.1 / -2.3 |  |
| MYM | 15 | h16 | -0.545 | -1.319 .. +0.229 | -0.0173 | 0.17 / 0.15 / 0.16 | 0.168 |  |  | 6/8 | n/a | -0.545 |  | -1.4 / -1.4 |  |
| MYM | 15 | eod | -0.284 | -1.254 .. +0.685 | +0.0086 | 0.57 / 0.58 / 0.57 | 0.532 |  |  | 5/8 | n/a | -0.284 |  | -0.6 / -0.6 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.217 | -0.378 .. -0.056 | -15.4% | -0.538 | 0.0084 |  | 8/8 |
| MES | 15 | h2 | -0.549 | -0.931 .. -0.167 | -28.9% | -1.209 | 0.0056 |  | 8/8 |
| MES | 15 | h4 | -0.778 | -1.272 .. -0.284 | -30.2% | -1.487 | 0.002 |  | 8/8 |
| MES | 15 | h8 | -0.844 | -1.413 .. -0.274 | -25.7% | -1.575 | 0.0045 |  | 7/8 |
| MES | 15 | h16 * | -1.187 | -1.686 .. -0.688 | -29.5% | -1.956 | 8.7e-06 | 0.000818 | 7/8 |
| MES | 15 | eod | -0.559 | -1.261 .. +0.142 | -10.4% | -0.998 | 0.18 |  | 6/8 |
| MNQ | 15 | h1 | -0.567 | -0.926 .. -0.209 | -29.7% | -1.008 | 0.0053 |  | 7/8 |
| MNQ | 15 | h2 | -0.757 | -1.116 .. -0.398 | -31.0% | -1.357 | 0.00048 |  | 8/8 |
| MNQ | 15 | h4 | -0.699 | -1.122 .. -0.277 | -22.1% | -1.569 | 0.014 |  | 7/8 |
| MNQ | 15 | h8 | -1.021 | -1.538 .. -0.504 | -25.7% | -1.650 | 0.0026 |  | 8/8 |
| MNQ | 15 | h16 * | -1.243 | -1.859 .. -0.627 | -26.3% | -1.873 | 0.00024 | 0.0202 | 8/8 |
| MNQ | 15 | eod | -0.457 | -1.328 .. +0.414 | -7.6% | -0.917 | 0.44 |  | 5/8 |
| MYM | 15 | h1 | -0.470 | -0.964 .. +0.023 | -26.7% | -0.955 | 0.074 |  | 6/8 |
| MYM | 15 | h2 | -0.594 | -0.958 .. -0.231 | -26.9% | -1.341 | 0.0017 |  | 8/8 |
| MYM | 15 | h4 | -0.882 | -1.366 .. -0.398 | -31.2% | -1.613 | 0.00045 |  | 8/8 |
| MYM | 15 | h8 | -0.909 | -1.422 .. -0.396 | -26.0% | -1.616 | 0.00062 |  | 8/8 |
| MYM | 15 | h16 * | -1.006 | -1.454 .. -0.557 | -24.1% | -1.957 | 0.00021 | 0.0183 | 8/8 |
| MYM | 15 | eod | -0.440 | -1.098 .. +0.219 | -8.2% | -0.798 | 0.34 |  | 5/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +1.96 pts | -4.60 .. +8.52 | 0.56 |
| MNQ | 15 | -1.54 pts | -7.72 .. +4.63 | 0.76 |
| MYM | 15 | -7.22 pts | -13.01 .. -1.44 | 0.053 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | long | 381 | +0.201 | 0.186 | +2.66 | -0.84 | +nan | -0.84 | -2.42 |
| MES | 15 | h2 | bottom fifth | long | 381 | +0.416 | 0.186 | +5.04 | +1.54 | +nan | +1.54 | -0.45 |
| MES | 15 | h4 | bottom fifth | long | 381 | +0.509 | 0.186 | +8.67 | +5.17 | +nan | +5.17 | +2.92 |
| MES | 15 | h8 | bottom fifth | long | 381 | +0.424 | 0.186 | +2.75 | -0.75 | +nan | -0.75 | -3.75 |
| MES | 15 | h16 | bottom fifth | long | 381 | +0.365 | 0.186 | +3.31 | -0.19 | +nan | -0.19 | -0.38 |
| MES | 15 | eod | top fifth | long | 379 | +0.444 | 0.110 | +20.84 | +17.34 | +nan | +17.34 | +20.47 |
| MNQ | 15 | h1 | top fifth | long | 380 | +0.148 | 0.039 | +3.52 | +1.52 | +nan | +1.52 | -1.05 |
| MNQ | 15 | h2 | bottom fifth | long | 381 | +0.348 | 0.068 | +7.31 | +5.31 | +nan | +5.31 | +6.11 |
| MNQ | 15 | h4 | top fifth | long | 380 | +0.295 | 0.039 | +17.31 | +15.31 | +nan | +15.31 | +17.04 |
| MNQ | 15 | h8 | bottom fifth | long | 381 | +0.287 | 0.068 | +0.58 | -1.42 | +nan | -1.42 | -9.91 |
| MNQ | 15 | h16 | top fifth | long | 380 | +0.379 | 0.039 | +28.85 | +26.85 | +nan | +26.85 | +22.95 |
| MNQ | 15 | eod | top fifth | long | 380 | +0.654 | 0.039 | +45.53 | +43.53 | +nan | +43.53 | +54.16 |
| MYM | 15 | h1 | top fifth | short | 380 | +0.095 | 0.084 | +3.59 | +1.59 | +nan | +1.59 | +3.73 |
| MYM | 15 | h2 | bottom fifth | long | 380 | +0.403 | 0.136 | +2.30 | +0.30 | +nan | +0.30 | -0.28 |
| MYM | 15 | h4 | bottom fifth | long | 380 | +0.616 | 0.136 | +6.63 | +4.63 | +nan | +4.63 | +3.66 |
| MYM | 15 | h8 | bottom fifth | long | 380 | +0.505 | 0.136 | +3.43 | +1.43 | +nan | +1.43 | -0.27 |
| MYM | 15 | h16 | bottom fifth | long | 380 | +0.260 | 0.136 | +2.87 | +0.87 | +nan | +0.87 | +4.68 |
| MYM | 15 | eod | bottom fifth | long | 380 | +0.012 | 0.136 | +0.33 | -1.67 | +nan | -1.67 | +3.20 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.615 | -0.627 | -0.511 | -0.035 | +0.002 | +0.000 | +0.363 | +0.151 | +0.175 | +0.075 | +0.517 |
| MNQ | 15 | -0.511 | -0.539 | -0.301 | -0.010 | -0.045 | +0.000 | +0.307 | -0.186 | +0.043 | +0.068 | +0.277 |
| MYM | 15 | -0.423 | -0.514 | -0.379 | -0.049 | -0.026 | +0.000 | +0.315 | -0.333 | -0.557 | -0.485 | -0.352 |

## Calibration

- MES 15-min: 1901 bars, 379 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 1901 bars, 380 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 1900 bars, 380 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 0% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
