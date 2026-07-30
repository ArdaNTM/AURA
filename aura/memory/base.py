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

        Default implementation performs
        simple keyword matching over history.
        """

        normalized = query.casefold()

        return [
            (role, content)
            for role, content in self.history()
            if normalized in content.casefold()
        ]

    @abstractmethod
    def clear(self) -> None:
        """Clear stored messages."""