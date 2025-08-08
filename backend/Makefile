.PHONY: help install setup dev test lint format clean docker-build docker-run docker-stop

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install Python dependencies
	pip install -r requirements.txt

setup: ## Setup development environment
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	npm install

dev: ## Start development server
	npm run dev

test: ## Run tests
	python3 -m pytest

lint: ## Lint code
	flake8 .

format: ## Format code
	black .

clean: ## Clean up
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -delete
	rm -rf venv
	rm -rf .pytest_cache
	rm -rf htmlcov

docker-build: ## Build Docker image
	docker build -t stock-analyst-backend .

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker Compose
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

health: ## Check service health
	curl http://localhost:5003/api/health
	curl http://localhost:5002/api/health

migrate: ## Run database migrations
	flask db upgrade

seed: ## Seed database with initial data
	python3 -c "from app.main import create_app; app = create_app(); app.app_context().push(); print('Database seeded')" 