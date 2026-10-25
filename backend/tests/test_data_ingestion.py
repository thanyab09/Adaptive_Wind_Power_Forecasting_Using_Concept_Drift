"""Tests for synthetic data generation and CSV ingestion validation."""
import io
import pandas as pd
import numpy as np
import pytest
from backend.app.ml.simulator import generate_synthetic_stream, power_curve
from backend.app.ml.dataset_manager import DatasetManager


def test_power_curve_physics():
    """Verify piecewise aerodynamic turbine conversion curve."""
    # Below cut-in (3 m/s) power must be 0
    assert power_curve(2.0, 15.0) == 0.0
    assert power_curve(0.0, 15.0) == 0.0

    # Between cut-in and rated (12 m/s), power rises with cubic speed
    p5 = float(power_curve(5.0, 15.0))
    p10 = float(power_curve(10.0, 15.0))
    assert 0 < p5 < p10 <= 2000.0

    # Above rated (12 m/s) power is capped at 2000 kW
    assert power_curve(15.0, 15.0) == 2000.0
    assert power_curve(20.0, 15.0) == 2000.0

    # At or above cut-out (25 m/s), turbine cuts out to 0
    assert power_curve(25.5, 15.0) == 0.0


def test_synthetic_stream_generation():
    """Verify generation parameters, shapes, and reproducibility."""
    d1 = generate_synthetic_stream(seed=42, n_weeks=4, drift=True)
    d2 = generate_synthetic_stream(seed=42, n_weeks=4, drift=True)

    # Deterministic given same seed
    np.testing.assert_array_equal(d1["v"], d2["v"])
    np.testing.assert_array_equal(d1["p"], d2["p"])

    # Correct number of hours (4 weeks = 672 hours)
    assert d1["n"] == 672
    assert len(d1["v"]) == 672
    assert len(d1["p"]) == 672

    # Physical boundaries
    assert (d1["p"] >= 0.0).all()
    assert (d1["p"] <= 2000.0).all()
    assert (d1["v"] >= 0.0).all()


def test_csv_validation_valid():
    """Verify valid CSV ingestion."""
    dm = DatasetManager()
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=1000, freq="h"),
        "wind_speed": np.random.uniform(3.0, 15.0, 1000),
        "wind_direction": np.random.uniform(0.0, 360.0, 1000),
        "temperature": np.random.uniform(10.0, 25.0, 1000),
        "power": np.random.uniform(50.0, 1800.0, 1000),
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    content = buffer.getvalue()

    success, msg, meta = dm.validate_and_load_csv(content, "test.csv")
    assert success is True
    assert meta["rows"] == 1000
    assert dm.mode == "uploaded"


def test_csv_validation_missing_columns():
    """Verify rejection when mandatory columns are missing."""
    dm = DatasetManager()
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=1000, freq="h"),
        "wind_speed": np.random.uniform(3.0, 15.0, 1000),
        # missing direction, temperature, power
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    content = buffer.getvalue()

    success, msg, meta = dm.validate_and_load_csv(content, "incomplete.csv")
    assert success is False
    assert "missing mandatory columns" in msg


def test_csv_validation_unrealistic_values():
    """Verify rejection when wind speed has unrealistic negative or hurricane values."""
    dm = DatasetManager()
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=1000, freq="h"),
        "wind_speed": [-10.0] + list(np.random.uniform(3.0, 15.0, 999)),
        "wind_direction": np.random.uniform(0.0, 360.0, 1000),
        "temperature": np.random.uniform(10.0, 25.0, 1000),
        "power": np.random.uniform(50.0, 1800.0, 1000),
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    content = buffer.getvalue()

    success, msg, meta = dm.validate_and_load_csv(content, "bad_speed.csv")
    assert success is False
    assert "unrealistic physical values" in msg


def test_csv_validation_insufficient_rows():
    """Verify rejection when dataset is shorter than 672 hours."""
    dm = DatasetManager()
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=100, freq="h"),
        "wind_speed": np.random.uniform(3.0, 15.0, 100),
        "wind_direction": np.random.uniform(0.0, 360.0, 100),
        "temperature": np.random.uniform(10.0, 25.0, 100),
        "power": np.random.uniform(50.0, 1800.0, 100),
    })
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    content = buffer.getvalue()

    success, msg, meta = dm.validate_and_load_csv(content, "short.csv")
    assert success is False
    assert "minimum of 672 hours" in msg
