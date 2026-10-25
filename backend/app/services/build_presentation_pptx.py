"""
Builds an authentic, comprehensive, publication-grade 20-slide PowerPoint presentation
for Team B14: Adaptive Wind Power Forecasting Using Concept Drift Detection.
Panimalar Engineering College - B.Tech AI & ML Final-Year Project.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
OUTPUT_PPTX_REPORTS = os.path.join(BASE_DIR, "reports", "Adaptive_Wind_Power_Forecasting_Team_B14.pptx")
USER_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads", "Adaptive_Wind_Power_Forecasting_Team_B14.pptx")

# Color Constants
C_NAVY = RGBColor(15, 23, 42)        # #0F172A
C_TEAL = RGBColor(13, 148, 136)      # #0D9488
C_EMERALD = RGBColor(5, 150, 105)    # #059669
C_SKY = RGBColor(2, 132, 199)        # #0284C7
C_AMBER = RGBColor(217, 119, 6)      # #D97706
C_ROSE = RGBColor(225, 29, 72)       # #E11D48
C_PURPLE = RGBColor(124, 58, 237)    # #7C3AED
C_BG_LIGHT = RGBColor(248, 250, 252) # #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)  # White
C_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
C_TEXT_DARK = RGBColor(30, 41, 59)   # #1E293B
C_TEXT_MUTED = RGBColor(100, 116, 139)# #64748B
C_WHITE = RGBColor(255, 255, 255)

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    def add_header(slide, title_text, category_text="TEAM B14  |  FINAL YEAR CAPSTONE"):
        # Header banner shape
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = C_TEAL

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY

        # Right-side Team Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.6), Inches(0.45), Inches(1.9), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_BG_LIGHT
        badge.line.color.rgb = C_TEAL
        badge.line.width = Pt(1)
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = "TEAM: B14"
        bp.font.size = Pt(12)
        bp.font.bold = True
        bp.font.color.rgb = C_TEAL
        bp.alignment = PP_ALIGN.CENTER

        # Separator line
        sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        sep.fill.solid()
        sep.fill.fore_color.rgb = C_BORDER
        sep.line.fill.background()

    def add_footer(slide, slide_num):
        # Footer text
        footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf = footer.text_frame
        p = tf.paragraphs[0]
        p.text = "Adaptive Wind Power Forecasting Using Concept Drift Detection | Panimalar Engineering College | Slide " + str(slide_num)
        p.font.size = Pt(9)
        p.font.color.rgb = C_TEXT_MUTED
        p.font.italic = True

    def add_card(slide, left, top, width, height, title, items, accent_color=C_TEAL, bg_color=C_WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(13)
            p0.font.bold = True
            p0.font.color.rgb = accent_color
            p0.space_after = Pt(8)

        for i, item in enumerate(items):
            p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
            p.text = "• " + item if isinstance(item, str) else item[0]
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(4)

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    # Background card
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(241, 245, 249) # Slate-100
    bg.line.fill.background()

    # Inner White Plaque
    plaque = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.8), Inches(10.933), Inches(5.9))
    plaque.fill.solid()
    plaque.fill.fore_color.rgb = C_WHITE
    plaque.line.color.rgb = C_TEAL
    plaque.line.width = Pt(2)

    ptf = plaque.text_frame
    ptf.word_wrap = True
    ptf.margin_top = Inches(0.4)
    ptf.margin_left = Inches(0.6)
    ptf.margin_right = Inches(0.6)

    p0 = ptf.paragraphs[0]
    p0.text = "PANIMALAR ENGINEERING COLLEGE"
    p0.font.size = Pt(15)
    p0.font.bold = True
    p0.font.color.rgb = C_NAVY
    p0.alignment = PP_ALIGN.CENTER

    p1 = ptf.add_paragraph()
    p1.text = "An Autonomous Institution, Affiliated to Anna University, Chennai\nDepartment of Artificial Intelligence & Machine Learning"
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = C_TEXT_MUTED
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(18)

    p2 = ptf.add_paragraph()
    p2.text = "ADAPTIVE WIND POWER FORECASTING USING CONCEPT DRIFT DETECTION"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = C_TEAL
    p2.alignment = PP_ALIGN.CENTER

    p3 = ptf.add_paragraph()
    p3.text = "Final-Year B.Tech Capstone Project Presentation | October 2026"
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.color.rgb = C_AMBER
    p3.alignment = PP_ALIGN.CENTER
    p3.space_after = Pt(24)

    # Info Grid inside plaque
    tbox = slide1.shapes.add_textbox(Inches(2.2), Inches(4.3), Inches(8.933), Inches(1.8))
    ttf = tbox.text_frame
    tp0 = ttf.paragraphs[0]
    tp0.text = "TEAM B14 MEMBERS:"
    tp0.font.size = Pt(11)
    tp0.font.bold = True
    tp0.font.color.rgb = C_NAVY

    tp1 = ttf.add_paragraph()
    tp1.text = "1. THANYA B  [Reg. No: 211423247227]\n2. THEJESSRI S  [Reg. No: 211423247229]"
    tp1.font.size = Pt(11)
    tp1.font.color.rgb = C_TEXT_DARK
    tp1.space_after = Pt(10)

    tp2 = ttf.add_paragraph()
    tp2.text = "PROJECT SUPERVISOR:  Mr. M. Ezhilvendhan, M.E., Assistant Professor"
    tp2.font.size = Pt(11)
    tp2.font.bold = True
    tp2.font.color.rgb = C_EMERALD

    # ==========================================
    # SLIDE 2: AGENDA
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Presentation Outline & Key Agenda")
    add_card(slide2, 0.8, 1.6, 5.6, 5.1, "Part I: Problem & Methodology", [
        "1. Introduction, Non-Linear Cubic Aerodynamics & Motivation",
        "2. Concept Drift in Wind Energy: Real vs Virtual Drift",
        "3. Problem Statement & Research Hypotheses (H1 to H4)",
        "4. Literature Survey & Surveyed Works Comparison",
        "5. Proposed 7-Module Adaptive Architecture & Data Flow",
        "6. 10-Feature Engineering Pipeline & Leakage-Free Preprocessing",
        "7. Base Forecaster: HistGradientBoostingRegressor"
    ], accent_color=C_TEAL)

    add_card(slide2, 6.8, 1.6, 5.7, 5.1, "Part II: Results, Verification & UI", [
        "8. Heteroscedastic Error Calibration (6-Quantile Map)",
        "9. Dual Drift Monitoring: Page-Hinkley & KS/PSI Advisory Channel",
        "10. Adaptive Controller: Exponential Recency & Change-Point Weighting",
        "11. Benchmark Results: 75.0% MAE Reduction under Injected Drift",
        "12. Computational Overhead: 4.9× Fewer Retrainings than Weekly",
        "13. No-Drift Control Scenario & False Alarm Verification",
        "14. Full-Stack SCADA Web Platform & UI Outputs Gallery",
        "15. Conclusion, UN SDG Alignment & Future Roadmap"
    ], accent_color=C_SKY)
    add_footer(slide2, 2)

    # ==========================================
    # SLIDE 3: MOTIVATION & CUBIC LAW
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Wind Power Aerodynamics & Forecasting Motivation")
    add_card(slide3, 0.8, 1.6, 5.6, 5.1, "The Physics: Cubic Power Law", [
        "Kinetic Power Equation: P = 0.5 * rho * A * Cp * v^3",
        "Cubic Sensitivity: A 10% error in wind speed causes ~33% discrepancy in electrical generation!",
        "Non-linear turbine curve: Cut-in at 3 m/s, rated speed at 12 m/s (2000 kW), cut-out at 25 m/s.",
        "Steep Region 2 (8-12 m/s): Where 85% of operational forecasting errors concentrate.",
        "Air density variations: Cold winter air is denser, producing higher kinetic energy."
    ], accent_color=C_AMBER)

    add_card(slide3, 6.8, 1.6, 5.7, 5.1, "Grid Impact & Operational Challenges", [
        "Grid Dispatch Stability: Inaccurate forecasts force expensive spinning fossil reserves.",
        "Wholesale Market Penalties: Deviations between day-ahead bids and generation incur heavy imbalance fines.",
        "Intermittent Nature: Fast diurnal and seasonal fluctuations require continuous 1h-ahead accuracy.",
        "Conventional Failure: Models trained once assume stationarity, deteriorating silently as turbine physics evolve.",
        "Project Goal: Build an evidence-driven adaptive system that recalibrates only when necessary."
    ], accent_color=C_TEAL)
    add_footer(slide3, 3)

    # ==========================================
    # SLIDE 4: CONCEPT DRIFT IN WIND POWER
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Concept Drift Taxonomy: Real Drift vs Virtual Drift")
    add_card(slide4, 0.8, 1.6, 5.6, 5.1, "1. Real Concept Drift: P(y | x) Changes", [
        "Physical Turbine Degradation: Blade erosion, icing, gearbox friction reduce power output for identical wind speeds.",
        "Aerodynamic Wake Deficits: Construction of nearby downwind turbine clusters creates direction-dependent shadow losses (8.5% loss in 200°-265° sector).",
        "Operational Curtailment: Grid operator caps maximum power below rated nameplate.",
        "Critical Threat: Learned weather-to-power mapping becomes invalid; static models suffer persistent positive forecast bias."
    ], accent_color=C_ROSE)

    add_card(slide4, 6.8, 1.6, 5.7, 5.1, "2. Virtual Concept Drift: P(x) Changes", [
        "Seasonal Weather Regime Changes: Transition between summer and winter shifts mean speed and direction distributions.",
        "Sensor Recalibration: Anemometer recalibration shifts recorded speeds (e.g. 1.04x scaling) without altering energy conversion.",
        "Key Research Insight: Virtual weather shifts produce low KS p-values (< 1e-19) even when turbine physics remain stationary.",
        "Decoupling Rule: Input drift must act strictly as an advisory channel to prevent alarm storming."
    ], accent_color=C_SKY)
    add_footer(slide4, 4)

    # ==========================================
    # SLIDE 5: PROBLEM STATEMENT & EXISTING SYSTEMS
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Problem Statement & Limitations of Existing Systems")
    add_card(slide5, 0.8, 1.6, 5.6, 5.1, "Existing Practice & Drawbacks", [
        "1. Train-Once Static Deployment: Model trained on historical data is deployed frozen. When drift occurs, error jumps silently from 25 kW to 135 kW with no alert.",
        "2. Blind Calendar Retraining (Weekly/Monthly): Wastes massive computation when conditions are stationary; still reacts with days of lag to abrupt mid-week changes.",
        "3. Small Sample Variance Penalty: Blindly fitting a short 4-week window under stationary conditions worsens error by +30.2% due to high estimator variance.",
        "4. Complex Deep Learning Pipelines: Spatio-temporal GNNs/LSTMs are compute-heavy, hard to tune, and lack interpretable drift evidence."
    ], accent_color=C_ROSE)

    add_card(slide5, 6.8, 1.6, 5.7, 5.1, "Our Proposed Solution", [
        "Evidence-Driven Adaptation: Retraining triggers only when sequential statistical test proves error distribution has shifted.",
        "Lightweight Standard Regressor: Fast histogram gradient boosting (120 trees, 0.12s training time).",
        "Scale-Free Error Calibration: Normalizes errors by expected power variance to avoid seasonal false alarms.",
        "Drift-Aware Weighting: Retrains on 672h window, penalizing pre-change samples (0.08x) so new physics dominate.",
        "Honest Evaluation: 10 random seeds, no-drift controls, and reported detection latency and compute cost."
    ], accent_color=C_EMERALD)
    add_footer(slide5, 5)

    # ==========================================
    # SLIDE 6: RESEARCH QUESTION & HYPOTHESES
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Research Questions & Testable Hypotheses")
    add_card(slide6, 0.8, 1.6, 11.733, 5.1, "Formal Research Hypotheses (Table 1.3 in Report)", [
        "Central Question: Can concept drift detection and adaptive learning keep wind-power forecasts reliable under changing conditions than a model trained once, and at what cost?",
        "H1 [Supported]: When the weather-to-power relationship changes, drift-triggered retraining yields a statistically significant lower forecast error than a static model (MAE 134.7 -> 33.7 kW, p = 3.0e-13).",
        "H2 [Supported]: When no drift occurs, the adaptive model raises ZERO alarms and its accuracy equals the static model (MAE 25.5 kW; 0 false alarms across 10 random seeds).",
        "H3 [Supported]: Drift-triggered retraining reaches accuracy comparable or superior to blind weekly retraining (33.7 kW vs 35.3 kW) while requiring 4.9x fewer retrainings (16.2 vs 80.0 retrains).",
        "H4 [Supported]: Adaptation benefits scale non-linearly with drift magnitude; subtle shifts (<= 0.1) are safely ignored, while large shifts yield up to 83% error reduction."
    ], accent_color=C_TEAL)
    add_footer(slide6, 6)

    # ==========================================
    # SLIDE 7: LITERATURE SURVEY & GAPS
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Literature Survey & Identified Research Gaps")
    add_card(slide7, 0.8, 1.6, 5.6, 5.1, "Key Surveyed Works (2025-2026)", [
        "He et al. (Appl. Energy 2025): Online quantile-regression LSTM using KL divergence for virtual drift and CRPS for real drift. Complex deep pipeline; update compute cost not analyzed.",
        "Cao et al. (Appl. Energy 2025): Online probabilistic forecast combination under load drift. Showed ensembles degrade by 12% under drift.",
        "Cao, He & Zhou (Eng. Appl. AI 2026): Online feature extraction with TCN-BiLSTM; re-selects inputs at drift. Heavy architecture, difficult to reproduce.",
        "Bahi et al. (2026 FreeGNN): Spatio-temporal graph network with memory replay. High GPU compute; subtle drift missed."
    ], accent_color=C_NAVY)

    add_card(slide7, 6.8, 1.6, 5.7, 5.1, "Identified Gaps Addressed by This Project", [
        "Gap 1: Absence of a lightweight, interpretable statistical trigger. Most prior works rely on complex deep nets rather than standard gradient boosted trees.",
        "Gap 2: Neglect of adaptation costs. Prior literature rarely reports detection latency, false alarm rates, or cumulative wall-clock retraining runtime.",
        "Gap 3: Flawed evaluation protocols. Literature frequently uses random train/test splits that leak future temporal patterns, hiding true drift penalties.",
        "Our Position: First study to benchmark accuracy, detection delay, false alarms, and CPU cost concurrently across 10 random seeds with no-drift controls."
    ], accent_color=C_PURPLE)
    add_footer(slide7, 7)

    # ==========================================
    # SLIDE 8: SYSTEM ARCHITECTURE
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Proposed Modular System Architecture")
    add_card(slide8, 0.8, 1.6, 11.733, 5.1, "7 End-to-End Operational Modules (Figure 4.1)", [
        "M1  |  Data Acquisition: Ingests continuous SCADA telemetry (wind speed, wind direction, temperature, power generation).",
        "M2  |  Chronological Preprocessing: Builds 10 features strictly preserving time order (speed, sin/cos direction, temperature, power lags, rolling means).",
        "M3  |  Base Forecast Model: Scikit-learn HistGradientBoostingRegressor (120 boosting trees, learning rate 0.1, max depth 6).",
        "M4  |  Error Monitor & Calibration: Heteroscedastic standardization: z(t) = |y(t) - ŷ(t)| / m(ŷ(t)) using a 6-quantile error map.",
        "M5  |  Dual Drift Detectors: Page-Hinkley sequential change detector on z(t) (threshold λ = 15σ₀ = 12.0) + daily KS/PSI input monitors.",
        "M6  |  Adaptation Controller: Enforces 48-hour refractory cooldown, extracts 672h sliding window, applies recency and drift-aware weights, fits updated model.",
        "M7  |  Evaluation Engine: Prequential (test-then-train) scoring comparing Static, Adaptive, and Weekly models over 13,440 stream hours."
    ], accent_color=C_TEAL)
    add_footer(slide8, 8)

    # ==========================================
    # SLIDE 9: CHRONOLOGICAL STREAMING & SYNTHETIC DATA
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Data Generation & Chronological Streaming Protocol")
    add_card(slide9, 0.8, 1.6, 5.6, 5.1, "Physically Grounded Synthetic Stream", [
        "Total Horizon: 106 weeks = 17,808 hourly observations for a 2,000 kW (2 MW) wind farm unit.",
        "Wind Speed Physics: Seasonal cycle + diurnal cycle + AR(1) turbulence noise (mean 7.6 m/s, std 2.7 m/s, φ = 0.96).",
        "Temperature & Direction: Annual/daily thermal cycle + prevailing South-Westerly wind (225° ± 55°).",
        "Piecewise Turbine Conversion: Follows Betz-law aerodynamics with air-density correction (ρ / 1.225) and sensor noise."
    ], accent_color=C_SKY)

    add_card(slide9, 6.8, 1.6, 5.7, 5.1, "Injected Multi-Component Drift at Week 28", [
        "Drift Onset: Hour 4,704 (Week 28)  |  exactly 2 weeks after initial model deployment.",
        "1. Real Derating Drift: 7.5% drop in aerodynamic efficiency across all wind speeds (blade ageing/mechanical wear).",
        "2. Real Wake Loss Drift: Additional 8.5% power loss restricted to 200°-265° sector (downwind wake turbulence).",
        "3. Virtual Anemometer Drift: 1.04x scaling on recorded wind speed (sensor calibration offset).",
        "Prequential Protocol: Test-then-train  |  forecast issued at hour t, actual power revealed at t+1; zero future leakage."
    ], accent_color=C_AMBER)
    add_footer(slide9, 9)

    # ==========================================
    # SLIDE 10: 10-FEATURE ENGINEERING PIPELINE
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Feature Engineering & Gradient Boosted Forecaster")
    add_card(slide10, 0.8, 1.6, 5.6, 5.1, "10 Engineered Features (Table 5.2)", [
        "1. Wind Speed v(t): Primary driver under cubic conversion law.",
        "2-3. Cyclic Direction [sin(d), cos(d)]: Eliminates 0°/360° discontinuity; captures direction-dependent wake losses.",
        "4. Temperature T(t): Models air density variations impacting swept rotor kinetic energy.",
        "5-7. Power Lags [P(t-1), P(t-2), P(t-24)]: Exploits strong autoregressive persistence and 24h diurnal cycles.",
        "8. Rolling Mean Power (6h): Captures short-term generation momentum.",
        "9-10. Speed Lag v(t-1) & Rolling Speed (3h): Tracks atmospheric wind velocity acceleration."
    ], accent_color=C_TEAL)

    add_card(slide10, 6.8, 1.6, 5.7, 5.1, "HistGradientBoostingRegressor Setup", [
        "Algorithm: Histogram-based gradient boosted decision trees (LightGBM-inspired).",
        "Boosting Trees (max_iter): 120 iterations with squared error loss (targets conditional mean).",
        "Learning Rate (ν): 0.10 shrinkage rate.",
        "Tree Max Depth: 6 levels (captures non-linear feature interactions without overfitting).",
        "Min Samples per Leaf: 20 observations (regularization for small sliding windows).",
        "Blazing Speed: Bins continuous features into 255 discrete integer buckets; retrains in just 0.12 seconds on CPU!"
    ], accent_color=C_NAVY)
    add_footer(slide10, 10)

    # ==========================================
    # SLIDE 11: HETEROSCEDASTIC RESIDUAL STANDARDIZATION
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Heteroscedastic Error Calibration Mechanism")
    add_card(slide11, 0.8, 1.6, 11.733, 5.1, "Why Scale-Free Error Calibration is Mandatory (Section 5.5)", [
        "The Problem with Raw Error Monitoring: Absolute error |y - ŷ| naturally scales with power output. Wind speeds in Region 2 (8-12 m/s) produce raw errors of 65 kW, whereas low winds produce only 12 kW.",
        "The Consequence: A detector monitoring uncalibrated raw residuals fires constant false alarms during windy winter weeks and sleeps during calm summer drifts.",
        "Our 6-Quantile Calibration Map: Rolling-origin validation in initial window partitions forecasts into 6 quantile bins [0-71, 71-196, 196-373, 373-636, 636-1049, 1049-2000 kW].",
        "Scale-Free Error Signal: Standardized residual z(t) = |y(t) - ŷ(t)| / m(ŷ(t)).",
        "Invariant Baseline Properties: Under stationary conditions, z(t) maintains a stable baseline mean μ₀ = 1.00 and standard deviation σ₀ = 0.80 regardless of season or wind intensity!"
    ], accent_color=C_EMERALD)
    add_footer(slide11, 11)

    # ==========================================
    # SLIDE 12: DUAL DRIFT DETECTION (PAGE-HINKLEY & KS/PSI)
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Dual-Channel Concept Drift Detection")
    add_card(slide12, 0.8, 1.6, 5.6, 5.1, "Channel 1: Page-Hinkley Error Detector", [
        "Monitors cumulative deviation: m_t = sum(z_i - μ₀ - δ), with M_t = min(m_i).",
        "Alarm Trigger: Alarm raised when m_t - M_t > λ.",
        "Calibrated Parameters: Tolerance δ = 0.6σ₀ = 0.48, Threshold λ = 15σ₀ = 12.0.",
        "Exact Change Point Estimate: τ̂ = argmin(m_i) pinpoints exact hour when degradation started.",
        "Detection Performance: Caught drift in 10/10 seeds with mean delay 21.5h and ZERO false alarms before onset."
    ], accent_color=C_AMBER)

    add_card(slide12, 6.8, 1.6, 5.7, 5.1, "Channel 2: Daily KS & PSI Advisory Monitor", [
        "Kolmogorov-Smirnov (KS): Compares 168h window against reference distribution.",
        "Population Stability Index (PSI): Binned distribution shift across 10 quantiles (PSI > 0.25).",
        "The Autocorrelation Hazard: Hourly wind speed has serial autocorrelation φ = 0.96. Normal weather fluctuations routinely yield KS p < 1e-19.",
        "Advisory Rule: If KS/PSI triggered retraining alone, it would cause > 150 false alarms per year! Input drift is therefore accepted ONLY when corroborated by degraded accuracy (mean z > μ₀ + 2σ₀)."
    ], accent_color=C_SKY)
    add_footer(slide12, 12)

    # ==========================================
    # SLIDE 13: ADAPTIVE CONTROLLER & SAMPLE WEIGHTING
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Adaptive Learning Controller & Sample Weighting")
    add_card(slide13, 0.8, 1.6, 11.733, 5.1, "3 Core Design Principles Governing Model Updates (Section 5.7)", [
        "1. Sliding 4-Week Window (W = 672 hours): When an authorized alarm fires, the forecaster is retrained on the most recent 672 hours ending at the alarm step, allowing the model to naturally discard outdated operating regimes.",
        "2. Exponential Recency Weighting: Each sample receives weight w_i = 2^(-(k - i) / 336), establishing a half-life of 2 weeks (336 hours) so recent observations receive greater mathematical emphasis.",
        "3. Drift-Aware Change-Point Downweighting: Samples older than the estimated change point (i < τ̂ - 12) are multiplied by penalty factor κ = 0.08 (12.5x downweighting). As a result, the few fresh post-drift observations dominate gradient boosting splits immediately after an alarm!",
        "4. 48-Hour Refractory Cooldown Guard: Locks retraining for 48 hours following an update, preventing alarm thrashing while the new model settles on the online stream."
    ], accent_color=C_PURPLE)
    add_footer(slide13, 13)

    # ==========================================
    # SLIDE 14: BENCHMARK RESULTS (75% MAE GAIN)
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Empirical Evaluation: 10-Seed Benchmark Results")
    add_card(slide14, 0.8, 1.6, 11.733, 5.1, "Forecast Accuracy in Drift Scenario (Table 6.1 in Report)", [
        "Evaluated on 10 random seeds (80 weeks, 13,440 hourly evaluations per stream):",
        "• Static Model: MAE = 134.7 ± 5.6 kW | RMSE = 178.4 ± 5.6 kW | nRMSE = 8.92% | Retrainings = 0",
        "• Weekly Retrained: MAE = 35.3 ± 1.3 kW | RMSE = 62.7 ± 5.4 kW | nRMSE = 3.14% | Retrainings = 80.0",
        "• Adaptive (Proposed): MAE = 33.7 ± 2.1 kW | RMSE = 53.0 ± 3.7 kW | nRMSE = 2.65% | Retrainings = 16.2 ± 6.6",
        "",
        "Key Statistical Milestones:",
        "1. 75.0% Error Reduction over Static Baseline: MAE drops by 101.0 kW; paired t = 63.5, p = 3.0e-13 (Wilcoxon p = 0.0020).",
        "2. Superior Accuracy to Weekly Retraining: 4.4% lower MAE and 15.5% lower RMSE with statistical significance (p = 0.014).",
        "3. Consistent Performance: Error reduction fell between 72.6% and 76.4% across all 10 independent random seeds."
    ], accent_color=C_EMERALD)
    add_footer(slide14, 14)

    # ==========================================
    # SLIDE 15: COMPUTATIONAL OVERHEAD & NO-DRIFT CONTROL
    # ==========================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "Computational Efficiency & No-Drift Controls")
    add_card(slide15, 0.8, 1.6, 5.6, 5.1, "4.9× Computational Cost Reduction", [
        "Retraining Frequency: Adaptive model required only 16.2 retrains vs 80.0 for weekly schedule (4.9x fewer updates).",
        "Cumulative Retraining Time: 1.98 ± 0.82 s vs 9.59 ± 0.53 s (4.9x less CPU compute).",
        "Per-Step Monitoring Cost: Heteroscedastic error division and Page-Hinkley update take only 0.049 ms per hour  |  completely negligible for real-time SCADA deployment.",
        "Hardware Independence: Entire 10-seed experiment completes in ~5 minutes on a standard laptop CPU; zero GPU required."
    ], accent_color=C_TEAL)

    add_card(slide15, 6.8, 1.6, 5.7, 5.1, "No-Drift Control Scenario (Table 6.3)", [
        "Hypothesis H2 Verification: What happens when NO drift occurs?",
        "Adaptive Model: ZERO alarms raised across all 10 seeds; 0 retrainings performed; forecasts match static model identically (MAE 25.5 kW).",
        "Weekly Retraining Failure: Blind weekly updates worsened MAE to 33.2 kW (+30.2% error penalty!).",
        "Root Cause: Short 4-week window lacks rare extreme wind states, inflating estimator variance when conditions are stationary.",
        "Takeaway: Scheduled retraining is actively harmful during stationary regimes."
    ], accent_color=C_ROSE)
    add_footer(slide15, 15)

    # ==========================================
    # SLIDE 16: SENSITIVITY STUDIES & DETECTOR COMPARISON
    # ==========================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_header(slide16, "Detector Comparison & Sensitivity Analysis")
    add_card(slide16, 0.8, 1.6, 5.6, 5.1, "Detector Comparison (Table 6.7)", [
        "Page-Hinkley (Proposed): MAE 33.7 kW, Delay 19.4h, Retrains 15.2, 0.0 False Alarms. (Optimal balance).",
        "CUSUM Detector: MAE 33.8 kW, Delay 12.6h, but 37.4 retrainings and 7.8 false alarms per no-drift run.",
        "ADWIN (Adaptive Window): MAE 36.2 kW, Delay 40.6h, 1.6 false alarms (sensitive to heavy-tailed noise).",
        "KS + PSI Only (No Error Check): 153.0 false alarms per run, Delay 128.6h, MAE 32.4 kW. Completely unusable on its own."
    ], accent_color=C_NAVY)

    add_card(slide16, 6.8, 1.6, 5.7, 5.1, "Sensitivity Sweeps (Sections 6.8-6.10)", [
        "Threshold λ: Usable Pareto frontier is 15σ₀ to 25σ₀. At 6σ₀, false alarms rise to 18.6; at 40σ₀, delay grows to 30.4h.",
        "Cooldown Guard: 48h baseline provides robust compromise against alarm thrashing (15.2 retrains vs 22.0 at 12h).",
        "Retraining Window: 4 to 8 weeks perform identically (32.9-33.7 kW); 2-week window degrades to 38.3 kW.",
        "Drift Magnitude: Benefit scales non-linearly: 15% gain at mag 0.25, 53% at 0.5, 75% at 1.0, 83% at 1.5. Subtle shifts (<= 0.1) are safely ignored."
    ], accent_color=C_AMBER)
    add_footer(slide16, 16)

    # ==========================================
    # SLIDE 17: WEB DASHBOARD OUTPUT 1 (LOGIN & OVERVIEW)
    # ==========================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_header(slide17, "Full-Stack SCADA Platform: Login Portal & Live Overview")
    
    img1 = os.path.join(SCREENSHOTS_DIR, "01_login_access_portal.png")
    if os.path.exists(img1):
        slide17.shapes.add_picture(img1, Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.8))
    
    img2 = os.path.join(SCREENSHOTS_DIR, "02_overview_dashboard_live.png")
    if os.path.exists(img2):
        slide17.shapes.add_picture(img2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(3.8))

    add_card(slide17, 0.8, 5.55, 5.6, 1.35, "", [
        "SCADA Login & Role Access Portal",
        "Panimalar AI/ML academic branding with Examiner & Operator roles and 1-Click Quick Demo Access for viva exams."
    ], accent_color=C_PURPLE)

    add_card(slide17, 6.8, 5.55, 5.7, 1.35, "", [
        "Executive Live Overview Dashboard",
        "Real-time generation hero gauge (kW), 3 colorful KPI cards, capacity factor gauge (0-2000 kW), and drift onset tracking."
    ], accent_color=C_TEAL)
    add_footer(slide17, 17)

    # ==========================================
    # SLIDE 18: WEB DASHBOARD OUTPUT 2 (STUDIO & COMPARISON)
    # ==========================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_header(slide18, "Full-Stack SCADA Platform: Studio & Model Comparison")
    
    img3 = os.path.join(SCREENSHOTS_DIR, "04_forecasting_studio.png")
    if os.path.exists(img3):
        slide18.shapes.add_picture(img3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.8))
    
    img4 = os.path.join(SCREENSHOTS_DIR, "07_model_comparison.png")
    if os.path.exists(img4):
        slide18.shapes.add_picture(img4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(3.8))

    add_card(slide18, 0.8, 5.55, 5.6, 1.35, "", [
        "Forecasting Studio & Model Workbench",
        "1-Click weather presets (🍃 Light, 💨 Moderate, ⚡ Gale), interactive SCADA sliders, and 90% confidence intervals."
    ], accent_color=C_SKY)

    add_card(slide18, 6.8, 5.55, 5.7, 1.35, "", [
        "Baseline Model Comparison & Statistical Verification",
        "3 pastel comparison cards (Static in Rose, Adaptive in Mint, Weekly in Sky), paired t-test (p < 0.05), and compute bars."
    ], accent_color=C_EMERALD)
    add_footer(slide18, 18)

    # ==========================================
    # SLIDE 19: UN SDG ALIGNMENT
    # ==========================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_header(slide19, "Alignment with UN Sustainable Development Goals (SDGs)")
    add_card(slide19, 0.8, 1.6, 5.6, 2.45, "SDG 7: Affordable & Clean Energy", [
        "Target 7.2: Increase global share of renewable energy.",
        "Impact: Accurate 1h-ahead wind forecasting minimizes reserve curtailment, enabling higher penetration of clean wind power into national grids at lower cost."
    ], accent_color=C_EMERALD)

    add_card(slide19, 6.8, 1.6, 5.7, 2.45, "SDG 13: Climate Action", [
        "Target 13.2: Integrate climate measures into national policies.",
        "Impact: Mitigates reliance on fast-ramping fossil/coal peaker plants, directly reducing grid carbon emissions; alerts operators early to mechanical wear."
    ], accent_color=C_TEAL)

    add_card(slide19, 0.8, 4.3, 5.6, 2.45, "SDG 9: Industry, Innovation & Infrastructure", [
        "Target 9.4: Upgrade infrastructure with clean technologies.",
        "Impact: Provides a lightweight, drop-in Python/React SCADA layer that modernizes existing wind farms without requiring expensive GPU infrastructure."
    ], accent_color=C_SKY)

    add_card(slide19, 6.8, 4.3, 5.7, 2.45, "SDG 12: Responsible Consumption & Production", [
        "Target 12.2: Sustainable management & efficient resource use.",
        "Impact: Eliminates wasteful 80-week scheduled compute (4.9x reduction in CPU energy and carbon footprint for AI inference)."
    ], accent_color=C_AMBER)
    add_footer(slide19, 19)

    # ==========================================
    # SLIDE 20: CONCLUSION & FUTURE SCOPE
    # ==========================================
    slide20 = prs.slides.add_slide(blank_layout)
    add_header(slide20, "Conclusion & Future Research Directions")
    add_card(slide20, 0.8, 1.6, 5.6, 5.1, "Project Conclusions", [
        "1. Evidence-Driven Adaptation Validated: Concept drift detection on scale-standardized residuals delivers 75.0% error reduction under abrupt turbine derating and wake loss.",
        "2. Efficiency Superiority: Matches or exceeds weekly retraining accuracy while demanding 4.9x less CPU compute and zero GPU hardware.",
        "3. Zero False Alarms: Page-Hinkley detector with heteroscedastic standardization raised 0 false alarms across 10 independent random seeds.",
        "4. Ready for Deployment: Complete full-stack SCADA dashboard with interactive login access portal and 100% test coverage (29/29 tests)."
    ], accent_color=C_EMERALD)

    add_card(slide20, 6.8, 1.6, 5.7, 5.1, "Future Scope & Extensions", [
        "1. Multi-Season Measured Data: Validate pipeline on real-world multi-year SCADA datasets (e.g. NREL / Kelmarsh wind farms).",
        "2. Gradual & Incremental Drift: Extend change-point estimation to detect subtle blade icing and slow bearing wear.",
        "3. Probabilistic & Quantile Forecasting: Extend point predictions to full quantile densities (CRPS scoring) for risk-aware bidding.",
        "4. Spatial Farm-to-Farm Transfer: Transfer drift-learned representations to newly commissioned adjacent wind farms."
    ], accent_color=C_NAVY)
    add_footer(slide20, 20)

    # Save presentation
    os.makedirs(os.path.dirname(OUTPUT_PPTX_REPORTS), exist_ok=True)
    prs.save(OUTPUT_PPTX_REPORTS)
    print(f"Saved PPTX to: {OUTPUT_PPTX_REPORTS}")

    # Copy to user Downloads
    try:
        import shutil
        shutil.copy2(OUTPUT_PPTX_REPORTS, USER_DOWNLOADS)
        print(f"Copied PPTX to Downloads: {USER_DOWNLOADS}")
    except Exception as e:
        print(f"Error copying to Downloads: {e}")

if __name__ == "__main__":
    create_presentation()
