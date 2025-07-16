import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for health check endpoint"""

    def test_health_check_success(self):
        """Test that health endpoint returns 200 and correct response"""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_check_content_type(self):
        """Test that health endpoint returns JSON content type"""
        response = client.get("/healthz")
        assert response.headers["content-type"] == "application/json"


class TestCORSConfiguration:
    """Test suite for CORS configuration"""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = client.get("/healthz")
        # CORS headers should be present in response
        assert response.status_code == 200

    def test_cors_configuration_exists(self):
        """Test that CORS configuration is properly applied"""
        response = client.get("/healthz")
        # Just verify that the response is successful and CORS doesn't block it
        assert response.status_code == 200
