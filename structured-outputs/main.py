import openai
from config import settings
from models import CalenderEvent
import json


client = openai.OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# using responses api
responses_response = client.responses.parse(
    model="openai/gpt-oss-120b",
    instructions="You are ai assitant which gives dummy event info",
    input="tell me about jasons wedding",
    text_format=CalenderEvent,
)

# using chat completions api
completions_response = client.chat.completions.parse(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are ai assitant which gives dummy event info"},
        {"role": "user", "content": "You are ai assitant which gives dummy event info"},
    ],
    response_format=CalenderEvent,
)

# using json mode
json_mode_response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are an AI assistant which gives dummy event info. Respond in JSON with keys: event_name, venue, date, participants (a list of {name})."},
        {"role": "user", "content": "tell me about jason's wedding"},
    ],
    response_format={"type": "json_object"},   # ← JSON mode
)

raw = json_mode_response.choices[0].message.content
data = json.loads(raw)
event = CalenderEvent.model_validate(data)
print(event)

print(responses_response.output_parsed)
print(completions_response.choices[0].message.parsed)
