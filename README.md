# ai-pivot-practice

The artifact repository for my AI-pivot practice tasks — **Dart/Flutter → AI Engineer** (Karachi → remote, 25-week plan).

This is a `uv`-managed monorepo: one shared virtual environment, multiple self-contained practice projects in their own folders.

## Artifacts

| Project | What it does | Stack |
|---------|--------------|-------|
| [`pokemon-cli`](./pokemon-cli) | Fetches the PokéAPI, parses the response into typed Pydantic models, prints it. | Python · httpx · Pydantic |
| [`chat-completion-script`](./chat-completion-script) | Sends one prompt to Gemini, Groq (Llama 3.3), and OpenRouter and prints the responses side-by-side for comparison. | Python · google-genai · groq · openai |
| [`structured-outputs`](./structured-outputs) | Asks an LLM to return JSON matching a Pydantic schema and parses it into typed models, three ways: the Responses API, the Chat Completions API, and JSON mode. | Python · openai · Pydantic |
| [`instructor`](./instructor) | Gets schema-validated LLM output via the `instructor` library — pass a Pydantic model as `response_model` and get a typed instance back. | Python · instructor · Pydantic |
| [`tool_calling`](./tool_calling) | Gives an LLM a `get_weather` tool and runs the multi-turn loop: the model calls the tool, the script executes it against Open-Meteo, and the result is fed back for a final answer. | Python · groq · httpx · Pydantic |
| [`prompt-caching`](./prompt-caching) | Manual Gemini tool calling plus implicit prompt caching — reuses the system-instruction + tools prefix across turns and prints the cache hit. | Python · google-genai · httpx |
| [`fastapi-chat-streaming-endpoint`](./fastapi-chat-streaming-endpoint) | A FastAPI SSE endpoint that streams an LLM response token-by-token via Groq + `AsyncGroq`. | Python · fastapi · groq |
| [`testing-llm-calls`](./testing-llm-calls) | A runnable cheat-sheet for testing LLM code — pytest, pytest-mock, and respx examples covering chat, async, streaming, tool calls, and structured output. | Python · pytest · pytest-mock · respx |
| [`litellm-tryout`](./litellm-tryout) | One LiteLLM interface over Gemini/Groq/OpenRouter with automatic fallbacks (mock-tested), plus Instructor layered on the Router. | Python · litellm · instructor |
| [`pr-review-bot`](./pr-review-bot) | A FastAPI service that auto-reviews GitHub PRs: verified webhook → fetch diff → LLM produces a structured, Pydantic-validated review (→ posts back, stores, deploys — in progress). | Python · FastAPI · LiteLLM · instructor · Pydantic |

## Setup

```bash
uv sync
```

API keys live in a `.env` at the repo root (git-ignored):

```
GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Run

```bash
uv run pokemon-cli/main.py
uv run chat-completion-script/main.py
uv run structured-outputs/main.py
```

## Artifact README convention

This repo is the artifact source for the companion **ai-pivot-tracker** web app. Its "Artifacts" panel lists this repo's top-level folders at runtime (via the GitHub API), fetches each folder's `README.md`, and parses metadata from a hidden HTML-comment block at the very top. **A folder with no `README.md` in this format is invisible in the tracker.**

Every top-level project folder's `README.md` must begin with:

```markdown
<!-- artifact
emoji: 🧱
tasks: p1-w2-t2
stack: Python, openai, groq, Pydantic
-->

# Project Title

One-sentence description — the first paragraph after the H1 becomes the card description.
```

Fields:

- `emoji` — one emoji by the card title (optional; defaults to 📦)
- `tasks` — comma-separated tracker task IDs this project fulfills, pattern `p<phase>-w<week>-t<task>` (e.g. `p0-w0-t8`, `p1-w1-t3`) or buffer IDs like `buf1-t1`. These link the card to roadmap checkboxes — **get them right.**
- `stack` — comma-separated tech tags shown as pills (optional)
- `name` — card title (optional; defaults to the first `#` H1)
- `desc` — card description (optional; defaults to the first paragraph after the H1)

When adding a new project folder, always include a `README.md` in this format with a correct `tasks:` mapping, and keep `stack`/scope in sync if they change.
