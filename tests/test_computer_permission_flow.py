from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.permission import PermissionManager
from aura.brain.permission_gate import PermissionGate
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools import ComputerTool


def test_runtime_creates_computer_permission_request():
    registry = ToolRegistry()

    registry.register(
        ComputerTool(),
    )

    permission_manager = PermissionManager()

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
            permission_manager,
        ),
    )

    state = runtime.run(
        "bilgisayarı kontrol et",
    )

    assert state.completed

    assert state.decision is not None

    assert state.decision.intent == "computer"

    assert state.decision.target == "computer"

    assert state.decision.requires_permission

    assert state.permission_request is not None

    assert state.permission_request.capability == "computer"
