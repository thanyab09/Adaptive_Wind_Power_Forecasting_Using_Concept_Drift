/** API service client for communicating with the FastAPI backend */

const API_BASE = '/api';

async function fetchJSON(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  try {
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        ...(options.headers || {})
      },
      ...options,
    });

    if (!response.ok) {
      let errorMsg = `Server error ${response.status}: ${response.statusText}`;
      try {
        const errData = await response.json();
        if (errData && errData.detail) {
          errorMsg = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
        }
      } catch (e) {
        // use default errorMsg
      }
      throw new Error(errorMsg);
    }

    return await response.json();
  } catch (err) {
    console.error(`API Error on ${url}:`, err);
    throw err;
  }
}

export const api = {
  // System Health
  getHealth: () => fetchJSON('/health'),

  // Page 1: Overview Dashboard
  getDashboardSummary: () => fetchJSON('/dashboard/summary'),

  // Page 2 & 6: Data & Dataset Explorer
  generateSyntheticData: (seed = 0, drift = true, magnitude = 1.0) =>
    fetchJSON('/data/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ seed, drift, magnitude }),
    }),

  uploadDatasetCSV: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/data/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Failed to upload CSV dataset.');
    }
    return await response.json();
  },

  getDatasetPreview: () => fetchJSON('/data/preview'),
  getDownloadDatasetUrl: () => `${API_BASE}/data/download`,

  // Page 2: Forecasting Studio
  predictForecast: (payload) =>
    fetchJSON('/forecast/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }),

  getForecastHistory: () => fetchJSON('/forecast/history'),

  trainBaseModel: () =>
    fetchJSON('/forecast/train', {
      method: 'POST',
    }),

  // Page 3: Drift Monitoring
  getDriftStatus: () => fetchJSON('/drift/status'),
  getDriftEvents: () => fetchJSON('/drift/events'),
  getDriftTrace: () => fetchJSON('/drift/trace'),

  simulateStep: (hours = 24) =>
    fetchJSON('/drift/simulate_step', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hours }),
    }),

  simulateReset: () =>
    fetchJSON('/drift/simulate_reset', {
      method: 'POST',
    }),

  // Page 4: Adaptive Learning
  getAdaptationStatus: () => fetchJSON('/adaptation/status'),
  getRetrainingHistory: () => fetchJSON('/adaptation/history'),
  getWeightsCurve: () => fetchJSON('/adaptation/weights_curve'),

  triggerManualRetrain: (reason = 'Manual operator demonstration') =>
    fetchJSON('/adaptation/retrain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason }),
    }),

  // Page 5: Model Comparison
  getModelComparison: (scenario = 'drift') => fetchJSON(`/model/comparison?scenario=${scenario}`),

  // Page 7: Experiments & Reports
  runExperiment: (seed = 0, drift = true, magnitude = 1.0, detector = 'ph') =>
    fetchJSON('/experiments/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ seed, drift, magnitude, detector }),
    }),

  getExperimentStatus: (jobId) => fetchJSON(`/experiments/status/${jobId}`),
  getBenchmarkResults: (scenario = 'drift') => fetchJSON(`/experiments/benchmark?scenario=${scenario}`),
  getSensitivityAnalysis: () => fetchJSON('/experiments/sensitivity'),

  getDownloadReportPdfUrl: () => `${API_BASE}/reports/pdf`,
  getDownloadReportJsonUrl: () => `${API_BASE}/reports/json`,
  getDownloadReportCsvUrl: () => `${API_BASE}/reports/csv`,
};
