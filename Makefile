.PHONY: help install dev build test lint

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	cd backend && uv sync --all-extras
	cd frontend && npm install

dev-backend: ## Run backend dev server
	cd backend && uv run uvicorn arq_dashboard:app --reload --port 8000

dev-frontend: ## Run frontend dev server
	cd frontend && npm run dev

build-frontend: ## Build frontend into backend static dir
	cd frontend && npm run build

test-backend: ## Run backend tests
	cd backend && uv run pytest tests/ -v

test-frontend: ## Run frontend tests
	cd frontend && npm test

test: test-backend test-frontend ## Run all tests

lint-backend: ## Lint backend code
	cd backend && uv run ruff check . && uv run ruff format --check .

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

lint: lint-backend lint-frontend ## Lint all code

format: ## Format all code
	cd backend && uv run ruff format . && uv run ruff check --fix .
	cd frontend && npm run lint:fix
