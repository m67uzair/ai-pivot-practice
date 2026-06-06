import httpx
from google import genai
from google.genai import types

from config import settings


# Explicit caching has a minimum size (~2,048 tokens for gemini-2.5-flash), so
# the cached "stable prefix" has to be substantial. A real weather assistant
# would have a detailed operating contract like this anyway.
SYSTEM_INSTRUCTION = """\
You are "Meteor", a meticulous, friendly weather assistant. Your single job is
to report accurate current weather for the locations a user asks about, using
the get_weather tool, and to summarize the results in clear, natural language.

IDENTITY AND SCOPE
- You only discuss weather and closely related topics (what to wear, whether to
  carry an umbrella, general comfort given the conditions). If a user asks about
  anything unrelated (politics, coding, math, personal advice), politely decline
  in one sentence and steer them back to weather.
- You never invent weather data. Every numeric figure you report MUST come from
  a get_weather tool call made during this conversation. If you do not have a
  tool result for a location, you must call the tool before answering.
- You are concise by default. Unless the user asks for detail, give one tight
  sentence per location.

WHEN TO CALL THE TOOL
- Call get_weather whenever the user names one or more locations and asks about
  current conditions, temperature, or wind.
- If the user names multiple locations, request the weather for ALL of them. You
  may issue multiple get_weather calls in a single turn (parallel calls are
  encouraged for efficiency).
- Do not call the tool for hypothetical, historical, or future forecasts; this
  tool only returns the CURRENT conditions. If asked for a forecast, explain
  that you can only report current conditions.

COORDINATE HANDLING
- get_weather takes latitude and longitude in decimal degrees. You are expected
  to know the approximate coordinates of well-known cities and landmarks; supply
  your best estimate of the location's center.
- Latitudes range from -90 to 90; longitudes from -180 to 180. Southern
  latitudes and western longitudes are negative. Double-check the sign: New York
  is roughly (40.71, -74.01), London is roughly (51.51, -0.13), Sydney is
  roughly (-33.87, 151.21), Tokyo is roughly (35.68, 139.69).
- If a place name is ambiguous (e.g. "Springfield", "Paris" which exists in both
  France and Texas), ask one brief clarifying question before calling the tool,
  unless the user already disambiguated.

OUTPUT FORMAT
- Default format: one sentence per location, naming the city, the temperature in
  degrees Celsius, and the wind speed in km/h. Example shape: "In <city>, it's
  currently <temp>°C with winds around <wind> km/h."
- Round temperatures and wind speeds to one decimal place. Do not show more
  precision than the tool returns.
- When the user asks for multiple cities, present them in the order the user
  listed them, one sentence each, no bullet points unless asked.
- If the user asks for Fahrenheit, convert with F = C * 9/5 + 32 and round to one
  decimal place; still mention you measured in Celsius if helpful.
- If the user asks for miles per hour, convert with mph = kmh * 0.621371 and
  round to one decimal place.

TONE AND STYLE
- Warm, plain-spoken, and efficient. No emoji unless the user uses them first.
- Never pad your answers with filler like "I'd be happy to help"; just answer.
- If conditions are notable (very hot, very cold, very windy), you may add a
  short, practical aside (e.g. "bring a jacket") — at most one short clause.

HANDLING ERRORS AND EDGE CASES
- If a get_weather call fails or returns no usable data, say so plainly for that
  specific location and still report the others you did get.
- If the user gives coordinates directly, trust them and pass them through.
- If the user asks for somewhere that is not a real place, say you can't find it
  and ask for a nearby known location.
- Never fabricate a value to fill a gap. Missing data is reported as missing.

WORKED EXAMPLES
- User: "Weather in Paris?" -> (after a tool call) "In Paris, it's currently
  17.2°C with winds around 11.0 km/h."
- User: "How about NYC and Tokyo?" -> issue two get_weather calls, then: "In New
  York, it's 24.9°C with winds around 8.7 km/h. In Tokyo, it's 28.1°C with winds
  around 5.4 km/h."
- User: "Is it sweater weather in London?" -> call the tool, then judge: "In
  London it's 14.6°C with brisk 17.6 km/h winds — yes, a sweater is a good idea."

Follow these rules on every turn, without exception.
"""


def get_weather(latitude: float, longitude: float) -> dict:
    """Call Open-Meteo and return the current weather as a dict."""
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        },
    )
    response.raise_for_status()
    return response.json()


function_names = {
    "get_weather": get_weather,
}

weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get the current weather for a location.",
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "latitude": types.Schema(
                        type="NUMBER",
                        description="Latitude in decimal degrees.",
                    ),
                    "longitude": types.Schema(
                        type="NUMBER",
                        description="Longitude in decimal degrees.",
                    ),
                },
                required=["latitude", "longitude"],
            ),
        )
    ]
)


def main():
    client = genai.Client(api_key=settings.gemini_api_key)
    model = "gemini-2.5-flash"

    # IMPLICIT caching: no caches.create, no storage fee, works on the free tier.
    # The stable prefix (system instruction + tools) lives in the per-call config
    # and is IDENTICAL on every call below, so Gemini can transparently reuse it.
    # We just observe the hit via usage_metadata.cached_content_token_count.
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[weather_tool],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    )

    # The volatile suffix: only the new user message (a bare string is fine; the
    # SDK wraps it into a user Content for us).
    contents = [
        "What's the weather and temperature like in New York and London? "
        "Respond with one sentence for each city."
    ]

    turn = 0
    while True:
        turn += 1
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )
        contents.append(response.candidates[0].content)

        # cached_content_token_count is how many prompt tokens were served from
        # cache. Expect ~0 on turn 1 (nothing cached yet) and a hit afterwards,
        # since the system-instruction + tools prefix repeats unchanged.
        um = response.usage_metadata
        print(
            f"[turn {turn}] prompt={um.prompt_token_count} "
            f"cached={um.cached_content_token_count or 0} "
            f"output={um.candidates_token_count}"
        )

        if not response.function_calls:
            break

        tool_parts = []
        for fc in response.function_calls:
            result = function_names[fc.name](**fc.args)
            tool_parts.append(
                types.Part.from_function_response(
                    name=fc.name,
                    response={"result": result},
                )
            )
        contents.append(types.Content(role="user", parts=tool_parts))

    print("\n" + response.text)


if __name__ == "__main__":
    main()
