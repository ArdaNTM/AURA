from aura.brain.learning_profile import LearningProfile
from aura.brain.planner import Planner


def test_planner_uses_adaptive_threshold():

    profile = LearningProfile()

    for _ in range(5):
        profile.register_confidence(
            confidence=0.9,
            success=False,
        )

    planner = Planner(
        learning_profile=profile,
    )

    assert planner._get_confidence_threshold() == 0.85
