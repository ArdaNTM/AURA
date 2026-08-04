"""Persistent autonomous task storage."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from aura.agent.autonomous_task import AutonomousTask


class TaskStore:
    """SQLite storage for autonomous tasks."""

    def __init__(
        self,
        path: str = "aura_tasks.db",
    ) -> None:
        self._connection = sqlite3.connect(
            path,
        )

        self._connection.execute("""
            CREATE TABLE IF NOT EXISTS autonomous_tasks (
                task_id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                interval INTEGER NOT NULL,
                enabled INTEGER NOT NULL,
                last_run TEXT,
                run_count INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                result TEXT,
                error TEXT
            )
            """)

        self._connection.commit()

    def save(
        self,
        task: AutonomousTask,
    ) -> None:
        """Persist task."""

        self._connection.execute(
            """
            INSERT OR REPLACE INTO autonomous_tasks
            (
                task_id,
                description,
                interval,
                enabled,
                last_run,
                run_count,
                status,
                result,
                error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.task_id,
                task.description,
                task.interval,
                int(task.enabled),
                task.last_run.isoformat() if task.last_run else None,
                task.run_count,
                task.status,
                str(task.result) if task.result is not None else None,
                task.error,
            ),
        )

        self._connection.commit()

    def load_all(
        self,
    ) -> list[AutonomousTask]:
        """Load stored tasks."""

        cursor = self._connection.execute("""
            SELECT
                task_id,
                description,
                interval,
                enabled,
                last_run,
                run_count,
                status,
                result,
                error
            FROM autonomous_tasks
            """)

        tasks = []

        for row in cursor.fetchall():

            task = AutonomousTask(
                description=row[1],
                interval=row[2],
                enabled=bool(row[3]),
                task_id=row[0],
            )

            if row[4]:
                task.last_run = datetime.fromisoformat(
                    row[4],
                )

            task.run_count = row[5]
            task.status = row[6]
            task.result = row[7]
            task.error = row[8]

            tasks.append(
                task,
            )

        return tasks

    def delete(
        self,
        task_id: str,
    ) -> None:
        """Delete task."""

        self._connection.execute(
            """
            DELETE FROM autonomous_tasks
            WHERE task_id = ?
            """,
            (task_id,),
        )

        self._connection.commit()
