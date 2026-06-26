from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_here = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_here.parent / ".env",
                                      extra="ignore")

    github_token: str
    webhook_secret: str
    debug: bool = False


settings = Settings()
