"""Tool execution coordinator."""

from __future__ import annotations

from typing import Any

from aura.core.tools import ToolRegistry
from aura.core.tool_result import ToolResult


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

        return self._registry.execute(
            name,
            *args,
            **kwargs,
        )