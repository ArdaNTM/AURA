from aura.brain.skill import Skill
from aura.brain.skill_registry import SkillRegistry


def test_registry_registers_skill():

    registry = SkillRegistry()

    skill = Skill(
        name="calculation",
        domain="math",
    )

    registry.register(
        skill,
    )

    assert (
        registry.get(
            "calculation",
        )
        == skill
    )


def test_registry_updates_skill():

    registry = SkillRegistry()

    registry.update(
        "coding",
        success=True,
        score=0.8,
    )

    skill = registry.get(
        "coding",
    )

    assert skill is not None

    assert skill.usage_count == 1

    assert skill.success_rate == 1.0


def test_registry_finds_strongest_skill():

    registry = SkillRegistry()

    registry.update(
        "math",
        True,
        0.9,
    )

    registry.update(
        "coding",
        True,
        0.5,
    )

    strongest = registry.strongest()

    assert strongest is not None

    assert strongest.name == "math"
