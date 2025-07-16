#!/usr/bin/env python3
"""
LogiVault AI Deployment Verification Script
Tests deployment configuration and validates fixes
"""

import requests
import json
import time
import sys
from pathlib import Path

class DeploymentVerifier:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []

    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        
        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_cors_configuration(self):
        """Test CORS configuration in main.py"""
        print("\n🔍 Testing CORS Configuration...")
        
        main_py_path = self.project_root / "backend" / "main.py"
        
        if not main_py_path.exists():
            self.log_test("CORS Config File Exists", False, "main.py not found")
            return
        
        try:
            with open(main_py_path, 'r') as f:
                content = f.read()
            
            # Check for required CORS origins
            required_origins = [
                "https://logivault-ai.vercel.app",
                "https://steven-bryants-projects.vercel.app",
                "http://localhost:3000"
            ]
            
            all_origins_present = all(origin in content for origin in required_origins)
            
            self.log_test(
                "CORS Origins Configuration", 
                all_origins_present,
                "All required origins present" if all_origins_present else "Missing required origins"
            )
            
            # Check for CORS middleware
            has_cors_middleware = "CORSMiddleware" in content
            self.log_test(
                "CORS Middleware Present",
                has_cors_middleware,
                "CORSMiddleware configured" if has_cors_middleware else "CORSMiddleware missing"
            )
            
        except Exception as e:
            self.log_test("CORS Configuration Read", False, f"Error reading config: {e}")

    def test_environment_variables(self):
        """Test environment variable configuration"""
        print("\n🔍 Testing Environment Variables...")
        
        # Test backend .env
        backend_env_path = self.project_root / ".env"
        if backend_env_path.exists():
            try:
                with open(backend_env_path, 'r') as f:
                    backend_env = f.read()
                
                has_claude_key = "CLAUDE_API_KEY=" in backend_env
                self.log_test(
                    "Backend Claude API Key",
                    has_claude_key,
                    "Claude API key configured" if has_claude_key else "Claude API key missing"
                )
                
            except Exception as e:
                self.log_test("Backend Environment Read", False, f"Error: {e}")
        else:
            self.log_test("Backend Environment File", False, ".env file missing")
        
        # Test frontend .env.local
        frontend_env_path = self.project_root / "frontend" / ".env.local"
        if frontend_env_path.exists():
            try:
                with open(frontend_env_path, 'r') as f:
                    frontend_env = f.read()
                
                has_api_url = "REACT_APP_API_URL=" in frontend_env
                self.log_test(
                    "Frontend API URL",
                    has_api_url,
                    "API URL configured" if has_api_url else "API URL missing"
                )
                
            except Exception as e:
                self.log_test("Frontend Environment Read", False, f"Error: {e}")
        else:
            self.log_test("Frontend Environment File", False, ".env.local file missing")

    def test_deployment_configs(self):
        """Test deployment configuration files"""
        print("\n🔍 Testing Deployment Configurations...")
        
        # Test Vercel config
        vercel_config_path = self.project_root / "vercel.json"
        if vercel_config_path.exists():
            try:
                with open(vercel_config_path, 'r') as f:
                    vercel_config = json.load(f)
                
                has_name = "name" in vercel_config
                has_builds = "builds" in vercel_config
                
                self.log_test(
                    "Vercel Configuration",
                    has_name and has_builds,
                    "Vercel config properly structured" if has_name and has_builds else "Vercel config incomplete"
                )
                
            except Exception as e:
                self.log_test("Vercel Config Read", False, f"Error: {e}")
        else:
            self.log_test("Vercel Configuration File", False, "vercel.json missing")
        
        # Test requirements.txt
        requirements_path = self.project_root / "requirements.txt"
        if requirements_path.exists():
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read()
                
                required_packages = ["fastapi", "uvicorn", "anthropic"]
                has_all_packages = all(pkg in requirements for pkg in required_packages)
                
                self.log_test(
                    "Requirements File",
                    has_all_packages,
                    "All required packages present" if has_all_packages else "Missing required packages"
                )
                
            except Exception as e:
                self.log_test("Requirements Read", False, f"Error: {e}")
        else:
            self.log_test("Requirements File", False, "requirements.txt missing")

    def test_api_endpoints(self):
        """Test API endpoint definitions"""
        print("\n🔍 Testing API Endpoints...")
        
        main_py_path = self.project_root / "backend" / "main.py"
        
        if not main_py_path.exists():
            self.log_test("API Endpoints File", False, "main.py not found")
            return
        
        try:
            with open(main_py_path, 'r') as f:
                content = f.read()
            
            # Check for required endpoints
            required_endpoints = [
                '@app.get("/healthz")',
                '@app.post("/claude")',
                '@app.post("/generate")'
            ]
            
            for endpoint in required_endpoints:
                has_endpoint = endpoint in content
                endpoint_name = endpoint.split('"')[1]
                self.log_test(
                    f"Endpoint {endpoint_name}",
                    has_endpoint,
                    f"Endpoint defined" if has_endpoint else f"Endpoint missing"
                )
            
        except Exception as e:
            self.log_test("API Endpoints Read", False, f"Error: {e}")

    def test_live_deployment(self, backend_url=None, frontend_url=None):
        """Test live deployment if URLs provided"""
        if not backend_url and not frontend_url:
            print("\n⏭️  Skipping live deployment tests (no URLs provided)")
            return
        
        print("\n🔍 Testing Live Deployment...")
        
        if backend_url:
            try:
                # Test health endpoint
                response = requests.get(f"{backend_url}/healthz", timeout=10)
                self.log_test(
                    "Backend Health Check",
                    response.status_code == 200,
                    f"Status: {response.status_code}" if response.status_code == 200 else f"Failed: {response.status_code}"
                )
                
                # Test CORS headers
                if response.status_code == 200:
                    cors_headers = response.headers.get('Access-Control-Allow-Origin', '')
                    self.log_test(
                        "CORS Headers Present",
                        bool(cors_headers),
                        f"CORS: {cors_headers}" if cors_headers else "No CORS headers"
                    )
                
            except requests.RequestException as e:
                self.log_test("Backend Connectivity", False, f"Connection error: {e}")
        
        if frontend_url:
            try:
                response = requests.get(frontend_url, timeout=10)
                self.log_test(
                    "Frontend Accessibility",
                    response.status_code == 200,
                    f"Status: {response.status_code}" if response.status_code == 200 else f"Failed: {response.status_code}"
                )
                
            except requests.RequestException as e:
                self.log_test("Frontend Connectivity", False, f"Connection error: {e}")

    def run_all_tests(self, backend_url=None, frontend_url=None):
        """Run all verification tests"""
        print("🧪 Starting LogiVault AI Deployment Verification...")
        print("=" * 60)
        
        # Run all test methods
        self.test_cors_configuration()
        self.test_environment_variables()
        self.test_deployment_configs()
        self.test_api_endpoints()
        self.test_live_deployment(backend_url, frontend_url)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 VERIFICATION SUMMARY")
        print("=" * 60)
        
        total_tests = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        if self.tests_failed > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"   • {result['test']}: {result['message']}")
        
        print(f"\n🎯 Deployment Status: {'✅ READY' if self.tests_failed == 0 else '❌ NEEDS FIXES'}")
        
        return self.tests_failed == 0

if __name__ == "__main__":
    verifier = DeploymentVerifier()
    
    # Optional: Test live deployments if URLs provided as arguments
    backend_url = sys.argv[1] if len(sys.argv) > 1 else None
    frontend_url = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = verifier.run_all_tests(backend_url, frontend_url)
    sys.exit(0 if success else 1)

