import React, { useEffect, useState } from 'react';
import {
  RefreshCw,
  Clock,
  Layers,
  Sliders,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  Scale,
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ReferenceLine,
} from 'recharts';
import ChartContainer from '../components/ChartContainer';
import MetricCard from '../components/MetricCard';
import RetrainModal from '../components/RetrainModal';
import { api } from '../services/api';
import { formatNumber, formatSeconds } from '../utils/formatters';

export default function AdaptiveLearning() {
  const [status, setStatus] = useState(null);
  const [history, setHistory] = useState([]);
  const [weightsCurve, setWeightsCurve] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [retraining, setRetraining] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAdaptationData();
  }, []);

  const loadAdaptationData = async () => {
    try {
      setLoading(true);
      const [st, hist, wc] = await Promise.all([
        api.getAdaptationStatus(),
        api.getRetrainingHistory(),
        api.getWeightsCurve(),
      ]);
      setStatus(st);
      setHistory(hist.retrainings || []);
      setWeightsCurve(wc.curve || []);
    } catch (err) {
      console.error('Error loading adaptation data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleManualRetrainConfirm = async (reason) => {
    try {
      setRetraining(true);
      await api.triggerManualRetrain(reason);
      setIsModalOpen(false);
      await loadAdaptationData();
      alert('Manual model retraining successfully executed and logged.');
    } catch (err) {
      alert(`Retraining failed: ${err.message}`);
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="p-2 rounded-xl bg-purple-50 text-purple-700 border border-purple-200/60">
              <RefreshCw className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold tracking-tight text-slate-800">
              Adaptive Learning & Retraining Controller
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
            Governs model updates when concept drift is authorized. Fits the forecaster to a 4-week (672 h) window,
            applying recency weighting (half-life 336 h) and downweighting pre-change observations (0.08x).
          </p>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs rounded-xl shadow-soft active:scale-95 transition-all self-start md:self-center"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Manual Retrain Trigger</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Active Model Version"
          value={`v${status?.model_version || 1}`}
          subtext="HistGradientBoostingRegressor"
          icon={Layers}
          accentColor="teal"
          badge={
            <span className="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-bold">
              Deployed
            </span>
          }
        />

        <MetricCard
          title="Retraining Window"
          value="672 h"
          unit="(4 Weeks)"
          subtext="Sliding window discards outdated regimes"
          icon={Clock}
          accentColor="cyan"
          badge={
            <span className="text-[10px] text-sky-700 bg-sky-50 border border-sky-200 px-2 py-0.5 rounded-full font-mono font-bold">
              w = 672
            </span>
          }
        />

        <MetricCard
          title="Cooldown Guard"
          value={status?.cooldown_active ? `${status.cooldown_remaining_hours} h` : 'Ready'}
          unit={status?.cooldown_active ? 'remaining' : ''}
          subtext="48h refractory lock prevents thrashing"
          icon={ShieldCheck}
          accentColor={status?.cooldown_active ? 'amber' : 'emerald'}
          badge={
            <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
              status?.cooldown_active 
                ? 'bg-amber-50 text-amber-800 border border-amber-200' 
                : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
            }`}>
              {status?.cooldown_active ? 'Active' : 'Standby'}
            </span>
          }
        />

        <MetricCard
          title="Total Retrainings"
          value={formatNumber(status?.total_retrainings || history.length, 0)}
          subtext="Cumulative compute ~1.98 s"
          icon={RefreshCw}
          accentColor="purple"
          badge={
            <span className="text-[10px] text-purple-700 bg-purple-50 border border-purple-200 px-2 py-0.5 rounded-full font-bold">
              4.9x Less Compute
            </span>
          }
        />
      </div>

      {/* Sample Weighting Visualization */}
      <ChartContainer
        title="Sample Weighting Function Over the 672-Hour Retraining Window"
        subtitle="Recency decay (half-life 336 h) with drift-aware downweighting (0.08x) before estimated change point τ̂"
        height="h-72"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={weightsCurve} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="hour_in_window" label={{ value: 'Hours within 672h Window (Oldest → Newest)', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} tick={{ fill: '#64748B', fontSize: 10 }} />
            <YAxis tick={{ fill: '#64748B', fontSize: 10 }} domain={[0, 1.1]} />
            <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
            <Legend verticalAlign="top" height={30} wrapperStyle={{ fontSize: '11px' }} />
            <ReferenceLine x={520} stroke="#E11D48" strokeDasharray="3 3" label={{ value: 'Estimated Change Point τ̂', fill: '#E11D48', fontSize: 10 }} />
            <Line type="monotone" dataKey="recency_weight" name="Standard Recency Decay (w = 2^(-age/336))" stroke="#0284C7" strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
            <Line type="monotone" dataKey="drift_aware_weight" name="Drift-Aware Weighting (Pre-change × 0.08)" stroke="#059669" strokeWidth={2.2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      {/* Retraining Audit History Table */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Model Retraining Audit Log</h3>
            <p className="text-xs text-slate-500 mt-0.5">Full operational record of autonomous drift adaptations and manual interventions</p>
          </div>
          <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-full self-start">
            {history.length} Events Logged
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-200/80 text-slate-500 uppercase text-[10px] font-bold bg-slate-50/70 font-sans">
                <th className="py-2.5 px-3">Model Version</th>
                <th className="py-2.5 px-3">Stream Hour</th>
                <th className="py-2.5 px-3">Week</th>
                <th className="py-2.5 px-3">Samples Used</th>
                <th className="py-2.5 px-3">Training Duration</th>
                <th className="py-2.5 px-3">Trigger Reason</th>
                <th className="py-2.5 px-3">Change Point τ̂</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono">
              {history.map((ev, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2.5 px-3 font-bold text-emerald-700">v{ev.model_version}</td>
                  <td className="py-2.5 px-3 font-semibold text-slate-800">{ev.hour?.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-slate-600 font-sans">{ev.week}</td>
                  <td className="py-2.5 px-3 text-slate-600">{ev.sample_count} h</td>
                  <td className="py-2.5 px-3 text-slate-700">{formatSeconds(ev.duration_sec)}</td>
                  <td className="py-2.5 px-3 font-sans text-slate-600">{ev.reason}</td>
                  <td className="py-2.5 px-3 text-slate-500">{ev.estimated_tau ? `Hour ${ev.estimated_tau}` : 'None'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Confirmation Modal */}
      <RetrainModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleManualRetrainConfirm}
        loading={retraining}
      />
    </div>
  );
}
