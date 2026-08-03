"""Evaluate AURA autonomous improvement quality."""

from __future__ import annotations

from dataclasses import dataclass

from aura.brain.improvement_memory import ImprovementMemory
from aura.brain.performance import PerformanceReport
from aura.brain.self_evaluation import SelfEvaluation


@dataclass
class ImprovementEvaluation:
    """Result of improvement evaluation."""

    evolution_score: float

    improvement_success_rate: float

    recommended_strategy: str | None

    approved: bool

    reasons: list[str]


class ImprovementEvaluator:
    """Evaluate whether AURA improvements are useful."""

    def evaluate(
        self,
        memory: ImprovementMemory,
        performance: PerformanceReport,
        self_evaluation: SelfEvaluation,
    ) -> ImprovementEvaluation:
        """Calculate evolution quality."""

        improvement_rate = 0.0

        if memory.records:
            improvement_rate = sum(
                1 for record in memory.records if record.success
            ) / len(memory.records)

        evolution_score = (
            performance.performance_score * 0.5
            + improvement_rate * 0.3
            + self_evaluation.overall_score * 0.2
        )

        reasons = []

        if improvement_rate >= 0.5:
            reasons.append(
                "Improvement experiments are producing positive results.",
            )
        else:
            reasons.append(
                "Improvement experiments require more validation.",
            )

        if performance.performance_score >= 0.8:
            reasons.append(
                "Execution performance is stable.",
            )

        else:
            reasons.append(
                "Execution reliability should improve.",
            )

        approved = evolution_score >= 0.5

        recommended_strategy = memory.best_strategy()

        return ImprovementEvaluation(
            evolution_score=round(
                evolution_score,
                2,
            ),
            improvement_success_rate=round(
                improvement_rate,
                2,
            ),
            recommended_strategy=recommended_strategy,
            approved=approved,
            reasons=reasons,
        )
