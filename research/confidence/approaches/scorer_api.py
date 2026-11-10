"""
Common interface for every confidence-weighting approach (hand-set, statistical, machine-learned), so the walk-forward
harness (../walkforward.py) can fit and compare them on identical folds, trades and $ scoring.

Data the harness passes in (one row per candidate: an entry event, or an exit row of an open trade):
  X     DataFrame of features, ALREADY ORIENTED by trade direction: every signed column (features.SIGNED) has been
        multiplied by d, so + always means "with the trade" (bullish pattern on a long, bearish pattern on a short).
        Column names follow ../SPEC.md (pat_<name>, fam_*, dist_swhi_5, brk_5, struct_5, ema_stack, mom, dist_vwap,
        tod_*, h1_*, x_<SYM>_*, ... and for exit rows the trade state: open_R, mfe_R, mae_R, bars_held,
        dist_stop_R, mins_to_1645).
        For EXIT rows the orientation is the same (+ = with the open trade), so a high exit-confidence means
        "evidence against the trade" -> the scorer learns/sets NEGATIVE weights on with-trade evidence.
  y     0/1 numpy array. Entries: y = 1 if the trade made money after costs (primary label y_1.5). Exits: y = 1 if
        exiting at the next bar's open beat holding (y_exit).
  w     sample weights (uniqueness x cross-market), or None.
  meta  DataFrame aligned with X: t (signal timestamp), t_end (label end timestamp), d (+1/-1), market, year,
        pnl_usd (net $ of the labelled trade, entries) or exit_gain_usd (exits), trade_id (exits).
        Approaches may use meta for screening by $ (e.g. data-snooping tests on per-signal $), never as features.
  task  "entry" or "exit".

Every approach is a class with this interface:
"""
from __future__ import annotations

import numpy as np
import pandas as pd


class Scorer:
    name = "base"          # short unique id, e.g. "hand_bulkowski", "stat_nb_woe", "ml_afml_rf"
    family = "base"        # "hand" | "stat" | "ml" | "prior_ml"
    source = ""            # citation(s) of the published method it follows

    def __init__(self, task: str = "entry", **params):
        self.task = task
        self.params = params

    def fit(self, X: pd.DataFrame, y: np.ndarray, w: np.ndarray | None = None, meta: pd.DataFrame | None = None):
        """Learn (or, for fixed hand weights, only calibrate) using TRAINING rows only. Return self."""
        raise NotImplementedError

    def score(self, X: pd.DataFrame) -> np.ndarray:
        """Raw confidence score (higher = more confident). For linear approaches this is the log-odds-like sum of
        weights x features; used as a PRIOR / offset by the prior-informed ML variants."""
        raise NotImplementedError

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Calibrated P(y = 1) in [0, 1]. Approaches whose raw score is not a probability (hand-set points) must map
        score -> probability with a monotone calibration (Platt or isotonic) fitted inside fit() on TRAINING rows."""
        raise NotImplementedError

    def weights_table(self) -> pd.DataFrame | None:
        """Readable weights: columns signal, weight, points (credit-scorecard scaling: points = weight / (ln 2 / 20),
        i.e. +20 points doubles the odds, when the weight is in log-odds units; otherwise the approach's own points),
        meaning (plain English), source (where the number came from). None if not applicable (e.g. tree ensembles:
        give feature importances instead, flagged as such)."""
        return None


def platt(score_train: np.ndarray, y: np.ndarray, w: np.ndarray | None = None):
    """Fit P(y=1) = sigmoid(a * score + b) on training rows; returns a callable score -> probability."""
    from sklearn.linear_model import LogisticRegression
    s = np.asarray(score_train, float).reshape(-1, 1)
    m = LogisticRegression(C=1e6, max_iter=1000).fit(s, y, sample_weight=w)
    return lambda sc: m.predict_proba(np.asarray(sc, float).reshape(-1, 1))[:, 1]


REGISTRY: dict[str, type] = {}


def register(cls):
    """Decorator: approach modules register their Scorer classes so the harness can list and build them."""
    REGISTRY[cls.name] = cls
    return cls
