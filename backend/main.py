from fastapi import FastAPI, Request
from backend.claude_api import call_claude
import os

app = FastAPI()

<<<<<<< HEAD
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

=======
>>>>>>> 919e917761a526ae56f2f900d0c0f81616ec577b
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
