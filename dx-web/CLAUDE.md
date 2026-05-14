# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this subproject.

## Project Overview

**DataX 监控调度平台** — A DataX job monitoring & scheduling platform frontend built with Vue 3 + TypeScript + TailwindCSS. The project is in a prototyping phase: all views use hardcoded mock data, and the API layer is defined but not yet connected.

## Tech Stack

- **Framework**: Vue 3.4 (Composition API via `<script setup>`)
- **Language**: TypeScript 5.3 (strict mode)
- **Build**: Vite 5
- **Router**: Vue Router 4 (web history mode)
- **State**: Pinia 2
- **HTTP**: Axios 1.6
- **CSS**: TailwindCSS 3.4 (custom dark theme with `dx-` palette)
- **Charts**: ECharts 5 + vue-echarts 7
- **Lint/Format**: ESLint 8 + Prettier 3

No external UI component library — all UI elements are hand-built with Tailwind utility classes.

## Development Commands

```bash
cd dx-web/frontend

npm run dev          # Start Vite dev server (port 5174)
npm run build        # Type-check (vue-tsc --noEmit) + Vite build
npm run preview      # Preview production build
npm run lint         # ESLint with --fix
npm run lint:check   # ESLint without fix (CI)
npm run format       # Prettier write
npm run format:check # Prettier check (CI)
npm run type-check   # vue-tsc --noEmit only
```

## Directory Structure

```
dx-web/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts          # Vite config (port 5174, @ -> src alias)
│   ├── tsconfig.json
│   ├── tailwind.config.js      # Custom dx- dark theme palette
│   ├── postcss.config.js
│   ├── design-mockups/         # 10 static HTML prototypes
│   └── src/
│       ├── main.ts             # App entry: Pinia + Router + main.css
│       ├── App.vue             # Root: renders <AppLayout />
│       ├── assets/styles/main.css  # Tailwind directives + custom scrollbar
│       ├── api/index.ts        # Axios instance + dashboardApi/taskApi/healthApi
│       ├── router/index.ts     # 9 lazy-loaded routes, dynamic page titles
│       ├── stores/app.ts       # Pinia store: sidebar, menus, user info
│       ├── types/index.ts      # Shared TypeScript interfaces
│       ├── composables/
│       │   └── useEchartsTheme.ts  # Shared ECharts dark theme + color palette
│       ├── components/
│       │   ├── layout/         # AppLayout, AppNavbar, AppSidebar
│       │   ├── dashboard/      # MetricCard, TaskTrendChart, TaskStatusChart, RecentTasksTable
│       │   ├── charts/         # CpuTrendChart, MemoryRingChart
│       │   └── task/           # FieldCheckboxGrid
│       └── views/
│           ├── DashboardView.vue     # Metrics cards + charts + recent table
│           ├── TaskListView.vue      # Search/filter/sort/paginate + action menus
│           ├── TaskBuilderView.vue   # 4-step wizard: reader → writer → mapping → build
│           ├── ScheduleView.vue      # Schedule task config (Cron management)
│           ├── TaskRunDetailView.vue  # Task execution run history
│           ├── DataSourceView.vue    # Datasource CRUD + JDBC auto-fill + connection test
│           ├── LogQueryView.vue      # Log viewer with filtering + real-time tail
│           ├── ClusterView.vue       # Cluster node management
│           ├── ResourceView.vue      # CPU/memory resource monitoring
│           └── JsonToolView.vue      # JSON format/minify/validate tool
```

## Routes

| Path | Name | View | Title |
|------|------|------|-------|
| `/` | `dashboard` | DashboardView | 任务监控仪表盘 |
| `/tasks/list` | `task-list` | TaskListView | 任务明细列表 |
| `/tasks/builder` | `task-builder` | TaskBuilderView | 任务构建 |
| `/schedule` | `schedule-config` | ScheduleView | 调度任务配置 |
| `/schedule/run-detail` | `schedule-run-detail` | TaskRunDetailView | 任务运行明细 |
| `/datasource` | `datasource` | DataSourceView | 数据源管理 |
| `/logs` | `logs` | LogQueryView | 日志查询 |
| `/cluster` | `cluster` | ClusterView | DataX执行集群管理 |
| `/resource` | `resource` | ResourceView | 资源使用监控 |
| `/json-tool` | `json-tool` | JsonToolView | JSON格式化 |

## Design System (Tailwind `dx-` palette)

All colors use the `dx-` prefix. Theme is permanently dark (`<html class="dark">`).
Key tokens: `dx-page` (#0A0E1A), `dx-card` (#1A2236), `dx-input` (#131B2B), `dx-accent` (#06B6D4 cyan), `dx-accent-secondary` (#3B82F6 blue), `dx-success` (#10B981), `dx-warning` (#F59E0B), `dx-danger` (#EF4444).

Fonts: Inter (body), JetBrains Mono / Fira Code (monospace).

## Key Conventions

- All views use `<script setup lang="ts">` with Composition API
- Each view is self-contained in a single `.vue` file (template + script + styles)
- Imports use `@` alias for `src/` (e.g. `@/api/index`)
- All views currently use local mock data, not the API layer
- Charts are pure CSS (no Chart.js/ECharts dependency)
- UI is fully in Chinese (labels, placeholders, route titles, errors)
- The `design-mockups/` directory contains static HTML prototypes matching each view
- Always don't run the dev server — the user will start it manually
- use uv to run python files