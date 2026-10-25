"""Dataset manager handling synthetic generation, CSV upload, validation, and statistics."""
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import io
import numpy as np
import pandas as pd
from ..config import (
    RATED_POWER_KW,
    INITIAL_HOURS,
    TOTAL_HOURS,
    SAMPLE_DATA_DIR,
    UPLOADS_DATA_DIR,
    FEATURE_NAMES,
)
from .simulator import generate_synthetic_stream
from .preprocessor import compute_features


class DatasetManager:
    """Manages active dataset state, CSV validation, and feature preparation."""

    def __init__(self):
        self.mode: str = "synthetic"  # "synthetic" or "uploaded"
        self.dataset_name: str = "Synthetic Wind Farm (2 MW, Seed 0)"
        self.raw_data: Optional[Dict[str, np.ndarray]] = None
        self.df: Optional[pd.DataFrame] = None
        self.features: Optional[np.ndarray] = None
        self.metadata: Dict[str, Any] = {}
        # Load default demo dataset on startup
        self.load_synthetic(seed=0, drift=True, magnitude=1.0)

    def load_synthetic(self, seed: int = 0, drift: bool = True, magnitude: float = 1.0) -> Dict[str, Any]:
        """Generates synthetic wind-farm data using the project's physics engine."""
        D = generate_synthetic_stream(seed=seed, drift=drift, magnitude=magnitude)
        self.raw_data = D
        n = D["n"]

        # Build clean pandas DataFrame with synthetic timestamps
        timestamps = pd.date_range("2024-01-01 00:00:00", periods=n, freq="h")
        self.df = pd.DataFrame({
            "timestamp": timestamps,
            "wind_speed": D["v"],
            "wind_direction": D["d"],
            "temperature": D["temp"],
            "power": D["p"],
        })
        self.features = compute_features(D)
        self.mode = "synthetic"
        self.dataset_name = f"Synthetic Wind Farm (Seed {seed}{', Abrupt Drift' if drift else ', No Drift'})"
        self.metadata = {
            "mode": "synthetic",
            "seed": seed,
            "drift": drift,
            "magnitude": magnitude,
            "drift_onset_hour": D["onset"],
            "rows": n,
            "rated_power_kw": RATED_POWER_KW,
            "initial_hours": INITIAL_HOURS,
        }
        return self.metadata

    def validate_and_load_csv(self, file_content: bytes, filename: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Parses, validates, and ingests an uploaded CSV file.
        Enforces required columns, checks for missing data, duplicate timestamps,
        validates physical ranges, and sorts chronologically.
        """
        try:
            df = pd.read_csv(io.BytesIO(file_content))
        except Exception as ex:
            return False, f"Failed to parse CSV file: {str(ex)}", None

        # Standardize column names (lowercase, strip whitespace)
        col_map = {col: col.strip().lower() for col in df.columns}
        df.rename(columns=col_map, inplace=True)

        # Flexible column resolution
        synonyms = {
            "timestamp": ["timestamp", "time", "datetime", "date_time", "date"],
            "wind_speed": ["wind_speed", "windspeed", "speed", "v", "ws"],
            "wind_direction": ["wind_direction", "winddirection", "direction", "dir", "wd", "d"],
            "temperature": ["temperature", "temp", "air_temp", "t"],
            "power": ["power", "active_power", "power_output", "p", "kw", "mw"],
        }

        matched_cols = {}
        for target, syn_list in synonyms.items():
            for c in df.columns:
                if c in syn_list:
                    matched_cols[target] = c
                    break

        missing = [t for t in ["timestamp", "wind_speed", "wind_direction", "temperature", "power"] if t not in matched_cols]
        if missing:
            return False, f"Uploaded CSV is missing mandatory columns: {', '.join(missing)}. Found: {list(df.columns)}", None

        # Build clean dataframe
        clean_df = pd.DataFrame({
            "timestamp": pd.to_datetime(df[matched_cols["timestamp"]], errors="coerce"),
            "wind_speed": pd.to_numeric(df[matched_cols["wind_speed"]], errors="coerce"),
            "wind_direction": pd.to_numeric(df[matched_cols["wind_direction"]], errors="coerce"),
            "temperature": pd.to_numeric(df[matched_cols["temperature"]], errors="coerce"),
            "power": pd.to_numeric(df[matched_cols["power"]], errors="coerce"),
        })

        # Check for invalid timestamps
        invalid_ts_count = clean_df["timestamp"].isna().sum()
        if invalid_ts_count > 0:
            clean_df = clean_df.dropna(subset=["timestamp"])

        # Check row count
        if len(clean_df) < 672:
            return False, f"Dataset has only {len(clean_df)} valid rows. A minimum of 672 hours (4 weeks) is required for reliable model evaluation.", None

        # Check duplicate timestamps
        dups = clean_df.duplicated(subset=["timestamp"]).sum()
        if dups > 0:
            clean_df = clean_df.drop_duplicates(subset=["timestamp"])

        # Sort chronologically
        clean_df = clean_df.sort_values(by="timestamp").reset_index(drop=True)

        # Check for nulls in numeric columns and interpolate/ffill
        null_counts = clean_df[["wind_speed", "wind_direction", "temperature", "power"]].isna().sum()
        if null_counts.sum() > 0:
            clean_df[["wind_speed", "wind_direction", "temperature", "power"]] = (
                clean_df[["wind_speed", "wind_direction", "temperature", "power"]]
                .interpolate(method="linear")
                .bfill()
                .ffill()
            )

        # Range validation
        if (clean_df["wind_speed"] < 0).any() or (clean_df["wind_speed"] > 60).any():
            return False, "Wind speed contains unrealistic physical values (must be between 0 and 60 m/s).", None

        if (clean_df["power"] < 0).any():
            clean_df["power"] = clean_df["power"].clip(lower=0.0)

        # Check direction wrapping
        clean_df["wind_direction"] = clean_df["wind_direction"] % 360.0

        # Save to uploads dir
        safe_name = Path(filename).name
        upload_path = UPLOADS_DATA_DIR / safe_name
        clean_df.to_csv(upload_path, index=False)

        # Prepare active state
        self.df = clean_df
        self.raw_data = {
            "v": clean_df["wind_speed"].to_numpy(dtype=float),
            "v_true": clean_df["wind_speed"].to_numpy(dtype=float),
            "d": clean_df["wind_direction"].to_numpy(dtype=float),
            "temp": clean_df["temperature"].to_numpy(dtype=float),
            "p": clean_df["power"].to_numpy(dtype=float),
            "p_clean": clean_df["power"].to_numpy(dtype=float),
            "onset": None,
            "n": len(clean_df),
        }
        self.features = compute_features(self.raw_data)
        self.mode = "uploaded"
        self.dataset_name = f"Uploaded: {safe_name}"

        # Determine rated power from max observed power
        observed_max = float(clean_df["power"].max())
        rated = 2000.0 if observed_max <= 2000.0 else round(observed_max, -2)

        self.metadata = {
            "mode": "uploaded",
            "filename": safe_name,
            "rows": len(clean_df),
            "start_time": str(clean_df["timestamp"].iloc[0]),
            "end_time": str(clean_df["timestamp"].iloc[-1]),
            "rated_power_kw": rated,
            "initial_hours": min(4368, int(len(clean_df) * 0.3)),
            "missing_imputed": int(null_counts.sum()),
            "duplicates_removed": int(dups),
        }
        return True, "Dataset successfully validated and loaded.", self.metadata

    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculates descriptive statistics for each column."""
        if self.df is None:
            return {}
        stats_dict = {}
        for col in ["wind_speed", "wind_direction", "temperature", "power"]:
            s = self.df[col]
            stats_dict[col] = {
                "min": round(float(s.min()), 2),
                "max": round(float(s.max()), 2),
                "mean": round(float(s.mean()), 2),
                "std": round(float(s.std()), 2),
                "median": round(float(s.median()), 2),
            }
        return stats_dict

    def get_correlation_matrix(self) -> Dict[str, Any]:
        """Computes Pearson correlation matrix."""
        if self.df is None:
            return {"columns": [], "matrix": []}
        cols = ["wind_speed", "wind_direction", "temperature", "power"]
        corr = self.df[cols].corr().round(3)
        return {
            "columns": cols,
            "matrix": corr.values.tolist(),
        }

    def get_power_curve_scatter(self, sample_size: int = 500) -> List[Dict[str, float]]:
        """Returns subsampled wind speed vs power points for scatter visualization."""
        if self.df is None:
            return []
        step = max(1, len(self.df) // sample_size)
        sub = self.df.iloc[::step]
        return [
            {"wind_speed": round(float(r["wind_speed"]), 2), "power": round(float(r["power"]), 2)}
            for _, r in sub.iterrows()
        ]

    def get_wind_rose_data(self, num_sectors: int = 16) -> List[Dict[str, Any]]:
        """Binned wind direction and mean wind speed per sector for wind rose visualization."""
        if self.df is None:
            return []
        bin_width = 360.0 / num_sectors
        bins = np.linspace(0, 360, num_sectors + 1)
        labels = [f"{(i * bin_width):.0f}°" for i in range(num_sectors)]
        cats = pd.cut(self.df["wind_direction"] % 360.0, bins=bins, labels=labels, include_lowest=True)

        grouped = self.df.groupby(cats, observed=False)
        counts = grouped.size()
        mean_speeds = grouped["wind_speed"].mean().fillna(0.0)
        mean_powers = grouped["power"].mean().fillna(0.0)

        total = len(self.df)
        rose = []
        for label in labels:
            cnt = int(counts.get(label, 0))
            rose.append({
                "sector": label,
                "percentage": round(cnt / total * 100.0, 2) if total > 0 else 0.0,
                "mean_speed": round(float(mean_speeds.get(label, 0.0)), 2),
                "mean_power": round(float(mean_powers.get(label, 0.0)), 2),
                "wake_sector": bool("200°" in label or "225°" in label or "247°" in label or "270°" in label),
            })
        return rose

    def export_csv_bytes(self) -> bytes:
        """Exports current dataset to CSV bytes."""
        if self.df is None:
            return b""
        buffer = io.StringIO()
        self.df.to_csv(buffer, index=False)
        return buffer.getvalue().encode("utf-8")


# Singleton instance across application
dataset_manager = DatasetManager()
