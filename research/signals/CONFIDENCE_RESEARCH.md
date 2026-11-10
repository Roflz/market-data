# Confidence-Weighted Entries and Exits: What the Research Says and How We Would Build It

## The short version

- **Yes, people have built this.** It goes by several names: "weight of the evidence" scores, confluence scores, boosting, Bayesian signal combination and, closest to your idea, **meta-labeling**. Meta-labeling fits your design almost exactly. The textbook pattern picks the direction. A second model, learned from data, says how confident to be in that signal right now.
- **Your machine-learning idea is sound, and it is a standard method.** The simplest version is regularized logistic regression. Its output is a table with one weight per signal, which you can read as a confidence weight. We can learn one table for entries and a separate one for exits.
- **You're right about the exits.** The rule "exit when ANY opposite pattern fires" was always going to exit almost at once. Several of our 28 patterns fire on 20-40% of bars, and many of them measure the same thing. A weighted score with a higher bar for exiting than for entering fixes this by design.
- **Be realistic about the odds.** Most of the evidence says single candlestick patterns have no edge, intraday futures included. Combining weak signals usually beats using them one at a time, but the gain is often too small to cover costs. A real chance is that the learned weights come back close to zero for most patterns. That would still be a useful answer, and the way we test it has to be able to show it.

---

## 1. Have people built confidence-weighted signal systems?

They have, in three main forms. They range from hand-set weights to fully learned ones.

### a) Hand-weighted "confluence" or "weight of the evidence" scores

- **Greg Morris's Weight of the Evidence model.** Each component gets a fixed weight, and all weights add up to 100. Components are short, medium and long-term trend measures plus market breadth. Morris adds up the weights of the components that are currently "on" to get a 0-100 score, which he reads in bands: 0-30 red, 31-50 orange, 51-80 yellow, 81-100 green. The two middle bands are deliberately neutral zones, so the model "absorbs some volatility" instead of flipping on every wiggle. ([StockCharts, Morris](https://articles.stockcharts.com/article/articles-dancing-2018-07-building-a-rules-based-trend-following-model---12))
  *Evidence: none published.* His weights are secret and no backtest is shown.
- **Ned Davis Research composites** work the same way. One of them is simply the percentage of 100+ indicators that are bullish, which makes it an equal-weight vote. Reported thresholds are above 70 bullish, 55-70 neutral and below 55 danger. ([Morris, Weight of the Evidence](https://articles.stockcharts.com/article/articles-dancing-2018-08-weight-of-the-evidence))
  *Caveat:* these thresholds come from a secondary write-up I could not check against NDR's own material. They are daily and weekly stock-allocation models.
- **Vendor confluence guidance** ([LuxAlgo](https://www.luxalgo.com/library/concept/confluence-and-scoring-systems/), plus TradingView confluence scripts) gives the same advice every time:
  - Use 3-5 *independent* factors. Five momentum indicators agreeing is one vote, not five.
  - Default to equal weights unless data says otherwise.
  - Require a minimum score, such as 4 of 6.
  - Add hard vetoes, such as news or time of day.
  - Test on data the system wasn't built on.

  *Evidence: none.* It is sensible design advice with no results attached.
- **Al Brooks** thinks about every setup as a probability: roughly 60% in strong context and roughly 40% in a trading range, where he wants at least 2x reward to risk. He decides trades with the "trader's equation" (probability x reward compared with (1 - probability) x risk). He also treats staying in a trade as a decision made fresh on every bar. ([Brooks Trading Course](https://www.brookstradingcourse.com/?p=57617))
  *Evidence: his own experience and opinion.* The 60/40 figures are rules of thumb, not measured rates.

### b) Weights derived from statistics

- **Bulkowski's candle statistics** are the only large practitioner dataset. They show that a pattern's hit rate and its follow-through are different things. Bullish engulfing reverses 63% of the time, yet ranks 84th of 103 on overall performance. Results also change with context: market trend, and where the candle sits in the yearly range. ([ThePatternSite](https://www.thepatternsite.com/BullEngulfing.html))
  *Caveats:* daily US stocks, no costs, many in-sample context slices.
- **Bayesian combination.** Hassanniakalager, Sermpinis & Stasinakis (2021) first screened many technical rules with a data-snooping test, then combined the survivors with several methods. Naive Bayes, where each signal adds its own evidence score, was the weakest combiner; model averaging and the other methods did better. They tested walk-forward, after costs, on daily FX. The combined systems earned *up to* 4-5x the profit of the single surviving rules (a maximum, not a typical result). The thesis reports an out-of-sample Sharpe of about 0.6 against about 0.2 ([journal abstract](https://ideas.repec.org/a/eee/empfin/v63y2021icp230-251.html)). ([thesis PDF](https://theses.gla.ac.uk/30934/1/2018HassanniakalagerPhD.pdf))
  *This is the best evidence that weighting beats single signals.* The absolute edge was still small, and the data was daily, not intraday.

### c) Weights learned by machine learning

- **Boosting** (Creamer & Freund, 2010). The model learns a weight for each indicator rule, adds them into one score, and trades only when the score clears a threshold set to cover costs. ([RePEc](https://ideas.repec.org/a/taf/quantf/v10y2010i4p401-420.html))
  *Warning:* a related working paper by the same authors (one MSFT stock, 840 days) had a 48.8% error rate, which is a coin flip ([PDF](https://c.mql5.com/forextsd/forum/174/a_boosting_approach_for_automated_trading.pdf)). The 2010 paper's after-cost results are unverified. A later version on intraday Euro STOXX and DAX futures was tested on only about one month. ([RePEc](https://econpapers.repec.org/RePEc:taf:quantf:v:12:y:2012:i:4:p:531-545))
- **Meta-labeling** (López de Prado, *Advances in Financial Machine Learning*, 2018). This is the closest match to your idea, and section 4 covers it.
- **TradingView "ML" indicators**, such as the Lorentzian Classification script. These exist, but they publish no out-of-sample or after-cost results, and their inputs are mostly overlapping oscillators. ([LuxAlgo copy](https://www.luxalgo.com/library/indicator/WhBzgfDu-machine-learning-lorentzian-classification/))
  We should not use one as is.

---

## 2. Does combining many weak signals actually work?

The honest answer: combining helps compared with single signals, but whether the result clears costs is often no.

**On candlestick patterns specifically, the evidence is negative:**
- **Marshall, Young & Rose (2006)** tested 28 candle signals on DJIA stocks with bootstrap methods and found none with predictive power. ([RePEc](https://econpapers.repec.org/RePEc:eee:jbfina:v:30:y:2006:i:8:p:2303-2323))
- **Fock, Klein & Zwergel (2005)** tested candlestick patterns on **intraday DAX and Bund futures**. They found no predictive ability, and the same held when patterns were combined with other indicators. ([summary](https://improbable.com/2015/06/28/fock-performance-of-candlestick-analysis))
  *Uncertain:* I only saw a summary, so I don't know how they did the combining.
- **Aronson** tested 6,402 technical rules on the S&P 500. After adjusting for data mining, none were significant. ([CXO review](https://www.cxoadvisory.com/technical-trading/evidence-based-technical-analysis-applying-the-scientific-method-and-statistical-inference-to-trading-signals-chapter-by-chapter-review))
- A StockCharts review of Bulkowski's numbers puts many popular patterns near a coin flip: hammer 60%, shooting star 59%, bullish harami 53%, bearish harami 47%. ([StockCharts](https://articles.stockcharts.com/article/stockcharts-insider-every-candlestick-scan-in-the-library-ranked-and-why-the-popular-ones-may-fall-short/))

All of this agrees with what we already found: single patterns hit 42-55% and don't cover costs.

**On ML with candle features:**
- **Lin et al. (2021).** ML on candle shape plus indicators such as momentum looked good, but only after picking the best-scoring patterns afterwards. The "trade every pattern" pool lost money after costs. ([PLoS ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC8345893))
- **Goumatianos et al. (2013)** reported thousands of "60-95% confidence" candle sequences. The study used shuffled cross-validation, a 20-occurrence minimum and no costs. It is a good example of how *not* to estimate confidence. ([paper](https://www.scitepress.org/Papers/2013/43341/43341.pdf))

**On ML on intraday index futures:**
- **Huddleston, Liu & Stentoft (2023).** ML found real 5-minute predictability in US equity indices, with a Sharpe of 0.98 after costs. But the useful inputs were **lead-lag between related instruments**, not candle shapes. ([RePEc](https://ideas.repec.org/a/oup/jfinec/v21y2023i2p485-527..html))
  *Abstract only.* The predictors were lagged returns of the index's own constituent stocks, which we don't have. So the lesson is that the edge came from data beyond candles. Whether ES/NQ/YM lead-lag helps is a separate idea we'd have to test ourselves.
- **Mesfin (2026).** Gradient boosting and an LSTM on **MNQ 5-minute bars**, tested walk-forward, found nothing above the base rate: best 50.9% against a 51.8% base rate. The target was one daily direction call (close vs the 10:30 open), not bar-by-bar entries, so it's indirect evidence. ([arXiv](https://arxiv.org/abs/2605.17724))
  *Single-author preprint, about 4 years of data.* We have 16 years across three contracts, which is a big advantage.

**General warnings:**
- Genetic and ML rule search often finds real structure that is too small to pay costs. That held on daily S&P ([Allen & Karjalainen](https://www.cs.montana.edu/courses/spring2007/536/materials/Lopez/genetic.pdf)) and on intraday FX ([Neely & Weller](https://gpbib.cs.ucl.ac.uk/gp-html/neely_2003_JIMF.html)).
- Rules that look like winners in the past often don't stay winners. You could not have picked the future winners in advance. ([Bajgrowicz & Scaillet](https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Bajgrowicz_Scaillet.pdf))

**What this means for us.** The weighted approach is the right shape, and it is the best-supported way to use weak signals. Any edge will most likely come from **context and interactions**: the same pattern in an uptrend vs a downtrend, near a swing level vs mid-range, at 9:45 vs 15:30. It will not come from the pattern labels themselves. The scorecard has to be **net $ per trade after costs**, not hit rate.

---

## 3. Exits specifically

**Why "exit on any opposite pattern" fails.** Here is an illustration (not our measured number). Suppose some opposite pattern among the 28 fires on half of all bars. Then a trade has only a 1-in-8 chance (0.5 × 0.5 × 0.5) of surviving 3 bars without an exit signal. On top of that, the patterns overlap heavily: engulfing, outside bar and close-location extremes often fire on the same bar. One piece of evidence gets counted many times, so the trigger is basically always on. LuxAlgo calls independence the "binding design constraint" for this reason.

**What experienced discretionary traders do.** Brooks ties the exit to the trade's *premise*: exit when the reason for the trade is gone. Sometimes one strong opposite bar is enough. In a strong trend, he waits for 2-3 opposite bars or for structure to break, such as a trendline break and then a strong reversal bar. ([Brooks forum](https://www.brookstradingcourse.com/support-forum/09-pullbacks-and-bar-counting/confused-about-consecutive-bottom-attempts-in-a-bear-trend/)) In score terms, that means:
- a structure break (CHoCH, swing break) carries much more weight than a single candle;
- the exit bar rises when the trend is strong;
- several pieces of evidence have to stack up before you exit.

**Morris's bands** give the mechanism. Make the exit bar *deeper* than the entry bar, with a neutral zone in between, so the score has to move a long way before you're out.

**What's known about learned exits:**
- **Theory** (Kaminski & Lo, 2014). An exit rule can only add value if price has real follow-through or snap-back at that horizon. On a random walk, stopping out early can only lower your average result (it may lower swings). ([RePEc](https://econpapers.repec.org/RePEc:eee:finmar:v:18:y:2014:i:c:p:234-254))
  So we first need to test whether opposite signals during open trades predict *anything* about the next N bars. Only signals that pass deserve a weight.
- **The closest public test of a smart exit.** A model estimated, every bar, the odds of hitting the target first vs the stop first, and exited when holding no longer paid. It predicted outcomes 20% better than a time-only baseline. In a holdout-year backtest (costs not stated) it **raised win rate but lowered profit factor**, and both versions lost money. ([MQL5](https://www.mql5.com/en/articles/24106))
  This is the classic trap: early exits make you "right" more often while cutting your winners. A learned exit must be judged on net $, never on win rate.
- **Stops and exit triggers on trend systems** often add turnover and cost without adding edge (Clare et al., S&P 500). ([City Univ.](https://openaccess.city.ac.uk/id/eprint/17842)) They can still shrink the worst losses (Han, Zhou & Zhu, momentum crashes, before costs). ([CXO](https://www.cxoadvisory.com/technical-trading/stop-losses-to-avoid-stock-momentum-crashes/)) That matters for a prop drawdown limit even when the average trade doesn't improve.
- **"Exits matter more than entries"** comes from the Tharp/Basso random-entry test. The evidence is weaker than its reputation: secondhand, barely profitable, trending futures, trailing stops. ([Nasdaq](https://www.nasdaq.com/articles/revisiting-tom-basso-how-important-your-entry-forex-trading-part-1-2016-11-05)) It doesn't prove smart exits can rescue an entry with no edge. It does give us the right baselines: random entry with our exit, and our entry with random-time exit.
- **Reinforcement learning and deep "optimal stopping"** exist ([Becker et al.](https://jmlr.csail.mit.edu/papers/v20/18-232.html), [Zhang et al.](https://arxiv.org/abs/1911.10107)). They either use simulated data or lack clean after-cost out-of-sample results, and they overfit easily at this noise level. They are a later step, not a first one.

---

## 4. Meta-labeling and triple-barrier, mapped onto our setup

**The idea in one line:** keep your textbook rules as the thing that *proposes* a trade or an exit, and train a second model that answers *"how likely is it that acting on this one actually pays, given everything else on the chart right now?"* That likelihood is the confidence weight. ([Singh & Joubert, quoting López de Prado](https://hudsonthames.org/wp-content/uploads/2022/04/Does-Meta-Labeling-Add-to-Signal-Efficacy.pdf))

The method works best when the first-stage rule fires often and is right only part of the time; the second model then filters out the bad ones. That describes our patterns.

### Triple-barrier labels

Every candidate trade gets three "barriers":
- a **target** above;
- a **stop** below;
- a **time limit**.

Whichever is hit first decides the outcome. Our pullback study already does almost exactly this: continuation (leg high hit), failure (close below the pullback low), or neither within 40 bars / by 16:45 ET. To turn it into a training label, we add the entry, the stop 1 tick past the pullback low and the $2-3.50 cost. The label is **1 if the trade made money net of cost, otherwise 0**. Touches must be checked with 1-minute highs and lows, not closes.

### Entries

| Piece | What it is in our project |
|---|---|
| Primary signal (sets direction) | A textbook-direction pattern (bullish engulfing → long) or a pullback setup |
| The trade we simulate | Enter at the next bar's open, stop 1 tick past the pattern/pullback low, target and time limit fixed in advance |
| Label | 1 if net $ > 0 after costs, else 0 |
| Confidence model inputs | The pattern itself plus context: EMA 8/20/50 alignment, Momentum(14), VWAP side and distance, swing/Fib location, time of day, bar size vs recent bars, higher-timeframe trend, ES/NQ/YM agreement |
| Output | P(win) for this setup, right now |
| Decision | Take the trade only if expected $ = P(win) × avg win − (1 − P(win)) × avg loss − cost > 0 |

### Exits

The literature does not define this directly. It is our own extension of the method.

| Piece | What it is |
|---|---|
| Candidate exit moment | Each bar inside an open trade where opposite evidence appears (or every bar) |
| Label | 1 if exiting at this bar beat holding to the trade's planned stop, target or time exit, net of the extra cost; else 0 |
| Inputs | The opposite signals now firing (grouped into families) **plus trade state**: open profit in $ or points, bars in trade, distance to stop and target, time left to 16:45 |
| Output | P(exiting now is better) |
| Decision | Exit only when P clears a threshold chosen on net $. One weak opposite candle won't move P much; a CHoCH plus a bearish engulfing at a swing high against EMA 20 might |

This gives you Brooks's approach in a form we can test: "exit when the premise is gone, and it takes more evidence in a strong trend." The data sets how much each signal counts.

### Evidence on meta-labeling itself (thin)

- **Supportive.** On ES futures, a random-forest meta-model raised precision on a trend rule from 0.48 to 0.54 and on a mean-reversion rule from 0.17 to 0.20. ([Hudson & Thames](https://hudsonthames.org/does-meta-labeling-add-to-signal-efficacy/))
  *Weak:* one out-of-sample year, no costs, ordinary cross-validation, tuned until in-sample "looked acceptable", and vendor-affiliated. The authors themselves say a bad base rule "would likely only reduce the downside."
- **Negative.** An independent test on EURUSD with real spreads: meta-filtering cut trades from 576 to 121 and halved drawdown, but profit factor *fell* from 0.93 to 0.72. It was still losing. ([MQL5](https://www.mql5.com/en/articles/22274))
  Lower drawdown from trading less is not an edge.
- **Practitioner consensus.** Meta-labeling adds nothing if the second model sees the same information as the first. It helps most on top of rule-based or discretionary signals, which is our case, *if* it gets context the rule ignores. ([QuantConnect forum](https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/))
- I found **no peer-reviewed meta-labeling study on intraday index futures with costs included.** We would be doing a more rigorous version than what's published.

---

## 5. Pitfalls and the rules we must follow

1. **Data snooping is the main danger.** Every pattern, filter, timeframe, threshold and exit variant we try counts as another attempt.
   - Bailey et al.: with 5 years of data, about 45 tries are enough for a zero-skill strategy to *look* like a Sharpe of 1. ([paper](https://carmamaths.org/jon/backtest.pdf))
   - Sullivan, Timmermann & White: the best rule chosen by 1986 earned 2.8%/yr afterwards, which is not significant. On S&P futures no rule beat the benchmark. ([paper](https://www.fmg.ac.uk/sites/default/files/2020-11/dp303.pdf))

   **Rule:** keep a log of every configuration we try, fix the feature list before looking at results, and report results adjusted for the number of tries. Harvey, Liu & Zhu suggest wanting a t-statistic above 3, not 2. ([NBER](https://www.nber.org/papers/w20592))
2. **Overlapping trades leak information.** Pattern events cluster on consecutive bars, and a 40-bar label overlaps its neighbours. Ten engulfing bars on one trend day are not ten independent wins.
   **Rule:** walk forward by time (train through year Y, test on Y+1). Remove training trades whose windows overlap the test period, and leave a gap of at least one session between them. Down-weight overlapping events so they share one vote. ([López de Prado ch. 3, 4, 7 notes](https://reasonabledeviations.com/notes/adv_fin_ml))
3. **Only test new ideas on time periods the model has never seen.** Keep **Jan 2024 to 2026 locked away** and look at it once, at the end.
4. **Confidence numbers must mean what they say.** A threshold of "exit at 60%" only works if 60% really means 60%. Logistic regression is usually close to calibrated already. Gradient-boosted trees are not and need correcting on a separate later period. ([Niculescu-Mizil & Caruana](https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting)) Don't fix rare classes by oversampling, because that distorts the probabilities.
5. **Costs go into every label**, at $2-3.50 per micro round trip, including the extra cost of exits that lead to re-entries.
6. **Market behaviour drifts.** Predictability tends to fade: anomaly returns were 26% lower out of sample and 58% lower after publication. ([McLean & Pontiff](https://ideas.repec.org/p/zbw/iwqwdp/032016.html))
   **Rule:** refit every year, check that each weight keeps the same sign in most years (say 75% or more), include regime features (how volatile the day is, overnight gap), and plan on the live edge being 25-50% smaller than the backtest.
7. **Simple models first.** On tabular data like ours, tree models beat deep learning, and junk features (most of our 28 flags may be junk) hurt neural nets. ([Grinsztajn et al.](https://arxiv.org/abs/2207.08815)) Start with logistic regression, then shallow boosted trees, and skip deep learning and RL.
8. **Count trades, not bars.** We have millions of bars and hundreds of thousands of pattern events, but far fewer *independent* trades. As a rough guide (my judgment, not from a source), aim for at least 50-100 independent outcomes per weight we fit. Pooling MES, MNQ and MYM helps less than it looks: they move together, so the same pattern on the same bar in all three is close to one trade. Count effective trades, not rows.
9. **Feature-importance charts mislead when signals overlap** ([Hooker et al.](https://arxiv.org/abs/1905.03151)). We judge a signal family by whether removing it hurts out-of-sample $, and by whether its weight is stable year to year.

---

## 6. What I recommend we build

### Step 0: baselines and labels (needed before any ML)

- **Labels.** Build the trade labeler: entry, stop 1 tick past the low, a target and time limit fixed in advance, costs included. One label set for entries, one for exits.
- **Baselines that any weighting must beat:**
  - an **equal-weight vote** across signal families;
  - **random-time exits** with the same entry;
  - **random skipping** with the same number of trades (so "trading less" doesn't fool us);
  - fixed stop/target with no signal exits.

### Step 1: group the signals into families

Group the 28 patterns into a handful of families so the same evidence isn't counted many times, for example:
- reversal candles (engulfing, hammer/shooting star, pin bar, stars, tweezers);
- continuation (three soldiers/crows);
- range breaks (inside/outside bar breakouts, NR7);
- close-location extremes;
- structure (swing break / CHoCH);
- EMA location;
- momentum;
- VWAP;
- Fib zone.

Then run a simple screen: does each family, firing during an open trade, change what price does next? This is the Kaminski & Lo test.

### Step 2: regularized logistic regression, one model for entries and one for exits

The penalty pulls weak signals' weights toward zero unless the data clearly supports them. The result is a **readable weight table**. The example below is made up, only to show the format:

| Signal family (exit model, long trade) | Weight | Plain meaning |
|---|---|---|
| Close below last 5-bar swing low (CHoCH) | +0.45 | Strong evidence to exit |
| Bearish reversal candle *at a swing high* | +0.25 | Moderate |
| Bearish reversal candle mid-range | +0.02 | Basically noise |
| Close back through EMA 20 | +0.15 | Mild |
| Higher-timeframe trend still up | −0.30 | Evidence to *stay in* |
| Open profit already over 1R | +0.10 | Mild lean toward taking profit |

The weights add up into a score, which converts into a probability. You can read the table and argue with it the way you would with a trading plan.

### Step 3: shallow gradient boosting as a challenger

Use only shallow trees (depth 2-3), strongly limited and calibrated. Its job is to test whether *combinations* add value, such as "engulfing *and* at VWAP *and* in the first hour". We keep it only if it beats the logistic model on locked-away years, net of costs.

### Features

- all signal families, including from the 5/15/60-minute bars;
- EMA alignment and distance;
- Momentum(14);
- VWAP side and distance;
- distance to the nearest swing and Fib level;
- time of day;
- bar size compared with the last 20 bars (instead of ATR);
- overnight gap;
- ES/NQ/YM agreement;
- for exits, trade state as well.

Distances in points mean different things at MES 1,200 (2012) and 6,000 (2025). We'll express them relative to price or to recent bar size so one weight works across 16 years.

### Validation

- Expanding walk-forward by year, with the overlap removal and one-session gap described in section 5.
- 2024-2026 locked away.
- Every trial logged.
- A shuffled-label (permutation) test: if the model does about as well on scrambled outcomes, it learned nothing.
- Results adjusted for the number of tries.
- Weight stability year by year.

### How we judge success, at fixed size (1 micro)

1. **Net $ per trade after costs**, and how much cost per trade the edge could absorb before breaking even. As a reference point: risking 8 MES points ($40) for an 8-point target with $3 round-trip cost, you need a win rate of **53.75%** just to break even. That is already at the top of our single-pattern range.
2. Total net $, worst day, and maximum trailing drawdown compared with the prop firm's limits.
3. **Prop pass odds.** Replay the out-of-sample trades many times in shuffled order and count how often the account reaches the profit target before hitting the drawdown limit, compared with the baselines.
4. It must beat all the Step 0 baselines in the out-of-sample years, not just on the full history.

### Main risks

- **There may be no edge to find.** Fock et al. found none in intraday futures candles, and Mesfin found none on MNQ.
- Smarter exits that raise win rate but cut winners (the MQL5 result).
- Drawdown that looks better only because we trade less.
- Weights that drift over time.
- Overfitting from trying too many variants.

The plan above checks for each of these. If the result is "patterns carry almost no weight, but structure, trend and cross-market context do," that is still a usable answer. It tells us which parts of the textbook rules to keep.

---

### Sources to treat with caution

- Several key papers were read only as abstracts or summaries: Fock et al., Creamer & Freund net-of-cost results, the four journal papers on meta-labeling, Huddleston et al., Kaminski & Lo magnitudes, and the NDR thresholds.
- Meta-labeling's supporting evidence comes mostly from a vendor (Hudson & Thames).
- Applying meta-labeling to exits is our own extension, not a published method.
- Brooks's probabilities are his rules of thumb, not measurements.

---

# Reviewer's corrections and additions

A skeptical reviewer checked six key citations against their sources. Its corrections are already applied above. Its full notes, including additions the report missed, follow.


I checked six citations against their source pages: Mesfin, Huddleston, Hassanniakalager, the MQL5 survival-exit article, Creamer & Freund, and Duvinage et al. I also looked up Gao et al. to propose it as an addition. I did not open the other sources, and the DOIs in part B are given from memory.

## A. Corrections: claims that are wrong, overstated or wrongly sourced

1. **Hassanniakalager et al. (section 1b).** The report says the combined rules earned "about 3-4x the profit". The journal abstract says "up to five times", and the thesis says "up to four". Both are maxima, not typical results, so "up to 4-5x" should replace "about 3-4x".
   - The Sharpe figures (0.6 vs 0.2) come only from the thesis.
   - The rules were screened with a data-snooping test before they were combined.
   - The report presents adding up log-likelihood ratios (Naive Bayes) as the method that worked. The findings say Naive Bayes was the weakest combiner; model averaging and the other methods did better.
   - Sources: https://ideas.repec.org/a/eee/empfin/v63y2021icp230-251.html and https://eprints.gla.ac.uk/246954/2/246954.pdf

2. **Creamer & Freund (section 1c).** The report calls the 48.8% error over 840 days "the authors' own longer test". That figure comes from a working paper, "A boosting approach for automated trading" (a chapter of Creamer's 2007 Columbia PhD thesis, tested on MSFT in the PLAT competition). It is not from the 2010 Quantitative Finance paper, which covers 100 S&P 500 stocks over 2003-2005.
   - The report should attribute the figure to that working paper and say the net-of-cost results of the 2010 paper are unverified.
   - Source: https://c.mql5.com/forextsd/forum/174/a_boosting_approach_for_automated_trading.pdf

3. **MQL5 survival-exit test (section 3).** The report calls it "live-style out-of-sample trading". It was a MetaTrader Strategy Tester backtest on a holdout year, and the article never says whether spreads or commissions were included.
   - The entry lost money in both versions.
   - The survival exits traded more (2,037 trades vs 1,852).
   - Net results: -$16.9k vs -$15.8k.
   - Profit factor: 0.77 vs 0.84.
   - The prediction gain was a 20-22% better log-loss.
   - The conclusion still holds: win rate went up and profit factor went down. Only the framing needs fixing.
   - Source: https://www.mql5.com/en/articles/24106

4. **Huddleston, Liu & Stentoft (section 2).** The report says the useful inputs were "lead-lag between related instruments" and draws the lesson "ES/NQ/YM agreement may be worth more". That doesn't follow from the paper.
   - The predictors were lagged returns of the index's constituent stocks.
   - The predictability fell after decimalization.
   - The lesson that does follow is that the edge came from cross-sectional data we don't have, not from candles. ES/NQ/YM lead-lag at 1-minute resolution is a separate idea we would need to test ourselves.
   - Source: https://ideas.repec.org/a/oup/jfinec/v21y2023i2p485-527..html

5. **Mesfin (2026).** The target is a once-a-day direction call: will the session close more than 10 points above the 10:30 open? It is not a bar-by-bar entry or exit model, so it is only indirect evidence about entry and exit timing.
   - Every model scored below the 51.8% base rate.
   - The abstract says "four years", but the data runs 2021-2025.
   - Source: https://arxiv.org/abs/2605.17724

6. **Kaminski & Lo (section 3).** The report says "on a random walk, stopping out early can only lower your average result". That is true for stocks with positive drift measured against cash, which is their setup. For intraday futures with near-zero drift, the more precise statement is the optional stopping theorem:
   - If price is a martingale, no exit rule changes the expected gross P&L. An exit only changes the shape of results, trading win rate against average win, and each extra exit adds cost.
   - That is the mechanism behind the MQL5 result, and it is why a higher win rate from an exit is expected even when it means nothing.
   - The report should say this outright.

7. **"Two of the researchers proposed it independently" (section 4, exits).** This should be removed. The research threads were given the same prompt, so their agreement is not independent evidence.

8. **Pooling MES, MNQ and MYM (section 5, item 8).** These contracts are highly correlated, so pattern events on the same bar across the three are close to duplicates. Pooling does not triple the number of independent trades.
   - The rule should be to cluster or down-weight events by timestamp and by day across instruments, and to count effective trades, not rows.

9. **Calibration (section 5, item 4).** Strongly regularized logistic regression pulls its probabilities toward the base rate, so its confidence is understated. It needs the same check on a later held-out period, with reliability plots and Brier score, as the tree models.

10. **Breakeven example (section 6).** The 53.75% figure is right for $3 of commission alone. Adding 1 tick ($1.25) of slippage on the stop raises breakeven to about 54.5%. Stop orders in fast markets slip, and the report's $2-3.50 covers commission only. Slippage should be modelled on its own: 1 tick is $1.25 on MES, $0.50 on MNQ and $0.50 on MYM.

11. **Prop pass odds (section 6).** "Replay the trades in shuffled order" breaks up the clustering of losing days, which overstates pass rates.
    - Use a block bootstrap by day.
    - If the firm's trailing drawdown counts unrealized P&L, the simulation needs each trade's worst open loss, not just its closed result.

## B. Gaps that matter for this design

1. **Look-ahead leakage is missing from section 5, and it is the biggest practical risk for an ML version.**
   - Fractal swing highs and lows, CHoCH, Fibonacci levels of swing legs and "pullback known" are only confirmed some bars after the fact.
   - 5/15/60-minute patterns are only known once that bar closes.
   - Every feature must carry the timestamp at which it became known. A shifted-feature test (lag every feature one extra bar; if results barely change, that's fine, and if they collapse, something is leaking) should be part of the protocol.

2. **Same-bar ties.** When one 1-minute bar touches both the stop and the target, the labeler must assume the stop was hit first, or use tick data. The same applies when the entry bar's open is already past the stop.

3. **Forecast-combination puzzle and unit weights.** Estimated weights often fail to beat a simple equal-weight average out of sample.
   - Dawes (1979): unit weights do nearly as well as regression weights. https://doi.org/10.1037/0003-066X.34.7.571
   - Smith & Wallis (2009) and Claeskens et al. (2016). https://doi.org/10.1016/j.ijforecast.2015.12.005
   - Implication: shrink the learned weights toward the equal-weight family vote, not toward zero, and treat that vote as the main baseline to beat. This is the most relevant missing body of evidence for a confidence-weighting system.

4. **Credit-risk scorecards are the established industry version of "confidence points".** Logistic regression with weight-of-evidence binning is scaled into integer points per signal, with a cutoff score. The user could read a table like "bearish engulfing at swing high = +12".
   - Reference: Siddiqi, *Credit Risk Scorecards* (Wiley). The report uses the phrase "weight of the evidence" but never links it to this.

5. **Exits as optimal stopping by regression (Longstaff & Schwartz 2001).** At each bar, regress the realized remaining $ of holding on the current state (opposite-signal families plus trade state). Exit when the estimated value of continuing is below zero minus the exit cost.
   - This predicts the remaining dollars of holding, where the report's exit model predicts whether exiting beats holding. It avoids the MQL5 win-rate trap. https://doi.org/10.1093/rfs/14.1.113
   - Related: weight training labels by the size of P&L, or use cost-sensitive thresholds (Elkan 2001). https://cseweb.ucsd.edu/~elkan/rescale.pdf

6. **A principled basis for "exit needs more than entry".** Under transaction costs, the optimal policy has a no-trade band (Davis & Norman 1990; Gârleanu & Pedersen 2013, https://doi.org/10.1111/jofi.12080).
   - Concretely: enter when expected edge is above the cost, and exit only when expected edge of holding is below minus the cost.
   - That gives the entry/exit gap a basis in theory, where the report currently rests it on Morris's bands.

7. **The strongest intraday candlestick evidence is missing: Duvinage, Mazza & Petitjean (2013), Quantitative Finance 13(7).**
   - 83 candlestick rules on 5-minute data for the 30 DJIA stocks.
   - About a third beat buy-and-hold before costs, even at the strict Bonferroni level, but only a few survived costs.
   - Combined trading systems showed no outperformance after costs.
   - Under the SSPA data-snooping test, no single rule beat buy-and-hold.
   - This is the closest published match to the user's plan, and it is verified from the abstract, which makes it stronger support than the Fock et al. summary. https://ideas.repec.org/a/taf/quantf/v13y2013i7p1059-1070.html

8. **Intraday index predictors with real evidence, usable as context features.**
   - Gao, Han, Li & Zhou (2018, JFE): the S&P 500 ETF's first half-hour return predicts its last half-hour return (predictive R² about 1.6%), and more strongly on high-volatility days. https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414
   - Baltussen et al. (2021, JFE): the same effect in index futures, linked to hedging demand. https://doi.org/10.1016/j.jfineco.2021.04.029
   - These support time of day and session state as features better than candle shapes do.

9. **Lo, Mamaysky & Wang (2000).** Pattern signals change the spread and shape of returns more than their mean. That supports judging exit signals on drawdown and tail risk as well as on mean $. https://doi.org/10.1111/0022-1082.00265

10. **Selection bias in the exit model.** An exit model trained only on trades the entry model took inherits that model's quirks.
    - Train exits on a broad set of entries: all primary signals plus random entries.
    - Group the every-bar exit samples by trade so a single trade doesn't contribute dozens of near-duplicate rows.

11. **The trial count must include the work already done.** The single-pattern, filter and timeframe tests the user has already run count as attempts. They belong in the data-snooping adjustment, and if they touched the 2024-2026 data, that period is no longer clean.

Sources:
- [Hassanniakalager et al., IDEAS/RePEc](https://ideas.repec.org/a/eee/empfin/v63y2021icp230-251.html)
- [Hassanniakalager et al., Glasgow eprint](https://eprints.gla.ac.uk/246954/2/246954.pdf)
- [Creamer & Freund working paper](https://c.mql5.com/forextsd/forum/174/a_boosting_approach_for_automated_trading.pdf)
- [Creamer & Freund 2010, Quantitative Finance](https://ideas.repec.org/a/taf/quantf/v10y2010i4p401-420.html)
- [MQL5 survival-exit article](https://www.mql5.com/en/articles/24106)
- [Huddleston et al. 2023](https://ideas.repec.org/a/oup/jfinec/v21y2023i2p485-527..html)
- [Mesfin 2026, arXiv](https://arxiv.org/abs/2605.17724)
- [Duvinage et al. 2013](https://ideas.repec.org/a/taf/quantf/v13y2013i7p1059-1070.html)
- [Gao et al. 2018, Market intraday momentum](https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414)