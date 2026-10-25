"""Script to generate the Project Explanation & Viva Guide PDF using ReportLab."""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_PATH = Path(r"C:\Users\SFJ036\.gemini\antigravity\scratch\wind-power-forecasting\reports\Project_Explanation_and_Viva_Guide.pdf")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def build_pdf():
    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    primary = colors.HexColor("#0F172A")    # Dark slate
    teal = colors.HexColor("#0D9488")       # Teal
    accent = colors.HexColor("#334155")     # Border
    text_dark = colors.HexColor("#1E293B")
    subtext = colors.HexColor("#475569")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=teal,
        fontStyle="italic",
        spaceAfter=8,
    )
    h2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=teal,
        spaceBefore=10,
        spaceAfter=4,
    )
    h3_style = ParagraphStyle(
        "DocH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=primary,
        spaceBefore=6,
        spaceAfter=2,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=5,
    )
    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        leftIndent=12,
        spaceAfter=3,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=text_dark,
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Adaptive Wind Power Forecasting Using Concept Drift Detection", title_style))
    story.append(Paragraph("Complete Project Explanation, Methodology Breakdown & Viva Voce Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=teal, spaceAfter=8))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Project:</b> Final-Year AI/ML Engineering Project", body_style),
            Paragraph("<b>Institution:</b> Panimalar Engineering College (Anna University)", body_style),
        ],
        [
            Paragraph("<b>Candidates:</b> Thanya B (211423247227) & Thejessri S (211423247229)", body_style),
            Paragraph("<b>Supervisor:</b> Mr. M. Ezhilvendhan, M.E. | <b>HoD:</b> Dr. G. Suresh", body_style),
        ],
        [
            Paragraph("<b>Target Horizon:</b> 1-Hour-Ahead Generation Forecast", body_style),
            Paragraph("<b>Turbine Rating:</b> 2.0 MW (2,000 kW Aggregated Farm)", body_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # Section 1
    story.append(Paragraph("1. The Big Picture (What is this project?)", h2_style))
    p1 = (
        "Wind power is one of the most vital clean energy sources, but unlike thermal or hydro plants, its output cannot be "
        "dispatched on demand—it depends second-by-second on fluctuating weather. Power grid operators must know "
        "<b>exactly how much electricity the wind farm will produce 1 hour in advance</b> to balance grid supply and demand, schedule "
        "reserves, and avoid expensive fossil-fuel ramp-ups. In this project, we built an intelligent Machine Learning system that "
        "consumes meteorological data (wind speed, direction, temperature) and recent generation history to deliver accurate, "
        "reliable 1-hour-ahead forecasts for a 2 MW turbine unit."
    )
    story.append(Paragraph(p1, body_style))

    # Section 2
    story.append(Paragraph("2. The Core Problem: Concept Drift in Wind Energy", h2_style))
    p2 = (
        "Wind turbine physics follows the non-linear cubic law: <i>Power ∝ (Wind Speed)³</i>. Because of this cubic relationship, "
        "a tiny <b>10% change in wind speed creates a huge ~33% swing in electrical generation</b>.<br/>"
        "Traditional machine learning models assume <i>stationarity</i> (the belief that weather-to-power patterns never change). "
        "In the real world, turbines operate outdoors across years where conditions inevitably shift:"
    )
    story.append(Paragraph(p2, body_style))
    story.append(Paragraph("• <b>Turbine Blade Ageing & Derating (Real Drift):</b> Blade surface erosion, dirt, and mechanical wear degrade aerodynamic efficiency. The same wind produces less power than when the model was trained.", bullet_style))
    story.append(Paragraph("• <b>New Wake Deficits & Obstacles (Real Drift):</b> Newly built turbines or physical obstacles create directional wind turbulence and shadow deficits (e.g. in the South-West sector 200°–265°).", bullet_style))
    story.append(Paragraph("• <b>Sensor Recalibration (Virtual Drift):</b> Anemometers replaced or recalibrated shift recorded speeds (+4%) without altering the actual physical wind.", bullet_style))
    story.append(Paragraph("When these shifts occur (<b>Concept Drift</b>), a standard model trained once (a <b>Static Model</b>) fails silently: its error quadruples from 25 kW to 134.7 kW, yet it has no awareness that it has become outdated.", body_style))

    # Section 3
    story.append(Paragraph("3. The Trap of Blind Calendar Retraining (Why Not Retrain Every Week?)", h2_style))
    p3 = (
        "A common industry workaround is retraining models on a fixed calendar schedule (e.g. every Sunday night). "
        "Our empirical research proves this approach has severe flaws:<br/>"
        "1. <b>Late Reaction to Sudden Shifts:</b> If an obstacle or blade derating occurs on Monday morning, a weekly model remains inaccurate for nearly 6 full days before its next update.<br/>"
        "2. <b>Variance Penalty When Stationary:</b> When conditions are normal (no drift), retraining on a short 4-week window actually makes forecasts <b>30.2% worse</b> (MAE degrades from 25.5 kW to 33.2 kW) because the model forgets rare weather extremes.<br/>"
        "3. <b>Computational Waste:</b> Performing 80 retrainings when nothing has changed wastes substantial compute and operational effort."
    )
    story.append(Paragraph(p3, body_style))

    # Section 4
    story.append(Paragraph("4. The Proposed 4-Step Adaptive Solution", h2_style))
    story.append(Paragraph("<b>Step 1: Prequential 1-Hour-Ahead Forecast:</b> A HistGradientBoostingRegressor (120 trees, max depth 6) predicts generation using 10 strictly causal features (speed, sin/cos direction, temperature, lagged power t-1, t-2, t-24, rolling power mean 6h, lagged speed, rolling speed mean 3h) with zero future target leakage.", bullet_style))
    story.append(Paragraph("<b>Step 2: Heteroscedastic Error Standardisation:</b> Absolute error naturally scales with power level. We divide the raw error by the expected error for that power level using a 6-quantile calibration map, creating a scale-free score <i>z(t) = |y(t) - ŷ(t)| / m(ŷ(t))</i> whose baseline mean sits stably at μ₀ ≈ 1.0.", bullet_style))
    story.append(Paragraph("<b>Step 3: Sequential Drift Alarm (Page-Hinkley Test):</b> The system tracks the cumulative excess deviation <i>m(t) - M(t)</i>. When errors surge, the statistic crosses threshold λ = 15σ₀ = 12.0, sounding an alarm. It detected drift in <b>21.5 hours on average with zero false alarms</b> before onset.", bullet_style))
    story.append(Paragraph("<b>Step 4: Smart Adaptive Retraining Controller:</b> An adaptation controller enforces a <b>48-hour refractory cooldown</b> (preventing thrashing), retrains on the recent 4-week window (672 h), applies recency decay (half-life 336 h), and downweights data prior to the estimated change point (0.08x).", bullet_style))

    # Section 5
    story.append(Paragraph("5. Empirical Benchmark Results (10 Random Seeds)", h2_style))
    t_data = [
        [
            Paragraph("Evaluation Metric", table_header),
            Paragraph("Static Model (Train Once)", table_header),
            Paragraph("Adaptive Framework (Proposed)", table_header),
            Paragraph("Weekly Retrained (Schedule)", table_header),
            Paragraph("Takeaway / Conclusion", table_header),
        ],
        [
            Paragraph("<b>Drift: MAE (kW)</b>", table_cell),
            Paragraph("134.7 ± 5.6", table_cell),
            Paragraph("<b>33.7 ± 2.1</b>", table_cell),
            Paragraph("35.3 ± 1.3", table_cell),
            Paragraph("<b>75.0% error reduction</b> (p = 3e-13)", table_cell),
        ],
        [
            Paragraph("<b>Drift: RMSE (kW)</b>", table_cell),
            Paragraph("178.4 ± 5.6", table_cell),
            Paragraph("<b>53.0 ± 3.7</b>", table_cell),
            Paragraph("62.7 ± 5.4", table_cell),
            Paragraph("<b>70.3% error reduction</b> (p = 2.2e-4)", table_cell),
        ],
        [
            Paragraph("<b>Drift: nRMSE (%)</b>", table_cell),
            Paragraph("8.92 ± 0.28%", table_cell),
            Paragraph("<b>2.65 ± 0.19%</b>", table_cell),
            Paragraph("3.14 ± 0.27%", table_cell),
            Paragraph("Substantial grid reliability improvement", table_cell),
        ],
        [
            Paragraph("<b>Retrainings Count</b>", table_cell),
            Paragraph("0", table_cell),
            Paragraph("<b>16.2 ± 6.6</b>", table_cell),
            Paragraph("80.0", table_cell),
            Paragraph("<b>4.9× fewer retrainings</b>", table_cell),
        ],
        [
            Paragraph("<b>Compute Runtime (s)</b>", table_cell),
            Paragraph("0.00 s", table_cell),
            Paragraph("<b>1.98 ± 0.82 s</b>", table_cell),
            Paragraph("9.59 ± 0.53 s", table_cell),
            Paragraph("<b>4.9× less computation</b>", table_cell),
        ],
        [
            Paragraph("<b>No-Drift MAE (kW)</b>", table_cell),
            Paragraph("25.5 ± 0.6", table_cell),
            Paragraph("<b>25.5 ± 0.6</b>", table_cell),
            Paragraph("33.2 ± 1.5", table_cell),
            Paragraph("Weekly model suffered <b>+30.2% penalty</b>", table_cell),
        ],
        [
            Paragraph("<b>False Alarms</b>", table_cell),
            Paragraph("—", table_cell),
            Paragraph("<b>0 in 10 seeds</b>", table_cell),
            Paragraph("—", table_cell),
            Paragraph("Zero false alarms before drift onset", table_cell),
        ],
    ]
    res_table = Table(t_data, colWidths=[110, 100, 115, 105, 110])
    res_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary),
        ("GRID", (0, 0), (-1, -1), 0.5, accent),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 6))

    # Section 6
    story.append(Paragraph("6. Architecture of the 7 Web Dashboard Pages", h2_style))
    story.append(Paragraph("1. <b>Overview Dashboard:</b> Real-time SCADA telemetry, live KPIs, actual vs predicted power chart with drift onset zoom, 80-week MAE divergence curves, and drift alarm timeline.", bullet_style))
    story.append(Paragraph("2. <b>Forecasting Studio:</b> Interactive workbench to adjust wind speed, direction, and temperature sliders, compute immediate 1h forecasts, tune hyperparameters, and export results.", bullet_style))
    story.append(Paragraph("3. <b>Drift Monitoring:</b> Simulated playback controls (Step 1h, Step 24h, Reset), Page-Hinkley statistic curve vs threshold line λ = 12.0, Kolmogorov-Smirnov test and PSI input monitors.", bullet_style))
    story.append(Paragraph("4. <b>Adaptive Learning:</b> Active model version telemetry, 48h cooldown timer, sample weights curve chart (recency decay + pre-change downweighting), and Manual Retrain trigger.", bullet_style))
    story.append(Paragraph("5. <b>Model Comparison:</b> Head-to-head bar charts (Static vs Adaptive vs Weekly), paired Student's t-test and Wilcoxon statistical tables, and automated analytical evaluation.", bullet_style))
    story.append(Paragraph("6. <b>Dataset Explorer:</b> Paginated data table, 0-missing-value health verification, empirical wind speed vs power scatter plot with power curve overlay, and 16-sector wind rose.", bullet_style))
    story.append(Paragraph("7. <b>Experiments & Reports:</b> Multi-seed test lab (seeds 0–9), sensitivity curves (threshold, cooldown, window, magnitude), and instant downloadable PDF executive report.", bullet_style))

    # Section 7: Elevator Pitch
    story.append(Paragraph("7. Three-Sentence Elevator Pitch for Viva Voce Examination", h2_style))
    pitch = (
        "<i>\"Our project develops an intelligent 1-hour-ahead wind power forecasting system that detects when turbine degradation "
        "or environmental wake effects cause prediction errors to rise. Instead of retraining blindly on a calendar schedule, "
        "our system uses scale-standardized residual monitoring and the Page-Hinkley test to retrain only when statistical evidence "
        "proves the model has become outdated. This achieves a 75% error reduction under concept drift while requiring 4.9 times less "
        "computation than traditional scheduled retraining.\"</i>"
    )
    story.append(Paragraph(pitch, body_style))

    doc.build(story)
    print(f"PDF built successfully at {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")

if __name__ == "__main__":
    build_pdf()
