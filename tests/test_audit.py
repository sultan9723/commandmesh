import pytest
from src.commandmesh.models.route import RouteRequest, SensitivityLevel
from src.commandmesh.services.audit import get_audit_logs
from src.commandmesh.services.routing import process_route_request
from src.commandmesh.database import engine, Base, SessionLocal
from src.commandmesh.models.db import AuditLog, ApprovalRequest

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(AuditLog).delete()
    db.query(ApprovalRequest).delete()
    db.commit()
    db.close()
    yield

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


def test_audit_log_created_for_pending_request():
    request = RouteRequest(
        prompt="Access patient medical data",
        sensitivity=SensitivityLevel.high,
        user_role="developer"
    )

    process_route_request(request)

    logs = get_audit_logs()
    assert len(logs) == 1
    assert logs[0]["allowed"] is False
    assert logs[0]["status"] == "pending"
    assert logs[0]["selected_model"] is None
