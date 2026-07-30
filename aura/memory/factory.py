"""Memory backend factory."""

from __future__ import annotations

from aura.config.settings import Settings
from aura.memory.base import Memory
from aura.memory.in_memory import InMemoryMemory
from aura.memory.sqlite_memory import SQLiteMemory


class MemoryFactory:
    """Create configured memory backend."""

    @staticmethod
    def create(settings: Settings) -> Memory:
        """Create memory implementation from settings."""

        if settings.memory_backend == "sqlite":
            return SQLiteMemory(
                str(settings.memory_path),
            )

        return InMemoryMemory()