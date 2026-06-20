"""LESSON 1 — pytest fundamentals (no mocking yet).

Run just this file:   uv run pytest testing-llm-calls/test_01_pytest_basics.py -v
"""

import pytest

from app import build_messages, estimate_cost


# ── Plain test: a function whose name starts with `test_` is collected. ──────
# `assert` is all you need — pytest rewrites it to show a rich diff on failure.
def test_estimate_cost_basic():
    assert estimate_cost(1000, 1000) == pytest.approx(0.004)
    # pytest.approx handles float rounding — never assert == on raw floats.


# ── pytest.raises: assert that bad input raises the right exception. ─────────
def test_estimate_cost_rejects_negative():
    with pytest.raises(ValueError, match="non-negative"):
        estimate_cost(-1, 0)
    # `match` is a regex checked against the exception message.


# ── Parametrize: run the SAME test body across many input/expected pairs. ────
# Each tuple becomes a separate reported test case (3 tests, not 1).
@pytest.mark.parametrize(
    "prompt_tokens, completion_tokens, expected",
    [
        (0, 0, 0.0),
        (500, 500, 0.002),
        (1000, 0, 0.002),
    ],
)
def test_estimate_cost_table(prompt_tokens, completion_tokens, expected):
    assert estimate_cost(prompt_tokens, completion_tokens) == pytest.approx(expected)


# ── Fixtures: setup shared across tests. A function with @pytest.fixture is ──
# requested by naming it as a test argument. pytest injects the return value.
@pytest.fixture
def sample_text():
    return "The quarterly review is on Friday with Sam and Jo."


def test_build_messages_uses_fixture(sample_text):
    msgs = build_messages("Summarize.", sample_text)
    assert msgs[0]["role"] == "system"
    assert msgs[1]["content"] == sample_text


# ── Markers: tag tests to select/deselect them. ─────────────────────────────
# Run only these:  uv run pytest -m slow      Skip them:  uv run pytest -m "not slow"
@pytest.mark.slow
def test_marked_slow():
    assert estimate_cost(10, 10) > 0
