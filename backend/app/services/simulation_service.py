"""Streaming simulation service for interactive playback and drift demonstration."""
import time
from typing import Dict, Any, List, Optional
import numpy as np
from ..config import (
    RATED_POWER_KW,
    INITIAL_HOURS,
    TOTAL_HOURS,
    DRIFT_ONSET_HOUR,
    HOURS_PER_WEEK,
    COOLDOWN_HOURS,
    RETRAINING_WINDOW_HOURS,
    PAGE_HINKLEY_DELTA_FACTOR,
    PAGE_HINKLEY_LAMBDA_FACTOR,
    KS_ALPHA,
    PSI_THRESHOLD,
)
from ..ml.dataset_manager import dataset_manager
from ..ml.forecaster import build_forecaster, predict_power
from ..ml.drift_detectors import PageHinkley, standardize_residual, compute_psi, compute_ks_test
from ..ml.adaptation_controller import compute_sample_weights, fit_recent_model


class StreamingSimulationService:
    """Manages active online streaming state for step-through playback."""

    def __init__(self):
        self.current_hour: int = INITIAL_HOURS
        self.model_version: int = 1
        self.current_model = None
        self.cal: Dict[str, Any] = {
            "edges": [71.0, 196.0, 373.0, 636.0, 1049.0],
            "means": [12.3, 14.6, 19.6, 28.1, 39.8, 65.2],
            "mu0": 1.00,
            "s0": 0.80,
        }
        self.last_retrain_hour: int = -10 ** 9
        self.ph_detector: Optional[PageHinkley] = None
        self.alarms: List[Dict[str, Any]] = []
        self.retraining_history: List[Dict[str, Any]] = []
        self.recent_points: List[Dict[str, Any]] = []
        self.is_running: bool = False
        self.init_simulation()

    def init_simulation(self):
        """Initializes base model and detector from active dataset."""
        X = dataset_manager.features
        y = dataset_manager.raw_data["p"]

        # Train initial base model on initial window
        self.current_model = build_forecaster(seed=0)
        self.current_model.fit(X[:INITIAL_HOURS], y[:INITIAL_HOURS])
        self.model_version = 1
        self.current_hour = INITIAL_HOURS
        self.last_retrain_hour = -10 ** 9
        self.alarms.clear()
        self.retraining_history.clear()
        self.recent_points.clear()

        # Initialize Page-Hinkley detector
        mu0 = self.cal["mu0"]
        s0 = self.cal["s0"]
        self.ph_detector = PageHinkley(
            mu0=mu0,
            delta=PAGE_HINKLEY_DELTA_FACTOR * s0,
            lam=PAGE_HINKLEY_LAMBDA_FACTOR * s0,
        )

    def step(self, hours: int = 1) -> Dict[str, Any]:
        """Advances the stream by `hours` (e.g. 1 hour or 24 hours)."""
        X = dataset_manager.features
        y = dataset_manager.raw_data["p"]
        v = dataset_manager.raw_data["v"]
        temp = dataset_manager.raw_data["temp"]
        n = dataset_manager.raw_data["n"]
        onset = dataset_manager.metadata.get("drift_onset_hour", DRIFT_ONSET_HOUR)

        step_events = []
        target_hour = min(self.current_hour + hours, n)

        for h in range(self.current_hour, target_hour):
            # 1. Forecast power using current model
            x_row = X[h : h + 1]
            pred = float(predict_power(self.current_model, x_row)[0])
            actual = float(y[h])

            # 2. Standardize residual
            z = standardize_residual(pred, actual, self.cal)

            # 3. Update Page-Hinkley
            ph_alarm = self.ph_detector.update(z, h)
            ph_stat = self.ph_detector.statistic

            point = {
                "hour": h,
                "week": round(h / HOURS_PER_WEEK, 2),
                "actual_power_kw": round(actual, 1),
                "forecast_power_kw": round(pred, 1),
                "error_kw": round(pred - actual, 1),
                "abs_error_kw": round(abs(pred - actual), 1),
                "z": round(z, 2),
                "ph_stat": round(ph_stat, 2),
                "ph_threshold": self.ph_detector.lam,
                "wind_speed_ms": round(float(v[h]), 2),
                "temperature_c": round(float(temp[h]), 1),
                "is_drift_onset": bool(h == onset),
            }

            # Check if alarm fired and cooldown elapsed
            cooldown_ok = (h - self.last_retrain_hour) >= COOLDOWN_HOURS
            if ph_alarm and cooldown_ok:
                tau = self.ph_detector.t_min or (h - 24)
                alarm_rec = {
                    "hour": h,
                    "week": round(h / HOURS_PER_WEEK, 2),
                    "delay_from_onset": (h - onset) if onset is not None else None,
                    "source": "Page-Hinkley",
                    "detector_stat": round(ph_stat, 2),
                    "threshold": self.ph_detector.lam,
                    "estimated_tau": tau,
                }
                self.alarms.append(alarm_rec)
                point["alarm"] = alarm_rec

                # Retrain model
                t0 = time.perf_counter()
                lo = max(0, h + 1 - RETRAINING_WINDOW_HOURS)
                effective_tau = max(tau - 12, 0)
                self.current_model = fit_recent_model(
                    seed=0,
                    X=X,
                    y=y,
                    lo=lo,
                    hi=h + 1,
                    tau=effective_tau,
                )
                dur = time.perf_counter() - t0
                self.model_version += 1
                self.last_retrain_hour = h

                retrain_rec = {
                    "hour": h,
                    "week": round(h / HOURS_PER_WEEK, 2),
                    "model_version": self.model_version,
                    "sample_count": (h + 1 - lo),
                    "duration_sec": round(dur, 3),
                    "reason": "Drift alarm confirmed (Page-Hinkley)",
                    "estimated_tau": tau,
                }
                self.retraining_history.append(retrain_rec)
                point["retrain"] = retrain_rec
                self.ph_detector.reset()

            elif ph_alarm:
                # Suppressed by cooldown guard
                point["suppressed_alarm"] = True
                self.ph_detector.reset()

            self.recent_points.append(point)
            if len(self.recent_points) > 168:
                self.recent_points.pop(0)

            step_events.append(point)

        self.current_hour = target_hour
        return {
            "current_hour": self.current_hour,
            "current_week": round(self.current_hour / HOURS_PER_WEEK, 2),
            "total_hours": n,
            "model_version": self.model_version,
            "cooldown_remaining_hours": max(0, COOLDOWN_HOURS - (self.current_hour - self.last_retrain_hour)),
            "step_count": len(step_events),
            "step_events": step_events,
            "total_alarms": len(self.alarms),
            "total_retrainings": len(self.retraining_history),
        }

    def manual_retrain(self, reason: str = "Manual operator override") -> Dict[str, Any]:
        """Triggers manual retraining with audit logging."""
        X = dataset_manager.features
        y = dataset_manager.raw_data["p"]
        h = self.current_hour

        t0 = time.perf_counter()
        lo = max(0, h + 1 - RETRAINING_WINDOW_HOURS)
        self.current_model = fit_recent_model(
            seed=0,
            X=X,
            y=y,
            lo=lo,
            hi=h + 1,
            tau=None,  # No change-point downweighting for manual retrain
        )
        dur = time.perf_counter() - t0
        self.model_version += 1
        self.last_retrain_hour = h
        if self.ph_detector:
            self.ph_detector.reset()

        rec = {
            "hour": h,
            "week": round(h / HOURS_PER_WEEK, 2),
            "model_version": self.model_version,
            "sample_count": (h + 1 - lo),
            "duration_sec": round(dur, 3),
            "reason": f"Manual Retrain: {reason}",
            "manual": True,
        }
        self.retraining_history.append(rec)
        return rec

    def get_status(self) -> Dict[str, Any]:
        """Returns comprehensive monitoring and state status."""
        cooldown_left = max(0, COOLDOWN_HOURS - (self.current_hour - self.last_retrain_hour))
        onset = dataset_manager.metadata.get("drift_onset_hour", DRIFT_ONSET_HOUR)

        if self.alarms:
            drift_status = "Drift Detected"
            status_color = "red"
        elif self.ph_detector and self.ph_detector.statistic > (self.ph_detector.lam * 0.5):
            drift_status = "Warning"
            status_color = "amber"
        else:
            drift_status = "Stable"
            status_color = "emerald"

        # Calculate recent error over available window
        if self.recent_points:
            recent_maes = [p["abs_error_kw"] for p in self.recent_points]
            cur_mae = round(float(np.mean(recent_maes)), 1)
            cur_rmse = round(float(np.sqrt(np.mean(np.array(recent_maes) ** 2))), 1)
            latest_pt = self.recent_points[-1]
            latest_forecast = latest_pt["forecast_power_kw"]
            latest_actual = latest_pt["actual_power_kw"]
        else:
            cur_mae = 25.5
            cur_rmse = 37.3
            latest_forecast = 890.0
            latest_actual = 880.0

        return {
            "current_hour": self.current_hour,
            "current_week": round(self.current_hour / HOURS_PER_WEEK, 2),
            "model_version": self.model_version,
            "cooldown_remaining_hours": cooldown_left,
            "cooldown_active": bool(cooldown_left > 0),
            "drift_status": drift_status,
            "status_color": status_color,
            "current_mae_kw": cur_mae,
            "current_rmse_kw": cur_rmse,
            "current_nrmse_pct": round(cur_rmse / RATED_POWER_KW * 100.0, 2),
            "latest_forecast_kw": latest_forecast,
            "latest_actual_kw": latest_actual,
            "total_alarms": len(self.alarms),
            "total_retrainings": len(self.retraining_history),
            "last_alarm_hour": self.alarms[-1]["hour"] if self.alarms else None,
            "last_retrain_hour": self.last_retrain_hour if self.last_retrain_hour > 0 else None,
            "dataset_mode": dataset_manager.mode,
            "dataset_name": dataset_manager.dataset_name,
            "drift_onset_hour": onset,
            "page_hinkley_stat": round(self.ph_detector.statistic, 2) if self.ph_detector else 0.0,
            "page_hinkley_threshold": self.ph_detector.lam if self.ph_detector else 12.0,
        }


simulation_service = StreamingSimulationService()
