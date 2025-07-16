import subprocess
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("[INIT] Launching Logivault AI local test...")

# Ensure Claude API Key is set
claude_key = os.getenv("CLAUDE_API_KEY")
if not claude_key or not claude_key.startswith("sk-ant-"):
    raise EnvironmentError("Missing or invalid CLAUDE_API_KEY in .env")

# Try different app directories to handle common import issues
backend_targets = [
    ["uvicorn", "backend.main:app", "--reload", "--app-dir", "./"],
    ["uvicorn", "main:app", "--reload", "--app-dir", "./backend"]
]

server_process = None
for cmd in backend_targets:
    try:
        print("[STEP] Trying server start:", " ".join(cmd))
        server_process = subprocess.Popen(cmd)
        time.sleep(4)
        break
    except Exception as e:
        print("[ERROR] Failed to start with:", cmd, "Error:", e)

if not server_process:
    raise RuntimeError("Failed to launch Uvicorn with any fallback paths.")

try:
    print("[HEALTHZ] Checking /healthz...")
    health = requests.get("http://127.0.0.1:8000/healthz")
    print(f"[HEALTHZ] {health.status_code} – {health.text}")

    print("[CLAUDE TEST] Sending prompt...")
    test_payload = {
        "prompt": "Stoicism teaches resilience through acceptance of what we cannot control."
    }
    claude = requests.post("http://127.0.0.1:8000/claude", json=test_payload)
    print(f"[CLAUDE] {claude.status_code} – {claude.text}")

finally:
    input("[DONE] Press Enter to shut down server...")
    if server_process:
        server_process.terminate()