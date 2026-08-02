from aura.brain.learning_profile import LearningProfile


def test_skill_learning_updates_profile():

    profile = LearningProfile()

    profile.register_skill_result(
        "calculation",
        1.0,
    )

    profile.register_skill_result(
        "calculation",
        0.5,
    )

    assert profile.skill_scores["calculation"] == 0.9
