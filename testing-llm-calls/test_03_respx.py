"""LESSON 3 — respx (mock at the HTTP layer).

Instead of replacing the SDK method, respx intercepts the underlying httpx
request and returns a fake HTTP response. Your REAL client code runs — request
building, auth headers, JSON parsing into SDK objects — only the network is
faked. This catches bugs mocker can't (wrong URL, wrong payload, parse errors).

The Groq SDK posts to https://api.groq.com/openai/v1/chat/completions.

Run:  uv run pytest testing-llm-calls/test_03_respx.py -v
"""

import json

import groq
import httpx
import pytest
import respx

import app

CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


def _chat_response(content: str) -> dict:
    """A realistic non-streaming chat-completion JSON body."""
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1,
        "model": "llama-3.3-70b-versatile",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


# ── @respx.mock decorator: routes are intercepted inside the test. ───────────
@respx.mock
def test_summarize_over_http():
    route = respx.post(CHAT_URL).mock(
        return_value=httpx.Response(200, json=_chat_response("A cat learned Python."))
    )

    result = app.summarize("a long story about a cat")

    assert result == "A cat learned Python."
    # The real SDK ran, so we can inspect the ACTUAL request bytes it sent:
    assert route.called
    sent = json.loads(route.calls.last.request.content)
    assert sent["model"] == "llama-3.3-70b-versatile"
    assert sent["messages"][1]["content"] == "a long story about a cat"


# ── The respx_mock fixture: same thing without the decorator. ────────────────
def test_with_fixture(respx_mock):
    respx_mock.post(CHAT_URL).mock(
        return_value=httpx.Response(200, json=_chat_response("hello"))
    )
    assert app.summarize("hi") == "hello"


# ── .respond() shorthand + retry sequence via side_effect list. ──────────────
@respx.mock
def test_http_500_raises():
    respx.post(CHAT_URL).respond(500, json={"error": "server"})
    # The SDK turns a 5xx into an exception — assert your code surfaces it.
    with pytest.raises(Exception):
        app.summarize("x")


@respx.mock
def test_sdk_auto_retries_5xx():
    # GOTCHA worth knowing: the SDK auto-retries 5xx responses. Give it a 503
    # then a 200 and a SINGLE summarize() call transparently recovers — BOTH
    # responses are consumed by that one call (the SDK retried internally).
    route = respx.post(CHAT_URL).mock(
        side_effect=[
            httpx.Response(503, json={"error": "busy"}),
            httpx.Response(200, json=_chat_response("recovered")),
        ]
    )
    result = app.summarize("once")
    assert result == "recovered"
    assert route.call_count == 2   # proof it retried under the hood


# ── Simulate a network/connection error (not an HTTP status). ────────────────
@respx.mock
def test_connection_error():
    respx.post(CHAT_URL).mock(side_effect=httpx.ConnectError("no route"))
    # The SDK catches the raw httpx transport error and (after its retries)
    # re-raises it as its own typed error — assert the SDK's type, not httpx's.
    with pytest.raises(groq.APIConnectionError):
        app.summarize("x")


# ── Structured output, end-to-end through the real parser. ───────────────────
@respx.mock
def test_extract_event_over_http():
    payload = json.dumps(
        {"name": "Launch", "date": "Monday", "attendees": ["Ada"]}
    )
    respx.post(CHAT_URL).mock(
        return_value=httpx.Response(200, json=_chat_response(payload))
    )
    event = app.extract_event("launch monday with Ada")
    assert event.name == "Launch"
    assert event.attendees == ["Ada"]
