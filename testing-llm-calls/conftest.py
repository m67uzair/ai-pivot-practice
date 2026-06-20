"""Shared fixtures.

conftest.py is auto-discovered by pytest — any fixture defined here is available
to every test in this folder without importing it. This is *the* idiomatic place
to put reusable test scaffolding.
"""

import json
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def make_completion():
    """Factory fixture: build a fake non-streaming chat completion.

    Returns a callable so each test can ask for a response with specific
    content. A factory fixture (fixture-returns-a-function) is the clean way to
    parametrize fixture output per test.
    """
    def _make(content: str) -> MagicMock:
        resp = MagicMock()
        # MagicMock supports __getitem__, so choices[0] works and returns the
        # same child mock each time — that's why this single assignment sticks.
        resp.choices[0].message.content = content
        resp.choices[0].message.tool_calls = None
        return resp
    return _make


@pytest.fixture
def make_tool_call():
    """Factory: build one fake tool_call object shaped like the SDK's."""
    def _make(name: str, args: dict) -> MagicMock:
        tc = MagicMock()
        # GOTCHA: MagicMock(name=...) sets the *mock's* repr name, NOT a `.name`
        # attribute. You must assign .name explicitly, or reads give a child mock.
        tc.function.name = name
        tc.function.arguments = json.dumps(args)
        return tc
    return _make


@pytest.fixture
def sse_body():
    """Factory: build a Server-Sent-Events body like a streaming LLM returns."""
    def _make(tokens: list[str]) -> str:
        lines = []
        for tok in tokens:
            chunk = {
                "id": "chatcmpl-test",
                "object": "chat.completion.chunk",
                "created": 1,
                "model": "llama-3.3-70b-versatile",
                "choices": [
                    {"index": 0, "delta": {"content": tok}, "finish_reason": None}
                ],
            }
            lines.append(f"data: {json.dumps(chunk)}\n\n")
        lines.append("data: [DONE]\n\n")
        return "".join(lines)
    return _make
