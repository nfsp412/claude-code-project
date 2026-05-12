/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'dx-page': '#0A0E1A',
        'dx-navbar': '#111827',
        'dx-sidebar': '#0C1222',
        'dx-card': '#1A2236',
        'dx-card-hover': '#1E293B',
        'dx-input': '#131B2B',
        'dx-accent': '#06B6D4',
        'dx-accent-secondary': '#3B82F6',
        'dx-text-primary': '#E2E8F0',
        'dx-text-secondary': '#94A3B8',
        'dx-text-muted': '#64748B',
        'dx-border': '#1E293B',
        'dx-border-active': '#06B6D4',
        'dx-success': '#10B981',
        'dx-warning': '#F59E0B',
        'dx-danger': '#EF4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.6875rem', { lineHeight: '1rem' }],
      },
    },
  },
  plugins: [],
};
