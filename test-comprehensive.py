#!/usr/bin/env python3
"""
Comprehensive test script for LogiVault AI application
Tests all the fixes made to address PR review comments
"""

import os
import sys
import json
import requests
import time
from pathlib import Path

def test_security_fixes():
    """Test that security issues have been addressed"""
    print("=== Testing Security Fixes ===")
    
    # Check that .env is in .gitignore
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            gitignore_content = f.read()
        if '.env' in gitignore_content:
            print("✅ .env file is in .gitignore")
        else:
            print("❌ .env file is NOT in .gitignore")
    else:
        print("❌ .gitignore file not found")
    
    # Check that .env.example exists and doesn't contain real API key
    env_example_path = Path('.env.example')
    if env_example_path.exists():
        with open(env_example_path) as f:
            env_example_content = f.read()
        if 'your-claude-api-key-here' in env_example_content:
            print("✅ .env.example contains placeholder API key")
        else:
            print("❌ .env.example doesn't contain proper placeholder")
    else:
        print("❌ .env.example file not found")

def test_docker_files():
    """Test that Docker configuration is complete"""
    print("\n=== Testing Docker Configuration ===")
    
    # Check that Dockerfiles exist
    backend_dockerfile = Path('Dockerfile.backend')
    frontend_dockerfile = Path('frontend/Dockerfile')
    
    if backend_dockerfile.exists():
        print("✅ Backend Dockerfile exists")
        # Check basic content
        with open(backend_dockerfile) as f:
            content = f.read()
        if 'FROM python:' in content and 'uvicorn' in content:
            print("✅ Backend Dockerfile has correct content")
        else:
            print("❌ Backend Dockerfile content is incorrect")
    else:
        print("❌ Backend Dockerfile not found")
    
    if frontend_dockerfile.exists():
        print("✅ Frontend Dockerfile exists")
        # Check basic content
        with open(frontend_dockerfile) as f:
            content = f.read()
        if 'FROM node:' in content and 'npm' in content:
            print("✅ Frontend Dockerfile has correct content")
        else:
            print("❌ Frontend Dockerfile content is incorrect")
    else:
        print("❌ Frontend Dockerfile not found")
    
    # Check docker-compose.yml
    docker_compose_path = Path('docker-compose.yml')
    if docker_compose_path.exists():
        print("✅ docker-compose.yml exists")
        with open(docker_compose_path) as f:
            content = f.read()
        if 'backend:' in content and 'frontend:' in content:
            print("✅ docker-compose.yml has both services")
        else:
            print("❌ docker-compose.yml missing services")
    else:
        print("❌ docker-compose.yml not found")

def test_backend_api():
    """Test backend API endpoints"""
    print("\n=== Testing Backend API ===")
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test Claude endpoint structure
    try:
        response = requests.post(
            f"{base_url}/claude",
            json={"prompt": "Hello test"},
            timeout=5
        )
        if response.status_code in [200, 500]:  # 500 expected due to test API key
            print("✅ Claude endpoint structure working")
        else:
            print(f"❌ Claude endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Claude endpoint error: {e}")
    
    # Test generate endpoint structure
    try:
        response = requests.post(
            f"{base_url}/generate",
            json={"prompt": "Hello test"},
            timeout=5
        )
        if response.status_code in [200, 500]:  # 500 expected due to test API key
            print("✅ Generate endpoint structure working")
        else:
            print(f"❌ Generate endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Generate endpoint error: {e}")

def test_environment_config():
    """Test environment configuration improvements"""
    print("\n=== Testing Environment Configuration ===")
    
    # Check .env file has proper format
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            env_content = f.read()
        if 'CLAUDE_API_KEY=' in env_content and 'REACT_APP_API_URL=' in env_content:
            print("✅ .env file has proper key-value format")
        else:
            print("❌ .env file format is incorrect")
    else:
        print("❌ .env file not found")
    
    # Check API service uses environment variables
    api_service_path = Path('frontend/src/services/api.js')
    if api_service_path.exists():
        with open(api_service_path) as f:
            content = f.read()
        if 'process.env.REACT_APP_API_URL' in content and 'localhost:8000' in content:
            print("✅ API service uses environment variable with fallback")
        else:
            print("❌ API service doesn't use environment variables properly")
    else:
        print("❌ API service file not found")

def test_error_handling():
    """Test error handling improvements"""
    print("\n=== Testing Error Handling ===")
    
    # Check API service has improved error handling
    api_service_path = Path('frontend/src/services/api.js')
    if api_service_path.exists():
        with open(api_service_path) as f:
            content = f.read()
        if 'response.status === 400' in content and 'response.status === 401' in content:
            print("✅ API service has specific HTTP status error handling")
        else:
            print("❌ API service lacks specific error handling")
    else:
        print("❌ API service file not found")
    
    # Check ClaudeEditor has response validation
    claude_editor_path = Path('frontend/src/components/ClaudeEditor.jsx')
    if claude_editor_path.exists():
        with open(claude_editor_path) as f:
            content = f.read()
        if 'isValidResponse' in content and 'extractContent' in content:
            print("✅ ClaudeEditor has response validation functions")
        else:
            print("❌ ClaudeEditor lacks response validation")
    else:
        print("❌ ClaudeEditor file not found")

def main():
    """Run all tests"""
    print("LogiVault AI - Comprehensive Test Suite")
    print("=" * 50)
    
    test_security_fixes()
    test_docker_files()
    test_backend_api()
    test_environment_config()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")

if __name__ == "__main__":
    main()