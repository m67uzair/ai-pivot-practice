from google import genai
from google.genai import types
from groq import Groq
from openai import OpenAI
from config import settings


def main():
    gemini_api_key = settings.gemini_api_key
    groq_api_key = settings.groq_api_key
    openrouter_api_key = settings.openrouter_api_key

    genai_client = genai.Client(
        api_key=gemini_api_key
    )

    groq_client = Groq(
        api_key=groq_api_key
    )

    openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key
    )

    separator = "-" * 60

    def show(label, text):
        print(f"\n{separator}")
        print(label)
        print(separator)
        print(text)

    print("Calling Gemini...", flush=True)
    gemini_response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents="how does AI work?",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    show("GEMINI 2.5 Flash (Google)", gemini_response.text)

    print("\nCalling Groq...", flush=True)
    groq_response = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a funny assistant"
            },
            {
                "role": "user",
                "content": "how does ai work?"
            },
        ],
        model="llama-3.3-70b-versatile"
    )
    show("Llama 3.3 70B (Groq)", groq_response.choices[0].message.content)

    print("\nCalling OpenRouter...", flush=True)
    openrouter_response = openrouter_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a rude assistant"
            },
            {
                "role": "user",
                "content": "how does ai work?"
            },
        ],
        model="moonshotai/kimi-k2.6:free"
    )
    show("Kimi v2.6 (OpenRouter)", openrouter_response.choices[0].message.content)


if __name__ == "__main__":
    main()
