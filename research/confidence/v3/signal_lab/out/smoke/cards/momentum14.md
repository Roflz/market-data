# Impact card: momentum14

Momentum(14) - 100

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 60-min: no measurable direction effect (best +0.017 R20 over the next 1 bar (1 h), p=0.14; we would catch an effect of 0.079 R20 or more 80% of the time).
- MES 60-min size: the market moves 9% LESS in the metric's top fifth than in its bottom fifth over the next 1 bar (1 h) (-0.048 R20, CONFIRMED, q=1.76e-09, 14 of 16 years same sign).
- MES 60-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.59 at recent bar sizes, 90% range up to $4.58); about 3.1x more data would settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:24; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.055 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 * | +0.017 | +0.003 .. +0.031 | +0.0051 | 0.017 / 0.019 / 0.042 | 0.0396 | 0.628 | 0.146 | 14/16 | +0.014 | +0.020 | False | +2.2 / +2.4 |  |
| MES | 60 | h2 | +0.026 | -0.000 .. +0.053 | +0.0063 | 0.053 / 0.055 / 0.096 | 0.0946 |  |  | 12/16 | +0.022 | +0.031 |  | +2.4 / +1.9 |  |
| MES | 60 | h4 | +0.041 | -0.007 .. +0.089 | +0.0090 | 0.093 / 0.093 / 0.15 | 0.156 |  |  | 11/16 | +0.033 | +0.050 |  | +2.6 / +1.7 | 0.079 |
| MES | 60 | h8 | +0.060 | -0.027 .. +0.148 | +0.0105 | 0.18 / 0.16 / 0.23 | 0.227 |  |  | 11/16 | +0.038 | +0.083 |  | +2.9 / +1.4 |  |
| MES | 60 | h16 | +0.024 | -0.125 .. +0.173 | +0.0044 | 0.75 / 0.74 / 0.77 | 0.767 |  |  | 8/16 | -0.041 | +0.089 |  | +0.8 / +0.3 |  |
| MES | 60 | eod | +0.006 | -0.157 .. +0.169 | +0.0012 | 0.94 / 0.94 / 0.94 | 0.944 |  |  | 6/16 | -0.046 | +0.058 |  | +0.2 / +0.1 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 * | -0.048 | -0.062 .. -0.034 | -9.4% | -0.120 | 5.4e-11 | 1.76e-09 | 14/16 |
| MES | 60 | h2 | -0.063 | -0.084 .. -0.042 | -8.6% | -0.154 | 3e-09 |  | 15/16 |
| MES | 60 | h4 | -0.088 | -0.122 .. -0.055 | -8.3% | -0.191 | 2.9e-07 |  | 14/16 |
| MES | 60 | h8 | -0.117 | -0.166 .. -0.068 | -7.8% | -0.244 | 1.3e-05 |  | 14/16 |
| MES | 60 | h16 | -0.133 | -0.224 .. -0.042 | -6.5% | -0.305 | 0.0043 |  | 14/16 |
| MES | 60 | eod | -0.140 | -0.248 .. -0.033 | -6.5% | -0.322 | 0.014 |  | 13/16 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 60 | +1.71 pts | -0.11 .. +3.53 | 0.088 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | h1 | top fifth | long | 16683 | +0.020 | 0.074 | +0.69 | -2.81 | -3.02 | -2.64 | -2.87 |
| MES | 60 | h2 | top fifth | long | 16683 | +0.033 | 0.074 | +1.18 | -2.32 | -2.52 | -2.17 | -2.54 |
| MES | 60 | h4 | top fifth | long | 16683 | +0.055 | 0.074 | +2.25 | -1.25 | -1.75 | -0.84 | -1.80 |
| MES | 60 | h8 | top fifth | long | 16683 | +0.097 | 0.074 | +4.63 | +1.13 | +0.04 | +2.01 | -0.03 |
| MES | 60 | h16 | top fifth | long | 16683 | +0.125 | 0.074 | +5.82 | +2.32 | +0.72 | +3.61 | +0.23 |
| MES | 60 | eod | top fifth | long | 16683 | +0.126 | 0.074 | +5.34 | +1.84 | +0.91 | +2.59 | -0.75 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 60 | -4.419 | -2.967 | -1.583 | -0.863 | -0.464 | +0.000 | +0.014 | +0.019 | +0.021 | +0.010 | -0.065 |

## Calibration

- MES 60-min: 83413 bars, 16683 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 88467 bars).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
