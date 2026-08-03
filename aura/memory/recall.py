"""Memory recall engine for AURA."""

from __future__ import annotations

from aura.memory.base import Memory


class RecallEngine:
    """Retrieve and rank memories."""

    def __init__(
        self,
        memory: Memory,
    ) -> None:
        self._memory = memory

    @property
    def memory(
        self,
    ) -> Memory:
        """Return backing memory."""

        return self._memory

    def recall(
        self,
        query: str,
    ) -> list[tuple[str, str]]:
        """Recall relevant memories."""

        memories = self._memory.search(
            query,
        )

        return self.rank(
            memories,
        )

    def rank(
        self,
        memories: list[tuple[str, str]],
    ) -> list[tuple[str, str]]:
        """Rank memories using memory scoring."""

        return sorted(
            memories,
            key=self._memory._experience_score,
            reverse=True,
        )

    def recall_successful(
        self,
        intent: str,
    ) -> list[tuple[str, str]]:
        """Recall successful strategies."""

        return self._memory.rank_experiences(
            intent,
        )
