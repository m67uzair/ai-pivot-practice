from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_here = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_here.parent / ".env",
                                      extra="ignore")

    gemini_api_key: str
    debug: bool = False


settings = Settings()
