#!/usr/bin/env python3
"""
Self-Healer Installation Script
Sets up the autonomous self-healing system as a background service
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command):
    """Run command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        "requests",
        "schedule", 
        "psutil"
    ]
    
    for package in packages:
        success, stdout, stderr = run_command(f"pip3 install {package}")
        if success:
            print(f"✅ Installed {package}")
        else:
            print(f"⚠️  Failed to install {package}: {stderr}")

def create_systemd_service():
    """Create systemd service for autonomous mode"""
    service_content = f"""[Unit]
Description=LogiVault AI Self-Healer
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={Path.cwd()}
ExecStart=/usr/bin/python3 {Path.cwd()}/auto-resolver/autonomous_self_healer.py --autonomous
Restart=always
RestartSec=10
Environment=PATH=/usr/bin:/usr/local/bin
Environment=PYTHONPATH={Path.cwd()}

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "/etc/systemd/system/logivault-healer.service"
    
    try:
        # Write service file (requires sudo)
        with open("/tmp/logivault-healer.service", "w") as f:
            f.write(service_content)
        
        success, _, stderr = run_command(f"sudo mv /tmp/logivault-healer.service {service_file}")
        if success:
            print(f"✅ Created systemd service: {service_file}")
            
            # Enable and start service
            run_command("sudo systemctl daemon-reload")
            run_command("sudo systemctl enable logivault-healer")
            
            print("🚀 Self-healer service installed and enabled")
            print("Use these commands to control it:")
            print("  sudo systemctl start logivault-healer    # Start")
            print("  sudo systemctl stop logivault-healer     # Stop") 
            print("  sudo systemctl status logivault-healer   # Check status")
            print("  sudo journalctl -u logivault-healer -f   # View logs")
            
        else:
            print(f"❌ Failed to create service: {stderr}")
            
    except Exception as e:
        print(f"❌ Service creation failed: {e}")

def create_cron_job():
    """Create cron job as alternative to systemd"""
    print("📅 Setting up cron job...")
    
    cron_entry = f"*/30 * * * * cd {Path.cwd()} && /usr/bin/python3 auto-resolver/autonomous_self_healer.py >> self_healer_cron.log 2>&1"
    
    # Add to crontab
    success, stdout, stderr = run_command(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -')
    
    if success:
        print("✅ Cron job created - self-healer will run every 30 minutes")
    else:
        print(f"⚠️  Cron job creation failed: {stderr}")

def create_startup_scripts():
    """Create convenient startup scripts"""
    
    # One-time fix script
    oneshot_script = f"""#!/bin/bash
cd {Path.cwd()}
python3 auto-resolver/autonomous_self_healer.py
"""
    
    with open("fix_now.sh", "w") as f:
        f.write(oneshot_script)
    os.chmod("fix_now.sh", 0o755)
    
    # Start autonomous mode script
    autonomous_script = f"""#!/bin/bash
cd {Path.cwd()}
echo "🤖 Starting Autonomous Self-Healer..."
echo "Press Ctrl+C to stop"
python3 auto-resolver/autonomous_self_healer.py --autonomous
"""
    
    with open("start_autonomous.sh", "w") as f:
        f.write(autonomous_script)
    os.chmod("start_autonomous.sh", 0o755)
    
    print("✅ Created startup scripts:")
    print("  ./fix_now.sh           # Run one-time fix")
    print("  ./start_autonomous.sh  # Start autonomous mode")

def create_configuration():
    """Create configuration file"""
    config = {
        "monitoring": {
            "check_interval_minutes": 5,
            "services_to_monitor": [
                "https://logivault-ai.vercel.app",
                "https://logivault-ai-backend.onrender.com/healthz"
            ]
        },
        "healing": {
            "max_retries": 5,
            "retry_delay_minutes": 2,
            "auto_deploy": True
        },
        "maintenance": {
            "daily_check_time": "02:00",
            "log_rotation_size_mb": 10,
            "cleanup_old_files": True
        }
    }
    
    import json
    with open("auto-resolver/healer_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created configuration file")

def main():
    """Main installation process"""
    print("🚀 Installing LogiVault AI Self-Healer")
    print("=" * 50)
    
    # Check if running as root for systemd service
    is_root = os.geteuid() == 0
    
    # Install dependencies
    install_dependencies()
    
    # Create configuration
    create_configuration()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Try to create systemd service (preferred)
    if shutil.which("systemctl"):
        create_systemd_service()
    else:
        print("⚠️  systemctl not available, using cron instead")
        create_cron_job()
    
    print("\n" + "=" * 50)
    print("✅ Self-Healer Installation Complete!")
    print("\n🎯 Quick Start Options:")
    print("1. Run immediate fix:     ./fix_now.sh")
    print("2. Start autonomous mode: ./start_autonomous.sh")
    print("3. Install as service:    sudo systemctl start logivault-healer")
    print("\n🤖 The self-healer will:")
    print("  • Monitor your services 24/7")
    print("  • Automatically fix deployment issues")
    print("  • Self-heal without any intervention")
    print("  • Keep logs of all actions taken")
    print("\n📋 No further action required - it's fully autonomous!")

if __name__ == "__main__":
    main()

