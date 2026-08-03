from aura.brain.skill_registry import SkillRegistry


def test_skill_registry_updates_from_reflection():

    registry = SkillRegistry()

    registry.update_from_reflection(
        "calculation",
        True,
        1.0,
        False,
    )

    skill = registry.get(
        "calculation",
    )

    assert skill is not None
    assert skill.usage_count == 1
    assert skill.success_rate == 1.0
    assert skill.confidence > 0
