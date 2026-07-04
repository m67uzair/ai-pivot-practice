<!-- artifact
emoji: 🤖
tasks: p1-w4-t1, p1-w4-t2, p1-w4-t3, p1-w4-t4, p1-w4-t6
stack: Python, FastAPI, LiteLLM, instructor, Pydantic
-->

# PR Review Bot

A FastAPI service that auto-reviews GitHub pull requests with an LLM. A webhook receives PR events, the bot fetches the diff, an LLM produces a **structured, Pydantic-validated** review (issues + severity + suggested fix), and posts it back to the PR. Built incrementally across the week — this README grows as each task ships.

## Roadmap

- [x] **t1** — GitHub webhook → FastAPI receives PR diff (HMAC-verified, diff fetched)
- [x] **t2** — Structured review output (issues, severity, suggested fix), Pydantic-validated
- [x] **t3** — Post review comment back via the GitHub API
- [x] **t4** — Store reviews (SQLAlchemy + Alembic + SQLite)
- [~] **t5** — Dockerfile (multi-stage) ✓ · GitHub Actions CI *(pending)*
- [x] **t6** — Deploy to Railway
- [ ] **t7** — 90-sec demo video

## How it works (so far)

1. **Receive + verify** (`main.py`) — `POST /webhook` reads the raw body, verifies GitHub's `X-Hub-Signature-256` HMAC against `WEBHOOK_SECRET` (constant-time), answers the `ping`, and filters to `pull_request` events (`opened`/`synchronize`/`reopened`).
2. **Ack fast, work in the background** — it returns `200` to GitHub immediately and runs the slow part in a `BackgroundTask`; the blocking LLM call is offloaded with `asyncio.to_thread` so it never freezes the event loop.
3. **Fetch the diff** — `GET`s the PR's API URL with `Accept: application/vnd.github.diff` to get the raw unified diff.
4. **Review it** (`reviewer.py`) — LiteLLM makes the call, instructor (JSON mode) validates the result into a `Review` model, re-asking the model if it doesn't fit the schema.
5. **Post it back** — `format_review` renders the `Review` as markdown and it's posted to the PR via the GitHub issues-comments endpoint.
6. **Persist it** (`db.py`) — `save_review` writes a `StoredReview` + its `StoredIssue` rows to SQLite via SQLAlchemy. Schema is managed by Alembic migrations (`pr-review-bot/migrations/`).

## Database

Apply migrations before running:

```bash
uv run alembic -c pr-review-bot/alembic.ini upgrade head
```

After changing the models in `db.py`, generate a new migration:

```bash
uv run alembic -c pr-review-bot/alembic.ini revision --autogenerate -m "..."
uv run alembic -c pr-review-bot/alembic.ini upgrade head
```

## Deploy

Live on **Railway**. Railway builds the image from the `Dockerfile` on each push and runs the container. Secrets (`GITHUB_TOKEN`, `WEBHOOK_SECRET`, `GROQ_API_KEY`) are set as **Railway environment variables** — never baked into the image — and read at runtime by `pydantic-settings`. The container binds `0.0.0.0` so Railway's router can reach it.

## Roadmap: making it usable by others

Today it auto-reviews PRs on a repo where you've configured the webhook + a PAT. To open it up:

- **`@reviewBot` mention trigger** — handle `issue_comment` events so anyone can comment `@reviewBot` on a PR to trigger a review on demand (reuses the whole pipeline).
- **Installable GitHub App** — give the bot its own identity (`reviewbot[bot]`) and one-click install on any repo, authenticating with per-installation tokens (App JWT → installation access token) instead of a personal PAT.

## Setup

Add to the `.env` at the repo root:

```
GITHUB_TOKEN=...      # PAT with Pull requests read/write
WEBHOOK_SECRET=...     # must match the secret set on the GitHub webhook
GROQ_API_KEY=...
```

## Run

```bash
uv run fastapi dev pr-review-bot/main.py
```

Then expose it with a tunnel (smee.io / ngrok) and register a webhook on a test repo (Payload URL `…/webhook`, content type `application/json`, secret = `WEBHOOK_SECRET`, events = Pull requests). GitHub's webhook **Recent Deliveries** tab is the best debugging view.
