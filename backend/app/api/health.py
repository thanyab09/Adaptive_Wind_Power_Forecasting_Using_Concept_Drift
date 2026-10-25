"""Health and diagnostic endpoint."""
import sys
import time
from fastapi import APIRouter
from ..schemas.schemas import HealthResponse
from ..ml.dataset_manager import dataset_manager
from ..services.simulation_service import simulation_service

router = APIRouter(prefix="/health", tags=["Health"])

START_TIME = time.time()

@router.get("", response_model=HealthResponse)
def get_health():
    """Returns application status and diagnostic information."""
    return HealthResponse(
        status="healthy",
        app_version="1.0.0",
        python_version=sys.version.split()[0],
        dataset_mode=dataset_manager.mode,
        dataset_name=dataset_manager.dataset_name,
        model_version=simulation_service.model_version,
        uptime_seconds=round(time.time() - START_TIME, 1),
    )
