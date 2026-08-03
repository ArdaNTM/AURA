from aura.brain.planner import Planner


def test_planner_uses_weak_skill_strategy():

    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "skills": {
                "calculation": {
                    "confidence": 0.2,
                }
            }
        },
    )

    assert decision.strategy == "safe_tool_execution"

    assert decision.risk_level == "medium"


def test_planner_uses_strong_skill_strategy():

    planner = Planner()

    decision = planner.decide(
        "5+5 hesapla",
        learning={
            "skills": {
                "calculation": {
                    "confidence": 0.95,
                }
            }
        },
    )

    assert decision.strategy == "tool_execution"

    assert decision.risk_level == "low"

    assert decision.confidence == 0.95
