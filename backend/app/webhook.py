import os
import hmac
import hashlib
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter()

def verify_signature(secret: str, payload: bytes, signature: str) -> bool:
    """
    Validates GitHub webhook HMAC SHA-256 signature.

    GitHub sends header:
    X-Hub-Signature-256: sha256=<hash>

    We must compute our own hash using the webhook secret.
    """
    if signature is None:
        return False

    mac = hmac.new(secret.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()

    # timing attack–safe comparison
    return hmac.compare_digest(expected, signature)


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None)
):
    # Read raw request body bytes
    body = await request.body()

    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if secret is None:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    # 1️⃣ Signature validation
    if not verify_signature(secret, body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 2️⃣ Determine which event this is
    event = request.headers.get("X-GitHub-Event")
    
    # 3️⃣ Load the JSON payload
    payload = await request.json()

    # 4️⃣ Debug print (remove in production)
    print(f"Received event: {event}")
    print(payload)

    # 5️⃣ Later we will enqueue Celery task here
    # e.g. analyze_pr_task.delay(...)

    return {"status": "ok"}
