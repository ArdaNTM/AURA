from pathlib import Path

from aura.memory.sqlite_memory import SQLiteMemory


def test_sqlite_memory_starts_empty(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    assert memory.history() == []

    memory.close()


def test_sqlite_add_message(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    memory.add(
        "user",
        "Hello",
    )

    memory.add(
        "assistant",
        "Hi!",
    )

    assert memory.history() == [
        (
            "user",
            "Hello",
        ),
        (
            "assistant",
            "Hi!",
        ),
    ]

    memory.close()


def test_sqlite_persists_data(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    memory.add(
        "user",
        "Remember this",
    )

    memory.close()

    memory2 = SQLiteMemory(
        str(db_path),
    )

    assert memory2.history() == [
        (
            "user",
            "Remember this",
        ),
    ]

    memory2.close()


def test_sqlite_clear(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    memory.add(
        "user",
        "Hello",
    )

    memory.clear()

    assert memory.history() == []

    memory.close()


def test_sqlite_search(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    memory.add(
        "user",
        "AURA projesine devam ediyoruz",
    )

    memory.add(
        "assistant",
        "Sprint 4 başladı",
    )

    result = memory.search(
        "AURA",
    )

    assert result == [
        (
            "user",
            "AURA projesine devam ediyoruz",
        )
    ]

    memory.close()


def test_sqlite_search_empty(tmp_path: Path):
    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    result = memory.search(
        "bulunmayan",
    )

    assert result == []

    memory.close()
