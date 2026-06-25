<!-- artifact
emoji: 🔀
tasks: p1-w3-t5
stack: Python, litellm, instructor
-->

# LiteLLM Tryout

Uses [LiteLLM](https://docs.litellm.ai/) to put one unified interface in front of three free providers (Gemini, Groq, OpenRouter), with automatic **fallbacks** — and shows that Instructor layers cleanly on top.

## Examples

1. **Router fallbacks** (`fallback_demo`). A `litellm.Router` with a `model_list` of the three providers behind logical names, and `fallbacks=[{"primary": ["backup-groq", "backup-openrouter"]}]`. Calling with `mock_testing_fallbacks=True` forces the primary (Gemini) to raise, so the chain actually fails over — the printed `answered by:` confirms the response came from Groq, the first backup.
2. **Instructor over the Router** (`instructor_demo`). `instructor.from_litellm(router.completion)` wraps the Router's call, so you get a validated Pydantic `response_model` back **and** the fallback resilience.

## Key ideas

- `litellm.completion(...)` is the low-level single call; `router.completion(...)` wraps it to add fallbacks / load-balancing / rate limits, accepting the same kwargs.
- `mock_testing_fallbacks=True` is the built-in way to exercise the fallback path without real failures (it forces the primary to raise, then runs the real backup).

## Setup

Add all three keys to the `.env` file at the project root:

```
GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Run

From the project root:

```bash
uv run litellm-tryout/main.py
```
