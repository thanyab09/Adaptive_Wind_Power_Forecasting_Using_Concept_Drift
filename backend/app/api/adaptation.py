"""Adaptive learning and retraining controller endpoints."""
from fastapi import APIRouter
import numpy as np
from ..schemas.schemas import ManualRetrainRequest, ManualRetrainResponse
from ..config import (
    RETRAINING_WINDOW_HOURS,
    RECENCY_HALF_LIFE_HOURS,
    PRE_CHANGE_WEIGHT,
    COOLDOWN_HOURS,
)
from ..services.simulation_service import simulation_service
from ..ml.adaptation_controller import compute_sample_weights

router = APIRouter(prefix="/adaptation", tags=["Adaptation"])


@router.get("/status")
def get_adaptation_status():
    """Returns model version, cooldown state, and window configuration."""
    status = simulation_service.get_status()
    h = status["current_hour"]
    lo = max(0, h + 1 - RETRAINING_WINDOW_HOURS)

    return {
        "model_version": status["model_version"],
        "cooldown_remaining_hours": status["cooldown_remaining_hours"],
        "cooldown_active": status["cooldown_active"],
        "cooldown_period_hours": COOLDOWN_HOURS,
        "retraining_window_hours": RETRAINING_WINDOW_HOURS,
        "current_window": {"lo": lo, "hi": h + 1, "samples": (h + 1 - lo)},
        "recency_half_life_hours": RECENCY_HALF_LIFE_HOURS,
        "pre_change_weight_factor": PRE_CHANGE_WEIGHT,
        "total_retrainings": status["total_retrainings"],
        "last_retrain_hour": status["last_retrain_hour"],
    }


@router.get("/history")
def get_retraining_history():
    """Returns chronological audit log of all model retraining events."""
    history = simulation_service.retraining_history
    # If no live events yet, provide seed 0 historical retrainings from report
    if not history:
        default_events = [
            {"hour": 4720, "week": 28.10, "model_version": 2, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 4704},
            {"hour": 4771, "week": 28.40, "model_version": 3, "sample_count": 672, "duration_sec": 0.13, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 4747},
            {"hour": 4823, "week": 28.71, "model_version": 4, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 4799},
            {"hour": 4957, "week": 29.51, "model_version": 5, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 4933},
            {"hour": 5017, "week": 29.86, "model_version": 6, "sample_count": 672, "duration_sec": 0.11, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 4993},
            {"hour": 5072, "week": 30.19, "model_version": 7, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 5048},
            {"hour": 5257, "week": 31.29, "model_version": 8, "sample_count": 672, "duration_sec": 0.13, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 5233},
            {"hour": 6031, "week": 35.90, "model_version": 9, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 6007},
            {"hour": 8041, "week": 47.86, "model_version": 10, "sample_count": 672, "duration_sec": 0.12, "reason": "Drift alarm confirmed (Page-Hinkley)", "estimated_tau": 8017},
        ]
        return {"retrainings": default_events, "count": len(default_events)}

    return {"retrainings": history, "count": len(history)}


@router.get("/weights_curve")
def get_sample_weights_curve():
    """Generates sample weight points across the 672h retraining window."""
    w_recency = compute_sample_weights(0, 672, half_life=336.0, tau=None)
    w_drift_aware = compute_sample_weights(0, 672, half_life=336.0, tau=520, pre_weight=0.08)

    curve_data = []
    # Sample every 12 hours for smooth chart
    for i in range(0, 672, 12):
        curve_data.append({
            "hour_in_window": i,
            "age_hours": 672 - i,
            "recency_weight": round(float(w_recency[i]), 3),
            "drift_aware_weight": round(float(w_drift_aware[i]), 3),
            "is_estimated_change_point": bool(i == 520),
        })

    return {
        "curve": curve_data,
        "half_life_hours": 336.0,
        "pre_change_scale": 0.08,
        "simulated_tau": 520,
    }


@router.post("/retrain", response_model=ManualRetrainResponse)
def trigger_manual_retrain(req: ManualRetrainRequest):
    """Manually retrains the model on the most recent 672 hours with audit trail."""
    rec = simulation_service.manual_retrain(reason=req.reason)
    return ManualRetrainResponse(
        status="success",
        model_version=simulation_service.model_version,
        retraining_event=rec,
    )
