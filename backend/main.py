from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import asyncio
import time
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from collections import defaultdict

app = FastAPI()

# === CORS Setup ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Token Bucket for IP Rate Limiting ===
rate_limits = defaultdict(lambda: {"tokens": 5, "last": time.time()})
def token_bucket(ip: str):
    bucket = rate_limits[ip]
    now = time.time()
    elapsed = now - bucket["last"]
    bucket["last"] = now
    bucket["tokens"] = min(5, bucket["tokens"] + elapsed * 0.2)  # 1 token per 5s
    if bucket["tokens"] >= 1:
        bucket["tokens"] -= 1
        return True
    return False

# === Claude Proxy Route ===
@app.post("/claude")
async def claude(request: Request):
    ip = request.client.host
    if not token_bucket(ip):
        raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return JSONResponse(content={"error": "Missing prompt"}, status_code=400)

    # === Logging ===
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] IP: {ip} | Prompt len: {len(prompt)}")

    # === Claude API Call ===
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            for attempt in range(5):
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": "YOUR_CLAUDE_API_KEY",
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "max_tokens": 500,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                )
                if response.status_code == 200:
                    return response.json()
                await asyncio.sleep(2 ** attempt)  # exponential backoff
            return JSONResponse(content={"error": "Claude API failed after retries"}, status_code=502)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# === Uptime & Root Check ===
@app.get("/")
def root():
    return {"message": "Claude backend is live"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
