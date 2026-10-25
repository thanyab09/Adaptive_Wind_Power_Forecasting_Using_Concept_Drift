"""Reproducible experiments and sensitivity analysis endpoints."""
from fastapi import APIRouter, HTTPException, Query
from ..schemas.schemas import ExperimentJobRequest, ExperimentJobStatusResponse
from ..services.experiment_service import experiment_service

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/run")
def run_experiment(req: ExperimentJobRequest):
    """Enqueues an asynchronous reproducible experiment run."""
    job_id = experiment_service.start_experiment_job(
        seed=req.seed,
        drift=req.drift,
        magnitude=req.magnitude,
        detector=req.detector,
    )
    return {
        "status": "queued",
        "job_id": job_id,
        "message": f"Experiment job {job_id} successfully queued.",
    }


@router.get("/status/{job_id}", response_model=ExperimentJobStatusResponse)
def get_job_status(job_id: str):
    """Polls progress and results for an experiment job."""
    job = experiment_service.get_job_status(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return ExperimentJobStatusResponse(
        job_id=job["job_id"],
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        result=job.get("result"),
    )


@router.get("/benchmark")
def get_benchmark_results(scenario: str = Query(default="drift", pattern="^(drift|nodrift)$")):
    """Returns the comprehensive 10-seed evaluation table from the project report."""
    return experiment_service.get_benchmark(scenario)


@router.get("/sensitivity")
def get_sensitivity_analysis():
    """Returns sensitivity curves for threshold lambda, cooldown, window, magnitude, and detectors."""
    return experiment_service.get_sensitivity()
