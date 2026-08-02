"""Self evaluation engine for AURA."""

from __future__ import annotations

from aura.brain.learning_profile import LearningProfile
from aura.brain.performance import PerformanceReport
from aura.brain.self_evaluation import SelfEvaluation


class SelfEvaluationEngine:
    """Analyze AURA performance and learning."""

    def evaluate(
        self,
        profile: LearningProfile,
        performance: PerformanceReport,
    ) -> SelfEvaluation:
        """Create self evaluation report."""

        strongest_skill = None
        weakest_skill = None

        if profile.skill_scores:

            strongest_skill = max(
                profile.skill_scores,
                key=profile.skill_scores.get,
            )

            weakest_skill = min(
                profile.skill_scores,
                key=profile.skill_scores.get,
            )

        best_strategy = profile.best_strategy()

        recommendations = []

        if performance.performance_score < 0.5:
            recommendations.append(
                "Improve execution reliability.",
            )

        if profile.confidence_error > 0.35:
            recommendations.append(
                "Reduce confidence calibration error.",
            )

        if weakest_skill:
            recommendations.append(
                f"Improve skill: {weakest_skill}",
            )

        return SelfEvaluation(
            overall_score=performance.performance_score,
            strongest_skill=strongest_skill,
            weakest_skill=weakest_skill,
            best_strategy=best_strategy,
            recommendations=recommendations,
        )
