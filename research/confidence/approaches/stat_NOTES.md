# Statistically derived weights (`approach_stat.py`)

Ten registered scorers (family `stat`). Each one estimates every signal's weight from the TRAINING rows with a published statistical method. All of them work for `task="entry"` and `task="exit"`.

`score()` always returns **log-odds**: the method's raw output passed through a monotone Platt map fitted on the training rows. `raw_score()` returns the method's own output, and `predict_proba() = sigmoid(score())`. For the linear methods, `weights_table()` rows add up exactly to `score()`: the intercept plus each weight times its indicator or bin. That makes them usable as priors or offsets for the ML variants. Points = weight / (ln 2 / 20), so +20 points doubles the odds.

| name | method | source |
|---|---|---|
| `stat_screen_nb` | screen, then naive Bayes on the best 15 survivors | Hassanniakalager, Sermpinis & Stasinakis (2021) §2.5 |
| `stat_screen_rvm` | screen, then a Relevance Vector Machine (RBF) on all survivors | same paper §2.2; Tipping (2001) |
| `stat_screen_dma` | screen, then Dynamic Model Averaging over all 2^10 subsets of the best 10 survivors | same paper §2.3; Raftery, Kárný & Ettler (2010) |
| `stat_screen_dms` | screen, then Dynamic Model Selection (same recursion, top model) | same paper §2.3 |
| `stat_screen_bma` | screen, then conventional BMA = DMA with δ = λ = 1 | same paper §2.3 ("δ = λ = 1 … conventional BMA") |
| `stat_screen_bnn` | screen, then a Bayesian-regularised neural net (Levenberg–Marquardt) on the best 15 | same paper §2.4; Ticknor (2013); Foresee & Hagan (1997) |
| `stat_screen_sa` | screen, then a simple average of the best 15 (the paper's naive benchmark) | same paper §4.2 |
| `stat_nb_woe` | naive Bayes / weight-of-evidence sum, Laplace add-one | Good (1950); Spiegelhalter & Knill-Jones (1984) |
| `stat_woe_scorecard` | monotone coarse classing, WoE, IV ≥ 0.02, logistic regression on WoE, PDO = 20 points | Siddiqi (2006); Anderson (2007) |
| `stat_shrink_combo` | one logistic forecast per signal family, combined with weights shrunk toward 1/K; δ chosen on an inner purged time split | Diebold & Pauly (1990); Diebold & Shin (2019); Smith & Wallis (2009); Claeskens et al. (2016) |

The linear scorers are `nb`, `sa`, `dma`, `dms`, `bma`, `nb_woe`, `scorecard` and `shrink_combo`. RVM and BNN are nonlinear. Their `weights_table` is a least-squares linearisation of the log-odds score, flagged as such in `meaning`, with R² shown.

---

## 1. Hassanniakalager, Sermpinis & Stasinakis (2021): screen, then combine

**Sources read:**
- the journal eprint (https://eprints.gla.ac.uk/246954/), full text;
- the thesis, chapter 2 (https://theses.gla.ac.uk/30934/);
- Romano & Wolf (2010, *Ann. Statist.* 38:598-633), full text;
- Romano & Wolf (2005, *Econometrica*), working-paper version (Oct 2003), full text;
- Raftery, Kárný & Ettler (2010, *Technometrics* 52:52-66), full text.

Romano, Shaikh & Wolf (2008, *Econometric Theory* 24:404-447) could not be accessed: it is paywalled and the working-paper link is dead. Its k-StepM is the k-FWER stepdown that Romano & Wolf (2010) restate and balance, so that is the version implemented.

### What the paper does, and what we copy

| paper (section / equation) | what we do |
|---|---|
| 7,846 rules from five families (filters, MAs, S&R, channel breakouts, OBV), each signalling long/short/hold (§3.1, App. A) | **Adapted.** Our candidates already carry a direction, so a rule is a feature condition that says TAKE (fires) or SKIP. The universe covers both directions of every condition: each value of a {−1,0,1} or {0,1} flag (`ema_stack = +1`, `ema_stack = -1`, …) and `> q` / `<= q` at the training quintile cuts q20..q80 of each continuous column (our grid, a fallback). About 780 rules on the SPEC columns. |
| Test statistic: studentized mean excess return over a benchmark, H0: θ ≤ 0 vs H1: θ > 0 (eq. 1-3) | Per **session day**, rule excess = Σ over that day's candidates of w·(fires − f)·net $, where f is the rule's training firing share. That is the rule's $ minus a **random skip of the same activity**. Net $ = `pnl_usd` (entries) or `exit_gain_usd` (exits). Sessions run 18:00–17:00 ET, so day = date(t + 6 h). |
| Benchmark: random walk / "zero-rate" (§2.1, footnote 8) | **Adapted** (default `benchmark="random_skip"`). The paper's no-information benchmark earns 0 in FX. For candidate trades the no-information selector is a random skip of the same fraction, which is also the SPEC's "random skip" and "random exit times" baselines. `benchmark="zero"` is the literal paper version; for exits it equals the hold baseline. |
| Romano et al. (2008) k-FWER StepM, one-sided, with Romano & Wolf (2010) balancing (§2.1) | Romano & Wolf (2010): one-sided studentized roots (Remark 3.2), prepivoting U = H_s(R*) (Remark 3.1, eq. 3.6), critical value from eq. 5.1, **streamlined stepdown Algorithm 4.2**. Resampling is from the data, not under the null (§5). Rejection rule: reject H_s if H_s(Z_s) > the (1−α) quantile of the k-th largest U over K. |
| k = 39 ≈ 0.5% of 7,846 (§2.1; footnote 5: top 5% of rules × 10% Type I) | k = max(1, round(0.005 × #rules)). That gives k = 4 for 780 rules. |
| α (significance level): **not stated** | **Fallback α = 0.10**: the FWE level of Romano & Wolf (2005)'s empirical application and simulations. |
| Bootstrap type, replications, block length: **not stated** (refers to Romano et al. 2008) | Circular block bootstrap, studentized in the bootstrap world by the "natural" block variance and in the real world by the matching Bartlett block-sum long-run variance. This is Romano & Wolf (2005)'s own empirical choice, after Götze & Künsch (1996); they used a QS-kernel HAC in the real world. Block length is the integer Politis & White (2004) / Patton et al. (2009) automatic choice, with constants checked against the `arch` package source. `bootstrap="sb"` gives the stationary bootstrap (Politis & Romano 1994) with plain-sd studentization. **B = max(1000, 20 × rules)**: Romano & Wolf (2005) say "J ≥ 1,000". It is raised because the balanced critical value has resolution 1/B: with S rules the max-U reaches 1 with probability ≈ 1−(1−1/B)^S, which needs B ≫ S/α (our derivation). |
| Combiners get the best 5/10/15 survivors by in-sample accuracy; RVM gets all survivors (§3.2) | Survivors ranked by IS accuracy, where accuracy = weighted share of candidates where "fires ⇔ win" (our classifier reading of their next-day-direction accuracy). Defaults: NB / SA / BNN use 15, the paper's best size (Table 6 portfolio averages: DMA(15) 6.25%, BNN(15) 6.09%, NB(15) 2.59%, SA ≈ 0). DMA / DMS / BMA use **10**, because 2^15 models × 16 forgetting pairs is impractical at our row count; the paper's footnote 9 also limits DMA for run time. RVM uses all survivors. Exact-duplicate firing columns are dropped (they would make the combiners singular). |
| NB on signals in {−1,0,1}, multinomial (§2.5, eq. 27-28) | Bernoulli/multinomial NB on the 0/1 rule indicators. **Laplace add-one smoothing is a fallback** (the paper states none). It is linear in log-odds. |
| RVM, Gaussian regression form, RBF kernel "mostly considered", updates α = γ/μ², σ² = ‖t−Φμ‖²/(T−Σγ) (§2.2, eq. 4-18) | Implemented exactly as those equations, with target y ∈ {0,1}. **Compute adaptation:** the basis is ≤300 distinct training input patterns (Tipping uses every training point), the evidence iterations run on ≤5,000 weighted-sampled rows, and the output is Platt-calibrated. **Fallbacks** (kernel width, initialisation and stopping are not given): RBF r² = median pairwise squared distance; initial α = 1, β = 1/var(t); prune at α > 1e9; tol 1e-3; ≤300 iterations. |
| DMA/DMS (§2.3, eq. 19-24; Raftery et al. 2010) with δ, λ ∈ {0.90, 0.95, 0.99, 1}; best chosen in-sample, with "IS … first 80%" (footnote 6) | All 2^N subsets, intercept always in. Raftery's forgetting R_t = C_{t−1}/λ (their eq. 5; the paper's eq. 24 prints the sign as (1−λ⁻¹), a typo). V_t uses Raftery's recursive moment estimator A_t. Model prediction is (π^δ + c)/Σ with **c = 0.001/K** (Raftery eq. 17). Prior per Raftery §4: θ₀ = 0, Σ₀ = diag(β̂₀² + Var y, Var y / Var x_j), β̂₀ from a static OLS on the training rows. **V₀ = Var y is a fallback.** The 16 (δ, λ) pairs are scored by one-step-ahead MSE over the **last 20% of training days**, with the first 80% as burn-in/IS. The paper scored by trading return; we use a proper score because the harness picks the decision threshold. |
| DMA time step = one daily FX observation | **Adapted:** one step = one session day. All candidates of a day update the state as one batch, so the forgetting half-lives stay in days (λ = 0.99 → 69 days) as in the paper. Sample weights act as precision weights. |
| DMA updates online through the OOS year | **Deviation:** the Scorer API gives no test labels, so test rows use the end-of-training state with one-step-ahead model probabilities, refitted every walk-forward fold. The DMA forecast averages linear models, so it is linear and its weights table is exact. |
| BNN (§2.4): Ticknor (2013) Bayesian regularisation, F = γ₁E_D + γ₂E_W, Levenberg–Marquardt, early stopping in IS | One tanh hidden layer with a linear output. Foresee & Hagan (1997) updates: γ = N_w − 2α tr(H⁻¹), α = γ/(2E_W), β = (n−γ)/(2E_D), starting from α = 0, β = 1. Early stopping on the last 20% of training time. **Fallbacks:** H = 5 hidden units, taken from a secondary summary of Ticknor (5 or 20) that was not verified against the paper. μ = 0.005, ×0.1 / ×10, μ_max = 1e10, 1,000 epochs and max_fail = 6 are MATLAB trainbr/trainlm defaults, not from the paper. Inputs map 0/1 → ±1. Compute caps: ≤20,000 fit rows and ≤5,000 validation rows. |
| SA = simple average of the best rules (benchmark, §4.2) | Raw score = share of the best 15 rules that fire. |

**Paper's findings, for calibration of expectations.** About 5-15% of rules survived (§4.1). Equal-weight survivors earned ≤1%/yr out of sample. DMA and BNN were best, NB was the weakest Bayesian combiner, and SA was about zero (Tables 3-6). The paper says "model averaging almost always works better than model selection". The thesis adds a Sharpe of 0.614 vs 0.2 and "up to four times" the profit. The journal abstract says "up to five times". All of this is daily FX at 3 bp per trade.

**Measured size of the screen** (our simulation, not a published number; k = 1, 40 rules, B = 1,000, 150-200 null panels, nominal α = 0.10):

| null panel | measured FWER |
|---|---|
| iid days | 0.08–0.115 |
| AR(1) φ = 0.3 days, T = 500 | 0.18 (stationary bootstrap: 0.20) |
| AR(1) φ = 0.3 days, T = 2,500 | 0.15 |
| AR(1) φ = 0.6 days, T = 500 | 0.19 (stationary bootstrap: 0.245) |

Block bootstraps are known to over-reject in finite samples under dependence. The published remedy is Romano & Wolf (2005) Algorithm 6.1 (calibrated block size), which is **not implemented** because of compute. The chosen block is stored in `block_`: if it is near 1 on real data, the days are close to independent and the size is close to nominal.

**Diagnostics kept on every fitted screen scorer:**
- `screen_`: every rule with t-stat, marginal p, survivor flag, accuracy, firing share and $ lift per trade;
- `survivors_`, `selected_`, `k_`, `B_`, `block_`, `T_days_`;
- DMA: `combo_`, `grid_mse_`, `pi_`, `inclusion_`.

Zero survivors means the scorer returns the training base rate (AUC exactly 0.5) and a one-row table that says so. That is a legitimate result.

## 2. `stat_nb_woe`: naive Bayes as a weight-of-evidence sum

Good (1950), *Probability and the Weighing of Evidence*; Spiegelhalter & Knill-Jones (1984), *JRSS A* 147:35-77. For every feature bin, WoE = ln(P(bin|y=1)/P(bin|y=0)), with Laplace add-one smoothing per class. Raw score = ln(prior odds) + Σ WoE (the task's definition).

**Fallback choices:**
- Features with ≤5 distinct values are categorical.
- Other features are cut at the training deciles.
- NaN gets its own class; a missing class never seen in training gets WoE 0.

`score()` applies one Platt factor a (one global shrinkage of all WoEs, fitted on the training rows) because the independence assumption double-counts correlated signals. Spiegelhalter & Knill-Jones correct the WoEs per variable by logistic regression; we only use the single-factor version. The table lists the raw WoE and the calibrated weight for every bin.

## 3. `stat_woe_scorecard`: credit-risk scorecard

Siddiqi (2006), *Credit Risk Scorecards*, Wiley; Anderson (2007), *The Credit Scoring Toolkit*, OUP. **Neither book was accessed directly.** Here "good" means y = 1 (a winning trade, or exiting beats holding).

| step | choice | provenance |
|---|---|---|
| Fine classing | 20 equal-frequency classes (continuous); one class per value (≤5-valued flags); missing values get their own class | 20 = the common "5% fine classes" practice, **unverified fallback**. Not merging rare pattern flags is **our choice**, so rare patterns are not pooled away. |
| Coarse classing | merge adjacent classes until the event rate is monotone (pool-adjacent-violators in the direction of its rank trend), then merge any class under **5%** of rows into its closer-rate neighbour | Siddiqi's "logical trend", read as monotone; the 5% minimum is an **unverified fallback** |
| WoE / IV | WoE = ln(%good/%bad) (Laplace add-one); IV = Σ(%good−%bad)·WoE | standard |
| IV filter | keep IV ≥ **0.02**; bands are <0.02 unpredictive, 0.02–0.1 weak, 0.1–0.3 medium, ≥0.3 strong | Siddiqi (2006) as quoted by du Pisanie, Allison & Visagie (2023), arXiv 2303.01227 (**verified secondary**) |
| Model | logistic regression on WoE codes, C = 1e6 (practically unpenalised). Features whose coefficient comes out negative are dropped and the model refitted (sign reversal = collinearity). Fits on ≤400k sampled rows. | negative-coefficient removal is **common practice, unverified against the books** |
| Points | points = (PDO/ln 2) × coef × WoE with **PDO = 20**; offset 0 (the intercept row carries the base points) | Score = Offset + Factor·ln(odds), Factor = PDO/ln 2, attributed to Siddiqi by secondary sources; PDO 20 is the scorer_api convention |

`iv_table_` lists every feature's IV, and `dropped_negative_` lists the sign-reversed features that were removed.

## 4. `stat_shrink_combo`: forecast combination shrunk toward equal weights

- **Diebold & Pauly (1990)**, *IJF* 6:503-508. Only the RePEc abstract was read: weights are shrunk toward equality by Bayesian (g-prior) estimation, LS and equal weights are the polar cases, and in their GNP example "a large amount of shrinkage" was optimal.
- The posterior-mean form β₁ = β₀ + δ(β̂_OLS − β₀), δ ∈ [0,1], is taken from **Diebold & Shin (2019)** (*IJF* 35; PIER WP 17-017, §4), read in full.
- **Smith & Wallis (2009)** and **Claeskens, Magnus, Vasnev & Wang (2016)** (the forecast-combination puzzle) are cited as motivation only.
- A Stock & Watson (2004) κ-shrinkage formula could **not** be verified, so it is not used.

How it works:
1. Families: the SPEC groups (reversal, continuation, breakout, closeloc, exhaustion, neutral patterns, swing_5, swing_10, trend, momentum, vwap, bar, day, time, htf, cross_market, trade_state for exits, other). Each family's own forecast is an L2 logistic regression on its standardised columns. C = 1.0 is the sklearn default (fallback). NaN → 0 for signed columns, median otherwise. Fits use ≤300k rows.
2. Combination is in log-odds space: s = Σ_k w_k (logit f_k − logit ȳ), then Platt. Combination weights come from a logistic regression ("OLS") on **out-of-sample** family forecasts and are shrunk toward 1/K.
3. δ is chosen on an inner, purged, expanding time split of the training rows. The split is the last two training years (B, C) when there are ≥4 years, as in the SPEC's inner split; otherwise time quantiles 60/80% (fallback). Family models fit on A forecast B, and weights are estimated on B. For each δ, family models fit on A+B forecast C and the out-of-sample log loss on C is scored. The grid is δ ∈ {0, 0.1, …, 1} (fallback). Training rows whose `t_end` reaches the next block are purged.
4. Final model: family models are refitted on all training rows, the weights are re-estimated on the stacked out-of-sample forecasts of B and C, and then shrunk with the chosen δ.

`delta_curve_` records the inner-split log loss for every δ. Per-signal weight = Platt slope × w_k × family coefficient. The table also has one `family:<name>` row per family.

## Tests (`test_approach_stat.py`, about 6 s)

Synthetic candidates with SPEC column names: 320 session days × 22 candidates; train on the first 70% of days, test on the rest. Planted entry signal: logit = −0.3 + 1.2·[pat_engulfing=+1] + 0.7·ema_stack + 0.5·dist_vwap. Planted exit signal: −0.9·ema_stack (with-trade trend means don't exit) + 0.8·[open_R>1] − 0.4·dist_vwap.

Out-of-sample AUC:

| scorer | entry planted | entry noise | exit planted |
|---|---|---|---|
| nb_woe | 0.693 | 0.515 | 0.722 |
| screen_bma | 0.696 | 0.500 | 0.703 |
| screen_bnn | 0.700 | 0.500 | 0.702 |
| screen_dma | 0.695 | 0.500 | 0.703 |
| screen_dms | 0.690 | 0.500 | 0.701 |
| screen_nb | 0.690 | 0.500 | 0.690 |
| screen_rvm | 0.696 | 0.500 | 0.700 |
| screen_sa | 0.678 | 0.500 | 0.646 |
| shrink_combo | 0.694 | 0.488 | 0.728 |
| woe_scorecard | 0.707 | 0.500 | 0.735 |

**Also checked:**
- The screen keeps the planted rules (`pat_engulfing = +1`, `ema_stack = +1`, the dist_vwap thresholds) and keeps 0 of 50 rules on noise.
- The scorecard IV filter keeps ema_stack (0.29), pat_engulfing (0.18), dist_vwap (0.15) and fam_reversal (0.08), and keeps nothing on noise.
- Linear tables reproduce `score()`.
- Planted signs are right: exit `ema_stack` weight < 0, and `ema_stack = -1` survives the exit screen.
- Points = weight/(ln 2/20).
- Probabilities are in [0, 1].
- `fit()` does not modify X.
- The k-StepM rejects 3 planted columns among 57 nulls, and its null FWER over 40 runs is 0.05.

## Scale (synthetic, 1,001,000 training rows × 150 columns, 2,600 days)

| scorer | fit time |
|---|---|
| nb_woe | 7.9 s |
| first screen scorer (screen computed: 780 rules, k = 4, B = 15,600) | 23 s |
| other screen scorers (screen cached) | 0.3–4.9 s |
| shrink_combo | 8.7 s |
| scorecard | 8.2 s |

Peak RSS was 3.3 GB. DMA with the full 10 inputs takes about 20 ms per day (16,384 Kalman filters), so roughly 1–1.5 minutes at 2,600–4,000 days.

The screen and the DMA recursion are cached by a fingerprint of the training rows: y, w, time and payoff are hashed fully, and X through a 10k-row strided sample plus its shape and column names. So the 7 screen scorers, and DMA with DMS, share one computation per fold. The cache is never reused across different data.

## Caveats

- The paper is daily FX, three currency pairs, 2010-2016, with 3 bp costs. Our rules are candidate filters on intraday futures. The screen's per-day aggregation, the random-skip benchmark, the session-day DMA step, the classifier-accuracy ranking, and the end-of-training DMA state (the API gives no test labels) are our adaptations.
- Real data is likely to yield few or no survivors. The research summary (Marshall et al., Duvinage et al.) expects most candle rules to fail data-snooping tests. A screen scorer with 0 survivors is the honest output, not a bug.
- Numbers that are **not** from a verified source are labelled in the code as fallbacks:
  - α = 0.10;
  - B and the block rule;
  - quintile thresholds;
  - Laplace smoothing;
  - RVM width and initialisation;
  - BNN H = 5 and the MATLAB defaults;
  - V₀;
  - decile / 20-bin / 5% binning;
  - negative-coefficient removal;
  - the δ grid and the 60/80% split;
  - sklearn C values;
  - row caps.
