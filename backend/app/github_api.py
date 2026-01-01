import httpx
from backend.app.github_auth import get_installation_access_token


def github_request(method, url, **kwargs):
    token = get_installation_access_token()

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"token {token}"
    headers["Accept"] = "application/vnd.github+json"

    with httpx.Client(timeout=20.0) as client:
        response = client.request(
            method,
            url,
            headers=headers,
            **kwargs
        )

    if response.status_code >= 400:
        print("GitHub API Error:", response.text)

    return response

def get_pr_files(owner, repo, pr_number):
    """
    Fetch list of files changed in a PR
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = github_request("GET", url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {response.text}")

    return response.json()

def get_file_content(owner, repo, file_path, ref):
    """
    Fetch full file contents from GitHub using the repo contents API.
    ref = commit SHA (head_sha)
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={ref}"

    response = github_request("GET", url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch file content: {response.text}")

    data = response.json()

    # GitHub sends file content in base64 format
    import base64
    decoded = base64.b64decode(data["content"]).decode("utf-8")

    return decoded

def get_pr_head_sha(owner: str, repo: str, pr_number: int) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = github_request("GET", url)
    data = response.json()
    return data["head"]["sha"]

def post_pr_comment(owner: str, repo: str, pr_number: int, body: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    payload = {"body": body}

    response = github_request("POST", url, json=payload)

    if response.status_code >= 400:
        raise Exception(f"Failed to post comment: {response.text}")

    return response.json()
