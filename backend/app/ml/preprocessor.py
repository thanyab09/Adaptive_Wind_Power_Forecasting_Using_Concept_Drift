"""Feature engineering and preprocessing for wind power forecasting."""
import numpy as np
import pandas as pd
from typing import Dict, Any, Union
from ..config import FEATURE_NAMES


def compute_features(data: Union[Dict[str, np.ndarray], pd.DataFrame]) -> np.ndarray:
    """
    Constructs the 10 forecasting features for one-hour-ahead prediction.
    Enforces strict chronological preservation and prevents any target leakage.

    Features:
      0: v       - Current measured wind speed (m/s)
      1: sin_d   - sin(direction in radians)
      2: cos_d   - cos(direction in radians)
      3: temp    - Ambient air temperature (°C)
      4: p_l1    - Observed power at t-1 (kW)
      5: p_l2    - Observed power at t-2 (kW)
      6: p_l24   - Observed power at t-24 (kW)
      7: p_m6    - Rolling mean of observed power over [t-6 .. t-1] (kW)
      8: v_l1    - Wind speed at t-1 (m/s)
      9: v_m3    - Rolling mean of wind speed over [t-3 .. t-1] (m/s)
    """
    if isinstance(data, pd.DataFrame):
        p = data["power"].to_numpy(dtype=float)
        v = data["wind_speed"].to_numpy(dtype=float)
        d = data["wind_direction"].to_numpy(dtype=float)
        temp = data["temperature"].to_numpy(dtype=float)
        n = len(p)
    else:
        p = np.asarray(data["p"], dtype=float)
        v = np.asarray(data["v"], dtype=float)
        d = np.asarray(data["d"], dtype=float)
        temp = np.asarray(data["temp"], dtype=float)
        n = len(p)

    rad = np.deg2rad(d % 360.0)
    X = np.zeros((n, len(FEATURE_NAMES)), dtype=float)

    # Instantaneous inputs available at forecast time
    X[:, 0] = v
    X[:, 1] = np.sin(rad)
    X[:, 2] = np.cos(rad)
    X[:, 3] = temp

    # Helper for causal lag (replicates earliest available observation for initial boundary)
    def lag(arr: np.ndarray, k: int) -> np.ndarray:
        if k >= n:
            return np.full(n, arr[0])
        return np.concatenate([np.full(k, arr[0]), arr[:-k]])

    # Lagged power features
    X[:, 4] = lag(p, 1)
    X[:, 5] = lag(p, 2)
    X[:, 6] = lag(p, 24)

    # 6-hour rolling mean of power strictly over [t-6 .. t-1]
    # Using cumsum for exact, fast computation
    cs_p = np.cumsum(np.insert(p, 0, 0.0))
    p_m6 = np.zeros(n, dtype=float)
    for i in range(n):
        # Window of recent power values ending at i-1
        # Range is max(0, i-6) to i
        start_idx = max(i - 6, 0)
        end_idx = i
        count = end_idx - start_idx
        if count <= 0:
            p_m6[i] = p[0]
        else:
            p_m6[i] = (cs_p[end_idx] - cs_p[start_idx]) / count
    X[:, 7] = p_m6

    # Lagged wind speed feature
    X[:, 8] = lag(v, 1)

    # 3-hour rolling mean of wind speed strictly over [t-3 .. t-1]
    cs_v = np.cumsum(np.insert(v, 0, 0.0))
    v_m3 = np.zeros(n, dtype=float)
    for i in range(n):
        start_idx = max(i - 3, 0)
        end_idx = i
        count = end_idx - start_idx
        if count <= 0:
            v_m3[i] = v[0]
        else:
            v_m3[i] = (cs_v[end_idx] - cs_v[start_idx]) / count
    X[:, 9] = v_m3

    return X
