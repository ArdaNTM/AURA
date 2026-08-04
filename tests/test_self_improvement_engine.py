from aura.brain.self_improvement import (
    SelfImprovementEngine,
)


def test_failed_task_creates_improvement():

    engine = SelfImprovementEngine()

    result = engine.analyze(
        success=False,
        strategy="tool_execution",
        confidence=0.8,
        reflection="tool failed",
    )

    assert result.success is False

    assert result.strategy_change == "adaptive_retry"


def test_success_updates_strategy():

    engine = SelfImprovementEngine()

    result = engine.analyze(
        success=True,
        strategy="safe_tool_execution",
        confidence=0.9,
    )

    assert result.strategy_change == ("safe_tool_execution")

    assert len(result.suggestions) > 0
