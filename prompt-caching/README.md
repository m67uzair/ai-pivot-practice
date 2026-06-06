<!-- artifact
emoji: 🗄️
tasks: p1-w2-t5
stack: Python, google-genai, httpx
-->

# Prompt Caching

Manual function calling with Gemini, plus **implicit prompt caching** — the same `get_weather` tool as the `tool_calling` module, but rebuilt on the `google-genai` SDK so the reused system-instruction + tools prefix gets cached automatically.

## What it shows

- **Manual tool loop on Gemini.** AFC is disabled; the script drives the loop itself: read `response.function_calls`, run the function, send results back as a `role="user"` `Part.from_function_response` (matched by name — Gemini has no `tool_call_id`), repeat until the model returns text. Note `fc.args` arrives already parsed (no `json.loads`).
- **Implicit caching.** The stable prefix (a large system instruction + the tool declarations) is sent first on every call, so Gemini reuses it transparently. Running it prints the proof:

  ```
  [turn 1] prompt=1195 cached=0   output=55     ← cold
  [turn 2] prompt=1644 cached=768 output=52     ← 768 tokens served from cache
  ```

## Caching notes

- **Implicit caching** (used here): automatic for Gemini 2.5+, no setup, no storage fee, best-effort. Observe hits via `usage_metadata.cached_content_token_count`. Design rule: **stable prefix first, volatile content last.**
- **Explicit caching** (`client.caches.create`): guarantees the discount but is **not available on the free API tier** (`429 RESOURCE_EXHAUSTED`, storage limit 0) and requires a minimum prefix of ~2,048 tokens for `gemini-2.5-flash`. Needs a billing-enabled project.

## Setup

Add your Gemini key to the `.env` file at the project root:

```
GEMINI_API_KEY=...
```

The weather API ([Open-Meteo](https://open-meteo.com/)) needs no key.

## Run

From the project root:

```bash
uv run prompt-caching/main.py
```
