from src.commandmesh.models.route import RouteRequest, SensitivityLevel
from src.commandmesh.services.audit import AUDIT_LOGS, get_audit_logs
from src.commandmesh.services.routing import process_route_request


def setup_function():
    AUDIT_LOGS.clear()


def test_audit_log_created_for_allowed_request():
    request = RouteRequest(
        prompt="Review quarterly operations report",
        sensitivity=SensitivityLevel.medium,
        user_role="manager"
    )

    process_route_request(request)

    logs = get_audit_logs()
    assert len(logs) == 1
    assert logs[0]["allowed"] is True
    assert logs[0]["status"] == "routed"


def test_audit_log_created_for_blocked_request():
    request = RouteRequest(
        prompt="Access patient medical data",
        sensitivity=SensitivityLevel.high,
        user_role="developer"
    )

    process_route_request(request)

    logs = get_audit_logs()
    assert len(logs) == 1
    assert logs[0]["allowed"] is False
    assert logs[0]["status"] == "blocked"
    assert logs[0]["selected_model"] is None