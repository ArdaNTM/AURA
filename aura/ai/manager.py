"""AI service boundary used by the rest of AURA."""

from __future__ import annotations

from aura.ai.providers.base import AIProvider


class AIManager:
    """Delegate response generation to the configured provider."""

    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    @property
    def provider(self) -> AIProvider:
        """Return the active AI provider."""
        return self._provider

    def set_provider(self, provider: AIProvider) -> None:
        """Replace the active AI provider."""
        self._provider = provider

    def respond(self, user_message: str) -> str:
        """Generate a response for a user message."""
        return self._provider.generate_response(user_message)