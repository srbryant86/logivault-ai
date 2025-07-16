from fastapi import FastAPI, Request
import os
import httpx
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI()

# Logging Setup
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "claude.log"

file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Load Claude API key
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

@app.post("/claude")
async def claude_handler(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    logger.info(f"Incoming prompt: {prompt}")

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Claude response: {result}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Claude: {e.response.text}")
        return {"error": e.response.text}
    except Exception as e:
        logger.exception("Unexpected error calling Claude API")
        return {"error": "Internal server error"}

    return {"reply": result.get("content", [{}])[0].get("text", "Error")}

@app.get("/")
def root():
    return {"message": "Claude backend is online"}

@app.get("/status")
def status():
    return {"message": "Claude API is live"}
