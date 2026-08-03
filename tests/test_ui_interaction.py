from aura.tools.ui_interaction import UIInteractionTool


def test_ui_interaction_metadata():
    tool = UIInteractionTool()

    assert tool.name == "ui_interaction"
    assert tool.capability == "computer"
    assert tool.requires_permission


def test_ui_click():

    tool = UIInteractionTool()

    result = tool.execute(
        action="click",
        x=100,
        y=200,
    )

    assert result.success
    assert "100" in result.output


def test_ui_type():

    tool = UIInteractionTool()

    result = tool.execute(
        action="type",
        text="hello",
    )

    assert "hello" in result.output
