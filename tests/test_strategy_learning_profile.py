from aura.brain.learning_profile import LearningProfile
from aura.brain.planner import Planner


def test_planner_uses_best_strategy_from_profile():

    profile = LearningProfile()

    for _ in range(5):
        profile.register_task(
            success=True,
            strategy="safe_tool_execution",
        )

    for _ in range(5):
        profile.register_task(
            success=False,
            strategy="tool_execution",
        )

    planner = Planner(
        learning_profile=profile,
    )

    decision = planner.decide(
        "5+5 hesapla",
    )

    assert decision.strategy == "safe_tool_execution"
