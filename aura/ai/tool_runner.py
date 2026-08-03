"""Tool execution coordinator."""

from __future__ import annotations

import time
from typing import Any

from aura.brain.tool_reliability import ToolReliabilityTracker
from aura.core.tool_result import ToolResult
from aura.core.tools import ToolRegistry


class ToolRunner:
    """Execute tools through the registry."""

    def __init__(
        self,
        registry: ToolRegistry,
        reliability_tracker: ToolReliabilityTracker | None = None,
    ) -> None:
        self._registry = registry

        self._reliability_tracker = reliability_tracker or ToolReliabilityTracker()

    @property
    def registry(self) -> ToolRegistry:
        """Return the underlying registry."""

        return self._registry

    @property
    def reliability_tracker(
        self,
    ) -> ToolReliabilityTracker:
        """Return reliability tracker."""

        return self._reliability_tracker

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
            result = ToolResult(
                name=name,
                output="",
                success=False,
                error=f"Unknown tool '{name}'.",
            )

            self._reliability_tracker.record(
                result,
            )

            return result

        start = time.perf_counter()

        result = self._registry.execute(
            name,
            *args,
            **kwargs,
        )

        duration = time.perf_counter() - start

        result = ToolResult(
            name=result.name,
            output=result.output,
            success=result.success,
            error=result.error,
            duration=duration,
            timestamp=result.timestamp,
            metadata=result.metadata,
        )

        self._reliability_tracker.record(
            result,
        )

        return result
