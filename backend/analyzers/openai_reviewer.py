import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a senior software engineer performing a professional code review.

Rules:
- Be concise
- Be constructive
- Do not repeat the diff
- Focus on correctness, readability, performance, and security
- Ignore formatting-only changes unless harmful
"""

USER_PROMPT_TEMPLATE = """
File path:
{file_path}

Diff (changes only):
{diff}

Full file content:
{content}

Respond ONLY in valid JSON with this schema:

{{
  "summary": "short overall review",
  "issues": [
    {{
      "type": "bug | style | performance | security | maintainability",
      "line": number_or_null,
      "message": "what is wrong",
      "suggestion": "how to improve"
    }}
  ]
}}

If there are no issues, return an empty issues array.
"""


def analyze_code(file_path: str, diff: str, content: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    file_path=file_path,
                    diff=diff,
                    content=content[:8000],  # prevent token overflow
                ),
            },
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "summary": "AI returned invalid JSON",
            "issues": [],
            "raw_response": raw,
        }
