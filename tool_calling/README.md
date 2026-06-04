<!-- artifact
emoji: 🛠️
tasks: p1-w2-t4
stack: Python, groq, httpx, Pydantic
-->

# Tool Calling

Lets an LLM call a real function. The model is given a `get_weather` tool, decides when to invoke it, and the script runs the actual call (a live Open-Meteo request) and feeds the result back so the model can answer in natural language.

It asks for the weather in two cities, which exercises the **multi-turn tool loop**: the model requests one city, gets the result, requests the next, then summarizes both.

## How it works

1. A Pydantic model (`GetWeatherArgs` in [`models.py`](./models.py)) generates the tool's JSON schema via `.model_json_schema()`.
2. The first call uses `tool_choice="required"` to force the model to call the tool.
3. A `while response_message.tool_calls:` loop services each tool call — running `get_weather`, then appending a `role: "tool"` message (with the matching `tool_call_id` and the result `json.dumps`'d to a string) — and re-sends.
4. Once the model stops calling tools and returns text, the loop exits and the answer is printed.

The two gotchas this demonstrates: tool-result `content` must be a **string** (serialize with `json.dumps`), and each tool message needs its **`tool_call_id`**.

## Setup

Add your Groq key to the `.env` file at the project root:

```
GROQ_API_KEY=...
```

The weather API ([Open-Meteo](https://open-meteo.com/)) needs no key.

## Run

From the project root:

```bash
uv run tool_calling/main.py
```
