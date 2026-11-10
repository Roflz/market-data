# Next steps (agreed or proposed), as of 2026-11-09

## Finish v1
1. Resume the paused pipeline: finish the NQ boosting, YM and exit models, write REPORT.md with Lucid pass odds, and run the audit (leakage check, labels recomputed by hand).
2. Rerun the earlier pattern stats, exit study and galleries with the fixed detector (no patterns on flat bars).

## Weighting approaches
3. Run every approach on the same folds and compare in $: hand-set (Bulkowski, Morris, Ned Davis), statistical (screen + Bayesian model averaging, naive Bayes, weight-of-evidence scorecard, shrinkage), ML, and ML started from a prior.
4. Your own weights: fill in approaches/user_weights.csv.
5. Finish the independent review of the ML module, which was skipped to save tokens.

## Published-method gaps (López de Prado)
6. Combinatorial purged cross-validation (CPCV) alongside walk-forward.
7. His random forest with the sequential bootstrap.
8. Feature importance by MDA and SFI under purged validation.
9. Deflated Sharpe ratio and probability of backtest overfitting.
10. Labels: add a $-weighted or $-amount model next to the yes/no label.

## Features
11. Test feature blocks A to L (FEATURE_RESEARCH.md) one at a time against v1; keep a block only if out-of-sample $ improves. Blocks: multi-horizon returns, range position, volatility and cost-in-bars, session and time of day, trend quality and EMA-cross timing, volume, cross-market, prior-candle shapes, VWAP events, recent pattern history, earlier signal confidences, regime proxies.

## Entry triggers (beyond candles)
12. Pullback triggers: H1/H2 bar counting (Al Brooks) inside a real trend (swing structure, higher lows held).
13. Structure triggers: swing breaks and changes of character (BOS/CHoCH), level reclaims; maybe EMA/VWAP/momentum crosses and time-of-day triggers.
14. Tag each candidate with its trigger so the model learns which triggers work in which context.
15. Rebuild the pullback detector: real trend required, minimum leg size, pullback weaker than the impulse, H1/H2 entry.

## Trade management (replace v1's fixed placeholders)
16. Stop loss chosen by ML: label each trade under several stop placements and learn the best one per setup.
17. No fixed target: exits from the exit model (weighted opposite evidence, exiting needs more evidence than entering), plus trailing and structure exits.
18. Remove the 4-hour time limit once exits are model-driven.
19. Adds on pullbacks with a breakeven stop.
20. Stronger "after a decline / after a rise" context for the candle patterns; compare against the current loose version.

## Evaluation
21. Judge everything in net $ per micro after costs, by year on unseen data, plus Lucid pass odds simulated in whole-day blocks. Keep July 2025 onward locked until the end.
