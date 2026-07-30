"""Construct configured AI providers."""

from __future__ import annotations

from aura.ai.providers.base import AIProvider
from aura.ai.providers.dummy_provider import DummyProvider
from aura.config.settings import Settings


class ProviderFactory:
    """Select a provider without exposing provider details to the application."""

    @staticmethod
    def create(settings: Settings) -> AIProvider:
        """Create the provider selected by configuration."""
        _ = settings
        return DummyProvider()
