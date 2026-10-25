"""Precomputes authentic benchmark data from project report for instant loading."""
import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

# Table 6.1, 6.3, 6.4, 6.5, 6.6, D.1, D.2
TEN_SEEDS_BENCHMARK = {
    "drift": {
        "scenario": "Abrupt Concept Drift at Week 28 (Hour 4,704)",
        "rated_power_kw": 2000.0,
        "seeds": list(range(10)),
        "summary": {
            "static": {
                "name": "Static Model (Train Once)",
                "mae": [134.7, 5.6],
                "rmse": [178.4, 5.6],
                "nrmse": [8.92, 0.28],
                "retrainings": [0.0, 0.0],
                "retraining_time_s": [0.0, 0.0],
            },
            "adaptive": {
                "name": "Adaptive Model (Drift-Triggered)",
                "mae": [33.7, 2.1],
                "rmse": [53.0, 3.7],
                "nrmse": [2.65, 0.19],
                "retrainings": [16.2, 6.6],
                "retraining_time_s": [1.98, 0.82],
            },
            "weekly": {
                "name": "Weekly Retrained Model (Calendar Schedule)",
                "mae": [35.3, 1.3],
                "rmse": [62.7, 5.4],
                "nrmse": [3.14, 0.27],
                "retrainings": [80.0, 0.0],
                "retraining_time_s": [9.59, 0.53],
            },
        },
        "per_seed": [
            {"seed": 0, "static_mae": 137.6, "adaptive_mae": 33.9, "weekly_mae": 35.0, "static_rmse": 182.0, "adaptive_rmse": 52.8, "weekly_rmse": 60.8, "delay_h": 16, "early_retrains": 6, "late_retrains": 3, "false_alarms": 0, "reduction_pct": 75.4},
            {"seed": 1, "static_mae": 125.9, "adaptive_mae": 30.5, "weekly_mae": 34.4, "static_rmse": 168.3, "adaptive_rmse": 48.6, "weekly_rmse": 60.0, "delay_h": 25, "early_retrains": 4, "late_retrains": 20, "false_alarms": 0, "reduction_pct": 75.7},
            {"seed": 2, "static_mae": 144.1, "adaptive_mae": 33.9, "weekly_mae": 36.4, "static_rmse": 185.2, "adaptive_rmse": 51.3, "weekly_rmse": 58.7, "delay_h": 2,  "early_retrains": 8, "late_retrains": 17, "false_alarms": 0, "reduction_pct": 76.4},
            {"seed": 3, "static_mae": 134.9, "adaptive_mae": 32.5, "weekly_mae": 35.1, "static_rmse": 179.6, "adaptive_rmse": 50.8, "weekly_rmse": 61.2, "delay_h": 47, "early_retrains": 4, "late_retrains": 5, "false_alarms": 0, "reduction_pct": 75.9},
            {"seed": 4, "static_mae": 137.0, "adaptive_mae": 37.5, "weekly_mae": 36.9, "static_rmse": 179.6, "adaptive_rmse": 58.5, "weekly_rmse": 66.7, "delay_h": 7,  "early_retrains": 6, "late_retrains": 3, "false_alarms": 0, "reduction_pct": 72.6},
            {"seed": 5, "static_mae": 141.7, "adaptive_mae": 35.1, "weekly_mae": 37.2, "static_rmse": 186.2, "adaptive_rmse": 52.4, "weekly_rmse": 73.4, "delay_h": 19, "early_retrains": 6, "late_retrains": 14, "false_alarms": 0, "reduction_pct": 75.2},
            {"seed": 6, "static_mae": 131.9, "adaptive_mae": 31.1, "weekly_mae": 32.9, "static_rmse": 177.7, "adaptive_rmse": 48.2, "weekly_rmse": 55.0, "delay_h": 9,  "early_retrains": 6, "late_retrains": 4, "false_alarms": 0, "reduction_pct": 76.4},
            {"seed": 7, "static_mae": 132.9, "adaptive_mae": 32.5, "weekly_mae": 35.6, "static_rmse": 176.9, "adaptive_rmse": 52.3, "weekly_rmse": 64.1, "delay_h": 68, "early_retrains": 7, "late_retrains": 8, "false_alarms": 0, "reduction_pct": 75.6},
            {"seed": 8, "static_mae": 128.9, "adaptive_mae": 34.7, "weekly_mae": 33.9, "static_rmse": 171.4, "adaptive_rmse": 58.9, "weekly_rmse": 59.4, "delay_h": 15, "early_retrains": 9, "late_retrains": 13, "false_alarms": 0, "reduction_pct": 73.1},
            {"seed": 9, "static_mae": 131.6, "adaptive_mae": 35.3, "weekly_mae": 35.1, "static_rmse": 177.1, "adaptive_rmse": 55.8, "weekly_rmse": 68.2, "delay_h": 7,  "early_retrains": 6, "late_retrains": 13, "false_alarms": 0, "reduction_pct": 73.2},
        ],
        "detection": {
            "mean_delay_hours": 21.5,
            "median_delay_hours": 15.5,
            "std_delay_hours": 20.7,
            "min_delay_hours": 2,
            "max_delay_hours": 68,
            "detection_rate": "10/10 (100%)",
            "false_alarms_before_onset": 0,
            "mean_early_retrains_3w": 6.2,
            "mean_later_retrains": 10.0,
            "total_alarms_raised": 162,
            "page_hinkley_alarms": 161,
            "input_monitor_alarms": 1,
        },
        "statistical_tests": [
            {"comparison": "Static vs Adaptive", "mae_diff_kw": 101.0, "t_stat": 63.5, "t_p_value": 3.0e-13, "wilcoxon_w": 0.0, "wilcoxon_p_value": 0.0020, "significant": True},
            {"comparison": "Weekly vs Adaptive", "mae_diff_kw": 1.5, "t_stat": 2.97, "t_p_value": 0.014, "wilcoxon_w": 5.0, "wilcoxon_p_value": 0.027, "significant": True},
            {"comparison": "Static vs Weekly", "mae_diff_kw": 99.4, "t_stat": 61.2, "t_p_value": 2.0e-13, "wilcoxon_w": 0.0, "wilcoxon_p_value": 0.0020, "significant": True},
        ],
        "compute": {
            "monitoring_cost_per_hour_ms": 0.049,
            "single_retrain_time_s": 0.12,
            "retraining_count_ratio": "4.9x fewer retrainings for Adaptive vs Weekly",
            "compute_time_ratio": "4.9x less compute for Adaptive vs Weekly",
        }
    },
    "nodrift": {
        "scenario": "No Drift Control Scenario (Stationary)",
        "summary": {
            "static": {
                "name": "Static Model",
                "mae": [25.5, 0.6],
                "rmse": [37.3, 0.7],
                "nrmse": [1.87, 0.03],
                "retrainings": [0.0, 0.0],
                "retraining_time_s": [0.0, 0.0],
            },
            "adaptive": {
                "name": "Adaptive Model",
                "mae": [25.5, 0.6],
                "rmse": [37.3, 0.7],
                "nrmse": [1.87, 0.03],
                "retrainings": [0.0, 0.0],
                "retraining_time_s": [0.0, 0.0],
                "alarms_raised": 0,
            },
            "weekly": {
                "name": "Weekly Retrained Model",
                "mae": [33.2, 1.5],
                "rmse": [60.6, 8.4],
                "nrmse": [3.03, 0.42],
                "retrainings": [80.0, 0.0],
                "retraining_time_s": [9.92, 0.39],
            },
        },
        "per_seed": [
            {"seed": 0, "static_mae": 25.5, "adaptive_mae": 25.5, "weekly_mae": 31.1, "static_rmse": 37.6, "adaptive_rmse": 37.6, "weekly_rmse": 52.6},
            {"seed": 1, "static_mae": 25.0, "adaptive_mae": 25.0, "weekly_mae": 33.9, "static_rmse": 36.8, "adaptive_rmse": 36.8, "weekly_rmse": 60.3},
            {"seed": 2, "static_mae": 26.3, "adaptive_mae": 26.3, "weekly_mae": 33.3, "static_rmse": 38.0, "adaptive_rmse": 38.0, "weekly_rmse": 51.3},
            {"seed": 3, "static_mae": 25.7, "adaptive_mae": 25.7, "weekly_mae": 33.0, "static_rmse": 37.8, "adaptive_rmse": 37.8, "weekly_rmse": 56.0},
            {"seed": 4, "static_mae": 26.1, "adaptive_mae": 26.1, "weekly_mae": 34.6, "static_rmse": 38.0, "adaptive_rmse": 38.0, "weekly_rmse": 64.9},
            {"seed": 5, "static_mae": 26.3, "adaptive_mae": 26.3, "weekly_mae": 35.5, "static_rmse": 38.1, "adaptive_rmse": 38.1, "weekly_rmse": 74.5},
            {"seed": 6, "static_mae": 25.1, "adaptive_mae": 25.1, "weekly_mae": 31.0, "static_rmse": 36.8, "adaptive_rmse": 36.8, "weekly_rmse": 50.9},
            {"seed": 7, "static_mae": 25.1, "adaptive_mae": 25.1, "weekly_mae": 34.2, "static_rmse": 36.9, "adaptive_rmse": 36.9, "weekly_rmse": 64.4},
            {"seed": 8, "static_mae": 25.0, "adaptive_mae": 25.0, "weekly_mae": 31.8, "static_rmse": 36.3, "adaptive_rmse": 36.3, "weekly_rmse": 58.7},
            {"seed": 9, "static_mae": 25.1, "adaptive_mae": 25.1, "weekly_mae": 34.1, "static_rmse": 36.8, "adaptive_rmse": 36.8, "weekly_rmse": 72.6},
        ],
        "weekly_penalty_pct": 30.2,
    }
}

# Sensitivity studies (Tables 6.7, 6.8, 6.9, 6.10, 6.11)
SENSITIVITY_BENCHMARK = {
    "detectors": [
        {"detector": "Page-Hinkley (Proposed)", "drift_mae": 33.7, "retrainings": 15.2, "delay_h": 19.4, "detected": "5/5", "no_drift_alarms": 0.0, "no_drift_mae": 25.7, "type": "Error sequential"},
        {"detector": "CUSUM", "drift_mae": 33.8, "retrainings": 37.4, "delay_h": 12.6, "detected": "5/5", "no_drift_alarms": 7.8, "no_drift_mae": 26.8, "type": "Error sequential"},
        {"detector": "ADWIN", "drift_mae": 36.2, "retrainings": 9.2, "delay_h": 40.6, "detected": "5/5", "no_drift_alarms": 1.6, "no_drift_mae": 27.4, "type": "Window adaptive"},
        {"detector": "KS + PSI Only", "drift_mae": 35.0, "retrainings": 153.4, "delay_h": 128.6, "detected": "5/5", "no_drift_alarms": 153.0, "no_drift_mae": 32.4, "type": "Input distribution"},
    ],
    "threshold_lambda": [
        {"lambda": 6, "delay_h": 12.4, "drift_retrainings": 45.8, "drift_mae": 33.6, "no_drift_alarms": 18.6, "no_drift_mae": 27.8},
        {"lambda": 10, "delay_h": 14.0, "drift_retrainings": 25.0, "drift_mae": 34.0, "no_drift_alarms": 3.8, "no_drift_mae": 26.4},
        {"lambda": 15, "delay_h": 19.4, "drift_retrainings": 15.2, "drift_mae": 33.7, "no_drift_alarms": 0.0, "no_drift_mae": 25.7, "baseline": True},
        {"lambda": 25, "delay_h": 24.4, "drift_retrainings": 9.4, "drift_mae": 34.5, "no_drift_alarms": 0.0, "no_drift_mae": 25.7},
        {"lambda": 40, "delay_h": 30.4, "drift_retrainings": 8.8, "drift_mae": 37.7, "no_drift_alarms": 0.0, "no_drift_mae": 25.7},
    ],
    "cooldown_hours": [
        {"cooldown_h": 12, "retrainings": 22.0, "mae_kw": 33.0, "retraining_time_s": 3.49},
        {"cooldown_h": 24, "retrainings": 20.4, "mae_kw": 33.3, "retraining_time_s": 3.56},
        {"cooldown_h": 48, "retrainings": 15.2, "mae_kw": 33.7, "retraining_time_s": 2.60, "baseline": True},
        {"cooldown_h": 96, "retrainings": 11.8, "mae_kw": 33.5, "retraining_time_s": 1.95},
        {"cooldown_h": 168, "retrainings": 10.4, "mae_kw": 34.3, "retraining_time_s": 1.71},
    ],
    "retraining_window_weeks": [
        {"window_weeks": 2, "retrainings": 31.2, "mae_kw": 38.3, "retraining_time_s": 3.71},
        {"window_weeks": 4, "retrainings": 15.2, "mae_kw": 33.7, "retraining_time_s": 2.60, "baseline": True},
        {"window_weeks": 6, "retrainings": 12.4, "mae_kw": 32.9, "retraining_time_s": 2.35},
        {"window_weeks": 8, "retrainings": 13.8, "mae_kw": 33.5, "retraining_time_s": 2.57},
    ],
    "drift_magnitude": [
        {"magnitude": 0.0, "static_mae": 25.7, "adaptive_mae": 25.7, "reduction_pct": 0.0, "detected": "0/5", "retrainings": 0.0},
        {"magnitude": 0.1, "static_mae": 28.4, "adaptive_mae": 28.4, "reduction_pct": 0.0, "detected": "0/5", "retrainings": 0.0},
        {"magnitude": 0.25, "static_mae": 40.2, "adaptive_mae": 34.0, "reduction_pct": 15.4, "detected": "4/5", "retrainings": 5.2},
        {"magnitude": 0.5, "static_mae": 69.8, "adaptive_mae": 32.6, "reduction_pct": 53.3, "detected": "5/5", "retrainings": 9.8},
        {"magnitude": 1.0, "static_mae": 135.9, "adaptive_mae": 33.7, "reduction_pct": 75.2, "detected": "5/5", "retrainings": 15.2, "baseline": True},
        {"magnitude": 1.5, "static_mae": 202.0, "adaptive_mae": 34.7, "reduction_pct": 82.8, "detected": "5/5", "retrainings": 21.2},
    ],
}

def generate_benchmark_cache():
    with open(OUT_DIR / "ten_seeds_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(TEN_SEEDS_BENCHMARK, f, indent=2)

    with open(OUT_DIR / "sensitivity_benchmark.json", "w", encoding="utf-8") as f:
        json.dump(SENSITIVITY_BENCHMARK, f, indent=2)

    print("Precomputed benchmarks successfully generated.")

if __name__ == "__main__":
    generate_benchmark_cache()
