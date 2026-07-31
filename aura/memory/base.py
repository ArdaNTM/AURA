"""Memory abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Memory(ABC):
    """Abstract memory interface."""

    @abstractmethod
    def add(
        self,
        role: str,
        content: str,
    ) -> None:
        """Store a message."""

    @abstractmethod
    def history(self) -> list[tuple[str, str]]:
        """Return conversation history."""

    def search(
        self,
        query: str,
    ) -> list[tuple[str, str]]:
        """
        Search stored memories.

        Performs simple keyword matching
        using query terms.
        """

        words = [word for word in query.casefold().split() if len(word) > 2]

        return [
            (role, content)
            for role, content in self.history()
            if any(word in content.casefold() for word in words)
        ]

    @abstractmethod
    def clear(self) -> None:
        """Clear stored messages."""
