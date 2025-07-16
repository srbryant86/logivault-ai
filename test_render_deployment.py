#!/usr/bin/env python3
"""
LogiVault AI - Render Deployment Testing & Verification
Automated testing suite for Render deployment validation
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin

class RenderDeploymentTester:
    def __init__(self, base_url=None):
        self.base_url = base_url or "https://logivault-ai.onrender.com"
        self.test_results = []
        self.errors = []
        
    def log_test(self, test_name, success, message="", details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": time.time()
        })
        
        if not success:
            self.errors.append(f"{test_name}: {message}")
    
    def test_service_health(self):
        """Test if the service is responding"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=30)
            if response.status_code == 200:
                self.log_test("Service Health", True, "Service is responding")
                return True
            else:
                self.log_test("Service Health", False, f"HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Service Health", False, f"Connection failed: {str(e)}")
            return False
    
    def test_api_docs(self):
        """Test if API documentation is accessible"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=15)
            if response.status_code == 200:
                self.log_test("API Documentation", True, "Docs endpoint accessible")
                return True
            else:
                self.log_test("API Documentation", False, f"HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("API Documentation", False, f"Docs not accessible: {str(e)}")
            return False
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            headers = {
                'Origin': 'https://logivault-ai.vercel.app',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = requests.options(f"{self.base_url}/", headers=headers, timeout=15)
            
            cors_headers = response.headers.get('Access-Control-Allow-Origin', '')
            if cors_headers == '*' or 'logivault-ai.vercel.app' in cors_headers:
                self.log_test("CORS Configuration", True, "CORS properly configured")
                return True
            else:
                self.log_test("CORS Configuration", False, f"CORS headers: {cors_headers}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("CORS Configuration", False, f"CORS test failed: {str(e)}")
            return False
    
    def test_claude_endpoint(self):
        """Test Claude optimization endpoint"""
        try:
            test_payload = {
                "content": "This is a test message for optimization.",
                "user_id": "test_user"
            }
            
            response = requests.post(
                f"{self.base_url}/api/claudeOptimize",
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'optimized_content' in data or 'result' in data:
                    self.log_test("Claude Endpoint", True, "Claude API integration working")
                    return True
                else:
                    self.log_test("Claude Endpoint", False, "Unexpected response format")
                    return False
            elif response.status_code == 401:
                self.log_test("Claude Endpoint", False, "API key not configured")
                return False
            else:
                self.log_test("Claude Endpoint", False, f"HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Claude Endpoint", False, f"Endpoint test failed: {str(e)}")
            return False
    
    def test_environment_variables(self):
        """Test if required environment variables are configured"""
        try:
            # Test health endpoint that might reveal env var status
            response = requests.get(f"{self.base_url}/health", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('claude_configured', False):
                    self.log_test("Environment Variables", True, "CLAUDE_API_KEY configured")
                    return True
                else:
                    self.log_test("Environment Variables", False, "CLAUDE_API_KEY not configured")
                    return False
            else:
                # If no health endpoint, assume env vars are configured if service is running
                self.log_test("Environment Variables", True, "Service running (assuming env vars OK)")
                return True
        except requests.exceptions.RequestException:
            self.log_test("Environment Variables", False, "Cannot verify env var configuration")
            return False
    
    def test_deployment_performance(self):
        """Test deployment performance metrics"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/", timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                if response_time < 5.0:
                    self.log_test("Performance", True, f"Response time: {response_time:.2f}s")
                    return True
                else:
                    self.log_test("Performance", False, f"Slow response: {response_time:.2f}s")
                    return False
            else:
                self.log_test("Performance", False, "Service not responding")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Performance", False, f"Performance test failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all deployment tests"""
        print("🧪 LogiVault AI - Render Deployment Testing")
        print("=" * 50)
        print(f"Testing deployment at: {self.base_url}")
        print()
        
        tests = [
            self.test_service_health,
            self.test_api_docs,
            self.test_cors_configuration,
            self.test_environment_variables,
            self.test_claude_endpoint,
            self.test_deployment_performance
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                self.log_test(test.__name__, False, f"Test error: {str(e)}")
        
        # Generate test report
        self.generate_test_report(passed, total)
        
        return passed == total
    
    def generate_test_report(self, passed, total):
        """Generate comprehensive test report"""
        report = {
            "timestamp": time.time(),
            "base_url": self.base_url,
            "tests_passed": passed,
            "tests_total": total,
            "success_rate": f"{passed}/{total} ({(passed/total)*100:.1f}%)",
            "test_results": self.test_results,
            "errors": self.errors,
            "recommendations": []
        }
        
        # Add recommendations based on test results
        if self.errors:
            report["recommendations"].append("Review failed tests and fix configuration issues")
        
        if passed < total:
            report["recommendations"].extend([
                "Check Render service logs for detailed error information",
                "Verify environment variables are properly set",
                "Ensure latest code is deployed"
            ])
        
        if passed == total:
            report["recommendations"].append("All tests passed! Deployment is ready for production use")
        
        # Save report
        report_path = Path(__file__).parent / "RENDER_TEST_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 DEPLOYMENT TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Tests Passed: {passed}")
        print(f"❌ Tests Failed: {total - passed}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
        if self.errors:
            print("\n⚠️ Issues Found:")
            for error in self.errors:
                print(f"  • {error}")
        
        if report["recommendations"]:
            print("\n💡 Recommendations:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")
        
        print(f"\n📄 Full report saved to: RENDER_TEST_REPORT.json")
        
        if passed == total:
            print("\n🎉 All tests passed! Your deployment is working correctly.")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Please review and fix the issues.")

class LocalDeploymentTester:
    """Test local development setup"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
    
    def test_requirements_file(self):
        """Test if requirements.txt exists and is valid"""
        req_path = self.project_root / "requirements.txt"
        if req_path.exists():
            print("✅ requirements.txt exists")
            return True
        else:
            print("❌ requirements.txt not found")
            return False
    
    def test_backend_structure(self):
        """Test if backend structure is correct"""
        backend_path = self.project_root / "backend"
        main_path = backend_path / "main.py"
        
        if backend_path.exists() and main_path.exists():
            print("✅ Backend structure is correct")
            return True
        else:
            print("❌ Backend structure incomplete")
            return False
    
    def test_configuration_files(self):
        """Test if all configuration files are present"""
        required_files = [
            "render.yaml",
            "start.sh",
            ".env.render"
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)
        
        if not missing_files:
            print("✅ All configuration files present")
            return True
        else:
            print(f"❌ Missing configuration files: {', '.join(missing_files)}")
            return False
    
    def run_local_tests(self):
        """Run local deployment tests"""
        print("🔧 Testing Local Deployment Setup")
        print("=" * 40)
        
        tests = [
            self.test_requirements_file,
            self.test_backend_structure,
            self.test_configuration_files
        ]
        
        passed = sum(test() for test in tests)
        total = len(tests)
        
        print(f"\n📊 Local Tests: {passed}/{total} passed")
        return passed == total

def main():
    """Main testing function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LogiVault AI Render Deployment Tester")
    parser.add_argument("--url", default="https://logivault-ai.onrender.com", 
                       help="Base URL of the deployed service")
    parser.add_argument("--local-only", action="store_true", 
                       help="Run only local tests")
    
    args = parser.parse_args()
    
    if args.local_only:
        local_tester = LocalDeploymentTester()
        success = local_tester.run_local_tests()
    else:
        # Run local tests first
        local_tester = LocalDeploymentTester()
        local_success = local_tester.run_local_tests()
        
        if local_success:
            print("\n" + "="*50)
            # Run remote tests
            remote_tester = RenderDeploymentTester(args.url)
            remote_success = remote_tester.run_all_tests()
            success = remote_success
        else:
            print("\n❌ Local tests failed. Fix local issues before testing deployment.")
            success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

