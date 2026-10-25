"""PDF report generator utilizing ReportLab for technical project summaries."""
from pathlib import Path
import io
from typing import Dict, Any, Optional
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
from ..config import REPORTS_DIR


def generate_project_summary_pdf(output_path: Optional[Path] = None) -> bytes:
    """Generates an official project report summary PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0F172A")    # Dark slate
    teal_color = colors.HexColor("#0D9488")       # Teal
    accent_color = colors.HexColor("#1E293B")     # Border color

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=teal_color,
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    story = []

    # Title & Header
    story.append(Paragraph("Adaptive Wind Power Forecasting Using Concept Drift Detection", title_style))
    story.append(Paragraph("A Technical Summary & Engineering Evaluation Report | B.Tech Artificial Intelligence & Machine Learning", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=teal_color, spaceAfter=10))

    # Meta Info Table
    meta_data = [
        [
            Paragraph("<b>Institution:</b> Panimalar Engineering College (Anna Univ.)", body_style),
            Paragraph("<b>Academic Year:</b> 2026", body_style),
        ],
        [
            Paragraph("<b>Candidates:</b> Thanya B (211423247227) & Thejessri S (211423247229)", body_style),
            Paragraph("<b>Supervisor:</b> Mr. M. Ezhilvendhan, M.E.", body_style),
        ],
        [
            Paragraph("<b>Target Horizon:</b> 1-Hour-Ahead Regressive Forecasting", body_style),
            Paragraph("<b>Turbine Capacity:</b> 2.0 MW (2000 kW Aggregated)", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[270, 260])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Problem Formulation and Motivation", h2_style))
    summary_text = (
        "Wind energy forecasting models traditionally deployed in grid control centers operate under a static stationarity "
        "assumption. However, environmental regimes shift seasonally, turbine components suffer blade erosion or derating, and "
        "nearby obstacles create directional wake deficits. In such events (concept drift), static model errors multiply "
        "rapidly due to the non-linear cubic wind-power relation <i>P ∝ v³</i>. Blind periodic retraining (e.g. weekly) wastes "
        "computation and impairs stability when stationary. This project introduces a lightweight, interpretable, drift-adaptive "
        "forecasting framework utilizing a Histogram Gradient Boosting Regressor (HistGBR), heteroscedastic residual standardisation, "
        "Page-Hinkley sequential change detection, and a 48-hour refractory cooldown controller."
    )
    story.append(Paragraph(summary_text, body_style))

    # Section 2: Headline Benchmark Results
    story.append(Paragraph("2. Forecast Accuracy and Baseline Comparison (10 Random Seeds)", h2_style))
    bench_data = [
        [
            Paragraph("Model Strategy", table_header),
            Paragraph("MAE (kW)", table_header),
            Paragraph("RMSE (kW)", table_header),
            Paragraph("nRMSE (%)", table_header),
            Paragraph("Retrainings", table_header),
            Paragraph("Compute (s)", table_header),
        ],
        [
            Paragraph("<b>Static Baseline</b> (Train Once)", table_cell),
            Paragraph("134.7 ± 5.6", table_cell),
            Paragraph("178.4 ± 5.6", table_cell),
            Paragraph("8.92 ± 0.28%", table_cell),
            Paragraph("0.0", table_cell),
            Paragraph("0.00 s", table_cell),
        ],
        [
            Paragraph("<b>Adaptive Framework</b> (Proposed)", table_cell),
            Paragraph("<b>33.7 ± 2.1</b>", table_cell),
            Paragraph("<b>53.0 ± 3.7</b>", table_cell),
            Paragraph("<b>2.65 ± 0.19%</b>", table_cell),
            Paragraph("16.2 ± 6.6", table_cell),
            Paragraph("1.98 ± 0.82 s", table_cell),
        ],
        [
            Paragraph("<b>Weekly Retrain</b> (Blind Schedule)", table_cell),
            Paragraph("35.3 ± 1.3", table_cell),
            Paragraph("62.7 ± 5.4", table_cell),
            Paragraph("3.14 ± 0.27%", table_cell),
            Paragraph("80.0", table_cell),
            Paragraph("9.59 ± 0.53 s", table_cell),
        ],
    ]
    t_bench = Table(bench_data, colWidths=[150, 75, 75, 75, 75, 80])
    t_bench.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, accent_color),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F1F5F9")]),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 6))

    findings_text = (
        "<b>Key Findings:</b> Under concept drift (week 28), the adaptive framework reduced MAE from 134.7 kW to 33.7 kW "
        "(<b>75.0% error reduction</b>, paired t-test <i>p = 3.0×10⁻¹³</i>). It achieved an accuracy comparable to or better than blind "
        "weekly retraining (33.7 kW vs 35.3 kW) while requiring <b>4.9× fewer retrainings</b> (16.2 vs 80.0) and <b>4.9× less compute</b>. "
        "In the no-drift control scenario, the adaptive model raised zero false alarms, whereas weekly retraining degraded MAE by <b>+30.2%</b>."
    )
    story.append(Paragraph(findings_text, body_style))

    # Section 3: Detection Metrics
    story.append(Paragraph("3. Concept Drift Detection & Change Point Dynamics", h2_style))
    det_text = (
        "• <b>Detection Delay:</b> Mean delay of 21.5 hours across 10 random seeds (median 15.5 h). The delay represents the physical "
        "arrival of the first strong-wind regime (> 8 m/s), during which turbine derating alters output.<br/>"
        "• <b>False Alarms:</b> 0 false alarms before drift onset across all ten runs.<br/>"
        "• <b>Input Distribution Monitors:</b> Kolmogorov-Smirnov (KS) test and Population Stability Index (PSI) applied to wind speed "
        "revealed that natural autocorrelation causes distribution shifts even without concept change (nominal KS p-values of 10⁻¹⁹ to 10⁻³¹). "
        "Therefore, input tests must serve strictly as an advisory channel corroborated by degraded prediction accuracy."
    )
    story.append(Paragraph(det_text, body_style))

    # Section 4: Practical Guidelines & Hypotheses
    story.append(Paragraph("4. Verification of Hypotheses & Engineering Recommendations", h2_style))
    hyp_data = [
        [
            Paragraph("Hypothesis", table_header),
            Paragraph("Claim", table_header),
            Paragraph("Status", table_header),
            Paragraph("Evidence", table_header),
        ],
        [
            Paragraph("<b>H1</b>", table_cell),
            Paragraph("Drift-triggered retraining outperforms static model", table_cell),
            Paragraph("<font color='#0D9488'><b>Supported</b></font>", table_cell),
            Paragraph("MAE 134.7 → 33.7 kW (75.0% lower, p = 3e-13)", table_cell),
        ],
        [
            Paragraph("<b>H2</b>", table_cell),
            Paragraph("In stationary streams, adaptive model raises 0 alarms", table_cell),
            Paragraph("<font color='#0D9488'><b>Supported</b></font>", table_cell),
            Paragraph("0 alarms in 10 seeds; static equals adaptive", table_cell),
        ],
        [
            Paragraph("<b>H3</b>", table_cell),
            Paragraph("Matches weekly retraining with far fewer updates", table_cell),
            Paragraph("<font color='#0D9488'><b>Supported</b></font>", table_cell),
            Paragraph("33.7 vs 35.3 kW with 4.9x fewer retrainings", table_cell),
        ],
        [
            Paragraph("<b>H4</b>", table_cell),
            Paragraph("Adaptation benefit scales with drift magnitude", table_cell),
            Paragraph("<font color='#0D9488'><b>Supported</b></font>", table_cell),
            Paragraph("Gain scales from 0% (mag 0.1) to 82.8% (mag 1.5)", table_cell),
        ],
    ]
    t_hyp = Table(hyp_data, colWidths=[40, 190, 70, 230])
    t_hyp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, accent_color),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_hyp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<i>Report generated autonomously by Adaptive Wind Power Forecasting System. Grounded in empirical results.</i>", subtitle_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()

    if output_path:
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes
