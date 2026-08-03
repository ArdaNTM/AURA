from aura.ai.tool_runner import ToolRunner
from aura.brain.tool_reliability import ToolReliabilityTracker
from aura.core.tools import ToolRegistry
from aura.tools.calculator import CalculatorTool


def test_tool_reliability_tracks_success():

    registry = ToolRegistry()

    registry.register(
        CalculatorTool(),
    )

    tracker = ToolReliabilityTracker()

    runner = ToolRunner(
        registry,
        tracker,
    )

    result = runner.run(
        "calculator",
        expression="2+2",
    )

    assert result.success

    stats = tracker.get(
        "calculator",
    )

    assert stats.runs == 1
    assert stats.successes == 1
    assert stats.failures == 0
    assert stats.success_rate == 1.0
