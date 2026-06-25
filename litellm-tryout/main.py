import instructor
import litellm
from litellm import Router

from config import settings
from models import CalendarEvent

# ── Example 1: Router with fallbacks across the three free providers ─────────
# The Router picks "primary" first, and on failure walks the fallbacks in order.
router = Router(
    model_list=[
        {
            "model_name": "primary",
            "litellm_params": {
                "model": "gemini/gemini-2.5-flash",
                "api_key": settings.gemini_api_key,
            },
        },
        {
            "model_name": "backup-groq",
            "litellm_params": {
                "model": "groq/llama-3.3-70b-versatile",
                "api_key": settings.groq_api_key,
            },
        },
        {
            "model_name": "backup-openrouter",
            "litellm_params": {
                "model": "openrouter/openai/gpt-oss-120b:free",
                "api_key": settings.openrouter_api_key,
            },
        },
    ],
    # If "primary" (Gemini) fails, try Groq, then OpenRouter.
    fallbacks=[{"primary": ["backup-groq", "backup-openrouter"]}],
)


def fallback_demo():
    response = router.completion(
        model="primary",
        messages=[{"role": "user", "content": "In one sentence, what is LiteLLM?"}],
        # mock_testing_fallbacks forces the PRIMARY call to raise, so the
        # fallback chain actually runs. The real answer comes from the first
        # fallback (Groq) — proof the failover works without breaking anything.
        mock_testing_fallbacks=True,
    )
    print(f"answered by: {response.model}")
    print(response.choices[0].message.content)




# ── Example 2: Instructor layered on top of LiteLLM ──────────────────────────
def instructor_demo():
    client = instructor.from_litellm(router.completion)
    event = client.chat.completions.create(
        model="groq/llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Standup is on Monday with Sam, Jo, and Lee.",
            }
        ],
        response_model=CalendarEvent,
        api_key=settings.groq_api_key,
    )
    print(event)


def main():
    print("=== 1. Router fallback ===")
    fallback_demo()
    print("\n=== 2. Instructor (response_model) ===")
    instructor_demo()


if __name__ == "__main__":
    main()
