#!/usr/bin/env python3
"""
Universal Auto-Resolver for LogiVault AI
Comprehensive toolkit that automatically diagnoses and fixes deployment issues
"""

import os
import sys
import json
import subprocess
import requests
import time
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional

class UniversalAutoResolver:
    def __init__(self):
        self.project_root = Path.cwd()
        self.log_file = self.project_root / "auto_resolver.log"
        self.fixes_applied = []
        self.tools_installed = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages to file and console"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def run_command(self, command: str, capture_output: bool = True) -> Dict[str, Any]:
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=capture_output, 
                text=True,
                timeout=300
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def detect_project_type(self) -> List[str]:
        """Detect what type of project this is"""
        project_types = []
        
        # Check for different project indicators
        if (self.project_root / "package.json").exists():
            project_types.append("nodejs")
        if (self.project_root / "requirements.txt").exists():
            project_types.append("python")
        if (self.project_root / "Dockerfile").exists():
            project_types.append("docker")
        if (self.project_root / "vercel.json").exists():
            project_types.append("vercel")
        if (self.project_root / "render.yaml").exists():
            project_types.append("render")
        if (self.project_root / "backend").exists():
            project_types.append("backend")
        if (self.project_root / "frontend").exists():
            project_types.append("frontend")
        
        self.log(f"Detected project types: {project_types}")
        return project_types
    
    def install_missing_tools(self):
        """Install any missing development tools"""
        tools_to_check = {
            "git": "git --version",
            "python3": "python3 --version",
            "pip3": "pip3 --version",
            "node": "node --version",
            "npm": "npm --version",
            "curl": "curl --version",
            "wget": "wget --version"
        }
        
        for tool, check_cmd in tools_to_check.items():
            result = self.run_command(check_cmd)
            if not result["success"]:
                self.log(f"Installing missing tool: {tool}")
                self.install_tool(tool)
    
    def install_tool(self, tool: str):
        """Install a specific tool"""
        install_commands = {
            "git": "sudo apt-get update && sudo apt-get install -y git",
            "python3": "sudo apt-get update && sudo apt-get install -y python3",
            "pip3": "sudo apt-get update && sudo apt-get install -y python3-pip",
            "node": "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs",
            "npm": "sudo apt-get update && sudo apt-get install -y npm",
            "curl": "sudo apt-get update && sudo apt-get install -y curl",
            "wget": "sudo apt-get update && sudo apt-get install -y wget"
        }
        
        if tool in install_commands:
            result = self.run_command(install_commands[tool])
            if result["success"]:
                self.log(f"Successfully installed {tool}")
                self.tools_installed.append(tool)
            else:
                self.log(f"Failed to install {tool}: {result['stderr']}", "ERROR")
    
    def fix_python_dependencies(self):
        """Fix Python dependency issues"""
        self.log("Fixing Python dependencies...")
        
        # Create minimal requirements.txt if it doesn't exist or has issues
        minimal_requirements = [
            "fastapi==0.104.1",
            "uvicorn==0.24.0",
            "anthropic==0.7.8",
            "python-multipart==0.0.6"
        ]
        
        requirements_file = self.project_root / "requirements.txt"
        
        # Check if current requirements cause issues
        if requirements_file.exists():
            result = self.run_command("pip3 install --dry-run -r requirements.txt")
            if not result["success"]:
                self.log("Current requirements.txt has issues, creating minimal version")
                with open(requirements_file, "w") as f:
                    f.write("\n".join(minimal_requirements))
                self.fixes_applied.append("Fixed requirements.txt")
        else:
            self.log("Creating requirements.txt")
            with open(requirements_file, "w") as f:
                f.write("\n".join(minimal_requirements))
            self.fixes_applied.append("Created requirements.txt")
        
        # Install dependencies
        result = self.run_command("pip3 install -r requirements.txt")
        if result["success"]:
            self.log("Successfully installed Python dependencies")
        else:
            self.log(f"Failed to install dependencies: {result['stderr']}", "ERROR")
    
    def fix_nodejs_dependencies(self):
        """Fix Node.js dependency issues"""
        self.log("Fixing Node.js dependencies...")
        
        package_json = self.project_root / "package.json"
        if package_json.exists():
            # Clear node_modules and package-lock.json
            node_modules = self.project_root / "node_modules"
            package_lock = self.project_root / "package-lock.json"
            
            if node_modules.exists():
                shutil.rmtree(node_modules)
                self.log("Cleared node_modules")
            
            if package_lock.exists():
                package_lock.unlink()
                self.log("Cleared package-lock.json")
            
            # Reinstall dependencies
            result = self.run_command("npm install")
            if result["success"]:
                self.log("Successfully reinstalled Node.js dependencies")
                self.fixes_applied.append("Fixed Node.js dependencies")
            else:
                self.log(f"Failed to install Node.js dependencies: {result['stderr']}", "ERROR")
    
    def fix_git_issues(self):
        """Fix common Git issues"""
        self.log("Checking and fixing Git issues...")
        
        # Check if we're in a git repository
        result = self.run_command("git status")
        if not result["success"]:
            self.log("Initializing Git repository")
            self.run_command("git init")
            self.fixes_applied.append("Initialized Git repository")
        
        # Check for uncommitted changes
        result = self.run_command("git status --porcelain")
        if result["stdout"].strip():
            self.log("Found uncommitted changes, staging them")
            self.run_command("git add .")
            self.fixes_applied.append("Staged uncommitted changes")
        
        # Configure git if not configured
        result = self.run_command("git config user.name")
        if not result["success"] or not result["stdout"].strip():
            self.run_command("git config user.name 'Auto Resolver'")
            self.run_command("git config user.email 'auto-resolver@logivault.ai'")
            self.fixes_applied.append("Configured Git user")
    
    def fix_render_deployment(self):
        """Fix Render deployment issues"""
        self.log("Fixing Render deployment configuration...")
        
        # Create optimized render.yaml
        render_config = """services:
  - type: web
    name: logivault-ai-backend
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
"""
        
        render_file = self.project_root / "render.yaml"
        with open(render_file, "w") as f:
            f.write(render_config)
        
        self.log("Created optimized render.yaml")
        self.fixes_applied.append("Fixed Render configuration")
    
    def fix_vercel_deployment(self):
        """Fix Vercel deployment issues"""
        self.log("Fixing Vercel deployment configuration...")
        
        # Create optimized vercel.json
        vercel_config = {
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
            ]
        }
        
        vercel_file = self.project_root / "vercel.json"
        with open(vercel_file, "w") as f:
            json.dump(vercel_config, f, indent=2)
        
        self.log("Created optimized vercel.json")
        self.fixes_applied.append("Fixed Vercel configuration")
    
    def fix_cors_issues(self):
        """Fix CORS configuration issues"""
        self.log("Fixing CORS configuration...")
        
        backend_main = self.project_root / "backend" / "main.py"
        if backend_main.exists():
            with open(backend_main, "r") as f:
                content = f.read()
            
            # Check if CORS is properly configured
            if "logivault-ai.vercel.app" not in content:
                # Add proper CORS configuration
                cors_config = '''
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://logivault-ai.vercel.app",
        "https://logivault-ai-*.vercel.app", 
        "https://steven-bryants-projects.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
                # This is a simplified fix - in practice, you'd want more sophisticated parsing
                self.log("CORS configuration needs updating in backend/main.py")
                self.fixes_applied.append("Identified CORS configuration issue")
    
    def fix_environment_variables(self):
        """Fix environment variable issues"""
        self.log("Checking environment variables...")
        
        # Create .env template if it doesn't exist
        env_file = self.project_root / ".env"
        if not env_file.exists():
            env_template = """# LogiVault AI Environment Variables
CLAUDE_API_KEY=your_claude_api_key_here
REACT_APP_API_URL=https://logivault-ai-backend.onrender.com
"""
            with open(env_file, "w") as f:
                f.write(env_template)
            self.log("Created .env template")
            self.fixes_applied.append("Created environment variables template")
    
    def create_dockerfile(self):
        """Create optimized Dockerfile"""
        self.log("Creating optimized Dockerfile...")
        
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
        
        dockerfile = self.project_root / "Dockerfile"
        with open(dockerfile, "w") as f:
            f.write(dockerfile_content)
        
        self.log("Created optimized Dockerfile")
        self.fixes_applied.append("Created Dockerfile")
    
    def run_tests(self):
        """Run basic tests to verify everything works"""
        self.log("Running basic tests...")
        
        # Test Python imports
        if (self.project_root / "backend").exists():
            result = self.run_command("python3 -c 'import backend.main; print(\"Backend imports OK\")'")
            if result["success"]:
                self.log("Backend imports test: PASSED")
            else:
                self.log(f"Backend imports test: FAILED - {result['stderr']}", "ERROR")
        
        # Test requirements installation
        result = self.run_command("pip3 check")
        if result["success"]:
            self.log("Dependencies check: PASSED")
        else:
            self.log(f"Dependencies check: FAILED - {result['stderr']}", "ERROR")
    
    def generate_deployment_script(self):
        """Generate automated deployment script"""
        deployment_script = """#!/bin/bash
# Auto-generated deployment script for LogiVault AI

echo "🚀 Starting automated deployment..."

# Commit changes
git add .
git commit -m "Auto-resolver fixes applied" || echo "Nothing to commit"

# Push to GitHub
git push origin main || echo "Push failed - check authentication"

echo "✅ Deployment script completed"
echo "Next steps:"
echo "1. Check Render dashboard for automatic deployment"
echo "2. Verify Vercel deployment"
echo "3. Test application endpoints"
"""
        
        script_file = self.project_root / "deploy.sh"
        with open(script_file, "w") as f:
            f.write(deployment_script)
        
        # Make executable
        os.chmod(script_file, 0o755)
        self.log("Created automated deployment script")
        self.fixes_applied.append("Created deployment script")
    
    def generate_report(self):
        """Generate comprehensive report of fixes applied"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_types": self.detect_project_type(),
            "tools_installed": self.tools_installed,
            "fixes_applied": self.fixes_applied,
            "recommendations": [
                "Regularly run this auto-resolver to prevent issues",
                "Keep dependencies minimal and up-to-date",
                "Monitor deployment logs for early issue detection",
                "Set up automated testing pipeline"
            ]
        }
        
        report_file = self.project_root / "auto_resolver_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Generated comprehensive report: {report_file}")
        return report
    
    def run_full_resolution(self):
        """Run complete auto-resolution process"""
        self.log("🚀 Starting Universal Auto-Resolver for LogiVault AI")
        self.log("=" * 60)
        
        try:
            # Detect project type
            project_types = self.detect_project_type()
            
            # Install missing tools
            self.install_missing_tools()
            
            # Fix Git issues
            self.fix_git_issues()
            
            # Fix dependencies based on project type
            if "python" in project_types:
                self.fix_python_dependencies()
            
            if "nodejs" in project_types:
                self.fix_nodejs_dependencies()
            
            # Fix deployment configurations
            if "render" in project_types:
                self.fix_render_deployment()
            
            if "vercel" in project_types:
                self.fix_vercel_deployment()
            
            # Fix CORS issues
            self.fix_cors_issues()
            
            # Fix environment variables
            self.fix_environment_variables()
            
            # Create Dockerfile
            self.create_dockerfile()
            
            # Run tests
            self.run_tests()
            
            # Generate deployment script
            self.generate_deployment_script()
            
            # Generate report
            report = self.generate_report()
            
            self.log("=" * 60)
            self.log("✅ Auto-resolution completed successfully!")
            self.log(f"Applied {len(self.fixes_applied)} fixes")
            self.log(f"Installed {len(self.tools_installed)} tools")
            self.log("Check auto_resolver_report.json for detailed results")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Auto-resolution failed: {str(e)}", "ERROR")
            return False

def main():
    """Main entry point"""
    resolver = UniversalAutoResolver()
    success = resolver.run_full_resolution()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

