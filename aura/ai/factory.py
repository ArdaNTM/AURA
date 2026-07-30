"""Construct configured AI providers."""

from __future__ import annotations

from collections.abc import Callable

from aura.ai.providers.base import AIProvider
from aura.ai.providers.dummy_provider import DummyProvider
from aura.ai.providers.openai_provider import OpenAIProvider
from aura.config.settings import Settings


class ProviderFactory:
    """Create AI providers from application settings."""

    _providers: dict[str, Callable[[Settings], AIProvider]] = {
        "dummy": lambda settings: DummyProvider(),
        "openai": lambda settings: OpenAIProvider(
            api_key=settings.openai_api_key.get_secret_value(),
            model=settings.openai_model,
        ),
    }

    @classmethod
    def create(cls, settings: Settings) -> AIProvider:
        """Create the configured AI provider."""
        try:
            factory = cls._providers[settings.model_provider]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported model provider: {settings.model_provider!r}"
            ) from exc

        return factory(settings)

    @classmethod
    def register(
        cls,
        name: str,
        factory: Callable[[Settings], AIProvider],
    ) -> None:
        """Register a new provider."""
        cls._providers[name.casefold()] = factory
