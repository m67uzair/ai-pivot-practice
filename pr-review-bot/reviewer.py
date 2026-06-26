"""The actual 'agent': turn a PR diff into a structured, validated Review.

LiteLLM makes the call (one interface over any provider); instructor wraps it so
we get a validated `Review` back and an automatic re-ask if the model's output
doesn't fit the schema.
"""

import instructor
import litellm

from config import settings
from models import Review, Severity

_EMOJI = {Severity.critical: "🔴", Severity.high: "🟠",
          Severity.medium: "🟡", Severity.low: "🔵"}

MODEL = "groq/openai/gpt-oss-120b"

SYSTEM_PROMPT = """\
You are a meticulous senior software engineer reviewing a GitHub pull request.
You are given a unified diff; review ONLY the changed code.

Flag real problems: bugs, correctness errors, security issues, and language
footguns (e.g. mutable default arguments, bypassed validation, wrong units,
resource leaks, unsafe comparisons). Do NOT nitpick style or formatting.

For each issue: name the file, explain WHY it is wrong, and give a concrete
suggested fix. If the diff is genuinely clean, return an empty issues list."""

# LiteLLM is the engine; instructor adds validation + retries on top.
# Mode.JSON (not the default TOOLS): the model returns JSON in the message
# content, so instructor validates it CLIENT-SIDE — which lets its retry feed
# Pydantic errors back to the model. With TOOLS mode, Groq validates the schema
# server-side and rejects off-schema output with a 400 before instructor can
# re-ask, so the self-correction never happens.
client = instructor.from_litellm(litellm.completion, mode=instructor.Mode.JSON)


def review_diff(diff: str) -> Review:
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review this pull request diff:\n\n{diff}"},
        ],
        response_model=Review,
        api_key=settings.groq_api_key,
        max_retries=2,        # instructor re-asks the model if validation fails
    )


def format_review(review: Review) -> str:
    if not review.issues:
        return f"## 🤖 Automated review\n\n{review.summary}\n\n✅ No issues found."

    parts = [f"## 🤖 Automated review\n\n{review.summary}"]
    for i in review.issues:
        where = f"`{i.file}`" + (f" · {i.location}" if i.location else "")
        parts.append(
            f"### {_EMOJI[i.severity]} {i.severity.value.upper()} — {i.title}\n"
            f"{where}\n\n{i.explanation}\n\n"
            f"**Suggested fix:**\n\n{i.suggested_fix}"
        )
    return "\n\n---\n\n".join(parts)
