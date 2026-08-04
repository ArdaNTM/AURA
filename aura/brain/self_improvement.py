from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ImprovementSuggestion:
    area: str

    problem: str

    suggestion: str

    confidence_change: float

    priority: float = 0.5


@dataclass
class ImprovementReport:

    success: bool

    suggestions: list[ImprovementSuggestion] = field(default_factory=list)

    strategy_change: str | None = None


class SelfImprovementEngine:
    """
    Autonomous strategy improvement system.
    """

    def analyze(
        self,
        success: bool,
        strategy: str | None,
        confidence: float,
        reflection: str | None = None,
    ) -> ImprovementReport:

        suggestions = []

        if not success:

            suggestions.append(
                ImprovementSuggestion(
                    area="strategy",
                    problem=(reflection or "Task failed"),
                    suggestion=("Try alternative execution strategy"),
                    confidence_change=-0.05,
                    priority=0.8,
                )
            )

            return ImprovementReport(
                success=False,
                suggestions=suggestions,
                strategy_change="adaptive_retry",
            )

        if confidence < 0.5:

            suggestions.append(
                ImprovementSuggestion(
                    area="confidence",
                    problem="Low confidence despite success",
                    suggestion="Increase confidence calibration",
                    confidence_change=0.03,
                    priority=0.5,
                )
            )

        if strategy:

            suggestions.append(
                ImprovementSuggestion(
                    area="strategy",
                    problem="Successful strategy found",
                    suggestion=(f"Prefer {strategy} in similar tasks"),
                    confidence_change=0.02,
                    priority=0.7,
                )
            )

        return ImprovementReport(
            success=True,
            suggestions=suggestions,
            strategy_change=strategy,
        )
