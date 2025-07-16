#!/bin/bash
# LogiVault AI - Development Startup Script

echo "🔧 Starting LogiVault AI Backend in Development Mode..."

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PORT=${PORT:-8000}

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start with hot reload
uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --reload \
    --log-level debug
