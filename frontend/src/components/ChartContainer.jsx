import React from 'react';

export default function ChartContainer({
  title,
  subtitle,
  children,
  action,
  className = '',
  height = 'h-72',
}) {
  return (
    <div className={`bg-white border border-slate-200/80 rounded-2xl p-6 shadow-soft flex flex-col ${className}`}>
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-800 tracking-tight">{title}</h3>
          {subtitle && <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{subtitle}</p>}
        </div>
        {action && <div className="flex-shrink-0">{action}</div>}
      </div>
      <div className={`w-full ${height} flex-1 min-h-[180px]`}>
        {children}
      </div>
    </div>
  );
}
