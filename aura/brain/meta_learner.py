"""Meta learning engine for AURA."""

from __future__ import annotations

from aura.brain.improvement import ImprovementPlan
from aura.brain.learning import LearningContext


class MetaLearner:
    """Analyze learning state and suggest improvements."""

    def analyze(
        self,
        context: LearningContext,
    ) -> ImprovementPlan:
        """Generate improvement recommendations."""

        quality = context.learning_quality()

        if quality < 0.5:
            return ImprovementPlan(
                suggestions=[
                    "Increase execution reliability.",
                    "Prefer safer strategies.",
                ],
                target_strategy="safe_tool_execution",
                confidence_change=-0.1,
                risk_adjustment="medium",
            )

        if quality < 0.8:
            return ImprovementPlan(
                suggestions=[
                    "Continue collecting successful experiences.",
                ],
                target_strategy=context.preferred_strategy(),
                confidence_change=0.0,
                risk_adjustment="normal",
            )

        return ImprovementPlan(
            suggestions=[
                "Maintain current strategy.",
                "Optimize successful patterns.",
            ],
            target_strategy=context.preferred_strategy(),
            confidence_change=0.1,
            risk_adjustment="low",
        )
