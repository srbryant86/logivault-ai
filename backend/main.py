from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.claude_api import call_claude
from backend.routes.optimization import router as optimization_router
from backend.routes.certnode_integration import router as certnode_router
import os

app = FastAPI(title="LogiVault API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://logivault.ai",
        "https://www.logivault.ai",
        "https://logivault-ai.vercel.app",
        "https://logivault-ai-*.vercel.app", 
        "https://steven-bryants-projects.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(optimization_router)
app.include_router(certnode_router)

@app.get("/")
def root():
    return {"message": "LogiVault API is running", "version": "1.0.0"}

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

