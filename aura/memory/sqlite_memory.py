"""SQLite backed memory implementation."""

from __future__ import annotations

import sqlite3

from aura.memory.base import Memory


class SQLiteMemory(Memory):
    """Persistent conversation memory using SQLite."""

    def __init__(
        self,
        path: str = "aura_memory.db",
    ) -> None:
        self._connection = sqlite3.connect(
            path,
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )

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

    def history(self) -> list[tuple[str, str]]:
        cursor = self._connection.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id ASC
            """
        )

        return list(
            cursor.fetchall(),
        )

    def search(
        self,
        query: str,
    ) -> list[tuple[str, str]]:
        """Search messages using SQLite."""

        cursor = self._connection.execute(
            """
            SELECT role, content
            FROM messages
            WHERE content LIKE ?
            ORDER BY id ASC
            """,
            (
                f"%{query}%",
            ),
        )

        return list(
            cursor.fetchall(),
        )

    def clear(self) -> None:
        self._connection.execute(
            """
            DELETE FROM messages
            """
        )

        self._connection.commit()

    def close(self) -> None:
        """Close database connection."""

        self._connection.close()