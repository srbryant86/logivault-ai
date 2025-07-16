
import subprocess
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000/claude"
HEALTH_URL = "http://127.0.0.1:8000/healthz"
PROMPT = "Summarize Stoicism in 1 sentence."

def try_server_start(commands):
    for cmd in commands:
        try:
            print(f"[STEP] Trying server start: {' '.join(cmd)}")
            server_process = subprocess.Popen(["python", "-m"] + cmd)
            return server_process
        except Exception as e:
            print(f"[ERROR] Failed to start with: {cmd} Error: {e}")
    raise RuntimeError("Failed to launch Uvicorn with any fallback paths.")

print("[INIT] Launching Logivault AI local test...")

if not os.getenv("CLAUDE_API_KEY"):
    raise EnvironmentError("CLAUDE_API_KEY not found in .env file.")

commands_to_try = [
    ["uvicorn", "backend.main:app", "--reload", "--app-dir", "./"],
    ["uvicorn", "main:app", "--reload", "--app-dir", "./backend"],
]

server_process = try_server_start(commands_to_try)

try:
    time.sleep(3)
    print("[HEALTHZ]", end=" ")
    res = requests.get(HEALTH_URL)
    print(res.status_code, "–", res.text)

    print("[CLAUDE TEST] Sending prompt...")
    res = requests.post(API_URL, json={"prompt": PROMPT})
    print("[CLAUDE]", res.status_code, "–", res.text)
finally:
    input("[DONE] Press Enter to shut down server...")
    server_process.terminate()
