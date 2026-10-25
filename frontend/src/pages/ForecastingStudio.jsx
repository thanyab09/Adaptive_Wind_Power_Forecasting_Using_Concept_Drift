import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Play,
  Upload,
  Download,
  Sliders,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Compass,
  Thermometer,
  Wind,
  Sparkles,
  Zap,
  Table,
} from 'lucide-react';
import ChartContainer from '../components/ChartContainer';
import { api } from '../services/api';
import { formatKW, formatNumber } from '../utils/formatters';

export default function ForecastingStudio() {
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [trainingLoading, setTrainingLoading] = useState(false);
  const [predictLoading, setPredictLoading] = useState(false);
  const [trainMessage, setTrainMessage] = useState(null);
  const [singleResult, setSingleResult] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [activeTab, setActiveTab] = useState('workbench'); // 'workbench' or 'stream'

  // Forecast manual input state
  const [inputs, setInputs] = useState({
    wind_speed: 10.5,
    wind_direction: 225.0,
    temperature: 16.5,
    power_lag_1: 1240.0,
    power_lag_2: 1190.0,
    power_lag_24: 1050.0,
    power_rolling_6h: 1210.0,
    wind_speed_lag_1: 10.2,
    wind_speed_rolling_3h: 10.1,
  });

  const presets = [
    {
      name: '🍃 Light Breeze',
      speed: 5.5,
      dir: 180,
      temp: 18.0,
      p1: 280,
      p2: 260,
      p24: 300,
      r6: 275,
      color: 'bg-emerald-100/90 text-emerald-800 border-emerald-300 hover:bg-emerald-200',
    },
    {
      name: '💨 Moderate Wind',
      speed: 10.5,
      dir: 225,
      temp: 16.0,
      p1: 1240,
      p2: 1190,
      p24: 1050,
      r6: 1210,
      color: 'bg-sky-100/90 text-sky-800 border-sky-300 hover:bg-sky-200',
    },
    {
      name: '⚡ Gale / High Wind',
      speed: 16.8,
      dir: 240,
      temp: 13.5,
      p1: 1980,
      p2: 1950,
      p24: 1890,
      r6: 1960,
      color: 'bg-amber-100/90 text-amber-800 border-amber-300 hover:bg-amber-200',
    },
  ];

  const applyPreset = (p) => {
    setInputs({
      wind_speed: p.speed,
      wind_direction: p.dir,
      temperature: p.temp,
      power_lag_1: p.p1,
      power_lag_2: p.p2,
      power_lag_24: p.p24,
      power_rolling_6h: p.r6,
      wind_speed_lag_1: p.speed - 0.3,
      wind_speed_rolling_3h: p.speed - 0.2,
    });
  };

  useEffect(() => {
    loadForecastHistory();
  }, []);

  const loadForecastHistory = async () => {
    try {
      setLoading(true);
      const res = await api.getForecastHistory();
      setHistory(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTrain = async () => {
    try {
      setTrainingLoading(true);
      setTrainMessage(null);
      const res = await api.trainBaseModel();
      setTrainMessage(`Model v${res.model_version} trained successfully! Training MAE: ${res.training_metrics.mae} kW, RMSE: ${res.training_metrics.rmse} kW.`);
      await loadForecastHistory();
    } catch (err) {
      setTrainMessage(`Training error: ${err.message}`);
    } finally {
      setTrainingLoading(false);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    try {
      setPredictLoading(true);
      const res = await api.predictForecast(inputs);
      setSingleResult(res);
    } catch (err) {
      alert(`Prediction failed: ${err.message}`);
    } finally {
      setPredictLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      setUploadError(null);
      await api.uploadDatasetCSV(file);
      alert('CSV uploaded and loaded successfully! Models initialized.');
      await loadForecastHistory();
    } catch (err) {
      setUploadError(err.message);
    }
  };

  const recentRows = history?.recent_24h || [];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Studio Header & Tab Switcher */}
      <div className="bg-white border border-slate-200/80 rounded-3xl p-5 sm:p-6 shadow-soft flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-soft">
              <TrendingUp className="w-5 h-5 stroke-[2.4]" />
            </div>
            <div>
              <h2 className="text-xl font-black tracking-tight text-slate-800">
                Forecasting Studio & Model Workbench
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Execute 1-hour-ahead inference with HistGradientBoostingRegressor against meteorological conditions.
              </p>
            </div>
          </div>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center gap-2 self-start md:self-center">
          <div className="flex items-center p-1 bg-slate-100 rounded-2xl border border-slate-200/70 shadow-soft-sm">
            <button
              onClick={() => setActiveTab('workbench')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                activeTab === 'workbench'
                  ? 'bg-white text-emerald-800 shadow-soft'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Zap className="w-3.5 h-3.5 text-emerald-600" />
              <span>⚡ Live Predictor</span>
            </button>

            <button
              onClick={() => setActiveTab('stream')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                activeTab === 'stream'
                  ? 'bg-white text-sky-800 shadow-soft'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Table className="w-3.5 h-3.5 text-sky-600" />
              <span>📋 24h SCADA Stream</span>
            </button>
          </div>

          <label className="flex items-center gap-1.5 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-2xl border border-slate-200 cursor-pointer active:scale-95 transition-all shadow-soft-sm">
            <Upload className="w-3.5 h-3.5 text-sky-600" />
            <span>Upload CSV</span>
            <input type="file" accept=".csv" onChange={handleFileUpload} className="hidden" />
          </label>
        </div>
      </div>

      {uploadError && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-xs text-rose-800 flex items-center gap-2.5 shadow-soft">
          <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
          <span>{uploadError}</span>
        </div>
      )}

      {trainMessage && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-800 flex items-center gap-2.5 shadow-soft">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
          <span>{trainMessage}</span>
        </div>
      )}

      {/* SUB-VIEW 1: INTERACTIVE FORECASTER (Clean Form + Result Card) */}
      {activeTab === 'workbench' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in">
          {/* Left 2 Cols: 1h Forecast Generator Form */}
          <div className="lg:col-span-2 bg-white border border-slate-200/80 rounded-3xl p-6 shadow-soft space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-sm font-bold text-slate-800">Meteorological Condition Inputs</h3>
                <p className="text-xs text-slate-500 mt-0.5">Select a quick preset or adjust turbine sensor inputs</p>
              </div>

              {/* Colorful 1-Click Preset Buttons */}
              <div className="flex items-center gap-1.5 flex-wrap">
                {presets.map((p, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => applyPreset(p)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all active:scale-95 shadow-soft-sm ${p.color}`}
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            </div>

            <form onSubmit={handlePredict} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="bg-emerald-50/50 p-3.5 rounded-2xl border border-emerald-200/70">
                  <label className="text-[11px] font-bold text-emerald-900 uppercase tracking-wider block mb-1">
                    Wind Speed (m/s)
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="35"
                      value={inputs.wind_speed}
                      onChange={(e) => setInputs({ ...inputs, wind_speed: parseFloat(e.target.value) || 0 })}
                      className="w-full bg-white border border-emerald-200 rounded-xl p-2.5 pl-8 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                    />
                    <Wind className="w-3.5 h-3.5 text-emerald-600 absolute left-2.5 top-3" />
                  </div>
                  <span className="text-[10px] text-emerald-700 font-medium block mt-1">Rated power at ~12 m/s</span>
                </div>

                <div className="bg-sky-50/50 p-3.5 rounded-2xl border border-sky-200/70">
                  <label className="text-[11px] font-bold text-sky-900 uppercase tracking-wider block mb-1">
                    Wind Direction (°)
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      step="1"
                      min="0"
                      max="360"
                      value={inputs.wind_direction}
                      onChange={(e) => setInputs({ ...inputs, wind_direction: parseFloat(e.target.value) || 0 })}
                      className="w-full bg-white border border-sky-200 rounded-xl p-2.5 pl-8 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-100"
                    />
                    <Compass className="w-3.5 h-3.5 text-sky-600 absolute left-2.5 top-3" />
                  </div>
                  {inputs.wind_direction >= 200 && inputs.wind_direction <= 265 ? (
                    <span className="text-[10px] text-rose-700 font-bold block mt-1">⚠️ Wake sector (200°-265°)</span>
                  ) : (
                    <span className="text-[10px] text-sky-700 font-medium block mt-1">Free-stream sector</span>
                  )}
                </div>

                <div className="bg-purple-50/50 p-3.5 rounded-2xl border border-purple-200/70">
                  <label className="text-[11px] font-bold text-purple-900 uppercase tracking-wider block mb-1">
                    Temperature (°C)
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      step="0.5"
                      value={inputs.temperature}
                      onChange={(e) => setInputs({ ...inputs, temperature: parseFloat(e.target.value) || 0 })}
                      className="w-full bg-white border border-purple-200 rounded-xl p-2.5 pl-8 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                    />
                    <Thermometer className="w-3.5 h-3.5 text-purple-600 absolute left-2.5 top-3" />
                  </div>
                  <span className="text-[10px] text-purple-700 font-medium block mt-1">Air density effect</span>
                </div>
              </div>

              {/* Lagged Features */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-100">
                <div>
                  <label className="text-[10px] font-semibold text-slate-500 block mb-1">Power Lag t-1 (kW)</label>
                  <input
                    type="number"
                    value={inputs.power_lag_1}
                    onChange={(e) => setInputs({ ...inputs, power_lag_1: parseFloat(e.target.value) || 0 })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-mono text-slate-700"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-semibold text-slate-500 block mb-1">Power Lag t-2 (kW)</label>
                  <input
                    type="number"
                    value={inputs.power_lag_2}
                    onChange={(e) => setInputs({ ...inputs, power_lag_2: parseFloat(e.target.value) || 0 })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-mono text-slate-700"
                  />
                </div>
                <div>
                  <label className="text-[10px] font-semibold text-slate-500 block mb-1">Rolling Mean (6h)</label>
                  <input
                    type="number"
                    value={inputs.power_rolling_6h}
                    onChange={(e) => setInputs({ ...inputs, power_rolling_6h: parseFloat(e.target.value) || 0 })}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2 text-xs font-mono text-slate-700"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-slate-500 font-mono">
                  Horizon: <strong className="text-slate-800">1 Hour Ahead (t+1)</strong>
                </span>
                <button
                  type="submit"
                  disabled={predictLoading}
                  className="px-6 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold rounded-2xl shadow-soft transition-all active:scale-95 disabled:opacity-50 flex items-center gap-2"
                >
                  {predictLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
                  <span>Generate 1h Forecast</span>
                </button>
              </div>
            </form>

            {/* Prominent Forecast Result Card */}
            {singleResult && (
              <div className="mt-4 p-5 rounded-3xl bg-gradient-to-r from-emerald-100/80 via-teal-100/50 to-emerald-100/80 border-2 border-emerald-300 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-fade-in shadow-soft">
                <div>
                  <div className="text-[11px] text-emerald-900 font-extrabold uppercase tracking-wider">
                    Predicted Generation Output
                  </div>
                  <div className="text-4xl font-black font-mono text-emerald-950 mt-0.5">
                    {formatKW(singleResult.predicted_power_kw)}
                  </div>
                  <div className="text-xs text-emerald-800 font-semibold mt-1">
                    90% Confidence Interval: [{formatKW(singleResult.confidence_interval.lower)} — {formatKW(singleResult.confidence_interval.upper)}]
                  </div>
                </div>
                <div className="sm:text-right bg-white px-5 py-3 rounded-2xl border border-emerald-300 shadow-soft-sm">
                  <span className="text-3xl font-black font-mono text-emerald-700">
                    {singleResult.capacity_factor_pct}%
                  </span>
                  <span className="block text-[10px] text-slate-500 uppercase font-bold tracking-wider">Capacity Factor</span>
                </div>
              </div>
            )}
          </div>

          {/* Right Col: Forecaster Specifications Card */}
          <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-soft space-y-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                <Sliders className="w-4 h-4 text-emerald-700" />
                <h3 className="text-sm font-bold text-slate-800">Forecaster Specification</h3>
              </div>

              <div className="space-y-3.5 text-xs text-slate-600 pt-2">
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Algorithm</span>
                  <span className="font-bold text-slate-800 text-sm">HistGradientBoostingRegressor</span>
                  <span className="block text-[11px] text-slate-500 mt-0.5">Histogram-binned gradient boosted decision trees</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Hyperparameters</span>
                  <div className="grid grid-cols-2 gap-2 mt-1.5 font-mono text-xs text-slate-700">
                    <div>Trees: <b className="text-slate-900">120</b></div>
                    <div>Learning Rate: <b className="text-slate-900">0.10</b></div>
                    <div>Max Depth: <b className="text-slate-900">6</b></div>
                    <div>Min Leaf: <b className="text-slate-900">20</b></div>
                  </div>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Feature Pipeline</span>
                  <span className="text-[11px] text-slate-600 block mt-0.5 leading-relaxed">
                    10 meteorological features: wind speed, cube power proxy (v³), cyclical wind direction (sin/cos), temperature, power lags (t-1, t-2, t-24), rolling means.
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleTrain}
              disabled={trainingLoading}
              className="w-full py-2.5 px-4 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold border border-slate-200 transition-all flex items-center justify-center gap-2"
            >
              {trainingLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
              <span>Retrain Base Model</span>
            </button>
          </div>
        </div>
      )}

      {/* SUB-VIEW 2: 24-HOUR SCADA STREAM TABLE */}
      {activeTab === 'stream' && (
        <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-soft space-y-4 animate-fade-in">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Recent 24-Hour Prequential Forecast Stream</h3>
              <p className="text-xs text-slate-500 mt-0.5">Sequential hour-by-hour actual vs predicted power and residual error</p>
            </div>
            <a
              href={api.getDownloadDatasetUrl()}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-50 hover:bg-slate-100 text-xs font-bold text-slate-700 border border-slate-200 rounded-2xl transition-colors self-start shadow-soft-sm"
            >
              <Download className="w-3.5 h-3.5 text-emerald-700" />
              <span>Download Full Results CSV</span>
            </a>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 uppercase text-[10px] font-bold bg-slate-50/80">
                  <th className="py-2.5 px-3">Hour</th>
                  <th className="py-2.5 px-3">Wind Speed</th>
                  <th className="py-2.5 px-3">Temp</th>
                  <th className="py-2.5 px-3 text-right">Actual Power</th>
                  <th className="py-2.5 px-3 text-right">Predicted Power</th>
                  <th className="py-2.5 px-3 text-right">Error (kW)</th>
                  <th className="py-2.5 px-3 text-right">Abs Error</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {recentRows.map((r, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-2.5 px-3 font-bold text-slate-800">{r.hour}</td>
                    <td className="py-2.5 px-3 text-slate-600">{r.wind_speed_ms} m/s</td>
                    <td className="py-2.5 px-3 text-slate-600">{r.temperature_c} °C</td>
                    <td className="py-2.5 px-3 text-right text-slate-700 font-bold">{formatNumber(r.actual_power_kw)} kW</td>
                    <td className="py-2.5 px-3 text-right text-emerald-700 font-bold">{formatNumber(r.predicted_power_kw)} kW</td>
                    <td className={`py-2.5 px-3 text-right font-bold ${r.error_kw > 0 ? 'text-amber-800' : 'text-sky-800'}`}>
                      {r.error_kw > 0 ? `+${r.error_kw}` : r.error_kw}
                    </td>
                    <td className="py-2.5 px-3 text-right text-slate-600">{r.abs_error_kw} kW</td>
                  </tr>
                ))}
                {recentRows.length === 0 && (
                  <tr>
                    <td colSpan={7} className="py-8 text-center text-slate-400 font-sans">
                      No forecast predictions available yet. Click "Train Base Model" to initialize.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
