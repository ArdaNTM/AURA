from __future__ import annotations

from aura.agent.experience import AgentExperience


class AgentMemoryLoop:
    """Store and recall agent experiences."""

    def __init__(
        self,
    ) -> None:

        self._experiences: list[AgentExperience] = []

    @property
    def experiences(
        self,
    ) -> list[AgentExperience]:
        return self._experiences

    def remember(
        self,
        experience: AgentExperience,
    ) -> None:

        self._experiences.append(
            experience,
        )

    def successful_strategies(
        self,
    ) -> dict[str, int]:

        result: dict[str, int] = {}

        for experience in self._experiences:

            if not experience.success:
                continue

            if not experience.strategy:
                continue

            result[experience.strategy] = (
                result.get(
                    experience.strategy,
                    0,
                )
                + 1
            )

        return result

    def preferred_strategy(
        self,
    ) -> str | None:

        scores = self.successful_strategies()

        if not scores:
            return None

        return max(
            scores,
            key=scores.get,
        )

    def context(
        self,
    ) -> dict[str, object]:
        """Return experience context for reasoning."""

        return {
            "experience_count": len(
                self._experiences,
            ),
            "preferred_strategy": self.preferred_strategy(),
            "successful_strategies": self.successful_strategies(),
        }
