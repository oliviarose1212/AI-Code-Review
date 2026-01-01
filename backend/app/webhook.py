import os
import hmac
import hashlib
from fastapi import APIRouter, Header, HTTPException, Request

from backend.app.pr_review_service import run_pr_review

router = APIRouter()


def verify_signature(secret: str, payload: bytes, signature: str) -> bool:
    mac = hmac.new(secret.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
):
    body = await request.body()

    if not verify_signature(
        os.getenv("GITHUB_WEBHOOK_SECRET"),
        body,
        x_hub_signature_256,
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    # We only care about PR events
    if event == "pull_request":
        action = payload.get("action")

        if action in ("opened", "synchronize", "reopened"):
            pr_number = payload["number"]
            repo = payload["repository"]["name"]
            owner = payload["repository"]["owner"]["login"]

            # 🔥 AUTOMATION HAPPENS HERE
            run_pr_review(owner, repo, pr_number)

    return {"status": "ok"}
