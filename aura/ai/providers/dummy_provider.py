"""A deterministic provider for offline development."""

from __future__ import annotations

from typing import Any

from aura.ai.provider_response import ProviderResponse
from aura.ai.providers.base import AIProvider


class DummyProvider(AIProvider):
    """Provide predictable responses without network access."""

    @property
    def name(self) -> str:
        """Return the provider name."""
        return "dummy"

    def generate_response(
        self,
        user_message: str,
        history: list[dict[str, str]] | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> ProviderResponse:
        """Generate a deterministic response."""

        _ = history
        _ = tools

        normalized = user_message.strip().casefold()

        responses = {
            "merhaba": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
            "selam": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
            "hey": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
        }

        response = responses.get(
            normalized,
            f"Mesajını aldım: {user_message.strip()}",
        )

        return ProviderResponse(
            text=response,
        )