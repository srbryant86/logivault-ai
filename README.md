# LogiVault AI

LogiVault AI is an AI-powered logging and analysis tool that provides intelligent insights into your application logs using Claude AI.

## Features

- **AI-Powered Analysis**: Leverage Claude AI to analyze logs and provide intelligent insights
- **Real-time Processing**: Process logs in real-time with rate limiting and queue management
- **Web Interface**: Clean, responsive web interface for easy interaction
- **RESTful API**: Backend API for integration with other systems
- **Health Monitoring**: Built-in health checks and monitoring endpoints

## Architecture

- **Backend**: Python FastAPI server with Claude AI integration
- **Frontend**: React.js web application
- **API**: RESTful API with rate limiting and error handling

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Claude AI API key from Anthropic

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/srbryant86/logivault-ai.git
cd logivault-ai
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Claude API key:
# CLAUDE_API_KEY=your-api-key-here
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
CLAUDE_API_KEY=your-claude-api-key-here
```

To get a Claude API key:
1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Create a new API key
3. Add it to your `.env` file

## Usage

### Running the Application

#### Option 1: Using the Start Script

```bash
# Start the backend server
chmod +x start.sh
./start.sh
```

#### Option 2: Manual Start

```bash
# Terminal 1: Start the backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start the frontend (in development mode)
cd frontend
npm start
```

### API Endpoints

- `GET /` - Health check endpoint
- `GET /healthz` - Health status endpoint  
- `POST /claude` - Send prompts to Claude AI

#### Example API Usage

```bash
# Test the health endpoint
curl http://localhost:8000/healthz

# Send a prompt to Claude
curl -X POST http://localhost:8000/claude \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze this log entry: ERROR - Database connection failed"}'
```

### Web Interface

Once both servers are running:
1. Open your browser to `http://localhost:3000` (frontend)
2. The frontend will proxy API requests to the backend at `http://localhost:8000`
3. Enter your prompts in the text area and click "Send"

## Development

### Backend Development

```bash
cd backend
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Features

### Rate Limiting
- Token bucket algorithm with 5 tokens per IP
- Refill rate: 1 token per 5 seconds
- Prevents API abuse and controls costs

### Error Handling
- Comprehensive error handling for API failures
- Exponential backoff for retries
- User-friendly error messages

### CORS Support
- Configured for cross-origin requests
- Supports all origins in development

## Deployment

### Production Deployment

The application is configured for deployment on platforms like:
- **Render**: See `render.yaml` for configuration
- **Vercel**: Frontend deployment configuration in `vercel.json`
- **Docker**: Docker configuration available

### Environment Configuration

For production deployment, ensure:
1. Set `CLAUDE_API_KEY` in your environment
2. Configure proper CORS origins
3. Set up proper SSL/TLS certificates
4. Configure rate limiting for your use case

## Troubleshooting

### Common Issues

1. **"Claude API key not configured"**
   - Ensure your `.env` file has the correct `CLAUDE_API_KEY`
   - Check that the `.env` file is in the root directory

2. **Network errors**
   - Verify your internet connection
   - Check if the Claude API is accessible from your network

3. **Rate limiting errors**
   - Wait for the rate limit to reset (5 seconds per token)
   - Consider implementing user authentication for higher limits

4. **Frontend not loading**
   - Ensure Node.js dependencies are installed (`npm install`)
   - Check that the backend is running on port 8000

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the API documentation

---

**Note**: This application uses the Claude AI API which requires an API key and may incur costs based on usage. Please review Anthropic's pricing and usage policies.
