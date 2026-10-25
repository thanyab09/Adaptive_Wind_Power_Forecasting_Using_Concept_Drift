"""Report generation and export endpoints (PDF, CSV, JSON)."""
import io
import json
import pandas as pd
from fastapi import APIRouter, Response
from ..services.pdf_service import generate_project_summary_pdf
from ..services.experiment_service import experiment_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/pdf")
def export_pdf_report():
    """Generates and downloads a comprehensive technical report PDF using ReportLab."""
    pdf_bytes = generate_project_summary_pdf()
    filename = "Adaptive_Wind_Power_Forecasting_Report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/json")
def export_json_report():
    """Exports full benchmark results as structured JSON."""
    data = {
        "ten_seeds_drift": experiment_service.get_benchmark("drift"),
        "ten_seeds_nodrift": experiment_service.get_benchmark("nodrift"),
        "sensitivity": experiment_service.get_sensitivity(),
    }
    content = json.dumps(data, indent=2).encode("utf-8")
    filename = "wind_power_forecasting_results.json"
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/csv")
def export_csv_report():
    """Exports per-seed benchmark comparison as CSV."""
    drift_data = experiment_service.get_benchmark("drift")
    per_seed = drift_data.get("per_seed", [])
    df = pd.DataFrame(per_seed)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    content = buffer.getvalue().encode("utf-8")
    filename = "per_seed_drift_results.csv"
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
