from aura.tools.terminal import TerminalTool


def test_terminal_executes_command():

    tool = TerminalTool()

    result = tool.execute(
        "echo AURA",
    )

    assert "AURA" in result


def test_terminal_blocks_dangerous_command():

    tool = TerminalTool()

    try:
        tool.execute(
            "shutdown",
        )

        assert False

    except PermissionError:
        assert True
