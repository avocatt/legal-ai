.PHONY: help setup test lint clean build run docker-up docker-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Setup development environment
	./scripts/setup/setup_dev.sh

test: ## Run all tests
	@echo "Running backend tests..."
	cd backend && poetry run pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

lint: ## Run linters
	@echo "Linting backend..."
	cd backend && poetry run black . && poetry run isort . && poetry run flake8
	@echo "Linting frontend..."
	cd frontend && npm run lint

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +

build: ## Build all components
	@echo "Building backend..."
	cd backend && poetry install
	@echo "Building frontend..."
	cd frontend && npm install && npm run build

run: ## Run development servers
	@echo "Starting development servers..."
	docker-compose -f config/development/docker-compose.dev.yml up

docker-up: ## Start all Docker containers
	docker-compose -f config/development/docker-compose.dev.yml up -d

docker-down: ## Stop all Docker containers
	docker-compose -f config/development/docker-compose.dev.yml down
