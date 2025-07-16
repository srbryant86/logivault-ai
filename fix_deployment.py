#!/usr/bin/env python3
"""
LogiVault AI Deployment Fix Automation Script
Addresses CORS configuration, environment variables, and deployment issues
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class LogiVaultFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
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

    def log_info(self, message):
        """Log informational message"""
        print(f"ℹ️  {message}")

    def fix_cors_configuration(self):
        """Fix CORS configuration to allow current deployment URL"""
        self.log_info("Fixing CORS configuration...")
        
        main_py_path = self.backend_dir / "main.py"
        if not main_py_path.exists():
            self.log_error("Backend main.py not found")
            return False

        try:
            with open(main_py_path, 'r') as f:
                content = f.read()

            # Update CORS configuration to be more flexible
            old_cors = '''allow_origins=[
        "https://logivault-ai.vercel.app",
        "https://logivault-ai-*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],'''

            new_cors = '''allow_origins=[
        "https://logivault-ai.vercel.app",
        "https://logivault-ai-*.vercel.app", 
        "https://steven-bryants-projects.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],'''

            if old_cors in content:
                content = content.replace(old_cors, new_cors)
                
                with open(main_py_path, 'w') as f:
                    f.write(content)
                
                self.log_fix("Updated CORS configuration to allow current deployment URL")
                return True
            else:
                self.log_info("CORS configuration already updated or different format")
                return True

        except Exception as e:
            self.log_error(f"Failed to update CORS configuration: {e}")
            return False

    def fix_environment_variables(self):
        """Fix environment variable configurations"""
        self.log_info("Fixing environment variables...")
        
        # Backend environment variables
        backend_env_path = self.project_root / ".env"
        try:
            with open(backend_env_path, 'r') as f:
                backend_env = f.read()

            # Check if API URL is correctly configured
            if "REACT_APP_API_URL=https://api.logivault.ai/api/v1" in backend_env:
                # Update to use the actual backend deployment URL
                backend_env = backend_env.replace(
                    "REACT_APP_API_URL=https://api.logivault.ai/api/v1",
                    "REACT_APP_API_URL=https://logivault-ai-backend.onrender.com"
                )
                
                with open(backend_env_path, 'w') as f:
                    f.write(backend_env)
                
                self.log_fix("Updated backend API URL in environment")

        except Exception as e:
            self.log_error(f"Failed to update backend environment: {e}")

        # Frontend environment variables
        frontend_env_path = self.frontend_dir / ".env.local"
        try:
            # Create production environment configuration
            production_env = "REACT_APP_API_URL=https://logivault-ai-backend.onrender.com\n"
            
            with open(frontend_env_path, 'w') as f:
                f.write(production_env)
            
            self.log_fix("Updated frontend environment for production")

        except Exception as e:
            self.log_error(f"Failed to update frontend environment: {e}")

        # Create environment template
        env_template_path = self.project_root / ".env.template"
        try:
            template_content = """# Backend Environment Variables
CLAUDE_API_KEY=your_claude_api_key_here

# Frontend Environment Variables  
REACT_APP_API_URL=https://logivault-ai-backend.onrender.com

# Optional: Stripe Configuration
STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here
"""
            
            with open(env_template_path, 'w') as f:
                f.write(template_content)
            
            self.log_fix("Created environment template file")

        except Exception as e:
            self.log_error(f"Failed to create environment template: {e}")

    def create_deployment_configs(self):
        """Create deployment configuration files"""
        self.log_info("Creating deployment configurations...")
        
        # Vercel configuration for frontend
        vercel_config = {
            "name": "logivault-ai",
            "version": 2,
            "builds": [
                {
                    "src": "frontend/package.json",
                    "use": "@vercel/static-build",
                    "config": {
                        "distDir": "build"
                    }
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "/frontend/$1"
                }
            ],
            "env": {
                "REACT_APP_API_URL": "https://logivault-ai-backend.onrender.com"
            }
        }

        try:
            vercel_path = self.project_root / "vercel.json"
            with open(vercel_path, 'w') as f:
                json.dump(vercel_config, f, indent=2)
            
            self.log_fix("Created Vercel deployment configuration")

        except Exception as e:
            self.log_error(f"Failed to create Vercel config: {e}")

        # Render configuration for backend
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": "logivault-ai-backend",
                    "env": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                    "envVars": [
                        {
                            "key": "CLAUDE_API_KEY",
                            "sync": False
                        }
                    ]
                }
            ]
        }

        try:
            render_path = self.project_root / "render.yaml"
            with open(render_path, 'w') as f:
                json.dump(render_config, f, indent=2)
            
            self.log_fix("Created Render deployment configuration")

        except Exception as e:
            self.log_error(f"Failed to create Render config: {e}")

    def fix_api_endpoints(self):
        """Ensure API endpoints are properly configured"""
        self.log_info("Checking API endpoint configuration...")
        
        main_py_path = self.backend_dir / "main.py"
        try:
            with open(main_py_path, 'r') as f:
                content = f.read()

            # Check if both /claude and /generate endpoints exist
            has_claude = '@app.post("/claude")' in content
            has_generate = '@app.post("/generate")' in content

            if has_claude and has_generate:
                self.log_fix("API endpoints are properly configured")
            else:
                self.log_error("Missing required API endpoints")

        except Exception as e:
            self.log_error(f"Failed to check API endpoints: {e}")

    def create_requirements_file(self):
        """Create or update requirements.txt"""
        self.log_info("Creating requirements.txt...")
        
        requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
anthropic==0.7.8
python-multipart==0.0.6
pydantic==2.5.0
"""
        
        try:
            req_path = self.project_root / "requirements.txt"
            with open(req_path, 'w') as f:
                f.write(requirements)
            
            self.log_fix("Created/updated requirements.txt")

        except Exception as e:
            self.log_error(f"Failed to create requirements.txt: {e}")

    def create_startup_script(self):
        """Create startup script for backend"""
        self.log_info("Creating startup script...")
        
        startup_script = """#!/bin/bash
# LogiVault AI Backend Startup Script

echo "Starting LogiVault AI Backend..."

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
"""
        
        try:
            script_path = self.project_root / "start.sh"
            with open(script_path, 'w') as f:
                f.write(startup_script)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            self.log_fix("Created startup script")

        except Exception as e:
            self.log_error(f"Failed to create startup script: {e}")

    def run_all_fixes(self):
        """Run all automated fixes"""
        print("🚀 Starting LogiVault AI Deployment Fixes...")
        print("=" * 50)
        
        # Run all fix methods
        self.fix_cors_configuration()
        self.fix_environment_variables()
        self.create_deployment_configs()
        self.fix_api_endpoints()
        self.create_requirements_file()
        self.create_startup_script()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT FIX SUMMARY")
        print("=" * 50)
        
        if self.fixes_applied:
            print(f"✅ Fixes Applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   • {fix}")
        
        if self.errors:
            print(f"\n❌ Errors Encountered ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        print(f"\n🎯 Next Steps:")
        print("   1. Commit and push these changes to GitHub")
        print("   2. Redeploy frontend to logivault-ai.vercel.app")
        print("   3. Redeploy backend to Render with environment variables")
        print("   4. Test the application end-to-end")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    fixer = LogiVaultFixer()
    success = fixer.run_all_fixes()
    sys.exit(0 if success else 1)

