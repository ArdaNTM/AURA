"""Autonomous improvement history tracking."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ImprovementRecord:
    strategy: str
    before_score: float
    after_score: float
    success: bool
    timestamp: datetime


class ImprovementHistory:
    """Track autonomous improvement changes."""

    def __init__(self):
        self._records: list[ImprovementRecord] = []

    @property
    def records(self):
        return self._records

    def add(
        self,
        strategy: str,
        before_score: float,
        after_score: float,
        success: bool,
    ):
        self._records.append(
            ImprovementRecord(
                strategy=strategy,
                before_score=before_score,
                after_score=after_score,
                success=success,
                timestamp=datetime.now(),
            )
        )

    def latest(self):
        if not self._records:
            return None

        return self._records[-1]
