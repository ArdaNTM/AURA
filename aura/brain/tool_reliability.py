"""Tool reliability tracking."""

from __future__ import annotations

from dataclasses import dataclass

from aura.core.tool_result import ToolResult


@dataclass
class ToolReliability:
    """Statistics for a single tool."""

    runs: int = 0

    successes: int = 0

    failures: int = 0

    total_duration: float = 0.0

    @property
    def success_rate(
        self,
    ) -> float:
        """Return success ratio."""

        if self.runs == 0:
            return 0.0

        return self.successes / self.runs

    @property
    def average_duration(
        self,
    ) -> float:
        """Return average execution duration."""

        if self.runs == 0:
            return 0.0

        return self.total_duration / self.runs


class ToolReliabilityTracker:
    """Track tool execution reliability."""

    def __init__(
        self,
    ) -> None:
        self._stats: dict[str, ToolReliability] = {}

    def record(
        self,
        result: ToolResult,
    ) -> None:
        """Record tool execution."""

        stats = self._stats.setdefault(
            result.name,
            ToolReliability(),
        )

        stats.runs += 1

        stats.total_duration += result.duration

        if result.success:
            stats.successes += 1
        else:
            stats.failures += 1

    def get(
        self,
        name: str,
    ) -> ToolReliability:
        """Return tool statistics."""

        return self._stats.setdefault(
            name,
            ToolReliability(),
        )

    def all(
        self,
    ) -> dict[str, ToolReliability]:
        """Return all statistics."""

        return self._stats

    def snapshot(
        self,
    ) -> dict[str, dict[str, float]]:
        """Return serializable reliability data."""

        return {
            name: {
                "success_rate": stats.success_rate,
                "average_duration": stats.average_duration,
                "runs": float(stats.runs),
            }
            for name, stats in self._stats.items()
        }
