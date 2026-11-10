# Impact card: rev_nr7_quiet

narrowest bar of the last 7 -> SMALLER move next hour (no 'squeeze' breakout)

Kind: event. Units: R20 = 'average bar' (mean high-low of the last 20 bars); $ per ONE micro. Every effect is measured AGAINST matched bars (same 15-min slot, weekday, volatility decile, EMA trend, last-bar direction, year), so plain drift such as 'NQ goes up' is removed. Because last-bar direction is a control, a candle-type signal is credited only for what it adds beyond 'the last bar was up / down'. Data 2010 - 2025-06-30 (locked holdout untouched).

## Verdict

- MES 15-min: no measurable direction effect (best +0.010 R20 over the next 1 bar (15 min), p=0.11; we would catch an effect of 0.030 R20 or more 80% of the time).
- MES 15-min size: the market moves 7% LESS after the event than after matched bars over the next 1 bar (15 min) (-0.036 R20, CONFIRMED, q=2.36e-22, 8 of 8 years same sign).
- MES 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $3.50 round trip (best hold now $0.22 at recent bar sizes, 90% range up to $1.90); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 3.0% at p<0.05, 80%-detectable effect 0.041 R20 for ~1 event/session).
- MNQ 15-min: no measurable direction effect (best +0.018 R20 over the next 1 bar (15 min), p=0.89; we would catch an effect of 0.041 R20 or more 80% of the time).
- MNQ 15-min size: no measurable effect on how much price moves (best p=0.31).
- MNQ 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.71 at recent bar sizes, 90% range up to $4.64); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 2.5% at p<0.05, 80%-detectable effect 0.069 R20 for ~1 event/session).
- MYM 15-min: no measurable direction effect (best +0.008 R20 over the next 1 bar (15 min), p=1; we would catch an effect of 0.039 R20 or more 80% of the time).
- MYM 15-min size: no measurable effect on how much price moves (best p=0.02).
- MYM 15-min BOTTOM LINE (direction): INCONCLUSIVE - not confirmed, but the data cannot rule out a per-trade edge as big as the $2.00 round trip (best hold now $0.13 at recent bar sizes, 90% range up to $4.03); the 16-bar / to-16:45 holds hint at an edge at least as big as the cost, so more data on short holds alone will not settle it. Lab self-test for this market/timeframe: PASSED (2026-11-09 13:14; false-positive rate 1.0% at p<0.05, 80%-detectable effect 0.076 R20 for ~1 event/session).

## Direction (does price go further up or down than usual?)

| market | tf | hold | effect R20 | 95% CI | IC | p boot / NW / placebo | placebo rank p | q (BY) | RW p | years same sign | 2010-17 | 2018-25H1 | replicated | t naive / t honest | MDE80 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | +0.010 | +0.002 .. +0.019 | +0.0052 | 0.017 / 0.019 / 0.014 | 0.0142 | 1 | 0.375 | 6/8 | n/a | +0.010 | False | +2.3 / +2.4 |  |
| MES | 15 | h2 | +0.004 | -0.014 .. +0.022 | +0.0014 | 0.63 / 0.64 / 0.5 | 0.487 |  |  | 5/8 | n/a | +0.004 |  | +0.5 / +0.5 |  |
| MES | 15 | h4 | -0.001 | -0.037 .. +0.035 | -0.0002 | 0.96 / 0.96 / 0.91 | 0.913 |  |  | 3/8 | n/a | -0.001 |  | -0.1 / -0.1 | 0.030 |
| MES | 15 | h8 | -0.016 | -0.085 .. +0.052 | -0.0025 | 0.64 / 0.64 / 0.25 | 0.258 |  |  | 4/8 | n/a | -0.016 |  | -0.8 / -0.5 |  |
| MES | 15 | h16 | -0.043 | -0.199 .. +0.112 | -0.0047 | 0.59 / 0.59 / 0.034 | 0.0348 |  |  | 3/8 | n/a | -0.043 |  | -1.6 / -0.5 |  |
| MES | 15 | eod | -0.452 | -1.372 .. +0.469 | -0.0183 | 0.34 / 0.34 / 9.4e-15 | 0.000527 |  |  | 4/8 | n/a | -0.452 |  | -5.3 / -1.0 |  |
| MNQ | 15 | h1 * | +0.018 | -0.005 .. +0.041 | +0.0061 | 0.12 / 0.15 / 0.0023 | 0.0116 | 1 | 0.934 | 7/8 | n/a | +0.018 | False | +1.4 / +1.6 |  |
| MNQ | 15 | h2 | +0.005 | -0.025 .. +0.035 | +0.0010 | 0.73 / 0.77 / 0.62 | 0.536 |  |  | 6/8 | n/a | +0.005 |  | +0.2 / +0.3 |  |
| MNQ | 15 | h4 | +0.000 | -0.068 .. +0.068 | +0.0000 | 0.99 / 0.99 / 0.99 | 0.993 |  |  | 5/8 | n/a | +0.000 |  | +0.0 / +0.0 | 0.041 |
| MNQ | 15 | h8 | -0.000 | -0.103 .. +0.102 | -0.0000 | 0.99 / 0.99 / 0.99 | 0.986 |  |  | 3/8 | n/a | -0.000 |  | -0.0 / -0.0 |  |
| MNQ | 15 | h16 | -0.098 | -0.374 .. +0.178 | -0.0075 | 0.49 / 0.51 / 0.00021 | 0.00105 |  |  | 1/8 | n/a | -0.098 |  | -1.8 / -0.7 |  |
| MNQ | 15 | eod | -0.597 | -2.080 .. +0.886 | -0.0151 | 0.43 / 0.45 / 7.9e-13 | 0.000527 |  |  | 1/8 | n/a | -0.597 |  | -3.2 / -0.8 |  |
| MYM | 15 | h1 * | +0.008 | -0.004 .. +0.019 | +0.0031 | 0.19 / 0.26 / 0.11 | 0.11 | 1 | 0.965 | 7/8 | n/a | +0.008 | False | +0.9 / +1.3 |  |
| MYM | 15 | h2 | -0.011 | -0.050 .. +0.029 | -0.0025 | 0.6 / 0.61 / 0.18 | 0.181 |  |  | 4/8 | n/a | -0.011 |  | -0.6 / -0.5 |  |
| MYM | 15 | h4 | -0.038 | -0.121 .. +0.046 | -0.0053 | 0.38 / 0.4 / 0.011 | 0.0137 |  |  | 6/8 | n/a | -0.038 |  | -1.2 / -0.9 | 0.039 |
| MYM | 15 | h8 | -0.056 | -0.222 .. +0.110 | -0.0061 | 0.51 / 0.51 / 0.014 | 0.0153 |  |  | 3/8 | n/a | -0.056 |  | -1.4 / -0.7 |  |
| MYM | 15 | h16 | -0.182 | -0.603 .. +0.238 | -0.0141 | 0.4 / 0.4 / 2.3e-12 | 0.000527 |  |  | 3/8 | n/a | -0.182 |  | -3.3 / -0.8 |  |
| MYM | 15 | eod | -0.606 | -1.741 .. +0.528 | -0.0194 | 0.29 / 0.3 / 2.5e-21 | 0.000527 |  |  | 4/8 | n/a | -0.606 |  | -4.7 / -1.0 |  |

## Size (does price move MORE, either way?)

| market | tf | hold | extra abs move R20 | 95% CI | % vs average | extra range R20 | p | q (BY) | years same sign |
|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 * | -0.036 | -0.042 .. -0.030 | -6.9% | -0.071 | 7e-25 | 2.36e-22 | 8/8 |
| MES | 15 | h2 | -0.041 | -0.061 .. -0.021 | -5.5% | -0.073 | 4.2e-05 |  | 7/8 |
| MES | 15 | h4 | -0.032 | -0.089 .. +0.025 | -3.0% | -0.052 | 0.26 |  | 7/8 |
| MES | 15 | h8 | -0.015 | -0.112 .. +0.082 | -0.9% | +0.019 | 0.76 |  | 7/8 |
| MES | 15 | h16 | +0.009 | -0.153 .. +0.171 | +0.4% | +0.157 | 0.91 |  | 1/8 |
| MES | 15 | eod | +0.294 | -0.565 .. +1.153 | +5.0% | +0.483 | 0.5 |  | 1/8 |
| MNQ | 15 | h1 * | -0.021 | -0.043 .. +0.000 | -4.1% | -0.039 | 0.052 | 1 | 7/8 |
| MNQ | 15 | h2 | -0.006 | -0.089 .. +0.076 | -0.8% | -0.006 | 0.88 |  | 7/8 |
| MNQ | 15 | h4 | +0.056 | -0.168 .. +0.280 | +5.0% | +0.094 | 0.63 |  | 1/8 |
| MNQ | 15 | h8 | +0.117 | -0.254 .. +0.488 | +7.0% | +0.315 | 0.54 |  | 1/8 |
| MNQ | 15 | h16 | +0.119 | -0.273 .. +0.512 | +4.8% | +0.605 | 0.56 |  | 1/8 |
| MNQ | 15 | eod | +0.725 | -1.020 .. +2.470 | +11.4% | +1.161 | 0.42 |  | 1/8 |
| MYM | 15 | h1 * | -0.028 | -0.046 .. -0.009 | -5.2% | -0.059 | 0.0033 | 0.244 | 7/8 |
| MYM | 15 | h2 | -0.019 | -0.077 .. +0.039 | -2.5% | -0.041 | 0.52 |  | 7/8 |
| MYM | 15 | h4 | +0.018 | -0.119 .. +0.155 | +1.6% | +0.029 | 0.8 |  | 1/8 |
| MYM | 15 | h8 | +0.035 | -0.189 .. +0.260 | +2.2% | +0.147 | 0.76 |  | 1/8 |
| MYM | 15 | h16 | +0.136 | -0.274 .. +0.545 | +5.5% | +0.376 | 0.52 |  | 1/8 |
| MYM | 15 | eod | +0.451 | -0.646 .. +1.548 | +7.5% | +0.624 | 0.43 |  | 1/8 |

## Path: chance of +1 R20 before -1 R20 within 16 bars (change vs matched bars, in the signal's sense)

| market | tf | change in probability | 95% CI | p |
|---|---|---|---|---|
| MES | 15 | +0.32 pts | -0.33 .. +0.97 | 0.33 |
| MNQ | 15 | +0.79 pts | +0.17 .. +1.40 | 0.017 |
| MYM | 15 | +0.15 pts | -0.46 .. +0.76 | 0.63 |

## Money: trading the best leg at each hold ($ per micro per trade, raw = includes drift)

| market | tf | hold | leg | side | trades | gross R20 | cost R20 | gross $ | net $ | net $ 2010-17 | net $ 2018-25H1 | signal-only $ net |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | h1 | event | long | 33280 | +0.012 | 0.129 | +0.32 | -3.18 | +nan | -3.18 | -3.24 |
| MES | 15 | h2 | event | long | 33280 | +0.010 | 0.129 | +0.44 | -3.06 | +nan | -3.06 | -3.13 |
| MES | 15 | h4 | event | short | 33280 | -0.012 | 0.129 | -0.68 | -4.18 | +nan | -4.18 | -4.05 |
| MES | 15 | h8 | event | short | 33280 | -0.006 | 0.129 | -1.08 | -4.58 | +nan | -4.58 | -4.45 |
| MES | 15 | h16 | event | short | 33280 | +0.007 | 0.129 | -2.09 | -5.59 | +nan | -5.59 | -5.43 |
| MES | 15 | eod | event | short | 33280 | +0.291 | 0.129 | -3.92 | -7.42 | +nan | -7.42 | -8.00 |
| MNQ | 15 | h1 | event | long | 29049 | +0.022 | 0.042 | +0.49 | -1.51 | +nan | -1.51 | -1.70 |
| MNQ | 15 | h2 | event | long | 29049 | +0.010 | 0.042 | +0.64 | -1.36 | +nan | -1.36 | -1.54 |
| MNQ | 15 | h4 | event | long | 29049 | +0.008 | 0.042 | +1.15 | -0.85 | +nan | -0.85 | -1.05 |
| MNQ | 15 | h8 | event | short | 29049 | -0.020 | 0.042 | -1.48 | -3.48 | +nan | -3.48 | -3.02 |
| MNQ | 15 | h16 | event | short | 29049 | +0.067 | 0.042 | -3.03 | -5.03 | +nan | -5.03 | -4.81 |
| MNQ | 15 | eod | event | short | 29049 | +0.546 | 0.042 | -7.83 | -9.83 | +nan | -9.83 | -13.95 |
| MYM | 15 | h1 | event | long | 30811 | +0.008 | 0.093 | +0.28 | -1.72 | +nan | -1.72 | -1.75 |
| MYM | 15 | h2 | event | short | 30811 | +0.009 | 0.093 | -0.33 | -2.33 | +nan | -2.33 | -2.36 |
| MYM | 15 | h4 | event | short | 30811 | +0.038 | 0.093 | -0.30 | -2.30 | +nan | -2.30 | -2.48 |
| MYM | 15 | h8 | event | short | 30811 | +0.074 | 0.093 | -0.50 | -2.50 | +nan | -2.50 | -3.07 |
| MYM | 15 | h16 | event | short | 30811 | +0.205 | 0.093 | -0.95 | -2.95 | +nan | -2.95 | -4.05 |
| MYM | 15 | eod | event | short | 30811 | +0.540 | 0.093 | -2.02 | -4.02 | +nan | -4.02 | -6.10 |

## Event study: controlled average path around the signal (R20, close-to-close from the signal bar)

| market | tf | -16 | -8 | -4 | -2 | -1 | +0 | +1 | +2 | +4 | +8 | +16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MES | 15 | -0.103 | -0.148 | -0.162 | -0.084 | -0.006 | +0.000 | -0.003 | -0.009 | -0.013 | -0.033 | -0.084 |
| MNQ | 15 | -0.075 | -0.128 | -0.151 | -0.083 | -0.001 | +0.000 | -0.011 | -0.027 | -0.035 | -0.036 | -0.179 |
| MYM | 15 | -0.079 | -0.113 | -0.131 | -0.060 | +0.002 | +0.000 | -0.017 | -0.037 | -0.067 | -0.099 | -0.278 |

## Calibration

- MES 15-min: 171560 bars, 33280 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 100% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MNQ 15-min: 171530 bars, 29049 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 65% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).
- MYM 15-min: 171427 bars, 30811 in the signal group; power: a true 0.050 R20 effect at dir_h4 is detected 85% of the time (recovered 0.049); look-ahead truncation check: passed (100 cuts, 40 of them on the metric's own signal bars, over 174085 bars; the check tests the metric's code, so a batch runs it once, on its first market / timeframe).

How to read: 'effect' = average extra move in R20 (positive = up for continuous/event, in the trade's favour for sided). p = max(bootstrap-by-session, Newey-West, placebo) (the most conservative). q = Benjamini-Yekutieli false-discovery q over every metric x market x tf in this batch. 'replicated' = found in one half of the data (2010-17 or 2018-25H1) and confirmed in the other. 't naive' ignores overlapping returns and same-day clustering; 't honest' is the session-bootstrap t used for decisions.
