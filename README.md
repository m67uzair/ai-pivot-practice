# ai-pivot-practice

The artifact repository for my AI-pivot practice tasks — **Dart/Flutter → AI Engineer** (Karachi → remote, 25-week plan).

This is a `uv`-managed monorepo: one shared virtual environment, multiple self-contained practice projects in their own folders.

## Artifacts

| Project | What it does | Stack |
|---------|--------------|-------|
| [`pokemon-cli`](./pokemon-cli) | Fetches the PokéAPI, parses the response into typed Pydantic models, prints it. | Python · httpx · Pydantic |
| [`chat-completion-script`](./chat-completion-script) | Sends one prompt to Gemini, Groq (Llama 3.3), and OpenRouter and prints the responses side-by-side for comparison. | Python · google-genai · groq · openai |

## Setup

```bash
uv sync
```

API keys live in a `.env` at the repo root (git-ignored):

```
GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Run

```bash
uv run pokemon-cli/main.py
uv run chat-completion-script/main.py
```
