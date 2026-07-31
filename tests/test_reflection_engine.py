from aura.brain.observation import Observation
from aura.brain.reflection_engine import ReflectionEngine


def test_reflection_engine_marks_successful_execution():
    engine = ReflectionEngine()

    observation = Observation(
        source="calculator",
        output="4",
        score=1.0,
        success=True,
    )

    reflection = engine.reflect(
        observation,
    )

    assert reflection.success

    assert reflection.summary == "Execution completed successfully."

    assert reflection.metadata["retry_needed"] is False


def test_reflection_engine_detects_improvement_area():
    engine = ReflectionEngine()

    observation = Observation(
        source="calculator",
        output="",
        score=0.5,
        success=True,
    )

    reflection = engine.reflect(
        observation,
    )

    assert reflection.success

    assert reflection.summary == "Execution completed with room for improvement."

    assert (
        len(
            reflection.improvements,
        )
        == 1
    )


def test_reflection_engine_handles_failure():
    engine = ReflectionEngine()

    observation = Observation(
        source="calculator",
        output="error",
        score=0.0,
        success=False,
    )

    reflection = engine.reflect(
        observation,
    )

    assert not reflection.success

    assert reflection.summary == "Execution failed."

    assert reflection.metadata["retry_needed"] is True


def test_reflection_engine_selects_retry_strategy_after_tool_failure():
    from aura.brain.models import Decision

    engine = ReflectionEngine()

    observation = Observation(
        source="calculator",
        output="error",
        score=0.0,
        success=False,
    )

    decision = Decision(
        intent="calculation",
        strategy="tool_execution",
    )

    reflection = engine.reflect(
        observation,
        decision,
    )

    assert not reflection.success

    assert reflection.retry_needed

    assert reflection.retry_strategy == "safe_tool_execution"

    assert reflection.metadata["retry_strategy"] == "safe_tool_execution"


def test_reflection_engine_switches_strategy_after_safe_failure():
    from aura.brain.models import Decision

    engine = ReflectionEngine()

    observation = Observation(
        source="calculator",
        output="error",
        score=0.0,
        success=False,
    )

    decision = Decision(
        intent="calculation",
        strategy="safe_tool_execution",
    )

    reflection = engine.reflect(
        observation,
        decision,
    )

    assert reflection.retry_needed

    assert reflection.retry_strategy == "tool_execution"
