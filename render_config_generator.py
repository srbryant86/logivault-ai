#!/usr/bin/env python3
"""
LogiVault AI - Render Configuration Generator
Generates optimized configuration files for Render deployment
"""

import json
import os
from pathlib import Path

class RenderConfigGenerator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.configs_created = []
    
    def generate_optimized_requirements(self):
        """Generate optimized requirements.txt specifically for Render"""
        requirements = [
            "# LogiVault AI - Render Optimized Dependencies",
            "# Core FastAPI stack",
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "",
            "# AI/ML dependencies", 
            "anthropic==0.7.8",
            "",
            "# Web framework dependencies",
            "python-multipart==0.0.6",
            "pydantic==2.5.0",
            "python-dotenv==1.0.0",
            "",
            "# HTTP and async support",
            "requests==2.31.0",
            "aiofiles==23.2.1",
            "httpx==0.25.2",
            "",
            "# Build tools (helps with Render deployment)",
            "setuptools>=65.0.0",
            "wheel>=0.38.0",
            ""
        ]
        
        requirements_path = self.project_root / "requirements.txt"
        with open(requirements_path, 'w') as f:
            f.write('\n'.join(requirements))
        
        self.configs_created.append("requirements.txt")
        return requirements_path
    
    def generate_render_yaml(self):
        """Generate render.yaml for Infrastructure as Code deployment"""
        config = {
            "services": [
                {
                    "type": "web",
                    "name": "logivault-ai-backend",
                    "runtime": "python3",
                    "buildCommand": "pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt",
                    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1",
                    "plan": "starter",
                    "envVars": [
                        {
                            "key": "PYTHON_VERSION", 
                            "value": "3.11.0"
                        },
                        {
                            "key": "PIP_DISABLE_PIP_VERSION_CHECK",
                            "value": "1"
                        },
                        {
                            "key": "PYTHONPATH",
                            "value": "/opt/render/project/src"
                        }
                    ]
                }
            ]
        }
        
        # Write as YAML format manually (avoiding yaml dependency)
        yaml_content = """services:
  - type: web
    name: logivault-ai-backend
    runtime: python3
    buildCommand: pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1
    plan: starter
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: PIP_DISABLE_PIP_VERSION_CHECK
        value: "1"
      - key: PYTHONPATH
        value: "/opt/render/project/src"
"""
        
        render_yaml_path = self.project_root / "render.yaml"
        with open(render_yaml_path, 'w') as f:
            f.write(yaml_content)
        
        self.configs_created.append("render.yaml")
        return render_yaml_path
    
    def generate_dockerfile(self):
        """Generate Dockerfile for containerized deployment option"""
        dockerfile_content = """# LogiVault AI - Production Dockerfile for Render
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port (Render will set PORT env var)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:$PORT/health || exit 1

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "1"]
"""
        
        dockerfile_path = self.project_root / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        self.configs_created.append("Dockerfile")
        return dockerfile_path
    
    def generate_startup_scripts(self):
        """Generate startup scripts for different deployment scenarios"""
        
        # Main startup script
        start_sh_content = """#!/bin/bash
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
exec uvicorn backend.main:app \\
    --host 0.0.0.0 \\
    --port $PORT \\
    --workers 1 \\
    --access-log \\
    --log-level info
"""
        
        start_path = self.project_root / "start.sh"
        with open(start_path, 'w') as f:
            f.write(start_sh_content)
        os.chmod(start_path, 0o755)
        
        # Development startup script
        start_dev_content = """#!/bin/bash
# LogiVault AI - Development Startup Script

echo "🔧 Starting LogiVault AI Backend in Development Mode..."

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PORT=${PORT:-8000}

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start with hot reload
uvicorn backend.main:app \\
    --host 0.0.0.0 \\
    --port $PORT \\
    --reload \\
    --log-level debug
"""
        
        start_dev_path = self.project_root / "start-dev.sh"
        with open(start_dev_path, 'w') as f:
            f.write(start_dev_content)
        os.chmod(start_dev_path, 0o755)
        
        self.configs_created.extend(["start.sh", "start-dev.sh"])
        return [start_path, start_dev_path]
    
    def generate_environment_configs(self):
        """Generate environment configuration files"""
        
        # Render environment template
        render_env_content = """# LogiVault AI - Render Environment Variables
# Add these to your Render service environment variables

# Required: Your Claude API key
CLAUDE_API_KEY=your_claude_api_key_here

# Python configuration
PYTHON_VERSION=3.11.0
PYTHONPATH=/opt/render/project/src
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# Pip configuration
PIP_DISABLE_PIP_VERSION_CHECK=1

# Application configuration
PORT=8000
"""
        
        render_env_path = self.project_root / ".env.render"
        with open(render_env_path, 'w') as f:
            f.write(render_env_content)
        
        # Production environment template
        prod_env_content = """# LogiVault AI - Production Environment Template
# Copy and customize for your production deployment

CLAUDE_API_KEY=your_production_claude_api_key
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
"""
        
        prod_env_path = self.project_root / ".env.production"
        with open(prod_env_path, 'w') as f:
            f.write(prod_env_content)
        
        self.configs_created.extend([".env.render", ".env.production"])
        return [render_env_path, prod_env_path]
    
    def generate_deployment_instructions(self):
        """Generate step-by-step deployment instructions"""
        instructions = """# LogiVault AI - Render Deployment Instructions

## Automated Configuration Complete! 🎉

The following configuration files have been generated for your Render deployment:

### Generated Files:
- `requirements.txt` - Optimized Python dependencies
- `render.yaml` - Infrastructure as Code configuration
- `Dockerfile` - Container deployment option
- `start.sh` - Production startup script
- `start-dev.sh` - Development startup script
- `.env.render` - Environment variables template
- `.env.production` - Production environment template

## Deployment Steps:

### 1. Commit and Push Changes
```bash
git add .
git commit -m "Add optimized Render deployment configuration"
git push origin main
```

### 2. Configure Render Service

#### Option A: Using Render Dashboard
1. Go to your Render dashboard
2. Select your `logivault-ai` service
3. Go to Settings → Build & Deploy
4. Update **Build Command**:
   ```
   pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
   ```
5. Update **Start Command**:
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1
   ```

#### Option B: Using render.yaml (Recommended)
1. Render will automatically detect the `render.yaml` file
2. It will use the optimized configuration automatically

### 3. Set Environment Variables
In your Render service settings, add:
- **CLAUDE_API_KEY**: Your actual Claude API key
- **PYTHON_VERSION**: 3.11.0 (optional, already in render.yaml)

### 4. Deploy
1. Click "Manual Deploy" → "Deploy latest commit"
2. Monitor the build logs for any issues
3. The deployment should complete successfully

## Troubleshooting

### If Build Still Fails:
1. Check the build logs for specific error messages
2. Try the Dockerfile deployment option
3. Ensure all environment variables are set correctly

### If App Doesn't Start:
1. Check that CLAUDE_API_KEY is set
2. Verify the start command is correct
3. Check application logs for runtime errors

## Testing Your Deployment

Once deployed, test your backend:
1. Visit your Render service URL
2. Check `/docs` endpoint for API documentation
3. Test a simple API call to verify functionality

## Support

If you encounter issues:
1. Check the generated `RENDER_FIX_REPORT.json` for details
2. Review Render's deployment logs
3. Ensure all configuration files are committed to your repository

---
Generated by LogiVault AI Automated Deployment System
"""
        
        instructions_path = self.project_root / "RENDER_DEPLOYMENT.md"
        with open(instructions_path, 'w') as f:
            f.write(instructions)
        
        self.configs_created.append("RENDER_DEPLOYMENT.md")
        return instructions_path
    
    def generate_all_configs(self):
        """Generate all configuration files"""
        print("🔧 Generating Render deployment configurations...")
        
        try:
            self.generate_optimized_requirements()
            self.generate_render_yaml()
            self.generate_dockerfile()
            self.generate_startup_scripts()
            self.generate_environment_configs()
            self.generate_deployment_instructions()
            
            print(f"✅ Successfully generated {len(self.configs_created)} configuration files:")
            for config in self.configs_created:
                print(f"  • {config}")
            
            return True
        except Exception as e:
            print(f"❌ Error generating configurations: {e}")
            return False

if __name__ == "__main__":
    generator = RenderConfigGenerator()
    generator.generate_all_configs()

