"""Memory abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Memory(ABC):
    """Abstract memory interface."""

    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """Store a message."""

    @abstractmethod
    def history(self) -> list[tuple[str, str]]:
        """Return conversation history."""

    @abstractmethod
    def clear(self) -> None:
        """Clear stored messages."""