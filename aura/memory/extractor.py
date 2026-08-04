from __future__ import annotations

from aura.memory.models import (
    MemoryItem,
    MemoryType,
)


class MemoryExtractor:
    """
    Extract useful long term memories.
    """

    def extract(
        self,
        text: str,
    ) -> list[MemoryItem]:

        memories = []

        lower = text.lower()

        if "seviyorum" in lower or "tercih ederim" in lower:

            memories.append(
                MemoryItem(
                    content=text,
                    memory_type=MemoryType.PREFERENCE,
                    importance=0.8,
                    confidence=0.8,
                    tags=["preference"],
                )
            )

        if "proje" in lower or "project" in lower:

            memories.append(
                MemoryItem(
                    content=text,
                    memory_type=MemoryType.PROJECT,
                    importance=0.7,
                    confidence=0.7,
                    tags=["project"],
                )
            )

        return memories
