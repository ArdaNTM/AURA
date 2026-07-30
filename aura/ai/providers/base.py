"""Common contract for AI model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Base interface for all AI providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @abstractmethod
    def generate_response(self, user_message: str) -> str:
        """Generate a response for a user message."""
        raise NotImplementedError