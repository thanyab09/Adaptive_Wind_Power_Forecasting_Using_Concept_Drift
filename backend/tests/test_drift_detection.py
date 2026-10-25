"""Tests for Page-Hinkley, heteroscedastic calibration, KS test, and PSI."""
import numpy as np
import pytest
from backend.app.ml.drift_detectors import (
    PageHinkley,
    compute_psi,
    compute_ks_test,
    standardize_residual,
)


def test_page_hinkley_stationary():
    """Verify Page-Hinkley stays below threshold when data is stationary."""
    rng = np.random.default_rng(0)
    mu0, delta, lam = 1.0, 0.5, 12.0
    ph = PageHinkley(mu0=mu0, delta=delta, lam=lam)

    # Stationary series with mean = 1.0
    series = rng.normal(1.0, 0.2, 500)
    alarms = [ph.update(x, t) for t, x in enumerate(series)]

    # Must raise zero alarms
    assert not any(alarms)
    assert ph.statistic < lam


def test_page_hinkley_drift_trigger():
    """Verify Page-Hinkley triggers alarm when stream mean shifts upwards."""
    rng = np.random.default_rng(42)
    mu0, delta, lam = 1.0, 0.48, 12.0
    ph = PageHinkley(mu0=mu0, delta=delta, lam=lam)

    # Step 0 to 100: mean 1.0; Step 100 onwards: mean shifts to 3.5
    series = np.concatenate([
        rng.normal(1.0, 0.2, 100),
        rng.normal(3.5, 0.5, 100),
    ])

    alarm_times = []
    for t, x in enumerate(series):
        if ph.update(x, t):
            alarm_times.append(t)
            break

    # Must detect drift shortly after step 100
    assert len(alarm_times) == 1
    assert alarm_times[0] > 100
    assert alarm_times[0] < 120  # Fast detection within 20 steps
    assert ph.t_min is not None
    assert abs(ph.t_min - 100) < 10  # Accurately pinpoints change point


def test_psi_and_ks_metrics():
    """Verify distribution metrics respond to distribution shifts."""
    rng = np.random.default_rng(10)
    ref = rng.normal(7.5, 2.0, 500)
    same_dist = rng.normal(7.5, 2.0, 500)
    shifted_dist = rng.normal(11.0, 2.0, 500)

    # Identical distributions -> low PSI (< 0.1), high KS p-value (> 0.05)
    psi_low = compute_psi(ref, same_dist)
    ks_stat_low, ks_p_low = compute_ks_test(ref, same_dist)
    assert psi_low < 0.1
    assert ks_p_low > 0.05

    # Shifted distributions -> high PSI (> 0.25), very small KS p-value (< 1e-10)
    psi_high = compute_psi(ref, shifted_dist)
    ks_stat_high, ks_p_high = compute_ks_test(ref, shifted_dist)
    assert psi_high > 0.25
    assert ks_p_high < 1e-10


def test_standardize_residual():
    """Verify scale-free standardization using calibration bins."""
    cal = {
        "edges": [200.0, 500.0, 1000.0],
        "means": [10.0, 25.0, 50.0, 100.0],
        "mu0": 1.0,
        "s0": 0.8,
    }
    # For low power prediction (100 kW), bin 0 error scale is 10.0 kW
    z1 = standardize_residual(pred_power=100.0, actual_power=120.0, cal=cal)
    assert z1 == 2.0  # |100 - 120| / 10 = 2.0

    # For high power prediction (1500 kW), bin 3 error scale is 100.0 kW
    z2 = standardize_residual(pred_power=1500.0, actual_power=1700.0, cal=cal)
    assert z2 == 2.0  # |1500 - 1700| / 100 = 2.0
