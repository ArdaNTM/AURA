"""Background task persistence."""

from __future__ import annotations

import sqlite3

from aura.brain.background_task import BackgroundTask


class TaskStore:
    """Persist background tasks."""

    def __init__(
        self,
        path: str = "aura_tasks.db",
    ) -> None:

        self._connection = sqlite3.connect(
            path,
        )

        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT,
                status TEXT,
                progress REAL,
                current_step TEXT
            )
            """)

        self._connection.commit()

    def save(
        self,
        task: BackgroundTask,
    ) -> None:

        self._connection.execute(
            """
            INSERT OR REPLACE INTO tasks
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                task.task_id,
                task.description,
                task.status,
                task.progress,
                task.current_step,
            ),
        )

        self._connection.commit()

    def get(
        self,
        task_id: str,
    ) -> BackgroundTask | None:

        row = self._connection.execute(
            """
            SELECT id, description, status,
                   progress, current_step
            FROM tasks
            WHERE id=?
            """,
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        return BackgroundTask(
            description=row[1],
            status=row[2],
            progress=row[3],
            current_step=row[4],
            task_id=row[0],
        )
