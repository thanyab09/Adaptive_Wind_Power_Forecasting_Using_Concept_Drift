"""Adaptation controller managing retraining windows, sample weights, and cooldown."""
import time
from typing import Optional, Dict, Any, List
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from ..config import (
    RECENCY_HALF_LIFE_HOURS,
    PRE_CHANGE_WEIGHT,
    COOLDOWN_HOURS,
    RETRAINING_WINDOW_HOURS,
)
from .forecaster import build_forecaster


def compute_sample_weights(
    lo: int,
    hi: int,
    half_life: float = RECENCY_HALF_LIFE_HOURS,
    tau: Optional[int] = None,
    pre_weight: float = PRE_CHANGE_WEIGHT,
) -> np.ndarray:
    """
    Computes sample weights combining:
      1. Exponential recency decay: 2^(-age / half_life)
      2. Drift-aware downweighting: samples before change point tau are scaled by pre_weight (0.08).
    """
    indices = np.arange(lo, hi)
    age = (hi - 1 - indices).astype(float)
    weights = 0.5 ** (age / half_life)

    if tau is not None:
        # Scale older concept regime observations
        weights = np.where(indices < tau, weights * pre_weight, weights)

    return weights


def fit_recent_model(
    seed: int,
    X: np.ndarray,
    y: np.ndarray,
    lo: int,
    hi: int,
    half_life: float = RECENCY_HALF_LIFE_HOURS,
    tau: Optional[int] = None,
    pre_weight: float = PRE_CHANGE_WEIGHT,
) -> HistGradientBoostingRegressor:
    """Trains a new HistGradientBoostingRegressor on recent rows lo..hi with drift-aware weights."""
    w = compute_sample_weights(lo, hi, half_life=half_life, tau=tau, pre_weight=pre_weight)
    model = build_forecaster(seed)
    model.fit(X[lo:hi], y[lo:hi], sample_weight=w)
    return model


class AdaptationController:
    """
    Manages model updates, enforcing the 48-hour refractory cooldown period,
    logging retraining events, and computing drift-aware sample weights.
    """
    def __init__(self, cooldown: int = COOLDOWN_HOURS, window_size: int = RETRAINING_WINDOW_HOURS):
        self.cooldown = cooldown
        self.window_size = window_size
        self.last_retrain_hour = -10 ** 9
        self.retraining_history: List[Dict[str, Any]] = []

    def can_retrain(self, current_hour: int) -> bool:
        """Returns True if cooldown period has elapsed since last retrain."""
        return (current_hour - self.last_retrain_hour) >= self.cooldown

    def cooldown_remaining(self, current_hour: int) -> int:
        """Returns hours remaining in current cooldown period, or 0 if ready."""
        elapsed = current_hour - self.last_retrain_hour
        return max(0, self.cooldown - elapsed)

    def retrain(
        self,
        current_hour: int,
        seed: int,
        X: np.ndarray,
        y: np.ndarray,
        tau: Optional[int],
        source: str = "error",
        notes: str = "",
    ) -> Tuple[HistGradientBoostingRegressor, float, Dict[str, Any]]:
        """
        Executes model retraining on the most recent window ending at current_hour.
        Returns (new_model, elapsed_seconds, event_record).
        """
        t0 = time.perf_counter()
        lo = max(0, current_hour + 1 - self.window_size)
        hi = current_hour + 1

        effective_tau = None
        if tau is not None:
            # Shift back 12 hours as safety margin before estimated change point
            effective_tau = max(tau - 12, 0)

        new_model = fit_recent_model(
            seed=seed,
            X=X,
            y=y,
            lo=lo,
            hi=hi,
            tau=effective_tau,
        )
        duration = time.perf_counter() - t0
        self.last_retrain_hour = current_hour

        event = {
            "hour": int(current_hour),
            "week": round(current_hour / 168.0, 2),
            "window_lo": int(lo),
            "window_hi": int(hi),
            "sample_count": int(hi - lo),
            "estimated_tau": int(tau) if tau is not None else None,
            "effective_tau": int(effective_tau) if effective_tau is not None else None,
            "source": source,
            "duration_sec": round(duration, 3),
            "notes": notes,
        }
        self.retraining_history.append(event)
        return new_model, duration, event
