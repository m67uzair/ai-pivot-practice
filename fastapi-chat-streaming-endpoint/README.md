<!-- artifact
emoji: 📡
tasks: p1-w3-t3
stack: Python, fastapi, groq
-->

# FastAPI Chat Streaming Endpoint

A FastAPI `GET /chat?prompt=...` endpoint that streams an LLM response token-by-token over Server-Sent Events, using Groq (Llama 3.3) with `stream=True`.

## How it streams

- `StreamingResponse(get_chat_stream(), media_type="text/event-stream")` sends each token as it's produced, framed as SSE (`data: <token>\n\n`).
- It uses the **async** Groq client (`AsyncGroq`) with `await ... create(stream=True)` and `async for chunk in stream`. This matters: the `async for` hands control back to the event loop after each token, so FastAPI flushes it immediately.

### The gotcha this demonstrates

The naive version used the **synchronous** Groq client with `for chunk in stream` inside an `async def` generator. That blocking iteration never yields to the event loop, so the whole response is buffered and arrives **all at once** at the end — not streamed. `async` alone isn't concurrency; you only get streaming at real `await`/yield points. Fix: use `AsyncGroq` + `async for` (or make the generator a plain `def` so FastAPI runs it in a threadpool).

> Note: streaming also requires nothing downstream to buffer — a reverse proxy (`proxy_buffering`), gzip middleware, or `curl` without `-N` will re-batch the tokens.

## Setup

Add your Groq key to the `.env` file at the project root:

```
GROQ_API_KEY=...
```

## Run

From the project root:

```bash
uv run fastapi dev fastapi-chat-streaming-endpoint/main.py
```

Then watch tokens arrive incrementally (`-N` disables curl's own buffering):

```bash
curl -N "http://127.0.0.1:8000/chat?prompt=tell+me+a+short+joke"
```
