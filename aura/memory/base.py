"""Memory abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


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

    def recall(
        self,
        query: str,
    ) -> list[tuple[str, str]]:
        """Recall ranked memories."""

        memories = self.search(
            query,
        )

        return sorted(
            memories,
            key=self._experience_score,
            reverse=True,
        )

    def _experience_score(
        self,
        experience: tuple[str, str],
    ) -> float:
        """
        Calculate adaptive experience value.

        Ranking considers:
        - success
        - confidence
        - strategy quality
        - recency
        """

        _, content = experience

        score = 0.0

        if "success=True" in content:
            score += 2.0

        if "success=False" in content:
            score -= 2.0

        if "confidence=" in content:
            try:
                confidence = float(
                    content.split(
                        "confidence=",
                    )[1].split(
                        ";",
                    )[0],
                )

                score += confidence

            except (
                ValueError,
                IndexError,
            ):
                pass

        if "strategy=safe_tool_execution" in content:
            score += 0.5

        elif "strategy=tool_execution" in content:
            score += 0.2

        if "timestamp=" in content:
            try:
                timestamp = content.split(
                    "timestamp=",
                )[1].split(
                    ";",
                )[0]

                created = datetime.fromisoformat(
                    timestamp,
                )

                age_days = (datetime.now() - created).days

                score -= min(
                    age_days * 0.01,
                    1.0,
                )

            except (
                ValueError,
                IndexError,
            ):
                pass

        return score

    def consolidate(
        self,
    ) -> int:
        """
        Consolidate stored memories.

        Default implementation does nothing.
        """

        return 0

    @abstractmethod
    def clear(self) -> None:
        """Clear stored messages."""
