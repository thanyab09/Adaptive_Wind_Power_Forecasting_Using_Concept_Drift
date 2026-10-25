from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
UPLOADS_DATA_DIR = DATA_DIR / "uploads"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
SAVED_MODELS_DIR = ARTIFACTS_DIR / "saved_models"
REPORTS_DIR = BASE_DIR / "reports"
PRECOMPUTED_DIR = Path(__file__).resolve().parent / "data" / "precomputed"

for d in [DATA_DIR, SAMPLE_DATA_DIR, UPLOADS_DATA_DIR, ARTIFACTS_DIR, SAVED_MODELS_DIR, REPORTS_DIR, PRECOMPUTED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Wind farm and simulation parameters (from project report)
RATED_POWER_KW = 2000.0  # 2 MW turbine unit
CUT_IN_SPEED = 3.0       # m/s
RATED_SPEED = 12.0       # m/s
CUT_OUT_SPEED = 25.0     # m/s
HOURS_PER_WEEK = 168
TOTAL_WEEKS = 106
TOTAL_HOURS = TOTAL_WEEKS * HOURS_PER_WEEK  # 17,808 hours
INITIAL_WEEKS = 26
INITIAL_HOURS = INITIAL_WEEKS * HOURS_PER_WEEK  # 4,368 hours
STREAM_WEEKS = 80
STREAM_HOURS = STREAM_WEEKS * HOURS_PER_WEEK  # 13,440 hours
DRIFT_WEEK = 28
DRIFT_ONSET_HOUR = DRIFT_WEEK * HOURS_PER_WEEK  # 4,704 hours

# Feature list
FEATURE_NAMES = [
    "v",       # measured wind speed (m/s)
    "sin_d",   # cyclic sin(direction)
    "cos_d",   # cyclic cos(direction)
    "temp",    # air temperature (°C)
    "p_l1",    # power lag 1 hour
    "p_l2",    # power lag 2 hours
    "p_l24",   # power lag 24 hours
    "p_m6",    # rolling mean power 6h
    "v_l1",    # wind speed lag 1 hour
    "v_m3",    # rolling mean wind speed 3h
]

# Forecaster model parameters
BOOSTING_MAX_ITER = 120
BOOSTING_LEARNING_RATE = 0.1
BOOSTING_MAX_DEPTH = 6
BOOSTING_MIN_SAMPLES_LEAF = 20
BOOSTING_LOSS = "squared_error"

# Drift detector parameters
PAGE_HINKLEY_DELTA_FACTOR = 0.6   # delta = 0.6 * sigma0
PAGE_HINKLEY_LAMBDA_FACTOR = 15.0 # lambda = 15.0 * sigma0
KS_ALPHA = 1e-6                   # p-value threshold for input drift
PSI_THRESHOLD = 0.25              # population stability index threshold
ERROR_CORROBORATION_SIGMA = 2.0   # recent error must exceed mu0 + 2*sigma0

# Adaptation controller parameters
RETRAINING_WINDOW_HOURS = 4 * HOURS_PER_WEEK  # 672 hours (4 weeks)
RECENCY_HALF_LIFE_HOURS = 336.0               # 2 weeks
PRE_CHANGE_WEIGHT = 0.08                      # downweight factor for pre-change samples
COOLDOWN_HOURS = 48                           # refractory period after retraining
PREDICTION_BLOCK_HOURS = 24                   # 24-hour block stepping for fast evaluation
