#!/usr/bin/env python3
"""
LogiVault AI Render Deployment Automation
Automates backend deployment to Render
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class RenderDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"

    def log_info(self, message):
        print(f"ℹ️  {message}")

    def log_success(self, message):
        print(f"✅ {message}")

    def log_error(self, message):
        print(f"❌ {message}")

    def create_render_yaml(self):
        """Create render.yaml configuration"""
        self.log_info("Creating Render deployment configuration...")
        
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": "logivault-ai-backend",
                    "runtime": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                    "plan": "free",
                    "envVars": [
                        {
                            "key": "CLAUDE_API_KEY",
                            "sync": False
                        },
                        {
                            "key": "PYTHON_VERSION",
                            "value": "3.11.0"
                        }
                    ],
                    "healthCheckPath": "/healthz"
                }
            ]
        }

        try:
            render_path = self.project_root / "render.yaml"
            with open(render_path, 'w') as f:
                import yaml
                yaml.dump(render_config, f, default_flow_style=False)
            
            self.log_success("Created render.yaml configuration")
            return True

        except ImportError:
            # Fallback to JSON format if PyYAML not available
            try:
                with open(render_path, 'w') as f:
                    json.dump(render_config, f, indent=2)
                self.log_success("Created render.yaml configuration (JSON format)")
                return True
            except Exception as e:
                self.log_error(f"Failed to create render.yaml: {e}")
                return False

        except Exception as e:
            self.log_error(f"Failed to create render.yaml: {e}")
            return False

    def create_requirements_txt(self):
        """Create or update requirements.txt"""
        self.log_info("Creating requirements.txt...")
        
        requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
anthropic==0.7.8
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
"""
        
        try:
            req_path = self.project_root / "requirements.txt"
            with open(req_path, 'w') as f:
                f.write(requirements)
            
            self.log_success("Created requirements.txt")
            return True

        except Exception as e:
            self.log_error(f"Failed to create requirements.txt: {e}")
            return False

    def create_python_version_file(self):
        """Create Python version file for Render"""
        self.log_info("Creating Python version file...")
        
        try:
            version_path = self.project_root / ".python-version"
            with open(version_path, 'w') as f:
                f.write("3.11.0\n")
            
            self.log_success("Created .python-version file")
            return True

        except Exception as e:
            self.log_error(f"Failed to create .python-version: {e}")
            return False

    def create_startup_script(self):
        """Create startup script for Render"""
        self.log_info("Creating startup script...")
        
        startup_script = """#!/bin/bash
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
"""
        
        try:
            script_path = self.project_root / "start.sh"
            with open(script_path, 'w') as f:
                f.write(startup_script)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            self.log_success("Created start.sh script")
            return True

        except Exception as e:
            self.log_error(f"Failed to create startup script: {e}")
            return False

    def create_dockerfile(self):
        """Create Dockerfile for alternative deployment"""
        self.log_info("Creating Dockerfile...")
        
        dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/healthz || exit 1

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        try:
            dockerfile_path = self.project_root / "Dockerfile"
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile_content)
            
            self.log_success("Created Dockerfile")
            return True

        except Exception as e:
            self.log_error(f"Failed to create Dockerfile: {e}")
            return False

    def create_deployment_guide(self):
        """Create deployment guide"""
        self.log_info("Creating deployment guide...")
        
        guide_content = """# LogiVault AI Backend Deployment Guide

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
"""
        
        try:
            guide_path = self.project_root / "DEPLOYMENT.md"
            with open(guide_path, 'w') as f:
                f.write(guide_content)
            
            self.log_success("Created DEPLOYMENT.md guide")
            return True

        except Exception as e:
            self.log_error(f"Failed to create deployment guide: {e}")
            return False

    def run_setup(self):
        """Run all setup steps"""
        print("🚀 Setting up LogiVault AI Render Deployment...")
        print("=" * 50)
        
        steps = [
            ("Creating Render configuration", self.create_render_yaml),
            ("Creating requirements.txt", self.create_requirements_txt),
            ("Creating Python version file", self.create_python_version_file),
            ("Creating startup script", self.create_startup_script),
            ("Creating Dockerfile", self.create_dockerfile),
            ("Creating deployment guide", self.create_deployment_guide)
        ]
        
        for step_name, step_func in steps:
            self.log_info(f"Step: {step_name}")
            if not step_func():
                self.log_error(f"Failed at step: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("✅ RENDER DEPLOYMENT SETUP COMPLETE")
        print("=" * 50)
        print("\n🎯 Next Steps:")
        print("   1. Push changes to GitHub")
        print("   2. Connect repository to Render")
        print("   3. Create Web Service with provided configuration")
        print("   4. Set CLAUDE_API_KEY environment variable")
        print("   5. Deploy and test /healthz endpoint")
        print("\n📖 See DEPLOYMENT.md for detailed instructions")
        
        return True

if __name__ == "__main__":
    deployer = RenderDeployer()
    success = deployer.run_setup()
    sys.exit(0 if success else 1)

