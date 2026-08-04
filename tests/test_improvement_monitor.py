from aura.brain.improvement_monitor import ImprovementMonitor


def test_improvement_accepts_better_result():

    monitor = ImprovementMonitor()

    result = monitor.record(
        "tool_strategy",
        0.5,
        0.8,
    )

    assert result is True


def test_improvement_blocks_regression():

    monitor = ImprovementMonitor()

    result = monitor.record(
        "bad_strategy",
        0.8,
        0.5,
    )

    assert result is False
