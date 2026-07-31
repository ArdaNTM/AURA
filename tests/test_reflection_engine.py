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
