from fastapi import FastAPI, Request
from backend.claude_api import call_claude
import os

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/claude")
async def claude(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided."}
    response = await call_claude(prompt)
    return {"response": response}
