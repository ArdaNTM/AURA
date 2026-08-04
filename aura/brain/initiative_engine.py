from __future__ import annotations

from aura.brain.initiative import Initiative
from aura.brain.self_evaluation import SelfEvaluation


class InitiativeEngine:
    """Create autonomous tasks from self evaluation."""

    def create(
        self,
        evaluation: SelfEvaluation,
    ) -> Initiative | None:
        """Generate initiative from evaluation."""

        if evaluation.weakest_skill:

            return Initiative(
                reason=(f"Weak skill detected: " f"{evaluation.weakest_skill}"),
                task=(f"Improve skill: " f"{evaluation.weakest_skill}"),
                priority="medium",
                strategy=evaluation.best_strategy,
            )

        if evaluation.overall_score < 0.5:

            return Initiative(
                reason="Low performance detected.",
                task="Improve execution reliability.",
                priority="high",
                strategy="safe_tool_execution",
            )

        if evaluation.recommendations:

            return Initiative(
                reason=evaluation.recommendations[0],
                task=evaluation.recommendations[0],
                priority="normal",
                strategy=evaluation.best_strategy,
            )

        return None
