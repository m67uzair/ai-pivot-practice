This week I built an AI pull-request reviewer, and used it to learn a big chunk of the modern LLM-app stack.

Open a PR and a few seconds later a bot comments on it with the bugs it found, how serious each one is, and a suggested fix. Real structured feedback, not a vague summary paragraph.

What went into it:

• FastAPI for the webhook, with HMAC signature verification so only GitHub can trigger it, and background tasks so the webhook responds instantly while the review runs in the background.
• LiteLLM as a single interface over multiple providers, with automatic fallbacks when one is down.
• Structured outputs through instructor: the model is forced to return a Pydantic-validated schema (file, severity, suggested fix), and it re-asks the model automatically when the shape is wrong.
• SQLAlchemy + Alembic to persist every review behind proper migrations.
• A multi-stage Docker build, GitHub Actions CI running the tests on every commit, deployed on Railway.

I tested it on a PR with three subtle bugs planted on purpose: a mutable default argument, a money-transfer function with no balance check, and an interest calculation missing a divide-by-100. It caught all three, with the right severities.

It reviews a ~500-line diff in about 3 seconds.

The lessons that stuck: getting an LLM to reliably return valid structured data instead of hoping over a raw JSON string, why "async" does not mean "returns immediately," and how much unglamorous-but-critical plumbing (signature verification, migrations, CI, deploy) sits around the actual model call.

Repo and a 40-second demo in the comments.

#AIEngineering #Python #LLM #BuildInPublic
