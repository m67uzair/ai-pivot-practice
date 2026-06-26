from enum import Enum

from pydantic import BaseModel, Field


# ── Incoming GitHub webhook payload (the slice we use) ───────────────────────

class PullRequest(BaseModel):
    url: str
    title: str


class Repo(BaseModel):
    full_name: str


class PullRequestEvent(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repo


# ── Outgoing structured review (what the LLM must produce) ───────────────────

class Severity(str, Enum):
    """Constrains the model to these exact values — no free-text severities."""
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class ReviewIssue(BaseModel):
    file: str = Field(description="Path of the file the issue is in.")
    location: str | None = Field(
        default=None,
        description="Where in the file, e.g. a function name or code snippet.",
    )
    severity: Severity = Field(description="How serious the issue is.")
    title: str = Field(description="One-line summary of the issue.")
    explanation: str = Field(description="Why this is a problem.")
    suggested_fix: str = Field(description="A concrete fix for it.")


class Review(BaseModel):
    summary: str = Field(description="One-paragraph overall assessment of the PR.")
    issues: list[ReviewIssue] = Field(
        description="Every real issue found; empty list if the diff looks clean."
    )
