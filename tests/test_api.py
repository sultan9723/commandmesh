import pytest
from fastapi.testclient import TestClient
from src.commandmesh.main import app
from src.commandmesh.database import engine, Base, SessionLocal
from src.commandmesh.models.db import AuditLog, ApprovalRequest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(AuditLog).delete()
    db.query(ApprovalRequest).delete()
    db.commit()
    db.close()
    yield

def test_api_route_and_audit_logs():
    # Submit a request
    response = client.post("/route", json={
        "prompt": "Test audit log",
        "sensitivity": "low",
        "user_role": "developer"
    })
    assert response.status_code == 200
    
    # Check audit logs
    response = client.get("/audit/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["logs"][0]["prompt"] == "Test audit log"

def test_api_pending_approvals():
    # Submit a high-sensitivity request from developer
    response = client.post("/route", json={
        "prompt": "Secret data",
        "sensitivity": "high",
        "user_role": "developer"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    
    # Check pending approvals
    response = client.get("/approvals/pending")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["approvals"][0]["prompt"] == "Secret data"
