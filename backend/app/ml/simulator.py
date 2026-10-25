"""Synthetic wind-farm data generator and physics engine."""
import numpy as np
from ..config import (
    RATED_POWER_KW,
    CUT_IN_SPEED,
    RATED_SPEED,
    CUT_OUT_SPEED,
    HOURS_PER_WEEK,
    TOTAL_WEEKS,
    DRIFT_WEEK,
)


def power_curve(v, temp, vin=CUT_IN_SPEED, vr=RATED_SPEED, vout=CUT_OUT_SPEED, rated=RATED_POWER_KW):
    """
    Theoretical wind turbine power curve with air density temperature adjustment.
    Ideal gas law: rho = p / (Rs * T)
    corr = rho / 1.225 (standard air density at sea level)
    """
    # Air pressure 1013.25 hPa, specific gas constant Rs = 287.05 J/(kg*K)
    rho = 101325.0 / (287.05 * (np.asarray(temp) + 273.15))
    corr = rho / 1.225

    # Cubic conversion between cut-in and rated speeds
    v_arr = np.asarray(v, dtype=float)
    p = rated * (v_arr ** 3 - vin ** 3) / (vr ** 3 - vin ** 3) * corr
    p = np.where(v_arr < vin, 0.0, p)
    p = np.minimum(p, rated)
    p = np.where(v_arr >= vout, 0.0, p)
    return np.maximum(p, 0.0)


def ar1(rng: np.random.Generator, n: int, phi: float) -> np.ndarray:
    """Stationary AR(1) autoregressive noise process with unit variance."""
    x = np.zeros(n)
    e = rng.standard_normal(n)
    scale = np.sqrt(1.0 - phi ** 2)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + scale * e[i]
    return x


def generate_synthetic_stream(
    seed: int = 0,
    drift: bool = True,
    magnitude: float = 1.0,
    n_weeks: int = TOTAL_WEEKS,
    drift_week: int = DRIFT_WEEK,
) -> dict:
    """
    Generates hourly synthetic wind-farm dataset for n_weeks.
    Incorporates:
      - Seasonal annual wind trend (windier in winter)
      - Diurnal daily cycle
      - Autocorrelated wind speed turbulence (AR1 phi=0.96)
      - Seasonal temperature cycle (warmer in summer)
      - Wind direction around 225 deg (South-West prevailing)
      - Sensor measurement noise
      - Injected concept drift at drift_week (real derating + wake loss, virtual anemometer scaling)
    """
    rng = np.random.default_rng(seed)
    n = n_weeks * HOURS_PER_WEEK
    t = np.arange(n)
    doy = (t / 24.0) % 365

    # Weather dynamics
    season = 1.0 * np.cos(2 * np.pi * (doy - 20) / 365)  # Peak wind in winter
    diurnal = 0.7 * np.sin(2 * np.pi * ((t % 24) - 14) / 24)
    v_true = 7.6 + 1.3 * season + diurnal + 2.7 * ar1(rng, n, 0.96)
    v_true = np.clip(v_true, 0.0, 30.0)

    # Ambient temperature
    temp = (
        17.0
        + 9.0 * np.cos(2 * np.pi * (doy - 200) / 365)
        + 3.0 * np.sin(2 * np.pi * ((t % 24) - 15) / 24)
        + 1.5 * ar1(rng, n, 0.97)
    )

    # Prevailing wind direction
    d = 225.0 + 55.0 * ar1(rng, n, 0.97)
    d = d % 360.0

    # True aerodynamic power before perturbation
    p_true = power_curve(v_true, temp)

    # Measured sensor inputs
    v_meas = v_true + 0.15 * rng.standard_normal(n)
    d_meas = (d + 4.0 * rng.standard_normal(n)) % 360.0

    onset = None
    if drift:
        onset = drift_week * HOURS_PER_WEEK
        m = float(magnitude)
        after = t >= onset

        # (1) Real concept drift: 7.5% derating + 8.5% wake loss in 200°-265° sector
        deg = 1.0 - 0.075 * m
        sector = ((d > 200.0) & (d < 265.0)).astype(float)
        wake = 1.0 - 0.085 * m * sector
        p_true = np.where(after, p_true * deg * wake, p_true)

        # (2) Virtual drift: anemometer recalibration (+4% speed offset)
        v_meas = np.where(after, v_meas * (1.0 + 0.04 * m), v_meas)

    # Observed power with multiplicative and additive electrical noise
    p_obs = p_true * (1.0 + 0.008 * rng.standard_normal(n)) + 7.0 * rng.standard_normal(n)
    p_obs = np.clip(p_obs, 0.0, RATED_POWER_KW)

    return {
        "v": v_meas,
        "v_true": v_true,
        "d": d_meas,
        "temp": temp,
        "p": p_obs,
        "p_clean": p_true,
        "onset": onset,
        "n": n,
        "seed": seed,
        "drift": drift,
        "magnitude": magnitude,
    }
