from aura.brain.learning_profile import LearningProfile


def test_learning_profile_updates_skill_score_gradually():

    profile = LearningProfile()

    profile.register_skill_result(
        "coding",
        1.0,
    )

    profile.register_skill_result(
        "coding",
        0.5,
    )

    assert profile.skill_scores["coding"] == 0.9
