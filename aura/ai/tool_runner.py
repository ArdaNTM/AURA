"""Tool execution coordinator."""

from __future__ import annotations

from typing import Any

from aura.core.tool_result import ToolResult
from aura.core.tools import ToolRegistry


class ToolRunner:
    """Execute tools through the registry."""

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self._registry = registry

    @property
    def registry(self) -> ToolRegistry:
        """Return the underlying registry."""

        return self._registry

    def run(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute a registered tool."""

        if not self._registry.has(
            name,
        ):
            return ToolResult(
                name=name,
                output="",
                success=False,
                error=f"Unknown tool '{name}'.",
            )

        return self._registry.execute(
            name,
            *args,
            **kwargs,
        )
