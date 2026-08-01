"""Long term learning profile for AURA."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LearningProfile:
    """Persistent learning state of AURA."""

    total_tasks: int = 0

    successful_tasks: int = 0

    failed_tasks: int = 0

    strategy_usage: dict[str, int] = field(
        default_factory=dict,
    )

    strategy_success: dict[str, int] = field(
        default_factory=dict,
    )

    skill_scores: dict[str, float] = field(
        default_factory=dict,
    )

    @property
    def success_rate(
        self,
    ) -> float:
        """Calculate overall task success rate."""

        if self.total_tasks == 0:
            return 0.0

        return self.successful_tasks / self.total_tasks

    def register_task(
        self,
        success: bool,
        strategy: str | None = None,
    ) -> None:
        """Record completed task experience."""

        self.total_tasks += 1

        if success:
            self.successful_tasks += 1
        else:
            self.failed_tasks += 1

        if strategy:
            self.strategy_usage[strategy] = (
                self.strategy_usage.get(
                    strategy,
                    0,
                )
                + 1
            )

            if success:
                self.strategy_success[strategy] = (
                    self.strategy_success.get(
                        strategy,
                        0,
                    )
                    + 1
                )

    def strategy_success_rate(
        self,
        strategy: str,
    ) -> float:
        """Return success rate of a strategy."""

        usage = self.strategy_usage.get(
            strategy,
            0,
        )

        if usage == 0:
            return 0.0

        success = self.strategy_success.get(
            strategy,
            0,
        )

        return success / usage

    def update_skill(
        self,
        skill: str,
        score: float,
    ) -> None:
        """Update learned skill score."""

        self.skill_scores[skill] = score
