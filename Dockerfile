# ---------- builder: install dependencies into a venv ----------
FROM python:3.14-slim AS builder

# grab the uv binary from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY uv.lock pyproject.toml ./

# Deps only, before the app code — so editing code later doesn't bust this
# (slow) layer. The cache mount keeps uv's download cache across builds.
RUN --mount=type=cache,id=s/404117c7-7281-48f9-b435-4ee290eb2b6a-pr-review-bot-uv-cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ---------- runtime: slim image with just the venv + the bot ----------
FROM python:3.14-slim

WORKDIR /app

# Bring the finished venv from the builder and put it first on PATH, so
# `fastapi`, `python`, etc. resolve to it.
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Only the bot's source (the other practice modules never enter the image).
COPY pr-review-bot/ ./pr-review-bot/

EXPOSE 8000
CMD ["fastapi", "run", "pr-review-bot/main.py", "--host", "0.0.0.0"]
