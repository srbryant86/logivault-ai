import json
import os
from datetime import datetime

LOG_FILE = "data/sessions.json"  # Create this folder if needed

def log_session(data: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": data.get("prompt"),
        "originalOutput": data.get("originalOutput"),
        "optimizedOutput": data.get("optimizedOutput"),
        "metrics": data.get("metrics"),
        "contentType": data.get("contentType", "Generic"),
        "retryCount": data.get("retryCount", 0),
        "userId": data.get("userId", "anon")
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    try:
        # Append session to file
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r+") as f:
                sessions = json.load(f)
                sessions.append(entry)
                f.seek(0)
                json.dump(sessions, f, indent=2)
        else:
            with open(LOG_FILE, "w") as f:
                json.dump([entry], f, indent=2)

        print(f"✅ Session logged: {entry['timestamp']}")
    except Exception as e:
        print(f"❌ Failed to log session: {str(e)}")