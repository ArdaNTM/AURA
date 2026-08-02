from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.permission import PermissionManager
from aura.brain.permission_gate import PermissionGate
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry


def test_runtime_creates_permission_request_without_permission():
    registry = ToolRegistry()

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

    assert state.permission_request is not None

    assert state.permission_request.capability == "computer"

    assert not state.permission_request.approved


def test_runtime_permission_request_contains_reason_and_risk():
    registry = ToolRegistry()

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

    assert state.permission_request is not None

    assert state.permission_request.reason == "computer capability requires permission."

    assert state.permission_request.risk_level == "high"
