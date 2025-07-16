#!/bin/bash
# LogiVault AI Render Startup Script

echo "Starting LogiVault AI Backend..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Set environment variables
export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"

# Start the application
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1
