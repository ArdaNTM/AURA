"""Agent performance evaluation models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PerformanceReport:
    """Overall agent performance evaluation."""

    success_rate: float

    average_score: float

    retry_rate: float

    performance_score: float
