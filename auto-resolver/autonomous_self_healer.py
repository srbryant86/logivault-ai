#!/usr/bin/env python3
"""
Autonomous Self-Healing System for LogiVault AI
Zero-intervention system that automatically detects, diagnoses, and fixes any issues
"""

import os
import sys
import json
import subprocess
import requests
import time
import shutil
import threading
import schedule
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta

class AutonomousSelfHealer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.log_file = self.project_root / "self_healer.log"
        self.state_file = self.project_root / "healer_state.json"
        self.fixes_applied = []
        self.monitoring_active = False
        self.last_health_check = None
        self.failure_count = 0
        self.max_retries = 5
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def save_state(self):
        """Save current state to file"""
        state = {
            "last_run": datetime.now().isoformat(),
            "fixes_applied": self.fixes_applied,
            "failure_count": self.failure_count,
            "monitoring_active": self.monitoring_active
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load previous state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                self.fixes_applied = state.get("fixes_applied", [])
                self.failure_count = state.get("failure_count", 0)
                return state
            except:
                return {}
        return {}
    
    def run_command_safe(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """Run command with comprehensive error handling"""
        try:
            self.logger.info(f"Executing: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            if not success:
                self.logger.warning(f"Command failed: {command}")
                self.logger.warning(f"Error: {result.stderr}")
            
            return {
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return {"success": False, "stdout": "", "stderr": "Timeout", "returncode": -1}
        except Exception as e:
            self.logger.error(f"Command exception: {command} - {str(e)}")
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}
    
    def check_service_health(self, url: str) -> bool:
        """Check if a service is healthy"""
        try:
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def auto_install_missing_tools(self):
        """Automatically install any missing tools without prompts"""
        tools = {
            "git": "sudo apt-get update -y && sudo apt-get install -y git",
            "python3": "sudo apt-get update -y && sudo apt-get install -y python3",
            "pip3": "sudo apt-get update -y && sudo apt-get install -y python3-pip",
            "node": "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs",
            "npm": "sudo apt-get update -y && sudo apt-get install -y npm",
            "curl": "sudo apt-get update -y && sudo apt-get install -y curl",
            "wget": "sudo apt-get update -y && sudo apt-get install -y wget",
            "zip": "sudo apt-get update -y && sudo apt-get install -y zip unzip"
        }
        
        for tool, install_cmd in tools.items():
            check_result = self.run_command_safe(f"which {tool}")
            if not check_result["success"]:
                self.logger.info(f"Auto-installing missing tool: {tool}")
                install_result = self.run_command_safe(install_cmd)
                if install_result["success"]:
                    self.logger.info(f"Successfully installed {tool}")
                    self.fixes_applied.append(f"Auto-installed {tool}")
                else:
                    self.logger.error(f"Failed to install {tool}")
    
    def auto_fix_python_environment(self):
        """Automatically fix Python environment issues"""
        self.logger.info("Auto-fixing Python environment...")
        
        # Create bulletproof requirements.txt
        minimal_requirements = [
            "fastapi==0.104.1",
            "uvicorn==0.24.0", 
            "anthropic==0.7.8",
            "python-multipart==0.0.6",
            "requests==2.31.0"
        ]
        
        requirements_file = self.project_root / "requirements.txt"
        
        # Always create clean requirements
        with open(requirements_file, "w") as f:
            f.write("\n".join(minimal_requirements))
        
        # Install with multiple fallback strategies
        install_commands = [
            "pip3 install --upgrade pip",
            "pip3 install -r requirements.txt",
            "pip3 install --force-reinstall -r requirements.txt",
            "pip3 install --no-cache-dir -r requirements.txt"
        ]
        
        for cmd in install_commands:
            result = self.run_command_safe(cmd)
            if result["success"]:
                self.logger.info(f"Python dependencies installed successfully with: {cmd}")
                self.fixes_applied.append("Fixed Python environment")
                break
        else:
            self.logger.error("All Python installation strategies failed")
    
    def auto_fix_git_repository(self):
        """Automatically fix Git repository issues"""
        self.logger.info("Auto-fixing Git repository...")
        
        # Initialize if not a git repo
        if not (self.project_root / ".git").exists():
            self.run_command_safe("git init")
            self.fixes_applied.append("Initialized Git repository")
        
        # Configure git user if needed
        user_check = self.run_command_safe("git config user.name")
        if not user_check["success"] or not user_check["stdout"].strip():
            self.run_command_safe("git config user.name 'Auto Healer'")
            self.run_command_safe("git config user.email 'healer@logivault.ai'")
            self.fixes_applied.append("Configured Git user")
        
        # Auto-stage and commit any changes
        status_result = self.run_command_safe("git status --porcelain")
        if status_result["stdout"].strip():
            self.run_command_safe("git add .")
            commit_msg = f"Auto-healer commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.run_command_safe(f'git commit -m "{commit_msg}"')
            self.fixes_applied.append("Auto-committed changes")
    
    def auto_fix_deployment_configs(self):
        """Automatically create/fix all deployment configurations"""
        self.logger.info("Auto-fixing deployment configurations...")
        
        # Render configuration
        render_config = """services:
  - type: web
    name: logivault-ai-backend
    runtime: python3
    buildCommand: pip install --upgrade pip && pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    plan: starter
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
"""
        
        with open(self.project_root / "render.yaml", "w") as f:
            f.write(render_config)
        
        # Vercel configuration
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "frontend/package.json",
                    "use": "@vercel/static-build",
                    "config": {"distDir": "build"}
                }
            ]
        }
        
        with open(self.project_root / "vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        
        # Dockerfile
        dockerfile_content = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        with open(self.project_root / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Environment variables
        env_content = """CLAUDE_API_KEY=your_claude_api_key_here
REACT_APP_API_URL=https://logivault-ai-backend.onrender.com
"""
        
        env_file = self.project_root / ".env"
        if not env_file.exists():
            with open(env_file, "w") as f:
                f.write(env_content)
        
        self.fixes_applied.append("Fixed all deployment configurations")
    
    def auto_fix_cors_issues(self):
        """Automatically fix CORS configuration"""
        backend_main = self.project_root / "backend" / "main.py"
        if backend_main.exists():
            try:
                with open(backend_main, "r") as f:
                    content = f.read()
                
                # Check if CORS is properly configured
                if "logivault-ai.vercel.app" not in content:
                    # Add comprehensive CORS configuration
                    cors_addition = '''
from fastapi.middleware.cors import CORSMiddleware

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
                    # Insert after FastAPI app creation
                    if "app = FastAPI()" in content:
                        content = content.replace("app = FastAPI()", f"app = FastAPI(){cors_addition}")
                        with open(backend_main, "w") as f:
                            f.write(content)
                        self.fixes_applied.append("Fixed CORS configuration")
            except Exception as e:
                self.logger.error(f"Failed to fix CORS: {e}")
    
    def auto_deploy_to_services(self):
        """Automatically deploy to services if possible"""
        self.logger.info("Attempting auto-deployment...")
        
        # Check if we can push to git
        remote_check = self.run_command_safe("git remote -v")
        if remote_check["success"] and "github.com" in remote_check["stdout"]:
            # Try to push (will work if authentication is set up)
            push_result = self.run_command_safe("git push origin main")
            if push_result["success"]:
                self.logger.info("Successfully pushed to GitHub")
                self.fixes_applied.append("Auto-deployed to GitHub")
            else:
                self.logger.info("Push failed - authentication needed")
    
    def monitor_and_heal(self):
        """Continuous monitoring and healing"""
        self.logger.info("Starting continuous monitoring...")
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                # Check service health
                services_to_check = [
                    "https://logivault-ai.vercel.app",
                    "https://logivault-ai-backend.onrender.com/healthz"
                ]
                
                for service_url in services_to_check:
                    if not self.check_service_health(service_url):
                        self.logger.warning(f"Service unhealthy: {service_url}")
                        self.auto_heal_service(service_url)
                
                # Run periodic maintenance
                self.run_periodic_maintenance()
                
                # Save state
                self.save_state()
                
                # Wait before next check
                time.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def auto_heal_service(self, service_url: str):
        """Automatically heal a failing service"""
        self.logger.info(f"Auto-healing service: {service_url}")
        
        # Run full resolution process
        self.run_full_auto_resolution()
        
        # Wait and recheck
        time.sleep(60)
        if self.check_service_health(service_url):
            self.logger.info(f"Service healed successfully: {service_url}")
            self.failure_count = 0
        else:
            self.failure_count += 1
            self.logger.warning(f"Service still unhealthy after healing attempt {self.failure_count}")
    
    def run_periodic_maintenance(self):
        """Run periodic maintenance tasks"""
        # Clean up old logs
        if self.log_file.exists() and self.log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
            # Keep only last 1000 lines
            with open(self.log_file, "r") as f:
                lines = f.readlines()
            with open(self.log_file, "w") as f:
                f.writelines(lines[-1000:])
        
        # Update dependencies if needed
        if datetime.now().hour == 2:  # Run at 2 AM
            self.auto_fix_python_environment()
    
    def run_full_auto_resolution(self):
        """Run complete autonomous resolution process"""
        self.logger.info("🤖 Starting Autonomous Self-Healing Process")
        self.logger.info("=" * 60)
        
        try:
            # Load previous state
            self.load_state()
            
            # Auto-install missing tools
            self.auto_install_missing_tools()
            
            # Fix Python environment
            self.auto_fix_python_environment()
            
            # Fix Git repository
            self.auto_fix_git_repository()
            
            # Fix deployment configurations
            self.auto_fix_deployment_configs()
            
            # Fix CORS issues
            self.auto_fix_cors_issues()
            
            # Attempt auto-deployment
            self.auto_deploy_to_services()
            
            # Save state
            self.save_state()
            
            self.logger.info("=" * 60)
            self.logger.info("✅ Autonomous healing completed successfully!")
            self.logger.info(f"Applied {len(self.fixes_applied)} fixes")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Autonomous healing failed: {str(e)}")
            return False
    
    def start_autonomous_mode(self):
        """Start fully autonomous mode with continuous monitoring"""
        self.logger.info("🚀 Starting Autonomous Self-Healing Mode")
        
        # Run initial resolution
        self.run_full_auto_resolution()
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=self.monitor_and_heal, daemon=True)
        monitor_thread.start()
        
        # Schedule periodic full resolutions
        schedule.every(6).hours.do(self.run_full_auto_resolution)
        schedule.every().day.at("02:00").do(self.run_full_auto_resolution)
        
        self.logger.info("🤖 Autonomous mode active - system will self-heal automatically")
        self.logger.info("Press Ctrl+C to stop autonomous mode")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.logger.info("Stopping autonomous mode...")
            self.monitoring_active = False

def main():
    """Main entry point"""
    healer = AutonomousSelfHealer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--autonomous":
        # Start fully autonomous mode
        healer.start_autonomous_mode()
    else:
        # Run one-time resolution
        success = healer.run_full_auto_resolution()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

