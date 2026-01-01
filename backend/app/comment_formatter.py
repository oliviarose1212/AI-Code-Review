def format_review_as_markdown(file_path: str, review: dict) -> str:
    lines = []
    lines.append(f"### 🤖 AI Code Review: `{file_path}`\n")
    lines.append(f"**Summary:** {review.get('summary', '')}\n")

    issues = review.get("issues", [])
    if not issues:
        lines.append("✅ No issues found.\n")
        return "\n".join(lines)

    for idx, issue in enumerate(issues, start=1):
        lines.append(f"**{idx}. {issue['type'].capitalize()}**")
        if issue.get("line"):
            lines.append(f"- Line: `{issue['line']}`")
        lines.append(f"- Problem: {issue['message']}")
        lines.append(f"- Suggestion: {issue['suggestion']}\n")

    return "\n".join(lines)
