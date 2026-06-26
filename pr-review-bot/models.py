from pydantic import BaseModel


# We model ONLY the slice of GitHub's (huge) PR-event payload that we use.
# Pydantic ignores every other field by default, so this stays small.

class PullRequest(BaseModel):
    url: str        # API URL for the PR — we GET the diff from here (step C)
    title: str


class Repo(BaseModel):
    full_name: str  # e.g. "m67uzair/pr-review-bot-test"


class PullRequestEvent(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    repository: Repo
