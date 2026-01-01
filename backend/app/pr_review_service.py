from backend.app.github_api import (
    get_pr_files,
    get_pr_head_sha,
    get_file_content,
    post_pr_comment,
)
from backend.analyzers.reviewer import analyze_code
from backend.app.comment_formatter import format_review_as_markdown


def run_pr_review(owner: str, repo: str, pr_number: int):
    head_sha = get_pr_head_sha(owner, repo, pr_number)
    files = get_pr_files(owner, repo, pr_number)

    for f in files:
        if f["status"] not in ("modified", "added"):
            continue

        file_path = f["filename"]
        diff = f.get("patch", "")
        content = get_file_content(owner, repo, file_path, head_sha)

        review = analyze_code(file_path, diff, content)
        comment = format_review_as_markdown(file_path, review)

        post_pr_comment(owner, repo, pr_number, comment)
