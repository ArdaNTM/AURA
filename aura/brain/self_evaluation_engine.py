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

        diagnosis = []

        actions = []

        recommendations = []

        if performance.performance_score < 0.5:
            diagnosis.append(
                "Execution performance is below target.",
            )

            actions.append(
                "Improve execution reliability.",
            )

            recommendations.append(
                "Use safer execution strategy.",
            )

        if performance.retry_rate > 0.3:
            diagnosis.append(
                "Too many retries detected.",
            )

            actions.append(
                "Analyze failure causes before retry.",
            )

        if profile.confidence_error > 0.35:
            diagnosis.append(
                "Confidence calibration is inaccurate.",
            )

            actions.append(
                "Adjust confidence threshold.",
            )

            recommendations.append(
                "Verify uncertain decisions.",
            )

        if weakest_skill:

            diagnosis.append(
                f"Weak skill detected: {weakest_skill}",
            )

            actions.append(
                f"Improve skill: {weakest_skill}",
            )

        best_strategy = profile.best_strategy()

        if best_strategy:
            recommendations.append(
                f"Prefer successful strategy: {best_strategy}",
            )

        return SelfEvaluation(
            overall_score=performance.performance_score,
            strongest_skill=strongest_skill,
            weakest_skill=weakest_skill,
            best_strategy=best_strategy,
            diagnosis=diagnosis,
            improvement_actions=actions,
            recommendations=recommendations,
        )
