.PHONY: install test test-backend test-frontend lint format clean help

help:
	@echo "Available commands:"
	@echo "  install       - Install all dependencies"
	@echo "  test          - Run all tests"
	@echo "  test-backend  - Run backend tests only"
	@echo "  test-frontend - Run frontend tests only"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code"
	@echo "  clean         - Clean temporary files"

install:
	pip install -r requirements.txt
	cd frontend && npm install

test: test-backend test-frontend

test-backend:
	python -m pytest backend/tests/ -v --cov=backend --cov-report=term-missing

test-frontend:
	cd frontend && npm test -- --watchAll=false --coverage

lint:
	flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 backend/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	black --check backend/
	isort --check-only backend/

format:
	black backend/
	isort backend/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml