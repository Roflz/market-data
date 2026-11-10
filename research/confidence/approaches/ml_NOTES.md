# ML confidence scorers (approach_ml.py)

Published machine-learning scorers for the confidence study, plus machine learning that **starts from a prior**: your
idea of starting training from the hand-set or statistical weights. Every class follows `scorer_api.Scorer`, is
registered in `scorer_api.REGISTRY`, and runs for `task="entry"` and `task="exit"`.

Files: `approach_ml.py` (module), `test_approach_ml.py` (21 tests, about 15 s), this note.

| name | what it is | primary source |
|---|---|---|
| `ml_logit_l2` | StandardScaler + L2 logistic regression; C picked on an inner time split | SPEC.md walk-forward `logit` (reference model) |
| `ml_afml_rf` | meta-labeling random forest with uniqueness weights, isotonic calibration and `bet_size(p)` | López de Prado, *Advances in Financial Machine Learning* (AFML), ch. 3, 4, 6, 10; Meyer, Barziy & Joubert (2023) |
| `ml_creamer_boost` | alternating decision tree (ADT) grown by LogitBoost; rounds picked on a later validation block | Creamer & Freund (QF 2010); Creamer (2007 thesis); Creamer (QF 2012); Freund & Mason (1999) |
| `ml_creamer_experts` | the same ADTs as "experts" on moving 2-year windows, combined by the Creamer & Freund expert-weighting layer | Creamer (2007 thesis) ch. 6, which is the QF 2010 study |
| `prior_logit_offset` | logistic regression with offset = the prior's log-odds; learns only corrections | GLM offset; Gelman et al. (2008) prior and scaling |
| `prior_logit_shrink` | logistic regression whose Gaussian prior is centred on the prior's own per-feature weights | Gelman et al. (2008) sec. 3.1, "informative prior N(mu_j, sigma_j^2)" |
| `prior_gbm` | `GradientBoostingClassifier(init=<fitted prior>)`: boosting starts from the prior's log-odds | Friedman (2001/2002); SPEC.md gbm settings; Ridgeway's gbm guide |

How sure each source fact is: **[V]** means I read it in the source (or a verbatim quote of it) during this session.
**[R]** means I recalled it from the book and could *not* re-open the text online. **[F]** marks a fallback or choice of
ours with no published number behind it.

---

## Conventions shared by every scorer

* **No look-ahead.** `fit()` sees only the rows it is given. Every hyper-parameter and every calibration map is chosen
  on an **inner time split** of those rows, and then the model is refit on all of them (`inner_split`).
  - With 4 or more training years, the last 2 years validate (SPEC.md: "C chosen by an inner time-split (last 2
    training years)"). With 2-3 years the last year validates. Otherwise the last 25% of rows by `t` do.
  - Inner-training rows whose label ends (`t_end`) at or after the first validation timestamp are **purged**
    (AFML ch. 7 purging; SPEC walk-forward purge).
* **Missing values (NaN).**
  - Linear models impute with the training median.
  - `RandomForestClassifier` uses scikit-learn's native NaN support.
  - The ADT lets missing values **abstain**: a rule on that feature adds nothing and the row does not descend.
  - `GradientBoostingClassifier` rejects NaN, so NaN is coded as -1e9 ("very low"). The prior wrapper turns it back
    into NaN before it calls the prior, so the prior always sees the real NaNs.
* **score() vs predict_proba().**
  - `score()` is log-odds-like: the linear predictor, logit(raw forest probability), or the Platt-scaled boosting
    score. A downstream prior or offset can use it.
  - `predict_proba()` is the calibrated P(y=1).
* **weights_table()** always has the columns `signal, weight, points, meaning, source`.
  - Linear models: `weight` is log-odds per raw unit, and `points = weight / (ln 2 / 20)`.
  - Tree ensembles: feature importances, and `meaning` says plainly that these are **not** log-odds weights.
  - ADT: one row per rule (precondition & condition), in log-odds via the Platt slope.
* **Exits.** Nothing changes except the extra trade-state columns. The tests check that the logit learns a
  **negative** weight on with-trade `ema_stack` for exits, i.e. it treats it as evidence to stay in.

---

## 1. `ml_afml_rf`: López de Prado meta-labeling forest

| design choice | value | source |
|---|---|---|
| Role of the model | the textbook rule sets the side, and the model decides act or pass and the size | AFML ch. 3.6 "Meta-labeling", p. 50 **[V]**, quoted verbatim in Singh & Joubert, *Does Meta-Labeling Add to Signal Efficacy?* App. B.0.1: "use the probability of this secondary prediction to derive the size of the bet". |
| Sample weights | `w` from the harness (uniqueness x cross-market) | AFML ch. 4: uniqueness, i.e. counting concurrent labels and averaging 1/c over each label's life **[V]** (Martin's AFML notes; doda's AFML notebook reproduces snippets 4.3-4.4). |
| Bootstrap size | `max_samples = average uniqueness (avgU)` of the training labels | AFML ch. 4/6: "bag with max_samples set at the average uniqueness" and "reimplement random forest to bag decision trees with max_samples equal to the average uniqueness" **[V]** (Martin's notes). avgU comes from `label_uniqueness(meta)`; see adaptation (a). |
| Sequential bootstrap | written (`sequential_bootstrap`), and usable with `bootstrap="sequential"` | AFML ch. 4.5, snippets 4.5-4.6 **[V concept]**. It is O(n^2), so the default is the documented avgU approximation, and the sequential option draws each tree from at most `seq_max_rows=3000` labels **[F]**. |
| Forest settings | `n_estimators=1000, criterion='entropy', class_weight='balanced_subsample'` | AFML Snippet 6.2 ("three ways of setting up an RF") **[R]**. I could not open ch. 6 online; the TOC confirms 6.4 "Random Forest" on p. 98 **[V]**. |
| Features per split | `max_features='sqrt'` (about 12 of 150) | AFML 6.4 says to *lower* `max_features` so the trees differ ("reducing the number of features available to each tree" **[V]**, notes). The book gives no number. Snippet 6.2 uses `'auto'`, which is sqrt for classifiers **[R]**. |
| Early stopping | `min_weight_fraction_leaf=0.05` | AFML 6.4: set it high enough "(e.g., 5%)" that out-of-bag accuracy converges to k-fold accuracy **[R]**. The early-stopping remedy itself is **[V]** (notes). |
| Time decay | `time_decay=1.0` (off); supports AFML's piecewise-linear decay on cumulative uniqueness | AFML ch. 4 snippet 4.11 `getTimeDecay` **[V]** (doda's notebook reproduces the code). |
| Return attribution | `return_attribution=False`; when on, weights are multiplied by abs(net $) | AFML ch. 4: "weight should be a function of uniqueness and the size of the returns" **[V]** (notes). See adaptation (b). |
| Calibration | isotonic, fitted on the inner validation block; the final forest is refit on all rows | Meyer, Barziy & Joubert (2023), "Meta-Labeling: Calibration and Position Sizing", JFDS 5(2), abstract: "the performance of fixed position sizing methods is significantly improved by calibration" **[V]**. Their code uses `CalibratedClassifierCV(method='isotonic')` **[V]**. Calibration is mandatory here anyway, because `balanced_subsample` skews raw probabilities toward 0.5. |
| Bet size | `bet_size(p) = 2*Phi(z) - 1`, `z = (p - 1/2) / sqrt(p (1-p))`, clipped at 0 (pass); `step` discretises | AFML ch. 10.3, snippet 10.1 `getSignal` **[V]** (doda's notebook code; H&T `de_prado_bet_size`). Snippet 10.3 `discreteSignal` gives the step rounding **[R]**. |
| Importances | MDI: mean over trees, standard error = std/sqrt(trees); a Spearman sign is added | AFML snippet 8.2 **[R]**. The sign column is ours **[F]**, and it only helps you read the table. |

**Adaptations, and why.**
* **(a) Uniqueness in clock time.** The book counts concurrency per **bar**. We have candidate events with
  `[t, t_end]` but no bar grid inside the scorer, so concurrency is integrated over clock time, per market. For
  intraday labels the two agree closely. The harness's own `w` is still used as the sample weight; our avgU only sets
  the bootstrap size.
* **(b) Return attribution uses net $.** AFML attributes bar log-returns. We use the labelled trade's net $
  (`pnl_usd` / `exit_gain_usd`). It is off by default because the harness already supplies the weights.
* **(c) No up-sampling.** Singh & Joubert up-sampled the minority class **[V]**. We do not, because resampling distorts
  probabilities (CONFIDENCE_RESEARCH.md pitfall 4). AFML's `balanced_subsample` plus calibration does the same job.
* **(d) Calibration on a time block.** The H&T code calibrates with shuffled 5-fold CV. We use the later time block,
  because overlapping labels make shuffled CV leak (AFML ch. 7).
* **(f) scikit-learn 1.9 bootstrap semantics.** In sklearn 1.9 a *float* `max_samples` is a fraction of
  `sample_weight.sum()`, not of n, and rows are drawn with probability proportional to `sample_weight` (each tree
  is then fit on the draw counts x `balanced_subsample` class weights). Passing `max_samples=avgU` as a float with
  uniqueness weights (mean about avgU) would draw only avgU^2 x n rows. So the forest gets an **integer**
  `max_samples = round(avgU x n)` (AFML's bag size), and the harness weights act through weighted sampling, which
  is AFML's intent for bagging overlapping labels. Tested (`test_afml_rf_bag_size_is_avgU_times_n`).
* **(e) Exits.** Exit rows of one trade overlap heavily, so avgU is small and each tree sees few rows. A floor of
  `min_tree_rows=200` stops tiny trees **[F]**.

---

## 2. `ml_creamer_boost` and `ml_creamer_experts`: Creamer & Freund boosting

**What the sources say [V]**: I read the working paper "A boosting approach for automated trading" and the Columbia
tech report of Creamer's 2007 thesis (ch. 6 is the QF 2010 study), plus Creamer (2012). The QF 2010 full text is
paywalled; I read only its abstract.

* **Base learner.** An ADT (Freund & Mason 1999) grown by LogitBoost.
  - Thesis fig. 2.2 / working-paper fig. 1: weights `w_i = 1/(1 + e^{y_i F(x_i)})` and rule value
    `alpha = 1/2 ln(sum w over y=+1 / sum w over y=-1)`.
  - Implemented exactly in numpy (`ADTLogitBoost`). Each round adds one splitter to any prediction node; the split
    criterion is Freund & Mason's `Z = 2(sqrt(W+W-)_c1&c2 + sqrt(W+W-)_c1&~c2) + W(~c1)`.
* **Number of rounds.**
  - Thesis ch. 7: "we used a validation set to select a number of iterations" (p. 130-131).
  - Creamer (2012) sec. 6.1, intraday FESX/FDAX futures: "run with 20 iterations".
  - Other studies in the thesis used 10, 50 and 300 iterations.
  - So: at most 20 rounds (`max_rounds=20`), with the best count chosen on the later validation block by
    Platt-calibrated log loss. The QF 2010 round count is **not published in anything I could read**.
* **Training window.** The working paper uses the last 90 days. Thesis sec. 6.3 uses a "moving window of two years"
  with a new expert every 50 trading days, 11 experts in total, and C in {0, 0.05, ..., 50}. Thesis sec. 6.4:
  results are insensitive to C except above 10, so C = 1 is the setting shown. The weak-signal threshold is
  gamma0 = 0.20 and gamma1 = 0. Creamer (2012) used a maximum of 25 experts with gamma0 = 0.20 and gamma1 = 0.
* **Expert weighting** (thesis sec. 6.2.2.1, fig. 6.2):
  - cart_i = sum of sign(S_i) x r since expert i's training end.
  - First expert: `exp(C cart/sqrt(t))`.
  - Later experts: `I_i x ramp(t - t_i) x exp(C cart_i/sqrt(t - t_i))`, where I_i is the mean weight of the earlier
    experts when expert i is added, and the ramp is `min((t - t_i)/(t_{i+1} - t_i), 1)`.
  - The "simple" and "none" time-adjustment versions are also available.
  - Signal `W = L - S`, which lies in [-1, 1].
* **Their own caveats.**
  - Working paper: test error **48.8%** over an 840-day simulation.
  - Conclusion: "a simple and straightforward application of boosting to financial time series does not bring a
    significant improvement in forecasting", and logistic regression performs similarly.

**Adaptations, and why.**
* **Implemented in numpy, not sklearn.** The suggested stand-in, `GradientBoostingClassifier(loss='log_loss',
  max_depth=1)`, is boosted stumps with Newton leaf values. That is equivalent to LogitBoost (Friedman, Hastie &
  Tibshirani 2000) but **not** an ADT: it cannot grow rules under earlier rules, and it uses gradient-fit splits
  instead of the Z criterion. Writing the ADT directly closes that gap, and the weights table then lists Creamer's
  readable rules.
* **ADT rule variant.** The thesis says a splitter attaches to a prediction node "unless it already has a splitter
  node attached". Freund & Mason's original allows several. The default follows Freund & Mason;
  `single_splitter=True` follows Creamer's wording.
* **Thresholds are binned.** Candidates are training quantiles, at most 32 per feature, or the midpoints between
  distinct values when a feature has 32 or fewer values, so rare pattern flags stay splittable **[F]**. Purpose: speed.
* **Smoothing.** `eps` = 0.5 x the current mean example weight. Schapire & Singer (1999) smooth with a small eps of
  order 1/m; the exact constant used in MLJAVA/JBoost is unpublished **[F]**.
* **Inputs and labels.**
  - Inputs: our feature set (patterns, structure, EMA, momentum, VWAP, time, cross-market) instead of Creamer's TA list
    (SMA, ADX, Bollinger, MACD, RSI, stochastics, MFI, ...). Both are technical-indicator inputs.
  - Labels: our net-of-cost meta-labels instead of "price up by more than tau". tau covered costs, so the two are
    equivalent in spirit.
  - Weights: instances are weighted by the harness `w`, not by the Sharpe ratio (thesis 6.2.1).
* **Expert schedule.**
  - Ends at `t_end_train - j x 3 months` for j = 1..11; each expert trains on the 2 years before its end, purged, and
    is subsampled to 50k rows. This mirrors the 50-trading-day spacing **[F: 3 months]**.
  - The newest expert ends 3 months before the training end, so its weight has a ramp and track record. In their
    online scheme a just-trained expert has weight 0 until it ramps up.
  - r is the labelled trade's net $ standardised (thesis: beta-abnormal return). The "time" in sqrt(t - t_i) is the
    count of resolved outcomes, because our events are irregular.
* **Main gap: no online re-weighting.** Creamer re-weights the experts **every day** of the test period. The
  `fit/score` interface has no outcome feedback during a test year, so the weights are **frozen at the end of
  training**, and the harness refits yearly. If this approach looks promising, the closest fix is a harness that
  refits monthly.
* **Calibration and risk layer.**
  - W is Platt-calibrated on the last training year, with weights frozen at its start, the same way they are frozen
    for the test year.
  - Layer 3 (gamma0 = 0.20) is exposed as `trade_signal(X)`.
  - The gamma1 drawdown rule is not implemented: it needs the live P&L path, which the harness owns.

---

## 3. Prior-informed ML: starting from the hand or statistical weights

No single published paper does exactly this. Each piece rests on standard practice:

* **Gelman, Jakulin, Pittau & Su (2008)**, Ann. Appl. Stat. 2(4), arXiv:0901.4011 **[V]** (PDF text read).
  - Sec. 2.1: binary inputs are centred and differ by 1; other inputs get mean 0 and SD 0.5.
  - Sec. 2.2: default Cauchy(0, 2.5) on the coefficients and Cauchy(0, 10) on the intercept; the normal is the t
    family with infinite degrees of freedom.
  - Sec. 3.1: "the simplest informative prior distribution assigns normal prior distributions" beta_j ~ N(mu_j, sigma_j^2).
  - Sec. 5: on their corpus the Cauchy outperforms the normal on average.
* **Offset.** A fixed-coefficient term in a GLM linear predictor (standard GLM practice; I did not re-open McCullagh &
  Nelder in this session).
* **Stacking with cross-fitted level-one predictions.** Wolpert 1992 and Breiman 1996, cited from memory and not
  re-opened. This is the optional `crossfit=k`.

**How the prior is used.**
* Pass the prior by name: `REGISTRY["prior_logit_offset"](task, prior="hand_bulkowski", prior_params={...})`.
* It is built from `REGISTRY`. `approach_hand` and `approach_stat` are imported on demand.
* It is **fit inside fit()**: on the inner-training rows to select s, then on all training rows for the final model.

| scorer | model | strength / settings |
|---|---|---|
| `prior_logit_offset` | `logit p = prior_logodds(x) + b0 + Z(x) beta`, with beta ~ N(0, s^2) on Gelman-scaled Z. `prior_logodds` = logit of the prior's **calibrated** probability (`offset_source="score"` uses raw `score()`). | s is picked from {0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5} on the inner split **[F grid; 2.5 = Gelman default]**. As s -> 0 the model returns the prior plus an intercept shift (tested). `prior_dist="cauchy"` gives Gelman's default family. `crossfit=k` computes the training offset out-of-fold in k time blocks, which avoids an over-trusted in-sample prior. |
| `prior_logit_shrink` | beta_j ~ N(mu_j, s^2), where mu_j are the prior's log-odds weights per Gelman-scaled unit | mu_j comes from, in order: (1) `prior.linear_weights()`; (2) `weights_table()` rows whose `signal` is a column, accepted when `score()` correlates >= 0.98 with them, then times the slope of the prior's calibrated log-odds on its score; (3) otherwise a least-squares projection of the prior's log-odds on the features (R^2 reported in `mu_how_`). The same s grid applies. As s -> 0 the model returns the prior (tested). |
| `prior_gbm` | `GradientBoostingClassifier(loss='log_loss', init=_PriorInit(prior))`, so the first raw prediction is the prior's log-odds | Depth 3, learning_rate 0.05, at most 300 trees, min_samples_leaf 500 (SPEC.md gbm); subsample 0.5 (Ridgeway's gbm guide: "0.5 is recommended", citing Friedman 2002 **[V]**; depth "~2-5 will suffice" **[V]**). The number of trees is picked on the inner split, by the guide's holdout method in time order. **0 trees allowed**, which keeps the prior. Isotonic calibration on that split (SPEC.md gbm). |

**Gaps.**
* SPEC's gbm uses `HistGradientBoosting(l2_regularization=1)`, but HistGB has no `init`, so `prior_gbm` uses the
  exact `GradientBoostingClassifier`. It has no L2 term and is slower, so `max_rows=100k` subsamples **[F]**.
* The intercept is unpenalised. Gelman uses Cauchy(0, 10), which barely matters at our sample sizes.
* Sample weights enter the likelihood as given. The prior's strength is therefore relative to sum(w), the effective
  sample size, which is how it should be with uniqueness weights.

---

## 4. Practicality at integration size

Measured on synthetic data with 150 columns, 15 years, and roughly 186k training rows from n = 200k, on this
12-core machine. These are fit times, including the inner-split refit:

RUNTIME_TABLE

Defaults that cap cost: ADT `max_rows=100k` and 20 rounds; experts 11 x 50k rows; `prior_gbm` `max_rows=100k`. These
are documented subsamples (uniform without replacement, weights kept). The linear models and the forest use all rows.

---

## 5. Things to watch when comparing

* Every scorer here reaches out-of-sample AUC of about 0.73-0.75 on the planted synthetic signal (the logit optimum
  is about 0.75). On pure noise all stay within 0.49-0.52. That shows the machinery works; it is not evidence of an
  edge in real data.
* Creamer & Freund's own results were weak: 48.8% test error, and logistic regression did about as well. AFML's
  settings were written for daily bars and dollar bars. Treat `ml_logit_l2` and the vote as the baselines to beat.
* For the prior scorers, `val_loss_` stores the inner-validation log loss of **the prior alone** next to each
  strength s. If the chosen s is the smallest one, the data did not improve on your prior.
