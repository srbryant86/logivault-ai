from fastapi import FastAPI, Request
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

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
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers=headers
        )

    result = response.json()
    return {"reply": result.get("content", [{}])[0].get("text", "No response")}
