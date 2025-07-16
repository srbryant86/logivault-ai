import os
import sys
from pathlib import Path

import pytest

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up test environment
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("CLAUDE_API_KEY", "test-key-for-testing")


@pytest.fixture
def mock_claude_api_key():
    """Mock Claude API key for testing"""
    return "test-key-for-testing"
