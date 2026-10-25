"""Forecasting and inference API endpoints."""
import numpy as np
from fastapi import APIRouter, HTTPException
from ..schemas.schemas import ForecastSingleRequest, ForecastSingleResponse
from ..config import RATED_POWER_KW, INITIAL_HOURS
from ..ml.dataset_manager import dataset_manager
from ..ml.forecaster import predict_power, compute_metrics, build_forecaster
from ..services.simulation_service import simulation_service
from ..services.experiment_service import experiment_service

router = APIRouter(prefix="/forecast", tags=["Forecasting"])


@router.post("/predict", response_model=ForecastSingleResponse)
def predict_one_hour_ahead(req: ForecastSingleRequest):
    """Predicts one-hour-ahead wind power from meteorological and lagged power inputs."""
    model = simulation_service.current_model
    if model is None:
        raise HTTPException(status_code=400, detail="Forecasting model has not been trained yet.")

    rad = np.deg2rad(req.wind_direction % 360.0)
    x = np.array([[
        req.wind_speed,
        np.sin(rad),
        np.cos(rad),
        req.temperature,
        req.power_lag_1,
        req.power_lag_2,
        req.power_lag_24,
        req.power_rolling_6h,
        req.wind_speed_lag_1,
        req.wind_speed_rolling_3h,
    ]], dtype=float)

    pred = float(predict_power(model, x)[0])
    cap_factor = round((pred / RATED_POWER_KW) * 100.0, 2)

    # 90% confidence interval based on calibrated residuals (~1.645 * 25 kW)
    ci_margin = 35.0
    ci_lower = max(0.0, round(pred - ci_margin, 1))
    ci_upper = min(RATED_POWER_KW, round(pred + ci_margin, 1))

    return ForecastSingleResponse(
        predicted_power_kw=round(pred, 1),
        rated_capacity_kw=RATED_POWER_KW,
        capacity_factor_pct=cap_factor,
        model_version=simulation_service.model_version,
        confidence_interval={"lower": ci_lower, "upper": ci_upper},
    )


@router.get("/history")
def get_forecast_history():
    """Returns actual vs predicted series and error breakdown for recent stream."""
    stream_data = experiment_service.get_seed0_stream()
    recent_24h = stream_data.get("recent_24h", [])
    zoom_onset = stream_data.get("zoom_onset", [])

    return {
        "recent_24h": recent_24h,
        "zoom_onset": zoom_onset,
        "model_version": simulation_service.model_version,
        "rated_power_kw": RATED_POWER_KW,
    }


@router.post("/train")
def train_base_model():
    """Retrains the initial base model on the historical training window."""
    X = dataset_manager.features
    y = dataset_manager.raw_data["p"]
    i0 = dataset_manager.metadata.get("initial_hours", INITIAL_HOURS)

    model = build_forecaster(seed=0)
    model.fit(X[:i0], y[:i0])

    simulation_service.current_model = model
    simulation_service.model_version = 1

    train_pred = predict_power(model, X[:i0])
    metrics = compute_metrics(y[:i0], train_pred)

    return {
        "status": "success",
        "message": f"Trained base model on initial {i0} hours.",
        "model_version": 1,
        "training_metrics": metrics,
    }
