"""Application configuration loaded from environment variables."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, with safe defaults for an offline first run."""

    aura_name: str = "AURA"

    model_provider: Literal["dummy", "openai"] = "dummy"

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4.1-mini"

    memory_backend: Literal["memory", "sqlite"] = "sqlite"
    memory_path: Path = Path("data/aura_memory.db")

    log_level: str = "INFO"
    log_directory: Path = Path("data/logs")

    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("model_provider", mode="before")
    @classmethod
    def normalize_provider(cls, value: object) -> object:
        """Normalize provider names."""
        return value.casefold().strip() if isinstance(value, str) else value

    @field_validator("memory_backend", mode="before")
    @classmethod
    def normalize_memory_backend(cls, value: object) -> object:
        """Normalize memory backend names."""
        return value.casefold().strip() if isinstance(value, str) else value

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Validate logging level."""
        normalized = value.upper().strip()

        if normalized not in logging.getLevelNamesMapping():
            raise ValueError(f"Unsupported log level: {value!r}")

        return normalized

    @field_validator("log_directory")
    @classmethod
    def normalize_log_directory(cls, value: Path | str) -> Path:
        """Normalize log directory."""
        return Path(value)

    @field_validator("memory_path")
    @classmethod
    def normalize_memory_path(cls, value: Path | str) -> Path:
        """Normalize memory database path."""
        return Path(value)

    @model_validator(mode="after")
    def validate_openai_settings(self) -> Settings:
        """Validate provider-specific settings."""
        if self.model_provider == "openai" and self.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY must be set when model_provider='openai'.")

        return self
