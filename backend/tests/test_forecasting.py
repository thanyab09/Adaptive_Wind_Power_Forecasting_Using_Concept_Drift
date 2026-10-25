"""Tests for HistGradientBoostingRegressor training, prediction, and metrics."""
import numpy as np
import pytest
from backend.app.ml.forecaster import (
    build_forecaster,
    compute_metrics,
    predict_power,
    save_model,
    load_model,
)
from backend.app.config import RATED_POWER_KW


def test_model_training_and_inference():
    """Verify forecaster trains, converges, and predicts valid physical power."""
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 10, size=(200, 10))
    y = np.clip(100.0 * X[:, 0] + rng.normal(0, 10, size=200), 0.0, RATED_POWER_KW)

    model = build_forecaster(seed=0)
    model.fit(X, y)

    preds = predict_power(model, X[:10])
    assert len(preds) == 10
    assert (preds >= 0.0).all()
    assert (preds <= RATED_POWER_KW).all()


def test_metric_calculations():
    """Verify MAE, RMSE, and nRMSE formulas."""
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 310.0])
    # Errors: +10, -10, +10 -> MAE = 10.0, RMSE = 10.0
    # nRMSE = (10 / 2000) * 100 = 0.5%
    metrics = compute_metrics(y_true, y_pred, rated=2000.0)
    assert metrics["mae"] == 10.0
    assert metrics["rmse"] == 10.0
    assert metrics["nrmse"] == 0.5


def test_model_serialization_roundtrip(tmp_path):
    """Verify model save and reload produces identical predictions."""
    rng = np.random.default_rng(1)
    X = rng.uniform(0, 10, size=(50, 10))
    y = np.clip(50.0 * X[:, 0], 0.0, RATED_POWER_KW)

    model = build_forecaster(seed=1)
    model.fit(X, y)
    original_preds = predict_power(model, X)

    # Save and reload
    save_path = save_model(model, "test_temp_model")
    reloaded_model = load_model("test_temp_model")
    reloaded_preds = predict_power(reloaded_model, X)

    np.testing.assert_array_almost_equal(original_preds, reloaded_preds)

    if save_path.exists():
        save_path.unlink()
