#!/usr/bin/env python3
"""
LogiVault AI - Render Deployment Fix v2
Comprehensive solution for Render deployment issues
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def create_minimal_requirements():
    """Create a minimal, working requirements.txt for Render"""
    requirements_content = """# LogiVault AI - Minimal Render Dependencies
fastapi==0.104.1
uvicorn==0.24.0
anthropic==0.7.8
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    print("✅ Created minimal requirements.txt")

def create_render_yaml():
    """Create optimized render.yaml configuration"""
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "logivault-ai-backend",
                "runtime": "python3",
                "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt",
                "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                "plan": "starter",
                "envVars": [
                    {"key": "PYTHON_VERSION", "value": "3.11"},
                    {"key": "PIP_NO_CACHE_DIR", "value": "1"}
                ]
            }
        ]
    }
    
    # Write as YAML format
    yaml_content = """services:
  - type: web
    name: logivault-ai-backend
    runtime: python3
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    plan: starter
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: PIP_NO_CACHE_DIR
        value: "1"
"""
    
    with open("render.yaml", "w") as f:
        f.write(yaml_content)
    print("✅ Created optimized render.yaml")

def create_dockerfile():
    """Create Dockerfile as backup deployment option"""
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created Dockerfile")

def update_main_py():
    """Ensure main.py has proper CORS configuration"""
    main_py_path = Path("backend/main.py")
    
    if main_py_path.exists():
        with open(main_py_path, "r") as f:
            content = f.read()
        
        # Check if CORS is properly configured
        if "logivault-ai.vercel.app" not in content:
            print("⚠️  CORS configuration may need updating in backend/main.py")
            print("   Make sure it includes: https://logivault-ai.vercel.app")
    else:
        print("❌ backend/main.py not found")

def create_start_script():
    """Create a startup script for Render"""
    start_script = """#!/bin/bash
# LogiVault AI Render Startup Script

echo "Starting LogiVault AI Backend..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Set environment variables
export PYTHONPATH="/opt/render/project/src:$PYTHONPATH"

# Start the application
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1
"""
    
    with open("start.sh", "w") as f:
        f.write(start_script)
    
    # Make executable
    os.chmod("start.sh", 0o755)
    print("✅ Created start.sh script")

def test_imports():
    """Test if all required packages can be imported"""
    test_script = """
import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import uvicorn
    print(f"✅ Uvicorn: {uvicorn.__version__}")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

try:
    import anthropic
    print(f"✅ Anthropic: {anthropic.__version__}")
except ImportError as e:
    print(f"❌ Anthropic import failed: {e}")

try:
    from backend.main import app
    print("✅ Backend main app imported successfully")
except ImportError as e:
    print(f"❌ Backend main import failed: {e}")
"""
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    print("✅ Created import test script")

def create_deployment_instructions():
    """Create step-by-step deployment instructions"""
    instructions = """# LogiVault AI - Render Deployment Instructions

## Quick Fix Steps:

1. **Commit these changes:**
   ```bash
   git add .
   git commit -m "Fix Render deployment configuration v2"
   git push origin main
   ```

2. **In Render Dashboard:**
   - Go to your logivault-ai service
   - Click "Settings" → "Build & Deploy"
   - Update Build Command to: `pip install --upgrade pip && pip install -r requirements.txt`
   - Update Start Command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Click "Save Changes"

3. **Set Environment Variables:**
   - Go to "Environment" tab
   - Add: `CLAUDE_API_KEY` = your_actual_claude_key
   - Add: `PYTHON_VERSION` = 3.11
   - Add: `PIP_NO_CACHE_DIR` = 1

4. **Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

## If Still Failing:

Try these alternative approaches:

### Option A: Use Dockerfile
- Render will automatically detect the Dockerfile
- This provides more control over the build environment

### Option B: Minimal Requirements
- The new requirements.txt has only essential packages
- Reduces chance of dependency conflicts

### Option C: Check Logs
- Look for specific error messages
- Common issues: missing system dependencies, Python version mismatch

## Testing:
After deployment, test the endpoint:
```bash
curl https://your-render-url.onrender.com/health
```

## Support:
If issues persist, check:
1. Python version compatibility
2. System dependencies
3. Environment variable configuration
4. CORS settings in backend/main.py
"""
    
    with open("RENDER_DEPLOYMENT_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    print("✅ Created deployment instructions")

def main():
    """Run all fixes"""
    print("🚀 LogiVault AI - Render Deployment Fix v2")
    print("=" * 50)
    
    try:
        create_minimal_requirements()
        create_render_yaml()
        create_dockerfile()
        create_start_script()
        test_imports()
        update_main_py()
        create_deployment_instructions()
        
        print("\n" + "=" * 50)
        print("✅ All fixes applied successfully!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Fix Render deployment v2'")
        print("3. git push origin main")
        print("4. Update Render settings as per RENDER_DEPLOYMENT_INSTRUCTIONS.md")
        print("5. Deploy on Render")
        
    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
