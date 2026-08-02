from aura.brain.planner import Planner


def test_planner_uses_self_evaluation_skill_signal():

    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "self_evaluation": {
                "weakest_skill": "calculation",
            }
        },
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"

    assert decision.confidence == 0.75
