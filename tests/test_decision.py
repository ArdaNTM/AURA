from aura.brain.decision import DecisionEngine
from aura.brain.models import Decision


def test_decision_engine_selects_tool_action():
    engine = DecisionEngine()

    decision = Decision(
        intent="calculation",
        requires_tool=True,
        target="calculator",
        strategy="tool_execution",
        confidence=0.9,
        priority="normal",
        risk_level="low",
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

    assert action.metadata["intent"] == "calculation"

    assert action.metadata["strategy"] == "tool_execution"

    assert "requires a tool" in action.reason


def test_decision_engine_selects_response_action():
    engine = DecisionEngine()

    decision = Decision(
        intent="conversation",
        requires_tool=False,
        strategy="direct_answer",
        confidence=0.7,
        priority="normal",
        risk_level="low",
    )

    action = engine.decide(
        decision,
    )

    assert action.name == "generate_response"

    assert action.tool_name is None

    assert action.parameters == {}

    assert action.metadata["intent"] == "conversation"

    assert action.metadata["strategy"] == "direct_answer"

    assert "handled conversationally" in action.reason


def test_decision_engine_requests_confirmation():
    engine = DecisionEngine()

    decision = Decision(
        intent="delete_file",
        strategy="ask_confirmation",
        risk_level="high",
    )

    action = engine.decide(
        decision,
    )

    assert action.name == "request_confirmation"

    assert action.metadata["risk_level"] == "high"

    assert "requires user confirmation" in action.reason
