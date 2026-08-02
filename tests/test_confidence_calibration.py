from aura.brain.learning_profile import LearningProfile


def test_learning_profile_calibrates_confidence_threshold():

    profile = LearningProfile()

    for _ in range(5):
        profile.register_confidence(
            confidence=0.9,
            success=False,
        )

    assert profile.calibrated_confidence_threshold() == 0.85
