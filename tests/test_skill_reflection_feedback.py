from aura.brain.skill import Skill


def test_skill_uses_reflection_feedback():

    skill = Skill(
        name="calculation",
        domain="math",
    )

    skill.register_reflection(
        success=True,
        quality_score=1.0,
        retry_needed=False,
    )

    assert skill.usage_count == 1
    assert skill.success_rate == 1.0
    assert skill.confidence > 0
