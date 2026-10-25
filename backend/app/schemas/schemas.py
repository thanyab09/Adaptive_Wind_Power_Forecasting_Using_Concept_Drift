"""Pydantic models for API request and response validation."""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    app_version: str
    python_version: str
    dataset_mode: str
    dataset_name: str
    model_version: int
    uptime_seconds: float


class DashboardSummaryResponse(BaseModel):
    current_hour: int
    current_week: float
    model_version: int
    drift_status: str
    status_color: str
    latest_forecast_kw: float
    latest_actual_kw: float
    current_mae_kw: float
    current_rmse_kw: float
    current_nrmse_pct: float
    total_alarms: int
    total_retrainings: int
    cooldown_remaining_hours: int
    cooldown_active: bool
    last_alarm_hour: Optional[int]
    last_retrain_hour: Optional[int]
    dataset_mode: str
    dataset_name: str
    page_hinkley_stat: float
    page_hinkley_threshold: float
    weekly_trends: List[Dict[str, Any]]
    zoom_onset: List[Dict[str, Any]]
    alarms: List[Dict[str, Any]]


class SyntheticGenerateRequest(BaseModel):
    seed: int = Field(default=0, ge=0, le=999)
    drift: bool = True
    magnitude: float = Field(default=1.0, ge=0.0, le=3.0)


class DatasetPreviewResponse(BaseModel):
    dataset_name: str
    mode: str
    rows: int
    columns: List[str]
    preview_rows: List[Dict[str, Any]]
    summary_stats: Dict[str, Any]
    correlation_matrix: Dict[str, Any]
    power_curve_scatter: List[Dict[str, float]]
    wind_rose: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class ForecastSingleRequest(BaseModel):
    wind_speed: float = Field(..., ge=0.0, le=60.0)
    wind_direction: float = Field(..., ge=0.0, le=360.0)
    temperature: float = Field(..., ge=-50.0, le=60.0)
    power_lag_1: float = Field(default=500.0, ge=0.0)
    power_lag_2: float = Field(default=480.0, ge=0.0)
    power_lag_24: float = Field(default=520.0, ge=0.0)
    power_rolling_6h: float = Field(default=490.0, ge=0.0)
    wind_speed_lag_1: float = Field(default=7.5, ge=0.0)
    wind_speed_rolling_3h: float = Field(default=7.4, ge=0.0)


class ForecastSingleResponse(BaseModel):
    predicted_power_kw: float
    rated_capacity_kw: float
    capacity_factor_pct: float
    model_version: int
    confidence_interval: Dict[str, float]


class StepSimulationRequest(BaseModel):
    hours: int = Field(default=24, ge=1, le=168)


class StepSimulationResponse(BaseModel):
    current_hour: int
    current_week: float
    total_hours: int
    model_version: int
    cooldown_remaining_hours: int
    step_count: int
    step_events: List[Dict[str, Any]]
    total_alarms: int
    total_retrainings: int


class ManualRetrainRequest(BaseModel):
    reason: str = Field(default="Demonstration of manual model adaptation")


class ManualRetrainResponse(BaseModel):
    status: str
    model_version: int
    retraining_event: Dict[str, Any]


class ModelComparisonResponse(BaseModel):
    scenario: str
    rated_power_kw: float
    summary: Dict[str, Any]
    per_seed: List[Dict[str, Any]]
    statistical_tests: List[Dict[str, Any]]
    detection: Dict[str, Any]
    compute: Dict[str, Any]
    analytical_interpretation: str


class ExperimentJobRequest(BaseModel):
    seed: int = Field(default=0, ge=0, le=9)
    drift: bool = True
    magnitude: float = Field(default=1.0, ge=0.0, le=2.0)
    detector: str = Field(default="ph", pattern="^(ph|cusum|adwin|kspsi)$")


class ExperimentJobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None
