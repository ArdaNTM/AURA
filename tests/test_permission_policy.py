from aura.brain.permission_policy import PermissionPolicy


def test_policy_allows_low_risk_capability():
    policy = PermissionPolicy()

    result = policy.evaluate(
        capability="calculation",
        risk_level="low",
        confidence=0.9,
        requires_permission=False,
    )

    assert result.action == "allow"


def test_policy_requests_confirmation_for_computer():
    policy = PermissionPolicy()

    result = policy.evaluate(
        capability="computer",
        risk_level="high",
        confidence=0.9,
        requires_permission=True,
    )

    assert result.action == "ask"
