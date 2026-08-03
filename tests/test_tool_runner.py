from aura.ai.tool_runner import ToolRunner
from aura.core.tools import Tool, ToolRegistry


class EchoTool(Tool):
    @property
    def name(self) -> str:
        return "echo"

    def execute(self, value: str) -> str:
        return value


def test_tool_runner_executes_tool() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())

    runner = ToolRunner(registry)

    result = runner.run(
        "echo",
        "hello",
    )

    assert result.success
    assert result.output == "hello"


def test_tool_runner_returns_failure() -> None:
    registry = ToolRegistry()

    runner = ToolRunner(registry)

    result = runner.run(
        "missing",
    )

    assert not result.success

    assert result.name == "missing"

    assert "Unknown tool" in result.error


def test_tool_runner_records_reliability():
    registry = ToolRegistry()
    registry.register(EchoTool())

    runner = ToolRunner(
        registry,
    )

    result = runner.run(
        "echo",
        "hello",
    )

    stats = runner.reliability_tracker.get(
        "echo",
    )

    assert result.success
    assert stats.runs == 1
    assert stats.successes == 1


def test_tool_runner_records_failed_reliability():
    registry = ToolRegistry()

    runner = ToolRunner(
        registry,
    )

    result = runner.run(
        "missing",
    )

    stats = runner.reliability_tracker.get(
        "missing",
    )

    assert not result.success
    assert stats.runs == 1
    assert stats.failures == 1
