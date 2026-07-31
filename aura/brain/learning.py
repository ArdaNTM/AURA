"""Learning context for AURA brain."""

from __future__ import annotations


class LearningContext:
    """Provide previous experience to the brain."""

    def __init__(
        self,
        memories: list[tuple[str, str]] | None = None,
    ) -> None:
        self._memories = memories or []

    @property
    def memories(self) -> list[tuple[str, str]]:
        """Return stored learning memories."""

        return self._memories

    def summarize(self) -> dict[str, object]:
        """Create learning summary."""

        return {
            "memory_count": len(
                self._memories,
            ),
            "previous_experience": self._memories,
            "has_failures": self.has_previous_failure(),
            "strategy_scores": self.strategy_scores(),
            "preferred_strategy": self.preferred_strategy(),
            "strategy_confidence": self.strategy_confidence(),
            "success_rate": self.success_rate(),
            "learning_quality": self.learning_quality(),
        }

    def has_previous_failure(
        self,
    ) -> bool:
        """Check whether previous experience contains failures."""

        failure_keywords = [
            "fail",
            "error",
            "failed",
            "hata",
            "baÅŸarÄ±sÄ±z",
            "baÅŸarisiz",
        ]

        return any(
            any(keyword in content.casefold() for keyword in failure_keywords)
            for _, content in self._memories
        )

    def strategy_scores(
        self,
    ) -> dict[str, int]:
        """Count successful strategy usage."""

        scores: dict[str, int] = {}

        for _, content in self._memories:
            if "success=True" not in content:
                continue

            if "strategy=" not in content:
                continue

            strategy = self._extract_strategy(
                content,
            )

            if strategy:
                scores[strategy] = (
                    scores.get(
                        strategy,
                        0,
                    )
                    + 1
                )

        return scores

    def preferred_strategy(
        self,
    ) -> str | None:
        """Return most successful strategy."""

        scores = self.strategy_scores()

        if not scores:
            return None

        return max(
            scores,
            key=scores.get,
        )

    def strategy_confidence(
        self,
    ) -> float:
        """Calculate confidence of preferred strategy."""

        scores = self.strategy_scores()

        if not scores:
            return 0.0

        total = sum(
            scores.values(),
        )

        best = max(
            scores.values(),
        )

        return best / total

    def success_rate(
        self,
    ) -> float:
        """Calculate successful experience ratio."""

        if not self._memories:
            return 0.0

        successful = sum(
            1 for _, content in self._memories if "success=True" in content
        )

        return successful / len(
            self._memories,
        )

    def learning_quality(
        self,
    ) -> float:
        """Calculate overall learning quality."""

        success = self.success_rate()

        strategy = self.strategy_confidence()

        return success * 0.6 + strategy * 0.4

    def _extract_strategy(
        self,
        content: str,
    ) -> str | None:
        """Extract strategy value from memory content."""

        for part in content.split(";"):
            part = part.strip()

            if part.startswith(
                "strategy=",
            ):
                return part.replace(
                    "strategy=",
                    "",
                )

        return None
