# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A `uv`-managed monorepo of self-contained Python practice scripts for an AI-engineer pivot (see `README.md`). Each top-level folder (`pokemon-cli/`, `chat-completion-script/`, `structured-outputs/`) is an independent learning artifact that calls a public API or LLM provider and parses the response with Pydantic. They share one virtual environment and one `.env`, but no code.

## Commands

```bash
uv sync                                  # install deps into the shared .venv
uv run pokemon-cli/main.py               # run a project (always from repo root)
uv run chat-completion-script/main.py
uv run structured-outputs/main.py
```

There are no tests, linter, or build step configured. Requires Python >= 3.14.

## Conventions that matter

- **Run scripts from the repo root via `uv run <folder>/main.py`.** Each project uses flat, root-relative imports (`from config import settings`, `from models import Pokemon`) that only resolve because the run command puts the script's own folder on `sys.path`. Running from inside a project folder, or importing across projects, will break.

- **Each project carries its own `config.py` and `models.py`.** The `config.py` files are near-identical copies of the same `pydantic-settings` `Settings` class — duplication is intentional (projects are meant to stand alone), so changing one does not change the others.

- **All three API keys are required to instantiate `Settings`, regardless of which one a project uses.** Every `config.py` declares `gemini_api_key`, `groq_api_key`, and `openrouter_api_key` as required fields loaded from the root `.env`. A project that only calls Groq will still fail at import if the other keys are absent. The root `.env` (git-ignored) must contain all three:

  ```
  GEMINI_API_KEY=...
  GROQ_API_KEY=...
  OPENROUTER_API_KEY=...
  ```

- **The OpenAI SDK is reused against non-OpenAI providers via `base_url`.** `chat-completion-script` points it at OpenRouter; `structured-outputs` points it at Groq's `/openai/v1` endpoint. When editing these, the SDK is OpenAI's but the model and host are not.

## Artifact README convention

This repo is the artifact source for the companion **ai-pivot-tracker** web app, whose "Artifacts" panel lists top-level folders at runtime by fetching each folder's `README.md` and parsing a hidden HTML-comment metadata block at the very top. **A top-level project folder with no `README.md` in this format is invisible in the tracker**, so every new project folder must include one.

Each project `README.md` must begin with this block (before the H1):

```markdown
<!-- artifact
emoji: 🧱
tasks: p1-w2-t2
stack: Python, openai, groq, Pydantic
-->
```

- `tasks` — comma-separated tracker task IDs the project fulfills, pattern `p<phase>-w<week>-t<task>` (e.g. `p0-w0-t8`) or buffer IDs like `buf1-t1`. These link the card to roadmap checkboxes — get them right.
- `emoji` (defaults to 📦) and `stack` are optional; `name`/`desc` default to the first H1 and first paragraph.

Keep the block's `stack`/scope in sync when a project changes. Full spec in `README.md`.

## Per-project notes

- `pokemon-cli` — fetches the PokéAPI with `httpx`, parses into `Pokemon` Pydantic models. No API key needed.
- `chat-completion-script` — sends one prompt to Gemini, Groq (Llama 3.3), and OpenRouter using three different SDKs (`google-genai`, `groq`, `openai`), printing results side-by-side.
- `structured-outputs` — coerces an LLM into a Pydantic schema (`CalenderEvent`) three ways: the OpenAI Responses API (`.parse`), Chat Completions (`.parse`), and JSON mode (manual `json.loads` + `model_validate`). The `parse` APIs require `model_config = {"extra": "forbid"}` on every model.
