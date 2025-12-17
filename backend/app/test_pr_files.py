from backend.app.github_api import get_pr_files

# CHANGE THIS to your repo info:
OWNER = "oliviarose1212"
REPO = "AI-Code-Review"
PR_NUMBER = 1   # Change to the PR you want to test

files = get_pr_files(OWNER, REPO, PR_NUMBER)

for f in files:
    print("-" * 80)
    print("Filename:", f["filename"])
    print("Status:", f["status"])
    print("Patch (diff):\n", f.get("patch"))
