"""Main FastAPI application entrypoint."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.health import router as health_router
from .api.dashboard import router as dashboard_router
from .api.data import router as data_router
from .api.forecast import router as forecast_router
from .api.drift import router as drift_router
from .api.adaptation import router as adaptation_router
from .api.models import router as models_router
from .api.experiments import router as experiments_router
from .api.reports import router as reports_router
from .ml.dataset_manager import dataset_manager
from .services.simulation_service import simulation_service

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("wind_forecast_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown procedures."""
    logger.info("Initializing Adaptive Wind Power Forecasting Backend...")
    # Preload default dataset and baseline simulation state
    try:
        dataset_manager.load_synthetic(seed=0, drift=True, magnitude=1.0)
        simulation_service.init_simulation()
        logger.info("Default synthetic dataset and simulation state ready.")
    except Exception as ex:
        logger.error(f"Error during application startup: {ex}")
    yield
    logger.info("Shutting down Adaptive Wind Power Forecasting Backend.")


app = FastAPI(
    title="Adaptive Wind Power Forecasting API",
    description="REST backend for one-hour-ahead wind power forecasting with Page-Hinkley concept drift detection and adaptive retraining.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for local React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(forecast_router, prefix="/api")
app.include_router(drift_router, prefix="/api")
app.include_router(adaptation_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(experiments_router, prefix="/api")
app.include_router(reports_router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint providing project overview and documentation links."""
    return {
        "project": "Adaptive Wind Power Forecasting Using Concept Drift Detection",
        "institution": "Panimalar Engineering College (Anna University)",
        "authors": ["Thanya B", "Thejessri S"],
        "status": "online",
        "docs_url": "/docs",
        "health_check": "/api/health",
        "dashboard_summary": "/api/dashboard/summary",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Clean global exception handler preventing leaking internal stack traces."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred. Please verify your request parameters."},
    )
