from aura.brain.learning_profile import LearningProfile
from aura.brain.planner import Planner


def test_planner_adjusts_strategy_from_skill_score():

    profile = LearningProfile()

    profile.update_skill(
        "calculation",
        0.3,
    )

    planner = Planner(
        learning_profile=profile,
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"

    assert decision.confidence == 0.75
