#!/bin/bash
# LogiVault AI Backend Startup Script for Render

echo "🚀 Starting LogiVault AI Backend on Render..."

# Set Python path
export PYTHONPATH="${PYTHONPATH}:."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start the application
echo "🌐 Starting FastAPI server..."
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
