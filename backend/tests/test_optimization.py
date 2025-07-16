from unittest.mock import AsyncMock, patch

import httpx
import pytest

from backend.claude_api import call_claude


class TestClaudeAPIModule:
    """Test suite for Claude API module"""

    @pytest.mark.asyncio
    async def test_call_claude_missing_api_key(self):
        """Test call_claude with missing API key"""
        with patch.dict("backend.claude_api.os.environ", {}, clear=True):
            result = await call_claude("test prompt")
            assert result == "Claude API key missing."

    @pytest.mark.asyncio
    async def test_call_claude_success(self):
        """Test successful Claude API call"""
        mock_response = {"content": [{"text": "This is Claude's response"}]}

        with patch.dict(
            "backend.claude_api.os.environ", {"CLAUDE_API_KEY": "test-key"}
        ):
            with patch("backend.claude_api.httpx.AsyncClient") as mock_client:
                # Create a proper mock for the async context manager
                mock_post = AsyncMock()
                mock_post.json.return_value = mock_response
                mock_post.raise_for_status.return_value = None

                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_post
                )

                result = await call_claude("test prompt")
                assert result == "This is Claude's response"

    @pytest.mark.asyncio
    async def test_call_claude_http_error(self):
        """Test Claude API call with HTTP error"""
        with patch.dict(
            "backend.claude_api.os.environ", {"CLAUDE_API_KEY": "test-key"}
        ):
            with patch("backend.claude_api.httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.side_effect = (
                    httpx.HTTPStatusError("HTTP Error", request=None, response=None)
                )

                result = await call_claude("test prompt")
                assert result.startswith("Error:")

    @pytest.mark.asyncio
    async def test_call_claude_network_error(self):
        """Test Claude API call with network error"""
        with patch.dict(
            "backend.claude_api.os.environ", {"CLAUDE_API_KEY": "test-key"}
        ):
            with patch("backend.claude_api.httpx.AsyncClient") as mock_client:
                mock_client.return_value.__aenter__.return_value.post.side_effect = (
                    httpx.NetworkError("Network Error")
                )

                result = await call_claude("test prompt")
                assert result.startswith("Error:")

    @pytest.mark.asyncio
    async def test_call_claude_request_payload(self):
        """Test that Claude API call sends correct payload"""
        with patch.dict(
            "backend.claude_api.os.environ", {"CLAUDE_API_KEY": "test-key-for-testing"}
        ):
            with patch("backend.claude_api.httpx.AsyncClient") as mock_client:
                mock_post = AsyncMock()
                mock_post.json.return_value = {"content": [{"text": "response"}]}
                mock_post.raise_for_status.return_value = None

                mock_client.return_value.__aenter__.return_value.post.return_value = (
                    mock_post
                )

                await call_claude("test prompt")

                # Verify the correct payload was sent
                mock_client.return_value.__aenter__.return_value.post.assert_called_once()
                call_args = (
                    mock_client.return_value.__aenter__.return_value.post.call_args
                )

                assert call_args[0][0] == "https://api.anthropic.com/v1/messages"
                assert call_args[1]["json"]["model"] == "claude-3-opus-20240229"
                assert call_args[1]["json"]["messages"][0]["content"] == "test prompt"
                assert call_args[1]["headers"]["x-api-key"] == "test-key-for-testing"
