"""Integration tests for all REST API endpoints using FastAPI TestClient."""
import io
import pandas as pd
import numpy as np
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify GET /api/health."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_version" in data
    assert data["dataset_mode"] in ["synthetic", "uploaded"]


def test_dashboard_summary_endpoint():
    """Verify GET /api/dashboard/summary."""
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "latest_forecast_kw" in data
    assert "current_mae_kw" in data
    assert data["drift_status"] in ["Stable", "Warning", "Drift Detected"]
    assert "weekly_trends" in data
    assert len(data["weekly_trends"]) > 0


def test_data_preview_endpoint():
    """Verify GET /api/data/preview."""
    response = client.get("/api/data/preview")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "preview_rows" in data
    assert "summary_stats" in data
    assert "power_curve_scatter" in data
    assert "wind_rose" in data


def test_data_generate_endpoint():
    """Verify POST /api/data/generate."""
    payload = {"seed": 1, "drift": True, "magnitude": 1.0}
    response = client.post("/api/data/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["metadata"]["seed"] == 1


def test_forecast_predict_endpoint():
    """Verify POST /api/forecast/predict."""
    payload = {
        "wind_speed": 10.5,
        "wind_direction": 225.0,
        "temperature": 18.0,
        "power_lag_1": 1200.0,
        "power_lag_2": 1150.0,
        "power_lag_24": 1100.0,
        "power_rolling_6h": 1180.0,
        "wind_speed_lag_1": 10.2,
        "wind_speed_rolling_3h": 10.1,
    }
    response = client.post("/api/forecast/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_power_kw" in data
    assert 0.0 <= data["predicted_power_kw"] <= 2000.0
    assert "confidence_interval" in data


def test_drift_status_endpoint():
    """Verify GET /api/drift/status."""
    response = client.get("/api/drift/status")
    assert response.status_code == 200
    data = response.json()
    assert "input_monitor" in data
    assert "ks_statistic" in data["input_monitor"]
    assert "psi_score" in data["input_monitor"]


def test_drift_simulation_step():
    """Verify POST /api/drift/simulate_step."""
    initial_status = client.get("/api/drift/status").json()
    start_hour = initial_status["current_hour"]

    response = client.post("/api/drift/simulate_step", json={"hours": 24})
    assert response.status_code == 200
    data = response.json()
    assert data["current_hour"] == start_hour + 24
    assert len(data["step_events"]) == 24


def test_model_comparison_endpoint():
    """Verify GET /api/model/comparison for both scenarios."""
    for sc in ["drift", "nodrift"]:
        response = client.get(f"/api/model/comparison?scenario={sc}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "static" in data["summary"]
        assert "adaptive" in data["summary"]
        assert "weekly" in data["summary"]
        assert "analytical_interpretation" in data


def test_report_pdf_download():
    """Verify GET /api/reports/pdf generates binary PDF."""
    response = client.get("/api/reports/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000
    # PDF magic byte signature %PDF-
    assert response.content[:4] == b"%PDF"
