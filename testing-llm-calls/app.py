"""The code under test.

A small set of functions that make every common *kind* of LLM call, so the
test files have something realistic to mock. We use Groq (its SDK is built on
httpx, which is what respx intercepts), but the patterns are identical for the
OpenAI / Anthropic SDKs.

No real API key is needed: every test replaces the call. The placeholder key
just lets the module import and the client construct.
"""

import json
import os

from groq import AsyncGroq, Groq

from models import CalendarEvent

MODEL = "llama-3.3-70b-versatile"

# Real key not required — tests mock the network. Falls back to a placeholder so
# `uv run pytest` works with zero secrets.
_API_KEY = os.environ.get("GROQ_API_KEY", "test-key-not-used")

client = Groq(api_key=_API_KEY)
async_client = AsyncGroq(api_key=_API_KEY)


# ── Pure helpers (no LLM) — for the pytest-basics lesson ─────────────────────

def estimate_cost(prompt_tokens: int, completion_tokens: int,
                  rate_per_1k: float = 0.002) -> float:
    """Estimate $ cost. Raises on negative token counts."""
    if prompt_tokens < 0 or completion_tokens < 0:
        raise ValueError("token counts must be non-negative")
    return (prompt_tokens + completion_tokens) / 1000 * rate_per_1k


def build_messages(system: str, user: str) -> list[dict]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


# ── 1. Plain chat completion (sync) ──────────────────────────────────────────

def summarize(text: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=build_messages("Summarize in one sentence.", text),
    )
    return resp.choices[0].message.content


# ── 2. Plain chat completion (async) ─────────────────────────────────────────

async def summarize_async(text: str) -> str:
    resp = await async_client.chat.completions.create(
        model=MODEL,
        messages=build_messages("Summarize in one sentence.", text),
    )
    return resp.choices[0].message.content


# ── 3. Streaming ─────────────────────────────────────────────────────────────

def stream_summary(text: str):
    """Yields tokens as they arrive."""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=build_messages("Summarize in one sentence.", text),
        stream=True,
    )
    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        if token:
            yield token


# ── 4. Tool / function calling ───────────────────────────────────────────────

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}


def detect_tool_calls(prompt: str) -> list[tuple[str, dict]]:
    """Return [(tool_name, parsed_args), ...] the model wants to call."""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        tools=[WEATHER_TOOL],
        tool_choice="auto",
    )
    message = resp.choices[0].message
    if not message.tool_calls:
        return []
    return [
        (tc.function.name, json.loads(tc.function.arguments))
        for tc in message.tool_calls
    ]


# ── 5. Structured output (JSON mode → Pydantic) ──────────────────────────────

def extract_event(text: str) -> CalendarEvent:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=build_messages(
            "Extract the event as JSON with keys name, date, attendees.", text
        ),
        response_format={"type": "json_object"},
    )
    return CalendarEvent.model_validate_json(resp.choices[0].message.content)
