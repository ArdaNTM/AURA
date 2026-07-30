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