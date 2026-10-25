"""Forecasting model definition, fitting, inference, and serialization."""
from pathlib import Path
from typing import Dict, Tuple, Optional, Union
import numpy as np
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from ..config import (
    BOOSTING_MAX_ITER,
    BOOSTING_LEARNING_RATE,
    BOOSTING_MAX_DEPTH,
    BOOSTING_MIN_SAMPLES_LEAF,
    BOOSTING_LOSS,
    RATED_POWER_KW,
    SAVED_MODELS_DIR,
)


def build_forecaster(seed: int = 0) -> HistGradientBoostingRegressor:
    """Builds a HistGradientBoostingRegressor matching the research report specification."""
    return HistGradientBoostingRegressor(
        max_iter=BOOSTING_MAX_ITER,
        learning_rate=BOOSTING_LEARNING_RATE,
        max_depth=BOOSTING_MAX_DEPTH,
        min_samples_leaf=BOOSTING_MIN_SAMPLES_LEAF,
        loss=BOOSTING_LOSS,
        random_state=seed,
    )


def compute_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, rated: float = RATED_POWER_KW
) -> Dict[str, float]:
    """Calculates MAE, RMSE, and normalized RMSE as percentage of rated capacity."""
    e = np.asarray(y_pred, dtype=float) - np.asarray(y_true, dtype=float)
    mae = float(np.mean(np.abs(e)))
    rmse = float(np.sqrt(np.mean(e ** 2)))
    nrmse = float((rmse / rated) * 100.0) if rated > 0 else 0.0
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "nrmse": round(nrmse, 2),
    }


def predict_power(model: HistGradientBoostingRegressor, X: np.ndarray) -> np.ndarray:
    """Generates wind power forecast clipped to physical operating bounds [0, RATED_POWER_KW]."""
    preds = model.predict(X)
    return np.clip(preds, 0.0, RATED_POWER_KW)


def save_model(model: HistGradientBoostingRegressor, model_name: str) -> Path:
    """Serializes model to designated artifacts directory."""
    path = SAVED_MODELS_DIR / f"{model_name}.joblib"
    joblib.dump(model, path)
    return path


def load_model(model_name: str) -> HistGradientBoostingRegressor:
    """Loads serialized model from artifacts directory."""
    path = SAVED_MODELS_DIR / f"{model_name}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model file {path} not found.")
    return joblib.load(path)
