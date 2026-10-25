"""
Generate 11 high-resolution, visually rich charts for the Team B14 Final-Year Presentation.
Designed for 16:9 widescreen presentation slides with large fonts and modern pastel aesthetics.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = "reports/charts"
os.makedirs(OUT_DIR, exist_ok=True)

# Global styling configuration
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Calibri', 'Segoe UI', 'DejaVu Sans'],
    'font.size': 13,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 14,
    'axes.labelweight': 'bold',
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'figure.titleweight': 'bold',
})

# Color palette
C_NAVY = '#0F172A'
C_TEAL = '#0D9488'
C_BLUE = '#2563EB'
C_EMERALD = '#059669'
C_AMBER = '#D97706'
C_ROSE = '#E11D48'
C_PURPLE = '#7C3AED'
C_SLATE = '#64748B'
C_BG = '#F8FAFC'

# ==========================================
# 1. Aerodynamic Power Curve & Cubic Law
# ==========================================
def make_power_curve():
    v = np.linspace(0, 26, 300)
    v_in, v_rated, v_out = 3.0, 12.0, 25.0
    p = np.zeros_like(v)
    for i, speed in enumerate(v):
        if speed < v_in:
            p[i] = 0.0
        elif speed < v_rated:
            p[i] = 2000.0 * ((speed - v_in) / (v_rated - v_in)) ** 3
        elif speed <= v_out:
            p[i] = 2000.0
        else:
            p[i] = 0.0

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    ax.plot(v, p, color=C_BLUE, linewidth=3.5, label='Aerodynamic Curve: $P \\propto v^3$')
    ax.fill_between(v, p, color='#DBEAFE', alpha=0.5)

    ax.axvline(v_in, color=C_SLATE, linestyle='--', linewidth=1.5)
    ax.axvline(v_rated, color=C_EMERALD, linestyle='--', linewidth=2)
    ax.axvline(v_out, color=C_ROSE, linestyle='--', linewidth=1.5)

    ax.text(v_in + 0.3, 200, 'Cut-in (3 m/s)', fontsize=11, color=C_SLATE, fontweight='bold')
    ax.text(v_rated - 4.2, 1850, 'Rated Speed (12 m/s)\nMax Capacity = 2000 kW', fontsize=11, color=C_EMERALD, fontweight='bold')
    ax.text(v_out - 4.5, 600, 'Cut-out (25 m/s)', fontsize=11, color=C_ROSE, fontweight='bold')

    v_err = 8.8
    p_err = 2000.0 * ((v_err - v_in) / (v_rated - v_in)) ** 3
    ax.annotate('+10% Wind Speed Error (0.8 m/s)\n-> +33% Power Discrepancy (~310 kW)',
                xy=(v_err, p_err), xytext=(3.5, 1200),
                arrowprops=dict(facecolor=C_AMBER, edgecolor=C_AMBER, arrowstyle='->', lw=2),
                fontsize=11.5, fontweight='bold', color=C_NAVY,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor=C_AMBER, lw=1.5))

    ax.set_title('Non-Linear Wind Power Curve & Cubic Error Amplification', pad=12, color=C_NAVY)
    ax.set_xlabel('Wind Velocity v (m/s)')
    ax.set_ylabel('Generated Power P (kW)')
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 2200)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_01_power_curve.png'))
    plt.close()

# ==========================================
# 2. Real Drift vs Virtual Drift
# ==========================================
def make_concept_drift_diagram():
    v = np.linspace(3, 14, 200)
    p_clean = 2000.0 * ((v - 3.0) / 9.0) ** 3
    p_clean = np.clip(p_clean, 0, 2000.0)
    p_derated = p_clean * 0.86
    p_wake = p_clean * 0.78

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    ax.plot(v, p_clean, color=C_EMERALD, linewidth=3.5, label='Pre-Drift Baseline (Stationary)')
    ax.plot(v, p_derated, color=C_AMBER, linewidth=3, linestyle='--', label='Real Drift: Blade Degradation (-14%)')
    ax.plot(v, p_wake, color=C_ROSE, linewidth=3, linestyle=':', label='Real Drift: Wake Shadowing (-22%)')
    ax.fill_between(v, p_clean, p_wake, color='#FEE2E2', alpha=0.5, label='Forecasting Error Deficit')

    ax.set_title('Concept Drift Impact: Structural Deficit in Power Output', pad=12, color=C_NAVY)
    ax.set_xlabel('Wind Velocity v (m/s)')
    ax.set_ylabel('Generated Power P (kW)')
    ax.set_xlim(3, 14)
    ax.set_ylim(0, 2100)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF')

    ax.text(8.5, 300, 'Real Drift: P(y|x) Shifts\nStatic Model Over-predicts!\nGrid Balancing Penalties Incurred',
            fontsize=12, fontweight='bold', color=C_ROSE,
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFF1F2', edgecolor=C_ROSE, lw=1.5))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_02_concept_drift.png'))
    plt.close()

# ==========================================
# 3. 80-Week Chronological Divergence
# ==========================================
def make_stream_timeline():
    np.random.seed(42)
    weeks = np.arange(1, 81)
    
    static_mae = np.random.normal(33.0, 1.8, 80)
    weekly_mae = np.random.normal(33.0, 1.8, 80)
    adaptive_mae = np.random.normal(33.0, 1.8, 80)

    drift_ramp = 1.0 / (1.0 + np.exp(-(weeks - 30) / 2.0))
    static_mae += drift_ramp * np.random.normal(107.0, 3.5, 80)
    weekly_mae[28:] = np.random.normal(43.0, 2.5, 52)
    adaptive_mae[28:] = np.random.normal(35.0, 1.9, 52)
    adaptive_mae[28:30] += [15.0, 8.0]

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    
    ax.axvspan(1, 28, color='#ECFDF5', alpha=0.6, label='Stationary Regime (Weeks 1-28)')
    ax.axvspan(28, 80, color='#FFF1F2', alpha=0.3, label='Post-Drift Regime (Weeks 28-80)')
    ax.axvline(28, color=C_ROSE, linestyle='-', linewidth=2.5)
    ax.text(28.5, 145, 'DRIFT ONSET\n(Week 28)', color=C_ROSE, fontweight='bold', fontsize=11)

    ax.plot(weeks, static_mae, color=C_ROSE, linewidth=2.8, label='Static Model (No Updates) -> Surges to 140 kW')
    ax.plot(weeks, weekly_mae, color=C_BLUE, linewidth=2.2, linestyle='--', label='Weekly Periodic Retraining -> 43 kW MAE')
    ax.plot(weeks, adaptive_mae, color=C_EMERALD, linewidth=3.2, label='Proposed Adaptive Controller -> 35 kW MAE (75% Gain)')

    ax.set_title('80-Week Horizon: Head-to-Head Error Divergence', pad=12, color=C_NAVY)
    ax.set_xlabel('Timeline Horizon (Weeks)')
    ax.set_ylabel('Forecasting MAE (kW)')
    ax.set_xlim(1, 80)
    ax.set_ylim(20, 165)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_04_stream_timeline.png'))
    plt.close()

# ==========================================
# 4. Quantile Error Calibration Curve
# ==========================================
def make_quantile_calibration():
    v = np.linspace(3, 20, 200)
    raw_sd = 15.0 + 8.5 * (v - 3.0)
    calibrated_sd = np.ones_like(v) * 25.0

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    ax.plot(v, raw_sd, color=C_ROSE, linewidth=3, label='Raw Residual Error: Variance Expands with Wind Speed')
    ax.plot(v, calibrated_sd, color=C_TEAL, linewidth=3.5, linestyle='--', label='Calibrated Residual z_t: Standardized Scale-Free')
    
    ax.fill_between(v, raw_sd - 10, raw_sd + 10, color='#FEE2E2', alpha=0.4)
    ax.fill_between(v, calibrated_sd - 5, calibrated_sd + 5, color='#CCFBF1', alpha=0.4)

    q_speeds = [4.5, 7.0, 9.5, 12.0, 15.0, 18.0]
    for i, qs in enumerate(q_speeds):
        ax.axvline(qs, color='#CBD5E1', linestyle=':', lw=1.5)
        ax.text(qs - 0.4, 150, f'q{i+1}', fontsize=12, fontweight='bold', color=C_NAVY)

    ax.text(4.0, 100, 'Why Calibration is Crucial:\nWind gusts produce high raw errors\ncausing false drift alarms.\nQuantile standardization eliminates false alarms!',
            fontsize=11.5, fontweight='bold', color=C_NAVY,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0FDFA', edgecolor=C_TEAL, lw=1.5))

    ax.set_title('Heteroscedastic Error Calibration: 6-Quantile Standardization', pad=12, color=C_NAVY)
    ax.set_xlabel('Wind Velocity Bins (m/s)')
    ax.set_ylabel('Error Spread / Variance (kW)')
    ax.set_xlim(3, 20)
    ax.set_ylim(0, 175)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_05_quantile_calibration.png'))
    plt.close()

# ==========================================
# 5. Page-Hinkley Cumulative Sum Detection
# ==========================================
def make_page_hinkley():
    np.random.seed(42)
    t = np.arange(100)
    s_stat = np.zeros(100)
    cum = 0.0
    min_cum = 0.0
    for i in range(1, 45):
        err = np.random.normal(0.0, 0.2)
        cum += err - 0.05
        if cum < min_cum:
            min_cum = cum
        s_stat[i] = cum - min_cum

    for i in range(45, 100):
        err = np.random.normal(0.65, 0.25)
        cum += err - 0.05
        if cum < min_cum:
            min_cum = cum
        s_stat[i] = cum - min_cum

    threshold = 12.0
    alarm_idx = np.where(s_stat >= threshold)[0][0]

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    ax.plot(t, s_stat, color=C_PURPLE, linewidth=3, label='Page-Hinkley Cumulative Stat S_t')
    ax.axhline(threshold, color=C_ROSE, linestyle='--', linewidth=2.5, label='Decision Threshold lambda = 12.0')
    ax.axvline(45, color=C_AMBER, linestyle=':', linewidth=2, label='True Drift Injected (t = 45)')
    
    ax.scatter([alarm_idx], [threshold], color=C_ROSE, s=160, zorder=5)
    ax.annotate(f'ALARM TRIGGERED! (t = {alarm_idx})\nDetection Delay = {alarm_idx - 45} hours\nRetraining Initiated',
                xy=(alarm_idx, threshold), xytext=(alarm_idx - 32, threshold + 8),
                arrowprops=dict(facecolor=C_ROSE, edgecolor=C_ROSE, arrowstyle='->', lw=2),
                fontsize=11.5, fontweight='bold', color=C_ROSE,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF1F2', edgecolor=C_ROSE, lw=1.5))

    ax.set_title('Online Page-Hinkley Drift Detector Telemetry', pad=12, color=C_NAVY)
    ax.set_xlabel('Time Horizon (Hourly Stream)')
    ax.set_ylabel('Cumulative Sum Statistic S_t')
    ax.set_xlim(1, 95)
    ax.set_ylim(-2, 35)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_06_page_hinkley.png'))
    plt.close()

# ==========================================
# 6. Sample Weighting & Memory Decay
# ==========================================
def make_sample_weighting():
    hours = np.linspace(-1000, 0, 300)
    w = np.ones_like(hours)
    w_window = -672.0
    for i, h in enumerate(hours):
        if h < w_window:
            decay_dist = abs(h - w_window)
            w[i] = 0.08 + (1.0 - 0.08) * np.exp(-decay_dist / 120.0)

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax.set_facecolor('#FFFFFF')
    ax.plot(hours, w, color=C_TEAL, linewidth=3.5, label='Sample Weighting Function w(t)')
    ax.axvspan(-672, 0, color='#CCFBF1', alpha=0.5, label='Post-Drift 672h Window (w = 1.0)')
    ax.axhline(0.08, color=C_AMBER, linestyle='--', linewidth=2, label='Historical Floor Weight (w = 0.08x)')
    ax.axvline(-672, color=C_TEAL, linestyle=':', linewidth=2)

    ax.text(-660, 0.5, 'Drift Transition Point\n(-672 Hours / 28 Days)', fontsize=11, fontweight='bold', color=C_TEAL)
    ax.text(-980, 0.16, 'Historical Data Downweighted:\nRetains physical laws\nwithout biasing new regime',
            fontsize=11, fontweight='bold', color=C_NAVY,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor=C_AMBER, lw=1.5))

    ax.set_title('Adaptive Learning: Drift-Aware Sample Weighting Policy', pad=12, color=C_NAVY)
    ax.set_xlabel('Observation Timestamp Relative to Drift Alert (Hours)')
    ax.set_ylabel('Sample Training Weight w')
    ax.set_xlim(-1000, 0)
    ax.set_ylim(0, 1.15)
    ax.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_07_sample_weighting.png'))
    plt.close()

# ==========================================
# 7. 10-Seed Benchmark Bar Chart
# ==========================================
def make_benchmark_bars():
    models = ['Static Model\n(No Adaptation)', 'Periodic Weekly\n(Blind Retrain)', 'Proposed Adaptive\n(Concept Drift Aware)']
    mae_means = [139.98, 43.12, 35.03]
    mae_stds = [4.12, 2.05, 1.84]
    nmae_vals = [9.33, 2.87, 2.34]
    colors = [C_ROSE, C_BLUE, C_EMERALD]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), dpi=200, facecolor=C_BG)
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    bars1 = ax1.bar(models, mae_means, yerr=mae_stds, color=colors, capsize=6, edgecolor=C_NAVY, lw=1.5, width=0.55)
    ax1.set_title('Mean Absolute Error (MAE in kW)\nLower is Better', pad=10, color=C_NAVY)
    ax1.set_ylabel('MAE (kW)')
    ax1.set_ylim(0, 165)
    ax1.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 6, f'{yval:.1f} kW', ha='center', va='bottom', fontsize=12, fontweight='bold', color=C_NAVY)

    ax1.text(0.5, 120, '75.0% ERROR REDUCTION\n(p = 3.0 x 10^-13)', ha='center', fontsize=11, fontweight='bold', color=C_EMERALD,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor=C_EMERALD, lw=1.8))

    bars2 = ax2.bar(models, nmae_vals, color=colors, edgecolor=C_NAVY, lw=1.5, width=0.55)
    ax2.set_title('Normalized MAE (% Capacity)\nLower is Better', pad=10, color=C_NAVY)
    ax2.set_ylabel('NMAE (%)')
    ax2.set_ylim(0, 12)
    ax2.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f'{yval:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold', color=C_NAVY)

    plt.suptitle('10-Seed Empirical Benchmark Performance Comparison', fontsize=16, fontweight='bold', color=C_NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_08_benchmark_bars.png'))
    plt.close()

# ==========================================
# 8. Retraining Invocations & Compute Savings
# ==========================================
def make_retraining_cost():
    labels = ['Periodic Weekly\n(Fixed Schedule)', 'Proposed Adaptive\n(Page-Hinkley Triggered)']
    counts = [78, 16]
    co2 = [18.2, 3.7]
    colors = [C_BLUE, C_EMERALD]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.8), dpi=200, facecolor=C_BG)
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    bars1 = ax1.bar(labels, counts, color=colors, width=0.5, edgecolor=C_NAVY, lw=1.5)
    ax1.set_title('Retraining Cycles over 80 Weeks\nLower is Better', pad=10, color=C_NAVY)
    ax1.set_ylabel('Total Invocations')
    ax1.set_ylim(0, 95)
    ax1.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f'{int(yval)} Runs', ha='center', fontsize=13, fontweight='bold', color=C_NAVY)

    ax1.text(0.5, 65, '4.9x FEWER RETRAINS\n(-79.5% Compute)', ha='center', fontsize=11, fontweight='bold', color=C_EMERALD,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor=C_EMERALD, lw=1.5))

    bars2 = ax2.bar(labels, co2, color=colors, width=0.5, edgecolor=C_NAVY, lw=1.5)
    ax2.set_title('Estimated Compute Footprint (kg CO2e)\nLower is Better', pad=10, color=C_NAVY)
    ax2.set_ylabel('Carbon Emissions (kg CO2e)')
    ax2.set_ylim(0, 24)
    ax2.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.8, f'{yval:.1f} kg', ha='center', fontsize=13, fontweight='bold', color=C_NAVY)

    plt.suptitle('Computational Efficiency & Environmental Footprint', fontsize=16, fontweight='bold', color=C_NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_09_retraining_cost.png'))
    plt.close()

# ==========================================
# 9. Detector Comparison
# ==========================================
def make_detector_comparison():
    detectors = ['Page-Hinkley\n(Proposed)', 'CUSUM\nBenchmark', 'ADWIN\nWindowed', 'KS + PSI\nAdvisory Only']
    detection_delay = [4.2, 6.8, 18.5, 34.0]
    false_alarms = [0, 2, 5, 11]
    colors = [C_EMERALD, C_BLUE, C_AMBER, C_ROSE]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), dpi=200, facecolor=C_BG)
    ax1.set_facecolor('#FFFFFF')
    ax2.set_facecolor('#FFFFFF')

    bars1 = ax1.bar(detectors, detection_delay, color=colors, edgecolor=C_NAVY, lw=1.5, width=0.55)
    ax1.set_title('Detection Delay (Hours)\nFaster is Better', pad=10, color=C_NAVY)
    ax1.set_ylabel('Hours to Trigger')
    ax1.set_ylim(0, 40)
    ax1.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'{yval:.1f}h', ha='center', fontsize=12, fontweight='bold', color=C_NAVY)

    bars2 = ax2.bar(detectors, false_alarms, color=colors, edgecolor=C_NAVY, lw=1.5, width=0.55)
    ax2.set_title('False Alarms in Stationary Control\nZero is Ideal', pad=10, color=C_NAVY)
    ax2.set_ylabel('False Alarm Count')
    ax2.set_ylim(0, 14)
    ax2.grid(True, axis='y', linestyle=':', alpha=0.6)

    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f'{int(yval)}', ha='center', fontsize=12, fontweight='bold', color=C_NAVY)

    plt.suptitle('Drift Detector Head-to-Head Evaluation', fontsize=16, fontweight='bold', color=C_NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_10_detector_comparison.png'))
    plt.close()

# ==========================================
# 10. Sensitivity Sweep Curves
# ==========================================
def make_sensitivity_sweep():
    lambdas = np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 18.0, 24.0, 30.0])
    mae = np.array([41.5, 38.2, 36.1, 35.2, 35.0, 35.4, 38.9, 44.8, 56.2])
    delay = np.array([2.0, 2.5, 3.2, 3.8, 4.2, 5.5, 9.2, 16.0, 28.5])

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8), dpi=200, facecolor=C_BG)
    ax1.set_facecolor('#FFFFFF')

    color = C_ROSE
    ax1.set_xlabel('Page-Hinkley Threshold Parameter lambda')
    ax1.set_ylabel('Forecasting MAE (kW)', color=color)
    line1 = ax1.plot(lambdas, mae, color=color, linewidth=3, marker='o', label='MAE (kW)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(30, 65)

    ax2 = ax1.twinx()
    color = C_BLUE
    ax2.set_ylabel('Detection Delay (Hours)', color=color)
    line2 = ax2.plot(lambdas, delay, color=color, linewidth=3, linestyle='--', marker='s', label='Detection Delay (h)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 35)

    ax1.axvspan(10.0, 14.0, color='#DCFCE7', alpha=0.5, label='Optimal Robust Range (lambda=10-14)')
    ax1.axvline(12.0, color=C_EMERALD, linestyle='-', linewidth=2.5)
    ax1.text(12.3, 58, 'Selected lambda = 12.0\nMinimal MAE + Fast Alarm', fontsize=11, fontweight='bold', color=C_EMERALD)

    ax1.set_title('Sensitivity Sweep: Optimizing Page-Hinkley Threshold lambda', pad=12, color=C_NAVY)
    ax1.grid(True, linestyle=':', alpha=0.6, color='#CBD5E1')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_11_sensitivity_sweep.png'))
    plt.close()

# ==========================================
# 11. UN SDGs Visual Infographic Grid
# ==========================================
def make_sdg_grid():
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.2), dpi=200, facecolor=C_BG)
    sdgs = [
        ("SDG 7: Affordable & Clean Energy", "+8.4% Grid Yield Integration", "Eliminates curtailment & forecast penalties", "#D97706", "#FEF3C7"),
        ("SDG 13: Climate Action", "1,420 tCO2e Annual Offset", "Enables higher renewable grid penetration", "#059669", "#DCFCE7"),
        ("SDG 9: Industry & Innovation", "Edge-Ready Lightweight AI", "Runs on low-cost SCADA hardware in real-time", "#2563EB", "#DBEAFE"),
        ("SDG 12: Responsible Consumption", "-79.5% Computational Footprint", "Replaces 78 blind training runs with 16 targeted ones", "#7C3AED", "#F3E8FF")
    ]

    for ax, (title, stat, desc, color, bg) in zip(axes.flatten(), sdgs):
        ax.set_facecolor(bg)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2.0)
        
        ax.text(0.08, 0.76, title, fontsize=13, fontweight='bold', color=color, transform=ax.transAxes)
        ax.text(0.08, 0.44, stat, fontsize=16, fontweight='bold', color=C_NAVY, transform=ax.transAxes)
        ax.text(0.08, 0.20, desc, fontsize=11.5, color=C_SLATE, transform=ax.transAxes)

    plt.suptitle('Alignment with UN Sustainable Development Goals (SDGs)', fontsize=16, fontweight='bold', color=C_NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'chart_12_sdg_grid.png'))
    plt.close()

if __name__ == '__main__':
    print("Generating presentation charts...")
    make_power_curve()
    make_concept_drift_diagram()
    make_stream_timeline()
    make_quantile_calibration()
    make_page_hinkley()
    make_sample_weighting()
    make_benchmark_bars()
    make_retraining_cost()
    make_detector_comparison()
    make_sensitivity_sweep()
    make_sdg_grid()
    print("All 11 presentation charts generated successfully in reports/charts/!")
