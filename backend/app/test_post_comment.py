from backend.app.github_api import (
    get_pr_files,
    get_pr_head_sha,
    get_file_content,
    post_pr_comment,
)
from backend.analyzers.reviewer import analyze_code
from backend.app.comment_formatter import format_review_as_markdown

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
    content = get_file_content(OWNER, REPO, file_path, head_sha)

    review = analyze_code(file_path, diff, content)
    comment = format_review_as_markdown(file_path, review)

    post_pr_comment(OWNER, REPO, PR_NUMBER, comment)

print("✅ AI review comments posted to PR")
