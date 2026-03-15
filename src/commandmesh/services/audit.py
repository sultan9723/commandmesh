from datetime import datetime, UTC


AUDIT_LOGS: list[dict] = []


def record_audit_event(event: dict) -> None:
    audit_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        **event
    }
    AUDIT_LOGS.append(audit_entry)


def get_audit_logs(limit: int = 10) -> list[dict]:
    return AUDIT_LOGS[-limit:][::-1]