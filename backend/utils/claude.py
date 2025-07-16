# backend/utils/claude.py

import httpx
import os

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Make sure this exists in your .env

headers = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json",
}

BASE_SYSTEM_PROMPT = "You are a professional content editor. Improve clarity, tone, and engagement while preserving meaning."
FALLBACK_PROMPT = "Be aggressive. Strip fluff, boost readability, and maximize impact."

async def call_claude(prompt: str) -> str:
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "temperature": 0.7,
        "system": BASE_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
    except Exception:
        # Fallback modifier
        payload["system"] = FALLBACK_PROMPT
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["content"][0]["text"]
        except Exception as fallback_error:
            return f"[Claude error]: {str(fallback_error)}"