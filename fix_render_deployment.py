#!/usr/bin/env python3
"""
LogiVault AI - Automated Render Deployment Fix
Resolves Python interpreter errors and optimizes build configuration
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class RenderDeploymentFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.fixes_applied = []
        self.errors = []
    
    def log_fix(self, message):
        """Log a successful fix"""
        print(f"✅ {message}")
        self.fixes_applied.append(message)
    
    def log_error(self, message):
        """Log an error"""
        print(f"❌ {message}")
        self.errors.append(message)
    
    def create_optimized_requirements(self):
        """Create optimized requirements.txt for Render"""
        try:
            requirements_content = """# LogiVault AI - Optimized for Render Deployment
fastapi==0.104.1
uvicorn[standard]==0.24.0
anthropic==0.7.8
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
aiofiles==23.2.1
"""
            
            requirements_path = self.project_root / "requirements.txt"
            with open(requirements_path, 'w') as f:
                f.write(requirements_content)
            
            self.log_fix("Created optimized requirements.txt for Render")
            return True
        except Exception as e:
            self.log_error(f"Failed to create requirements.txt: {e}")
            return False
    
    def create_render_yaml(self):
        """Create render.yaml configuration file"""
        try:
            render_config = {
                "services": [
                    {
                        "type": "web",
                        "name": "logivault-ai-backend",
                        "runtime": "python3",
                        "buildCommand": "pip install --upgrade pip setuptools wheel && pip install -r requirements.txt",
                        "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                        "envVars": [
                            {
                                "key": "PYTHON_VERSION",
                                "value": "3.11.0"
                            },
                            {
                                "key": "PIP_DISABLE_PIP_VERSION_CHECK",
                                "value": "1"
                            }
                        ]
                    }
                ]
            }
            
            render_yaml_path = self.project_root / "render.yaml"
            with open(render_yaml_path, 'w') as f:
                import yaml
                yaml.dump(render_config, f, default_flow_style=False)
            
            self.log_fix("Created render.yaml configuration")
            return True
        except ImportError:
            # Fallback without yaml library
            render_yaml_content = """services:
  - type: web
    name: logivault-ai-backend
    runtime: python3
    buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: PIP_DISABLE_PIP_VERSION_CHECK
        value: "1"
"""
            render_yaml_path = self.project_root / "render.yaml"
            with open(render_yaml_path, 'w') as f:
                f.write(render_yaml_content)
            
            self.log_fix("Created render.yaml configuration (fallback)")
            return True
        except Exception as e:
            self.log_error(f"Failed to create render.yaml: {e}")
            return False
    
    def create_dockerfile_fallback(self):
        """Create Dockerfile as fallback deployment option"""
        try:
            dockerfile_content = """# LogiVault AI Backend - Render Deployment
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE $PORT

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
"""
            
            dockerfile_path = self.project_root / "Dockerfile"
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile_content)
            
            self.log_fix("Created Dockerfile as fallback deployment option")
            return True
        except Exception as e:
            self.log_error(f"Failed to create Dockerfile: {e}")
            return False
    
    def create_startup_script(self):
        """Create startup script for Render"""
        try:
            startup_content = """#!/bin/bash
# LogiVault AI - Render Startup Script

echo "🚀 Starting LogiVault AI Backend..."

# Set Python path
export PYTHONPATH="${PYTHONPATH}:/app"

# Start the application
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
"""
            
            startup_path = self.project_root / "start.sh"
            with open(startup_path, 'w') as f:
                f.write(startup_content)
            
            # Make executable
            os.chmod(startup_path, 0o755)
            
            self.log_fix("Created startup script (start.sh)")
            return True
        except Exception as e:
            self.log_error(f"Failed to create startup script: {e}")
            return False
    
    def update_backend_main(self):
        """Ensure backend/main.py has proper CORS configuration"""
        try:
            main_py_path = self.project_root / "backend" / "main.py"
            
            if not main_py_path.exists():
                self.log_error("backend/main.py not found")
                return False
            
            # Read current content
            with open(main_py_path, 'r') as f:
                content = f.read()
            
            # Check if CORS is properly configured
            if "CORSMiddleware" not in content:
                # Add CORS configuration
                cors_import = "from fastapi.middleware.cors import CORSMiddleware"
                cors_config = '''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
'''
                
                # Insert after FastAPI app creation
                if "app = FastAPI(" in content:
                    lines = content.split('\n')
                    new_lines = []
                    app_created = False
                    
                    for line in lines:
                        new_lines.append(line)
                        if "app = FastAPI(" in line and not app_created:
                            # Find the end of FastAPI initialization
                            if line.strip().endswith(')'):
                                new_lines.append('')
                                new_lines.extend(cors_config.strip().split('\n'))
                                app_created = True
                    
                    # Add import at the top
                    if cors_import not in content:
                        import_lines = []
                        other_lines = []
                        in_imports = True
                        
                        for line in new_lines:
                            if line.startswith('from ') or line.startswith('import '):
                                import_lines.append(line)
                            elif line.strip() == '':
                                if in_imports:
                                    import_lines.append(line)
                                else:
                                    other_lines.append(line)
                            else:
                                in_imports = False
                                other_lines.append(line)
                        
                        import_lines.append(cors_import)
                        new_lines = import_lines + other_lines
                    
                    # Write updated content
                    with open(main_py_path, 'w') as f:
                        f.write('\n'.join(new_lines))
                    
                    self.log_fix("Updated backend/main.py with proper CORS configuration")
            else:
                self.log_fix("CORS already configured in backend/main.py")
            
            return True
        except Exception as e:
            self.log_error(f"Failed to update backend/main.py: {e}")
            return False
    
    def create_environment_template(self):
        """Create .env.render template for deployment"""
        try:
            env_content = """# LogiVault AI - Render Environment Variables
# Copy this to your Render service environment variables

CLAUDE_API_KEY=your_claude_api_key_here
PYTHON_VERSION=3.11.0
PIP_DISABLE_PIP_VERSION_CHECK=1
PYTHONPATH=/app
"""
            
            env_path = self.project_root / ".env.render"
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            self.log_fix("Created .env.render template")
            return True
        except Exception as e:
            self.log_error(f"Failed to create .env.render: {e}")
            return False
    
    def run_fixes(self):
        """Run all deployment fixes"""
        print("🔧 LogiVault AI - Automated Render Deployment Fix")
        print("=" * 50)
        
        fixes = [
            self.create_optimized_requirements,
            self.create_render_yaml,
            self.create_dockerfile_fallback,
            self.create_startup_script,
            self.update_backend_main,
            self.create_environment_template
        ]
        
        for fix in fixes:
            try:
                fix()
            except Exception as e:
                self.log_error(f"Unexpected error in {fix.__name__}: {e}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate deployment fix report"""
        report = {
            "timestamp": subprocess.check_output(["date"], text=True).strip(),
            "fixes_applied": self.fixes_applied,
            "errors": self.errors,
            "success_rate": f"{len(self.fixes_applied)}/{len(self.fixes_applied) + len(self.errors)}",
            "next_steps": [
                "1. Commit and push changes to GitHub",
                "2. Go to Render dashboard",
                "3. Update Build Command: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt",
                "4. Update Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                "5. Set environment variable: CLAUDE_API_KEY=your_key",
                "6. Deploy latest commit"
            ]
        }
        
        report_path = self.project_root / "RENDER_FIX_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT FIX SUMMARY")
        print("=" * 50)
        print(f"✅ Fixes Applied: {len(self.fixes_applied)}")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
        if self.fixes_applied:
            print("\n🎯 Successfully Applied:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        if self.errors:
            print("\n⚠️ Errors Encountered:")
            for error in self.errors:
                print(f"  • {error}")
        
        print(f"\n📄 Full report saved to: RENDER_FIX_REPORT.json")
        print("\n🚀 Next Steps:")
        for step in report["next_steps"]:
            print(f"  {step}")

if __name__ == "__main__":
    fixer = RenderDeploymentFixer()
    fixer.run_fixes()

