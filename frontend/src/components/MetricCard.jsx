import React from 'react';

export default function MetricCard({
  title,
  value,
  unit = '',
  subtext,
  icon: Icon,
  trend,
  trendPositive = true,
  badge,
  accentColor = 'teal',
}) {
  const accentStyles = {
    teal: {
      borderTop: 'border-t-4 border-t-emerald-500',
      iconBg: 'bg-emerald-100/80 text-emerald-800 border border-emerald-200/60',
      trendColor: 'text-emerald-700 bg-emerald-50 border-emerald-200',
    },
    cyan: {
      borderTop: 'border-t-4 border-t-sky-500',
      iconBg: 'bg-sky-100/80 text-sky-800 border border-sky-200/60',
      trendColor: 'text-sky-700 bg-sky-50 border-sky-200',
    },
    emerald: {
      borderTop: 'border-t-4 border-t-teal-500',
      iconBg: 'bg-teal-100/80 text-teal-800 border border-teal-200/60',
      trendColor: 'text-teal-700 bg-teal-50 border-teal-200',
    },
    amber: {
      borderTop: 'border-t-4 border-t-amber-500',
      iconBg: 'bg-amber-100/80 text-amber-800 border border-amber-200/60',
      trendColor: 'text-amber-800 bg-amber-50 border-amber-200',
    },
    red: {
      borderTop: 'border-t-4 border-t-rose-500',
      iconBg: 'bg-rose-100/80 text-rose-800 border border-rose-200/60',
      trendColor: 'text-rose-700 bg-rose-50 border-rose-200',
    },
    purple: {
      borderTop: 'border-t-4 border-t-purple-500',
      iconBg: 'bg-purple-100/80 text-purple-800 border border-purple-200/60',
      trendColor: 'text-purple-700 bg-purple-50 border-purple-200',
    },
  };

  const style = accentStyles[accentColor] || accentStyles.teal;

  return (
    <div className={`bg-white border border-slate-200/80 rounded-2xl p-5 shadow-soft hover:shadow-soft-md transition-all duration-200 ${style.borderTop}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider truncate mb-1">
            {title}
          </p>
          <div className="flex items-baseline gap-1.5 flex-wrap">
            <span className="text-2xl font-black tracking-tight text-slate-800 font-mono">
              {value}
            </span>
            {unit && <span className="text-xs text-slate-500 font-semibold">{unit}</span>}
          </div>
        </div>
        {Icon && (
          <div className={`p-2.5 rounded-xl flex-shrink-0 ${style.iconBg} shadow-soft-sm`}>
            <Icon className="w-5 h-5 stroke-[2.2]" />
          </div>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div className="truncate font-medium text-slate-600">{subtext}</div>
        {badge && <div className="ml-2 flex-shrink-0">{badge}</div>}
        {trend && (
          <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${trendPositive ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-rose-50 text-rose-700 border-rose-200'}`}>
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}
