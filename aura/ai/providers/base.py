"""Common contract for AI model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from aura.ai.provider_response import ProviderResponse


class AIProvider(ABC):
    """Base interface for all AI providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @abstractmethod
    def generate_response(
        self,
        user_message: str,
        history: list[dict[str, str]] | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> ProviderResponse:
        """Generate a response for a user message."""
        raise NotImplementedError