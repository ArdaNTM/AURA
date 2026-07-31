from aura.brain.observation import Observation
from aura.brain.performance_engine import PerformanceEngine


def test_performance_engine_calculates_success_metrics():
    engine = PerformanceEngine()

    observations = [
        Observation(
            source="calculator",
            output="4",
            success=True,
            score=1.0,
        ),
        Observation(
            source="calculator",
            output="error",
            success=False,
            score=0.0,
            retry_needed=True,
        ),
    ]

    report = engine.evaluate(
        observations,
    )

    assert report.success_rate == 0.5

    assert report.average_score == 0.5

    assert report.retry_rate == 0.5

    assert report.performance_score == 0.5


def test_performance_engine_handles_perfect_execution():
    engine = PerformanceEngine()

    observations = [
        Observation(
            source="calculator",
            output="4",
            success=True,
            score=1.0,
        ),
        Observation(
            source="calculator",
            output="8",
            success=True,
            score=1.0,
        ),
    ]

    report = engine.evaluate(
        observations,
    )

    assert report.success_rate == 1.0

    assert report.average_score == 1.0

    assert report.retry_rate == 0.0

    assert report.performance_score == 1.0


def test_performance_engine_handles_empty_history():
    engine = PerformanceEngine()

    report = engine.evaluate(
        [],
    )

    assert report.success_rate == 0.0

    assert report.average_score == 0.0

    assert report.retry_rate == 0.0

    assert report.performance_score == 0.0
