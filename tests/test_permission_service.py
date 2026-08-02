from aura.brain.permission_request import PermissionRequest
from aura.brain.permission_service import PermissionService


def test_permission_service_approves_request():

    service = PermissionService()

    request = PermissionRequest(
        capability="filesystem",
        reason="Create file",
        risk_level="medium",
    )

    service.create(
        request,
    )

    assert service.pending is request

    assert service.approve()

    assert service.pending.approved


def test_permission_service_handles_empty_request():

    service = PermissionService()

    assert not service.approve()
