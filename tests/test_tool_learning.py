from aura.brain.learning_profile import LearningProfile
from aura.brain.learning_profile_store import LearningProfileStore


def test_learning_profile_stores_tool_reliability(
    tmp_path,
):
    profile = LearningProfile()

    profile.register_tool_reliability(
        "calculator",
        1.0,
        0.2,
        10,
    )

    store = LearningProfileStore(
        tmp_path / "profile.json",
    )

    store.save(
        profile,
    )

    loaded = store.load()

    assert loaded.tool_scores["calculator"]["success_rate"] == 1.0

    assert loaded.tool_scores["calculator"]["runs"] == 10
