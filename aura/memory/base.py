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

    def search_successful_strategy(
        self,
        intent: str,
    ) -> list[tuple[str, str]]:
        """Find successful previous strategies."""

        return [
            (role, content)
            for role, content in self.history()
            if (f"intent={intent}" in content and "success=True" in content)
        ]

    def rank_experiences(
        self,
        intent: str,
    ) -> list[tuple[str, str]]:
        """Rank previous experiences by value."""

        experiences = self.search_successful_strategy(
            intent,
        )

        return sorted(
            experiences,
            key=self._experience_score,
            reverse=True,
        )

    def _experience_score(
        self,
        experience: tuple[str, str],
    ) -> float:
        """Calculate experience value score."""

        _, content = experience

        score = 0.0

        if "success=True" in content:
            score += 1.0

        if "confidence=" in content:
            try:
                confidence = float(
                    content.split(
                        "confidence=",
                    )[1].split(
                        ";"
                    )[0],
                )

                score += confidence
            except (
                ValueError,
                IndexError,
            ):
                pass

        if "strategy=" in content:
            score += 0.1

        return score

    @abstractmethod
    def clear(self) -> None:
        """Clear stored messages."""
