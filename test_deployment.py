#!/usr/bin/env python3
"""
LogiVault AI Deployment Testing Script
Comprehensive testing of deployment configuration and functionality
"""

import requests
import json
import time
import sys
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional

class DeploymentTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Test configuration
        self.backend_urls = [
            "http://localhost:8000",
            "https://logivault-ai-backend.onrender.com"
        ]
        
        self.frontend_urls = [
            "http://localhost:3000",
            "https://logivault-ai.vercel.app",
            "https://steven-bryants-projects.vercel.app"
        ]

    def log_test(self, test_name: str, passed: bool, message: str = "", details: Dict = None):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
        
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details or {}
        })
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

    def test_backend_health(self, backend_url: str) -> bool:
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{backend_url}/healthz", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    f"Backend Health ({backend_url})",
                    True,
                    f"Status: {data.get('status', 'unknown')}",
                    {"response_time": f"{response.elapsed.total_seconds():.2f}s"}
                )
                return True
            else:
                self.log_test(
                    f"Backend Health ({backend_url})",
                    False,
                    f"HTTP {response.status_code}"
                )
                return False
                
        except requests.RequestException as e:
            self.log_test(
                f"Backend Health ({backend_url})",
                False,
                f"Connection error: {str(e)[:100]}"
            )
            return False

    def test_cors_headers(self, backend_url: str) -> bool:
        """Test CORS headers"""
        try:
            # Test preflight request
            headers = {
                'Origin': 'https://logivault-ai.vercel.app',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(f"{backend_url}/generate", headers=headers, timeout=10)
            
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            has_cors = any(cors_headers.values())
            
            self.log_test(
                f"CORS Headers ({backend_url})",
                has_cors,
                "CORS properly configured" if has_cors else "CORS headers missing",
                cors_headers
            )
            
            return has_cors
            
        except requests.RequestException as e:
            self.log_test(
                f"CORS Headers ({backend_url})",
                False,
                f"Connection error: {str(e)[:100]}"
            )
            return False

    def test_api_endpoint(self, backend_url: str, endpoint: str = "/generate") -> bool:
        """Test API endpoint functionality"""
        try:
            test_payload = {
                "prompt": "Test prompt for LogiVault AI"
            }
            
            response = requests.post(
                f"{backend_url}{endpoint}",
                json=test_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                has_content = 'content' in data or 'response' in data
                
                self.log_test(
                    f"API Endpoint {endpoint} ({backend_url})",
                    has_content,
                    "API responding correctly" if has_content else "Unexpected response format",
                    {"response_keys": list(data.keys()) if isinstance(data, dict) else "non-dict"}
                )
                return has_content
            else:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', str(error_data))
                except:
                    error_detail = response.text[:100]
                
                self.log_test(
                    f"API Endpoint {endpoint} ({backend_url})",
                    False,
                    f"HTTP {response.status_code}: {error_detail}"
                )
                return False
                
        except requests.RequestException as e:
            self.log_test(
                f"API Endpoint {endpoint} ({backend_url})",
                False,
                f"Connection error: {str(e)[:100]}"
            )
            return False

    def test_frontend_accessibility(self, frontend_url: str) -> bool:
        """Test frontend accessibility"""
        try:
            response = requests.get(frontend_url, timeout=15)
            
            if response.status_code == 200:
                # Check if it's a React app
                is_react_app = (
                    'react' in response.text.lower() or 
                    'root' in response.text or
                    'app' in response.text.lower()
                )
                
                self.log_test(
                    f"Frontend Access ({frontend_url})",
                    True,
                    "Frontend accessible",
                    {
                        "content_length": len(response.text),
                        "appears_react": is_react_app
                    }
                )
                return True
            else:
                self.log_test(
                    f"Frontend Access ({frontend_url})",
                    False,
                    f"HTTP {response.status_code}"
                )
                return False
                
        except requests.RequestException as e:
            self.log_test(
                f"Frontend Access ({frontend_url})",
                False,
                f"Connection error: {str(e)[:100]}"
            )
            return False

    async def test_end_to_end_flow(self, backend_url: str, frontend_url: str) -> bool:
        """Test end-to-end application flow"""
        try:
            async with aiohttp.ClientSession() as session:
                # Test the full flow that a user would experience
                test_prompt = "Optimize this text: Hello world, this is a test."
                
                async with session.post(
                    f"{backend_url}/generate",
                    json={"prompt": test_prompt},
                    headers={
                        'Content-Type': 'application/json',
                        'Origin': frontend_url
                    },
                    timeout=30
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        has_content = 'content' in data or 'response' in data
                        
                        self.log_test(
                            f"End-to-End Flow ({frontend_url} → {backend_url})",
                            has_content,
                            "Full flow working" if has_content else "Response format issue",
                            {"response_size": len(str(data))}
                        )
                        return has_content
                    else:
                        error_text = await response.text()
                        self.log_test(
                            f"End-to-End Flow ({frontend_url} → {backend_url})",
                            False,
                            f"HTTP {response.status}: {error_text[:100]}"
                        )
                        return False
                        
        except Exception as e:
            self.log_test(
                f"End-to-End Flow ({frontend_url} → {backend_url})",
                False,
                f"Error: {str(e)[:100]}"
            )
            return False

    def test_configuration_files(self) -> bool:
        """Test configuration files exist and are valid"""
        config_files = {
            "vercel.json": self.project_root / "vercel.json",
            "requirements.txt": self.project_root / "requirements.txt",
            ".env": self.project_root / ".env",
            "frontend/.env.local": self.project_root / "frontend" / ".env.local",
            "frontend/.env.production": self.project_root / "frontend" / ".env.production"
        }
        
        all_valid = True
        
        for file_name, file_path in config_files.items():
            exists = file_path.exists()
            
            if exists:
                try:
                    content = file_path.read_text()
                    is_valid = len(content.strip()) > 0
                    
                    # Additional validation for specific files
                    if file_name == "vercel.json":
                        json.loads(content)  # Validate JSON
                    elif file_name == "requirements.txt":
                        is_valid = "fastapi" in content and "uvicorn" in content
                    elif ".env" in file_name:
                        is_valid = "=" in content
                    
                    self.log_test(
                        f"Config File: {file_name}",
                        is_valid,
                        "Valid configuration" if is_valid else "Invalid content"
                    )
                    
                    if not is_valid:
                        all_valid = False
                        
                except Exception as e:
                    self.log_test(
                        f"Config File: {file_name}",
                        False,
                        f"Parse error: {str(e)[:50]}"
                    )
                    all_valid = False
            else:
                self.log_test(
                    f"Config File: {file_name}",
                    False,
                    "File not found"
                )
                all_valid = False
        
        return all_valid

    async def run_all_tests(self):
        """Run all deployment tests"""
        print("🧪 Starting LogiVault AI Deployment Tests...")
        print("=" * 60)
        
        # Test configuration files
        print("\n📁 Testing Configuration Files...")
        self.test_configuration_files()
        
        # Test backend endpoints
        print("\n🔧 Testing Backend Services...")
        for backend_url in self.backend_urls:
            self.test_backend_health(backend_url)
            self.test_cors_headers(backend_url)
            self.test_api_endpoint(backend_url, "/generate")
            self.test_api_endpoint(backend_url, "/claude")
        
        # Test frontend accessibility
        print("\n🌐 Testing Frontend Services...")
        for frontend_url in self.frontend_urls:
            self.test_frontend_accessibility(frontend_url)
        
        # Test end-to-end flows
        print("\n🔄 Testing End-to-End Flows...")
        for backend_url in self.backend_urls:
            for frontend_url in self.frontend_urls:
                if "localhost" not in backend_url or "localhost" not in frontend_url:
                    await self.test_end_to_end_flow(backend_url, frontend_url)
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 DEPLOYMENT TEST SUMMARY")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {self.passed_tests}")
        print(f"❌ Tests Failed: {self.failed_tests}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        
        # Categorize results
        critical_failures = []
        warnings = []
        
        for result in self.test_results:
            if not result['passed']:
                if any(keyword in result['test'].lower() for keyword in ['health', 'cors', 'api endpoint']):
                    critical_failures.append(result)
                else:
                    warnings.append(result)
        
        if critical_failures:
            print(f"\n🚨 Critical Failures ({len(critical_failures)}):")
            for failure in critical_failures:
                print(f"   • {failure['test']}: {failure['message']}")
        
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"   • {warning['test']}: {warning['message']}")
        
        # Deployment status
        deployment_ready = len(critical_failures) == 0
        status = "✅ READY FOR PRODUCTION" if deployment_ready else "❌ NEEDS FIXES"
        print(f"\n🎯 Deployment Status: {status}")
        
        if deployment_ready:
            print("\n🚀 Recommended Actions:")
            print("   • Deploy frontend to logivault-ai.vercel.app")
            print("   • Deploy backend to Render with environment variables")
            print("   • Monitor application performance")
        else:
            print("\n🔧 Required Actions:")
            print("   • Fix critical failures listed above")
            print("   • Re-run tests after fixes")
            print("   • Verify CORS configuration")

if __name__ == "__main__":
    tester = DeploymentTester()
    
    # Run async tests
    try:
        asyncio.run(tester.run_all_tests())
        success = tester.failed_tests == 0
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        sys.exit(1)

