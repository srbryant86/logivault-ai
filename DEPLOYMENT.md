# LogiVault AI Deployment Configuration

## Backend Deployment (Render)

The backend is configured to deploy on Render with the following setup:

### Environment Variables Required:
- `CLAUDE_API_KEY`: Your Claude API key from Anthropic

### Render Configuration:
- **Runtime**: Python 3.12
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
- **Service Type**: Web Service

### Configuration Files:
- `render.yaml`: Render service configuration
- `requirements.txt`: Python dependencies including `fastapi-cors`
- `.render-python-version`: Python version specification

## Frontend Deployment (Vercel)

The frontend is configured to deploy on Vercel with the following setup:

### Environment Variables Required:
- `REACT_APP_API_URL`: Backend API URL (should be set to your Render service URL)

### Vercel Configuration:
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Node Version**: Auto-detected from package.json

### Configuration Files:
- `vercel.json`: Vercel deployment configuration
- `frontend/.env.local`: Local development environment variables

## Integration Features

### CORS Configuration
The backend includes CORS middleware that allows requests from:
- `https://logivault-ai.vercel.app`
- `https://logivault-ai-*.vercel.app` (for preview deployments)
- `http://localhost:3000` (local development)

### API Endpoints
- `/healthz` - Health check endpoint
- `/generate` - Main endpoint for Claude AI generation (matches frontend expectations)
- `/claude` - Legacy endpoint (maintained for backward compatibility)

### Response Format
The `/generate` endpoint returns responses in the format expected by the frontend:
```json
{
  "content": "Generated response text"
}
```

### Error Handling
- Proper HTTP status codes (400 for bad requests, 500 for server errors)
- Detailed error messages in `detail` field
- Retry logic in frontend with exponential backoff

## Local Development

### Backend:
```bash
cd /home/runner/work/logivault-ai/logivault-ai
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

### Environment Variables:
- Copy `.env` to include your `CLAUDE_API_KEY`
- Frontend will use `REACT_APP_API_URL=http://localhost:8000` for local development

## Deployment URLs

### Production:
- Frontend: `https://logivault-ai.vercel.app`
- Backend: `https://logivault-api.onrender.com`

### Integration Test:
Run the integration test to verify the complete setup:
```bash
python /tmp/integration_test.py
```