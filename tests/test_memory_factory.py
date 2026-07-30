from pathlib import Path

from aura.config.settings import Settings
from aura.memory.factory import MemoryFactory
from aura.memory.in_memory import InMemoryMemory
from aura.memory.sqlite_memory import SQLiteMemory


def test_factory_creates_in_memory_backend():
    settings = Settings(
        memory_backend="memory",
    )

    memory = MemoryFactory.create(settings)

    assert isinstance(memory, InMemoryMemory)


def test_factory_creates_sqlite_backend(tmp_path: Path):
    settings = Settings(
        memory_backend="sqlite",
        memory_path=tmp_path / "memory.db",
    )

    memory = MemoryFactory.create(settings)

    assert isinstance(memory, SQLiteMemory)
