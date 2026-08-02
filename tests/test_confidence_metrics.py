from aura.brain.learning_profile import LearningProfile


def test_learning_profile_tracks_confidence_accuracy():

    profile = LearningProfile()

    profile.register_confidence(
        confidence=0.9,
        success=True,
    )

    profile.register_confidence(
        confidence=0.2,
        success=False,
    )

    assert profile.confidence_accuracy == 1.0

    assert profile.confidence_error < 0.2
