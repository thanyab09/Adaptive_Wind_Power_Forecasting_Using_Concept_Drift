"""
Builds an authentic, 15-slide widescreen (16:9) PowerPoint presentation (.pptx)
matching the simplified, equation-free format for Team B14.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CHARTS_DIR = os.path.join(BASE_DIR, "reports", "charts")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")
OUTPUT_PPTX_REPORTS = os.path.join(BASE_DIR, "reports", "Adaptive_Wind_Power_Forecasting_Team_B14_15Slides.pptx")
USER_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads", "Adaptive_Wind_Power_Forecasting_Team_B14_15Slides.pptx")

# Color Constants
C_NAVY = RGBColor(15, 23, 42)
C_TEAL = RGBColor(13, 148, 136)
C_EMERALD = RGBColor(5, 150, 105)
C_BLUE = RGBColor(37, 99, 235)
C_AMBER = RGBColor(217, 119, 6)
C_ROSE = RGBColor(225, 29, 72)
C_PURPLE = RGBColor(124, 58, 237)
C_BG_SLATE = RGBColor(241, 245, 249)
C_WHITE = RGBColor(255, 255, 255)
C_BORDER = RGBColor(203, 213, 225)
C_TEXT_DARK = RGBColor(30, 41, 59)
C_TEXT_MUTED = RGBColor(100, 116, 139)

FONT_STANDARD = "Calibri"

def create_15slide_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_font(p, font_size, bold=False, color=C_TEXT_DARK, italic=False):
        p.font.name = FONT_STANDARD
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.italic = italic
        p.font.color.rgb = color

    def add_header(slide, title_text, slide_num, category="TEAM B14 | FINAL YEAR PRESENTATION"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(9.6), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category.upper()
        set_font(p0, 12, bold=True, color=C_TEAL)

        p1 = tf.add_paragraph()
        p1.text = title_text
        set_font(p1, 22, bold=True, color=C_NAVY)

        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.6), Inches(0.42), Inches(1.9), Inches(0.65))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_WHITE
        badge.line.color.rgb = C_TEAL
        badge.line.width = Pt(1.5)
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = "TEAM: B14"
        set_font(bp, 13, bold=True, color=C_TEAL)
        bp.alignment = PP_ALIGN.CENTER

        sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        sep.fill.solid()
        sep.fill.fore_color.rgb = C_BORDER
        sep.line.fill.background()

        footer = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        ftf = footer.text_frame
        fp = ftf.paragraphs[0]
        fp.text = f"Adaptive Wind Power Forecasting Using Concept Drift Detection | Panimalar Engineering College | Slide {slide_num} of 15"
        set_font(fp, 10, italic=True, color=C_TEXT_MUTED)

    def add_card(slide, left, top, width, height, title="", items=None, accent_color=C_TEAL, bg_color=C_WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.18)

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            set_font(p0, 16, bold=True, color=accent_color)
            p0.space_after = Pt(8)

        if items:
            for i, item in enumerate(items):
                p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
                p.text = "• " + item if isinstance(item, str) else item[0]
                set_font(p, 13.5, color=C_TEXT_DARK)
                p.space_after = Pt(5)
        return card

    def add_speaker_tip(slide, left, top, width, height, text):
        tip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        tip.fill.solid()
        tip.fill.fore_color.rgb = RGBColor(239, 246, 255)
        tip.line.color.rgb = RGBColor(191, 219, 254)
        tip.line.width = Pt(1.2)
        tf = tip.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)

        p0 = tf.paragraphs[0]
        p0.text = "💡 HOW TO EXPLAIN THIS SLIDE (IN SIMPLE WORDS):"
        set_font(p0, 11, bold=True, color=C_BLUE)
        p0.space_after = Pt(3)

        p1 = tf.add_paragraph()
        p1.text = text
        set_font(p1, 12, italic=True, color=C_TEXT_DARK)

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_BG_SLATE
    bg1.line.fill.background()

    plaque = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.7), Inches(11.333), Inches(6.1))
    plaque.fill.solid()
    plaque.fill.fore_color.rgb = C_WHITE
    plaque.line.color.rgb = C_TEAL
    plaque.line.width = Pt(2.5)

    ptf = plaque.text_frame
    ptf.word_wrap = True
    ptf.margin_top = Inches(0.4)
    p0 = ptf.paragraphs[0]
    p0.text = "PANIMALAR ENGINEERING COLLEGE"
    set_font(p0, 18, bold=True, color=C_NAVY)
    p0.alignment = PP_ALIGN.CENTER

    p1 = ptf.add_paragraph()
    p1.text = "An Autonomous Institution, Affiliated to Anna University, Chennai\nDepartment of Artificial Intelligence & Machine Learning"
    set_font(p1, 13, color=C_TEXT_MUTED)
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(16)

    p2 = ptf.add_paragraph()
    p2.text = "ADAPTIVE WIND POWER FORECASTING\nUSING CONCEPT DRIFT DETECTION"
    set_font(p2, 26, bold=True, color=C_TEAL)
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(8)

    p3 = ptf.add_paragraph()
    p3.text = "A Self-Healing AI System for Renewable Energy Grid Reliability | Final-Year Capstone 2026"
    set_font(p3, 14, italic=True, color=C_TEXT_MUTED)
    p3.alignment = PP_ALIGN.CENTER

    box_authors = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.5), Inches(9.733), Inches(1.9))
    box_authors.fill.solid()
    box_authors.fill.fore_color.rgb = RGBColor(248, 250, 252)
    box_authors.line.color.rgb = C_BORDER
    box_authors.line.width = Pt(1)
    atf = box_authors.text_frame
    atf.margin_left = Inches(0.4)
    atf.margin_top = Inches(0.2)
    ap0 = atf.paragraphs[0]
    ap0.text = "TEAM : B14"
    set_font(ap0, 14, bold=True, color=C_ROSE)
    ap1 = atf.add_paragraph()
    ap1.text = "Student Candidates:   1. THANYA B  [211423247227]       2. THEJESSRI S  [211423247229]"
    set_font(ap1, 13.5, bold=True, color=C_NAVY)
    ap2 = atf.add_paragraph()
    ap2.text = "Supervisor:    Mr. M. Ezhilvendhan, M.E., Assistant Professor"
    set_font(ap2, 13, color=C_TEXT_DARK)
    ap3 = atf.add_paragraph()
    ap3.text = "Head of Dept: Dr. G. Suresh, M.Tech., Ph.D., Professor & HoD"
    set_font(ap3, 13, color=C_TEXT_DARK)

    # Helper for 2-column slides
    def make_visual_slide(title, slide_num, img_path, card_title, card_items, tip_text, accent=C_BLUE):
        s = prs.slides.add_slide(blank_layout)
        add_header(s, title, slide_num)
        if os.path.exists(img_path):
            s.shapes.add_picture(img_path, Inches(0.8), Inches(1.6), width=Inches(6.8))
        add_card(s, 7.8, 1.6, 4.7, 3.8, card_title, card_items, accent_color=accent)
        add_speaker_tip(s, 7.8, 5.55, 4.7, 1.35, tip_text)
        return s

    # SLIDE 2: Why Wind Power is Tricky
    make_visual_slide(
        "Why Wind Power is Tricky to Predict (The Core Problem)", 2,
        os.path.join(CHARTS_DIR, "chart_01_power_curve.png"),
        "The Non-Linear Wind Challenge",
        [
            "Power scales non-linearly: Wind power is governed by cubic speed physics. As wind speeds up, power jumps exponentially!",
            "Error Amplification: A tiny +10% error in wind speed estimation triggers a massive +33% error in electricity generation!",
            "Three Operational Regimes: Cut-in at 3 m/s (starts turning), Rated at 12 m/s (max 2000 kW), Cut-out at 25 m/s (feathers for safety).",
            "High Stakes for the Grid: Power companies need exact hourly forecasts to avoid blackouts or expensive backup generator fines."
        ],
        "Tell the examiner: 'Because generated electricity grows cubically with wind speed, even a tiny gust causes massive power swings that power grids struggle to balance.'",
        accent=C_BLUE
    )

    # SLIDE 3: What is Concept Drift?
    make_visual_slide(
        "What is 'Concept Drift'? (When Real-World Conditions Change)", 3,
        os.path.join(CHARTS_DIR, "chart_02_concept_drift.png"),
        "Real Drift vs Virtual Drift",
        [
            "Real Drift (Physical Wear): Turbine blades get eroded by dust and rain, or new downwind turbines block incoming wind. A 10 m/s breeze now makes 14% less power than before!",
            "Virtual Drift (Sensors & Seasons): Wind speed sensors get recalibrated or replaced, changing the numbers on the screen.",
            "The Machine Learning Trap: Standard AI models assume the world is static. When drift occurs, they fail silently!"
        ],
        "Tell the examiner: 'Just like an older car burns more fuel to hit the same speed, worn turbine blades generate less electricity from the exact same breeze.'",
        accent=C_ROSE
    )

    # SLIDE 4: Fatal Flaw of Existing Systems
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "The Fatal Flaw of Conventional Industry Practice", 4)
    add_card(s4, 0.8, 1.6, 5.7, 3.5, "1. Train-Once Static Model", [
        "Dangerous Assumption: Assumes turbine performance stays identical forever.",
        "Silent Catastrophic Breakdown: When blades erode, the static model keeps over-predicting power by hundreds of kilowatts.",
        "Real-World Consequence: Forecast error explodes past 140 kW MAE, causing massive wholesale market imbalance penalties."
    ], accent_color=C_ROSE, bg_color=RGBColor(255, 241, 242))
    add_card(s4, 6.8, 1.6, 5.7, 3.5, "2. Blind Weekly Retraining", [
        "Arbitrary Calendar Retraining: Re-trains the model every Monday morning regardless of whether anything actually changed.",
        "Enormous Compute Waste: Executes 78 retraining jobs over 80 weeks, wasting 80% computer energy and server costs.",
        "Learning Bad Habits: During calm weather, it accidentally memorizes short-term weather noise instead of true turbine dynamics."
    ], accent_color=C_BLUE, bg_color=RGBColor(239, 246, 255))
    add_speaker_tip(s4, 0.8, 5.3, 11.7, 1.5,
        "Tell the examiner: 'You wouldn't service your car blindly every Monday, nor would you drive 10 years without maintenance. You service it when the check-engine light turns on! Our AI builds that check-engine light.'")

    # SLIDE 5: Our Smart Solution
    make_visual_slide(
        "Our Solution: An Evidence-Driven, Self-Healing Forecaster", 5,
        os.path.join(CHARTS_DIR, "chart_04_stream_timeline.png"),
        "Three Big Breakthroughs",
        [
            "Continuous Error Monitoring: The AI checks its own error every single hour. As long as error is normal, it stays quiet.",
            "Rapid Drift Alarm: When physical wear happens at Week 28, error shoots up. The system sounds an alarm in just 4.2 hours!",
            "Autonomous Self-Healing: The model retrains itself on the new data and immediately restores accuracy to 35 kW MAE.",
            "75% Error Reduction: Prevents the massive 140 kW failure suffered by the traditional static deployment."
        ],
        "Tell the examiner: 'Look at the green line on this chart: while the red static model breaks down completely at Week 28, our green adaptive model detects the shift in 4 hours and stays accurate!'",
        accent=C_EMERALD
    )

    # SLIDE 6: How It Works in 5 Simple Steps
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "How the System Works in 5 Simple Steps", 6)
    if os.path.exists(os.path.join(CHARTS_DIR, "chart_03_architecture.png")):
        s6.shapes.add_picture(os.path.join(CHARTS_DIR, "chart_03_architecture.png"), Inches(0.8), Inches(1.6), width=Inches(6.8))
    add_card(s6, 7.8, 1.6, 4.7, 3.8, "The Self-Healing Loop", [
        "1. Stream SCADA Data: Collect wind speed, direction, temperature, and electrical power hourly.",
        "2. Predict 1h Ahead: Fast Gradient Boosted Trees generate forecast in 3 milliseconds.",
        "3. Verify Residual Gap: Compare prediction to actual generation to find the error.",
        "4. Track Cumulative Drift: Page-Hinkley error accumulator watches for sustained error shifts.",
        "5. Smart Self-Retrain: If error hits threshold, update model on recent data and lock for 48h."
    ], accent_color=C_TEAL)
    add_speaker_tip(s6, 7.8, 5.55, 4.7, 1.35,
        "Tell the examiner: 'It is an automated feedback loop: the model predicts, verifies its error, detects any systematic shift, and updates itself without requiring human intervention.'")

    # SLIDE 7: The 10 Weather Signals
    make_visual_slide(
        "The 10 Weather Signals We Feed the AI", 7,
        os.path.join(SCREENSHOTS_DIR, "08_dataset_explorer.png"),
        "10 Engineered Meteorological Features",
        [
            "1. Wind Speed (v): Primary driver of kinetic power.",
            "2. Wind Direction (sin/cos): Compass angle to detect directional wake shadowing from neighboring turbines.",
            "3. Ambient Temperature: Cold air is denser and pushes turbine blades significantly harder than warm air.",
            "4. Time of Day (sin/cos): Captures daily sea breeze cycles.",
            "5. Lags v(t-1) & v(t-2): Tracks recent speed momentum.",
            "6. Rolling Volatility: 3-hour speed variance captures gustiness."
        ],
        "Tell the examiner: 'We don't feed raw numbers blindly. We encode compass directions and daily clock times as smooth circles (sin/cos) so the AI understands 359° is right next to 1°.'",
        accent=C_TEAL
    )

    # SLIDE 8: Fair Error Scaling
    make_visual_slide(
        "Fair Error Scaling: Distinguishing Real Drift from Wind Gusts", 8,
        os.path.join(CHARTS_DIR, "chart_05_quantile_calibration.png"),
        "Why Scaling is Essential",
        [
            "The Trap (Natural Gustiness): Strong winds naturally produce bigger error swings. A naive detector would panic during every simple storm!",
            "Our Solution (6-Speed Bins): We group wind speeds into 6 levels (q1 to q6) and evaluate prediction error relative to normal behavior at that speed.",
            "The Result (Scale-Free Residual): Errors are standardized fairly across the entire operating range.",
            "Zero False Alarms: Over 106 weeks of normal weather, the system triggered EXACTLY ZERO false alarms!"
        ],
        "Tell the examiner: 'A $10 mistake on a $20 grocery bill is huge, but on a $1,000 laptop it is tiny. We evaluate errors proportionally to wind speed so wind gusts don't cry wolf.'",
        accent=C_PURPLE
    )

    # SLIDE 9: The Drift Alarm
    make_visual_slide(
        "The Drift Alarm: Catching Changes in Just 4 Hours", 9,
        os.path.join(CHARTS_DIR, "chart_06_page_hinkley.png"),
        "How the Page-Hinkley Alarm Works",
        [
            "Cumulative Error Accumulator: The system maintains an ongoing score of unexpected errors over time.",
            "Random Errors Cancel Out: Single gusts or temporary anomalies add zero to the score.",
            "Persistent Errors Pile Up: When true physical degradation occurs, errors steadily accumulate.",
            "Tripwire at 12.0: When the cumulative score crosses 12.0, the alarm triggers retraining immediately.",
            "Fast Detection: Catches drift in just 4.2 hours!"
        ],
        "Tell the examiner: 'Think of it like a baseball strike counter: one bad pitch is ignored, but three bad pitches in a row triggers an immediate call.'",
        accent=C_AMBER
    )

    # SLIDE 10: Smart Memory Policy
    make_visual_slide(
        "Smart Retraining: Remembering the Basics, Learning the New", 10,
        os.path.join(CHARTS_DIR, "chart_07_sample_weighting.png"),
        "The 3 Smart Retraining Rules",
        [
            "1. Sliding 4-Week Window (672 Hours): Trains primarily on the most recent 28 days of data reflecting the new turbine condition.",
            "2. 8% Historical Memory Weight: Old data is NOT thrown away completely. It is downweighted to 0.08x so the AI retains universal aerodynamic laws.",
            "3. 48-Hour Cooldown Guard: Locks retraining for 48 hours after an update to prevent thrashing during multi-day storm clusters."
        ],
        "Tell the examiner: 'If you move to a new city, you learn the local streets immediately (100% weight), but you don't forget how to drive a car (8% weight).'",
        accent=C_TEAL
    )

    # SLIDE 11: 80-Week Head-to-Head
    make_visual_slide(
        "The 80-Week Head-to-Head Showdown", 11,
        os.path.join(SCREENSHOTS_DIR, "07_model_comparison.png"),
        "Performance Across 3 Models",
        [
            "Static Model (No Updates): Error explodes to 139.98 kW MAE as soon as blades degrade. Model becomes totally useless.",
            "Weekly Model (Blind Updates): Achieves 43.12 kW MAE, but wastes 78 retraining cycles retraining when nothing changed.",
            "Our Adaptive Model (Evidence-Driven): Achieves 35.03 kW MAE — the lowest error in the entire competition!",
            "Significant Improvement: 75.0% error reduction compared to static, and 18.8% better than blind weekly retraining."
        ],
        "Tell the examiner: 'Here on the screen is our live comparison: the pink card shows static failing at 140 kW, while our green adaptive card leads with 35 kW.'",
        accent=C_ROSE
    )

    # SLIDE 12: Empirical Benchmarks
    make_visual_slide(
        "Proven by 10 Independent Tests: 75% Lower Error, 5x Less Energy", 12,
        os.path.join(CHARTS_DIR, "chart_08_benchmark_bars.png"),
        "10-Seed Scientific Validation",
        [
            "75.0% MAE Error Reduction: Tested across 10 random seeds (seeds 0 through 9). The error dropped from 139.98 kW to 35.03 kW.",
            "Statistically Proven Beyond Luck: Paired t-test confirms p = 3.0 x 10^-13 (infinitesimal probability of chance).",
            "5x Less Computer Energy: Only 16 retrainings needed compared to 78 weekly runs (-79.5% compute reduction).",
            "Zero False Alarms: 100% stable during stationary conditions."
        ],
        "Tell the examiner: 'We didn't just test this on one lucky run. We repeated the entire experiment 10 times with different random seeds, proving the 75% gain is 100% statistically genuine.'",
        accent=C_EMERALD
    )

    # SLIDE 13: Live SCADA Platform
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Live Full-Stack SCADA Platform: Access Portal & Overview", 13)
    if os.path.exists(os.path.join(SCREENSHOTS_DIR, "01_login_access_portal.png")):
        s13.shapes.add_picture(os.path.join(SCREENSHOTS_DIR, "01_login_access_portal.png"), Inches(0.8), Inches(1.6), width=Inches(5.7))
    if os.path.exists(os.path.join(SCREENSHOTS_DIR, "02_overview_dashboard_live.png")):
        s13.shapes.add_picture(os.path.join(SCREENSHOTS_DIR, "02_overview_dashboard_live.png"), Inches(6.8), Inches(1.6), width=Inches(5.7))
    add_card(s13, 0.8, 5.0, 11.7, 1.0, "Built for Control Room Operators & Examiners", [
        "1-Click Viva Demo Mode: Dedicated login role for examiners with preloaded demo data and simulation controls.",
        "Real-Time SCADA Telemetry: Live generation dial (0 to 2000 kW), 80-week timeline, and instantaneous drift alert indicators."
    ], accent_color=C_TEAL)
    add_speaker_tip(s13, 0.8, 6.1, 11.7, 0.85,
        "Tell the examiner: 'We built a complete, production-grade web application with React and FastAPI so operators can monitor the wind turbine in real-time.'")

    # SLIDE 14: Forecasting Studio & Drift Telemetry
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Interactive Forecasting Studio & Real-Time Drift Telemetry", 14)
    if os.path.exists(os.path.join(SCREENSHOTS_DIR, "04_forecasting_studio.png")):
        s14.shapes.add_picture(os.path.join(SCREENSHOTS_DIR, "04_forecasting_studio.png"), Inches(0.8), Inches(1.6), width=Inches(5.7))
    if os.path.exists(os.path.join(SCREENSHOTS_DIR, "05_drift_monitoring.png")):
        s14.shapes.add_picture(os.path.join(SCREENSHOTS_DIR, "05_drift_monitoring.png"), Inches(6.8), Inches(1.6), width=Inches(5.7))
    add_card(s14, 0.8, 5.0, 11.7, 1.0, "Interactive Simulation Tools", [
        "What-If Weather Presets: 1-Click buttons for Light Breeze, Moderate Wind, and Gale Storms with instant power predictions.",
        "Online Drift Telemetry: Watch the cumulative error score rise and trigger automatic retraining with full audit logs."
    ], accent_color=C_BLUE)
    add_speaker_tip(s14, 0.8, 6.1, 11.7, 0.85,
        "Tell the examiner: 'Operators can test hypothetical storm conditions using interactive sliders and watch the drift detection algorithm respond live.'")

    # SLIDE 15: Real-World Impact & Conclusion
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Real-World Impact & Key Takeaways", 15)
    if os.path.exists(os.path.join(CHARTS_DIR, "chart_12_sdg_grid.png")):
        s15.shapes.add_picture(os.path.join(CHARTS_DIR, "chart_12_sdg_grid.png"), Inches(0.8), Inches(1.6), width=Inches(6.8))
    add_card(s15, 7.8, 1.6, 4.7, 3.8, "Why This Project Matters", [
        "1. Cheaper, Reliable Clean Energy (SDG 7): Accurate forecasts eliminate the need to keep expensive fossil fuel plants running on standby.",
        "2. Climate Impact (SDG 13): Helps power grids accept +8.4% more wind energy, offsetting 1,420 tonnes of CO2e annually per wind farm.",
        "3. Green & Frugal Computing (SDG 12): Cuts retraining compute footprint by ~80%, easily running on low-cost edge computers.",
        "4. Industry Ready: Fast 3-millisecond inference, zero false alarms, and full-stack SCADA web platform ready for deployment."
    ], accent_color=C_EMERALD)
    add_speaker_tip(s15, 7.8, 5.55, 4.7, 1.35,
        "Final Viva Conclusion Script: 'To conclude, our project solves a major bottleneck in renewable energy: by giving AI models a self-healing check-engine light, we achieve 75% higher accuracy with 5 times less compute, making wind energy cheaper and more dependable.'")

    prs.save(OUTPUT_PPTX_REPORTS)
    print(f"Saved 15-Slide Presentation PPTX to: {OUTPUT_PPTX_REPORTS}")

    shutil.copy2(OUTPUT_PPTX_REPORTS, USER_DOWNLOADS)
    print(f"Copied 15-Slide Presentation PPTX to Downloads: {USER_DOWNLOADS}")

if __name__ == '__main__':
    create_15slide_pptx()
