def analyze_code(file_path: str, diff: str, content: str) -> dict:
    issues = []

    # Very simple heuristic examples
    if "print(" in content:
        issues.append({
            "type": "maintainability",
            "line": None,
            "message": "Debug print statement detected.",
            "suggestion": "Remove print statements or replace with logging."
        })

    if "TODO" in content:
        issues.append({
            "type": "maintainability",
            "line": None,
            "message": "TODO comment found.",
            "suggestion": "Resolve TODOs before merging."
        })

    if not issues:
        summary = "No major issues found. Code looks clean."
    else:
        summary = f"Found {len(issues)} potential issue(s)."

    return {
        "summary": summary,
        "issues": issues
    }
