<!-- artifact
emoji: 🧑‍🏫
tasks: p1-w2-t3
stack: Python, instructor, Pydantic
-->

# Instructor

Gets structured, schema-validated output from an LLM using the [`instructor`](https://python.useinstructor.com/) library instead of a provider's native parse API. You pass a Pydantic model as `response_model` and `instructor` handles the prompting, validation, and retries, returning a typed instance directly.

Here it asks an OpenRouter-hosted model for career advice and coerces the reply into a `CareerAdvice` model ([`models.py`](./models.py)).

## Schema

| Model          | Fields                                              |
|----------------|-----------------------------------------------------|
| `CareerAdvice` | `summary`, `steps: list[CareerStep]`, `timeline_months` |
| `CareerStep`   | `title`, `detail`                                   |

## How it works

- `instructor.from_provider("openrouter/...")` builds a client; the `openrouter/` prefix tells `instructor` which provider to wire up.
- `extra_body={"provider": {"require_parameters": True}}` forces OpenRouter to only route to backends that support structured-output parameters.
- `client.create(..., response_model=CareerAdvice)` returns a validated `CareerAdvice` — no manual JSON parsing.

## Setup

Add your OpenRouter key to the `.env` file at the project root:

```
OPENROUTER_API_KEY=...
```

## Run

From the project root:

```bash
uv run instructor/main.py
```
