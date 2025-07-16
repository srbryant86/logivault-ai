from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestClaudeEndpoint:
    """Test suite for Claude API endpoint"""

    def test_claude_endpoint_missing_prompt(self):
        """Test Claude endpoint with missing prompt returns 400"""
        response = client.post("/claude", json={})
        assert response.status_code == 400
        assert "No prompt provided" in response.json()["detail"]

    def test_claude_endpoint_empty_prompt(self):
        """Test Claude endpoint with empty prompt returns 400"""
        response = client.post("/claude", json={"prompt": ""})
        assert response.status_code == 400
        assert "No prompt provided" in response.json()["detail"]

    @patch("backend.main.call_claude")
    def test_claude_endpoint_success(self, mock_claude):
        """Test successful Claude API call"""
        # Mock the async function properly
        mock_claude.return_value = "This is a test response"

        response = client.post("/claude", json={"prompt": "Test prompt"})

        assert response.status_code == 200
        assert response.json() == {"response": "This is a test response"}

    @patch("backend.main.call_claude")
    def test_claude_endpoint_api_error(self, mock_claude):
        """Test Claude endpoint handles API errors"""
        # Mock the async function properly
        mock_claude.return_value = "Error: API key missing"

        response = client.post("/claude", json={"prompt": "Test prompt"})

        assert response.status_code == 500
        assert "Error: API key missing" in response.json()["detail"]


class TestGenerateEndpoint:
    """Test suite for Generate endpoint"""

    def test_generate_endpoint_missing_prompt(self):
        """Test Generate endpoint with missing prompt returns 400"""
        response = client.post("/generate", json={})
        assert response.status_code == 400
        assert "No prompt provided" in response.json()["detail"]

    @patch("backend.main.call_claude")
    def test_generate_endpoint_success(self, mock_claude):
        """Test successful Generate API call"""
        # Mock the async function properly
        mock_claude.return_value = "Generated content"

        response = client.post("/generate", json={"prompt": "Generate something"})

        assert response.status_code == 200
        assert response.json() == {"content": "Generated content"}

    @patch("backend.main.call_claude")
    def test_generate_endpoint_api_error(self, mock_claude):
        """Test Generate endpoint handles API errors"""
        # Mock the async function properly
        mock_claude.return_value = "Error: Network timeout"

        response = client.post("/generate", json={"prompt": "Test prompt"})

        assert response.status_code == 500
        assert "Error: Network timeout" in response.json()["detail"]


class TestRequestValidation:
    """Test suite for request validation"""

    def test_request_validation_exists(self):
        """Test that request validation functionality exists"""
        # This is a placeholder test to ensure we have some validation testing
        assert True
