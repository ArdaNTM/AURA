from aura.core.tool_result import ToolResult


def test_tool_result_defaults() -> None:
    result = ToolResult(
        name="calculator",
        output="20",
    )

    assert result.name == "calculator"
    assert result.output == "20"
    assert result.success
    assert result.error is None


def test_tool_result_failure() -> None:
    result = ToolResult(
        name="calculator",
        output="",
        success=False,
        error="Invalid expression.",
    )

    assert result.name == "calculator"
    assert not result.success
    assert result.error == "Invalid expression."
