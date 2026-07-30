"""A deterministic provider used before a real model is connected."""

from __future__ import annotations

from aura.ai.providers.base import AIProvider


class DummyProvider(AIProvider):
    """Provide a predictable conversational experience for Sprint 1."""

    def generate_response(self, user_message: str) -> str:
        """Return a friendly response without requiring network access."""
        normalized = user_message.strip().casefold()
        if normalized in {"merhaba", "selam", "hey"}:
            return "Merhaba! Ben AURA. Şimdilik çekirdek moddayım."
        return f"Mesajını aldım: {user_message.strip()}"
