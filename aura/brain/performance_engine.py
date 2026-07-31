"""Agent performance calculation engine."""

from __future__ import annotations

from aura.brain.performance import PerformanceReport


class PerformanceEngine:
    """Calculate overall agent performance."""

    def evaluate(
        self,
        observations: list[object],
    ) -> PerformanceReport:
        """Generate performance report."""

        if not observations:
            return PerformanceReport(
                success_rate=0.0,
                average_score=0.0,
                retry_rate=0.0,
                performance_score=0.0,
            )

        total = len(
            observations,
        )

        successful = sum(1 for observation in observations if observation.success)

        retries = sum(1 for observation in observations if observation.retry_needed)

        total_score = sum(observation.score for observation in observations)

        success_rate = successful / total

        average_score = total_score / total

        retry_rate = retries / total

        performance_score = (
            success_rate * 0.5 + average_score * 0.4 + (1 - retry_rate) * 0.1
        )

        return PerformanceReport(
            success_rate=success_rate,
            average_score=average_score,
            retry_rate=retry_rate,
            performance_score=performance_score,
        )
