#!/usr/bin/env python3
"""
Test runner script for LogiVault AI project.
This script demonstrates the automated testing setup.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Run the test suite."""
    print("LogiVault AI - Automated Testing Demo")
    print("====================================")
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = True
    
    # Install dependencies
    success &= run_command(
        "pip install -r requirements.txt",
        "Installing backend dependencies"
    )
    
    # Run backend tests
    success &= run_command(
        "python -m pytest backend/tests/test_demo.py backend/tests/test_api_endpoints.py backend/tests/test_integration.py -v --cov=backend --cov-report=term-missing",
        "Running backend tests with coverage"
    )
    
    # Run linting checks
    success &= run_command(
        "flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics",
        "Running critical linting checks"
    )
    
    # Check if black would make changes
    run_command(
        "black --check backend/ || echo 'Code formatting issues found - run: black backend/'",
        "Checking code formatting"
    )
    
    # Check if isort would make changes
    run_command(
        "isort --check-only backend/ || echo 'Import sorting issues found - run: isort backend/'",
        "Checking import sorting"
    )
    
    print(f"\n{'='*60}")
    if success:
        print("✅ All tests passed successfully!")
        print("The automated testing setup is working correctly.")
    else:
        print("❌ Some tests failed.")
        print("Please check the output above for details.")
    print(f"{'='*60}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())