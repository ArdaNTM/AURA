"""In-memory memory implementation."""

from __future__ import annotations

from aura.memory.base import Memory


class InMemoryMemory(Memory):
    """Simple in-process conversation memory."""

    def __init__(self) -> None:
        self._messages: list[tuple[str, str]] = []

    def add(self, role: str, content: str) -> None:
        self._messages.append((role, content))

    def history(self) -> list[tuple[str, str]]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()