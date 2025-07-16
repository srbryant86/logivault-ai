# LogiVault AI Backend Deployment Guide

## Render Deployment

### Option 1: Automatic Deployment (Recommended)
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - **Name**: logivault-ai-backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/healthz`

### Option 2: Manual Deployment
1. Push your code to GitHub
2. In Render dashboard, create new Web Service
3. Connect to your GitHub repository
4. Configure environment variables:
   - `CLAUDE_API_KEY`: Your Claude API key
   - `PYTHON_VERSION`: 3.11.0

### Environment Variables Required
- `CLAUDE_API_KEY`: Your Anthropic Claude API key
- `PORT`: Automatically set by Render

### Testing Deployment
After deployment, test these endpoints:
- Health check: `https://your-app.onrender.com/healthz`
- API endpoint: `https://your-app.onrender.com/generate` (POST)

## Alternative: Docker Deployment
If you prefer Docker:
1. Build: `docker build -t logivault-ai-backend .`
2. Run: `docker run -p 8000:8000 -e CLAUDE_API_KEY=your_key logivault-ai-backend`

## Troubleshooting
- Check logs in Render dashboard
- Ensure all environment variables are set
- Verify Python version compatibility
- Test health endpoint first
