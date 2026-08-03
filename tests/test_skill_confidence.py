from aura.brain.skill import Skill
from aura.brain.skill_registry import SkillRegistry


def test_skill_registry_returns_confidence():

    registry = SkillRegistry()

    skill = Skill(
        name="calculation",
        domain="math",
        confidence=0.85,
    )

    registry.register(
        skill,
    )

    assert (
        registry.confidence(
            "calculation",
        )
        == 0.85
    )


def test_unknown_skill_confidence_is_zero():

    registry = SkillRegistry()

    assert (
        registry.confidence(
            "unknown",
        )
        == 0.0
    )
