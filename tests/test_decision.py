from aura.brain.decision import DecisionEngine
from aura.brain.models import Decision


def test_decision_engine_selects_tool_action():
    engine = DecisionEngine()

    decision = Decision(
        intent="calculation",
        requires_tool=True,
        metadata={
            "expression": "2+2",
        },
    )

    action = engine.decide(
        decision,
    )

    assert action.name == "execute_tool"

    assert action.tool_name == "calculator"

    assert action.parameters["expression"] == "2+2"

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

    assert action.tool_name is None

    assert action.parameters == {}

    assert "handled conversationally" in action.reason
