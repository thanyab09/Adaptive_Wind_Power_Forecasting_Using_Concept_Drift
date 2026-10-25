"""Tests for sample weighting and cooldown enforcement in the adaptation controller."""
import numpy as np
import pytest
from backend.app.ml.adaptation_controller import (
    compute_sample_weights,
    AdaptationController,
)


def test_recency_and_drift_aware_weights():
    """Verify exponential recency decay and pre-change downweighting."""
    lo, hi = 0, 672
    half_life = 336.0
    tau = 500
    pre_weight = 0.08

    weights = compute_sample_weights(lo, hi, half_life=half_life, tau=tau, pre_weight=pre_weight)

    # Most recent sample (index 671) has age 0 -> weight = 1.0
    assert pytest.approx(weights[-1], 0.01) == 1.0

    # Sample exactly half_life (336 hours) before hi has unscaled weight = 0.5
    # Since 336 hours before 672 is step 336, and 336 < tau (500), it is scaled by 0.08:
    assert pytest.approx(weights[336], 0.01) == 0.5 * 0.08

    # Post-change sample (e.g. index 600 >= tau) should NOT be downweighted by pre_weight
    expected_w600 = 0.5 ** ((671 - 600) / half_life)
    assert pytest.approx(weights[600], 0.01) == expected_w600


def test_cooldown_enforcement():
    """Verify 48-hour refractory cooldown behavior."""
    controller = AdaptationController(cooldown=48)

    # Initial state: can retrain
    assert controller.can_retrain(100) is True

    # Simulate retrain event at hour 100
    controller.last_retrain_hour = 100

    # Within 48 hours (e.g. hour 110, 140, 147), cannot retrain
    assert controller.can_retrain(110) is False
    assert controller.cooldown_remaining(110) == 38
    assert controller.can_retrain(147) is False
    assert controller.cooldown_remaining(147) == 1

    # At or after hour 148, cooldown has elapsed and retraining is permitted
    assert controller.can_retrain(148) is True
    assert controller.cooldown_remaining(148) == 0
    assert controller.can_retrain(200) is True
