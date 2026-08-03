"""Memory consolidation utilities for AURA."""

from __future__ import annotations

from collections import defaultdict

from aura.memory.base import Memory


class MemoryConsolidator:
    """Reduce duplicate memories and preserve valuable experiences."""

    def consolidate(
        self,
        memory: Memory,
    ) -> int:
        """
        Consolidate stored memories.

        Returns number of removed duplicate entries.
        """

        history = memory.history()

        if not history:
            return 0

        unique: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()

        removed = 0

        for item in history:
            normalized = (
                item[0],
                self._normalize(
                    item[1],
                ),
            )

            if normalized in seen:
                removed += 1
                continue

            seen.add(normalized)
            unique.append(item)

        if removed:
            memory.clear()

            for role, content in unique:
                memory.add(
                    role,
                    content,
                )

        return removed

    def summarize_groups(
        self,
        memory: Memory,
    ) -> dict[str, list[str]]:
        """
        Group memories by intent or task.
        """

        groups: dict[str, list[str]] = defaultdict(list)

        for _, content in memory.history():

            key = self._extract_key(
                content,
            )

            groups[key].append(
                content,
            )

        return dict(groups)

    def _extract_key(
        self,
        content: str,
    ) -> str:
        """Extract memory grouping key."""

        for prefix in (
            "intent=",
            "task=",
        ):
            if prefix in content:
                value = content.split(prefix)[1].split(";")[0]

                return value

        return "general"

    def _normalize(
        self,
        content: str,
    ) -> str:
        """Normalize memory content."""

        return " ".join(
            content.casefold().split(),
        )
