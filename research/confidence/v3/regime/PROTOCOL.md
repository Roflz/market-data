# How we choose test data: our protocol

Written 2026-11-09, around 14:50 MST. Everything here uses data from before the locked holdout only (cut-off 2025-06-30 18:00 ET).
Sources are rated **strong** (peer-reviewed, widely replicated), **moderate** (peer-reviewed but narrower, a practitioner journal, or our own analysis with caveats) or **weak** (preprint, disputed, or not checked this run).

Supporting files in this folder: `sources_window_selection.csv`, `sources_regime_matching.csv`, `break_test.py/.json`, `holdout_power.py/.json`, `pool_test.py/.log/_out.csv`, `regime_diag.py`, `eras.py`, `out/REGIME_TABLES.md` (plus the CSVs in `out/`), `pb_memory.py`, `pb_memory_tests.csv`, `pb_memory_by_year.csv`, `pb_tod_blocks.csv`, `pb_depth_since.csv`.

---

## 1. The honest answer: recent data only, all history, or older periods that look like today?

**Short version.** Your instinct is partly right, but the reason is not the one we assumed.

- **Our three edges really did switch on around 2017-2018.** A break test searched every possible date for the P1 daily P&L (in risk units) and picked **2017-05-17**. The p-value of **0.025** already allows for having searched all those dates. From 2018 on, the years look statistically alike (p = 0.69). So scoring rules mainly on 2018 onward is supported by evidence, not cherry-picked.
- **But the market's behaviour did not change much.** Over 15 years these stayed flat in ES, NQ and YM:
  - how much one 15-min or 60-min bar's direction carries into the next;
  - how often the EMA 8/20/50 stack is still lined up the same way an hour later (about 0.85 every year);
  - how often a pullback continues (about 0.50).

  A change-point search found **no break** in pullback continuation or EMA persistence for any of the three.
- **What did change is the size of moves compared with trading costs.** A typical daytime 15-min ES bar moved about 3.6x the round-trip cost of one MES trade in 2010-17, 9.6x in 2018-24 and about 15x in the last 12 months. For NQ the figure went from 6x to 30x to 51x. The breaks land at 2018Q1 and 2020Q1, the same time our edges appear. The likely story: in 2010-17, costs ate a small edge. **This is a hypothesis we have not yet tested** (experiment E1 below).
- **What the research says.** The peer-reviewed answer is not "use only recent data". It is: the right amount of history is a trade-off between old data that is out of date and too little data that is mostly luck. Settle it with a fixed, out-of-sample procedure, and prefer fading old data over deleting it (Pesaran & Timmermann 2007; Pesaran, Pick & Pranovich 2013; Clark & McCracken 2009; Inoue, Jin & Rossi 2017). Choosing a start year after seeing which years looked good is a known way to fool yourself (Rossi & Inoue 2012).
- **"Older periods that look like today" (regime matching).** There is some recent support (Mulliner, Harvey et al. 2025/26), but it covers monthly macro timing, not intraday futures. On our data it would mostly match on noise. The last four quarters before the holdout differ from each other about as much as random past quarters differ from them, and 2025Q2 (the tariff crash) looks nothing like 2024H2. Matching on volatility level and move-size-versus-cost is meaningful, because those are measured precisely. Matching on chart "behaviour" is not, at least with the variables we tried.

**Our verdict.**

| Choice | Verdict for us | Why |
|---|---|---|
| All history, unadjusted | No, as the main score | 2010-17 P&L is flat because costs were large relative to moves; it hides the current edge |
| 2018+ only (hard cut) | **Yes, as the main score for now** | The break is confirmed by a date-search test (p 0.025); 2018-25 is one homogeneous regime; about 7.5 years is enough for a Sharpe near 0.75 or more |
| 2010-17 | **Keep, as a stress tier** | Same behaviour as today; a rule must not lose badly there, but need not profit. If E1 shows the edge comes back once costs are scaled, promote it into the main data |
| Fading weights (half-life 2-4 years) | Yes, report alongside | The research-backed middle ground; costs sample size (half-life 3y leaves about 2,100 effective days of 3,876) |
| Regime-matched older periods | Only as a side check, not as a training filter | Recent quarters are not one steady state; matching would pick noise. Use the closest periods (2019Q2-2020Q2, 2015Q3-2016Q2, 2022Q4-2023Q1) as "looks like today" check sets |
| A 1-2 year recent window alone | No | Too small: it can only confirm a rule with an annual Sharpe of about 2 or more |

### How much data a rule needs (rule of thumb: years needed = (t / annual Sharpe)², treating the three tickers as one)

| Annual Sharpe of rule | Years for t = 2 ("probably real") | Years for t = 3 (strict) |
|---|---|---|
| 0.5 | 16.0 | 36.0 |
| 1.0 | 4.0 | 9.0 |
| 1.5 | 1.8 | 4.0 |
| 2.0 | 1.0 | 2.2 |
| 3.0 | 0.4 | 1.0 |

---

## 2. How to build the training data

1. **Window rule (pre-registered, not chosen by eye).**
   - Main score: 2018-01 to 2025-06.
   - Every rule is also reported under all of the following: all history; rolling 2, 3, 5 and 7 years ending 2025-06; fading weights with half-lives of 1, 2 and 4 years; and a 50/50 blend of the all-history and 2018+ estimates (Clark & McCracken 2009).
   - **A rule passes only if it is positive in most of these schemes**, not just the best one (Rossi & Inoue 2012).
2. **Fitted models** (anything with settings learned from data): the look-back length is itself a setting. An inner walk-forward loop picks among {expanding, 3y, 5y, since-2018, half-life 2y, half-life 4y} using only past data, and an outer loop scores it (Inoue, Jin & Rossi 2017). Averaging the options is an acceptable, often safer, alternative.
3. **Put every era on the same footing before comparing.**
   - Measure results in R (multiples of the risk taken) or in units of ATR or typical range, not raw dollars. Dollar P&L grows with the index price.
   - Apply costs at **today's cost-to-range ratio** when asking "does this behaviour carry an edge?". Use real historical costs only when asking "would it have made money then?".
4. **Measuring how similar a past day is to today**, if used as a feature or weight (never a filter that is tuned after seeing results):
   - Use only information from before that day: 20-day realised volatility, move size versus cost, EMA 20/50 slope (trend strength), overnight gap, recent range, NQ-ES correlation, volume.
   - Score each against its own trailing values (for example, the previous 2-3 years), never the full-sample average.
   - Leave a gap of at least 20 sessions before "today" when picking matches, so the best matches are not simply last week.
   - Fix the variables, k (the number of nearest days, with a minimum) and the distance measure in PREREG before running anything.
   - (Method copied from Mulliner et al. 2025/26, moderate; their gap rule was not confirmed, so we add our own.)
5. **Live regime labels**, if ever used: compute them online, from data up to that moment only, with a penalty against flip-flopping (jump model; Nystrup et al. 2020, Shu, Yu & Mulvey 2024). Never use a "smoothed" estimate, because it quietly uses future data.

---

## 3. Pooling ES, NQ and YM

**Answer: pool, but partially, and never count the three as three times the evidence.**

- **Research.** Pooling works when one mechanism drives all the instruments:
  - Moskowitz, Ooi & Pedersen 2012, Baltussen et al. 2021 and Montero-Manso & Hyndman 2021 (all strong) find that a single model across many series does as well as or better than separate models.
  - The modern method is **partial pooling**: estimate each ticker, then pull each estimate toward the group average by an amount the data decides (Jensen, Kelly & Pedersen 2023; Gelman et al. 2013; strong).
- **Our test** (15-min EMA pullbacks, 2018 to 2025-06-27, 12,267 events): the three are statistically indistinguishable.

| Measure | ES | NQ | YM | Pooled | Do they differ? (Cochran's Q p) | Share of spread that is real (I²) |
|---|---|---|---|---|---|---|
| Continuation rate | 50.9% | 49.8% | 50.9% | 50.5% | 0.59 | 0 |
| Outcome (pullback-depth units) | +0.082 | +0.056 | +0.048 | +0.062 | 0.80 | 0 |
| Outcome, 2023 only | +0.025 | +0.316 | +0.028 | +0.116 | 0.09 | 0.58 |

- **The three are not independent.** How much a pooled sample is really worth depends on what you measure:

| What is correlated | Correlation | Worth this many independent tickers |
|---|---|---|
| Same-day pullback win/loss | 0.34 average | about 1.8 |
| Same-day pullback outcome size | 0.48 average | about 1.5 |
| 15-min bar returns (direction signals firing together) | 0.92-0.98 | about 1.06 |

  About 28% of signal bars fire on two or more tickers at the same moment. So for direction signals, pooling barely adds evidence. For trade outcomes it adds roughly 50-80%. Either way, **the trading day is the unit for all error bars** (group or block-resample by date).
- **Recipe for each rule:**
  1. Convert net results to R, with costs converted to R per ticker (MYM's tick is coarse relative to its range).
  2. Compute each ticker's estimate with error bars grouped by day.
  3. Run Cochran's Q and I², overall and per year. With only 3 tickers these tests are weak, so "no difference" is not proof of "same".
  4. **Leave one ticker out**: build or tune the rule on two tickers and test it untouched on the third.
  5. Report the partially pooled per-ticker edge. Trade a ticker only if that edge, after costs, is positive.
- **Rule types.** Market-wide rules (expiry Friday, CPI/NFP fade) are natural candidates for pooling. The MNQ noise-band rule is named for one ticker, so pool it only if leave-one-ticker-out holds.
- **For real diversification of evidence**, we would need markets that do not move with the indexes (rates, energy, FX). Their behaviour may differ, and this is not planned.

---

## 4. Validation scheme

| Step | Data | Role |
|---|---|---|
| Discovery and selection | 2018-01 to 2025-06 | Main score. Forward-chaining walk-forward (always test on later data), with a 1-session gap at fold edges; purge only labels that span several days |
| Stress tier | 2010-06 to 2017-12 | Must not be significantly negative in R; need not be positive. Re-scored at today's cost-to-range (E1) |
| Recent validation window | the last 12-24 months before the holdout (2023-07 to 2025-06) | Rolling 12-month result for each rule must still be alive here (fluctuation check; Giacomini & Rossi 2010, Rossi 2021) |
| Overfitting diagnostic | inside 2018-25 only | CPCV / PBO (probability of backtest overfitting) when choosing among many rule variants; never the main score, because shuffled splits mix eras (Cerqueira et al. 2020; Bergmeir et al. 2018) |
| Locked holdout | 2025-06-30 18:00 ET to now (about 340 sessions) | Run the frozen final exam **once, with your approval**, as a tripwire: a net result at or below 0 is a real warning; "not confirmed" is the expected outcome even if the edge is real. Then release it to research |
| Confirmation | forward paper trading from 2026-11-10 | Planned looks with O'Brien-Fleming bounds (z 4.05 / 2.86 / 2.34 / 2.02), plus an optional early-stop monitor to drop a dead rule |
| Live alarm during the eval | live per-trade P&L | Page-Hinkley or CUSUM drift alarm as an "edge stopped working" warning (weak evidence; use as an alarm only) |

**Why the holdout cannot prove much by itself** (P1 = the three v3 rules combined, 1 micro, daily net P&L):

| History used to estimate the edge | Days | $/day | Daily Sharpe | Expected z on the 340-day holdout | Chance the holdout shows significance | Days needed for an 80% chance |
|---|---|---|---|---|---|---|
| 2010-25H1 | 3,876 | 10.75 | 0.073 | 1.35-1.59 | about 48% | 830-1,150 |
| 2018-25H1 | 1,935 | 21.30 | 0.104 | 1.93-2.27 | about 61-74% | 410-570 |
| 2022-25H1 | 901 | 27.00 | 0.107 | 1.98-2.29 | about 74% | 400-540 |
| 2010-17 | 1,941 | 0.24 | 0.007 | 0.12 | about 6% | no edge |

- Edges usually shrink after discovery: about 26-58% weaker (McLean & Pontiff 2016), and live strategies keep about half their backtest performance (Falck, Rej & Thesmar 2022). **Plan on a daily Sharpe of about 0.07, not 0.104.** At that level, an 80% chance of significance needs 1,100+ days. That is why the early-stop monitor matters.
- **Caution:** earlier archive runs already looked at the holdout months for these rules, so it is partly used up as a clean test (Dwork et al. 2015, "the reusable holdout"). Spend it once, then fold it into the research data. It is the closest data we have to today's market.

---

## 5. Pattern-persistence test: does recent structure predict the next pullback?

**Question tested.** Does the way the last few pullbacks turned out tell us how the next one will go?
- Data: every pre-holdout pullback in ES, NQ and YM at 15 min, and NQ at 5 and 60 min (50,730 events).
- Only past pullbacks whose full outcome window had already closed were used, so nothing was unknown at the time.

**Answer: no.**

| Market / timeframe | Base continuation | Last 3 good minus bad | Last 5 | Last 10 | Decoy (history from a random other day) |
|---|---|---|---|---|---|
| ES 15m | 43.1% | -2.5 pts (range -5.0 to -0.1) | -1.7 | +0.7 | about 0 |
| NQ 15m | 42.0% | +1.9 | +1.9 | +2.1 | about 0 |
| YM 15m (2018+) | 43.2% | -1.0 | +0.7 | -0.2 | about 0 |
| NQ 5m | 45.1% | -0.1 | +0.6 | +1.8 | about 0 |
| NQ 60m | 38.9% | +0.2 | +0.2 | +6.2 (p about 0.007, n 2,314) | about +1 |

- **No test survives correction for running 30 tests at once.** The year-by-year sign flips often (ES is negative in 12 of 16 years; NQ 15m is positive in 10 of 16), and the picture is the same in 2010-17 and 2018-25.
- **ES leans slightly the other way.** After recent successes, the next pullback continues a little less often and its best move is about 6% of the leg smaller.
- **The depth of recent pullbacks and the time since the last success add nothing.**
- **The 43% base here and the "about 0.50" in section 1 use different definitions.** Here a third outcome, "neither continued nor failed", is counted; section 1 counts only pullbacks that resolved one way or the other.

**Time of day matters much more** (2018-25H1, 15-min, out of 100 pullbacks: continue / fail):

| Block (ET) | ES | NQ | YM | Reading |
|---|---|---|---|---|
| 18:00-22:59 | 40 / 53 | 39 / 56 | 42 / 52 | worst block: early-evening pullbacks fail more often than they work |
| 23:00-02:59 | 46 / 54 | 48 / 52 | 51 / 48 | coin flip |
| 03:00-08:59 | 54 / 46 | 52 / 48 | 51 / 49 | biggest follow-through, but its window runs into the 09:30 open |
| 09:00-11:59 | 53 / 40 | 53 / 38 | 51 / 40 | **best balance**: "after the open settles" |
| 12:00-16:59 | 33 / 23 | 31 / 23 | 30 / 24 | most just stall, partly because of the 16:45 flat rule |

**What this means for your chart reading.**
- "The last few pullbacks worked, so take the next one" is not an edge in our mechanical pullback events.
- Your read probably uses more than that: trend strength, where price sits in its recent range, and agreement across 5/15/60-min. Those still need their own pre-registered tests (E4).
- Time of day is the stronger lead. Your MESZ6 example falls inside the locked holdout, so we cannot test it without spending the holdout.
- Only 137 ES events fall exactly in 09:30-10:30, so we cannot yet say whether the open itself behaves more extremely.

---

## 6. Experiment plan (run on pre-holdout data before adopting anything)

Ground rules for every experiment:
- Write the hypothesis, metric and pass bar into PREREG **before** running.
- Report every variant, not just the best.
- Use errors grouped by day, and block-resample by date in blocks of 20 sessions.
- Measure results in R after costs.
- Correct for the number of tests run (Holm correction across each experiment's variants).
- Run one heavy job at a time.

| # | Experiment | What to run | How to judge it | Guard against fooling ourselves |
|---|---|---|---|---|
| E1 | **Was 2010-17 flat only because of costs?** | Re-score the v3 rules on 2010-17 with costs scaled to today's cost-to-range ratio, and P&L in R / ATR units | If the gross edge in 2010-17 is positive and within the 2018+ confidence interval, old data becomes usable training data (main tier). If still flat, the break is behavioural and 2010-17 stays a stress tier | Fix the cost scaling formula first; report both real-cost and scaled-cost results |
| E2 | **Window comparison** | Each rule under: all history, rolling 2/3/5/7y, half-lives 1/2/4y, 50/50 blend, 2018+ | Count the schemes where the edge is positive and t > 1.5. Adopt a rule only if it is positive in at least 7 of 10. For fitted models, nested walk-forward picks the window; compare its out-of-sample loss with the blend | No picking the start year after the fact; the scheme list is fixed now |
| E3 | **Break test per rule and ticker** | Date-search break test (15% trimming, block permutation) on each rule's daily R, per ticker | The break dates should cluster (2017-2020) and match the cost-to-range breaks | A break date at a sample edge or disagreeing across rules means "no clean break" |
| E4 | **Multi-timeframe structure features** | Pre-register 3-5 features matching your reads: 60-min EMA stack agrees with the 15-min signal; price position in the 5-day range; 15-min trend slope; time-of-day block | Each feature's lift on continuation and net R, 2018+, with a stress check on 2010-17; must hold in at least 2 of 3 tickers (leave one ticker out) | Feature definitions are frozen before any outcome is seen; at most 5 features; Holm correction |
| E5 | **Time-of-day filter** | Skip 18:00-22:59, favour 03:00-11:59, compared on a **common exit window** (fixed bars, same flat rule) | Net R per trade and per day improves in both halves (2010-17, 2018+) and in each ticker | Equalise outcome windows first; the current block differences are partly mechanical |
| E6 | **Pooling per rule** | Q, I², leave-one-ticker-out and partially pooled per-ticker edge for each v3 rule | Pool if leave-one-ticker-out holds and the after-cost partially pooled edge is positive per ticker | Errors grouped by day; MYM costs in R |
| E7 | **Regime-matched check set** (optional) | Score rules on 2019Q2-2020Q2, 2015Q3-2016Q2 and 2022Q4-2023Q1 | Rule must not be negative there | Check sets fixed now; not used for tuning |
| E8 | **Holdout and forward test** | After E1-E6 are frozen: one holdout run (with approval), then forward paper trading | Section 4 bounds | One look only; no changes after seeing it |

---

## 7. Caveats

- **The cost explanation for the 2018 break is a hypothesis** until E1 runs. Rising index prices also make costs smaller relative to moves, so the two explanations overlap.
- **The 2018+ regime is one block of about 7.5 years.** It is one regime, not many independent examples. A brand-new kind of market (for example, the growth of same-day options) has no historical match. Research on same-day options is mixed and weak.
- **Quarterly diagnostics are noisy.** One quarter's 15-min autocorrelation has a standard error of about 0.025. The change-point search is a simple level-shift search and can miss gradual drift. The similarity score uses 6 hand-picked variables, equally weighted.
- **Recent pooled pullback continuation rose** (0.527 in 2023-25H1 against 0.495 in 2018-22; naive z about 3.4). The three tickers overlap heavily, so it is weaker than it looks. It is a candidate, not a finding.
- **The pullback tests are before costs.** They depend on the 40-bar outcome window and the 16:45 flat rule.
- **The P1 Sharpe is helped by a few huge days** (the 10 best days are about 40% of profit), so skew-adjusted power numbers are optimistic. Use the conservative ones.
- **Weak or disputed sources, used only as context:**
  - "Pockets of Predictability" (Farmer, Schmidt & Timmermann 2023): disputed by a replication that found look-ahead.
  - Drift-detector papers: preprints, daily data.
  - Same-day options papers: working papers and a thesis.
  - Mulliner et al. 2025/26: practitioner journal, monthly data, before costs.
- **Some citations were given from memory and not re-checked this run:** Rossi & Inoue 2012; Giacomini & Rossi 2010; Killick et al. 2012; Lo & MacKinlay 1988.

### Sources

| Source | Year | Strength | Used for |
|---|---|---|---|
| Pesaran & Timmermann, J. Econometrics 137(1) | 2007 | strong | window trade-off; average across windows |
| Pesaran, Pick & Pranovich, J. Econometrics 177(2) | 2013 | strong | fading weights |
| Clark & McCracken, Int. Economic Review 50(2) | 2009 | strong | blending all-history and recent estimates |
| Inoue, Jin & Rossi, J. Econometrics 196(1) | 2017 | strong | choosing the window by out-of-sample loss |
| Rossi & Inoue, J. Business & Economic Statistics 30(3) | 2012 | strong | report results across all windows |
| Rossi, J. Economic Literature 59(4) | 2021 | strong | instability; fluctuation checks |
| Giacomini & Rossi, J. Applied Econometrics | 2010 | strong | fluctuation test |
| Andrews, Econometrica; Bai & Perron, Econometrica | 1993/1998 | strong | break test at an unknown date |
| Cerqueira, Torgo & Mozetic, Machine Learning 109 | 2020 | strong | forward-in-time validation beats CV when data drift |
| Bergmeir, Hyndman & Koo, Comp. Stat. & Data Analysis | 2018 | strong | limits of k-fold for time series |
| Arian et al., Knowledge-Based Systems | 2024 | moderate | CPCV as an overfitting diagnostic only |
| Bailey & Lopez de Prado (MinTRL, deflated Sharpe, PBO) | 2012-2017 | strong / moderate | track-record length, overfitting |
| Dwork et al., Science | 2015 | strong | every look uses up the holdout |
| O'Brien & Fleming 1979; Lan & DeMets 1983; Wald 1945; Howard et al. 2021; Ramdas et al. 2023 | 1945-2023 | strong | forward-test stopping bounds |
| McLean & Pontiff, J. Finance 71(1) | 2016 | strong | edge decay |
| Falck, Rej & Thesmar, Quantitative Finance 22(11) | 2022 | moderate | live strategies keep about half their edge |
| Lo, J. Portfolio Management 30(5) | 2004 | moderate | edges come and go |
| Mulliner, Harvey, Xia, Fang & van Hemert, "Regimes", J. Portfolio Management | 2025/2026 | moderate | similarity-based period selection |
| Nystrup, Lindstrom & Madsen, Expert Systems w/ Applications 150 | 2020 | strong | persistent regime labels |
| Shu, Yu & Mulvey, J. Asset Management 25(5) | 2024 | moderate | online regime gating out of sample |
| Adams & MacKay 2007; Killick, Fearnhead & Eckley, JASA 2012 | 2007/2012 | moderate | online and offline change points |
| Moskowitz, Ooi & Pedersen, J. Financial Economics 104(2) | 2012 | strong | pooling futures after volatility scaling |
| Baltussen, Da, Lammers & Martens, J. Financial Economics 142 | 2021 | strong | intraday momentum across 60+ futures; hedging mechanism |
| Gao, Han, Li & Zhou, J. Financial Economics 129(2) | 2018 | strong | market intraday momentum |
| Montero-Manso & Hyndman, Int. J. Forecasting 37(4) | 2021 | strong | global vs per-series models |
| Sirignano & Cont, Quantitative Finance 19(9) | 2019 | strong | pooled model beats per-stock models |
| Jensen, Kelly & Pedersen, J. Finance 78(5) | 2023 | strong | partial pooling |
| Higgins & Thompson 2002; von Hippel 2015 | 2002/2015 | strong | Q and I², weak with few groups |
| Kish, Survey Sampling | 1965 | strong | effective sample size with correlation |
| Asness, Chandra, Ilmanen & Israel, J. Portfolio Management 43(5) | 2017 | moderate | timing overlays often add little after costs |
| Kanas 2003; Panagiotidis 2010 | 2003/2010 | weak | chart-pattern matching mostly fails out of sample |
| Farmer, Schmidt & Timmermann, J. Finance 78(3) | 2023 | weak (disputed) | pockets of predictability |
| Concept-drift papers (Frontiers in AI 2022; Neri 2021 preprint) | 2021-2022 | weak | live drift alarms |
