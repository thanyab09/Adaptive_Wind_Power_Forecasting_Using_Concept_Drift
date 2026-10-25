/** Number and string formatters for wind power metrics */

export function formatKW(val, decimals = 1) {
  if (val === null || val === undefined || isNaN(val)) return '— kW';
  return `${Number(val).toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })} kW`;
}

export function formatPct(val, decimals = 1) {
  if (val === null || val === undefined || isNaN(val)) return '— %';
  return `${Number(val).toFixed(decimals)}%`;
}

export function formatSpeed(val, decimals = 2) {
  if (val === null || val === undefined || isNaN(val)) return '— m/s';
  return `${Number(val).toFixed(decimals)} m/s`;
}

export function formatHours(val, decimals = 1) {
  if (val === null || val === undefined || isNaN(val)) return '— h';
  return `${Number(val).toFixed(decimals)} h`;
}

export function formatSeconds(val, decimals = 2) {
  if (val === null || val === undefined || isNaN(val)) return '— s';
  return `${Number(val).toFixed(decimals)} s`;
}

export function formatNumber(val, decimals = 1) {
  if (val === null || val === undefined || isNaN(val)) return '—';
  return Number(val).toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}
