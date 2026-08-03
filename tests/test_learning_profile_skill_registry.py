from aura.brain.learning_profile import LearningProfile


def test_learning_profile_updates_skill_registry():

    profile = LearningProfile()

    profile.register_skill_result(
        "coding",
        0.8,
        True,
    )

    skill = profile.skill_registry.get(
        "coding",
    )

    assert skill is not None

    assert skill.usage_count == 1

    assert skill.success_rate == 1.0

    assert skill.confidence == 0.16
