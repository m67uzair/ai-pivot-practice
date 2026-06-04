from models import CareerAdvice
from config import settings
import instructor


def main():
    openrouter_api_key = settings.openrouter_api_key

    openrouter_client = instructor.from_provider(
        "openrouter/openai/gpt-oss-120b:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )

    response = openrouter_client.create(
        messages=[
            {
                "role": "system",
                "content": "You are a blunt, funny career coach who gives concrete, no-fluff advice.",
            },
            {
                "role": "user",
                "content": "How can I switch my career to an AI focus in 2026?",
            },
        ],
        extra_body={
            "provider": {
                "require_parameters": True
                }
            },
        response_model=CareerAdvice,
    )

    print(response)


if __name__ == "__main__":
    main()
