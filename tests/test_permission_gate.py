from aura.brain.models import Decision
from aura.brain.permission_gate import PermissionGate


def test_permission_gate_blocks_policy_confirmation():
    gate = PermissionGate()

    decision = Decision(
        intent="computer",
        requires_permission=True,
        risk_level="high",
        confidence=0.9,
        metadata={
            "capability": "computer",
        },
    )

    assert not gate.can_execute(
        decision,
    )
