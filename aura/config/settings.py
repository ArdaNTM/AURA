"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, with safe defaults for an offline first run."""

    aura_name: str = "AURA"
    model_provider: str = "dummy"
    openai_api_key: str = ""
    log_level: str = "INFO"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
