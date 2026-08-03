from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Skill:
    """Represents an AURA learned capability."""

    name: str

    domain: str

    confidence: float = 0.0

    success_rate: float = 0.0

    usage_count: int = 0

    required_tools: list[str] = field(
        default_factory=list,
    )

    improvement_history: list[float] = field(
        default_factory=list,
    )

    def register_result(
        self,
        success: bool,
        score: float,
    ) -> None:
        """Update skill from execution result."""

        self.usage_count += 1

        self.improvement_history.append(
            score,
        )

        successful = self.success_rate * (self.usage_count - 1)

        if success:
            successful += 1

        self.success_rate = successful / self.usage_count

        self.confidence = round(
            (self.confidence * 0.8 + score * 0.2),
            2,
        )

    def add_tool(
        self,
        tool: str,
    ) -> None:
        """Register required tool."""

        if tool not in self.required_tools:
            self.required_tools.append(
                tool,
            )

    def register_reflection(
        self,
        success: bool,
        quality_score: float,
        retry_needed: bool,
    ) -> None:
        """Update skill using reflection feedback."""

        adjusted_score = quality_score

        if retry_needed:
            adjusted_score *= 0.8

        self.register_result(
            success,
            adjusted_score,
        )
