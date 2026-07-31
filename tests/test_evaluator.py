from aura.brain.evaluator import Evaluator
from aura.brain.observation import Observation


def test_evaluator_marks_successful_observation():
    evaluator = Evaluator()

    observation = Observation(
        source="calculator",
        output="4",
    )

    result = evaluator.evaluate(
        observation,
    )

    assert result.score == 1.0

    assert result.feedback == ("Observation completed successfully.")

    assert not result.retry_needed


def test_evaluator_marks_failed_observation():
    evaluator = Evaluator()

    observation = Observation(
        source="calculator",
        output="",
        success=False,
    )

    result = evaluator.evaluate(
        observation,
    )

    assert result.score == 0.0

    assert result.feedback == ("Observation failed during execution.")

    assert result.retry_needed


def test_evaluator_handles_empty_output():
    evaluator = Evaluator()

    observation = Observation(
        source="calculator",
        output="",
    )

    result = evaluator.evaluate(
        observation,
    )

    assert result.score == 0.5

    assert result.feedback == ("Execution succeeded but produced no output.")

    assert not result.retry_needed
