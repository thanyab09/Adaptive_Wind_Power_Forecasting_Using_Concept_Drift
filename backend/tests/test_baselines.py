"""Tests for Static, Weekly, and Adaptive model behavior and benchmarks."""
import pytest
from backend.app.services.experiment_service import experiment_service


def test_drift_benchmark_results():
    """Verify headline drift metrics match project report."""
    benchmark = experiment_service.get_benchmark("drift")
    assert "summary" in benchmark

    summary = benchmark["summary"]
    static_mae = summary["static"]["mae"][0]
    adaptive_mae = summary["adaptive"]["mae"][0]
    weekly_mae = summary["weekly"]["mae"][0]

    # Static error must be high (~134.7 kW)
    assert 130.0 <= static_mae <= 140.0

    # Adaptive error must achieve ~75% reduction (~33.7 kW)
    assert 30.0 <= adaptive_mae <= 36.0

    # Adaptive must match or exceed weekly accuracy
    assert adaptive_mae <= weekly_mae + 1.0

    # Retrainings: adaptive ~16.2 vs weekly exactly 80
    assert summary["adaptive"]["retrainings"][0] < 25.0
    assert summary["weekly"]["retrainings"][0] == 80.0


def test_nodrift_benchmark_penalty():
    """Verify that weekly retraining suffers penalty while adaptive raises 0 alarms without drift."""
    benchmark = experiment_service.get_benchmark("nodrift")
    summary = benchmark["summary"]

    static_mae = summary["static"]["mae"][0]
    adaptive_mae = summary["adaptive"]["mae"][0]
    weekly_mae = summary["weekly"]["mae"][0]

    # Without drift, adaptive equals static (MAE ~25.5 kW)
    assert adaptive_mae == pytest.approx(static_mae, 0.1)

    # Weekly retraining must be significantly worse (~33.2 kW, >30% penalty)
    assert weekly_mae > static_mae * 1.2
    assert summary["adaptive"]["alarms_raised"] == 0
