# Feature importance: NQ 15-minute entry model (v1 features)

Generated 2026-11-09 02:05 by run_importance.py. Out of sample only: walk-forward test years 2013-2024 + 2025H1, training purged (labels must end 1 day before the test year), the 2025-07-01+ holdout never used. Money = net $ per 1 MNQ micro after costs (stop fills slip 1 extra tick). Target = 1.5R target before the stop within 16 bars.

How to read it:

* **MDA log loss** (milli-nats, mn): how much WORSE the model's probabilities get on the unseen year when this feature (or cluster / family) is shuffled across that year's trades. Positive = the model uses it and it is real; ~0 or negative = the model does not need it. **t** = mean / standard error across the 13 test years; 'yrs+' = share of years where it helped.
* **MDA $/trade**: drop in the average $ of the trades the model keeps (p >= its threshold) when the feature is shuffled. Positive = it makes the kept trades better. Much noisier than log loss.
* **SFI**: the feature ALONE (logistic on it, or a 10-bin win-rate table), improvement in log loss over the plain base rate on the unseen year. Judges each feature on its own, so overlap with other features does not hide it.
* **Clusters**: groups of features with average |correlation| >= 0.3 (cut adjusted to give 15-30 groups). Shuffling a whole cluster avoids the trap where two near-copies each look useless because the other one covers for it.

## Full logit model, by test year

Pooled: keeps 26,399 of 273,954 events (9.6%), -0.69 $/trade kept vs all events -2.22 $/trade and random skip at the same count -1.91 $/trade; total -18,258 $ (-1,461 $/year). Mean OOS AUC 0.612.

| year | events | kept | AUC | $/kept | $/all events | $/random skip | random 5-95% | total $ |
|---|---|---|---|---|---|---|---|---|
| 2013 | 21,370 | 172 | 0.701 | -3.54 | -2.55 | -2.56 | -3.50 .. -1.72 | -609 |
| 2014 | 21,354 | 1,451 | 0.686 | -1.02 | -2.40 | -2.41 | -2.86 .. -1.98 | -1,473 |
| 2015 | 22,174 | 2,888 | 0.643 | -1.53 | -2.40 | -2.40 | -2.82 .. -1.98 | -4,411 |
| 2016 | 22,366 | 2,484 | 0.651 | -2.18 | -2.42 | -2.45 | -2.90 .. -1.96 | -5,414 |
| 2017 | 21,588 | 412 | 0.679 | -1.00 | -2.38 | -2.40 | -3.19 .. -1.54 | -412 |
| 2018 | 22,031 | 3,445 | 0.596 | -1.13 | -2.07 | -2.13 | -2.86 .. -1.43 | -3,895 |
| 2019 | 21,373 | 1,214 | 0.597 | -4.04 | -2.29 | -2.35 | -3.35 .. -1.36 | -4,899 |
| 2020 | 21,674 | 8,500 | 0.563 | -0.14 | -1.24 | -1.23 | -2.08 .. -0.39 | -1,172 |
| 2021 | 21,837 | 792 | 0.570 | -7.13 | -2.40 | -2.50 | -5.01 .. +0.43 | -5,644 |
| 2022 | 22,344 | 2,703 | 0.564 | -0.53 | -1.69 | -1.56 | -3.67 .. +0.54 | -1,437 |
| 2023 | 22,370 | 671 | 0.565 | +1.23 | -2.74 | -2.48 | -5.36 .. +0.05 | +827 |
| 2024 | 22,395 | 820 | 0.573 | +13.00 | -1.72 | -1.77 | -5.17 .. +1.96 | +10,662 |
| 2025H1 | 11,078 | 847 | 0.563 | -0.45 | -2.85 | -2.92 | -8.51 .. +2.08 | -382 |

## logit: correlation clusters, ranked by MDA log loss

| cluster | members | MDA ll (mn) | t | yrs+ | MDA $/trade | t | yrs+ | verdict |
|---|---|---|---|---|---|---|---|---|
| c07 | candle pattern + candle family + momentum + signal bar shape/volume + cross-market + stop size / cost: pat_marubozu, pat_outside_bar, pat_inside_bar_breakout, pat_nr7_breakout, pat_clv_extreme +12 | +76.83 | +5.4 | 100% | +1.67 | +1.4 | 62% | matters for the probability, not clearly for $ |
| c25 | signal bar shape/volume + time of day: rng_rel, vol_rel, tod_open | +0.20 | +3.9 | 77% | -0.21 | -0.4 | 46% | matters for the probability, not clearly for $ |
| c27 | day so far + time of day: day_range_rel, tod_asia, tod_europe, tod_midday | +0.14 | +3.8 | 85% | +0.50 | +0.8 | 62% | matters for the probability, not clearly for $ |
| c29 | time of day: tod_close | +0.14 | +2.7 | 62% | +0.16 | +1.6 | 46% | weak |
| c19 | swing structure + trend (EMAs) + momentum + VWAP + day so far + 60-min trend + cross-market: dist_swhi_5, dist_swlo_5, fibpos_5, dist_swhi_10, dist_swlo_10 +13 | +0.11 | +2.1 | 62% | +0.01 | +0.0 | 46% | weak |
| c28 | time of day: tod_uspre | +0.10 | +4.8 | 100% | +0.34 | +1.7 | 77% | matters for the probability, not clearly for $ |
| c23 | swing structure + 60-min trend: struct_10, h1_ema_stack, h1_struct_5 | +0.07 | +1.4 | 54% | +0.04 | +0.1 | 46% | weak |
| c11 | candle pattern: pat_dark_cloud | +0.05 | +1.9 | 69% | +0.18 | +1.4 | 62% | weak |
| c18 | candle pattern: pat_nr7 | +0.05 | +1.9 | 69% | +0.05 | +0.5 | 54% | weak |
| c03 | candle pattern: pat_hammer, pat_pin_bar | +0.03 | +2.4 | 69% | +0.26 | +2.3 | 69% | helps $ only (weak on probability) |
| c06 | candle pattern: pat_shooting_star | +0.02 | +2.5 | 69% | +0.06 | +0.8 | 77% | weak |
| c10 | candle pattern: pat_piercing | +0.01 | +1.2 | 54% | -0.03 | -0.2 | 62% | weak |
| c24 | momentum: mom_x100 | +0.01 | +3.1 | 85% | -0.04 | -0.3 | 54% | matters for the probability, not clearly for $ |
| c16 | candle pattern + signal bar shape/volume: pat_doji, pat_spinning_top, body_frac | +0.01 | +0.8 | 69% | -0.05 | -0.3 | 62% | dead weight |
| c21 | swing structure: struct_5 | +0.01 | +1.0 | 62% | -0.16 | -0.7 | 38% | dead weight |
| c01 | candle pattern: pat_dragonfly_doji | +0.01 | +1.0 | 54% | +0.06 | +1.3 | 62% | dead weight |
| c09 | candle pattern: pat_harami | +0.00 | +0.3 | 54% | -0.09 | -1.2 | 31% | dead weight |
| c13 | candle pattern: pat_three_soldiers_crows | +0.00 | +0.6 | 77% | +0.13 | +1.7 | 69% | dead weight |
| c26 | day so far: gap_open | +0.00 | +0.1 | 46% | -0.13 | -0.5 | 31% | dead weight |
| c22 | swing structure: atfib_5, atfib_10 | +0.00 | +0.1 | 54% | -0.17 | -1.2 | 38% | dead weight |
| c15 | candle pattern + candle family: pat_five_lower_lows_higher_highs, fam_exhaustion | -0.00 | -0.0 | 62% | +0.12 | +0.8 | 62% | dead weight |
| c12 | candle pattern: pat_morning_evening_star | -0.00 | -0.1 | 62% | +0.01 | +0.2 | 38% | dead weight |
| c05 | candle pattern: pat_inverted_hammer | -0.00 | -0.8 | 62% | +0.05 | +2.7 | 85% | helps $ only (weak on probability) |
| c02 | candle pattern: pat_gravestone_doji | -0.00 | -0.9 | 38% | +0.09 | +1.6 | 54% | dead weight |
| c04 | candle pattern: pat_hanging_man | -0.01 | -0.6 | 23% | -0.01 | -0.7 | 38% | dead weight |
| c17 | candle pattern: pat_inside_bar | -0.01 | -0.7 | 38% | -0.01 | -0.1 | 54% | dead weight |
| c14 | candle pattern: pat_three_inside | -0.01 | -1.2 | 38% | -0.04 | -1.7 | 31% | dead weight |
| c30 | day of week: dow_0, dow_1, dow_2, dow_3, dow_4 | -0.01 | -2.4 | 23% | -0.15 | -0.5 | 46% | dead weight |
| c08 | candle pattern + candle family: pat_engulfing, pat_tweezer, fam_reversal | -0.02 | -0.6 | 54% | +0.02 | +0.1 | 46% | dead weight |
| c20 | swing structure: brk_5, brk_10 | -0.02 | -2.2 | 31% | +0.31 | +1.8 | 54% | dead weight |


## logit: feature families, ranked by MDA log loss

| family | cols | MDA ll (mn) | t | yrs+ | MDA $/trade | t | yrs+ | verdict |
|---|---|---|---|---|---|---|---|---|
| stop size / cost | 2 | +86.88 | +5.5 | 100% | +1.81 | +1.6 | 77% | matters for the probability, not clearly for $ |
| signal bar shape/volume | 4 | +1.62 | +4.0 | 92% | +0.73 | +0.8 | 77% | matters for the probability, not clearly for $ |
| candle family | 5 | +1.23 | +3.6 | 85% | +0.87 | +0.9 | 62% | matters for the probability, not clearly for $ |
| candle pattern | 28 | +1.15 | +8.3 | 100% | +1.50 | +1.6 | 69% | matters for the probability, not clearly for $ |
| time of day | 6 | +0.54 | +7.3 | 100% | -0.21 | -0.6 | 46% | matters for the probability, not clearly for $ |
| momentum | 3 | +0.21 | +5.2 | 92% | +0.50 | +1.5 | 69% | matters for the probability, not clearly for $ |
| trend (EMAs) | 6 | +0.18 | +2.0 | 62% | +0.24 | +0.5 | 38% | weak |
| swing structure | 12 | +0.18 | +4.4 | 85% | +0.49 | +0.8 | 54% | matters for the probability, not clearly for $ |
| day so far | 3 | +0.17 | +2.3 | 77% | +0.39 | +0.6 | 62% | matters for the probability, not clearly for $ |
| VWAP | 1 | +0.09 | +2.2 | 77% | -0.24 | -1.2 | 31% | matters for the probability, not clearly for $ |
| cross-market | 4 | +0.06 | +0.9 | 54% | +0.07 | +0.1 | 46% | dead weight |
| 60-min trend | 3 | +0.02 | +0.5 | 38% | -0.09 | -0.2 | 38% | dead weight |
| day of week | 5 | -0.01 | -2.0 | 31% | -0.09 | -0.3 | 54% | dead weight |


MDA $/kept trade by test year, top 5 clusters (logit):

| cluster | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025H1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c07 | -1.13 | +1.37 | +0.70 | -0.13 | +1.04 | +1.03 | -1.49 | +0.43 | -2.35 | -1.41 | +3.57 | +14.31 | +5.71 |
| c25 | -0.07 | +0.48 | +0.37 | -0.54 | -0.73 | -0.06 | -1.67 | +0.39 | -6.01 | -0.24 | +1.86 | +1.66 | +1.84 |
| c27 | -0.50 | +0.59 | +0.44 | -0.27 | +0.30 | +0.14 | +0.08 | +0.51 | -1.68 | -1.35 | +1.72 | +7.58 | -1.06 |
| c29 | -0.09 | +0.04 | -0.10 | -0.08 | -0.04 | +0.37 | -0.06 | -0.08 | +0.99 | -0.19 | +0.76 | +0.31 | +0.23 |
| c19 | -0.50 | +0.92 | +0.06 | +0.17 | -0.74 | -0.09 | -0.63 | +0.58 | -3.43 | +0.07 | -0.03 | +3.76 | -0.03 |


## Single features (logit MDA + model-free SFI), ranked by MDA log loss

| feature | family | cluster | MDA ll (mn) | t | MDA $ | t | SFI logit (mn) | t | SFI bins (mn) | t | SFI AUC | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cost_R | stop size / cost | c07 | +87.63 | +5.3 | +1.45 | +1.4 | +34.21 | +6.9 | +35.88 | +6.7 | 0.613 | matters for the probability, not clearly for $ |
| clv | signal bar shape/volume | c07 | +1.42 | +3.6 | +0.58 | +0.6 | +9.73 | +3.2 | +17.30 | +4.4 | 0.600 | matters for the probability, not clearly for $ |
| fam_breakout | candle family | c07 | +0.56 | +3.8 | +0.67 | +1.1 | +2.44 | +2.1 | +2.92 | +2.7 | 0.543 | matters for the probability, not clearly for $ |
| fam_continuation | candle family | c07 | +0.27 | +1.9 | -0.14 | -0.2 | +2.71 | +3.2 | +2.66 | +3.2 | 0.541 | weak |
| tod_asia | time of day | c27 | +0.24 | +6.4 | +0.44 | +1.1 | +0.58 | +1.0 | +0.58 | +1.0 | 0.518 | matters for the probability, not clearly for $ |
| stop_R20 | stop size / cost | c07 | +0.20 | +2.9 | +0.90 | +1.1 | +5.28 | +2.8 | +8.60 | +1.8 | 0.600 | weak |
| ema20_slope | trend (EMAs) | c19 | +0.18 | +2.2 | +0.21 | +0.8 | -0.00 | -0.0 | -0.04 | -1.6 | 0.502 | matters for the probability, not clearly for $ |
| pat_tall_trend_bar | candle pattern | c07 | +0.17 | +4.4 | +0.72 | +2.1 | +1.52 | +2.9 | +1.63 | +2.8 | 0.530 | matters (probability and $) |
| day_ret | day so far | c19 | +0.15 | +3.3 | -0.13 | -0.5 | +0.12 | +1.2 | +0.30 | +1.5 | 0.513 | matters for the probability, not clearly for $ |
| dist_ema50 | trend (EMAs) | c19 | +0.11 | +1.6 | -0.33 | -0.7 | +0.39 | +3.1 | +0.33 | +2.5 | 0.516 | weak |
| mom_slope3 | momentum | c07 | +0.11 | +4.2 | +0.10 | +0.4 | +0.44 | +1.4 | +1.61 | +3.6 | 0.529 | matters for the probability, not clearly for $ |
| tod_close | time of day | c29 | +0.11 | +2.3 | +0.04 | +0.4 | +0.05 | +2.0 | +0.04 | +1.7 | 0.503 | weak |
| above_ema20_share | trend (EMAs) | c19 | +0.10 | +1.2 | -0.10 | -0.4 | -0.02 | -0.5 | -0.06 | -1.6 | 0.502 | weak |
| rng_rel | signal bar shape/volume | c25 | +0.09 | +2.4 | +0.59 | +1.1 | +0.40 | +0.7 | +1.10 | +1.5 | 0.533 | matters for the probability, not clearly for $ |
| tod_uspre | time of day | c28 | +0.09 | +4.2 | +0.50 | +2.4 | -0.08 | -4.0 | -0.08 | -4.2 | 0.498 | matters (probability and $) |
| pat_bar_80_20 | candle pattern | c07 | +0.08 | +2.1 | -0.02 | -0.1 | +3.74 | +3.2 | +3.76 | +3.1 | 0.548 | weak |
| dist_vwap | VWAP | c19 | +0.08 | +2.1 | -0.07 | -0.2 | +0.54 | +2.1 | +0.83 | +2.8 | 0.525 | weak |
| mom | momentum | c19 | +0.06 | +2.2 | +0.26 | +1.0 | +0.10 | +0.7 | +1.34 | +3.7 | 0.523 | matters for the probability, not clearly for $ |
| dist_swlo_10 | swing structure | c19 | +0.05 | +4.3 | -0.05 | -0.2 | -0.00 | -0.0 | +0.03 | +0.5 | 0.507 | matters for the probability, not clearly for $ |
| pat_dark_cloud | candle pattern | c11 | +0.05 | +2.2 | +0.12 | +1.1 | +0.16 | +2.3 | +0.17 | +2.3 | 0.503 | matters for the probability, not clearly for $ |
| tod_open | time of day | c25 | +0.04 | +2.4 | -0.53 | -1.6 | +0.05 | +0.2 | +0.05 | +0.2 | 0.506 | weak |
| pat_inside_bar_breakout | candle pattern | c07 | +0.04 | +3.4 | -0.51 | -2.0 | +1.22 | +2.5 | +1.29 | +2.7 | 0.521 | matters for the probability, not clearly for $ |
| day_range_rel | day so far | c27 | +0.04 | +1.0 | +0.79 | +1.5 | +1.19 | +2.3 | +2.14 | +3.0 | 0.530 | dead weight |
| pat_nr7 | candle pattern | c18 | +0.03 | +1.6 | -0.02 | -0.1 | -0.14 | -1.3 | -0.14 | -1.3 | 0.506 | weak |
| fam_reversal | candle family | c08 | +0.03 | +2.2 | -0.15 | -0.8 | +2.58 | +2.3 | +2.58 | +2.3 | 0.543 | matters for the probability, not clearly for $ |
| pat_hammer | candle pattern | c03 | +0.03 | +3.2 | +0.29 | +2.6 | +0.21 | +2.5 | +0.21 | +2.5 | 0.503 | matters (probability and $) |
| pat_clv_extreme | candle pattern | c07 | +0.03 | +1.0 | -0.41 | -0.8 | +7.45 | +2.9 | +8.37 | +2.7 | 0.580 | dead weight |
| x_ES_ema_stack | cross-market | c19 | +0.03 | +0.7 | +0.30 | +0.9 | -0.01 | -0.6 | +0.01 | +0.4 | 0.502 | dead weight |
| dist_ema20 | trend (EMAs) | c19 | +0.03 | +2.0 | +0.11 | +0.6 | +0.92 | +3.7 | +0.94 | +2.8 | 0.527 | weak |
| dist_swhi_10 | swing structure | c19 | +0.02 | +2.0 | +0.05 | +0.7 | +0.54 | +3.9 | +0.57 | +3.2 | 0.519 | weak |
| pat_piercing | candle pattern | c10 | +0.02 | +1.9 | +0.01 | +0.1 | +0.44 | +2.6 | +0.45 | +2.6 | 0.506 | weak |
| fibpos_10 | swing structure | c19 | +0.02 | +1.7 | -0.27 | -1.1 | +0.08 | +1.8 | +0.32 | +2.8 | 0.514 | weak |
| mom_x100 | momentum | c24 | +0.02 | +4.0 | -0.03 | -0.2 | +0.88 | +4.0 | +0.88 | +4.0 | 0.517 | matters for the probability, not clearly for $ |
| body_frac | signal bar shape/volume | c16 | +0.02 | +2.1 | +0.03 | +0.2 | +0.28 | +4.4 | +1.05 | +7.0 | 0.514 | matters for the probability, not clearly for $ |
| dist_swhi_5 | swing structure | c19 | +0.02 | +1.8 | -0.09 | -0.4 | +0.67 | +5.1 | +0.60 | +3.3 | 0.518 | weak |
| fam_closeloc | candle family | c07 | +0.02 | +0.8 | +0.30 | +0.7 | +7.37 | +2.8 | +8.34 | +2.6 | 0.579 | dead weight |
| pat_pin_bar | candle pattern | c03 | +0.01 | +1.6 | +0.18 | +1.2 | +0.33 | +1.8 | +0.30 | +1.5 | 0.508 | weak |
| tod_midday | time of day | c27 | +0.01 | +2.4 | -0.14 | -1.0 | +0.59 | +1.9 | +0.59 | +1.8 | 0.512 | matters for the probability, not clearly for $ |
| pat_outside_bar | candle pattern | c07 | +0.01 | +0.9 | +0.04 | +0.3 | +0.60 | +1.6 | +0.69 | +2.0 | 0.516 | dead weight |
| h1_ema_stack | 60-min trend | c23 | +0.01 | +0.6 | +0.05 | +0.2 | -0.01 | -0.8 | -0.03 | -1.9 | 0.500 | dead weight |
| pat_marubozu | candle pattern | c07 | +0.01 | +1.9 | -0.18 | -1.4 | +2.16 | +4.4 | +3.12 | +4.8 | 0.519 | weak |
| tod_europe | time of day | c27 | +0.01 | +2.8 | -0.06 | -0.9 | -0.01 | -0.7 | -0.01 | -1.1 | 0.499 | matters for the probability, not clearly for $ |
| pat_shooting_star | candle pattern | c06 | +0.01 | +0.8 | +0.03 | +0.3 | +0.10 | +1.6 | +0.11 | +1.9 | 0.502 | dead weight |
| pat_dragonfly_doji | candle pattern | c01 | +0.01 | +0.9 | +0.06 | +2.3 | +0.12 | +2.4 | +0.21 | +2.9 | 0.503 | helps $ only (weak on probability) |
| struct_10 | swing structure | c23 | +0.01 | +0.3 | -0.01 | -0.0 | -0.02 | -0.7 | -0.02 | -0.9 | 0.500 | dead weight |
| pat_clv5_extreme | candle pattern | c07 | +0.01 | +1.7 | -0.23 | -1.2 | +3.07 | +2.9 | +3.10 | +2.8 | 0.543 | weak |
| h1_mom | 60-min trend | c19 | +0.01 | +0.4 | +0.34 | +0.9 | -0.01 | -0.9 | +0.37 | +1.6 | 0.505 | dead weight |
| gap_open | day so far | c26 | +0.00 | +0.5 | +0.05 | +0.2 | -0.01 | -0.5 | -0.11 | -1.5 | 0.496 | dead weight |
| pat_three_soldiers_crows | candle pattern | c13 | +0.00 | +1.4 | +0.10 | +1.2 | +0.16 | +4.0 | +0.15 | +4.3 | 0.502 | weak |
| x_ES_ret | cross-market | c07 | +0.00 | +0.3 | +0.15 | +0.4 | +3.82 | +3.1 | +5.27 | +2.7 | 0.569 | dead weight |
| dist_swlo_5 | swing structure | c19 | +0.00 | +0.6 | +0.09 | +0.6 | +0.03 | +1.1 | +0.14 | +1.3 | 0.516 | dead weight |
| pat_nr7_breakout | candle pattern | c07 | +0.00 | +0.2 | +0.09 | +0.9 | +1.24 | +2.0 | +1.31 | +2.1 | 0.523 | dead weight |
| vol_rel | signal bar shape/volume | c25 | +0.00 | +1.0 | +0.05 | +0.3 | +0.06 | +0.2 | +2.02 | +6.2 | 0.526 | weak |
| x_YM_ema_stack | cross-market | c19 | +0.00 | +0.0 | -0.15 | -0.6 | -0.01 | -0.2 | +8.37 | +5.4 | 0.500 | dead weight |
| dow_4 | day of week | c30 | +0.00 | +0.5 | +0.01 | +0.1 | +0.00 | +0.7 | -0.00 | -0.3 | 0.501 | dead weight |
| pat_morning_evening_star | candle pattern | c12 | +0.00 | +0.1 | +0.02 | +0.1 | +0.13 | +2.5 | +0.13 | +2.9 | 0.502 | dead weight |
| x_YM_ret | cross-market | c07 | +0.00 | +0.1 | -0.09 | -0.4 | +1.44 | +2.7 | +10.35 | +6.9 | 0.538 | dead weight |
| brk_10 | swing structure | c20 | +0.00 | +0.0 | +0.15 | +1.4 | +0.28 | +2.4 | +0.29 | +2.6 | 0.505 | dead weight |
| struct_5 | swing structure | c21 | -0.00 | -0.1 | -0.20 | -1.0 | -0.01 | -1.2 | -0.02 | -1.3 | 0.498 | dead weight |
| pat_five_lower_lows_higher_highs | candle pattern | c15 | -0.00 | -0.1 | +0.13 | +0.8 | -0.02 | -0.9 | +0.07 | +1.6 | 0.503 | dead weight |
| dow_1 | day of week | c30 | -0.00 | -0.5 | -0.05 | -0.8 | -0.00 | -0.0 | -0.00 | -0.8 | 0.500 | dead weight |
| atfib_5 | swing structure | c22 | -0.00 | -0.2 | +0.02 | +0.1 | -0.00 | -0.3 | -0.01 | -0.5 | 0.503 | dead weight |
| pat_engulfing | candle pattern | c08 | -0.00 | -0.1 | +0.26 | +0.9 | +0.97 | +2.2 | +0.98 | +2.3 | 0.519 | dead weight |
| pat_hanging_man | candle pattern | c04 | -0.00 | -0.2 | -0.01 | -0.6 | +0.04 | +0.8 | +0.02 | +0.4 | 0.501 | dead weight |
| fam_exhaustion | candle family | c15 | -0.00 | -0.3 | +0.21 | +1.5 | -0.02 | -0.9 | +0.07 | +1.6 | 0.503 | dead weight |
| dow_3 | day of week | c30 | -0.00 | -1.2 | +0.09 | +0.6 | -0.01 | -1.6 | -0.01 | -2.0 | 0.500 | dead weight |
| dow_0 | day of week | c30 | -0.00 | -0.9 | -0.05 | -0.5 | -0.01 | -1.7 | -0.01 | -2.8 | 0.498 | dead weight |
| pat_gravestone_doji | candle pattern | c02 | -0.00 | -0.5 | +0.00 | +0.1 | +0.08 | +1.3 | +0.19 | +1.6 | 0.502 | dead weight |
| pat_inverted_hammer | candle pattern | c05 | -0.00 | -1.2 | +0.01 | +0.9 | +0.04 | +1.8 | +0.03 | +1.0 | 0.501 | dead weight |
| pat_spinning_top | candle pattern | c16 | -0.00 | -0.6 | +0.07 | +1.1 | +0.29 | +2.9 | +0.29 | +2.8 | 0.506 | dead weight |
| pat_doji | candle pattern | c16 | -0.00 | -1.5 | +0.04 | +1.7 | -0.01 | -0.5 | -0.01 | -0.7 | 0.500 | dead weight |
| atfib_10 | swing structure | c22 | -0.01 | -1.5 | +0.02 | +0.3 | -0.01 | -2.3 | -0.01 | -2.9 | 0.499 | dead weight |
| pat_inside_bar | candle pattern | c17 | -0.01 | -0.5 | -0.03 | -0.2 | -0.10 | -2.4 | -0.10 | -2.4 | 0.503 | dead weight |
| dow_2 | day of week | c30 | -0.01 | -1.6 | -0.11 | -1.2 | -0.01 | -0.8 | -0.01 | -1.1 | 0.500 | dead weight |
| pat_three_inside | candle pattern | c14 | -0.01 | -0.8 | +0.00 | +0.1 | +0.07 | +1.1 | +0.07 | +1.4 | 0.501 | dead weight |
| pat_tweezer | candle pattern | c08 | -0.01 | -0.7 | -0.00 | -0.0 | +0.53 | +2.4 | +0.53 | +2.2 | 0.511 | dead weight |
| h1_struct_5 | 60-min trend | c23 | -0.01 | -0.7 | +0.13 | +0.7 | -0.01 | -0.2 | -0.01 | -0.4 | 0.502 | dead weight |
| pat_harami | candle pattern | c09 | -0.01 | -0.6 | -0.14 | -1.1 | +0.15 | +1.1 | +0.15 | +1.1 | 0.504 | dead weight |
| brk_5 | swing structure | c20 | -0.01 | -2.4 | +0.03 | +0.2 | +0.47 | +2.7 | +0.49 | +2.9 | 0.509 | dead weight |
| ema_stack | trend (EMAs) | c19 | -0.02 | -2.9 | +0.03 | +0.1 | -0.00 | -0.2 | -0.00 | -0.1 | 0.503 | dead weight |
| fibpos_5 | swing structure | c19 | -0.02 | -1.3 | -0.03 | -0.2 | +0.17 | +2.4 | +0.41 | +2.6 | 0.517 | dead weight |
| dist_ema8 | trend (EMAs) | c19 | -0.02 | -1.5 | +0.25 | +0.6 | +1.91 | +4.1 | +2.11 | +2.8 | 0.544 | dead weight |


## Plain English

* Families the model really leans on (shuffling them hurts the probabilities in most test years, t >= 2): stop size / cost (+86.88 mn, $ +1.81), signal bar shape/volume (+1.62 mn, $ +0.73), candle family (+1.23 mn, $ +0.87), candle pattern (+1.15 mn, $ +1.50), time of day (+0.54 mn, $ -0.21), momentum (+0.21 mn, $ +0.50), swing structure (+0.18 mn, $ +0.49), day so far (+0.17 mn, $ +0.39), VWAP (+0.09 mn, $ -0.24).
* Families that are dead weight in the logit model (shuffling them changes nothing or helps): cross-market, 60-min trend, day of week.
* Single features that are dead weight both inside the model (MDA) and alone (SFI t < 2): 26 of 82: x_ES_ema_stack, h1_ema_stack, pat_shooting_star, struct_10, h1_mom, gap_open, dist_swlo_5, dow_4, struct_5, pat_five_lower_lows_higher_highs, dow_1, atfib_5, pat_hanging_man, fam_exhaustion, dow_3, dow_0, pat_gravestone_doji, pat_inverted_hammer, pat_doji, atfib_10, pat_inside_bar, dow_2, pat_three_inside, h1_struct_5, pat_harami, ema_stack.
* Clusters that measurably raise the $ of the kept trades (MDA $ t >= 2, >= 60% of years): c03 [candle pattern: pat_hammer, pat_pin_bar] +0.26 $/trade, c05 [candle pattern: pat_inverted_hammer] +0.05 $/trade.
* Caveat: importance says what the model uses, not that the model makes money; compare the full-model $/kept with the all-events and random-skip columns above.
