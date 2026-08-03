from aura.brain.brain import Brain
from aura.brain.learning_profile import LearningProfile


def test_brain_adds_skill_metadata():

    profile = LearningProfile()

    profile.register_skill_result(
        "calculation",
        0.95,
        True,
    )

    brain = Brain(
        learning_profile=profile,
    )

    decision, _ = brain.think(
        "5+5 hesapla",
    )

    skill_context = decision.metadata["skill_context"]

    assert skill_context["name"] == "calculation"

    assert skill_context["confidence"] > 0

    assert skill_context["success_rate"] > 0
