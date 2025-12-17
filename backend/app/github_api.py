import httpx
from backend.app.github_auth import get_installation_access_token


def github_request(method, url, **kwargs):
    """
    Wrapper around GitHub API that automatically adds authentication.
    """
    token = get_installation_access_token()

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"token {token}"
    headers["Accept"] = "application/vnd.github+json"

    response = httpx.request(method, url, headers=headers, **kwargs)

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
