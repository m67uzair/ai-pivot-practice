<!-- artifact
emoji: 🧱
tasks: p1-w2-t2
stack: Python, openai, groq, Pydantic
-->

# Structured Outputs

Asks an LLM to return a JSON object that conforms to a Pydantic schema, then turns the response into typed model instances — no manual JSON wrangling (except in JSON mode, where you parse it yourself).

It demonstrates the same task three ways, using the OpenAI SDK pointed at Groq's OpenAI-compatible endpoint:

- **Responses API** — `client.responses.parse(..., text_format=CalenderEvent)`; read the result from `.output_parsed`.
- **Chat Completions API** — `client.chat.completions.parse(..., response_format=CalenderEvent)`; read the result from `.choices[0].message.parsed`.
- **JSON mode** — `client.chat.completions.create(..., response_format={"type": "json_object"})`; the model returns raw JSON text that you `json.loads` and validate yourself with `CalenderEvent.model_validate(...)`. The schema isn't enforced by the API, so the prompt has to describe the expected keys.

## Schema

The target shape is defined in [`models.py`](./models.py):

| Model              | Fields                                                        |
|--------------------|---------------------------------------------------------------|
| `CalenderEvent`    | `event_name`, `venue`, `date`, `participants: list[...]`      |
| `ParticipantEntry` | `name`                                                        |

Both models set `model_config = {"extra": "forbid"}`, which the `parse` structured-output APIs require (additional properties must be disallowed in the JSON schema).

## Setup

Add your Groq key to the `.env` file at the project root:

```
GROQ_API_KEY=...
```

## Run

From the project root:

```bash
uv run structured-outputs/main.py
```

This prints the parsed `CalenderEvent` from each of the three approaches.
