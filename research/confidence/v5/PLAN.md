# v5 PLAN - volatility-forecast sizing vs fixed sizing for the proven rules (frozen before any eval)

Written 2026-11-09 ~17:10 MST, before any eval of any sizing policy. sha256 recorded in v5/out/PLAN.sha256.
Question: does sizing each trade from a FORECAST OF MOVE SIZE raise LucidFlex 25K eval pass odds and shorten time to
pass for P1 = A1 + A3 + A4 (and for A1 alone) versus fixed sizing, by more than zero-timing-edge twins would by chance?
Every choice below names its published source, or is marked **[OUR ASSUMPTION]**.

## 1. Data (holdout untouched)
- Trades: v5/out/trades_vol.parquet (A1 1,640 MNQ, A3 270 = 90 each MES/MNQ/MYM, A4 178 MNQ), sessions
  2018-01-02 .. 2025-06-27, net $ per micro after costs, forecasts known at entry. Nothing at/after 2025-06-30 18:00.
- Calendar: v3 protocol calendar (v3/out/daily/A1.csv sessions <= 2025-06-27), from 2018-01-01.
- Eval: v2/eval_sim.py rules (LucidFlex 25K: +$1,250 target, $1,000 EOD trailing drawdown locking at $25,100, $600
  daily limit = no new trade once the day's realized P&L <= -$600 and day floored at -$600, max 20 open micros,
  flat 16:45-18:00), prop_sim.run_starts from every start day. Sizing loop = eval_sim.size_trades with a per-trade
  wanted-micros array (identical code path; checked to reproduce eval_sim for FIXED before use).

## 2. Forecast (chosen by documented out-of-sample quality on 2018-2021 trades ONLY)
Criterion: highest Spearman correlation between the forecast and the realized window SD (sqrt of 5-minute realized
variance over [entry, scheduled end); realized variance per Andersen, Bollerslev, Diebold & Labys 2003, Econometrica
71(2)), 2018-2021 trades, among the v5 prep candidates. **[OUR ASSUMPTION: Spearman vs realized window SD as the
selection metric.]** Result (computed 2026-11-09 from trades_vol.parquet, 2018-2021 only):

| rule | chosen forecast s_t | 2018-21 Spearman | runner-up |
|---|---|---|---|
| A1 | v4 sigma x rv_60 (last-hour realized vol, 5-min mark <= entry) | 0.799 | rng_60 0.750, HAR-log x share 0.737 |
| A3 | sqrt(HAR-log daily RV x periodicity share 09:30-16:00) (Corsi 2009 JFEc 7(2); Andersen, Bollerslev & Diebold 2007 REStat 89(4); Andersen & Bollerslev 1997 JEF 4) | 0.829 | HAR-levels 0.822 |
| A4 | v4 sigma x rv_240 (last-4-hour realized vol at 08:45) | 0.747 | HAR-log x share 0.720 |

A3 trades with no HAR forecast (13 MYM trades before Feb 2019) get n0 (fixed). s_t is a return-scale volatility;
policies use it relative to its own history within (rule, market), so its units cancel. For EV (policy 6) it is
converted to $ per micro: s$_t = s_t x entry_px x $/pt (MES 5, MNQ 2, MYM 0.5).
Note: the v4 last-hour/4-hour realized-vol features are our construction (realized volatility from intraday returns,
ABDL 2003); they win on the pre-declared criterion, not because a paper prescribes them.

## 3. Sizing policies (n = wanted micros per trade; integer by rounding to nearest, 0 = trade skipped, <= 20; then the
eval_sim open-micro cap and $600 rule). History statistics are EXPANDING over PRIOR trades of the same rule and
market (twins: of the same twin rep), never the full sample (Liu, Tang & Zhou 2019 JPM 46(1) look-ahead critique;
Bongaerts et al. 2020 use expanding history). Fewer than 20 prior trades -> n = n0. **[OUR ASSUMPTION: 20-trade
minimum; history starts 2018, far shorter than Bongaerts' >= 10 years.]**

| id | policy | formula | source |
|---|---|---|---|
| FIXED | fixed micros (control) | n = n0, n0 in {1,2,3,4,5,6,8,10} | baseline (Dubins & Savage 1965 / Browne 1997 for the size-vs-pass trade-off) |
| FIXRISK | fixed $ risk (v3 baseline) | n = floor(B / risk_usd), risk_usd = sd of the rule's per-micro net $ over its previous 100 trades (v3 synth_p1 definition), B in {100,150,250,400,600} | v3 baseline **[OUR ASSUMPTION, inherited from v3; fixed-fractional practice, no peer-reviewed source]** |
| VT | volatility targeting | n = round(n0 * sbar/s), sbar = expanding mean of s | Harvey et al. 2018 JPM 45(1); Barroso & Santa-Clara 2015 JFE 116(1); Zarattini, Aziz & Barbon 2024 SFI WP 24-97 (shares ~ target/sigma) |
| CVT | conditional vol targeting, both tails | if s >= expanding 80th pct or <= 20th pct: n = round(n0 * min(sbar/s, 2)); else n0 | Bongaerts, Kang & van Dijk 2020 FAJ 76(4) eq. 3 (quintiles); Lmax = 2 **[OUR ASSUMPTION]** |
| CVTDN | conditional, down-only | if s >= expanding 80th pct: n = round(n0 * min(sbar/s, 1)); else n0 | Bongaerts et al. 2020 high-vol leg only, leverage <= 1 **[OUR ASSUMPTION: the down-only variant is our combination]** |
| IV | inverse variance | n = round(c / s^2), c = n0 * mean_p(s) / mean_p(1/s) | Moreira & Muir 2017 JF 72(4); weak out of sample per Cederburg et al. 2020 JFE 138(1) |
| EV | edge-over-variance (Kelly shape) | muhat = a + b*s$ (expanding OLS of 1-micro net $ on s$ over prior trades of the rule, A3 pooled over markets, >= 50 prior trades else n0); w = max(muhat,0)/s$^2; n = round(n0 * w * mean_p(s$) / mean_p(w_p*s$)) | MacLean, Thorp & Ziemba 2010 QF 10(7) (Kelly/fractional Kelly); Browne 1997 MOR 22(2) (edge/variance allocation for reaching a goal) **[OUR ASSUMPTION: linear muhat, 50-trade minimum]** |

Risk matching (comparison rule step 1): every vol policy's constant is set on PRIOR trades so that its mean predicted
risk per trade, mean(n*s), equals FIXED n0's, mean(n0*s) (before rounding). Realized daily P&L sd is reported to show
how well this held. Step 2: sweep the overall level n0 (and B) and compare frontiers.
Not tested: cushion-proportional (Grossman & Zhou 1993) - sizing would depend on each account's own path, which the
every-start-day engine cannot do within the time budget. Declared here, not run.

## 4. Runs
- Portfolios: P1 = A1 + A3 + A4 (each trade sized on its own; open micros across markets share the 20 cap), and A1 alone.
- Real stream: every policy x level above.
- Twins: 200 C1 random-day twins (rep 0-199) = same rule, side, clock entry/exit marks, random session of the same
  year (v3 caches: exp_g1_noiseband/cache/twins_A1.parquet, exp_g3_expiry/cache/c1_A3_{ES,NQ,YM}_999.parquet;
  A4 regenerated with v3 g4lib.run_leg(R=200), as in v3 synth_p1). Each twin trade gets ITS OWN session's forecast at
  the same clock time (same feature definitions; A3 HAR-log x share rebuilt for every session with v5/vol.py
  functions) and its own expanding history; FIXRISK twins inherit the real trade's risk_usd (v3 convention).
  Twin levels: n0 in {1,2,3,5}, B in {150,250,400}.
- Windows: start days 2018+ (2018-01-01..2025-06-30) and 2022+ (2022-01-01..). Consistency 40% (Lucid) and 50% (check).

## 5. Metrics
pass %, bust %, open %, median trading days to pass, % passed within 5 / 10 / 20 trading days (eval_sim definitions),
worst day ($), daily Sharpe (mean/sd of daily P&L over the window's calendar; also x sqrt(252)), max drawdown ($, of
cumulative daily P&L over the window), daily P&L sd, $/day, mean micros, trades taken.

## 6. Decision rule (pre-declared)
Primary: P1, start days 2018+, consistency 40%, levels n0 = 3 and n0 = 5. For each X in {VT, CVT, CVTDN, IV, EV}
and metric m in {pass %, within-20 %}: D = m(X, n0) - m(FIXED, n0) on the real stream (paired, same start days).
1. Bootstrap p (one-sided, H0: D <= 0): stationary bootstrap over start days (Politis & Romano 1994 JASA 89), mean
   block 20 and 60 trading days, 2,000 resamples each, the larger p is used; 95% CI reported.
2. Twin p = (1 + #twin reps with D_twin >= D_real) / 201 - is the gain bigger than a zero-timing-edge stream gets
   from the same policy?
3. Family correction: Holm over the 5 policies x 2 levels x 2 metrics = 20 bootstrap p-values (Holm 1979; White
   2000 / Hansen 2005 SPA as the literature motivation for correcting a best-of search).
X "beats fixed sizing" only if, for some level, D > 0 with Holm-adjusted bootstrap p < 0.05 AND twin p < 0.05 for
pass % or within-20 %, and its bust % is not higher than FIXED's at that level by more than the 95% bootstrap CI
allows (CI of the bust difference must include 0 or be negative). Otherwise: fixed sizing stands.
Secondary (descriptive, no claim): 2022+ window, 50% consistency, A1 alone, other levels, frontiers (pass % vs
median days; within-20 vs bust), FIXRISK vs FIXED, and the diagnostic below.
Diagnostic (descriptive): per rule, 2018-2021 trades: mean 1-micro net $ and $/s$ by forecast quintile and OLS slope
of net $ on s$ - if the per-trade Sharpe rises with volatility (as Zarattini et al. 2024 report for SPY intraday
momentum vs VIX), inverse-volatility sizing is expected to cut the best trades.

## 7. Log
run_pipeline.log_trial(module='v5-sizing', ...) one row per policy (primary cell). Outputs in v5/out/sizing_*.csv.
