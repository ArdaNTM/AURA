"""Rollback support for autonomous execution."""

from __future__ import annotations


class RollbackManager:
    """Track reversible operations."""

    def __init__(self):
        self._snapshots = []

    def checkpoint(
        self,
        state,
    ):
        self._snapshots.append(
            state,
        )

    def rollback(self):
        if not self._snapshots:
            return None

        return self._snapshots.pop()

    def clear(self):
        self._snapshots.clear()
