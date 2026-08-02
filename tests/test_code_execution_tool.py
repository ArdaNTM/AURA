from aura.tools.code_execution import CodeExecutionTool


def test_code_execution_runs_python():

    tool = CodeExecutionTool()

    result = tool.execute(
        "print('AURA')",
    )

    assert result == "AURA"


def test_code_execution_blocks_system_access():

    tool = CodeExecutionTool()

    try:
        tool.execute(
            "import os\nos.system('dir')",
        )

        assert False

    except PermissionError:
        assert True
