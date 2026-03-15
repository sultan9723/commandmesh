from src.commandmesh.models.db import AuditLog
from src.commandmesh.database import SessionLocal

def record_audit_event(event: dict) -> None:
    db = SessionLocal()
    try:
        audit_entry = AuditLog(
            prompt=event.get("prompt"),
            user_role=event.get("user_role"),
            sensitivity=event.get("sensitivity"),
            selected_model=event.get("selected_model"),
            reason=event.get("reason"),
            status=event.get("status"),
            allowed=event.get("allowed")
        )
        db.add(audit_entry)
        db.commit()
    finally:
        db.close()

def get_audit_logs(limit: int = 10) -> list[dict]:
    db = SessionLocal()
    try:
        logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": log.id,
                "timestamp": log.timestamp.isoformat(),
                "prompt": log.prompt,
                "user_role": log.user_role,
                "sensitivity": log.sensitivity,
                "selected_model": log.selected_model,
                "reason": log.reason,
                "status": log.status,
                "allowed": log.allowed
            }
            for log in logs
        ]
    finally:
        db.close()
