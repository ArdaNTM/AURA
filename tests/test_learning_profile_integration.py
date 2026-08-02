from aura.brain.brain import Brain
from aura.brain.learning_profile import LearningProfile


def test_brain_uses_learning_profile():

    profile = LearningProfile()

    for _ in range(5):
        profile.register_confidence(
            confidence=0.9,
            success=False,
        )

    brain = Brain(
        learning_profile=profile,
    )

    decision, _ = brain.think(
        "5+5 hesapla",
    )

    assert decision.metadata["learning"]

    assert decision.metadata["learning"]["profile"]["confidence_error"] > 0.35


def test_brain_changes_strategy_when_confidence_is_bad():

    profile = LearningProfile()

    for _ in range(5):
        profile.register_confidence(
            confidence=0.9,
            success=False,
        )

    brain = Brain(
        learning_profile=profile,
    )

    decision, _ = brain.think(
        "5+5 hesapla",
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"

    assert decision.confidence == 0.75
