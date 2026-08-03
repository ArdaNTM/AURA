"""Mouse control abstraction."""

from __future__ import annotations


class MouseController:
    """Control mouse actions."""

    def move(
        self,
        x: int,
        y: int,
    ) -> str:
        """Move mouse."""

        return f"Mouse moved to ({x},{y})"

    def click(
        self,
        x: int,
        y: int,
    ) -> str:
        """Click mouse."""

        return f"Mouse clicked at ({x},{y})"

    def double_click(
        self,
        x: int,
        y: int,
    ) -> str:
        """Double click mouse."""

        return f"Mouse double clicked at ({x},{y})"
