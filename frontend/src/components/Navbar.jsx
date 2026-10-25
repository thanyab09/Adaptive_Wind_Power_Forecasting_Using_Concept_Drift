import React from 'react';
import { Wind, Database, LogOut, User, Sparkles } from 'lucide-react';

export default function Navbar({ health, datasetName, datasetMode, user, onLogout }) {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-6 py-3 flex items-center justify-between shadow-soft-sm">
      {/* Brand & Project Identity */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white shadow-soft">
          <Wind className="w-5 h-5 stroke-[2.2]" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-sm font-bold tracking-tight text-slate-900 font-sans">
              Wind Power Forecasting
            </h1>
            <span className="text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full uppercase tracking-wider">
              Concept Drift v1.0
            </span>
          </div>
          <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
            Panimalar Engineering College — Final-Year Project Demonstration
          </p>
        </div>
      </div>

      {/* Right Telemetry, User Badge & Logout */}
      <div className="flex items-center gap-3">
        {/* Dataset Mode Badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600">
          <Database className="w-3.5 h-3.5 text-sky-600" />
          <span className="text-slate-400 font-medium">Dataset:</span>
          <span className="font-semibold text-slate-700 truncate max-w-[180px]">
            {datasetName || 'Synthetic Farm (Seed 0)'}
          </span>
          <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
            datasetMode === 'uploaded' 
              ? 'bg-amber-100 text-amber-800 border border-amber-200' 
              : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
          }`}>
            {datasetMode || 'Synthetic'}
          </span>
        </div>

        {/* Backend Health Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-bold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>Connected</span>
        </div>

        {/* User Profile Pill & Logout */}
        {user && (
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-2xl bg-slate-50 border border-slate-200/90 shadow-soft-sm">
              <span className="text-base select-none">{user.avatar || '👤'}</span>
              <div className="text-left hidden lg:block">
                <span className="text-xs font-bold text-slate-800 block leading-tight">
                  {user.name}
                </span>
                <span className="text-[10px] text-slate-500 block leading-tight">
                  {user.role}
                </span>
              </div>
            </div>

            <button
              onClick={onLogout}
              title="Sign Out to Login Portal"
              className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 border border-slate-200/80 active:scale-95 transition-all"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
