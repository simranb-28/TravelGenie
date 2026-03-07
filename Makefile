.PHONY: help docker-up docker-down docker-build docker-logs docker-clean setup test lint format

help:
	@echo "TravelGenie - Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-up       - Start all services with Docker Compose"
	@echo "  make docker-down     - Stop all services"
	@echo "  make docker-build    - Build Docker images"
	@echo "  make docker-logs     - View logs from all services"
	@echo "  make docker-clean    - Remove all containers and volumes"
	@echo ""
	@echo "Development Commands:"
	@echo "  make setup           - Set up development environment"
	@echo "  make test            - Run tests"
	@echo "  make lint            - Run linting checks"
	@echo "  make format          - Format code"
	@echo ""

# Docker commands
docker-up:
	@echo "Starting TravelGenie services..."
	docker-compose up

docker-up-detach:
	@echo "Starting TravelGenie services (background)..."
	docker-compose up -d

docker-down:
	@echo "Stopping TravelGenie services..."
	docker-compose down

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-logs:
	@echo "Showing logs from all services..."
	docker-compose logs -f

docker-logs-backend:
	docker-compose logs -f backend

docker-logs-frontend:
	docker-compose logs -f frontend

docker-logs-redis:
	docker-compose logs -f redis

docker-clean:
	@echo "Removing all containers and volumes..."
	docker-compose down -v
	@echo "Cleaned!"

# Development commands
setup:
	@echo "Setting up development environment..."
	cd travelgenie && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd travelgenie-frontend && npm install
	cp .env.example .env
	@echo "Setup complete! Fill in your API keys in .env"

test:
	@echo "Running tests..."
	cd travelgenie && pytest tests/ -v

test-coverage:
	@echo "Running tests with coverage..."
	cd travelgenie && pytest tests/ --cov=app --cov-report=html

lint:
	@echo "Running linters..."
	cd travelgenie && pylint app/
	cd travelgenie-frontend && npm run lint

format:
	@echo "Formatting code..."
	cd travelgenie && black app/ tests/
	cd travelgenie-frontend && npm run format

# Docker inspection
docker-ps:
	docker-compose ps

docker-shell-backend:
	docker-compose exec backend /bin/bash

docker-shell-frontend:
	docker-compose exec frontend /bin/sh

# Health check
health-check:
	@echo "Checking service health..."
	@echo "Backend: " && curl -s http://localhost:8000/health || echo "Backend not responding"
	@echo "Frontend: " && curl -s http://localhost:5173 | head -n 1 || echo "Frontend not responding"
	@echo "Redis: " && redis-cli -p 6379 ping || echo "Redis not responding"
