# webhook test commit
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))
from fastapi import FastAPI
from backend.app.webhook import router as webhook_router   # <-- FIXED IMPORT

app = FastAPI(title="AI Code Review Backend")
print("This is a test PR")
app.include_router(webhook_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
