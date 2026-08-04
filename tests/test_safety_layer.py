from aura.brain.audit_log import AuditLog
from aura.brain.rollback import RollbackManager
from aura.brain.safety_policy import SafetyPolicy


def test_high_risk_action_requires_permission():

    policy = SafetyPolicy()

    result = policy.evaluate(
        "delete_file",
    )

    assert result.requires_permission
    assert not result.allowed


def test_audit_records_execution():

    audit = AuditLog()

    audit.record(
        "calculator",
        True,
        True,
    )

    assert len(audit.entries) == 1


def test_rollback_checkpoint():

    rollback = RollbackManager()

    rollback.checkpoint(
        {"state": 1},
    )

    assert rollback.rollback() == {
        "state": 1,
    }
