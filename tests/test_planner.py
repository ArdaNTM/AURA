from aura.brain.planner import Planner


def test_planner_detects_calculation():

    planner = Planner()

    decision = planner.decide(
        "5 + 5 hesapla",
    )

    assert decision.intent == "calculation"

    assert decision.requires_tool

    assert len(decision.plan) == 2


def test_planner_detects_conversation():

    planner = Planner()

    decision = planner.decide(
        "Merhaba AURA",
    )

    assert decision.intent == "conversation"

    assert not decision.requires_tool
