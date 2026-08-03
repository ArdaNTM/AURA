from aura.brain.learning_profile import LearningProfile
from aura.brain.learning_profile_store import LearningProfileStore


def test_learning_profile_store_persists_skills(
    tmp_path,
):

    store = LearningProfileStore(
        tmp_path / "skills.json",
    )

    profile = LearningProfile()

    profile.register_skill_result(
        "coding",
        0.9,
        True,
    )

    profile.skill_registry.get(
        "coding",
    ).add_tool(
        "terminal",
    )

    store.save(
        profile,
    )

    loaded = store.load()

    skill = loaded.skill_registry.get(
        "coding",
    )

    assert skill is not None

    assert skill.usage_count == 1

    assert skill.success_rate == 1.0

    assert skill.required_tools == [
        "terminal",
    ]
