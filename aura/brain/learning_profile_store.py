"""Persistent storage for learning profiles."""

from __future__ import annotations

import json
from pathlib import Path

from aura.brain.learning_profile import LearningProfile


class LearningProfileStore:
    """Load and save learning profiles."""

    def __init__(
        self,
        path: str | Path = "learning_profile.json",
    ) -> None:
        self._path = Path(
            path,
        )

    def save(
        self,
        profile: LearningProfile,
    ) -> None:
        """Persist profile."""

        data = {
            "total_tasks": profile.total_tasks,
            "successful_tasks": profile.successful_tasks,
            "failed_tasks": profile.failed_tasks,
            "strategy_usage": profile.strategy_usage,
            "strategy_success": profile.strategy_success,
            "skill_scores": profile.skill_scores,
            "tool_scores": profile.tool_scores,
            "self_evaluation": profile.self_evaluation,
            "confidence_predictions": profile.confidence_predictions,
            "confidence_correct": profile.confidence_correct,
            "confidence_error_total": profile.confidence_error_total,
        }

        self._path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(
        self,
    ) -> LearningProfile:
        """Load profile from disk."""

        if not self._path.exists():
            return LearningProfile()

        data = json.loads(
            self._path.read_text(
                encoding="utf-8",
            ),
        )

        return LearningProfile(
            total_tasks=data.get(
                "total_tasks",
                0,
            ),
            successful_tasks=data.get(
                "successful_tasks",
                0,
            ),
            failed_tasks=data.get(
                "failed_tasks",
                0,
            ),
            strategy_usage=data.get(
                "strategy_usage",
                {},
            ),
            strategy_success=data.get(
                "strategy_success",
                {},
            ),
            skill_scores=data.get(
                "skill_scores",
                {},
            ),
            tool_scores=data.get(
                "tool_scores",
                {},
            ),
            self_evaluation=data.get(
                "self_evaluation",
                {},
            ),
            confidence_predictions=data.get(
                "confidence_predictions",
                0,
            ),
            confidence_correct=data.get(
                "confidence_correct",
                0,
            ),
            confidence_error_total=data.get(
                "confidence_error_total",
                0.0,
            ),
        )
