from __future__ import annotations

from aura.memory.models import (
    MemoryItem,
    MemoryType,
)


class LongTermMemory:
    """
    Persistent semantic memory layer.
    """

    def __init__(self):
        self._items: list[MemoryItem] = []

    def remember(
        self,
        item: MemoryItem,
    ) -> None:

        self._items.append(item)

    def recall(
        self,
        query: str,
    ) -> list[MemoryItem]:

        words = query.lower().split()

        results = []

        for item in self._items:

            text = item.content.lower()

            if any(word in text for word in words):
                results.append(item)

        return sorted(
            results,
            key=lambda x: x.score(),
            reverse=True,
        )

    def by_type(
        self,
        memory_type: MemoryType,
    ):

        return [item for item in self._items if item.memory_type == memory_type]

    def all(self):

        return list(self._items)
