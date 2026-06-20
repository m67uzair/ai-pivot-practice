"""LESSON 4 — async tests + streaming over HTTP.

pytest-asyncio runs `async def` tests on an event loop. We set
`asyncio_mode = "auto"` in pyproject.toml, so async tests need NO per-test
marker (in the default 'strict' mode you'd add @pytest.mark.asyncio to each).

Run:  uv run pytest testing-llm-calls/test_04_async_streaming.py -v
"""

import json

import httpx
import respx

import app

CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


# ── Async + mocker: mocker.patch auto-returns an AsyncMock for async methods, ─
# so `await create(...)` works and you set its return_value as usual.
async def test_summarize_async_with_mocker(mocker, make_completion):
    create = mocker.patch.object(
        app.async_client.chat.completions,
        "create",
        return_value=make_completion("async summary"),
    )
    result = await app.summarize_async("text")
    assert result == "async summary"
    create.assert_awaited_once()   # note: assert_AWAITED, not just assert_called


# ── Async + respx: respx intercepts AsyncClient exactly the same way. ────────
@respx.mock
async def test_summarize_async_over_http():
    respx.post(CHAT_URL).mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "x", "object": "chat.completion", "created": 1,
                "model": "llama-3.3-70b-versatile",
                "choices": [{"index": 0, "finish_reason": "stop",
                             "message": {"role": "assistant", "content": "hi async"}}],
            },
        )
    )
    assert await app.summarize_async("text") == "hi async"


# ── Streaming over HTTP: return a Server-Sent-Events body; the SDK decodes it ─
# into chunks and our generator yields the tokens.
@respx.mock
def test_stream_summary_over_http(sse_body):
    body = sse_body(["A ", "cat ", "coded."])
    respx.post(CHAT_URL).mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=body.encode(),
        )
    )

    tokens = list(app.stream_summary("text"))

    assert tokens == ["A ", "cat ", "coded."]
    assert "".join(tokens) == "A cat coded."
