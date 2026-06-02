<!-- artifact
emoji: 💬
tasks: p1-w1-t3
stack: Python, google-genai, groq, openai
-->

# Chat Completion Script

Sends the same prompt to three different LLM providers and prints their responses side-by-side for comparison.

## Models compared

| Provider   | Model                     | SDK used            |
|------------|---------------------------|---------------------|
| Google     | gemini-2.5-flash          | `google-genai`      |
| Groq       | llama-3.3-70b-versatile   | `groq`              |
| OpenRouter | deepseek-chat-v3.1 (free) | `openai` (compat)   |

## Setup

Add the following keys to the `.env` file at the project root:

```
GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
```

## Run

From the project root:

```bash
uv run chat-completion-script/main.py
```
