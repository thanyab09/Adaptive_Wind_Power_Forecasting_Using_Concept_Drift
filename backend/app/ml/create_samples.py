"""Creates sample CSV datasets in data/sample/."""
from pathlib import Path
import pandas as pd
import numpy as np
from backend.app.config import SAMPLE_DATA_DIR
from backend.app.ml.simulator import generate_synthetic_stream

def create_sample_datasets():
    print("Generating sample datasets...")
    # 1. Synthetic wind farm demo (106 weeks = 17,808 hours)
    D = generate_synthetic_stream(seed=0, drift=True, magnitude=1.0)
    timestamps = pd.date_range("2024-01-01 00:00:00", periods=D["n"], freq="h")
    df_synthetic = pd.DataFrame({
        "timestamp": timestamps,
        "wind_speed": np.round(D["v"], 2),
        "wind_direction": np.round(D["d"], 1),
        "temperature": np.round(D["temp"], 1),
        "power": np.round(D["p"], 1),
    })
    synthetic_path = SAMPLE_DATA_DIR / "synthetic_wind_farm_demo.csv"
    df_synthetic.to_csv(synthetic_path, index=False)
    print(f"Created {synthetic_path} ({len(df_synthetic)} rows)")

    # 2. Real-world format sample dataset (4,000 hours ~ 24 weeks)
    # Using seed 3 with realistic turbine characteristics
    D_real = generate_synthetic_stream(seed=3, drift=False)
    n_sample = 4000
    timestamps_real = pd.date_range("2025-01-01 00:00:00", periods=n_sample, freq="h")
    df_real = pd.DataFrame({
        "timestamp": timestamps_real,
        "wind_speed": np.round(D_real["v"][:n_sample], 2),
        "wind_direction": np.round(D_real["d"][:n_sample], 1),
        "temperature": np.round(D_real["temp"][:n_sample], 1),
        "power": np.round(D_real["p"][:n_sample], 1),
    })
    real_path = SAMPLE_DATA_DIR / "real_wind_farm_sample.csv"
    df_real.to_csv(real_path, index=False)
    print(f"Created {real_path} ({len(df_real)} rows)")

if __name__ == "__main__":
    create_sample_datasets()
