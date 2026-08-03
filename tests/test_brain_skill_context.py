from aura.brain.brain import Brain
from aura.brain.learning_profile import LearningProfile


def test_brain_adds_skill_context():

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

    learning = decision.metadata["learning"]

    assert "skills" in learning

    assert "calculation" in learning["skills"]

    assert learning["skills"]["calculation"]["confidence"] > 0
