import React from 'react';
import {
  Activity,
  TrendingUp,
  AlertTriangle,
  RefreshCw,
  BarChart2,
  Database,
  FileText,
  GraduationCap,
} from 'lucide-react';

export default function Sidebar({ activePage, setActivePage }) {
  const navItems = [
    {
      id: 'overview',
      label: 'Overview Dashboard',
      icon: Activity,
      color: 'text-emerald-700 bg-emerald-100/80',
      activeBg: 'bg-emerald-50 text-emerald-900 border-emerald-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'forecasting',
      label: 'Forecasting Studio',
      icon: TrendingUp,
      color: 'text-sky-700 bg-sky-100/80',
      activeBg: 'bg-sky-50 text-sky-900 border-sky-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'drift',
      label: 'Drift Monitoring',
      icon: AlertTriangle,
      color: 'text-amber-800 bg-amber-100/80',
      activeBg: 'bg-amber-50 text-amber-900 border-amber-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'adaptation',
      label: 'Adaptive Learning',
      icon: RefreshCw,
      color: 'text-purple-700 bg-purple-100/80',
      activeBg: 'bg-purple-50 text-purple-900 border-purple-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'comparison',
      label: 'Model Comparison',
      icon: BarChart2,
      color: 'text-indigo-700 bg-indigo-100/80',
      activeBg: 'bg-indigo-50 text-indigo-900 border-indigo-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'dataset',
      label: 'Dataset Explorer',
      icon: Database,
      color: 'text-teal-700 bg-teal-100/80',
      activeBg: 'bg-teal-50 text-teal-900 border-teal-200/90 shadow-soft-sm font-bold',
    },
    {
      id: 'experiments',
      label: 'Experiments & Reports',
      icon: FileText,
      color: 'text-rose-700 bg-rose-100/80',
      activeBg: 'bg-rose-50 text-rose-900 border-rose-200/90 shadow-soft-sm font-bold',
    },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200/80 flex flex-col justify-between p-4 flex-shrink-0 shadow-soft-sm">
      <div>
        <div className="text-[11px] font-bold text-slate-400 tracking-wider uppercase px-3 mb-2.5">
          Navigation Modules
        </div>
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-2xl text-xs transition-all border ${
                  isActive
                    ? item.activeBg
                    : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <div className={`p-1.5 rounded-xl ${item.color}`}>
                  <Icon className="w-4 h-4 stroke-[2.2]" />
                </div>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Academic Citation Box */}
      <div className="p-4 rounded-3xl bg-gradient-to-br from-slate-50 to-emerald-50/40 border border-slate-200/80 text-[11px] text-slate-500 space-y-1.5 shadow-soft-sm">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
          <GraduationCap className="w-4 h-4 text-emerald-700" />
          <span>B.Tech AI/ML Project</span>
        </div>
        <div className="text-slate-700 font-bold">Panimalar Engineering College</div>
        <div className="text-[10px] text-slate-500 leading-tight">
          Thanya B [211423247227]<br/>
          Thejessri S [211423247229]
        </div>
        <div className="pt-2 border-t border-slate-200 text-[10px] font-semibold text-emerald-800">
          Supervisor: Mr. M. Ezhilvendhan
        </div>
      </div>
    </aside>
  );
}
