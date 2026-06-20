"""LESSON 2 — pytest-mock (the `mocker` fixture).

Mock at the PYTHON level: replace the SDK method so no HTTP happens at all.
This is the fastest, most common way to test LLM code. You control exactly what
the client "returns" and you assert exactly what your code sent it.

Run:  uv run pytest testing-llm-calls/test_02_mocker.py -v
"""

import json

import pytest

import app


# ── Patch a method to return a canned response. ──────────────────────────────
def test_summarize_returns_content(mocker, make_completion):
    # mocker.patch replaces app.client.chat.completions.create for THIS test
    # only; mocker auto-undoes it at teardown (no decorators/with-blocks needed).
    fake = make_completion("A cat learned Python.")
    create = mocker.patch.object(
        app.client.chat.completions, "create", return_value=fake
    )

    result = app.summarize("long text about a cat")

    assert result == "A cat learned Python."
    # Assert HOW the SDK was called — model, and that our text was forwarded.
    create.assert_called_once()
    kwargs = create.call_args.kwargs
    assert kwargs["model"] == "llama-3.3-70b-versatile"
    assert kwargs["messages"][1]["content"] == "long text about a cat"


# ── side_effect = exception: simulate an API failure. ────────────────────────
def test_summarize_propagates_api_error(mocker):
    mocker.patch.object(
        app.client.chat.completions, "create",
        side_effect=RuntimeError("rate limited"),
    )
    with pytest.raises(RuntimeError, match="rate limited"):
        app.summarize("anything")


# ── side_effect = list: return different values on successive calls. ─────────
# Great for testing retry logic (fail once, then succeed).
def test_side_effect_sequence(mocker, make_completion):
    create = mocker.patch.object(
        app.client.chat.completions, "create",
        side_effect=[make_completion("first"), make_completion("second")],
    )
    assert app.summarize("a") == "first"
    assert app.summarize("b") == "second"
    assert create.call_count == 2


# ── Tool calling: build a fake message carrying tool_calls. ──────────────────
def test_detect_tool_calls(mocker, make_tool_call):
    message = mocker.MagicMock()
    message.tool_calls = [make_tool_call("get_weather", {"city": "Karachi"})]
    resp = mocker.MagicMock()
    resp.choices[0].message = message
    mocker.patch.object(app.client.chat.completions, "create", return_value=resp)

    calls = app.detect_tool_calls("weather in Karachi?")

    assert calls == [("get_weather", {"city": "Karachi"})]
    # ^ This is why make_tool_call sets `.name` explicitly: MagicMock(name="x")
    #   would NOT give tc.function.name == "x" (see conftest note).


def test_detect_tool_calls_none(mocker, make_completion):
    # make_completion sets tool_calls = None → function returns [].
    mocker.patch.object(
        app.client.chat.completions, "create",
        return_value=make_completion("just chatting"),
    )
    assert app.detect_tool_calls("hi") == []


# ── Structured output: mock the JSON string, assert the parsed Pydantic. ─────
def test_extract_event(mocker, make_completion):
    payload = json.dumps(
        {"name": "Quarterly review", "date": "Friday", "attendees": ["Sam", "Jo"]}
    )
    mocker.patch.object(
        app.client.chat.completions, "create",
        return_value=make_completion(payload),
    )

    event = app.extract_event("review Friday with Sam and Jo")

    assert event.name == "Quarterly review"
    assert event.attendees == ["Sam", "Jo"]


def test_extract_event_invalid_json_raises(mocker, make_completion):
    # If the model returns junk, model_validate_json raises — assert we don't
    # silently swallow it.
    mocker.patch.object(
        app.client.chat.completions, "create",
        return_value=make_completion("not json at all"),
    )
    with pytest.raises(Exception):
        app.extract_event("bad")


# ── Streaming via mocker: create() returns an ITERABLE of fake chunks. ───────
def test_stream_summary_with_mocker(mocker):
    def chunk(content):
        c = mocker.MagicMock()
        c.choices[0].delta.content = content
        return c

    # Note the empty-string chunk — stream_summary should skip it.
    fake_stream = [chunk("A "), chunk("cat "), chunk(""), chunk("coded.")]
    mocker.patch.object(
        app.client.chat.completions, "create", return_value=iter(fake_stream)
    )

    tokens = list(app.stream_summary("text"))

    assert tokens == ["A ", "cat ", "coded."]
    assert "".join(tokens) == "A cat coded."
