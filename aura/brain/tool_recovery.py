"""Tool failure recovery system."""

from __future__ import annotations

from aura.core.tool_result import ToolResult


class ToolRecovery:
    """Handle failed tool executions."""

    def __init__(
        self,
        max_retries: int = 1,
    ) -> None:
        self._max_retries = max_retries

    @property
    def max_retries(
        self,
    ) -> int:
        """Return retry limit."""

        return self._max_retries

    def should_retry(
        self,
        result: ToolResult,
        attempt: int,
    ) -> bool:
        """Decide whether retry is allowed."""

        if result.success:
            return False

        return attempt < self._max_retries

    def analyze(
        self,
        result: ToolResult,
    ) -> dict[str, object]:
        """Analyze failed execution."""

        return {
            "tool": result.name,
            "error": result.error,
            "retry_available": True,
        }
