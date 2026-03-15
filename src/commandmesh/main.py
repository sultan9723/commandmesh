from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session

from src.commandmesh.models.route import RouteRequest, RouteResponse
from src.commandmesh.services.audit import get_audit_logs
from src.commandmesh.services.routing import process_route_request
from src.commandmesh.services.approval import get_pending_approvals
from src.commandmesh.database import engine, Base, get_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CommandMesh")


@app.get("/")
def root():
    return {
        "message": "CommandMesh API is running",
        "docs": "/docs",
        "health": "/health",
        "audit_logs": "/audit/logs",
        "pending_approvals": "/approvals/pending"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "CommandMesh"
    }


@app.get("/audit/logs")
def read_audit_logs(limit: int = Query(default=10, ge=1, le=100)):
    logs = get_audit_logs(limit)
    return {
        "count": len(logs),
        "logs": logs
    }


@app.get("/approvals/pending")
def read_pending_approvals():
    approvals = get_pending_approvals()
    return {
        "count": len(approvals),
        "approvals": approvals
    }


@app.post("/route", response_model=RouteResponse)
def route_request(request: RouteRequest):
    result = process_route_request(request)
    return RouteResponse(**result)
