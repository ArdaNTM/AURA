"""Detect performance regressions after improvements."""

from __future__ import annotations


class RegressionDetector:
    """Identify harmful autonomous changes."""

    def __init__(
        self,
        threshold: float = 0.15,
    ):
        self._threshold = threshold

    def detect(
        self,
        before_score: float,
        after_score: float,
    ) -> bool:
        """
        Return True when regression exists.
        """

        if before_score <= 0:
            return False

        drop = before_score - after_score

        return drop >= self._threshold
