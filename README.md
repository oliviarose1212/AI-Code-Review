# AI Code Review

One-line: AI-driven code review & developer productivity platform.

## What
MVP: GitHub-integrated automated analysis + LLM-generated fix suggestions and unit-test skeletons.

## Structure
- `backend/` — FastAPI, workers
- `frontend/` — Next.js dashboard
- `analyzers/` — language-specific analyzer containers
- `infra/` — docker-compose, infra config
- `docs/` — architecture, design docs

## Getting started (local)
1. Fill .env
2. docker-compose up -d
3. Start backend & worker

## License
MIT
