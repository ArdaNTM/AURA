from aura.brain.decision import DecisionEngine
from aura.brain.models import Decision


def test_decision_engine_selects_tool_action():
    engine = DecisionEngine()

    decision = Decision(
        intent="calculation",
        requires_tool=True,
    )

    action = engine.decide(
        decision,
    )

    assert action.name == "execute_tool"

    assert "requires a tool" in action.reason


def test_decision_engine_selects_response_action():
    engine = DecisionEngine()

    decision = Decision(
        intent="conversation",
        requires_tool=False,
    )

    action = engine.decide(
        decision,
    )

    assert action.name == "generate_response"

    assert "handled conversationally" in action.reason
