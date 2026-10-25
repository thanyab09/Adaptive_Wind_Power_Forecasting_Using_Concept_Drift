import React from 'react';
import { Play, StepForward, RotateCcw, FastForward, Clock } from 'lucide-react';

export default function PlaybackControls({
  currentHour,
  currentWeek,
  onStep,
  onReset,
  loading = false,
}) {
  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl p-4 shadow-soft flex flex-wrap items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-sky-50 text-sky-700 border border-sky-200/70">
          <Clock className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] text-slate-400 font-bold uppercase tracking-wider">Stream Position</div>
          <div className="flex items-baseline gap-2 mt-0.5">
            <span className="text-lg font-bold font-mono text-slate-800">Hour {currentHour?.toLocaleString()}</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Week {currentWeek}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2.5">
        <button
          onClick={() => onStep(1)}
          disabled={loading}
          className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-50 hover:bg-slate-100 active:scale-95 text-xs font-semibold text-slate-700 border border-slate-200 rounded-xl transition-all disabled:opacity-50 shadow-soft-sm"
        >
          <StepForward className="w-3.5 h-3.5 text-sky-600" />
          <span>Step 1h</span>
        </button>

        <button
          onClick={() => onStep(24)}
          disabled={loading}
          className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 active:scale-95 text-xs font-bold text-white rounded-xl shadow-soft transition-all disabled:opacity-50"
        >
          <FastForward className="w-4 h-4" />
          <span>Step 24h (1 Day)</span>
        </button>

        <button
          onClick={onReset}
          disabled={loading}
          title="Reset playback to initial stream hour (hour 4,368)"
          className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl border border-slate-200 transition-colors disabled:opacity-50"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
