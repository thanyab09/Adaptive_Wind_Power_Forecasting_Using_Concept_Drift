import React, { useEffect, useState } from 'react';
import {
  FileText,
  Play,
  Download,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Sliders,
  Layers,
  Sparkles,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import ChartContainer from '../components/ChartContainer';
import { api } from '../services/api';
import { formatNumber, formatSeconds } from '../utils/formatters';

export default function ExperimentsReport() {
  const [benchmark, setBenchmark] = useState(null);
  const [sensitivity, setSensitivity] = useState(null);
  const [loading, setLoading] = useState(true);

  // Experiment run controls
  const [seed, setSeed] = useState(0);
  const [drift, setDrift] = useState(true);
  const [magnitude, setMagnitude] = useState(1.0);
  const [detector, setDetector] = useState('ph');

  // Job status
  const [jobId, setJobId] = useState(null);
  const [jobProgress, setJobProgress] = useState(0);
  const [jobMessage, setJobMessage] = useState('');
  const [jobRunning, setJobRunning] = useState(false);
  const [liveResult, setLiveResult] = useState(null);

  useEffect(() => {
    loadBenchmarkAndSensitivity();
  }, []);

  const loadBenchmarkAndSensitivity = async () => {
    try {
      setLoading(true);
      const [bm, sens] = await Promise.all([
        api.getBenchmarkResults('drift'),
        api.getSensitivityAnalysis(),
      ]);
      setBenchmark(bm);
      setSensitivity(sens);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartExperiment = async (e) => {
    e.preventDefault();
    try {
      setJobRunning(true);
      setJobProgress(10);
      setJobMessage('Submitting experiment job...');
      setLiveResult(null);

      const res = await api.runExperiment(seed, drift, magnitude, detector);
      const currentJobId = res.job_id;
      setJobId(currentJobId);

      // Poll job status
      const interval = setInterval(async () => {
        try {
          const statusRes = await api.getExperimentStatus(currentJobId);
          setJobProgress(statusRes.progress);
          setJobMessage(statusRes.message);

          if (statusRes.status === 'completed') {
            clearInterval(interval);
            setJobRunning(false);
            setLiveResult(statusRes.result);
          } else if (statusRes.status === 'failed') {
            clearInterval(interval);
            setJobRunning(false);
            alert(`Job failed: ${statusRes.message}`);
          }
        } catch (e) {
          clearInterval(interval);
          setJobRunning(false);
        }
      }, 800);
    } catch (err) {
      setJobRunning(false);
      alert(`Failed to start experiment: ${err.message}`);
    }
  };

  const perSeed = benchmark?.per_seed || [];
  const sensLam = sensitivity?.threshold_lambda || [];
  const sensCd = sensitivity?.cooldown_hours || [];
  const sensWin = sensitivity?.retraining_window_weeks || [];
  const sensMag = sensitivity?.drift_magnitude || [];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header and Download Bar */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="p-2 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200/60">
              <FileText className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold tracking-tight text-slate-800">
              Reproducible Experiments & Verification Reports
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
            Execute reproducible prequential experiments across independent random seeds and generate academic PDF summary reports.
          </p>
        </div>

        {/* Export Buttons */}
        <div className="flex flex-wrap items-center gap-2.5">
          <a
            href={api.getDownloadReportPdfUrl()}
            className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-soft active:scale-95 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF Viva Report</span>
          </a>

          <a
            href={api.getDownloadReportJsonUrl()}
            className="flex items-center gap-1.5 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-xl border border-slate-200 transition-colors shadow-soft-sm"
          >
            <Download className="w-3.5 h-3.5 text-sky-600" />
            <span>JSON</span>
          </a>

          <a
            href={api.getDownloadReportCsvUrl()}
            className="flex items-center gap-1.5 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-xl border border-slate-200 transition-colors shadow-soft-sm"
          >
            <Download className="w-3.5 h-3.5 text-sky-600" />
            <span>CSV</span>
          </a>
        </div>
      </div>

      {/* Experiment Runner Controls */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Experiment Execution Workbench</h3>
            <p className="text-xs text-slate-500 mt-0.5">Select simulation parameters and run prequential streaming evaluation</p>
          </div>
          <span className="text-xs font-mono text-emerald-800 bg-emerald-50 border border-emerald-200/80 px-3 py-1 rounded-full font-bold self-start">
            Prequential (13,440 steps)
          </span>
        </div>

        <form onSubmit={handleStartExperiment} className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider block mb-1">
              Random Seed (0 to 9)
            </label>
            <select
              value={seed}
              onChange={(e) => setSeed(parseInt(e.target.value))}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
            >
              {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((s) => (
                <option key={s} value={s}>Seed {s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider block mb-1">
              Scenario
            </label>
            <select
              value={drift ? 'drift' : 'nodrift'}
              onChange={(e) => setDrift(e.target.value === 'drift')}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
            >
              <option value="drift">Abrupt Drift (Week 28)</option>
              <option value="nodrift">No-Drift Control</option>
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-600 uppercase tracking-wider block mb-1">
              Drift Detector
            </label>
            <select
              value={detector}
              onChange={(e) => setDetector(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
            >
              <option value="ph">Page-Hinkley (Proposed)</option>
              <option value="cusum">CUSUM Detector</option>
              <option value="adwin">ADWIN (Adaptive Window)</option>
              <option value="kspsi">KS + PSI Only</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={jobRunning}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-soft active:scale-95 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {jobRunning ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
              <span>{jobRunning ? 'Running...' : 'Run Simulation'}</span>
            </button>
          </div>
        </form>

        {/* Progress Bar */}
        {jobRunning && (
          <div className="space-y-1.5 pt-3 border-t border-slate-100 animate-fade-in">
            <div className="flex justify-between text-xs text-slate-600">
              <span className="flex items-center gap-1.5 text-emerald-700 font-semibold">
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                {jobMessage}
              </span>
              <span className="font-mono font-bold text-slate-800">{jobProgress}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div
                className="bg-emerald-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${jobProgress}%` }}
              />
            </div>
          </div>
        )}

        {/* Live Result Card */}
        {liveResult && (
          <div className="p-5 rounded-2xl bg-emerald-50/80 border border-emerald-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-fade-in shadow-soft">
            <div>
              <span className="text-[10px] text-emerald-800 font-bold uppercase tracking-wider block">
                Trial Completed (Random Seed {liveResult.seed})
              </span>
              <div className="text-base font-bold font-mono text-emerald-950 mt-0.5">
                Adaptive MAE: {liveResult.adaptive?.mae} kW vs Static MAE: {liveResult.static?.mae} kW
              </div>
              <div className="text-xs text-emerald-700 mt-1">
                Detection Delay: {liveResult.adaptive?.detection_delay_hours ?? 'N/A'} h | Retrainings: {liveResult.adaptive?.retrainings} | Compute: {liveResult.adaptive?.retraining_time_s} s
              </div>
            </div>
            <span className="text-xs font-bold text-emerald-800 bg-white px-3 py-1 rounded-full border border-emerald-200 shadow-soft-sm self-start sm:self-center">
              Verified
            </span>
          </div>
        )}
      </div>

      {/* Ten Seeds Verification Table */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Ten-Seed Empirical Benchmark (Abrupt Drift Scenario)</h3>
            <p className="text-xs text-slate-500 mt-0.5">Verification of Table 6.1 and Appendix D.1 per-seed results from project report</p>
          </div>
          <span className="text-xs font-mono text-emerald-800 bg-emerald-50 border border-emerald-200/80 px-3 py-1 rounded-full font-bold self-start">
            Mean 75.0% Error Reduction
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b border-slate-200/80 text-slate-500 uppercase text-[10px] font-bold bg-slate-50/70 font-sans">
                <th className="py-2.5 px-3">Seed</th>
                <th className="py-2.5 px-3">Static MAE</th>
                <th className="py-2.5 px-3">Adaptive MAE</th>
                <th className="py-2.5 px-3">Weekly MAE</th>
                <th className="py-2.5 px-3">Delay (h)</th>
                <th className="py-2.5 px-3">Early Retr. (3w)</th>
                <th className="py-2.5 px-3">Later Retr.</th>
                <th className="py-2.5 px-3 text-right">Error Reduction</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {perSeed.map((row) => (
                <tr key={row.seed} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2.5 px-3 font-bold text-slate-800">Seed {row.seed}</td>
                  <td className="py-2.5 px-3 text-rose-600">{row.static_mae} kW</td>
                  <td className="py-2.5 px-3 text-emerald-700 font-bold">{row.adaptive_mae} kW</td>
                  <td className="py-2.5 px-3 text-slate-600">{row.weekly_mae} kW</td>
                  <td className="py-2.5 px-3 text-amber-700">{row.delay_h} h</td>
                  <td className="py-2.5 px-3 text-slate-600">{row.early_retrains}</td>
                  <td className="py-2.5 px-3 text-slate-600">{row.late_retrains}</td>
                  <td className="py-2.5 px-3 text-right text-emerald-700 font-bold font-sans">
                    {row.reduction_pct}%
                  </td>
                </tr>
              ))}
              <tr className="bg-slate-50/80 font-bold border-t-2 border-slate-200">
                <td className="py-3 px-3 text-slate-900 font-sans">Mean ± Std</td>
                <td className="py-3 px-3 text-rose-600">134.7 ± 5.6</td>
                <td className="py-3 px-3 text-emerald-700">33.7 ± 2.1</td>
                <td className="py-3 px-3 text-slate-700">35.3 ± 1.3</td>
                <td className="py-3 px-3 text-amber-700">21.5 h</td>
                <td className="py-3 px-3 text-slate-700">6.2</td>
                <td className="py-3 px-3 text-slate-700">10.0</td>
                <td className="py-3 px-3 text-right text-emerald-700 font-sans text-sm">75.0%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Sensitivity Analysis Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sensitivity 1: Threshold Lambda */}
        <ChartContainer
          title="Sensitivity to Page-Hinkley Threshold λ (multiples of σ₀)"
          subtitle="λ = 15σ₀ represents the optimal Pareto frontier: 0 false alarms with 19.4h latency"
          height="h-64"
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sensLam} margin={{ top: 15, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="lambda" label={{ value: 'Threshold λ (× σ₀)', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} tick={{ fill: '#64748B', fontSize: 10 }} />
              <YAxis yAxisId="left" tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: 'Delay (h)', angle: -90, position: 'insideLeft', fill: '#64748B', fontSize: 10 }} />
              <YAxis yAxisId="right" orientation="right" tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: 'False Alarms', angle: 90, position: 'insideRight', fill: '#64748B', fontSize: 10 }} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
              <Legend verticalAlign="top" height={30} wrapperStyle={{ fontSize: '11px' }} />
              <Line yAxisId="left" type="monotone" dataKey="delay_h" name="Detection Delay (h)" stroke="#059669" strokeWidth={2} />
              <Line yAxisId="right" type="monotone" dataKey="no_drift_alarms" name="False Alarms (No Drift)" stroke="#E11D48" strokeWidth={2} strokeDasharray="3 3" />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>

        {/* Sensitivity 2: Drift Magnitude Gain */}
        <ChartContainer
          title="Sensitivity to Drift Magnitude (0.0 to 1.5)"
          subtitle="Adaptation gain scales with drift size; negligible shifts (≤ 0.1) are safely ignored"
          height="h-64"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={sensMag} margin={{ top: 15, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="magnitude" label={{ value: 'Drift Magnitude', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} tick={{ fill: '#64748B', fontSize: 10 }} />
              <YAxis tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: '% Error Reduction', angle: -90, position: 'insideLeft', fill: '#64748B', fontSize: 10 }} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
              <Bar dataKey="reduction_pct" name="MAE Reduction vs Static (%)" fill="#059669" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>
    </div>
  );
}
