from aura.brain.planner import Planner


def test_planner_detects_calculation():
    planner = Planner()

    decision = planner.decide(
        "5 + 5 hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.requires_tool

    assert decision.confidence == 0.9

    assert decision.priority == "normal"

    assert decision.risk_level == "low"

    assert decision.strategy == "tool_execution"

    assert decision.explanation is not None

    assert len(decision.plan) == 2

    assert decision.metadata["expression"] == "5+5"


def test_planner_detects_conversation():
    planner = Planner()

    decision = planner.decide(
        "Merhaba AURA",
    )

    assert decision.intent == "conversation"

    assert not decision.requires_tool

    assert decision.confidence == 0.7

    assert decision.priority == "normal"

    assert decision.risk_level == "low"

    assert decision.strategy == "direct_answer"

    assert decision.explanation is not None
