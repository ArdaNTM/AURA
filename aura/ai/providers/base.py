"""Common contract for AI model providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """A provider capable of generating one text response."""

    @abstractmethod
    def generate_response(self, user_message: str) -> str:
        """Generate a response for one user message."""
        raise NotImplementedError
