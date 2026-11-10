# Overfitting statistics: MNQ v1 entry models (CPCV, deflated Sharpe ratio, PBO)

Generated 2026-11-09 01:45 by run_cpcv.py (methods: cpcv.py). Money = net $ per 1 MNQ micro after costs, label = 1.5 R target / 16-bar limit (v1). Everything is out of sample and before the locked holdout (sessions from 2025-07-01 are never used).

## 2. Deflated Sharpe ratio of the walk-forward daily $ (Bailey & Lopez de Prado 2014)

DSR = Z[(SR - SR0) sqrt(T-1) / sqrt(1 - skew*SR + (kurt-1)/4 * SR^2)], SR0 = sqrt(V[SR_n]) * ((1-g) Z^-1(1-1/N) + g Z^-1(1-1/(N e))), all Sharpe ratios per SESSION (non-annualized; annualized = x sqrt(252) shown for reading), kurt not excess. The daily series = $ of the walk-forward's taken trades per Globex session 2013-01 .. 2025-06, 0 on sessions without a trade.

Trials in out/trials.csv: 52 rows, 48 entry configurations (modules {'entry': 14, 'entry-approach': 11, 'entry-stop-option': 9, 'entry-ablation': 7, 'entry-context': 4, 'entry-h1h2': 1, 'entry-features': 1, 'entry-structure': 1}), 42 of them on NQ or pooled (which includes NQ). The CPCV rows (module entry-cpcv) re-evaluate existing configurations and are not counted.

V[SR_n] (variance of the trials' per-session Sharpe ratios): 0.00354 from 24 configurations: 6 with a daily series on file (exact) and 18 with only yearly results (APPROXIMATION: per-session SR ~ Sharpe of the 12 yearly totals 2013-2024 / sqrt(252), which has about the same sampling error as a daily estimate under i.i.d. days). Alternative: the sampling variance of one SR estimate under the null, 1/(T-1) = 0.000311 (T = 3212 sessions), i.e. trials that differ only by noise.

| model | N | V | T sessions | $ total | SR/session | SR ann. | skew | kurt | SR0 ann. | PSR(0) | DSR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| logit | 48 (all entry trials) | cross-trial V | 3212 | -18,258.250 | -0.021 | -0.335 | 0.610 | 39.703 | 2.134 | 0.118 | 0.000 |
| logit | 48 (all entry trials) | null V = 1/(T-1) | 3212 | -18,258.250 | -0.021 | -0.335 | 0.610 | 39.703 | 0.633 | 0.118 | 0.000 |
| logit | 42 (NQ/pooled entry trials) | cross-trial V | 3212 | -18,258.250 | -0.021 | -0.335 | 0.610 | 39.703 | 2.085 | 0.118 | 0.000 |
| logit | 42 (NQ/pooled entry trials) | null V = 1/(T-1) | 3212 | -18,258.250 | -0.021 | -0.335 | 0.610 | 39.703 | 0.619 | 0.118 | 0.000 |
| gbm | 48 (all entry trials) | cross-trial V | 3212 | 5,002.000 | 0.005 | 0.073 | 1.386 | 20.979 | 2.134 | 0.603 | 0.000 |
| gbm | 48 (all entry trials) | null V = 1/(T-1) | 3212 | 5,002.000 | 0.005 | 0.073 | 1.386 | 20.979 | 0.633 | 0.603 | 0.022 |
| gbm | 42 (NQ/pooled entry trials) | cross-trial V | 3212 | 5,002.000 | 0.005 | 0.073 | 1.386 | 20.979 | 2.085 | 0.603 | 0.000 |
| gbm | 42 (NQ/pooled entry trials) | null V = 1/(T-1) | 3212 | 5,002.000 | 0.005 | 0.073 | 1.386 | 20.979 | 0.619 | 0.603 | 0.025 |
| vote | 48 (all entry trials) | cross-trial V | 3212 | -273,399.500 | -0.211 | -3.347 | 1.201 | 17.613 | 2.134 | 0.000 | 0.000 |
| vote | 48 (all entry trials) | null V = 1/(T-1) | 3212 | -273,399.500 | -0.211 | -3.347 | 1.201 | 17.613 | 0.633 | 0.000 | 0.000 |
| vote | 42 (NQ/pooled entry trials) | cross-trial V | 3212 | -273,399.500 | -0.211 | -3.347 | 1.201 | 17.613 | 2.085 | 0.000 | 0.000 |
| vote | 42 (NQ/pooled entry trials) | null V = 1/(T-1) | 3212 | -273,399.500 | -0.211 | -3.347 | 1.201 | 17.613 | 0.619 | 0.000 | 0.000 |

Read: PSR(0) = probability the true Sharpe is above 0 ignoring how many things were tried; DSR = the same against the best Sharpe expected from N tries of zero-skill rules. DSR >= 0.95 would be a discovery at 95%.

Trial Sharpe ratios used for V[SR_n]:

| configuration | SR/session | SR ann. | source |
|---|---|---|---|
| h1h2 stop_logit | 0.046 | 0.724 | yearly approx. |
| context strong-context events only X=1.5 | 0.012 | 0.186 | yearly approx. |
| entry NQ gbm | 0.005 | 0.073 | daily |
| entry pooled gbm (NQ trades) | -0.002 | -0.033 | daily |
| context strong-context events only X=3 | -0.008 | -0.129 | yearly approx. |
| approach stat_woe_scorecard | -0.010 | -0.162 | yearly approx. |
| approach stat_shrink_combo | -0.017 | -0.270 | yearly approx. |
| context reversal events only (loose, control) | -0.020 | -0.313 | yearly approx. |
| context all events + strong_ctx X=3 | -0.020 | -0.316 | yearly approx. |
| entry NQ logit | -0.021 | -0.335 | daily |
| features v1/all/logit | -0.021 | -0.338 | yearly approx. |
| context all events + strong_ctx X=1.5 | -0.025 | -0.401 | yearly approx. |
| approach stat_screen_nb | -0.027 | -0.429 | yearly approx. |
| approach stat_screen_sa | -0.030 | -0.480 | yearly approx. |
| approach hand_bulkowski | -0.036 | -0.565 | yearly approx. |
| approach ml_logit_l2 | -0.037 | -0.583 | yearly approx. |
| entry pooled logit (NQ trades) | -0.040 | -0.632 | daily |
| approach ml_creamer_boost | -0.048 | -0.756 | yearly approx. |
| approach stat_screen_rvm | -0.049 | -0.780 | yearly approx. |
| approach stat_nb_woe | -0.058 | -0.917 | yearly approx. |
| approach hand_ndr_composite | -0.068 | -1.077 | yearly approx. |
| approach hand_morris_woe | -0.084 | -1.336 | yearly approx. |
| entry NQ vote | -0.211 | -3.347 | daily |
| entry pooled vote (NQ trades) | -0.216 | -3.436 | daily |

## 3. Probability of backtest overfitting by CSCV (Bailey, Borwein, Lopez de Prado, Zhu 2015/2017)

M = years x configurations matrix of out-of-sample $ (each configuration's walk-forward test-year totals). All C(S, S/2) halvings of the S row-blocks: pick the configuration with the best in-sample half, find its rank in the other half; PBO = share of halvings where that pick lands at or below the median (logit <= 0). Also: probability of loss = share of halvings where the pick loses money in the other half; degradation = slope of out-half on in-half performance of the pick.

| matrix | configs | combinations | PBO | P(loss OOS) | degradation slope | most often picked |
|---|---|---|---|---|---|---|
| main: 2013-2024, 12 one-year blocks, total $ | 21 | 924 | 0.105 | 0.525 | -0.766 | entry NQ gbm (489); context strong-context events only X=1.5 (270); entry pooled gbm (NQ trades) (85) |
| 2013-2024, 12 blocks, Sharpe of yearly $ | 21 | 924 | 0.241 | 0.593 | -1.581 | context strong-context events only X=1.5 (407); entry NQ gbm (335); context strong-context events only X=3 (112) |
| 2013-2024, 6 two-year blocks, total $ | 21 | 20 | 0.100 | 0.450 | -0.782 | entry NQ gbm (12); context strong-context events only X=1.5 (4); entry pooled gbm (NQ trades) (1) |
| 2015-2024 incl. configs starting 2014 (h1h2), 10 blocks, total $ | 23 | 252 | 0.079 | 0.389 | -0.650 | entry NQ gbm (156); entry pooled gbm (NQ trades) (47); context strong-context events only X=1.5 (37) |
| daily $ 2013-2025H1, 16 blocks, Sharpe (6 configs with daily series) | 6 | 12870 | 0.020 | 0.551 | -0.929 | entry NQ gbm (8789); entry pooled gbm (NQ trades) (3736); entry NQ logit (345) |

Configurations in the main matrix (21): entry NQ gbm; entry NQ logit; entry NQ vote; entry pooled logit (NQ trades); entry pooled gbm (NQ trades); approach hand_bulkowski; approach hand_morris_woe; approach hand_ndr_composite; approach ml_creamer_boost; approach ml_logit_l2; approach stat_nb_woe; approach stat_screen_nb; approach stat_screen_rvm; approach stat_screen_sa; approach stat_shrink_combo; approach stat_woe_scorecard; context all events + strong_ctx X=1.5; context all events + strong_ctx X=3; context reversal events only (loose, control); context strong-context events only X=1.5; context strong-context events only X=3.

Approximations: (a) only configurations with out-of-sample results BY YEAR on file can enter M: entry NQ vote/logit/gbm (entry_folds.csv), the pooled models' NQ trades (oos_entry_pooled_*), the approach comparison (approach_folds_NQ_*), feature blocks and context rule walk-forwards (by-year rows), and h1h2 (from 2014, so only in the 2015-2024 matrix). The stop-option (9) and cost-ablation (7) trials saved only pooled numbers, and the two 2-fold timing tests cover 2013-2014 only: they are counted in N for the DSR but are not in M. (b) Identical series (the same configuration logged twice) are kept once; not in M: entry pooled vote (NQ trades); features v1/all/logit; h1h2 stop_logit. (c) Rows are calendar years (synchronous across configurations, as CSCV requires), 2025H1 is left out so the 12 blocks are equal; with 12 rows the in/out halves are 6 years each, so PBO is coarse (924 halvings). (d) Configurations trade different event sets (e.g. stop options, H1/H2 triggers); CSCV only needs synchronous rows, not identical events.

