"""LLM provider abstraction for AURA."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Base interface for language model providers."""

    @abstractmethod
    def complete(
        self,
        prompt: str,
    ) -> str:
        """Generate a completion from prompt."""
