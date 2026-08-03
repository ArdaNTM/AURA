from __future__ import annotations

from aura.brain.skill import Skill


class SkillRegistry:
    """Registry for AURA learned skills."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(
        self,
        skill: Skill,
    ) -> None:
        """Register a skill."""

        self._skills[skill.name] = skill

    def get(
        self,
        name: str,
    ) -> Skill | None:
        """Return skill by name."""

        return self._skills.get(
            name,
        )

    def all(
        self,
    ) -> list[Skill]:
        """Return all skills."""

        return list(
            self._skills.values(),
        )

    def update(
        self,
        name: str,
        success: bool,
        score: float,
    ) -> None:
        """Update skill learning result."""

        skill = self.get(
            name,
        )

        if skill is None:
            skill = Skill(
                name=name,
                domain="unknown",
            )

            self.register(
                skill,
            )

        skill.register_result(
            success,
            score,
        )

    def update_from_reflection(
        self,
        name: str,
        success: bool,
        quality_score: float,
        retry_needed: bool,
    ) -> None:
        """Update skill using reflection feedback."""

        skill = self.get(
            name,
        )

        if skill is None:
            skill = Skill(
                name=name,
                domain="unknown",
            )

            self.register(
                skill,
            )

        skill.register_reflection(
            success,
            quality_score,
            retry_needed,
        )

    def update_reflection(
        self,
        name: str,
        reflection,
        score: float,
    ) -> None:
        """Update skill from reflection feedback."""

        skill = self.get(
            name,
        )

        if skill is None:
            skill = Skill(
                name=name,
                domain="unknown",
            )

            self.register(
                skill,
            )

        skill.register_reflection(
            success=reflection.success,
            quality_score=reflection.quality_score,
            retry_needed=reflection.retry_needed,
        )

    def to_dict(
        self,
    ) -> dict[str, dict[str, object]]:
        """Serialize skills."""

        return {
            name: {
                "name": skill.name,
                "domain": skill.domain,
                "confidence": skill.confidence,
                "success_rate": skill.success_rate,
                "usage_count": skill.usage_count,
                "required_tools": skill.required_tools,
                "improvement_history": skill.improvement_history,
            }
            for name, skill in self._skills.items()
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, dict[str, object]],
    ) -> SkillRegistry:
        """Restore skills."""

        registry = cls()

        for name, skill_data in data.items():

            skill = Skill(
                name=str(
                    skill_data.get(
                        "name",
                        name,
                    )
                ),
                domain=str(
                    skill_data.get(
                        "domain",
                        "unknown",
                    )
                ),
                confidence=float(
                    skill_data.get(
                        "confidence",
                        0.0,
                    )
                ),
                success_rate=float(
                    skill_data.get(
                        "success_rate",
                        0.0,
                    )
                ),
                usage_count=int(
                    skill_data.get(
                        "usage_count",
                        0,
                    )
                ),
                required_tools=list(
                    skill_data.get(
                        "required_tools",
                        [],
                    )
                ),
                improvement_history=list(
                    skill_data.get(
                        "improvement_history",
                        [],
                    )
                ),
            )

            registry.register(
                skill,
            )

        return registry

    def strongest(
        self,
    ) -> Skill | None:
        """Return highest confidence skill."""

        if not self._skills:
            return None

        return max(
            self._skills.values(),
            key=lambda skill: skill.confidence,
        )

    def confidence(
        self,
        name: str,
    ) -> float:
        """Return learned confidence."""

        skill = self.get(
            name,
        )

        if skill is None:
            return 0.0

        return skill.confidence

    def preferred_tool(
        self,
        name: str,
    ) -> str | None:
        """Return preferred tool."""

        skill = self.get(
            name,
        )

        if skill is None:
            return None

        if not skill.required_tools:
            return None

        return skill.required_tools[0]
