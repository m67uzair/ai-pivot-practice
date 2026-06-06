<!-- artifact
emoji: 🗄️
tasks: p1-w2-t5
stack: Python, google-genai, httpx
-->

# Prompt Caching

Manual function calling with Gemini, plus **both prompt-caching strategies** — the same `get_weather` tool as the `tool_calling` module, rebuilt on the `google-genai` SDK. One run exercises implicit caching (works on the free tier) and then attempts explicit caching (gracefully skipped if unbilled), so both code paths are visible.

## What it shows

- **Manual tool loop on Gemini.** AFC is disabled; the script drives the loop itself: read `response.function_calls`, run the function, send results back as a `role="user"` `Part.from_function_response` (matched by name — Gemini has no `tool_call_id`), repeat until the model returns text. Note `fc.args` arrives already parsed (no `json.loads`). The loop is shared by both caching paths; only the `config` differs.
- **Implicit caching** (`run_implicit`). The stable prefix (a large system instruction + the tool declarations) is sent first on every call, so Gemini reuses it transparently. Running it prints the proof:

  ```
  [implicit turn 1] prompt=1195 cached=0   output=55     ← cold
  [implicit turn 2] prompt=1644 cached=766 output=52     ← 766 tokens served from cache
  ```

- **Explicit caching** (`run_explicit`). Creates a server-side cache with `client.caches.create` (system instruction + tools), points the per-call config at it via `cached_content=cache.name`, and deletes it afterward. The discount is *guaranteed* (so `cached` would be non-zero even on turn 1). On the free tier this raises `429 RESOURCE_EXHAUSTED`, which `main()` catches and reports instead of crashing:

  ```
  [explicit] skipped — explicit caching needs a billing-enabled project and a >=2,048-token prefix.
  ```

## Caching notes

- **Implicit caching**: automatic for Gemini 2.5+, no setup, no storage fee, best-effort. Observe hits via `usage_metadata.cached_content_token_count`. Design rule: **stable prefix first, volatile content last.**
- **Explicit caching** (`client.caches.create`): guarantees the discount but bills storage for the TTL, is **not available on the free API tier** (`429`, storage limit 0), and requires a minimum prefix of ~2,048 tokens for `gemini-2.5-flash` (our prefix is ~1,172, so it would also need a bigger system instruction). Needs a billing-enabled project. Unlike Anthropic's inline `cache_control` breakpoints, a Gemini cache is one fixed object — to cache conversation history you put the turns in the cache's `contents` field.

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
