# Impact card: noise7

Kind: continuous. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best -0.106 R20 over the next 8 bars (2 h), p=0.073; we would catch an effect of 0.076 R20 or more 80% of the time).
- MES 15-min size: no measurable effect on how much price moves (best p=0.67).
- MES 15-min BOTTOM LINE (direction): CONFIDENTLY NOTHING - at every hold of 1-8 bars the 90% range of the per-trade edge is at most $0.51 per micro (at recent bar sizes), inside the $3.50 round trip (break-even 0.587 R20), and longer holds are below it too: whatever the true effect is, it cannot pay for the trade. WARNING: look-ahead UNCHECKED - the metric was given as numbers, so the lab could not test it for peeking at the future; pass it as a function fn(bars) to get it checked. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.003 | -0.028 .. +0.022 | -0.0012 | 0.82 / 0.82 / 0.84 | 0.834 |  |  | 1/2 | -0.016 | +0.021 |  | -0.2 / -0.2 |  |
| MES | 15 | h2 | -0.027 | -0.059 .. +0.004 | -0.0068 | 0.09 / 0.15 / 0.18 | 0.18 |  |  | 2/2 | -0.027 | -0.028 |  | -1.3 / -1.7 |  |
| MES | 15 | h4 | -0.058 | -0.111 .. -0.004 | -0.0082 | 0.034 / 0.041 / 0.042 | 0.047 |  |  | 2/2 | -0.044 | -0.083 |  | -2.0 / -2.1 | 0.076 |
| MES | 15 | h8 * | -0.106 | -0.187 .. -0.025 | -0.0111 | 0.011 / 0.0084 / 0.0081 | 0.00829 | 1 | 0.3 | 2/2 | -0.107 | -0.104 | False | -2.6 / -2.6 |  |
| MES | 15 | h16 | -0.107 | -0.227 .. +0.013 | -0.0067 | 0.08 / 0.06 / 0.054 | 0.0497 |  |  | 2/2 | -0.130 | -0.066 |  | -1.9 / -1.8 |  |
| MES | 15 | eod | -0.239 | -0.426 .. -0.051 | -0.0120 | 0.013 / 0.013 / 0.01 | 0.0166 |  |  | 2/2 | -0.278 | -0.165 |  | -2.4 / -2.5 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | -0.004 | -0.022 .. +0.014 | -0.6% | -0.003 | 0.67 |  | 1/2 |
| MES | 15 | h2 | -0.004 | -0.025 .. +0.017 | -0.4% | -0.005 | 0.79 |  | 2/2 |
| MES | 15 | h4 * | -0.033 | -0.065 .. -0.002 | -2.5% | -0.009 | 0.11 | 1 | 2/2 |
| MES | 15 | h8 | +0.006 | -0.039 .. +0.050 | +0.3% | +0.002 | 0.81 |  | 1/2 |
| MES | 15 | h16 | +0.034 | -0.032 .. +0.100 | +1.3% | +0.021 | 0.31 |  | 2/2 |
| MES | 15 | eod | -0.039 | -0.149 .. +0.072 | -0.9% | -0.025 | 0.5 |  | 2/2 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | -0.44 pts | -1.83 .. +0.94 | 0.55 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | top fifth | short | 7196 | +0.007 | 0.589 | +0.04 | -3.46 | -3.46 | -3.46 | -3.48 |
| MES | 15 | h2 | bottom fifth | long | 7197 | +0.014 | 0.589 | +0.09 | -3.41 | -3.37 | -3.47 | -3.38 |
| MES | 15 | h4 | bottom fifth | long | 7197 | +0.036 | 0.589 | +0.23 | -3.27 | -3.18 | -3.44 | -3.21 |
| MES | 15 | h8 | bottom fifth | long | 7197 | +0.058 | 0.589 | +0.36 | -3.14 | -2.84 | -3.69 | -3.02 |
| MES | 15 | h16 | top fifth | short | 7196 | +0.101 | 0.589 | +0.60 | -2.90 | -3.43 | -1.97 | -3.21 |
| MES | 15 | eod | top fifth | short | 7196 | +0.387 | 0.589 | +2.26 | -1.24 | -2.09 | +0.23 | -2.90 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.012 | -0.024 | +0.006 | +0.017 | -0.011 | +0.000 | -0.003 | -0.027 | -0.052 | -0.101 | -0.115 |

## Calibration

- MES 15-min: 35981 bars, 7196 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 60% of the time (recovered 0.050); look-ahead truncation check: UNCHECKED (metric given as numbers; pass a function fn(bars) so the lab can test it).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
