# Adaptive Wind Power Forecasting Using Concept Drift Detection

**Team:** `B14` | **A Final-Year Artificial Intelligence & Machine Learning Engineering Project**  
*Department of Artificial Intelligence and Machine Learning*  
*Panimalar Engineering College (An Autonomous Institution, Affiliated to Anna University, Chennai)*  

**Candidates:**  
- **Thanya B**  
- **Thejessri S**  

**Supervisor:** Mr. M. Ezhilvendhan, M.E., Assistant Professor  
**Head of Department:** Dr. G. Suresh, M.Tech., Ph.D.  
**Academic Year:** 2025–2026 | October 2026  

> 📊 **Official Deliverables for Viva Examination:**
> - 🖥️ **Presentation Deck (20 Slides, Widescreen 16:9):** [`reports/Adaptive_Wind_Power_Forecasting_Team_B14.pptx`](reports/Adaptive_Wind_Power_Forecasting_Team_B14.pptx)
> - 📄 **Complete 69-Page Final Project Report:** [`reports/Adaptive_Wind_Power_Forecasting_Team_B14_Final_Report.pdf`](reports/Adaptive_Wind_Power_Forecasting_Team_B14_Final_Report.pdf)
> - 🎓 **Viva Voce & Technical Guide:** [`reports/Project_Explanation_and_Viva_Guide.pdf`](reports/Project_Explanation_and_Viva_Guide.pdf)

---

## 🖼️ Application Screenshots & Output Gallery

| View & Output | Screenshot |
| :--- | :--- |
| **1. SCADA Login & Access Control Portal**<br>*Features Panimalar Engineering College branding, Examiner & Operator roles, and 1-Click Quick Demo Access for viva exams.* | ![Login Access Portal](docs/screenshots/01_login_access_portal.png) |
| **2. Executive Live Overview Dashboard**<br>*Real-time generation hero gauge (kW), 3 colorful metric cards, capacity factor gauge (0-2000 kW), and drift onset tracking.* | ![Live Overview](docs/screenshots/02_overview_dashboard_live.png) |
| **3. 80-Week Horizon & Drift Audit Log**<br>*Weekly error divergence (Static surging to 140 kW vs Adaptive steady at 33 kW) and chronological Page-Hinkley audit trail.* | ![80-Wk Drift History](docs/screenshots/03_overview_dashboard_drift_history.png) |
| **4. Forecasting Studio & Model Workbench**<br>*1-Click weather presets (🍃 Light, 💨 Moderate, ⚡ Gale), interactive meteorological sliders, and generation forecast.* | ![Forecasting Studio](docs/screenshots/04_forecasting_studio.png) |
| **5. Concept Drift Detection & Telemetry**<br>*Page-Hinkley cumulative deviation stat vs threshold λ=12.0, online stream playback controls, and KS/PSI distribution checks.* | ![Drift Monitoring](docs/screenshots/05_drift_monitoring.png) |
| **6. Adaptive Learning Controller**<br>*Sample weighting curve (0.08x pre-change decay), 48h cooldown guard, and autonomous retraining audit history.* | ![Adaptive Learning](docs/screenshots/06_adaptive_learning.png) |
| **7. Baseline Model Comparison & Verification**<br>*3 pastel hero cards (Static in Rose, Adaptive in Mint, Weekly in Sky), paired t-test ($p < 0.05$), and 4.9x compute reduction.* | ![Model Comparison](docs/screenshots/07_model_comparison.png) |
| **8. Dataset Explorer & Feature Analytics**<br>*Empirical aerodynamic power curve scatter plot, 16-sector wind rose with wake highlighting, and paginated SCADA table.* | ![Dataset Explorer](docs/screenshots/08_dataset_explorer.png) |
| **9. Reproducible Experiments & Reports**<br>*10-seed empirical benchmark table verifying the 75.0% error reduction, sensitivity curves, and one-click PDF export.* | ![Experiments & Reports](docs/screenshots/09_experiments_report.png) |

---

## 1. Project Overview & Motivation

Wind power generation is governed by the non-linear aerodynamic cubic law:
$$P = \frac{1}{2} \rho A C_p v^3$$
Because power scales with the cube of wind speed, a modest $10\%$ error in wind velocity amplifies into a $\sim 33\%$ discrepancy in generated electrical power.

Most conventional wind power forecasting systems deploy models trained once on historical records under an implicit assumption of stationarity. However, real-world wind turbine operations are inherently non-stationary:
1. **Turbine Component Derating & Ageing:** Blade erosion, surface roughness, and mechanical wear degrade output curves over time.
2. **Directional Wake Losses:** Construction of downwind turbine clusters or physical obstacles causes direction-dependent aerodynamic turbulence and shadow losses.
3. **Sensor Recalibration / Virtual Drift:** Anemometers replaced or recalibrated shift recorded speeds without altering actual physical energy yield.

When such concept drifts occur, static forecasting models deteriorate silently, accumulating severe economic penalties in wholesale electricity dispatch and grid balancing reserves. Blind periodic retraining (such as fixed weekly updates) wastes computational resources and increases forecast variance when conditions are stationary.

This project implements an **evidence-driven, lightweight, interpretable drift-adaptive forecasting framework** that continuously monitors forecast errors, detects statistical concept shifts, and retrains the model on a drift-aware sliding window only when empirical evidence justifies adaptation.

---

## 2. Core Methodology & Architecture

```
[Raw SCADA / Weather Stream]
            │
            ▼
┌─────────────────────────────────┐
│ M2: 10-Feature Preprocessing   │ ── Strict chronological ordering;
│ (Wind speed, sin/cos dir, lags) │    no future target leakage
└─────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│ M3: Base Forecasting Model      │ ── HistGradientBoostingRegressor
│ (Trained on initial 26 weeks)   │    (120 trees, lr=0.1, max_depth=6)
└─────────────────────────────────┘
            │
            ├──► Forecast Issued: ŷ(t)
            │
            ▼ (Hour t+1: Actual Power y(t) Revealed)
┌─────────────────────────────────┐
│ M4: Prediction & Error Monitor  │ ── Heteroscedastic standardization:
│ (Residual Standardisation)      │    z(t) = |y(t) - ŷ(t)| / m(ŷ(t))
└─────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│ M5: Dual Drift Detectors        │ ── Error: Page-Hinkley test (λ=15σ₀, δ=0.6σ₀)
│ (Error Stream + Input Checks)   │    Input: Daily KS-test & PSI (advisory channel)
└─────────────────────────────────┘
            │
            ▼ (Alarm Condition Breached)
┌─────────────────────────────────┐
│ M6: Adaptation Controller       │ ── 48-hour refractory cooldown check;
│ (Drift-Aware Retraining)        │    4-week window (672 h), recency half-life 336 h,
└─────────────────────────────────┘    pre-change downweighting (0.08x for t < τ̂ - 12)
            │
            └──► Deploys Updated Model v(k+1)
```

### Key Algorithmic Contributions

1. **Heteroscedastic Residual Standardisation:**
   Absolute prediction errors grow naturally on the steep region of the power curve ($8-12\text{ m/s}$). Raw error monitoring would cause seasonal false alarms during windy months. We calibrate a 6-quantile error map $m(\hat{y}_t)$ on rolling origins in the initial window, creating a scale-free score $z_t = |y_t - \hat{y}_t| / m(\hat{y}_t)$ with baseline mean $\mu_0 \approx 1.0$ and std $\sigma_0 \approx 0.8$.

2. **Page-Hinkley Sequential Inspection:**
   Monitors cumulative excess deviations:
   $$m_t = \sum_{i \le t} (z_i - \mu_0 - \delta), \quad M_t = \min_{i \le t} m_i$$
   An alarm is raised when $m_t - M_t > \lambda$ ($\lambda = 15 \sigma_0 = 12.0$, $\delta = 0.6 \sigma_0 = 0.48$).
   The minimum step yields an exact change point estimate:
   $$\hat{\tau} = \text{argmin}_{i \le t} m_i$$

3. **Decoupling Input Drift from Retraining Triggers:**
   Hourly wind speed is an autocorrelated process ($\text{AR}(1)\ \phi = 0.96$). Two-sample Kolmogorov-Smirnov (KS) tests and the Population Stability Index (PSI) fire repeatedly on harmless seasonal regime shifts ($p < 10^{-19}$). The framework treats input distribution shifts strictly as an **advisory channel**, accepting input alarms only when corroborated by degraded prediction accuracy ($\bar{z}_{24\text{h}} > \mu_0 + 2\sigma_0$).

4. **Drift-Aware Sample Weighting & Cooldown Guard:**
   When retraining is authorized:
   - Only the most recent $W = 672$ hours (4 weeks) are ingested.
   - Recency weights decay with a half-life of 2 weeks: $w_i = 2^{-(k-i)/336}$.
   - Observations preceding the estimated change point ($\hat{\tau} - 12$) are downweighted by $\kappa = 0.08$.
   - A 48-hour refractory cooldown prevents repeated retraining before the new model takes effect.

---

## 3. Empirical Results & Hypotheses Verification

Evaluated on an 80-week online stream ($13,440$ hourly forecasts per seed) across 10 independent random seeds against a frozen Static baseline and a scheduled Weekly-retrained baseline:

### Forecast Accuracy (10 Random Seeds, Mean ± Std)

| Scenario & Metric | Static Model | Adaptive Framework (Proposed) | Weekly Retrain | Performance Gain |
| :--- | :---: | :---: | :---: | :---: |
| **Drift: MAE (kW)** | $134.7 \pm 5.6$ | **$33.7 \pm 2.1$** | $35.3 \pm 1.3$ | **75.0% error reduction** ($p = 3.0 \times 10^{-13}$) |
| **Drift: RMSE (kW)** | $178.4 \pm 5.6$ | **$53.0 \pm 3.7$** | $62.7 \pm 5.4$ | **70.3% error reduction** ($p = 2.2 \times 10^{-4}$) |
| **Drift: nRMSE (%)** | $8.92 \pm 0.28\%$ | **$2.65 \pm 0.19\%$** | $3.14 \pm 0.27\%$ | Improved by 6.27 percentage points |
| **Drift: Retrainings** | $0$ | **$16.2 \pm 6.6$** | $80.0$ | **4.9× fewer retrainings** |
| **Drift: Compute Time (s)** | $0.00\text{ s}$ | **$1.98 \pm 0.82\text{ s}$** | $9.59 \pm 0.53\text{ s}$ | **4.9× less computation** |
| **No-Drift: MAE (kW)** | $25.5 \pm 0.6$ | **$25.5 \pm 0.6$** | $33.2 \pm 1.5$ | Weekly suffers **+30.2% penalty** |
| **No-Drift: Alarms** | — | **0 in 10 seeds** | — | **Zero false alarms** |

### Outcome of Research Hypotheses

- **H1 (Supported):** Drift-triggered retraining lowers MAE from $134.7$ to $33.7\text{ kW}$ under drift ($p = 3.0 \times 10^{-13}$).
- **H2 (Supported):** Under stationary conditions, the adaptive model raises 0 alarms; forecasts are identical to the static baseline.
- **H3 (Supported):** Adaptive forecasting matches or outperforms blind weekly retraining ($33.7\text{ vs } 35.3\text{ kW}$) with $4.9\times$ fewer retrainings.
- **H4 (Supported):** Adaptation gain scales with drift magnitude ($15\%$ gain at mag 0.25, $75\%$ at mag 1.0, $83\%$ at mag 1.5).

---

## 4. Technology Stack

- **Backend:** Python 3.12 / 3.14, FastAPI, Uvicorn, Scikit-learn, SciPy, Pandas, NumPy, Joblib, Pydantic, ReportLab, Pytest.
- **Frontend:** React 18, Vite, Tailwind CSS, Recharts, Lucide React.
- **Architecture:** Clean REST API with asynchronous background jobs, modular ML services, and dark-themed SCADA dashboard.

---

## 5. Quick Start & Execution Guide

### Prerequisites
- Python 3.11+ installed and available on PATH (`python --version`).
- Node.js v18+ and npm installed (`node --version`).

### Option A: One-Click Startup (Recommended for Windows)
Double-click `start_project.bat` in the project root folder.
This script automatically:
1. Launches the FastAPI backend server on `http://127.0.0.1:8000`.
2. Launches the React Vite development server on `http://localhost:5173`.
3. Opens the interactive analytics dashboard in your default web browser.

---

### Option B: Manual Terminal Execution

#### Terminal 1 — Backend API
```powershell
# Navigate to the project root
cd C:\Users\SFJ036\.gemini\antigravity\scratch\wind-power-forecasting

# Start the FastAPI backend with uvicorn
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Swagger API Documentation: `http://127.0.0.1:8000/docs`
- Health Diagnostic: `http://127.0.0.1:8000/api/health`

#### Terminal 2 — React Frontend Dashboard
```powershell
# Navigate to the frontend directory
cd C:\Users\SFJ036\.gemini\antigravity\scratch\wind-power-forecasting\frontend

# Install dependencies (if not already installed)
npm.cmd install --strict-ssl=false

# Launch Vite development server
npm.cmd run dev
```
- Open browser at: `http://localhost:5173`

---

## 6. Running Automated Tests

A comprehensive suite of 29 unit and integration tests verifies the entire pipeline:
```powershell
cd C:\Users\SFJ036\.gemini\antigravity\scratch\wind-power-forecasting

# Run pytest suite
python -m pytest backend/tests/ -v
```

Tests cover:
- Synthetic data generation and Betz-curve aerodynamic equations.
- Target leakage prevention in 10-feature engineering.
- HistGradientBoostingRegressor model training, inference, and serialization.
- Scale-free heteroscedastic residual standardization.
- Page-Hinkley detector sensitivity, change point estimation, and reset mechanics.
- Two-sample Kolmogorov-Smirnov and Population Stability Index (PSI) metrics.
- 48-hour refractory cooldown enforcement and sample weighting decay.
- Benchmark verification of Static, Adaptive, and Weekly models under drift and no-drift.
- CSV upload validation (column schema, range checks, timestamp ordering).
- REST API endpoint contracts.

---

## 7. Web Dashboard Pages & Features

1. **Overview Dashboard (`/`):**
   - Live KPI cards: Latest 1h forecast, observed power, MAE, RMSE, nRMSE, Page-Hinkley statistic, model version.
   - Actual vs Predicted wind power chart with zoom into the drift onset window.
   - 80-week MAE divergence curve comparing Static, Adaptive, and Weekly models.
   - Resource dynamics chart (weekly wind speed vs generated power).
   - Drift alarm and retraining events log.

2. **Forecasting Studio (`/forecasting`):**
   - Interactive 1-hour-ahead forecast generator with manual input sliders for wind speed, direction, temperature, and power lags.
   - Model hyperparameter tuning workbench (boosting trees, learning rate, tree depth).
   - One-click model training trigger.
   - Recent 24-hour prequential forecast verification table with CSV download.

3. **Drift Monitoring (`/drift`):**
   - Simulated stream playback controls (Step 1h, Step 24h, Reset).
   - Standardized error stream $z(t)$ and Page-Hinkley statistic curve against threshold $\lambda = 15\sigma_0$.
   - Live input-distribution monitor cards (KS test p-value, KS statistic, PSI score).
   - Educational callouts explaining why virtual input drift is decoupled from retraining triggers.
   - Detailed change-point history and detection latency table.

4. **Adaptive Learning (`/adaptation`):**
   - Active model version and training window telemetry.
   - 48-hour refractory cooldown countdown timer.
   - Interactive sample weights curve showing recency decay ($h = 336\text{ h}$) and change-point downweighting ($0.08\times$).
   - Full audit history of autonomous and manual model retrainings.
   - Manual retraining trigger with safety confirmation modal.

5. **Model Comparison (`/comparison`):**
   - Direct head-to-head performance comparison of Static, Adaptive, and Weekly-retrained models.
   - Toggle between **Drift Scenario** (abrupt shift at week 28) and **No-Drift Control Scenario**.
   - Interactive comparison bar charts for MAE, RMSE, nRMSE, Retraining Count, and Cumulative Runtime.
   - Paired Student's t-test and Wilcoxon signed-rank test statistical significance tables ($p < 0.05$).
   - Automatically generated analytical interpretation grounded strictly in computed results.

6. **Dataset Explorer (`/dataset`):**
   - Paginated observation table with live search and filtering.
   - Dataset health summary (sample count, time span, 0 missing values).
   - Measured wind speed vs power scatter plot with empirical turbine power curve.
   - Directional wind rose distribution with red highlighting for the wake sector ($200^\circ-265^\circ$).
   - Pearson correlation heatmap between meteorological features and power output.
   - Active CSV dataset export.

7. **Experiments & Reports (`/experiments`):**
   - Reproducible research runner: select random seed (0 to 9), scenario, and detector (Page-Hinkley, CUSUM, ADWIN, KS+PSI).
   - Non-blocking background execution with live progress bar.
   - 10-seed aggregate verification table matching project report Table 6.1 and Appendix D.1.
   - Interactive sensitivity curves (threshold $\lambda$, cooldown hours, window length, drift magnitude).
   - One-click export to CSV, structured JSON, and **Download Publication-Quality PDF Report**.

---

## 8. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check, dataset mode, and model version |
| `GET` | `/api/dashboard/summary` | Real-time overview KPIs, weekly trends, and alarms |
| `POST` | `/api/data/generate` | Generate synthetic stream with configurable seed and drift |
| `POST` | `/api/data/upload` | Upload and validate custom CSV dataset |
| `GET` | `/api/data/preview` | Paginated dataset rows, summary stats, and scatter data |
| `GET` | `/api/data/download` | Download active dataset as CSV |
| `POST` | `/api/forecast/predict` | Compute 1-hour-ahead forecast for specified inputs |
| `GET` | `/api/forecast/history` | Historical actual vs predicted values and error series |
| `POST` | `/api/forecast/train` | Train base model on historical training window |
| `GET` | `/api/drift/status` | Current Page-Hinkley statistic, KS test, and PSI metrics |
| `GET` | `/api/drift/events` | List of confirmed drift alarms, change points, and delays |
| `GET` | `/api/drift/trace` | Time-series trace of Page-Hinkley statistic vs threshold |
| `POST` | `/api/drift/simulate_step` | Advance online stream playback by N hours (1h / 24h) |
| `POST` | `/api/drift/simulate_reset` | Reset simulation playback to initial stream hour (hour 4,368) |
| `GET` | `/api/adaptation/status` | Model version, cooldown status, and window config |
| `GET` | `/api/adaptation/history` | Audit log of all model retraining events |
| `GET` | `/api/adaptation/weights_curve` | Sample weights function over 672h retraining window |
| `POST` | `/api/adaptation/retrain` | Trigger manual retraining with audit logging |
| `GET` | `/api/model/comparison` | Head-to-head comparison of Static, Adaptive, and Weekly models |
| `POST` | `/api/experiments/run` | Enqueue background experiment job (seed 0-9) |
| `GET` | `/api/experiments/status/{id}` | Poll background experiment job progress and results |
| `GET` | `/api/experiments/benchmark` | Retrieve 10-seed benchmark results table |
| `GET` | `/api/experiments/sensitivity` | Retrieve sensitivity sweep analysis data |
| `GET` | `/api/reports/pdf` | Download official executive summary report PDF |
| `GET` | `/api/reports/json` | Export full benchmark results as JSON |
| `GET` | `/api/reports/csv` | Export per-seed drift comparison as CSV |

---

## 9. Visual Studio Code Workspace Configuration

To open and debug in Visual Studio Code:
1. Open Visual Studio Code.
2. Select **File -> Open Folder...** and choose:
   `C:\Users\SFJ036\.gemini\antigravity\scratch\wind-power-forecasting`
3. The project includes pre-configured `.vscode/launch.json` debug profiles:
   - **FastAPI: Run Backend**: Runs the backend under the debugpy debugger with hot reload.
   - **Pytest: Run All Tests**: Executes all 29 automated tests directly within VS Code's Test Explorer.

---

## 10. Authors & Acknowledgements

- Thanya B & Thejessri S
