# Impact card: noise6

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.126 R20 over the rest of the session (to 16:45), p=1; we would catch an effect of 0.079 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=1).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.20 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.586 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.013 | -0.045 .. +0.018 | +0.0021 | 0.42 / 0.36 / 0.39 | 0.42 |  |  | 1/2 | -0.029 | +0.017 |  | -0.9 / -0.8 |  |
| MES | 15 | h2 | -0.017 | -0.056 .. +0.023 | -0.0002 | 0.41 / 0.42 / 0.45 | 0.467 |  |  | 1/2 | -0.042 | +0.030 |  | -0.8 / -0.8 |  |
| MES | 15 | h4 | +0.017 | -0.034 .. +0.067 | +0.0076 | 0.52 / 0.57 / 0.59 | 0.583 |  |  | 1/2 | -0.011 | +0.067 |  | +0.6 / +0.6 | 0.079 |
| MES | 15 | h8 | -0.004 | -0.078 .. +0.070 | +0.0054 | 0.92 / 0.92 / 0.91 | 0.89 |  |  | 1/2 | -0.034 | +0.052 |  | -0.1 / -0.1 |  |
| MES | 15 | h16 | +0.034 | -0.072 .. +0.141 | +0.0063 | 0.53 / 0.5 / 0.53 | 0.564 |  |  | 2/2 | +0.030 | +0.042 |  | +0.6 / +0.6 |  |
| MES | 15 | eod * | -0.126 | -0.380 .. +0.128 | -0.0038 | 0.33 / 0.25 / 0.24 | 0.26 | 1 | 1 | 2/2 | -0.071 | -0.229 | False | -1.3 / -1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.003 | -0.018 .. +0.013 | -0.4% | -0.001 | 0.73 |  | 1/2 |
| MES | 15 | h2 | -0.008 | -0.032 .. +0.015 | -0.9% | -0.003 | 0.6 |  | 2/2 |
| MES | 15 | h4 | -0.015 | -0.047 .. +0.016 | -1.1% | -0.011 | 0.68 |  | 2/2 |
| MES | 15 | h8 * | +0.026 | -0.011 .. +0.064 | +1.4% | +0.015 | 0.22 | 1 | 2/2 |
| MES | 15 | h16 | +0.004 | -0.052 .. +0.059 | +0.1% | +0.001 | 0.9 |  | 1/2 |
| MES | 15 | eod | -0.065 | -0.165 .. +0.035 | -1.4% | -0.050 | 0.25 |  | 2/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.97 pts | -2.68 .. +0.74 | 0.27 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | bottom fifth | long | 7197 | +0.008 | 0.589 | +0.04 | -3.46 | -3.38 | -3.59 | -3.45 |
| MES | 15 | h2 | bottom fifth | long | 7197 | +0.009 | 0.589 | +0.06 | -3.44 | -3.33 | -3.65 | -3.42 |
| MES | 15 | h4 | bottom fifth | short | 7197 | +0.020 | 0.589 | +0.11 | -3.39 | -3.52 | -3.15 | -3.44 |
| MES | 15 | h8 | top fifth | short | 7196 | +0.012 | 0.590 | +0.07 | -3.43 | -3.52 | -3.28 | -3.56 |
| MES | 15 | h16 | bottom fifth | short | 7197 | +0.050 | 0.589 | +0.28 | -3.22 | -3.59 | -2.53 | -3.52 |
| MES | 15 | eod | top fifth | short | 7196 | +0.335 | 0.590 | +1.98 | -1.52 | -2.60 | +0.52 | -3.14 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.042 | +0.008 | -0.024 | -0.004 | +0.003 | +0.000 | -0.012 | -0.018 | +0.022 | +0.001 | +0.047 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 40% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
