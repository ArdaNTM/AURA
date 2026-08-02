from aura.tools import ComputerTool


def test_computer_tool_metadata():
    tool = ComputerTool()

    assert tool.name == "computer"

    assert tool.capability == "computer"

    assert tool.risk_level == "high"

    assert tool.requires_permission


def test_computer_tool_execution():
    tool = ComputerTool()

    result = tool.execute(
        "open_browser",
    )

    assert result == ("Computer action executed: open_browser")


def test_computer_tool_schema_contains_permission():
    tool = ComputerTool()

    schema = tool.schema()

    assert schema["name"] == "computer"

    assert schema["capability"] == "computer"

    assert schema["requires_permission"]
