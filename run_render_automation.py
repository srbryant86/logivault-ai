#!/usr/bin/env python3
"""
LogiVault AI - Master Render Deployment Automation
Runs all automated fixes and configurations for Render deployment
"""

import subprocess
import sys
import json
import time
from pathlib import Path

class RenderAutomationRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.results = {
            "timestamp": time.time(),
            "steps_completed": [],
            "errors": [],
            "success": False
        }
    
    def log_step(self, step, success, message=""):
        """Log automation step"""
        status = "✅" if success else "❌"
        print(f"{status} {step}: {message}")
        
        self.results["steps_completed"].append({
            "step": step,
            "success": success,
            "message": message,
            "timestamp": time.time()
        })
        
        if not success:
            self.results["errors"].append(f"{step}: {message}")
    
    def run_deployment_fixer(self):
        """Run the main deployment fixer"""
        try:
            print("🔧 Running Render Deployment Fixer...")
            result = subprocess.run([
                sys.executable, "fix_render_deployment.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_step("Deployment Fixer", True, "Configuration fixes applied")
                return True
            else:
                self.log_step("Deployment Fixer", False, f"Exit code: {result.returncode}")
                print(f"Error output: {result.stderr}")
                return False
        except Exception as e:
            self.log_step("Deployment Fixer", False, f"Exception: {str(e)}")
            return False
    
    def run_config_generator(self):
        """Run the configuration generator"""
        try:
            print("⚙️ Running Configuration Generator...")
            result = subprocess.run([
                sys.executable, "render_config_generator.py"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_step("Config Generator", True, "Configuration files generated")
                return True
            else:
                self.log_step("Config Generator", False, f"Exit code: {result.returncode}")
                print(f"Error output: {result.stderr}")
                return False
        except Exception as e:
            self.log_step("Config Generator", False, f"Exception: {str(e)}")
            return False
    
    def run_local_tests(self):
        """Run local deployment tests"""
        try:
            print("🧪 Running Local Tests...")
            result = subprocess.run([
                sys.executable, "test_render_deployment.py", "--local-only"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_step("Local Tests", True, "All local tests passed")
                return True
            else:
                self.log_step("Local Tests", False, "Some local tests failed")
                print(f"Test output: {result.stdout}")
                return False
        except Exception as e:
            self.log_step("Local Tests", False, f"Exception: {str(e)}")
            return False
    
    def commit_changes(self):
        """Commit changes to git"""
        try:
            print("📝 Committing Changes to Git...")
            
            # Add all changes
            result = subprocess.run([
                "git", "add", "."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode != 0:
                self.log_step("Git Add", False, "Failed to add files")
                return False
            
            # Commit changes
            result = subprocess.run([
                "git", "commit", "-m", "Automated Render deployment fixes and optimizations"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_step("Git Commit", True, "Changes committed successfully")
                return True
            elif "nothing to commit" in result.stdout:
                self.log_step("Git Commit", True, "No changes to commit")
                return True
            else:
                self.log_step("Git Commit", False, f"Commit failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_step("Git Commit", False, f"Exception: {str(e)}")
            return False
    
    def push_changes(self):
        """Push changes to GitHub"""
        try:
            print("🚀 Pushing Changes to GitHub...")
            result = subprocess.run([
                "git", "push", "origin", "main"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_step("Git Push", True, "Changes pushed to GitHub")
                return True
            else:
                self.log_step("Git Push", False, f"Push failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_step("Git Push", False, f"Exception: {str(e)}")
            return False
    
    def generate_final_report(self):
        """Generate final automation report"""
        successful_steps = sum(1 for step in self.results["steps_completed"] if step["success"])
        total_steps = len(self.results["steps_completed"])
        
        self.results["success"] = len(self.results["errors"]) == 0
        self.results["success_rate"] = f"{successful_steps}/{total_steps}"
        
        # Save detailed report
        report_path = self.project_root / "RENDER_AUTOMATION_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Generate summary
        summary = f"""
# LogiVault AI - Render Deployment Automation Summary

## Results
- **Success Rate**: {self.results['success_rate']}
- **Overall Status**: {'✅ SUCCESS' if self.results['success'] else '❌ FAILED'}
- **Timestamp**: {time.ctime(self.results['timestamp'])}

## Steps Completed
"""
        
        for step in self.results["steps_completed"]:
            status = "✅" if step["success"] else "❌"
            summary += f"- {status} **{step['step']}**: {step['message']}\n"
        
        if self.results["errors"]:
            summary += "\n## Errors Encountered\n"
            for error in self.results["errors"]:
                summary += f"- ❌ {error}\n"
        
        summary += f"""
## Next Steps

### If All Steps Succeeded:
1. Go to your Render dashboard
2. Your service should automatically redeploy with the new configuration
3. Monitor the deployment logs
4. Test your application once deployment completes

### If Some Steps Failed:
1. Review the errors above
2. Check the detailed report: `RENDER_AUTOMATION_REPORT.json`
3. Fix any issues manually
4. Re-run the automation: `python run_render_automation.py`

### Manual Render Configuration (if needed):
1. **Build Command**: `pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt`
2. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1`
3. **Environment Variables**: Add `CLAUDE_API_KEY` with your API key

## Testing Your Deployment
Run the deployment tester:
```bash
python test_render_deployment.py
```

---
Generated by LogiVault AI Automated Deployment System
"""
        
        summary_path = self.project_root / "RENDER_AUTOMATION_SUMMARY.md"
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        return summary_path
    
    def run_full_automation(self):
        """Run the complete automation process"""
        print("🤖 LogiVault AI - Render Deployment Automation")
        print("=" * 60)
        print("This will automatically fix your Render deployment issues")
        print("=" * 60)
        print()
        
        # Run automation steps
        steps = [
            ("Deployment Fixes", self.run_deployment_fixer),
            ("Configuration Generation", self.run_config_generator),
            ("Local Testing", self.run_local_tests),
            ("Git Commit", self.commit_changes),
            ("Git Push", self.push_changes)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            success = step_func()
            if not success:
                print(f"⚠️ {step_name} failed, but continuing...")
        
        # Generate final report
        print("\n📊 Generating Final Report...")
        summary_path = self.generate_final_report()
        
        # Print final summary
        print("\n" + "=" * 60)
        print("🎯 AUTOMATION COMPLETE")
        print("=" * 60)
        
        successful_steps = sum(1 for step in self.results["steps_completed"] if step["success"])
        total_steps = len(self.results["steps_completed"])
        
        print(f"✅ Steps Completed: {successful_steps}/{total_steps}")
        
        if self.results["errors"]:
            print(f"❌ Errors: {len(self.results['errors'])}")
            print("\nErrors encountered:")
            for error in self.results["errors"]:
                print(f"  • {error}")
        
        print(f"\n📄 Detailed report: RENDER_AUTOMATION_REPORT.json")
        print(f"📋 Summary: RENDER_AUTOMATION_SUMMARY.md")
        
        if self.results["success"]:
            print("\n🎉 All automation steps completed successfully!")
            print("Your Render deployment should now work correctly.")
        else:
            print("\n⚠️ Some steps failed. Please review the errors and fix manually.")
        
        print("\n🧪 Test your deployment:")
        print("python test_render_deployment.py")
        
        return self.results["success"]

def main():
    """Main automation function"""
    automation = RenderAutomationRunner()
    success = automation.run_full_automation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

