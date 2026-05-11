# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A multi-project repository containing:

- **json-parser** — Full-stack JSON formatting/minifying/validation tool (Vue 3 + FastAPI)
- **next-app** — Next.js 16 analytics dashboard with Recharts for sales visualization
- **sales_analysis** — Python data analysis module (pandas/Streamlit) for sales metrics
- **pm** — Product management docs (PRD, API specifications)

## Development Commands

### json-parser — Frontend (`json-parser/frontend/`)

```bash
npm run dev          # Start Vite dev server (port 5173)
npm run build        # Type-check (vue-tsc) and build for production
npm run preview      # Preview production build
npm run lint         # ESLint with --fix
npm run lint:check   # ESLint without fix (CI)
npm run format       # Prettier write
npm run format:check # Prettier check (CI)
npm run type-check   # vue-tsc --noEmit
```

### json-parser — Backend (`json-parser/backend/`)

```bash
uv run uvicorn app.main:app --reload  # Start dev server (port 8000)
uv run python -m unittest discover tests/  # Run all tests
uv run python -m unittest tests/test_json_utils.py  # Single test file
```

Backend tests require `httpx` (included in the `dev` dependency group).

### next-app (`next-app/`)

```bash
npm run dev    # Start Next.js dev server (port 3000)
npm run build  # Production build
npm run lint   # ESLint
```

**IMPORTANT**: This project uses Next.js 16.2.1, which has breaking changes from earlier versions. When writing Next.js code, consult `next-app/node_modules/next/dist/docs/` for the correct APIs and conventions. See `next-app/AGENTS.md`.

### sales_analysis (`sales_analysis/`)

```bash
streamlit run dashboard.py   # Launch interactive analytics dashboard (port 8501)
pip install -r requirements.txt  # Install Streamlit dependencies
```

The module can also be imported directly:
```python
from sales_analysis.data_loader import SalesDataLoader
from sales_analysis.business_calc import SalesMetricsCalculator
```

## Architecture

```
json-parser/
├── frontend/              # Vue 3 SPA (Vite + TypeScript + Element Plus)
│   └── src/
│       ├── api/json.ts    # Axios API client
│       ├── components/    # Vue components (JsonFormatter.vue is the main one)
│       ├── constants/     # Theme constants
│       ├── data/          # Sample JSON data
│       └── types/         # TypeScript interfaces
└── backend/               # FastAPI service (Python >=3.12)
    └── app/
        ├── main.py        # App entry, CORS config, routers
        ├── api/json.py    # All /api/json/ endpoints
        └── utils/json_utils.py  # Core JSON operations

next-app/
└── app/
    ├── page.tsx           # Entry page → renders Dashboard
    ├── layout.tsx         # Root layout (Geist fonts)
    └── components/        # React components
        ├── Dashboard.tsx          # Main dashboard with cross-filtering
        ├── FilterSection.tsx      # Category/Region/Time period filters
        ├── MetricsCards.tsx       # KPI metric cards
        ├── SalesTrendChart.tsx    # Line chart
        ├── RevenuePieChart.tsx    # Pie chart
        ├── YoYGrowthChart.tsx     # Year-over-year bar chart
        ├── PerformanceChart.tsx   # Performance scatter/bubble chart
        └── data/sampleData.ts     # Sample sales dataset

sales_analysis/
├── data_loader.py         # SalesDataLoader: reads Excel, context manager support
├── business_calc.py       # SalesMetricsCalculator: KPIs, regional/product/customer metrics
├── dashboard.py           # Streamlit app with 8 analysis pages
└── sales_analysis.ipynb   # Jupyter notebook (analysis + visualization)
```

## API Endpoints (json-parser backend)

All endpoints under `/api/json/`:
- `POST /format` — Format JSON with indentation (1, 2, 4, 8, or "tab")
- `POST /minify` — Minify JSON (remove whitespace)
- `POST /validate` — Validate JSON (`{valid, error}`)
- `POST /size` — Get JSON size in bytes
- `POST /lines` — Get line count
- `POST /validate-columns` — DataX job config column order validator
- `GET /health` — Health check
- `GET /docs` — Auto-generated Swagger UI

## Key Conventions

- Frontend uses `@` alias for `src/` imports (configured in `vite.config.ts`)
- Backend uses Python's built-in `json` module for all JSON operations
- CORS allows `localhost:5173` (Vite) and `localhost:3000` (Next.js)
- Python package manager is `uv`; frontend uses `npm`
- Always use `uv run python` to execute Python scripts, never bare `python`
- Pinia is installed but not currently used — state is local/reactive
- `.claude/settings.json` has a PostToolUse hook on Read that plays a voice announcement
- Always don't run the server. i will start it by myself