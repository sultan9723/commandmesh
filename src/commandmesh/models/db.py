from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime, UTC
from src.commandmesh.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
    prompt = Column(Text)
    user_role = Column(String)
    sensitivity = Column(String)
    selected_model = Column(String, nullable=True)
    reason = Column(Text)
    status = Column(String)
    allowed = Column(Boolean)

class ApprovalRequest(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))
    prompt = Column(Text)
    user_role = Column(String)
    sensitivity = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
