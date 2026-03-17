# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JSON Formatter - a full-stack web application for formatting, minifying, validating, and analyzing JSON.

## Tech Stack

- **Frontend**: Vue 3 + TypeScript + Vite + Pinia + Element Plus
- **Backend**: FastAPI (Python 3.13+)
- **Package Manager**: npm (frontend), uv (backend)

## Development Commands

### Frontend (`json-parser/frontend/`)

```bash
npm run dev      # Start dev server (port 5173)
npm run build    # Type-check and build
npm run preview  # Preview production build
```

### Backend (`json-parser/backend/`)

```bash
uv run uvicorn app.main:app --reload  # Start dev server (port 8000)
```

### Running Tests

```bash
# Backend tests (from json-parser/backend/)
python -m unittest discover tests/

# Run single test file
python -m unittest tests/test_json_utils.py
python -m unittest tests/test_api_json.py
```

## Architecture

```
json-parser/
├── frontend/           # Vue 3 SPA
│   ├── src/
│   │   ├── api/        # API client (axios)
│   │   ├── components/ # Vue components
│   │   ├── constants/  # App constants
│   │   ├── data/       # Sample JSON data
│   │   ├── types/      # TypeScript types
│   │   └── assets/     # CSS styles
│   └── vite.config.ts  # Path alias: @ -> src/
│
└── backend/            # FastAPI service
    └── app/
        ├── api/        # API route handlers
        └── utils/      # JSON utility functions
```

## API Endpoints

All endpoints under `/api/json/`:
- `POST /format` - Format JSON with indentation (1-8 spaces)
- `POST /minify` - Minify JSON
- `POST /validate` - Validate JSON (returns `{valid, error}`)
- `POST /size` - Get JSON size in bytes
- `POST /lines` - Get line count

Health check: `GET /health`

## Key Conventions

- Frontend uses `@` alias for `src/` imports
- Backend uses `app/` as the main package
- CORS configured for `localhost:5173` (Vite) and `localhost:3000`
- Backend uses Python's built-in `json` module for all operations
- Frontend state is reactive (no Pinia stores currently used)
