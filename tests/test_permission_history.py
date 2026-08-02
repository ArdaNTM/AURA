from aura.brain.permission_request import PermissionRequest
from aura.brain.permission_service import PermissionService


def test_permission_history_records_approval():

    service = PermissionService()

    request = PermissionRequest(
        capability="filesystem",
        reason="Create file",
        risk_level="medium",
    )

    service.create(
        request,
    )

    service.approve()

    assert (
        len(
            service.history,
        )
        == 1
    )

    entry = service.history[0]

    assert entry.capability == "filesystem"

    assert entry.approved


def test_permission_history_records_denial():

    service = PermissionService()

    request = PermissionRequest(
        capability="computer",
        reason="Control computer",
        risk_level="high",
    )

    service.create(
        request,
    )

    service.deny()

    assert (
        len(
            service.history,
        )
        == 1
    )

    assert not service.history[0].approved
