import React from 'react';

export default function StatusBadge({ status, size = 'md' }) {
  const s = (status || 'stable').toLowerCase();

  let bg = 'bg-emerald-50 text-emerald-700 border-emerald-200/80';
  let dot = 'bg-emerald-500';
  let label = status || 'Stable';

  if (s.includes('drift') || s.includes('alarm') || s.includes('detected')) {
    bg = 'bg-rose-50 text-rose-700 border-rose-200/80';
    dot = 'bg-rose-500';
  } else if (s.includes('warn')) {
    bg = 'bg-amber-50 text-amber-800 border-amber-200/80';
    dot = 'bg-amber-500';
  }

  const padding = size === 'sm' ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-xs font-semibold';

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border shadow-soft-sm ${bg} ${padding}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />
      <span>{label}</span>
    </span>
  );
}
