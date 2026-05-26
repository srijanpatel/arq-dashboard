# arq-dash

A modernized dashboard for [ARQ](https://github.com/samuelcolvin/arq) (async Redis job queue), built with FastAPI and Vue 3.

## Acknowledgements

This project is a fork of [ninoseki/arq-dashboard](https://github.com/ninoseki/arq-dashboard) and [ninoseki/arq-dashboard-frontend](https://github.com/ninoseki/arq-dashboard-frontend) by [@ninoseki](https://github.com/ninoseki). The original work provided the foundation — this repo combines both into a monorepo with a modernized stack.

## What changed from the original

- **Monorepo**: Backend and frontend now live in a single repository
- **Backend**: Python 3.11+, Pydantic v2, pydantic-settings, uv, hatchling, ruff
- **Frontend**: Vue 3.5+ with `<script setup>`, Vite 6, TypeScript 5, Vitest, ESLint 9 flat config
- **Removed dependencies**: `async-cache`, `arrow`, `vue-concurrency`, `regenerator-runtime` — replaced with lightweight alternatives or stdlib

## Project structure

```
arq-dash/
├── backend/           # FastAPI backend (Python)
│   ├── arq_dashboard/ # Application package
│   └── tests/         # pytest test suite
├── frontend/          # Vue 3 SPA (TypeScript)
│   ├── src/           # Application source
│   └── tests/         # Vitest test suite
└── Makefile           # Dev commands
```

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Redis
- [uv](https://docs.astral.sh/uv/)

### Install dependencies

```bash
make install
```

### Development

Run the backend and frontend dev servers in separate terminals:

```bash
make dev-backend   # http://localhost:8000
make dev-frontend  # http://localhost:5173 (proxies API to backend)
```

### Build for production

```bash
make build-frontend  # Builds frontend into backend/arq_dashboard/frontend/
```

Then run the backend — it serves the built frontend as static files:

```bash
cd backend && uv run uvicorn arq_dashboard:app
```

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ARQ_DASHBOARD_REDIS_URL` | `redis://localhost:6379` | Redis connection URL |
| `ARQ_DASHBOARD_DEBUG` | `false` | Debug mode |
| `ARQ_DASHBOARD_LOG_LEVEL` | `DEBUG` | Log level |
| `ARQ_DASHBOARD_CACHE_TTL` | `60` | API cache TTL in seconds |

See `.env.example` for the full list.

### Testing

```bash
make test           # Run all tests
make test-backend   # Backend only (requires Redis)
make test-frontend  # Frontend only
```

### Linting

```bash
make lint    # Check all
make format  # Auto-fix all
```

## License

MIT — see the original [LICENSE](https://github.com/ninoseki/arq-dashboard/blob/main/LICENSE).
