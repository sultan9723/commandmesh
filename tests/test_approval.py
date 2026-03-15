import pytest
from src.commandmesh.models.route import RouteRequest, SensitivityLevel
from src.commandmesh.services.routing import process_route_request
from src.commandmesh.services.approval import get_pending_approvals
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

def test_pending_approval_request_stored():
    request = RouteRequest(
        prompt="Access sensitive financial data",
        sensitivity=SensitivityLevel.high,
        user_role="developer"
    )

    process_route_request(request)

    pending = get_pending_approvals()
    assert len(pending) == 1
    assert pending[0]["prompt"] == "Access sensitive financial data"
    assert pending[0]["user_role"] == "developer"
    assert pending[0]["status"] == "pending"

def test_allowed_request_not_stored_in_approvals():
    request = RouteRequest(
        prompt="Normal query",
        sensitivity=SensitivityLevel.low,
        user_role="developer"
    )

    process_route_request(request)

    pending = get_pending_approvals()
    assert len(pending) == 0
