"""Long term learning profile for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LearningProfile:
    """Persistent learning state of AURA."""

    total_tasks: int = 0

    successful_tasks: int = 0

    failed_tasks: int = 0

    confidence_predictions: int = 0

    confidence_correct: int = 0

    confidence_error_total: float = 0.0

    quality_predictions: int = 0

    quality_total: float = 0.0

    strategy_usage: dict[str, int] = field(
        default_factory=dict,
    )

    strategy_success: dict[str, int] = field(
        default_factory=dict,
    )

    skill_scores: dict[str, float] = field(
        default_factory=dict,
    )
    self_evaluation: dict[str, object] = field(
        default_factory=dict,
    )
    tool_scores: dict[str, dict[str, float]] = field(
        default_factory=dict,
    )

    @property
    def success_rate(
        self,
    ) -> float:
        """Calculate overall task success rate."""

        if self.total_tasks == 0:
            return 0.0

        return self.successful_tasks / self.total_tasks

    def register_task(
        self,
        success: bool,
        strategy: str | None = None,
    ) -> None:
        """Record completed task experience."""

        self.total_tasks += 1

        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1

        if strategy:
            self.strategy_usage[strategy] = (
                self.strategy_usage.get(
                    strategy,
                    0,
                )
                + 1
            )

            if success:
                self.strategy_success[strategy] = (
                    self.strategy_success.get(
                        strategy,
                        0,
                    )
                    + 1
                )

    def register_confidence(
        self,
        confidence: float,
        success: bool,
    ) -> None:
        """Track confidence accuracy."""

        self.confidence_predictions += 1

        expected = 1.0 if success else 0.0

        error = abs(
            confidence - expected,
        )

        self.confidence_error_total += error

        if (confidence >= 0.5 and success) or (confidence < 0.5 and not success):
            self.confidence_correct += 1

    @property
    def confidence_accuracy(
        self,
    ) -> float:
        """Return confidence prediction accuracy."""

        if self.confidence_predictions == 0:
            return 0.0

        return self.confidence_correct / self.confidence_predictions

    @property
    def confidence_error(
        self,
    ) -> float:
        """Return average confidence error."""

        if self.confidence_predictions == 0:
            return 0.0

        return self.confidence_error_total / self.confidence_predictions

    def calibrated_confidence_threshold(
        self,
        default: float = 0.75,
    ) -> float:
        """Calculate adaptive confidence threshold."""

        if self.confidence_predictions < 5:
            return default

        if self.confidence_error > 0.35:
            return min(
                0.9,
                default + 0.1,
            )

        if self.confidence_error < 0.15:
            return max(
                0.5,
                default - 0.1,
            )

        return default

    def strategy_success_rate(
        self,
        strategy: str,
    ) -> float:
        """Return success rate of a strategy."""

        usage = self.strategy_usage.get(
            strategy,
            0,
        )

        if usage == 0:
            return 0.0

        success = self.strategy_success.get(
            strategy,
            0,
        )

        return success / usage

    def update_skill(
        self,
        skill: str,
        score: float,
    ) -> None:
        """Update learned skill score."""

        self.skill_scores[skill] = score

    @property
    def average_quality(
        self,
    ) -> float:
        """Return average execution quality."""

        if self.quality_predictions == 0:
            return 0.0

        return self.quality_total / self.quality_predictions

    def register_quality(
        self,
        score: float,
    ) -> None:
        """Track execution quality."""

        self.quality_predictions += 1

        self.quality_total += score

    def best_strategy(
        self,
    ) -> str | None:
        """Return the most successful strategy."""

        if not self.strategy_usage:
            return None

        strategies = list(
            self.strategy_usage.keys(),
        )

        return max(
            strategies,
            key=self.strategy_success_rate,
        )

    def register_skill_result(
        self,
        skill: str,
        score: float,
    ) -> None:
        """Update skill score using gradual learning."""

        if skill not in self.skill_scores:
            self.skill_scores[skill] = score
            return

        current = self.skill_scores[skill]

        self.skill_scores[skill] = round(
            (current * 0.8 + score * 0.2),
            2,
        )

    def register_tool_reliability(
        self,
        name: str,
        success_rate: float,
        average_duration: float,
        runs: int,
    ) -> None:
        """Store learned tool reliability."""

        self.tool_scores[name] = {
            "success_rate": success_rate,
            "average_duration": average_duration,
            "runs": float(runs),
        }
