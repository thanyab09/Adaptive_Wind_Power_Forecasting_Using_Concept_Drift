"""Data ingestion, CSV upload, validation, and exploration endpoints."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from ..schemas.schemas import SyntheticGenerateRequest, DatasetPreviewResponse
from ..ml.dataset_manager import dataset_manager
from ..services.simulation_service import simulation_service

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/generate")
def generate_synthetic_data(req: SyntheticGenerateRequest):
    """Generates synthetic wind-farm dataset and updates active state."""
    meta = dataset_manager.load_synthetic(
        seed=req.seed,
        drift=req.drift,
        magnitude=req.magnitude,
    )
    simulation_service.init_simulation()
    return {
        "status": "success",
        "message": f"Generated synthetic dataset with Seed {req.seed} (Drift: {req.drift}, Magnitude: {req.magnitude}).",
        "metadata": meta,
    }


@router.post("/upload")
async def upload_dataset_csv(file: UploadFile = File(...)):
    """Uploads, validates, and activates a custom wind-farm CSV dataset."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files (.csv) are supported.")

    content = await file.read()
    if len(content) > 50 * 1024 * 1024:  # 50 MB limit
        raise HTTPException(status_code=400, detail="Uploaded file exceeds 50MB limit.")

    success, message, meta = dataset_manager.validate_and_load_csv(content, file.filename)
    if not success:
        raise HTTPException(status_code=422, detail=message)

    simulation_service.init_simulation()
    return {
        "status": "success",
        "message": message,
        "metadata": meta,
    }


@router.get("/preview", response_model=DatasetPreviewResponse)
def get_dataset_preview():
    """Returns dataset preview rows, summary stats, correlation matrix, and charts data."""
    if dataset_manager.df is None:
        raise HTTPException(status_code=404, detail="No active dataset available.")

    df = dataset_manager.df
    preview_rows = df.head(50).to_dict(orient="records")
    for r in preview_rows:
        if "timestamp" in r:
            r["timestamp"] = str(r["timestamp"])

    return DatasetPreviewResponse(
        dataset_name=dataset_manager.dataset_name,
        mode=dataset_manager.mode,
        rows=len(df),
        columns=list(df.columns),
        preview_rows=preview_rows,
        summary_stats=dataset_manager.get_summary_stats(),
        correlation_matrix=dataset_manager.get_correlation_matrix(),
        power_curve_scatter=dataset_manager.get_power_curve_scatter(sample_size=400),
        wind_rose=dataset_manager.get_wind_rose_data(num_sectors=16),
        metadata=dataset_manager.metadata,
    )


@router.get("/download")
def download_active_dataset():
    """Downloads active dataset as CSV."""
    csv_bytes = dataset_manager.export_csv_bytes()
    filename = "wind_farm_active_dataset.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
