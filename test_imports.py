
import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import uvicorn
    print(f"✅ Uvicorn: {uvicorn.__version__}")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

try:
    import anthropic
    print(f"✅ Anthropic: {anthropic.__version__}")
except ImportError as e:
    print(f"❌ Anthropic import failed: {e}")

try:
    from backend.main import app
    print("✅ Backend main app imported successfully")
except ImportError as e:
    print(f"❌ Backend main import failed: {e}")
