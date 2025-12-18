.PHONY: help install install-dev test test-cov test-fast lint format type-check clean docker-build docker-test run

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make test-fast     - Run tests without coverage"
	@echo "  make lint          - Run linters (flake8, mypy)"
	@echo "  make format        - Format code (black, isort)"
	@echo "  make type-check    - Run type checker (mypy)"
	@echo "  make clean         - Clean temporary files"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-test   - Build and test Docker image"
	@echo "  make run           - Run the application"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest test_app.py -v --cov=app --cov=utils --cov-report=html --cov-report=term-missing

test-cov:
	pytest test_app.py -v --cov=app --cov=utils --cov-report=html --cov-report=xml --cov-report=term-missing

test-fast:
	pytest test_app.py -v --no-cov

test-specific:
	pytest test_app.py::$(TEST) -v

# Code quality
lint:
	flake8 app.py utils.py test_app.py --max-line-length=120 --extend-ignore=E501,W503,E203
	mypy app.py utils.py --ignore-missing-imports
	bandit -r app.py utils.py -f json -o bandit-report.json

format:
	black app.py utils.py test_app.py --line-length=120
	isort app.py utils.py test_app.py --profile black --line-length=120

format-check:
	black app.py utils.py test_app.py --line-length=120 --check
	isort app.py utils.py test_app.py --profile black --line-length=120 --check-only

type-check:
	mypy app.py utils.py --ignore-missing-imports --show-error-codes

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	rm -rf dist/ build/ *.egg-info

clean-all: clean
	rm -rf outputs/ temp/ venv/ .venv/

# Docker
docker-build:
	docker build -t text-to-video-app:latest .

docker-build-test:
	docker build --target test -t text-to-video-app:test .

docker-test: docker-build-test
	docker run --rm text-to-video-app:test pytest test_app.py -v

docker-run:
	docker run -p 7860:7860 --gpus all text-to-video-app:latest

# Run application
run:
	python app.py

run-dev:
	DEBUG_MODE=true python app.py

# Pre-commit
pre-commit:
	pre-commit run --all-files

# CI simulation
ci: format-check lint test-cov

# All checks before commit
check-all: format-check lint type-check test-fast
