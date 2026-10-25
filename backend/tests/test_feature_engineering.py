"""Tests for feature engineering, cyclic encoding, and target leakage prevention."""
import numpy as np
import pytest
from backend.app.ml.preprocessor import compute_features
from backend.app.config import FEATURE_NAMES


def test_feature_matrix_dimensions():
    """Verify that compute_features outputs n rows and 10 columns."""
    n = 200
    dummy_data = {
        "p": np.random.uniform(0, 2000, n),
        "v": np.random.uniform(3, 20, n),
        "d": np.random.uniform(0, 360, n),
        "temp": np.random.uniform(5, 25, n),
    }
    X = compute_features(dummy_data)
    assert X.shape == (n, 10)
    assert len(FEATURE_NAMES) == 10


def test_cyclic_wind_direction_encoding():
    """Verify trigonometric continuity and sin^2 + cos^2 = 1."""
    dummy_data = {
        "p": np.zeros(360),
        "v": np.ones(360) * 10.0,
        "d": np.arange(360),
        "temp": np.ones(360) * 15.0,
    }
    X = compute_features(dummy_data)
    sin_col = X[:, 1]
    cos_col = X[:, 2]

    # Bounds [-1, 1]
    assert np.all(sin_col >= -1.0) and np.all(sin_col <= 1.0)
    assert np.all(cos_col >= -1.0) and np.all(cos_col <= 1.0)

    # Pythagorean identity
    sums = sin_col ** 2 + cos_col ** 2
    np.testing.assert_allclose(sums, 1.0, atol=1e-5)


def test_target_leakage_guard():
    """
    CRITICAL TEST: Verify no future information leaks into past or current features.
    Changing the target y at time step t+1 or t+10 must have ZERO effect on X[t].
    """
    n = 100
    p1 = np.ones(n) * 500.0
    p2 = np.copy(p1)
    # Alter future power at step 50
    p2[50:] = 1999.0

    d1 = {"p": p1, "v": np.ones(n) * 8.0, "d": np.ones(n) * 180.0, "temp": np.ones(n) * 15.0}
    d2 = {"p": p2, "v": np.ones(n) * 8.0, "d": np.ones(n) * 180.0, "temp": np.ones(n) * 15.0}

    X1 = compute_features(d1)
    X2 = compute_features(d2)

    # All feature rows strictly prior to step 50 (rows 0 to 49) must be identical
    np.testing.assert_array_equal(X1[:50], X2[:50])

    # At step 50, lag1 feature (index 4) should STILL reflect p[49] and be identical
    assert X1[50, 4] == X2[50, 4]
