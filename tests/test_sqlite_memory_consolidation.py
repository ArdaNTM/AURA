from pathlib import Path

from aura.memory.sqlite_memory import SQLiteMemory


def test_sqlite_memory_consolidates_duplicates(
    tmp_path: Path,
):

    db_path = tmp_path / "memory.db"

    memory = SQLiteMemory(
        str(db_path),
    )

    memory.add(
        "assistant",
        "intent=test; success=True",
    )

    memory.add(
        "assistant",
        "intent=test; success=True",
    )

    removed = memory.consolidate()

    assert removed == 1

    assert memory.history() == [
        (
            "assistant",
            "intent=test; success=True",
        )
    ]

    memory.close()
