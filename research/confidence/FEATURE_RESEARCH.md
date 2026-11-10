# Which features should the trade-scoring model use? What the research says

*For: MES/MNQ/MYM micro futures, 1-minute data from 2010 to 2026 built into 5/15/60-minute bars. A model scores candlestick and pullback setups by the chance they make money after $2–3.50 in costs.*

**Units used below**
- **"Average bars" (avg bars):** a move or distance divided by the average bar range, which is how v1 already scales distances.
- **z-score:** how many standard deviations a value is from its recent average.
- **R²:** the share of the up-and-down movement a model or line explains. 0% means it explains nothing; 100% means it explains everything.
- **IC:** the correlation between a forecast and what actually happened.
- **"Out of sample":** results on years the model never saw while it was being built.

---

## 1. Short answer

**Research has not established which features work for your exact setup.** No published, out-of-sample study ranks features for scoring candle or pullback entries on intraday index futures using only OHLCV bars. Most of the large studies cover stocks on daily or monthly bars, ranked against each other. Many ignore costs or only partly include them.

Still, the studies agree on more than you might expect. The same families come up again and again:

1. **Recent returns over a few lookbacks come first everywhere.** The shortest lookbacks (the last 1–5 bars) usually carry the most information, and the effect is often *reversal*, not momentum.
   - Gu, Kelly & Xiu, RFS 2020: https://dachxiu.chicagobooth.edu/download/ML.pdf
   - Krauss, Do & Huck, EJOR 2017: https://www.econstor.eu/bitstream/10419/130166/1/856307327.pdf
2. **Volatility and volume/liquidity come next.** They matter mostly as *conditions*: when patterns work and when they don't.
3. **How you scale prices matters as much as which features you pick.** The strongest chart-pattern study found that putting the last few bars' open/high/low/close inside the recent high-low range (0 = range low, 1 = range high) captured most of what a deep image model learned.
   - Jiang, Kelly & Xiu, J. Finance 2023: https://doi.org/10.1111/jofi.13268
4. **For index futures specifically, the best-documented intraday effect is "time of day × return so far today".** The return from yesterday's close to 30 minutes before today's close predicts the final half hour.
   - Baltussen et al., JFE 2021: https://academicweb.nd.edu/~zda/intramom.pdf
5. **Expect small edges.**
   - Careful benchmarks find forecast-vs-outcome correlations of about 0.04–0.05 (Qlib: https://github.com/microsoft/qlib/blob/main/examples/benchmarks/README.md).
   - Intraday studies find R² of about 1–3%.
   - The study closest to your data (MNQ, 5-minute OHLCV, 2021–2025) found **no** significant edge in predicting direction, and its feature rankings changed from one test period to the next (https://arxiv.org/abs/2605.17724).
   - Your design only scores setups the patterns already propose. That is a narrower, better-posed problem, but it sets realistic expectations.

Practitioners say features matter more than model choice. The G-Research minute-bar crypto competition is one example: https://www.gresearch.com/news/wrapping-up-the-g-research-crypto-forecasting-competition/. But recent research gives no feature list you can copy. **You have to test feature groups yourself, inside your walk-forward, after costs.**

---

## 2. Feature families ranked by evidence for our setup

The ranking weighs three things: how strong the evidence is, how close it is to our setup (OHLCV only, intraday index futures, scoring entries), and how cheap the family is to add.

### 2.1 Multi-horizon returns and short-term reversal: **strong evidence, partly in v1**
- **What it is:** how far price moved over the last N bars.
- **How to compute at bar close:** `ret_N = (Close_t − Close_{t−N}) / avg bar range`, for N = 1, 2, 3, 5, 10, 20, 60. A volatility-scaled version divides by the average range × √N.
- **Evidence:**
  - Krauss et al. (S&P 500 stocks, daily): the last 1–5 returns mattered most to the tree models, there was a sharp drop after lag 4, and 10–20-day returns mattered least. After costs, every model *lost* money in 2010–2015.
  - Fischer & Krauss (https://iwf.rw.fau.de/files/2015/12/11-2017.pdf): a deep network given raw returns mostly rediscovered "5-day reversal in high-volatility stocks."
  - Crypto minute bars (https://www.mdpi.com/1911-8074/12/1/31): the last 20–60 minutes of returns mattered most, and the logistic regression signs were mostly *reversal*.
  - Gu, Kelly & Xiu: 5 of the 7 top predictors were price-trend or reversal variables.
- **Caveats:** these are mostly stocks ranked against each other on daily bars. Effects have faded since about 2010. The direction (momentum or reversal) may differ for index futures, so let the model learn the sign.
- **In v1?** Only partly: Momentum(14), day return, and same-bar ES/NQ/YM returns. **No sparse ladder of short lookbacks.**

### 2.2 Position in the recent range and "bars since the high/low": **strong evidence (by analogy), partly in v1**
- **What it is:** where the close sits between the lowest low and highest high of the last N bars, and how long ago that high or low happened.
- **How to compute:**
  - `RSV_N = (C − lowest low_N) / (highest high_N − lowest low_N)`
  - `bars_since_high_N / N` and `bars_since_low_N / N`
  - Both at N = 5, 20, 60.
- **Evidence:**
  - Jiang, Kelly & Xiu put each window on a 0–1 range scale. A plain logistic regression on those rescaled last bars got a weekly Sharpe of 5.56, against 7.15 for the image model and 2.50 for the same regression on raw cumulative returns. The latest bar's close, high and low dominated; bars 2–5 back added little. Closing near the low of the recent range predicted *higher* returns, which is reversal.
  - Qlib's Alpha158 library includes RSV and bars-since-high/low (IMAX/IMIN): https://github.com/microsoft/qlib/blob/main/qlib/contrib/data/loader.py
- **Caveats:** daily stocks, before costs, stocks ranked against each other.
- **In v1?** Partly: close location within the bar, and Fib position within the current swing. **No multi-window range position and no bars-since-extreme.**

### 2.3 Volatility level and change, including OHLC estimators: **moderate evidence, mostly missing from v1**
- **What it is:** how much the market is moving now compared with normal.
- **How to compute (rolling averages of each bar's value):**
  - Parkinson = (ln H/L)² / (4 ln 2)
  - Garman-Klass = 0.5(ln H/L)² − (2 ln 2 − 1)(ln C/O)²
  - Rogers-Satchell is robust to trend.
  - Yang-Zhang handles the session open and overnight gap.
- **Evidence:**
  - Range-based estimators are several times more precise than close-to-close. Molnar names Garman-Klass the best: https://ideas.repec.org/a/eee/finana/v23y2012icp20-29.html
  - Intraday index predictability is concentrated in high-volatility, high-volume days and crises (Gao et al. https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414 ; Huddleston et al. https://ideas.repec.org/a/oup/jfinec/v21y2023i2p485-527..html).
  - In Easley, López de Prado et al. (87 futures), the change in volatility was the *most* predictable target: https://conference.nber.org/conf_papers/f117415.pdf
- **Caveats:** no study shows these estimators improve trade-outcome models. The 0.25-point tick distorts estimates on small 5-minute MES bars, so prefer windows of 20+ bars.
- **In v1?** Only indirectly: average bar range is the normalizer, plus bar size and day range. **No volatility-regime features such as short vs long ratios.**
- **Worth adding for a cost-aware model:** *your cost measured in average bars* = $cost / ($ per point × average bar range in points). The same $3.50 is a much bigger hurdle in a quiet market. This one is my suggestion; the sources don't test it.

### 2.4 Time of day and intraday momentum: **strongest evidence that is specific to index futures, partly in v1**
- **What it is:** the day's return so far, which matters especially near the close.
- **How to compute:**
  - Return from the prior RTH close to now, in avg bars.
  - That return split into the overnight gap and the move since the RTH open.
  - The prior day's last-30-minute return.
  - Minutes until the RTH close.
- **Evidence:**
  - Baltussen et al. (60+ futures, 1974–2020): "prior close → 30 minutes before close" predicts the last half hour. Equity futures out-of-sample R² was **+2.88%**, Sharpe about 1.7 *before costs*. In that broader sample the popular first-half-hour signal **failed out of sample (R² −1.71%)**. Yesterday's last half hour negatively predicts today's.
  - Gao et al. (SPY 1993–2013): out-of-sample R² was 1.2–1.8%, and much stronger in high-volatility periods and crises.
- **Caveats:** this is a last-30-minutes effect. The gross edge is about 2.7 basis points per trade (my rough arithmetic), and micro costs of about 0.7–1.3 basis points eat much of it.
- **In v1?** Time of day, day return and gap are in. **The specific "return so far × last hour" interaction and the prior day's last 30 minutes are missing.** Logistic regression needs the interaction written explicitly; boosting can find it on its own.

### 2.5 Cross-asset (ES/NQ/YM): **moderate evidence, partly in v1**
- **What it is:** what the sister indices did over the last few bars, and whether yours is leading or lagging them.
- **How to compute:**
  - Each index's return over 1, 3, 5 and 12 bars.
  - Own return minus the 3-index average over 5 and 20 bars (relative strength).
  - Spread between the three.
  - 20-bar rolling correlation.
- **Evidence:**
  - Lagged returns of index *constituents* predict 5-minute index returns beyond the index's own returns (Huddleston et al., abstract only).
  - Market-average and deviation-from-average features helped in three competition wins: G-Research 3rd place https://www.kaggle.com/competitions/g-research-crypto-forecasting/writeups/gaba-3rd-place-solution , Ubiquant 1st, and Jane Street 2024 8th.
- **Caveats:** three highly correlated indices carry far less information than 500 stocks or 14 coins. Expect a small gain (my inference).
- **In v1?** Only same-bar returns. **Lags and relative strength are missing.**

### 2.6 Continuous candle shape vs pattern flags: **moderate evidence for shape ratios, weak evidence for flags, mostly in v1**
- **What it is:** body, upper wick, lower wick and close position as continuous fractions of the range, for the current bar *and the last 1–2 bars*.
- **How to compute:**
  - body/range, upper wick/range, lower wick/range, (2C − H − L)/(H − L)
  - Inside/outside-bar code: higher-high/lower-low vs the prior bar, plus close up or down.
- **Evidence:**
  - Alpha158 uses exactly these ratios (KMID2/KUP2/KLOW2/KSFT2). Its importance-selected 20-feature list kept bar range (KLEN) and lower wick (KLOW): https://github.com/microsoft/qlib/blob/main/examples/benchmarks/GRU/workflow_config_gru_Alpha158.yaml
  - Textbook patterns on 5-minute DJIA bars showed some gross edge, but almost none after costs and corrections for testing many rules (Duvinage et al. 2013): https://ideas.repec.org/p/cor/louvrp/2671.html
  - Separate models per pattern beat one pooled model in Lin et al. 2021 (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0255558). This was on daily Chinese stocks, with selection bias. It supports **pattern × context interactions**.
  - No study compares flags and continuous ratios head to head.
- **In v1?** Yes for the current bar. **Missing: lagged shape ratios and the inside/outside code.**

### 2.7 Trend quality and moving-average features: **moderate evidence, partly in v1**
- **What it is:** not just "is it trending" but "how clean is the trend, and how stretched is price from its trend line."
- **How to compute:**
  - Rolling straight-line fit of closes over 10, 20 and 60 bars: slope in avg bars per bar, R², and how far the last close sits from the line (residual) in avg bars.
  - MACD-style EMA differences: (EMA8 − EMA24), (EMA16 − EMA48), (EMA32 − EMA96), each divided by average bar range.
- **Evidence:**
  - In Qlib's importance-selected list, trend-fit R² (RSQR, 4 slots) and residual (RESI, 2) were among the most-picked. Plain moving-average distances were *not* picked. That list comes from daily Chinese stocks with no out-of-sample check, so treat it as a hypothesis.
  - Scaled EMA differences at 3 speeds are standard inputs in futures ML (Lim, Zohren & Roberts: https://arxiv.org/abs/1904.04912), but gains vanished at about 2–4 basis points of cost.
- **EMA-cross timing** ("bars since EMA8 crossed EMA20"): **no direct evidence.** The nearest tested idea is bars since the high or low.
- **In v1?** EMA stack, slope, distances and 60-minute trend are in. **Fit quality (R²/residual) and multi-speed MACD are missing.**

### 2.8 Volume and liquidity (Amihud, volume z-scores, price-volume correlation): **moderate evidence, partly in v1**
- **What it is:** whether volume is unusual for this time of day, and how much price moves per unit of volume.
- **How to compute:**
  - Volume ÷ average volume for *this same time slot* over the last 20 sessions.
  - Volume z-score over 20 bars.
  - Amihud-style = average of |return in avg bars| ÷ relative volume over 20 bars.
  - Rolling correlation of price change with log volume over 10 and 20 bars (Alpha158 CORR/CORD).
- **Evidence:**
  - Liquidity is the second-ranked family in Gu, Kelly & Xiu.
  - Price-volume correlation took 7 of the 20 slots in Qlib's importance list.
  - Jiang, Kelly & Xiu: rising volume helps predict.
  - The Optiver competition winner normalized by time-of-day bucket and replaced features that drifted over time with ranks: https://www.kaggle.com/competitions/optiver-trading-at-the-close/writeups/hyd-1st-place-solution
- **Caveats:** volume levels shift between years. Micro contracts launched in 2019, so check what your pre-2019 volume actually is. Use **ratios only, never raw volume.**
- **In v1?** Only volume ratios. **Missing: time-of-day-normalized volume, Amihud, price-volume correlation.**

### 2.9 VWAP: **weak evidence, partly in v1**
- **Evidence:** VWAP minus close appears as a mean-reversion signal in Kakushadze's 101 Alphas (#42, #57): https://arxiv.org/abs/1601.00991 . That source is daily stocks and ignores costs. Nothing tests "VWAP events" such as crosses or band touches.
- **In v1?** VWAP distance is in. **Events are untested hypotheses.**

### 2.10 Recent pattern history and bars since a pattern: **no direct evidence, not in v1**
- No study tests these. The indirect evidence points to **short memory**:
  - In Jiang, Kelly & Xiu, bars 2–5 back carried little weight.
  - In Lin et al., 3-bar pattern combinations did worse than 2-bar ones because the data got spread too thin.
- If you add them, keep them few and simple, and cap them at 10–20 bars.

### 2.11 Earlier signals' confidences or recent setup outcomes: **no direct evidence, not in v1**
- The closest analogue: in Jane Street 2024, feeding recent outcomes back through online learning added about 4× more than feature engineering (https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/writeups/evgeniia-grigoreva-private-lb-8th-solution).
- **Big leakage risk:** these values must come from predictions made out of sample and from trades already closed before the current bar.

### 2.12 Microstructure proxies from OHLC (Roll, Corwin-Schultz, Kyle lambda, VPIN): **weak evidence for our purpose, not in v1**
- Easley, López de Prado et al. (87 futures, ~50 bars/day) found these predict *changes in volatility and distribution shape* about a week ahead, with 52–61% accuracy, no costs, and **not direction**.
- In that study, VPIN led out of sample and the Roll measure led for serial correlation. Bar type barely mattered.
- VPIN's value is disputed (https://ideas.repec.org/a/eee/finmar/v17y2014icp1-46.html). Built from bars, it is mostly a function of absolute bar return, which you already have (my algebra).
- Spread estimators (Corwin-Schultz, EDGE: https://irf.fhnw.ch/entities/publication/f9b26d6d-1a1e-4767-af52-b5b253b5877f) mostly measure noise when MES/MNQ quotes are almost always 1 tick wide (my inference).
- **Low priority.** If tried at all: the Roll measure, or the lag-1 autocorrelation of 1-minute returns, as a "choppy vs trending" regime feature.

### 2.13 Structural breaks and entropy (SADF, CUSUM, Lempel-Ziv): **no evidence for our purpose, not in v1**
- Proposed in López de Prado's book (chapters 17–18). I found **no out-of-sample study** on intraday futures. SADF is also slow to compute. **Lowest priority.**

### 2.14 Fractional differentiation: **no predictive evidence, effectively already in v1**
- On ES, it becomes stationary at about d = 0.35 while keeping 0.995 correlation to price (https://smallake.kr/wp-content/uploads/2017/10/SSRN-id3031282.pdf). That is in-sample only.
- At that setting it is roughly "price minus a long weighted average of past prices", which is close to your EMA distances. The leftover price level (about 5%) drifts from 2010 to 2026 (my calculation). **Skip.**

### 2.15 Chart-image CNNs: **strong evidence in stocks, not needed here**
- Jiang, Kelly & Xiu's CNN beat traditional signals, and standard signals explained only about 10% of it. But a **logistic regression on the same range-scaled numbers got most of the way.**
- Candle-image papers are weak:
  - GAF-CNN only reproduces rule-based pattern labels: https://arxiv.org/abs/1901.05237
  - The S&P futures GAF study has no costs and picked its cutoff on the test period: https://www.iris.unina.it/retrieve/e268a731-4efe-4c8f-e053-1705fe0a812c/IEEE_CAA_Journal_of_Automatica_Sinica-3.pdf
  - Claims of about 90% accuracy (https://arxiv.org/abs/1903.12258) are not credible.
- A commodity-futures follow-up (abstract only) found the patterns did not transfer from US to Chinese markets. **Use the range-scaled numbers (2.2), not images.**

**Other indicator sets.** Classic indicators such as RSI, Stochastic, CCI, Williams %R and MACD flags come with 70–90% accuracy claims (Kara 2011, Patel 2015). I could only read abstracts, and the designs look prone to leakage. A 1-minute SPY test found adding them did *not* beat raw OHLCV out of sample (https://arxiv.org/abs/2412.15448), though that study is weak. **Give them little weight.** v1 already covers the same ground.

---

## 3. What tends to overfit or fail to generalize, and validation lessons

**What overfits**
- **Many features with weak regularization.** Plain regression on all 900+ predictors had out-of-sample R² of **−3.46%**, against about +0.3% for regularized or tree models (Gu, Kelly & Xiu). Keep strong regularization and shallow trees.
- **Generic feature generators** (tsfresh, hundreds of features): https://tsfresh.readthedocs.io/en/latest/text/list_of_features.html
  - In one competition, the winning tsfresh model was really detecting *repeated price values from tick rounding*. Adding tiny noise dropped it to coin-flip: https://arxiv.org/abs/1811.07792
  - Your prices sit on a 0.25-point grid, and tick size relative to price shrank from 2010 to 2026. Features like "share of repeated values" or "entropy" can end up tracking the era, not the market.
- **Short-horizon return signals fade.** Krauss and Fischer's daily strategies turned negative or flat after costs in 2010–2015. Intraday predictability fell after decimalization (Huddleston). Expect any edge to vary by year.
- **Results that depend on costs and turbulent periods.** ML gains come mostly from volatile, hard-to-trade states and shrink with costs (Avramov et al.: https://papers.ssrn.com/abstract=3450322). Futures ML survived only about 2–4 basis points of cost (Lim et al.).
- **Too-good numbers.** Careful studies get about 52–54% direction accuracy and forecast correlations of 0.04–0.05. If a new feature block pushes AUC well above about 0.60, **look for look-ahead first.** AUC is the model's ability to rank winners above losers: 0.5 is a coin flip, 1.0 is perfect.
- **Slicing too thin.** Lin et al.'s 3-bar pattern combinations spread trades across 2,197 cells and did worse than 2-bar ones. The same risk applies to many "pattern N bars ago" flags.
- **Misleading importance rankings.**
  - In-sample tree importance (MDI) and out-of-sample importance (MDA) disagreed on real futures data (Easley et al.).
  - Tree split importance systematically **underrates yes/no flags** compared with continuous features: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1796903/ . Your 25 pattern flags will look less important than they are.
  - Correlated features split credit between them. EMA distances, Momentum(14), swing distances and new return features will all overlap.
- **Unstable importance on your exact market.** The MNQ 5-minute preprint found rankings changed from fold to fold (https://arxiv.org/abs/2605.17724).
- **Running too many backtests.** López de Prado: about 20 trial variations typically produce one false "winner" at 5% significance (https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf). **Count your trials.**

**Validation lessons from competitions**
- **Use a gap between train and test.** Remove (purge) training trades whose exit falls inside the test year, and leave a gap (embargo) at least as long as your longest holding time. G-Research 2nd place (https://www.kaggle.com/competitions/g-research-crypto-forecasting/writeups/nathaniel-maddux-2nd-place-solution) used 1-week gaps. Jane Street 2021 1st place used a 31-day gap (https://www.kaggle.com/competitions/jane-street-market-prediction/writeups/cats-trading-yirun-s-solution-1st-place-training-s).
- **Fit everything inside each fold.** Scalers, "historical win rate of this pattern" and any first-stage confidence model must be fit inside each training window only. The Jane Street 2021 winner found that a public approach leaked because one step was fit before the data was split.
- **Judge by year, not just the total** (Numerai: https://forum.numer.ai/t/model-diagnostics-feature-exposure/899). Report net $ per year and the worst year. A model that is slightly worse on average but steadier is usually the better bet. Also check that no single feature dominates the predictions.
- **Check that score differences are not just noise.** If results jump around between neighbouring settings or random seeds, the difference isn't real (G-Research 2nd place).
- **Find drifting features.** Train a quick model to guess the *year* from your features (adversarial validation, Optiver 1st place: https://www.kaggle.com/competitions/optiver-realized-volatility-prediction/discussion/274970). Anything that guesses the year easily is drifting. Replace it with a ratio, a rank, or a comparison to the same time of day.
- **Refit more often.** Online updating or periodic refits beat adding features in two competitions (Jane Street 2024; Optiver Trading at the Close, where refitting every 12 days helped). Yearly refits may be too coarse, so compare quarterly refits once the feature set is stable.
- **Weight by what matters.** Weighting training samples by trade size in $ or R helps keep the model from optimizing on scratch trades (Jane Street 2021 1st place).
- **Treat competition wins with care.** They had no costs, short live windows that winners themselves called lucky, and sometimes gains that came from leakage.

---

## 4. Feature blocks to add to v1, in priority order

**Conventions for every block**
- Everything is computed **at the signal bar's close** from that bar and earlier bars only.
- Prices are in **avg bars**: divide by the same average bar range v1 uses, measured up to the previous bar.
- Volumes are ratios or z-scores, never raw.
- **Windows N count bars of the timeframe being scored** (5, 15 or 60 minutes).
- "Signed" means flipped by trade direction, so a positive value always means "in favour of the proposed trade." This lets one model handle longs and shorts.

### Block A: Multi-horizon returns (reversal and momentum), 7 features
1. `ret1, ret2, ret3, ret5, ret10, ret20` = (C_t − C_{t−N}) / avg bar range, signed.
2. `ret60_volscaled` = (C_t − C_{t−60}) / (avg bar range × √60), signed.

*Why first:* the strongest and most consistent evidence (2.1). It directly tests your "momentum over 5/10/20 bars" idea, and it is cheap. Don't assume momentum: the reversal sign is common.

### Block B: Range position and timing of extremes, 8 features
1. `rsv5, rsv20, rsv60` = (C − lowest low_N) / (highest high_N − lowest low_N), signed by mapping to 1 − rsv for shorts.
2. `prev_close_rsv20` = the same as `rsv20` but for bar t−1's close.
3. `bars_since_high20/20` and `bars_since_low20/20`.
4. `bars_since_high60/60` and `bars_since_low60/60`.
5. `range20_width` = (highest high_20 − lowest low_20) / avg bar range.

*Why:* range scaling was the key ingredient in the best chart study (2.2), and Alpha158 has RSV and IMAX/IMIN.

### Block C: Volatility regime and cost hurdle, 6 features
1. `gk_vol10 / gk_vol60`: Garman-Klass volatility over 10 bars ÷ over 60 bars (short vs long).
2. `gk_vol60 / gk_vol_20days`: today's level vs the 20-day level at the same bar size.
3. `day_range_so_far / avg_daily_range_20d`.
4. `bar_range_t / avg bar range` and `bar_range_{t−1} / avg bar range`.
5. **`cost_in_avgbars`** = round-trip $cost / ($ per point × average bar range in points).
6. `stop_distance_in_avgbars`, if the setup has a defined stop. This comes from my reasoning about cost-aware labels, not from a paper.

### Block D: Session return and time-of-day interactions, 6 features
1. `ret_since_prior_rth_close` (avg bars, signed).
2. `overnight_gap` (avg bars, signed). v1 has the gap, so keep it here only if it is a different version.
3. `ret_since_rth_open` (avg bars, signed).
4. `prior_day_last30min_ret` (avg bars, signed).
5. `minutes_to_rth_close` (capped at 0 outside RTH).
6. `ret_since_prior_close × is_last_60min`: the explicit interaction for logistic regression.

*Evidence:* Baltussen and Gao (2.4). This is the only family with direct index-futures evidence.

### Block E: Trend quality and multi-speed MACD, 8 features
1. `fit_slope20` (avg bars per bar, signed), `fit_r2_20`, `fit_resid20` (last close minus the fitted line, in avg bars, signed).
2. `fit_r2_60` and `fit_resid60`.
3. `macd_8_24` and `macd_32_96` = EMA difference / avg bar range, signed.
4. `bars_since_ema8x20_cross`, signed (+ means the cross is in the trade direction), capped at ±50. This tests your EMA-cross timing idea. It has no direct evidence, so it rides inside this block to be judged together with its near-duplicates.

### Block F: Volume and liquidity, 6 features
1. `vol_rel_tod` = bar volume ÷ average volume for this time slot over the last 20 sessions, as log ratio.
2. `vol_z20` = z-score of log volume over 20 bars.
3. `vol_rel_tod_prev` = the same as `vol_rel_tod` for bar t−1.
4. `amihud20` = average over 20 bars of |return in avg bars| ÷ `vol_rel_tod`.
5. `corr_ret_logvol10` and `corr_ret_logvol20`: rolling correlation of bar return with log relative volume. This is the Alpha158 CORD idea.

*Check first:* adversarial validation on the volume features across 2010–2026, because of the 2019 micro launch and volume shifts.

### Block G: Cross-asset context, 6 features
1. `basket_ret3` and `basket_ret12`: the average of ES/NQ/YM returns, each in its own avg bars, signed.
2. `rel_strength5` and `rel_strength20`: own return minus basket return, signed.
3. `leader_lag1`: the strongest other index's 1-bar return, lagged, signed.
4. `corr20_own_vs_basket`: falling correlation means the indices are diverging.

### Block H: Lagged candle shape, 7 features
1. For bars t−1 and t−2: `body/range` (signed), `upper_wick/range`, `lower_wick/range`. That is 6 features.
2. `loc_code_t`: inside, outside, higher-high/higher-low or lower-high/lower-low vs the prior bar. Treat it as a category, or as two numbers (Δhigh and Δlow in avg bars, signed).

### Block I: VWAP events, 5 features (untested hypotheses)
1. `vwap_z` = (C − VWAP) / standard deviation of price around VWAP for the session so far, signed.
2. `bars_since_vwap_cross`, signed, capped at 50.
3. `vwap_crosses_today`: a count, as a choppiness measure.
4. `vwap_slope10` (avg bars per bar, signed).
5. `touched_vwap_last3`: a yes/no flag.

### Block J: Recent pattern history, 5 features (untested hypotheses)
1. `bars_since_last_bull_pattern` and `bars_since_last_bear_pattern`, capped at 20.
2. `net_pattern_count10` = bullish minus bearish flags over the last 10 bars, signed.
3. `pattern_decay_score` = exponentially decayed count (half-life 3 bars) of same-direction patterns.
4. `same_family_last5`: a flag for whether the same pattern family fired in the last 5 bars.

### Block K: Earlier signals and recent outcomes, 4 features (untested; highest leakage risk, so test last)
1. `prev_signal_p`: the model's **out-of-sample** probability on the most recent earlier setup that day. It must come from the model trained on *prior* years only.
2. `bars_since_prev_signal`, capped.
3. `last3_closed_trades_net_R`: only trades whose exits came before the current bar.
4. `family_winrate_last50_closed`: only closed trades, and computed using training-window data only.

### Block L (optional, low priority): Regime proxies, 3 features
1. `ac1_1min_60`: lag-1 autocorrelation of 1-minute returns over the last 60 minutes.
2. `roll_ticks60` = 2√|cov(Δp_t, Δp_{t−1})| over 60 one-minute bars, in ticks.
3. `variance_ratio` = (variance of 5-minute returns) / (5 × variance of 1-minute returns) over the session so far.

**Not recommended:** fractional differentiation, SADF and entropy, VPIN, Corwin-Schultz/EDGE spreads, tsfresh dumps, GAF or CNN images, and extra classic indicators (RSI, Stochastic, CCI, Williams %R). Each has no evidence for our purpose or duplicates what v1 already has (see Section 2).

### How to test each block

1. **Freeze the baseline.** v1 features, labels, cost model ($2–3.50 round trip), model settings, and the **trade-taking rule**, e.g. take a trade if P > the break-even P from average win and loss. Set the rule in advance so threshold-picking can't create fake gains.
2. **Walk forward by year:**
   - Train on all prior years, test on the next year.
   - Purge training trades whose exit crosses into the test year.
   - Leave an embargo gap at least as long as your longest trade.
   - Fit all scalers and encodings inside each training window.
3. **Hold back the last 1–2 years (e.g. 2025–2026) entirely.** Look at them only once, after the block selection is final.
4. **Add one block at a time** to the current best set, in the order above.
5. **Keep a block only if all of these hold:**
   - Total out-of-sample **net $** over all walk-forward test years improves.
   - Net $ improves in **at least 60% of test years**, and the worst year is not worse.
   - Log-loss or Brier score does not worsen. These are standard accuracy scores for probabilities; lower is better.
   - Results hold under both models (logistic and boosting), or you understand why they don't.
6. **Sanity checks for each kept block:**
   - Re-run with the block's columns **shuffled across trades**. The gain should disappear.
   - Re-run with 2–3 random seeds.
   - Run adversarial validation (can the block guess the year?).
   - If AUC jumps far above about 0.60, audit for look-ahead before celebrating.
7. **Importance:** judge the *whole block* by shuffling it in the test years. Never use in-sample tree importance, which favours continuous features over your pattern flags.
8. **Log every trial:**
   - date, block, exact definitions and windows
   - net $ per year and in total
   - number of trades taken
   - log-loss and AUC
   - keep or drop, with the reason
   - **a running count of all trials**

   After about 20 trials, expect at least one false "winner." Be stricter, or confirm on the held-back years.
9. **After the block set is final:** compare yearly vs quarterly refits, because adapting to recent data helped more than features in two competitions.

**Uncertainty flags**
- Blocks A–D rest on real evidence, but it comes from other markets or horizons.
- Blocks E–H are reasonable analogues.
- Blocks I–K are your own ideas. **Nothing in the literature tests them**, so only your walk-forward can show whether they work.

---

# Reviewer's corrections and additions

# Review: Corrections and Additions for the Feature-Selection Report

## Citations I checked

1. **MNQ preprint (arXiv 2605.17724).** Confirmed: Mesfin, May 2026, MNQ, 5-minute OHLCV, 2021–2025, 944 days. Out-of-sample accuracy was 50.00–50.89% against a 51.8% base rate. Permutation p-values were 0.135 and 0.515, and feature importance was unstable across folds. The abstract does not mention costs. https://arxiv.org/abs/2605.17724
   - **Correction:** The report calls this "the study closest to your data" and lists it under small edges. Its label is a once-a-day direction call: does the session close more than 10 points above the 10:30 open? That is not a per-setup trade outcome. Its results also sit at or below the base rate, so it shows no edge at all, not a small one. Say both things wherever it is cited.

2. **Baltussen et al., JFE 2021.** I checked the full text. The +2.88% out-of-sample R² for the rest-of-day return and the −1.71% for the first half-hour ("in this extended equity futures index sample") are correct. The Sharpe range is 0.87–1.73. https://academicweb.nd.edu/~zda/intramom.pdf
   - **Correction:** The paper says "we do not consider transaction costs". It also says S&P 500 futures still give "a positive net Sharpe ratio" at a cost of one tick. The report quotes only the gross figures and its own estimate of about 2.7 bp per trade. Add the authors' net-of-one-tick statement.
   - **Correction:** The 2.7 bp estimate uses the annual return of an equal-weighted portfolio across many equity index futures. It is not the per-trade edge of one contract. Label it as a rough order of magnitude.
   - **Correction:** The 0.7–1.3 bp cost figure only holds at today's index levels. ES was about 1,100 in 2010, so $3.50 on an MES-sized contract would have been about 6 bp then. The cost hurdle changes a lot across the 2010–2026 walk-forward. This strengthens the case for `cost_in_avgbars`, and the report should say so explicitly.

3. **Molnar, IRFA 2012.** **Not confirmed.** The abstract only says that range-based estimators "provide significantly more precision, but still remain noisy". It does not name Garman-Klass as best, and the "several times more precise" efficiency figures come from an unchecked working-paper excerpt. Rewrite the line as "range estimators are more precise than close-to-close", or say the ranking is unverified. https://ideas.repec.org/a/eee/finana/v23y2012icp20-29.html

4. **Qlib benchmarks README.** Confirmed: IC of 0.0448 for LightGBM, 0.0498 for XGBoost, 0.0397 for Linear, 0.0521 for DoubleEnsemble, and 0.0400 for LightGBM on Alpha360. The README does not say whether results are before or after costs. Add one condition to the report's "IC 0.04–0.05 = small edges" benchmark: these ICs come from ranking about 300 Chinese stocks against each other on daily data, so they do not translate directly to AUC for a single contract. https://github.com/microsoft/qlib/blob/main/examples/benchmarks/README.md

5. **Krauss, Do & Huck (econstor PDF).** Confirmed: the variable-importance "elbow" with a sharp drop after R(4). The fourth sub-period (which the text writes as "01/01 to 10/15", i.e. 2010–2015) had returns of "-14 and -25 percent p.a. after transaction costs". https://www.econstor.eu/bitstream/10419/130166/1/856307327.pdf

6. **Jiang, Kelly & Xiu, JF 2023.** Confirmed: Sharpe ratios of 7.15 (CNN) and 5.56 (logistic on image-scaled data), and 2.50 for the logistic model on cumulative returns.
   - **Overstatement:** Sections 1.3 and 2.15 say the range-scaled logistic model "captured most of what a deep image model learned". The findings say the logistic model explains only 22–35% of the CNN's predictions (McFadden R²), and that more than half of the CNN signal is nonlinear. Rephrase as "got about 78% of the CNN's Sharpe in the 5-day case; much of the CNN's signal remains nonlinear".
   - **Overstatement:** Section 2.2 labels this evidence "strong (by analogy)". The data are US stocks ranked against each other, on daily bars, before costs. Downgrade to "moderate, by analogy".
   - https://doi.org/10.1111/jofi.13268

## Other overstated or misattributed claims

- **Section 1.1, reversal claim.** The cited reversal evidence (Krauss, Fischer & Krauss, the crypto minute-bar study, and Gu-Kelly-Xiu's mom1m) comes almost entirely from ranking many assets against each other. For a single index future over time, the direct evidence (Baltussen, Gao) points to *momentum* within the day. Say plainly that no source shows short-term reversal over time for intraday index futures.
- **Section 1.5, "Intraday studies find R² of about 1–3%".** This range comes only from predicting the last half hour. It does not apply to every bar of the day.
- **Section 2.11, Jane Street 2024 as the "closest analogue".** The gain there came from online model updating, not from a feature built on earlier predictions. Present it as weak support for frequent refitting only.
- **Section 2.12, "52–61% accuracy".** This mixes the best lookback windows with the averages. The averages were 0.52–0.57, and spread prediction was below chance (0.454). Note that the targets were changes in volatility and distribution shape about a week ahead, not direction.
- **Section 2.7 and Block E.** The Qlib importance-selected 20-feature list is the only support for adding trend-fit R² and residual. That list was chosen with no out-of-sample check, so Block E is weaker than the "reasonable analogue" label suggests.
- **Section 3, "about 20 trials, one false winner".** This is just 1/0.05. If López de Prado is cited, cite his actual tools for correcting it: the deflated Sharpe ratio and the probability of backtest overfitting (see below).
- **Joubert's meta-labeling framework is in the findings but missing from the report.** Its main design point is to prioritise features that detect regimes where the primary signal fails. That point should shape the block order. https://github.com/hudson-and-thames/meta-labeling

## Missing work worth adding

- **Li, Sakkas & Urquhart (J. Financial Markets 2022).** Intraday time-series momentum (first half hour predicting the last) across 16 developed markets. It is stronger when liquidity is low, volatility is high and news arrives in discrete bursts. This is independent support for Block D and for using volatility as a conditioning variable. https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html
- **Zarattini, Aziz & Barbon (SFI WP 24-97, 2024).** An intraday SPY momentum strategy that enters when price breaks out of a "noise band" built from the average move at the same time of day. It reports a Sharpe of 1.33 net of costs for 2007–2024, but the backtest is in-sample. It is directly relevant as a feature: distance of the current move-from-open beyond its usual size for this time of day. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
- **Heston, Korajczyk & Sadka (JF 2010), "Intraday patterns in the cross-section of stock returns".** Returns in the same half-hour slot on prior days predict that slot today. That suggests a cheap feature: the mean return of this time slot over the last N sessions. https://doi.org/10.1111/j.1540-6261.2010.01573.x
- **Chinco, Clark-Joseph & Ye (JF 2019), "Sparse signals in the cross-section of returns".** A LASSO on 1-minute bars finds that predictors are sparse and short-lived. This supports strong regularisation and frequent refits. https://doi.org/10.1111/jofi.12733
- **Bailey, Borwein, López de Prado & Zhu, probability of backtest overfitting (CSCV) and the deflated Sharpe ratio.** These are the right tools for the "count your trials" step in Section 4.8. https://papers.ssrn.com/abstract=2326253 and https://papers.ssrn.com/abstract=2460551
- **Probability calibration.** The trade-taking rule compares P with a break-even probability, which only works if P is calibrated. Add Platt or isotonic calibration, fitted inside each fold, and report calibration per year.

## Practicality and look-ahead problems the report misses

- **Swing points in v1 may use future bars.** Swing distances, swing breaks and Fib position need a swing high or low that is only confirmed once later bars print (fractal or zigzag rules). Each swing point must carry its *confirmation* time and be usable only after that bar. This is the most likely leak in v1. The "AUC above 0.60" sanity check should name it.
- **Continuous-contract adjustment.** Before 2019 the data must be spliced ES/NQ/YM. With additive back-adjustment, log-based features (Garman-Klass and Parkinson use ln H/L and ln C/O) and bp-based costs are distorted far back in history. Compute log features on unadjusted prices for each contract, or ratio-adjust. Mask or flag roll days.
- **Labels before 2019 are synthetic for micros.** MES/MNQ/MYM did not exist before May 2019, and costs and fills then are hypothetical. Report results for the walk-forward years before and after 2019 separately.
- **Session boundaries.** 20- and 60-bar windows on 5/15/60-minute bars cross the overnight session and the daily 17:00–18:00 CT maintenance break. Define each feature as either Globex or RTH. Fix the VWAP anchor (RTH or Globex). Use an exchange calendar so `minutes_to_rth_close` handles early-close holidays and DST, and work in CT.
- **Volume features.** Time-of-day-normalised volume needs the same slot across sessions, so half-days and roll weeks distort it. Also note that 1-minute OHLCV has no signed volume, so tick-rule or bulk-volume imbalance proxies are weak.
- **Block K, `prev_signal_p`.** Within a test year, the prior-years model also scores the earlier same-day setup, which is fine. But in training rows this feature must come from earlier-year walk-forward models, which means nested walk-forward. The first training years will have no value for it. State this, or drop the block.
- **Block C, `gk_vol_20days` at the same bar size.** It needs about 20 sessions of history, so the first weeks after each roll or data gap are missing. That is minor, but handle it explicitly.