import React, { useState } from 'react';
import {
  Wind,
  ShieldCheck,
  GraduationCap,
  Zap,
  Lock,
  Mail,
  ArrowRight,
  Sparkles,
  UserCheck,
} from 'lucide-react';

export default function LoginPage({ onLogin }) {
  const [role, setRole] = useState('examiner'); // 'examiner' or 'operator'
  const [email, setEmail] = useState('examiner@panimalar.edu.in');
  const [password, setPassword] = useState('viva2026');
  const [remember, setRemember] = useState(true);

  const handleRoleSelect = (selectedRole) => {
    setRole(selectedRole);
    if (selectedRole === 'examiner') {
      setEmail('examiner@panimalar.edu.in');
      setPassword('viva2026');
    } else {
      setEmail('operator@windpower.ai');
      setPassword('scada2026');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const user = {
      name: role === 'examiner' ? 'Dr. External Examiner' : 'SCADA Control Engineer',
      email: email,
      role: role === 'examiner' ? 'Academic Examiner' : 'Wind Farm Operator',
      institution: 'Panimalar Engineering College',
      avatar: role === 'examiner' ? '🎓' : '⚡',
      badgeColor: role === 'examiner' ? 'bg-purple-100 text-purple-800 border-purple-200' : 'bg-emerald-100 text-emerald-800 border-emerald-200',
    };
    onLogin(user);
  };

  const handleQuickDemo = () => {
    const user = {
      name: 'Dr. External Examiner',
      email: 'examiner@panimalar.edu.in',
      role: 'Academic Examiner',
      institution: 'Panimalar Engineering College',
      avatar: '🎓',
      badgeColor: 'bg-purple-100 text-purple-800 border-purple-200',
    };
    onLogin(user);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-teal-50/40 to-emerald-50 flex flex-col justify-between p-4 sm:p-6 font-sans">
      {/* Top Header Brand */}
      <header className="max-w-6xl mx-auto w-full flex items-center justify-between py-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white shadow-soft">
            <Wind className="w-5 h-5 stroke-[2.4]" />
          </div>
          <div>
            <span className="text-sm font-extrabold text-slate-800 tracking-tight block">
              Panimalar Engineering College
            </span>
            <span className="text-[11px] text-slate-500 font-medium block">
              Department of Artificial Intelligence & Machine Learning
            </span>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 border border-slate-200/80 shadow-soft-sm text-xs font-semibold text-slate-600">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>B.Tech Final-Year Capstone Portal</span>
        </div>
      </header>

      {/* Main Centered Login Card */}
      <main className="max-w-md w-full mx-auto my-6 animate-fade-in">
        <div className="bg-white/95 backdrop-blur-xl border border-slate-200/90 rounded-3xl p-7 sm:p-8 shadow-soft-lg">
          {/* Badge & Title */}
          <div className="text-center space-y-2 mb-6">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-[11px] font-bold uppercase tracking-wider shadow-soft-sm">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
              <span>SCADA Control Access</span>
            </div>
            <h1 className="text-2xl font-black tracking-tight text-slate-900">
              Wind Power Forecasting
            </h1>
            <p className="text-xs text-slate-500 max-w-xs mx-auto leading-relaxed">
              Adaptive 1-hour-ahead forecasting engine with real-time concept drift detection.
            </p>
          </div>

          {/* 1-Click Quick Demo Login Button */}
          <button
            type="button"
            onClick={handleQuickDemo}
            className="w-full mb-5 py-3 px-4 rounded-2xl bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-xs shadow-soft-md hover:shadow-soft-lg active:scale-98 transition-all flex items-center justify-center gap-2 group"
          >
            <Zap className="w-4 h-4 fill-current text-amber-200" />
            <span>⚡ 1-Click Quick Demo Access (Examiner)</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>

          <div className="flex items-center gap-3 my-5">
            <div className="flex-1 h-px bg-slate-200" />
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">or sign in</span>
            <div className="flex-1 h-px bg-slate-200" />
          </div>

          {/* Role Selector Tabs */}
          <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100/90 rounded-2xl mb-5 border border-slate-200/60">
            <button
              type="button"
              onClick={() => handleRoleSelect('examiner')}
              className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                role === 'examiner'
                  ? 'bg-white text-purple-900 shadow-soft border border-purple-100'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <GraduationCap className="w-3.5 h-3.5 text-purple-600" />
              <span>Examiner Role</span>
            </button>

            <button
              type="button"
              onClick={() => handleRoleSelect('operator')}
              className={`py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                role === 'operator'
                  ? 'bg-white text-emerald-900 shadow-soft border border-emerald-100'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Zap className="w-3.5 h-3.5 text-emerald-600" />
              <span>Operator Role</span>
            </button>
          </div>

          {/* Standard Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">
                Access ID / Email
              </label>
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full bg-slate-50 border border-slate-200/80 rounded-xl px-3.5 py-2.5 pl-9 text-xs font-medium text-slate-800 focus:outline-none focus:border-emerald-500 focus:bg-white focus:ring-2 focus:ring-emerald-100 transition-all"
                  placeholder="name@panimalar.edu.in"
                />
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">
                Security Password
              </label>
              <div className="relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full bg-slate-50 border border-slate-200/80 rounded-xl px-3.5 py-2.5 pl-9 text-xs font-medium text-slate-800 focus:outline-none focus:border-emerald-500 focus:bg-white focus:ring-2 focus:ring-emerald-100 transition-all"
                  placeholder="••••••••"
                />
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              </div>
            </div>

            <div className="flex items-center justify-between text-xs pt-1">
              <label className="flex items-center gap-2 cursor-pointer text-slate-600">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                  className="rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                />
                <span className="text-[11px]">Keep session active</span>
              </label>
              <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                Pre-authorized
              </span>
            </div>

            <button
              type="submit"
              className="w-full mt-2 py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-soft hover:shadow-soft-md active:scale-98 transition-all flex items-center justify-center gap-2"
            >
              <UserCheck className="w-4 h-4" />
              <span>Authorize & Enter Dashboard</span>
            </button>
          </form>
        </div>
      </main>

      {/* Academic Citation Footer */}
      <footer className="max-w-2xl mx-auto w-full text-center text-xs text-slate-500 py-3 space-y-1">
        <div className="font-semibold text-slate-700">
          Adaptive Wind Power Forecasting Using Concept Drift Detection
        </div>
        <div className="text-[11px] text-slate-500">
          Students: <strong className="text-slate-700">Thanya B</strong> (211423247227) & <strong className="text-slate-700">Thejessri S</strong> (211423247229)
        </div>
        <div className="text-[10px] text-emerald-700 font-medium">
          Supervisor: Mr. M. Ezhilvendhan | Department of AI & ML
        </div>
      </footer>
    </div>
  );
}
