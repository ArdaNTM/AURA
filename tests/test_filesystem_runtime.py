from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.permission import PermissionManager
from aura.brain.permission_gate import PermissionGate
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools.filesystem import FileSystemTool


def test_runtime_creates_filesystem_permission_request():

    registry = ToolRegistry()

    registry.register(
        FileSystemTool(),
    )

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_gate=PermissionGate(
            PermissionManager(),
        ),
    )

    state = runtime.run(
        "workspace içine test.txt oluştur",
    )

    assert state.completed

    assert state.permission_request is not None

    assert state.permission_request.capability == "filesystem"
