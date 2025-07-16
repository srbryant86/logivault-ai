from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.claude_api import call_claude
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://logivault-ai.vercel.app",
        "https://logivault-ai-*.vercel.app", 
        "https://steven-bryants-projects.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/claude")
async def claude(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided.")
    response = await call_claude(prompt)
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    return {"response": response}

@app.post("/generate")
async def generate(request: Request):
    """Generate endpoint that matches frontend expectations"""
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided.")
    response = await call_claude(prompt)
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    # Return format that matches frontend expectations (raw.content)
    return {"content": response}
