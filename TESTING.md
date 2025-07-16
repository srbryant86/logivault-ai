# Testing Guide

This document describes the testing setup and procedures for the LogiVault AI project.

## Overview

The project includes comprehensive testing for both backend and frontend components:

- **Backend Tests**: Unit tests and integration tests for the FastAPI backend
- **Frontend Tests**: Component tests for the React frontend
- **CI/CD Pipeline**: Automated testing on every pull request and push

## Backend Testing

### Test Structure

- `backend/tests/test_demo.py`: Health endpoint and CORS configuration tests
- `backend/tests/test_api_endpoints.py`: API endpoint validation and functionality tests
- `backend/tests/test_integration.py`: Integration tests for the complete API
- `backend/tests/test_optimization.py`: Claude API module tests (some tests may be flaky due to external API calls)

### Running Backend Tests

```bash
# Run all backend tests
make test-backend

# Or directly with pytest
python -m pytest backend/tests/ -v --cov=backend --cov-report=term-missing

# Run specific test file
python -m pytest backend/tests/test_api_endpoints.py -v

# Run with coverage report
python -m pytest backend/tests/ --cov=backend --cov-report=html
```

### Test Coverage

Current backend test coverage focuses on:
- Health endpoint functionality
- API endpoint validation
- Error handling for missing/empty prompts
- CORS middleware configuration
- Application structure validation

## Frontend Testing

### Test Structure

- `frontend/src/App.test.js`: Main application component tests
- `frontend/src/components/Header.test.js`: Header component tests
- `frontend/src/components/ClaudeEditor.test.js`: Claude editor component tests

### Running Frontend Tests

```bash
# Run all frontend tests
make test-frontend

# Or directly with npm
cd frontend && npm test -- --watchAll=false --coverage
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Backend Tests**: Runs pytest with coverage reporting
2. **Frontend Tests**: Runs Jest tests with coverage
3. **Quality Checks**: Runs linting and formatting checks
4. **Build & Deploy**: Builds Docker images and runs integration tests

### Pipeline Jobs

- `backend-tests`: Runs backend tests and uploads coverage to Codecov
- `frontend-tests`: Runs frontend tests with coverage reporting
- `quality-checks`: Runs code formatting and linting checks
- `build-and-deploy`: Builds Docker images and runs integration tests

## Quality Checks

### Linting and Formatting

```bash
# Run all quality checks
make lint

# Format code
make format

# Individual tools
black backend/
isort backend/
flake8 backend/
```

## Test Dependencies

### Backend
- `pytest`: Testing framework
- `pytest-asyncio`: Async testing support
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `isort`: Import sorting
- `flake8`: Linting

### Frontend
- `@testing-library/react`: React component testing
- `@testing-library/jest-dom`: DOM testing utilities
- `jest`: JavaScript testing framework
- `jest-environment-jsdom`: DOM environment for Jest

## Best Practices

1. **Test Structure**: Follow the AAA pattern (Arrange, Act, Assert)
2. **Mocking**: Use mocks for external API calls to ensure tests are reliable
3. **Coverage**: Aim for high test coverage but focus on critical paths
4. **Naming**: Use descriptive test names that explain what is being tested
5. **Isolation**: Each test should be independent and not rely on others

## Running Tests Locally

1. Install dependencies:
   ```bash
   make install
   ```

2. Run all tests:
   ```bash
   make test
   ```

3. Run specific test suites:
   ```bash
   make test-backend
   make test-frontend
   ```

4. Check code quality:
   ```bash
   make lint
   ```

## Continuous Integration

Tests are automatically run on:
- Every pull request
- Every push to the main branch
- Manual workflow dispatch

The CI pipeline ensures that all tests pass before code can be merged to the main branch.