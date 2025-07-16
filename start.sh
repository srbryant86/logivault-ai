#!/bin/bash
# LogiVault AI - Render Startup Script

set -e

echo "🚀 Starting LogiVault AI Backend on Render..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Validate required environment variables
if [ -z "$CLAUDE_API_KEY" ]; then
    echo "❌ Error: CLAUDE_API_KEY environment variable is required"
    exit 1
fi

# Set default port if not provided
export PORT=${PORT:-8000}

echo "✅ Environment configured"
echo "📡 Starting server on port $PORT"

# Start the application with proper error handling
exec uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --access-log \
    --log-level info
