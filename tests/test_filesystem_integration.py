from aura.brain.planner import Planner
from aura.core.tools import ToolRegistry
from aura.tools import FileSystemTool


def test_filesystem_tool_registration():
    tools = ToolRegistry()

    tools.register(
        FileSystemTool(),
    )

    assert tools.has(
        "filesystem",
    )


def test_planner_routes_filesystem_capability():
    tools = ToolRegistry()

    tools.register(
        FileSystemTool(),
    )

    planner = Planner(
        tools=tools,
    )

    decision = planner.decide(
        "workspace içine test.txt oluştur",
    )

    assert decision.intent == "filesystem"

    assert decision.requires_tool

    assert decision.target == "filesystem"

    assert decision.requires_permission
