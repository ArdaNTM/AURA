"""Safe autonomous improvement monitoring."""

from __future__ import annotations

from aura.brain.improvement_history import ImprovementHistory
from aura.brain.regression_detector import RegressionDetector


class ImprovementMonitor:
    """Monitor improvement impact."""

    def __init__(
        self,
        history: ImprovementHistory | None = None,
        detector: RegressionDetector | None = None,
    ):
        self.history = history or ImprovementHistory()
        self.detector = detector or RegressionDetector()

    def record(
        self,
        strategy: str,
        before_score: float,
        after_score: float,
    ) -> bool:

        regression = self.detector.detect(
            before_score,
            after_score,
        )

        self.history.add(
            strategy=strategy,
            before_score=before_score,
            after_score=after_score,
            success=not regression,
        )

        return not regression
