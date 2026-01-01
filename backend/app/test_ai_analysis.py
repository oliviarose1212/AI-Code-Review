from backend.analyzers.reviewer import analyze_code

from backend.app.github_api import (
    get_pr_files,
    get_file_content,
    get_pr_head_sha,
)

OWNER = "oliviarose1212"
REPO = "AI-Code-Review"
PR_NUMBER = 1  # update if needed

head_sha = get_pr_head_sha(OWNER, REPO, PR_NUMBER)
files = get_pr_files(OWNER, REPO, PR_NUMBER)

for f in files:
    if f["status"] not in ("modified", "added"):
        continue

    file_path = f["filename"]
    diff = f.get("patch", "")

    content = get_file_content(
        OWNER,
        REPO,
        file_path,
        head_sha,
    )

    print("\n" + "=" * 80)
    print("AI REVIEW:", file_path)

    review = analyze_code(file_path, diff, content)
    print(review)
