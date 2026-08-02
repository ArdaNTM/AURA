from aura.ai.tool_runner import ToolRunner
from aura.brain.brain import Brain
from aura.brain.executor import PlanExecutor
from aura.brain.permission_service import PermissionService
from aura.brain.runtime import AgentRuntime
from aura.core.tools import ToolRegistry
from aura.tools.filesystem import FileSystemTool


def test_runtime_stores_pending_permission_request():
    registry = ToolRegistry()

    registry.register(
        FileSystemTool(),
    )

    permission_service = PermissionService()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_service=permission_service,
    )

    state = runtime.run(
        "workspace içine test.txt oluştur",
    )

    assert state.permission_request is not None

    assert permission_service.pending is not None

    assert permission_service.pending.capability == "filesystem"


def test_runtime_stores_pending_decision():

    registry = ToolRegistry()

    registry.register(
        FileSystemTool(),
    )

    permission_service = PermissionService()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_service=permission_service,
    )

    state = runtime.run(
        "workspace içine test.txt oluştur",
    )

    assert state.decision is not None

    assert permission_service.decision is not None

    assert permission_service.decision.intent == "filesystem"

def test_runtime_resume_executes_approved_permission():

    registry = ToolRegistry()

    registry.register(
        FileSystemTool(),
    )

    permission_service = PermissionService()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_service=permission_service,
    )

    state = runtime.run(
        "workspace içine test.txt oluştur",
    )

    assert state.permission_request is not None

    permission_service.approve()

    resumed = runtime.resume()

    assert resumed.completed

    assert resumed.decision is not None

    assert resumed.decision.intent == "filesystem"

def test_resume_executes_with_observations():

    registry = ToolRegistry()

    registry.register(
        FileSystemTool(),
    )

    permission_service = PermissionService()

    runtime = AgentRuntime(
        Brain(
            tools=registry,
        ),
        PlanExecutor(
            ToolRunner(
                registry,
            ),
        ),
        permission_service=permission_service,
    )

    state = runtime.run(
        "workspace içine test.txt oluştur",
    )

    permission_service.approve()

    resumed = runtime.resume()

    assert resumed.completed

    assert len(
        resumed.observations,
    ) > 0    