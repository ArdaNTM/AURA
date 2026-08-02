from aura.brain.models import Decision
from aura.brain.permission_runtime import PermissionRuntime


def test_permission_runtime_blocks_unknown_permission():

    runtime = PermissionRuntime()

    decision = Decision(
        intent="computer",
        confidence=0.9,
        requires_tool=True,
        requires_permission=True,
        target="computer",
        priority="normal",
        risk_level="high",
        strategy="tool_execution",
        explanation="Computer access",
        metadata={
            "capability": "computer",
        },
    )

    result = runtime.check(
        decision,
    )

    assert result is False
    assert runtime.service.pending is not None
