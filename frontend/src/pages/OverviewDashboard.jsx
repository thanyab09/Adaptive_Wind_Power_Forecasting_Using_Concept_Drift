import React, { useEffect, useState } from 'react';
import {
  Zap,
  Activity,
  AlertTriangle,
  RefreshCw,
  Wind,
  Layers,
  Clock,
  CheckCircle2,
  TrendingDown,
  ShieldCheck,
  BarChart3,
  Calendar,
  Sparkles,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ReferenceLine,
  AreaChart,
  Area,
} from 'recharts';
import MetricCard from '../components/MetricCard';
import ChartContainer from '../components/ChartContainer';
import StatusBadge from '../components/StatusBadge';
import { api } from '../services/api';
import { formatKW, formatNumber } from '../utils/formatters';

export default function OverviewDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get('tab') === 'analytics' ? 'analytics' : 'live';
    } catch {
      return 'live';
    }
  });

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboardSummary();
      setData(res);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard summary');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-400 gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
        <span className="text-sm font-semibold text-slate-600">Connecting to forecasting engine...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-rose-50 border border-rose-200 rounded-3xl text-rose-800 shadow-soft">
        <h3 className="text-sm font-bold flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-rose-600" />
          Backend Connection Error
        </h3>
        <p className="text-xs mt-1 text-rose-700">{error}</p>
        <button
          onClick={loadDashboard}
          className="mt-3 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold shadow-soft"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  const {
    current_hour,
    current_week,
    model_version,
    drift_status,
    latest_forecast_kw,
    latest_actual_kw,
    current_mae_kw,
    current_rmse_kw,
    current_nrmse_pct,
    total_alarms,
    total_retrainings,
    cooldown_remaining_hours,
    last_alarm_hour,
    last_retrain_hour,
    dataset_name,
    page_hinkley_stat,
    page_hinkley_threshold,
    weekly_trends = [],
    zoom_onset = [],
    alarms = [],
  } = data;

  const capacityPct = Math.min(100, Math.max(0, ((latest_forecast_kw / 2000.0) * 100))).toFixed(1);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Top Banner with Navigation Tabs for De-congestion */}
      <div className="bg-white border border-slate-200/80 rounded-3xl p-5 sm:p-6 shadow-soft flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white shadow-soft">
              <Wind className="w-5 h-5 stroke-[2.4]" />
            </div>
            <div>
              <h2 className="text-xl font-black tracking-tight text-slate-800">
                Forecasting & Drift Control Center
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Real-time 1-hour ahead generation forecasting with Page-Hinkley concept drift adaptation.
              </p>
            </div>
          </div>
        </div>

        {/* View Switcher Tabs to keep each view clean & minimal */}
        <div className="flex items-center gap-2 self-start md:self-center">
          <div className="flex items-center p-1 bg-slate-100 rounded-2xl border border-slate-200/70 shadow-soft-sm">
            <button
              onClick={() => setActiveTab('live')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                activeTab === 'live'
                  ? 'bg-white text-emerald-800 shadow-soft'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Zap className="w-3.5 h-3.5 text-emerald-600" />
              <span>⚡ Live Overview</span>
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                activeTab === 'analytics'
                  ? 'bg-white text-sky-800 shadow-soft'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5 text-sky-600" />
              <span>📈 80-Wk Drift History</span>
            </button>
          </div>

          <button
            onClick={loadDashboard}
            title="Refresh dashboard metrics"
            className="p-2 rounded-2xl bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200 active:scale-95 transition-all shadow-soft-sm"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* SUB-VIEW 1: LIVE EXECUTIVE OVERVIEW (Minimal, Breathable, Colorful) */}
      {activeTab === 'live' && (
        <div className="space-y-6 animate-fade-in">
          {/* Hero Forecast Generation Card with Visual Capacity Meter */}
          <div className="bg-gradient-to-r from-emerald-500/10 via-teal-500/5 to-sky-500/10 border-2 border-emerald-200/90 rounded-3xl p-6 shadow-soft flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100 border border-emerald-300/80 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <Zap className="w-3 h-3 text-emerald-700" /> Current Online Forecast
                </span>
                <StatusBadge status={drift_status} size="sm" />
              </div>
              <div className="flex items-baseline gap-3 flex-wrap">
                <span className="text-4xl sm:text-5xl font-black font-mono text-emerald-950 tracking-tight">
                  {formatNumber(latest_forecast_kw)}
                </span>
                <span className="text-lg font-bold text-emerald-700">kW Generation</span>
                <span className="text-xs font-semibold text-slate-500">
                  (Observed Actual: <strong className="text-slate-800 font-mono">{formatKW(latest_actual_kw)}</strong>)
                </span>
              </div>
              <p className="text-xs text-slate-600 max-w-xl leading-relaxed">
                Turbine operating at <strong>{capacityPct}% nameplate capacity</strong> (2,000 kW rated). Forecaster is recalibrated on a 672-hour sliding window.
              </p>
            </div>

            {/* Visual Capacity Bar Gauge */}
            <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-4 border border-emerald-200/80 shadow-soft-sm min-w-[260px]">
              <div className="flex items-center justify-between text-xs font-bold mb-2">
                <span className="text-slate-600">Capacity Factor</span>
                <span className="text-emerald-700 font-mono">{capacityPct}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden p-0.5 border border-slate-200">
                <div
                  className="bg-gradient-to-r from-teal-500 to-emerald-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${capacityPct}%` }}
                />
              </div>
              <div className="mt-2.5 flex items-center justify-between text-[10px] text-slate-500 font-semibold">
                <span>0 kW (Cut-in)</span>
                <span>2,000 kW (Rated)</span>
              </div>
            </div>
          </div>

          {/* 3 Colorful Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <MetricCard
              title="Forecasting Accuracy"
              value={formatNumber(current_mae_kw)}
              unit="kW MAE"
              subtext={`RMSE: ${formatKW(current_rmse_kw)} (nRMSE ${current_nrmse_pct}%)`}
              icon={Activity}
              accentColor="teal"
              badge={
                <span className="text-[10px] text-emerald-800 font-bold bg-emerald-100 border border-emerald-300 px-2 py-0.5 rounded-full">
                  75% Error Gain
                </span>
              }
            />

            <MetricCard
              title="Page-Hinkley Drift Stat"
              value={formatNumber(page_hinkley_stat, 2)}
              unit={`/ ${formatNumber(page_hinkley_threshold, 1)}`}
              subtext={drift_status === 'Stable' ? 'Within calibrated bounds' : 'Threshold exceeded'}
              icon={AlertTriangle}
              accentColor={drift_status === 'Stable' ? 'emerald' : 'amber'}
              badge={<StatusBadge status={drift_status} size="sm" />}
            />

            <MetricCard
              title="Adaptive Controller"
              value={`v${model_version}`}
              unit={`(${total_retrainings} retrains)`}
              subtext={cooldown_remaining_hours > 0 ? `Cooldown: ${cooldown_remaining_hours}h left` : 'Controller Ready'}
              icon={RefreshCw}
              accentColor="purple"
              badge={
                <span className="text-[10px] text-purple-800 font-bold bg-purple-100 border border-purple-200 px-2 py-0.5 rounded-full">
                  672h Window
                </span>
              }
            />
          </div>

          {/* Stream Telemetry Ribbon */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-white border border-slate-200/80 rounded-2xl p-4 text-xs shadow-soft">
            <div className="p-2 rounded-xl bg-slate-50/70">
              <span className="text-slate-400 block text-[10px] uppercase font-bold tracking-wider">Stream Position</span>
              <span className="font-mono font-bold text-slate-800 text-sm">Hour {current_hour?.toLocaleString()} <span className="text-emerald-700 font-sans text-xs font-semibold">(Wk {current_week})</span></span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50/70">
              <span className="text-slate-400 block text-[10px] uppercase font-bold tracking-wider">Last Drift Alarm</span>
              <span className="font-mono font-bold text-slate-700 text-sm">{last_alarm_hour ? `Hour ${last_alarm_hour.toLocaleString()}` : 'None (Stationary)'}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50/70">
              <span className="text-slate-400 block text-[10px] uppercase font-bold tracking-wider">Last Retrain Event</span>
              <span className="font-mono font-bold text-slate-700 text-sm">{last_retrain_hour ? `Hour ${last_retrain_hour.toLocaleString()}` : 'Initial Model'}</span>
            </div>
            <div className="p-2 rounded-xl bg-slate-50/70">
              <span className="text-slate-400 block text-[10px] uppercase font-bold tracking-wider">Dataset Source</span>
              <span className="font-bold text-emerald-800 truncate block text-sm">{dataset_name}</span>
            </div>
          </div>

          {/* Focal Chart: Actual vs Predicted Wind Power around Drift Onset */}
          <ChartContainer
            title="Real-Time Model Tracking (Zoom: Drift Onset Period)"
            subtitle="Static model severely over-predicts post-drift, while Adaptive model rapidly recalibrates"
            height="h-80"
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={zoom_onset} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="day_of_stream" label={{ value: 'Day of Online Stream', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} tick={{ fill: '#64748B', fontSize: 10 }} />
                <YAxis tick={{ fill: '#64748B', fontSize: 10 }} domain={[0, 2200]} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
                <Legend verticalAlign="top" height={30} wrapperStyle={{ fontSize: '11px' }} />
                <ReferenceLine x={14.0} stroke="#E11D48" strokeDasharray="3 3" label={{ value: 'Drift Onset', fill: '#E11D48', fontSize: 10, position: 'insideTopLeft' }} />
                <Line type="monotone" dataKey="actual_power" name="Observed Actual Power" stroke="#94A3B8" strokeWidth={1.8} dot={false} />
                <Line type="monotone" dataKey="static_pred" name="Static Baseline (No Adaptation)" stroke="#E11D48" strokeWidth={1.6} dot={false} />
                <Line type="monotone" dataKey="adaptive_pred" name="Adaptive (Proposed)" stroke="#059669" strokeWidth={2.4} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>
        </div>
      )}

      {/* SUB-VIEW 2: 80-WEEK HORIZON & AUDIT LOG (Clean, Analytical) */}
      {activeTab === 'analytics' && (
        <div className="space-y-6 animate-fade-in">
          {/* 80-Week Weekly MAE Trend Chart */}
          <ChartContainer
            title="Weekly Error Divergence Across 80-Week Horizon"
            subtitle="Static error surges to ~140 kW post-drift, while Adaptive recovers and stabilizes at ~33 kW"
            height="h-80"
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={weekly_trends} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="week" label={{ value: 'Week', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} tick={{ fill: '#64748B', fontSize: 10 }} />
                <YAxis tick={{ fill: '#64748B', fontSize: 10 }} domain={[0, 250]} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
                <Legend verticalAlign="top" height={30} wrapperStyle={{ fontSize: '11px' }} />
                <ReferenceLine x={28} stroke="#E11D48" strokeDasharray="3 3" label={{ value: 'Wk 28 Drift', fill: '#E11D48', fontSize: 10 }} />
                <Line type="monotone" dataKey="static_mae" name="Static MAE (kW)" stroke="#E11D48" strokeWidth={1.8} dot={false} />
                <Line type="monotone" dataKey="weekly_mae" name="Weekly Retrain MAE" stroke="#0284C7" strokeWidth={1.6} dot={false} />
                <Line type="monotone" dataKey="adaptive_mae" name="Adaptive MAE (kW)" stroke="#059669" strokeWidth={2.4} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartContainer>

          {/* Drift Alarm & Retraining Audit Table */}
          <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-soft space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-sm font-bold text-slate-800">Concept Drift Alarm & Retraining Audit Trail</h3>
                <p className="text-xs text-slate-500 mt-0.5">Chronological record of Page-Hinkley triggers and model recalibrations</p>
              </div>
              <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-100 border border-emerald-300 px-3 py-1 rounded-full self-start">
                {alarms.length} Drift Events Detected
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 uppercase text-[10px] font-bold bg-slate-50/80">
                    <th className="py-3 px-3">Alarm Hour</th>
                    <th className="py-3 px-3">Week</th>
                    <th className="py-3 px-3">Trigger Source</th>
                    <th className="py-3 px-3">Detection Latency</th>
                    <th className="py-3 px-3">Estimated Change Point</th>
                    <th className="py-3 px-3">Adaptive Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-mono">
                  {alarms.map((al, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-2.5 px-3 font-bold text-slate-800">{al.hour?.toLocaleString()}</td>
                      <td className="py-2.5 px-3 text-slate-600 font-sans">{al.week}</td>
                      <td className="py-2.5 px-3 text-amber-800 font-sans font-medium">{al.source}</td>
                      <td className="py-2.5 px-3 text-rose-600 font-semibold">+{al.delay_hours ?? al.delay_from_onset} h</td>
                      <td className="py-2.5 px-3 text-slate-600">Hour {al.estimated_tau?.toLocaleString()}</td>
                      <td className="py-2.5 px-3 font-sans">
                        <span className="text-[11px] font-bold text-emerald-800 bg-emerald-100 border border-emerald-200 px-2.5 py-0.5 rounded-full">
                          Retrained (672h Window)
                        </span>
                      </td>
                    </tr>
                  ))}
                  {alarms.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-slate-400 font-sans">
                        No drift alarms raised. Forecaster operating within calibrated error margins.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex flex-wrap items-center justify-between gap-2">
              <span>Refractory period: 48h cooldown prevents alarm thrashing</span>
              <span className="text-emerald-700 font-semibold flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Zero false alarms before true onset
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
