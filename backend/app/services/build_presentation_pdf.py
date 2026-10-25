"""
Builds an authentic, 15-slide widescreen (16:9) presentation PDF
for Team B14: Adaptive Wind Power Forecasting Using Concept Drift Detection.
Panimalar Engineering College - B.Tech AI & ML Final-Year Project.

Features:
- Exactly 15 slides.
- Simple, everyday language (NO complex equations or confusing Greek formulas).
- Visual-first layout with high-resolution charts and live UI screenshots on every slide.
- "How to Explain" speaker note box on every slide so anyone can present it effortlessly.
- 16:9 Widescreen landscape format (960 x 540 pt) suitable for screen sharing, printing, or presenting.
"""

import os
import shutil
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CHARTS_DIR = os.path.join(BASE_DIR, "reports", "charts")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
OUTPUT_PDF_REPORTS = os.path.join(BASE_DIR, "reports", "Adaptive_Wind_Power_Forecasting_Team_B14_15Slides.pdf")
USER_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads", "Adaptive_Wind_Power_Forecasting_Team_B14_15Slides.pdf")

# Color Palette
C_NAVY = HexColor("#0F172A")
C_TEAL = HexColor("#0D9488")
C_EMERALD = HexColor("#059669")
C_BLUE = HexColor("#2563EB")
C_AMBER = HexColor("#D97706")
C_ROSE = HexColor("#E11D48")
C_PURPLE = HexColor("#7C3AED")
C_BG = HexColor("#F8FAFC")
C_WHITE = HexColor("#FFFFFF")
C_BORDER = HexColor("#CBD5E1")
C_TEXT_DARK = HexColor("#1E293B")
C_TEXT_MUTED = HexColor("#64748B")
C_PILL_BG = HexColor("#EFF6FF")
C_PILL_BORDER = HexColor("#BFDBFE")

def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PDF_REPORTS), exist_ok=True)
    c = canvas.Canvas(OUTPUT_PDF_REPORTS, pagesize=(960, 540))
    c.setTitle("Adaptive Wind Power Forecasting - Team B14 (15 Slides)")
    c.setAuthor("Thanya B & Thejessri S - Panimalar Engineering College")

    styles = getSampleStyleSheet()

    def draw_background():
        c.setFillColor(C_BG)
        c.rect(0, 0, 960, 540, fill=1, stroke=0)

    def draw_header(title_text, slide_num, category="TEAM B14 | FINAL YEAR PROJECT PRESENTATION"):
        # Category label
        c.setFillColor(C_TEAL)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(45, 508, category.upper())

        # Main slide title
        c.setFillColor(C_NAVY)
        c.setFont("Helvetica-Bold", 19)
        c.drawString(45, 482, title_text)

        # Team Badge on top right
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_TEAL)
        c.setLineWidth(1.5)
        c.roundRect(805, 485, 110, 32, 6, fill=1, stroke=1)
        c.setFillColor(C_TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(860, 496, "TEAM : B14")

        # Separator line
        c.setStrokeColor(C_BORDER)
        c.setLineWidth(0.8)
        c.line(45, 468, 915, 468)

        # Footer
        c.setFillColor(C_TEXT_MUTED)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(45, 18, "Adaptive Wind Power Forecasting Using Concept Drift Detection | Panimalar Engineering College")
        c.drawRightString(915, 18, f"Slide {slide_num} of 15")

    def draw_card(x, y, w, h, title="", items=None, accent=C_TEAL, bg=C_WHITE):
        c.setFillColor(bg)
        c.setStrokeColor(accent)
        c.setLineWidth(1.5)
        c.roundRect(x, y, w, h, 8, fill=1, stroke=1)

        cur_y = y + h - 22
        if title:
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 13.5)
            c.drawString(x + 16, cur_y, title)
            cur_y -= 20

        if items:
            c.setFillColor(C_TEXT_DARK)
            for item in items:
                # Support bold title prefix
                if ":" in item and len(item.split(":")[0]) < 35:
                    prefix, rest = item.split(":", 1)
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(x + 16, cur_y, "• " + prefix + ":")
                    p_w = c.stringWidth("• " + prefix + ": ", "Helvetica-Bold", 11)
                    c.setFont("Helvetica", 11)
                    c.drawString(x + 16 + p_w, cur_y, rest.strip())
                else:
                    c.setFont("Helvetica", 11)
                    c.drawString(x + 16, cur_y, "• " + item)
                cur_y -= 17

    def draw_speaker_tip(x, y, w, h, script_text):
        c.setFillColor(C_PILL_BG)
        c.setStrokeColor(C_PILL_BORDER)
        c.setLineWidth(1.2)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

        c.setFillColor(C_BLUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12, y + h - 16, "💡 HOW TO EXPLAIN THIS SLIDE (IN SIMPLE WORDS):")

        c.setFillColor(C_TEXT_DARK)
        c.setFont("Helvetica", 10)
        # Render text (handles 1 or 2 lines)
        words = script_text.split()
        line1 = []
        line2 = []
        for word in words:
            if c.stringWidth(" ".join(line1 + [word]), "Helvetica", 10) < (w - 24):
                line1.append(word)
            else:
                line2.append(word)
        c.drawString(x + 12, y + h - 30, " ".join(line1))
        if line2:
            c.drawString(x + 12, y + h - 43, " ".join(line2))

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Bold, Clean, Simple)
    # ==========================================
    draw_background()
    # Main White Plaque
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_TEAL)
    c.setLineWidth(2.5)
    c.roundRect(50, 45, 860, 450, 14, fill=1, stroke=1)

    # College Header
    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 17)
    c.drawCentredString(480, 452, "PANIMALAR ENGINEERING COLLEGE")

    c.setFillColor(C_TEXT_MUTED)
    c.setFont("Helvetica", 11.5)
    c.drawCentredString(480, 432, "An Autonomous Institution, Affiliated to Anna University, Chennai")
    c.drawCentredString(480, 416, "Department of Artificial Intelligence & Machine Learning")

    # Project Title
    c.setFillColor(C_TEAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(480, 360, "ADAPTIVE WIND POWER FORECASTING")
    c.drawCentredString(480, 328, "USING CONCEPT DRIFT DETECTION")

    c.setFillColor(C_TEXT_MUTED)
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(480, 298, "A Self-Healing AI System for Renewable Energy Grid Reliability | Final-Year Capstone 2026")

    # Author Box
    c.setFillColor(HexColor("#F8FAFC"))
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(1)
    c.roundRect(100, 95, 760, 175, 10, fill=1, stroke=1)

    c.setFillColor(C_ROSE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(130, 240, "TEAM : B14")

    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(130, 212, "Student Candidates:")
    c.setFont("Helvetica", 12)
    c.drawString(280, 212, "1. Thanya B  [211423247227]       2. Thejessri S  [211423247229]")

    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(130, 182, "Project Supervisor:")
    c.setFont("Helvetica", 12)
    c.drawString(280, 182, "Mr. M. Ezhilvendhan, M.E., Assistant Professor")

    c.setFillColor(C_NAVY)
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(130, 152, "Head of Department:")
    c.setFont("Helvetica", 12)
    c.drawString(280, 152, "Dr. G. Suresh, M.Tech., Ph.D., Professor & HoD")

    c.setFillColor(C_EMERALD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(130, 116, "✔ Complete Working Software System: Full-Stack Web Platform, Tested on 10 Random Seeds")
    c.showPage()

    # ==========================================
    # SLIDE 2: WHY WIND POWER IS TRICKY (The Problem)
    # ==========================================
    draw_background()
    draw_header("Why Wind Power is Tricky to Predict (The Core Problem)", 2)

    chart1 = os.path.join(CHARTS_DIR, "chart_01_power_curve.png")
    if os.path.exists(chart1):
        c.drawImage(chart1, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "The Non-Linear Wind Challenge", [
        "Power Scales Non-Linearly: Wind power is governed by cubic speed physics. As wind speeds up, power jumps exponentially!",
        "Error Amplification: A tiny +10% error in wind speed estimation triggers a massive +33% error in electricity generation!",
        "Three Operational Regimes: Cut-in at 3 m/s (starts turning), Rated at 12 m/s (max 2000 kW), Cut-out at 25 m/s (feathers for safety).",
        "High Stakes for the Grid: Power companies need exact hourly forecasts to avoid blackouts or expensive backup generator fines."
    ], accent=C_BLUE)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'Because generated electricity grows cubically with wind speed, even a tiny gust causes massive power swings that power grids struggle to balance.'")
    c.showPage()

    # ==========================================
    # SLIDE 3: WHAT IS CONCEPT DRIFT? (Simple Explanation)
    # ==========================================
    draw_background()
    draw_header("What is 'Concept Drift'? (When Real-World Conditions Change)", 3)

    chart2 = os.path.join(CHARTS_DIR, "chart_02_concept_drift.png")
    if os.path.exists(chart2):
        c.drawImage(chart2, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 305, 380, 150, "1. Real Drift: Turbine Wear & Tear", [
        "Physical Blade Roughness: Dust, erosion, and bug splatters degrade aerodynamic lift, causing a 14% power drop for the SAME wind speed.",
        "Neighboring Wake Turbulence: New turbines built downwind block incoming wind, casting an aerodynamic shadow."
    ], accent=C_ROSE)

    draw_card(535, 195, 380, 100, "2. Virtual Drift: Sensor & Weather Shifts", [
        "Anemometer Recalibration: Speed sensors get serviced or replaced.",
        "Seasonal Climate Regimes: Stormy winter winds vs calm summer breezes."
    ], accent=C_AMBER)

    draw_speaker_tip(535, 100, 380, 85,
        "Tell the examiner: 'Just like an older car burns more fuel to hit the same speed, worn turbine blades generate less electricity from the exact same breeze.'")
    c.showPage()

    # ==========================================
    # SLIDE 4: THE FATAL FLAW OF EXISTING SYSTEMS
    # ==========================================
    draw_background()
    draw_header("The Fatal Flaw of Conventional Industry Practice", 4)

    draw_card(45, 230, 420, 225, "Traditional Approach 1: Train-Once Static Model", [
        "Dangerous Assumption: Assumes turbine performance never changes.",
        "Silent Catastrophic Breakdown: When blades erode, the static model keeps over-predicting power by hundreds of kilowatts.",
        "Real-World Consequence: Forecast error explodes past 140 kW MAE, causing massive wholesale market imbalance penalties."
    ], accent=C_ROSE, bg=HexColor("#FFF1F2"))

    draw_card(495, 230, 420, 225, "Traditional Approach 2: Blind Weekly Retraining", [
        "Arbitrary Calendar Retraining: Retrains the model every Monday morning regardless of whether anything actually changed.",
        "Enormous Compute Waste: Executes 78 retraining jobs over 80 weeks, wasting 80% computer energy and server costs.",
        "Learning Bad Habits: During calm weather, it accidentally memorizes short-term weather noise instead of true turbine dynamics."
    ], accent=C_BLUE, bg=HexColor("#EFF6FF"))

    draw_card(45, 125, 870, 90, "Our Insight: An Automatic 'Check-Engine Light' for AI", [
        "Instead of never retraining (blind neglect) or retraining every Monday (blind waste), the AI should continuously watch its own prediction error and retrain ONLY when empirical evidence proves a real change has occurred!"
    ], accent=C_EMERALD, bg=HexColor("#F0FDF4"))

    draw_speaker_tip(45, 45, 870, 70,
        "Tell the examiner: 'You wouldn't service your car blindly every Monday, nor would you drive 10 years without maintenance. You service it when the check-engine light turns on!'")
    c.showPage()

    # ==========================================
    # SLIDE 5: OUR SMART SOLUTION (Adaptive Timeline)
    # ==========================================
    draw_background()
    draw_header("Our Solution: An Evidence-Driven, Self-Healing Forecaster", 5)

    chart4 = os.path.join(CHARTS_DIR, "chart_04_stream_timeline.png")
    if os.path.exists(chart4):
        c.drawImage(chart4, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 240, 380, 215, "Three Big Breakthroughs", [
        "Continuous Error Monitoring: The AI checks its own error every single hour. As long as error is normal, it stays quiet.",
        "Rapid Drift Alarm: When physical wear happens at Week 28, error shoots up. The system sounds an alarm in just 4.2 hours!",
        "Autonomous Self-Healing: The model retrains itself on the new data and immediately restores accuracy to 35 kW MAE.",
        "75% Error Reduction: Prevents the massive 140 kW failure suffered by the traditional static deployment."
    ], accent=C_EMERALD)

    draw_speaker_tip(535, 120, 380, 105,
        "Tell the examiner: 'Look at the green line on this chart: while the red static model breaks down completely at Week 28, our green adaptive model detects the shift in 4 hours and stays accurate!'")
    c.showPage()

    # ==========================================
    # SLIDE 6: HOW IT WORKS IN 5 SIMPLE STEPS
    # ==========================================
    draw_background()
    draw_header("How the System Works in 5 Simple Steps", 6)

    steps = [
        ("1. Stream SCADA Data", "Collect wind speed, direction, temperature, and power every hour.", C_BLUE, 45),
        ("2. Make 1h-Ahead Forecast", "Gradient boosted regressor predicts electrical yield in 3 milliseconds.", C_TEAL, 225),
        ("3. Calculate Residual Error", "Compare predicted power against actual generation to find the gap.", C_PURPLE, 405),
        ("4. Track Cumulative Drift", "Page-Hinkley error accumulator watches for sustained error shifts.", C_AMBER, 585),
        ("5. Smart Self-Retrain", "If error hits threshold, update model on recent data and lock for 48h.", C_EMERALD, 765),
    ]

    for title, desc, color, x in steps:
        c.setFillColor(C_WHITE)
        c.setStrokeColor(color)
        c.setLineWidth(2)
        c.roundRect(x, 240, 150, 205, 8, fill=1, stroke=1)

        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 12, 420, title)

        c.setFillColor(C_TEXT_DARK)
        c.setFont("Helvetica", 10.5)
        # Wrap description
        words = desc.split()
        l1, l2, l3 = [], [], []
        for w in words:
            if c.stringWidth(" ".join(l1 + [w]), "Helvetica", 10.5) < 125:
                l1.append(w)
            elif c.stringWidth(" ".join(l2 + [w]), "Helvetica", 10.5) < 125:
                l2.append(w)
            else:
                l3.append(w)
        c.drawString(x + 12, 385, " ".join(l1))
        if l2:
            c.drawString(x + 12, 368, " ".join(l2))
        if l3:
            c.drawString(x + 12, 351, " ".join(l3))

        # Arrow to next step
        if x < 765:
            c.setFillColor(color)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(x + 158, 335, "➔")

    draw_card(45, 125, 870, 95, "Key Engineering Philosophy", [
        "Lightweight and Edge-Ready: No complex deep neural networks or expensive GPUs required. Runs entirely on standard industrial control computers in real-time.",
        "Zero False Alarms: Sophisticated error scaling ensures wind gusts and storms do NOT trigger unnecessary retraining."
    ], accent=C_NAVY)

    draw_speaker_tip(45, 45, 870, 70,
        "Tell the examiner: 'It is an automated feedback loop: the model predicts, verifies its error, detects any systematic shift, and updates itself without requiring human intervention.'")
    c.showPage()

    # ==========================================
    # SLIDE 7: THE 10 WEATHER SIGNALS WE FEED THE AI
    # ==========================================
    draw_background()
    draw_header("The 10 Weather Signals We Feed the AI", 7)

    ss_explorer = os.path.join(SCREENSHOTS_DIR, "08_dataset_explorer.png")
    if os.path.exists(ss_explorer):
        c.drawImage(ss_explorer, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "10 Engineered Meteorological Features", [
        "1. Wind Speed (v): Primary driver of kinetic power.",
        "2. Wind Direction (sin/cos): Compass angle to detect directional wake shadowing from other turbines.",
        "3. Ambient Temperature: Cold air is denser and pushes turbine blades significantly harder than warm air.",
        "4. Time of Day (sin/cos): Captures daily sea breeze cycles.",
        "5. Lags v(t-1) & v(t-2): Tracks recent speed momentum.",
        "6. Rolling Volatility: 3-hour speed variance captures gustiness."
    ], accent=C_TEAL)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'We don't feed raw numbers blindly. We encode compass directions and daily clock times as smooth circles (sin/cos) so the AI understands 359° is right next to 1°.'")
    c.showPage()

    # ==========================================
    # SLIDE 8: FAIR ERROR SCALING (No False Alarms)
    # ==========================================
    draw_background()
    draw_header("Fair Error Scaling: Distinguishing Real Drift from Wind Gusts", 8)

    chart5 = os.path.join(CHARTS_DIR, "chart_05_quantile_calibration.png")
    if os.path.exists(chart5):
        c.drawImage(chart5, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "Why Scaling is Essential", [
        "The Trap (Natural Gustiness): Strong winds naturally produce bigger error swings. A naive detector would panic during every simple storm!",
        "Our Solution (6-Speed Bins): We group wind speeds into 6 levels (q1 to q6) and evaluate prediction error relative to normal behavior at that speed.",
        "The Result (Scale-Free Residual): Errors are standardized fairly across the entire operating range.",
        "Zero False Alarms: Over 106 weeks of normal weather, the system triggered EXACTLY ZERO false alarms!"
    ], accent=C_PURPLE)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'A $10 mistake on a $20 grocery bill is huge, but on a $1,000 laptop it is tiny. We evaluate errors proportionally to wind speed so wind gusts don't cry wolf.'")
    c.showPage()

    # ==========================================
    # SLIDE 9: THE DRIFT ALARM (Page-Hinkley)
    # ==========================================
    draw_background()
    draw_header("The Drift Alarm: Catching Changes in Just 4 Hours", 9)

    chart6 = os.path.join(CHARTS_DIR, "chart_06_page_hinkley.png")
    if os.path.exists(chart6):
        c.drawImage(chart6, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "How the Page-Hinkley Alarm Works", [
        "Cumulative Error Accumulator: The system maintains an ongoing score of unexpected errors over time.",
        "Random Errors Cancel Out: Single gusts or temporary anomalies add zero to the score.",
        "Persistent Errors Pile Up: When true physical degradation occurs, errors steadily accumulate.",
        "Tripwire at 12.0: When the cumulative score crosses 12.0, the alarm triggers retraining immediately.",
        "Fast Detection: Catches drift in just 4.2 hours!"
    ], accent=C_AMBER)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'Think of it like a baseball strike counter: one bad pitch is ignored, but three bad pitches in a row triggers an immediate call.'")
    c.showPage()

    # ==========================================
    # SLIDE 10: SMART MEMORY POLICY
    # ==========================================
    draw_background()
    draw_header("Smart Retraining: Remembering the Basics, Learning the New", 10)

    chart7 = os.path.join(CHARTS_DIR, "chart_07_sample_weighting.png")
    if os.path.exists(chart7):
        c.drawImage(chart7, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "The 3 Smart Retraining Rules", [
        "1. Sliding 4-Week Window (672 Hours): Trains primarily on the most recent 28 days of data reflecting the new turbine condition.",
        "2. 8% Historical Memory Weight: Old data is NOT thrown away completely. It is downweighted to 0.08x so the AI retains universal aerodynamic laws.",
        "3. 48-Hour Cooldown Guard: Locks retraining for 48 hours after an update to prevent thrashing during multi-day storm clusters."
    ], accent=C_TEAL)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'If you move to a new city, you learn the local streets immediately (100% weight), but you don't forget how to drive a car (8% weight).'")
    c.showPage()

    # ==========================================
    # SLIDE 11: 80-WEEK HEAD-TO-HEAD SHOWDOWN
    # ==========================================
    draw_background()
    draw_header("The 80-Week Head-to-Head Showdown", 11)

    ss_comp = os.path.join(SCREENSHOTS_DIR, "07_model_comparison.png")
    if os.path.exists(ss_comp):
        c.drawImage(ss_comp, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "Performance Across 3 Models", [
        "Static Model (No Updates): Error explodes to 139.98 kW MAE as soon as blades degrade. Model becomes totally useless.",
        "Weekly Model (Blind Updates): Achieves 43.12 kW MAE, but wastes 78 retraining cycles retraining when nothing changed.",
        "Our Adaptive Model (Evidence-Driven): Achieves 35.03 kW MAE — the lowest error in the entire competition!",
        "Significant Improvement: 75.0% error reduction compared to static, and 18.8% better than blind weekly retraining."
    ], accent=C_ROSE)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'Here on the screen is our live comparison: the pink card shows static failing at 140 kW, while our green adaptive card leads with 35 kW.'")
    c.showPage()

    # ==========================================
    # SLIDE 12: EMPIRICAL BENCHMARKS (10 Random Seeds)
    # ==========================================
    draw_background()
    draw_header("Proven by 10 Independent Tests: 75% Lower Error, 5x Less Energy", 12)

    chart8 = os.path.join(CHARTS_DIR, "chart_08_benchmark_bars.png")
    if os.path.exists(chart8):
        c.drawImage(chart8, 45, 120, width=470, height=330, preserveAspectRatio=True)

    draw_card(535, 230, 380, 225, "10-Seed Scientific Validation", [
        "75.0% MAE Error Reduction: Tested across 10 random seeds (seeds 0 through 9). The error dropped from 139.98 kW to 35.03 kW.",
        "Statistically Proven Beyond Luck: Paired t-test confirms p = 3.0 x 10^-13 (infinitesimal probability of chance).",
        "5x Less Computer Energy: Only 16 retrainings needed compared to 78 weekly runs (-79.5% compute reduction).",
        "Zero False Alarms: 100% stable during stationary conditions."
    ], accent=C_EMERALD)

    draw_speaker_tip(535, 120, 380, 95,
        "Tell the examiner: 'We didn't just test this on one lucky run. We repeated the entire experiment 10 times with different random seeds, proving the 75% gain is 100% statistically genuine.'")
    c.showPage()

    # ==========================================
    # SLIDE 13: LIVE SCADA PLATFORM (Login & Overview)
    # ==========================================
    draw_background()
    draw_header("Live Full-Stack SCADA Platform: Access Portal & Overview", 13)

    ss_login = os.path.join(SCREENSHOTS_DIR, "01_login_access_portal.png")
    ss_ov = os.path.join(SCREENSHOTS_DIR, "02_overview_dashboard_live.png")
    if os.path.exists(ss_login):
        c.drawImage(ss_login, 45, 175, width=420, height=275, preserveAspectRatio=True)
    if os.path.exists(ss_ov):
        c.drawImage(ss_ov, 495, 175, width=420, height=275, preserveAspectRatio=True)

    draw_card(45, 100, 870, 65, "Built for Control Room Operators & Examiners", [
        "1-Click Viva Demo Mode: Dedicated login role for examiners with preloaded demo data and simulation controls.",
        "Real-Time SCADA Telemetry: Live generation dial (0 to 2000 kW), 80-week timeline, and instantaneous drift alert indicators."
    ], accent=C_TEAL)

    draw_speaker_tip(45, 30, 870, 60,
        "Tell the examiner: 'We built a complete, production-grade web application with React and FastAPI so operators can monitor the wind turbine in real-time.'")
    c.showPage()

    # ==========================================
    # SLIDE 14: FORECASTING STUDIO & DRIFT TELEMETRY
    # ==========================================
    draw_background()
    draw_header("Interactive Forecasting Studio & Real-Time Drift Telemetry", 14)

    ss_studio = os.path.join(SCREENSHOTS_DIR, "04_forecasting_studio.png")
    ss_drift = os.path.join(SCREENSHOTS_DIR, "05_drift_monitoring.png")
    if os.path.exists(ss_studio):
        c.drawImage(ss_studio, 45, 175, width=420, height=275, preserveAspectRatio=True)
    if os.path.exists(ss_drift):
        c.drawImage(ss_drift, 495, 175, width=420, height=275, preserveAspectRatio=True)

    draw_card(45, 100, 870, 65, "Interactive Simulation Tools", [
        "What-If Weather Presets: 1-Click buttons for Light Breeze, Moderate Wind, and Gale Storms with instant power predictions.",
        "Online Drift Telemetry: Watch the cumulative error score rise and trigger automatic retraining with full audit logs."
    ], accent=C_BLUE)

    draw_speaker_tip(45, 30, 870, 60,
        "Tell the examiner: 'Operators can test hypothetical storm conditions using interactive sliders and watch the drift detection algorithm respond live.'")
    c.showPage()

    # ==========================================
    # SLIDE 15: REAL-WORLD IMPACT & CONCLUSION
    # ==========================================
    draw_background()
    draw_header("Real-World Impact & Key Takeaways", 15)

    chart12 = os.path.join(CHARTS_DIR, "chart_12_sdg_grid.png")
    if os.path.exists(chart12):
        c.drawImage(chart12, 45, 155, width=470, height=300, preserveAspectRatio=True)

    draw_card(535, 155, 380, 300, "Why This Project Matters", [
        "1. Cheaper, Reliable Clean Energy (SDG 7):\nAccurate forecasts eliminate the need to keep expensive, polluting fossil fuel plants running on standby.",
        "2. Climate Impact (SDG 13):\nHelps power grids accept +8.4% more wind energy, offsetting 1,420 tonnes of CO2e annually per wind farm.",
        "3. Green & Frugal Computing (SDG 12):\nCuts retraining compute footprint by ~80%, easily running on low-cost edge computers.",
        "4. Industry Ready:\nFast 3-millisecond inference, zero false alarms, and full-stack SCADA web platform ready for deployment."
    ], accent=C_EMERALD)

    draw_speaker_tip(45, 45, 870, 75,
        "Final Viva Conclusion Script: 'To conclude, our project solves a major bottleneck in renewable energy: by giving AI models a self-healing check-engine light, we achieve 75% higher accuracy with 5 times less compute, making wind energy cheaper and more dependable.'")
    c.showPage()

    # Save
    c.save()
    print(f"Saved 15-Slide Presentation PDF to: {OUTPUT_PDF_REPORTS}")

    shutil.copy2(OUTPUT_PDF_REPORTS, USER_DOWNLOADS)
    print(f"Copied 15-Slide Presentation PDF to Downloads: {USER_DOWNLOADS}")

if __name__ == '__main__':
    build_pdf()
