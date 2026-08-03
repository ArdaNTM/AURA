from aura.tools.input import InputTool


def test_input_tool_metadata():

    tool = InputTool()

    assert tool.name == "input"

    assert tool.capability == "computer"

    assert tool.requires_permission


def test_input_tool_click():

    tool = InputTool()

    result = tool.execute(
        action="click",
        value="left",
    )

    assert result == "Mouse clicked: left"


def test_input_tool_type():

    tool = InputTool()

    result = tool.execute(
        action="type",
        value="hello",
    )

    assert result == "Typed text: hello"
