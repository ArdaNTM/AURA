from aura.brain.learning_profile import LearningProfile
from aura.brain.learning_profile_store import LearningProfileStore


def test_learning_profile_store_saves_profile(
    tmp_path,
):
    path = tmp_path / "profile.json"

    store = LearningProfileStore(
        path,
    )

    profile = LearningProfile(
        total_tasks=10,
        successful_tasks=8,
        failed_tasks=2,
    )

    profile.strategy_usage["tool_execution"] = 10
    profile.strategy_success["tool_execution"] = 8
    profile.skill_scores["coding"] = 0.9

    store.save(
        profile,
    )

    assert path.exists()


def test_learning_profile_store_loads_profile(
    tmp_path,
):
    path = tmp_path / "profile.json"

    store = LearningProfileStore(
        path,
    )

    profile = LearningProfile(
        total_tasks=12,
        successful_tasks=9,
        failed_tasks=3,
    )

    profile.strategy_usage["safe_tool_execution"] = 5
    profile.strategy_success["safe_tool_execution"] = 5
    profile.skill_scores["research"] = 0.8

    store.save(
        profile,
    )

    loaded = store.load()

    assert loaded.total_tasks == 12

    assert loaded.successful_tasks == 9

    assert loaded.failed_tasks == 3

    assert loaded.strategy_usage["safe_tool_execution"] == 5

    assert loaded.strategy_success["safe_tool_execution"] == 5

    assert loaded.skill_scores["research"] == 0.8


def test_learning_profile_store_returns_empty_profile(
    tmp_path,
):
    store = LearningProfileStore(
        tmp_path / "missing.json",
    )

    profile = store.load()

    assert profile.total_tasks == 0

    assert profile.successful_tasks == 0

    assert profile.failed_tasks == 0


def test_learning_profile_persists_self_evaluation(tmp_path):
    store = LearningProfileStore(
        tmp_path / "learning.json",
    )

    profile = LearningProfile()

    profile.self_evaluation = {
        "overall_score": 0.9,
        "strongest_skill": "calculation",
        "weakest_skill": "coding",
        "best_strategy": "tool_execution",
        "recommendations": [
            "Improve coding skill",
        ],
    }

    store.save(
        profile,
    )

    loaded = store.load()

    assert loaded.self_evaluation["overall_score"] == 0.9

    assert loaded.self_evaluation["strongest_skill"] == "calculation"

    assert loaded.self_evaluation["weakest_skill"] == "coding"
