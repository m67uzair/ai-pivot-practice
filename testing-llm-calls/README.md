<!-- artifact
emoji: 🧪
tasks: p1-w3-t4
stack: Python, pytest, pytest-mock, respx
-->

# Testing LLM Calls

A runnable cheat-sheet for testing code that calls LLMs, using **pytest**,
**pytest-mock**, **respx**, and **pytest-asyncio**. Every concept has a passing
example you can read and tweak — so you can skim this instead of four doc sites.

`app.py` is the code under test (the kinds of LLM call: sync chat, async chat,
streaming, tool calling, structured output). Each `test_0*.py` teaches one tool.

## The one decision that matters: mock the method, or mock the HTTP?

| | **pytest-mock** (`mocker`) | **respx** |
|---|---|---|
| Replaces | the SDK *method* (`client.chat.completions.create`) | the *HTTP request* (httpx) underneath the SDK |
| Your real code that runs | just your function | your function **+ the whole SDK** (request build, auth, JSON→object parsing) |
| Speed | fastest | fast |
| Catches | your logic bugs | logic bugs **+** wrong URL/payload, parse errors, retry behavior |
| Use when | you just need "the model returned X" | you want confidence the real request/response round-trips |

Rule of thumb: **`mocker` for most unit tests; `respx` when the wire format matters** (streaming, structured output, error/retry handling).

## pytest essentials (`test_01`)

```python
def test_x(): assert f() == 3              # bare assert; pytest shows a rich diff
pytest.approx(0.004)                        # float comparison
with pytest.raises(ValueError, match="re"): ...   # assert an exception
@pytest.mark.parametrize("a,b,exp", [...])  # one test body × many cases
@pytest.fixture                             # reusable setup, injected by arg name
@pytest.mark.slow                           # tag tests; run `-m slow` / `-m "not slow"`
```
Markers must be registered in `pyproject.toml` (`[tool.pytest.ini_options] markers=[...]`) or pytest warns.

## pytest-mock (`test_02`)

```python
m = mocker.patch.object(app.client.chat.completions, "create", return_value=fake)
m.return_value = fake          # canned result
m.side_effect = RuntimeError() # raise instead
m.side_effect = [a, b]         # different result per call
m.assert_called_once()         # was it called?
m.call_args.kwargs["model"]    # what was it called WITH?
mocker.spy(obj, "method")      # wrap the real thing, record calls
```
`mocker` auto-undoes every patch at test end — no `with`/decorators. Use it over raw `unittest.mock`.

## respx (`test_03`)

```python
@respx.mock                                            # or the `respx_mock` fixture
route = respx.post(URL).mock(return_value=httpx.Response(200, json={...}))
respx.post(URL).respond(500, json={...})               # shorthand
respx.post(URL).mock(side_effect=[r1, r2])             # sequence
respx.post(URL).mock(side_effect=httpx.ConnectError()) # network failure
route.called; route.call_count
route.calls.last.request.content                       # the ACTUAL bytes sent
```

## pytest-asyncio (`test_04`)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"   # async tests need NO marker (strict mode needs @pytest.mark.asyncio)
```
```python
async def test_thing(): ...                 # just works in auto mode
mocker.patch.object(...)                     # auto-returns AsyncMock for async methods
m.assert_awaited_once()                      # awaited, not just called
```

## LLM-specific gotchas this artifact bakes in

- **`MagicMock(name="x")` does NOT set `.name`** — it names the mock's repr. For tool calls you must do `tc.function.name = "get_weather"` *after* construction. (`conftest.py`, `test_02`)
- **The SDK auto-retries 5xx and connection errors.** A `503→200` respx sequence is consumed by *one* call (it recovers transparently); a `httpx.ConnectError` comes back as `groq.APIConnectionError`, not the raw httpx type. (`test_03`)
- **Async needs `assert_awaited_*`**, not just `assert_called_*`. (`test_04`)
- **Streaming = an SSE body**: `data: {chunk json}\n\n` lines ending in `data: [DONE]`, served as `text/event-stream`. The SDK decodes it back into chunk objects. (`conftest.sse_body`, `test_04`)
- **Mock the right client object**: `app.client` (sync) vs `app.async_client` (async) are different instances.

## Setup & run

No API key needed — every test mocks the call. From the repo root:

```bash
uv sync                       # installs the dev group (pytest, pytest-mock, respx, pytest-asyncio)
uv run pytest                 # testpaths is pinned to this folder in pyproject
uv run pytest testing-llm-calls/test_02_mocker.py -v   # one file
uv run pytest -m "not slow"   # skip slow-marked tests
uv run pytest -k tool         # only tests with "tool" in the name
```
