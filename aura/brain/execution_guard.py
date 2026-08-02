"""Execution guard for AURA tool execution."""

from __future__ import annotations

from aura.brain.models import Decision
from aura.core.tools import ToolRegistry


class ExecutionGuard:
    """Validate execution before running tools."""

    def __init__(
        self,
        tools: ToolRegistry | None = None,
    ) -> None:
        self._tools = tools

    def can_execute(
        self,
        decision: Decision,
    ) -> bool:
        """Check whether decision can execute."""

        if not decision.requires_tool:
            return True

        if not decision.target:
            return False

        if not self._tools:
            return False

        return self._tools.has(
            decision.target,
        )
