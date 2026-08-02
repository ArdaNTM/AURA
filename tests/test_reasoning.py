from aura.brain.reasoning import ReasoningResult


def test_reasoning_result_defaults():
    result = ReasoningResult(
        intent="calculation",
    )

    assert result.intent == "calculation"

    assert result.goal == ""

    assert result.confidence == 0.0

    assert result.risk_level == "low"
