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
        self._snapshots.append(state.copy() if hasattr(state, "copy") else state)

    def rollback(self):

        if not self._snapshots:
            return None

        return self._snapshots.pop()

    def has_snapshot(self):

        return bool(self._snapshots)

    def clear(self):

        self._snapshots.clear()
