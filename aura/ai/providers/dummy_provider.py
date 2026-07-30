"""A deterministic provider for offline development."""

from __future__ import annotations

from aura.ai.providers.base import AIProvider


class DummyProvider(AIProvider):
    """Provide predictable responses without network access."""

    @property
    def name(self) -> str:
        """Return the provider name."""
        return "dummy"

    def generate_response(self, user_message: str) -> str:
        """Generate a deterministic response."""
        normalized = user_message.strip().casefold()

        responses = {
            "merhaba": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
            "selam": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
            "hey": "Merhaba! Ben AURA. Şimdilik çekirdek modundayım.",
        }

        return responses.get(
            normalized,
            f"Mesajını aldım: {user_message.strip()}",
        )