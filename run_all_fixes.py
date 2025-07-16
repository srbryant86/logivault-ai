#!/usr/bin/env python3
"""
LogiVault AI Master Fix Script
Orchestrates all deployment fixes and validations
"""

import subprocess
import sys
import time
from pathlib import Path

class MasterFixer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.scripts = [
            ("fix_deployment.py", "Apply deployment fixes"),
            ("deploy_to_vercel.py", "Setup Vercel deployment"),
            ("deploy_to_render.py", "Setup Render deployment"),
            ("verify_deployment.py", "Verify configuration"),
            ("test_deployment.py", "Test deployment")
        ]

    def log_info(self, message):
        print(f"ℹ️  {message}")

    def log_success(self, message):
        print(f"✅ {message}")

    def log_error(self, message):
        print(f"❌ {message}")

    def log_warning(self, message):
        print(f"⚠️  {message}")

    def run_script(self, script_name: str, description: str) -> bool:
        """Run a script and return success status"""
        script_path = self.project_root / script_name
        
        if not script_path.exists():
            self.log_error(f"Script not found: {script_name}")
            return False

        self.log_info(f"Running: {description}")
        print("-" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=self.project_root, check=False)
            
            if result.returncode == 0:
                self.log_success(f"Completed: {description}")
                return True
            else:
                self.log_error(f"Failed: {description} (exit code: {result.returncode})")
                return False
                
        except Exception as e:
            self.log_error(f"Error running {script_name}: {e}")
            return False

    def create_summary_report(self, results: dict):
        """Create a summary report of all fixes"""
        report_content = f"""# LogiVault AI Deployment Fix Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Fix Results Summary

"""
        
        for script, (description, success) in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            report_content += f"- **{description}**: {status}\n"
        
        report_content += f"""

## Next Steps

### If All Fixes Succeeded:
1. **Commit Changes**: `git add . && git commit -m "Apply automated deployment fixes"`
2. **Push to GitHub**: `git push origin main`
3. **Deploy Frontend**: 
   - Go to Vercel dashboard
   - Create new project: `logivault-ai`
   - Connect to GitHub repository
   - Deploy with environment variables
4. **Deploy Backend**:
   - Go to Render dashboard
   - Create new Web Service
   - Connect to GitHub repository
   - Set environment variables (CLAUDE_API_KEY)
5. **Test Application**: Visit deployed URLs and test functionality

### If Some Fixes Failed:
1. Review error messages above
2. Fix issues manually
3. Re-run specific scripts: `python3 script_name.py`
4. Re-run this master script: `python3 run_all_fixes.py`

## Configuration Files Created:
- `vercel.json` - Vercel deployment configuration
- `render.yaml` - Render deployment configuration  
- `requirements.txt` - Python dependencies
- `.env.production` - Production environment variables
- `start.sh` - Backend startup script
- `DEPLOYMENT.md` - Deployment guide

## URLs to Configure:
- **Frontend**: https://logivault-ai.vercel.app
- **Backend**: https://logivault-ai-backend.onrender.com

## Environment Variables Required:
- **Backend (Render)**: `CLAUDE_API_KEY`
- **Frontend (Vercel)**: `REACT_APP_API_URL=https://logivault-ai-backend.onrender.com`

## Testing Commands:
- Health check: `curl https://logivault-ai-backend.onrender.com/healthz`
- API test: `curl -X POST https://logivault-ai-backend.onrender.com/generate -H "Content-Type: application/json" -d '{{"prompt":"test"}}'`
"""
        
        try:
            report_path = self.project_root / "DEPLOYMENT_REPORT.md"
            with open(report_path, 'w') as f:
                f.write(report_content)
            self.log_success("Created DEPLOYMENT_REPORT.md")
        except Exception as e:
            self.log_error(f"Failed to create report: {e}")

    def run_all_fixes(self):
        """Run all deployment fixes"""
        print("🚀 LogiVault AI Master Deployment Fix")
        print("=" * 60)
        print("This script will run all automated fixes for LogiVault AI deployment issues.")
        print("=" * 60)
        
        results = {}
        overall_success = True
        
        for script_name, description in self.scripts:
            print(f"\n📋 Step: {description}")
            success = self.run_script(script_name, description)
            results[script_name] = (description, success)
            
            if not success:
                overall_success = False
                self.log_warning("Continuing with remaining fixes...")
            
            time.sleep(1)  # Brief pause between scripts
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 MASTER FIX SUMMARY")
        print("=" * 60)
        
        successful_fixes = sum(1 for _, (_, success) in results.items() if success)
        total_fixes = len(results)
        
        print(f"✅ Successful Fixes: {successful_fixes}/{total_fixes}")
        print(f"❌ Failed Fixes: {total_fixes - successful_fixes}/{total_fixes}")
        
        if overall_success:
            print("\n🎉 ALL FIXES COMPLETED SUCCESSFULLY!")
            print("\n🎯 Next Steps:")
            print("   1. Review DEPLOYMENT_REPORT.md")
            print("   2. Commit and push changes to GitHub")
            print("   3. Deploy to Vercel and Render")
            print("   4. Test the deployed application")
        else:
            print("\n⚠️  SOME FIXES FAILED")
            print("\n🔧 Required Actions:")
            print("   1. Review error messages above")
            print("   2. Fix issues manually")
            print("   3. Re-run failed scripts individually")
            print("   4. Re-run this master script")
        
        # Create detailed report
        self.create_summary_report(results)
        
        return overall_success

if __name__ == "__main__":
    fixer = MasterFixer()
    success = fixer.run_all_fixes()
    sys.exit(0 if success else 1)

