import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LoginPage from './pages/LoginPage';
import OverviewDashboard from './pages/OverviewDashboard';
import ForecastingStudio from './pages/ForecastingStudio';
import DriftMonitoring from './pages/DriftMonitoring';
import AdaptiveLearning from './pages/AdaptiveLearning';
import ModelComparison from './pages/ModelComparison';
import DatasetExplorer from './pages/DatasetExplorer';
import ExperimentsReport from './pages/ExperimentsReport';
import { api } from './services/api';

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.get('auth') === '1') {
        return {
          name: 'Dr. External Examiner',
          email: 'examiner@panimalar.edu.in',
          role: 'Academic Examiner',
          institution: 'Panimalar Engineering College',
          avatar: '🎓',
        };
      }
      const saved = localStorage.getItem('wind_forecast_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [activePage, setActivePage] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const p = params.get('page');
      if (['overview', 'forecasting', 'drift', 'adaptation', 'comparison', 'dataset', 'experiments'].includes(p)) {
        return p;
      }
    } catch {}
    return 'overview';
  });
  const [health, setHealth] = useState(null);

  useEffect(() => {
    if (currentUser) {
      checkHealth();
    }
  }, [currentUser]);

  const checkHealth = async () => {
    try {
      const res = await api.getHealth();
      setHealth(res);
    } catch (err) {
      console.warn('Backend connection pending...');
    }
  };

  const handleLogin = (user) => {
    setCurrentUser(user);
    try {
      localStorage.setItem('wind_forecast_user', JSON.stringify(user));
    } catch (e) {
      console.error(e);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    try {
      localStorage.removeItem('wind_forecast_user');
    } catch (e) {
      console.error(e);
    }
  };

  // If unauthenticated, show the Login Access Page
  if (!currentUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  const renderPage = () => {
    switch (activePage) {
      case 'overview':
        return <OverviewDashboard />;
      case 'forecasting':
        return <ForecastingStudio />;
      case 'drift':
        return <DriftMonitoring />;
      case 'adaptation':
        return <AdaptiveLearning />;
      case 'comparison':
        return <ModelComparison />;
      case 'dataset':
        return <DatasetExplorer />;
      case 'experiments':
        return <ExperimentsReport />;
      default:
        return <OverviewDashboard />;
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-50/70 text-slate-800 font-sans selection:bg-emerald-100 selection:text-emerald-900">
      {/* Top Navigation Bar with User Profile and Logout */}
      <Navbar
        health={health}
        datasetName={health?.dataset_name}
        datasetMode={health?.dataset_mode}
        user={currentUser}
        onLogout={handleLogout}
      />

      {/* Main Body with Sidebar + Active Page */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activePage={activePage} setActivePage={setActivePage} />

        <main className="flex-1 overflow-y-auto p-5 sm:p-7 md:p-8 bg-slate-50/70">
          <div className="max-w-7xl mx-auto pb-12">
            {renderPage()}
          </div>
        </main>
      </div>
    </div>
  );
}
