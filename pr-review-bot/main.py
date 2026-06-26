import asyncio
import hashlib
import hmac

import httpx
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

from config import settings
from models import PullRequestEvent
from reviewer import format_review, review_diff

app = FastAPI()


def verify_signature(raw: bytes, signature: str | None) -> None:
    """Reject the request unless it carries GitHub's valid HMAC signature.

    GitHub signs the raw body with the shared webhook secret (HMAC-SHA256) and
    sends `sha256=<hexdigest>` in X-Hub-Signature-256. We recompute it over the
    exact bytes we received and compare — in constant time, so we don't leak how
    much of the signature matched (timing attack).
    """
    if signature is None:
        raise HTTPException(status_code=401, detail="missing signature")
    expected = "sha256=" + hmac.new(
        settings.webhook_secret.encode(), raw, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail="bad signature")


async def fetch_pr_diff(pr_api_url: str) -> str:
    """GET a PR's unified diff as plain text.

    The magic is the Accept header: ask for `application/vnd.github.diff` and
    GitHub returns the raw diff text instead of the usual JSON. We hit the PR's
    API url (event.pull_request.url), which already points at the right PR.
    """
    headers = {
        "Accept": "application/vnd.github.diff",
        "Authorization": f"Bearer {settings.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(pr_api_url, headers=headers)
        resp.raise_for_status()
        return resp.text          # .text, not .json() — the body IS the diff


async def post_comment(repo: str, number: int, body: str) -> None:
    # PRs are issues, so a PR comment goes through the issues endpoint.
    url = f"https://api.github.com/repos/{repo}/issues/{number}/comments"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {settings.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, headers=headers, json={"body": body})
        resp.raise_for_status()


async def process_pr(pr_api_url: str, number: int, repo: str) -> None:
    # Runs after we've already 200'd GitHub, so the webhook never waits on this.
    diff = await fetch_pr_diff(pr_api_url)
    # review_diff blocks for seconds — offload it so it can't freeze the loop.
    review = await asyncio.to_thread(review_diff, diff)
    await post_comment(repo, number, format_review(review))
    print(f"PR #{number} in {repo}: posted review, {len(review.issues)} issue(s)")


@app.post("/webhook")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(default=None),
):
    raw = await request.body()
    # Verify FIRST, on the exact bytes — before we trust or parse anything.
    verify_signature(raw, request.headers.get("x-hub-signature-256"))

    if x_github_event == "ping":
        return {"msg": "pong"}
    if x_github_event != "pull_request":
        return {"ignored": x_github_event}

    # Validate + type the payload from the raw bytes (no re-read needed).
    event = PullRequestEvent.model_validate_json(raw)
    if event.action not in {"opened", "synchronize", "reopened"}:
        return {"ignored_action": event.action}

    # Hand the slow fetch+review to the background and ACK GitHub immediately,
    # well within its ~10s webhook timeout.
    background_tasks.add_task(
        process_pr,
        event.pull_request.url,
        event.number,
        event.repository.full_name,
    )
    return {"ok": True, "pr": event.number, "queued": True}
