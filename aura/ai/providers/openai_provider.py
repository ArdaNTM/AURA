"""OpenAI-backed implementation of the AURA provider contract."""

from __future__ import annotations

from openai import OpenAI

from aura.ai.providers.base import AIProvider


class OpenAIProvider(AIProvider):
    """Generate text with the OpenAI Responses API."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    @property
    def name(self) -> str:
        """Return the provider name."""
        return "openai"

    @property
    def model(self) -> str:
        """Return the configured model name."""
        return self._model

    def generate_response(self, user_message: str) -> str:
        """Return the provider's text output for a user message."""
        response = self._client.responses.create(
            model=self._model,
            input=user_message,
        )

        return response.output_text.strip() or "AURA şu anda yanıt üretemedi."