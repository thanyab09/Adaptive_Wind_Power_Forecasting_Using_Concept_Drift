"""Dashboard overview API endpoints."""
from fastapi import APIRouter
from ..schemas.schemas import DashboardSummaryResponse
from ..services.simulation_service import simulation_service
from ..services.experiment_service import experiment_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    """Returns overview KPIs, trends, and alarms for the main dashboard."""
    status = simulation_service.get_status()
    stream_data = experiment_service.get_seed0_stream()

    weekly_trends = stream_data.get("weekly_trends", [])
    zoom_onset = stream_data.get("zoom_onset", [])
    alarms = stream_data.get("alarms", [])

    return DashboardSummaryResponse(
        current_hour=status["current_hour"],
        current_week=status["current_week"],
        model_version=status["model_version"],
        drift_status=status["drift_status"],
        status_color=status["status_color"],
        latest_forecast_kw=status["latest_forecast_kw"],
        latest_actual_kw=status["latest_actual_kw"],
        current_mae_kw=status["current_mae_kw"],
        current_rmse_kw=status["current_rmse_kw"],
        current_nrmse_pct=status["current_nrmse_pct"],
        total_alarms=status["total_alarms"],
        total_retrainings=status["total_retrainings"],
        cooldown_remaining_hours=status["cooldown_remaining_hours"],
        cooldown_active=status["cooldown_active"],
        last_alarm_hour=status["last_alarm_hour"],
        last_retrain_hour=status["last_retrain_hour"],
        dataset_mode=status["dataset_mode"],
        dataset_name=status["dataset_name"],
        page_hinkley_stat=status["page_hinkley_stat"],
        page_hinkley_threshold=status["page_hinkley_threshold"],
        weekly_trends=weekly_trends,
        zoom_onset=zoom_onset,
        alarms=alarms,
    )
