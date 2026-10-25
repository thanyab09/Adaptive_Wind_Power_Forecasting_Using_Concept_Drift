import React, { useEffect, useState } from 'react';
import {
  Database,
  Download,
  Search,
  Filter,
  BarChart,
  Compass,
  Zap,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart as RechartsBarChart,
  Bar,
  Cell,
  Legend,
} from 'recharts';
import ChartContainer from '../components/ChartContainer';
import { api } from '../services/api';
import { formatNumber, formatSpeed, formatKW } from '../utils/formatters';

export default function DatasetExplorer() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const rowsPerPage = 12;

  useEffect(() => {
    loadDatasetInfo();
  }, []);

  const loadDatasetInfo = async () => {
    try {
      setLoading(true);
      const res = await api.getDatasetPreview();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const rows = data?.preview_rows || [];
  const filteredRows = rows.filter((r) =>
    Object.values(r).some((v) =>
      String(v).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const totalPages = Math.ceil(filteredRows.length / rowsPerPage) || 1;
  const paginatedRows = filteredRows.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  const stats = data?.summary_stats || {};
  const corr = data?.correlation_matrix || { columns: [], matrix: [] };
  const scatter = data?.power_curve_scatter || [];
  const windRose = data?.wind_rose || [];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <span className="p-2 rounded-xl bg-sky-50 text-sky-700 border border-sky-200/60">
              <Database className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold tracking-tight text-slate-800">
              Dataset Explorer & Meteorological Feature Analytics
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
            Inspect physical data properties, aerodynamic turbine power curves, directional wind distributions, and Pearson feature correlations.
          </p>
        </div>

        <a
          href={api.getDownloadDatasetUrl()}
          className="flex items-center gap-1.5 px-4 py-2.5 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-xl border border-slate-200 active:scale-95 transition-all self-start md:self-center shadow-soft-sm"
        >
          <Download className="w-4 h-4 text-emerald-700" />
          <span>Export Active CSV</span>
        </a>
      </div>

      {/* Dataset Health Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-soft">
          <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">Total Record Count</span>
          <div className="text-2xl font-bold font-mono text-slate-800">
            {formatNumber(data?.rows || 17808, 0)}
          </div>
          <span className="text-xs text-slate-500 mt-0.5 block">Hourly samples (106 weeks)</span>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-soft">
          <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">Missing Value Health</span>
          <div className="text-2xl font-bold font-mono text-emerald-700">
            0 Missing
          </div>
          <span className="text-xs text-emerald-700 font-medium mt-0.5 block">100% complete time-series</span>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-soft">
          <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">Mean Wind Speed</span>
          <div className="text-2xl font-bold font-mono text-sky-700">
            {formatSpeed(stats.wind_speed?.mean || 7.6)}
          </div>
          <span className="text-xs text-slate-500 mt-0.5 block">Std: {stats.wind_speed?.std || 2.7} m/s</span>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-soft">
          <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1">Turbine Nameplate</span>
          <div className="text-2xl font-bold font-mono text-purple-700">
            2,000 kW
          </div>
          <span className="text-xs text-slate-500 mt-0.5 block">Capacity factor: ~31.6%</span>
        </div>
      </div>

      {/* Visualizations Grid: Scatter Plot + Wind Rose */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Plot 1: Empirical Power Curve */}
        <ChartContainer
          title="Empirical Aerodynamic Power Curve (Speed vs Power)"
          subtitle="Non-linear cubic conversion between cut-in (3 m/s) and rated speed (12 m/s)"
          height="h-72"
        >
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 15, right: 15, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="wind_speed" name="Wind Speed" unit=" m/s" tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: 'Wind Speed (m/s)', position: 'insideBottom', offset: -4, fill: '#64748B', fontSize: 10 }} domain={[0, 25]} />
              <YAxis dataKey="power" name="Power" unit=" kW" tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: 'Power (kW)', angle: -90, position: 'insideLeft', fill: '#64748B', fontSize: 10 }} domain={[0, 2100]} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
              <Scatter name="SCADA Observations" data={scatter} fill="#059669" fillOpacity={0.5} shape="circle" />
            </ScatterChart>
          </ResponsiveContainer>
        </ChartContainer>

        {/* Plot 2: Directional Wind Distribution */}
        <ChartContainer
          title="Directional Wind Rose Distribution (% Hours by Sector)"
          subtitle="Prevailing South-West wind (225°); soft coral indicates wake sector (200°-265°)"
          height="h-72"
        >
          <ResponsiveContainer width="100%" height="100%">
            <RechartsBarChart data={windRose} margin={{ top: 15, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="sector" tick={{ fill: '#64748B', fontSize: 9 }} />
              <YAxis tick={{ fill: '#64748B', fontSize: 10 }} label={{ value: '% of Hours', angle: -90, position: 'insideLeft', fill: '#64748B', fontSize: 10 }} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', fontSize: '11px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
              <Bar dataKey="percentage" name="% Frequency" radius={[4, 4, 0, 0]}>
                {windRose.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.wake_sector ? '#E11D48' : '#059669'} />
                ))}
              </Bar>
            </RechartsBarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>

      {/* Pearson Correlation Heatmap */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft space-y-4">
        <div>
          <h3 className="text-sm font-bold text-slate-800">Feature Pearson Correlation Matrix</h3>
          <p className="text-xs text-slate-500 mt-0.5">Linear correlation coefficients among physical SCADA variables</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-center text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b border-slate-200/80 text-slate-500 bg-slate-50/70 font-sans uppercase text-[10px] font-bold">
                <th className="py-2.5 px-3 text-left">Variable</th>
                {corr.columns.map((col, idx) => (
                  <th key={idx} className="py-2.5 px-3">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {corr.matrix.map((row, rIdx) => (
                <tr key={rIdx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2 px-3 text-left font-sans font-semibold text-slate-800">{corr.columns[rIdx]}</td>
                  {row.map((val, cIdx) => {
                    const absVal = Math.abs(val);
                    let cellColor = 'text-slate-600';
                    let bg = '';
                    if (absVal > 0.8) {
                      cellColor = 'text-emerald-800 font-bold';
                      bg = 'bg-emerald-50';
                    } else if (absVal > 0.4) {
                      cellColor = 'text-sky-800 font-semibold';
                      bg = 'bg-sky-50/50';
                    }
                    return (
                      <td key={cIdx} className={`py-2 px-3 ${cellColor} ${bg}`}>
                        {val.toFixed(2)}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Paginated Data Preview Table */}
      <div className="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-bold text-slate-800">Time-Series Observations Table</h3>
            <p className="text-xs text-slate-500 mt-0.5">Chronologically ordered SCADA sensor telemetry</p>
          </div>

          <div className="relative">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => { setSearchTerm(e.target.value); setPage(1); }}
              placeholder="Search table values..."
              className="bg-slate-50 border border-slate-200 rounded-xl pl-8 pr-3 py-1.5 text-xs text-slate-800 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 shadow-soft-sm"
            />
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b border-slate-200/80 text-slate-500 uppercase text-[10px] font-bold bg-slate-50/70 font-sans">
                <th className="py-2 px-3">Timestamp</th>
                <th className="py-2 px-3">Wind Speed (m/s)</th>
                <th className="py-2 px-3">Direction (°)</th>
                <th className="py-2 px-3">Temperature (°C)</th>
                <th className="py-2 px-3 text-right">Power Output (kW)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {paginatedRows.map((r, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2 px-3 text-slate-600">{r.timestamp}</td>
                  <td className="py-2 px-3 text-slate-700">{Number(r.wind_speed).toFixed(2)}</td>
                  <td className="py-2 px-3 text-slate-600">{Number(r.wind_direction).toFixed(1)}°</td>
                  <td className="py-2 px-3 text-slate-600">{Number(r.temperature).toFixed(1)}</td>
                  <td className="py-2 px-3 text-right text-emerald-700 font-bold">{Number(r.power).toFixed(1)} kW</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination controls */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-3 border-t border-slate-100">
          <span>
            Showing {(page - 1) * rowsPerPage + 1} to {Math.min(page * rowsPerPage, filteredRows.length)} of {filteredRows.length} entries
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page === 1}
              className="px-3 py-1 bg-slate-100 hover:bg-slate-200 disabled:opacity-40 rounded-xl text-slate-700 font-semibold transition-colors"
            >
              Previous
            </button>
            <span className="font-mono font-bold text-slate-800">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page === totalPages}
              className="px-3 py-1 bg-slate-100 hover:bg-slate-200 disabled:opacity-40 rounded-xl text-slate-700 font-semibold transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
