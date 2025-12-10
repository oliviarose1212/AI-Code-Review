# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(title="AI Code Review - Backend", version="0.1.0")

@app.get("/health")
async def health():
    """
    Simple health endpoint
    """
    return {"status": "ok"}
