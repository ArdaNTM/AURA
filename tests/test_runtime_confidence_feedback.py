from aura.brain.learning_profile import LearningProfile


def test_runtime_tracks_confidence_feedback():

    profile = LearningProfile()

    profile.register_confidence(
        confidence=0.8,
        success=True,
    )

    assert profile.confidence_predictions == 1

    assert profile.confidence_accuracy == 1.0
