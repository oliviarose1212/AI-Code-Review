import os
import time
import jwt
import httpx
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))
from pathlib import Path



GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
INSTALLATION_ID = os.getenv("GITHUB_INSTALLATION_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")


def generate_jwt():
    now = int(time.time())

    payload = {
        "iat": now,           # issued at time (now)
        "exp": now + 540,     # expires in 9 minutes (540 seconds)
        "iss": GITHUB_APP_ID, # GitHub App ID
    }

    private_key = Path(PRIVATE_KEY_PATH).read_text()

    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )

    return token



def get_installation_access_token():
    """
    Exchange a JWT for an installation access token.
    This token is used to make GitHub API calls.
    """
    jwt_token = generate_jwt()

    url = f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens"

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    response = httpx.post(url, headers=headers)

    if response.status_code != 201:
        print("Error fetching token:", response.text)
        raise Exception("Could not get access token")

    data = response.json()
    return data["token"]
