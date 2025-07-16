from fastapi import FastAPI, Request, HTTPException
import os, time
import httpx
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

load_dotenv()
app = FastAPI()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# ========== RATE LIMIT CONFIG ==========
RATE_LIMIT = 10  # max requests
RATE_WINDOW = 60  # seconds

client_access_log = defaultdict(lambda: {"tokens": RATE_LIMIT, "timestamp": time.time()})

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = request.client.host
    record = client_access_log[ip]
    now = time.time()
    elapsed = now - record["timestamp"]
    # refill tokens
    refill = (elapsed / RATE_WINDOW) * RATE_LIMIT
    record["tokens"] = min(RATE_LIMIT, record["tokens"] + refill)
    record["timestamp"] = now

    if record["tokens"] < 1:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please slow down.")
    
    record["tokens"] -= 1
    return await call_next(request)

# ========== ROUTES ==========

@app.post("/claude")
async def claude_handler(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

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

    retries = 3
    backoff = 1
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload
                )
                result = response.json()
                return {"reply": result.get("content", [{}])[0].get("text", "Error")}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(backoff)
                backoff *= 2
            else:
                raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Claude backend is live"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
