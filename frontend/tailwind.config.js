/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pastel: {
          mint: {
            light: '#ECFDF5',
            subtle: '#D1FAE5',
            border: '#A7F3D0',
            text: '#065F46',
            primary: '#059669',
          },
          sky: {
            light: '#F0F9FF',
            subtle: '#E0F2FE',
            border: '#BAE6FD',
            text: '#075985',
            primary: '#0284C7',
          },
          peach: {
            light: '#FFFBEB',
            subtle: '#FEF3C7',
            border: '#FDE68A',
            text: '#92400E',
            primary: '#D97706',
          },
          rose: {
            light: '#FFF1F2',
            subtle: '#FFE4E6',
            border: '#FECDD3',
            text: '#9F1239',
            primary: '#E11D48',
          },
          lavender: {
            light: '#F5F3FF',
            subtle: '#EDE9FE',
            border: '#DDD6FE',
            text: '#5B21B6',
            primary: '#7C3AED',
          },
        },
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      boxShadow: {
        'soft-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.03)',
        'soft': '0 2px 8px -1px rgba(0, 0, 0, 0.05), 0 1px 3px -1px rgba(0, 0, 0, 0.03)',
        'soft-md': '0 4px 14px -2px rgba(0, 0, 0, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.04)',
        'soft-lg': '0 10px 25px -3px rgba(0, 0, 0, 0.07), 0 4px 10px -2px rgba(0, 0, 0, 0.03)',
      }
    },
  },
  plugins: [],
}
