"""SQLite backed memory implementation."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from aura.memory.base import Memory


class SQLiteMemory(Memory):
    """Persistent conversation memory using SQLite."""

    def __init__(
        self,
        path: str = "aura_memory.db",
    ) -> None:
        database_path = Path(path)

        if database_path.parent != Path("."):
            database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self._connection = sqlite3.connect(
            database_path,
        )

        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """)

        self._connection.commit()

    def add(
        self,
        role: str,
        content: str,
    ) -> None:
        self._connection.execute(
            """
            INSERT INTO messages (role, content)
            VALUES (?, ?)
            """,
            (
                role,
                content,
            ),
        )

        self._connection.commit()

    def history(
        self,
    ) -> list[tuple[str, str]]:
        cursor = self._connection.execute("""
            SELECT role, content
            FROM messages
            ORDER BY id ASC
            """)

        return list(cursor.fetchall())

    def clear(
        self,
    ) -> None:
        self._connection.execute("""
            DELETE FROM messages
            """)

        self._connection.commit()

    def close(
        self,
    ) -> None:
        """Close database connection."""

        self._connection.close()
