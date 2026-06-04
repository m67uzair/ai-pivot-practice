import json
import httpx

from config import settings
from groq import Groq
from models import GetWeatherArgs


def main():

    def get_weather(latitude: float, longitude: float):
        response = httpx.get("https://api.open-meteo.com/v1/forecast",
                             params={
                                "latitude": latitude,
                                "longitude": longitude,
                                "current": "temperature_2m,wind_speed_10m"
                                },)
        response.raise_for_status()
        return json.dumps(response.json())


    function_names = {
        "get_weather": get_weather,
    }
    
    messages = [
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": "What's the weather and temperature like in New York and London? Respond with one sentence for each city. Use tools to get the current weather and temperature."},
    ]
    
    tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": GetWeatherArgs.model_json_schema(),
    },}]

    groq_client = Groq(
        api_key=settings.groq_api_key,
        )
    
    def send_message(messages, tool_choice="auto"):
        groq_response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            tools=tools,
            tool_choice=tool_choice,
            messages=messages,
        )

        return groq_response.choices[0].message;

    # Force a tool call on the first turn; afterwards let the model decide.
    response_message = send_message(messages, tool_choice="required")

    # Keep servicing tool calls until the model replies with text instead.
    while response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = function_names[function_name]
            tool_response = function_to_call(**function_args)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_response,
            })

        response_message = send_message(messages)

    print(response_message.content)
    
    


if __name__ == "__main__":
    main()
