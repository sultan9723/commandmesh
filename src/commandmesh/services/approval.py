from src.commandmesh.models.db import ApprovalRequest
from src.commandmesh.database import SessionLocal

def record_approval_request(request_data: dict) -> None:
    db = SessionLocal()
    try:
        approval_entry = ApprovalRequest(
            prompt=request_data.get("prompt"),
            user_role=request_data.get("user_role"),
            sensitivity=request_data.get("sensitivity"),
            status="pending"
        )
        db.add(approval_entry)
        db.commit()
    finally:
        db.close()

def get_pending_approvals() -> list[dict]:
    db = SessionLocal()
    try:
        approvals = db.query(ApprovalRequest).filter(ApprovalRequest.status == "pending").all()
        return [
            {
                "id": app.id,
                "timestamp": app.timestamp.isoformat(),
                "prompt": app.prompt,
                "user_role": app.user_role,
                "sensitivity": app.sensitivity,
                "status": app.status
            }
            for app in approvals
        ]
    finally:
        db.close()
