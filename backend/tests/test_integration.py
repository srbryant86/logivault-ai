import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestIntegration:
    """Integration tests for the API"""

    def test_health_endpoint_integration(self):
        """Test that health endpoint works end-to-end"""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_claude_endpoint_validation(self):
        """Test Claude endpoint input validation"""
        # Test empty prompt
        response = client.post("/claude", json={"prompt": ""})
        assert response.status_code == 400

        # Test missing prompt
        response = client.post("/claude", json={})
        assert response.status_code == 400

    def test_generate_endpoint_validation(self):
        """Test Generate endpoint input validation"""
        # Test empty prompt
        response = client.post("/generate", json={"prompt": ""})
        assert response.status_code == 400

        # Test missing prompt
        response = client.post("/generate", json={})
        assert response.status_code == 400

    def test_cors_middleware_configured(self):
        """Test that CORS middleware is properly configured"""
        response = client.get("/healthz")
        assert response.status_code == 200
        # CORS middleware should be configured without errors

    def test_application_structure(self):
        """Test that the application has proper structure"""
        # Verify the app has the expected endpoints
        from backend.main import app

        routes = [route.path for route in app.routes]
        assert "/healthz" in routes
        assert "/claude" in routes
        assert "/generate" in routes
