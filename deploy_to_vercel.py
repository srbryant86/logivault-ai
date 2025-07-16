#!/usr/bin/env python3
"""
LogiVault AI Vercel Deployment Automation
Automates frontend deployment to correct Vercel project
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class VercelDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"

    def log_info(self, message):
        print(f"ℹ️  {message}")

    def log_success(self, message):
        print(f"✅ {message}")

    def log_error(self, message):
        print(f"❌ {message}")

    def check_vercel_cli(self):
        """Check if Vercel CLI is installed"""
        try:
            result = subprocess.run(['vercel', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.log_success(f"Vercel CLI found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_error("Vercel CLI not found. Please install with: npm i -g vercel")
            return False

    def setup_vercel_project(self):
        """Setup Vercel project configuration"""
        self.log_info("Setting up Vercel project configuration...")
        
        # Create vercel.json for frontend deployment
        vercel_config = {
            "name": "logivault-ai",
            "version": 2,
            "framework": "create-react-app",
            "buildCommand": "npm run build",
            "outputDirectory": "build",
            "installCommand": "npm install",
            "devCommand": "npm start",
            "env": {
                "REACT_APP_API_URL": "https://logivault-ai-backend.onrender.com"
            },
            "build": {
                "env": {
                    "REACT_APP_API_URL": "https://logivault-ai-backend.onrender.com"
                }
            }
        }

        vercel_path = self.project_root / "vercel.json"
        try:
            with open(vercel_path, 'w') as f:
                json.dump(vercel_config, f, indent=2)
            self.log_success("Created vercel.json configuration")
        except Exception as e:
            self.log_error(f"Failed to create vercel.json: {e}")
            return False

        return True

    def update_package_json(self):
        """Update package.json with deployment scripts"""
        self.log_info("Updating package.json...")
        
        package_json_path = self.frontend_dir / "package.json"
        
        if not package_json_path.exists():
            self.log_error("package.json not found in frontend directory")
            return False

        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)

            # Add deployment scripts
            if "scripts" not in package_data:
                package_data["scripts"] = {}

            package_data["scripts"]["deploy"] = "vercel --prod"
            package_data["scripts"]["deploy:preview"] = "vercel"

            # Ensure build script exists
            if "build" not in package_data["scripts"]:
                package_data["scripts"]["build"] = "react-scripts build"

            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)

            self.log_success("Updated package.json with deployment scripts")
            return True

        except Exception as e:
            self.log_error(f"Failed to update package.json: {e}")
            return False

    def create_deployment_script(self):
        """Create deployment script"""
        self.log_info("Creating deployment script...")
        
        deploy_script = """#!/bin/bash
# LogiVault AI Frontend Deployment Script

set -e

echo "🚀 Deploying LogiVault AI Frontend to Vercel..."

# Navigate to project root
cd "$(dirname "$0")"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building project..."
npm run build

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod --yes

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at: https://logivault-ai.vercel.app"
"""

        script_path = self.project_root / "deploy_frontend.sh"
        try:
            with open(script_path, 'w') as f:
                f.write(deploy_script)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            self.log_success("Created deployment script: deploy_frontend.sh")
            return True

        except Exception as e:
            self.log_error(f"Failed to create deployment script: {e}")
            return False

    def create_env_production(self):
        """Create production environment file"""
        self.log_info("Creating production environment configuration...")
        
        env_production = """# Production Environment Variables
REACT_APP_API_URL=https://logivault-ai-backend.onrender.com
GENERATE_SOURCEMAP=false
"""

        try:
            env_path = self.frontend_dir / ".env.production"
            with open(env_path, 'w') as f:
                f.write(env_production)
            
            self.log_success("Created .env.production file")
            return True

        except Exception as e:
            self.log_error(f"Failed to create .env.production: {e}")
            return False

    def run_setup(self):
        """Run all setup steps"""
        print("🚀 Setting up LogiVault AI Vercel Deployment...")
        print("=" * 50)
        
        steps = [
            ("Checking Vercel CLI", self.check_vercel_cli),
            ("Setting up Vercel project", self.setup_vercel_project),
            ("Updating package.json", self.update_package_json),
            ("Creating deployment script", self.create_deployment_script),
            ("Creating production environment", self.create_env_production)
        ]
        
        for step_name, step_func in steps:
            self.log_info(f"Step: {step_name}")
            if not step_func():
                self.log_error(f"Failed at step: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("✅ VERCEL DEPLOYMENT SETUP COMPLETE")
        print("=" * 50)
        print("\n🎯 Next Steps:")
        print("   1. Run: ./deploy_frontend.sh")
        print("   2. Or manually: cd frontend && vercel --prod")
        print("   3. Ensure deployment goes to logivault-ai.vercel.app")
        print("   4. Test the deployed application")
        
        return True

if __name__ == "__main__":
    deployer = VercelDeployer()
    success = deployer.run_setup()
    sys.exit(0 if success else 1)

